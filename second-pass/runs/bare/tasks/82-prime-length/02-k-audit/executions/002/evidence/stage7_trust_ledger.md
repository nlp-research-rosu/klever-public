# Proven-versus-assumed ledger

## What the reconstructed `#Top` establishes

Under the submitted `semantic.k`, for symbolic K `String` `S`, executing the
exact constructor term regenerated from `solution.py` reaches empty `<k>`,
sets the local map entries to the submitted semantics' native
`lengthString(S)`, and returns:

```text
VBool(lengthString(S) >=Int 2
      andBool noDivisors(lengthString(S), 2, lengthString(S)))
```

The postcondition's `isPrime` expands to exactly that expression. This is a
partial-correctness statement in the submitted K model. It is not by itself a
theorem that `lengthString` equals Python `len(str)`, nor a proof inside K that
the specialized generator bridge is equivalent to general Python generator
execution.

## Boundaries and dependents

| Boundary | Role and dependents | Evidence | Assessment |
|---|---|---|---|
| Trusted `py2mpy.py` | Maps `solution.py` AST to `solution.mpy`; every claim depends on the program term | Trusted and candidate copies match; regeneration is byte-identical; expanded KORE matches `solutionProgram` | Acceptable trusted syntactic front end |
| K BOOL/INT/MAP hooks | Boolean/integer/map evaluation; all rules and the claim depend on them | K 7.1.293 fresh builds/runs; ordinary positive-integer arithmetic | Acceptable low-level primitive boundary for this task |
| K STRING hook `lengthString` | S9 uses it as Python `len`; affects `n`, branches, divisibility, and final return | Fresh witnesses show K values 8 for `"😀😀"` and 6 for `"你好"`, while Python values are 2 | **Illegitimate bridge on intended domain** |
| Specialized S16 `all`/generator rule | Replaces the exact generator computation by `noDivisors`; affects final return | Ground recursive equations and finite concrete comparisons; no bridge-free universal connection theorem or general generator semantics | Truthful on tested/inspected target ground cases, but circular at the symbolic proof/property boundary; a material validation limitation |
| `noDivisors` S17–S19 | Ground mathematical recursion; symbol remains opaque on symbolic arguments because of `[concrete]` | Guards are disjoint and recursive descent is evident for target `D >= 2`; concrete Haskell runs agree on tested ASCII lengths | Acceptable ground mathematical definition within its target guard; not independently connected to general Python execution |
| V2 `isPrime` definition | Human-facing primality property | Standard fact: for natural `N`, `N >= 2` and no divisor in `[2,N)` iff prime | Acceptable informal mathematics, conditional on `noDivisors` meaning that range property |
| `[total]` attributes | Permit/function-mark `eval`, `valueLength`, `asInt`, `asBool`, `noDivisors`, `isPrime` | Fresh LLVM compilation reports five non-exhaustive-match warnings; target calls stay in covered cases | Overclaimed globally; not the target-domain false-result witness |
| Haskell backend | Used for intended concrete execution and proof | Fresh compile, runs, and `#Top` | Acceptable toolchain boundary |
| LLVM backend | Writing-semantics smoke-test path | Fresh build succeeds, but nontrivial ground `noDivisors` calls exit 113 because `[concrete]` rules do not execute there | Portability/executability concern, not the decisive theorem defect |
| Python differential oracle | Canonical versus candidate implementation bridge | 529 cases, zero mismatches | Finite support for implementation fidelity only; no universal proof |
| K/Python concrete comparison | Generated-semantics adequacy bridge | ASCII cases match; two Unicode witnesses mismatch | Disproves universal adequacy |

## Excluded or unproved facts

- The K proof does not establish correspondence with Python Unicode string
  length; concrete evidence refutes it.
- It does not provide a general semantics for Python calls, generators,
  iteration, short-circuit effects, exceptions, or Unicode.
- It does not prove termination as a total-correctness property.
- Differential tests do not replace the reachability proof or establish
  universal equivalence.
- Candidate generation reports, submitted `.kore` files, and candidate caches
  are not in the trust base and were not used for reconstruction.
