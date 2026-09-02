# Used-construct and proof-local static review

The complete 1,102-record declaration/rule inventory is in
`05_rule_inventory.md` and `05_rule_inventory.json`. It covers the supplied
assembly file, every supplied helper K file, `verification.k`, and `spec.k`.
There are 698 ordinary rules, 230 syntax blocks, five contexts, one
configuration, one claim, 22 `[no-evaluators]` opaque symbols, 35
`[concrete]` rule blocks, 45 priority rule blocks (priorities 39, 40, or 45),
26 `[owise]` rule blocks, and no `[functional]` or `[simplification]`
declarations. Unused supplied rules are retained in the inventory as fixed,
byte-identical baseline rules; they do not contribute to this target claim.

## Construct-to-rule map

| Submitted construct | Declaration | Execution path |
|---|---|---|
| `Module(...)` | `semantics/syntax.k:61` | `core.k:124-127` loads and sequences module statements. This path is exercised by concrete `krun`, but not by the target claim. |
| `FuncDef(...)` / `Params(...)` | `syntax.k:53,57,60` | `functions.k:14-16` binds a closure in the current scope. This path is also absent from the target claim, which constructs `closureVal` directly. |
| `Assign(Name("number"), ...)` | `syntax.k:12,41` | RHS strictness precedes `controls.k:9-11`, which updates the callee scope. |
| `Call(Name("float"), ...)` and `Call(Name("int"), ...)` | `syntax.k:12,28` | `call.k:19-21` evaluates the callee before arguments; `core.k:189-191` evaluates arguments left-to-right; `call.k:32` dispatches `typeV`; `float.k:185` and `float.k:211` apply conversion primitives. |
| `If(Compare(...), T, .Stmts)` | `syntax.k:30,32,49` | comparison contexts in `operators.k:15-17`; `float.k:127` dispatches `>` to `gtF`; `controls.k:51-54` branches on `truthy`, with `core.k:200` handling the Boolean. |
| `BinOp("+",...)` / `BinOp("-",...)` | `syntax.k:15` | sequential strictness evaluates left then right; `operators.k:12` dispatches; `float.k:105,113` produce `subF`/`addF`. |
| `Float(0.0)` / `Float(0.5)` | `syntax.k:10` | `float.k:20-21` yields the K `Float` value. |
| `Return(Call(...))` | `syntax.k:50` | strictness evaluates the result; `functions.k:78-90` records it, pops the frame, restores `env`, deletes the callee scope, restores `scopeLoc`, empties the stack, and resumes the saved continuation. |
| One-argument closure invocation | `core.k:31`, `functions.k:8-11` | `call.k:69-75` allocates scope 1, pushes the exact continuation, and runs `#bindP ~> BODY ~> #endcall`; `functions.k:63-66` binds `value`. |

The call does not allocate heap objects, mutate the module scope, emit output,
or raise a modeled exception along the symbolic paths. The claim pins every
configuration cell before and after execution: module environment 0, the empty
module scope with builtin parent, `scopeLoc` 1, empty heap and stack, `noRet`,
`NoExc`, and exit code 0. The fixed call/return rules restore those cells.

## Used opaque and concrete boundaries

The target proof uses the supplied `[function,total,symbol(...),no-evaluators]`
symbols `decStrToF`, `gtF`, `addF`, `subF`, and `truncF`. (The mechanical
range tag also marks nearby `divF`, but the submitted AST never dispatches
division.) Their concrete twins use K Float hooks in `float.k:161-164`,
`104`, `112`, `126`, and `210`. The proof does not derive IEEE-754 properties
of these operations. It is interpretation-parametric because the execution and
postcondition contain the same opaque applications. The LLVM smoke and ground
tests support ordinary examples but are finite evidence only.

Guards and overlaps in the used slice are benign at the formal structural
level: type dispatch is sort-specific; the positive and nonpositive `#if`
branches are complementary; duplicate mixed-float/type rules in `float.k`
have identical right-hand sides; no used total function has inconsistent
equations. The relevant priority rules concern cell/reference paths whose
guards are false for this plain scalar frame, so they do not preempt the
ordinary path. There are no proof-local priority, simplification, or loop
rules, and there are no auxiliary claims.

The supplied decimal primitive is intentionally narrower than CPython:
`float.k:157-185` handles digits, one decimal point, and optional leading
minus without digit-validation or Python exceptions; it does not implement
exponent notation, whitespace, or a leading plus. This is an empirical
Python/K bridge limitation, not a candidate modification to the supplied
baseline. `05_semantics_gap.*` gives the concrete witness `"5e-1"`.

## Exhaustive proof-local decisions

1. `closestBody : Stmts` (`verification.k:9`) is a total proof-local function.
   Its sole equation (`:10-17`) is byte-for-byte structurally consistent with
   the body currently printed in `solution.mpy`. The equation itself is
   truthful, terminating, and non-overlapping. It is nevertheless a copied
   body, not a formal dependency on the submitted module.
2. `runClosest : Str -> KItem` (`:20`) has one ordinary rule (`:21-23`). It
   constructs a one-argument closure with defining environment 0 and invokes
   the fixed call semantics. It preserves binding, evaluation order, frame
   state, and return control for that copied body. It never loads
   `solution.mpy`, never executes its `Module` or `FuncDef`, and has no
   connection claim from the submitted module to `closestBody`.
3. `nearestAway : Float -> Int` (`:29`) is total. Its sole equation
   (`:30-34`) is terminating, complete, and non-overlapping. It exactly
   restates the two result expressions used by the copied body, so it does not
   bypass execution. It is not an independent theorem that the expression is
   a closest integer under floating-point rounding.
4. The sole reachability claim (`spec.k:9-24`) has no side-condition and thus
   ranges over every `CS:IntSeq`, including sequences that are not valid
   Python numeric strings. It is satisfiable, result-constraining, and
   non-vacuous, but its source term invokes item 2, not the submitted module.

No proof-local rule is labeled mathematically unsound: each equation is true
as a definition on its declared K domain. The rejection is instead an
adequacy/identity failure with a direct sensitivity witness:
`04_pinning_test.log` rebuilds after changing the scratch `solution.py/.mpy`
to `return 777`; the target still proves `#Top` and Python prints `777`.

The natural-language interpretation of `nearestAway` is also false on the
intended decimal-string domain because binary addition can round before
truncation. For the satisfying input `"0.49999999999999994"`, both the trusted
canonical and an exact-decimal oracle return 0, while the candidate and
concrete supplied semantics return 1. This is the concrete false-result
witness in `02_differential.log` and `04_ground_concrete.log`.
