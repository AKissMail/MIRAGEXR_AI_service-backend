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
    model = serializers.CharField(default="openAI")


class SpeakOpenAISerializer(serializers.Serializer):
    """
       Serializer for validating request data for the speakOpenAI methode.
       Attributes:
           submodel (CharField): The preferred voice model to use for speech synthesis. The Default is 'onyx' but also
           allowed: 'alloy', 'echo', 'fable', 'onyx', 'nova', and 'shimmer'
           speed (FloatField): The speed of the speech output. Can be between 0.25 and 4.
       """
    message = serializers.CharField(required=True)
    submodel = serializers.CharField(default="onyx")
    speed = serializers.FloatField(default=1, min_value=0.25, max_value=4)
