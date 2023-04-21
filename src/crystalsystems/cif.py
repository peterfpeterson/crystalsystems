import logging
import re

import numpy as np

from crystalsystems.lattice import LatticeBuilder

logger = logging.getLogger("crystalsystems.cif")


def _split(handle):
    header = []
    body = []
    inHeader = True
    matcher = re.compile(r"^h.+k.+l.+")
    for line in handle:
        line = line.strip()
        if not line:
            continue
        if inHeader:
            if matcher.match(line):
                inHeader = False
            else:
                header.append(line)
        else:
            if line.startswith("#"):
                pass
            else:
                body.append(line)
    return header, body


def _read_crystal_info(header):
    a_length = 0.0
    b_length = 0.0
    c_length = 0.0
    alpha = 0.0
    beta = 0.0
    gamma = 0.0
    comment = ""
    for line in header:
        # pull off the comment marker
        if line.startswith("#"):
            line = line[1:].strip()

        # parse the lattice constants
        if line.startswith("al "):
            alpha = float(line.replace("al", "").strip())
        elif line.startswith("be "):
            beta = float(line.replace("be", "").strip())
        elif line.startswith("ga "):
            gamma = float(line.replace("ga", "").strip())
        elif line.startswith("a "):
            a_length = float(line.replace("a", "").strip())
        elif line.startswith("b "):
            b_length = float(line.replace("b", "").strip())
        elif line.startswith("c "):
            c_length = float(line.replace("c", "").strip())
        elif line.startswith("Space group"):
            comment = line.replace("Space group", "")
        else:
            logger.debug("Ignoring:", line)

    if comment:
        logger.info(f"Found space group {comment}")
    # return the right thing
    if a_length and b_length and c_length and alpha and beta and gamma:
        return LatticeBuilder.construct_from_scalars(a_length, b_length, c_length, alpha, beta, gamma)
    else:
        return None


def _read_data(body):
    h_vals = []
    k_vals = []
    l_vals = []
    d_vals = []

    for line in body:
        if not line:  # skip empty lines
            continue

        try:
            h_val, k_val, l_val, _, d_val = line.split()
            h_vals.append(int(h_val))
            k_vals.append(int(k_val))
            l_vals.append(int(l_val))
            d_vals.append(float(d_val))
        except ValueError as e:
            # log issues and carry on
            logger.debug(f'While parsing "{line}" encountered: {e}')

    if len(d_vals) == 0:
        raise RuntimeError("Failed to read any data")

    d_vals = np.asarray(d_vals)
    hkl = np.array([h_vals, k_vals, l_vals])
    return np.transpose(hkl), d_vals


def loadCIF(handle):
    header, body = _split(handle)
    lattice = _read_crystal_info(header)
    hkl, d_vals = _read_data(body)

    return lattice, hkl, d_vals
