from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from dataclasses import fields
from copy import deepcopy

def print_ui(machine, current_line):
    console = Console()
    console.clear()

    # Set fixed widths for each column
    instruction_width = 30
    register_width = 20
    var_width = 20
    stack_width = 10

    # Instructions (unchanged)
    instructions = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), width=instruction_width)
    for i, instr in enumerate(machine.instructions):
        parts = instr.split()
        if not parts[0].endswith(':'):
            instr = "    " + instr
        
        if i == current_line:
            instructions.add_row(Text(f"→ {instr}", style="yellow bold", overflow="ellipsis"))
        else:
            instructions.add_row(Text(instr, overflow="ellipsis"))

    # Registers (unchanged)
    registers = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), width=register_width)
    for field in fields(machine.registers):
        value = getattr(machine.registers, field.name)
        if machine.previous_registers and getattr(machine.previous_registers, field.name) != value:
            registers.add_row(
                Text(f"{field.name.upper()}:", overflow="ellipsis"),
                Text(f"{value}", style="yellow bold", overflow="ellipsis")
            )
        else:
            registers.add_row(
                Text(f"{field.name.upper()}:", overflow="ellipsis"),
                Text(f"{value}", overflow="ellipsis")
            )

    # Update previous_registers for next comparison
    machine.previous_registers = deepcopy(machine.registers)

    # Global Variables (new)
    variables = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), width=var_width)
    for var_name, value in machine.memory.variables.items():
        variables.add_row(
            Text(f"{var_name}:", overflow="ellipsis"),
            Text(f"{value}", overflow="ellipsis")
        )
    if not machine.memory.variables:
        variables.add_row("No variables")

    # Stack (unchanged)
    stack = Table(box=box.SIMPLE, show_header=False, padding=(0, 1), width=stack_width)
    for item in machine.stack.mem:
        stack.add_row(Text(str(item), overflow="ellipsis"))
    if not machine.stack.mem:
        stack.add_row("Empty")

    # Layout (updated)
    layout = Table(show_header=False, padding=0, box=None)
    layout.add_column(justify="left", width=instruction_width + 2)  # +2 for panel borders
    layout.add_column(justify="center", width=register_width + 2)
    layout.add_column(justify="center", width=var_width + 2)
    layout.add_column(justify="right", width=stack_width + 2)
    layout.add_row(
        Panel(instructions, title="Instructions", border_style="blue", width=instruction_width + 2),
        Panel(registers, title="Registers", border_style="green", width=register_width + 2),
        Panel(variables, title="Variables", border_style="cyan", width=var_width + 2),
        Panel(stack, title="Stack", border_style="red", width=stack_width + 2)
    )

    console.print(layout)

    # if machine.stepper_enabled:
    #     console.input("Press Enter to execute the highlighted instruction...")