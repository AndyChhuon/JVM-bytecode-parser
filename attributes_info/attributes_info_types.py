from typing import TypedDict

from attributes_info.exception_table.exception_table_types import Exception_table
from attributes_info.line_number_table.line_number_table_types import Line_number_table

class Attributes_info(TypedDict):
    attribute_name_index: int
    attribute_length: int
    debug: str

class ConstantValue_attribute(Attributes_info):
    constantvalue_index: int


class Signature_attribute(Attributes_info):
    signature_index: int

class Code_attribute(Attributes_info):
    max_stack: int
    max_locals: int
    code_length: int
    code: bytes
    exception_table_length: int
    exception_table: list[Exception_table]
    attributes_count: int
    attributes_info: list[Attributes_info]

class LineNumberTable_attribute(Attributes_info):
    line_number_table_length: int
    line_number_table: list[Line_number_table]

class SourceFile_attribute(Attributes_info):
    sourcefile_index: int