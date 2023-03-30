import pytest
import numpy as np
import numpy.testing as nptest

from lattice import calc_reciprocal, to_vector


def assert_dotprod(left, right, angle):
    left_length = np.sqrt(np.dot(left, left))
    right_length = np.sqrt(np.dot(right, right))

    dotprod = np.dot(left, right) / (left_length * right_length)
    cos_value = np.cos(np.deg2rad(angle))
    nptest.assert_allclose(dotprod, cos_value, atol=0.00001)


def test_vector_cubic():
    a, b, c = 1, 1, 1
    alpha, beta, gamma = 90, 90, 90

    a_vec, b_vec, c_vec = to_vector(a, b, c, alpha, beta, gamma)

    nptest.assert_allclose(a_vec, [a, 0, 0], atol=0.00001)
    nptest.assert_allclose(b_vec, [0, b, 0], atol=0.00001)
    nptest.assert_allclose(c_vec, [0, 0, c], atol=0.00001)

    assert_dotprod(a_vec, b_vec, 90.0)
    assert_dotprod(a_vec, c_vec, 90.0)
    assert_dotprod(b_vec, c_vec, 90.0)


def test_vector_hexagonal():
    a, b, c = 1, 1, 3
    alpha, beta, gamma = 90, 90, 120

    a_vec, b_vec, c_vec = to_vector(a, b, c, alpha, beta, gamma)

    nptest.assert_allclose(a_vec, [a, 0, 0], atol=0.00001)
    nptest.assert_allclose(b_vec[2], 0, atol=0.00001)
    nptest.assert_allclose(np.dot(b_vec, b_vec), b * b, atol=0.00001)
    nptest.assert_allclose(c_vec, [0, 0, c], atol=0.00001)

    assert_dotprod(a_vec, b_vec, gamma)
    assert_dotprod(a_vec, c_vec, beta)
    assert_dotprod(b_vec, c_vec, alpha)


def test_vector_monoclinic():
    a, b, c = 1, 2, 3
    alpha, beta, gamma = 60, 70, 80

    a_vec, b_vec, c_vec = to_vector(a, b, c, alpha, beta, gamma)

    nptest.assert_allclose(a_vec, [a, 0, 0], atol=0.00001)
    nptest.assert_allclose(np.dot(b_vec, b_vec), b * b, atol=0.00001)
    nptest.assert_allclose(np.dot(c_vec, c_vec), c * c, atol=0.00001)

    assert_dotprod(a_vec, b_vec, gamma)
    assert_dotprod(a_vec, c_vec, beta)
    assert_dotprod(b_vec, c_vec, alpha)


def test_reciprocal():
    a, b, c = 1, 1, 1
    alpha, beta, gamma = 90, 90, 90

    recip = calc_reciprocal(a, b, c, alpha, beta, gamma)

    found = calc_reciprocal(*recip)
    assert found[0] == a
    assert found[1] == b
    assert found[2] == c
    assert found[3] == alpha
    assert found[4] == beta
    assert found[5] == gamma


if __name__ == "__main__":
    pytest.main([__file__])
