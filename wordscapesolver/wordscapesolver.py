"""Utils"""
import glob
import itertools
from pathlib import Path

fpath = Path(__file__)
DICT = fpath.parent / '..' / 'etc' / "british-english.txt"

def get_pngs(xinput: str) -> None:
    """Generate list of PNGs to process

    Args:
        xinput (str): path to read input from as a string

    Returns:
        list: full path list of PNGs
    """
    xinput = Path(xinput)
    xquery = str(xinput) + r'\*.png'
    for im in glob.glob(xquery):
        yield Path(im)
    
def get_dict(fpath: Path) -> set:
    """Read a file of words

    Args:
        fpath (Path): file path of word list

    Returns:
        set: cleaned list of plausible words
    """
    if len(fpath) < 1:
        fpath = DICT

    words = set()
    with open(fpath, 'r') as fh:
        for w in fh.readlines():
            w = w.strip()
            if len(w) < 3 or "'" in w:
                continue
            if w[0].isupper():
                continue
            words.add(w.upper()) 

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
    l = sorted(list(letters))
    for wlen in range(2, len(letters) + 1):
        for wstring in itertools.permutations(l, wlen):
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
    for k, v in words.items():
        msg += f"{k} letter words\n"
        txt = ""
        for x in sorted(v):
            txt += f"\t{x}\n"
        msg += txt
        msg += "\n"
    
    return(msg)