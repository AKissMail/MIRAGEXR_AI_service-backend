from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .wisperOpenAI import wisperOpenAI
from .whisperNationalLibraryofNorway import whisperNationalLibraryofNorway

'''This View implements the listen endpoint, checks the send data for the correct format, pass it on to the 
correct model or returns an error to the client.'''


class ListenSerializer(serializers.Serializer):
    model = serializers.CharField()
    audio = serializers.FileField()


@api_view(['POST'])
def listen(request):
    if request.method == 'POST':
        serializer = ListenSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data['model'] in ("wisper", "default"):
                return wisperOpenAI(serializer.data)
            if serializer.data['model'] in "norwegian ":
                return whisperNationalLibraryofNorway(serializer.data)
            else:
                return Response({"message": "'model' not found"}, status=400)
        else:
            return Response({"message": "Data is not correctly formatted."
                                        " Follow this pattern: 'model': $preferred model or "
                                        "'default', 'audio': your payload as MP3"}, status=400)
    return Response({"message": "POST-Request only!"}, status=405)
