"""
    Approach: 
    1. Open file and read it's contents.
    2. Discard empty lines and comments.

    FIRST PASS:

    3. Maintain a list and a dictionary. (List: for instructions, Dictionary(symbol table): new labels,position you encounter)
    
    SECOND PASS: 

    4. Put instructions through Parser and Code. Resolve variables (if not in symbol_table assign addresses to them) and replace with 
    built in symbol table symbols.
    
"""



from Parser import Parser
from Code import Code
import sys

symbol_table = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0,  "R1": 1,  "R2": 2,  "R3": 3,
    "R4": 4,  "R5": 5,  "R6": 6,  "R7": 7,
    "R8": 8,  "R9": 9, "R10": 10, "R11": 11,
    "R12": 12,"R13": 13,"R14": 14,"R15": 15,
    "SCREEN": 16384, "KBD": 24576
}

instructions = []
binary=[]
line_number=0
var_add=16

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: python assembler.py <inputfile.asm> <outputfile.hack>")
        sys.exit(1)

    input_file = sys.argv[1]
    out_file=sys.argv[2]
    parse=Parser()
    code=Code()
    with open(input_file,"r") as file:
        # 1st pass: 
        
        for line in file:
            line = line.strip()
            if line and not line.startswith("//"):
                line = line.split("//")[0].strip()

                if line.startswith('(') and line.endswith(')'):
                    label = line[1:-1]
                    if label not in symbol_table: # changed from label.upper()
                        symbol_table[label] = line_number
                    else:
                        raise ValueError(f"Label '{label}' already defined in symbol table!")

                else:
                    instructions.append(line)
                    line_number += 1  # Only increment for real instructions
        #print(instructions)
        #print(symbol_table)
        # Labels should not have a line number. So instead of list use dictionary and give 0 line number
        # 2nd PASS: 
        # 1. take instruction-> classify A or C -> parser -> code: produce it's binary
        # 2. find variables. if not in symbol table add them. starting from address 16. Replace with their address.

        for instruction in instructions:
            bin_code=None
            val=None
            destn=None
            compn=None
            jumpn=None

            # A instruction using label
            if instruction[0]=='@' and (not instruction.split("@")[1].isdigit()):
                sym=instruction.split("@")[1]
                
                if sym in symbol_table:
                    val=symbol_table[sym]
                else:
                    symbol_table[sym]=var_add
                    val=var_add
                    var_add+=1
                bin_code = format(val, '016b')

                binary.append(bin_code)
            # A instruction without label
            elif instruction[0]=='@' and  instruction.split("@")[1].isdigit():
                val = parse.address(instruction)
                bin_code='0'+code.address(val)
                binary.append(bin_code)
            # C instruction 
            else:
                #111 + comp + dest + jump
                destn=parse.dest(instruction)
                compn=parse.comp(instruction)
                jumpn=parse.jump(instruction)

                bin_code='111'+ code.comp(compn)+code.dest(destn)+code.jump(jumpn)
                binary.append(bin_code)

    
    # After all instructions have been processed and binary list is filled:
    with open(out_file, "w") as out_file:
        for line in binary:
            out_file.write(line + "\n")
