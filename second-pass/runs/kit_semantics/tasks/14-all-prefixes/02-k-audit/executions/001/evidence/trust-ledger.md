# Proven-versus-assumed ledger

| Boundary | Effect on this theorem | Dependents | Evidence and disposition |
|---|---|---|---|
| Supplied `MPY` source semantics | Defines all execution, configuration, value, allocation, binding, call, loop, mutation, and return behavior | Both K claims | Required fixed boundary in `SUPPLIED_SEMANTICS`; candidate tree is recursively byte/type-identical to trusted mount; material rules are mapped in `used-rule-map.md`; fresh concrete and symbolic builds succeed. Acceptable. |
| K parser/compiler/Haskell reachability backend | Parses constructor terms, compiles equations/rules, and checks circular reachability | Both K claims and the fresh mutation | K 7.1.293, the campaign-pinned version. Fresh `#Top` and rejected mutation are conditional on toolchain correctness. Standard acceptable proof checker boundary. |
| LLVM K backend | Finite concrete MPY executions | Empirical K-side checks only | Fresh build and six reviewer-authored assertions. Supports, but does not replace, the Haskell reachability proof. |
| Trusted `py2mpy.py` | CPython-AST to MPY constructor translation | Real-program pinning | Candidate translator is byte-identical to trusted mount; trusted regeneration is byte-identical to submitted `solution.mpy`; emitted-KAST comparison pins that regenerated module to the claim. Acceptable. |
| CPython and trusted `canonical.py` | Executable source-contract oracle | Differential evidence only | 516 cases with zero mismatches. Finite evidence; no K claim assumes its result. |
| Human interpretation of `prefixesAcc` | Connects the recursive constructor sequence to “all nonempty prefixes, shortest to longest” | Intent statement | The two constructor equations make this a direct structural induction: base `[]`; step appends `P+c` then recurses on the strict tail. No empirical or opaque value is used. Acceptable ordinary-mathematics bridge. |
| Partial-correctness convention | Does not prove separate termination/liveness | Scope of theorem | Explicitly excluded by the requested Kit workflow. The concrete implementation does terminate for finite strings, but that is not a separate K liveness theorem. Acceptable. |

The imported fixed semantics declares 22 `no-evaluators` symbols:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`,
and `md5hexCodes`. They affect float operations, sorting, or MD5. Neither
entry claim, the loop claim, nor any proof-local definition contains or
reaches one. They are therefore fixed but nondependent primitives, not
result-bearing abstractions in this proof.

The fresh builds warn that fixed functions `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt` are non-exhaustive over the entire broad
declared sort. None is reachable from this submitted term. No false conclusion
witness exists on the intended input domain through these declarations, so the
narrow finding is an unused fixed-semantics coverage gap, not a proof-local
unsoundness claim.
