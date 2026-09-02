# K proof trust-boundary discovery

The canonical inventory is `/reference/rule-inventory.json`, with schema
version 2 and inventory SHA-256
`55a78cf76899cbb801e44ed21e4217bf95f2ef58a9da1f097435c4d394fafc3e`.
It contains 16 rules in the local `VERIFICATION` module closure. Every
canonical `source_rule_id` appears exactly once and in canonical order in
`trust-boundary.json`.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 16 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 0 |

All 16 rules are definitions:

- The first seven inventory entries define exact named AST, closure, and module
  terms: `isPalindromeBody`, `reverseLoopBody`, `searchLoopBody`,
  `makePalindromeBody`, `isPalindromeClosure`, `makePalindromeClosure`, and
  `solutionModule`. Their declarations are macros, and their rules expand
  names into the corresponding MPY terms. They do not replace an MPY
  configuration transition.
- The remaining nine entries are equations for mathematical summaries. The
  two `reverseAcc` rules are its base case and structurally decreasing
  recurrence; `palIS` defines a Boolean summary; the two complementary
  `seedResult` rules define its guarded cases; the three `searchResult` rules
  define its base and recursive cases; and `completePal` defines the initial
  summary call.

No inventory rule matches a configuration cell such as `<k>`, skips a source
operation, or adds an observation transition, so the `OPERATIONAL_RULE` set is
empty. The canonical inventory records an empty attribute list for every rule,
so there are no rules carrying `simplification`.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

The Stage 1 evidence in `/reference/k-proof/prove.sh` first compiles
`verification.k` as module `VERIFICATION`, which already contains all 16
canonical rules. It then invokes `kprove` on the reachability claims
`SPEC.reverse-loop`, `SPEC.search-loop`, and the complete `SPEC` module. The
three successful invocations are recorded as `#Top` in
`/reference/k-proof/prove-run.out`.

Those reachability claims validate execution against the summary definitions,
but none is the exact statement of a canonical rule proved first against a
module that omits that rule. The later vacuity and body-mutation commands are
expected-failure validation probes, not proofs of reusable rules. Therefore no
canonical rule meets the required evidence and ordering for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The `DOMAIN_LEMMA` set is empty. No canonical rule adds a separate,
unproved mathematical fact: each rule is an expansion, equation, recurrence,
guarded defining case, or structural initializer for a named term.
