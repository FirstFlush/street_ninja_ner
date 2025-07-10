from .base_enum import CustomEnum


class ModelType(CustomEnum):
    SPACY = "spacy"
    HUGGING_FACE = "hugging_face"


class AnnotationLabels(CustomEnum):
    LOCATION = "LOCATION"
    RESOURCE = "RESOURCE"
    QUALIFIER = "QUALIFIER"