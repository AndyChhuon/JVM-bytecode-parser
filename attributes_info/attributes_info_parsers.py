from io import BufferedReader, BytesIO
from typing import cast
from attributes_info.attributes_info_types import Attributes_info, Code_attribute, ConstantValue_attribute, LineNumberTable_attribute, Signature_attribute
from abc import ABC, abstractmethod

from attributes_info.exception_table.exception_table_parser import ExceptionTableParser
from attributes_info.line_number_table.line_number_parser import LineNumberTableParser
from constant_pool.const_info_types import CONSTANT_Utf8_info, CONSTANT_info

class Attribute_info_parser(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, attribute_name_index: int, buffer:BufferedReader | BytesIO, cp_info:list[CONSTANT_info]) -> Attributes_info:
        pass


class Attribute_info_Constant_Value_Parser(Attribute_info_parser):
    @classmethod
    def parse(cls, attribute_name_index: int, buffer:BufferedReader | BytesIO, cp_info:list[CONSTANT_info]) -> ConstantValue_attribute:
        attribute_length = int.from_bytes(buffer.read(4))
        constantvalue_index = int.from_bytes(buffer.read(2))
        return {"attribute_name_index": attribute_name_index, "attribute_length": attribute_length, "constantvalue_index": constantvalue_index, "debug":cls.__name__.removesuffix("_Parser")}

class Attribute_info_Signature_Parser(Attribute_info_parser):
    @classmethod
    def parse(cls, attribute_name_index: int, buffer:BufferedReader | BytesIO, cp_info:list[CONSTANT_info]) -> Signature_attribute:
        attribute_length = int.from_bytes(buffer.read(4))
        signature_index = int.from_bytes(buffer.read(2))
        return {"attribute_name_index": attribute_name_index, "attribute_length": attribute_length, "signature_index": signature_index, "debug":cls.__name__.removesuffix("_Parser")}

class Attribute_info_Code_Parser(Attribute_info_parser):
    @classmethod
    def parse(cls, attribute_name_index: int, buffer: BufferedReader|BytesIO, cp_info:list[CONSTANT_info]) -> Code_attribute:
        attribute_length = int.from_bytes(buffer.read(4))
        max_stack = int.from_bytes(buffer.read(2))
        max_locals = int.from_bytes(buffer.read(2))
        code_length = int.from_bytes(buffer.read(4))
        code = buffer.read(code_length)
        exception_table_length = int.from_bytes(buffer.read(2))
        exception_table = []
        for _ in range(exception_table_length):
            exception_table.append(ExceptionTableParser.parse(cp_info, buffer))
        attributes_count = int.from_bytes(buffer.read(2))
        attributes_info = []
        print("exception_table_length", exception_table_length)
        for _ in range(attributes_count):
            attributes_info.append(Attributes_info_parser.parse(cp_info, buffer))
        
        return {"attribute_name_index": attribute_name_index, "attribute_length": attribute_length, "max_stack":max_stack, "max_locals":max_locals, "code_length": code_length, "code": code, "exception_table_length": exception_table_length, "exception_table": exception_table, "attributes_count": attributes_count, "attributes_info": attributes_info, "debug": cls.__name__.removesuffix("_Parser")}


class Attribute_info_Line_Number_Table_Parser(Attribute_info_parser):
    @classmethod
    def parse(cls, attribute_name_index: int, buffer: BufferedReader|BytesIO, cp_info:list[CONSTANT_info]) -> LineNumberTable_attribute:
        attribute_length = int.from_bytes(buffer.read(4))
        line_number_table_length = int.from_bytes(buffer.read(2))
        line_number_table = []

        for _ in range(line_number_table_length):
            line_number_table.append(LineNumberTableParser.parse(buffer))
        
        return {"attribute_name_index": attribute_name_index, "attribute_length": attribute_length, "line_number_table_length": line_number_table_length, "line_number_table": line_number_table, "debug": cls.__name__.removesuffix("_Parser")}



class Attributes_info_parser:
    ATTRIBUTES_DICT_PARSERS : dict[str, type[Attribute_info_parser]] = {
        "ConstantValue": Attribute_info_Constant_Value_Parser,
        "Signature": Attribute_info_Signature_Parser,
        "Code": Attribute_info_Code_Parser,
        "LineNumberTable": Attribute_info_Line_Number_Table_Parser
    }

    @classmethod
    def parse(cls, cp_info:list[CONSTANT_info],  buffer:BufferedReader | BytesIO,) -> Attributes_info:
        attribute_name_index = int.from_bytes(buffer.read(2))
        
        Utf8_info_attribute_name = cast(CONSTANT_Utf8_info, cp_info[attribute_name_index-1])
        print(Utf8_info_attribute_name["bytes"])
        attribute_type = Utf8_info_attribute_name["bytes"].decode('utf-8')

        if attribute_type not in cls.ATTRIBUTES_DICT_PARSERS:
            raise NotImplementedError(f"{attribute_type} not implemented yet in ATTRIBUTES_DICT_PARSERS")

        return cls.ATTRIBUTES_DICT_PARSERS[attribute_type].parse(attribute_name_index, buffer, cp_info)