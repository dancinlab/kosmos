## Examples

| File | Demonstrates |
|---|---|
| `01_text_only.kosmos` | Minimal general anchor — required placement triple (`coord`/`lane`/`radius`) + one inline `text` payload. The only consumable modality today. **No `profile` field** — demonstrates the valid *unspecified / legacy* case (§2.4): `profile` is optional-but-recommended, and a file with no named profile binding stays valid. |
| `02_multimodal.kosmos` | General anchor with all three payload forms — inline `text`, `ref` (image/audio with sha256+bytes content commitment), and `pending` (video). 3-D `coord` vector. Also **no `profile`** — a general anchor not bound to a named profile (§2.4). |
| `03_anima_knuth_077_mandala.kosmos` | The `anima-consciousness-carving` **profile** — declares `profile = "anima-consciousness-carving"` (§2.4 self-identification); `coord`=vacuum_psi, `lane`=cell_id, `radius`=basin_radius, `tier`=Knuth Tier, `tags`=category+top_emotion; anima-native `tension` modality; 4-path co-existence. |

All examples are valid `kosmos/1.1` (and were valid `kosmos/1.0` — the new `profile` field is optional, so a profile-less file is conformant under both):

- UTF-8, no BOM, LF line endings
- Exactly one `@anchor` header at column 0; coordinate/payload body at 2-space indent
- The placement triple is defined even when payloads are zero/pending
- Unmeasured `coord`/`radius` carry a `# design placeholder, measured later` comment
- `profile` (§2.4) is declared when the anchor is bound to a named profile (`03`); omitted when the anchor is a general, unbound example (`01`, `02`)

The `ref` sha256/bytes in `02_multimodal.kosmos` are illustrative (the sibling `media/` binaries are not shipped — `.kosmos` is a *manifest*). See [`../spec/kosmos.md`](../spec/kosmos.md) for the full grammar and [`../spec/profiles/`](../spec/profiles/) for profile bindings.

## Quick grep cookbook

```bash
# the single anchor header of each file
grep '^@anchor ' *.kosmos

# every sensory payload
grep '^  @payload ' *.kosmos

# payloads not yet materialized
grep '^  @payload .* := pending ' *.kosmos

# binary payloads (content commitment present)
grep '^  @payload .* := ref ' *.kosmos

# placement coordinates
grep -E '^  (coord|lane|radius|tier|tags) ' *.kosmos
```
