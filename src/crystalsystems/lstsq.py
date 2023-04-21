import logging

import numpy as np

from crystalsystems.lattice import Lattice, LatticeBuilder

logger = logging.getLogger("crystalsystems.lattice")


def toSolverConstants(h_val, k_val, l_val):
    hh = h_val * h_val
    kk = k_val * k_val
    ll = l_val * l_val
    hk = h_val * k_val
    hl = h_val * l_val
    kl = k_val * l_val

    return (hh, kk, ll, hk, hl, kl)


def getLattice(hkl, dSpacing) -> Lattice:
    # convert the hkl to the values used by the least-squares solver
    inputs = np.asarray([toSolverConstants(*vals) for vals in hkl], dtype=float)

    qCrysSq = 1.0 / np.square(dSpacing)

    # gets the solution up to a scale factor
    solution, residuals, rank, singular = np.linalg.lstsq(inputs, qCrysSq, rcond=None)

    # since we designed the problem to be 6 values, the answer should have 6 values
    if rank != 6:
        raise RuntimeError(f"Something went wrong with lstq, rank of result isn't 6 it is {rank}")

    logging.debug(f"SLN {solution}")  # design matrix result
    logging.debug(f"RES {residuals}")  # (Ax - y)**2
    logging.debug(f"SNG {singular}")  # np.linalg.svd(A, compute_uv=False)

    return LatticeBuilder.from_solution(solution)
