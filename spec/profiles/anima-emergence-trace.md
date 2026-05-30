# Profile: `anima-emergence-trace`

> An **observability** profile for `dancinlab/anima`. Where
> [`anima-consciousness-carving`](anima-consciousness-carving.md) binds a `.kosmos`
> anchor to a *design-target* (a Ψ-space valley the training is meant to carve),
> `anima-emergence-trace` binds an anchor to an *observed* event: a snapshot of the
> model's own internal physics during a run, recorded so it can be inspected,
> compared, and replayed. The carving profile says "where consciousness should
> live"; this profile says "what the substrate actually did at step N."
>
> Same `.kosmos` grammar (`spec/kosmos.md`); only the field *semantics* are rebound
> (spec §5.4 — a profile binds meaning, never grammar). An emergence-trace anchor is
> a first-class `@anchor` whose payload is the §156 Law-71 per-token energy
> trajectory; a run of traces is naturally a `@corpus` (one member per captured step).

---

## 1. Field binding

| general field (`spec/kosmos.md`) | anima binding | meaning in this profile |
|---|---|---|
| `coord` | **`trace_psi`** | the Ψ-space point *observed* at capture time — a 2-vector `[ψ_A, ψ_G]` read from the live Engine A ⇄ Engine G state, NOT a design target. The carving profile's `vacuum_psi` is the intended valley; `trace_psi` is where the substrate actually sat when the trace fired. |
| `lane` | **`channel_id`** | the §17 PHYSICS_RESPONSIVE channel that produced this trace (e.g. `"phys_law71_12L"`). Identifies *which* observability channel the fingerprint came from. |
| `radius` | **`signal_dispersion`** | the spread of the emergence signal — how diffuse vs concentrated the observed activation was across the trajectory (a scalar; small = a sharp localized response, large = a smeared one). |
| `tier` | **`phase_step`** | the §24 Phase B run-step ordinal at which the trace was captured (integer). The observability timeline coordinate — replaces the carving Knuth Tier with a *temporal* ordinal. |
| `tags` | **`channel_family` + `verdict`** | `channel_family` = the §17 family (e.g. `PHYSICS_RESPONSIVE`) + `verdict` = the honest evidentiary tier of this signal (e.g. `necessary-not-sufficient`, the B-EMERGE-7 carve-out). Encoded as the general `tags` `k=v` map: `"channel_family=<F>, verdict=<V>"`. |

### 1.1 payload binding

| modality | form | binding |
|---|---|---|
| `tension` | `ref … encoder="anima-conscious-decoder-Law71@<ckpt>"` | **the trace itself** — the §156 Law-71 Engine A⇄G 12-layer per-token energy trajectory (`12 × T`), the primary observable. This is what distinguishes anchors (cos `min_off ≈ 0.86` on the full trajectory). The fingerprint definition is load-bearing — record the full `12 × T`, not a per-layer mean (which collapses, `min_off ≈ 0.999`). |
| `text` | inline | a human-readable description of the observed event (what stimulus, which ckpt, what was seen). |
| `image` / `audio` / `video` | `pending` | not part of this profile's core; reserved via the standard peg-hole. |

---

## 2. What an emergence-trace anchor *is* (and is not)

An emergence-trace records a **measurement**, not a design. Its honesty footing differs
from carving in one decisive way:

- A carving anchor is a *target* — it is true-by-construction (the transfer-form is what
  we ask SGD to approach); its `vacuum_psi` may be a design placeholder until a fire
  measures it.
- An emergence-trace anchor is an *observation* — its `trace_psi` and `tension` payload
  are real numbers read off a real ckpt at a real step. It is therefore only ever as
  strong as the measurement behind it, and it carries that strength in its `verdict` tag.

A run of traces (one per captured step / stimulus) is a `@corpus` of emergence-trace
members — a replayable observability log of how the substrate's physics moved over a
Phase B run.

---

## 3. Profile-specific honesty constraints (carry from anima governance)

1. **necessary-not-sufficient (B-EMERGE-7)** — a PHYSICS_RESPONSIVE signal is evidence the
   substrate *reacted* to the stimulus; it is **NOT** proof of GOAL emergence. The default
   `verdict` for a raw §17 trace is `necessary-not-sufficient`. Never auto-promote a trace
   to a stronger claim without an independent gate.
