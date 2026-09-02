# Static rule review

This review is keyed to every record in `rule_inventory.md`; the one-row-per-ID
decision ledger is `rule_decisions.tsv`.

## Scope and result

The inventory contains 959 records: 237 syntax declarations, one configuration,
five contexts, 714 rules, and two claims. It contains 115 `[total]`
declarations, 25 `symbol`/`no-evaluators` boundaries, 48 concrete rules, 33
priority occurrences, and no simplification or functional declarations. Every
record has an explicit decision in the TSV. No candidate proof-local rule is an
operational bridge, simplification, priority rewrite, opaque oracle, or
unconstrained result producer.

## Constructor-to-rule map for `solution.mpy`

| Submitted construct | Declaration/evaluation path | Decision |
|---|---|---|
| `Module`, statement list | `syntax.k`; `core.k` `#loadAll` and statement sequencing | Exact left-to-right module execution. |
| `ImportFrom("typing","List")` | `syntax.k`; `controls.k` non-math import rule | It is executed as typing-only no-op. Python would bind `List`, but the name is never read and this cannot affect the function return. |
| `FuncDef`, closure, call, return | `functions.k` and `call.k`; `core.k` lookup | Exact name binding, two-argument binding, call frame, body, return, frame restoration/deallocation. No closure escapes. |
| docstring `Expr(Str(...))` | `str.k` literal; `controls.k` expression discard | Exact inert docstring behavior for this theorem. |
| name assignments | strict syntax; `controls.k` assignment | RHS evaluates first and current function scope is updated. |
| `zip(a,b)` | lookup/call; `builtins.k` lines 164 and 171-174 | Exact string-code pairing and truncation at the shorter input. |
| `For` | strict iterable; `controls.k` lines 69-74 | Iterable evaluated once; each yielded pair is bound, body runs, and loop recurs. |
| tuple target `(x,y)` | `tuple.k` `#bindTgt/#unpackSeq` | Binds `x` then `y` from the exact two-element tuple. |
| `Compare(x == y)` | `operators.k`; `str.k` line 25 | Both operands evaluate left-to-right and code-sequence equality selects the branch. |
| string `+` | `operators.k`; `str.k` `seqConcat` and line 24 | Exact immutable string-code concatenation. |
| `If` | strict test; `controls.k` branch rules | Exactly one branch executes from truthiness of the Bool comparison. |

Every material operation and control effect therefore executes under the fixed
semantics. The program path allocates no heap objects and raises no modeled
exception; heap, heap counter, return state, stack, exit code, and non-local
scopes are correctly framed.

## Module decisions, exhaustive ranges

- `INV-0001`–`INV-0928` are the supplied fixed semantics. The detailed ledger
  records every item. The used path above was checked rule-by-rule for
  evaluation order, guards, priority, state footprint, and control. Remaining
  modules are operation-specific and unreachable from this submitted
  constructor tree.
- `INV-0001`–`INV-0017` (assert/bool): coherent success/failure and
  short-circuit rules; only concrete smoke assertions use `assert`.
- `INV-0018`–`INV-0192` (builtins): zip's creation/yield/done guards are
  disjoint and complete for string pairs. Other builtins are unused.
- `INV-0193`–`INV-0216` (call): callee and arguments evaluate in order; the
  closure dispatch preserves the caller continuation and all state cells.
- `INV-0217`–`INV-0247` (comprehension/concrete): unused. The LLVM-only rules
  are not imported by the proof definition.
- `INV-0248`–`INV-0284` (controls): the used assignment, import, expression,
  if, and for rules are exact; priority rules only dereference heap refs, which
  this path never has. Break/continue/while are unused.
- `INV-0285`–`INV-0368` (core): configuration, lookup, sequencing, builtins
  scope, literal evaluation, truthiness, and structural folds are coherent.
  Priority-40 cell lookup cannot match the plain function frame (no `$cells`).
- `INV-0369`–`INV-0563` (dict/float): unused limited sublanguages. All opaque
  float symbols are fixed-semantics trust boundaries with no target dependent.
- `INV-0564`–`INV-0599` (functions/int): the unannotated-closure path is exact.
  Cell closures and Python integer operators are otherwise unused.
- `INV-0600`–`INV-0797` (iterator/list/methods/operators/range/set/sort):
  iterator declarations and generic operator dispatch support the used
  zip/string path; collection methods, range, set, and opaque sorts are unused.
- `INV-0798`–`INV-0928` (str/subscript/syntax/tuple): string literal,
  concatenate, compare, grammar, and tuple unpacking match the program.
  Index/slice rules are unused.

The fresh LLVM build reported incomplete match coverage for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. Their precise inventory
records are marked `LIMITATION_UNUSED_NO_FALSE_TARGET_CONCLUSION`; none of
their symbols or callers occurs in the submitted term, proof-local helpers, or
claims. These are fixed-semantics coverage limitations, not equations enabling
a false XOR conclusion. No claim of global Python completeness is made.

The named opaque boundaries `md5hexCodes`, float operations/conversions,
`sortVS`, and `sortKeyVS` are likewise all unused. There is no empirical or
opaque bridge on the material target path.

## Candidate proof-local decisions

- `INV-0929`–`INV-0930`: `binaryCode` is exactly membership in ASCII
  `{48,49}` and is total.
- `INV-0931`–`INV-0933`: the two `xorCode` guards are disjoint; under
  `binaryCode(A) ∧ binaryCode(B)` they cover equality and inequality and return
  the four-row XOR truth table.
- `INV-0934`–`INV-0940`: `xorAcc` and `binaryCodes` recurse structurally.
  The two base cases are disjoint and implement zip truncation; the recursive
  case appends exactly one XOR code.
- `INV-0941`–`INV-0947`: `xorLastX/Y` recurse over the same paired suffix and
  exactly model the last tuple binding, retaining the prior value when no pair
  exists.
- `INV-0948`–`INV-0957`: target, loop body, function body, closure, and module
  are definitional aliases only. The constructor-pinning claim proves the
  module alias equals the trusted-regenerated term. The body mutation changes
  this term and makes the real proof stick.
- `INV-0958`: the loop claim is a fixed-semantics auxiliary execution theorem,
  universally quantified over `CONT`. Its match context and justification
  context coincide: the exact target/body, current environment/frame, binary
  remaining suffixes, arbitrary continuation, and framed untouched cells.
  It returns normally and cannot discard or fabricate control.
- `INV-0959`: the entry claim starts from a realizable initial configuration,
  loads the pinned module, calls the selected `"string_xor"` binding, and
  requires the returned `Str` to equal `xorAcc(.IntSeq,A,B)`. The result is not
  fresh, existential, tautological, or merely implied one way.

No guards overlap with disagreeing right-hand sides, every recursive helper
descends on an algebraic sequence, and all `[total]` proof-local declarations
cover their stated constructor domains. No false-conclusion witness exists for
any candidate proof-local rule; accordingly none is labeled unsound.
