from io import BufferedReader, BytesIO
from typing import TypedDict

class ClassFile(TypedDict):
    magic:str
    minor_version:int
    major_version:int


class JVMParser:
    def parse(self, buffer:BufferedReader|BytesIO) -> ClassFile:
        magic = hex(int.from_bytes(buffer.read(4)))
        minor_version = int.from_bytes(buffer.read(2))
        major_version = int.from_bytes(buffer.read(2))

        return {"magic":magic, "minor_version": minor_version, "major_version": major_version}

with open("Main.class", "rb") as file:
    parser = JVMParser()
    print(parser.parse(file))
