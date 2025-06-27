#### VM Translator (I):
- We build implement a Translator capable of translating from our Virtual Machine Code to Hack Assembly code. 
- As far as this project is concerned, only arithmetic, logical and memory access commands are implemented.
- Program Flow and Function Calling will be implemented later.


E.g.
**VM Code**:
``` vm code
push constant 7

```

would transform to **Hack Assembly**:

``` hack assembly
@7        // D = 7
D=A
@SP
A=M       // A = SP
M=D       // *SP = D
@SP
M=M+1     // SP++

```

#### *File Structure*:
```
project7/
├── __pycache__/
├── tests/
│   ├── BasicTest.vm
│   ├── PointerTest.vm
│   ├── SimpleAdd.vm
│   ├── StackTest.vm
│   └── StaticTest.vm
├── Codewriter.py        # Writes Hack assembly code from VM commands
├── Parser.py            # Parses each line of the VM input
├── main.py              # Entry point for the VM translator
├── output.asm           # Output Hack assembly file
└── README.md            # Project description and usage guide


```