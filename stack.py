class Stack:
    def __init__(self):
        self.mem = []
        self.size: int = 0
        self.sp: int = 0
        self.bp: int = 0

    def push(self, value: int):
        self.mem.append(value)
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("pop from empty stack")
        self.size -= 1
        return self.mem.pop()

    def print_stack(self):
        if not self.mem:
            print("Stack is empty")
        else:
            print("Stack contents (top to bottom):")
            for item in self.mem:
                print(item)
            print("↓ Bottom of stack")