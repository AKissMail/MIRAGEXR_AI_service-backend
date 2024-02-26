from transformers import pipeline


# https://huggingface.co/NbAiLab/nb-whisper-large

def whisperNationalLibraryofNorway(task, language, return_timestamps, chunk_length_s, ):
    asr = pipeline("automatic-speech-recognition", "NbAiLabBeta/nb-whisper-large")
    return asr("king.mp3", generate_kwargs={'task': 'transcribe', 'language': 'no'})
