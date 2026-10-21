<p align="center"><img src="brand/cover.png" alt="Duyan 渡言" width="100%"></p>

# Duyan 渡言

[简体中文](README.md) · **English**

**One character, one word.** A serif typeface for Chinese and Latin, drawn from scratch and still in the making.

The Latin is a calm, bookish serif. The Chinese is written with the same pen: heavy verticals and light horizontals, round teardrop dots, and a soft beak at the end of each horizontal stroke. The Chinese side is still growing, one character at a time. The name 渡言 means "words that ferry across": the font carries text between Chinese and English. Every glyph is drawn from scratch; no outlines from existing fonts are used.

[Design and construction](docs/DESIGN.md) · [Drawing rules](docs/RULES.md) · [Chinese structure rules](docs/STRUCTURE.md) (all in Chinese)

## Progress

This is the 0.11 preview. It is not ready for body text yet: characters it does not cover fall back to other fonts on your system.

- Latin: upper and lowercase letters, figures and common punctuation, with 226 kerning pairs. Symbols such as &, @ and # and accented letters are not drawn yet.
- Chinese: 351 common characters (Simplified), plus the kana の and the Chinese comma and full stop.
- One weight only: Regular.

Next, the Chinese grows component by component. Rough milestones:

| Stage | Characters | Share of everyday text |
| --- | --- | --- |
| Now | 351 | |
| Next | 500 | about 80% |
| | 1000 | about 90% |
| | 2500 (common characters) | 98% |
| | 3500 | 99.5% |
| Complete | 6763 (GB 2312) | |

After that come Traditional Chinese and Japanese forms where they differ, and more weights.

## Try it

- Font file: [`sample/Duyan-Sample.otf`](sample/Duyan-Sample.otf) (OpenType CFF). Once installed it appears as Duyan Sample (渡言 小样 on Chinese systems).
- Specimen page: start a local server in the repository folder, then open http://localhost:8766/sample/

```bash
python3 -m http.server 8766
```

## Logo and cover

[`brand/`](brand/) holds the wordmark (`logo.svg`, and `logo-dark.svg` for dark backgrounds), the single-character icon (`mark.svg`, `icon.svg`) and the cover (`cover.png`). The wordmark "Duyan 渡言" uses two colours: ink for the Latin, deep teal for the Chinese; the icon is a teal 渡. All of them are built from the font's own outlines by `python3 tools/brand.py`.

## Build it yourself

You need Python 3.9 or later.

```bash
pip3 install -r requirements.txt
```

```bash
python3 build.py
```

`build.py` first checks every glyph against the design intent (ends that should be tucked into another stroke, self-intersecting outlines, gaps that are too narrow, Chinese structure and spacing), then writes `sample/Duyan-Sample.otf`. On macOS it also checks how the system renderer draws the font. The rules are described in [docs/DESIGN.md](docs/DESIGN.md) and [docs/STRUCTURE.md](docs/STRUCTURE.md).

## Feedback

It is early days. If a character looks off, please open an issue, ideally with a screenshot and the font size.

## License

Duyan is licensed under the [SIL Open Font License 1.1](OFL.txt): you may use it for free (commercial use included), embed it in websites and documents, modify it and redistribute it. Modified versions must stay under the OFL, and the font files may not be sold on their own. The drawing code and build scripts are part of the font's source and are licensed under the OFL as well.
