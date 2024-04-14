from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ListenSerializer
from .whisperNBAiLab import whisper_nb_ai_lab
from .whisperOpenAI import whisper_open_ai_remote, wisper_open_ai_local


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
                                  "'default', 'message': your payload as mp3, wav or ogg"}, status=400)
