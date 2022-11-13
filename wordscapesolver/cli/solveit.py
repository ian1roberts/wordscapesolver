import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import click

from wordscapesolver import imageparse as ip
from wordscapesolver import wordscapesolver as ws


@click.command()
@click.argument("xinput", type=str, default=os.getcwd())
@click.argument("xoutput", type=str, default="-")
@click.option("--task", type=click.Choice(["run", "debug"], case_sensitive=False),
    help="run normally or in debug mode. Debug displays letter detection images, click close to continue.",
    default="run")
@click.option(
    "--force/--no-force", default=False,
    help="Force overwrite of output text.")
@click.option("--logfile/--no-logfile", help="Save a session log.", default=False)
@click.option("--move/--no-move", help="Move processed images to an output directory.", default=False)
def _solveit(xinput: str, xoutput: str, task: str, force: bool, logfile: bool, move: bool) -> None:
    """Given an input directory, iterate over PNG screenshots and process WordScape puzzles.
       Words are sent to standard out (-) or `output` file
       
       python -m wordscapesolver.cli.solveit --move --force --task run [input directory] [output file]
    """
    if not logfile:
        logout = sys.stderr
    else:
        logfn = str(datetime.now()) + '_wordscapesolver.log'
        logfn = logfn.replace(" ", "-").replace(":", ".")
        logout = open(logfn, "a")
        
    logging.basicConfig(stream=logout, level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("wordscapesolver.cli.solveit --task %s %s %s", task, xoutput, xinput)
    logger.info("Reading input from %s and writing output to %s", xinput, xoutput)
    
    # set up output file if not stdout
    if xoutput != "-":
        if os.path.exists(xoutput) and not force:
            raise FileExistsError(f"Output file exists: {xoutput}\tMaybe try with --force\n")
        else:
            fout = open(xoutput, "a")
    else:
        fout = sys.stdout
        
    if move:
        if not os.path.exists("output"):
            os.mkdir("output")
    
    # Load dirctionary
    words = ws.get_dict("")
    
    # Process all the PNGs, letters & solutions
    for im in ws.get_pngs(xinput):
        logger.info(f"Working on ... {im.name}")
        letters = ip.procImage(im)
        logger.info(f"Processed {im.name} --> {letters}")
        if "*" in set(letters):
            logger.debug("!! Failed to decode letters !!")
        allwords = ws.solver(letters, words)

        tot = 0
        for k, v in allwords.items():
            logger.info(f"\t{k} letter words ...\t{len(v)}")
            tot += len(v)
        lwords = " ".join(v)
        logger.info(f"\tLongest words ... {lwords}")

        # tidyy up
        if move:
            newname = Path(im.parent) / ".." / "output" / im.name
            logger.info(f"Move {str(im.resolve())} --> {str(newname.resolve())}")
            im.rename(newname)
        
        msg = ws.print_words(allwords)
        fout.write(im.name + "\n")
        fout.write(letters + "\n")
        fout.write(msg)
        fout.write("=" * 80 + "\n\n")
        logger.info(f"Done {im.name}\t{tot} words found.\n")

    # 


if __name__ == "__main__":
    _solveit()
