import base64
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import SpeakSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from speak.models.openAI import speak_open_ai, valid_openai_voices
from speak.models.googleCloud import speak_google, valid_google_voices


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def speak(request):
    """
       Processes GET requests sent to the speak endpoint, validates the request data, and uses the specified
       speech synthesis model to generate speech from text.
       Parameters:
           request (Request): The REST framework request object containing the parameters for speech synthesis.

       Returns:
           HttpResponse or Response: Depending on the outcome, it returns an HttpResponse containing the audio
           content if the request is successful, or a Response object with an error message if the request fails
           validation or if an unsupported model is specified.
       """

    data = {
        'model': request.headers.get('model'),
        'message': base64.b64decode(request.headers.get('message')).decode('utf-8'),
        'speed': request.headers.get('speed', 1)
    }
    print(data)
    serializer = SpeakSerializer(data=data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in valid_openai_voices(True):
            response = speak_open_ai(data)
            if isinstance(response, dict):
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif response is None:
                return Response({"detail": "Could not fetch response from OpenAI"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif isinstance(response, StreamingHttpResponse):
                return response

        if serializer.validated_data['model'] in valid_google_voices():
            return speak_google(data)
        else:
            defaultdata = {
                'model': valid_openai_voices(False)[0],
                'message': base64.b64decode(request.headers.get('message')).decode('utf-8'),
                'speed': request.headers.get('speed', 1)
            }
            response = speak_open_ai(defaultdata)
            if isinstance(response, dict):
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif response is None:
                return Response({"detail": "Could not fetch response from OpenAI"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif isinstance(response, StreamingHttpResponse):
                return response
            else:
                return Response({"detail": "Unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
