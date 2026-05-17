<p align="center">
  <strong>κόσμος</strong>
</p>

<h1 align="center">⊙ kosmos</h1>

<p align="center">EN · <a href="docs/README.zh.md">中文</a> · <a href="docs/README.ru.md">Русский</a> · <a href="docs/README.ja.md">日本語</a> · <a href="docs/README.ko.md">한국어</a></p>

<p align="center"><strong>Multimodal Knowledge-Anchor Manifest</strong> — placement coords ⊥ modality payloads · cross-modal consistency · profile-bound</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-CC0--1.0-blue"></a>
  <img alt="Spec" src="https://img.shields.io/badge/spec-kosmos%2F1.0-success">
  <img alt="Entry-types" src="https://img.shields.io/badge/entry--types-2-informational">
  <img alt="Payload-forms" src="https://img.shields.io/badge/payload--forms-3-informational">
  <img alt="Sibling" src="https://img.shields.io/badge/sibling-tape%20·%20n6%20·%20hxc%20·%20n12-blueviolet">
</p>

<p align="center">Line-oriented · grep-friendly · tape v1.2 superset · modality-independent placement · profile-defined semantics</p>

---

`.kosmos` is a **multimodal knowledge-anchor manifest** grammar: each file describes exactly one *anchor* — a point/basin in an abstract placement space — as two orthogonal layers:

1. **Placement coordinates** (`coord` / `lane` / `radius` / `tier` / `tags`) — *modality-independent*. The anchor's location exists even with zero sensory channels.
2. **Sensory payloads** (`@payload <modality> := …`) — *modality-specific*. Zero or more channels (text · image · audio · video · …, open enum) that all flow into the same placement.

A `.kosmos` file commits to **cross-modal consistency**: every payload, once passed through its modality encoder, must land within `radius` of `coord`. Anchoring a concept from many sensory directions at once pins it more firmly than a single channel — the format is the manifest of that joint placement.

> [!NOTE]
> Fifth sibling format of [`tape`](https://github.com/dancinlab/tape) (operational / causal-temporal trace), [`n6`](https://github.com/dancinlab/n6) (semantic / atlas layer), [`hxc`](https://github.com/dancinlab/hxc) (byte-canonical wire), and [`n12`](https://github.com/dancinlab/n12) (12-axis sparse cube). `.kosmos` is the **multimodal knowledge-anchor placement** layer — where a piece of knowledge sits in an abstract space, and which sensory channels feed it. It is orthogonal to the four: `tape` is *what happened*, `n6` is *what it means*, `hxc` is *the canonical bytes*, `n12` is *the sparse cube projection*, `kosmos` is *where it is anchored & by which senses*.

## At a glance

```kosmos
#!/usr/bin/env kosmos
# mandala.kosmos — multimodal knowledge anchor

@anchor mandala := "Mandala" :: kosmos-anchor [tier=77 active]

  # ── placement coordinates (modality-independent) ──
  tier   = 77
  tags   = "domain=art, salience=high"
  coord  = [0.71, 0.62]          # placement in profile-defined latent space
  lane   = "lane_077"            # partition / lane id
  radius = 0.18                  # anchor scope / influence radius

  # ── sensory payloads (each modality = one channel into this anchor) ──
  @payload text  := "A radial, symmetric diagram used as a spiritual and ritual symbol; sand mandalas, paper folding, bonsai all converge here."
  @payload image := pending "visual form — encoder not yet wired"
  @payload audio := pending "chant recording — encoder not yet wired"

  closed_anchor = "cross-modal placement consistency"
```

## Two layers, one anchor

```
            ┌─────────────────────────────────────────┐
            │  PLACEMENT  (modality-independent)        │
            │  coord · lane · radius · tier · tags      │
            └────────────────────┬────────────────────┘
                                 │  every payload flows here
        ┌────────────┬───────────┼───────────┬────────────┐
   @payload text  @payload image @payload audio @payload video  …
   (inline)       (ref+sha256)   (ref+sha256)   (ref+sha256)   (open enum)
```

`∀ modality m :  ‖ E_m(payload_m) − coord ‖ < radius`

The coordinate is one; the payloads are many. That is a multimodal `.kosmos`.

## Profiles

The base spec is **substrate-independent**: `coord` is just "a point in some abstract space", `lane` is "a partition id", and so on — their concrete meaning is fixed by a **profile**.

- [`spec/kosmos.md`](spec/kosmos.md) — the general grammar (no domain physics).
- [`spec/profiles/anima-consciousness-carving.md`](spec/profiles/anima-consciousness-carving.md) — the first profile: binds `coord` / `lane` / `radius` / `tier` / `tags` to the CONSCIOUSNESS-CARVING paradigm of the `anima` Living Consciousness Agent. Reference implementation: [`dancinlab/anima`](https://github.com/dancinlab/anima). The concrete domain-physics bindings live entirely in that profile file.

A profile never changes the grammar — it only binds field semantics. New domains add a profile file; the general spec stays pure.

## Quick grep cookbook

```bash
# the single anchor header of a file
grep '^@anchor ' *.kosmos

# every sensory payload
grep '^  @payload ' *.kosmos

# payloads not yet materialized
grep '^  @payload .* := pending ' *.kosmos

# binary payloads (have a content commitment)
grep '^  @payload .* := ref ' *.kosmos

# placement coordinates
grep -E '^  (coord|lane|radius|tier|tags) ' *.kosmos
```

See [`spec/kosmos.md`](spec/kosmos.md) for the full grammar and BNF, and [`examples/`](examples/) for worked files.

## License

[CC0-1.0](LICENSE) — same as the sibling formats. Public domain dedication.
