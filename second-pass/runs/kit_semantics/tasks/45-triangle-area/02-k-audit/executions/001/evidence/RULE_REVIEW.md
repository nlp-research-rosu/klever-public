# Rule-by-rule static review record

This record is keyed to `16-k-inventory.log`, which lists every non-comment K
source line with its path, original line number, and declaration attributes.
That inventory contains 695 source `rule` declarations, 227 `syntax`
declarations, 110 occurrences of `total`, 149 function declarations, 45
priority occurrences, 36 concrete occurrences, 25 `symbol` occurrences, 22
`no-evaluators` occurrences, four claims, and no local `simplification` or
`functional` declaration. The decisions below apply to every inventoried row
of each named module; target-path rows are then identified individually.

## Assembly, syntax, configuration, and target execution

- `semantics.k`: both modules and all imports are assembly declarations. The
  proof imports `MPY`, not `MPY-KRUN`, so the LLVM-only `MPY-CONCRETE` rules do
  not enter the proof theory. No operational rule is declared here.
- `semantics/syntax.k`: all productions describe the translator-emitted AST.
  The target uses `Module`, `FuncDef`, `Params`, `Return`, `BinOp`, `Name`,
  `Float`, and `Call`. `BinOp` is `seqstrict(2,3)` and `Return` is strict, which
  gives the required left-to-right operand evaluation before return. Other
  productions are unused by the target; none rewrites a result.
- `semantics/core.k`: the configuration at lines 49-60 is exactly the entry
  state in all claims. Target execution uses module loading/sequencing
  (125-127), name lookup (131-154), argument evaluation (185-191), and shared
  literal/operator declarations (193-210). The lookup rules select the
  just-created local/module bindings and preserve all cells. The remaining
  allocation, closure-cell, keyword, truthiness, collection, and helper rules
  are not reached by this program. They are ordinary subset semantics and do
  not overlap the target redexes.
- `semantics/functions.k`: the target uses ordinary function definition
  (14-16), parameter binding (63-66), return (78-79), and frame pop (85-90).
  The abrupt return discards the callee-body suffix, while pop restores the
  exact caller continuation, environment, scope location, stack, and return
  state. Annotated-closure/cell rules and implicit `None` return are unused.
- `semantics/call.k`: the target uses generic callee/argument routing (20-21)
  and the ordinary closure frame rule (69-75). It evaluates the callee, then
  arguments left-to-right through `#evalArgs`, binds the selected closure, and
  pushes the exact caller continuation. Builtin, method, ref-deref, and
  annotated-closure rules are unused and have disjoint top symbols or value
  constructors.
- `semantics/operators.k`: target `BinOp` dispatch uses line 12 after syntax
  strictness. Ref-deref and comparison rules are unused and cannot intercept
  Int/Float operands.
- `semantics/int.k`: only Int×Int multiplication at line 14 is used. It is the
  ordinary mathematical-integer product. All other arithmetic/comparison rules
  are unused. Their guards are sort/operator disjoint from the target step.
- `semantics/float.k`: target rules are Float literal evaluation (19), Int/Float
  true-division dispatch (24-27), opaque `subF/divF/addF/mulF/powF` declarations
  and concrete twins (103-121), mixed multiplication (140-141 and duplicate
  agreeing rules 219-220), and `intToF` (195-197). In the target, the final
  denominator is the fixed nonzero literal `2.0`. Duplicate mixed rules have
  identical right-hand sides on their overlaps.
- `verification.k`: it only requires the immutable supplied semantics and
  imports `MPY`. It adds no syntax, function, totality assertion, opaque symbol,
  priority, ordinary rule, simplification, macro, lemma, or auxiliary claim.
- `spec.k`: its four claims are the only proof declarations. They are symbolic
  over Int×Int, Int×Float, Float×Int, and Float×Float, with no guard. Each exact
  translated module occurs under `#loadAll`, calls the resulting binding, fixes
  the result term, consumes the computation, and restores/constrains every
  configuration cell.

