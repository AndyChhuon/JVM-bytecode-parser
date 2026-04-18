import unittest
from access_flag.access_flag_parser import access_flag_parser

class TestAccessFLagParser(unittest.TestCase):
    def setUp(self) -> None:
        self.access_flag_parser = access_flag_parser()
        return super().setUp()
    
    def test_parse_public_final(self):
        flags = self.access_flag_parser.parse(0x31)
        self.assertListEqual(flags, ["ACC_PUBLIC","ACC_FINAL","ACC_SUPER"])
    
    def test_parse_no_flags(self):
      flags = self.access_flag_parser.parse(0x0000)
      self.assertListEqual(flags, [])

    def test_parse_plain_class(self):
        flags = self.access_flag_parser.parse(0x0020)
        self.assertListEqual(flags, ["ACC_SUPER"])

    def test_parse_final_class(self):
        flags = self.access_flag_parser.parse(0x0030)
        self.assertListEqual(flags, ["ACC_FINAL", "ACC_SUPER"])

    def test_parse_public_interface(self):
        flags = self.access_flag_parser.parse(0x0601)
        self.assertListEqual(flags, ["ACC_PUBLIC", "ACC_INTERFACE", "ACC_ABSTRACT"])

    def test_parse_enum(self):
        flags = self.access_flag_parser.parse(0x4030)
        self.assertListEqual(flags, ["ACC_FINAL", "ACC_SUPER", "ACC_ENUM"])