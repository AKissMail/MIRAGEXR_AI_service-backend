from openai import OpenAI
from rest_framework import serializers
import logging


class ThinkOpenAISerializer(serializers.Serializer):
    model = serializers.CharField()
    message = serializers.CharField()
    context = serializers.CharField()


def gpt(data):
    serializer = ThinkOpenAISerializer(data=data)
    print(serializer.is_valid())
    if serializer.is_valid():
        message_template = [
            {"role": "system", "content": serializer.validated_data["context"]},
            {"role": "user", "content": serializer.validated_data["message"]}
        ]

        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model=serializer.validated_data['model'],
                messages=message_template
            )
            return response.choices[0].message.content
        except Exception as e:

            return {"error": "An error occurred while processing your request." + e.__str__()}
    else:
        # todo  logger.error(f"Validation error: {serializer.errors}")
        return {"error": "Input data is invalid.", "details": serializer.errors}
