import pytest
from crystalsystems import __version__
from crystalsystems.__main__ import main


def test_version_import():
    assert __version__


def test_version():
    assert main(["--version"]) == 0


def test_help():
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.value.code == 0


def test_noargs():
    with pytest.raises(SystemExit) as e:
        main([])
    assert e.value.code == 2


if __name__ == "__main__":
    pytest.main([__file__])
