import numpy as np


class Lattice:
    def __init__(self, a=0.0, b=0.0, c=0.0, alpha=0.0, beta=0.0, gamma=0.0, a_vec=None, b_vec=None, c_vec=None):
        if Lattice.__scalars_are_valid(a, b, c, alpha, beta, gamma):
            self.set_scalars(a, b, c, alpha, beta, gamma)
        elif Lattice.__vectors_are_valid(a_vec, b_vec, c_vec):
            self.set_vectors(a_vec, b_vec, c_vec)
        else:
            raise RuntimeError("Do not know how to initialize Lattice from supplied parameters")

    def __scalars_are_valid(a, b, c, alpha, beta, gamma) -> bool:
        return a > 0 and b > 0 and c > 0 and alpha > 0 and beta > 0 and gamma > 0

    def set_scalars(self, a, b, c, alpha, beta, gamma):
        if not Lattice.__scalars_are_valid(a, b, c, alpha, beta, gamma):
            raise ValueError("Scalar values are invalid")
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

    def __vectors_are_valid(a_vec, b_vec, c_vec) -> bool:
        def is_ok(vector) -> bool:
            if vector is None:
                return False
            if len(vector) != 3:
                return False
            return True

        return is_ok(a_vec) and is_ok(b_vec) and is_ok(c_vec)

    def set_vectors(self, a_vec, b_vec, c_vec):
        if not Lattice.__vectors_are_valid(a_vec, b_vec, c_vec):
            raise ValueError("Vector values are invalid")
        self.a_vec = np.asarray(a_vec)
        self.b_vec = np.asarray(b_vec)
        self.c_vec = np.asarray(c_vec)

    @property
    def volume(self) -> float:
        return np.dot(self.a_vec, np.cross(self.b_vec, self.c_vec))

    def reciprocal(self):
        # cache the value
        volume = self.volume

        a_vec = np.cross(self.b_vec, self.c_vec) / volume
        b_vec = np.cross(self.c_vec, self.a_vec) / volume
        c_vec = np.cross(self.a_vec, self.b_vec) / volume

        return Lattice(a_vec=a_vec, b_vec=b_vec, c_vec=c_vec)

    def assert_allclose(self, other, atol=0.00001):
        np.testing.assert_allclose(self.a_vec, other.a_vec, atol=atol)
        np.testing.assert_allclose(self.b_vec, other.b_vec, atol=atol)
        np.testing.assert_allclose(self.c_vec, other.c_vec, atol=atol)
