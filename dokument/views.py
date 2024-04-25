import os
from typing import Dict, Any

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.conf import settings

from .handelData import handelDokument
from .serializers import DocumentSerializer, ConfigurationSerializer

import json


@api_view(['POST'])
@permission_classes([IsAdminUser])
def dokument(request):
    """
    Create a new document.

    Parameters:
    - request: HTTP request object

    Returns:
    - Response object

    Raises:
    - None
    """
    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        result = handelDokument(serializer.validated_data)
        if result:
            return Response(
                "Document " + serializer.validated_data['name'] + "added to " + serializer.validated_data['database'],
                status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def configuration(request):
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
                    }
                    configurationJson = json.dumps(config)
                    configurationJsonPath = os.path.join(os.path.join(settings.BASE_DIR, 'config'),
                                                         serializer.validated_data['database_name'] + '.json')
                    with open(configurationJsonPath, mode='w') as file:
                        file.write(configurationJson)
                    return Response({'configurationJson': configurationJsonPath}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return HttpResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if serializer.validated_data['delete_database']:
                try:
                    os.remove(os.path.join(settings.BASE_DIR, 'config', serializer.validated_data['database_name'] +
                                           '.json'))
                    return Response({'delete Config': True}, status=status.HTTP_200_OK)
                except Exception as e:
                    print(e)
                    return HttpResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Invalid booleans, exactly one boolean should be True.'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
