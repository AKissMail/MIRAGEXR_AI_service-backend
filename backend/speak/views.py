from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .openAI import speakOpenAI
'''
This is the view for the speak endpoint, at the moment it validates the request before it get send to the diffrent model. 
By now the OpenAI API in implement.'''

class SpeakSerializer(serializers.Serializer):
    speakOut = serializers.CharField(required=True)
    voice = serializers.CharField(required=True)
    model = serializers.CharField(required=True)
    speed = serializers.FloatField(required=True)


@api_view(['POST'])
def speak(request):
    if request.method == 'POST':
        serializer = SpeakSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['model'] in ("openAI", "default"):
                r = speakOpenAI(serializer.data)
                return HttpResponse(r, content_type='audio/mpeg')
            if serializer.data['model'] == '':
                pass
            else:
                return Response({"message": "'model' not found"}, status=400)
        else:
            return Response({"message": "Data is not corecley formatted. Follow this pattern:'speakOut': $Content, "
                                        "'voice': $preferred voice or 'default' , 'model': $preferred model or "
                                        "'default'"}, status=400)
    return Response({"message": "POST-Request only!"}, status=405)
