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
        "study_index": input_data.get("study_index", 0)
    }
    if "pre_survey_responses" in input_data:
        parent_info["pre_survey_responses"] = input_data["pre_survey_responses"]
    if "post_survey_responses" in input_data:
        parent_info["post_survey_responses"] = input_data["post_survey_responses"]
    if "stimulus_responses" in input_data:
        responses = input_data["stimulus_responses"]
        for response in responses:
            if "stimulus_id" not in response:
                return "stimulus_id key required in response", 400
            if "fluidTreatment" not in response:
                return "fluidTreatment key required in response", 400
            if "vasopressorTreatment" not in response:
                return "vasopressorTreatment key required in response", 400
            if "confidence" not in response:
                return "confidence key required in response", 400
            if "caseDifficulty" not in response:
                return "caseDifficulty key required in response", 400
            if not results_collection.document(participant_id).get().exists:
                return "Participant ID not initialized", 400
            results_collection.document(participant_id).collection('responses').document(response["stimulus_id"]).set(response)
        
    # Update the participant ID document
    results_collection.document(participant_id).update(parent_info)
    
    return {
        "success": True
    }