import base64
import subprocess

from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ListenSerializer
from .whisperNBAiLab import whisper_nb_ai_lab
from .whisperOpenAI import whisper_open_ai_remote, wisper_open_ai_local


def handleBinary(validated_data):
    print(validated_data)
    if validated_data['message']:
        header = validated_data['message'].read(4)
        print(header)
        validated_data['message'].seek(0)
        mp3_data = convert_wav_to_mp3(validated_data['message'])
        base64_encoded = base64.b64encode(mp3_data).decode()
        content_file = ContentFile(base64.b64decode(base64_encoded), name="demo.mp3")
        validated_data['message'] = content_file
        with open("demo.mp3", 'wb+') as destination:
            for chunk in content_file.chunks():
                destination.write(chunk)
        return validated_data


def convert_wav_to_mp3(wav_input):

    command = [
        'ffmpeg',
        '-i', '-',
        '-acodec', 'libmp3lame',
        '-f', 'mp3',
        'pipe:1'
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=wav_input.read())

    if process.returncode != 0:
        raise Exception(f"FFmpeg error: {stderr.decode()}")

    return stdout


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def listen(request):
    """
    Handles the POST request to listen.

    @api_view: Specifies that this view is used for handling API requests.
                The allowed methods for this view are specified in the list within the square brackets.

    @permission_classes: Specifies the permission classes that control access to this view.
                            In this case, only authenticated users are allowed access.

    Parameters:
        - request: The HTTP request object containing the incoming request data.

    Returns:
        - If the request data is valid and the specified model is "whisper" or "default",
          it calls the whisper_open_ai_remote function with the validated data and returns the response.

        - If the specified model is "whisperNBAiLab", it calls the whisper_nb_ai_lab function with the validated data
          and returns the response.

        - If the specified model is "whisperOpenAILocal", it calls the wisper_open_ai_local function with the validated data
          and returns the response.

        - If the specified model is not found, it returns a response with an error message and status code 400.

        - If the request data is not correctly formatted, it returns a response with an error message
          containing the expected pattern for the data and status code 400.
    """
    serializer = ListenSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['model'].strip() == "NO":
            return Response(whisper_nb_ai_lab(serializer.validated_data))
        if serializer.validated_data['model'].strip() == "BinaryWhisperOpenAILocal":
            r = Response(whisper_open_ai_remote(handleBinary(serializer.validated_data)))
            print(r)
            return r
        else:
            return Response(whisper_open_ai_remote(serializer.validated_data))
    else:
        print(request.data)
        return Response({"error": "Data is not correctly formatted."
                                  " Follow this pattern: 'model': $preferred model or "
                                  "'default', 'message': your payload as mp3, wav or ogg"}, status=400)
