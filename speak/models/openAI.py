import os
import json
from http import HTTPStatus

import requests
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from speak.serializers import SpeakOpenAISerializer


def speak_open_ai(request):
    """
    Perform OpenAI text-to-speech using the provided request data.

    Parameters:
    - request: The request data containing the text to convert and the model to use.

    Returns:
    - If the request is valid and the model is supported, returns the OpenAI response from successful conversion.
    - If there was an error in the conversion process, returns an error response with the corresponding status code
      and error message.
      Example: "Error: 500 - Internal Server Error".
    - If the model is not valid or supported, returns an error response indicating the available models.

    Note: This method expects a valid request in the form of a dictionary.

    Usage:
    - Create a dictionary with the required request parameters.
    - Call this method with the request dictionary as an argument.
    """
    serializer = SpeakOpenAISerializer(data=request)
    if serializer.is_valid():
        model = serializer.validated_data['model']
        if model in valid_openai_voices():
            response = fetch_openai_response(serializer)
            if response is not None:
                return response
            else:
                return error_response(f"Error: {response.status_code} - {response.text}")
        else:
            return available_models_error_response()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def valid_openai_voices():
    """
    Returns a tuple of valid voices for OpenAI.
    """
    file_path = os.path.join(settings.BASE_DIR, 'config', 'speak', 'openai.json')
    print(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
            voices = tuple(config['valid_openai_voices'])
            return voices
    except FileNotFoundError:
        return HttpResponse("Config file not found.", status=HTTPStatus.INTERNAL_SERVER_ERROR)


def fetch_openai_response(serializer):
    """
    Fetch OpenAI response.

    Parameters:
    - serializer (Serializer): The serializer containing validated data.

    Returns:
    - StreamingHttpResponse: The streaming HTTP response with audio content if the request is successful.
    - None: If the request is not successful.

    Example Usage:
        serializer = MySerializer(data=request.data)
        if serializer.is_valid():
            response = fetch_openai_response(serializer)
            if response:
                return response
            else:
                return Response("Request Failed", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    url = "https://api.openai.com/v1/audio/speech"
    headers = {"Authorization": f'Bearer {settings.OPENAI_API_KEY}'}
    data = {
        "model": "tts-1",
        "input": serializer.validated_data['message'],
        "voice": serializer.validated_data['model'],
        "speed": serializer.validated_data['speed']
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code == 200:
        def generate():
            for chunk in response.iter_content(chunk_size=1024):
                yield chunk

        return StreamingHttpResponse(
            streaming_content=generate(),
            content_type="audio/mpeg"
        )
    return None


def error_response(err_msg):
    """
    Returns a dictionary containing an error message.

    Parameters:
    err_msg (str): The error message to be included in the response.

    Returns:
    dict: A dictionary with the key "error" and the value of the error message.
    """
    return {"error": err_msg}


def available_models_error_response():
    """
    Returns an error response if a model is not found.

    :return: A dictionary containing the error message.
    :rtype: dict
    """
    return {
        "error": "Error: Model not found! Options that are available are " + ', '.join(valid_openai_voices())
    }
