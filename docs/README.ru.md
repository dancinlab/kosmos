<p align="center">
  <strong>κόσμος</strong>
</p>

<h1 align="center">⊙ kosmos</h1>

<p align="center"><strong>Мультимодальный манифест якорей знания (Multimodal Knowledge-Anchor Manifest)</strong> — координаты размещения ⊥ полезные нагрузки модальностей · кроссмодальная согласованность · привязка к profile</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-CC0--1.0-blue"></a>
  <img alt="Spec" src="https://img.shields.io/badge/spec-kosmos%2F1.0-success">
  <img alt="Entry-types" src="https://img.shields.io/badge/entry--types-2-informational">
  <img alt="Payload-forms" src="https://img.shields.io/badge/payload--forms-3-informational">
  <img alt="Sibling" src="https://img.shields.io/badge/sibling-tape%20·%20n6%20·%20hxc%20·%20n12-blueviolet">
</p>

<p align="center">Построчный · удобный для grep · надмножество tape v1.2 · размещение, не зависящее от модальности · семантика, определяемая profile</p>

<p align="center"><a href="../README.md">EN</a> · <a href="README.zh.md">中文</a> · Русский · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a></p>

---

`.kosmos` — это грамматика **мультимодального манифеста якорей знания (multimodal knowledge-anchor manifest)**: каждый файл описывает ровно один *якорь (anchor)* — точку/бассейн в абстрактном пространстве размещения — в виде двух ортогональных слоёв:

1. **Координаты размещения (Placement coordinates)** (`coord` / `lane` / `radius` / `tier` / `tags`) — *не зависят от модальности*. Местоположение якоря существует даже при нулевом количестве сенсорных каналов.
2. **Сенсорные полезные нагрузки (Sensory payloads)** (`@payload <modality> := …`) — *зависят от модальности*. Ноль или более каналов (text · image · audio · video · …, открытое перечисление), которые все стекаются в одно и то же размещение.

Файл `.kosmos` обязуется обеспечивать **кроссмодальную согласованность (cross-modal consistency)**: каждая полезная нагрузка, пройдя через свой модальный энкодер, должна оказаться в пределах `radius` от `coord`. Закрепление понятия сразу с многих сенсорных направлений фиксирует его прочнее, чем один канал, — формат и есть манифест этого совместного размещения (joint placement).

> [!NOTE]
> Пятый родственный формат после [`tape`](https://github.com/dancinlab/tape) (операционная / причинно-временна́я трасса), [`n6`](https://github.com/dancinlab/n6) (семантический / atlas-слой), [`hxc`](https://github.com/dancinlab/hxc) (байт-канонический провод) и [`n12`](https://github.com/dancinlab/n12) (12-осевой разреженный куб). `.kosmos` — это слой **размещения мультимодального якоря знания (multimodal knowledge-anchor placement)**: где фрагмент знания находится в абстрактном пространстве и какие сенсорные каналы его питают. Он ортогонален остальным четырём: `tape` — *что произошло*, `n6` — *что это значит*, `hxc` — *канонические байты*, `n12` — *проекция на разреженный куб*, `kosmos` — *где это закреплено и какими чувствами*.

## Кратко (At a glance)

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

## Два слоя, один якорь (Two layers, one anchor)

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

Координата одна; полезных нагрузок много. Это и есть мультимодальный `.kosmos`.

## Profiles

Базовая спецификация **не зависит от субстрата (substrate-independent)**: `coord` — это просто «точка в некотором абстрактном пространстве», `lane` — «идентификатор раздела» и так далее; их конкретный смысл фиксируется **profile**.

- [`spec/kosmos.md`](../spec/kosmos.md) — общая грамматика (без доменной физики).
- [`spec/profiles/anima-consciousness-carving.md`](../spec/profiles/anima-consciousness-carving.md) — первый profile: привязывает `coord` / `lane` / `radius` / `tier` / `tags` к парадигме CONSCIOUSNESS-CARVING агента `anima` (Living Consciousness Agent). Эталонная реализация: [`dancinlab/anima`](https://github.com/dancinlab/anima). Конкретные привязки доменной физики полностью находятся в этом файле profile.

Profile никогда не меняет грамматику — он лишь привязывает семантику полей. Новые домены добавляют файл profile; общая спецификация остаётся чистой.

## Краткий справочник по grep (Quick grep cookbook)

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

Полную грамматику и BNF см. в [`spec/kosmos.md`](../spec/kosmos.md), а проработанные файлы — в [`examples/`](../examples/).

## License

[CC0-1.0](../LICENSE) — то же, что и у родственных форматов. Передача в общественное достояние (Public domain dedication).
