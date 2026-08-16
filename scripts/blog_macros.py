"""mkdocs-macros plugin hooks: scans docs/post/**/*.md front-matter to
build the blog post list and the recent posts / categories / tags sidebar,
so docs/index.md never has to be hand-edited when a post is added."""

import re
from pathlib import Path

import yaml

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def _load_posts(docs_dir: Path):
    posts = []
    for md_file in (docs_dir / "post").glob("**/*.md"):
        text = md_file.read_text(encoding="utf-8")
        match = FRONT_MATTER_RE.match(text)
        if not match:
            continue
        meta = yaml.safe_load(match.group(1)) or {}
        if not meta.get("title") or not meta.get("date"):
            continue
        url = str(md_file.relative_to(docs_dir).with_suffix("")) + "/"
        posts.append(
            {
                "title": meta["title"],
                "date": str(meta["date"]),
                "category": meta.get("category", ""),
                "tags": meta.get("tags", []) or [],
                "url": url,
            }
        )
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def _render_posts(posts):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    parts = ['<div class="post-list">']
    for post in posts:
        year, month, day = post["date"].split("-")
        pretty_date = f"{months[int(month) - 1]} {int(day)}, {year}"
        parts.append(
            '<article class="post-card">'
            f'<h2 class="post-card-title"><a href="{post["url"]}">{post["title"]}</a></h2>'
            f'<p class="post-card-meta">Published on {pretty_date} — by Fernando Celmer</p>'
            f'<a class="post-card-cta" href="{post["url"]}">CONTINUE READING &rarr;</a>'
            "</article>"
        )
    parts.append("</div>")
    return "\n".join(parts)


def _render_sidebar(posts, recent_count=5):
    categories = {}
    tags = {}
    for post in posts:
        if post["category"]:
            categories.setdefault(post["category"], post["url"])
        for tag in post["tags"]:
            tags.setdefault(tag, post["url"])

    parts = ['<aside class="blog-sidebar">']

    parts.append('<section class="sidebar-widget">')
    parts.append('<h3 class="sidebar-widget-title">Recent posts</h3>')
    parts.append('<ul class="sidebar-list">')
    for post in posts[:recent_count]:
        parts.append(f'<li><a href="{post["url"]}">{post["title"]}</a></li>')
    parts.append("</ul>")
    parts.append("</section>")

    parts.append('<section class="sidebar-widget">')
    parts.append('<h3 class="sidebar-widget-title">Categories</h3>')
    parts.append('<ul class="sidebar-list">')
    for name, url in categories.items():
        parts.append(f'<li><a href="{url}">{name}</a></li>')
    parts.append("</ul>")
    parts.append("</section>")

    parts.append('<section class="sidebar-widget">')
    parts.append('<h3 class="sidebar-widget-title">Tags</h3>')
    parts.append('<div class="tag-cloud">')
    for name, url in tags.items():
        parts.append(f'<a class="tag" href="{url}">{name}</a>')
    parts.append("</div>")
    parts.append("</section>")

    parts.append("</aside>")
    return "\n".join(parts)


def define_env(env):
    docs_dir = Path(env.conf["docs_dir"])

    @env.macro
    def blog_posts():
        return _render_posts(_load_posts(docs_dir))

    @env.macro
    def blog_sidebar():
        return _render_sidebar(_load_posts(docs_dir))
