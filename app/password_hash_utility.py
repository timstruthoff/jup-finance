import bcrypt

class PasswordHashUtility:
    def __init__(self):
        pass
    
    def get_hashed_password(self, plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password.encode("utf8"), bcrypt.gensalt())

    def check_password(self, plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        utf_encoded_plaid_text_password = plain_text_password.encode("utf8")
        utf_encoded_hashed_password = hashed_password.encode("utf8")
    
        return bcrypt.checkpw(utf_encoded_plaid_text_password, utf_encoded_hashed_password)