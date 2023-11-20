import multiprocessing as mp
import pathlib
import subprocess

from .convert import flac2mp3


def clone_file(
    in_file: pathlib.Path, out_file: pathlib.Path
) -> subprocess.CompletedProcess[str]:
    out_file.parent.mkdir(exist_ok=True, parents=True)
    return flac2mp3(in_file, out_file)


def clone_dir(
    root_dir: pathlib.Path, target_dir: pathlib.Path
) -> list[subprocess.CompletedProcess[str]]:
    jobs = (
        (in_file, out_file)
        for in_file in root_dir.glob("**/*.flac")
        if (
            out_file := (target_dir / in_file.relative_to(root_dir)).with_suffix(".mp3")
        )
    )

    with mp.Pool() as p:
        results = p.starmap(clone_file, jobs)

    errors = [res for res in results if res.returncode != 0]

    return errors
