import requests
from django.http import StreamingHttpResponse
from django.conf import settings
from .serializers import SpeakOpenAISerializer

'''
This it the wrapper for the OpenAI API, which allows you to crate an Voice based on a given String.
'''


def speak_open_ai(request):
    """
    Generates voice audio from a text using OpenAI's Text-to-Speech (TTS) API based on the provided parameters.
        Parameters:
        data (dict): A dictionary containing the following keys:
            - speakOut (str): The text to be converted into speech.
            - voice (str): The voice model to use for the speech. Valid options are "alloy", "echo", "fable",
                           "onyx", "nova", and "shimmer". If default is send as an option it will use the onyx voice.
            - Speed (float): The speed at which the speech should be delivered. Affects the pace of the resulting audio.

    Returns:
        StreamingHttpResponse: A Django StreamingHttpResponse object containing the audio stream.
        On success:
            - dict: A dictionary containing an error message if the API request failed.
        On fail:
            - str: A string with an errormessage.
    """
    serializer = SpeakOpenAISerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['voice'] in ("alloy", "echo", "fable", "onyx", "nova", "shimmer", "default"):
            if serializer.validated_data['voice'] == "default":
                serializer.validated_data['voice'] = "onyx"
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
            return {
                "error": "Error: Voice not found! I know: 'alloy', 'echo', 'fable', 'onyx', 'nova', and 'shimmer'"}
    else:
        return serializer.errors + request
