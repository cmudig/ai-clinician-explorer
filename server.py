from flask import Flask, render_template, send_from_directory, request, redirect
from blueprints.patient import patient_blueprint
from blueprints.model import model_blueprint
from blueprints.user import User
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
import os

# If in production mode, enable authentication
PRODUCTION_MODE = os.environ.get("PRODUCTION_MODE") == "1"

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "client", "public"))
csrf = CSRFProtect(app)

app.register_blueprint(patient_blueprint)
app.register_blueprint(model_blueprint)
csrf.exempt(model_blueprint)
app.config['LOGIN_DISABLED'] = not PRODUCTION_MODE

# Read secret key from secret.txt if available, otherwise fallback (dev only)
if os.path.exists("secret.txt"):
    with open("secret.txt", "r") as file:
        app.secret_key = file.read().strip()
else:
    print("WARNING: Using the development secret key. If using in production, please make sure a secret.txt file is present.")
    app.secret_key = "efd06fa9d66fbdc84025a05066bc85d337e1c89a9cbff62ab4cf6fc6c5077f50"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

# Path for our main Svelte page
@app.route("/")
@login_required
def base():
    return render_template('index.html')

@app.route("/patient")
@login_required
def patient():
    return render_template('patient/index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.authenticate(user_id, password)
        if user:
            login_user(user, remember=remember)
            return redirect("/")
        else:
            return render_template('login/index.html', template_params='The user ID and password you entered are invalid.')
    return render_template('login/index.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login/index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == "__main__":
    app.run(debug=True, port=4999)
