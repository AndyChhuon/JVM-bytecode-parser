from io import BufferedReader, BytesIO
from access_flag.access_flag_parser import access_flag_parser
from constant_pool.const_info_types import CONSTANT_info
from methods_info.methods_info_types import Method_info
from attributes_info.attributes_info_parsers import Attributes_info_parser

class MethodsInfoParser:
    @classmethod
    def parse(cls, cp_info:list[CONSTANT_info], buffer:BufferedReader|BytesIO) -> Method_info:
        access_flags = access_flag_parser.parse(int.from_bytes(buffer.read(2)))

        name_index = int.from_bytes(buffer.read(2))
        descriptor_index = int.from_bytes(buffer.read(2))

        attributes_count = int.from_bytes(buffer.read(2))
        
        attributes = []
        for _ in range(attributes_count):
            attributes.append(Attributes_info_parser.parse(cp_info, buffer))

        return {"access_flags":access_flags, "name_index":name_index, "descriptor_index":descriptor_index, "attributes_count": attributes_count, "attributes":attributes}