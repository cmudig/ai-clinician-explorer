import os
from flask import Blueprint, request, abort, jsonify
from ai_clinician.modeling.models import AIClinicianModel

model_blueprint = Blueprint('model', __name__, url_prefix='/api/model')

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "models")
# TODO support DuelingDQNModels here
MODELS = {
    os.path.splitext(model_name)[0]: AIClinicianModel.load(os.path.join(MODEL_DIR, model_name))
    for model_name in os.listdir(MODEL_DIR) if model_name.endswith(".pkl")
}

def get_model_info(model):
    if isinstance(model, AIClinicianModel):
        model_data = {
            'model_type': 'AIClinicianModel',
            'Qon': model.Q.tolist(),
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
        print(MODELS)
        return {'models': {mid: get_model_info(m) for mid, m in MODELS.items()}}
    elif model_id not in MODELS:
        return "Model not found", 404
    else:
        model = MODELS[model_id]
        return {'model': get_model_info(model)}