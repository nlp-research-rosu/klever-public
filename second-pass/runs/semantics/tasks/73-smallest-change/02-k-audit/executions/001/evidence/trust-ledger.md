# Proven-versus-assumed trust ledger

| Boundary | Exact symbols/rules | Value/control influence | Dependents | Audit disposition |
|---|---|---|---|---|
| K toolchain and hooks | K v7.1.337; Haskell reachability backend; LLVM concrete backend; builtin `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, `K-EQUAL` modules and compiler-generated heating/cooling rules | All parsing, execution, arithmetic, maps, and proof closure | Every build/run/proof | Normal low-level trust boundary |
| Fixed selected language | Entire byte-identical `/reference/reference-semantics` tree | Defines `.mpy` execution model | Concrete run and proof definition | Authoritative in `SUPPLIED_SEMANTICS`; candidate made no changes |
| Total positional access | `valSeqAt` (`subscript.k:11-14`) | Values compared in `changeRange` and target recurrence | Synthetic correctness claim | Acceptable on the proved helper precondition because every recursive access is in bounds; globally opaque/OOB cases remain outside intent |
| Opaque float symbols | `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF` | Float values/branches in unrelated programs | Imported theory only | Supplied-semantics primitives, all unused by this integer/list program |
| Other `symbol` declarations | `floorFI`, `toF`, `ceilF` | Float conversion in unrelated programs | Imported theory only | Supplied-semantics symbols with concrete equations; unused |
| Opaque sorting/digest symbols | `sortVS`, `sortKeyVS`, `md5hexCodes` | Sort/digest results in unrelated programs | Imported theory only | Supplied-semantics primitives, unused |
| Proof-local mathematical functions | `changeRange`, `targetAnswer`, `targetValid` and their equations (`verification.k:52-59,118-128`) | Directly fixes the claimed result/domain | `smallest-change-correct` | Equations are guarded, disjoint, terminating, and mathematically correct on intended integer arrays; not opaque |
| Manual AST/closure copy | `#helperBody`, `#mainBody`, `#helperClosure`, `#mainClosure` (`verification.k:7-49`) | Selects which closure the bridges match | Entry bridge claims | Text matches the submitted AST and trusted translation in this candidate, but this is only an informal/textual link; no claim loads `solution.mpy` |
| Operational call substitution | priority-40 rules at `verification.k:73-86` | Replaces binding, frame push/pop, body execution, recursive lookup/call, and return with `#targetCall` | All three positive claims as a program-correctness argument | Illegitimate for real-program pinning: no bridge-free universal connection theorem; removing rules breaks both entry claims; body mutation is undetected |
| Synthetic execution rules | `#targetCall`/`#addMismatch` rules (`verification.k:90-116`) | Computes final count directly from heap sequence | `smallest-change-correct` | Internally truthful recurrence, but it proves the substituted machine rather than the submitted program |
| Trusted translation | `/reference/py2mpy.py` | Establishes `solution.py` to submitted AST identity | Program provenance bridge | Byte identity established; finite/file-specific, not a proof that proof-local macros are mechanically imported |
| Trusted canonical oracle | `/reference/canonical.py` | Natural-language adequacy oracle | Differential and ground witness checks | Trusted input by audit contract |
| Differential evidence | 11,853 arrays: examples, branch boundaries, all lengths 0..8 over `{-1,0,1}`, 2,000 seeded arrays, two length-2200 runtime cases | Python implementation-to-intent bridge | Adequacy only | 11,851 matches; two real `RecursionError` divergences; finite evidence, never a K proof |
| Concrete K smoke evidence | Six assertions in trusted-translated `concrete-tests.mpy` | Exercises supplied concrete semantics and real candidate code on small inputs | Semantics/program sanity only | Passed; finite evidence, never a reachability connection theorem |
| Informal palindrome argument | One element change can repair each unequal mirrored pair, and distinct pairs are independent | Connects mismatch count to minimum number of changes | Natural-language contract | Standard mathematical argument; not stated as a separate K theorem |
| Runtime-model boundary | Supplied semantics uses unbounded recursion/math integers and does not model CPython recursion depth | Termination/exception behavior on long arrays | Natural-language/Python adequacy | Material documented limitation; `[0]*2200` and a 2,200-element mismatch array raise in candidate Python while canonical returns |

There are no `[simplification]` or `[functional]` declarations in the audited
source. The exhaustive source inventory found 25 `symbol` declarations, 22 of
them `[no-evaluators]`; all 25 are in the trusted supplied semantics and are
unused by this program. The candidate proof extension adds no fresh opaque
`symbol`, but its two operational bridge rules are a more serious
result-bearing trust assumption because they bypass the code under verification.
