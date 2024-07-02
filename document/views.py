import json
import os
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .handleData import handle_data
from .serializers import ConfigurationSerializer, OptionSerializer
from .serializers import DocumentSerializer
from .config_utility import compose_cofig


@api_view(['POST'])
@permission_classes([IsAdminUser])
def document(request):
    """
    Create a new document with the specified configuration.

    Parameters:
    - request: HTTP request object

    Returns:
    - Response object
    """
    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        config_name = serializer.validated_data.get('config_name')
        if not config_name:
            return Response({'error': 'Config name is required'}, status=status.HTTP_400_BAD_REQUEST)

        result = handle_data(serializer.validated_data, config_name)
        if result:
            return Response(
                f"Document {serializer.validated_data['name']} added to {serializer.validated_data['database']}",
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'Invalid file type, processing error or Configuration not found '},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def configuration(request):
    """
    Saves or deletes configuration based on the given parameters and updates the option.json file

    Parameters:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response object.

    Raises:
        HttpResponse: If there is an internal server error.

    """
    serializer = ConfigurationSerializer(data=request.data)
    if serializer.is_valid():
        booleans = [
            serializer.validated_data['update_database'],
            serializer.validated_data['new_database'],
            serializer.validated_data['delete_database']
        ]
        if sum(bool(val) for val in booleans) == 1:
            if serializer.validated_data['new_database'] or serializer.validated_data['update_database']:
                try:
                    config: dict[str, Any] = {
                        'prompt_start': serializer.validated_data['prompt_start'],
                        'prompt_end': serializer.validated_data['prompt_end'],
                        'context_start': serializer.validated_data['context_start'],
                        'context_end': serializer.validated_data['context_end'],
                        "provider": serializer.validated_data['provider'],
                        "model": serializer.validated_data['model'],
                        "rag_function": serializer.validated_data['rag_function'],
                        "rag_function_call": serializer.validated_data['rag_function_call'],
                        "apiName": serializer.validated_data['apiName'],
                        "name": serializer.validated_data['name'],
                        "description": serializer.validated_data['description']
                    }
                    configurationJson = json.dumps(config)
                    configurationJsonPath = os.path.join(os.path.join(settings.BASE_DIR, 'config', 'think', ),
                                                         serializer.validated_data['database_name'] + '.json')
                    with open(configurationJsonPath, mode='w') as file:
                        file.write(configurationJson)
                    compose_cofig.update_options_json()
                    return Response({'Configuration is created!'}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return HttpResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if serializer.validated_data['delete_database']:
                try:
                    os.remove(
                        os.path.join(settings.BASE_DIR, 'config', 'think', serializer.validated_data['database_name'] +
                                     '.json'))
                    compose_cofig.update_options_json()
                    return Response({'delete Config': True}, status=status.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    return HttpResponse('Error: Database dose not exist!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Invalid booleans, exactly one boolean should be True.'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
