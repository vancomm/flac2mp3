import logging
from pathlib import Path
from venv import logger

import click

from . import clone


@click.command
@click.option(
    "-c",
    "--clone-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=False,
    help="Convert all files in directory recursively, preserving its structure.",
)
@click.option(
    "-o",
    "--out-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
    help="Destination directory.",
)
def cli(*, clone_dir: Path | None, out_dir: Path):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

    out_dir = out_dir.expanduser().resolve()

    if clone_dir:
        clone_dir = clone_dir.expanduser().resolve()

        errors = clone.clone_dir(root_dir=clone_dir, target_dir=out_dir)

        logger.info(errors)
