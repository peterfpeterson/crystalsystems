import logging

from crystalsystems import __version__
from crystalsystems.cif import loadCIF
from crystalsystems.lstsq import getLattice


def main(args=None):
    """Underlying entrypoint for the backend.

    The function args are exposed this way to allow for testing.
    Passing in None causes argparse to use ``sys.argv``.
    """
    # set up the command line parser
    import argparse

    parser = argparse.ArgumentParser(
        prog="crystalsystems",
        description="TODO",
        epilog="https://github.com/peterfpeterson/crystalsystems/",
    )
    parser.add_argument("--version", action="store_true", help="Print version information and exit")
    parser.add_argument(
        "-l",
        "--log",
        nargs="?",
        default="info",
        choices=["debug", "info", "warn", "error"],
        help="The log level (default: %(default)s)",
    )
    parser.add_argument("filename", nargs="?", type=argparse.FileType("r"), help="Name of CIF file to read in")
    # configure
    args = parser.parse_args(args)

    if args.version:
        print(__version__)
        return 0

    # configure logging - setup default handlers and formatting
    logging.basicConfig(level=args.log.upper())
    logger = logging.getLogger("crystalsystems")

    if args.filename:
        lattice_exp, hkl, dSpacing = loadCIF(args.filename)
        if lattice_exp:
            logger.info(f"CIF file contained {lattice_exp}")

        # find the lattice and output the result
        lattice_obs = getLattice(hkl, dSpacing)
        logger.info("Found lattice:")
        logger.info(lattice_obs)
    else:
        # error out if file wasn't provided
        parser.error("Failed to specify any work to do")


if __name__ == "__main__":
    import sys

    sys.exit(main())
