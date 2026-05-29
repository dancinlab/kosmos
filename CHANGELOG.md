# Changelog

Chronological log of notable changes. One section per ship batch, date-keyed. Spec version tracked as `kosmos/<major>.<minor>`.

For the full audit trail, see `git log`.

---

## 2026-05-30

- **`kosmos/2.0` — `@corpus` 데이터셋 collection 계층 (MAJOR)** — 세 번째 entry type `@corpus` 도입. `.kosmos` 파일의 최상위 entry가 `@anchor` XOR `@corpus`로 일반화. `@corpus` = 데이터셋(멤버 앵커들의 정렬된 모음)이자 그 자체로 meta-anchor(coord=멤버 centroid). §5.5가 예약했던 collection 계층을 엶(inter-anchor edge와는 구분 — containment지 relation 아님). spec `@anchor "exactly one"` 불변은 "최상위 entry 정확히 하나"로 일반화되되, 기존 1.x 단일-앵커 파일은 변경 없이 유효(migration note §8).
- **corpus meta** — `anchor_level`(sample|topic|2tier, 기본 2tier, scale-free zoom) · `count` · `lane_mix` · `vocab` · `encoding` · `merkle`. 멤버 2-form: inline 중첩 `@anchor` ⊕ `member = ref "*.kanchors"`(packed anchor-pack). `attr` BNF에 float 허용(`frac=0.8`).
- **`.kanchors` 포맷 spec** (`spec/kanchors.md`) — `member = ref`가 가리키는 packed anchor-pack 바이너리(magic+version+count+length-prefixed 앵커 레코드+merkle root). opaque blob 아님 — 멤버 앵커를 디코드 가능하게 담음.
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
