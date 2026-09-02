# Trust-boundary rule discovery

## Canonical inventory and integrity

The exhaustive input is `/reference/rule-inventory.json`, with
`inventory_sha256`
`2ed8f1e00a992ffb3f759fe8c7c61e8766ab82bbf0e80ff4f6562940c03a1e93`.
It contains eight rules, in one verification-module closure:
`VERIFICATION`.

The inventory records verification source hash
`d019861f570f855722bb54971461cbe467b7e369e9240c150647a0a8c1b1c0c1`.
Computing SHA-256 directly over the mounted
`/reference/k-proof/verification.k` produced the same value. No mounted Stage 1
artifact was modified or copied.

## Rule classifications

Every canonical rule is classified exactly once, in inventory order:

| Source rule | Classification | Reason |
|---|---|---|
| `rule-0a82089db438d6896e57def6a6d687fd829e250b2e3a57f86e1114728cabfd3d` | `DEFINITION` | The guarded zero case defines `binRel` by comparing its accumulator and output. |
| `rule-311c7818aa61ab48edceaaf524aa96cdc5343c25e35edeb7b7895c50438f7e39` | `DEFINITION` | The guarded positive case is the descending quotient-and-remainder recurrence defining `binRel`. |
| `rule-73d9b9e52c4141a668b87a1bda99e477853f9ac07bdde4e178dff6db56018487` | `DEFINITION` | The negative case completes the disjoint sign partition of the total `binRel` summary. |
| `rule-bb0dd8b44a02de305b300de162887fd197bafc6ab3bffe93bdff08e62e6f569e` | `DEFINITION` | The zero case defines the required tail codes for `decimalTailRel`. |
| `rule-288f1d1aa76e8c443e284a26c6a3ffaa6dc11746b856850011993c220b27b228` | `DEFINITION` | The positive case defines `decimalTailRel` by composing it with `binRel` and the trailing wrapper. |
| `rule-b28ffaf5f18a64587bbe6d9f806d4536c273d62a4236f1341522cafaef664d27` | `DEFINITION` | The negative case completes the disjoint sign partition of the total `decimalTailRel` summary. |
| `rule-7c2e6fd20be28dd4a2b6f16a4389ef39d505f39f3f321b7eab857f76d1bf7526` | `DEFINITION` | The structural leading-wrapper case defines `decimalResultRel` by delegating its tail. |
| `rule-c6ae0b2b0ab8b9dfc28262926c22380fb803f9275d4e040bba7d777a9d8c61d9` | `DEFINITION` | The `owise` complement defines every other `decimalResultRel` shape as false. |

These rules rewrite only the proof-local Boolean functions `binRel`,
`decimalTailRel`, and `decimalResultRel`. They do not match `<k>` or any state
cell and therefore do not execute or observe the Python model. Consequently,
the `OPERATIONAL_RULE` set is empty.

The inventory has no rule carrying the `simplification` attribute. Seven rules
have no attributes; the final structural complement carries only `owise`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

Stage 1 `prove.sh` first compiles `verification.k` with `VERIFICATION` as the
main module (lines 16–20), so all eight canonical rules are already installed.
It then runs `kprove spec.k` against that compiled definition (lines 22–24);
`spec.k` imports `VERIFICATION`. The single `#Top` at line 149 of
`prove-stage1.log` is therefore evidence for the two reachability claims under
the complete verification module, not evidence that the exact statement of
any inventory rule was first proved in a module omitting that rule.

`SPEC.binary-loop` is a reachability circularity proved as part of that
`kprove` invocation. It is not one of the canonical inventory rules and is not
subsequently installed as a reusable rule, so it does not create a
`PROVED_DERIVED_LEMMA` classification in this ledger.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. None of the eight rules asserts an additional
trusted arithmetic or mathematical fact: each is an equation, recurrence, or
structural/totalization case defining one of the three named proof summaries.
