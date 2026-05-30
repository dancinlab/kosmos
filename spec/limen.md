# limen.md — `.limen` packed anchor-harbor binary format (spec)

> **STATUS: spec + reference codec** (codec landed 2026-05-31) · a `kosmos/2.x` follow-on layer.
> This document defines the **binary container** that a `@corpus` member `ref`
> points at (`member = ref "shards/web.limen" sha256=… count=… frac=… lane=…`,
> see `spec/kosmos.md` §5.6.3 form (b)). The `kosmos/2.0` entry (`spec/kosmos.md`
> §8) deferred the `.limen` binary + the merkle construction detail to a 2.x
> layer; **this document fills that deferral** — the format + ASCII layout + the
> merkle construction. The decode/encode **reference implementation is
> `impl/limen.hexa`** (landed 2026-05-31; pure-hexa pack/unpack/verify + byte-array
> SHA-256 + CRC-32 + merkle, 14/14 self-test in `impl/test_limen_roundtrip.hexa`) —
> this is the wire spec it obeys.

---

## 0. What it is — one sentence

A `.limen` file is a **packed shard of member anchors**: a length-prefixed
sequence of serialized `@anchor` entries (each = one corpus member) plus a
trailing **merkle root** over the members' content hashes — a decodable pack, not
an opaque blob (it unpacks back to a stream of `@anchor` manifests, exactly the
inline form of `spec/kosmos.md` §5.6.3 (a)).

The point of the `ref` form (vs inline nested `@anchor`s) is **scale**: a
million-sample corpus cannot list a million 2-space-indented anchors in one
`.kosmos` text file. A `.limen` shard packs them compactly while staying
**content-addressable** (the corpus `member = ref … sha256=` commits to the whole
shard's bytes; the in-shard merkle root commits to each member independently, so
a single member can be verified without re-hashing the whole shard).

---

## 1. byte layout (ASCII diagram)

All multi-byte integers are **little-endian unsigned**. Offsets are byte offsets
from the start of file. `hex64` member hashes are the **raw 32 bytes** (not the
64-char ASCII hex used in the `.kosmos` text manifest — the text form ASCII-encodes
the same 32 bytes).

```
 offset  size   field                 notes
 ──────  ─────  ────────────────────  ─────────────────────────────────────────
 0       8      magic                 ASCII "LIMEN\0\0\0" (4C 49 4D 45 4E 00 00 00)
 8       2      version_major         u16 LE — pack format major (this doc = 2)
 10      2      version_minor         u16 LE — pack format minor (this doc = 0)
 12      4      count                 u32 LE — number of member records
 16      4      flags                 u32 LE — bit0 = members sorted by hash
                                              (canonical merkle order); other
                                              bits reserved 0
 20      4      header_crc32          u32 LE — CRC-32 of bytes [0, 20)
                                              (cheap header-corruption guard;
                                              integrity proper = §3 merkle)
 ──────  ─────  ────────────────────  ─────────────────────────────────────────
 24      …      RECORD[0]             first member record (§2)
 …       …      RECORD[1]             …
 …       …      RECORD[count-1]       last member record
 ──────  ─────  ────────────────────  ─────────────────────────────────────────
 R       32     merkle_root           raw 32-byte SHA-256 merkle root over the
                                      count member hashes (§3). R = 24 + Σ record
                                      sizes. The trailing root is the shard's
                                      self-integrity commitment.
```

`count` is redundant with the corpus `member = ref … count=N` attribute
(`spec/kosmos.md` §5.6.3); a decoder MUST check they agree and report a mismatch
as an error.

---

## 2. member record — one packed `@anchor`

Each record is a **length-prefixed serialized `@anchor`**. The payload is the
member's own `@anchor` manifest, byte-for-byte the UTF-8 text of the §1–§4
`@anchor` grammar (`spec/kosmos.md`), with leading indent stripped (a member is a
top-level `@anchor`, column 0, inside its own record):

