# Static rule review

The mechanically generated exhaustive declaration-by-declaration inventory is
[`rule_inventory.md`](rule_inventory.md), produced by
[`rule_inventory.py`](rule_inventory.py). It lists all 697 local rules, 229
syntax declarations, 148 function-bearing syntax declarations, 108 `total`
declarations, 32 `[concrete]` rules, 29 priority rules, 26 `[owise]` rules, five
contexts, the configuration, and the sole claim, with source lines and collapsed
bodies/guards. No local `[simplification]` declaration exists.

## Per-module disposition

The following table is the disposition ledger for every inventoried item.
"Inert" means that no head symbol in that group is reachable from this
program/claim execution; such a rule cannot contribute to closure or fabricate
this result. It is still part of the fixed supplied language theory, but the
theorem makes no claim about the associated Python construct.

| Source/module | Rules | Disposition |
|---|---:|---|
| `semantics.k` / `MPY`, `MPY-KRUN` | 0 | Assembly/import declarations only; proof imports `MPY`, not concrete-only `MPY-CONCRETE`. |
| `syntax.k` / `MPY-SYNTAX` | 0 | All 16 syntax groups inventoried. The used constructor map is detailed below; unused constructs are inert. |
| `core.k` / `MPY-CORE` | 46 | Configuration, sequencing, values, allocation, lookup, evaluation-order loops, and structural helpers reviewed. Used rules preserve all claimed cells. Cell/keyword and unrelated operator helpers are inert. |
| `iter.k` / `MPY-ITER` | 0 | Iterator constructors only; inert. |
| `range.k` / `MPY-RANGE` | 6 | Inert. Recursive equations have disjoint guards for nonzero valid ranges. |
| `operators.k` / `MPY-OPERATORS` | 10 | Inert for this body: method routing does not use unary/binary/compare nodes. |
| `int.k` / `MPY-INT` | 16 | Inert except ordinary integer equality used in helper guards; K integer hooks are trusted mathematics. |
| `bool.k` / `MPY-BOOL` | 13 | Inert except Boolean hook evaluation of helper guards; no source `BoolOp`. |
| `float.k` / `MPY-FLOAT` | 121 | Entirely inert. Its opaque float symbols and concrete twins do not occur in the proof residual or result. |
| `str.k` / `MPY-STR` | 28 | `Str`, `strToCodes`, and `seqConcat` are used. Comma and ASCII-space literals satisfy the ASCII guard, and concatenation is structurally recursive. Membership/order rules are inert. |
| `set.k` / `MPY-SET` | 12 | Inert. |
| `list.k` / `MPY-LIST` | 27 | `valSeqConcat` is used by `flushTok`; its two equations are disjoint, exhaustive, and descending. Literal/comparison/mutation/membership rules are otherwise inert. |
| `tuple.k` / `MPY-TUPLE` | 21 | Inert. |
| `subscript.k` / `MPY-SUBSCRIPT` | 40 | Inert. Its deliberately total/underspecified OOB `valSeqAt` boundary does not enter this proof. |
| `comprehension.k` / `MPY-COMPREHENSION` | 7 | Inert macro expansion rules. |
| `methods.k` / `MPY-METHODS` | 75 | The replace and no-argument split path is material. Replace is faithful for the exact one-character arguments. Split has a material false value bridge described below. Other methods are inert. |
| `controls.k` / `MPY-CONTROLS` | 34 | Inert; the function has no assignment, branch, loop, import, or expression statement. |
| `functions.k` / `MPY-FUNCTIONS` | 15 | Plain parameter binding, return, and pop rules are used and preserve the observed heap while restoring control. Annotated-closure rules are inert. |
| `builtins.k` / `MPY-BUILTINS` | 137 | Inert; no builtin name is called. Registry entries are available only through the root scope. Opaque MD5 is not used. |
| `call.k` / `MPY-CALL` | 21 | Generic callee evaluation, bound-method dispatch, and plain-closure invocation are used. Argument evaluation remains the shared left-to-right loop. Builtin/type/ref/annotated-closure cases are inert. |
| `sort.k` / `MPY-SORT` | 19 | Entirely inert. Opaque `sortVS`/`sortKeyVS` cannot affect this claim. |
| `assert.k` / `MPY-ASSERT` | 3 | Inert in the target proof; used only by independent concrete harnesses. |
| `dict.k` / `MPY-DICT` | 28 | Inert. |
| `concrete.k` / `MPY-CONCRETE` | 16 | Excluded from the Haskell proof by construction and unrelated to the function. |
| `verification.k` | 2 | Both proof extensions are analyzed below. |
| `spec.k` | 0 | One reachability claim; result-constraining and satisfiable, but intent-inadequate because of the used split bridge. |

For groups marked inert, constructor disjointness supplies the proof-impact
decision: their left-hand heads cannot match any term on the call/replace/split/
return path. Partiality, intentionally opaque total functions, and subset
approximations in those groups therefore do not prove or assume any step of this
claim. The complete source text remains in the exhaustive inventory so this
grouping does not omit any declaration.

