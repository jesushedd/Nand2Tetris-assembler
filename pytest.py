from assembler import *

assert parse("   // JAJAJA")['type'] == "COMMENT", "Should detect comment"
assert parse("@786")['type'] == "A_INSTRUCTION", "Should A_INSTRUCTION"
assert parse("M=0")['type'] == "C_INSTRUCTION", "Should C_INSTRUCTION" 



#Parse  variable test
assert parse("@unaVariable")['type'] == 'A_INSTRUCTION'
#Parse label test
assert parse("(EQUIQUETAS)")['type'] == 'LABEL'
assert parse("(NO_ETIQUETAS)")['type'] != 'LABEL'
assert parse("(1ETIQUETAS)")['type'] != 'LABEL'
assert parse("(NO.TAS)")['type'] != 'LABEL'
assert parse("(NOETI2QUETAS)")['type'] == 'LABEL'
assert parse("\n")['type'] == 'COMMENT'

#manage  a instruction with symbols
sym_table = {'a':'2', 'b': '30', 'c':'50'}

expected = f'{bin(int(sym_table['a']))[2:]:0>16}\n'
actual = a_ins_to_binary("@a" , sym_table)
assert  actual == expected


actual = a_ins_to_binary("@b" , sym_table)
expected = f'{bin(int(sym_table['b']))[2:]:0>16}\n'
assert actual == expected

actual = a_ins_to_binary("@2" , sym_table)
expected = f'{bin(2)[2:]:0>16}\n'
assert actual == expected


actual = a_ins_to_binary("@99" , sym_table)
expected = f'{bin(99)[2:]:0>16}\n'
assert actual == expected

#manage a c instruction with symbols
actual = 







