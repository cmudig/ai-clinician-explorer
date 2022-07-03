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

def get_study_stimuli():
    """
    Retrieves a set of study stimuli for a participant. The returned value is
    a list of dictionaries. Each dictionary will contain the following keys:
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
    return final_set
    
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
    try:
        input_data = request.json
        if "participant_id" in input_data:
            # Attempt to resume the participant's session
            participant_id = input_data["participant_id"]
            if not results_collection.document(participant_id).get().exists:
                return "The Participant ID was not found.", 400
    except:
        participant_id = None
    
    if participant_id is None:
        participant_id = make_participant_id()
        while results_collection.document(participant_id).get().exists:
            participant_id = make_participant_id()
        data = {
            "participant_id": participant_id,
            "stimuli": get_study_stimuli()
        }
        results_collection.document(participant_id).set(data)
    else:
        data = results_collection.document(participant_id).get().to_dict()
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
    if "state" not in input_data:
        return "state key required", 400
    participant_id = input_data["participant_id"]
    state = input_data["state"] # this is the state that has been COMPLETED
    parent_info = {
        "state": state,
        "pre_survey_responses": input_data.get("pre_survey_responses", {}),
        "post_survey_responses": input_data.get("post_survey_responses", {})
    }
    if state == "STIMULI":
        if "response" not in input_data:
            return "response key required for state STIMULI", 400
        response = input_data["response"]
        if "stimulus_id" not in response:
            return "stimulus_id key required in response", 400
        if "chosen_action" not in response:
            return "chosen_action key required in response", 400
        if "confidence" not in response:
            return "confidence key required in response", 400
        if "study_index" not in input_data:
            return "study_index key required in input data", 400
        if not results_collection.document(participant_id).get().exists:
            return "Participant ID not initialized", 400
        document_data = {
            "chosen_action": response["chosen_action"],
            "confidence": response["confidence"],
            "stimulus_id": response["stimulus_id"]
        }
        results_collection.document(participant_id).collection('responses').document(response["stimulus_id"]).set(document_data)
        parent_info["study_index"] = input_data["study_index"]
        
    # Update the participant ID document
    results_collection.document(participant_id).update(parent_info)
    
    return {
        "success": True
    }