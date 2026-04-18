from io import BufferedReader, BytesIO
from abc import ABC, abstractmethod

from constant_pool.const_info_types import CONSTANT_Class_info, CONSTANT_Field_Method_InterfaceMethod_info, CONSTANT_NameAndType_info, CONSTANT_String_info, CONSTANT_Utf8_info, CONSTANT_info
class Class_info_parser(ABC):
    @classmethod
    @abstractmethod
    def parse(cls,tag:int, buffer:BufferedReader|BytesIO) -> CONSTANT_info:
        pass

class CONSTANT_Class_info_Parser(Class_info_parser):
    @classmethod
    def parse(cls,tag:int, buffer:BufferedReader|BytesIO) -> CONSTANT_Class_info:
        name_index = int.from_bytes(buffer.read(2))
        return {"tag":tag, "name_index":name_index, "debug":cls.__name__}
    
class CONSTANT_Field_Method_InterfaceMethod_ref_info_Parser(Class_info_parser):
    @classmethod
    def parse(cls,tag:int, buffer:BufferedReader|BytesIO) -> CONSTANT_Field_Method_InterfaceMethod_info:
        class_index = int.from_bytes(buffer.read(2))
        name_and_type_index = int.from_bytes(buffer.read(2))
        return {"tag":tag, "class_index":class_index, "name_and_type_index":name_and_type_index, "debug":cls.__name__}

class CONSTANT_Field_ref_info_Parser(CONSTANT_Field_Method_InterfaceMethod_ref_info_Parser):
    pass

class CONSTANT_Method_ref_info_Parser(CONSTANT_Field_Method_InterfaceMethod_ref_info_Parser):
    pass

class CONSTANT_Interface_Method_ref_info_Parser(CONSTANT_Field_Method_InterfaceMethod_ref_info_Parser):
    pass

class CONSTANT_NameAndType_info_Parser(Class_info_parser):
    @classmethod
    def parse(cls,tag:int, buffer:BufferedReader|BytesIO) -> CONSTANT_NameAndType_info:
        name_index = int.from_bytes(buffer.read(2))
        descriptor_index = int.from_bytes(buffer.read(2))
        return {"tag":tag, "name_index":name_index, "descriptor_index":descriptor_index, "debug":cls.__name__}

class CONSTANT_Utf8_info_Parser(Class_info_parser):
    @classmethod
    def parse(cls,tag:int, buffer:BufferedReader|BytesIO) -> CONSTANT_Utf8_info:
        length = int.from_bytes(buffer.read(2))
        bytes = buffer.read(length)
        return {"tag":tag, "length":length, "bytes":bytes, "debug":cls.__name__}
    
class CONSTANT_String_info_Parser(Class_info_parser):
    @classmethod
    def parse(cls,tag:int, buffer:BufferedReader|BytesIO) -> CONSTANT_String_info:
        string_index = int.from_bytes(buffer.read(2))
        return {"tag":tag, "string_index":string_index, "debug":cls.__name__}

class cp_info_parser:
    CP_DICT_Parsers : dict[int,type[Class_info_parser]] = {
        1:CONSTANT_Utf8_info_Parser,
        7: CONSTANT_Class_info_Parser,
        8: CONSTANT_String_info_Parser,
        9: CONSTANT_Field_ref_info_Parser,
        10: CONSTANT_Method_ref_info_Parser,
        11: CONSTANT_Interface_Method_ref_info_Parser,
        12: CONSTANT_NameAndType_info_Parser,
    }

    def __init__(self):
        self.tag:int
        self.info:CONSTANT_info

    @classmethod
    def parse(cls,buffer:BufferedReader|BytesIO) -> CONSTANT_info:
        tag = int.from_bytes(buffer.read(1))
        if tag not in cls.CP_DICT_Parsers:
            raise NotImplementedError(f"{tag} not implemented yet in CP_DICT_Parsers")
        info = cls.CP_DICT_Parsers[tag].parse(tag,buffer)

        return info