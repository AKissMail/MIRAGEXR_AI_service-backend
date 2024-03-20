from rest_framework.permissions import IsAuthenticated

from .serializers import SpeakSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .openAI import speak_open_ai


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def speak(request):
    """
       Processes POST requests sent to the speak endpoint, validates the request data, and uses the specified
       speech synthesis model to generate speech from text.
       Parameters:
           request (Request): The REST framework request object containing the parameters for speech synthesis.

       Returns:
           HttpResponse or Response: Depending on the outcome, it returns an HttpResponse containing the audio
           content if the request is successful, or a Response object with an error message if the request fails
           validation or if an unsupported model is specified.
       """

    serializer = SpeakSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in ("openAI", "default"):
            r = speak_open_ai(request)
            if isinstance(r, dict):
                return Response(r, status=500)
            return StreamingHttpResponse(r, content_type='audio/mpeg')
        else:
            return Response({"message": "'model' not found"}, status=400)
    else:
        return Response({"message": "Data is not correctly formatted. Follow this pattern: "
                                    "'speakOut': $Content, 'voice': $preferred voice or 'default', "
                                    "'model': $preferred model or 'default', 'speed': $speech speed"}, status=400)
