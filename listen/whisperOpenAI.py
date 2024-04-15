import os
import tempfile
from openai import OpenAI
from .serializers import WhisperOpenAiRemoteSerializer, WhisperOpenAiLocalSerializer
from transformers import pipeline
from django.core.files.uploadedfile import InMemoryUploadedFile

from .audio_transformator import AudioTransformator


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
        audio_file = serializer.validated_data['message']
        if isinstance(audio_file, InMemoryUploadedFile):
            file_extension = os.path.splitext(audio_file.name)[1]
            if not file_extension:
                file_extension = '.mp3'
            with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as tmp_file:
                for chunk in audio_file.chunks():
                    tmp_file.write(chunk)
                tmp_file.flush()
                with open(tmp_file.name, 'rb') as file_to_upload:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=file_to_upload
                    )
        else:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
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
        transformed_audio = AudioTransformator.transform(serializer.validated_data['message'])
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
