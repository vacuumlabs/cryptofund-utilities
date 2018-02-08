class Enum():
    pass

def create_enum(*constants):
    result = Enum()
    for constant in constants:
        setattr(result, constant, constant)
    result.__all__ = constants
    return result
