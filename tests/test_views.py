import json
import os
import base64

from django.contrib.auth.models import User as AuthUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from cfehome import settings


class TestViews(TestCase):
    adminToken = ""
    userToken = ""
    os.system('python manage.py makemigrations think')
    os.system('python manage.py makemigrations document')
    os.system('python manage.py migrate')

    def __init__(self, method_name: str = "runTest"):
        super().__init__(method_name)

    def setUp(self):
        self.admin_username = 'adminUser'
        self.admin_password = 'adminPass'
        self.admin_user = AuthUser.objects.create_superuser(
            username=self.admin_username, password=self.admin_password)

        self.username = 'myUser'
        self.password = 'myPass'
        self.user = AuthUser.objects.create_user(
            username=self.username, password=self.password)

        self.client = APIClient()

        response = self.client.post(reverse('authentication'), data={
            'username': self.admin_username,
            'password': self.admin_password,
        })
        self.adminToken = response.data['token']

        response = self.client.post(reverse('authentication'), data={
            'username': self.username,
            'password': self.password,
        })
        self.userToken = response.data['token']


    def test_authentication_success(self):
        response = self.client.post(reverse('authentication'), data={
            'username': self.username,
            'password': self.password,
        })

        self.assertEqual(response.status_code, 200)

    def test_authentication_failure(self):
        response = self.client.post(reverse('authentication'), data={
            'username': self.username,
            'password': 'invalid',
        })

        self.assertEqual(response.status_code, 401)
        error_message = response.data['error']
        self.assertEqual(error_message, 'Login data not valid')


    def test_get_options_authenticated(self):
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
        response = self.client.get(reverse('options'), **headers)
        self.assertEqual(response.status_code, 200)

        try:
            config = response.json()
        except json.JSONDecodeError:
            self.fail("Invalid JSON")

        required_keys = ["endpointName", "name"]
        optional_keys = ["description", "apiName"]
        endpoint_values = ["listen/", "speak/", "think/"]
        for section in config:
            self.assertTrue(all(key in section for key in required_keys))
            self.assertTrue(all(key in required_keys + optional_keys for key in section))
            self.assertIn(section["endpointName"], endpoint_values)

    def test_get_options_not_authenticated(self):
        client = APIClient()
        response = client.get(reverse('options'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_listen_view_with_file_upload(self):
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        with open(file_path, 'rb') as file_data:
            data = {
                "model": "whisper",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')

        self.assertEqual(response.status_code, 200)

    def test_listen_view_model_whisper(self):
        """ Test when model is whisper """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        with open(file_path, 'rb') as file_data:
            data = {
                "model": "whisper",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_default(self):
        """ Test when model is default """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        with open(file_path, 'rb') as file_data:
            data = {
                "model": "default",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_whisperNBAiLab(self):
        """ Test when model is whisperNBAiLab """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        with open(file_path, 'rb') as file_data:
            data = {
                "model": "whisperNBAiLab",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_whisperOpenAILocal(self):
        """ Test when model is whisperOpenAILocal """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        with open(file_path, 'rb') as file_data:
            data = {
                "model": "whisperOpenAILocal",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_invalid(self):
        """ Test when model is not valid """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        with open(file_path, 'rb') as file_data:
            data = {
                "model": "invalid",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_think_view_model_gpt_turbo_3_5(self):
        """ Test when model is gpt-3.5-turbo """
        data = {
            "model": "['gpt-3.5-turbo']",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_gpt_turbo_4_preview(self):
        """ Test when model is gpt-4-turbo-preview """
        data = {
            "model": "['gpt-4-turbo-preview']",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_norwegian_jaccard(self):
        """ Test when model is norwegian-on-the-jaccard """
        data = {
            "model": "jaccard",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_invalid(self):
        """ Test when model is not valid """
        data = {
            "model": "invalid",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 400)

    def helper_test_speak_view(self, model, expected_status_code, content_type=None):
        """ Helper function to make testing different models easier """
        testString = "Hello World"

        headers = {
            'HTTP_MESSAGE': base64.b64encode(testString.encode('utf-8')).decode('utf-8'),
            'HTTP_MODEL': model,
            'HTTP_AUTHORIZATION': 'Token {}'.format(self.userToken)
        }
        response = self.client.get(reverse('speak'), **headers)


        self.assertEqual(response.status_code, expected_status_code)


        if content_type:
            self.assertEqual(response['Content-Type'], content_type)

    def test_speak_view_model_invalid(self):
        """ Test when model is not valid """
        self.helper_test_speak_view('invalid', 400)

    def test_document_creation(self):
        """
            Testing the 'document' api endpoint for a success POST request
            """
        content = b'sample_content'
        document = SimpleUploadedFile('sample_file.txt', content)

        data = {
            'name': 'sample_name',
            'document': document,
            'database': 'test1',

        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.adminToken)}
        response = self.client.post(reverse('document'), data=data, **headers)
        self.assertEqual(response.status_code, 201)

    def test_document_invalid_request(self):
        """
            Testing the 'document' api endpoint for a bad POST request
            """
        data = {
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.adminToken)}
        response = self.client.post(reverse('document'), data=data, **headers)
        self.assertEqual(response.status_code, 400)

    def test_document_unauthorized_request(self):
        """
            Testing the 'document' api endpoint for unauthorized POST request
            """
        data = {
            'name': 'sample_name',
            'database': 'sample_database',
        }
        response = self.client.post(reverse('document'), data=data)
        self.assertEqual(response.status_code, 401)

    def test_non_admin_access(self):
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.adminToken)}
        database_name = 'test1'
        data = {
            "update_database": False,
            "new_database": True,
            "delete_database": False,
            "database_name": database_name,
        }
        response = self.client.post(reverse('configuration'), data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_configuration(self):
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.adminToken)}
        database_name = 'test1'
        data = {
            "update_database": False,
            "new_database": True,
            "delete_database": False,
            "database_name": database_name,
            "prompt_start": "start_prompt",
            "prompt_end": "end_prompt",
            "context_start": "start_context",
            "context_end": "end_context",
        }
        response = self.client.post(reverse('configuration'), data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(os.path.exists(os.path.join(settings.BASE_DIR, 'config', database_name + '.json')))

    def test_update_configuration(self):
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.adminToken)}
        database_name = 'test1'
        data = {
            "update_database": True,
            "new_database": False,
            "delete_database": False,
            "database_name": database_name,
            "prompt_start": "start_prompt_updated",
            "prompt_end": "end_prompt_updated",
            "context_start": "start_context_updated",
            "context_end": "end_context_updated",
        }
        response = self.client.post(reverse('configuration'), data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with open(os.path.join(settings.BASE_DIR, 'config', database_name + '.json')) as f:
            config = json.load(f)
        self.assertEqual(config.get('prompt_start'), "start_prompt_updated")

    def test_delete_configuration(self):
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.adminToken)}
        database_name = 'test1'
        data = {
            "update_database": False,
            "new_database": False,
            "delete_database": True,
            "database_name": database_name,
            "prompt_start": "start_prompt_updated",
            "prompt_end": "end_prompt_updated",
            "context_start": "start_context_updated",
            "context_end": "end_context_updated",
        }
        response = self.client.post(reverse('configuration'), data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(os.path.exists(os.path.join(settings.BASE_DIR, 'config', database_name + '.json')))
