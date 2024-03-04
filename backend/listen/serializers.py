from rest_framework import serializers


class WhisperNBAiLabSerializer(serializers.Serializer):
    """
    Serializer for validating and serializing data for automatic speech recognition.
    Attributes:
        audio (FileField): The audio file to be transcribed.
        subModel (CharField): Specify the submodule. Possible: tiny, base, small, medium, and large.
            Default to "nb-whisper-medium".
            mode (CharField): Indicates the transcription mode. Possible values: verbatim
            (a model for exact transcriptions) semantic (a model for semantic transcription with error correction)
            Defaults to "verbatim".

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


class WhisperOpenAiRemoteSerializer(serializers.Serializer):
    """
    Serializer for validating and serializing data for automatic speech recognition.
    Attributes:
        audio (FileField): The audio file to be transcribed. It Must be less than 25 MB.
        subModel (CharField): Specify the submodule. Possible: "whisper-1"
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
