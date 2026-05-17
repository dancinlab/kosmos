<p align="center">
  <strong>κόσμος</strong>
</p>

<h1 align="center">⊙ kosmos</h1>

<p align="center"><strong>多模态知识锚点清单（Multimodal Knowledge-Anchor Manifest）</strong> — 放置坐标 ⊥ 模态载荷 · 跨模态一致性 · 与 profile 绑定</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-CC0--1.0-blue"></a>
  <img alt="Spec" src="https://img.shields.io/badge/spec-kosmos%2F1.0-success">
  <img alt="Entry-types" src="https://img.shields.io/badge/entry--types-2-informational">
  <img alt="Payload-forms" src="https://img.shields.io/badge/payload--forms-3-informational">
  <img alt="Sibling" src="https://img.shields.io/badge/sibling-tape%20·%20n6%20·%20hxc%20·%20n12-blueviolet">
</p>

<p align="center">面向行 · 利于 grep · tape v1.2 超集 · 模态无关的放置 · 由 profile 定义语义</p>

<p align="center"><a href="../README.md">EN</a> · 中文 · <a href="README.ru.md">Русский</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a></p>

---

`.kosmos` 是一种**多模态知识锚点清单（multimodal knowledge-anchor manifest）**语法：每个文件恰好描述一个*锚点（anchor）*——抽象放置空间中的一个点/势阱——并将其表达为两个正交的层：

1. **放置坐标（Placement coordinates）**（`coord` / `lane` / `radius` / `tier` / `tags`）——*模态无关*。即使没有任何感官通道，锚点的位置依然存在。
2. **感官载荷（Sensory payloads）**（`@payload <modality> := …`）——*模态相关*。零个或多个通道（text · image · audio · video · …，开放枚举），它们全部汇入同一个放置位置。

一个 `.kosmos` 文件承诺**跨模态一致性（cross-modal consistency）**：每个 payload 一旦经过其模态编码器处理，都必须落在 `coord` 的 `radius` 范围之内。同时从多个感官方向锚定一个概念，比单一通道更牢固地将其钉住——该格式正是这一联合放置（joint placement）的清单。

> [!NOTE]
> 这是 [`tape`](https://github.com/dancinlab/tape)（操作 / 因果-时序 trace）、[`n6`](https://github.com/dancinlab/n6)（语义 / atlas 层）、[`hxc`](https://github.com/dancinlab/hxc)（字节正规线缆格式）和 [`n12`](https://github.com/dancinlab/n12)（12 轴稀疏立方体）之后的第五个同族格式。`.kosmos` 是**多模态知识锚点放置（multimodal knowledge-anchor placement）**层——一条知识位于抽象空间中的何处，以及由哪些感官通道供给它。它与那四者正交：`tape` 是*发生了什么*，`n6` 是*它意味着什么*，`hxc` 是*正规字节*，`n12` 是*稀疏立方体投影*，`kosmos` 是*它被锚定在哪里、由哪些感官锚定*。

## 概览（At a glance）

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

## 两个层，一个锚点（Two layers, one anchor）

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

坐标只有一个；载荷有多个。这就是一个多模态的 `.kosmos`。

## Profiles

基础规范是**与底层无关（substrate-independent）**的：`coord` 只是“某个抽象空间中的一个点”，`lane` 只是“一个分区 id”，依此类推——它们的具体含义由一个 **profile** 固定。

- [`spec/kosmos.md`](../spec/kosmos.md) — 通用语法（不含领域物理）。
- [`spec/profiles/anima-consciousness-carving.md`](../spec/profiles/anima-consciousness-carving.md) — 第一个 profile：将 `coord` / `lane` / `radius` / `tier` / `tags` 绑定到 `anima` 这一 Living Consciousness Agent 的 CONSCIOUSNESS-CARVING 范式。参考实现：[`dancinlab/anima`](https://github.com/dancinlab/anima)。具体的领域物理绑定完全位于该 profile 文件中。

profile 永远不会改变语法——它只绑定字段语义。新领域添加一个 profile 文件；通用规范保持纯净。

## 快速 grep 手册（Quick grep cookbook）

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

完整语法与 BNF 见 [`spec/kosmos.md`](../spec/kosmos.md)，已写好的示例文件见 [`examples/`](../examples/)。

## License

[CC0-1.0](../LICENSE) — 与同族格式相同。公共领域贡献声明（Public domain dedication）。
