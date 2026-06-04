# kosmos.md — `.kosmos` multimodal knowledge-anchor manifest (canonical spec)

> **SPEC VERSION: `kosmos/2.1`** (status: active · 2026-06-04)
> This document is the **canonical, versioned grammar** of the `.kosmos` format. It is *substrate-independent*: it defines placement coordinates and sensory payloads abstractly. Concrete field semantics are bound by a **profile** (see `spec/profiles/`).
>
> **kosmos/2.0** adds the `@corpus` collection entry (§5.6) — a `.kosmos` file is now EITHER one anchor (1.x, unchanged) OR one corpus (a dataset = an ordered collection of member anchors). Backward-compatible for single-anchor files; **major** because the top-level "exactly one `@anchor`" invariant is generalised to "exactly one top-level entry (`@anchor` XOR `@corpus`)". Migration note in §8.
> **kosmos/2.1** (§8) is a **grammar-identical** minor that records the four `kosmos/2.0` deferrals landing — the `.limen` packed-shard format + its reference codec, the merkle construction, the HF-dataset export tool, and LSP/tree-sitter `@corpus` recognition. No grammar delta; a 2.0 file is a 2.1 file and vice-versa.
>
> Spec changes append a new version entry to §8 (version history) and update the `SPEC VERSION` header. Semver: **major** = incompatible change (migration note required) · **minor** = backward-compatible extension · **patch** = clarification / typo.

---

## 0. What it is — one sentence

