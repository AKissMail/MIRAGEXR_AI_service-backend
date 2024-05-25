import json
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_options(request):
    """
    Retrieves the options from the configuration file.

    Parameters:
    - request: HttpRequest object representing the incoming request.

    Returns:
    - If the request has the appropriate permissions, retrieves the options from the configuration file and returns a
      JSON response containing the options with a status code of 200 (OK).
    - If the request does not have the appropriate permissions, returns a JSON response with an error message and a
      status code of 405 (Method Not Allowed).
    """
    if permission_classes:
        file_path = os.path.join(os.path.dirname(__file__), '../config/options.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return Response(config, status=status.HTTP_200_OK)
    else:
        return Response({"message": "GET-Request only!"}, status=status.HTTP_400_BAD_REQUEST)
