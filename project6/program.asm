// Multiplies R0 and R1 and stores the result in R2.
// Uses repeated addition.

@R2
M=0         // Initialize result to 0

@R1
D=M
@i
M=D         // i = R1 (loop counter)

(loop)
@i
D=M
@end
D;JEQ       // if i == 0, goto end

@R0
D=M
@R2
M=D+M       // R2 += R0

@i
M=M-1       // i--

@loop
0;JMP       // goto loop

(end)
@END
0;JMP       // infinite halt loop