A `.kosmos` file is EITHER the manifest of **one knowledge anchor** — a single point/basin in an abstract placement space, described in two orthogonal layers (a **modality-independent placement coordinate** and zero or more **modality-specific sensory payloads** that all flow into the same placement) — OR (since `kosmos/2.0`, §5.6) one **corpus**: a dataset = an ordered collection of member anchors, itself a meta-anchor (the collection's own placement = the centroid its members carve).

Extension: `.kosmos` (Greek κόσμος, ordered universe). The grammar is a **superset of tape v1.2** — it uses tape's `@<type> <id> := "<subject>" :: <kind> [<grades>]` entry form plus 2-space-indent body lines, and adds **three new entry types**: `@anchor`, `@payload`, and `@corpus` (§5.6, kosmos/2.0).

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
| `profile` | quoted string (profile id) | optional-but-recommended | which profile binds this file's `coord` / `lane` / `radius` / `tier` / `tags` semantics. See §2.4. |

`coord`, `lane`, `radius` are the **required placement triple**. `tier` and `tags` are optional refinements; `profile` is an optional-but-recommended self-identification field (§2.4). A profile MAY require additional orthogonal fields but MUST NOT redefine these six.

### 2.2 dimension of `coord`

`coord` is a float vector of **any dimension ≥ 1**. A 2-vector `[0.71, 0.62]` and a 768-vector are both valid; the profile fixes which dimension is expected for that domain and what the axes mean. Distance in §4 is the Euclidean norm in whatever dimension `coord` declares (a profile MAY substitute a different metric, declared in the profile).

### 2.3 coordinate-vs-payload separation invariant

The placement-coordinate fields **must be defined even when there are zero modalities** — an anchor's location exists with no sensory channel. Conversely, `@payload` count is zero-or-more (open).

### 2.4 profile self-identification — the `profile` field

`coord` is a vector of profile-defined dimension and axis meaning (§2.2): a reader cannot interpret `coord = [0.71, 0.62]` without knowing *which* profile binds it. A `.kosmos` file therefore SHOULD declare its profile **inside the file** rather than relying on external context (directory name, comment, consuming repo):

```
profile = "anima-consciousness-carving"
```

- The `profile` value is a **profile id** — the canonical string a profile under `spec/profiles/` defines for itself (e.g. `anima-consciousness-carving`, declared in `spec/profiles/anima-consciousness-carving.md`).
- `profile` is **optional-but-recommended**. A file MAY omit it; an absent `profile` field means the binding is **unspecified / legacy** — a reader falls back to external context. Omission is allowed (a `kosmos/1.0` file has no `profile` field and stays valid — see §8).
- `profile` binds only field *semantics* interpretation; it never changes the grammar (§5.4). It does not make any otherwise-valid file invalid, and an unrecognised profile id is not a parse error (a parser MAY warn — see §"conformance").

Self-identification is a manifest-format property: a manifest that cannot say what schema interprets its numbers is under-specified. Placing `profile` next to the placement coordinates it governs keeps the binding declaration local to the data it affects.

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

One attribute is standardised: `encoder=` records **which encoder produced the placement measurement** for this payload (§4.4 — encoder provenance):

```
@payload image := ref "media/wave.png" sha256=<hex64> bytes=148213 encoder="clip-vit-b32@2026-05"
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

### 4.4 encoder provenance

The cross-modal rule (§4.2) references an encoder `E_m` per modality, but a measured anchor needs to record *which* encoder produced its placement — otherwise a measurement is not reproducible and two payloads measured by different encoders cannot be compared.

Two optional, backward-compatible provenance fields are provided:

- **per-`@payload` `encoder=` attribute** (preferred — granular): records the encoder for *that one* modality's measurement.

  ```
  @payload audio := ref "media/wave.wav" sha256=<hex64> bytes=882044 encoder="wav2vec2-base@2026-05"
  ```

- **anchor-level `measured_by` field** (placement-coordinate body line): records a single encoder/run when one encoder produced the whole anchor's placement, or when the anchor is text-only.

  ```
  measured_by = "anima-S-module@UBM-E5"
  ```

The `encoder=` value is a free string — an encoder id, version, or run tag (`<name>@<version-or-run>` is the recommended shape but not enforced). Both fields are **optional**: an unmeasured / design-placeholder anchor (§4.3) has no encoder yet, so it carries neither. When a payload is later measured, the `encoder=` attribute is added next to its `ref` — an orthogonal additive change, never a rewrite (§5.3).

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

### 5.5 inter-anchor relations — out of scope (one anchor = one file)

A natural extension request is an `@edge` / `@relation` entry to express that anchor A *relates to* anchor B (similarity, contains, precedes, …). The `kosmos/1.1` decision is **`.kosmos` stays strictly 1-anchor-atomic — no inter-anchor relation entry is added**. Rationale:

1. **"One anchor = one file" is a load-bearing invariant.** The BNF (§6.1 rule 1, §6.2 conformance rule 1), the grep cookbook (one `@anchor` per file), the LSP "exactly one `@anchor`" diagnostic, and the §0 one-sentence definition all rest on it. An `@edge` entry — whether it names a foreign file or embeds a second anchor — erodes that invariant and turns a *manifest* into a *graph fragment*.
2. **The format's verification physics is intra-anchor.** The cross-modal consistency rule (§4.2) constrains payloads *of the same anchor* against *its own* `coord`/`radius`. An inter-anchor relation has no analogous closed transfer-form in this grammar; it would be an unverified annotation, weakening the format's honesty posture.
3. **Relations are a profile / corpus concern, not a manifest concern.** Where a consuming project needs anchor-to-anchor structure, it expresses that in its own corpus / graph layer keyed by anchor `id` — `.kosmos` files are the *nodes*; the *edges* live in whatever layer consumes the nodes. (Concretely: the anima reference implementation surfaced this need and resolved it by carving anchor-interaction relations as *corpus* `<relate>` tags, **not** as `.kosmos` entries — the manifest stays 1-anchor-atomic and the corpus layer owns the graph.)

A future profile MAY define a relation-bearing companion artefact, and a future `kosmos/2.0` MAY revisit a graph layer with its own verification rule — but within `kosmos/1.x` the manifest is one anchor, one file, and inter-anchor relations are explicitly out of scope.

> **kosmos/2.0 update**: the collection layer foreshadowed here is now opened as the `@corpus` entry (§5.6) — a dataset = an ordered *collection* of member anchors. This is **not** the same as inter-anchor *edges*: `@corpus` adds containment (a corpus *holds* members), not pairwise relations. The `@edge`/`@relation` prohibition above still stands; a corpus member carries no edge to another member. Verification stays intra-member (each member's own cross-modal rule) plus a corpus-level integrity rule (§5.6.4).

---

## 5.6 § `@corpus` — dataset collection layer (kosmos/2.0)

A `.kosmos` file's top-level entry is **either** one `@anchor` (1.x, unchanged) **or** one `@corpus`. A `@corpus` is a **dataset**: an ordered collection of member anchors that is *itself* a meta-anchor (it has its own placement = the centroid its members carve). This is the format's training-data layer (a corpus of samples, each sample an anchor).

### 5.6.1 header + meta-anchor placement

```
@corpus <id> := "<name>" :: kosmos-corpus [active]
  profile = "anima-consciousness-carving"
  coord   = [0.0, 0.0]   # meta-anchor: centroid of members — design placeholder, measured later
  lane    = "clm_p1"
  radius  = 1.0          # corpus spread — design placeholder, measured later
```

A `@corpus` carries the **same required placement triple** (`coord`/`lane`/`radius`) as `@anchor` (§2) — the corpus is a *meta-anchor*: its `coord` is the centroid its members occupy, its `radius` the dataset's spread. Until an encoder (§4.4) measures it, `coord`/`radius` are design placeholders (§4.3 honesty rule) carrying the inline comment. `tier`/`tags`/`profile` carry over unchanged.

### 5.6.2 corpus meta fields

| field | type | required | meaning |
|---|---|---|---|
| `anchor_level` | enum `sample` \| `topic` \| `2tier` | optional (default `2tier`) | granularity of members — `sample`: one member per training sample · `topic`: one member per Ψ-cluster · `2tier`: cluster-members each holding a sample stream (default; VQ centroid+residual / filesystem inode+extent analog). A scale-free zoom parameter, not a fixed choice. |
| `count` | integer ≥ 0 | required | total member anchors (across inline + ref) |
| `lane_mix` | quoted `k=v, …` map | optional | per-lane mixing fractions, Σ = 1.0 (e.g. `"web=0.8, register=0.2"`) — maps a MoE 2-lane corpus to its sources |
| `vocab` | integer | optional | tokenisation vocabulary size (e.g. `256` for byte-vocab) |
| `encoding` | quoted string | optional | token encoding id (e.g. `"byte-utf8"`) |
| `merkle` | hex64 | optional | Merkle root over member `sha256`s — scale integrity without listing all (full format: a future minor) |

`anchor_level` is open-by-default per §6.2 (an unknown value tolerated); the three named values are the standard set.

### 5.6.3 members — two forms (inline ⊕ ref)

A corpus lists members in **either or both** forms (mix freely):

**(a) inline** — a nested `@anchor` member at 2-space indent (small / cold-readable corpora). The nested `@anchor` is the full §1–§3 anchor grammar, indented; because it is **not** at column 0 it does not violate the legacy "one `@anchor` at column 0" rule — a single-anchor `.kosmos` file is still exactly one column-0 `@anchor`.

```
  @anchor s0001 := "sample 1" :: kosmos-anchor [active]
    coord = [..]   # member placement
    @payload text := "…"
```

**(b) ref** — a packed shard of many members (large corpora; avoids file-explosion). The shard is an anchor-pack (`.limen`, wire format spec'd in [`spec/limen.md`](limen.md)), **not** an opaque blob — it holds packed member anchors (length-prefixed serialized `@anchor` records + a trailing merkle root over their content hashes, decodable straight back into inline members):

```
  member = ref "shards/web.limen" sha256=<hex64> count=<N> frac=0.8 lane="web"
```

`member` ref attrs: `sha256=` (content commitment, required), `count=` (members in shard), `frac=` (this shard's mixing fraction, float; Σ frac over all members = 1.0), `lane=` (source-lane label). `attr` is open (§6.2 rule 6).

### 5.6.4 corpus verification — `closed_corpus`

```
  closed_corpus = "Σ frac = 1.0 ∧ ∀ member sha256 verified ∧ (merkle present → root recomputes)"
```

Analogous to `@anchor`'s `closed_anchor` (§4.1). The corpus-level integrity rule is: mixing fractions sum to 1.0, every `ref` member's `sha256` matches its shard bytes, and (if `merkle` present) the root recomputes. The **cross-modal rule (§4.2) applies per member** (each member anchor against its own `coord`/`radius`), not to the corpus as a whole; the corpus `coord` is verified as the members' centroid once an encoder is wired.

### 5.6.5 multimodal members + open growth

Each member anchor carries the full open modality set (§3.2) — `text` (inline), `image`/`audio`/`video` (ref), `tension` (anima profile, 5-channel), and any open-enum modality. A corpus is therefore multimodal-by-construction: a sample may feed text now and `audio`/`tension` later via the `pending`→`ref` peg-hole (§5.2), zero format change. A corpus MAY also grow (append members) — append-only is the natural mode (consistent with no train/infer split); a `frozen` snapshot for training reproducibility is a profile/tooling concern.

---

## 6. BNF-ish grammar + conformance

### 6.1 BNF-ish grammar

```bnf
kosmos-file   ::= [ shebang ] { comment } ( anchor-entry | corpus-entry )  ; 2.0: top-level XOR

shebang       ::= "#!/usr/bin/env kosmos" NEWLINE
comment       ::= "#" { any-char } NEWLINE

anchor-entry  ::= anchor-header NEWLINE
                  { INDENT ( coord-field | payload-entry | meta-field ) NEWLINE }

corpus-entry  ::= corpus-header NEWLINE                    ; (§5.6, kosmos/2.0)
                  { INDENT ( coord-field | corpus-field | member-entry
                           | corpus-meta-field ) NEWLINE }
corpus-header ::= "@corpus" SP id SP ":=" SP qstring SP "::" SP
                  "kosmos-corpus" SP "[" grade-list "]"
corpus-field  ::= "anchor_level" SP "=" SP ( "sample"|"topic"|"2tier"|ident )
                | "count"    SP "=" SP integer
                | "lane_mix" SP "=" SP qstring
                | "vocab"    SP "=" SP integer
                | "encoding" SP "=" SP qstring
                | "merkle"   SP "=" SP hex64
member-entry  ::= INDENT anchor-entry                      ; (a) inline nested @anchor
                | "member" SP "=" SP "ref" SP qstring
                    SP "sha256=" hex64 { SP attr }          ; (b) packed shard ref
corpus-meta-field ::= "closed_corpus" SP "=" SP qstring

anchor-header ::= "@anchor" SP id SP ":=" SP qstring SP "::" SP
                  "kosmos-anchor" SP "[" grade-list "]"

grade-list    ::= [ "tier=" integer SP ] state-tag
state-tag     ::= "active" | "draft" | "deprecated"

coord-field   ::= "coord"   SP "=" SP vector  [ comment ]  ; required
                | "lane"    SP "=" SP qstring              ; required
                | "radius"  SP "=" SP float   [ comment ]  ; required, > 0
                | "tier"    SP "=" SP integer              ; optional, >= 0
                | "tags"    SP "=" SP qstring              ; optional
                | "profile" SP "=" SP qstring              ; optional-but-recommended (§2.4)

vector        ::= "[" float { "," SP float } "]"           ; dimension >= 1

payload-entry ::= "@payload" SP modality SP ":=" SP payload-body
payload-body  ::= qstring                                  ; (a) inline
                | "ref" SP qstring SP "sha256=" hex64
                      SP "bytes=" integer { SP attr }       ; (b) ref
                | "pending" SP qstring                      ; (c) pending
attr          ::= ident "=" ( integer | float | ident | qstring )  ; e.g. channels=5,
                                                            ;  frac=0.8 (§5.6.3), encoder="clip@2026-05" (§4.4)
modality      ::= "text" | "image" | "audio" | "video"
                | ident                                    ; open enum

meta-field    ::= "closed_anchor" SP "=" SP qstring
                | "measured_by"   SP "=" SP qstring         ; optional (§4.4)

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
7. `profile`, `tier`, `tags`, `measured_by`, and `encoder=` are optional — a file omitting them is valid.

### 6.2 conformance

This section consolidates parser obligations. "MUST" / "SHOULD" / "MAY" are used in the RFC 2119 sense.

**A conformant `.kosmos` parser MUST:**

1. accept exactly **one top-level entry per file** — `@anchor` XOR `@corpus`, at column 0 (§5.6, kosmos/2.0); report a file with zero, or more-than-one column-0 entry, as an **error**. A single-anchor file is still exactly one column-0 `@anchor` (legacy invariant preserved); a `@corpus` file's nested `@anchor` members are indented (2-space), not column 0, so they do not count as top-level entries.
2. accept the required placement triple `coord` / `lane` / `radius` as defined even when `@payload` count is zero; report a missing required field as an **error**.
3. accept `@payload` as zero-or-more.
4. **not reject an unknown modality tag** — the modality enum is open (§3.2 / §5.1). The parser validates only that the payload body is one of the three forms (inline / `ref` / `pending`).
5. **not reject an unknown 2-space-indent body field** — the placement-field set is open to orthogonal additions (§5.3). A line of the form `<ident> = <value>` whose key is not one of the known fields is accepted and either retained verbatim or ignored; it is **never an error**. (This is what makes `profile`, `measured_by`, and any future field backward-compatible: a `kosmos/1.0` parser meets this rule and therefore already tolerates `kosmos/1.1` files.)
6. **not reject an unknown `@payload` attribute** — `attr` is open (§3.1 / §4.4); an unrecognised `encoder=`/`channels=`/… attribute is accepted, never an error.
7. preserve file bytes it does not interpret — a parser MUST NOT silently rewrite or reorder existing fields (drift-avoidance, §5.3).

**A conformant `.kosmos` parser SHOULD:**

8. treat an absent `profile` field as *unspecified / legacy* (§2.4), not as an error, and MAY surface it as a hint/recommendation.
9. emit a **warning** (not an error) for: an unrecognised `profile` id; an unrecognised modality or attribute; an unmeasured `coord`/`radius` lacking the design-placeholder comment (§4.3).
10. validate that a `ref` payload carries both `sha256=` (64 hex) and `bytes=`, and that `coord` is a vector of dimension ≥ 1.

**Malformed-input behavior (error vs skip):**

- A **structural** violation — no `@anchor`, multiple `@anchor`, a missing required placement field, a malformed `@anchor` header, a `@payload` body matching none of the three forms — is an **error**: the file is not a conformant `.kosmos` file. A validating tool MUST report it; a one-shot linter exits non-zero.
- An **unknown-but-well-formed** construct — an unknown modality, an unknown body field, an unknown attribute, an unrecognised `profile` id — is **skipped/tolerated**, never an error (rules 4–6, 8–9). This open-by-default stance is the format's extension contract: new fields and modalities are added without a grammar break.

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

### `kosmos/1.1` — 2026-05-18 (backward-compatible extension · active)
- **`profile` field (§2.4)** — an optional-but-recommended placement-coordinate body line `profile = "<profile-id>"` that self-identifies which profile (`spec/profiles/`) binds the file's `coord`/`lane`/`radius`/`tier`/`tags` semantics. A reader no longer needs external (directory / comment) context to interpret a `coord` vector. Absent `profile` = unspecified/legacy, still valid.
- **§6.2 conformance** — a new conformance subsection consolidating parser MUST/SHOULD rules and malformed-input behavior (structural violation = error; unknown-but-well-formed construct = skip/tolerate). Codifies the previously-scattered "parser MUST NOT reject an unknown modality" rule into a full open-by-default extension contract (unknown modality / body field / attribute / profile id all tolerated).
- **encoder provenance (§4.4)** — an optional per-`@payload` `encoder="<id>"` attribute and an optional anchor-level `measured_by = "<id>"` field, recording which encoder produced a placement measurement (the §4.2 cross-modal rule's `E_m`). Both optional; a design-placeholder anchor carries neither. `attr` BNF extended to allow a quoted-string value.
- **G2 — inter-anchor relations resolved out-of-scope (§5.5)** — a documented decision that `.kosmos` stays strictly 1-anchor-atomic; no `@edge`/`@relation` entry is added. Inter-anchor relations are a profile/corpus/graph-layer concern keyed by anchor `id`; the manifest stays one anchor per file.
- **Backward compatibility**: every `kosmos/1.0` file remains a valid `kosmos/1.1` file — all new fields/attributes are optional, no field removed, no grammar construct changed. A `kosmos/1.0` parser meeting the open-field/open-modality rules already tolerates `kosmos/1.1` files (§6.2 rule 5). Semver: **minor**.

### `kosmos/2.0` — 2026-05-30 (collection layer · MAJOR · active)
- **`@corpus` entry (§5.6)** — the third entry type. A `.kosmos` file's top-level entry is now `@anchor` **XOR** `@corpus`. A `@corpus` is a **dataset**: an ordered collection of member anchors, itself a meta-anchor carrying the required placement triple (`coord` = members' centroid · `lane` · `radius`). This opens the collection layer foreshadowed in §5.5 (distinct from inter-anchor *edges*, which stay out of scope — a corpus adds *containment*, not pairwise relations).
- **corpus meta fields (§5.6.2)** — `anchor_level` (`sample`|`topic`|`2tier`, default `2tier`; a scale-free granularity *zoom* parameter — sample/topic/2tier are special cases of one record, not a fork) · `count` · `lane_mix` · `vocab` · `encoding` · `merkle`.
- **two member forms (§5.6.3)** — inline (nested 2-space `@anchor`) ⊕ ref (`member = ref "*.limen" sha256=… frac=…`, a packed anchor-pack — NOT an opaque blob). Mix freely. `attr` BNF extended to allow a `float` value (`frac=0.8`).
- **`closed_corpus` (§5.6.4)** — corpus-level integrity (Σ frac = 1.0 ∧ ∀ ref member sha256 verified ∧ merkle root recomputes). The §4.2 cross-modal rule applies **per member**, not corpus-wide.
- **MIGRATION NOTE (1.x → 2.0)**: every `kosmos/1.x` single-anchor file remains valid **unchanged** — it is one column-0 `@anchor`, which 2.0 accepts as one of the two top-level forms. The breaking change is only at the parser/spec contract level: a 1.x parser hard-coding "exactly one `@anchor`" will reject a `@corpus` file (it must learn the `@corpus` top-level form). No existing file is rewritten; no field removed. Producers emitting only `@anchor` need no change. Semver: **major** (top-level invariant generalised). The entry-type count badge moves 2 → 3 (`@anchor`, `@payload`, `@corpus`).
- **Out of scope (deferred to 2.x minors)**: the `.limen` packed-shard binary format, the `merkle` tree construction detail, HF-dataset export, and LSP/tree-sitter `@corpus` recognition — each a follow-on layer; this entry defines the *grammar* only.

### `kosmos/2.1` — 2026-06-04 (the 2.0 deferrals land · backward-compatible · active)
- **No grammar change.** The `.kosmos` grammar (§1–§6) is byte-identical to `kosmos/2.0`; a 2.0 file is a 2.1 file and a 2.1 file is a 2.0 file. This entry only records that the four layers the `kosmos/2.0` entry deferred to "2.x minors" have all **landed** — the format is now fully implemented around its 2.0 grammar, not just specified. Semver: **minor** (companion-layer completion, zero grammar delta).
- **`.limen` packed-shard binary format — SPEC'D + reference codec LANDED.** [`spec/limen.md`](limen.md) defines the wire format (`magic` + LE header + CRC-32 header guard + length-prefixed `@anchor` records + trailing SHA-256 merkle root) the `member = ref "*.limen"` form (§5.6.3 (b)) points at. The pure-hexa reference codec is `impl/limen.hexa` (`limen_pack`/`limen_unpack`/`limen_verify` + byte-array SHA-256 (FIPS 180-4) + CRC-32/IEEE + RFC-6962-style merkle); 14/14 self-test (`impl/test_limen_roundtrip.hexa`: FIPS+CRC vectors, round-trip, tamper, merkle edges, disk I/O).
- **merkle tree construction — SPEC'D.** [`spec/limen.md`](limen.md) §3 fixes the construction (binary tree over per-record leaf hashes · odd-level last-node duplication · `count==0`→SHA-256(empty), `count==1`→leaf). The within-shard root is authoritative now; the corpus-of-shards root (a `merkle` field over *all* shards) stays a future minor (`spec/limen.md` §4 note).
- **HF-dataset export — LANDED.** `tool/corpus_to_hf.hexa` projects a `@corpus` file to a HuggingFace `datasets` manifest (repo_id + card carrying the corpus meta `anchor_level`/`vocab`/`encoding`/`lane_mix`/`count`/`merkle` + a `data_files` array of the `member = ref` shards with `sha256`/`num_rows`/`frac`/`lane`). Docs: [`docs/hf_export.md`](../docs/hf_export.md).
- **LSP / tree-sitter `@corpus` recognition — LANDED.** The canonical hexa-native linter `lsp/kosmos_lsp.hexa` accepts `@corpus` as a column-0 top-level entry, lints nested `@anchor` members + `member = ref` shards + the corpus meta fields, and hovers `@corpus`/`anchor_level`/`lane_mix`/`member`/`closed_corpus`. The `tree-sitter-kosmos/` grammar recognises the `@corpus` rule. The deprecated `.py` editor server is synced to the same `@corpus` behaviour (`lsp/PARITY_VERIFY.md`: 26/26 files byte-equal between `.py` and `.hexa`, incl. the `@corpus` example). `.limen` shard *bytes* stay out of LSP scope (binary, not a `.kosmos` text grammar — `spec/limen.md` §6).
