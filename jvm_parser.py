from enum import Enum
from io import BufferedReader, BytesIO
from typing import TypedDict

from constant_pool.const_info_parsers import cp_info_parser
from constant_pool.const_info_types import CONSTANT_info
from access_flag.access_flag_parser import access_flag_parser
from access_flag.access_flag_types import AccessFlag
from field_info.field_info_parser import FieldInfoParser
from field_info.fields_info_types import Field_info
from methods_info.methods_info_parser import MethodsInfoParser

import pprint
import json

from methods_info.methods_info_types import Method_info

class ClassFile(TypedDict):
    magic:str
    minor_version:int
    major_version:int
    constant_pool_count:int
    cp_info:list[CONSTANT_info]
    access_flags: list[AccessFlag]
    this_class: CONSTANT_info
    super_class: CONSTANT_info
    interfaces_count: int
    interfaces: list[CONSTANT_info]
    fields_count: int
    fields: list[Field_info]
    methods_count: int
    methods: list[Method_info]

class BytesEncoder(json.JSONEncoder):
      def default(self, o):
          if isinstance(o, bytes):
              try:
                  return o.decode("utf-8")
              except UnicodeDecodeError:
                  return o.hex(" ")
          if isinstance(o, Enum):
              return o.value
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

        fields_count = int.from_bytes(buffer.read(2))
        fields = []
        for _ in range(fields_count):
            field = FieldInfoParser.parse(cp_info, buffer)
            fields.append(field)

        methods_count = int.from_bytes(buffer.read(2))
        methods = []

        for _ in range(methods_count):
            methods.append(MethodsInfoParser.parse(cp_info, buffer))

        return {"magic":magic, "minor_version": minor_version, "major_version": major_version, "constant_pool_count":constant_pool_count, "cp_info":cp_info, "access_flags":access_flags, "this_class": this_class, "super_class":super_class, "interfaces_count":interfaces_count, "interfaces": interfaces, "fields_count": fields_count, "fields":fields, "methods_count": methods_count, "methods": methods}

with open("Main.class", "rb") as file:
    parser = JVMParser()
    parsedClassFile = parser.parse(file)
    pprint.pp(parsedClassFile)
    with open("output.json","w", encoding="utf-8") as output:
        json.dump(parsedClassFile, output, cls=BytesEncoder, indent=2)

