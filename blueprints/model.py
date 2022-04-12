import os
from flask import Blueprint, request, abort, jsonify
from .firestore import db
from ai_clinician.modeling.models import AIClinicianModel
from ai_clinician.modeling.columns import ALL_FEATURE_COLUMNS
from ai_clinician.preprocessing.columns import *
from ai_clinician.modeling.normalization import DataNormalization
from ai_clinician.modeling.models.common import transform_actions
import numpy as np
import pandas as pd

model_blueprint = Blueprint('model', __name__, url_prefix='/api/model')

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "models")
# TODO support DuelingDQNModels here
MODELS = {
    model_name: {
        'model': AIClinicianModel.load(os.path.join(MODEL_DIR, model_name, 'model.pkl')),
        'normalization': DataNormalization.load(os.path.join(MODEL_DIR, model_name, "normalization.pkl"))
    }
    for model_name in os.listdir(MODEL_DIR) if os.path.isdir(os.path.join(MODEL_DIR, model_name))
}

# Initialize Firestore DB - we retrieve model state information from here
model_db = db.collection('AI_clinician_models')

def get_model_info(model):
    if isinstance(model, AIClinicianModel):
        model_data = {
            'model_type': 'AIClinicianModel',
            'Qon': model.Q.tolist(),
            'actions': model.metadata['actions'],
            'params': {
                'n_cluster_states': model.n_cluster_states,
                'n_actions': model.n_actions,
                'cluster_fit_fraction': model.cluster_fit_fraction,
                'n_cluster_init': model.n_cluster_init,
                'gamma': model.gamma,
                'random_state': model.random_state,
                'reward_val': model.reward_val,
                'transition_threshold': model.transition_threshold,
                'soften_factor': model.soften_factor
            }
        }
        return model_data
    raise NotImplementedError("get_model_info does not support instance of type {}".format(type(model)))

@model_blueprint.route('/', methods=['GET'], defaults={'model_id': None})
@model_blueprint.route('/<model_id>')
def model_info(model_id):
    """
    If called without a model_id (/api/model), returns a list of all models and
    available metadata.
    
    If called with a model_id (/api/model/<model_id>), returns the info about a
    specific model.
    """
    if model_id is None:
        return {'models': {mid: get_model_info(m['model']) for mid, m in MODELS.items()}}
    elif model_id not in MODELS:
        return "Model not found", 404
    else:
        model = MODELS[model_id]['model']
        return {'model': get_model_info(model)}

def explain_states(model_id, states):
    """
    Retrieves explanations of the given list of states, and returns them as a
    list of dictionaries corresponding to the states in the list.
    """
    unique_states = set(states)
    states_collection = model_db.document(model_id).collection('states')
    explanations = {s: states_collection.document(str(s)).get().to_dict()
                    for s in unique_states}
    return [explanations[s] for s in states]
    
@model_blueprint.route('/<model_id>/predict', methods=['POST'])
def predict(model_id):
    """
    Predict the value of possible actions to take at the given state. The POSTed
    JSON should include the following keys:
    
    * states: a list of dictionaries containing all fields in ALL_FEATURE_COLUMNS,
        which describes the state of the patient at a series of timesteps.
    * actions: (optional) a list of dictionaries containing the actions taken
        by the clinicians at each of the states in the `states` key. The
        dictionaries should have the C_INPUT_STEP and C_MAX_DOSE_VASO keys.
    
    The result will be JSON containing a "results" list, where each item corresponds
    to one of the input states. Each item will contain the following keys:
    
    * state: A latent representation of the state (for the default AI Clinician,
        this is an integer representing the state number).
    * model_Q: a list of n_actions float values indicating the Q value of taking
        each action according to the model.
    * physician_prob: a list of n_actions float values indicating the probability
        of taking each action according to the observed physician data.
    """
    if model_id not in MODELS:
        return "Model not found", 404
    try:
        input_data = request.json
        state_info = input_data["states"]
        action_info = input_data.get("actions", None)
    except:
        return "Expected JSON input data with 'states' key", 400
    
    model = MODELS[model_id]['model']
    normer = MODELS[model_id]['normalization']
    try:
        X = pd.DataFrame(state_info)
    except KeyError:
        return "Missing value(s) in input state data", 400
    
    normed_X = normer.transform(X[ALL_FEATURE_COLUMNS])
    state_reps = model.compute_states(normed_X.values)

    Q = model.compute_Q(states=state_reps)
    physprob = model.compute_physician_probabilities(states=state_reps, soften=False)
    Q = np.where(physprob <= 1e-6, np.nan, Q)
    
    if action_info is not None:
        if len(action_info) != len(state_info):
            return "Length of actions needs to match length of states", 400
        clin_actions = transform_actions(
            [x.get(C_INPUT_STEP, 0) for x in action_info],
            [x.get(C_MAX_DOSE_VASO, 0) for x in action_info],
            model.metadata['actions']['action_bins'])
        clin_actions = [a if C_INPUT_STEP in x and C_MAX_DOSE_VASO in x else -1
                        for a, x in zip(clin_actions, action_info)]
        clin_actions = clin_actions[1:] + [-1]
    else:
        clin_actions = None
    
    try:
        explanations = explain_states(model_id, state_reps)
    except Exception as e:
        print(e)
        return "Error retrieving explanations", 400
        
    return jsonify({'results': [{
        'state': int(state_reps[i]),
        'state_explanation': explanations[i],
        'model_Q': [x if not np.isnan(x) else None for x in Q[i].astype(float).tolist()],
        'physician_prob': physprob[i].astype(float).tolist(),
        'recommendation': int(np.argmax(np.where(np.isnan(Q[i]), -1e9, Q[i]))),
        'actual_action': int(clin_actions[i]) if clin_actions else None
    } for i in range(len(state_reps))]})