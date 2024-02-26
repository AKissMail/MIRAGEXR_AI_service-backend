from openai import OpenAI
from rest_framework import serializers
from transformers import pipeline

from backend.listen.audio_transformator import AudioTransformator


class WhisperOpenAiRemoteSerializer(serializers.Serializer):
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


# todo fixing the OpenAI api and come up with a local universal solution. Good for now.
def whisper_open_ai_remote(data):
    return wisper_open_ai_local(data)


def whisper_open_ai_remote2(data):
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
    serializer = WhisperOpenAiRemoteSerializer(data=data)
    print(serializer.is_valid())
    if serializer.is_valid():
        print("Validating the data")
        audio_file = serializer.validated_data['audio']
        audio_content = audio_file.read()
        file = (audio_content, audio_content, "audio/mp3")

        # print(audio_content)
        transcript = client.audio.transcriptions.create(
            model=serializer.validated_data['subModel'],
            file=file,
            response_format=serializer.validated_data['response_format'],
            timestamp_granularities=["word"],
            prompt=serializer.validated_data['prompt']
        )
        return transcript
    else:
        return serializer.errors.__str__()


class WhisperOpenAiLocalSerializer(serializers.Serializer):
    audio = serializers.FileField()
    subModel = serializers.CharField(default="medium")
    task = serializers.CharField(default="transcribe")
    language = serializers.CharField(default="no")
    pipelineTask = serializers.CharField(default="automatic-speech-recognition")


def wisper_open_ai_local(data):
    serializer = WhisperOpenAiLocalSerializer(data=data)
    if serializer.is_valid():
        model_str = "openai/whisper-" + serializer.validated_data['subModel']
        model = pipeline(
            "automatic-speech-recognition", model=model_str
        )
        transformed_audio = AudioTransformator.transform(serializer.validated_data['audio'])
        return model(
            transformed_audio,
            chunk_length_s=28,
            generate_kwargs={
                'task': serializer.validated_data['task'],
                'language': serializer.validated_data['language']
            }
        )
    else:
        return serializer.errors
