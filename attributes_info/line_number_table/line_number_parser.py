from io import BufferedReader, BytesIO

from attributes_info.line_number_table.line_number_table_types import Line_number_table

class LineNumberTableParser:
    @classmethod
    def parse(cls, buffer:BufferedReader|BytesIO) -> Line_number_table:
        start_pc = int.from_bytes(buffer.read(2))
        line_number = int.from_bytes(buffer.read(2))

        return {"start_pc":start_pc, "line_number": line_number}