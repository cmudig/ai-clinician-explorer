from flask import Blueprint, request, abort, jsonify
from google_auth_oauthlib import flow
from google.cloud.exceptions import NotFound
from .firestore import db, FIRESTORE_KEY_PATH
import numpy as np
import string

study_blueprint = Blueprint('study', __name__, url_prefix='/api/study')

stimuli_doc = db.collection('pilot_study_stimuli').document('staging')
num_cohorts = stimuli_doc.get().to_dict()['num_cohorts']

results_collection = db.collection('pilot_study_data')

PARTICIPANT_ID_CHARACTERS = string.ascii_uppercase + string.digits

@study_blueprint.route('/', methods=['GET'])
def get_study_stimuli():
    """
    Retrieves a set of study stimuli for a participant. The returned dictionary
    will contain a key "stimuli", which contains a list of dictionaries. Each
    dictionary will contain the following keys:
    * "patient_id" - the ID number of the patient
    * "timestep" - the timestep number to show
    * TODO more keys (e.g. choices)
    """
    final_set = []
    for cohort in range(num_cohorts):
        collection = stimuli_doc.collection('cohort_{}'.format(cohort))
        candidate_patients = [doc for doc in collection.stream()]
        chosen = candidate_patients[np.random.choice(len(candidate_patients))]
        chosen_json = chosen.to_dict()
        chosen_json['cohort'] = cohort
        chosen_json['stimulus_id'] = chosen.id
        final_set.append(chosen_json)
    return jsonify({
        "stimuli": final_set
    })
    
def make_participant_id():
    return ''.join([PARTICIPANT_ID_CHARACTERS[i] for i in np.random.choice(len(PARTICIPANT_ID_CHARACTERS), size=6)])

@study_blueprint.route('/init', methods=['POST'])
def initialize_study():
    """
    Initializes data collection for a study participant. Returns a JSON dictionary
    that contains the following keys:
    * "participant_id": The ID number of the participant
    * TODO more keys (e.g. randomization)
    """
    
    participant_id = make_participant_id()
    while results_collection.document(participant_id).get().exists:
        participant_id = make_participant_id()
    data = {
        "participant_id": participant_id
    }
    results_collection.document(participant_id).set(data)
    return jsonify(data)

@study_blueprint.route('/update', methods=['POST'])
def submit_study_data():
    """
    Submits a response to an individual study stimulus.
    """
    try:
        input_data = request.json
    except:
        return "Expected JSON input data", 400
    if "participant_id" not in input_data:
        return "participant_id key required", 400
    if "stimulus_id" not in input_data:
        return "stimulus_id key required", 400
    if "chosen_action" not in input_data:
        return "chosen_action key required", 400
    if "confidence" not in input_data:
        return "confidence key required", 400
    participant_id = input_data["participant_id"]
    if not results_collection.document(participant_id).get().exists:
        return "Participant ID not initialized", 400
    document_data = {
        "chosen_action": input_data["chosen_action"],
        "confidence": input_data["confidence"],
        "stimulus_id": input_data["stimulus_id"]
    }
    results_collection.document(participant_id).collection('responses').document(input_data["stimulus_id"]).set(document_data)
    return {
        "success": True,
        "document": document_data
    }