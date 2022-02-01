from flask import Flask, send_from_directory
from blueprints.patient import patient_blueprint

app = Flask(__name__)
app.register_blueprint(patient_blueprint)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

@app.route("/patient")
def patient():
    return send_from_directory('client/public/patient', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


if __name__ == "__main__":
    app.run(debug=True, port=4999)
