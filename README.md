# Wi-Fi Password Generator

Generate random, easy-to-type Wi-Fi passphrases in English or Brazilian
Portuguese. Designed for entering passwords on TVs, consoles, and other devices
where switching between keyboard layouts is inconvenient.

The output contains **lowercase letters and hyphens**. Portuguese accents are
removed, and every generated password fits within **8–63 ASCII characters**.

## Features

- Cryptographically secure selection with Python's `secrets` module.
- Six random words by default, with an optional five-word mode.
- English and Brazilian Portuguese word lists included.
- Acronym mode: choose initials and generate one random word for each letter.
- Optional minimum and maximum word lengths in acronym mode.
- Offline generation with no dependencies outside Python's standard library.
- One password printed to standard output; the script does not save passwords.

## Quick start

Install Python 3 (tested with Python 3.12), then clone this repository:

```bash
git clone https://github.com/semblano/wifi-password-generator.git
cd wifi-password-generator
python3 wifi_password.py
```

No `pip install` or virtual environment is required. Alternatively, download and
extract the repository using GitHub's **Code → Download ZIP** menu.

On Windows, use `py -3` instead of `python3`:

```powershell
py -3 wifi_password.py
```

Keep `wifi_words_eff.txt` and `wifi_words_pt_br.txt` beside `wifi_password.py`.
Only the selected language's word list is needed at runtime. Word lists are
resolved relative to the script, so it can also be invoked from another folder.

## Usage

### Random words

Generate six English words:

```bash
python3 wifi_password.py
```

Generate six Brazilian Portuguese words:

```bash
python3 wifi_password.py --language pt-br
```

Generate five words instead:

```bash
python3 wifi_password.py --language pt-br --words 5
```

Each run selects new random words. Words are selected independently, so repeated
words are possible.

### Acronym mode

Provide the desired initials with `-a` or `--acronym`:

```bash
python3 wifi_password.py --language pt-br -a senha
```

This produces five words whose first letters are **s-e-n-h-a**, in that order,
joined with hyphens. The acronym determines the word count; it cannot be combined
with `-w` / `--words`.

Acronyms are case-insensitive: `SENHA` and `senha` impose the same constraints.
Output is always lowercase. Acronyms must contain only ASCII letters (`a-z`);
spaces, digits, accented letters, and punctuation are not accepted.

### Control word lengths

Require at least four characters per word:

```bash
python3 wifi_password.py --language pt-br -a senha -min 4
```

Require between four and six characters per word, inclusive:

```bash
python3 wifi_password.py --language pt-br -a senha -min 4 -max 6
```

Require exactly four characters per word:

```bash
python3 wifi_password.py --language pt-br -a senha -min 4 -max 4
```

The equivalent long-form options are:

```bash
python3 wifi_password.py --language pt-br --acronym senha --min-length 4 --max-length 6
```

Both length flags apply **only to acronym mode**. Without them, the requested
range is 1–9 characters per word. The generator may narrow this range further
to satisfy Wi-Fi password length limits.

### Command-line reference

| Option | Description | Default |
| --- | --- | --- |
| `-h`, `--help` | Show usage and exit. | — |
| `--language {en,pt-br}` | Select English or Brazilian Portuguese. | `en` |
| `-w`, `--words {5,6}` | Number of words in unrestricted random mode. | `6` |
| `-a`, `--acronym TEXT` | One word per supplied initial; mutually exclusive with `--words`. | Disabled |
| `-min`, `--min-length N` | Minimum word length in acronym mode; positive integer. | `1` |
| `-max`, `--max-length N` | Maximum word length in acronym mode; positive integer. | `9` |

```bash
python3 wifi_password.py --help
```

Successful generation prints one newline-terminated password and exits with code
`0`. Invalid arguments, unavailable words, and unreadable or incomplete word lists
produce an error on standard error and exit with code `2`.

## Wi-Fi length limits

The generator includes the separating hyphens in its 8–63 character budget.
Dictionary words longer than nine characters are excluded.

In acronym mode, each word receives an equal length budget. For an acronym of
`n` letters, the maximum allowed word length is the smallest of:

