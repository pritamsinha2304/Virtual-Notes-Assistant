""" Module for storing file paths """

from dataclasses import dataclass
import os

@dataclass
class Constants:
    """Stores all the config filepath as `dataclass`
    """
    config_fp: str = os.path.join("models", "config.json")
    vocab_fp: str = os.path.join("models", "vocab.json")
    tokenizer_config_fp: str = os.path.join("models", "tokenizer_config.json")
    feature_config_fp: str = os.path.join("models", "feature_extractor_config.json")
    model_fp: str = os.path.join("models", "tf_model.h5")
    processor_config_fp: str = os.path.join("models", "processor_config.json")
    