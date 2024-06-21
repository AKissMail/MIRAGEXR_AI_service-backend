import base64
import subprocess

from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ListenSerializer
from listen.models.whisperNBAiLab import whisper_nb_ai_lab
from listen.models.whisperOpenAI import whisper_open_ai_remote


def handleBinary(validated_data):
    """
    Handle binary data.

    This method takes in a dictionary of validated data and performs the following tasks:
    1. If the 'message' key exists in the validated data dictionary, it reads the first 4 bytes of the message/
    2. Seeks the message back to the beginning.
    3. Converts the WAV data in the message to MP3 format using the 'convert_wav_to_mp3' function.
    4. Base64 encodes the MP3 data.
    5. Creates a ContentFile object from the base64 decoded MP3 data with the name "demo.mp3".
    6. Replaces the 'message' key in the validated data dictionary with the content file.
    7. Writes the content of the content file to a file named "demo.mp3".
    8. Returns the modified validated data dictionary.

    Parameters:
        validated_data (dict): A dictionary of validated data.

    Returns:
        dict: The modified validated data dictionary.
    """
    if validated_data['message']:
        header = validated_data['message'].read(4)
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
    """
    Converts a WAV audio file to an MP3 audio file using FFmpeg.
    """
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
        error_message = stderr.decode()
        print(f"FFmpeg error: {error_message}")
        raise Exception(f"FFmpeg error: {error_message}")

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
        validated_data = serializer.validated_data
        try:

            audio_file = validated_data['message']
            if hasattr(audio_file, 'content_type'):
                audio_format = audio_file.content_type.split('/')[-1]
            else:
                audio_format = 'octet-stream'

            supported_formats = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']
            if audio_format not in supported_formats:
                return Response({"error": f"Invalid file format. Supported formats: {supported_formats}"}, status=status.HTTP_400_BAD_REQUEST)

            if validated_data['model'].strip() == "Norwegian":
                response_data = whisper_nb_ai_lab(validated_data)
            elif validated_data['model'].strip() == "BinaryWhisperOpenAILocal":
                response_data = whisper_open_ai_remote(handleBinary(validated_data))
                print(response_data)
            else:
                response_data = whisper_open_ai_remote(validated_data)
            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
                            "error": "Data is not correctly formatted. Follow this pattern: 'model': $preferred model or 'default', 'message': your payload as mp3, wav or ogg"},
                        status=status.HTTP_400_BAD_REQUEST)