import logging


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
    parser.add_argument(
        "-l",
        "--log",
        nargs="?",
        default="info",
        choices=["debug", "info", "warn", "error"],
        help="The log level (default: %(default)s)",
    )
    # configure
    args = parser.parse_args(args)

    # configure logging
    logging.basicConfig()  # setup default handlers and formatting
    # override log level
    for handler in logging.getLogger().handlers:
        handler.setLevel(args.log.upper())
    logging.getLogger("crystalsystems")

    # TODO do stuff


if __name__ == "__main__":
    import sys

    sys.exit(main())
