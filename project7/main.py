from Parser import Parser
from Codewriter import CodeWriter
def main():
    # Initialize the parser with the input file
    import sys

    if len(sys.argv) != 3:
        print("Usage: python myscript.py input.vm output.asm")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    parser = Parser(input_file)
    parser.parse()  # Read and parse the VM commands

    # Initialize the code writer with the output file
    code_writer = CodeWriter()
    code_writer.setFileName(output_file)

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

if __name__ == "__main__":
    main()