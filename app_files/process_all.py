""" Module for processing and decoding audio """

import tensorflow as tf
from .audio_processor import AudioProcessor
from .json_to_dict import JsonToDict
from .constants_filepath import Constants


class ProcessAll:
    """Process audio and Decode audio
    """
    def __init__(self, audio_fp, model, processor) -> None:
        """Call all the underlying class into one.

        Args:
            audio_fp (`str`): Filepath of the audio file
        """

        self.audio = AudioProcessor(audio_fp).audio_decoder()

        self.model, self.processor = model, processor

        self.constants = Constants()

    def __process_inp(self):
        input_values = self.processor(
            self.audio, **((JsonToDict(Constants().processor_config_fp)).convert()))
        return input_values.input_values

    def process_model(self):
        """Process audio and give prediction

        Returns:
            numpy.array
        """
        input_values = self.__process_inp()
        predictions = self.model(input_values).logits
        return predictions

    def decode_predictions(self, predictions):
        """Decode the predicted values

        Args:
            predictions (_type_): _description_

        Returns:
            str: Decoded String
        """
        pred = tf.argmax(predictions, axis=-1)
        transcriptions = self.processor.batch_decode(pred)
        return transcriptions
    