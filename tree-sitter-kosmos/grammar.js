/**
 * tree-sitter grammar for .kosmos (multimodal knowledge-anchor manifest).
 *
 * Total line model, no external scanner, no regex look-around. Every
 * line token requires a trailing newline → the top-level repeat always
 * progresses. .kosmos is a superset of tape v1.2: one column-0 `@anchor`
 * entry + 2-space body lines, with `@payload <modality> :=` payloads.
 * Exposes `anchor_kw` / `payload_kw` / `edge_op` / `comment` for
 * queries/highlights.scm; coordinate fields and prose fall through to
 * `body`. Block structure is the LSP's job.
 */
module.exports = grammar({
  name: 'kosmos',

  extras: $ => [],

  rules: {
    source_file: $ => repeat($._line),

    _line: $ => choice(
      $.blank,
      $.comment,
      $.anchor,
      $.payload,
      $.edge,
      $.body,
      $.text,
    ),

    blank: $ => token(prec(1, /[ \t]*\n/)),

    comment: $ => token(prec(5, /[ \t]*#[^\n]*\n/)),

    // column-0 `@anchor <id> := "<name>" :: kosmos-anchor [...]`
    anchor: $ => seq($.anchor_kw, $._rest),

    anchor_kw: $ => token(prec(5, '@anchor')),

    // 2-space body `@payload <modality> := ...`
    payload: $ => seq($._indent, $.payload_kw, $._rest),

    payload_kw: $ => token(prec(5, '@payload')),

    edge: $ => seq($._indent, $.edge_op, $._rest),

    body: $ => seq($._indent, $._rest),

    _indent: $ => token(prec(3, /[ \t]+/)),

    // tape v1.2 edge alphabet (12)
    edge_op: $ => token(prec(4, choice(
      '<-', '->', '=>', '==', '~>', '|>', '!!',
      '<:', ':>', '?>', '!>', '@>',
    ))),

    _rest: $ => token(prec(1, /[^\n]*\n/)),

    text: $ => token(prec(0, /[^ \t#@\n][^\n]*\n/)),
  },
});
