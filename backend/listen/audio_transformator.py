import numpy
import soundfile
from io import BytesIO


class AudioTransformator:

    @staticmethod
    def transform(file):
        file_buffer = BytesIO(file.read())
        data, sample_rate = soundfile.read(file_buffer, dtype='float32')
        if len(data.shape) > 1 and data.shape[1] > 1:
            data = numpy.mean(data, axis=1)
        return data
