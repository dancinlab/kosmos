## Examples

| File | Demonstrates |
|---|---|
| `01_text_only.kosmos` | Minimal general anchor — required placement triple (`coord`/`lane`/`radius`) + one inline `text` payload. The only consumable modality today. |
| `02_multimodal.kosmos` | General anchor with all three payload forms — inline `text`, `ref` (image/audio with sha256+bytes content commitment), and `pending` (video). 3-D `coord` vector. |
| `03_anima_knuth_077_mandala.kosmos` | The `anima-consciousness-carving` **profile** — `coord`=vacuum_psi, `lane`=cell_id, `radius`=basin_radius, `tier`=Knuth Tier, `tags`=category+top_emotion; anima-native `tension` modality; 4-path co-existence. |

All examples are valid `kosmos/1.0`:

- UTF-8, no BOM, LF line endings
- Exactly one `@anchor` header at column 0; coordinate/payload body at 2-space indent
- The placement triple is defined even when payloads are zero/pending
- Unmeasured `coord`/`radius` carry a `# design placeholder, measured later` comment

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
