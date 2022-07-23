""" Module for loading the audio files """

import os
import librosa
from .json_to_dict import JsonToDict
from .constants_filepath import Constants

class AudioProcessor:
    """Audio Loader
    """
    def __init__(self, filepath) -> None:
        """This will process the audio samples.

        Args:
            filepath(`str`): Filepath of the audio file
        """
        self.config = JsonToDict(Constants().processor_config_fp).convert()
        self.filepath = filepath
        print(self.filepath)

    def audio_decoder(self):
        """Decode the audio signal into array

        Returns:
            `numpy.array`: An array of decoded signal as array depending on sampling rate
        """
        samples, _ = librosa.load(os.path.join(self.filepath),
                                  sr=self.config["sampling_rate"], mono=True)
        return samples
