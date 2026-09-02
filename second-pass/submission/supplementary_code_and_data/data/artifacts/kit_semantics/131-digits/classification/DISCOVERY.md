# Trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with
`inventory_sha256`
`0a1d759c28623d9c6b243594fed4806c09dcfb862b9aac752f052cfe8f180f0d`.
It contains 10 rules, all from the local `VERIFICATION` module. The
classification preserves canonical inventory order and does not add claims or
rules from outside that inventory.

## Classification summary

| Classification | Count | Reason |
|---|---:|---|
| `DEFINITION` | 6 | These are the base and guarded recursive equations defining `oddDigitsProduct` and `oddDigitSeen`. |
| `OPERATIONAL_RULE` | 0 | No canonical rule executes or observes Python program state; the operational semantics is imported rather than added by the local verification module. |
| `PROVED_DERIVED_LEMMA` | 0 | Stage 1 contains no qualifying prior, rule-free proof of an exact reusable rule. |
| `DOMAIN_LEMMA` | 4 | These are trusted integer simplification facts used to close the symbolic proof. |

The first three canonical rules define `oddDigitsProduct`: its nonpositive
base, its odd-last-digit recurrence, and its even-last-digit recurrence. The
next three analogously define `oddDigitSeen`. They are `DEFINITION` because
they give the equations for named mathematical summaries and do not add
execution behavior.

The final four rules carry the `simplification` attribute and state facts about
built-in integer multiplication, addition, and subtraction. They do not define
a new named summary, so they are `DOMAIN_LEMMA`, not `DEFINITION`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence does not establish the ordering required for
`PROVED_DERIVED_LEMMA`:

1. `/reference/k-proof/prove.sh` first compiles
   `/reference/k-proof/verification.k` into `verification-kompiled`.
2. That compiled module already contains all four simplification rules.
3. The script then runs `kprove spec.k` against that definition.
4. The remaining `kprove` commands are expected-failure mutation probes using
   the same compiled definition.

No command first proves any simplification rule's exact statement against a
module from which that rule is absent. The combined reachability proof of
`SPEC.digits-loop` and `SPEC.digits-entry` therefore proves those claims under
the simplification rules; it does not separately prove the rules themselves.
The Stage 1 comment and `PROOF.md` description calling the identities
"derived lemmas" do not supply the missing proof ordering.

## Domain-lemma set

The domain-lemma set is **not empty**. It consists of exactly these four
canonical rules:

- `rule-082958cd68b6ff48e923703bfbdc398fbdc293247656d1a01d3339fbcf725de4`:
  left multiplication by one.
- `rule-2ab4c7bc73ad01bbe3db34c2b3cc0d6c95c87c850e1e3f40e6891b9a061c05a7`:
  right multiplication by one.
- `rule-b09bdfe5e2bc74b215bed27c498fc03e78a4929071d23d07a626110c519fed02`:
  the integer cancellation normalization used for the presence bit.
- `rule-6c033d38e2e8c948160d245d94624fb6c578d69ea99fc1c15c896b557eaa1ee3`:
  multiplication associativity oriented toward right association.

These identities are mathematically standard, but under the requested
evidence-sensitive classification they remain trusted domain lemmas because
Stage 1 used them while proving the target claims and did not separately prove
their exact statements first.
