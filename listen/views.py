from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import ListenSerializer
from listen.models.whisperNBAiLab import whisper_nb_ai_lab
from listen.models.whisperOpenAI import whisper_open_ai_remote, wisper_open_ai_local
from listen.audio_utility.audio_transformator import AudioTransformator





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
                response_data = wisper_open_ai_local(AudioTransformator.handleBinary(validated_data))
            else:
                response_data = whisper_open_ai_remote(validated_data)
            return Response(response_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
                            "error": "Data is not correctly formatted. Follow this pattern: 'model': $preferred model "
                                     "or 'default', 'message': your payload as mp3, wav or ogg"},
                        status=status.HTTP_400_BAD_REQUEST)