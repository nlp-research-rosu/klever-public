# Trust-boundary discovery

## Canonical scope

The exhaustive source for this classification is
`/reference/rule-inventory.json`, whose `inventory_sha256` is
`993975976aee2a5aec1109c062dbe6168d9391fcdc989e7a2667ebe9d68d6bb1`.
It contains two rules in the local `VERIFICATION` closure. Both are classified
once below, in canonical inventory order. Neither rule has the
`simplification` attribute.

Rules from the supplied reference semantics are not added: the launcher
inventory is canonical and exhaustive for the requested local
verification-module closure.

## Classifications

| Inventory order | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 0 | `rule-0f02393212bfcf7e7c8810a806f9829aa2bbf9b5bd9795c9a7b5db26160d7995` | `DEFINITION` | This is the guarded base equation for the newly introduced mathematical summary `largestDivisorAtOrBelow`: when `D >= 1` and `pyMod(N,D) == 0`, the summary is `D`. It defines a named proof term and does not match an execution cell or add a fact about pre-existing symbols. |
| 1 | `rule-99644c7600e08ea07b0c26314084adf2ab5eb468a6b1eb4aadd857b2f427b14a` | `DEFINITION` | This is the guarded recursive equation for the same summary: when `D > 1` and `pyMod(N,D) != 0`, search continues at `D -Int 1`. It is a decreasing recurrence defining the summary and does not match an operational configuration. |

No inventoried rule is an `OPERATIONAL_RULE`: neither equation rewrites a
Python term, K cell, continuation, call, loop, state, or observation.

## Separately proved derived lemmas

No inventoried rule qualifies as `PROVED_DERIVED_LEMMA`. Stage 1's `prove.sh`
first compiles `verification.k` containing both summary equations:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Only afterward does it run `kprove`. There is no earlier proof against a module
that omits either rule, and no Stage 1 claim has an exact statement
corresponding to either equation. Calling the later target proof successful
therefore cannot turn either admitted equation into a proved derived lemma.

Stage 1 does separately prove the reachability claim `SPEC.loop-invariant`:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
```

`/reference/k-proof/PROOF.md` records `#Top` and exit code `0` for that command.
This is proof evidence for a claim in `spec.k`, not for a reusable rule in the
canonical rule inventory, so it receives no JSON rule classification.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. The two admitted mathematical rules introduce
and define `largestDivisorAtOrBelow`; they do not assert additional trusted
facts about an already defined domain.
