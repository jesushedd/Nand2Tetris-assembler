from pathlib import Path
from csv import DictReader
import re


def main():

    symbol_table=dict()
    type_ins:str
    out = str()
    fill_symbol_table(symbol_table)#symble table for ops codes and memory directions
    #Paths for io
    file_path = managePath()
    out_path = file_path.with_suffix(".hack")
    #instruction counter 
    number_of_instruction = -1
    #memory address counter
    memory_address = 16 
    
    with open(file_path) as source:
        
        #First pass to find label symbols
        for line in source:
            countable_instructions = ('A_INSTRUCTION', 'C_INSTRUCTION')
            
            instruction = parse(line)
            #Counting number of instructions
            if instruction['type'] in countable_instructions:
                number_of_instruction +=1
                continue
            """if instruction['type'] == "COMMENT":
                continue
            if instruction['type'] == "A_INSTRUCTION":
                out = out + a_ins_to_binary(instruction['body'], symbol_table)
                continue
            if instruction['type'] == "C_INSTRUCTION":
                out = out + c_ins_to_binary(instruction['body'], symbol_table)
                """
            #Proced only with ROM labels
            if instruction['type'] != 'LABEL':
                continue
            #Fill symbol table with labels
            if instruction['body'] in symbol_table:
                raise ValueError("Label Collission error.")
            symbol_table[instruction['body']] = str(number_of_instruction + 1)
            
        #second pass to find variables symbols and predifined symbols
        source.seek(0)
        for line in source:
            instruction = parse(line)
            #Proceed only with A_instructions that are symbols
            if instruction['type'] != 'A_INSTRUCTION' or instruction['body'][1:].isdecimal():
                continue
            #if symbol already in symbol table pass and continue with next instruction
            if instruction['body'] in symbol_table:
                continue
            symbol_table[instruction['body']] = str(memory_address)

        #Final pass to replace all symbols
        source.seek(0)    
        for line in source:
            instruction = parse(line)
            if instruction['type'] == "COMMENT":
                continue
            if instruction['type'] == "A_INSTRUCTION":
                out = out + a_ins_to_binary(instruction['body'], symbol_table)
                continue
            if instruction['type'] == "C_INSTRUCTION":
                out = out + c_ins_to_binary(instruction['body'], symbol_table)

            

            
    with open(out_path, "w", encoding="UTF-8") as outfile:
        outfile.write(out)



"""Returns a valid Path to a hack.asm file"""
def managePath():
    asm_file = None
    while asm_file is None or not asm_file.exists() or asm_file.suffix != '.asm':
        asm_file_str= input("Enter file path: ")
        asm_file:Path = Path(asm_file_str)
        if not asm_file.is_absolute():
            asm_file= asm_file.resolve()
        if not asm_file.exists() or not asm_file.is_file():
            print("Asm file doesn't exists.")
            continue
        if asm_file.suffix != '.asm':
            print("Incorrect file extension.")
            continue
    return asm_file




"""Load symbol:values from csv file to a dict"""
def fill_symbol_table(table:dict):
    with open("keyvalues.txt") as csv_symbols:
        reader = DictReader(csv_symbols)
        for row in reader:
            table[row['symbol']] = row['value'] 


"""Translade a valid a instruction to its binary interpretation"""
def a_ins_to_binary(a_instruction:str, table:dict) -> str: 
    
    try:
        bin_num = bin(int(a_instruction[1:]))
    except ValueError:
        bin_num = bin(int(table[a_instruction[1:]]))
    bin_num = bin_num[2:]
    return f"{bin_num:0>16}\n"



"""Translade a valid c instruction to its binary interpretation
*** a Valid C instruction: M=M+1,JEQ
                        dest = op, jump"""
def c_ins_to_binary(c_instruction:str, symbTable:dict) -> str:

    binary_ins = "111"#First 3 most significand bits==1, indentifier of c instr

    c_instruction, *jump = c_instruction.split(";")
    *dest, comp = c_instruction.split("=")
    binary_ins = binary_ins + symbTable[f'{comp}']
    if len(dest) != 0:
        binary_ins = binary_ins + symbTable[f'{dest[0]}=']
    else: 
        binary_ins = binary_ins + "000"
    if len(jump) != 0:
        binary_ins = binary_ins + symbTable[jump[0]]
    else:
        binary_ins = binary_ins + "000"
    return binary_ins + "\n"
   

"""Returns a len 2 dictionary with instruction 'type' and 'body' of instruction"""
def parse(line:str):
    # split instrution and comments
    instruction, *_ = line.split("//")
    instruction = instruction.strip()
    type_ins = ""
    #load re patterns
    label_pattern = r'\([a-zA-Z][a-zA-Z0-9]*\)'
    

    #CHECK CASES
    if instruction == "":
        type_ins = "COMMENT"
    elif re.search(label_pattern, instruction):
        type_ins = "LABEL"
        instruction = instruction.replace("(", "").replace(")","")
    elif "@" in line:
        type_ins = "A_INSTRUCTION"
    else:
        type_ins = "C_INSTRUCTION"
    return {'type':type_ins, 'body':instruction}


if __name__ == "__main__":
    main()

        
        


    