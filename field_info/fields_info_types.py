from access_flag.access_flag_types import AccessFlag
from attributes_info.attributes_info_types import Attributes_info
from typing import TypedDict

class Field_info(TypedDict):
    access_flags: list[AccessFlag]
    name_index: int
    descriptor_index: int
    attributes_count: int
    attributes: list[Attributes_info]