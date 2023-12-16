from pathlib import Path

fpath: Path

def solveit(xinput: str, xoutput: str, task: str,
            force: bool, logfile: bool, move: bool,
            config: Path) -> None: ...
