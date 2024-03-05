import json
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_options(request):
    """
    Handles GET requests to retrieve configuration options from './options.json'.
    Returns:
        Response: A DRF Response object containing the parsed JSON data with a 200 OK status.
    """
    if permission_classes:
        file_path = os.path.join(os.path.dirname(__file__), '../config/options.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return Response(config, status=200)
    else:
        return Response({"message": "GET-Request only!"}, status=405)
