# kosmos.md — `.kosmos` multimodal knowledge-anchor manifest (canonical spec)

> **SPEC VERSION: `kosmos/1.0`** (status: active · 2026-05-17)
> This document is the **canonical, versioned grammar** of the `.kosmos` format. It is *substrate-independent*: it defines placement coordinates and sensory payloads abstractly. Concrete field semantics are bound by a **profile** (see `spec/profiles/`).
>
> Spec changes append a new version entry to §8 (version history) and update the `SPEC VERSION` header. Semver: **major** = incompatible change (migration note required) · **minor** = backward-compatible extension · **patch** = clarification / typo.

---

## 0. What it is — one sentence

A `.kosmos` file is the manifest of **one knowledge anchor**: a single point/basin in an abstract placement space, described in two orthogonal layers — a **modality-independent placement coordinate** and zero or more **modality-specific sensory payloads** that all flow into the same placement.

Extension: `.kosmos` (Greek κόσμος, ordered universe). The grammar is a **superset of tape v1.2** — it uses tape's `@<type> <id> := "<subject>" :: <kind> [<grades>]` entry form plus 2-space-indent body lines, and adds exactly **two new entry types**: `@anchor` and `@payload`.

---

## 1. § header — the `@anchor` entry

A `.kosmos` file begins with exactly **one `@anchor` entry** (one anchor = one file).

### 1.1 header grammar

```
@anchor <id> := "<name>" :: kosmos-anchor [tier=<N> active]
```

