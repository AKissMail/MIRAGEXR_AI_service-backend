from transformers import pipeline
from .audio_transformator import AudioTransformator
from .serializers import WhisperNBAiLabSerializer


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
