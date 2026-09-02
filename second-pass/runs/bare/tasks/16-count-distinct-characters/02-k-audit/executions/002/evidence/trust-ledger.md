# Proven versus assumed ledger

## What the reconstructed reachability proof establishes

Conditional on K 7.1.293, its Haskell backend, and the submitted generated
semantics, the four source claims close. The universal claim says that, from
the exact initial program/configuration for any K `String` `S`, terminating
execution consumes `<k>`, binds `string` to `StrVal(S)`, and writes
`IntVal(size(charsSet(lowerString(S))))`. Three ground instances establish
3 for `"xyzXYZ"`, 4 for `"Jerry"`, and 0 for `""`.

The result is constrained and non-vacuous, and the executed constructor term
is the parsed submitted `solution.mpy` term.

## Trust and assumptions

| Boundary | Effect | Dependents | Assessment / evidence |
|---|---|---|---|
| K compiler, parser, Haskell/LLVM backends | proof and execution engine | all claims/tests | ordinary unavoidable toolchain trust; versions recorded |
| K `STRING` operations (`lengthString`, `substrString`, `+String`, `ordChar`, `chrChar`) | character traversal and ASCII mapping | R12-R14, all claims | low-level primitive trust; concrete boundary runs support only tested cases |
| K `SET` operations (`SetItem`, `|Set`, `size`) | duplicate elimination/count | R07, R09, R15-R17, all claims | low-level primitive trust |
| K `MAP` lookup/update/matching | binds and reads parameter | R01, R03, all claims | low-level state primitive trust |
| Generated dispatch rules for `lower`, `set`, and `len` | replace Python primitive calls | all claims | must faithfully model the real Python bindings; set/len are adequate for this program, lower is materially false on Unicode |
| `lowerString`/`lowerChar` | determines a result-bearing value | C01 and R17 | fully equational rather than opaque, but equations cover only ASCII uppercase behavior; false witness `"Ää"` |
| `charsSet` | determines result-bearing set | C01 and R17 | exhaustive decreasing equations over modeled strings; backed by K SET trust |
| `expectedDistinctCharacters` | postcondition result | C01 | merely unfolds to the same generated helpers used during execution; no bridge theorem to Python `str.lower` |
| Trusted translator and byte comparison | links `solution.py` to `solution.mpy` | real-program pinning | byte identity independently checked |
| `kast` constructor comparison | links `.mpy` to entry claim | real-program pinning | normalized KAST JSON hashes equal and `cmp` exits 0 |
| Python differential test | candidate Python vs canonical Python | implementation fidelity only | 18 fixed/boundary plus 2,000 seeded cases, zero mismatch; finite evidence |
| Python/K Unicode comparison | generated semantics vs real implementation | semantics adequacy | decisive counterexample, not merely finite support: K proves/returns 2 for `"Ää"` while both Python implementations return 1 |

There are no submitted opaque symbols, axioms, simplification lemmas, totality
declarations, or proof-local operational bridges beyond the generated semantic
rules themselves. Differential testing does not substitute for the K proof or
for a universal Python-semantics connection theorem.
