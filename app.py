from datetime import datetime
from pathlib import Path

import markdown
from flask import Flask, abort, render_template

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
ARTICLES_DIR = BASE_DIR / "articles"


def article_files():
    if not ARTICLES_DIR.exists():
        return []

    articles = []
    for path in ARTICLES_DIR.rglob("*.md"):
        stat = path.stat()
        articles.append(
            {
                "slug": path.relative_to(ARTICLES_DIR).with_suffix("").as_posix(),
                "title": path.stem,
                "date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
                "mtime": stat.st_mtime,
            }
        )

    return sorted(articles, key=lambda article: article["mtime"], reverse=True)


def article_path(slug: str) -> Path:
    """Resolve a URL slug without allowing access outside ARTICLES_DIR."""
    candidate = (ARTICLES_DIR / f"{slug}.md").resolve()
    articles_root = ARTICLES_DIR.resolve()
    if articles_root not in candidate.parents:
        abort(404)
    return candidate


def render_article_markdown(path: Path) -> str:
    return markdown.markdown(
        path.read_text(encoding="utf-8"),
        extensions=[
            "extra",
            "fenced_code",
            "footnotes",
            "sane_lists",
            "tables",
            "toc",
        ],
    )


@app.get("/")
def index():
    return render_template("index.html", title="ramblings.derukugi.dev")


@app.get("/ramblings")
def ramblings():
    return render_template(
        "ramblings.html",
        title="ramblings.derukugi.dev",
        articles=article_files(),
    )


@app.get("/ramblings/<path:slug>")
def article(slug: str):
    path = article_path(slug)
    if not path.is_file():
        abort(404)

    return render_template(
        "article.html",
        title=path.stem,
        name=path.stem,
        date=datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
        content=render_article_markdown(path),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4321, debug=True)