## Inventoried modules not reached by the target

Every rule and declaration in the following modules was inspected in
`16-k-inventory.log`. None of their redexes occurs in the submitted module or
the four target calls, and none is a simplification/global equation over the
target's result symbols.

- `assert.k`: three assertion/heap-deref rules; smoke-only, unused.
- `bool.k`: 13 boolean, short-circuit, and heap-ref rules; unused.
- `builtins.k`: 137 builtin/fold/tokenizer/digest rules. The opaque
  `md5hexCodes` primitive is unused.
- `comprehension.k`: seven comprehension macro rules; unused.
- `concrete.k`: 16 LLVM-only deep-equality/keyed-sort rules; excluded from the
  Haskell proof module and unused by the concrete target.
- `controls.k`: 34 assignment/import/branch/loop/control rules; unused.
- `dict.k`: 28 ordered-dict rules; unused.
- `iter.k`: iterator syntax only; unused.
- `list.k`: 27 list/iteration/equality/allocation rules; unused.
- `methods.k`: 75 string/list method and helper rules; unused.
- `range.k`: six range rules; unused.
- `set.k`: 12 set/helper rules; unused.
- `sort.k`: 19 sort rules, including opaque `sortVS` and `sortKeyVS`; unused.
- `str.k`: 28 ASCII string/helper rules; unused.
- `subscript.k`: 40 indexing/slicing rules, including total under-specified
  `valSeqAt`; unused.
- `tuple.k`: 21 tuple/target-binding rules; unused.

These fixed modules intentionally implement a limited Python subset. Total
helpers with compiler warnings (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`) do not appear in the target dependency slice.
The warnings are therefore evidence gaps for reuse, not mechanisms that close
these claims.

## Opaque values and concrete bridges

All 22 `no-evaluators` declarations are listed in
`23-special-k-attributes.log`. Only four families influence the result here:

- `intFloatDiv(Int,Float)` for Int×Int after exact integer multiplication;
- `intToF(Int)` for each mixed multiplication;
- `mulF(Float,Float)` for mixed and Float×Float multiplication;
- `divF(Float,Float)` for mixed and Float×Float final division.

They are fixed external arithmetic primitives, not program-defined summaries.
The body executes up to ordinary arithmetic dispatch, and the theorem returns
the exact primitive term without asserting a separate numerical equation.
Thus the K claim is interpretation-parametric in these opaque symbols. Their
LLVM `[concrete]` equations are empirical/model bridges, not universal
Haskell-proved facts.

## Concrete false-conclusion/model witnesses

Two fixed-semantics limitations were found. Neither is introduced by
`verification.k`.

1. **Target-reachable integer-to-float exception gap.** For
   `A = 2**1024, H = 1`, CPython canonical and generated implementations both
   raise `OverflowError("int too large to convert to float")`
   (`04-python-differential.log`). The supplied LLVM semantics instead reaches
   `.K`, `NoExc`, exit 0 (`09-krun-huge-int.log`), and the symbolic Int×Int
   claim admits that same input with a normal opaque `intFloatDiv` result. Thus
   any unconditional bridge from the K claim to exact CPython control behavior
   over every mathematical `Int` would be false. The valid K theorem must be
   read relative to MPY's numeric primitive/exception model.
2. **Off-target NaN comparison gap.** `float.k` defines Float `>=` as
   `notBool floatLt` and `<=` as `notBool gtF` (lines 129-130). For a NaN
   operand, Python makes both ordered comparisons false while these negations
   are true after their concrete comparison returns false. This is a concrete
   false-rule witness for comparison claims, but no comparison occurs in this
   program and the rule cannot help close any target claim.

Similarly, the fixed Float division rules do not model Python
`ZeroDivisionError` at a zero divisor. The target divisor is syntactically and
semantically fixed at `2.0`, so no satisfying target input reaches that bad
case. No false conclusion witness was found for the target-path equations at
the fixed divisor and ordinary finite Int/Float inputs.
