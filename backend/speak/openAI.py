import requests
from django.http import StreamingHttpResponse
from django.conf import settings

'''
This it the wrapper for the OpenAI API, which allows you to crate an Voice based on a given String.
'''


def speakOpenAI(data):
    param = data
    if param['voice'] == "default":
        param['voice'] = "onyx"
    if data['voice'] in ("alloy", "echo", "fable", "onyx", "nova", "shimmer"):
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f'Bearer {settings.OPENAI_API_KEY}',
        }
        data = {
            "model": "tts-1",
            "input": param['speakOut'],
            "voice": param['voice'],
            "speed": param['speed']
        }

        response = requests.post(url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            def generate():
                for chunk in response.iter_content(chunk_size=1024):
                    print(f"Chunk size: {len(chunk)}")
                    yield chunk
            return StreamingHttpResponse(
                streaming_content=generate(),
                content_type="audio/mpeg"
            )
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    else:
        return "Voice not found! I know: 'alloy', 'echo', 'fable', 'onyx', 'nova', and 'shimmer'"
