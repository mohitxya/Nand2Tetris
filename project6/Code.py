"""
    The Code class has dest_map, comp_map and jump_map defined.
"""


class Code:
    def __init__(self):
        self.dest_map = {
            "null": "000",
            "M":    "001",
            "D":    "010",
            "MD":   "011",
            "A":    "100",
            "AM":   "101",
            "AD":   "110",
            "AMD":  "111"
        }

        self.comp_map = {
            # a=0
            "0":   "0101010",
            "1":   "0111111",
            "-1":  "0111010",
            "D":   "0001100",
            "A":   "0110000",
            "!D":  "0001101",
            "!A":  "0110001",
            "-D":  "0001111",
            "-A":  "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            # a=1
            "M":   "1110000",
            "!M":  "1110001",
            "-M":  "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }

        self.jump_map = {
            "null": "000",
            "JGT":  "001",
            "JEQ":  "010",
            "JGE":  "011",
            "JLT":  "100",
            "JNE":  "101",
            "JLE":  "110",
            "JMP":  "111"
        }

    def dest(self, mnemonic):
        return self.dest_map.get(mnemonic or "null", "000")

    def comp(self, mnemonic):
        if mnemonic not in self.comp_map:
            raise ValueError(f"Invalid comp mnemonic: {mnemonic}")
        return self.comp_map[mnemonic]


    def jump(self, mnemonic):
        return self.jump_map.get(mnemonic or "null", "000")
    def address(self,num):
        return format(num, '016b')

