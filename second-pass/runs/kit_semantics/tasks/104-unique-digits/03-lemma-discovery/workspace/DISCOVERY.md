# Trust-boundary discovery

## Canonical scope and result

The exhaustive classification source is
`/reference/rule-inventory.json`, with inventory SHA-256
`32bb0f36be98d96562f1768dc23748ba3c4cda812d63bfd210f22e1017c522c7`.
It contains 15 rules, all from module `VERIFICATION`, and every one is
classified exactly once in `trust-boundary.json`.

| Classification | Count |
|---|---:|
| `DEFINITION` | 15 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All 15 inventory entries have an empty `attributes` array. In particular, no
inventory rule carries `simplification`, so the special constraint on
simplification rules is satisfied vacuously.

## Why the rules are definitions

`VERIFICATION-SYNTAX` declares `integerVals`, `scanBad`, `scanNumber`,
`appendCandidate`, `collect`, `afterValue`, `afterNumber`, and `afterBad` as
proof-local function symbols. Every inventory rule is an equation, guarded
equation, or structural recurrence defining one of those symbols:

- The two `integerVals` rules define the empty and cons cases of the input
  predicate.
- The two `scanBad` rules define its guarded base case and positive-integer
  recurrence; the `scanNumber` rule directly defines that summary.
- The two `appendCandidate` rules define complementary append and no-append
  branches.
- The two `collect` rules define a fold by empty and cons cases.
- The two rules for each of `afterValue`, `afterNumber`, and `afterBad` define
  structural helpers for the empty and cons cases.

These rules reduce named mathematical summaries. None matches a `<k>` cell,
configuration cell, Python expression, statement, call, loop, continuation, or
control transition. Therefore none is an `OPERATIONAL_RULE`.

## Separately proved derived lemmas

There are no separately proved derived lemmas in the canonical rule inventory.

The Stage 1 ordering is visible in `/reference/k-proof/prove.sh`: it first
compiles `verification.k` into `verification-kompiled`, with all 15 inventory
rules already present, and then runs:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

The positive run is recorded as `#Top` in `/reference/k-proof/prove.log`.
The only later `kprove` invocations are expected-failure body and result
mutations. There is no Stage 1 command that proves the exact statement of an
inventory rule against a module omitting that rule, followed by a build that
admits the proved statement as a reusable rule. Consequently the evidence does
not meet the required ordering for `PROVED_DERIVED_LEMMA`.

`SPEC.digit-loop`, `SPEC.outer-loop`, and `SPEC.program` are reachability claims
in `spec.k`; they are not rules in the launcher-generated canonical inventory
and have no `source_rule_id`, so they are not classification entries.

## Domain-lemma boundary

The domain-lemma set is empty. No inventory entry asserts an additional
mathematical fact about a previously defined symbol; each one participates
directly in defining a fresh proof-local function. Thus the local rule
inventory adds definitions but no trusted `DOMAIN_LEMMA`.
