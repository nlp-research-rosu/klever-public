# K proof trust-boundary discovery

## Canonical scope

The exhaustive canonical inventory is `/reference/rule-inventory.json`, with
inventory SHA-256
`b3fa8a5381b9381ea830bab098cb994b6aa8b0c5dea0153f90dc993b7121880b`.
It contains exactly two rules, both from `MPY-VERIFICATION`. Each is classified
once and in canonical inventory order in `trust-boundary.json`.

Neither inventory rule carries the `simplification` attribute.

## Rule classifications

1. `rule-cdbb88438338221c6abc83e861a0d0f5d51ef2d0eb77a741b93d283454376efd`
   is a **DEFINITION**. It expands the named term `#solutionProgram` into the
   exact `Module(FuncDef(...))` constructor tree representing the translated
   solution. This is a macro-like structural helper naming the program used by
   the proof.

2. `rule-1ed36d8958dd79169cb11e8d42d25c3c76cf31afbf7f97146470ba0d49914dce`
   is a **DEFINITION**. It defines `#byLength(XS)` as the concatenation of the
   names from nine through one, each repeated according to that digit's count
   in `XS`. This is the named mathematical summary used as the postcondition.

The canonical verification-module inventory contains no
**OPERATIONAL_RULE** entries. Execution rules such as expression evaluation,
list addition, repetition, and counting occur in the Stage 1 semantics module,
but they are not members of the launcher-defined canonical inventory and are
therefore outside this classification list.

## Separately proved derived lemmas

There are no **PROVED_DERIVED_LEMMA** entries.

Stage 1 `prove.sh` compiles `semantic.k` with `MPY-VERIFICATION` already
included, then proves the single reachability claim in `spec.k`. It does not
first prove either inventory rule's exact statement against a module lacking
that rule and then reuse the proved statement. The failed `mutation-spec.k`
probe is negative validation of the proof harness, not evidence establishing a
reusable derived lemma.

## Domain lemmas

The **DOMAIN_LEMMA set is empty**. Neither canonical rule asserts an additional
trusted mathematical fact: one names the exact program AST and the other
defines the contract summary.
