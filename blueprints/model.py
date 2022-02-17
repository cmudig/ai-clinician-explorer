import os
from flask import Blueprint, request, abort, jsonify
from ai_clinician.modeling.models import AIClinicianModel
from ai_clinician.modeling.columns import ALL_FEATURE_COLUMNS
from ai_clinician.modeling.normalization import DataNormalization
import numpy as np
import pandas as pd

model_blueprint = Blueprint('model', __name__, url_prefix='/api/model')

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "models")
# TODO support DuelingDQNModels here
MODELS = {
    os.path.splitext(model_name)[0]: AIClinicianModel.load(os.path.join(MODEL_DIR, model_name))
    for model_name in os.listdir(MODEL_DIR) if model_name.endswith(".pkl") and not model_name.startswith("normalization")
}

DATA_NORMER = DataNormalization.load(os.path.join(MODEL_DIR, "normalization.pkl"))

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
        return {'models': {mid: get_model_info(m) for mid, m in MODELS.items()}}
    elif model_id not in MODELS:
        return "Model not found", 404
    else:
        model = MODELS[model_id]
        return {'model': get_model_info(model)}

@model_blueprint.route('/<model_id>/predict', methods=['POST'])
def predict(model_id):
    """
    Predict the value of possible actions to take at the given state. The POSTed
    JSON should include the following keys:
    
    * state: a dictionary containing all fields in ALL_FEATURE_COLUMNS, which describes
        the state of the patient.
    
    The result will be JSON containing the following keys:
    
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
        state_info = input_data["state"]
    except:
        return "Expected JSON input data with 'state' key", 400
    
    print(state_info)
    model = MODELS[model_id]
    try:
        X = pd.DataFrame([state_info])
    except KeyError:
        return "Missing value(s) in input state data", 400
    
    normed_X = DATA_NORMER.transform(pd.DataFrame(X, columns=ALL_FEATURE_COLUMNS))
    print(normed_X.values.tolist())
    state = model.compute_states(normed_X.values)
    Q = model.compute_Q(states=state)
    physprob = model.compute_physician_probabilities(states=state)
    
    return jsonify({
        'state': int(state[0]),
        'model_Q': Q[0].astype(float).tolist(),
        'physician_prob': physprob[0].astype(float).tolist()
    })