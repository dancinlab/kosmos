#!/usr/bin/env python3
# kosmos-lsp — canonical LSP server for the .kosmos manifest grammar.
# Stdio JSON-RPC, zero deps (Python 3.8+). Spec-grounded diagnostics +
# hover from spec/kosmos.md. .kosmos is a superset of tape v1.2 adding
# exactly two entry types: @anchor (exactly one per file, at top) and
# @payload (2-space body). Required placement triple: coord/lane/radius.
# Conservative — missing optional structure is a hint (sev 2).
#
#   kosmos-lsp                # speak LSP on stdin/stdout
#   kosmos-lsp --check FILE   # one-shot lint (exit 1 on any error)
import json
import re
import sys

ANCHOR = re.compile(
    r'^@anchor\s+\S+\s*:=\s*".*?"\s*::\s*\S+\s*(?:\[[^\]\n]*\])?\s*$')
PAYLOAD = re.compile(r"^@payload\s+\S+\s*:=")
KV = re.compile(r"^\S+\s*=")
EDGES = ("<-", "->", "=>", "==", "~>", "|>", "!!",
         "<:", ":>", "?>", "!>", "@>")
HEREDOC = re.compile(r"<<~?([A-Za-z_][\w-]*)\s*$")
TRIPLE = ("coord", "lane", "radius")


def diag(ln, c0, c1, msg, sev=1):
    return {"range": {"start": {"line": ln, "character": c0},
                      "end": {"line": ln, "character": c1}},
            "severity": sev, "source": "kosmos-lsp", "message": msg}


def validate(text):
    out = []
    if text.startswith("﻿"):
        out.append(diag(0, 0, 1, "byte-canonical: UTF-8 with no BOM"))
    if "\r" in text:
        out.append(diag(0, 0, 1, "byte-canonical: LF line endings only"))
    lines = text.split("\n")
    anchors, anchor_ln = 0, -1
    seen = set()
    heredoc = None
    for i, raw in enumerate(lines):
        s = raw.rstrip("\r")
        if heredoc is not None:
            if s.strip() == heredoc:
                heredoc = None
            continue
        t = s.strip()
        if t == "" or t.startswith("#"):
            continue
        indent = len(s) - len(s.lstrip(" "))
        if s.startswith("@anchor"):
            anchors += 1
            anchor_ln = i
            if indent:
                out.append(diag(i, 0, len(s),
                           "@anchor must be at column 0"))
            elif not ANCHOR.match(s):
                out.append(diag(i, 0, len(s),
                    'malformed @anchor — expected `@anchor <id> := '
                    '"<name>" :: kosmos-anchor [tier=<N> active]`'))
            continue
        if s.startswith("@"):
            out.append(diag(i, 0, len(s),
                "only @anchor is a column-0 entry; @payload and fields "
                "are 2-space body lines"))
            continue
        # body line
        if indent != 2:
            out.append(diag(i, 0, len(s),
                "body line indented exactly 2 spaces (under @anchor)"))
            continue
        m = HEREDOC.search(t)
        if m:
            heredoc = m.group(1)
            continue
        if t.startswith("@payload"):
            if not PAYLOAD.match(t):
                out.append(diag(i, 2, len(s),
                    "malformed @payload — expected "
                    "`@payload <modality> := ...`"))
            continue
        key = t.split("=", 1)[0].strip() if "=" in t else ""
        if key in TRIPLE:
            seen.add(key)
        tok = t.split(" ", 1)[0]
        if not (tok in EDGES or t.startswith('"') or t.startswith("`")
                or KV.match(t)):
            out.append(diag(i, 2, len(s),
                "unrecognised body form — coord/lane/radius/tier/tags, "
                "an edge, `key = val`, or \"prose\"", sev=2))
    if anchors == 0:
        out.append(diag(0, 0, 1,
            "a .kosmos file must contain exactly one @anchor entry"))
    elif anchors > 1:
        out.append(diag(anchor_ln, 0, 1,
            "exactly one @anchor per file (one anchor = one file)"))
    else:
        miss = [k for k in TRIPLE if k not in seen]
        if miss:
            out.append(diag(anchor_ln, 0, 1,
                "missing required placement field(s): %s "
                "(coord/lane/radius are the required triple)"
                % ", ".join(miss), sev=2))
    return out


