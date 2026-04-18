from io import BufferedReader, BytesIO
from typing import TypedDict

from constant_pool.const_info_parsers import cp_info_parser
from constant_pool.const_info_types import CONSTANT_info

import pprint
import json

class ClassFile(TypedDict):
    magic:str
    minor_version:int
    major_version:int
    constant_pool_count:int
    cp_info:list[CONSTANT_info]

class BytesEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.decode("utf-8")
        return super().default(o)

class JVMParser:
    def parse(self, buffer:BufferedReader|BytesIO) -> ClassFile:
        magic = hex(int.from_bytes(buffer.read(4)))
        minor_version = int.from_bytes(buffer.read(2))
        major_version = int.from_bytes(buffer.read(2))
        constant_pool_count = int.from_bytes(buffer.read(2))
        cp_info = []

        for i in range(1,constant_pool_count):
            info = cp_info_parser.parse(buffer)
            cp_info.append({**info,"debug_i":i})
            

        return {"magic":magic, "minor_version": minor_version, "major_version": major_version, "constant_pool_count":constant_pool_count, "cp_info":cp_info}

with open("Main.class", "rb") as file:
    parser = JVMParser()
    parsedClassFile = parser.parse(file)
    pprint.pp(parsedClassFile)
    with open("output.json","w", encoding="utf-8") as output:
        json.dump(parsedClassFile, output, cls=BytesEncoder, indent=2)

