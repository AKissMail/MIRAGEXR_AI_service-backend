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
    """
    Serializer for handling SpeakOpenAI requests.
    Attributes:
    - speed (FloatField): A field for specifying the speed of the speech. The default value is 1, and it must be between 0.25 and 4.
    - message (CharField): A required field for the message to be converted to speech.
    - model (CharField): A required field for specifying the model to be used for the speech synthesis.

    """
    speed = serializers.FloatField(default=1, min_value=0.25, max_value=4)
    message = serializers.CharField(required=True)
    model = serializers.CharField(required=True)


class SpeakGoogleSerializer(serializers.Serializer):
    """
    A serializer class for Google Text-to-Speech API.

    Attributes:
        message (str): The text message to be converted into speech.
        model (str): The language and voice model to be used for speech synthesis.
    """
    message = serializers.CharField(required=True)
    model = serializers.CharField(required=True)