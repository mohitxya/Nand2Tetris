"""
    Approach: 
    1. Open file and read it's contents.
    2. Discard empty lines and comments.
    FIRST PASS:
    3. Maintain a list and a dictionary. (List: for instructions, Dictionary: new labels,position you encounter)
    SECOND PASS: 
    4. Put instructions through Parser and Code. Resolve variables (if not in symbol_table assign addresses to them) and replace with 
    built in symbol table symbols.
    
"""



import Parser
import Code

symbol_table = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0,  "R1": 1,  "R2": 2,  "R3": 3,
    "R4": 4,  "R5": 5,  "R6": 6,  "R7": 7,
    "R8": 8,  "R9": 9, "R10": 10, "R11": 11,
    "R12": 12,"R13": 13,"R14": 14,"R15": 15,
    "SCREEN": 16384, "KBD": 24576
}

instructions = []
labels={}
line_number=0

if __name__=="__main__":
    with open("./program.asm","r") as file:
        '''instructions = [
            line.split("//")[0].strip()  
            for line in file
            if line.strip() and not line.strip().startswith("//")  
        ]'''

        
        for line in file:
            line = line.strip()
            if line and not line.startswith("//"):
                line = line.split("//")[0].strip()

                if line.startswith('(') and line.endswith(')'):
                    label = line[1:-1]
                    labels[label] = line_number  # Map label to current instruction address
                else:
                    instructions.append(line)
                    line_number += 1  # Only increment for real instructions
                print(instructions)
        # Labels should not have a line number. So instead of list use dictionary and give 0 line number