from flask import Blueprint, request, abort, jsonify
from google_auth_oauthlib import flow
from google.cloud.exceptions import NotFound
from .firestore import db, FIRESTORE_KEY_PATH
import numpy as np
import string

study_blueprint = Blueprint('study', __name__, url_prefix='/api/study')

stimuli_collection = db.collection('pilot_study_stimuli')
DEFAULT_STIMULUS_SET = 'cases_220801'

results_collection = db.collection('pilot_study_data')

PARTICIPANT_ID_CHARACTERS = string.ascii_uppercase + string.digits
DEV_PARTICIPANT_ID = "DEV"

def get_study_stimuli(dev=False, stimulus_set=None):
    """
    Retrieves a set of study stimuli for a participant. The returned value is
    a list of dictionaries. Each dictionary will contain the following keys:
    * "patient_id" - the ID number of the patient
    * "timestep" - the timestep number to show
    * TODO more keys (e.g. choices)
    """
    final_set = []
    chosen_stimuli_doc = stimuli_collection.document(stimulus_set or DEFAULT_STIMULUS_SET)
    num_cohorts = chosen_stimuli_doc.get().to_dict()['num_cohorts']

    if dev:
        # Return a list of all the possible stimuli
        for cohort in range(num_cohorts):
            collection = chosen_stimuli_doc.collection('cohort_{}'.format(cohort))
            candidate_patients = [doc for doc in collection.stream()]
            for chosen in candidate_patients:
                chosen_json = chosen.to_dict()
                chosen_json['cohort'] = cohort
                chosen_json['stimulus_id'] = chosen.id
                final_set.append(chosen_json)
    elif chosen_stimuli_doc.collection('sequence').get():
        # There is a predefined sequence
        participant_number = chosen_stimuli_doc.get().get("participantCount")
        chosen_stimuli_doc.update({"participantCount": participant_number + 1})
        stimulus_ids = chosen_stimuli_doc.collection('sequence').document(str(participant_number)).get().get('stimuli')
        print("Participant number {}, sequence: {}".format(participant_number, stimulus_ids))
        for cohort, stid in enumerate(stimulus_ids):
            chosen = chosen_stimuli_doc.collection('cohort_{}'.format(cohort)).document(stid)
            chosen_json = chosen.get().to_dict()
            chosen_json['cohort'] = cohort
            chosen_json['stimulus_id'] = chosen.id
            final_set.append(chosen_json)
    else:
        seen_ids = set()
        for cohort in range(num_cohorts):
            collection = chosen_stimuli_doc.collection('cohort_{}'.format(cohort))
            candidate_patients = [doc for doc in collection.stream()]
            chosen = candidate_patients[np.random.choice(len(candidate_patients))]
            if any(c.get("patient_id") not in seen_ids for c in candidate_patients):
                while chosen.get("patient_id") in seen_ids:
                    chosen = candidate_patients[np.random.choice(len(candidate_patients))]
            else:
                print(("WARNING: This participant may be shown repeat study " +
                    "stimuli because there are no stimuli available for cohort " +
                    "{} that have not already appeared in a previous cohort.").format(cohort))
            chosen_json = chosen.to_dict()
            chosen_json['cohort'] = cohort
            chosen_json['stimulus_id'] = chosen.id
            final_set.append(chosen_json)
            seen_ids.add(chosen_json["patient_id"])
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
        else:
            participant_id = None
    except:
        participant_id = None
        input_data = {}
    
    if participant_id is None:
        stimulus_set = input_data.get("stimulus_set", None)
        dev_mode = input_data.get("dev", 0) == 1
        if dev_mode: participant_id = DEV_PARTICIPANT_ID
        else: 
            participant_id = make_participant_id()
            while results_collection.document(participant_id).get().exists:
                participant_id = make_participant_id()
        data = {
            "participant_id": participant_id,
            "stimuli": get_study_stimuli(dev=dev_mode, stimulus_set=stimulus_set)
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