import sys
from machine import Machine

if len(sys.argv) < 2:
    print("Usage: python main.py <instruction_file> [--step]")
    sys.exit(1)
file_path = sys.argv[1]

mc = Machine()

if "--step" in sys.argv:
    mc.enable_stepper()

mc.load_program_from_file(file_path)
mc.execute_program()