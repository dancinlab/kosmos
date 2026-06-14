# kosmos — Architecture (SSOT · update-in-place)

> Single source of truth for the final architecture. **Overwrite (update) this file** when the architecture changes — do not append. History and decisions live in `CHANGELOG.md`.

## Overview

`kosmos` is a **multimodal knowledge-anchor manifest format** — the fifth sibling
of the dancinlab format family (`tape` = causal-temporal trace, `n6` = semantic
atlas layer, `hxc` = byte-canonical wire, `n12` = 12-axis sparse cube). A
`.kosmos` file describes exactly one top-level entry — an **anchor** (one point /
basin in an abstract placement space) or a **corpus** (an ordered collection of
member anchors, kosmos/2.0) — as two orthogonal layers:

1. **Placement coordinates** (`coord` / `lane` / `radius` / `tier` / `tags`) —
   *modality-independent*. The anchor's location exists with zero sensory
   channels.
2. **Sensory payloads** (`@payload <modality> := …`) — *modality-specific*. Zero
   or more channels (text · image · audio · video · …, open enum) that all flow
   into the same placement.

The format commits to **cross-modal consistency**: `∀ modality m : ‖ Eₘ(payloadₘ) − coord ‖ < radius`.
The grammar is a strict **tape v1.2 superset** (line-oriented, grep-friendly).
The base spec is substrate-independent; concrete field semantics are bound by a
**profile** — a profile binds semantics only, never grammar.

## Components

| Component | Path | Role | Anchor / Profile / IO |
|---|---|---|---|
| `.kosmos` format (grammar SSOT) | `spec/kosmos.md` | Canonical, versioned grammar (kosmos/2.1) — `@anchor` / `@payload` / `@corpus` entry types, placement triple, 3 payload forms | Grammar SSOT — profiles bind semantics, never grammar |
| `.limen` packed format | `spec/limen.md` | Binary container a `@corpus` member `ref` points at (packed anchor-harbor shards, merkle commitment) | IO — corpus shard payload |
| Profile: anima-consciousness-carving | `spec/profiles/anima-consciousness-carving.md` | First profile — binds `coord`/`lane`/`radius`/`tier`/`tags` to the anima CONSCIOUSNESS-CARVING paradigm | Profile (semantics only) |
| Profile: anima-emergence-trace | `spec/profiles/anima-emergence-trace.md` | Second profile binding | Profile (semantics only) |
| LSP linter (canonical) | `lsp/kosmos_lsp.hexa` | hexa-native spec-grounded diagnostics + hover (`k_hexa_native`) | IO — editor diagnostics; `bin/kosmos-lsp --check` |
| LSP stdio server (deprecated) | `lsp/kosmos_lsp.py` | Interactive JSON-RPC server (retained only for live-editor Content-Length framing) | IO — editor stdio; byte-parity with `.hexa` (`lsp/PARITY_VERIFY.md`) |
| tree-sitter grammar | `tree-sitter-kosmos/` | Total line model for tree-sitter editors (Neovim · Helix · Zed · Emacs) | IO — syntax highlight |
| limen reference codec | `impl/limen.hexa` | Reference encoder/decoder for the `.limen` packed format | IO — corpus pack/unpack |
| HF export tool | `tool/corpus_to_hf.hexa` | `@corpus` → Hugging Face `datasets` manifest emitter (`docs/hf_export.md`) | IO — dataset mirror export |
| Examples & anchors | `examples/`, `anchors/` | Worked `.kosmos` files (text-only · multimodal · corpus · anima) | Anchor instances |

## Data flow

```
authoring → validation → consumption
─────────────────────────────────────────────────────────────────
  *.kosmos        bin/kosmos-lsp --check   payload encoders Eₘ
  (one @anchor      → lsp/kosmos_lsp.hexa     → assert ‖Eₘ(payloadₘ) − coord‖ < radius
   XOR @corpus)     (spec-grounded lint)     → cross-modal placement is the anchor
        │                  │
        │           tree-sitter-kosmos/      @corpus → tool/corpus_to_hf.hexa
        │           (editor highlight)         → HF datasets mirror
        └─────── profile binds field semantics (spec/profiles/*) ──────┘
                 grammar stays pure (spec/kosmos.md)
```

- **Input** — a `.kosmos` manifest: exactly one top-level entry (`@anchor` XOR
  `@corpus`), a placement triple (`coord`/`lane`/`radius`), zero+ `@payload`
  channels (inline · ref+sha256 · pending).
- **Processing** — the hexa-native LSP validates spec conformance; a profile
  resolves abstract fields to domain semantics; encoders project each payload to
  the coordinate space.
- **Output** — verified cross-modal placement; optionally a `@corpus` exported to
  a Hugging Face dataset mirror via the HF tool.

## Governance / verify

Governance invariants (SSOT: `CLAUDE.md` / `project.tape` `@D` entries):

- **`k_spec_ssot`** — `spec/kosmos.md` is the single grammar SSOT; a profile binds
  field semantics only, never grammar.
- **`k_orthogonal`** — placement ⊥ payload; a `coord` is modality-independent.
- **`k_cross_modal`** — every materialized payload lands within `radius` of `coord`;
  un-materialized channels use `:= pending "<reason>"`.
- **`k_line_oriented`** — strict tape v1.2 superset; exactly one top-level entry per
  file; one entry per line (grep-friendly).
- **`k_payload_forms`** — exactly three payload forms (inline · ref+sha256 · pending).
- **`k_hexa_native`** — tooling (parser · emitter · anchor · LSP) is authored in
  hexa-lang; `hexa check` clean.

Verify:

- `bin/kosmos-lsp --check FILE` — one-shot hexa-native lint (exit 1 on any error).
- `lsp/PARITY_VERIFY.md` — `.hexa` ↔ `.py` byte-parity record.
- `cd tree-sitter-kosmos && tree-sitter parse examples/*.kosmos` — 0 ERROR.
- Harness gates — `harness lint` (staged-L0 + changelog freshness), `harness docs check`
  (single-doc discipline · root scope), protected branches (`main`/`master`).
