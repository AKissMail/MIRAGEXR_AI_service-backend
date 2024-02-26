import requests
from django.http import StreamingHttpResponse
from django.conf import settings
from rest_framework import serializers

'''
This it the wrapper for the OpenAI API, which allows you to crate an Voice based on a given String.
'''
class SpeakOpenAISerializer(serializers.Serializer):
    """
       Serializer for validating request data for the speakOpenAI methode.
       Attributes:
           voice (CharField): The preferred voice model to use for speech synthesis. The Default is 'onyx' but also
           allowed: 'alloy', 'echo', 'fable', 'onyx', 'nova', and 'shimmer'
           speed (FloatField): The speed of the speech output. Can be between 0.25 and 4.
       """
    speakOut = serializers.CharField(required=True)
    voice = serializers.CharField(default="onyx")
    speed = serializers.FloatField(default=1, min_value=0.25, max_value=4)


def speakOpenAI(data):
    """
    Generates voice audio from text using OpenAI's Text-to-Speech (TTS) API based on the provided parameters.

    This function sends a request to the OpenAI API to convert text (specified in the `data` dictionary) into
    speech audio. It supports specifying the voice and speed of the speech. The audio is streamed back to the
    client as a response.

    Parameters:
        data (dict): A dictionary containing the following keys:
            - speakOut (str): The text to be converted into speech.
            - voice (str): The voice model to use for the speech. Valid options are "alloy", "echo", "fable",
                           "onyx", "nova", and "shimmer".
            - speed (float): The speed at which the speech should be delivered. Affects the pace of the resulting audio.

    Returns:
        StreamingHttpResponse: A Django StreamingHttpResponse object containing the audio stream if the request
        was successful and the specified voice is supported.

        dict: A dictionary containing an error message if the API request failed.

        str: A string message indicating that the specified voice is not supported if the `voice` parameter
        does not match any of the expected voice models.

    This wrapper function for the OpenAI API handles the construction and sending of the request to the API,
    including authentication using the OPENAI_API_KEY setting from Django's settings. If the voice specified is
    not among the supported voices, it immediately returns a message indicating the available options without
    making an API request. If the request is successful and returns a 200 status code, it streams the audio
    content back. For non-200 responses, it returns the error details from the API.
    """
    serializer = SpeakOpenAISerializer(data)
    if serializer.is_valid():
        if serializer.validated_data['voice'] in ("alloy", "echo", "fable", "onyx", "nova", "shimmer"):
            url = "https://api.openai.com/v1/audio/speech"
            headers = {
                "Authorization": f'Bearer {settings.OPENAI_API_KEY}',
            }
            data = {
                "model": "tts-1",
                "input": serializer.validated_data['speakOut'],
                "voice": serializer.validated_data['voice'],
                "speed": serializer.validated_data['speed']
            }

            response = requests.post(url, headers=headers, json=data, stream=True)
            if response.status_code == 200:
                def generate():
                    for chunk in response.iter_content(chunk_size=1024):
                        print(f"Chunk size: {len(chunk)}")
                        yield chunk
                return StreamingHttpResponse(
                    streaming_content=generate(),
                    content_type="audio/mpeg"
                )
            else:
                return {"error": f"Error: {response.status_code} - {response.text}"}
        else:
            return "Voice not found! I know: 'alloy', 'echo', 'fable', 'onyx', 'nova', and 'shimmer'"
    else:
        return serializer.errors
