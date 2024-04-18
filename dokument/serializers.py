from rest_framework import serializers


class DokumentSerializer(serializers.Serializer):
    document = serializers.FileField()
    name = serializers.CharField()
    database = serializers.CharField()
