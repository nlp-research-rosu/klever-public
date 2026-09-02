# Trust-boundary discovery

## Scope and method

`/reference/rule-inventory.json` is the exhaustive canonical inventory for the
local verification-module closure. It identifies one closure module,
`VERIFICATION`, and seven source rules. This report classifies those seven
rules only; rules in the supplied reference semantics are outside this
launcher-generated local inventory.

The canonical inventory hash copied into `trust-boundary.json` is:

```text
03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52
```

Classification was based on each canonical rule text plus the mounted Stage 1
`verification.k`, `prove.sh`, and `PROOF.md`. Comments in Stage 1 were treated
as explanations, not as machine-checked derivations.

## Definitions

Four rules are `DEFINITION`:

1. `rule-ea80c64ba3e52dd72b25433dd6dd721d97e283355279ee9fc2a39f905f582faa`
   is the `I >= N` base equation for `mergeThirdFrom`.
2. `rule-8eaaf331b2562006a2a6f4704a4b81a167862611d6c8b82d78a59369cb08a019`
   is its divisible-by-three recurrence, selecting from the sorted third-value
   sequence.
3. `rule-4860445cf3432071a9a322001c5e3ce052bb80b75147a784f2df24a8fbba41ca`
   is its complementary recurrence, selecting from the original sequence.
4. `rule-0855e7c5303f3b1835ec56db22a573c2fc2903b161c139dd7b0ff4a1d1ee9ed0`
   folds the exact complete `mergeThirdFrom` expression into the named
   `sortThirdResult` proof summary.

The first three are a guarded recurrence defining a mathematical result. The
fourth carries `simplification`, but it is still definitional: it introduces a
solver-friendly name for that exact complete result. None matches a K
configuration cell or replaces an MPY execution step.

## Operational rules

The local inventory contains no `OPERATIONAL_RULE`. Every inventoried rule
rewrites a pure mathematical/proof-summary term. The operational Python model
is imported from the supplied reference semantics, whose rules are not present
in this canonical local inventory.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The required evidence ordering is absent for every candidate. Stage 1
`prove.sh` first compiles:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

That `verification.k` already contains all seven canonical rules. Both
successful `kprove` commands then use `verification-kompiled`. There is no
earlier command that proves the exact zero-length, associativity, or
right-identity statement against a module from which the corresponding rule is
absent. The successful program and loop claims therefore demonstrate closure
under those rules, not independent proofs of the rules themselves.

In particular, the comments in `verification.k` and the prose in `PROOF.md`
that describe the concatenation laws as derived by structural induction are
not Stage 1 machine-checked proof evidence satisfying the required ordering.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly three rules:

1. `rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2`
   reduces `sortThirdResult(VS)` to the empty sequence under
   `vsLen(VS) <=Int 0`. It is a consequence expected from the summary
   definitions and length domain, but Stage 1 trusts it as a simplifier rather
   than first proving its exact guarded statement.
2. `rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918`
   asserts associativity of `valSeqConcat`.
3. `rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9`
   asserts right identity of `valSeqConcat`.

All three carry the `simplification` attribute and are classified as
`DOMAIN_LEMMA`, as required for unproved mathematical simplifiers. The two
concatenation rules state reusable facts about the pre-existing
`valSeqConcat` definition. The zero-length rule is also additional to the
primary complete-result folding definition and was available while Stage 1
proved its target claims.

## Completeness

`trust-boundary.json` preserves canonical inventory order, contains seven
entries for seven canonical rules, and assigns each `source_rule_id` exactly
once. No theorem statement, Lean content, replacement rule, or alternative
formulation is included in the JSON.
