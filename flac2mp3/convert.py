import logging
import pathlib
import shutil
import subprocess


logger = logging.getLogger(__name__)


def flac2mp3(
    in_file: pathlib.Path, out_file: pathlib.Path
) -> subprocess.CompletedProcess[str]:
    """
    ffmpeg -n -hide_banner -loglevel error -i "$in_file" -qscale:a 0 "$out_file"
    """

    if not shutil.which("ffmpeg"):
        logger.fatal("ffmpeg was not found in $PATH")
        exit(1)

    logger.info(f'"{out_file}": start converting...')

    res = subprocess.run(
        [
            "ffmpeg",
            "-n",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            in_file.resolve(),
            "-qscale:a",
            "0",
            out_file.resolve(),
        ],
        capture_output=True,
        text=True,
    )

    if res.returncode == 0:
        logger.info(f'"{out_file}": done!')
    else:
        logger.error(f"ffmpeg failed with code {res.returncode}: {res.stderr}")

    return res
