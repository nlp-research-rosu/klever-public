# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`. Its embedded
`inventory_sha256` is
`2d87f8c3a92e823f4d0d371615d6dcd90d727062ca2f8b6781053a4aa3c5c0b1`.
It contains 10 rules, all in module `VERIFICATION`; the output preserves their
canonical order and classifies every `source_rule_id` exactly once.

The inventory reports no rule with a `simplification` attribute. Inspection of
the mounted `verification.k` confirms that every inventoried rule is an
equation for a symbol declared `[function, total]`. None matches a `<k>` term,
configuration cell, call, continuation, or other operational state.

## Classification result

All 10 rules are `DEFINITION`:

| Inventory position | Rule | Reason |
|---:|---|---|
| 1 | `rule-fb20023f3ba749b6a41948fafafdc7905c1e57b1259087a8c997c632a8bd73f2` | Empty-input base equation for `scanParenGroups`. |
| 2 | `rule-f583a745ad66ed7a6e6edb157fb92dfc7e453138bc5a043f0dbf0e242b8b1744` | Nonempty-input structural recurrence for `scanParenGroups`; every recursive branch consumes `REST`. |
| 3 | `rule-266caab93c8c959eb43fe3fde11de8216d1c60cd5431406325b896207f56d732` | Initializing equation for the named specification `separateParenGroupsSpec`. |
| 4 | `rule-5fa22cb1d66dafd2b9bada586c05b79c0cfe0cec65e7a2a55e378bb073ccb99d` | Initializing equation for `validParenInput`. |
| 5 | `rule-9297847690746ec6b7a953f8ec6199c0cc1ca947667b52a9a763ada9a8a90526` | Empty-suffix base equation for the input predicate. |
| 6 | `rule-faaebe512f2fb221e1c01b55fc337a2320d72bde4bf95cc458f645a1f22a570e` | Space-skipping recurrence for the input predicate. |
| 7 | `rule-ef55521d20d979a944b03b4a5c2b520ede0470c003e497a95cb3a64e4368cebd` | Opening-parenthesis recurrence for the input predicate. |
| 8 | `rule-0d136db51cb932ee0db51ebee82648fe6326c816b2b001c977a27e11a6dd3536` | Positive-depth closing-parenthesis recurrence. |
| 9 | `rule-19f01337879b20309edbcbec89745dccd80d15204bdafa01537236676ea0902b` | Nonpositive-depth closing-parenthesis invalidity case. |
| 10 | `rule-f18ac752ae9a55086836d401b1f975ed7ba1dc1a1dfe6020469ec40361b27db8` | Invalid-character catch-all case. |

These equations define the mathematical scanner, its initialized result, and
the formal balanced-input domain. They do not add a mathematical fact about a
previously defined symbol and do not execute or observe the program
configuration.

The `OPERATIONAL_RULE` set is empty.

## Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

Stage 1 has no proof evidence satisfying the required admission order.
`/reference/k-proof/prove.sh` first compiles `verification.k` as module
`VERIFICATION`, so all 10 inventoried rules are already present in
`verification-kompiled`. It then invokes:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

That command proves the two reachability claims in `spec.k`; it does not first
prove the exact statement of any inventoried reusable rule against a module
that omits that rule. The later vacuity and body-mutation commands use the same
compiled definition and are expected-failure validation probes. Accordingly,
neither the Stage 1 `#Top` result nor the description of the loop claim as
derived evidence upgrades any inventoried equation to
`PROVED_DERIVED_LEMMA`. The loop invariant is a claim in `spec.k`, not a rule
in the canonical inventory.

## Domain lemmas

The domain-lemma set is empty. No inventoried rule asserts an additional
trusted mathematical fact used to close the proof; all are defining equations
for the three proof-local functions.
