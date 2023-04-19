import numpy as np


class Lattice:
    def __init__(self, a_vec, b_vec, c_vec):
        if Lattice.__vectors_are_valid(a_vec, b_vec, c_vec):
            self.set_vectors(a_vec, b_vec, c_vec)
        else:
            raise RuntimeError("Do not know how to initialize Lattice from supplied parameters")

    @staticmethod
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
        self.a_vec = np.asarray(a_vec, dtype=float)
        self.b_vec = np.asarray(b_vec, dtype=float)
        self.c_vec = np.asarray(c_vec, dtype=float)
        # set things that are almost zero to zero
        self.a_vec[np.isclose(self.a_vec, 0.0)] = 0.0
        self.b_vec[np.isclose(self.b_vec, 0.0)] = 0.0
        self.c_vec[np.isclose(self.c_vec, 0.0)] = 0.0

    @property
    def volume(self) -> float:
        return np.dot(self.a_vec, np.cross(self.b_vec, self.c_vec))

    def scalar_lattice_constants(self):
        # lengths are easy
        a_length = np.sqrt(np.dot(self.a_vec, self.a_vec))
        b_length = np.sqrt(np.dot(self.b_vec, self.b_vec))
        c_length = np.sqrt(np.dot(self.c_vec, self.c_vec))

        def to_angle(left, right, left_length, right_length):
            cos_angle = np.dot(left, right) / (left_length * right_length)
            return np.rad2deg(np.arccos(cos_angle))

        # angles are a little more interesting as a dot product of zero means
        # the lattices are perpendicular
        alpha = to_angle(self.b_vec, self.c_vec, b_length, c_length)
        beta = to_angle(self.a_vec, self.c_vec, a_length, c_length)
        gamma = to_angle(self.a_vec, self.b_vec, a_length, b_length)

        return (a_length, b_length, c_length, alpha, beta, gamma)

    def reciprocal(self):
        # cache the value
        volume = self.volume

        a_vec = np.cross(self.b_vec, self.c_vec) / volume
        b_vec = np.cross(self.c_vec, self.a_vec) / volume
        c_vec = np.cross(self.a_vec, self.b_vec) / volume

        return Lattice(a_vec=a_vec, b_vec=b_vec, c_vec=c_vec)

    def toQCrysSq(self, h_val, k_val, l_val):
        """Calculate the Qcrys making the assumption that this is the direct space lattice"""
        matrix = self.toB()
        vec = np.dot(matrix, [h_val, k_val, l_val])

        return np.dot(vec, vec)

    def toB(self):
        """Calculates the B-matrix with the assumption that this is the direct-space lattice"""
        reciprocal = self.reciprocal()
        astar, bstar, cstar, alphastar, betastar, gammastar = reciprocal.scalar_lattice_constants()

        cos_alpha = np.cos(np.deg2rad(alphastar))
        cos_beta = np.cos(np.deg2rad(betastar))
        sin_beta = np.sin(np.deg2rad(betastar))
        cos_gamma = np.cos(np.deg2rad(gammastar))
        sin_gamma = np.sin(np.deg2rad(gammastar))

        _, _, c_length, _, _, _ = self.scalar_lattice_constants()

        matrix = [
            [astar, bstar * cos_gamma, cstar * cos_beta],
            [0, bstar * sin_gamma, -1 * cstar * sin_beta * cos_alpha],
            [0, 0, 1 / c_length],
        ]
        return np.asarray(matrix)

    def assert_allclose(self, other, atol=0.00001):
        # this is more consistent/understandable when looking at scalar constants
        lattice_self = self.scalar_lattice_constants()
        lattice_other = other.scalar_lattice_constants()

        for me, you, label in zip(lattice_self, lattice_other, ["a", "b", "c", "alpha", "beta", "gamma"]):
            np.testing.assert_allclose(me, you, atol=atol, err_msg=label)


def get_angle_from_dot(dotprod: float, left_scalar: float, right_scalar: float) -> float:
    cos_ang = 0.5 * dotprod / (left_scalar * right_scalar)
    if np.isclose(cos_ang, 0.0):
        return 90.0
    else:
        return np.rad2deg(np.arccos(cos_ang))


class LatticeBuilder:
    @staticmethod
    def construct_from_scalars(
        a: float, b: float, c: float, alpha: float, beta: float, gamma: float  # pylint: disable=invalid-name
    ) -> Lattice:
        if not LatticeBuilder.__scalars_are_valid(a, b, c, alpha, beta, gamma):
            raise RuntimeError("scalar values are invalid")

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

        a_vec = np.asarray([a, 0, 0])
        b_vec = np.asarray([b * cos_gamma, b * sin_gamma, 0])
        c_vec = np.asarray([c * cos_beta, c * (cos_alpha - cos_gamma * cos_beta) / sin_gamma, c * v_term / sin_gamma])

        return Lattice(a_vec, b_vec, c_vec)

    @staticmethod
    def __scalars_are_valid(
        a: float, b: float, c: float, alpha: float, beta: float, gamma: float  # pylint: disable=invalid-name
    ) -> bool:
        return a > 0 and b > 0 and c > 0 and alpha > 0 and beta > 0 and gamma > 0

    # TODO should this use the residuals?
    @staticmethod
    def from_solution(solution) -> Lattice:
        # lengths are easy
        a_star = np.sqrt(solution[0])
        b_star = np.sqrt(solution[1])
        c_star = np.sqrt(solution[2])

        # get the angles
        gamma_star = get_angle_from_dot(solution[3], a_star, b_star)
        beta_star = get_angle_from_dot(solution[4], a_star, c_star)
        alpha_star = get_angle_from_dot(solution[5], b_star, c_star)

        # create the reciprocal lattice
        recip = LatticeBuilder.construct_from_scalars(a_star, b_star, c_star, alpha_star, beta_star, gamma_star)

        # reciprocal of that is the real space lattice
        return recip.reciprocal()

    @staticmethod
    def construct_cubic(a: float) -> Lattice:  # pylint: disable=invalid-name
        return LatticeBuilder.construct_from_scalars(a, a, a, 90, 90, 90)

    @staticmethod
    def construct_hexagonal(a: float, c: float) -> Lattice:  # pylint: disable=invalid-name
        return LatticeBuilder.construct_from_scalars(a, a, c, 90, 90, 120)

    @staticmethod
    def construct_from_vectors(a_vec, b_vec, c_vec) -> Lattice:
        return Lattice(a_vec, b_vec, c_vec)
