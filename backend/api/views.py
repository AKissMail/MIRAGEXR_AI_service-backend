import json
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.response import Response

from products.models import Product

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("id").last()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=['id', 'price'])
    return JsonResponse(data)
