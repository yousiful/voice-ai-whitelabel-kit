#!/usr/bin/env python3
"""Fill {{placeholders}} in an agreement template from a JSON file.

Usage: python agreement/fill.py agreement.md deal.json > out.md

Exits with an error if any placeholder has no value in the JSON file.
Keys in the JSON that the template does not use are reported on stderr.
"""
import json
import re
import sys

PATTERN = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


def fill(template, values):
    """Return (filled_text, missing_keys, unused_keys)."""
    used = set()
    missing = []

    def sub(match):
        key = match.group(1)
        if key not in values:
            if key not in missing:
                missing.append(key)
            return match.group(0)
        used.add(key)
        return str(values[key])

    text = PATTERN.sub(sub, template)
    unused = sorted(k for k in values if k not in used and not k.startswith("_"))
    return text, missing, unused


def main(argv):
    if len(argv) != 3:
        print("usage: fill.py agreement.md deal.json > out.md", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        template = f.read()
    with open(argv[2], encoding="utf-8") as f:
        values = json.load(f)
    text, missing, unused = fill(template, values)
    if missing:
        print("error: missing values for: " + ", ".join(missing), file=sys.stderr)
        return 1
    if unused:
        print("note: unused keys: " + ", ".join(unused), file=sys.stderr)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
