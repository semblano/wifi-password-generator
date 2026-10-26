#!/usr/bin/env python3
"""Generate an easy-to-type Wi-Fi passphrase from randomly selected words.

Keep the selected word list beside this script. Generation works offline.
English: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
Brazilian Portuguese: https://github.com/thoughtworks/dadoware
Portuguese accents are removed and duplicate spellings merged before sampling.
"""

import argparse
from pathlib import Path
import secrets
import unicodedata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    length_options = parser.add_mutually_exclusive_group()
    length_options.add_argument(
        "-w", "--words", type=int, choices=(5, 6), default=6,
        help="number of random words (default: 6; recommended)",
    )
    length_options.add_argument(
        "-a", "--acronym",
        help="choose one word per initial, e.g. -a senha (case-insensitive)",
    )
    parser.add_argument(
        "--language", choices=("en", "pt-br"), default="en",
        help="word language (default: en)",
    )
    parser.add_argument(
        "-min", "--min-length", type=int,
        help="minimum word length in acronym mode (default: 1)",
    )
    parser.add_argument(
        "-max", "--max-length", type=int,
        help="maximum word length in acronym mode (default: 9)",
    )
    args = parser.parse_args()
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
            candidates.append("".join(
                char for char in unicodedata.normalize("NFD", fields[0])
                if not unicodedata.combining(char)
            ))

    # Deduplicate before sampling so accent removal does not bias selection.
    # Exclude punctuation and limit word length so six words plus hyphens
    # fit within the Wi-Fi passphrase limit of 63 characters.
    words = sorted({
        word for word in candidates
        if word.isascii()
        and word.isalpha()
        and word.islower()
        and 1 <= len(word) <= 9
    })
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
                word for word in words
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
