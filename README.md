# AI Clinician Explorer

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
`1`.