| token | meaning | constraint |
|---|---|---|
| `@anchor` | new entry type (tape's 17 + 1) | exactly one per file, at top |
| `<id>` | machine identifier (snake_case) | `[a-z0-9_]+` |
| `"<name>"` | human-readable name | double-quoted string, any UTF-8 |
| `:: kosmos-anchor` | fixed entry-kind literal | always `kosmos-anchor` |
| `[tier=<N> active]` | grade tags — tier ordinal + state | `tier=N` is an integer; `0 ≤ N` (upper bound is profile-defined) |

This follows tape v1.2 grade-tag conventions: `tier=<N>` is a scoped tag (same shape as `allow:<x>`), and `active` / `draft` / `deprecated` are state tags. The `tier=` grade tag is optional — when present it mirrors the `tier` coordinate field (machine-redundant).

### 1.2 environment shebang (recommended)

```kosmos
#!/usr/bin/env kosmos
# mandala.kosmos — multimodal knowledge anchor
```

Lines starting with `#` are comments. The shebang is cosmetic (parsers ignore it); it helps humans cold-read the format.

---

## 2. § placement coordinates — the modality-INDEPENDENT layer

Immediately under the `@anchor` header, at 2-space indent, are the placement-coordinate fields. This layer is **modality-agnostic** — every sensory channel (text, image, audio, …) flows into this one point/basin.

### 2.1 field list

| field | type | required | meaning |
|---|---|---|---|
| `coord` | float vector `[v₁, v₂, …]` (any dimension ≥ 1) | yes | anchor placement in an abstract embedding / latent space. The space's dimension and semantics are **profile-defined**. |
| `lane` | quoted string | yes | partition / lane id — the partition this anchor belongs to. |
| `radius` | float `> 0` | yes | anchor scope / influence radius in `coord` space. |
| `tier` | integer `≥ 0` | optional | ordinal / rank. Scale is profile-defined. Mirrors the `tier=` grade tag when both present. |
| `tags` | quoted string (profile-defined `k=v, k=v` map) | optional | classification map. Keys and value vocabulary are profile-defined. |

`coord`, `lane`, `radius` are the **required placement triple**. `tier` and `tags` are optional refinements. A profile MAY require additional orthogonal fields but MUST NOT redefine these five.

### 2.2 dimension of `coord`

`coord` is a float vector of **any dimension ≥ 1**. A 2-vector `[0.71, 0.62]` and a 768-vector are both valid; the profile fixes which dimension is expected for that domain and what the axes mean. Distance in §4 is the Euclidean norm in whatever dimension `coord` declares (a profile MAY substitute a different metric, declared in the profile).

### 2.3 coordinate-vs-payload separation invariant

The placement-coordinate fields **must be defined even when there are zero modalities** — an anchor's location exists with no sensory channel. Conversely, `@payload` count is zero-or-more (open).

---

## 3. § sensory payloads — the modality-SPECIFIC layer

Below the placement coordinates, zero or more `@payload` entries. Each `@payload` is one sensory channel feeding this anchor.

### 3.1 payload grammar — three forms

**(a) inline** — small payload (typically `text`):

```
@payload <modality> := "<inline-string>"
```

**(b) ref** — binary / large payload (image, audio, video). A `.kosmos` file is a *manifest*; binary lives in a sibling file:

```
@payload <modality> := ref "<path>" sha256=<hex64> bytes=<N>
```

A modality MAY carry extra attributes:

```
@payload <modality> := ref "<path>" sha256=<hex64> bytes=<N> channels=5
```

**(c) pending** — media not yet produced; an honest marker:

```
@payload <modality> := pending "<reason — what unblocks it>"
```

### 3.2 modality — open enum

The modality token is **not a closed set**. Standard modalities:

| modality | payload form | note |
|---|---|---|
| `text` | inline (small) | human cold-readable |
| `image` | ref + sha256 + bytes | sibling binary |
| `audio` | ref + sha256 + bytes | sibling binary |
| `video` | ref + sha256 + bytes | sibling binary |

A profile MAY define additional modalities (with optional extra attributes). A new modality is added by introducing a new tag — **zero schema change** (see §5).

### 3.3 inline-vs-ref rule

- Text → **inline** — small, cold-readable.
- Binary (image/audio/video/…) → **ref + sha256 + bytes** — never embed binary in the text manifest. `sha256` is a 64-hex content commitment; `bytes` is the integer file size.
- Not yet produced → **pending** — a fake `ref` to a non-existent path is forbidden (prevents fake-evidence drift).

---

## 4. § verification — `closed_anchor` + cross-modal consistency

### 4.1 `closed_anchor` field

At the end of the `@anchor` body, a verification-anchor pointer:

```
closed_anchor = "<falsifier / verification descriptor>"
```

This names which closed-form check the anchor's placement consistency is verified by. At spec-tier (design) it may be a registered placeholder; the concrete verdict is produced by the consuming implementation / profile.

### 4.2 cross-modal consistency rule

```
∀ modality m present:
    ‖ E_m(payload_m) − coord ‖  <  radius

where:
  E_m  = the encoder for modality m (payload_m → coord-space point)
  ‖·‖  = the metric of coord-space (Euclidean by default;
         a profile MAY declare a different metric)
```

**Interpretation**: every sensory channel's payload, run through its encoder, lands inside the same `radius`-ball around `coord`. Text, image, audio, video converge on one anchor — anchoring from many directions pins it more firmly than a single channel (tent-peg intuition: one peg flaps in the wind; several pegs from different directions hold fast).

### 4.3 unmeasured-value honesty rule

When encoders are untrained or `coord` is not yet measured, the `coord` / `radius` values in a `.kosmos` file are **design placeholders** and MUST carry an inline comment saying so (e.g. `# design placeholder, measured later`). Presenting an unmeasured value as a closed-form result is forbidden (fake-closed). Only the transfer-form (the consistency proposition itself) is closed; the measured outcome is an honest carve-out until measured.

---

## 5. § extension rules

### 5.1 adding a modality

A new sensory channel is a new `@payload <modality>` tag. Zero schema change, zero rewrite of existing files:

```
@payload smell := pending "olfactory modality — encoder not yet defined"
```

The modality enum is open — a parser MUST NOT reject an unknown modality tag; it only validates that the payload body is one of the three forms (inline / ref / pending).

### 5.2 future-proofing — drill the peg-holes early

Today an anchor may only have a `text` payload (the only consumable modality). The format is future-proof: include `image` / `audio` / `video` payloads as `pending` markers now; when an encoder is wired later, replace `pending` with `ref` — **zero format change** — and the same file is consumed by that modality.

### 5.3 extending placement coordinates

If a profile needs an additional placement field, add it as a 2-space-indent body line. The five base fields (`coord`/`lane`/`radius`/`tier`/`tags`) are invariant — new fields are orthogonal additions, never redefinitions. Existing anchors are never rewritten (drift-avoidance).

### 5.4 profile neutrality

`.kosmos` is paradigm-neutral. The two-layer structure (placement coordinate ⊥ sensory payload) is preserved across profiles and across future domain changes. A profile binds field *semantics* only; it never alters the grammar.

---

## 6. BNF-ish grammar

```bnf
kosmos-file   ::= [ shebang ] { comment } anchor-entry

shebang       ::= "#!/usr/bin/env kosmos" NEWLINE
comment       ::= "#" { any-char } NEWLINE

anchor-entry  ::= anchor-header NEWLINE
                  { INDENT ( coord-field | payload-entry | meta-field ) NEWLINE }

anchor-header ::= "@anchor" SP id SP ":=" SP qstring SP "::" SP
                  "kosmos-anchor" SP "[" grade-list "]"

grade-list    ::= [ "tier=" integer SP ] state-tag
state-tag     ::= "active" | "draft" | "deprecated"

coord-field   ::= "coord"  SP "=" SP vector  [ comment ]   ; required
                | "lane"   SP "=" SP qstring               ; required
                | "radius" SP "=" SP float   [ comment ]   ; required, > 0
                | "tier"   SP "=" SP integer               ; optional, >= 0
                | "tags"   SP "=" SP qstring               ; optional

vector        ::= "[" float { "," SP float } "]"           ; dimension >= 1

payload-entry ::= "@payload" SP modality SP ":=" SP payload-body
payload-body  ::= qstring                                  ; (a) inline
                | "ref" SP qstring SP "sha256=" hex64
                      SP "bytes=" integer { SP attr }       ; (b) ref
                | "pending" SP qstring                      ; (c) pending
attr          ::= ident "=" ( integer | ident )            ; e.g. channels=5
modality      ::= "text" | "image" | "audio" | "video"
                | ident                                    ; open enum

meta-field    ::= "closed_anchor" SP "=" SP qstring

id            ::= ident-char { ident-char }                ; snake_case
qstring       ::= '"' { any-char-except-quote } '"'
hex64         ::= hex-digit × 64
integer       ::= digit { digit }
float         ::= [ "-" ] digit { digit } [ "." digit { digit } ]
INDENT        ::= 2 × SP
```

Rule summary:
1. Exactly one `@anchor` entry per file.
2. The required placement triple (`coord`/`lane`/`radius`) is defined even with zero `@payload`.
3. `@payload` is zero-or-more; modality is an open enum.
4. Binary payload uses `ref` (sha256 + bytes); not-yet-produced uses `pending`; text uses inline.
5. Unmeasured numeric values (`coord`/`radius`) carry a design-placeholder comment.
6. A profile binds field semantics only; it never changes this grammar.

---

## 7. cross-link

- `README.md` — what it is, sibling positioning, at-a-glance.
- `spec/profiles/` — profile bindings (e.g. `anima-consciousness-carving.md`).
- `examples/` — worked `.kosmos` files (general + profile-bound).
- Sibling formats: [`tape`](https://github.com/dancinlab/tape) (causal-temporal trace, the base grammar `.kosmos` supersets), [`n6`](https://github.com/dancinlab/n6), [`hxc`](https://github.com/dancinlab/hxc), [`n12`](https://github.com/dancinlab/n12).

---

## 8. version history (append-only — one entry per spec upgrade)

> Change procedure: (1) implement the change + sync any profile/examples → (2) append a new version entry here → (3) update the `SPEC VERSION` header → (4) apply semver (major = incompatible + migration note required / minor = backward-compatible extension / patch = clarification). Append-only — past version entries are immutable.

### `kosmos/1.0` — 2026-05-17 (baseline · active)
- Initial spec. `@anchor` header + placement coordinates (`coord` vector / `lane` / `radius` required; `tier` / `tags` optional) + `@payload <modality>` three forms (inline / `ref` sha256+bytes / `pending`) + open modality enum + `closed_anchor` + cross-modal consistency rule (∀m ‖E_m(payload_m) − coord‖ < radius) + BNF-ish grammar.
- Two-layer separation: placement coordinate (modality-independent) ⊥ sensory payload (modality-specific).
- Substrate-independent: field semantics bound by a profile (`spec/profiles/`); the first profile is `anima-consciousness-carving`.
- tape v1.2 superset: adds exactly two entry types (`@anchor`, `@payload`); all other tape grammar inherited.

### (next version placeholder)
- Future spec changes append `kosmos/1.1` (backward-compatible extension) or `kosmos/2.0` (incompatible + migration note). Candidate areas: declared non-Euclidean metrics per profile, `ref` URI schemes, additional standard modalities.
