def concat_message(num: int, message1: str, message2: str) -> str:
    return ", ".join([message1 if i % 2 == 0 else message2 for i in range(num)])


def print_loves_me(num: int):
    print(concat_message(num, "Loves me", "Loves me not"))


print_loves_me(5)
