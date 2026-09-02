# Trust-boundary rule discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, with inventory hash:

```text
f18755c8299c46ecc0c49530526a2460c852955ad805fe23a7788caeb6175604
```

It contains 14 rules, all in the local `VERIFICATION` module closure.  Every
canonical `source_rule_id` appears exactly once in `trust-boundary.json`, in
inventory order.

## Classification result

- `DEFINITION`: 13 rules.
- `OPERATIONAL_RULE`: 1 rule.
- `PROVED_DERIVED_LEMMA`: 0 rules.
- `DOMAIN_LEMMA`: 0 rules.

The definition rules are:

- `rightAngleTriangleClosure()`, which expands a named proof term to the exact
  closure containing the translated candidate body.
- The concrete `trustedFloatEq` equation, which defines its concrete-backend
  evaluation through the existing `==Float` hook.
- Both `ratSquare` cases, all four `ratAdd` cases, all four `ratEq` cases, and
  `ratExpected`.  These are sort-dispatched equations defining the
  postcondition's mathematical summaries.

The sole operational rule is
`rule-c6539c39ccea106c35e916b768648493791aeac70bc31344ebb53f72dbce4b71`.
It rewrites an evaluated Float `Compare` in the `<k>` cell to
`trustedFloatEq`, framing the continuation.  This changes the execution model's
observation of Float equality and is therefore operational rather than a
mathematical definition or lemma.

No inventory rule carries the `simplification` attribute.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The mounted Stage 1 `prove.sh` first compiles `verification.k`, with all 14
inventory rules already present, into `verification-kompiled`.  It then runs
`kprove spec.k` against that definition.  The eight claims in `spec.k` prove
the target function behavior; none first proves the exact statement of an
inventory rule against a module omitting that rule.

The other K proof commands use `spec-vacuity.k` and
`spec-body-mutation.k`.  Both are expected-failure validation probes, not
successful proofs of reusable rules.  Thus Stage 1 provides no ordering or
exact-correspondence evidence that would permit a
`PROVED_DERIVED_LEMMA` classification.

## Domain lemmas

The domain-lemma set is empty.

No inventory rule asserts an additional mathematical fact trusted to close the
proof.  The `rat*` rules define named summaries, while the Float comparison
bridge is an operational abstraction.  The Stage 1 report separately records
the semantic trust placed in opaque Float primitives, but that trust does not
turn any canonical inventory equation into a `DOMAIN_LEMMA` under the requested
classification scheme.
