from rest_framework import serializers


class ThinkSerializer(serializers.Serializer):
    """
     Serializer for validating and deserializing input data for the think view function. This serializer defines
     the expected in the following Fields:
     - model (serializers.CharField): The AI model to use for generating a response.
     - message (serializers.CharField): The message or query to process.
     - context (serializers.CharField): The context in which the message or query should be processed.
     """
    model = serializers.CharField(default="gpt-3.5-turbo")
    message = serializers.CharField()
    context = serializers.CharField()
    subModel = serializers.CharField(required=False)
