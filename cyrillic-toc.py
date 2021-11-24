import re
import sys
from re import Match
from typing import Callable

error_msg = """
Usage: {} toc-filename
to make links with cyrillic symbols for github markdown table of contents.

Example:
[Выхухоль обыкновенная](#---) |-> [Выхухоль обыкновенная](#выхухоль-обыкновенная)
"""


def main():
    if len(sys.argv) != 2:
        raise RuntimeError(error_msg.format(sys.argv[0]))
    filename = sys.argv[1]
    read_content(filename, handle)


def handle(toc: str):
    """
    :param toc: table of contents with cyrillic symbols in headers
    :return:
    """
    result_toc = re.sub("\[(.*)\]\((#.*)\)", replacer, toc)
    save_content(result_toc, new_filename())


def replacer(match: Match):
    return f"[{match.group(1)}](#{linkify(match.group(1))})"


def linkify(candidate: str) -> str:
    r_map = {"<": "", ">": "", " ": "-", "\\": "", "/": "", "(": "", ")": ""}
    for from_, to_ in r_map.items():
        candidate = candidate.replace(from_, to_)
    return candidate.lower()


def read_content(filename: str, callback: Callable):
    with open(filename, "r", encoding="utf-8") as fin:
        callback(fin.read())


def save_content(content: str, filename: str):
    with open(filename, "w", encoding="utf-8") as fout:
        fout.write(content)


def new_filename() -> str:
    return "toc.txt"


if __name__ == "__main__":
    main()
