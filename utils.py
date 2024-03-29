from decimal import Decimal
from random import uniform


def genCoef() -> Decimal:
    return Decimal(uniform(1, 300))
