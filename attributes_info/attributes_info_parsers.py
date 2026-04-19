from io import BufferedReader, BytesIO
from typing import cast
from attributes_info.attributes_info_types import Attributes_info, ConstantValue_attribute, Signature_attribute
from abc import ABC, abstractmethod

from constant_pool.const_info_types import CONSTANT_Utf8_info, CONSTANT_info

class Attribute_info_parser(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, attribute_name_index: int, buffer:BufferedReader | BytesIO) -> Attributes_info:
        pass


class Attribute_info_Constant_Value_Parser(Attribute_info_parser):
    @classmethod
    def parse(cls, attribute_name_index: int, buffer:BufferedReader | BytesIO) -> ConstantValue_attribute:
        attribute_length = int.from_bytes(buffer.read(4))
        constantvalue_index = int.from_bytes(buffer.read(2))
        return {"attribute_name_index": attribute_name_index, "attribute_length": attribute_length, "constantvalue_index": constantvalue_index, "debug":cls.__name__.removesuffix("_Parser")}

class Attribute_info_Signature_Parser(Attribute_info_parser):
    @classmethod
    def parse(cls, attribute_name_index: int, buffer:BufferedReader | BytesIO) -> Signature_attribute:
        attribute_length = int.from_bytes(buffer.read(4))
        signature_index = int.from_bytes(buffer.read(2))
        return {"attribute_name_index": attribute_name_index, "attribute_length": attribute_length, "signature_index": signature_index, "debug":cls.__name__.removesuffix("_Parser")}


class Attributes_info_parser:
    ATTRIBUTES_DICT_PARSERS : dict[str, type[Attribute_info_parser]] = {
        "ConstantValue": Attribute_info_Constant_Value_Parser,
        "Signature": Attribute_info_Signature_Parser
    }

    @classmethod
    def parse(cls, cp_info:list[CONSTANT_info],  buffer:BufferedReader | BytesIO,) -> Attributes_info:
        attribute_name_index = int.from_bytes(buffer.read(2))
        
        Utf8_info_attribute_name = cast(CONSTANT_Utf8_info, cp_info[attribute_name_index-1])
        attribute_type = Utf8_info_attribute_name["bytes"].decode('utf-8')

        if attribute_type not in cls.ATTRIBUTES_DICT_PARSERS:
            raise NotImplementedError(f"{attribute_type} not implemented yet in ATTRIBUTES_DICT_PARSERS")

        return cls.ATTRIBUTES_DICT_PARSERS[attribute_type].parse(attribute_name_index, buffer)