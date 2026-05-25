@V := "tape" :: spec [active]
  version = "1.2"

@I := "kosmos" :: identity [active]
  kind     = "Multimodal knowledge-anchor manifest format (placement coordinates ⊥ modality payloads)"
  brief    = "Anima CONSCIOUSNESS-CARVING as first profile."
  parent   = "dancinlab"
  ssot     = "github.com/dancinlab/kosmos (`hx install kosmos`)"
  siblings = "hexa-lang · anima"

@D k_spec_ssot := "spec is grammar SSOT — profiles bind semantics, never grammar" :: governance [required active]
  do   = "`spec/kosmos.md` = single grammar SSOT"
  do   = "a profile binds field semantics (coord/lane/radius/tier/tags) ONLY, never grammar"
  dont = "change grammar inside a profile · fork the spec · add a field outside spec"

@D k_orthogonal := "placement ⊥ payload — coord is modality-independent" :: governance [required active]
  do   = "keep placement (coord·lane·radius·tier·tags) separable from payloads"
  do   = "anchor location exists with zero sensory channels"
  dont = "entangle a coord with a modality · require a payload for placement validity"

@D k_cross_modal := "cross-modal consistency is the core invariant" :: governance [required active]
  do   = "every materialized payload, once encoded, lands within `radius` of `coord`"
  do   = "un-materialized channels use `:= pending \"<reason>\"`"
  dont = "ship a non-pending payload that violates radius · fake cross-modal consistency"

@D k_line_oriented := "line-oriented · grep-friendly · tape v1.2 superset" :: governance [required active]
  do   = "stay a strict tape v1.2 superset · exactly one `@anchor` per file, at the top"
  do   = "one entry per line so `grep '^@anchor '` / `^  @payload ` stay reliable"
  dont = "multi-anchor files · multi-line entries that break line-grep · binary-only bodies"

@D k_payload_forms := "exactly 3 payload forms — inline · ref+sha256 · pending" :: governance [required active]
  do   = "inline · ref+sha256 · pending — open modality enum (text·image·audio·video·…)"
  dont = "invent a 4th payload form · ref without sha256 · pending without a reason"

@D k_hexa_native := "tooling is hexa-native — parser · emitter · LSP in hexa" :: governance [required active]
  do   = "author parser/emitter/anchor/LSP in hexa-lang (family = hexa-lang · anima)"
  do   = "`hexa check` clean"
  dont = "add new `.py` / `.sh` tooling · keep a non-hexa canonical LSP"
