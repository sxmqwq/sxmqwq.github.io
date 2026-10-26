#!/usr/bin/env python3
"""Assemble the portal, generated blog, and permanent legacy entry points."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BLOG = DOCS / "blog"
ORIGIN = "https://sxmqwq.github.io"
BLOG_HOME = ORIGIN + "/blog"
GENERATED_ROUTE = re.compile(r"^/(?:post/.*|(?:index|tag|page\d+)\.html|(?:rss\.xml|postList\.json))$")
NAV = '''<nav id="site-navigation" aria-label="站点导航" style="display:flex;flex-wrap:wrap;gap:16px;margin-bottom:20px;font-size:13px"><a href="/">返回主页</a><a href="/blog/">blog</a><a href="/scorem/">scorem</a><a href="/rhythm/">rhythm</a><a href="/tellshift/">Tellshift</a></nav>'''


def blog_url(value):
    parts = urlsplit(value)
    if parts.netloc and (parts.scheme not in ("https", "http") or parts.netloc != "sxmqwq.github.io"):
        return value
    if parts.netloc and parts.path in ("", "/"):
        parts = parts._replace(scheme="https", path="/blog/")
    elif GENERATED_ROUTE.fullmatch(parts.path):
        parts = parts._replace(path="/blog" + parts.path)
    else:
        return value
    return urlunsplit(parts)


def redirect_page(target):
    target = quote(target, safe="/")
    escaped = html.escape(target, quote=True)
    script_target = json.dumps(target).replace("<", "\\u003c")
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>博客已迁移 · sxmqwq</title><link rel="canonical" href="{ORIGIN}{escaped}">
<script>location.replace({script_target}+location.search+location.hash);</script>
<meta http-equiv="refresh" content="0;url={escaped}"></head>
<body><p>博客已迁移至 <a href="{escaped}">{escaped}</a>。</p></body></html>
'''


def import_blog(source):
    source = source.resolve()
    if source == BLOG.resolve() or BLOG.resolve() in source.parents:
        raise ValueError("The generated source must be outside the published blog")
    for required in ("index.html", "tag.html", "rss.xml", "postList.json"):
        if not (source / required).is_file():
            raise ValueError(f"Incomplete Gmeek output: {required}")
    # Copy first so a failed generation or copy never removes the published files.
    staged = DOCS / ".blog-staging"
    if staged.exists():
        shutil.rmtree(staged)
    shutil.copytree(source, staged)
    if BLOG.exists():
        shutil.rmtree(BLOG)
    staged.rename(BLOG)


def assemble(source=None, metadata=None, backup=None):
    DOCS.mkdir(exist_ok=True)
    if source:
        import_blog(source)
    if not (BLOG / "index.html").is_file():
        raise ValueError("Missing docs/blog/index.html")
    if metadata:
        shutil.copy2(metadata, ROOT / "blogBase.json")
    if backup:
        shutil.copytree(backup, ROOT / "backup", dirs_exist_ok=True)

    # Gmeek uses root-relative pagination even with a custom homeUrl.
    # Rewrite generated navigation and metadata, while leaving app routes alone.
    for path in BLOG.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r'''\b(href|src|content)=(['"])(.*?)\2''',
            lambda m: m[1] + "=" + m[2] + blog_url(m[3]) + m[2],
            text,
        )
        if 'id="site-navigation"' in text:
            text = re.sub(r'<nav\b[^>]*id="site-navigation"[^>]*>.*?</nav>', lambda m: NAV, text, count=1, flags=re.S)
        else:
            text = re.sub(r"<body\b[^>]*>", lambda m: m[0] + "\n" + NAV, text, count=1)
        canonical = "/blog/" if path == BLOG / "index.html" else "/blog/" + quote(path.relative_to(BLOG).as_posix(), safe="/")
        if not re.search(r'''rel=['"]canonical['"]''', text):
            text = text.replace("</head>", f'<link rel="canonical" href="{ORIGIN}{canonical}">\n</head>', 1)
        text = "\n".join(line.rstrip() for line in text.splitlines()).rstrip() + "\n"
        path.write_text(text, encoding="utf-8")

        relative = path.relative_to(BLOG)
        if relative != Path("index.html"):
            legacy = DOCS / relative
            legacy.parent.mkdir(parents=True, exist_ok=True)
            legacy.write_text(redirect_page("/blog/" + relative.as_posix()), encoding="utf-8")

    feed = BLOG / "rss.xml"
    # Only replace URLs in XML fields, not arbitrary article text.
    text = re.sub(r">(https?://sxmqwq\.github\.io[^<]*)<", lambda m: ">" + blog_url(m[1]) + "<", feed.read_text(encoding="utf-8"))
    feed.write_text(text, encoding="utf-8")
    # An XML copy keeps existing feed readers subscribed to /rss.xml working.
    shutil.copy2(feed, DOCS / "rss.xml")
    shutil.copy2(BLOG / "postList.json", DOCS / "postList.json")

    base_path = ROOT / "blogBase.json"
    base = json.loads(base_path.read_text(encoding="utf-8"))
    base["homeUrl"] = BLOG_HOME
    for collection in ("postListJson", "singeListJson"):
        for post in base.get(collection, {}).values():
            if "htmlDir" in post:
                relative = post["htmlDir"].removeprefix("docs/blog/").removeprefix("docs/")
                post["htmlDir"] = "docs/blog/" + relative
    for key in ("prevUrl", "nextUrl"):
        if key in base:
            base[key] = blog_url(base[key])
    base_path.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for path in (ROOT / "home").iterdir():
        if path.is_file():
            shutil.copy2(path, DOCS / path.name)
    (DOCS / ".nojekyll").touch()
    print("Assembled portal at / and blog at /blog/; preserved legacy article and RSS URLs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blog-source", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--backup", type=Path)
    args = parser.parse_args()
    assemble(args.blog_source, args.metadata, args.backup)
