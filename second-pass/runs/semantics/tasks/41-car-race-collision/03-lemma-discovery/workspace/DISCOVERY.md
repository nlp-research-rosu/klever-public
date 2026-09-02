# Trust-boundary discovery

The canonical inventory contains two rules, both from the local
`VERIFICATION` module. Neither rule carries the `simplification` attribute.
Both are classified as `DEFINITION`.

## Rule classifications

| Inventory order | Source rule ID | Classification | Reason |
|---:|---|---|---|
| 1 | `rule-9b1cd001fa1574b5d38ed3c286fe702d05d566d93fcf98abd5e049d981abc968` | `DEFINITION` | The rule is the macro expansion of `solutionModule` into the exact `Module` term found in Stage 1 `solution.mpy`. It only names the translated program. |
| 2 | `rule-d05c71cafbdcedd65ca2027e7a81d8d6fbdfe3240186222e046807d78f81ff16` | `DEFINITION` | The rule unfolds the named proof harness `#runCarRaceCollision` into loading `solutionModule` and invoking the required entry point. It defines proof setup and supplies no additional mathematical fact. |

No inventory rule is an `OPERATIONAL_RULE`: the two local rules name the
program and the proof harness, while execution itself is supplied by the
imported reference semantics.

## Separately proved derived lemmas

There are no separately proved derived lemmas.

Stage 1 `prove.sh` compiles `verification.k` as module `VERIFICATION` and then
runs `kprove spec.k` against that compiled definition. Both inventoried rules
are already present in that module. There is no earlier proof command, no
module variant excluding either rule, and no proof of an exact rule statement
before its use. Consequently, neither rule meets the evidence requirement for
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is empty. Neither local rule asserts an additional
mathematical fact used to close the proof.
