from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


class RagViewSerializer(serializers.Serializer):
    model = serializers.CharField()
    response_format = serializers.JSONField(default={"type": "json_object"})
    message = serializers.CharField()
    context = serializers.CharField()

@api_view(['POST'])
def now(request):
    serializer = RagViewSerializer(data=request.data)
    if serializer.is_valid():
        print(request.data)
        return Response("HI", status=200)
    else:
        return Response(serializer.errors, status=400)
