# AI Clinician Explorer

The AI Clinician Explorer is a prototype visualization tool and study interface that enables clinicians and health data experts to browse patient trajectories and analyze AI-generated treatment recommendations.

![Screenshot of the AI Clinician Explorer showing a patient's demographics, vitals, labs, past treatments, and model predictions.](/assets/example-screenshot.png)

For privacy reasons, a live demo is currently not available. To learn more about the project, please see the following paper:

> Sivaraman, V., Bukowski, L., Levin, J., Kahn, J.M., Perer, A. Ignore, trust, or negotiate: Understanding clinician acceptance of AI-based treatment recommendations in health care. _ACM CHI 2023._

## Setup

```
pip install -r requirements.txt
cd client && npm install && cd ..
```

Make sure you have the Firestore key included in the top-level directory.

Start the flask server: `python server.py`

In a separate terminal, run the frontend: `cd client && npm run autobuild`

## Deployment

In the deployed container, create a `secret.txt` file using the following command:

```python
python -c 'import secrets; print(secrets.token_hex())' > secret.txt
```

Create a user profile by running the `blueprints/user.py` script. Also, make sure
you have uploaded the `firestore_key.json` file.

In the production environment, set the environment variable `PRODUCTION_MODE` to
`1`. You can also set a different value for the environment variable `FIRESTORE_KEY_PATH`
to retrieve the key from somewhere other than the default `firestore_key.json`
path.
