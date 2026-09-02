# Proven versus assumed ledger

| Boundary | Effect and dependents | Accounting |
|---|---|---|
| K v7.1.337 compiler, Haskell prover/backend, LLVM backend, and builtin K integer/Boolean/map/list hooks | All build, proof, and concrete-execution evidence | Ordinary toolchain trust; versions and fresh builds are logged. |
| Trusted mounted translator `/reference/py2mpy.py` | Source-to-`solution.mpy` identity | The candidate translator is byte-identical, and trusted regeneration is byte-identical to the submitted `.mpy`. Translator correctness itself is trusted. |
| Byte-identical supplied semantics tree | Meaning of every `.mpy` construct | Provenance integrity passes, but integrity does not prove Python fidelity. Every record is inventoried separately. |
| `SPEC.member-fold` | Later loop and function proof | Machine-proved first from fixed operational membership; trusted only in later commands. It soundly connects to `memberVS` under K structural equality. |
| `SPEC.common-loop` | Function proof | Machine-proved after `member-fold`; trusted only in the final command. It is an exact loop-head circularity over the submitted body and preserves the relevant state footprint. |
| `sortVS` (`sort.k:18`) | Final returned sequence | Externally supplied opaque total primitive. The symbolic proof establishes only `sortVS(commonSpec(...))`; ascending-sort/permutation meaning is assumed. Ground K execution and 25,347 integer-list differentials are finite supporting evidence, not a universal connection theorem. |
| Informal mathematics linking `commonAcc` to “unique intersection in encounter order” | Natural-language intent | The recursive equations are transparent and terminating, but the set/intersection characterization is not a separate K theorem. |
| Python canonical implementation | Differential oracle and intent evidence | Independently loaded from trusted source. Differential evidence is finite and does not replace K proof. |
| K structural membership equality in `list.k:63-66` | Both comparisons, `memberVS`, `commonAcc`, and final result | Illegitimate bridge for the full prompt domain: Python numeric cross-types compare equal, K constructors do not. Concrete witness `common([True],[1])` yields `[True]` in both Python implementations but empty under K, causing `AssertionError`. |
| Partial-correctness interpretation | The theorem excludes divergence | Termination is not proved. For this finite-list program termination is informally evident on ordinary terminating equality/sort inputs, but it is outside the reachability result. |
