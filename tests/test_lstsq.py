import pytest

from crystalsystems.lattice import LatticeBuilder
from crystalsystems.lstsq import getLattice


@pytest.mark.parametrize("a", [1, 2])
def test_cubic(a):
    lattice = LatticeBuilder.construct_cubic(a)

    # test array of hkl
    hkl = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 2], [2, 2, 0], [1, 2, 3]]
    # fake the observed Q-values
    dSpacing = [lattice.toDspacing(*vals) for vals in hkl]

    obs = getLattice(hkl, dSpacing)

    lattice.assert_allclose(obs)


@pytest.mark.parametrize(("a", "c"), [(1, 1), (1, 2)])
def test_hexagonal(a, c):
    lattice = LatticeBuilder.construct_hexagonal(a, c)

    # test array of hkl
    hkl = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 2], [2, 2, 0], [1, 2, 3]]
    # fake the observed d-values
    dSpacing = [lattice.toDspacing(*vals) for vals in hkl]

    obs = getLattice(hkl, dSpacing)

    print("LATTICE", obs.scalar_lattice_constants())

    lattice.assert_allclose(obs)


if __name__ == "__main__":
    pytest.main([__file__])
