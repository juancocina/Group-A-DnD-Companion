import sqlite3
from flask_login import UserMixin
from flask_login.login_manager import LoginManager, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, user_id, username, email, active=True):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.active = active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    def get_id(self):
        return self.user_id

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
