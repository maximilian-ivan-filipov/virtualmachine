

class Instruction:
    def __init__(self):
        self.result: int = 0

    def mov(self, a, b):
        a = b
        return a

    def add(self, a, b):
        result = a + b
        return result
