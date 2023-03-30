import numpy as np


class Lattice:
    def __init__(self, a, b, c, alpha, beta, gamma):
        self.set_scalars(a, b, c, alpha, beta, gamma)

    def set_scalars(self, a, b, c, alpha, beta, gamma):
        cos_alpha = np.cos(np.deg2rad(alpha))
        cos_beta = np.cos(np.deg2rad(beta))
        cos_gamma = np.cos(np.deg2rad(gamma))
        v_term = np.sqrt(
            1
            - cos_alpha * cos_alpha
            - cos_beta * cos_beta
            - cos_gamma * cos_gamma
            + 2 * cos_alpha * cos_beta * cos_gamma
        )

        sin_gamma = np.sin(np.deg2rad(gamma))

        self.a_vec = np.asarray([a, 0, 0])
        self.b_vec = np.asarray([b * cos_gamma, b * sin_gamma, 0])
        self.c_vec = np.asarray(
            [c * cos_beta, c * (cos_alpha - cos_gamma * cos_beta) / sin_gamma, c * v_term / sin_gamma]
        )

    @property
    def volume(self) -> float:
        return np.dot(self.a_vec, np.cross(self.b_vec, self.c_vec))

    def reciprocal(self):
        # cache the value
        volume = self.volume

        reciprocal = Lattice(1, 1, 1, 90, 90, 90)

        reciprocal.a_vec = np.cross(self.b_vec, self.c_vec) / volume
        reciprocal.b_vec = np.cross(self.c_vec, self.a_vec) / volume
        reciprocal.c_vec = np.cross(self.a_vec, self.b_vec) / volume

        return reciprocal

    def assert_allclose(self, other, atol=0.00001):
        np.testing.assert_allclose(self.a_vec, other.a_vec, atol=atol)
        np.testing.assert_allclose(self.b_vec, other.b_vec, atol=atol)
        np.testing.assert_allclose(self.c_vec, other.c_vec, atol=atol)
