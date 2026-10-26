#!/usr/bin/env python3
"""Generate a random Wi-Fi password, or use --dictionary for a word passphrase.

For dictionary mode, keep the selected word list beside this script.
Generation works offline in both modes.
English: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
Brazilian Portuguese: https://github.com/thoughtworks/dadoware
Portuguese accents are removed and duplicate spellings merged before sampling.
"""

import argparse
import secrets
import string
import unicodedata
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode_options = parser.add_mutually_exclusive_group()
    mode_options.add_argument(
        "-d",
        "--dictionary",
        action="store_true",
        help="generate a word-based passphrase instead of random characters",
    )
    mode_options.add_argument(
        "-l",
        "--length",
        type=int,
        help="random password length, from 16 to 63 characters (default: 24)",
    )
    length_options = parser.add_mutually_exclusive_group()
    length_options.add_argument(
        "-w",
        "--words",
        type=int,
        choices=(5, 6),
        help="number of dictionary words (requires -d; default: 6)",
    )
    length_options.add_argument(
        "-a",
        "--acronym",
        help="choose one word per initial, e.g. -d -a senha (case-insensitive)",
    )
    parser.add_argument(
        "--language",
        choices=("en", "pt-br"),
        help="dictionary language (requires -d; default: en)",
    )
    parser.add_argument(
        "-min",
        "--min-length",
        type=int,
        help="minimum word length in acronym mode (default: 1)",
    )
    parser.add_argument(
        "-max",
        "--max-length",
        type=int,
        help="maximum word length in acronym mode (default: 9)",
    )
    args = parser.parse_args()
    if not args.dictionary:
        if any(
            value is not None
            for value in (
                args.words,
                args.acronym,
                args.language,
                args.min_length,
                args.max_length,
            )
        ):
            parser.error("word options require -d / --dictionary")
        length = args.length if args.length is not None else 24
        if not 16 <= length <= 63:
            parser.error("length must be between 16 and 63")
        alphabet = string.ascii_letters + string.digits
        print("".join(secrets.choice(alphabet) for _ in range(length)))
        return

    args.words = args.words if args.words is not None else 6
    args.language = args.language if args.language is not None else "en"
    if args.min_length is not None or args.max_length is not None:
        if args.acronym is None:
            parser.error("-min and -max require -a / --acronym")
    requested_min = args.min_length if args.min_length is not None else 1
    requested_max = args.max_length if args.max_length is not None else 9
    if requested_min < 1 or requested_max < 1:
        parser.error("minimum and maximum word lengths must be positive")
    if requested_min > requested_max:
        parser.error("minimum word length cannot exceed maximum word length")
    if args.acronym is not None:
        if not (
            args.acronym.isascii()
            and args.acronym.isalpha()
            and 1 <= len(args.acronym) <= 32
        ):
            parser.error("acronym must contain 1 to 32 letters (a-z only)")
        args.acronym = args.acronym.lower()
    filenames = {"en": "wifi_words_eff.txt", "pt-br": "wifi_words_pt_br.txt"}
    word_file = Path(__file__).resolve().with_name(filenames[args.language])
    try:
        lines = word_file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        parser.error(f"cannot read {word_file}: {exc}")

    candidates = []
    for line in lines:
        fields = line.split()
        if args.language == "en" and len(fields) == 2:
            candidates.append(fields[1])
        elif args.language == "pt-br" and len(fields) == 1:
            candidates.append(
                "".join(
                    char
                    for char in unicodedata.normalize("NFD", fields[0])
                    if not unicodedata.combining(char)
                )
            )

    # Deduplicate before sampling so accent removal does not bias selection.
    # Exclude punctuation and limit word length so six words plus hyphens
    # fit within the Wi-Fi passphrase limit of 63 characters.
    words = sorted(
        {
            word
            for word in candidates
            if word.isascii()
            and word.isalpha()
            and word.islower()
            and 1 <= len(word) <= 9
        }
    )
    if len(words) < 7000:
        parser.error(f"word list is incomplete; restore {word_file.name}")

    if args.acronym is not None:
        count = len(args.acronym)
        # Budget for the hyphens and guarantee an 8–63 character password
        # for every combination, including short or long acronyms.
        min_length = max(requested_min, (8 - (count - 1) + count - 1) // count)
        max_length = min(requested_max, 9, (63 - (count - 1)) // count)
        if min_length > max_length:
            parser.error(
                "word length constraints cannot fit an 8–63 character Wi-Fi "
                "password with this acronym and dictionary (words up to 9 characters)"
            )
        pools = {}
        for initial in dict.fromkeys(args.acronym):
            pools[initial] = [
                word
                for word in words
                if word.startswith(initial) and min_length <= len(word) <= max_length
            ]
            if not pools[initial]:
                parser.error(
                    f"no words starting with '{initial}' in {args.language} "
                    f"with {min_length}–{max_length} characters; "
                    "try different lengths, an acronym, or a language"
                )
        selected = [secrets.choice(pools[initial]) for initial in args.acronym]
    else:
        selected = [secrets.choice(words) for _ in range(args.words)]
    print("-".join(selected))


if __name__ == "__main__":
    main()
