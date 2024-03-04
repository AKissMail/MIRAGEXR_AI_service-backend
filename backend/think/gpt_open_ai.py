from openai import OpenAI
from .serializers import ThinkSerializer


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
        return {"error": "Input data is invalid.", "details": serializer.errors}
