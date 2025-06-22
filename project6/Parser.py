"""
    This Parser class has the following methods defined: 
    1. dest(): Given an C-instruction gives the `destination` field.
    2. comp(): Given an C-instruction gives the `computation` field.
    3. jump(): Given an C-instruction gives the `Jump` field.
    4. address(): Given an A-instruction gives the `Address` field.
"""



class Parser:
    def __init__(self):
        self.jump_l=["JGT", "JEQ", "JGE", "JLT", "JNE", "JLE", "JMP","NULL"]

    # can split the c-instruction in to three types: only =, only ;, both = and ;
    # dest = comp; jump
    def dest(self, s):
        # keyword before the = to sign
        instruction = s.replace(" ", "")
        if '=' in instruction and ';' in instruction:
            # dest = comp; jmp
            instruction=instruction.split("=")[0].strip()
        elif '=' in instruction:
            # dest = comp
            instruction=instruction.split("=")[0]
            pass
        else:
            return "null"
        

        return instruction
    def comp(self,s):
        instruction = s.replace(" ", "")
        if '=' in instruction and ';' in instruction:
            #dest=comp;jmp
            instruction=(instruction.split("=")[1]).split(";")[0]
        elif '=' in instruction:
            # dest=comp
            instruction=instruction.split("=")[1]
        elif ';' in instruction:
            # comp;jmp
            instruction=instruction.split(";")[0]
        else:
            return "null"

        return instruction.upper()
    def jump(self,s):
        instruction=s.replace(" ","")
        if '=' in instruction and ';' in instruction:
            # dest = comp; jmp
            temp=instruction.split(";")[1]
            if  temp.upper() in self.jump_l:
                return temp.upper()
        elif '=' in instruction:
            # dest=comp
            return "null"
        elif ';' in instruction:
            # comp;jmp
            temp=instruction.split(";")[1]
            if temp.upper() in self.jump_l:
                return temp.upper()
        elif instruction.upper() in self.jump_l:
            return instruction.upper()
        return "null"
    
    def address(self, s):
        instruction=s.replace(" ","")
        if "@" in instruction:
            instruction=int(instruction.split("@")[1])
        else:
            return "null"
        return instruction
    
