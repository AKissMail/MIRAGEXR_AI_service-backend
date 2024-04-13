from rest_framework import serializers


class ListenSerializer(serializers.Serializer):
    """
    The ListenSerializer class is a serializer that is used to handle the serialization and validation of listen data.
    It defines two fields: 'model' and 'audio'.

    Attributes:
        model (serializers.CharField): A CharField that represents the model of the listen data.
        message (serializers.FileField): A FileField that represents the audio file of the listen data.

    """

    model = serializers.CharField()
    message = serializers.FileField()


class WhisperNBAiLabSerializer(serializers.Serializer):
    """

    WhisperNBAiLabSerializer

    This class is a serializer for the WhisperNBAiLab API.

    Attributes:
        message (serializers.FileField): The audio file to be processed.
        subModel (serializers.CharField): The submodel to be used for processing. Default is "nb-whisper-medium".
        task (serializers.CharField): The task to be performed. Default is "transcribe".
        language (serializers.CharField): The language of the audio. Default is "no".
        pipelineTask (serializers.CharField): The pipeline task for the API. Default is "automatic-speech-recognition".

    """
    message = serializers.FileField()
    subModel = serializers.CharField(default="nb-whisper-medium")
    task = serializers.CharField(default="transcribe")
    language = serializers.CharField(default="no")
    pipelineTask = serializers.CharField(default="automatic-speech-recognition")


class WhisperOpenAiRemoteSerializer(serializers.Serializer):
    """
    Class: WhisperOpenAiRemoteSerializer

        This class is a serializer for handling audio files and additional parameters for the Whisper OpenAI remote API.

    Attributes:
        message (serializers.FileField): Audio file field.
        subModel (serializers.CharField): Submodel parameter for the Whisper OpenAI remote API.
        Default value is "whisper-1".
        response_format (serializers.CharField): Response format parameter for the Whisper OpenAI remote API.
        Default value is "verbose_json".
        prompt (serializers.CharField): Prompt parameter for the Whisper OpenAI remote API.
        Default value is an empty string.

    """

    message = serializers.FileField()
    subModel = serializers.CharField(default="whisper-1")
    response_format = serializers.CharField(default="verbose_json")
    prompt = serializers.CharField(default="")


class WhisperOpenAiLocalSerializer(serializers.Serializer):
    """
    Serializer class for serializing Whisper OpenAI local API requests.

    Attributes:
        message (FileField): The uploaded audio file.
        subModel (CharField): The submodel to use for the task (default is 'tiny').
        task (CharField): The task to perform (default is 'transcribe').
        language (CharField): The language of the audio (default is 'no').
        pipelineTask (CharField): The pipeline task to perform (default is 'automatic-speech-recognition').
    """
    message = serializers.FileField()
    subModel = serializers.CharField(default="tiny")
    task = serializers.CharField(default="transcribe")
    language = serializers.CharField(default="no")
    pipelineTask = serializers.CharField(default="automatic-speech-recognition")
