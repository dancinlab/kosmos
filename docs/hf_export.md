# HF dataset export — `@corpus` → Hugging Face datasets (kosmos/2.0)

> `kosmos/2.0`의 `@corpus`(spec §5.6)를 Hugging Face `datasets` 레이아웃으로 내보내는 매핑. 도구: `tool/corpus_to_hf.hexa` (hexa-native, `k_hexa_native`).

## 무엇을 하나

`@corpus` 데이터셋(.kosmos)을 읽어 **HF 업로드용 매니페스트 JSON**을 emit한다. `.kosmos`는 데이터셋의 SSOT(배치·provenance)이고, HF는 배포 미러다.

```
clm_p1.kosmos (@corpus, SSOT)            HF dataset (dancinlab/<id>)
  coord/lane/radius (meta-anchor)   ─→   dataset card: placement metadata
  anchor_level·vocab·encoding       ─→   dataset card: config
  lane_mix "web=0.8, register=0.2"  ─→   dataset card: splits/configs + 비율
  member = ref "*.kanchors" sha256= ─→   data_files (sha256 무결성 carry)
  closed_corpus                     ─→   card: integrity statement
```

## 필드 매핑

| `@corpus` 필드 (spec §5.6) | HF datasets 대상 |
|---|---|
| `<id>` (헤더) | dataset repo 이름 (`dancinlab/<id>`) |
| `"<name>"` | dataset card `pretty_name` |
| `coord` / `lane` / `radius` | card `tags`: `placement.coord/lane/radius` (design-placeholder면 그대로 표기) |
| `anchor_level` | card `tags`: `kosmos.anchor_level` |
| `vocab` / `encoding` | card `tags`: `tokenization.{vocab,encoding}` |
| `lane_mix` | card `configs`: lane별 `data_dir` + `tags`: `mix.<lane>=<frac>` |
| `member = ref "..." sha256= count= frac= lane=` | `data_files`: 한 shard = 한 항목 `{path, sha256, num_rows:count, lane}` |
| inline `@anchor` member | shard로 packing 후 동일 처리(`spec/kanchors.md`) — 또는 소규모면 inline JSONL로 emit |
| `merkle` | card `tags`: `integrity.merkle_root` |
| `closed_corpus` | card 본문 integrity 문장 |

## emit 산출물

`tool/corpus_to_hf.hexa <corpus.kosmos>` →
- `<id>.hf-manifest.json` — repo_id · card 메타(위 매핑) · data_files(path+sha256+rows+lane) · split/config.

## 업로드 (수동 단계 — creds/network)

매니페스트는 도구가 emit하나, 실제 업로드는 자격증명+네트워크가 필요해 분리한다 (a_hf_complete·a_hf_autonomous 정책은 anima측 `tool/hf_upload_mk2.hexa` + `/HF.jsonl` 레지스트리가 관할):
1. `corpus_to_hf.hexa`로 매니페스트 생성 (sha256 carry).
2. shard(.kanchors) → HF data_files 경로로 배치 (대용량은 HF/R2, manifest만 git).
3. anima `tool/hf_upload_mk2.hexa`가 매니페스트 받아 org=dancinlab 업로드 (PUBLIC=closure PASS · PRIVATE=WIP, a_hf_autonomous 가시성 게이트).
4. 업로드 후 sha256 audit → `/HF.jsonl` row(`run·local_path·hf_repo_id·sha256·status`) 갱신.

## scope (정직)

- ✅ `@corpus` → HF 매니페스트 매핑 + emit (이 도구).
- ⏳ 실제 HF push: anima측 hf_upload_mk2 + creds (별개 계층, 위 §업로드).
- ⏳ `.kanchors` 디코드→HF rows 변환: `spec/kanchors.md` 바이너리 리더 구현 후 (2.x).
