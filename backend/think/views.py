from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from .gpt_open_ai import gpt
from .rag_manager import gpt_rag


class ThinkSerializer(serializers.Serializer):
    model = serializers.CharField(default="gpt-3.5")
    message = serializers.CharField()
    context = serializers.CharField()



@api_view(['POST'])
def think(request):
    serializer = ThinkSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in ('gpt-3.5-turbo', 'gpt-4-turbo-preview'):
            return Response(gpt(serializer.validated_data))
        if serializer.validated_data['model'] in 'norwegian-on-the-web':
            return Response(gpt_rag(serializer.validated_data))
        else:
            return Response({"error": "Invalid model"}, status=400)
    else:
        return Response(serializer.errors, status=400)
