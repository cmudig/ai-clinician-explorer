from flask import Blueprint, request, abort, jsonify
from firebase_admin import credentials, firestore, initialize_app

patient_blueprint = Blueprint('patient', __name__, url_prefix='/api/patient')

# Initialize Firestore DB
cred = credentials.Certificate('firestore_key.json')
default_app = initialize_app(cred)
db = firestore.client()
mimic_data = db.collection('MIMIC_dataset')

def match_sort_criterion_type(sort_criterion, val):
    """Converts the given value to the appropriate type for the given sort criterion."""
    if sort_criterion in ("age",
                          "delay_end_of_record_and_discharge_or_death",
                          "elixhauser",
                          "gender",
                          "icustayid",
                          "num_timesteps"):
        return int(val)
    elif sort_criterion in ("died_in_hosp", "died_within_48h_of_out_time", "morta_90", "re_admission"):
        return bool(val)
    return val

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
    * cursor_id: value of the stay ID after which to start returning results.
        For example, to return the second page of results, pass cursor as the 
        value of the icustayid of the last result from the first page (see
        https://firebase.google.com/docs/firestore/query-data/query-cursors).
    * cursor_sort: value of the sort criterion after which to start returning
        results. This is required if using a cursor and sorting by a field other
        than icustayid.
        
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

        cursor = args.get("cursor_id", None)
        if cursor:
            try:
                cursor = [match_sort_criterion_type('icustayid', cursor)]
            except:
                return "Invalid value for cursor_id query parameter", 400
        
        cursor_sort = args.get("cursor_sort", None)
        if cursor_sort:
            try:
                cursor_sort = match_sort_criterion_type(sort_criterion, cursor_sort)
            except:
                return "Invalid value for cursor_sort query parameter", 400
            if cursor is None:
                return "cursor_id is required if using a cursor", 400
            cursor = [cursor_sort, cursor]
        elif sort_criterion != 'icustayid' and cursor is not None:
            return "cursor_sort is required for using sort criteria other than 'icustayid'", 400
        
        try:
            size = int(args.get("size", 10))
        except ValueError:
            return "Invalid value for size query parameter", 400
        
        print(sort_criterion, ascending, cursor, size)
        query = mimic_data.order_by(
            sort_criterion,
            direction=firestore.Query.ASCENDING if ascending else firestore.Query.DESCENDING
        )
        if sort_criterion != 'icustayid':
            # Also sort by icustayid
            query = query.order_by('icustayid')
            
        if cursor:
            query = query.start_after(cursor)
        try:                
            docs = query.limit(size).get()
        except Exception as e:
            print(e)
            return "An error occurred returning the results.", 400
        print(docs[-1].to_dict())
        return jsonify({'results': [d.to_dict() for d in docs]})
    else:
        doc = mimic_data.document(patient_id).get()
        if doc.exists:
            return jsonify({
                'result': doc.to_dict()
            })
        else:
            return "Patient does not exist", 404