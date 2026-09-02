# Trust-boundary discovery

## Canonical inventory

The exhaustive source is `/reference/rule-inventory.json`, with:

- schema version: `2`
- inventory SHA-256:
  `d277ae12725aaa26772d37930e9cbe9a7b2e0699b8289d37fe7be0befeac524a`
- canonical rule count: `12`

`trust-boundary.json` preserves all 12 canonical `source_rule_id` values
exactly once and in inventory order. No Stage 1 artifact was edited or copied.

## Classification method

The first five rules expand productions declared `[macro]` in
`VERIFICATION-SYNTAX`. They define the named source-body and internal loop-head
terms used by the claims, so they are `DEFINITION`, not operational model
rules.

The remaining seven rules all carry `simplification`, so the requested policy
limits them to `DEFINITION` or `DOMAIN_LEMMA`:

- The base, divisor, and non-divisor-fold rules for `primeScan` are the
  defining cases and recurrence of that mathematical summary.
- The base and inductive-fold rules for `primeFibSearch` are the defining
  equations of the remaining Fibonacci-prime search.
- The false-flag absorption rule is an extra mathematical consequence of the
  scan recurrence. It is useful to close symbolic paths, but it is not itself
  a defining case needed to state the recurrence.
- The one-step exit-boundary rule for `primeFibSearch` is an extra consequence
  of the inductive step followed by the base case. It is likewise a
  proof-closing mathematical fact beyond the core recurrence.

Accordingly, the classification totals are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 10 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 2 |

## Separately proved derived lemmas

There are no separately proved derived rules in the canonical inventory.

Stage 1 `prove.sh` does establish an ordering for reachability *claims*:

1. It proves `SPEC.inner-loop` with `kprove ... --claims SPEC.inner-loop`.
2. It then proves `SPEC.outer-loop` while trusting that already-proved claim.
3. It finally proves `SPEC.prime-fib` while trusting the two already-proved
   loop claims.

Those claims are in `spec.k`; they are not any of the 12 canonical rule IDs.
More importantly, every positive command compiles and uses the finalized
`verification.k`, which already contains all seven simplification rules.
There is no Stage 1 command that first proves the exact statement of any
canonical rule against a module omitting that rule. Thus the staged claim
evidence cannot justify classifying an inventory rule as
`PROVED_DERIVED_LEMMA`.

Comments in `verification.k` and prose in `PROOF.md` call the absorption,
boundary, and folding facts “lemmas” or “derived.” That terminology is not
separate-proof evidence under the requested classification rule. The fold
equalities are classified by their actual role as recurrences; the two
additional unproved consequences are trusted domain lemmas.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly:

1. `rule-577938ca98678b9423c7ce676db6a34945e77e9da125b1d4877efb3bda8a48c2`
   — `primeScan(_A,D,false) => false` for `D >= 2`, the false-flag absorption
   fact.
2. `rule-a100ddf7646fa9f900ad120af90a1d1db8c452277cb178014ca5f3675572126f`
   — the `primeFibSearch` one-step exit-boundary fact.

Both affect result-bearing summaries and are trusted mathematical facts in the
finalized K theory. Neither is upgraded to `PROVED_DERIVED_LEMMA`, because the
required rule-free, exact-statement proof evidence does not exist in Stage 1.

## Operational rules

The canonical local verification-module closure contains no
`OPERATIONAL_RULE`. Program execution is supplied by the mounted reference
semantics. The five ordinary-looking local rules are macro expansions because
their left-hand productions are declared `[macro]`; the other seven rules
operate only on mathematical summary symbols.
