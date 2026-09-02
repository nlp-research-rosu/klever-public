# Static assessment ledger

This ledger is keyed to `full-rule-inventory.log`, which enumerates all 1,231
source declarations, including all 704 rules, 234 syntax records, 153 function
declarations, 114 `total` declarations, 34 priority-bearing rules, 47
`concrete` rules, 29 `owise` rules, 25 `symbol` declarations, the one
configuration, and the four submitted claims. There are no simplification
rules. The candidate's supplied-semantics tree is byte-identical to the trusted
tree, so the only candidate-authored theory is `verification.k`.

## File-level disposition covering the complete inventory

| Source | Inventoried rules | Reachability/disposition for this theorem |
|---|---:|---|
| `semantics.k` | 0 | Assembly/import declarations only; `MPY` excludes `MPY-CONCRETE`, while `MPY-KRUN` adds it only for LLVM execution. |
| `syntax.k` | 0 | Constructor grammar and strictness declarations. The used constructors are mapped below. |
| `core.k` | 46 | The used allocation, module loading, sequencing, lookup, argument evaluation, literal, truthiness, and list-helper rules are reviewed below. Remaining rules are constructor-disjoint cell and unused-value support; they cannot match the submitted term. |
| `functions.k` | 15 | Function definition, annotated lambda creation, parameter binding, return, and frame pop are on-path and reviewed below. Unused closure-cell recursion is guarded and constructor-disjoint for empty cell/free-variable lists. |
| `call.k` | 21 | Call routing, builtin dereference, ordinary and annotated closure invocation, and empty cell allocation are on-path and reviewed below. Other builtin/method routing is constructor-disjoint. |
| `sort.k` | 19 | Plain and keyed `sorted` routing is on-path. `sortVS` and `sortKeyVS` are the result-bearing supplied opaque primitives discussed below. Concrete insertion equations are enabled only for ground/LLVM use. Reverse and in-place variants are not in the submitted term. |
| `concrete.k` | 16 | Imported only by `MPY-KRUN`. The keyed-sort loop, real key calls, stable insertion, and allocation are exercised by fresh LLVM tests. Deep list equality and reverse sorting are inactive. |
| `builtins.k` | 137 | Only `bin`, `binCodes`, and `binAcc` are on the submitted/helper-claim path. All other builtin heads require names or constructors absent from the submitted term. |
| `methods.k` | 75 | Only string `count`, `cntSub`, and `dropIS` are on the helper-claim path. Other method names are constructor-disjoint. |
| `str.k` | 28 | String literal conversion and the prefix helper used by `cntSub` are on-path. Other string operators and lexicographic ordering are inactive. |
| `int.k` | 16 | Integer `<` is on-path. Other operator tags are absent. |
| `operators.k` | 10 | Comparison evaluation and dispatch are on-path. Other operator constructors are absent. |
| `controls.k` | 34 | The two guarded `IfExp` rules are on-path. Statement mutation, imports, branches, and loops are absent. |
| `assert.k` | 3 | Used only by the independent LLVM smoke module, not by any proof claim. Both truth branches and heap dereference are ordinary assertion behavior. |
| `list.k` | 27 | List values are consumed by `sorted`, but the submitted term uses no list literal/operator/method rule. The module is otherwise constructor-disjoint. |
| `bool.k` | 13 | Boolean values use `core.k` truthiness; no `BoolOp` node occurs. All rules here are inactive. |
| `comprehension.k` | 7 | No comprehension constructor occurs; inactive macros/rules. |
| `dict.k` | 28 | No dictionary constructor/value occurs; inactive. |
| `float.k` | 121 | No float constructor or float-producing operation occurs; all 22 float opaque symbols and their concrete twins are inactive. |
| `iter.k` | 0 | Iterator declarations only; the submitted term has no iterator consumer. |
| `range.k` | 6 | No range constructor occurs; inactive. |
| `set.k` | 12 | No set constructor occurs; inactive. |
| `subscript.k` | 40 | No subscript/slice constructor occurs; inactive. Its compiler-reported partial `valSeqAt` totalization is not used. |
| `tuple.k` | 21 | No tuple constructor occurs; inactive. |
| `verification.k` | 9 | All seven functions and all nine equations are candidate-authored and are reviewed individually below. |
| `spec.k` | 0 | Four positive reachability claims; each was rerun separately. |

For every rule classified inactive above, its left-hand operation name or AST
constructor is absent from the mechanically matched submitted module and from
all terms generated along the reviewed execution route. None is a
`simplification` rule, so inactive equations cannot rewrite unrelated terms.
Consequently no false conclusion witness from an inactive rule exists on the
intended non-negative-list input domain. This is a theorem-local
classification, not a claim that the supplied minimal Python model covers all
of CPython.

## Used source constructors and operational rules

