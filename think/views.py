from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ThinkSerializer
from .gpt_open_ai import gpt
from .rag_manager import rag_manager


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def think(request):
    """
       API view that processes incoming requests to generate responses using specified AI models. This view accepts
       POST requests and verifies the containing data before it passes the request on to the specific handler
       (GPT or RAG manager) to generate a response.

       Parameters:
       - request (Request): The REST framework request object containing the data.
       Returns:
       - Response: A REST framework response object containing the generated response from the AI model or
         an error message.
    """
    serializer = ThinkSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in ('gpt-3.5-turbo', 'gpt-4-turbo-preview', 'Default'):
            return gpt(serializer.validated_data)
        if serializer.validated_data['model'] in 'vector':
            return rag_manager(serializer.validated_data)
        else:
            return Response({"error": "Invalid model"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
