import os
import pickle
import getpass
from werkzeug.security import generate_password_hash, check_password_hash

CREDENTIAL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials.pkl")
USER_CREDENTIALS = {}

if os.path.exists(CREDENTIAL_PATH):
    with open(CREDENTIAL_PATH, "rb") as file:
        USER_CREDENTIALS = pickle.load(file)

class User:
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
        
    def get_id(self):
        return self.user_id
    
    @classmethod
    def authenticate(cls, user_id, password):
        if user_id not in USER_CREDENTIALS:
            return None
        user = USER_CREDENTIALS[user_id]
        if check_password_hash(user["password_hash"], password):
            return User(user_id) # Can add info from the user object here
        return None
    
    @classmethod
    def get(cls, user_id):
        return User(USER_CREDENTIALS.get(user_id, None))
    
if __name__ == "__main__":
    print("Create a new user here.")
    print("Username: ", end='')
    user_id = input()
    if not user_id:
        print("Must type a user ID.")
        exit(1)
    if user_id in USER_CREDENTIALS:
        print("User ID exists, do you want to overwrite? [Y/n] ", end='')
        confirmation = input()
        if confirmation and confirmation.lower() != "y":
            exit(0)
    passwd = ""
    while not passwd:
        passwd = getpass.getpass(prompt="Password: ")
    USER_CREDENTIALS[user_id] = { "password_hash": generate_password_hash(passwd) }
    with open(CREDENTIAL_PATH, "wb") as file:
        pickle.dump(USER_CREDENTIALS, file)
    print("Successfully saved user ID {}.".format(user_id))