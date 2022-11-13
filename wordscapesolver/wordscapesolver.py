"""Utils"""
import glob
import itertools
from pathlib import Path

fpath = Path(__file__)
DICT = fpath.parent / ".." / "etc" / "british-english.txt"


def get_pngs(xinput: str) -> None:
    """Generate list of PNGs to process

    Args:
        xinput (str): path to read input from as a string

    Returns:
        list: full path list of PNGs
    """
    xinput = Path(xinput)
    xquery = str(xinput) + r"\*.png"
    for cur_image in glob.glob(xquery):
        yield Path(cur_image)


def get_dict(fpath_dict: Path) -> set:
    """Read a file of words

    Args:
        fpath_dict (Path): file path of word list

    Returns:
        set: cleaned list of plausible words
    """
    if len(fpath_dict) < 1:
        fpath_dict = DICT

    words = set()
    with open(fpath_dict, "r") as fhandle:
        for words_in in fhandle.readlines():
            words_in = words_in.strip()
            if len(words_in) < 3 or "'" in words_in:
                continue
            if words_in[0].isupper():
                continue
            words.add(words_in.upper())

    return words


def solver(letters: str, words: set) -> dict:
    """Compute all possible words from letters in the dictionary.

    Args:
        letters (string): a word to serve as query
        words (set): known permissible words

    Returns:
        list of found words
    """
    found = dict()
    letters = sorted(list(letters))
    for wlen in range(2, len(letters) + 1):
        for wstring in itertools.permutations(letters, wlen):
            cand = "".join(wstring)
            if cand in words:
                if wlen in found:
                    found[wlen].add(cand)
                else:
                    found[wlen] = set()
                    found[wlen].add(cand)
    return found


def print_words(words: dict) -> str:
    """Format the words output

    Args:
        words (dict): dictionary of words. Key = length, value = words
    """
    msg = "\n"
    for key, values in words.items():
        msg += f"{key} letter words\n"
        txt = ""
        for msg_part in sorted(values):
            txt += f"\t{msg_part}\n"
        msg += txt
        msg += "\n"

    return msg
