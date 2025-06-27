from Parser import Parser
from Codewriter import CodeWriter
def main():
    # Initialize the parser with the input file
    parser = Parser("input.vm")
    parser.parse()  # Read and parse the VM commands

    # Initialize the code writer with the output file
    code_writer = CodeWriter()
    code_writer.setFileName("output.asm")

    # Process each command in the parsed data
    while parser.hasMoreCommands():
        command = parser.advance()
        command_type = parser.commandType()

        if command_type == 'C_ARITHMETIC':
            code_writer.writeArithmetic(parser.arg1())
        elif command_type == 'C_PUSH':
            code_writer.writePushPop('push', parser.arg1(), parser.arg2())
        elif command_type == 'C_POP':
            code_writer.writePushPop('pop', parser.arg1(), parser.arg2())
        # Add other command types as needed

    # Close the output file
    code_writer.file.close()