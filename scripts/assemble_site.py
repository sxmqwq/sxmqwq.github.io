#!/usr/bin/env python3
"""Publish the blog at the domain root and preserve former /blog/ URLs."""
import argparse
import html
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ORIGIN = "https://sxmqwq.github.io"


def blog_url(value):
    parts = urlsplit(value)
    if parts.netloc and (parts.scheme not in ("https", "http") or parts.netloc != "sxmqwq.github.io"):
        return value
    if parts.path == "/blog" or parts.path.startswith("/blog/"):
        return urlunsplit(parts._replace(path=parts.path[5:] or "/"))
    return value


def redirect_page(target):
    target = quote(target, safe="/")
    escaped = html.escape(target, quote=True)
    script_target = json.dumps(target).replace("<", "\\u003c")
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>blog · sxmqwq</title><link rel="canonical" href="{ORIGIN}{escaped}">
<script>location.replace({script_target}+location.search+location.hash);</script>
<meta http-equiv="refresh" content="0;url={escaped}"></head>
<body><a href="{escaped}">blog</a></body></html>
'''


def assemble(source=None, metadata=None, backup=None):
    source = (source or DOCS).resolve()
    for required in ("index.html", "tag.html", "rss.xml", "postList.json"):
        if not (source / required).is_file():
            raise ValueError(f"Incomplete Gmeek output: {required}")

    # Stage the complete site before replacing published files. When reassembling
    # docs, discard the compatibility directory so redirects never nest.
    with tempfile.TemporaryDirectory(prefix="blog-site-") as directory:
        staged = Path(directory) / "docs"
        shutil.copytree(source, staged, ignore=lambda folder, names: ["blog"] if Path(folder) == source and "blog" in names else [])
        pages = [path for path in staged.rglob("*.html") if path.name != "404.html"]
        for path in pages:
            text = path.read_text(encoding="utf-8")
            text = re.sub(r'''\b(href|src|content)=(['"])(.*?)\2''',
                          lambda m: m[1] + "=" + m[2] + blog_url(m[3]) + m[2], text)
            text = re.sub(r'<nav\b[^>]*id="site-navigation"[^>]*>.*?</nav>', "", text, flags=re.S)
            text = re.sub(r'''<link\b[^>]*\brel=['"]canonical['"][^>]*>\s*''', "", text)
            relative = path.relative_to(staged)
            target = "/" if relative == Path("index.html") else "/" + relative.as_posix()
            canonical = ORIGIN + quote(target, safe="/")
            text = text.replace("</head>", f'<link rel="canonical" href="{canonical}">\n</head>', 1)
            text = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
            path.write_text(text, encoding="utf-8")
            legacy = staged / "blog" / relative
            legacy.parent.mkdir(parents=True, exist_ok=True)
            legacy.write_text(redirect_page(target), encoding="utf-8")

        feed = staged / "rss.xml"
        text = re.sub(r">(https?://sxmqwq\.github\.io[^<]*)<", lambda m: ">" + blog_url(m[1]) + "<", feed.read_text(encoding="utf-8"))
        feed.write_text(text, encoding="utf-8")
        shutil.copy2(feed, staged / "blog/rss.xml")
        # Keep the old search-data URL usable with its original relative links.
        shutil.copy2(staged / "postList.json", staged / "blog/postList.json")
        (staged / "404.html").write_text('''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>404 · sxmqwq</title></head>
<body><h1>404</h1><a href="/">返回博客</a></body></html>
''', encoding="utf-8")
        (staged / ".nojekyll").touch()

        base_path = ROOT / "blogBase.json"
        base = json.loads((metadata or base_path).read_text(encoding="utf-8"))
        base["homeUrl"] = ORIGIN
        for collection in ("postListJson", "singeListJson"):
            for post in base.get(collection, {}).values():
                if "htmlDir" in post:
                    relative = post["htmlDir"].removeprefix("docs/blog/").removeprefix("docs/")
                    post["htmlDir"] = "docs/" + relative
                if "postUrl" in post:
                    post["postUrl"] = blog_url(post["postUrl"])
        for key in ("prevUrl", "nextUrl"):
            if key in base:
                base[key] = blog_url(base[key])

        if DOCS.exists():
            shutil.rmtree(DOCS)
        shutil.copytree(staged, DOCS)
        base_path.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if backup:
            shutil.copytree(backup, ROOT / "backup", dirs_exist_ok=True)
    print("Assembled blog at /; preserved /blog/ article, search and RSS URLs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blog-source", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--backup", type=Path)
    args = parser.parse_args()
    assemble(args.blog_source, args.metadata, args.backup)

