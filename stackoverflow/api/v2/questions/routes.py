from flask import request
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from ..auth.errors import (
    question_doesnt_exists
)
from stackoverflow import v2_api
from ..auth.serializers import questions, Pagination, answers
from stackoverflow.api.v1.auth.parsers import pagination_arguments
from stackoverflow.api.v2.models import Question, Answer
from stackoverflow import settings

ns = v2_api.namespace('questions', description='Questions operations')

@ns.route('')
class UserQuestionsResource(Resource):
    """Question resource endpoint"""
    @jwt_required
    @v2_api.doc('Question resource')
    @v2_api.response(201, 'Successfully created')
    @v2_api.expect(questions)
    def post(self):
        """Post a new question"""
        try:
            data = request.json
            title = data['title']
            description = data['description']
            questions = Question(
                title,
                description,
                created_by=get_jwt_identity()
            )
            questions.insert()
            response = {
                'status': 'success',
                'message': 'Question posted successfully',
                'data': questions.toJSON()
            }
            return response, 201
        except Exception as e:
            response = {
                'status': 'error',
                'message': 'Cannot post a question: {}'.format(e)
            }
            return response, 500

@ns.route('/<int:question_id>/answers')
@v2_api.response(404, 'question with the given id not found')
class UserAnswerResource(Resource):
    """Single question resource"""
    @jwt_required
    @v2_api.doc('Single question resource')
    @v2_api.response(200, 'Success')
    @v2_api.expect(answers)
    def post(self, question_id):
        """Post an answer to this particular question"""
        question_doesnt_exists(question_id)
        data = request.json
        answer = data['answer']
        question = Question.get_item_by_id(question_id)
        answer = Answer(answer,
                        owner=get_jwt_identity(),
                        question=question['id']
                    )
        answer.insert()
        response = {
            'status': 'success',
            'message': 'Answer posted successfully',
            'answer': answer.toJSON()
        }
        return response, 201
