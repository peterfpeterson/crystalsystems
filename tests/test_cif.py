import numpy as np
import pytest
from crystalsystems.cif import _read_crystal_info, _read_data, _split

DATA = """
# Space group P-1
# a    6.608677
# b    6.847855
# c    7.525497
# al   106.10666
# be   106.50219
# ga   111.62796


h   k   l   m    d_spacing

0   0   1   2    6.51876
0   1   0   2    5.75105
0   1  -1   2    5.68918
1   0  -1   2    5.57554
1  -1   0   2    5.56100
1   0   0   2    5.53898
1  -1  -1   2    4.27249
1  -1   1   2    4.19014
1   1  -1   2    3.77900
0   1   1   2    3.61223
0   1  -2   2    3.56638
""".split(
    "\n"
)


def test_split():
    results = _split(DATA)
    assert len(results) == 2
    # get local friendly names
    header, body = results
    assert len(header) == 7
    assert len(body) == 11


def test_split_no_header():
    # this skips over the header b/c it isn't clear it will always be there
    results = _split(DATA[8:])
    assert len(results) == 2

    # get local friendly names
    header, body = results
    assert len(header) == 0
    assert len(body) == 11


def test_read_empty_crystal():
    result = _read_crystal_info("")
    assert result is None


def test_read_partial_crystal():
    result = _read_crystal_info(DATA[:4])
    assert result is None


def test_read_crystal():
    result = _read_crystal_info(DATA[:8])
    assert result is not None

    # compare to values in the DATA section above
    a_length, b_length, c_length, alpha, beta, gamma = result.scalar_lattice_constants()
    np.testing.assert_allclose(a_length, 6.608677)
    np.testing.assert_allclose(b_length, 6.847855)
    np.testing.assert_allclose(c_length, 7.525497)
    np.testing.assert_allclose(alpha, 106.10666)
    np.testing.assert_allclose(beta, 106.50219)
    np.testing.assert_allclose(gamma, 111.62796)


def test_read_empty_data():
    with pytest.raises(RuntimeError):
        _read_data([])


def test_read_bad_data():
    result = _read_data(DATA[8:])
    assert len(result) == 2

    hkl, dSpacing = result
    assert hkl.shape[0] == dSpacing.shape[0]
    assert hkl.shape[1] == 3


if __name__ == "__main__":
    pytest.main([__file__])
