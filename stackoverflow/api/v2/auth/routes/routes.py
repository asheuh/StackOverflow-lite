import logging
from flask import request
from flask_bcrypt import Bcrypt
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_raw_jwt
)
from stackoverflow.api.v1.auth.parsers import pagination_arguments
from stackoverflow import v2_api
from stackoverflow.api.v2.auth.serializers import (
    user_register,
    user_login
)
from stackoverflow import settings

flask_bcrypt = Bcrypt()
log = logging.getLogger(__name__)
ns_auth = v2_api.namespace('auth', description='Authentication operations')
ns = v2_api.namespace('user', description='User operations')

@ns_auth.route('/register')
class UsersCollection(Resource):
    """This class creates a new user in the database"""
    @v2_api.doc(pagination_arguments)
    @v2_api.response(201, 'User created successfully')
    @v2_api.expect(user_register, validate=True)
    def post(self):
        """Creates a new user"""
        pass

@ns_auth.route('/login')
class UserLoginResource(Resource):
    """Login resource"""
    @v2_api.doc('login user')
    @v2_api.response(201, 'Login successful')
    @v2_api.expect(user_login, validate=True)
    def post(self):
        """Logs in a user"""
        pass

@ns_auth.route('/logout_access')
class UserLogoutResourceAccess(Resource):
    """Logout resource"""
    @v2_api.doc('logout user')
    @jwt_required
    @v2_api.response(201, 'Logout successful')
    def post(self):
        # get auth token
        """Logout a user"""
        pass
