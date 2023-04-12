import numpy as np
import pytest
from lattice import LatticeBuilder


@pytest.mark.parametrize("a", [1, 2])
def test_cubic(a):
    a = 1  # this is also reciprocal lattice constant

    lattice = LatticeBuilder.construct_cubic(a)

    hkl = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 2]]
    Qcrys = [lattice.toQCrysSq(*vals) for vals in hkl]

    # hh, kk, ll, 2hk, 2hl, 2kl
    hkl = [lattice.toTestConstants(*vals) for vals in hkl]

    solution, residuals, rank, singular = np.linalg.lstsq(hkl, Qcrys, rcond=None)
    print("SLN", solution)
    print("RES", residuals)
    print("RNK", rank)
    print("SNG", singular)

    print()
    obs = LatticeBuilder.from_solution(solution)
    print(obs.a_vec)
    print(obs.b_vec)
    print(obs.c_vec)

    lattice.assert_allclose(obs)


if __name__ == "__main__":
    pytest.main([__file__])
