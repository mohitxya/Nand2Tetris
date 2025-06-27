class CodeWriter:
    def __init__(self):
        self.filename = None
        self.file = None
        # Memory segment base addresses
        self.segment_pointers = {
            "local": "LCL",     # RAM[1] points to local segment
            "argument": "ARG",  # RAM[2] points to argument segment  
            "this": "THIS",     # RAM[3] points to this segment
            "that": "THAT"      # RAM[4] points to that segment
        }
        
        # Fixed memory locations
        self.fixed_segments = {
            "temp": 5,      # temp 0-7 maps to RAM[5-12]
            "pointer": 3,   # pointer 0-1 maps to RAM[3-4] (THIS/THAT)
            "static": 16    # static variables start at RAM[16]
        }
        
        # Stack pointer
        self.stack_pointer = 0  # RAM[0] contains stack pointer
    def write(self, code):
        self.file.write(code + '\n')

    def setFileName(self, filename):
        if isinstance(filename, str):
            # If a string is provided, treat it as a filename
            self.filename = filename
            self.file = open(filename, 'w')
        else:
            raise ValueError("Filename must be a string.")
    
    def writeArithmetic(self, command):
        command = command.lower()
        
        if command in ['add', 'sub', 'and', 'or']:
            # Binary arithmetic operations
            self.write(f"// {command}")
            self.write("@SP")
            self.write("AM=M-1")  # Decrement SP and go to top of stack
            self.write("D=M")     # Store top value in D
            self.write("A=A-1")   # Go to second value
            
            if command == 'add':
                self.write("M=D+M")   # Second = Second + First
            elif command == 'sub':
                self.write("M=M-D")   # Second = Second - First  
            elif command == 'and':
                self.write("M=D&M")   # Second = Second & First
            elif command == 'or':
                self.write("M=D|M")   # Second = Second | First
                
        elif command in ['neg', 'not']:
            # Unary operations
            self.write(f"// {command}")
            self.write("@SP")
            self.write("A=M-1")   # Go to top of stack (don't decrement SP)
            
            if command == 'neg':
                self.write("M=-M")    # Negate the value
            elif command == 'not':
                self.write("M=!M")    # NOT the value
                
        elif command in ['eq', 'gt', 'lt']:
            # Comparison operations (more complex - need labels)
            self.write(f"// {command}")
            self.write("@SP")
            self.write("AM=M-1")
            self.write("D=M")
            self.write("A=A-1")
            # TO DO: Implement comparison logic with labels
            
        else:
            raise ValueError(f"Unknown arithmetic command: {command}")

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()