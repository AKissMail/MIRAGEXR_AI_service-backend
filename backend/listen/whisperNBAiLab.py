from transformers import pipeline
from rest_framework import serializers
from .audio_transformator import AudioTransformator


class WhisperNBAiLabSerializer(serializers.Serializer):
    """
    Serializer for validating and serializing data for automatic speech recognition.
    Attributes:
        audio (FileField): The audio file to be transcribed.
        subModel (CharField): Specifies the sub-model. Possible: tiny, base, small, medium, and large.
            Default to "nb-whisper-medium".
        mode (CharField): Indicates the transcription mode. Possible values: verbatim (a model for exact transcriptions)
            semantic (a model for semantic transcription with error correction) Defaults to "verbatim".
            In a new release deprecate.
        task (CharField): The task to be performed. It is either translate (to eng) or transcribe.
        Defaults to "transcribe".
        language (CharField): Specifies the language of the audio. It is either "no" for dialects closer to
            Bokmål. "nn" for dialects closer to Nynorsk or "en" for english. Defaults to "no".
        pipelineTask (CharField): Specifies the pipeline task to be used. Defaults to "automatic-speech-recognition".
    """
    audio = serializers.FileField()
    subModel = serializers.CharField(default="nb-whisper-medium")
    # mode = serializers.CharField(default="verbatim")
    task = serializers.CharField(default="transcribe")
    language = serializers.CharField(default="no")
    pipelineTask = serializers.CharField(default="automatic-speech-recognition")


def whisper_nb_ai_lab(data):
    """
     Transcribes audio files using the fine-tuned Whisper model from the NB-AI-Lab after validating the data through
     WhisperNBAiLabSerializer.
    Parameters:
        data (dict): A dictionary containing keys corresponding to WhisperNBAiLabSerializer.
     Returns:
         dict or str: Returns a dictionary containing the transcription result if the transcription is successful.
         Returns a dictionary of validation errors if the data is invalid.
     """
    serializer = WhisperNBAiLabSerializer(data=data)
    if serializer.is_valid():
        model_str = "NbAiLabBeta/" + serializer.validated_data['subModel']
        model = pipeline(
            serializer.validated_data['pipelineTask'],
            model_str
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
