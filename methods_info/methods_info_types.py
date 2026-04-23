from typing import TypedDict
from access_flag.access_flag_types import AccessFlag
from attributes_info.attributes_info_types import Attributes_info

class Method_info(TypedDict):
    access_flags: list[AccessFlag]
    name_index: int
    descriptor_index: int
    attributes_count: int
    attributes: list[Attributes_info]