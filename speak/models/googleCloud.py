import base64
import json
import os
from http import HTTPStatus
from io import BytesIO

import requests
from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response

from speak.serializers import SpeakGoogleSerializer


def speak_google(request):
    """
    Speak Google.

    This method sends a request to the Google Text-to-Speech API to convert text into speech. It takes a request
    parameter and returns the generated audio as a streaming response.

    Parameters:
    - request: A dictionary representing the request data containing the following fields:
      - 'model': The language model to use for generating the speech (required).
      - 'message': The text message to convert into speech (required).

    Returns:
    A streaming HTTP response object containing the generated audio in the 'audio/mpeg' format.

    Example usage:
    request =
    {
        'model': 'en-US-Wavenet-D',
        'message': 'Hello, how are you?'
    }
    response = speak_google(request)
    """
    serializer = SpeakGoogleSerializer(data=request)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    language_code, ssml_gender = get_language_and_gender(serializer.validated_data.get('model'))
    if language_code is None:
        return Response(
            {"Error": "Invalid model specified. Model must be one of the following: {0}".format(valid_google_voices())},
            status=status.HTTP_400_BAD_REQUEST)

    key = settings.GOOGLE_API_KEY
    headers = {'Content-Type': 'application/json'}
    data = compose_request_data(language_code, ssml_gender, serializer.validated_data['message'])

    response = send_post_request_to_google_api(headers, data, key)
    if response.status_code != 200:
        return Response({"error": f"Error from Google API: {response.status_code} - {response.text}"},
                        status=response.status_code)

    return StreamingHttpResponse(
        streaming_content=generate_audio_stream(response),
        content_type="audio/mpeg"
    )


def get_language_and_gender(model):
    """
    Returns the language and gender for a given model.

    Parameters:
    model (str): The name of the model.

    Returns:
    tuple: A tuple containing the language and gender of the model.
        The first element is the language code (e.g. "el-GR").
        The second element is the gender (e.g. "FEMALE").

    Example:
        >>> get_language_and_gender("Greek")
        ("el-GR", "FEMALE")
        >>> get_language_and_gender("English")
        (None, None)
    """
    file_path = os.path.join(settings.BASE_DIR, 'config', 'speak', 'google.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
            if model in config['Voice_details']:
                language, gender = config['Voice_details'][model]
                return language, gender
            else:
                return None, None
    except FileNotFoundError:
        return None, None


def compose_request_data(language_code, ssml_gender, message):
    """
    Composes the request data for a text-to-speech API call.

    Args:
        language_code (str): The language code for the requested voice.
        ssml_gender (str): The SSML gender for the requested voice.
        message (str): The text message to be synthesized into speech.

    Returns:
        dict: The request data in the following format:
              {
                "input": {"text": message},
                "voice": {"languageCode": language_code, "ssmlGender": ssml_gender},
                "audioConfig": {"audioEncoding": "MP3"}
              }
    """
    return {
        "input": {"text": message},
        "voice": {"languageCode": language_code, "ssmlGender": ssml_gender},
        "audioConfig": {"audioEncoding": "MP3"}
    }


def send_post_request_to_google_api(headers, data, key):
    """
    Send a POST request to the Google API.

    :param headers: The headers for the request.
    :type headers: dict
    :param data: The data to include in the request body.
    :type data: dict
    :param key: The API key to authenticate the request.
    :type key: str
    :return: The response from the API.
    :rtype: requests.Response
    """
    return requests.post(f"{settings.GOOGLE_TTS_ENDPOINT}?key={key}", headers=headers, json=data)


def generate_audio_stream(response):
    """
    Generates an audio stream from the given response.

    :param response: The response object containing the audio content.
    :type response: object

    :return: The audio stream generated from the response.
    :rtype: object
    """
    audio_content_base64 = json.loads(response.text)['audioContent']
    audio_content = base64.b64decode(audio_content_base64)
    return generate_chunked_audio_stream(audio_content)


def generate_chunked_audio_stream(audio_content):
    """
    Generates audio chunks from the given audio content.

    Args:
        audio_content (bytes): The audio content to generate chunks from.

    Yields:
        bytes: The generated audio chunk.

    """
    audio_stream = BytesIO(audio_content)
    audio_stream.seek(0)
    while True:
        chunk = audio_stream.read(1024)
        if not chunk:
            break
        yield chunk


def valid_google_voices():
    """
    Returns a tuple of valid voices for Google API:
    """
    file_path = os.path.join(settings.BASE_DIR, 'config', 'speak', 'google.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
            voices = tuple(config['valid_openai_voices'])
            return voices
    except FileNotFoundError:
        return HttpResponse("Config file not found.", status=HTTPStatus.INTERNAL_SERVER_ERROR)