## Used syntax-to-rule map

| Submitted constructor | Declaration | Material execution |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k:53,57,61` | The trusted translation has one binding; `functions.k:14-16` would bind exactly the closure mechanically compared to the theorem. |
| `Return` | `syntax.k:50` `[strict]` | Its expression evaluates before `functions.k:78-90` records the return, pops the frame, restores env/scopeLoc, removes the callee scope, and preserves the allocated heap result. |
| `Call` | `syntax.k:28` | `call.k:20-21` evaluates the callee then `core.k:189-191` evaluates arguments left-to-right; `call.k:69-75` enters the plain closure. |
| `Attribute` | `syntax.k:29` `[strict(1)]` | `call.k:16` creates `boundMethodV` after receiver evaluation. |
| `Name("s")` | `syntax.k:12` | `core.k:131-154` finds the parameter in the fresh callee frame. |
| `Str(",")`, `Str(" ")` | `syntax.k:13` | `str.k:13-17` creates code sequences 44 and 32; both satisfy its ASCII guard. |
| `str`, `list`, `ref`, `closureVal`, `boundMethodV`, `IntSeq`, `ValSeq` | `core.k:13-34` | These are the value constructors carried through the claim. |
| `replace` | `methods.k:104-109` | `applyMethod` recursively replaces every code 44 with 32; guards are complementary and recursion descends. |
| no-argument `split` | `methods.k:72-86` | Priority 40 routes the exact bound-method call to allocation of `list(splitWS(...))`; this bridge is value-incorrect for part of real Python's domain. |
| result allocation | `core.k:117-121` | Fresh heap location 0 is allocated and heapLoc becomes 1, exactly as the postcondition requires. |

There are no source helpers or loops and no auxiliary/circularity claims.

## Proof-extension records

### `wordsStringFunction`

- Class: definitional program constructor / entry shortcut.
- Domain and context: the nullary function symbol reduces in any term context
  to a plain closure with parameter `s`, the exact submitted body, and defining
  scope 0. It reads or writes no cells.
- Binding/control effect: the entry claim calls that closure directly instead
  of loading the module and looking up `words_string`. Clean `krun` of the
  submitted module binds the same closure at scope 0. The constructor comparison
  mechanically proves equality of the function name, parameter sequence, and
  body after only list-tail surface normalization.
- Value influence: all program execution flows through the closure body.
- Validation: the body mutation comma→`x` fails with a residual unequal heap
  summary, so this is not an answer oracle independent of the body.
- Limitation: the claim omits the persistent module binding from its observable
  final scope. This is semantically inert for this nonrecursive body and is an
  allowed entry-function normalization, not a substitution.

### `wordsStringExpected`

- Class: definitional result summary.
- Complete domain: every `CS:IntSeq`.
- Equation: exactly
  `splitWS(replaceC(CS,44,32), .IntSeq, .ValSeq)`.
- State/control effect: none; it appears only in the target heap value.
- Coverage/termination/overlap: one unconditional equation; `replaceC`,
  `splitWS`, `flushTok`, `seqConcat`, and `valSeqConcat` recurse structurally
  under complementary guards.
- Value influence: it fully fixes heap object 0 and hence the returned list.
- K-level justification: fixed program execution independently reaches the same
  fixed-semantics helper term. There is no fresh/opaque program-derived value.
- Intent-level failure: using the same fixed helper term in execution and the
  postcondition establishes only the supplied semantics' split result. The
  claimed bridge to Python whitespace splitting is false.

## Material unsound used bridge

The operational bridge at `methods.k:72-86` replaces the evaluated no-argument
bound string method with allocation of `list(splitWS(CS,...))`. Its context,
control, continuation, heap allocation, and heapLoc update are appropriate.
Its result-bearing value is not faithful over the full match domain because
`isWSC(C)` is true only for code points 32, 9, 10, and 13.

Concrete false-conclusion witness:

- Input: Python string `"a\u000bb"`; theorem value
  `CS = [97, 11, 98]`.
- Real canonical and submitted Python results: `["a", "b"]`.
- Fixed K execution and claimed `wordsStringExpected`: `["a\u000bb"]`.
- The reviewer harness translated byte-identically, passed under Python, and
  exited 1 under clean K execution with the one-word actual list and two-word
  assertion list visible in the heap.

Thus the rule can and does enable a false conclusion for a satisfying intended
input. This is not a timeout, symbolic-evidence gap, or concern about an
unreachable rule. Unicode whitespace supplies additional witnesses, and the
concrete literal semantics itself becomes stuck beyond ASCII.

## Opaque and total boundaries

The full imported theory declares opaque or deliberately underspecified
boundaries for floats (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`), sorting (`sortVS`, `sortKeyVS`), MD5 (`md5hexCodes`), and total OOB
list access (`valSeqAt`). LLVM compilation also warns about non-exhaustive
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`.

None of these symbols occurs in the submitted body, target claim, proof-local
equations, successful residual, or mutated residual. They are accepted only as
inert parts of the supplied fixed definition, not as evidence for this result.
