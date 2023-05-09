# crystalsystems
Calculate the lattice constants from a set of observations

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/peterfpeterson/crystalsystems/main.svg)](https://results.pre-commit.ci/latest/github/peterfpeterson/crystalsystems/main)
[![codecov](https://codecov.io/gh/peterfpeterson/crystalsystems/branch/main/graph/badge.svg?token=KCW0SIZ5Y8)](https://codecov.io/gh/peterfpeterson/crystalsystems)

Developers
----------

```
conda env create -f environment.yml
conda activate crystalsystems
pre-commit install
pip install -e . # editable install
```

Notes
-----

From an [article about indexing from IUCr](https://onlinelibrary.wiley.com/iucr/itc/Ha/ch3o4v0001/#fd3o4o2)

* Cubic $Q=(h^2+k^2+l^2)A_{11}$
* Tetragonal $Q=(h^2+k^2) A_{11}+l^2 A_{33}$
* Hexagonal $Q=(h^2+hk+k^2) A_{11}+l^2 A_{33}$
* Orthorhombic $Q=h^2 A_{11}+k^2 A_{22}+l^2 A_{33}$
* Monoclinic $Q=h^2 A_{11}+k^2 A_{22}+l^2 A_{33} + hl A_{13}$
* Triclinic $Q=h^2 A_{11}+k^2 A_{22}+l^2 A_{33} + hk A_{12} + hl A_{13} + kl A_{23}$
