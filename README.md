# Simple Virtual Machine

This project implements a simple virtual machine that can execute a custom assembly-like language.

## How to Run

To execute a program on this virtual machine, use the following command:

```
python3 main.py <instruction_file> [--step]
```

- `<instruction_file>` is the path to your assembly-like code file.
- The optional `--step` flag enables step-by-step execution mode.

### Step-by-Step Execution

When you use the `--step` option, the program will pause after each instruction, allowing you to see the state of the machine (registers, variables, stack) after every step. This is useful for debugging and understanding the execution flow.

Example:

```
python3 main.py my_program.asm --step
```

This will execute `my_program.asm` in step-by-step mode, pausing after each instruction for you to examine the machine state.

## Example Code

Here's an example of the supported code:

```assembly
jmp start

secret:
    mov number1, -9
    mov number2, -7
    jmp done

start:
    var number1 = 4
    var number2 = 7

    mov eax, number1
    mov ebx, number2 
    add eax, ebx
    jmp secret

done:
    mov eax, number1
    mov ebx, number2
```

## Supported Features

1. **Global Variables**: Declare and initialize global variables using the `var` keyword.
   Example: `var number1 = 4`

2. **mov Instruction**: Move values between registers, from memory to registers, or from registers to memory.
   Example: `mov eax, number1`

3. **add Instruction**: Add values and store the result.
   Example: `add eax, ebx`

4. **sub Instruction**: Subtract values and store the result.
   Example: `sub eax, ebx`

5. **jmp Instruction**: Jump to a labeled address in the code.
   Example: `jmp start`

6. **Labels**: Define points in the code that can be jumped to.
   Example: `start:`

7. **Registers**: The VM supports several registers (eax, ebx, ecx, edx, esi, edi, ebp, esp, eip).

8. **Stack Operations**: Push and pop values to/from the stack.
   Example: `push eax`, `pop ebx`

9. **Immediate Values**: Use immediate values in instructions.
   Example: `mov eax, 42`

This virtual machine provides a simple yet powerful environment for executing assembly-like code, making it useful for educational purposes or as a foundation for more complex systems.
