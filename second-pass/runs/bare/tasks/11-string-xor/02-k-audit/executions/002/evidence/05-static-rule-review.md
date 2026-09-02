# Exhaustive local declaration and rule review

This inventory covers every local declaration in `semantic.k`, every local
proof extension in `verification.k`, and both claims in `spec.k`. Imported
`BOOL`, `INT`, and `STRING` operations are listed as trusted K primitives in the
trust ledger rather than re-inventoried as local rules.

## Syntax and attributes

| Location | Declaration | Audit decision |
|---|---|---|
| `semantic.k:6-7` | `Module`; juxtaposed `Stmts` list | Exact constructors emitted by the trusted translator. |
| `semantic.k:9-11` | `Stmt`: `FuncDef`, `Return`, `If` | Exactly the three submitted statement forms. |
| `semantic.k:13-14` | comma-separated `Strings`; `Params` | Exact submitted two-parameter constructor. |
| `semantic.k:16-22` | `Expr`: `Name`, `Str`, `Int`, `BinOp`, `Compare`, `Subscript`, `Call` | Covers every expression constructor in `solution.mpy`; no used expression is missing. |
| `semantic.k:24-27` | `CmpOp`, `Index`/`Slice`, `NoBound` | Covers equality, index `0`, and slice `[1:]` exactly. |
| `semantic.k:36-38` | `Stream`: `seed`, functional `next`; total functional `head : Stream -> Bool` | `seed(I)` encodes bits least-significant first. Every ground `Stream` normalizes through `next(seed(I))`; `head(seed(I))` fixes the bit. For symbolic stream variables, `head` is an abstract total bit selector and the theorem is parametric in the same selector. |
| `semantic.k:39-41` | `Text`: `empty`, `cons`, `segment` | `empty/cons` executes concrete strings; `segment(N,S)` is the proof representation of an `N`-bit prefix. |
| `semantic.k:43-51` | `Value`, `Args`, `Env`, `ExecResult`; result subsorts into `KResult`/`Sem` | The model has only two argument values and no call-stack depth or exception result. Heap/output/allocation are unnecessary, but omitting recursive-call depth and `RecursionError` is material because the submitted implementation recurses once per input character on an unrestricted source domain. |
| `semantic.k:52` | `eval` | Evaluation dispatcher. |
| `semantic.k:53-56` | strict `equal`, `concat`, `index`, `tail` | Enforces evaluation of operands. `strict` does not impose Python's left-to-right order, but every submitted operand is pure and has no modeled side effect, so this is sound for the target. |
| `semantic.k:57` | `call`, strict in arguments 1 and 2 | Both slice arguments are pure; the target observes no difference between strict evaluation orders. |
| `semantic.k:58-59` | strict `returnValue`, `makeReturn` | Correctly waits for a recursive/return expression result. |
| `semantic.k:60-62` | `exec`; `decide` and `continue`, strict in result position | Implements statement lists, condition selection, and return propagation. |
| `verification.k:8,41` | macro `solutionProgram`; macro `solutionBody` | Expanded KORE for `solutionProgram` is byte-identical to the trusted regenerated `solution.mpy`; `solutionBody` is the same constructor body and is matched by actual entry execution. |
| `verification.k:72` | functional `xorText` | Mathematical pairwise XOR summary. It is intentionally partial outside nonnegative lengths; the claim and recursive calls remain in its complete guarded domain. |
| `verification.k:86` | `prependResult`, strict in recursive result | Pure continuation which prepends one fixed Boolean after the recursive call returns a string. |
| `verification.k:94,101,113` | priority 40 on three `exec` accelerations | The guards are disjoint and the rules preempt ordinary statement execution only on the exact submitted body and segment environments. A fresh acceleration-free universal theorem closes with `#Top`, validating the displaced execution. |

There are no local `[simplification]` rules, `[functional]` declarations,
proof-local lemmas, or fresh result oracles.

