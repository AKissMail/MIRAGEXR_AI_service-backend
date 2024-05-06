from rest_framework.permissions import IsAuthenticated

from .serializers import SpeakSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .openAI import speak_open_ai


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
        'message': request.headers.get('message'),
        'speed': request.headers.get('speed', 1)
    }
    serializer = SpeakSerializer(data=data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in ("alloy", "echo", "fable", "onyx", "nova", "shimmer"):
            r = speak_open_ai(data)
            if isinstance(r, dict):
                return Response(r, status=500)
            return StreamingHttpResponse(r, content_type='audio/mpeg')
        else:
            return Response({"message": "'model' not found"}, status=400)
    else:
        return Response(serializer.errors, status=400)
