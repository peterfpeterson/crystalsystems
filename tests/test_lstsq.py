import pytest
from lattice import LatticeBuilder
from lstsq import getLattice


@pytest.mark.parametrize("a", [1, 2])
def test_cubic(a):
    lattice = LatticeBuilder.construct_cubic(a)

    # test array of hkl
    hkl = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 2], [2, 2, 0], [1, 2, 3]]
    # fake the observed Q-values
    QcrysSq = [lattice.toQCrysSq(*vals) for vals in hkl]

    obs = getLattice(hkl, QcrysSq)

    lattice.assert_allclose(obs)


if __name__ == "__main__":
    pytest.main([__file__])
