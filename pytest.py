from assembler import *

assert parse("   // JAJAJA")['type'] == "COMMENT", "Should detect comment"
assert parse("@786")['type'] == "A_INSTRUCTION", "Should A_INSTRUCTION"
assert parse("M=0")['type'] == "C_INSTRUCTION", "Should C_INSTRUCTION" 


