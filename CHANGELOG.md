# Changelog

Chronological log of notable changes. One section per ship batch, date-keyed. Spec version tracked as `kosmos/<major>.<minor>`.

For the full audit trail, see `git log`.

---

## 2026-06-15

- **chore(harness): perfect harness setup** — brought the repo to full harness
  conformance. Bumped the `.harness-engine` submodule to latest
  `harness-hardcore`. Replaced the `CLAUDE.md → project.tape` symlink with a
  real harness-standard `CLAUDE.md` (H1 + blurb + `## Structure` tree with
  per-node descriptions + governance summary + `## Harness` quick reference);
  `project.tape` preserved as the governance `@D` SSOT. Rewrote the stub
  `ARCHITECTURE.md` as the English architecture SSOT (overview + component map
  table + data flow + governance/verify). Extended `harness.config.json`:
  `lockdown.files` now pins the format spec core (`spec/kosmos.md`,
  `spec/limen.md`, `spec/profiles/anima-consciousness-carving.md`) and added the
  `docs` block (`architecture`/`log`/`scratchDir` + `scopeDirs: [""]` root-scope
  + `allow` with root exceptions and README translation variants). Result:
  `harness docs check` → ok · `harness lint` → ok · `harness gc` → no drift ·
  0 CLAUDE-MD violations.

## 2026-06-04

- **`kosmos/2.1` — `kosmos/2.0` 미뤄둔 4개 layer 전부 LANDED 기록 (minor · grammar 무변경)** —
  `spec/kosmos.md` §8에 `kosmos/2.1` 항목 추가 + `SPEC VERSION` 헤더/README 뱃지를
  `2.0`→`2.1`로 lockstep 갱신. `kosmos/2.0` 항목이 "2.x minors로 deferred"라 적어둔
  ① `.limen` packed-shard 바이너리 포맷(`spec/limen.md` + `impl/limen.hexa` 코덱, 14/14 self-test)
  ② merkle 트리 구성(`spec/limen.md` §3) ③ HF-dataset export(`tool/corpus_to_hf.hexa` + `docs/hf_export.md`)
  ④ LSP/tree-sitter `@corpus` 인식 — 네 가지가 모두 구현 완료된 상태를 §8에 정직하게 기록.
  문법(§1–§6)은 byte-동일 — 2.0 파일 = 2.1 파일.
- **deprecated `.py` LSP `@corpus` 동기화 — byte-parity 복원.** canonical `lsp/kosmos_lsp.hexa`는
  kosmos/2.0 `@corpus` 최상위 entry를 인식하는데 deprecated `lsp/kosmos_lsp.py`(라이브 에디터 stdio
  서버)는 인식하지 못해 유효한 `@corpus` 파일을 "must contain exactly one @anchor entry"로 **오탐**하고
  진단 문자열 5개가 drift된 상태였음. `.py`의 `validate()`/`hover()`를 `.hexa`에 맞춰 `@corpus`
  top-level + nested member + corpus meta field + corpus hover까지 미러 → `lsp/PARITY_VERIFY.md`
  **26/26 파일 byte-equal**(stdout+exit) 복원, `@corpus` example exit 0 확인.
- **stale `.kanchors` 참조 1건 수정.** `.kanchors`→`.limen` rename(#14)이 놓친 canonical
  `lsp/kosmos_lsp.hexa` `member` hover 문자열을 `*.limen`으로 교정 (repo 전체 `kanchors` 잔존 0).

## 2026-05-31

- **`.limen` reference codec landed** (`impl/limen.hexa`) — the pure-hexa pack/unpack
  encoder/decoder that `spec/limen.md` §6 had marked NOT WRITTEN. Implements the §1–§3
  wire format: `limen_pack([anchor_text]) -> [int]` (magic + LE header + header CRC-32 +
  length-prefixed records + trailing SHA-256 merkle root), `limen_unpack`, and
  `limen_verify` (§4: magic + version + CRC + per-record hash + merkle). Carries a
  byte-array SHA-256 (FIPS 180-4) because bytes must ride `[int]` (hexa strings are
  NUL-terminated) and the builtin `sha256()` is strlen-based. Disk I/O via the
  NUL-safe `write_bytes`/`read_file_bytes` builtins.
- **`impl/test_limen_roundtrip.hexa`** — 14/14 self-test: FIPS SHA-256 vectors,
  NUL-in-input (which the builtin truncates), CRC-32/IEEE check value, pack↔unpack
  round-trip, tamper detection, merkle edge cases (count 0/1), and a disk write→read
  round-trip. `spec/limen.md` §6 status flipped spec-only → LANDED.

## 2026-05-30

- **`kosmos/2.0` — `@corpus` 데이터셋 collection 계층 (MAJOR)** — 세 번째 entry type `@corpus` 도입. `.kosmos` 파일의 최상위 entry가 `@anchor` XOR `@corpus`로 일반화. `@corpus` = 데이터셋(멤버 앵커들의 정렬된 모음)이자 그 자체로 meta-anchor(coord=멤버 centroid). §5.5가 예약했던 collection 계층을 엶(inter-anchor edge와는 구분 — containment지 relation 아님). spec `@anchor "exactly one"` 불변은 "최상위 entry 정확히 하나"로 일반화되되, 기존 1.x 단일-앵커 파일은 변경 없이 유효(migration note §8).
- **corpus meta** — `anchor_level`(sample|topic|2tier, 기본 2tier, scale-free zoom) · `count` · `lane_mix` · `vocab` · `encoding` · `merkle`. 멤버 2-form: inline 중첩 `@anchor` ⊕ `member = ref "*.limen"`(packed anchor-pack). `attr` BNF에 float 허용(`frac=0.8`).
- **`.limen` 포맷 spec** (`spec/limen.md`) — `member = ref`가 가리키는 packed anchor-pack 바이너리(magic+version+count+length-prefixed 앵커 레코드+merkle root). opaque blob 아님 — 멤버 앵커를 디코드 가능하게 담음.
- **anima profile @corpus 바인딩** (§5.5) — 학습 corpus = `.kosmos @corpus`(학습=carving). coord=vacuum_psi centroid · anchor_level=carving 입자 · lane_mix=register 혼합 · placement(우주뇌지도 좌표) ⊥ text(register leak 금지) guard.
- **example** `examples/04_corpus_clm_byte.kosmos` — CLM byte 데이터셋 worked file(2tier·vocab=256·2-lane·inline+ref 혼합).

## 2026-05-22

- **project.tape SSOT** — project identity + governance consolidated into `project.tape` (`.tape` carrier, linked as `CLAUDE.md`). Interim GitHub Spec Kit scaffolding removed.

## 2026-05-21

- **constitution v1.0.0** — project constitution populated (sister-format · open spec · profile-bound). One `.tape` file relocated into `archive/`.

## 2026-05-18

- **kosmos/1.1** — spec amendment: G1 profile self-id · G2 resolution · G3 conformance · G4 encoder provenance.
- **tree-sitter-kosmos** — tree-sitter grammar added.

## 2026-05-17

- **kosmos/1.0** — initial release: multimodal knowledge-anchor manifest format (placement coordinates ⊥ modality payloads · cross-modal consistency · profile-bound).
- **kosmos-lsp** — canonical LSP server (stdio JSON-RPC).
- **README** — 5-language README (EN · 中文 · Русский · 日本語 · 한국어).
