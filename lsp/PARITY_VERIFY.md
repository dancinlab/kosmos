================================================================================
 kosmos LSP — hexa-native port PARITY VERIFICATION  (G2)
================================================================================
 reference : lsp/kosmos_lsp.py   (Python 3.x, DEPRECATED — kept for live LSP)
 port      : lsp/kosmos_lsp.hexa  (hexa 0.1.0-dispatch — canonical --check)
 date (UTC): 2026-06-04  (re-verified after kosmos/2.0 @corpus parity sync)
 git rev   : lane/kosmos-finalize  (off origin/main b329901)
 method    : for every file, compare `python3 lsp/kosmos_lsp.py --check F`
             against `hexa run --no-sentinel lsp/kosmos_lsp.hexa --check F`
             on BOTH stdout (verbatim diagnostic lines) AND exit code.
 note      : 2026-06-04 — the canonical .hexa learned the kosmos/2.0 @corpus
             top-level entry (§5.6); the DEPRECATED .py is now synced to it so
             both accept a @corpus file and emit identical "top-level entry
             (@anchor or @corpus)" diagnostics. 26/26 files byte-equal.
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
PASS  broken_two_anchor.kosmos        (exit=1)  → "exactly one top-level entry per file (@anchor XOR @corpus, kosmos/2.0)"
PASS  broken_missing_coord.kosmos     (exit=0)  → hint "missing ... coord" (sev2 = no exit-fail, matches .py)
PASS  broken_indent_malformed.kosmos  (exit=1)  → malformed @anchor + bad indent + 2 hints
PASS  broken_payload_col0.kosmos      (exit=1)  → "only @anchor / @corpus are column-0 entries" + no-top-entry
PASS  broken_bom_crlf.kosmos          (exit=1)  → BOM + bad indent + malformed @payload + no-top-entry
        (note: CRLF does NOT raise the LF diag under --check — Python text-mode
         universal-newlines normalize CRLF→LF before validate(); the hexa port
         replicates this in k_normalize_newlines() so --check stays byte-parity.)

── FALSIFIER 3 — diagnostic PARITY (identical stdout + exit, .py == .hexa) ──────
   16/16 fixture files (11 clean + 5 broken) : stdout verbatim-equal AND exit-equal.

── FALSIFIER 4 — kosmos/2.0 @corpus top-level entry accepted by BOTH ───────────
PASS  examples/01_text_only.kosmos          (exit=0)  @anchor (1.x) — unchanged
PASS  examples/02_multimodal.kosmos         (exit=0)  @anchor (1.x) — unchanged
PASS  examples/03_anima_knuth_077_mandala…  (exit=0)  @anchor (1.x) — unchanged
PASS  examples/04_corpus_clm_byte.kosmos    (exit=0)  @corpus (2.0) — nested @anchor
                                                      members + member=ref shards
                                                      accepted; pre-sync the .py
                                                      false-rejected this file
                                                      ("must contain exactly one
                                                      @anchor entry"), now fixed.
   4/4 example files : stdout verbatim-equal AND exit-equal (.py == .hexa).

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
 RESULT:  26/26 --check files (11 anchors + 11 fixtures + 4 examples,
          incl. the kosmos/2.0 @corpus example) + 45/45 hover lines → ALL PASS
          validate(text) + hover(line) + --check FILE  are byte-parity between
          the canonical .hexa and the deprecated .py. exit codes identical
          (error→1, hint-only/clean→0).
 SCOPE :  stdio JSON-RPC server NOT ported — hexa 0.1.0-dispatch has no
          incremental raw N-byte stdin read for Content-Length framing on a
          live (never-EOF) editor pipe. See kosmos_lsp.hexa header HONEST TODO.
          bin/kosmos-lsp keeps the .py for live editor sessions; --check (CI) is
          fully hexa-native. (k_validate / k_hover are already server-ready for
          a future port once hexa gains read_stdin_n(n) / fd-0 byte reads.)
================================================================================

── reproduce ───────────────────────────────────────────────────────────────────
  for f in anchors/anima/*.kosmos lsp/test_fixtures/*.kosmos examples/*.kosmos; do
    py=$(python3 lsp/kosmos_lsp.py --check "$f" 2>&1); pr=$?
    hx=$(hexa run --no-sentinel lsp/kosmos_lsp.hexa --check "$f" 2>&1); hr=$?
    [ "$py" = "$hx" ] && [ "$pr" = "$hr" ] && echo "PASS $f" || echo "FAIL $f"
  done
