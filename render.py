#!/bin/env python3

import sys
import schema
import click
from strictyaml import load
from datetime import datetime
from io import StringIO


def gen(layout):
    res = {}
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            res[cell] = (10 + x * 10, 10 + y * 10)
    return res


layout = gen(
    [
        [5, 4],
        [3, 2],
        [1, 0],
    ]
)

def point(x, y):
    return f'<circle cx="{x}" cy="{y}" r="1" stroke="#000" fill="#fff" />'

points = "".join(point(x, y) for x, y in layout.values())


def diagram(inp, path: str=""):
    res = ""
    for i, sub in enumerate(int(sub.strip()) for sub in inp.split(",")):
        x, y = layout[sub]
        if i == 0:
            res += "M{} {}".format(x, y)
        else:
            res += " L{} {}".format(x, y)
    return (
        '<svg class="diagram" viewBox="0 0 40 50" xmlns="http://www.w3.org/2000/svg">'
        + """<defs>
  <marker id="arrowhead" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto">
    <polygon points="0 0, 5 2.5, 0 5" />
  </marker>
</defs>"""
        + f'<path d="{res}" stroke="#000" fill="none" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />'
        + (f'<path d="{path}" stroke-dasharray="1,1" stroke="#000" fill="none" />' if path != "" else "")
        + points
        + "</svg>"
    )


@click.group()
def cli():
    pass

@cli.command()
@click.argument("typ", default=0)
def render(typ=0):
    res = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Kyokukey Layout</title>
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css" />
        <style>
            .diagram {
                height: 7rem;
            }
            .label {
                font-size: 1rem;
            }
            .letters :nth-child(odd) {
                background-color: #eee;
            }
        </style>
    </head>
    <body>
        <div id="letters" class="w3-container">
"""

    i = 0
    for line in sys.stdin:
        if line.startswith("#"):
            continue
        raw = line.split(' ', 2)
        name = raw[0]
        inp = raw[1]
        path = raw[2] if len(raw) > 2 else ""
        res += f'''
<div id="key-{name}" class="{'w3-quarter' if typ == 1 else 'w3-rest'}">
    <div class="w3-container">
        <a class="label w3-quarter" href="#key-{name}">{name}</a>
        <div class="w3-rest">{diagram(inp, path)}</div>
    </div>
</div>
'''
        #res += f'<tr id="key-{name}">'
        #res += f'<td><a href="#key-{name}">{name}</a></td>'
        #res += f"<td>{diagram(inp, path)}</td>"
        #res += "</tr>\n"

    res += """
        </div>
        <p>Generated on """+datetime.utcnow().isoformat()+""".</p>
        <a href="https://github.com/nyiyui/render">Source</a>
    </body>
</html>
    """

    sys.stdout.write(res)

@cli.command()
@click.option("--inf",
              type=click.Choice([e.value for e in schema.InputFormat]),
              default="yaml")
def data(inf):
    data = yeet.convert(sys.stdin) if inf == schema.InputFormat.TXT else load(sys.stdin.read())
    out = StringIO()
    out.write(f"# generated on {datetime.utcnow().isoformat()}\n")
    out.write("from adafruit_hid.keycode import Keycode\n")
    out.write("\n"*2)
    out.write("keys = {\n")
    for i, key in enumerate(data["keys"]):
        if schema.Format.DATA in key.get("ignore", []):
            continue
        out.write("    ")
        out.write(f"({', '.join(map(str, list(dict.fromkeys(key['seq']))))}{',' if len(key['seq']) in (0, 1) else ''}): [Keycode.{key['key']}],")
        out.write("\n")
    out.write("}\n")
    print(out.getvalue())

if __name__ == "__main__":
    cli()
