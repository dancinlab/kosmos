#!/usr/bin/env python3
# kosmos-lsp — LSP server for the .kosmos manifest grammar (DEPRECATED).
#
# The CANONICAL linter is the hexa-native lsp/kosmos_lsp.hexa (project.tape
# @D k_hexa_native). This .py is retained ONLY as the live-editor stdio
# JSON-RPC server, because hexa 0.1.0-dispatch has no incremental raw N-byte
# stdin read for LSP Content-Length framing on a never-EOF editor pipe. The
# `--check` (CI) path routes to the .hexa via bin/kosmos-lsp; this file backs
# only interactive sessions. validate()/hover() are kept byte-parity with the
# canonical .hexa (see lsp/PARITY_VERIFY.md).
#
# Stdio JSON-RPC, zero deps (Python 3.8+). Spec-grounded diagnostics +
# hover from spec/kosmos.md. .kosmos is a superset of tape v1.2 adding
# three entry types (kosmos/2.0): @anchor / @corpus (exactly one top-level
# entry per file, at column 0) and @payload (2-space body). Required
# placement triple: coord/lane/radius. Conservative — missing optional
# structure is a hint (sev 2).
#
#   kosmos-lsp                # speak LSP on stdin/stdout
#   kosmos-lsp --check FILE   # one-shot lint (exit 1 on any error)
import json
import re
import sys

ANCHOR = re.compile(
    r'^@anchor\s+\S+\s*:=\s*".*?"\s*::\s*\S+\s*(?:\[[^\]\n]*\])?\s*$')
# @corpus has the same header shape as @anchor (kosmos/2.0 §5.6); the kind
# token \S+ accepts kosmos-corpus. ANCHOR_BODY matches a nested @anchor
# member's header at any indent (validated against the column-0-stripped form).
CORPUS = re.compile(
    r'^@corpus\s+\S+\s*:=\s*".*?"\s*::\s*\S+\s*(?:\[[^\]\n]*\])?\s*$')
ANCHOR_BODY = re.compile(
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
    anchors, corpora, anchor_ln = 0, 0, -1
    corpus_mode = False   # True once a @corpus top-level entry is seen
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
        if indent == 0:
            # column-0 = the single top-level entry: @anchor XOR @corpus
            if t.startswith("@anchor"):
                anchors += 1
                anchor_ln = i
                if not ANCHOR.match(s):
                    out.append(diag(i, 0, len(s),
                        'malformed @anchor — expected `@anchor <id> := '
                        '"<name>" :: kosmos-anchor [tier=<N> active]`'))
            elif t.startswith("@corpus"):
                corpora += 1
                corpus_mode = True
                anchor_ln = i
                if not CORPUS.match(s):
                    out.append(diag(i, 0, len(s),
                        'malformed @corpus — expected `@corpus <id> := '
                        '"<name>" :: kosmos-corpus [tier=<N> active]`'))
            else:
                out.append(diag(i, 0, len(s),
                    "only @anchor / @corpus are column-0 entries; @payload "
                    "and fields are indented body lines"))
            continue
        # indented body line (indent >= 2)
        if corpus_mode:
            # §5.6 corpus body: nested @anchor members / member refs / corpus
            # fields / member payloads — accepted at any indent >= 2.
            m = HEREDOC.search(t)
            if m:
                heredoc = m.group(1)
                continue
            if t.startswith("@anchor"):
                if not ANCHOR_BODY.match(t):
                    out.append(diag(i, indent, len(s),
                        'malformed @corpus member — expected `@anchor <id> '
                        ':= "<name>" :: kosmos-anchor [...]`'))
                continue
            if t.startswith("@payload"):
                if not PAYLOAD.match(t):
                    out.append(diag(i, indent, len(s),
                        "malformed @payload — expected "
                        "`@payload <modality> := ...`"))
                continue
            key = t.split("=", 1)[0].strip() if "=" in t else ""
            if key in TRIPLE:
                seen.add(key)
            tok = t.split(" ", 1)[0]
            if not (tok in EDGES or t.startswith('"') or t.startswith("`")
                    or KV.match(t)):
                out.append(diag(i, indent, len(s),
                    "unrecognised @corpus body — member @anchor/@payload, "
                    "`key = val` (anchor_level/count/lane_mix/vocab/encoding/"
                    "merkle/member/closed_corpus), edge, or \"prose\"", sev=2))
            continue
        # @anchor body — strict 2-space (legacy 1.x path, unchanged)
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
    top = anchors + corpora
    if top == 0:
        out.append(diag(0, 0, 1,
            "a .kosmos file must contain exactly one top-level entry "
            "(@anchor or @corpus)"))
    elif top > 1:
        out.append(diag(anchor_ln, 0, 1,
            "exactly one top-level entry per file "
            "(@anchor XOR @corpus, kosmos/2.0)"))
    else:
        miss = [k for k in TRIPLE if k not in seen]
        if miss:
            out.append(diag(anchor_ln, 0, 1,
                "missing required placement field(s): %s "
                "(coord/lane/radius are the required triple)"
                % ", ".join(miss), sev=2))
    return out


def hover(line):
    # byte-parity with lsp/kosmos_lsp.hexa k_hover (same order, same strings).
    s = line.strip()
    if s.startswith("@anchor"):
        return "**@anchor** — the one knowledge anchor (placement basin)"
    if s.startswith("@corpus"):
        return ("**@corpus** — a dataset: an ordered collection of member "
                "anchors, itself a meta-anchor (kosmos/2.0 §5.6)")
    if s.startswith("@payload"):
        return "**@payload** — one sensory channel into the anchor"
    if s.startswith("anchor_level"):
        return ("**anchor_level** — member granularity: sample | topic | "
                "2tier (default 2tier)")
    if s.startswith("lane_mix"):
        return ("**lane_mix** — per-lane mixing fractions, Σ = 1.0 (e.g. "
                "\"web=0.8, register=0.2\")")
    if s.startswith("member"):
        return ("**member** — a packed anchor-pack shard: `member = ref "
                "\"*.limen\" sha256=… frac=…`")
    if s.startswith("closed_corpus"):
        return ("**closed_corpus** — corpus integrity (Σ frac = 1.0 ∧ ∀ "
                "member sha256 verified)")
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
