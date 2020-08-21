# This file is part of lp-fork. See LICENSE file for license info.
"""Launchpad Fork main module."""

import argparse
import logging
import sys

from .fork import Fork


def parse_args():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser("lp-fork")
    parser.add_argument("repo_url", help="URL to repo to fork")
    parser.add_argument("--debug", action="store_true", help="additional debug output")

    return parser.parse_args()


def setup_logging(debug):
    """Set up basic logging."""
    logging.basicConfig(
        stream=sys.stdout,
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
    )


def launch():
    """Parse args, set up logging, and launch lp-fork."""
    cli = vars(parse_args())
    setup_logging(cli.pop("debug"))

    fork = Fork(cli["repo_url"])
    fork.create_fork()


if __name__ == "__main__":
    sys.exit(launch())
