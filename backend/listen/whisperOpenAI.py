from openai import OpenAI
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
import requests



class WhisperOpenAISerializer(serializers.Serializer):
    """
    Serializer for validating and serializing data for automatic speech recognition.
    Attributes:
        audio (FileField): The audio file to be transcribed. Must be less than 25 MB.
        subModel (CharField): Specifies the sub-model. Possible: "whisper-1"
            Defaults to "whisper-1".
        response_format (CharField): Specifies the format of the transcription response. Possible:json, text, srt,
            verbose_json, or vtt. Defaults to "verbose_json.
        prompt (CharField): An optional prompt that can be provided to the model.
            Defaults to an empty string and can be changed to any given value.
    """

    audio = serializers.FileField()
    subModel = serializers.CharField(default="whisper-1")
    response_format = serializers.CharField(default="verbose_json")
    prompt = serializers.CharField(default="")


def whisper_open_ai(data):
    print(" whisper_open_ai")
    """
    Transcribes an audio file using OpenAI's Whisper model after validating the data
    through WisperOpenAISerializer.
    Parameters:
        data (dict): A dictionary containing keys corresponding to WisperOpenAISerializer.
      Returns:
         dict or str: Returns a dictionary containing the transcription result if the transcription is successful.
         Returns a dictionary of validation errors if the data is invalid.
    """
    client = OpenAI()
    serializer = WhisperOpenAISerializer(data=data)
    print(serializer.is_valid())
    if serializer.is_valid():
        print("Validating the data")
        audio_file: InMemoryUploadedFile = serializer.validated_data['audio']
        audio_content = audio_file.read()
        print(serializer.validated_data['audio'])
        transcript = client.audio.transcriptions.create(
            model=serializer.validated_data['subModel'],
            file=audio_content,
            response_format=serializer.validated_data['response_format'],
            timestamp_granularities=["word"],
            prompt=serializer.validated_data['prompt']
        )
        return transcript
    else:
        print(serializer.errors)
        return serializer.errors
