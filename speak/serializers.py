from rest_framework import serializers


class SpeakSerializer(serializers.Serializer):
    """
       Serializer for validating request data for the "speak" endpoint.
       Attributes:
           - message (CharField): The text content to be converted into speech.
           - model (CharField): Specifies the speech synthesis model to be used.
             Defaults to "openAI"
       """
    message = serializers.CharField(required=True)
    model = serializers.CharField(required=True)


class SpeakOpenAISerializer(serializers.Serializer):

    speed = serializers.FloatField(default=1, min_value=0.25, max_value=4)
