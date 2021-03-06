"""
Imports

"""
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import json
from stackoverflow.settings import VOTES, PENDING
from stackoverflow.database import blacklistdb

FLASK_BCRYPT = Bcrypt()

class MainModel:
    """This is the base model that creates common functions"""
    def toJSON(self):
        """Converts json string object to a dictionary"""
        return json.loads(json.dumps(self,
                                     default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S")
                                     if isinstance(o, datetime)
                                     else o.__dict__,
                                     sort_keys=True, indent=4))

class User(MainModel):
    """Creates the user model"""
    def __init__(self, name, username, email, password):
        """Initializes the user model"""

        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)
        self.registered_on = datetime.now().isoformat()

    def set_password(self, password):
        """Sets the hashed password"""
        self.password_hash = FLASK_BCRYPT.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify that the hashed password matches the user input password"""
        return FLASK_BCRYPT.check_password_hash(self.password_hash, password)

class Question(MainModel):
    """Question model"""
    def __init__(self, title=None,
                 description=None, created_by=None, answers=0):

        self.title = title
        self.description = description
        self.created_by = created_by
        self.answers = answers
        self.date_created = datetime.now()

class Answer(MainModel):
    """The answer model"""
    def __init__(self, answer=None,
                 votes=VOTES, owner=None, question=None):
        self.answer = answer
        self.accepted = PENDING
        self.votes = votes
        self.owner = owner
        self.question = question
        self.date_created = datetime.now()

class BlackListToken(MainModel):
    """Creates the blacklisting model"""
    def __init__(self, jti, blacklisted_on=datetime.now().isoformat()):
        """Initializes the blacklist model"""
        self.jti = jti
        self.blacklisted_on = blacklisted_on


    @classmethod
    def check_blacklist(cls, auth_token):
        """Check if the token is blacklisted"""
        res = cls.get_by_field(key='jti', value=auth_token)
        return bool(res)

    @classmethod
    def get_by_field(cls, key, value):
        if blacklistdb is None:
            return {}
        for item in blacklistdb.values():
            if item[key] == value:
                return item
