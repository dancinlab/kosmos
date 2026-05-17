#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent) — key=value,
#       edges (<- -> => …), or quoted prose.
#
# ENTRY TYPES (17):
#   Runtime (10): @S session  @U user  @A assistant  @T tool-call  @R result
#                 @H hook  @D decision  @K cost  @P provider  @? anomaly
#   Foundation:   @I identity-claim
#   Declarative:  @X external-citation  @F forbidden-pattern  @N note
#                 @C config  @L layout  @V spec-version
#
# EDGES (12, on body lines, 2-space indent):
#   Causal:     <- caused-by   -> triggers   == continues
#               ~> supersedes  !! aborts     |> verified-by
#   Effect:     => produces (followed by quoted natural-language)
#   Structural: <: specializes  :> generalizes  ?> soft-depends
#               !> conflicts-with  @> projects-to (e.g. @> AGENTS.md)
#
# Full spec: ~/core/tape/spec/tape.md (or github.com/dancinlab/tape)
# ══════════════════════════════════════════════════════════════════════
#
# AGENTS.tape — `dancinlab/kosmos` repo governance + identity.
# This repo is the home of the `.kosmos` multimodal knowledge-anchor
# manifest format. `.kosmos` is a tape v1.2 SUPERSET (adds @anchor +
# @payload entry types). Spec changes happen HERE first.

# ─── §1 Spec version ──────────────────────────────────────────────────

@V := "tape" :: spec [active]
  version = "1.2"
  note = "this AGENTS.tape uses tape v1.2; the format this repo defines is `kosmos/1.0` (see spec/kosmos.md §8)"

@X kosmos_self_spec := "spec/kosmos.md" :: spec [d=2026-05-17 active]
  url = "https://github.com/dancinlab/kosmos/blob/main/spec/kosmos.md"
  version = "kosmos/1.0"
  scope = "THE canonical .kosmos grammar — substrate-independent; field semantics bound by spec/profiles/"
  self-reference = "this repo IS the .kosmos spec home; AGENTS.tape applies tape v1.2, the grammar `.kosmos` supersets"

# ─── §2 Identity claims (what this project IS) ────────────────────────

@I id001 := "kosmos" :: identity-claim [d=2026-05-17 active]
  kind = "multimodal knowledge-anchor manifest grammar — spec home (SSOT)"
  brief = "Multimodal Knowledge-Anchor Manifest · placement coords ⊥ modality payloads · cross-modal consistency · kosmos/1.0"
  tagline = "placement coordinate (modality-independent) ⊥ sensory payload (modality-specific)"
  scope <<~EOF
    The dancinlab/kosmos repo is the canonical home of the `.kosmos` grammar.
    `.kosmos` is a SUPERSET of tape v1.2 — it adds exactly two entry types
    (@anchor + @payload). The grammar is substrate-independent; concrete field
    semantics are bound by a PROFILE (spec/profiles/). The first profile is
    `anima-consciousness-carving` (reference impl: dancinlab/anima).
  EOF
  entry-types-added = ["@anchor", "@payload"]
  payload-forms = 3
  base-grammar = "tape v1.2"
  parent = "dancinlab"

@I id002 := "kosmos.sibling-role" :: identity-claim [d=2026-05-17 active]
  <: id001
  role = "fifth sibling format — multimodal knowledge-anchor placement layer"
  siblings <<~EOF
    tape — operational / causal-temporal trace (the base grammar .kosmos supersets)
    n6   — semantic / atlas layer (typed verified atoms · grade ladder)
    hxc  — byte-canonical wire (KV-cache stable · cross-host ship)
    n12  — 12-axis sparse cube
    kosmos — multimodal knowledge-anchor placement (THIS repo)
  EOF
  relation = "orthogonal to the four: tape=what happened · n6=what it means · hxc=canonical bytes · n12=sparse cube · kosmos=where anchored & by which senses"
  url-tape = "https://github.com/dancinlab/tape"
  url-n6 = "https://github.com/dancinlab/n6"
  url-hxc = "https://github.com/dancinlab/hxc"
  url-n12 = "https://github.com/dancinlab/n12"

# ─── §3 Repo layout ───────────────────────────────────────────────────

