# Exhaustive local K inventory and soundness classification

Scope: `/candidate/semantic.k`, its generated helper `/candidate/list-domain.k`,
and `/candidate/verification.k`. Imported K standard modules are recorded as the
trust boundary rather than re-inventoried. Line numbers below refer to the
immutable candidate files.

## Inventory totals

- Local syntax declarations: 24 (`list-domain.k` 7, `semantic.k` 14,
  `verification.k` 3).
- Local ordinary rules: 32 (`list-domain.k` 15, `semantic.k` 14,
  `verification.k` 3).
- Configurations: one, the single `<k>` cell at `semantic.k:42-43`.
- Explicit `[function]` declarations: 13.
- Explicit `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
  `[owise]`, `[anywhere]`, priority, macro, alias, context, or opaque
  declarations: none.
- Constructor productions carry `[symbol(...)]`; no constructor is opaque.
- Proof claims in these three files: none. The sole entry claim is separately
  inventoried in `spec.k:9-29`.

## Every syntax declaration

| ID | Location | Declaration / productions | Role and assessment |
|---|---|---|---|
| S01 | `list-domain.k:7-8` | `IntList ::= Nil \| Cons(Int, IntList)` | Finite constructor list used for every formal input. |
| S02 | `list-domain.k:10` | `IntList ::= insertInt(Int, IntList) [function]` | Defined insertion helper. |
| S03 | `list-domain.k:15` | `IntList ::= sortInts(IntList) [function]` | Defined insertion sort. |
| S04 | `list-domain.k:19` | `Bool ::= eqIntLists(IntList, IntList) [function]` | Defined structural equality. |
| S05 | `list-domain.k:26` | `Int ::= countInt(Int, IntList) [function]` | Defined multiplicity count. |
| S06 | `list-domain.k:35` | `Bool ::= countsAtMost(IntList, IntList, Int) [function]` | Defined fold of count bounds. |
| S07 | `list-domain.k:41` | `Bool ::= countsAtMostTwo(IntList, IntList) [function]` | Defined limit-2 wrapper. |
| S08 | `semantic.k:9` | `Pgm ::= Module(Stmt)` | Exact translator constructor. |
| S09 | `semantic.k:11` | `Params ::= Params(String)` | One-parameter translator constructor. |
| S10 | `semantic.k:12` | `CellVars ::= CellVars(String)` | One captured-name constructor. |
| S11 | `semantic.k:13` | `FreeVars ::= FreeVars()` | Empty free-variable constructor. |
| S12 | `semantic.k:15-17` | `Stmt ::= FuncDef(...) \| Return(Expr)` | The two statement forms in the submitted module. |
| S13 | `semantic.k:19-26` | `Expr ::= Name \| Int \| Bool \| Attribute \| Call \| BoolOp \| Compare \| GenExp` | Every expression constructor in `solution.mpy`; unsupported AST forms remain absent. |
| S14 | `semantic.k:27` | `CmpOp ::= CmpOp(String, Expr)` | Translator comparison-pair constructor. |
| S15 | `semantic.k:28-29` | `CompFor ::= CompFor(Expr, Expr, Expr)` | Translator generator-clause constructor. |
| S16 | `semantic.k:31-33` | `Value ::= IntVal \| BoolVal \| PyList(IntList)` | Minimal runtime value domain. |
| S17 | `semantic.k:39-40` | `KItem ::= Run(Pgm, Value) \| EvalStmt(Stmt, Map)` | Entry and explicit-environment evaluation terms. |
| S18 | `semantic.k:53` | `Value ::= eval(Expr, Map) [function]` | Partial expression evaluator, complete for the submitted term. |
| S19 | `semantic.k:58` | `IntList ::= asList(Value) [function]` | Partial, typed projection. |
| S20 | `semantic.k:61` | `Bool ::= asBool(Value) [function]` | Partial, typed projection. |
| S21 | `semantic.k:64` | `Bool ::= eqValue(Value, Value) [function]` | Same-constructor equality cases used by list equality. |
| S22 | `verification.k:9` | `Bool ::= ascending(IntList) [function]` | Formal definition: fixed point of ascending sort. |
| S23 | `verification.k:12` | `Bool ::= duplicateBound(IntList) [function]` | Formal multiplicity bound. |
| S24 | `verification.k:15` | `Bool ::= isSortedContract(IntList) [function]` | Conjunction used in the entry postcondition. |

All constructor spellings used by `solution.mpy` occur in S08-S16. `Module`,
`FuncDef`, and `Params` are consumed by R16; `Return` by R17; `BoolOp`,
`Compare`, `Name`, `Call`, and `Int` by R18-R30; `Attribute`, `GenExp`,
`CompFor`, and the generator variable are intentionally consumed as part of the
exact fused R30 pattern. `CellVars` and `FreeVars` are parsed and framed by R16.
Inputs use S01 and `PyList`.

## Every rule

“Sound” means the equation or transition is true over its complete match
domain in this declared minimal value/AST model. “Supported-scope limitation”
means other Python programs can get stuck; the submitted program does not use
those missing cases, and the rule does not produce a known false result.

| ID | Location | Rule summary | Guard/overlap, descent, footprint, and decision |
|---|---|---|---|
| R01 | `list-domain.k:11` | `insertInt(I, Nil) => Cons(I, Nil)` | Base insertion; disjoint from nonempty rules. Sound. |
| R02 | `list-domain.k:12` | Insert before head when `I <=Int J`. | Guard disjoint from R03 and includes equality. Sound. |
| R03 | `list-domain.k:13` | Retain head and insert into tail when `I >Int J`. | Complement of R02; strict structural descent. Sound. |
| R04 | `list-domain.k:16` | `sortInts(Nil) => Nil` | Base sort. Sound. |
| R05 | `list-domain.k:17` | Sort tail, then insert head. | Strict descent on input tail; ordinary insertion sort. Sound. |
| R06 | `list-domain.k:20` | `eqIntLists(Nil, Nil) => true` | Constructor-disjoint base equality. Sound. |
| R07 | `list-domain.k:21` | Empty versus nonempty is false. | Constructor-disjoint. Sound. |
| R08 | `list-domain.k:22` | Nonempty versus empty is false. | Constructor-disjoint. Sound. |
| R09 | `list-domain.k:23-24` | Nonempty equality is head equality and tail equality. | Strict descent on both tails; implements Python integer-list equality. Sound. |
| R10 | `list-domain.k:27` | Count in empty list is zero. | Base count. Sound. |
| R11 | `list-domain.k:28-29` | Equal head contributes one. | Guard `I ==Int J`; disjoint from R12; strict descent. Sound. |
| R12 | `list-domain.k:30-31` | Unequal head contributes zero. | Guard `I =/=Int J`; complement of R11; strict descent. Sound. |
| R13 | `list-domain.k:36` | Empty item stream satisfies any limit. | Models vacuous `all`; source/limit intentionally irrelevant. Sound. |
| R14 | `list-domain.k:37-39` | Check current item’s source count and recurse through items. | Strict descent on `ITEMS`; exactly folds `count <= LIMIT`. Sound. |
| R15 | `list-domain.k:42` | Specialize `countsAtMost` to limit 2. | Transparent wrapper. Sound. |
| R16 | `semantic.k:48-49` | Invoke the one-argument `is_sorted` body with singleton binding `X |-> V`. | Reads/writes only `<k>`; preserves suffix; module contains one supported function. It ignores captured/free-variable metadata but the exact body’s only required capture is resolved from the parameter map. Sound for the supported invocation and exact claim. |
| R17 | `semantic.k:51` | Evaluate a returned expression in `RHO`. | Reads/writes only `<k>` and preserves continuation. There is no heap, output, allocation, mutation, exception, or call stack in the exercised pure program. Sound. |
| R18 | `semantic.k:54` | `eval(Int(I), _) => IntVal(I)` | Constructor-disjoint literal equation. Sound. |
| R19 | `semantic.k:55` | `eval(Bool(B), _) => BoolVal(B)` | Constructor-disjoint literal equation. Sound. |
| R20 | `semantic.k:56` | Resolve `Name(X)` from a map containing `X |-> V`. | K Map uniqueness prevents a conflicting duplicate key; exact binding lookup. Sound. |
| R21 | `semantic.k:59` | `asList(PyList(IS)) => IS` | Typed projection. Partial on other `Value` constructors, but never misreturns. Sound. |
| R22 | `semantic.k:62` | `asBool(BoolVal(B)) => B` | Typed projection. Partial on non-booleans, but never misreturns. Sound. |
| R23 | `semantic.k:65` | List `eqValue` delegates to structural integer-list equality. | Value-constructor-disjoint. Sound. |
| R24 | `semantic.k:66` | Integer `eqValue` uses K integer equality. | Value-constructor-disjoint. Sound. |
| R25 | `semantic.k:67` | Boolean `eqValue` uses K boolean equality. | Value-constructor-disjoint. Sound. Cross-type Python equality is unmodeled, not falsely equated; unused by the program. |
| R26 | `semantic.k:71-72` | Boolean-valued `and` evaluates to K boolean conjunction. | Top constructor/operator disjoint from other `eval` rules. The rule requires both operands to project to booleans; the exact operands do. Python operand-return behavior for non-booleans is intentionally unsupported. On the exercised pure, total boolean operands, eager/denotational presentation has the same value and no different state/control effect. Sound for every completing match; unused AST cases may stick. |
| R27 | `semantic.k:74-75` | `==` comparison delegates to `eqValue`. | Operator/top-constructor disjoint. Exact program compares two integer lists. Sound; cross-type cases may stick instead of giving Python’s result. |
| R28 | `semantic.k:77-78` | `sorted` on a projected integer list returns insertion sort. | Exact standard-builtin assumption, no mutation; insertion stability is unobservable for integers. Sound. |
| R29 | `semantic.k:83-91` | Fused evaluation of `all(source.count(x) <= LIMIT for x in source)`. | Exact AST pattern, correct `SOURCE` binding, and no filter. R14 checks every occurrence from the same finite source, using R10-R12 for Python integer equality. Rechecking duplicates changes cost only, not the boolean. This is a result-bearing high-level semantic bridge, but its value is exhaustively fixed by recursive equations rather than opaque or fresh. Sound on all `PyList(IS)`/integer `LIMIT` matches. The lack of an independently machine-checked lower-level generator/count connection is a trust/evidence limitation, not a witnessed false rule. |
| R30 | `verification.k:10` | `ascending(IS) => eqIntLists(IS, sortInts(IS))`. | Transparent definition, not an oracle. R04-R09 fully fix the value. Equality with an ascending insertion sort is mathematically equivalent to nondecreasing order for finite integer lists; that equivalence is not a separate K lemma. Sound definition with an informal intent bridge. |
| R31 | `verification.k:13` | `duplicateBound(IS) => countsAtMostTwo(IS, IS)`. | Transparent definition fully fixed by R10-R15. Exactly “no occurring value has multiplicity above two.” Sound. |
| R32 | `verification.k:16` | Contract is `ascending andBool duplicateBound`. | Transparent conjunction of R30-R31. Sound. |

Note: the semantic rule count is 14. R18-R20 and R26-R29 are the seven
`eval` rules; R16-R17, R21-R25 are the remaining seven. There is no omitted
semantic rule.

## Configuration, evaluation, and overlap audit

The configuration is only `<k> Run($PGM, $ARGS) </k>`. This is adequate because
the submitted function is pure: it reads its list, allocates only unobservable
Python temporaries (`sorted` output, generator/count traversal), and returns a
boolean. The explicit `Map` is passed inside `EvalStmt`; no rule mutates it.
There is no modeled I/O, heap identity, mutation, exception, or concurrency.

The exact program’s control path is:

`Run` (R16) → `EvalStmt(Return(...), map)` (R17) → nested `eval`
(R18-R29) → `BoolVal(...)`.

Top constructors or literal operator strings make the `eval` rules pairwise
disjoint. List-function constructor cases and guarded integer cases are
pairwise disjoint. Every recursive helper decreases a finite `IntList`. No
priority is needed, and none is declared. The equations used on the exact
program cover every normal input in the formal `IntList` domain.

## Trust boundary and conclusion

The imported `INT`, `BOOL`, and `MAP` modules supply unbounded mathematical
integer arithmetic/comparison, boolean operations, and finite-map matching.
Standard K constructor/function machinery is also trusted.

There is no fresh value, unconstrained oracle, answer-returning axiom,
simplification, totality assertion, or task-specific rule that rewrites the
whole function directly to `isSortedContract`. R29 is task-shaped, but computes
the actual submitted generator expression through fully defined count/fold
equations. The K proof’s universal result therefore depends on the audited
semantic correspondence of R28-R29 and the ordinary-mathematics intent bridge
for R30; those are the only material non-machine-proved bridges.
