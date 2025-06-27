class CodeWriter:
    def __init__(self):
        self.filename = None
        self.name=None  # Name of the file without extension
        # File to write the assembly code
        self.file = None
        self.label_counter = 0  # For generating unique labels
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
            "static": 16    # static variables start at RAM[16], like variables.
        }
        
        # Stack pointer
        self.stack_pointer = 0  # RAM[0] contains stack pointer
    def write(self, code):
        self.file.write(code + '\n')

    def setFileName(self, filename):
        if isinstance(filename, str):
            # If a string is provided, treat it as a filename
            self.filename = filename
            self.name=self.filename.split('.')[0] if self.filename else None
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
            # Comparison operations (need labels for branching)
            self.write(f"// {command}")
            self.write("@SP")
            self.write("AM=M-1")  # Decrement SP and go to top of stack
            self.write("D=M")     # Store first value in D
            self.write("A=A-1")   # Go to second value
            self.write("D=M-D")   # D = second - first
            
            # Generate unique labels
            true_label = f"{command.upper()}_TRUE_{self.label_counter}"
            end_label = f"{command.upper()}_END_{self.label_counter}"
            self.label_counter += 1
            
            self.write(f"@{true_label}")
            
            if command == 'eq':
                self.write("D;JEQ")   # Jump if equal (D == 0)
            elif command == 'gt':
                self.write("D;JGT")   # Jump if greater (D > 0)
            elif command == 'lt':
                self.write("D;JLT")   # Jump if less (D < 0)
            
            # False case: push 0
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=0")
            self.write(f"@{end_label}")
            self.write("0;JMP")
            
            # True case: push -1 (true in Hack)
            self.write(f"({true_label})")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=-1")
            
            self.write(f"({end_label})")
            
        else:
            raise ValueError(f"Unknown arithmetic command: {command}")
    def writePushPop(self, command, segment, index):
        command = command.lower()
        segment = segment.lower()
        
        if command == 'push':
            if segment == 'constant':
                self.write(f"// push constant {index}")
                self.write(f"@{index}")
                self.write("D=A")
                self.write("@SP")
                self.write("A=M")
                self.write("M=D")
                self.write("@SP")
                self.write("M=M+1")
            elif segment in self.segment_pointers:
                self.write(f"// push {segment} {index}")
                self.write(f"@{self.segment_pointers[segment]}")
                self.write("D=M")
                self.write(f"@{index}")
                self.write("A=D+A")  # A points to the segment + index
                self.write("D=M")
                self.write("@SP")   
                self.write("A=M")
                self.write("M=D")
                self.write("@SP")   
                self.write("M=M+1")
            elif segment in self.fixed_segments:
                if segment == 'temp':
                    self.write(f"// push temp {index}")
                    self.write(f"@{self.fixed_segments[segment] + int(index)}")
                elif segment == 'pointer':
                    if index in ['0', '1']:
                        self.write(f"// push pointer {index}")
                        self.write(f"@{self.fixed_segments[segment] + int(index)}")
                    else:
                        raise ValueError(f"Invalid pointer index: {index}. Must be 0 or 1.")
                elif segment == 'static':
                    self.write(f"// push static {index}")
                    self.write(f"@{self.name}.{int(index)}")
                
                self.write("D=M")
                self.write("@SP")
                self.write("A=M")
                self.write("M=D")
                self.write("@SP")
                self.write("M=M+1")
            else:
                raise ValueError(f"Unknown segment for push: {segment}")
        elif command == 'pop':
            if segment in self.segment_pointers:
                self.write(f"// pop {segment} {index}")
                self.write(f"@{self.segment_pointers[segment]}")
                self.write("D=M")
                self.write(f"@{index}")
                self.write("D=D+A")
                self.write("@R13")
                self.write("M=D")  # Store address in R13
                self.write("@SP")
                self.write("AM=M-1")  # Decrement SP and go to top of
                self.write("D=M")
                self.write("@R13")
                self.write("A=M")
                self.write("M=D")  # Store value at address in R13
            elif segment in self.fixed_segments:
                self.write(f"// pop {segment} {index}")
                self.write("@SP")
                self.write("AM=M-1")  # Decrement SP and go to top of stack
                self.write("D=M")     # Read value FROM stack into D
                
                if segment == 'temp':
                    self.write(f"@{self.fixed_segments[segment] + int(index)}")
                elif segment == 'pointer':
                    if index in ['0', '1']:
                        self.write(f"@{self.fixed_segments[segment] + int(index)}")
                    else:
                        raise ValueError(f"Invalid pointer index: {index}. Must be 0 or 1.")
                elif segment == 'static':
                    self.write(f"@{self.name}.{int(index)}")
                
                self.write("M=D")     # Store value TO the target location
            else:
                raise ValueError(f"Cannot pop to segment: {segment}")
        else:
            raise ValueError(f"Unknown command: {command}")

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()