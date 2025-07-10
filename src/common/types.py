from typing import TypedDict


# JsonPrimitive = Union[str, int, float, bool, None]
# JsonDictType = dict[str, "JsonType"]
# JsonListType = list["JsonType"]
# JsonType = Union[JsonPrimitive, JsonListType, JsonDictType]


class LabelStudioAnnotatedJson(TypedDict):
    data: dict[str, str]
    annotations: list[dict]


class SpacyFormattedJson(TypedDict):
    text: str
    entities: list[tuple[int, int, str]]

