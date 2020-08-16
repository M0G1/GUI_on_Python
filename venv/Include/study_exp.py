from contextlib import redirect_stdout
from io import StringIO
from enum import IntEnum


def printPetNames(owner, **pets):
    print(f"Owner Name: {owner}")
    for pet, name in pets.items():
        print(f"{pet}:{name}")


def contex_manager_and_stream():
    stream = StringIO()
    write_to_stream = redirect_stdout(stream)
    with write_to_stream:
        printPetNames("Muslim", dog="Alpha", turtule=("Uho", "Red", "Hunter"))

    print(stream.getvalue())


def enum_test():
    class Animal(IntEnum):
        ant = 1
        bee = 2
        cat = 3
        dog = 4

    arr = [0, 1, 2, 3, 4]
    print(Animal.ant)
    print(type(Animal.ant))
    print(f"ant have the value {arr[Animal.ant]}")


if __name__ == '__main__':
    enum_test()
