class access_flag_parser:
    ACCESS_FLAG_TABLE : dict[int, str] = {
        0x01: "ACC_PUBLIC",
        0x10: "ACC_FINAL",
        0x20: "ACC_SUPER",
        0x0200: "ACC_INTERFACE",
        0x0400: "ACC_ABSTRACT",
        0x1000: "ACC_SYNTHETIC",
        0x2000: "ACC_ANNOTATION",
        0x4000: "ACC_ENUM",
        0x8000: "ACC_MODULE"
    }

    @classmethod
    def parse(cls,bitmask:int) -> list[str]:
        access_flags = []
        for flag_bit in cls.ACCESS_FLAG_TABLE.keys():
            if (flag_bit & bitmask):
                access_flags.append(cls.ACCESS_FLAG_TABLE[flag_bit])
            
        return access_flags

