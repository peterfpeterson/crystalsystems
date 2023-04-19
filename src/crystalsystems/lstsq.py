import numpy as np

from crystalsystems.lattice import LatticeBuilder


def toSolverConstants(h_val, k_val, l_val):
    hh = h_val * h_val
    kk = k_val * k_val
    ll = l_val * l_val
    hk = h_val * k_val
    hl = h_val * l_val
    kl = k_val * l_val

    return (hh, kk, ll, hk, hl, kl)


def getLattice(hkl, dSpacing):
    # convert the hkl to the values used by the least-squares solver
    inputs = np.asarray([toSolverConstants(*vals) for vals in hkl], dtype=float)

    qCrysSq = 1.0 / np.square(dSpacing)

    # gets the solution up to a scale factor
    solution, residuals, rank, singular = np.linalg.lstsq(inputs, qCrysSq, rcond=None)

    print("SLN", solution)  # design matrix result
    print("RES", residuals)  # (Ax - y)**2
    print("RNK", rank)  # number of values
    print("SNG", singular)  # np.linalg.svd(A, compute_uv=False)

    return LatticeBuilder.from_solution(solution)