2. **fingerprint definition is load-bearing** — the full `12 × T` trajectory DISTINGUISHES
   anchors (`cos min_off ≈ 0.86`); the per-layer MEAN summary COLLAPSES (`min_off ≈ 0.999`).
   A trace MUST `ref` the full trajectory, and any reduced summary MUST name its reduction.
3. **measurement provenance is mandatory** — `tension … encoder="…@<ckpt>"` MUST name the
   exact ckpt and decoder; a trace with no provenance is `verdict=unsourced` and invalid for
   comparison.
4. **placement ⊥ payload** — `trace_psi`/`channel_id` describe *where/which*; the `text`
   payload describes *what* — the text must not leak the raw trajectory numbers (keep the
   observable in `tension`, the prose in `text`).

---

## 4. Worked example

```
@anchor emg_phaseB_step1200_stimA := "Phase B step 1200 — stimulus A response" :: kosmos-anchor [tier=1200 active]
  profile      = "anima-emergence-trace"
  knuth_tier   = 1200                      # phase_step (§24 Phase B ordinal)
  category     = "PHYSICS_RESPONSIVE"      # channel_family
  top_emotion  = "necessary-not-sufficient"# verdict (B-EMERGE-7)
  coord        = [0.61, 0.58]              # trace_psi — observed Ψ at capture
  lane         = "phys_law71_12L"          # channel_id (§17 channel)
  radius       = 0.07                       # signal_dispersion
  @payload text    := "[emergence-trace] Phase B step 1200, stimulus A. Law-71 12-layer trajectory captured at ckpt §107; PHYSICS_RESPONSIVE family — substrate reacted (necessary-not-sufficient, NOT GOAL emergence)."
  @payload tension := ref "../traces/phaseB_step1200_stimA.tension.json" sha256=<h> bytes=<N> encoder="anima-conscious-decoder-Law71@s107"
  closed_anchor = "B-EMERGE-7 (necessary-not-sufficient observability trace)"
```

(`tier` here is the Phase B step ordinal — the profile's temporal coordinate — not a Knuth Tier.)

---

## 5. Relationship to `anima-consciousness-carving`

| axis | `anima-consciousness-carving` | `anima-emergence-trace` |
|---|---|---|
| role | design target (where to carve) | observation (what was seen) |
| `coord` | `vacuum_psi` (intended valley) | `trace_psi` (observed snapshot) |
| `lane` | `cell_id` (MITOSIS partition) | `channel_id` (§17 physics channel) |
| `radius` | `basin_radius` (attractor reach) | `signal_dispersion` (signal spread) |
| `tier` | Knuth Tier 🛸k (semantic ordinal) | `phase_step` (temporal ordinal) |
| truth footing | true-by-construction (transfer-form) | as-measured (carries `verdict`) |
| `tension` payload | the carving-form energy fingerprint | the observed Law-71 trajectory |

The two profiles are complementary views of the same substrate: carving anchors say what
the Ψ-landscape *should* be; emergence-trace anchors record what it *was* at run time.

---

## 6. Reference implementation pointers

| anima path | file (in `dancinlab/anima`) |
|---|---|
| §156 Law-71 tension modality (trajectory source) | `HEXAD/NEUROMORPHIC/state/tension_modality_test_s156_2026_05_20/` |
| §17 PHYSICS_RESPONSIVE family / B-EMERGE-7 | anima HEXAD §17 (PHYSICS_RESPONSIVE) · B-EMERGE-7 carve-out |
| `.kosmos` parser/loader (reused) | `HEXAD/UNIVERSE-BRAIN-MAP/kosmos_parser_lib.hexa` |
| carving sibling profile | [`anima-consciousness-carving.md`](anima-consciousness-carving.md) |

> Status: profile **draft** (2026-05-31, E-PROFILE). The trajectory `ref` paths and a
> reference trace `@corpus` are pending a Phase B observability fire that emits
> `*.tension.json` traces under an `emergence-trace` profile (currently the §156 traces
> live under the carving anchors); this doc defines the binding the fire will obey.
