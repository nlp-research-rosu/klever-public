# Trust-boundary discovery

The canonical inventory has SHA-256
`6fdd0cbfc0fcd25cfdce05c3a734b3788c827b816a694cad314c9821edce6a7c`
and contains one rule. The classification preserves that inventory order and
covers its sole `source_rule_id` exactly once.

## Classification

`rule-163a865d82cdbf32cce773c75722becea55fcde50e42abef6f61661a7069c3a7`
is a `PROVED_DERIVED_LEMMA`. It summarizes execution of `lsiLoopBody` over
`list(intVals(IS))`: it consumes the loop, updates `largest_negative` with
`scanNeg`, updates `smallest_positive` with `scanPos`, and records the final
loop variable through `lastValue`, under the same `N <=Int 0` and
`P >=Int 0` guard as the separately proved claim.

Although the finalized rule carries `priority(40)` so the verification model
can reuse it as a rewrite, the mounted evidence shows that its exact
reachability statement was established independently before the rule was
added to the model. It therefore meets the required definition of a proved
derived lemma rather than an operational rule or a trusted domain lemma.

## Separately proved derived-lemma evidence

There is exactly one separately proved derived lemma:

1. In `/reference/k-proof/prove.sh`, lines 28–34 compile
   `verification-core.k` with main module `VERIFICATION-CORE`, then prove
   `loop-spec.k` against that compiled definition.
2. `verification-core.k` does not contain the loop-summary rule, and
   `verification-core-kompiled/mainModule.txt` confirms that the proof
   definition's main module is `VERIFICATION-CORE`. The corresponding
   `#loop(list(intVals(...)))` summary is also absent from
   `verification-core-kompiled/allRules.txt`.
3. The `[loop-connection]` claim in `/reference/k-proof/loop-spec.k` has the
   same initial and final `<k>` terms, `<env>` value, scope updates, closure
   binding, builtin scope, and side condition as the canonical inventory rule.
   The inventory rule adds only its reuse priority.
4. `/reference/k-proof/prove.log` records `#Top` for this second positive proof
   at line 271. Only afterward does `prove.sh`, at lines 36–42, compile
   `verification.k` containing the reusable rule and run the target proof.

Thus the exact rule is first proved against a module that lacks it, and the
successful result precedes its use by the finalized verification module.

## Trust-boundary summary

- `DEFINITION`: 0
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 1
- `DOMAIN_LEMMA`: 0

The domain-lemma set is empty. The canonical inventory contains no rule with
the `simplification` attribute.
