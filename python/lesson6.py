def to_sponge_case(text: str) -> str:
    return "".join([c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(text)])


print(to_sponge_case("spongeCase"))