## `semantic.k`: all 35 local rules

| # | Location | Rule and decision |
|---:|---|---|
| S1 | 64 | `head(seed(I))`: returns parity as a Boolean. Correct for the documented least-significant-bit encoding. |
| S2 | 65 | `next(seed(I))`: integer division by two advances that encoding one bit. |
| S3 | 71-73 | Module entry selects the exact `string_xor(a,b)` binding, binds the two supplied argument values, and retains the same body as recursive-call target. Exact for the submitted one-function module. |
| S4 | 75 | `Name("a")` lookup returns the first environment value. |
| S5 | 76 | `Name("b")` lookup returns the second environment value. |
| S6 | 77 | `Str("")` maps to `str(empty)`. |
| S7 | 78 | `Str("0")` maps to one false bit. |
| S8 | 79 | `Str("1")` maps to one true bit. |
| S9 | 80 | `Int(I)` maps to `i(I)`; used only for indices 0 and slice lower bound 1. |
| S10 | 82-83 | Submitted equality comparison evaluates both operands then delegates to `equal`. |
| S11 | 84-85 | Submitted `+` evaluates both operands then delegates to string concatenation. |
| S12 | 86-87 | An expression index evaluates receiver and index before indexing. |
| S13 | 88-89 | The exact `[1:]` slice evaluates its receiver then takes its tail. Its pattern is distinct from S12 because `Slice` is not an `Expr`. |
| S14 | 90-91 | The exact recursive global call evaluates both arguments and invokes the retained submitted body. There is no rebinding or mutable global state in the modeled target. |
| S15 | 93 | Empty equals empty. |
| S16 | 94 | Any concrete `cons` string is nonempty. |
| S17 | 95 | Symmetric concrete empty/nonempty case. |
| S18 | 96 | A proof segment is empty exactly when its tracked length is zero. |
| S19 | 97 | Symmetric segment/empty case. |
| S20 | 98-99 | One-character concrete strings are equal exactly when their Boolean heads agree; this is the only concrete nonempty equality shape used by the target. |
| S21 | 101 | Concatenating a one-character prefix to a text tail constructs the expected string. |
| S22 | 102 | Index 0 of a concrete nonempty string returns its one-character head. |
| S23 | 103-104 | Index 0 of a positive-length segment returns its abstract one-character head. The positivity guard excludes Python's empty-index error path, which the source guards prevent. |
| S24 | 105 | Tail of a concrete `cons` string is its stored tail. |
| S25 | 106-107 | Tail of a positive segment decrements length and advances the stream. The source takes the slice only after both nonempty checks. |
| S26 | 109 | Recursive call creates a fresh two-argument environment and wraps its return value, but has no call-stack bound or `RecursionError` transition. This is false as a model of actual CPython over the full intended domain. Concrete witness: with both valid inputs equal to `"0" * 998` under recursion limit 1000, trusted canonical Python returns 998 characters, candidate Python raises `RecursionError`, while `krun` on the real `solution.mpy` with both arguments `segment(998,seed(0))` exits 0 and returns 998 false bits. |
| S27 | 110 | A returned recursive value becomes the expression value. |
| S28 | 112 | Exhausted statement list completes normally with the current environment. |
| S29 | 113 | `Return(E)` evaluates `E`, ignores following statements, and constructs an abrupt return. |
| S30 | 114-115 | `If` evaluates its condition before selecting a branch and retains the following statement suffix. |
| S31 | 116-118 | True condition executes the then-list and later continues only after normal completion. |
| S32 | 119-121 | False condition symmetrically executes the else-list. The S31/S32 guards are disjoint and exhaustive for Boolean `C`. |
| S33 | 122 | A returned value becomes `returned(V)`. |
| S34 | 123 | Return propagation discards the current branch and following suffix, matching Python return control. |
| S35 | 124 | Normal branch completion resumes the retained suffix in the same environment. |

