class Master:
    def __init__(self):
        print("Master constructor")
        self.setup()

    def setup(self):
        print("Master setup")

class Child(Master):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        print("Child constructor")

    def setup(self):
        super().setup()  # Call the parent class setup method
        print("Child setup")

child = Child()