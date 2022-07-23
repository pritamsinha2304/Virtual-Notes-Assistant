""" Module for calling Model Processor """

from .constants_filepath import Constants
from .model_processor_initializer import ModelProcessorInitializer

class ModelProcessorCaller:
    """Load the model and processor
    """
    def __init__(self) -> None:
        """Call all the filepath

        """
        self.constants_fp = Constants()

    def __call__(self):
        model_ini = ModelProcessorInitializer(config_fp=self.constants_fp.config_fp,
                                vocab_fp=self.constants_fp.vocab_fp,
                                tokenizer_config_fp=self.constants_fp.tokenizer_config_fp,
                                feature_config_fp=self.constants_fp.feature_config_fp,
                                model_fp=self.constants_fp.model_fp)
        model = model_ini.load_model()
        processor = model_ini.load_processor()
        return model, processor
