# kosmos Constitution

## Core Principles

### I. Format-First — Substrate-Independent (NON-NEGOTIABLE)
`spec/kosmos.md` is the canonical, versioned grammar of the `.kosmos` file format. The core spec defines placement coordinates and sensory payloads abstractly. No substrate (no runtime, no ML model, no language, no profile-specific semantics) appears in the core spec body — those live in `spec/profiles/<name>.md`.

### II. Cross-Modal Consistency (NON-NEGOTIABLE)
Every `@payload` declared in a `.kosmos` file, once passed through its modality encoder, MUST land within `radius` of the anchor's `coord`. This is the binding contract of the format — anchoring a concept from multiple sensory directions only counts as one anchor when the placements agree. Implementations that ship without this check do not conform.

### III. Profile-Bound Semantics
The generic spec is substrate-independent; concrete field semantics (what `coord` space means, what `lane` partitions, what `tier` ordinals encode, what `tags` taxonomies exist) live in `spec/profiles/<name>.md`. Adding or amending a profile does NOT modify the core spec. The first profile is `anima-consciousness-carving`; future profiles attach as peers.

### IV. Sister Format ⊥ tape / n6 / hxc / n12
kosmos is the fifth sibling format. The five carry orthogonal axes: `tape` = what happened (causal-temporal trace) · `n6` = what it means (semantic atlas) · `hxc` = the canonical bytes (wire) · `n12` = the sparse cube projection · **`kosmos`** = where it is anchored & by which senses. kosmos consumes tape v1.2 syntax (`@<type> <id> := …` + 2-space-indent body, grade-tag conventions) as a superset, and adds exactly two new entry types: `@anchor` and `@payload`.

### V. Line-Oriented · Grep-Friendly
`.kosmos` files are plain UTF-8 text, line-oriented, comment-aware (`#` line prefix). No binary forms, no required tooling to read. A `grep "@anchor "` over a tree of `.kosmos` files MUST list every anchor.

### VI. PR-Only Spec Mutation
Spec changes land via PR that (a) appends a new version entry to `spec/kosmos.md` §8 with a dated note, and (b) updates the `SPEC VERSION` header. Semver — MAJOR = incompatible (migration note required) · MINOR = backward-compatible extension · PATCH = clarification or typo. Past version entries are append-only; in-place edits beyond PATCH wording are forbidden.

### VII. Open Spec — CC0
The kosmos spec is CC0-1.0 (public domain). Anyone may implement, fork, or profile-bind without royalty or attribution. The reference implementation and the first profile binding live at `dancinlab/anima` → `HEXAD/KOSMOS.md` + `HEXAD/UNIVERSE-BRAIN-MAP/*`; that pointer is non-exclusive — additional reference impls are welcome.

## Repository Layout

```
kosmos/
├── spec/
│   ├── kosmos.md                  # canonical spec (SSOT — substrate-independent)
│   └── profiles/                  # profile bindings
│       └── anima-consciousness-carving.md
├── docs/                          # multilingual READMEs (zh / ru / ja / ko)
├── examples/                      # sample .kosmos files
├── bin/                           # reference tooling
├── lsp/                           # language server scaffold
├── tree-sitter-kosmos/            # tree-sitter grammar
└── .specify/                      # Spec Kit pipeline artifacts (this constitution lives here)
```

## Development Workflow

1. **Spec change.** PR adds an entry to `spec/kosmos.md` §8 (version history) and bumps the `SPEC VERSION` header per semver. The change landing in a release branch is the canonical moment.
2. **Profile add / amend.** PR creates or edits `spec/profiles/<name>.md` only — never touches the core spec.
3. **Reference impl.** The anima reference implementation (`dancinlab/anima` `HEXAD/KOSMOS.md` + `UNIVERSE-BRAIN-MAP/*`) tracks the spec — when the spec ships a version, the anima hub updates its pointer. Other reference impls follow the same pattern.
4. **Multilingual READMEs.** English README is authoritative; the four language mirrors (`docs/README.{zh,ru,ja,ko}.md`) update in the same PR for material changes.
5. **Examples.** New entry types or fields land with at least one example under `examples/`.

## Governance

- This constitution governs kosmos repo-local concerns (spec discipline, profile separation, sibling-format orthogonality, multilingual sync).
- Spec authority for the core format = `spec/kosmos.md` SPEC VERSION header + §8 history. Spec authority for profile semantics = the project that owns the profile (e.g., `dancinlab/anima` for `anima-consciousness-carving`).
- Amendments to this constitution land via a PR that updates this file and bumps semver (MAJOR = principle removal/redefinition · MINOR = new principle/section · PATCH = wording).
- Complexity must be justified inline. Default = simpler. Spec-level complexity (new entry types, new field shapes) requires a MAJOR or MINOR bump of the format spec — not a PATCH.

**Version**: 1.0.0 | **Ratified**: 2026-05-21 | **Last Amended**: 2026-05-21
