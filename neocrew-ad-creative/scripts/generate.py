#!/usr/bin/env python3
"""
Templates NeoCrew ad variants from variants.json into individual HTML files.
Supports multiple ad FORMATS (not one locked template) — each variant picks
a format, and gets templated against that format's file in formats/.

Usage:
    python3 generate.py variants.json out_dir/

Each entry in variants.json needs a "format" field (one of: bold_statement,
big_stat, chat_thread, comparison_table, receipt) plus that format's fields
— see references/formats.md for the exact field list and examples per
format.
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
FORMATS_DIR = os.path.join(SKILL_DIR, "formats")

# Which JSON fields map to which {{PLACEHOLDER}} per format. Keys not
# present in a variant are simply skipped (so optional fields are fine).
FORMAT_FIELDS = {
    "bold_statement": ["headline", "subhead", "cta"],
    "big_stat": ["stat", "stat_label", "headline", "subhead", "bottom_tag", "cta"],
    "chat_thread": ["msg_user", "msg_neo", "cta"],
    "comparison_table": ["headline", "bottom_tag", "cta"],
    "receipt": ["headline", "total", "agency_total", "bottom_tag", "cta"],
}


def main():
    if len(sys.argv) != 3:
        print("usage: generate.py <variants.json> <out_dir>")
        sys.exit(1)

    variants_path, out_dir = sys.argv[1], sys.argv[2]

    with open(variants_path) as f:
        variants = json.load(f)

    os.makedirs(out_dir, exist_ok=True)

    templates_cache = {}

    for i, v in enumerate(variants):
        fmt = v.get("format")
        if fmt not in FORMAT_FIELDS:
            print(f"WARNING: variant {i} has unknown/missing format "
                  f"'{fmt}', skipping", file=sys.stderr)
            continue

        if fmt not in templates_cache:
            with open(os.path.join(FORMATS_DIR, f"{fmt}.html")) as f:
                templates_cache[fmt] = f.read()
        html = templates_cache[fmt]

        for field in FORMAT_FIELDS[fmt]:
            if field in v:
                html = html.replace("{{" + field.upper() + "}}", v[field])

        label = v.get("label") or f"ad-{i+1:02d}"
        with open(os.path.join(out_dir, f"{label}.html"), "w") as f:
            f.write(html)

    print(f"wrote {len(variants)} files to {out_dir}")


if __name__ == "__main__":
    main()
