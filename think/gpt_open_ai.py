from openai import OpenAI

from .serializers import ThinkSerializer
from rest_framework.response import Response
from django.http import HttpResponse


def gpt(data):
    """
      Processes input data to generate a response using the OpenAI GPT model.
      Parameters:
      - data (dict): Input data containing the context, message, and model to be used
        for generating a response.
        Expected keys:
            - 'context': The context of the request.
            - 'message': The message of the request.
            - 'model': The model to be in the request.

      Returns:
      - dict or str: If successful, returns the generated message as a string. If an
        error occurs or the input is invalid, returns an error.
      """
    serializer = ThinkSerializer(data=data)
    if serializer.is_valid():

        message_template = [
            {"role": "system", "content": serializer.validated_data["context"]},
            {"role": "user", "content": serializer.validated_data["message"]}
        ]
        if serializer.validated_data["model"] in ["gpt-4-turbo-preview"]:
            model = "gpt-4-turbo-preview"
        else:
            model = "gpt-3.5-turbo"
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model=model,
                messages=message_template
            )
            try:
                response =HttpResponse(response.choices[0].message.content, status=200)
                return response
            except Exception as e:
                return Response({"error": str(e)}, status=500)

        except Exception as _:
            return Response({"error": "An unexpected error occurred."}, status=500)
    else:
        return Response({"error": "Input data is invalid.", "details": serializer.errors}, status=403)
