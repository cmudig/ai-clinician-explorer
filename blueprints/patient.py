from flask import Blueprint, request, abort, jsonify
from google_auth_oauthlib import flow
from google.cloud.exceptions import NotFound
from google.cloud import bigquery
from ai_clinician.preprocessing.columns import *
from ai_clinician.modeling.columns import *
from .firestore import db

from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    'firestore_key.json', scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

patient_blueprint = Blueprint('patient', __name__, url_prefix='/api/patient')

# Initialize Firestore DB - we retrieve detailed patient data from there
mimic_data = db.collection('MIMICIV_provenance')

# Also initialize BigQuery client - we use this for fast search, filtering, and sorting
project = "ai-clinician"
bq_client = bigquery.Client(credentials=credentials, project=project)
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

def build_filter_query(filters, table_name, dataset=None):
    """
    Builds a SQL select command that filters the given table name, such as
    antibiotics, microbio, or comorbidities.
    """
    dataset = dataset or default_dataset
    query = f"SELECT {C_ICUSTAYID} FROM `{project}.{dataset}.{table_name}` "
    if filters:
        query += f"WHERE {' AND '.join(filters)} "
    return query

def search_patients(filters, sort_field, ascending=True, size=10, offset=0, dataset=None, joins=None):
    """
    Performs a search in the BigQuery table using the given filters, sort
    criteria, and size/offset.
    
    If joins is not None, it should be a list of strings defining SQL select
    commands that will be used as part of inner joins on the main stays table.
    For example, ["SELECT <fields> FROM <table> WHERE <filters>", ...]
    """
    dataset = dataset or default_dataset
    if filters:
        timestep_relevant = any(any(f in statement for f in TIMESTEP_RELEVANT_FIELDS)
                                for statement in filters)
    else:
        timestep_relevant = False
    if timestep_relevant:
        # We need to do a group by here because the bloc may not necessarily be 1
        fields = ", ".join([f"MAX({f}) as {f}" if f != C_ICUSTAYID else f for f in METADATA_FIELDS])
        query = f"SELECT {fields}, MIN({C_BLOC}) as {C_BLOC} FROM `{project}.{dataset}.stays` "
        if filters:
            query += f"WHERE {' AND '.join(filters)} "
        query += "GROUP BY icustayid "
    else:
        query = f"SELECT {', '.join(METADATA_FIELDS)} FROM `{project}.{dataset}.stays` "
        if filters:
            query += f"WHERE {' AND '.join(filters)} "
            query += "AND bloc = 1 "
        else:
            query += "WHERE bloc = 1 "

    field_prefix = ""
    if joins:
        # Put all the join tables and the stays table under a WITH clause
        join_statements = ', '.join(f"join{i} AS ( {stmt} )" for i, stmt in enumerate(joins))
        query = f"WITH {join_statements}, base AS ( {query} ) SELECT DISTINCT base.* FROM base "
        for i in range(len(joins)):
            query += f"INNER JOIN join{i} ON base.icustayid = join{i}.icustayid "
        field_prefix = "base."
        
    if sort_field is not None and sort_field != "icustayid":
        query += f"ORDER BY {field_prefix}{sort_field} "
        query += "ASC " if ascending else "DESC "
        query += ", icustayid ASC "
    else:
        query += f"ORDER BY {field_prefix}icustayid "
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
    * filters: a string containing filters to apply to the
        returned results. The string should be semicolon-separated, and each
        component should be a valid SQL 'where' clause. For example, the 
        query string "max_SOFA >= 5;max_SOFA <= 10" would return results with
        a max SOFA score between 5 and 10. When encoded using URL percent-
        escaping, this value would look like this: "max_SOFA+%3E%3D+5%3Bmax_SOFA+%3C%3D+10"
        
        Available fields for filters are:
        * "icustayid" - the ID number of the ICU stay
        * "gender" - the gender of the patient (0 = male, 1 = female)
        * "age" - the patient age in years
        * "elixhauser" - the Elixhauser comorbidity score of the patient
        * "re_admission" - whether the patient has been readmitted to the ICU in
            this hospital stay
        * "died_in_hosp" - whether the patient died in the hospital (the primary
            outcome)
        * "died_within_48h_of_out_time" - whether the patient died within 48
            hours of being discharged from the ICU
        * "morta_90" - 90-day mortality (not guaranteed to be accurate)
        
        Some examples of how filters might look:
        * "state = 10"
        * "physician_action in (0, 1, 2, 3, 4)"
        * "model_action = 20"
        * "died_in_hosp = 1"
    * abx_filters: a string containing filters to apply to the antibiotics
        prescribed to each patient, for which matching ICU stay IDs should be
        returned (same format as filters). Available fields for antibiotics are: 
        * "drug" - name of the drug. See ai_clinician/data_extraction/conversions/
            abx_drug_codes.csv for the available drug names.
        * "gsn" - drug Generic Sequence Number
        * "ndc" - drug National Drug Code
        * "dose_val" - quantitative dose of the drug
        * "dose_unit" - unit of measurement of the dose ("mg", "g", "gm", "TAB",
            "mL", etc.)
        * "route" - way the drug is delivered ("IV", "PO/NG", "PO", "NG", "ORAL",
            etc.)
    * mb_filters: a string containing filters to apply to the microbio cultures
        requested for each patient, for which matching ICU stay IDs should be
        returned (same format as filters). Available fields for microbio are: 
        * "spec_itemid" - the item ID number of the specimen. See ai_clinician/
            data_extraction/conversions/microbio_spec_itemids.csv for the
            mapping of specimen types to item IDs.
        * "org_itemid" - the item ID number of the organism identified. See
            ai_clinician/data_extraction/conversions/microbio_org_itemids.csv 
            for the mapping of specimen types to item IDs.
        * "ab_itemid" - the item ID number of the antibiotic tested. See
            ai_clinician/data_extraction/conversions/microbio_ab_itemids.csv for
            the mapping of antibiotics to item IDs.
        * "interpretation" - the interpretation of the antibiotic sensitivity
            test ("R" = resistant, "S" = sensitive, "I" = intermediate)
            
        For example, to find patients that tested positive for "STAPH AUREUS
        COAG +" with sensitivity to Oxacillin, one could use the following
        mb_filters: "org_itemid = 80023;ab_itemid = 90016;interpretation = S"
    * cm_filters: a string containing filters to apply to the comorbidities
        each patient has, for which matching ICU stay IDs should be
        returned (same format as filters). Available fields for comorbidities
        are (all are integers that can be either 1 or 0):
        * congestive_heart_failure
        * cardiac_arrhythmias
        * valvular_disease
        * pulmonary_circulation
        * peripheral_vascular
        * hypertension
        * paralysis
        * other_neurological
        * chronic_pulmonary
        * diabetes_uncomplicated
        * diabetes_complicated
        * hypothyroidism
        * renal_failure
        * liver_disease
        * peptic_ulcer
        * aids
        * lymphoma
        * metastatic_cancer
        * solid_tumor
        * rheumatoid_arthritis
        * coagulopathy
        * obesity
        * weight_loss
        * fluid_electrolyte
        * blood_loss_anemia
        * deficiency_anemias
        * alcohol_abuse
        * drug_abuse
        * psychoses
        * depression
    
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
            size = int(args.get("size", 20))
        except ValueError:
            return "Invalid value for size query parameter", 400

        try:
            offset = int(args.get("offset", 0))
        except ValueError:
            return "Invalid value for offset query parameter", 400
        
        model = args.get("model", None)
        
        filters = args.get("filters", None)

        additional_filters = [build_filter_query(args.get(filter_key).split(';'), table_name, dataset=model)
                              for filter_key, table_name in [
                                  ("abx_filters", "abx"),
                                  ("mb_filters", "microbio"),
                                  ("cm_filters", "comorbidities")
                              ] if args.get(filter_key, None)]
        
        try:                
            docs = search_patients(filters.split(';') if filters else None,
                                   sort_criterion, 
                                   ascending=ascending, 
                                   size=size, 
                                   offset=offset, 
                                   dataset=model,
                                   joins=additional_filters)
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
