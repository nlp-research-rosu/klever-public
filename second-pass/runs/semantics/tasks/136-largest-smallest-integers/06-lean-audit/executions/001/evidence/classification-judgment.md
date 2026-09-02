# Independent rule-by-rule classification

The local closure selected by `prove.sh` is the sole local module
`VERIFICATION`. It contains 26 rules. The classification below was made from
the frozen rule text, `solution.mpy`, `spec.k`, and the supplied MPY semantics,
not from the Stage 3 rationales.

| # | Frozen span and source rule ID | Independent class | Source/semantic reason |
|---:|---|---|---|
| 1 | 10, `rule-070812b155305927bd35f4cc85856d530ba7fe499c1bb003bd23f4252561d3ad` | `DEFINITION` | Defines the fresh `intValue` projection on integer values; it is used only under integer-sort evidence. |
| 2 | 12–15, `rule-5b53e5e1e7c389a2532855b2ec7b9b198ac32e2c188993cc5f36766b5113bf5f` | `OPERATIONAL_RULE` | Specialized ordinary list-iterator execution. Supplied `list.k:10` yields `V`; under `isInt(V)`, `intValue(V) => V`, so this yields the same head and tail and preserves the continuation and every other cell. |
| 3 | 23–39, `rule-2e6e9b319fe94fe1e7bcb719603e85c97cb59094c8d8db08fbdd30a6920d6b32` | `DEFINITION` | Defines the fresh named proof term `scanBody` as the exact two `If` statements in `solution.mpy:7–22`. |
| 4 | 41–49, `rule-726d1fc9c79efb9d375f1dc89bb1e237a1a3f799edf75518a8dddad0645f600a` | `DEFINITION` | Defines `finishBody` as the exact two sentinel conversions and return in `solution.mpy:23–30`. |
| 5 | 51–56, `rule-30e93f55051ebde71ed355b5428333e4efee2a26210e051d8dd481b74c2a5116` | `DEFINITION` | Defines `solutionBody` by composing the exact initializations, `For`, scan body, and finish body. |
| 6 | 59–61, `rule-2da62240a4ad6f4d9b9481b4c429b75d7016eaaa771bd9f79fe0a7322e6e67fa` | `DEFINITION` | Defines the fresh module term holding the translated target function. |
| 7 | 71–72, `rule-2aa8c74c2dcefa65cd1a8e1732d3251289ff057e75778c6aee98c627be5df151` | `DEFINITION` | First guarded equation of fresh summary function `negStep`: a negative value replaces the zero sentinel. |
| 8 | 73–74, `rule-a8ce937ddb4767b6678f9dbfa872967c818c893670ba0bffcf68dae61bb4fe47` | `DEFINITION` | Guarded `negStep` equation selecting a larger negative candidate. |
| 9 | 75–76, `rule-f7be8bcdb70bf74537ffb0f86d887e1c4841e3a45a5ac9a75959076cb7569695` | `DEFINITION` | Guarded `negStep` equation retaining the accumulator for a nonnegative input. |
| 10 | 77–78, `rule-06e7ed9338cf2f793d8f08f2a06ea909637145c8b5e62881ac82c37c114c2f4e` | `DEFINITION` | Final guarded `negStep` equation retaining a nonzero accumulator when the new negative is no larger. |
| 11 | 80–81, `rule-d43b03bb8c91409b0f2e1197abda5d2d7334f0b19b9e85788a053259dfa42951` | `DEFINITION` | First guarded equation of fresh summary function `posStep`: a positive value replaces the zero sentinel. |
| 12 | 82–83, `rule-452bbe16289abdee2dafe172896fb8dac7964723a2128f3ccb550b48bbddbffe` | `DEFINITION` | Guarded `posStep` equation selecting a smaller positive candidate. |
| 13 | 84–85, `rule-6fb1853a0b077ebc803320955c46c3673d3a18eadf4acdf70ffdd7446f358a24` | `DEFINITION` | Guarded `posStep` equation retaining the accumulator for a nonpositive input. |
| 14 | 86–87, `rule-261ad2d7d8a694096ea6bcedacba5e69570e5c4eb1ebaeebe7b5d75c66681a04` | `DEFINITION` | Final guarded `posStep` equation retaining a nonzero accumulator when the new positive is no smaller. |
| 15 | 89, `rule-00580234f8bc455ce1d583ce93aa718e8e3e7686701202ad4831be1804334d14` | `DEFINITION` | Base equation of fresh recursive negative-extremum summary `negFold`. |
| 16 | 90–92, `rule-ac3eb7fe88f6ae33ba4b40f71687c52eb0203cd3cdd367578d9b5349db402e2d` | `DEFINITION` | Structurally descending recurrence for `negFold` over an integer head and shorter tail. |
| 17 | 94, `rule-8157987e2d829522c5774028f16e05e90b26a27476add8d0bc82851dd53ee68e` | `DEFINITION` | Base equation of fresh recursive positive-extremum summary `posFold`. |
| 18 | 95–97, `rule-fa3ef94177ae1acc4436e2f686032194c0fe9239586b135a024d336286a13da6` | `DEFINITION` | Structurally descending recurrence for `posFold` over an integer head and shorter tail. |
| 19 | 99, `rule-187e6e47081ad6258aba693ab9da2cd2a2975bb4a15220e855fa3c77bf34a841` | `DEFINITION` | Base equation of fresh loop-variable summary `finalValue`. |
| 20 | 100–102, `rule-ceb3ffde4b83a1279539d5bfca456bfa29057a80a2a7d772bd1fb9d87867a058` | `DEFINITION` | Structurally descending recurrence defining the final iterated integer value. |
| 21 | 105, `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Base equation of fresh structural predicate `allInts`. |
| 22 | 106–107, `rule-fa394f9b181c0d7a89141e7d4e865895db0443da2d399ebaeb0492e3a9b63ed4` | `DEFINITION` | Structurally descending recurrence defining `allInts` from the head sort test and tail. |
| 23 | 111, `rule-df372afc7929272592e4625f73f1ee8a95746d22d81ee5221fa550497c4567d6` | `DEFINITION` | Defines `optionalNeg(0)` as the Python `None` sentinel result. |
| 24 | 112, `rule-9702e6e6fe7649923cff9ce82535fbf878a70f8b3db33bbc869ffdba3078d48b` | `DEFINITION` | Completes `optionalNeg` on nonzero integers by returning that integer. |
| 25 | 113, `rule-49fdcffdc48276e627acdfe63c293b24d0b373245efdd09f66b9b51182ea43ed` | `DEFINITION` | Defines `optionalPos(0)` as the Python `None` sentinel result. |
| 26 | 114, `rule-ac50ec8d00a7b631eeac436df0191e5bc541f096204c07dfb2cd8759fa1922a1` | `DEFINITION` | Completes `optionalPos` on nonzero integers by returning that integer. |

Classification totals are 25 `DEFINITION`, one `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`. No inventory rule has the
`simplification` attribute.

Every definition is source-relevant: the four named syntax terms reconstruct
the translated program; `negStep`, `posStep`, `negFold`, `posFold`,
`optionalNeg`, and `optionalPos` determine the entry-point postcondition;
`finalValue` determines the loop claim; and `allInts` is the formal input
precondition. None states an additional mathematical fact about already
defined symbols.

The operational rule is not a derived-lemma claim and was not classified as
one. Its match domain is the integer-headed subset of the supplied list
iterator rule. Ground boundary checks are discriminating: heads `-3`, `0`, and
`5` yield the same value and remainder under both rules; `noneV` does not meet
the specialized guard and remains handled by the supplied rule. A mutation
`intValue(I) => 0` would disagree on `-3` and `5`, so the equality is not
vacuous.
