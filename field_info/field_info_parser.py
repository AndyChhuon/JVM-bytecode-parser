from io import BufferedReader, BytesIO
from constant_pool.const_info_types import CONSTANT_info
from field_info.fields_info_types import Field_info
from access_flag.access_flag_parser import access_flag_parser
from attributes_info.attributes_info_parsers import Attributes_info_parser

class FieldInfoParser:
    @classmethod
    def parse(cls, cp_info:list[CONSTANT_info], buffer:BufferedReader|BytesIO) -> Field_info:
        access_flags = access_flag_parser.parse(int.from_bytes(buffer.read(2)))
        name_index = int.from_bytes(buffer.read(2))
        descriptor_index = int.from_bytes(buffer.read(2))
        attributes_count = int.from_bytes(buffer.read(2))
        attributes = []

        for _ in range(attributes_count):
            info = Attributes_info_parser.parse(cp_info, buffer)
            attributes.append(info)
        
        return {"access_flags": access_flags, "name_index":name_index, "descriptor_index": descriptor_index, "attributes_count":attributes_count, "attributes":attributes}
