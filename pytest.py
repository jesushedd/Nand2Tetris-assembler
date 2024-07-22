from assembler import *

assert parse("   // JAJAJA")['type'] == "COMMENT", "Should detect comment"
assert parse("@786")['type'] == "A_INSTRUCTION", "Should A_INSTRUCTION"
assert parse("M=0")['type'] == "C_INSTRUCTION", "Should C_INSTRUCTION" 



#Parse  variable test
assert parse("@unaVariable")['type'] == 'VARIABLE'
#Parse label test
assert parse("(EQUIQUETAS)")['type'] == 'LABEL'
assert parse("(NO_ETIQUETAS)")['type'] != 'LABEL'
assert parse("(1ETIQUETAS)")['type'] != 'LABEL'
assert parse("(NO.TAS)")['type'] != 'LABEL'
assert parse("(NOETI2QUETAS)")['type'] == 'LABEL'



