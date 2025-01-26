from typing import Literal


# Processed JSON Data:
Entity = tuple[int, int, str]
Annotations = dict[Literal["entities"], list[Entity]]  # e.g. {"entities": [(5, 9, "RESOURCE"), ...]}
NormalizedData = list[tuple[str, Annotations]]