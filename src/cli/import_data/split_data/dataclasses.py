from dataclasses import dataclass

@dataclass
class RatioSplit:
    training: float
    validation: float
    testing: float

@dataclass
class SplitData:
    training: list[str]
    validation: list[str]
    testing: list[str]