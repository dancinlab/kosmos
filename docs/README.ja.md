<p align="center">
  <strong>κόσμος</strong>
</p>

<h1 align="center">⊙ kosmos</h1>

<p align="center"><strong>マルチモーダル知識アンカー・マニフェスト（Multimodal Knowledge-Anchor Manifest）</strong> — 配置座標 ⊥ モダリティ・ペイロード · クロスモーダル整合性 · profile 束縛</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-CC0--1.0-blue"></a>
  <img alt="Spec" src="https://img.shields.io/badge/spec-kosmos%2F1.0-success">
  <img alt="Entry-types" src="https://img.shields.io/badge/entry--types-2-informational">
  <img alt="Payload-forms" src="https://img.shields.io/badge/payload--forms-3-informational">
  <img alt="Sibling" src="https://img.shields.io/badge/sibling-tape%20·%20n6%20·%20hxc%20·%20n12-blueviolet">
</p>

<p align="center">行指向 · grep フレンドリー · tape v1.2 のスーパーセット · モダリティ非依存の配置 · profile が定義する意味論</p>

<p align="center"><a href="../README.md">EN</a> · <a href="README.zh.md">中文</a> · <a href="README.ru.md">Русский</a> · 日本語 · <a href="README.ko.md">한국어</a></p>

---

`.kosmos` は **マルチモーダル知識アンカー・マニフェスト（multimodal knowledge-anchor manifest）** の文法です。各ファイルはちょうど 1 つの *アンカー（anchor）*——抽象的な配置空間における点／盆地——を、直交する 2 つの層として記述します。

1. **配置座標（Placement coordinates）**（`coord` / `lane` / `radius` / `tier` / `tags`）——*モダリティ非依存*。感覚チャネルがゼロであっても、アンカーの位置は存在します。
2. **感覚ペイロード（Sensory payloads）**（`@payload <modality> := …`）——*モダリティ依存*。0 個以上のチャネル（text · image · audio · video · …、オープン列挙）が、すべて同一の配置へと流れ込みます。

`.kosmos` ファイルは **クロスモーダル整合性（cross-modal consistency）** を約束します。すなわち、各ペイロードはそのモダリティ・エンコーダを通過した後、必ず `coord` の `radius` 以内に着地しなければなりません。1 つの概念を多数の感覚方向から同時にアンカリングすることは、単一チャネルよりもその概念をより強固に固定します——このフォーマットは、その共同配置（joint placement）のマニフェストです。

> [!NOTE]
> [`tape`](https://github.com/dancinlab/tape)（オペレーショナル／因果-時間的トレース）、[`n6`](https://github.com/dancinlab/n6)（意味論／atlas 層）、[`hxc`](https://github.com/dancinlab/hxc)（バイト正準ワイヤ）、[`n12`](https://github.com/dancinlab/n12)（12 軸スパースキューブ）に続く 5 番目の同族フォーマットです。`.kosmos` は **マルチモーダル知識アンカー配置（multimodal knowledge-anchor placement）** 層であり、知識の断片が抽象空間のどこに位置し、どの感覚チャネルがそれを供給するかを表します。これは他の 4 つと直交します。`tape` は *何が起きたか*、`n6` は *それが何を意味するか*、`hxc` は *正準バイト列*、`n12` は *スパースキューブ射影*、`kosmos` は *どこにアンカリングされ、どの感覚によるか* です。

## 概要（At a glance）

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

## 2 つの層、1 つのアンカー（Two layers, one anchor）

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

座標は 1 つ、ペイロードは多数。それがマルチモーダルな `.kosmos` です。

## Profiles

基本仕様は **基盤非依存（substrate-independent）** です。`coord` は単に「ある抽象空間内の 1 点」、`lane` は「パーティション id」などであり、それらの具体的な意味は **profile** によって固定されます。

- [`spec/kosmos.md`](../spec/kosmos.md) — 一般文法（ドメイン物理を含まない）。
- [`spec/profiles/anima-consciousness-carving.md`](../spec/profiles/anima-consciousness-carving.md) — 最初の profile：`coord` / `lane` / `radius` / `tier` / `tags` を、Living Consciousness Agent である `anima` の CONSCIOUSNESS-CARVING パラダイムに束縛します。リファレンス実装：[`dancinlab/anima`](https://github.com/dancinlab/anima)。具体的なドメイン物理の束縛は、すべてその profile ファイル内に存在します。

profile は文法を決して変更しません——フィールドの意味論を束縛するだけです。新しいドメインは profile ファイルを追加します。一般仕様は純粋なまま保たれます。

## grep クックブック（Quick grep cookbook）

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

完全な文法と BNF は [`spec/kosmos.md`](../spec/kosmos.md) を、作成済みのサンプルファイルは [`examples/`](../examples/) を参照してください。

## License

[CC0-1.0](../LICENSE) — 同族フォーマットと同じ。パブリックドメイン献呈（Public domain dedication）。
