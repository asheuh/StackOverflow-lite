import logging
from flask import request
from flask_bcrypt import Bcrypt
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_raw_jwt,
    create_access_token
)
from stackoverflow import v2_api
from stackoverflow.api.v2.auth.serializers import (
    user_register,
    user_login
)
from ..errors import (
    check_valid_email,
    user_is_valid,
    validate_username,
    validate_str_field,
    validate_password
)
from stackoverflow.api.v2.models import User, BlackList

flask_bcrypt = Bcrypt()
log = logging.getLogger(__name__)
ns_auth = v2_api.namespace('auth', description='Authentication operations')
ns = v2_api.namespace('user', description='User operations')

@ns_auth.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @v2_api.response(201, 'User created successfully')
    @v2_api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        data = request.json
        errors = user_is_valid(data)
        if check_valid_email(data['email']) is None:
            response = {
                'status': 'error',
                'message': 'Not a valid email address, please try again'}
            return response, 403
        if validate_username(data['username']):
            return validate_username(data['username'])
        if validate_str_field(data['name']):
            return validate_str_field(data['name'])
        if validate_password(data['password']):
            return validate_password(data['password'])
        elif errors:
            response = {
                'status': 'error',
                'message': errors}
            return response, 401
        else:
            user = User(data['name'], data['username'], data['email'], data['password'])
            user.insert()
            access_token = create_access_token(user.id)
            response = {
                'status': 'success',
                'message': 'user created successfully',
                'Authorization': {
                    'access_token': access_token}}
            return response, 201

@ns_auth.route('/login')
class UserLoginResource(Resource):
    """Login resource"""
    @v2_api.doc('login user')
    @v2_api.response(201, 'Login successful')
    @v2_api.expect(user_login, validate=True)
    def post(self):
        """Logs in a user"""
        try:
            data = request.json
            user = User.get_one_by_field(field='username', value=data.get('username'))
            if not user:
                response = {
                    'status': 'fail',
                    'message': 'The username you provided does not exist in the database'}
                return response, 404
            elif not flask_bcrypt.check_password_hash(user['password_hash'], data.get('password')):
                response = {
                    'status': 'fail',
                    'message': 'The password you provided did not match the database password'}
                return response, 401
            else:
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in',
                    'Authorization': {
                        'access_token': create_access_token(user['id'])}}
                return response, 201
        except Exception as e:
            response = {
                'message': 'Could not login: {}, try again'.format(e)}
            return response, 500

@ns_auth.route('/logout_access')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @v2_api.doc('logout user')
    @jwt_required # add jwt token based authentication
    @v2_api.response(201, 'Logout successful')
    def post(self):
        # get auth token
        """Logout a user"""
        jti = get_raw_jwt()['jti']
        try:
            blacklist_token = BlackList(jti=jti)
            blacklist_token.insert()
            response = {
                'status': 'success',
                'message': 'Access token has been revoked, you are now logged out'
            }
            return response, 200
        except Exception as e:
            response = {
                'message': 'could not generat access token: {}'.format(e)
            }
            return response