Rules S1-S35 have no overlaps producing disagreeing right-hand sides within the
candidate's idealized model. S3 is the only cell rule; it reads but does not
mutate `<args>`. All other local rules are pure term rewrites, so `<args>` is
preserved. That very absence of a stack/exception component causes the concrete
S26 false-conclusion witness above.

## `verification.k`: all 9 local rules

| # | Location | Class | Rule and decision |
|---:|---|---|---|
| V1 | 10-38 | Macro normalization | `solutionProgram` expands to the exact submitted constructor term. Independently compared after K macro expansion. |
| V2 | 42-68 | Macro normalization | `solutionBody` expands to the same body selected by S3. The exact-body pattern makes material program mutations stop matching the accelerations. |
| V3 | 73-74 | Definitional summary | `xorText(0,...) = empty`. Correct first exhausted-input case. |
| V4 | 75-76 | Definitional summary | For positive `N` and zero `M`, the result is empty. |
| V5 | 77-80 | Definitional summary | For positive lengths, prepend Boolean XOR of the two heads and recurse on both decremented segments. Guards V3-V5 are pairwise disjoint and exhaustive for the claims' nonnegative lengths; recursion descends. |
| V6 | 87 | Definitional continuation | `prependResult` maps a returned string to a returned string with the supplied head. It neither fabricates nor constrains the recursive tail. |
| V7 | 89-94 | Operational bridge | Exact body with `N=0` returns empty. Fixed execution takes the first source return. Reads only term arguments; writes only the enclosing computation; preserves any surrounding continuation and `<args>`. |
| V8 | 96-101 | Operational bridge | Exact body with `N>0,M=0` returns empty. Fixed execution skips the first branch and takes the second source return. Same state/control footprint as V7. |
| V9 | 103-113 | Operational bridge | Exact body with both lengths positive prepends head XOR and recurses on exact `[1:]` segments. Fixed execution chooses literal `0` iff heads agree and literal `1` otherwise, then performs the same recursive call. `Bool` XOR is exactly that truth table. The continuation waits for the same recursive result before returning. |

V7-V9 are central operational bridges, not merely harmless equations. Relative
to the candidate's idealized, unbounded-recursion semantics, their
independent justification is the reviewer-authored `bridge-free.k` and
`spec-bridge-free.k`: these import the candidate's fixed `semantic.k`, copy the
mechanically pinned program/body and identical summary definitions, contain no
V7-V9 or equivalent `exec` shortcut, and prove the recursive plus entry claims
with `#Top`. The body-sensitivity mutation also produces `returned("0")` where
the original result obligation requires `"1"`, so the bridge pattern does not
hide a changed body.

## `spec.k`: both claims

| Claim | Plain-language meaning | Adequacy |
|---|---|---|
| Recursive claim, lines 8-14 | For arbitrary nonnegative lengths and streams, executing the exact submitted body in a segment environment returns `xorText` of those arguments, preserving any caller continuation and arbitrary `<args>`. | Satisfiable, result-constraining, and used as the induction circularity. |
| Entry claim, lines 17-20 | Starting from the exact translated one-function module with two nonnegative-length segments returns their `xorText`. | Mechanically pins the real module and covers arbitrary input lengths, not finitely many examples. |

At the mathematical value level, for every finite binary string `c[0:n]`, choose
`I = sum(bit(c[i]) * 2^i)`. Then `segment(n,seed(I))` has exactly those heads
under S1/S2, including leading zeroes because `n` is tracked separately. Thus
the formal domain syntactically contains every source-contract input pair, and
V3-V5 yield pairwise XOR until the shorter length, exactly the canonical `zip`
behavior. Operationally, however, S26 makes all such mathematical recursions
return while actual CPython raises at a valid finite length (998 in the audited
runtime). The entry theorem therefore does not cover the real program on the
unrestricted source-contract domain.
