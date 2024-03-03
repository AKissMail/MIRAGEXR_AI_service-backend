import os
import tempfile
from openai import OpenAI
from rest_framework import serializers
from transformers import pipeline
from django.core.files.uploadedfile import InMemoryUploadedFile

from .audio_transformator import AudioTransformator


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


class WhisperOpenAiLocalSerializer(serializers.Serializer):
    """
     Serializer for configuring and validating inputs for local Whisper audio processing tasks.
     Attributes:
         audio (FileField): A required file field that takes an audio file.
         subModel (CharField): Optional; specifies the Whisper model variant to use.
         task (CharField): Optional; defines the type of task to perform ("transcribe", "Translate")
         language (CharField): Optional; specifies the language of the audio content. Defaults to "no"
         pipelineTask (CharField): Optional

     """
    audio = serializers.FileField()
    subModel = serializers.CharField(default="medium")
    task = serializers.CharField(default="transcribe")
    language = serializers.CharField(default="no")
    pipelineTask = serializers.CharField(default="automatic-speech-recognition")


def whisper_open_ai_remote(data):
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
    if serializer.is_valid():
        audio_file = serializer.validated_data['audio']

        if isinstance(audio_file, InMemoryUploadedFile):
            # Determine the file extension, if possible
            file_extension = os.path.splitext(audio_file.name)[1]
            if not file_extension:
                # Default to .wav if the file extension is unknown
                # This is a fallback. You might want to handle this differently.
                file_extension = '.wav'

            # Use a temporary file with the correct file extension
            with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as tmp_file:
                # Write the audio file's content to the temporary file
                for chunk in audio_file.chunks():
                    tmp_file.write(chunk)
                tmp_file.flush()  # Ensure all data is written to disk

                # Reopen the temporary file in binary read mode to pass to the API
                with open(tmp_file.name, 'rb') as file_to_upload:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=file_to_upload
                    )

        else:
            # If the file is already in a suitable format or path, handle accordingly
            # This part should be adjusted based on your application's requirements
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file  # Assuming this is a file path or file-like object
            )

        return transcription.text


def wisper_open_ai_local(data):
    """
    Processes local transcription of an audio file using the Whisper model based on validated serializer data.
    Parameters:
        data (dict): A dictionary containing the input data for the transcription task. Expected keys are:
            'audio' (the audio file to be transcribed),
            'subModel' (the Whisper model variant to use),
            'task' (the type of task, typically 'transcribe'),
            'language' (the language of the audio),
            'pipelineTask' (the ASR pipeline task to be performed).

    Returns:
        dict containing the transcription results or serializers.ValidationError
    """
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
