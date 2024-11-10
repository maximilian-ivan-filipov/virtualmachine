class Memory:
    def __init__(self):
        self.variables = {}

    def allocate(self, var_name, value):
        if var_name in self.variables:
            raise ValueError(f"Variable '{var_name}' already exists")
        if isinstance(value, int):
            self.variables[var_name] = value
        elif isinstance(value, float):
            self.variables[var_name] = value
        elif isinstance(value, str) and len(value) == 1:
            self.variables[var_name] = value
        else:
            raise TypeError("Value must be an integer, float, or single character")

    def read(self, var_name):
        if var_name not in self.variables:
            raise KeyError(f"Variable '{var_name}' not found")
        return self.variables[var_name]

    def write(self, var_name, value):
        if var_name not in self.variables:
            raise KeyError(f"Variable '{var_name}' not found")
        if not isinstance(value, (int, float, str)) or (isinstance(value, str) and len(value) != 1):
            raise TypeError("Value must be an integer, float, or single character")
        self.variables[var_name] = value

    def free(self, var_name):
        if var_name not in self.variables:
            raise KeyError(f"Variable '{var_name}' not found")
        del self.variables[var_name]

    def declare_and_initialize(self, var_name, value):
        self.allocate(var_name)
        self.write(var_name, value)
