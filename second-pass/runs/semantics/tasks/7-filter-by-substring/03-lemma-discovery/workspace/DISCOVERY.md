# K proof trust-boundary discovery

The canonical inventory identifies 17 rules in the local
`FILTER-VERIFICATION` module closure. Each inventory rule is classified exactly
once in `trust-boundary.json`, in canonical inventory order.

## Definitions

Rules 1–2 define the structural conversion from the proof-side `StrSeq`
representation to semantic string values. Rules 9–11 are the base and two
conditional recursive equations for the mathematical filter accumulator, and
rule 12 names the empty-accumulator instance as `filterStrings`. Rules 13–14
define the recursive `lastCodes` structural helper. Rules 15–17 are macro
expansions for the exact translated loop body, function body, and program.

The two rules carrying the `simplification` attribute are rules 10 and 11.
Both are classified as `DEFINITION`: together with rule 9 they are the
case-split recurrence defining the filter summary, rather than independent
mathematical facts.

## Operational verification rules

Rules 3–5 give the verification model's execution behavior for iterating the
typed `strVals` representation: dispatch, empty completion, and nonempty yield.
Rules 6–8 give its observation behavior for symbolic substring comparison:
dispatch to an explicit decision state, followed by the true and false cases
according to the supplied reference-semantic `strContains` function. These
rules extend the operational model for proof-side terms; they do not state
additional mathematical lemmas.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` classifications.

The Stage 1 `prove.sh` first compiles `verification.k` as
`FILTER-VERIFICATION` and then runs `kprove spec.k` against that compiled
definition. Thus every one of the 17 inventory rules is already present in the
definition used to prove the two claims in `spec.k`. Stage 1 does prove the
loop reachability invariant and the end-to-end correctness claim, but neither
claim is an inventory rule, and there is no earlier proof against a module
omitting an inventory rule followed by reuse of an exactly corresponding
rule. Consequently the mounted evidence does not satisfy the required
ordering or exact-correspondence test for any derived-rule classification.

## Domain lemmas

The domain-lemma set is empty. No inventory rule is classified as
`DOMAIN_LEMMA`; the non-definitional inventory rules are operational rules of
the verification model.
