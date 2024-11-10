from typing import List, Union, Dict
from stack import Stack
from memory import Memory
from instruction import *
from dataclasses import dataclass, fields
import sys
from termcolor import colored
from copy import deepcopy
from textwrap import dedent
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from ui import print_ui

@dataclass
class Registers:
    eax: int = 0
    ebx: int = 0
    ecx: int = 0
    edx: int = 0
    esi: int = 0
    edi: int = 0
    ebp: int = 0
    esp: int = 0
    eip: int = 0
    cmp: int = 0

class Machine:
    def __init__(self) -> None:
        self.stack: Stack = Stack()
        self.registers: Registers = Registers()
        self.memory: Memory = Memory()
        self.instructions: List[str] = []
        self.stepper_enabled: bool = False
        self.previous_registers = None
        self.labels: Dict[str, int] = {}  # Dictionary to store labels

    def load_program_from_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                self.instructions = [
                    line.strip()
                    for line in file
                    if line.strip() and not line.strip().startswith(';')
                ]
                # Collect labels
                for i, instruction in enumerate(self.instructions):
                    parts = instruction.split()
                    if parts[0].endswith(':'):
                        label = parts[0][:-1]  # Remove the colon
                        self.labels[label] = i + 1  # Point to the next instruction
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
        except IOError:
            print(f"Error: Unable to read file '{file_path}'.")
            sys.exit(1)

    def execute_program(self) -> None:
        while self.registers.eip < len(self.instructions):
            print_ui(self, self.registers.eip)
            instruction = self.instructions[self.registers.eip]
            parts = instruction.split()
            
            if parts[0] == "var":
                self.declare_variable(instruction)
            else:
                # Existing logic for handling other instructions
                if parts[0].endswith(':'):
                    self.registers.eip += 1
                    continue
                
                op = parts[0]
                args = [arg.rstrip(',') for arg in parts[1:]]

                if hasattr(self, op):
                    method = getattr(self, op)
                    method(*args)
                else:
                    print(f"Unknown instruction: {op}")
            
            self.registers.eip += 1

            if self.stepper_enabled:
                input("Press Enter to execute the next instruction...")

        print_ui(self, len(self.instructions))  # Show final state
        print("Program execution completed.")

    def get_value(self, operand: str) -> int:
        if operand in [f.name for f in fields(self.registers)]:
            return getattr(self.registers, operand)
        elif operand in self.memory.variables:
            return self.memory.read(operand)
        else:
            try:
                return int(operand)
            except ValueError:
                raise ValueError(f"Invalid operand: {operand}")

    def mov(self, dest: str, src: str) -> None:
        value = self.get_value(src)
        if dest in [f.name for f in fields(self.registers)]:
            setattr(self.registers, dest, value)
        elif dest in self.memory.variables:
            self.memory.write(dest, value)
        else:
            raise ValueError(f"Invalid destination: {dest}")

    def add(self, dest: str, src: str) -> None:
        dest_value = self.get_value(dest)
        src_value = self.get_value(src)
        result = dest_value + src_value
        if dest in [f.name for f in fields(self.registers)]:
            setattr(self.registers, dest, result)
        elif dest in self.memory.variables:
            self.memory.write(dest, result)
        else:
            raise ValueError(f"Invalid destination: {dest}")
    
    def inc(self, register: str) -> None:
        register_value = getattr(self.registers, register)
        setattr(self.registers, register, register_value + 1)

    def cmp(self, arg1: str, arg2: str) -> None:
        value1 = self.get_value(arg1)
        value2 = self.get_value(arg2)
        if value1 == value2:
            self.registers.cmp = True
        else:
            self.registers.cmp = False

    def jmp(self, target: str) -> None:
        if target in self.labels:
            self.registers.eip = self.labels[target] - 1  # -1 because eip will be incremented after this
        else:
            try:
                address = int(target)
                self.registers.eip = address - 1  # -1 because eip will be incremented after this
            except ValueError:
                print(f"Error: Invalid jump target: {target}")

    def je(self, target: str) -> None:
        if self.registers.cmp == True:
            self.jmp(target)

    def push(self, value: str) -> None:
        self.stack.push(self.get_value(value))

    def pop(self, register: str) -> None:
        value = self.stack.pop()
        setattr(self.registers, register, value)

    def debug(self) -> None:
        print("Register values:")
        for field in fields(self.registers):
            value = getattr(self.registers, field.name)
            print(f"{field.name.upper()}: {value}")

    def print_stack(self) -> None:
        self.stack.print_stack()

    def print_registers(self, old_registers) -> None:
        print("Register values:")
        for field in fields(self.registers):
            old_value = getattr(old_registers, field.name)
            new_value = getattr(self.registers, field.name)
            if old_value != new_value:
                print(f"{field.name.upper()}: {colored(new_value, 'green')} (was {old_value})")
            else:
                print(f"{field.name.upper()}: {new_value}")
        print()

    def enable_stepper(self) -> None:
        self.stepper_enabled = True

    def disable_stepper(self) -> None:
        self.stepper_enabled = False

    def declare_variable(self, instruction):
        parts = instruction.split()
        if len(parts) != 4 or parts[0] != "var" or parts[2] != "=":
            raise SyntaxError(f"Invalid variable declaration: {instruction}")
        
        var_name = parts[1]
        value = parts[3]

        # Determine the type and convert the value
        if value.isdigit():
            value = int(value)
        elif value.replace('.', '', 1).isdigit():
            value = float(value)
        elif len(value) == 3 and value[0] == value[2] == "'":
            value = value[1]  # Extract the character between quotes
        else:
            raise ValueError(f"Invalid value in variable declaration: {value}")

        self.memory.allocate(var_name, value)
