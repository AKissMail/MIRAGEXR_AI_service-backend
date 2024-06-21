from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from think.llm_models.gpt_open_ai import gpt
from .rag_manager import rag_manager
from .serializers import ThinkSerializer


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
        if serializer.validated_data['model'] in (
                "['gpt-3.5-turbo']",
                "['gpt-4-turbo-preview']",
                "gpt-3.5-turbo",
                "gpt-4-turbo-preview",
                "['gpt-4o']",
                "gpt-4o"
        ):
            r = gpt(serializer.validated_data)
        else:
            r = rag_manager(serializer.validated_data)
            if r == "'error': 'Configuration is missing required keys.'":
                return HttpResponse(r, status=status.HTTP_400_BAD_REQUEST)

        return HttpResponse(r, status=status.HTTP_200_OK)
