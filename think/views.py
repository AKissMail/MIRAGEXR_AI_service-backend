from django.http import HttpResponse
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
    print(request.data)
    serializer = ThinkSerializer(data=request.data)
    if serializer.is_valid():
        try:
            if serializer.validated_data['model'] in ("['gpt-3.5-turbo']", "['gpt-4-turbo-preview']"):
                r = gpt(serializer.validated_data)
                print(r)
                return HttpResponse(r, status=status.HTTP_200_OK)
            else:
                r = rag_manager(serializer.validated_data)
                print(r)
                return r
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=500)
