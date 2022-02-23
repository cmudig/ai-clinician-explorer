from flask import Blueprint, request, abort, jsonify
from firebase_admin import credentials, firestore, initialize_app
from google_auth_oauthlib import flow
from google.cloud.exceptions import NotFound
from google.cloud import bigquery
from ai_clinician.preprocessing.columns import *
from ai_clinician.modeling.columns import *

patient_blueprint = Blueprint('patient', __name__, url_prefix='/api/patient')

# Initialize Firestore DB - we retrieve detailed patient data from there
cred = credentials.Certificate('firestore_key.json')
default_app = initialize_app(cred)
db = firestore.client()
mimic_data = db.collection('MIMICIV_provenance')

# Also initialize BigQuery client - we use this for fast search, filtering, and sorting
project = "ai-clinician"
bq_client = bigquery.Client(project=project)
default_dataset = "mimiciv_220217_best"

METADATA_FIELDS = [
    C_ICUSTAYID,
    'num_timesteps',
    C_GENDER,
    C_AGE,
    C_ELIXHAUSER,
    C_MAX_SIRS,
    C_MAX_SOFA,
    C_MAX_DOSE_VASO,
    C_MORTA_90,
    C_DIED_IN_HOSP,
    C_RE_ADMISSION,
    C_HEIGHT,
]

# If these are used, the query should not limit to bloc == 0
TIMESTEP_RELEVANT_FIELDS = [
    'model_action',
    'bloc',
    'timestep',
    'physician_action',
    'state'
]

def match_sort_criterion_type(sort_criterion, val):
    """Converts the given value to the appropriate type for the given sort criterion."""
    if sort_criterion in ("age",
                          "delay_end_of_record_and_discharge_or_death",
                          "elixhauser",
                          "gender",
                          "icustayid",
                          "num_timesteps",
                          "max_SOFA",
                          "max_SIRS",
                          "max_dose_vaso"):
        return int(val)
    elif sort_criterion in ("died_in_hosp", "died_within_48h_of_out_time", "morta_90", "re_admission"):
        return bool(val)
    return val

def search_patients(filters, sort_field, ascending=True, size=10, offset=0, dataset=None):
    """
    Performs a search in the BigQuery table using the given filters, sort
    criteria, and size/offset.
    """
    dataset = dataset or default_dataset
    timestep_relevant = any(any(f in statement for f in TIMESTEP_RELEVANT_FIELDS)
                            for statement in filters)
    if timestep_relevant:
        # We need to do a group by here because the bloc may not necessarily be 1
        fields = ", ".join([f"MAX({f}) as {f}" for f in METADATA_FIELDS])
        query = f"SELECT {fields} FROM `{project}.{dataset}.stays` "
        query += "WHERE " + filters.join(' AND ') + " "
        query += "GROUP BY icustayid"
    else:
        query = f"SELECT {', '.join(METADATA_FIELDS)} FROM `{project}.{dataset}.stays` "
        if filters:
            query += "WHERE " + " AND ".join(filters) + " "
            query += "AND bloc = 1 "
        else:
            query += "WHERE bloc = 1 "

    if sort_field is not None and sort_field != "icustayid":
        query += f"ORDER BY {sort_field} "
        query += "ASC " if ascending else "DESC "
        query += ", icustayid ASC "
    else:
        query += "ORDER BY icustayid "
        query += "ASC " if ascending else "DESC "
    query += f"LIMIT {size} "
    if offset:
        query += f"OFFSET {offset} "
    print(query)
    query_result = bq_client.query(query)
    return [dict(row) for row in query_result]


@patient_blueprint.route('/', methods=['GET'], defaults={'patient_id': None})
@patient_blueprint.route('/<patient_id>')
def read(patient_id):
    """
    read() : Fetches documents from Firestore collection as JSON.
    
    If this is called as /patient with no patient ID, it will retrieve a set of
    records from the database. It will accept the following query parameters:
    * sort: a field by which to sort the results (default is 'icustayid').
    * ascending: 1 or 0 indicating whether the results should be sorted in
        ascending or descending order (default is 1 = ascending order)
    * size: number of results to return (default is 10)
    * offset: number of results to SKIP before returning. This enables you to
        create multiple pages of results.
    * model: ID of the model to retrieve results from.
        
    If this is called as /patient/<patient_id> with a string patient ICU stay
    ID, it will return all information about the patient with the given ID.
    """
    if patient_id is None:
        # Get query arguments
        args = request.args.to_dict()
        sort_criterion = args.get("sort", "icustayid")
        try:
            ascending = int(args.get("ascending", 1))
        except ValueError:
            return "Invalid value for ascending query parameter", 400

        try:
            size = int(args.get("size", 10))
        except ValueError:
            return "Invalid value for size query parameter", 400

        try:
            offset = int(args.get("offset", 0))
        except ValueError:
            return "Invalid value for offset query parameter", 400
        
        model = args.get("model", None)
        print(sort_criterion, ascending, offset, size)
        
        try:                
            docs = search_patients([], sort_criterion, ascending=ascending, size=size, offset=offset, dataset=model)
        except Exception as e:
            print(e)
            return "An error occurred returning the results.", 400
        return jsonify({'results': docs})
    else:
        doc_ref = mimic_data.document(patient_id)
        doc = doc_ref.get()
        if doc.exists:
            # Retrieve timesteps
            data = doc.to_dict()
            timesteps = [t.to_dict() for t in doc_ref.collection('timesteps').order_by('bloc').stream()]
            data['timesteps'] = timesteps
            return jsonify({
                'result': data
            })
        else:
            return "Patient does not exist", 404