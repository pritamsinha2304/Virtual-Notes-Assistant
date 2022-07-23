""" Module for initialize the model and processor for audio processing """

from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2FeatureExtractor, \
    Wav2Vec2Processor, TFWav2Vec2ForCTC, Wav2Vec2Config
from .json_to_dict import JsonToDict


class ModelProcessorInitializer:
    """Initialize the Model and Processor
    """
    def __init__(self,
                 config_fp,
                 vocab_fp,
                 tokenizer_config_fp,
                 feature_config_fp,
                 model_fp) -> None:
        self.config_fp = config_fp
        self.vocab_fp = vocab_fp
        self.tokenizer_config_fp = tokenizer_config_fp
        self.feature_config_fp = feature_config_fp
        self.model_fp = model_fp

    def __load_config(self):
        config_contents = Wav2Vec2Config.from_json_file(self.config_fp)
        return config_contents

    def load_model(self):
        """Load the Wav2Vec2 model from config file
        """
        model = TFWav2Vec2ForCTC.from_pretrained(self.model_fp, config=self.__load_config())
        return model

    def __load_tokenizer(self):
        tokenizer_config = JsonToDict(self.tokenizer_config_fp)
        tokenizer_dict = tokenizer_config.convert()
        tokenizer = Wav2Vec2CTCTokenizer(self.vocab_fp, **tokenizer_dict)
        return tokenizer

    def __load_feature(self):
        feature_config = JsonToDict(self.feature_config_fp)
        feature_dict = feature_config.convert()
        feature_extractor = Wav2Vec2FeatureExtractor(**feature_dict)
        return feature_extractor

    def load_processor(self):
        """Load the Wav2Vec2 Processor which loads Tokenizer and Feature Extractor
        """
        processor = Wav2Vec2Processor(
            feature_extractor=self.__load_feature(), tokenizer=self.__load_tokenizer())
        return processor
