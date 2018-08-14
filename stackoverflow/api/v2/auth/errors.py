import re
from ..models import User

def user_is_valid(data):
    """user error handling"""
    errors = {}
    if User.get_one_by_field(field='email', value=data.get('email')) is not None:
        errors['email'] = "The email you provided is in use by another user"
    if User.get_one_by_field(field='username', value=data.get('username')) is not None:
        errors['username'] = "The username you provided already exists"

    return errors

def check_valid_email(email):
    """Checks if the email provided is valid"""
    return re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', email)
