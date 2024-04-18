from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import DokumentSerializer
from .handelData import handelDokument



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dokument(request):
    print(request.data)
    serializer = DokumentSerializer(data=request.data)
    if serializer.is_valid():
        print("is valid")
        result = handelDokument(serializer.validated_data)
        if result:
            return Response("Document " + serializer.validated_data['name'] + "added to " + serializer.validated_data['database'], status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

