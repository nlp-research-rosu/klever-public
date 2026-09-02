# Trust-boundary discovery

## Canonical scope

The exhaustive source is `/reference/rule-inventory.json`, with canonical
`inventory_sha256`
`7b0c3a5cec95c8717ad8bdb6dce5cf1d85abf737e1ec48c0586929bb5e49d810`.
It contains three rules, all in module `VERIFICATION`; each is classified
exactly once and retained in canonical inventory order in
`trust-boundary.json`.

The inventory reports no attributes on any rule, so there are no
`simplification`-attributed rules requiring a `DEFINITION` or `DOMAIN_LEMMA`
choice.

## Rule classifications

| Canonical rule | Classification | Reason |
|---|---|---|
| `rule-c09d86f09f196dc6bfd7245139d77da63a26829d9dcf6ed5b3c1e876b4204f34` | `DEFINITION` | Base equation for the named recursive summary `lpfFrom` under `F >= 2` and `N <= F`. |
| `rule-4c37787b8b69deb1e9173a83d853af7a8fe0ee7441fddb5263a9d691cadc23ac` | `DEFINITION` | Divisible-case recurrence for `lpfFrom`, using the summary's guarded quotient transition. |
| `rule-de3529b439b11f78acab7501799690277d17c9e760bf812468bba7d69d04efd4` | `DEFINITION` | Non-divisible-case recurrence for `lpfFrom`, using the summary's guarded factor-increment transition. |

Together these rules are the exhaustive, disjoint guarded definition of the
proof-local result summary over every use (`F >= 2`). They rewrite only
`lpfFrom` terms used by the claims; they do not match a Python computation,
configuration cell, continuation, or execution-state term. Consequently none
is an `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` rules in the canonical inventory.

The Stage 1 ordering confirms this:

- `/reference/k-proof/prove.sh` lines 15–18 compile `verification.k`, already
  containing all three inventory rules.
- Lines 20–23 then prove the focused `SPEC.loop` reachability claim.
- Lines 25–27 prove the complete `SPEC` claim set.

Thus Stage 1 does not first prove the exact statement of any inventory rule
against a module from which that rule is absent. `SPEC.loop` is separately
machine-checked and is described in Stage 1 as a derived reachability
circularity, but it is a `claim` in `spec.k`, not a rule in the canonical
inventory, so it receives no rule classification here.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty.

Stage 1's paper-level number-theoretic argument connects the execution summary
to the phrase “largest prime factor,” but the canonical inventory contains no K
rule encoding that argument. None of the three defining equations is an
additional trusted mathematical fact beyond the definition of `lpfFrom`.
