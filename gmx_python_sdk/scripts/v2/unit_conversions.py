def oracle_precision(value: float) -> float:
    return 10 ** (30 - value)


def long_precision(value: float) -> float:
    return 10 ** (30 + value)
