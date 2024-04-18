from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import DokumentSerializer


# Create your views he



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dokument(request):
    serializer = DokumentSerializer(data=request.data)
    if serializer.is_valid():
        print('Passt')
        return Response(serializer.data['name'], status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

