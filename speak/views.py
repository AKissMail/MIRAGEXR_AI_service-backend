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
        if serializer.validated_data['model'] in valid_openai_voices():
            r = speak_open_ai(data)
            if isinstance(r, dict):
                return Response(r, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return StreamingHttpResponse(r, content_type='audio/mpeg')
        if serializer.validated_data['model'] in valid_google_voices():
            return speak_google(data)
        else:
            return Response({"message": "'model' not found"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
