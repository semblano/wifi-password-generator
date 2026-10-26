# Third-party notices

The MIT license for this project's original code and documentation does not
relicense the bundled word lists or their accompanying notices.

## English: EFF's Long Wordlist

- **Local file:** [`wifi_words_eff.txt`](wifi_words_eff.txt).
- **Creator:** Joseph Bonneau, Electronic Frontier Foundation (EFF).
- **Project:** [EFF Dice-Generated Passphrases](https://www.eff.org/dice).
- **Source:** <https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt>.
- **License:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/),
  under [EFF's copyright policy](https://www.eff.org/copyright).
- **Included license text:** [`wifi_words_eff_LICENSE.txt`](wifi_words_eff_LICENSE.txt),
  obtained from the [SPDX license list](https://github.com/spdx/license-list-data/blob/main/text/CC-BY-4.0.txt).

The bundled list is an unmodified copy of the source file. At runtime, the
generator reads the word column, removes duplicates, and keeps only lowercase
ASCII alphabetic words of 1–9 characters. This excludes four entries containing
hyphens, leaving 7,772 eligible words before acronym filtering.

## Brazilian Portuguese: Dadoware

- **Local file:** [`wifi_words_pt_br.txt`](wifi_words_pt_br.txt).
- **Project:** [Dadoware — Diceware em português do Brasil](https://github.com/thoughtworks/dadoware).
- **Authors:** Luciano Ramalho and the Dadoware contributors. The complete upstream
  credits are included in [`wifi_words_pt_br_CREDITS.txt`](wifi_words_pt_br_CREDITS.txt).
- **Source:** [`7776palavras-2e.txt`](https://github.com/thoughtworks/dadoware/blob/6b2375b49437f03f971a7c793e96090d657c2be5/7776palavras-2e.txt).
- **Upstream revision:** `6b2375b49437f03f971a7c793e96090d657c2be5`.
- **License:** [Creative Commons Attribution-NonCommercial 3.0 Unported](https://creativecommons.org/licenses/by-nc/3.0/).
- **Included license text:** [`wifi_words_pt_br_LICENSE.md`](wifi_words_pt_br_LICENSE.md),
  copied from upstream `LICENSE.md`.

The bundled word list, license, and credits are unmodified copies of the upstream
files (renamed locally). At runtime, the generator removes diacritics using Unicode
NFD normalization, merges duplicate spellings, and keeps only lowercase ASCII
alphabetic words of 1–9 characters. There are 7,762 eligible words before acronym
filtering. These runtime transformations do not change the distributed file.

**The Dadoware license includes a noncommercial restriction.** Its permissions
and conditions continue to apply to the bundled Dadoware material independently
of the MIT-licensed generator.

## Additional attribution

Dadoware credits Arnold G. Reinhold's [Diceware method](https://theworld.com/~reinhold/diceware.html).
This project uses Python's cryptographically secure random selection rather than
physical dice. No endorsement by EFF, Dadoware, or their contributors is implied.
