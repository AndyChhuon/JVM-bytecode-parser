from typing import TypedDict

from constant_pool.const_info_types import CONSTANT_info

class Exception_table(TypedDict):
    start_pc: int
    end_pc: int
    handler_pc: int
    catch_type: CONSTANT_info
