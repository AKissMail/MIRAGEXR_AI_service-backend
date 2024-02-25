from openai import OpenAI


def wisperOpenAI(data):
    client = OpenAI()
    audio_file = data['audio']
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["word"],
        prompt="Hi"
    )

    return transcript
