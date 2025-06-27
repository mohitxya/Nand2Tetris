class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.current_command = ""
        self.type =['C_ARITHMETIC', 'C_PUSH', 'C_POP', 'C_LABEL', 'C_GOTO', 'C_IF', 'C_FUNCTION', 'C_RETURN', 'C_CALL']
        self.arithmetic_commands = [
            'add', 'sub', 'neg', 'eq', 'gt', 'lt','and', 'or', 'not']
    def parse(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip() # Remove leading and trailing whitespace
                if line and not line.startswith("//"):
                    line = line.split("//")[0].strip() # Remove comments after "//"
                    if line:
                        self.data.append(line)
        return self.data
    def hasMoreCommands(self):
        return len(self.data) > 0
    def advance(self):
        if self.hasMoreCommands():
            self.current_command = self.data.pop(0)
            return self.current_command
        return None
    def commandType(self):
        if self.current_command:
            parts = self.current_command.split()
            temp = parts[0] if len(parts) > 0 else None
            if temp in self.arithmetic_commands:
                return 'C_ARITHMETIC'
            elif temp == 'push':
                return 'C_PUSH'
            elif temp == 'pop':
                return 'C_POP'
        return None
    def arg1(self):
        if self.current_command:
            parts = self.current_command.split()
            command_type = self.commandType()
            
            if command_type == 'C_ARITHMETIC':
                return parts[0]  # Return the arithmetic command itself
            elif command_type in ['C_PUSH', 'C_POP']:
                return parts[1] if len(parts) > 1 else None  # Return the memory segment
            
        return None
    def arg2(self):
        if self.current_command:
            parts = self.current_command.split()
            return parts[2] if len(parts) > 2 else None
        # Does not apply to arithmetic commands
        return None
    def get_data(self):
        return self.data