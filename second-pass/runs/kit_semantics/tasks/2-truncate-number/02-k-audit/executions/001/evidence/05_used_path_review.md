# Used-path static review

The candidate proof definition imports the supplied `MPY` module unchanged.
`verification.k` adds no syntax, function, totality declaration, symbol,
equation, rewrite, priority, simplification, helper claim, or bridge. The sole
candidate-local declaration that can contribute to closure is
`SPEC.truncate-number`.

## Construct-to-rule map

The submitted `solution.mpy` is:

```text
Module(
  Expr(Str("HumanEval solution for returning the fractional part of a float."))
  FuncDef("truncate_number", Params("number"),
    Return(BinOp("%", Name("number"), Float(1.0)))))
```

Its constructs map to the supplied semantics as follows:

| Construct | Declaration/evaluation order | Operational rules |
|---|---|---|
| `Module`, `Stmts` | `syntax.k:56,61`; initial configuration `core.k:49` | `core.k:125-127` loads and sequences the module |
| `Expr(Str(...))` | `syntax.k:9-13,52`; `Expr` is strict | `str.k:14` evaluates the string; `controls.k:48` discards the expression value |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` installs `closureVal` in the current module scope |
| `Call`, `Name`, one-element `Exprs` | `syntax.k:12,28,37` | `call.k:20-21`, `core.k:131-154`, and `core.k:189-191` evaluate callee then arguments left-to-right |
| `closureVal` call | `core.k:31`; call frame declaration `functions.k:8-11` | `call.k:69-74`, `functions.k:63-75`, and `functions.k:85-90` allocate, bind, execute, and pop a frame |
| `Return` | `syntax.k:50` is strict | `functions.k:78-90` captures the value and returns abruptly from the exact body suffix |
| `BinOp("%", ...)` | `syntax.k:15` is `seqstrict(2,3)` | `operators.k:12` dispatches after left-to-right operand evaluation |
| `Float(1.0)` | `syntax.k:10` | `float.k:20-21` injects the K float |
| float `%` | `float.k:37` declares total opaque `floatMod` with `no-evaluators` | `float.k:39` dispatches; `float.k:38` supplies the LLVM-only concrete equation |

## Configuration and state

The supplied configuration has `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`,
`<heap>`, `<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>` cells.
The candidate Call claim explicitly fixes all of them. The call rule allocates
scope 1, pushes a frame, binds `number`, executes the body, and the pop rule
deletes scope 1 and restores environment 0 and `scopeLoc` 1. No heap mutation,
exception, output, or allocation is used by this body.

The candidate claim nevertheless begins *after* module loading: it manually
places the closure in scope 0. Thus the fixed `#loadAll`, statement sequencing,
docstring, and `FuncDef` rules are exercised by concrete `krun solution.mpy`
but are absent from the formal reachability claim.

## Functions, opacity, overlaps, and totality

The result-bearing boundary is `floatMod(Float,Float)`, declared
`[function,total,symbol(floatMod),no-evaluators]`. Symbolic Haskell proof does
not evaluate it; the proof establishes only that execution returns the same
opaque term appearing in the destination. The `[concrete]` equation uses
floor-based modulo and is exercised only in the LLVM definition. On the used
domain its second argument is exactly `1.0`, so division-by-zero behavior is
irrelevant.

The used `applyBin("%",Float,Float)` rule is sort-disjoint from the integer
percent rule. Call special cases have priority over the generic `[owise]` call
route, but none matches `Name("truncate_number")`; the generic route is
selected. Cell-aware lookup and bind rules have priority 40, but the manually
supplied ordinary closure has no `$cells` marker, so their guards are false.
No used rule has an incompatible overlapping right-hand side.

A subnormal source-literal probe is deliberately reported narrowly rather than
mislabelled as a bad `floatMod` result. CPython parses `5e-324` as the minimum
binary64 subnormal. The K run stored the raw translated input/expected literal
as `0.49999999999999998e-323`, while `% 1.0` produced
`0.49406564584124654e-323`, the CPython binary64 value; consequently the K
assertion failed. This exposes a missing literal/input-encoding bridge between
translated decimal tokens and CPython binary64 values. It does not witness an
incorrect target result: the observed result agrees with CPython, and the only
literal in `solution.mpy` itself is the exactly representable `1.0`.

Fresh LLVM compilation warned that six unrelated total functions are not
exhaustive on the internal `cellsMark` value: `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt` (six warnings, with the float group
reported separately). None is reached by this program. These warnings are
recorded as a non-material coverage gap; they do not constitute an unsoundness
finding because no false conclusion witness on the intended input domain was
found.

## Rule-by-rule disposition

`05_rule_inventory.txt` enumerates every declaration, context, configuration,
rule, and claim in all 24 supplied K files plus `verification.k` and `spec.k`.
Every used-path rule is individually marked `USED_PATH_REVIEWED`. Every
unused supplied-baseline rule is marked `FIXED_UNUSED_NO_FALSE_WITNESS`: the
audit found no concrete or symbolic false conclusion it enables on this
program's intended domain. This is deliberately narrower than claiming a
universal validation of unused language features.

There is no candidate-local unsound rule and therefore no false-rule witness
to report. The decisive defect is instead claim/program disconnection: changing
the separately submitted program body does not change the claim's separately
embedded closure body.