```
 offset  size   field          notes
 ──────  ─────  ─────────────  ──────────────────────────────────────────────
 0       32     hash           raw 32-byte SHA-256 of `anchor_text` (the
                               record's content commitment / merkle leaf)
 32      4      anchor_len     u32 LE — byte length of `anchor_text`
 36      …      anchor_text    `anchor_len` bytes — the serialized @anchor
                               manifest (UTF-8). Decodable straight back into
                               an inline `@anchor` member (§5.6.3 form (a)).
```

Record total size = `36 + anchor_len`. Records are packed contiguously (no
padding). `anchor_text` is exactly what a `.kosmos` reader would see as a
single-anchor file: `@anchor <id> := "…" :: kosmos-anchor […]` + 2-space body
(`coord`/`lane`/`radius`/payloads/`closed_anchor`). Binary payloads inside a
member stay as `ref` lines (the binary itself is NOT inlined into the pack — the
pack holds the *manifest* of each member, same manifest-not-blob discipline as
`.kosmos`; a member's image bytes live in their own sibling file, sha256-committed
in the member's `@payload … := ref …` line).

`hash` is computed over **`anchor_text` only** (the `anchor_len` bytes), not over
the 36-byte prefix — so a member's leaf hash equals the `sha256` that the same
member would carry if listed inline, making inline⊕ref members hash-comparable.

---

## 3. merkle construction (trailing root)

The trailing `merkle_root` (§1) is a binary SHA-256 merkle tree over the `count`
member leaf hashes (the per-record `hash` field, §2). Construction (RFC-6962-style
domain separation to resist second-preimage / leaf-vs-node confusion):

```
leaf_hash(i)        = record[i].hash            ; already SHA-256(anchor_text), §2
node_hash(L, R)     = SHA-256( 0x01 || L || R ) ; interior node, 0x01 prefix
                                                ; (leaves are 0x00-domain via §2:
                                                ;  record.hash = SHA-256(text);
                                                ;  treat as leaf input directly)
```

Tree build (bottom-up, left-to-right over the member order as stored):

```
level[0] = [ leaf_hash(0), leaf_hash(1), …, leaf_hash(count-1) ]
while len(level) > 1:
    next = []
    for i in 0, 2, 4, … < len(level):
        L = level[i]
        R = level[i+1] if i+1 < len(level) else level[i]   ; odd → duplicate last
        next.append( node_hash(L, R) )
    level = next
merkle_root = level[0]                                       ; the single survivor
```

Edge cases:
- `count == 0` → `merkle_root` = SHA-256 of the empty string (the canonical empty-tree
  root). A zero-member shard is legal (an empty corpus partition) but unusual.
- `count == 1` → `merkle_root` = the single leaf hash (no interior node; the tree
  is the leaf itself).
- **odd level** → the last node is duplicated (paired with itself) before hashing
  (the common Bitcoin-style rule; deterministic, no padding sentinel).

**Member order is significant**: the merkle root depends on record order. When
`flags` bit0 = 1, members are stored sorted ascending by `hash` (canonical order —
two shards with the same member set produce the same root). When bit0 = 0, order
is as-produced (a stream); the root still commits to that exact order.

---

## 4. verification — ties into `closed_corpus`

The corpus-level `closed_corpus` rule (`spec/kosmos.md` §5.6.4) is:

```
Σ frac = 1.0 ∧ ∀ member sha256 verified ∧ (merkle present → root recomputes)
```

A `.limen` shard satisfies its slice of that rule:

1. **shard sha256** — the corpus `member = ref … sha256=H` (§5.6.3) commits to the
   **whole `.limen` file bytes**. A verifier recomputes SHA-256 over the file and
   checks it equals `H`. (This is the coarse, whole-shard commitment.)
2. **per-member integrity** — each record's `hash` (§2) MUST equal SHA-256 of that
   record's `anchor_text`. A verifier recomputes per record (the fine commitment —
   lets one member be verified/extracted without the whole shard).
