from openai import OpenAI
from rest_framework import serializers


class WhisperOpenAISerializer(serializers.Serializer):
    """
    Serializer for validating and serializing data for automatic speech recognition.
    Attributes:
        audio (FileField): The audio file to be transcribed.
        subModel (CharField): Specifies the sub-model. Possible: @todo
            Defaults to "whisper-1".
        response_format (CharField): Specifies the format of the transcription response. Possible @todo
            Defaults to "verbose_json".
        timestamp_granularities (CharField): Specifies the granularity of timestamps. Possible @todo
            Defaults to "word".
        prompt (CharField): An optional prompt that can be provided to the model.
            Defaults to an empty string and can be change to any given value.
    """

    audio = serializers.FileField()
    subModel = serializers.CharField(default="whisper-1")
    response_format = serializers.CharField(default="verbose_json")
    timestamp_granularities = serializers.CharField(default="word")
    prompt = serializers.CharField(default="")


def whisperOpenAI(data):
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
    if serializer.is_valid():
        transcript = client.audio.transcriptions.create(
            model=serializer.validated_data['subModel'],
            file=serializer.validated_data['audio'],
            response_format=serializer.validated_data['response_format'],
            timestamp_granularities=serializer.validated_data['timestamp_granularities'],
            prompt=serializer.validated_data['prompt']
        )
        return transcript
    else:
        return serializer.errors
