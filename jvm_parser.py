from io import BufferedReader, BytesIO
from typing import TypedDict

from constant_pool.const_info_parsers import cp_info_parser
from constant_pool.const_info_types import CONSTANT_info
from access_flag.access_flag_parser import access_flag_parser

import pprint
import json

class ClassFile(TypedDict):
    magic:str
    minor_version:int
    major_version:int
    constant_pool_count:int
    cp_info:list[CONSTANT_info]
    access_flags: list[str]
    this_class: CONSTANT_info
    super_class: CONSTANT_info
    interfaces_count: int
    interfaces: list[CONSTANT_info]

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
        access_flags = access_flag_parser.parse(int.from_bytes(buffer.read(2)))

        # constant pool index starts at 1
        this_class = cp_info[int.from_bytes(buffer.read(2)) - 1]
        super_class = cp_info[int.from_bytes(buffer.read(2)) - 1]

        interfaces_count = int.from_bytes(buffer.read(2))

        interfaces = []
        for _ in range(interfaces_count):
            interfaces.append(cp_info[int.from_bytes(buffer.read(2)) - 1])


        return {"magic":magic, "minor_version": minor_version, "major_version": major_version, "constant_pool_count":constant_pool_count, "cp_info":cp_info, "access_flags":access_flags, "this_class": this_class, "super_class":super_class, "interfaces_count":interfaces_count, "interfaces": interfaces}

with open("Main.class", "rb") as file:
    parser = JVMParser()
    parsedClassFile = parser.parse(file)
    pprint.pp(parsedClassFile)
    with open("output.json","w", encoding="utf-8") as output:
        json.dump(parsedClassFile, output, cls=BytesEncoder, indent=2)

