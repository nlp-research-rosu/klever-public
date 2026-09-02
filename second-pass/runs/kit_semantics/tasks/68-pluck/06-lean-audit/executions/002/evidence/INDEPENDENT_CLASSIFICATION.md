# Independent Stage 3 classification

This classification was made from the frozen `verification.k`, its local
verification-module closure, the source solution/specification, and the
operational K modules. It does not adopt the rationales in the protected
classification file.

The trusted inventory reconstructed module `VERIFICATION` as the entire local
verification-module closure. It contains 22 ordered, unique rules and has
inventory SHA-256
`db923cb4995eb9590d6a8f9ef245d3fdf66930a46476128f1053a8d3903bf90a`.
The frozen `verification.k` SHA-256 is
`6108afcbaffc3b32951a2aa04d3a699b8fac095bc7e1c199e8305c8f75f65244`.

| # | Source span | Source rule ID | Independent class | Reason |
|---:|:---:|---|---|---|
| 1 | 10 | `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5` | `DEFINITION` | Defines the named summary predicate `definedProjectInt` as `isInt`. |
| 2 | 15–17 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | `DOMAIN_LEMMA` | Characterizes definedness of the imported partial `Val`-to-`Int` projection; it does not define that projection or a named proof term. |
| 3 | 19–21 | `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0` | `DEFINITION` | Defines the guarded total projection summary from the operational cast. |
| 4 | 23–25 | `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d` | `DEFINITION` | Definitional bridge from the guarded cast to the named total projection. |
| 5 | 27 | `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442` | `DEFINITION` | Base equation for `projectIntTotal` on an integer. |
| 6 | 28–30 | `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081` | `DEFINITION` | Idempotence/normalization equation for the named total projection summary. |
| 7 | 35–38 | `rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167` | `DOMAIN_LEMMA` | A guarded theorem connecting dynamic `Val` addition to imported operational integer addition; it is not the ordinary fixed-sort execution rule. |
| 8 | 43 | `rule-cf4138b8c8c76302d40452525511bd8b4e31a4b3346bb98e6e73d97d1e6c2974` | `DEFINITION` | Base recurrence for the named `allNonNegative` summary. |
| 9 | 44–47 | `rule-83288e0b3172aab26d1ec54ec969884572eed5ce44f6238f19681d654d51ef2e` | `DEFINITION` | Recursive equation for `allNonNegative`. |
| 10 | 53–55 | `rule-7e939de20504830e917b8d5d873c3bb58561f3855213d88b9d59b50ef33c4bd5` | `DEFINITION` | Defines the named selection predicate `shouldTake`. |
| 11 | 58–59 | `rule-5252890cd97149023a2a416ba7c01b694a8ff30898028588da15ee87b14a256c` | `DEFINITION` | True branch of the named `nextBest` summary. |
| 12 | 60–61 | `rule-a50201bce4854fcc39ac7fff337c62431472104dcb3835fba7f50ce031f797bc` | `DEFINITION` | False branch of the named `nextBest` summary. |
| 13 | 64–65 | `rule-c92176e0f4b06badc71e64610b3f95be15c41c7b6a9f7ffc01c22e0063ad9616` | `DEFINITION` | True branch of the named index summary `nextBestIndex`. |
| 14 | 66–67 | `rule-8f2ab2609b1cc09149865009919218835e409941c760e0cd32d7cd314e854fd4` | `DEFINITION` | False branch of the named index summary `nextBestIndex`. |
| 15 | 70 | `rule-9e8ff4eeadc760fef596dec38dede08f7dc277396d3bf2a83be796e4bea29ae9` | `DEFINITION` | Base recurrence for `scanBest`. |
| 16 | 71–72 | `rule-17aa23fd17bc416e79da19dd2b02377da50a1a774104a3df16adb8cb3f6f753c` | `DEFINITION` | Recursive recurrence for `scanBest`. |
| 17 | 76 | `rule-a0a97ed4baae5f006d554885ce763a55d1f90f4dab1c6758f4f16e425d1fdf7e` | `DEFINITION` | Base recurrence for `scanBestIndex`. |
| 18 | 77–83 | `rule-7b59a9d33a341d5cac01e67da9523b88afc82daf3321b530741d506a69c5837d` | `DEFINITION` | Recursive recurrence for `scanBestIndex`. |
| 19 | 86 | `rule-c38110c90d754cdfc7a715c9dae55a5663f8de024b1fb80fce7a0c7835cf4e4b` | `DEFINITION` | Base recurrence for `afterIndex`. |
| 20 | 87–88 | `rule-60bf2bc0542914c544a3f677f13fe17eda968f8750e2064ce8b7c3e8d0999339` | `DEFINITION` | Recursive recurrence for `afterIndex`. |
| 21 | 91–92 | `rule-be6c5e486b28b9205e812b1977ae6d9af5349c88576c0eff80505fee2716790c` | `DEFINITION` | Negative-result branch of the named `resultList` summary. |
| 22 | 93–95 | `rule-615dd6754d1e5de3108d82927712a0b9350d18eb111423ada2109218959edb7d` | `DEFINITION` | Nonnegative-result branch of the named `resultList` summary. |

No entry is an `OPERATIONAL_RULE`: the ordinary execution rules live in the
imported MPython semantics, not this verification module. No entry is a
`PROVED_DERIVED_LEMMA`: `prove.sh` compiles this module with all 22 rules
present and then runs the specification proof; it never first proves either
domain lemma against a module from which that exact rule was removed.

Both domain lemmas are relevant. The program’s loop evaluates
`value % 2 == 0`, compares candidate integers, and executes
`value = value + 0`; the specification also projects list elements to
integers. The cast-definedness rule supplies the projection side condition,
and the guarded `applyBin("+", ...)` rule is the bridge for the assignment.
Every rule marked `simplification` is either one of these two domain lemmas or
a definition.

The protected classification has the same 22 entries, in this exact order,
with the same spans, normalized hashes, source rule IDs, and classifications.
