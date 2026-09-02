# Proven-versus-assumed ledger

| Boundary | Dependents | Classification | Audit disposition |
|---|---|---|---|
| K v7.1.293 parser, compiler, LLVM backend, Haskell backend, and reachability calculus | All parsing, execution, and proof results | Trusted primitive/toolchain | Necessary and acceptable foundational trust. Candidate-provided compiled artifacts were not used. |
| Builtin `Int`, `Bool`, `String`, and `Map` domains | All semantic rules and summaries | Trusted primitives | Acceptable low-level boundary. Arbitrary-precision integers match the reachable CPython behavior. |
| Builtin `+Int`, comparisons, and equality | Program arithmetic/control and summaries | Trusted primitives | Acceptable; direct ordinary integer mathematics. |
| Builtin `/Int` and `%Int` | Inner digit loop and divisibility tests | Trusted primitives with a scope condition | K uses truncating division/remainder. This matches every reachable operand in the submitted program because dividends are nonnegative. It differs from CPython for some negative dividends in other programs; the out-of-program witness is recorded in `scope-limitations.log`. |
| `/reference/py2mpy.py` | Link from `solution.py` to submitted `solution.mpy` | Trusted mounted translator | Candidate copy was byte-identical; fresh trusted regeneration was byte-identical to the submitted IR. |
| Candidate `semantic.k` | Connection from translated AST to K execution | Audited generated semantics, not an assumption | Every local declaration/rule was inventoried. It is a deliberately small entry-harness semantics, not a general Python semantics. It covers all constructs and reachable states in the actual program. |
| `INNER-LOOP` and `OUTER-LOOP` | Claim readability and program pinning | Compile-time definitional macros | Expanded forms were byte-identical at KORE level to the corresponding submitted-program term. They do not bypass execution. |
| `digitSevens`, `fizzContribution`, `fizzFrom`, `fizzEnd` | Loop postconditions and final result | Definitional summaries | Guards are disjoint/exhaustive and recursion descends. No opaque or oracle value remains. Inner and outer reachability claims connect the summaries to fixed semantic execution. |
| Integer-associativity simplifier | Symbolic normalization in loop proofs | Derived mathematical lemma | Universally true over K integers and terminating in its right-associating orientation. |
| Inner and outer loop claims | End-to-end proof | Machine-checked auxiliary reachability claims | Each independently returned `#Top`; audit-only dependency runs marked already-proved helpers trusted only to select one target at a time. |
| Natural-language reading of `fizzFrom(0,N)` as decimal-seven count among multiples of 11 or 13 below `N` | HumanEval intent bridge | Informal mathematical argument plus finite empirical evidence | Transparent from the equations, and supported by 797 zero-mismatch differential cases, but not a separately formalized theorem about CPython string conversion. This is a documented concern, not a substitute for the K proof. |
| `/reference/canonical.py` and CPython runs | Program-to-intent evidence | Independent executable oracle, finite only | Supports fidelity/adequacy on tested inputs; does not prove universal equivalence. |
| Program termination | Total-correctness interpretation | Excluded | The Kit proof is reported only as partial correctness. The audit does not upgrade it to a termination theorem. |

There are no local opaque symbols, fresh result-bearing values, unconstrained
oracles, priority rules, proof-time operational bridges, output primitives,
heap primitives, allocation primitives, or exception primitives.

