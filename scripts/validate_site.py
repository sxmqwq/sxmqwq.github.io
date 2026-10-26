#!/usr/bin/env python3
"""Validate navigation, article metadata, redirects, and RSS before deployment."""
import json
import posixpath
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ORIGIN = "https://sxmqwq.github.io"
APPS = {"rhythm", "tellshift", "scorem"}


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.canonical = []
        self.redirect = False
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.redirect = True


def assert_local(url, current="/"):
    absolute = urlsplit(urljoin(ORIGIN + current, url))
    if absolute.scheme not in ("http", "https") or absolute.netloc != "sxmqwq.github.io":
        return
    path = unquote(absolute.path)
    path = posixpath.normpath(path)
    if path.lstrip("/").split("/")[0] in APPS:
        return  # These are independently deployed project repositories.
    target = DOCS / path.lstrip("/")
    if target.is_dir():
        target /= "index.html"
    assert target.is_file(), f"Broken local URL {url!r} from {current}"


def main():
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    assert config["homeUrl"] == ORIGIN + "/blog"
    for required in ("index.html", "404.html", "favicon.svg", ".nojekyll", "blog/index.html", "blog/tag.html", "blog/rss.xml", "blog/postList.json"):
        assert (DOCS / required).is_file(), f"Missing {required}"

    home = Page((DOCS / "index.html").read_text(encoding="utf-8"))
    assert home.canonical == [ORIGIN + "/"]
    for destination in ("/blog/", "/rhythm/", "/tellshift/", "/scorem/"):
        assert destination in home.links, f"Missing project entry {destination}"

    pages = list(DOCS.rglob("*.html"))
    for file in pages:
        relative = file.relative_to(DOCS).as_posix()
        text = file.read_text(encoding="utf-8")
        page = Page(text)
        for link in page.links:
            assert_local(link, "/" + relative)
        if relative.startswith("blog/"):
            assert "/" in page.links, f"No portal navigation in {relative}"
            assert len(page.canonical) == 1 and page.canonical[0].startswith(ORIGIN + "/blog/"), f"Wrong blog canonical in {relative}"
            if relative != "blog/index.html":
                legacy = DOCS / relative.removeprefix("blog/")
                old = Page(legacy.read_text(encoding="utf-8"))
                assert old.redirect, f"Legacy URL does not redirect: {legacy}"
                assert old.canonical == page.canonical
                assert "location.search+location.hash" in legacy.read_text(encoding="utf-8")

    metadata = json.loads((ROOT / "blogBase.json").read_text(encoding="utf-8"))
    assert metadata["homeUrl"] == config["homeUrl"]
    posts = 0
    for collection in ("postListJson", "singeListJson"):
        for post in metadata.get(collection, {}).values():
            assert post["htmlDir"].startswith("docs/blog/")
            assert (ROOT / post["htmlDir"]).is_file()
            assert_local(post["postUrl"], "/blog/")
            posts += 1
    post_list = json.loads((DOCS / "blog/postList.json").read_text(encoding="utf-8"))
    for post in post_list.values():
        if isinstance(post, dict) and "postUrl" in post:
            assert_local(post["postUrl"], "/blog/")

    feed = ET.parse(DOCS / "blog/rss.xml")
    for node in feed.findall(".//link") + feed.findall(".//guid"):
        if node.text:
            assert node.text.startswith(config["homeUrl"]), f"Wrong RSS URL: {node.text}"
            assert_local(node.text)
    assert (DOCS / "rss.xml").read_bytes() == (DOCS / "blog/rss.xml").read_bytes()
    print(f"Validated {len(pages)} HTML pages, {posts} posts, four project entries, legacy redirects, metadata and RSS")


if __name__ == "__main__":
    main()
