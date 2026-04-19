from access_flag.access_flag_types import AccessFlag

class access_flag_parser:
    ACCESS_FLAG_TABLE : dict[int, AccessFlag] = {
        0x01: AccessFlag.ACC_PUBLIC,
        0x02: AccessFlag.ACC_PRIVATE,
        0x04: AccessFlag.ACC_PROTECTED,
        0x08: AccessFlag.ACC_STATIC,
        0x10: AccessFlag.ACC_FINAL,
        0x20: AccessFlag.ACC_SUPER,
        0x40: AccessFlag.ACC_VOLATILE,
        0x80: AccessFlag.ACC_TRANSIENT,
        0x0200: AccessFlag.ACC_INTERFACE,
        0x0400: AccessFlag.ACC_ABSTRACT,
        0x1000: AccessFlag.ACC_SYNTHETIC,
        0x2000: AccessFlag.ACC_ANNOTATION,
        0x4000: AccessFlag.ACC_ENUM,
        0x8000: AccessFlag.ACC_MODULE
    }

    @classmethod
    def parse(cls,bitmask:int) -> list[AccessFlag]:
        access_flags = []
        for flag_bit in cls.ACCESS_FLAG_TABLE.keys():
            if (flag_bit & bitmask):
                access_flags.append(cls.ACCESS_FLAG_TABLE[flag_bit])
            
        return access_flags

