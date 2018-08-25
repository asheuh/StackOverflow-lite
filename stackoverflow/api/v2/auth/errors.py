"""
Imports

"""
import re
from flask import jsonify
from stackoverflow.api.restplus import API
from ..models import User, Question, Answer

def user_is_valid(data):
    """user error handling"""
    errors = {}
    result = User.get_one_by_field('username', data.get('username'))
    error = "The email you provided is in use by another user"
    if User.get_one_by_field(field='email', value=data.get('email')) is not None:
        errors['email'] = error
    if result is not None:
        errors['username'] = "The username you provided already exists"

    return errors

def validate_str_field(string):
    """Validate the user has input as string"""
    regex = re.match("^[ A-Za-z0-9_-]*$", string)
    if not regex:
        return jsonify({"message": "Invalid data for username"}), 400
    return None

def validate_password(string):
    """validates user has followed Password rules"""
    passerror = "The password should have at least 1 digit, 1 caps, 1 number and minimum of 6 chars"
    if not re.match(r'(?=.*?[0-9])(?=.*?[A-Z])(?=.*?[a-z]).{6}', string):
        return jsonify({
            "message": passerror
        }), 400
    return None

def validate_username(string):
    """validate the user has input the right username format"""
    if not re.match("^[A-Za-z0-9_-]*$", string):
        return jsonify({"message": "Name should only contain letters, numbers, underscores and dashes"}), 400
    return None

def question_doesnt_exists(question_id):
    """Checks if given id exists in the database"""
    if not Question.get_one_by_field('id', value=question_id):
        API.abort(404, "Question with id {} doesn't exist \
                  or your provided an id that does not belong to you".format(question_id))

def answer_doesnt_exists(answer_id):
    """Checks if given id exists in the database"""
    if not Answer.get_one_by_field('id', value=answer_id):
        response_obj = {
            'message': 'The answer with the given id does not exist'
        }
        return jsonify(response_obj), 404
    return None

def check_valid_email(email):
    """Checks if the email provided is valid"""
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
