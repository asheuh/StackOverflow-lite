import json
from .base_test import BaseTestCase

class TestUserQuestions(BaseTestCase):
    def test_post_question(self):
        with self.client:
            resp_register = self.client.post(
                '/api/v2/auth/register',
                data=json.dumps(dict(
                    name='Brian Mboya',
                    email='asheuh@gmail.com',
                    username='asheuh',
                    password='mermaid'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['Authorization']['access_token']
                ),
                data=json.dumps(dict(
                    title='Gjango cli',
                    description='How to create cli project in django?'
                )),
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertTrue(response_data['message'] == 'Question posted successfully')
            self.assertEqual(response.status_code, 201)