3. **merkle root** — the trailing `merkle_root` (§1) MUST equal the §3 reconstruction
   over the records' `hash` fields. This is what `(merkle present → root recomputes)`
   in `closed_corpus` checks; the corpus `@corpus … merkle = <hex64>` field
   (`spec/kosmos.md` §5.6.2) MAY carry a root over *all* members across *all* shards
   (a corpus-of-shards merkle whose leaves are the per-shard roots) — a future-minor
   detail; within one shard, the trailing root is authoritative.
4. **count agreement** — header `count` == corpus `member = ref … count=N` (§1).

`cross-modal consistency` (`spec/kosmos.md` §4.2) applies **per member** (each
unpacked `@anchor` against its own `coord`/`radius`), not to the shard as a whole —
identical to the §5.6.4 per-member rule. The pack adds no new verification physics;
it only carries members compactly + commits to them via merkle.

---

## 5. relationship to the text manifest (round-trip)

`.limen` ⇄ inline `@anchor` members is a **lossless round-trip**:

```
   @corpus (kosmos text)                       shard.limen (binary)
   ─────────────────────                       ───────────────────────
     member = ref "shards/web.limen" ──────▶  [LIMEN\0][hdr]
        sha256=H count=N frac=0.8 lane="web"        RECORD: hash|len|@anchor text
                                                    RECORD: hash|len|@anchor text
                                                    …
                                                    [merkle_root]
                                                          │ unpack
                                                          ▼
                                              @anchor s0001 := "…" :: kosmos-anchor […]
                                                coord = […]   @payload text := "…"
                                              @anchor s0002 := …
```

- **pack** (inline → shard): take each inline `@anchor` member, strip its indent to
  column 0, serialize to UTF-8 `anchor_text`, prefix with SHA-256 + `anchor_len`,
  concatenate, append the merkle root. A producer MAY sort by hash (set `flags` bit0).
- **unpack** (shard → inline): read the header, walk `count` records, for each emit
  the `anchor_text` re-indented 2 spaces as a nested `@corpus` member. Verify each
  record `hash` and the trailing `merkle_root` while walking.

A corpus may mix forms freely (§5.6.3): small/cold-readable members stay inline in
the `.kosmos` text; bulk members live in one or more `.limen` shards. The two are
interchangeable views of the same member set.

---

## 6. impl status (HONEST)

| layer | status |
|---|---|
| wire format (this doc) | **stable** — defined here; the reference codec below obeys it |
| `impl/limen.hexa` pack/unpack codec | **LANDED** (2026-05-31) — pure-hexa reference encoder/decoder obeying §1–§3: `limen_pack`/`limen_unpack`/`limen_verify` + byte-array SHA-256 (FIPS 180-4) + CRC-32/IEEE + §3 merkle + `write_bytes`/`read_file_bytes` disk I/O. 14/14 self-test (`impl/test_limen_roundtrip.hexa`: FIPS+CRC vectors, round-trip, tamper, merkle edges, disk). Note: bytes ride `[int]` (hexa strings are NUL-terminated) and the builtin `sha256()` is strlen-based so a byte-array SHA-256 is carried here |
| LSP / tree-sitter recognition of `.limen` | out of scope — `.limen` is binary, not a `.kosmos` text grammar; the LSP validates the `member = ref` *line* in the `.kosmos` manifest (see `lsp/kosmos_lsp.hexa`), not the shard bytes |
| `merkle` field over *all* shards (corpus-of-shards root) | **future minor** (§4 note) — within-shard root is authoritative now |

No `.limen` file is shipped in this repo (a real shard needs a scale corpus,
which does not exist yet — the `examples/04_corpus_clm_byte.kosmos` worked example
references `shards/web.limen` as a manifest pointer with a placeholder sha256,
exactly as `examples/02_multimodal.kosmos` references unshipped `media/` binaries).

---

## 7. cross-link

- `spec/kosmos.md` §5.6.3 (member `ref` form) · §5.6.4 (`closed_corpus`) · §8 (this
  fills the deferred `.limen` + merkle detail).
- `spec/profiles/anima-consciousness-carving.md` §5.5 (anima corpus binding).
- `examples/04_corpus_clm_byte.kosmos` — a worked `@corpus` referencing a `.limen` shard.
