<p align="center">
  <strong>κόσμος</strong>
</p>

<h1 align="center">⊙ kosmos</h1>

<p align="center"><strong>[English](README.md) · [中文](README.zh.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md)</strong></p>

<p align="center"><strong>멀티모달 지식 앵커 매니페스트(Multimodal Knowledge-Anchor Manifest)</strong> — 배치 좌표 ⊥ 모달리티 페이로드 · 교차모달 일관성 · profile 바인딩</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-CC0--1.0-blue"></a>
  <img alt="Spec" src="https://img.shields.io/badge/spec-kosmos%2F1.0-success">
  <img alt="Entry-types" src="https://img.shields.io/badge/entry--types-2-informational">
  <img alt="Payload-forms" src="https://img.shields.io/badge/payload--forms-3-informational">
  <img alt="Sibling" src="https://img.shields.io/badge/sibling-tape%20·%20n6%20·%20hxc%20·%20n12-blueviolet">
</p>

<p align="center">행 지향 · grep 친화 · tape v1.2 상위집합 · 모달리티 독립적 배치 · profile 이 정의하는 의미론</p>

---

`.kosmos` 는 **멀티모달 지식 앵커 매니페스트(multimodal knowledge-anchor manifest)** 문법입니다. 각 파일은 정확히 하나의 *앵커(anchor)* — 추상 배치 공간 안의 한 점/분지(basin) — 를 서로 직교하는 두 개의 층으로 기술합니다.

1. **배치 좌표(Placement coordinates)** (`coord` / `lane` / `radius` / `tier` / `tags`) — *모달리티 독립적*. 감각 채널이 하나도 없어도 앵커의 위치는 존재합니다.
2. **감각 페이로드(Sensory payloads)** (`@payload <modality> := …`) — *모달리티 종속적*. 0개 이상의 채널(text · image · audio · video · …, 개방형 열거)이 모두 동일한 배치로 흘러듭니다.

`.kosmos` 파일은 **교차모달 일관성(cross-modal consistency)** 을 약속합니다. 즉, 모든 페이로드는 자신의 모달리티 인코더를 거친 뒤 반드시 `coord` 의 `radius` 이내에 안착해야 합니다. 하나의 개념을 여러 감각 방향에서 동시에 앵커링하면 단일 채널보다 더 단단하게 그것을 고정합니다 — 이 포맷은 그 결합 배치(joint placement)의 매니페스트입니다.

> [!NOTE]
> [`tape`](https://github.com/dancinlab/tape)(운영 / 인과-시간 trace), [`n6`](https://github.com/dancinlab/n6)(의미 / atlas 층), [`hxc`](https://github.com/dancinlab/hxc)(바이트 정준 와이어), [`n12`](https://github.com/dancinlab/n12)(12축 희소 큐브)에 이어지는 다섯 번째 동족 포맷입니다. `.kosmos` 는 **멀티모달 지식 앵커 배치(multimodal knowledge-anchor placement)** 층으로, 한 조각의 지식이 추상 공간의 어디에 위치하며 어떤 감각 채널이 그것을 공급하는지를 나타냅니다. 이것은 나머지 넷과 직교합니다. `tape` 는 *무엇이 일어났는가*, `n6` 는 *그것이 무엇을 의미하는가*, `hxc` 는 *정준 바이트*, `n12` 는 *희소 큐브 투영*, `kosmos` 는 *그것이 어디에, 어떤 감각으로 앵커링되었는가* 입니다.

## 한눈에 보기(At a glance)

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

## 두 개의 층, 하나의 앵커(Two layers, one anchor)

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

좌표는 하나, 페이로드는 여럿. 그것이 멀티모달 `.kosmos` 입니다.

## Profiles

기본 명세는 **기판 독립적(substrate-independent)** 입니다. `coord` 는 그저 "어떤 추상 공간 안의 한 점", `lane` 은 "파티션 id" 등이며, 그 구체적 의미는 **profile** 이 고정합니다.

- [`spec/kosmos.md`](spec/kosmos.md) — 일반 문법(도메인 물리 없음).
- [`spec/profiles/anima-consciousness-carving.md`](spec/profiles/anima-consciousness-carving.md) — 첫 번째 profile: `coord` / `lane` / `radius` / `tier` / `tags` 를 Living Consciousness Agent 인 `anima` 의 CONSCIOUSNESS-CARVING 패러다임에 바인딩합니다. 참조 구현: [`dancinlab/anima`](https://github.com/dancinlab/anima). 구체적인 도메인 물리 바인딩은 전적으로 그 profile 파일 안에 존재합니다.

profile 은 결코 문법을 바꾸지 않습니다 — 필드 의미론만 바인딩합니다. 새 도메인은 profile 파일을 추가하며, 일반 명세는 순수하게 유지됩니다.

## 빠른 grep 쿡북(Quick grep cookbook)

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

전체 문법과 BNF 는 [`spec/kosmos.md`](spec/kosmos.md) 를, 작성된 예제 파일은 [`examples/`](examples/) 를 참조하세요.

## License

[CC0-1.0](LICENSE) — 동족 포맷과 동일. 퍼블릭 도메인 헌정(Public domain dedication).
