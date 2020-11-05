from interpreter.interpreter import Interpreter


class CanOpenInterpreter(Interpreter):
    def __init__(self):
        super().__init__()

    def inform_interpreter(self, sdo_object):
        # Work in progress
        print(sdo_object)
    
    def interpret_object(self):
        pass