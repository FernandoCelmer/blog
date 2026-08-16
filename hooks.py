"""MkDocs hooks: registers Jinja filters used by theme template overrides
(overrides/modules/content.html, overrides/modules/head_extra_links.html)."""

import json

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def _fmt_date(value):
    if value is None or value == "":
        return value
    if hasattr(value, "year") and hasattr(value, "month") and hasattr(value, "day"):
        return f"{_MONTHS[value.month - 1]} {value.day}, {value.year}"
    return value


def _to_json(value):
    return json.dumps(value).replace("</", "<\\/")


def on_env(env, config, files):
    env.filters["fmt_date"] = _fmt_date
    env.filters["tojson"] = _to_json
    return env
