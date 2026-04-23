from io import BufferedReader, BytesIO

from attributes_info.exception_table.exception_table_types import Exception_table
from constant_pool.const_info_types import CONSTANT_info

class ExceptionTableParser:
    @classmethod
    def parse(cls, cp_info:list[CONSTANT_info], buffer:BufferedReader|BytesIO) -> Exception_table:
        start_pc = int.from_bytes(buffer.read(2))
        end_pc = int.from_bytes(buffer.read(2))
        handler_pc = int.from_bytes(buffer.read(2))
        catch_type_index = int.from_bytes(buffer.read(2))
        catch_type = cp_info[catch_type_index - 1]

        return {"start_pc":start_pc, "end_pc": end_pc, "handler_pc": handler_pc, "catch_type": catch_type}