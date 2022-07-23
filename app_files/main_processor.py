""" Main Processor Module for processing audio """

from .process_all import ProcessAll

class MainProcessor:
    """ Main Module """
    def __init__(self, file_path, model, processor) -> None:
        self.filepath = file_path
        self.model = model
        self.processor = processor

    def __call__(self):
        process_all = ProcessAll(self.filepath, self.model, self.processor)
        predictions = process_all.process_model()

        transcriptions = process_all.decode_predictions(predictions)
        return transcriptions
    