import numpy
import soundfile
from io import BytesIO

import base64
import subprocess

from django.core.files.base import ContentFile


class AudioTransformator:
    """
       A utility class for transforming audio file witch provides a method to read and transform audio files, into
       mono audio files.
    """
    @staticmethod
    def transform(file):
        """
             Parameters:
             - file: A file-like object with the audio file.

             Returns:
             - numpy.ndarray: A one-dimensional numpy array with the mono audio data.
             """
        file_buffer = BytesIO(file.read())
        try:
            data, sample_rate = soundfile.read(file_buffer, dtype='float32')
        except Exception as e:
            print(f"Error reading audio file: {e}")
            raise e
        if len(data.shape) > 1 and data.shape[1] > 1:
            data = numpy.mean(data, axis=1)
        return data

    @staticmethod
    def handleBinary(validated_data):
        """
        Handle binary data.

        This method takes in a dictionary of validated data and performs the following tasks:
        1. If the 'message' key exists in the validated data dictionary, it reads the first 4 bytes of the message/
        2. Seeks the message back to the beginning.
        3. Converts the WAV data in the message to MP3 format using the 'convert_wav_to_mp3' function.
        4. Base64 encodes the MP3 data.
        5. Creates a ContentFile object from the base64 decoded MP3 data with the name "demo.mp3".
        6. Replaces the 'message' key in the validated data dictionary with the content file.
        7. Writes the content of the content file to a file named "demo.mp3".
        8. Returns the modified validated data dictionary.

        Parameters:
            validated_data (dict): A dictionary of validated data.

        Returns:
            dict: The modified validated data dictionary.
        """
        if validated_data['message']:
            header = validated_data['message'].read(4)
            validated_data['message'].seek(0)
            mp3_data = AudioTransformator.convert_wav_to_mp3(validated_data['message'])
            base64_encoded = base64.b64encode(mp3_data).decode()
            content_file = ContentFile(base64.b64decode(base64_encoded), name="demo.mp3")
            validated_data['message'] = content_file
            with open("demo.mp3", 'wb+') as destination:
                for chunk in content_file.chunks():
                    destination.write(chunk)
            return validated_data

    @staticmethod
    def convert_wav_to_mp3(wav_input):
        """
        Converts a WAV audio file to an MP3 audio file using FFmpeg.
        """
        command = [
            'ffmpeg',
            '-i', '-',
            '-acodec', 'libmp3lame',
            '-f', 'mp3',
            'pipe:1'
        ]

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=wav_input.read())

        if process.returncode != 0:
            error_message = stderr.decode()
            print(f"FFmpeg error: {error_message}")
            raise Exception(f"FFmpeg error: {error_message}")

        return stdout
