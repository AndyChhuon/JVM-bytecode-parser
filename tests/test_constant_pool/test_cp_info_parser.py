import unittest
from io import BytesIO
from constant_pool.const_info_parsers import cp_info_parser


class TestCpInfoParser(unittest.TestCase):
    def test_parse_class_info(self):
        buffer = BytesIO(b"\x07\x00\x04")
        result = cp_info_parser.parse(buffer)
        self.assertEqual(result, {
            "tag": 7,
            "name_index": 4,
            "debug": "CONSTANT_Class_info",
        })

    def test_parse_utf8_info(self):
        buffer = BytesIO(b"\x01\x00\x05Hello")
        result = cp_info_parser.parse(buffer)
        self.assertEqual(result, {
            "tag": 1,
            "length": 5,
            "bytes": b"Hello",
            "debug": "CONSTANT_Utf8_info",
        })

    def test_parse_string_info(self):
        buffer = BytesIO(b"\x08\x00\x0e")
        result = cp_info_parser.parse(buffer)
        self.assertEqual(result, {
            "tag": 8,
            "string_index": 14,
            "debug": "CONSTANT_String_info",
        })

    def test_parse_name_and_type(self):
        # tag=12, name_index=5, descriptor_index=6
        buffer = BytesIO(b"\x0c\x00\x05\x00\x06")
        result = cp_info_parser.parse(buffer)
        self.assertEqual(result, {
            "tag": 12,
            "name_index": 5,
            "descriptor_index": 6,
            "debug": "CONSTANT_NameAndType_info",
        })

    def test_parse_fieldref(self):
        # tag=9, class_index=8, name_and_type_index=9
        buffer = BytesIO(b"\x09\x00\x08\x00\x09")
        result = cp_info_parser.parse(buffer)
        self.assertEqual(result, {
            "tag": 9,
            "class_index": 8,
            "name_and_type_index": 9,
            "debug": "CONSTANT_Field_ref_info",
        })

    def test_parse_methodref(self):
        buffer = BytesIO(b"\x0a\x00\x02\x00\x03")
        result = cp_info_parser.parse(buffer)
        self.assertEqual(result, {
            "tag": 10,
            "class_index": 2,
            "name_and_type_index": 3,
            "debug": "CONSTANT_Method_ref_info",
        })

    def test_parse_interface_methodref(self):
        buffer = BytesIO(b"\x0b\x00\x02\x00\x03")
        result = cp_info_parser.parse(buffer)
        self.assertEqual(result, {
            "tag": 11,
            "class_index": 2,
            "name_and_type_index": 3,
            "debug": "CONSTANT_Interface_Method_ref_info",
        })

    def test_unknown_tag_raises(self):
        buffer = BytesIO(b"\x63\x00\x00")
        with self.assertRaises(NotImplementedError) as ctx:
            cp_info_parser.parse(buffer)
        self.assertIn("99 not implemented yet in CP_DICT_PARSERS", str(ctx.exception))

    def test_utf8_empty_string(self):
      buffer = BytesIO(b"\x01\x00\x00")
      result = cp_info_parser.parse(buffer)
      self.assertEqual(result, {
          "tag": 1,
          "length": 0,
          "bytes": b"",
          "debug": "CONSTANT_Utf8_info",
      })

    def test_buffer_consumed_correctly(self):
      buffer = BytesIO(b"\x07\x00\x04\x01\x00\x03Foo")
      first = cp_info_parser.parse(buffer)
      second = cp_info_parser.parse(buffer)
      self.assertEqual(first, {
          "tag": 7,
          "name_index": 4,
          "debug": "CONSTANT_Class_info",
      })
      self.assertEqual(second, {
          "tag": 1,
          "length": 3,
          "bytes": b"Foo",
          "debug": "CONSTANT_Utf8_info",
      })