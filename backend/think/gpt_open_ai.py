from openai import OpenAI
from rest_framework import serializers
import logging


class ThinkOpenAISerializer(serializers.Serializer):
    model = serializers.CharField()
    response_format = serializers.CharField(default="json_object")
    message = serializers.CharField()
    context = serializers.CharField()


def gpt(data):
    serializer = ThinkOpenAISerializer(data=data)
    if serializer.is_valid():
        message_template = [
            {"role": "system", "content": serializer.validated_data["context"]},
            {"role": "user", "content": serializer.validated_data["message"]}
        ]
        response_format_template = [{type: serializer.validated_data["response_format"]}]

        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model=serializer.validated_data['model'],
                #response_format=response_format_template,
                messages=message_template
            )
            return response.choices[0].message.content
        except Exception as e:
            # Log the OpenAI API error
            return {"error": "An error occurred while processing your request."}
    else:
        # todo  logger.error(f"Validation error: {serializer.errors}")
        return {"error": "Input data is invalid.", "details": serializer.errors}
