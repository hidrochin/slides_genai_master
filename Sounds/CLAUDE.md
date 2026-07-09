# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

This directory (`Sounds`) is one module of a larger course-materials repository (`slides_genai_master`; git root is the parent `E:/GenAI_Master/slides`, with sibling modules such as `DDP`, `bio_AI`, `multi_model`, `code`, `chatbot`, `LLM_SW`). It holds the **speech technology** lecture set: numbered PDF decks by *TrangNTT* covering the full spoken-language pipeline — articulatory & acoustic phonetics, linguistics, digital signal processing, datasets, model evaluation, speech synthesis (TTS), and automatic speech recognition (ASR).

This is **not a software project**: there is no build system, test suite, linter, package manifest, or CI. The PDFs are read-only compiled artifacts (no source). The real work here is turning those decks into study materials.

## The task: PDF decks → Vietnamese study materials

The repeated workflow across modules (see the fleshed-out `DDP` and `bio_AI` for reference) is:

1. **Read the PDFs.** Extract text/outline; OCR the image-only slides. Group slides into thematic clusters.
2. **Write `on_tap/`** — condensed **revision notes** in Vietnamese: one Markdown file per cluster plus a `00-ONE-PAGER.md` cheat-sheet (must-remember formulas, "easy-to-confuse" comparison tables, cross-links between files).
3. **Write `trac_nghiem/`** — **multiple-choice quizzes** in Vietnamese: one file per cluster plus a combined mock exam. Answers/explanations go inside `<details><summary>Đáp án</summary>…</details>` blocks so the reader can self-test before revealing.

`Sounds` currently holds **only the source PDFs** — `on_tap/` and `trac_nghiem/` do not exist here yet. When creating them, mirror the conventions already established in `../DDP/on_tap/` and `../DDP/trac_nghiem/`.

### Output conventions (match the existing modules)
- **Language is Vietnamese.** All revision notes and quiz text are written in Vietnamese, even though the source slides are English.
- **Quiz options are deliberately uniform** — written roughly equal length, none bolded — so the answer can't be guessed from formatting; the reader must actually reason. Mark calculation-heavy / trap questions with `(Khó)`.
- Cross-link related files with relative Markdown links; keep the one-pager as the hub.

## Helper scripts

The PDF-processing helpers currently live in the sibling `../DDP/` folder (they are generic, not DDP-specific) and are run from within the folder containing the PDFs:

- `_extract.py` — lists every `*.pdf` in the cwd with page count and table-of-contents size (uses PyMuPDF / `fitz`).
- `_outline.py` — dumps document outlines/structure to `_outline.txt`.
- `_ocr.py <in.pdf> <out.txt>` — rasterizes pages at 2.2× and OCRs them with RapidOCR (`rapidocr_onnxruntime`) for image-only slides that have no extractable text.

Intermediate `_ocr_*.txt` / `_outline.txt` files are scratch artifacts, not deliverables. There is no `requirements.txt`; `fitz` (PyMuPDF) and `rapidocr_onnxruntime` come from the shared `../DDP/.venv` (git-ignored).

## Source decks in this folder

`00 - Speech Technology` (overview) · `01 - Articulatory Phonetics` · `02 - Acoustic Phonetics` · `02 - Linguistics and Phonetics` · `03 - Digital Signal Processing` · `04 - Dataset` · `05 - Model Evaluation` · `06 - Speech Synthesis` · `07 - Automatic Speech Recognition`.
