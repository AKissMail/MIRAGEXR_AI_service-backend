import google.cloud.texttospeech as tts
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from .serializers import SpeakGoogleSerializer


def speak_google(request):
    serializer = SpeakGoogleSerializer(data=request)
    if serializer.is_valid():
        try:
            language_code = "el-GR"

            text_input = tts.SynthesisInput(text=serializer.validated_data['message'])
            voice_params = tts.VoiceSelectionParams(
                language_code=language_code, name=serializer.validated_data['model']
            )
            audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

            client = tts.TextToSpeechClient()
            response = client.synthesize_speech(
                input=text_input,
                voice=voice_params,
                audio_config=audio_config,
            )
            print(response.status_code)
            return ContentFile(response.audio_content)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
