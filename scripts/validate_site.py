#!/usr/bin/env python3
"""Validate navigation, article metadata, redirects, and RSS before deployment."""
import json
import posixpath
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit

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
    assert path.lstrip("/").split("/")[0] not in APPS, f"Removed app URL: {url}"
    target = DOCS / path.lstrip("/")
    if target.is_dir():
        target /= "index.html"
    assert target.is_file(), f"Broken local URL {url!r} from {current}"


def main():
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    assert config["homeUrl"] == ORIGIN
    for required in ("index.html", "404.html", ".nojekyll", "tag.html", "rss.xml", "postList.json", "blog/index.html", "blog/tag.html", "blog/rss.xml", "blog/postList.json"):
        assert (DOCS / required).is_file(), f"Missing {required}"

    home = Page((DOCS / "index.html").read_text(encoding="utf-8"))
    assert home.canonical == [ORIGIN + "/"]
    assert not home.redirect, "The domain root must show the blog directly"
    assert any("post/" in link for link in home.links), "No blog articles on the home page"

    pages = list(DOCS.rglob("*.html"))
    for file in pages:
        relative = file.relative_to(DOCS).as_posix()
        text = file.read_text(encoding="utf-8")
        page = Page(text)
        for link in page.links:
            assert_local(link, "/" + relative)
        assert 'id="site-navigation"' not in text, f"Obsolete portal navigation in {relative}"
        if relative.startswith("blog/"):
            current = DOCS / relative.removeprefix("blog/")
            actual = Page(current.read_text(encoding="utf-8"))
            assert page.redirect, f"Legacy URL does not redirect: {relative}"
            assert page.canonical == actual.canonical
            assert "location.search+location.hash" in text
        elif relative != "404.html":
            target = "/" if relative == "index.html" else "/" + quote(relative, safe="/")
            assert page.canonical == [ORIGIN + target], f"Wrong blog canonical in {relative}"
            assert not page.redirect, f"Blog page unexpectedly redirects: {relative}"

    metadata = json.loads((ROOT / "blogBase.json").read_text(encoding="utf-8"))
    assert metadata["homeUrl"] == config["homeUrl"]
    posts = 0
    for collection in ("postListJson", "singeListJson"):
        for post in metadata.get(collection, {}).values():
            assert post["htmlDir"].startswith("docs/") and not post["htmlDir"].startswith("docs/blog/")
            assert (ROOT / post["htmlDir"]).is_file()
            assert_local(post["postUrl"], "/")
            posts += 1
    post_list = json.loads((DOCS / "postList.json").read_text(encoding="utf-8"))
    for post in post_list.values():
        if isinstance(post, dict) and "postUrl" in post:
            assert_local(post["postUrl"], "/")

    feed = ET.parse(DOCS / "rss.xml")
    for node in feed.findall(".//link") + feed.findall(".//guid"):
        if node.text:
            assert node.text.startswith(config["homeUrl"]), f"Wrong RSS URL: {node.text}"
            assert not urlsplit(node.text).path.startswith("/blog"), f"Old RSS URL: {node.text}"
            assert_local(node.text)
    assert (DOCS / "rss.xml").read_bytes() == (DOCS / "blog/rss.xml").read_bytes()
    print(f"Validated {len(pages)} HTML pages, {posts} posts, root blog, legacy redirects, metadata and RSS")


if __name__ == "__main__":
    main()

