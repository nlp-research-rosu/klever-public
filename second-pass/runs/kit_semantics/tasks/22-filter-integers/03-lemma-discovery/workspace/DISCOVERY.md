# Trust-boundary discovery

The canonical inventory at `/reference/rule-inventory.json` contains five
rules, all from the local `VERIFICATION` module. Each canonical
`source_rule_id` appears exactly once in `trust-boundary.json`, in inventory
order, and the copied inventory hash is
`ffdd03dae916c92bbeabedc0a48396bb3bec96dd06d1b7dedba0533f4cd5d4ae`.

## Classifications

- `rule-7a8aefa8550c8a06b16a409b5174a955c92023c5c954b847bc146b10750b669d`
  is `DEFINITION`. It expands the nullary `filterLoopBody` macro into the
  loop-body AST used by the claims. It defines a named proof term and does not
  add an execution or mathematical rule.
- `rule-8e8f01b5e0fd33ceb875a3d4d5eaaabb18bf343c33360eb7a965dd98e22a8685`
  is `DEFINITION`. It expands `filterBody` into the exact function-body
  statement sequence.
- `rule-55b672e7a2348769766678767d4f1ec37801c590e4687ecb281112debaebe350`
  is `DOMAIN_LEMMA`. It is a `simplification` equation for the already-defined
  semantic function `isIntV`, not a definition of a new proof symbol. It adds
  the symbolic-domain fact that `isIntV(V)` equals `isInt(V) orBool isBool(V)`
  for every `V:Val`, and the target proof relies on that fact to close symbolic
  classifier branches.
- `rule-577aa383be88832d9bea1ce3fa32e88bef61a50c8c009c29dd02cc4ee6b8dec4`
  is `DEFINITION`. It is the `.ValSeq` base equation of the total `filterAcc`
  summary.
- `rule-f78e3bc6b47e926e3c06b48a1fe9acb3eb68fda26c3b17ee0c8eb4ad23dfcd03`
  is `DEFINITION`. It is the `vCons` recurrence of `filterAcc`, with strict
  structural descent through `REST`.

No inventoried rule is an `OPERATIONAL_RULE`: the two body rules are macro
definitions, the two `filterAcc` rules define a mathematical summary, and the
remaining rule is an added mathematical simplification fact.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules.

The mounted Stage 1 `prove.sh` first compiles `verification.k`, including the
`isIntV` simplification rule, into `verification-kompiled`. It then proves
`spec.k` against that already-extended definition. The classifier and
non-integer mutation probes also import `VERIFICATION` and run against the same
compiled definition. Their expected failures provide sensitivity evidence, but
they do not first prove the exact simplification equation in a module from
which that equation is absent. Consequently neither the `#Top` target output
nor the mutation logs satisfy the required ordering for
`PROVED_DERIVED_LEMMA`.

Although the Stage 1 report informally calls the `isIntV` equation a derived
lemma, comments and report labels are not proof evidence under the discovery
classification rule.

## Domain-lemma set

The domain-lemma set is **not empty**. It contains exactly:

```text
rule-55b672e7a2348769766678767d4f1ec37801c590e4687ecb281112debaebe350
```

This classification identifies the exact additional mathematical fact trusted
by the finalized K proof; it does not introduce or restate any alternative
theorem.
