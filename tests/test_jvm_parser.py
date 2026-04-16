from jvm_parser import JVMParser
import unittest
from io import BytesIO

class TestJVMParser(unittest.TestCase):
    def setUp(self) -> None:
        self.jvmParser = JVMParser()
        self.byteCode = b'\xca\xfe\xba\xbe\x00\x00\x00F\x00\x1b\n\x00\x02\x00\x03\x07\x00\x04\x0c\x00\x05\x00\x06\x01\x00\x10java/lang/Object\x01\x00\x06<init>\x01\x00\x03()V\t\x00\x08\x00\t\x07\x00\n\x0c\x00\x0b\x00\x0c\x01\x00\x10java/lang/System\x01\x00\x03out\x01\x00\x15Ljava/io/PrintStream;\n\x00\x0e\x00\x0f\x07\x00\x10\x0c\x00\x11\x00\x12\x01\x00\x13java/io/PrintStream\x01\x00\x07println\x01\x00\x04(I)V\x07\x00\x14\x01\x00\x04Main\x01\x00\x04Code\x01\x00\x0fLineNumberTable\x01\x00\x04main\x01\x00\x16([Ljava/lang/String;)V\x01\x00\nSourceFile\x01\x00\tMain.java\x00 \x00\x13\x00\x02\x00\x00\x00\x00\x00\x02\x00\x00\x00\x05\x00\x06\x00\x01\x00\x15\x00\x00\x00\x1d\x00\x01\x00\x01\x00\x00\x00\x05*\xb7\x00\x01\xb1\x00\x00\x00\x01\x00\x16\x00\x00\x00\x06\x00\x01\x00\x00\x00\x01\x00\t\x00\x17\x00\x18\x00\x01\x00\x15\x00\x00\x00$\x00\x02\x00\x01\x00\x00\x00\x08\xb2\x00\x07\x05\xb6\x00\r\xb1\x00\x00\x00\x01\x00\x16\x00\x00\x00\n\x00\x02\x00\x00\x00\x03\x00\x07\x00\x04\x00\x01\x00\x19\x00\x00\x00\x02\x00\x1a'
        return super().setUp()
    
    def test_parse_magic(self):
        buffer = BytesIO(self.byteCode)
        result = self.jvmParser.parse(buffer)
        self.assertEqual(result['magic'], "0xcafebabe")

    def test_parse_minor_version(self):
        buffer = BytesIO(self.byteCode)
        result = self.jvmParser.parse(buffer)
        self.assertEqual(result['minor_version'], 0)

    def test_parse_minor_version_11(self):
        modified = bytearray(self.byteCode)
        # minor_version 11
        modified[4] = 0x00
        modified[5] = 0x0b
        
        buffer = BytesIO(modified)
        result = self.jvmParser.parse(buffer)
        self.assertEqual(result['minor_version'], 11)

    def test_parse_major_version(self):
        buffer = BytesIO(self.byteCode)
        result = self.jvmParser.parse(buffer)
        self.assertEqual(result['major_version'], 70)
    
    def test_parse_major_version_562(self):
        modified = bytearray(self.byteCode)
        # major_version 562
        modified[6] = 0x02
        modified[7] = 0x32
        buffer = BytesIO(modified)
        result = self.jvmParser.parse(buffer)
        self.assertEqual(result['major_version'], 562)
