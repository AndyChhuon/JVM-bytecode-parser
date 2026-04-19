from typing import TypedDict

class Attributes_info(TypedDict):
    attribute_name_index: int
    attribute_length: int
    debug: str

class ConstantValue_attribute(Attributes_info):
    constantvalue_index: int


class Signature_attribute(Attributes_info):
    signature_index: int
