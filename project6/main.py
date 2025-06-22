import Parser
import Code

symbol_table={} # Symbol,Address



if __name__=="__main__":
    with open("./program.asm","r") as file:
        instructions = [
            line.split("//")[0].strip()  
            for line in file
            if line.strip() and not line.strip().startswith("//")  
        ]
        print(instructions)