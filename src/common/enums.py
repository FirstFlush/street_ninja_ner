from enum import Enum


class ModelType(Enum):
    SPACY = "spacy"
    HUGGING_FACE = "hugging_face"

class DataType(Enum):
    TRAINING = "training"
    VALIDATION = "validation"
    TESTING = "testing"
    INFERENCE = "inference"

class RawDataFormat(Enum):
    LABEL_STUDIO = "label_studio"
    JSON_MINIMAL = "json_minimal"