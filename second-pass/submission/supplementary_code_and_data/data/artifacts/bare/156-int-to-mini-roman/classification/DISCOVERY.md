# Trust-boundary discovery

The canonical inventory hash is
`15b0fdae4ecec18050cdc11d01d501b659713a2e964097a347e97dce027fe12e`.
Its two rules are classified once each, in inventory order.

## Definitions

- `rule-00b13407b775d8f7c54a7237162b4d7ce28eaf42ee68f04dbd2bceab22d62733`
  is `romanProgram => Module(...)`. The `romanProgram` production is marked
  `macro`, and the rule expands that named ground proof term to the submitted
  Mini-Python AST. Stage 1's `kast --expand-macros`/`diff` check confirms that
  this expansion matches `solution.mpy`; the rule remains a macro definition.
- `rule-54c74217ad8efd4f90535b99e49caf9d7c1180c37fabc1b60442f6ab239a9b13`
  is `miniRoman(N) => ...`. It defines the expected Roman-numeral summary from
  the thousands, hundreds, tens, and ones tables and decimal-place arithmetic.
  The final claim refers to this named specification function.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The Stage 1 `prove.sh` has one `kprove` invocation, proving the
`int-to-mini-roman-correct` claim from `spec.k` against
`verification-kompiled`. That definition is compiled from `verification.k`
with both inventory rules already present. Stage 1 contains no earlier proof
against a module omitting either rule, and contains no proof whose exact
statement is later installed as a reusable rule. The macro-expansion `diff`
and the concrete `krun` checks are validation evidence, but they do not meet
the required prior-`kprove` evidence and ordering for a proved derived lemma.

## Domain lemmas

The domain-lemma set is empty. Neither inventory rule adds an independent
mathematical fact: both introduce named definitions used by the proof.
