from importlib import import_module

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from .llm_models.gpt_open_ai import gpt as openai_gpt
from .serializers import ThinkSerializer
from .think_model_factory import ThinkModelFactory


def prompt_with_configuration(validated_data, final_document, config):
    """
    Prompt with Configuration
    Prompts the LLM model with the given configuration and returns the response.
    Parameters:
    - validated_data (dict): The validated data message, context, and document.
    - final_document (Response): The final document as a response object.
    - config (dict): The configuration settings.
    Returns:
    - The response from the LLM model.
    """
    if isinstance(final_document, Response):
        return final_document

    gpt_prompt = validated_data
    gpt_prompt['message'] = (
            config['prompt_start'] +
            "User Message: {}\n\n"
            "User Context: {}\n\n"
            "Databases Document: {}\n\n" +
            config['prompt_end']
    ).format(validated_data['message'], validated_data['context'], final_document)
    gpt_prompt['context'] = (
            config['context_start'] +
            config['context_end']
    )
    gpt_prompt['model'] = config['model']

    if config['provider'] == 'openai':
        print(gpt_prompt)
        response = openai_gpt(gpt_prompt)
    else:
        return Response("Error: Unknown provider specified in configuration.", status=status.HTTP_400_BAD_REQUEST)
    return response


def rag_manager(data):
    """
    Perform RAG management based on provided data.
    Parameters:
    data (dict): The input data for RAG management.
    Returns:
    Response: The response indicating the result of RAG management.
    """
    serializer = ThinkSerializer(data=data)
    if serializer.is_valid():
        try:
            config = ThinkModelFactory.create_model(serializer.validated_data.get('model'))
        except ValueError as e:
            default = {
                "model": "gpt-4o",
                "prompt_start": "",
                "prompt_end": "",
                "context_start": "",
                "context_end": "",
            }
            return prompt_with_configuration(serializer.validated_data, '', default)

        if not all(key in config for key in ('rag_function', 'rag_function_call')):
            return "'error': 'Configuration is missing required keys.'"

        try:
            rag_function_module = import_module(f'think.rag_models.{config["rag_function"]}')
            rag_function = getattr(rag_function_module, config["rag_function_call"])
        except (ImportError, AttributeError) as e:
            print(e)
            return Response(f"Error: Could not find specified RAG function '{config['rag_function']}'. {str(e)}",
                            status=status.HTTP_400_BAD_REQUEST)

        document = rag_function(serializer.validated_data)

        return prompt_with_configuration(serializer.validated_data, document, config)
    else:
        return Response("Error: Input data is invalid! Details :" + serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
