#!python

import os
import IoContract
import json
import click
import logging
import PolyhedralTerm


def getVarset(aList):
    return set([IoContract.Var(varstr) for varstr in aList])


@click.command()
@click.argument('filename')
def readInputFile(filename):
    assert os.path.isfile(filename)
    with open(filename) as f:
        data = json.load(f)
    contracts = []
    for contKey in ['contract1', 'contract2']:
        c = data[contKey]
        reqs = []
        for key in ['assumptions', 'guarantees']:
            reqs.append([PolyhedralTerm.PolyhedralTerm(term['coefficients'], term['constant']) for term in c[key]])
        cont = IoContract.IoContract(inputVars=getVarset(c['InputVars']), outputVars=getVarset(c['OutputVars']),
            assumptions=PolyhedralTerm.PolyhedralTermSet(set(reqs[0])), guarantees=PolyhedralTerm.PolyhedralTermSet(set(reqs[1])))
        contracts.append(cont)
    logging.info("Contract1:\n" + str(contracts[0]))
    logging.info("Contract2:\n" + str(contracts[1]))
    if data['operation'] == 'composition':
        logging.info("Composed contract:\n" + str(contracts[0].compose(contracts[1])))
    elif data['operation'] == 'quotient':
        logging.info("Contract quotient:\n" + str(contracts[0].quotient(contracts[1])))
    else:
        logging.info("Operation not supported")


 
if __name__ == '__main__':
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    FORMAT1 = "[%(levelname)s:%(funcName)s()] %(message)s"
    FORMAT2 = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(filename='log.log', filemode='w', level = logging.DEBUG, format = FORMAT2)
    readInputFile()