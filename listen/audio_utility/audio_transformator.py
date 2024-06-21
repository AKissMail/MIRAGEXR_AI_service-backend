import numpy
import soundfile
from io import BytesIO


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