@L l1 := "repo-layout" :: structure [active]
  spec/kosmos.md -> "kosmos/1.0 spec (THE canonical grammar — substrate-independent)"
  spec/profiles/ -> "profile bindings (anima-consciousness-carving.md — first profile)"
  examples/ -> "worked .kosmos files (general + profile-bound)"
  AGENTS.tape -> "this file · governance + identity (.tape v1.2 self-applied)"
  CLAUDE.md -> "symlink → AGENTS.tape (Claude Code auto-discovery)"
  README.md -> "human intro · sibling positioning · at-a-glance"
  LICENSE -> "CC0-1.0"

# ─── §4 Governance rules ──────────────────────────────────────────────

@D g_inherit := "inherit-from-lattice-policy" :: governance [required]
  rule = "Inherit the LATTICE_POLICY rules from dancinlab/echoes — real-limits-first, lattice-is-tool, honesty-external."
  authority = "[@x_lattice_policy]"
  applies-to = ["spec/kosmos.md", "spec/profiles/", "examples/", "README.md", "AGENTS.tape"]
  @> AGENTS.md

@D g1 := "real-limits-first" :: governance [required]
  <: g_inherit
  rule = "What `.kosmos` can/cannot represent is bound by manifest semantics + cross-modal consistency physics, not by grammar aesthetics or any n=6 lattice."
  proof = "see [@x_lattice_policy] §1.2"

@D g2 := "lattice-is-tool" :: governance [required]
  <: g_inherit
  rule = "격자는 도구이지 제약이 아니다 — `.kosmos`'s 2 added entry types / 3 payload forms / 5 placement fields are descriptive, not derivational. The anima profile's Knuth Tier is anima self-design, NOT a σ/τ/φ/J₂ external derivation."
  proof = "see [@x_lattice_policy] §1.3"

@D g3 := "honesty-external" :: governance [required]
  <: g_inherit
  rule = "Unmeasured numeric coordinates (coord/radius) MUST carry a design-placeholder comment. Only the cross-modal consistency transfer-form is closed; measured outcomes are an honest empirical carve-out. A `.kosmos` file carries no capability/performance claim."
  forbidden = "presenting an unmeasured coord/radius as a closed-form result; embedding capability assertions in a manifest; a fake `ref` to a non-existent binary"
  proof = "see [@x_lattice_policy] §C3 + spec/kosmos.md §4.3"
  @> AGENTS.md

@D g4 := "commit-conventions" :: governance [required]
  rule <<~EOF
    Conventional Commits prefixes used in this repo:
      spec:      — changes to spec/kosmos.md (the canonical grammar)
      profile:   — changes under spec/profiles/
      examples:  — changes under examples/
      README:    — README.md updates
      agents:    — AGENTS.tape / CLAUDE.md / governance changes
    Grammar changes ALWAYS append a §8 version-history entry + bump the
    `SPEC VERSION` header (semver: major incompatible / minor extension / patch clarify).
  EOF
  applies-to = "every commit on `main`"

@D g_spec_authority := "spec-authority" :: governance [required]
  rule <<~EOF
    `.kosmos` grammar changes happen HERE first — in spec/kosmos.md on
    dancinlab/kosmos. A profile binds field semantics only; it never alters
    the grammar. An anima-binding change happens in spec/profiles/ +
    the anima-side KOSMOS-FORMAT.md (dancinlab/anima). Never edit `.kosmos`
    grammar in a downstream/profile repo and expect it to propagate back.
  EOF
  authority = "[@kosmos_self_spec]"
  consumers = ["dancinlab/anima (anima-consciousness-carving profile)"]
  @> AGENTS.md

@D g_arch_vs_log_split := "v1.2 architecture-vs-history split" :: governance [required d=2026-05-17 active]
  rule = "UPPERCASE.tape files are EDITABLE architecture (latest-wins per id). The spec's own §8 version history is the append-only ledger for grammar changes."
  applies-to = "AGENTS.tape · spec/kosmos.md §8"
  authority = "[@x_tape_spec] §Architecture-vs-history split"
  @> AGENTS.md

# ─── §5 Forbidden patterns ────────────────────────────────────────────