def hover(line):
    s = line.strip()
    if s.startswith("@anchor"):
        return "**@anchor** — the one knowledge anchor (placement basin)"
    if s.startswith("@payload"):
        return "**@payload** — one sensory channel into the anchor"
    for k, d in (("coord", "anchor placement (float vector, dim ≥ 1)"),
                 ("lane", "partition / lane id (quoted string)"),
                 ("radius", "influence radius in coord space (float > 0)"),
                 ("tier", "ordinal / rank (optional)"),
                 ("tags", "free annotation (optional)")):
        if s.startswith(k):
            return "**%s** — %s" % (k, d)
    return None


def _read():
    h = {}
    while True:
        ln = sys.stdin.buffer.readline()
        if not ln:
            return None
        ln = ln.decode("ascii", "replace").strip()
        if not ln:
            break
        if ":" in ln:
            k, v = ln.split(":", 1)
            h[k.strip().lower()] = v.strip()
    n = int(h.get("content-length", "0"))
    try:
        return json.loads(sys.stdin.buffer.read(n).decode("utf-8", "replace"))
    except Exception:
        return {}


def _send(o):
    b = json.dumps(o).encode("utf-8")
    sys.stdout.buffer.write(b"Content-Length: %d\r\n\r\n" % len(b) + b)
    sys.stdout.buffer.flush()


def _publish(uri, text):
    try:
        d = validate(text)
    except Exception as e:
        d = [diag(0, 0, 1, "kosmos-lsp internal: %s" % e, 2)]
    _send({"jsonrpc": "2.0", "method": "textDocument/publishDiagnostics",
           "params": {"uri": uri, "diagnostics": d}})


def serve():
    docs = {}
    while True:
        m = _read()
        if m is None:
            break
        meth = m.get("method")
        if meth == "initialize":
            _send({"jsonrpc": "2.0", "id": m.get("id"), "result": {
                "capabilities": {"textDocumentSync": 1,
                                 "hoverProvider": True},
                "serverInfo": {"name": "kosmos-lsp"}}})
        elif meth == "shutdown":
            _send({"jsonrpc": "2.0", "id": m.get("id"), "result": None})
        elif meth == "exit":
            break
        elif meth == "textDocument/didOpen":
            d = m["params"]["textDocument"]
            docs[d["uri"]] = d.get("text", "")
            _publish(d["uri"], docs[d["uri"]])
        elif meth == "textDocument/didChange":
            p = m["params"]
            ch = p.get("contentChanges") or [{}]
            docs[p["textDocument"]["uri"]] = ch[-1].get("text", "")
            _publish(p["textDocument"]["uri"],
                     docs[p["textDocument"]["uri"]])
        elif meth == "textDocument/didClose":
            u = m["params"]["textDocument"]["uri"]
            docs.pop(u, None)
            _send({"jsonrpc": "2.0",
                   "method": "textDocument/publishDiagnostics",
                   "params": {"uri": u, "diagnostics": []}})
        elif meth == "textDocument/hover":
            p = m["params"]
            txt = docs.get(p["textDocument"]["uri"], "")
            ln = p["position"]["line"]
            ls = txt.split("\n")
            hv = hover(ls[ln]) if 0 <= ln < len(ls) else None
            _send({"jsonrpc": "2.0", "id": m.get("id"),
                   "result": ({"contents": {"kind": "markdown",
                                            "value": hv}} if hv else None)})
        elif m.get("id") is not None:
            _send({"jsonrpc": "2.0", "id": m["id"], "result": None})


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--check":
        text = open(sys.argv[2], encoding="utf-8", errors="replace").read()
        ds = validate(text)
        for d in ds:
            print("%s:%d: %s%s" % (
                sys.argv[2], d["range"]["start"]["line"] + 1,
                "" if d["severity"] == 1 else "[hint] ", d["message"]))
        sys.exit(1 if any(d["severity"] == 1 for d in ds) else 0)
    serve()


if __name__ == "__main__":
    main()
