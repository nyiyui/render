#!/bin/env python3

from schema import schema, Format
from strictyaml import as_document

import sys

def convert(file):
    data = {
        "keys": [],
    }
    for line in sys.stdin:
        line = line.strip()
        raw = line.split(" ", 2)
        if len(raw) == 2:
            raw.append("")
        key, seq, svg = raw
        data["keys"].append({
            "key": key[1:] if line.startswith("#") else key,
            "seq": seq.split(','),
            **({"ignore": [Format.RENDER.value]} if line.startswith("#") else {}),
            **({"svg": svg} if svg else {}),
        })
    print(as_document(data, schema).as_yaml())

if __name__ == "__main__":
    convert(sys.stdin)
