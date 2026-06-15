# kosmos

`kosmos` is a **multimodal knowledge-anchor manifest format** — sister to `tape` / `n6` / `hxc` / `n12`. A `.kosmos` file pins one knowledge anchor (a point/basin in an abstract placement space) in two orthogonal layers: a **modality-independent placement coordinate** (`coord`/`lane`/`radius`/`tier`/`tags`) and zero+ **modality-specific sensory payloads** (`@payload text|image|audio|video|…`) that all flow into that one placement. The grammar is a strict tape v1.2 superset; profiles bind field semantics, never grammar.

## Structure

```
kosmos/
├─ spec/                  — grammar SSOT + profiles (the format definition)
│  ├─ kosmos.md           — canonical versioned grammar (kosmos/2.1) — grammar SSOT
│  ├─ limen.md            — .limen packed-shard binary container spec
│  └─ profiles/           — field-semantics bindings (anima-consciousness-carving, anima-emergence-trace)
├─ lsp/                   — editor tooling
│  ├─ kosmos_lsp.hexa     — canonical hexa-native linter (k_hexa_native)
│  ├─ kosmos_lsp.py       — deprecated stdio JSON-RPC server (byte-parity)
│  └─ PARITY_VERIFY.md    — .hexa ↔ .py parity record
├─ tree-sitter-kosmos/    — tree-sitter grammar (Neovim · Helix · Zed · Emacs)
├─ impl/                  — reference codecs (limen.hexa + roundtrip test)
├─ tool/                  — corpus_to_hf.hexa — @corpus → HF datasets export
├─ bin/kosmos-lsp         — LSP entrypoint (--check one-shot lint)
├─ examples/              — worked .kosmos files (text · multimodal · corpus · anima)
├─ anchors/               — anchor instances
├─ docs/                  — README translations (zh · ru · ja · ko) + hf_export guide
├─ ARCHITECTURE.md        — architecture SSOT (update-in-place)
├─ CHANGELOG.md           — append-only change log
├─ CLAUDE.md              — governance SSOT (@D invariants, markdown)
└─ .harness-engine/       — dancinlab/harness submodule (AI coding harness)
```

## Governance

This file is the single markdown governance SSOT (folded in from the retired `project.tape`). The governance invariants:

- **k_spec_ssot** — `spec/kosmos.md` is the single grammar SSOT; a profile binds field semantics only, never grammar.
- **k_orthogonal** — placement ⊥ payload; a `coord` is modality-independent (exists with zero channels).
- **k_cross_modal** — every materialized payload lands within `radius` of `coord`; un-materialized channels use `:= pending "<reason>"`.
- **k_line_oriented** — strict tape v1.2 superset; exactly one top-level entry per file; one entry per line (grep-friendly).
- **k_payload_forms** — exactly three payload forms: inline · ref+sha256 · pending.
- **k_hexa_native** — tooling (parser · emitter · anchor · LSP) is hexa-native; `hexa check` clean.

Architecture is documented once in `ARCHITECTURE.md` (overwrite in place); history goes to `CHANGELOG.md` (append only). Keep new docs out of the root — use `scripts/scratch/` for temporary notes.

## Harness

This repo runs the **dancinlab/harness** (hardcore profile) via the `.harness-engine` submodule. Hooks in `.claude/settings.json` delegate to it (guarded — no-op when the binary is absent). It enforces single-doc discipline, changelog freshness on code changes, L0 lockdown reminders, and protected branches (`main`/`master`).

Run the engine:

```bash
bash .harness-engine/bin/harness <cmd>
```

### Quick reference

| Command | Purpose |
|---|---|
| `harness lint` | staged-L0 + changelog freshness + convergence checks |
| `harness docs check` | single-doc discipline (ARCHITECTURE SSOT + quickref · root scope) |
| `harness verify` | run configured verification commands |
| `harness audit` | 6-axis self-scorecard |
| `harness gc` | broken markdown links in guides |
| `bin/kosmos-lsp --check FILE` | one-shot hexa-native `.kosmos` lint |
