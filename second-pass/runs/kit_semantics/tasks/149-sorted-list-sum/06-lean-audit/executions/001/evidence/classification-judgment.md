# Independent Stage 3 classification

The trusted inventory reconstructs nine rules in source order from modules
`VERIFICATION-SYNTAX` and `VERIFICATION`; all nine rules themselves occur in
`VERIFICATION`.

| Source rule (hash prefix) | Independent class | Judgment |
|---|---|---|
| `91f437c4` | `DEFINITION` | Base equation for the declared total function `stringsOnly`. |
| `0e7dac14` | `DEFINITION` | Constructor-recursive equation for `stringsOnly`; it tests the head and descends on the tail. |
| `cd5c2076` | `DEFINITION` | Base equation for the declared total summary `scanEven`. |
| `858547b3` | `DEFINITION` | Guarded recursive `scanEven` equation for an even-length string; it consumes the tail. Its `simplification` attribute is consistent with a definition. |
| `134ac8fc` | `DEFINITION` | Guarded recursive `scanEven` equation for an odd-length string; it consumes the tail. Its `simplification` attribute is consistent with a definition. |
| `bbdcfa64` | `DEFINITION` | Totalizing recursive `scanEven` equation for a non-string head; it consumes the tail. |
| `1136bead` | `DOMAIN_LEMMA` | This does not define `seqLen` or `isStrV`; it asserts the definedness proposition `#Ceil(seqLen(V)) => #Top` under `isStrV(V)`. It is not an execution rule and no earlier exact claim proves it in a module without the rule. It is true under the frozen semantics because `isStrV` is true exactly on `str(IntSeq)`, `seqLen(str(IS))` rewrites to total `isLen(IS)`, and `isLen` has exhaustive constructor equations. It is relevant to the source program's `len(word)` guard and the `scanEven` proof summary. Its `simplification` attribute therefore requires, and receives, `DOMAIN_LEMMA`. |
| `136aef47` | `DEFINITION` | Macro expansion of the named proof term `sortedListSumBody`; constructor-by-constructor it matches the translated source body. |
| `b75f2055` | `DEFINITION` | Macro expansion of the named module term `sortedListSumModule`. |

The two string/non-string guards are disjoint. On strings, integer remainder
equality versus inequality to zero partitions the defined `seqLen` result, so
the three recursive `scanEven` cases cover constructor inputs and all descend.
There are no independently proved derived lemmas and no ordinary operational
rules in the local verification-module closure.
