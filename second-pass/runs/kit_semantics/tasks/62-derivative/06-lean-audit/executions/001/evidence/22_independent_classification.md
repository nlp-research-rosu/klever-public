# Independent Stage 3 classification

The trusted inventory reconstructed exactly five rules in the local
`VERIFICATION`-module closure. The classifications below were made from the
frozen rule text, the source program, the Stage 1 claims, and the supplied
operational semantics.

| Source span | Source rule ID | Independent class | Judgment |
|---|---|---|---|
| `verification.k:9` | `rule-82fd85d7d877438e349407a829d1e35806842c5943d9c0f294aa58ed3173779c` | `DEFINITION` | Base equation for the fresh summary function `derivAcc`; an empty remainder returns the accumulator. |
| `verification.k:10-13` | `rule-51a3749a6415a476a599f9f4b4d86298466c83cbf2e19efd98a63953ec251c03` | `DEFINITION` | Guarded recurrence for the fresh summary function. It consumes one constructor and skips it exactly when `I > 0` is false. |
| `verification.k:14-20` | `rule-699bb53c2b20d45244efa55313af6891bd44df240c352ce9088ca451eccca62c` | `DEFINITION` | Guarded recurrence for the positive-index branch. It appends `applyBin("*", I, V)` and consumes the tail, matching the source loop's append branch. |
| `verification.k:25` | `rule-69d164c2333b75d39789a2087d0efc8310446075e2ed8ca85aaa99880622898f` | `DEFINITION` | Empty-sequence equation for the fresh structural predicate `noRefsVS`. |
| `verification.k:26-27` | `rule-cdffeaf04d811ef623fa1b34b1412c6bea8d70a043f5ca0aa93d9bec48680e9a` | `DEFINITION` | Constructor equation for `noRefsVS`; it checks the head with the supplied `isRefV` definition and recurses on the tail. |

The three `derivAcc` rules are the complete, disjoint, structurally recursive
definition of a named execution summary. The two nonempty guards are
`I > 0` and `notBool (I > 0)`. The recursive argument `REST` is structurally
smaller. The source loop tests `i > 0`, appends `i * x`, and increments `i`;
the supplied semantics implements list iteration, mutable `append`, operator
dispatch, and integer multiplication in exactly those terms.

The two `noRefsVS` rules are the complete structural definition of a named
precondition predicate over `.ValSeq`/`vCons`. They do not assert that an input
has no references; they define what that proposition means. The predicate is
relevant because the Stage 1 claims use it to exclude heap handles from the
read-only input sequence.

Neither symbol occurs on an operational `<k>`-cell left-hand side. Both are
declared fresh in `verification.k` and occur elsewhere only in Stage 1 claim
preconditions or postconditions. Thus none of the five rules replaces fixed
program execution, none is an ordinary observation rule, and none asserts a
separate mathematical fact about a pre-existing symbol.

Counterfactual checks also distinguish these definitions from convenient
assumptions: changing the positive guard to include index zero would append the
constant coefficient contrary to the source; replacing the appended value by
a constant would fail as soon as either `I` or `V` changes; replacing
`noRefsVS` by constant `true` would admit `ref(H)`, contrary to the supplied
`isRefV(ref(H)) => true` rule.

Independent classification counts:

- `DEFINITION`: 5
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

All three rules carrying `simplification` are `DEFINITION`s. The true domain
lemma set is genuinely empty.
