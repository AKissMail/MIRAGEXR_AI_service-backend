from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .whisperOpenAI import whisper_open_ai_remote, wisper_open_ai_local
from .whisperNBAiLab import whisper_nb_ai_lab


class ListenSerializer(serializers.Serializer):
    """
    Serializer for validating request data for the listen endpoint.
    Attributes:
        model (CharField): A string field for specifying the model: Can be either wisper or
        audio (FileField): A file field for uploading the audio file to be processed.
    """

    model = serializers.CharField()
    audio = serializers.FileField()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def listen(request):
    """
     Processes POST requests sent to the listen endpoint, validates the request data,
     and routes the audio file to the specified model for processing and returns the results.
     Parameters:
         request (Request): The REST framework request object containing the model identifier and the audio file.
     Returns:
         Response: A REST framework response object containing the transcription result or an error message.
     """
    serializer = ListenSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in ("whisper", "default"):
            i = whisper_open_ai_remote(serializer.validated_data)
            return Response(i)
        if serializer.validated_data['model'].strip() == "whisperNBAiLab":
            return Response(whisper_nb_ai_lab(serializer.validated_data))
        if serializer.validated_data['model'].strip() == "whisperOpenAILocal":
            return Response(wisper_open_ai_local(serializer.validated_data))
        else:
            return Response({"error": "'model' not found"}, status=400)
    else:
        return Response({"error": "Data is not correctly formatted."
                                  " Follow this pattern: 'model': $preferred model or "
                                  "'default', 'audio': your payload as MP3"}, status=400)