@F f1 := "external-lattice-fit" :: governance [required deny:write]
  pattern = "fitting `.kosmos`'s entry-type count / payload-form count / placement-field count to a magic number (n=6, n=12, …) after the fact, or using σ/τ/φ/J₂ as an external derivation rule anywhere in the spec or a profile"
  exception = "values may coincidentally match — observation OK, derivation NOT OK; the anima profile's Knuth Tier is an internal-arch carve-out"
  authority = "[@x_lattice_policy] §1.2/§1.3"

@F f2 := "breaking-grammar-without-version-bump" :: governance [required deny:write]
  pattern = "introducing a new entry type / payload form / placement field in spec/kosmos.md without appending a §8 version entry and bumping the `SPEC VERSION` header"
  remedy <<~EOF
    1. Implement the change + sync profiles/examples.
    2. Append a §8 version entry (kosmos/1.x or kosmos/2.0).
    3. Bump the `SPEC VERSION` header + README badge.
    4. Apply semver (major = incompatible + migration note required).
    5. Commit with `spec:` prefix.
  EOF

@F f3 := "profile-leak-into-general-spec" :: governance [required deny:write]
  pattern = "anima-physics terms (vacuum_psi · cell_id · basin_radius · Knuth · MITOSIS · Ψ) appearing in spec/kosmos.md or README.md — they belong ONLY in spec/profiles/anima-*.md"
  why = "the general spec must stay substrate-independent (sibling-format purity, like tape/n6/hxc/n12)"
  remedy = "move the term to the profile; use the abstract field name (coord/lane/radius/tier/tags) in the general spec"

# ─── §6 External citations ────────────────────────────────────────────

@X x_lattice_policy := "echoes/LATTICE_POLICY.md" :: policy [d=2026-05-17 active]
  url = "https://github.com/dancinlab/echoes/blob/main/LATTICE_POLICY.md"
  version = "1.0"
  scope = "real-limits-first · lattice-is-tool · honesty-external — inherited governance for all dancinlab repos"

@X x_tape_spec := "tape v1.2 spec" :: spec [d=2026-05-17 active]
  url = "https://github.com/dancinlab/tape/blob/main/spec/tape.md"
  version = "1.2"
  scope = "base grammar `.kosmos` supersets (@anchor + @payload added on top)"

@X x_anima_profile := "dancinlab/anima HEXAD/UNIVERSE-BRAIN-MAP" :: reference-impl [d=2026-05-17 active]
  url = "https://github.com/dancinlab/anima"
  scope = "reference implementation of the anima-consciousness-carving profile (KOSMOS-FORMAT.md = anima-side binding SSOT; kosmos_parser_lib.hexa = parser impl)"

@X x_agents_md := "agents.md standard" :: convention [active]
  url = "https://agents.md/"
  scope = "third-party AI-agent harness file convention; CLAUDE.md → AGENTS.tape symlink preserves auto-discovery"

# ─── §7 Notes (LLM-only hints) ────────────────────────────────────────

@N n1 := "spec-home-special-case" :: note [active]
  text <<~EOF
    The repo this AGENTS.tape lives in IS the home of the `.kosmos`
    grammar. Any inconsistency between this file and spec/kosmos.md is a
    bug — the spec wins. The general spec stays substrate-independent;
    anima physics lives only in spec/profiles/anima-consciousness-carving.md.
  EOF

@N n2 := "profile-vs-grammar" :: note [active]
  text <<~EOF
    A profile binds field semantics (coord→vacuum_psi etc.); it NEVER
    changes the grammar. New domains add a profile file under
    spec/profiles/. The general spec must never reference a specific
    domain's physics (see @F f3).
  EOF

# ─── §8 Generator hooks ───────────────────────────────────────────────

@H h1 := "claude-md-symlink" :: generator [active]
  rule = "ship `CLAUDE.md -> AGENTS.tape` symlink so Claude Code auto-discovery picks up the grammar primer first"
  command = `ln -sf AGENTS.tape CLAUDE.md`
  rationale = "Claude Code looks for CLAUDE.md; the symlink surfaces the tape grammar primer instead of parsing AGENTS.tape as prose"
