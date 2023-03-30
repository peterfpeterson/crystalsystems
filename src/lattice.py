import numpy as np


def to_vector(a, b, c, alpha, beta, gamma):
    cos_alpha = np.cos(np.deg2rad(alpha))
    cos_beta = np.cos(np.deg2rad(beta))
    cos_gamma = np.cos(np.deg2rad(gamma))
    v_term = np.sqrt(
        1 - cos_alpha * cos_alpha - cos_beta * cos_beta - cos_gamma * cos_gamma + 2 * cos_alpha * cos_beta * cos_gamma
    )

    a_vec = np.asarray([a, 0, 0])
    b_vec = np.asarray([b * cos_gamma, b * np.sin(np.deg2rad(gamma)), 0])
    c_vec = np.asarray(
        [
            c * cos_beta,
            c * (cos_alpha - cos_gamma * cos_beta) / np.sin(np.deg2rad(gamma)),
            c * v_term / np.sin(np.deg2rad(gamma)),
        ]
    )

    return a_vec, b_vec, c_vec


def calc_reciprocal(a, b, c, alpha, beta, gamma):
    """currently the angles are in degrees"""
    # need to sort this out
    return (a, b, c, alpha, beta, gamma)
