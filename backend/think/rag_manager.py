from .gpt_open_ai import gpt
from rest_framework import serializers


class ThinkRAGSerializer(serializers.Serializer):
    model = serializers.CharField()
    message = serializers.CharField()
    context = serializers.CharField()


def norwegian_on_the_web(validated_data):
    return gpt(validated_data)


def manager(data):
    serializer = ThinkRAGSerializer(data=data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in 'norwegian-on-the-web':
            norwegian_on_the_web(serializer.validated_data)
        else:
            return {"error": "RAG model not found"}
    else:
        return {"error": "Input data is invalid.", "details": serializer.errors}


def gpt_rag():
    return None