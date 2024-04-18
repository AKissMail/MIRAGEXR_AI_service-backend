from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views he
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dokument(request):
    pass