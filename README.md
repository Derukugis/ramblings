# ramblings

A small Flask and Jinja2 port of the original Rust/Axum ramblings site.

## Run locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open <http://localhost:4321>.

Markdown articles live in `articles/`. Their modification dates are shown in the article list, matching the original application.
