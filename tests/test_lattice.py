import pytest
import numpy as np
import numpy.testing as nptest

from lattice import LatticeBuilder


def assert_dotprod(left, right, angle):
    left_length = np.sqrt(np.dot(left, left))
    right_length = np.sqrt(np.dot(right, right))

    dotprod = np.dot(left, right) / (left_length * right_length)
    cos_value = np.cos(np.deg2rad(angle))
    nptest.assert_allclose(dotprod, cos_value, atol=0.00001)


def test_vector_cubic():
    a, b, c = 1, 1, 1
    alpha, beta, gamma = 90, 90, 90

    lattice = LatticeBuilder.constructFromScalars(a, b, c, alpha, beta, gamma)

    nptest.assert_allclose(lattice.a_vec, [a, 0, 0], atol=0.00001)
    nptest.assert_allclose(lattice.b_vec, [0, b, 0], atol=0.00001)
    nptest.assert_allclose(lattice.c_vec, [0, 0, c], atol=0.00001)

    assert_dotprod(lattice.a_vec, lattice.b_vec, 90.0)
    assert_dotprod(lattice.a_vec, lattice.c_vec, 90.0)
    assert_dotprod(lattice.b_vec, lattice.c_vec, 90.0)


def test_vector_hexagonal():
    a, b, c = 1, 1, 3
    alpha, beta, gamma = 90, 90, 120

    lattice = LatticeBuilder.constructFromScalars(a, b, c, alpha, beta, gamma)

    nptest.assert_allclose(lattice.a_vec, [a, 0, 0], atol=0.00001)
    nptest.assert_allclose(lattice.b_vec[2], 0, atol=0.00001)
    nptest.assert_allclose(np.dot(lattice.b_vec, lattice.b_vec), b * b, atol=0.00001)
    nptest.assert_allclose(lattice.c_vec, [0, 0, c], atol=0.00001)

    assert_dotprod(lattice.a_vec, lattice.b_vec, gamma)
    assert_dotprod(lattice.a_vec, lattice.c_vec, beta)
    assert_dotprod(lattice.b_vec, lattice.c_vec, alpha)


def test_vector_monoclinic():
    a, b, c = 1, 2, 3
    alpha, beta, gamma = 60, 70, 80

    lattice = LatticeBuilder.constructFromScalars(a, b, c, alpha, beta, gamma)

    nptest.assert_allclose(lattice.a_vec, [a, 0, 0], atol=0.00001)
    nptest.assert_allclose(np.dot(lattice.b_vec, lattice.b_vec), b * b, atol=0.00001)
    nptest.assert_allclose(np.dot(lattice.c_vec, lattice.c_vec), c * c, atol=0.00001)

    assert_dotprod(lattice.a_vec, lattice.b_vec, gamma)
    assert_dotprod(lattice.a_vec, lattice.c_vec, beta)
    assert_dotprod(lattice.b_vec, lattice.c_vec, alpha)


@pytest.mark.parametrize(
    "lattice_constants",
    [(1, 1, 1, 90, 90, 90), (1, 1, 3, 90, 90, 120), (1, 2, 3, 60, 70, 80)],
    ids=("cubic", "hexagonal", "triclinic"),
)
def test_reciprocal_roundtrip(lattice_constants):
    a, b, c = lattice_constants[:3]
    alpha, beta, gamma = lattice_constants[3:]

    lattice = LatticeBuilder.constructFromScalars(a, b, c, alpha, beta, gamma)

    reciprocal = lattice.reciprocal()

    backtoorig = reciprocal.reciprocal()

    lattice.assert_allclose(backtoorig)


if __name__ == "__main__":
    pytest.main([__file__])
