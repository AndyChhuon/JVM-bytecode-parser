from typing import TypedDict

class CONSTANT_info(TypedDict):
    tag:int
    debug: str

class CONSTANT_Class_info(CONSTANT_info):
    name_index:int

class CONSTANT_Field_Method_InterfaceMethod_info(CONSTANT_info):
    # points to CONSTANT_Class_info to which it belongs
    class_index:int
    # points to its CONSTANT_NameAndType_info
    name_and_type_index:int

class CONSTANT_NameAndType_info(CONSTANT_info):
    name_index:int
    descriptor_index:int

class CONSTANT_Utf8_info(CONSTANT_info):
    length:int
    bytes:bytes


class CONSTANT_String_info(CONSTANT_info):
    string_index:int
