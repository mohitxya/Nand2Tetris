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