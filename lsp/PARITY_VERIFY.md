================================================================================
 kosmos LSP — hexa-native port PARITY VERIFICATION  (G2)
================================================================================
 reference : lsp/kosmos_lsp.py   (Python 3.9.6, DEPRECATED — kept for live LSP)
 port      : lsp/kosmos_lsp.hexa  (hexa 0.1.0-dispatch — canonical --check)
 date (UTC): 2026-05-25T18:25:08Z
 git rev   : 1690345  (branch migrate/anima-kosmos-assets-2026-05-25)
 method    : for every file, compare `python3 lsp/kosmos_lsp.py --check F`
             against `hexa run --no-sentinel lsp/kosmos_lsp.hexa --check F`
             on BOTH stdout (verbatim diagnostic lines) AND exit code.
================================================================================

── FALSIFIER 1 — clean anchors must yield 0 error (exit 0) ─────────────────────
PASS  anchors/anima/knuth_000_zero.kosmos          (exit=0, 0 diag)
PASS  anchors/anima/knuth_015_curiosity.kosmos     (exit=0, 0 diag)
PASS  anchors/anima/knuth_030_compassion.kosmos    (exit=0, 0 diag)
PASS  anchors/anima/knuth_042_question.kosmos      (exit=0, 0 diag)
PASS  anchors/anima/knuth_051_day.kosmos           (exit=0, 0 diag)
PASS  anchors/anima/knuth_060_contemplation.kosmos (exit=0, 0 diag)
PASS  anchors/anima/knuth_077_mandala.kosmos       (exit=0, 0 diag)
PASS  anchors/anima/knuth_080_meditation.kosmos    (exit=0, 0 diag)
PASS  anchors/anima/knuth_091_nirvana.kosmos       (exit=0, 0 diag)
PASS  anchors/anima/knuth_095_unity.kosmos         (exit=0, 0 diag)
PASS  anchors/anima/knuth_100_big_bang.kosmos      (exit=0, 0 diag)

── FALSIFIER 2 — deliberately broken anchors must flag + exit 1 ────────────────
PASS  broken_two_anchor.kosmos        (exit=1)  → "exactly one @anchor per file"
PASS  broken_missing_coord.kosmos     (exit=0)  → hint "missing ... coord" (sev2 = no exit-fail, matches .py)
PASS  broken_indent_malformed.kosmos  (exit=1)  → malformed @anchor + bad indent + 2 hints
PASS  broken_payload_col0.kosmos      (exit=1)  → "only @anchor is a column-0 entry" + no-anchor
PASS  broken_bom_crlf.kosmos          (exit=1)  → BOM + bad indent + malformed @payload + no-anchor
        (note: CRLF does NOT raise the LF diag under --check — Python text-mode
         universal-newlines normalize CRLF→LF before validate(); the hexa port
         replicates this in k_normalize_newlines() so --check stays byte-parity.)

── FALSIFIER 3 — diagnostic PARITY (identical stdout + exit, .py == .hexa) ──────
   16/16 corpus files (11 clean + 5 broken) : stdout verbatim-equal AND exit-equal.

── EXTRA edge-case fixtures (regex-port faithfulness, not coincidental exit) ────
PASS  edge_heredoc_edges.kosmos     (exit=0)  heredoc body skipped (inner @anchor not counted);
                                              edge token `->`, "prose", `backtick`, tier/tags all accepted
PASS  edge_anchor_variants.kosmos   (exit=1)  @anchor missing closing `]` → malformed (group can't match)
PASS  edge_anchor_nobracket.kosmos  (exit=0)  optional grade-tag bracket absent → still valid
PASS  edge_empty.kosmos             (exit=1)  empty file → "must contain exactly one @anchor"
PASS  edge_comments_only.kosmos     (exit=1)  shebang+comments only → no anchor
PASS  edge_payload_malformed.kosmos (exit=1)  `@payload := ...` (no modality) + `@payload text ...` (no :=)
   6/6 edge files : stdout verbatim-equal AND exit-equal.

── HOVER parity (k_hover vs .py hover, line-by-line) ───────────────────────────
   45/45 lines of knuth_077_mandala.kosmos : hover string verbatim-equal.

================================================================================
 RESULT:  22/22 --check files + 6/6 edge files + 45/45 hover lines  → ALL PASS
          validate(text) + hover(line) + --check FILE  are byte-parity with the
          reference .py. exit codes identical (error→1, hint-only/clean→0).
 SCOPE :  stdio JSON-RPC server NOT ported — hexa 0.1.0-dispatch has no
          incremental raw N-byte stdin read for Content-Length framing on a
          live (never-EOF) editor pipe. See kosmos_lsp.hexa header HONEST TODO.
          bin/kosmos-lsp keeps the .py for live editor sessions; --check (CI) is
          fully hexa-native. (k_validate / k_hover are already server-ready for
          a future port once hexa gains read_stdin_n(n) / fd-0 byte reads.)
================================================================================

── reproduce ───────────────────────────────────────────────────────────────────
  for f in anchors/anima/*.kosmos lsp/test_fixtures/*.kosmos; do
    py=$(python3 lsp/kosmos_lsp.py --check "$f" 2>&1); pr=$?
    hx=$(/Users/ghost/.hx/bin/hexa run --no-sentinel lsp/kosmos_lsp.hexa --check "$f" 2>&1); hr=$?
    [ "$py" = "$hx" ] && [ "$pr" = "$hr" ] && echo "PASS $f" || echo "FAIL $f"
  done
