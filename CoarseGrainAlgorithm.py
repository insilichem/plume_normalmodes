#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Algorithm to do Coarse Grain
Same beta for same group
To pass to CalcNormalModes.calc_normal_modes()
"""

import prody


def alg1(moldy, n=7):
    """
    Coarse Grain Algorithm 1: groups per residues

    Parameters
    ----------
    moldy : prody.AtomGroup
    n : int, optional, default=7
        number of residues per group

    Returns
    ------
    moldy: prody.AtomGroup
        New betas added
    """
    group = 1
    alg1.title = 'Residues'
    for chain in moldy.iterChains():
        # selection = moldy.select('chain {}'.format(chain.getChid()))
        num_residues = sorted(list(set(chain.getResnums())))
        chain_name = chain.getChid()
        for a, b in chunker(len(num_residues), n):
            try:
                start, end = num_residues[a-1], num_residues[b-1]
                selector = 'chain {} and resnum {} to {}'.format(chain_name, start, end)
                selection = moldy.select(selector)
                selection.setBetas(group)
                group += 1
            except AttributeError as e:
                print('Warning: {}'.format(e))
                pass
    return moldy


def alg2(moldy, n=100):
    """
    Coarse Grain Algorithm 2: groups per mass percentage

    Parameters
    ----------
    moldy : prody.AtomGroup
    n : int, optional, default=100
        number of groups

    Returns
    -------
    moldy: prody.AtomGroup
        New Betas added
    """

    group = 1
    alg2.title = 'Masses'

    M = sum(moldy.getMasses())
    m = M/n
    mass = None

    for chain in moldy.iterChains():
        # selection = moldy.select('chain {}'.format(chain.getChid()))
        # num_residues = selection.getResnums()[-1]
        # num_atoms = selection.numAtoms()
        mass = 0.

        # for atom in iter(selection):  # atoms a la cadena? residus?
        for atom in chain.iterAtoms():
            atom.setBeta(group)
            mass += atom.getMass()
            if mass > m:
                mass = 0.
                group += 1
        group += 1
    return moldy


def alg3(moldy, n=2):
    """
    Coarse Grain Algorithm 3: Graph algorithm.
        New group when a vertice: have more than n,
                                  have 0 edges
                                  new chain

    Parameters
    ----------
    moldy : prody.AtomGroup
    n : int, optional, default=2
        maximum bonds number

    Returns
    -------
    moldy: prody.AtomGroup
        New Betas added
    """
    group = 1
    alg3.title = 'Graphs'

    for chain in moldy.iterChains():
        # selection = moldy.select('chain {}'.format(chain.getChid()))
        # for atom in iter(selection):
        for atom in chain.iterAtoms():
            atom.setBeta(group)
            if atom.numBonds() > n or atom.numBonds() == 0:
                group += 1
        group += 1
    return moldy


def chunker(end, n):
    for i in range(0, end-n+1, n):
        yield i+1, i+n
    if end % n:
        yield end-end % n+1, end
