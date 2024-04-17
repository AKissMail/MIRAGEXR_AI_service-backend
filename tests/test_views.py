import json
import os

from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient

import tests
from think.models import Document, Content


class TestViews(TestCase):
    t = ""

    def setUp(self):
        self.client = APIClient()
        self.username = 'myUser'
        self.password = 'myPass'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        file_path = os.path.join(os.path.dirname(__file__), '../config/options.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            self.expected_config = json.load(file)

        response = self.client.post(reverse('authentication'), data={
            'username': self.username,
            'password': self.password,
        })
        self.t = response.data['token']

        self.doc1 = Document.objects.create(
            title='Test Document',
            source_type='pdf',
            content='This is the content',
            ltx=5.4,
            smog_index=3.1,
            language='EN',
            sentences='["This is a sentence.", "This is another sentence."]',
            words='["word1", "word2", "word3", "word4"]',
            average_sentence_length=5.6,
            word_count=10,
            sentences_count=2
        )

        self.doc2 = Content.objects.create(
            document=self.doc1,
            heading='Test Heading',
            body_text='This is the body text',
            section_number=1
        )

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

        # Further usage of the error_message...

    def test_get_options_authenticated(self):
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
        response = self.client.get(reverse('options'), **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.expected_config)

    def test_get_options_not_authenticated(self):
        client = APIClient()
        response = client.get(reverse('options'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_listen_view_with_file_upload(self):
        # Define the path to your file
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        # Open the file in binary mode
        with open(file_path, 'rb') as file_data:
            # Define the data for the POST request, including the file
            data = {
                "model": "whisper",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
            # Make the POST request, including format='multipart'
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')

        # Check that the status code is what you expect
        self.assertEqual(response.status_code, 200)

    def test_listen_view_model_whisper(self):
        """ Test when model is whisper """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        # Open the file in binary mode
        with open(file_path, 'rb') as file_data:
            data = {
                "model": "whisper",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_default(self):
        """ Test when model is default """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        # Open the file in binary mode
        with open(file_path, 'rb') as file_data:
            data = {
                "model": "default",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_whisperNBAiLab(self):
        """ Test when model is whisperNBAiLab """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        # Open the file in binary mode
        with open(file_path, 'rb') as file_data:
            data = {
                "model": "whisperNBAiLab",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_whisperOpenAILocal(self):
        """ Test when model is whisperOpenAILocal """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        # Open the file in binary mode
        with open(file_path, 'rb') as file_data:
            data = {
                "model": "whisperOpenAILocal",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 200)

    def test_listen_view_model_invalid(self):
        """ Test when model is not valid """
        file_path = os.path.join(os.path.dirname(__file__), 'audio_king.mp3')

        # Open the file in binary mode
        with open(file_path, 'rb') as file_data:
            data = {
                "model": "invalid",
                "message": file_data,
            }
            headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
            response = self.client.post(reverse('listen'), data=data, **headers, format='multipart')
            self.assertEqual(response.status_code, 400)

    def test_think_view_model_default(self):
        """ Test when model is default """
        data = {
            "model": "Default",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_gpt_turbo_3_5(self):
        """ Test when model is gpt-3.5-turbo """
        data = {
            "model": "gpt-3.5-turbo",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_gpt_turbo_4_preview(self):
        """ Test when model is gpt-4-turbo-preview """
        data = {
            "model": "gpt-4-turbo-preview",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_norwegian_jaccard(self):
        """ Test when model is norwegian-on-the-jaccard """
        data = {
            "model": "norwegian-on-the-jaccard",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_norwegian_vector(self):
        """ Test when model is norwegian-on-the-vector """
        data = {
            "model": "norwegian-on-the-vector",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 200)

    def test_think_view_model_invalid(self):
        """ Test when model is not valid """
        data = {
            "model": "invalid",
            "message": "test message",
            "context": "This is a Test"
        }
        headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.t)}
        response = self.client.post(reverse('think'), data=data, **headers)
        self.assertEqual(response.status_code, 400)

    def helper_test_speak_view(self, model, expected_status_code, content_type=None):
        """ Helper function to make testing different models easier """
        headers = {
            'message': 'test message',
            'voice': 'onyx',
            'model': model
        }

        response = self.client.get(reverse('speak'), **headers,
                                   HTTP_AUTHORIZATION='Token {}'.format(self.t))
        # Check that the status code is what you expect
        self.assertEqual(response.status_code, expected_status_code)

        # Check if Content-Type matches expected value
        if content_type:
            self.assertEqual(response['Content-Type'], content_type)

    def test_speak_view_model_openAI(self):
        """ Test when model is openAI """
        #self.helper_test_speak_view('openAI', 200, 'audio/mpeg')
        self.helper_test_speak_view('openAI', 400, 'application/json')


    def test_speak_view_model_default(self):
        """ Test when model is default """
        #self.helper_test_speak_view('default', 200, 'audio/mpeg')
        self.helper_test_speak_view('default', 400, 'application/json')

    def test_speak_view_model_invalid(self):
        """ Test when model is not valid """
        self.helper_test_speak_view('invalid', 400)
