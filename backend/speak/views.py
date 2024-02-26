from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .openAI import speakOpenAI


class SpeakSerializer(serializers.Serializer):
    """
       Serializer for validating request data for the speak endpoint.
       Attributes:
           speakOut (CharField): The text content to be converted into speech.
           model (CharField): Specifies the speech synthesis model to be used. Defaults to "openAI"
       """
    speakOut = serializers.CharField(required=True)
    model = serializers.CharField(default="openAI")


@api_view(['POST'])
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
            r = speakOpenAI(serializer.validated_data)
            return HttpResponse(r, content_type='audio/mpeg')
        else:
            return Response({"message": "'model' not found"}, status=400)
    else:
        return Response({"message": "Data is not correctly formatted. Follow this pattern: "
                                    "'speakOut': $Content, 'voice': $preferred voice or 'default', "
                                    "'model': $preferred model or 'default', 'speed': $speech speed"}, status=400)