- The requested `-max` value (default `9`).
- Nine characters, the dictionary limit.
- `floor((63 - (n - 1)) / n)`, reserving space for the hyphens.

The minimum length also increases when needed to reach eight characters overall.
Consequently, a one-letter acronym requires a word at least eight characters long.

Acronyms may contain 1–32 letters, but a valid password requires matching words
for **every** initial within the resulting length range. For example, `-min 4`
allows at most 12 words: 12 four-letter words plus 11 hyphens total 59 characters.
The equal per-word budget is conservative; the script does not search for mixed
word-length combinations that might otherwise fit.

## How selection works

1. Read the selected local word list.
2. For Portuguese, remove accents using Unicode normalization (`ç` becomes `c`,
   for example).
3. Keep lowercase ASCII alphabetic words of 1–9 characters and remove duplicates.
4. In acronym mode, filter the eligible words by each initial and length range.
5. Select independently and uniformly from each eligible pool using
   `secrets.choice`, then join the words with hyphens.

The included files produce **7,772 eligible English words** and **7,762 eligible
Brazilian Portuguese words**. They are stored in their original upstream formats;
normalization and filtering happen in memory when the script runs.

### Randomness and constraints

Six unrestricted words from either list provide approximately 77.5 bits of
selection entropy; five provide approximately 64.6 bits. These figures describe
the selection space, not a guaranteed cracking time.

An acronym or narrow length range reduces the candidate pool. Its strength
depends on the available words for each position, so the unrestricted figures
do not apply to acronym mode. Treat the acronym as known rather than an
additional secret. Unrestricted six-word generation is the recommended default.

Store generated passwords in a password manager and generate separate passwords
for separate networks. Generation itself makes no network requests; the result
is visible in your terminal and its scrollback.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `python3` is not found | Install Python 3 or use `py -3` on Windows. |
| `cannot read ...` | Restore the selected word-list file beside the script. |
| `word list is incomplete` | Restore the bundled word list. The script requires at least 7,000 eligible words before applying acronym filters. |
| `-min and -max require -a / --acronym` | Supply an acronym, or omit the length flags. |
| `minimum word length cannot exceed maximum word length` | Set a minimum no larger than the maximum; the default maximum is nine. |
| `no words starting with ...` | Widen the length range, choose different initials, or change language. |
| `word length constraints cannot fit ...` | Shorten the acronym or adjust the word-length range. |

## Repository contents

```text
wifi_password.py                 Command-line generator
wifi_words_eff.txt               Original English EFF word list
wifi_words_eff_LICENSE.txt       CC BY 4.0 license text
wifi_words_pt_br.txt             Original Brazilian Portuguese Dadoware word list
wifi_words_pt_br_LICENSE.md      Upstream CC BY-NC 3.0 license text
wifi_words_pt_br_CREDITS.txt     Upstream Dadoware credits
THIRD_PARTY_NOTICES.md           Word-list sources, attribution, and processing
LICENSE                         MIT license for original code and documentation
```

## Contributing

Issues and pull requests are welcome. Keep the generator dependency-free and
preserve the existing command-line options. When changing selection logic, check
both languages, acronym initials, minimum/maximum word lengths, Wi-Fi length
boundaries, and rejection of impossible constraints. Keep generated passwords
out of commits and issue reports.

## License and acknowledgments

The original Python code and project documentation are licensed under the
[MIT License](LICENSE), copyright 2026 Marcus Semblano.

The bundled word lists retain their own licenses:

- **English:** EFF's Long Wordlist by Joseph Bonneau / Electronic Frontier
  Foundation, **CC BY 4.0**, under [EFF's copyright policy](https://www.eff.org/copyright).
- **Brazilian Portuguese:** Dadoware by Luciano Ramalho and contributors,
  **CC BY-NC 3.0**. This license includes a **noncommercial restriction**; the MIT
  license for the code does not override it.

See [third-party notices](THIRD_PARTY_NOTICES.md) for sources, attribution,
processing details, and links to the included license texts.
