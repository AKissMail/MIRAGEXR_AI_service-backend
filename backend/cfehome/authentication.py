from django.http import JsonResponse
import os


def api_key_auth_middleware(get_response):
    def middleware(request):
        api_key = request.headers.get('X-API-KEY')
        if api_key != os.getenv('API_KEY'):
            return JsonResponse({'error': 'Invalid API-KEY'}, status=401)
        return get_response(request)
    return middleware