| Program construct | Declaration / rules | Assessment |
|---|---|---|
| `Module`, `FuncDef`, `Params`, `Return`, `Call`, `Name`, `KwArg`, `Lambda`, `IfExp`, `Compare`, `CmpOp`, `Int`, `Attribute`, `Str` | `syntax.k:9-30,50-61` | Exact translator constructors; constructor comparison is recorded in `constructor-comparison.log`. |
| Module loading and function binding | `core.k:124-127`; `functions.k:14-16` | Executes the real `FuncDef`, binds `"sort_array"` in scope 0, and preserves heap/control cells. The isolated load claim proves this transition. |
| Closure call/frame | `call.k:69-75`; `functions.k:63-66,78-90` | One argument is bound to `"arr"`, a fresh scope is pushed, `Return` produces the value, and pop restores environment/scope while preserving escaping heap objects. Exact arity holds on this path. |
| Name resolution | `core.k:130-181` | `"arr"` resolves in the call frame; `"sorted"` and `"bin"` fall through scope 0 to the fixed builtin scope. No proof-local binding shortcut exists. |
| Callee/argument evaluation | `core.k:183-191`; `call.k:15-32` | Callee then arguments evaluate left-to-right. The inner `sorted(arr)` finishes before the outer key lambda is evaluated. |
| Keyword evaluation | `core.k:94-102` | The key expression evaluates to a tagged `kwV("key", closure)`; guards exclude retagging. |
| Annotated key lambda | `functions.k:50-60` | Empty cell/free-variable lists produce exactly `popcountKeyClosure`; no capture, state, or exception is skipped. |
| Integer branch | `operators.k:14-17`; `int.k:22`; `core.k:199-205`; `controls.k:56-60` | `value < 0` evaluates to a Boolean and selects exactly one branch. Guards are complementary. |
| `bin(value)` | `builtins.k:107-121` | Non-negative branch is exhaustive for the claim guard; recursion decreases by integer halving and yields `"0b"` plus the ordinary binary digits. |
| String literal and `.count("1")` | `str.k:12-17,32-41`; `call.k:15-24`; `methods.k:33-44` | `"1"` becomes code 49; `count` performs a terminating non-overlapping scan. For a one-character pattern this equals the binary popcount. |
| Inner plain `sorted` | `call.k:38-46`; `sort.k:18-24,34-37` | A heap reference is dereferenced, then a fresh heap list containing `sortVS(VS)` is allocated. The symbolic value remains conditional on the supplied primitive. |
| Outer keyed `sorted` | `sort.k:45-66` | A fresh heap list containing `sortKeyVS(sortVS(VS), keyClosure)` is allocated. No local rule bypasses the body; the abstraction is in the fixed supplied semantics. |
| Concrete keyed sort | `concrete.k:20-59` | Calls the real key closure for each element, inserts after equal keys (`not kLt`), hence is stable for ascending mode, and allocates the result. Fresh LLVM tests exercise normal/boundary cases. |
| Heap allocation/state | `core.k:117-121`; `call.k:38-46` | Freshness guard and monotone heap location produce heap 0 for the inner sort and heap 1 for the outer sort; result `ref(1)` is constrained. |

## Candidate-authored verification equations, one by one

| Rule | Class and decision |
|---|---|
| `sortArrayLambda => Lambda(...)` (`verification.k:9-19`) | Truthful definitional constructor. It does not rewrite an executing `Call` or replace fixed semantics. |
| `sortArrayBody => Return(...)` (`:22-27`) | Truthful definitional constructor. Mechanical comparison proves equality with the trusted translation's body. |
| `sortArrayClosure => closureVal("arr", sortArrayBody, 0)` (`:30-31`) | Truthful name for the closure installed by executing the module; the independent load claim proves the connection. |
| `sortArrayModule => Module(FuncDef(...))` (`:34-35`) | Truthful name for the complete submitted module after inert empty-parameter normalization. |
| `popcountKeyClosure => closureValC(...)` (`:41-52`) | Truthful constructor for evaluating the exact annotated lambda. A separate reachability claim executes this closure on arbitrary non-negative integers. |
| `sortArraySpec(VS) => sortKeyVS(sortVS(VS), popcountKeyClosure)` (`:55-56`) | Definitional postcondition summary. It does not replace execution. Its human meaning is conditional on the supplied opaque sorting contracts. |
| `allNonNegativeInts(.ValSeq) => true` (`:59`) | True base case. |
| `allNonNegativeInts(vCons(I,REST)) => I >= 0 and ...` (`:60-61`) | True structurally recursive integer case; strictly decreases on `REST`. |
| `allNonNegativeInts(vCons(_, _)) => false [owise]` (`:62`) | Disjoint fallback after the integer case; makes the total declaration exhaustive over `ValSeq`. |

The seven candidate functions each have complete, non-overlapping equations
over every use. There are no candidate priority, simplification, concrete,
functional, or opaque declarations.

## Opaque/trust findings

`sortVS` and `sortKeyVS` (`sort.k:18,49`) are total, result-bearing opaque
symbols in the proof definition. The main theorem is sound and
interpretation-parametric: it proves that executing the real body returns the
composition of these exact supplied primitives with the exact key closure.
However, no bridge-free K theorem in the mounted inputs establishes that the
opaque functions denote ascending and stable keyed sorting. The proof of the
key closure does not establish that `sortKeyVS` invokes it. The fixed LLVM-only
twin and finite differentials support this contract empirically, but cannot
universally connect the Haskell opaque interpretation to the concrete twin.
This is a trust-boundary limitation, not a false K equation.

The compiler reported non-exhaustive total-function patterns for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt` in the LLVM build.
All are inactive on the submitted proof path. The Haskell proof build only
reported unused pattern variables in truthful `strLt` branches.
