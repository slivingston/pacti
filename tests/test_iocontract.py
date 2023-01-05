import gear.iocontract as iocontract
from gear.terms.polyhedra.loaders import readContract


def validate_iocontract(contract):
    return isinstance(contract, iocontract.IoContract)


def create_contracts(num=1):
    """
    Creates `num` number of contracts and returns a list of dicts
    """
    contracts = []
    for i in range(num):
        c = {
            "InputVars": ["i" + str(i)],
            "OutputVars": ["o" + str(i)],
            "assumptions": [{"coefficients": {"i" + str(i): 1}, "constant": i}],
            "guarantees": [{"coefficients": {"o" + str(i): 1}, "constant": 1}],
        }
        contracts.append(c)
    if num == 1:
        return contracts[0]
    else:
        return contracts


def test_validate_iocontract():
    c1, c2 = readContract(create_contracts(num=2))
    print(type(c1))
    assert validate_iocontract(c1)
    assert validate_iocontract(c2)


def test_contract_equality():
    pass
