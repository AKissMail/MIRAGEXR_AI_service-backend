from openai import OpenAI
from rest_framework import status
from think.serializers import ThinkSerializer
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
        if serializer.validated_data["model"] in ("gpt-4-turbo-preview", "['gpt-4-turbo-preview']"):
            model = "gpt-4-turbo"
        elif serializer.validated_data["model"] in ("gpt-4o", "['gpt-4o']"):
            model = "gpt-4o"
        else:
            model = "gpt-3.5-turbo"
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model=model,
                messages=message_template
            )
            try:
                msg_content = response.choices[0].message.content
                response = HttpResponse(msg_content, status=status.HTTP_200_OK)
                return response
            except Exception as e:
                raise

        except Exception as _:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Input data is invalid.", "details": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
