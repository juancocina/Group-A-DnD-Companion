import sqlite3
from types import MethodType
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class Registration:
    """ Class that takes parameters to register a user. Class methos hash(self) takes password parameter and generates a SHA256 hash using werkzeug.security library functions """
    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])
        self.hash_pass = self.hash()

    def hash(self):
        return generate_password_hash(self.password, "sha256")


class Authenticate:
    """ Class that takes a dict of request parameters, does database query and password validation using werkzeug.security library functions """
    def __init__(self, dict, func):
        for key in dict:
            setattr(self, key, dict[key])
        self.func = MethodType(func, self)

    def check(self):
        database = self.func
        c = database.cursor()
        c.execute("SELECT EXISTS(SELECT email FROM users WHERE email=? LIMIT 1)", (self.email,))

        if c.fetchall()[0][0] == 0:
            return jsonify({"message":{"error": "Username not found."}}), 303

        c.execute("SELECT hash_pass FROM users WHERE email=?", (self.email,))
        users_hash = c.fetchall()[0][0]
        c.close()

        return check_password_hash(users_hash, self.password)

