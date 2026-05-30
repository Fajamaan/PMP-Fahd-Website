# PMP — Fahd Website

A self-contained **PMP (Project Management Professional) practice-quiz web app**, plus the
build pipeline that generates it and a companion Claude "exam coach" skill.

## What's here

| Path | Description |
|------|-------------|
| `PMP-Quiz/index.html` | **The deliverable.** A single, self-contained HTML/CSS/JS quiz app — no server or internet needed. Just open it in a browser. |
| `PMP-Quiz/README.md` | Notes for the app itself. |
| `build/build_html.py` | Build script: serializes the question data and embeds it into `index.html`. |
| `build/new_questions.py` | The "New set" question bank (399 questions transcribed from PMP 1/2/3 + Important Questions). |
| `build/parse.py`, `build/questions_data.js` | Pipeline + data for the original 228-question deck. |
| `build/serve.py` | Tiny local static server for previewing the app. |

## The app

- **Two question banks**, toggled by tabs:
  - 📘 **Original deck** — 228 questions
  - 🆕 **New set** — 399 questions (PMP 1, PMP 2, PMP 3, and "Important Questions")
- Each question shows the **correct answer + an explanation**.
- Supports single-answer and multi-select ("choose two/three") questions.
- Mixed **English and Arabic** (Arabic questions render right-to-left).
- **"Analyze with Claude"** button: after answering, opens a pre-filled `claude.ai` chat
  that analyzes the question through the PMI mindset using the `pmp-expert` skill persona.

## Building

The app is pre-built — `PMP-Quiz/index.html` is ready to use as-is. To regenerate it after
editing the question banks:

```bash
python build/build_html.py
```

## Previewing locally

```bash
python build/serve.py 8731
# then open http://localhost:8731
```

## Note on content

The question banks were transcribed from third-party PMP practice materials for personal
study use. This repository is **private** for that reason. Some answer keys from the source
were debatable and are flagged inside the relevant explanations.
