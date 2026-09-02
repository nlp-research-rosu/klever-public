# Reviewer rule and syntax inventory

Scope: scratch copies of candidate `semantic.k`, `verification.k`, and `spec.k`.
Line numbers below refer to those source files. The intended execution domain is
the exact submitted module applied to finite lists of mathematical integers.

## Local syntax declarations

| ID | Source | Declaration | Used by submitted program / decision |
|---|---|---|---|
| Y1 | `semantic.k:8` | `Pgm ::= Module(Stmts)` | Outer submitted AST; faithful. |
| Y2 | `semantic.k:10` | `Stmts ::= List{Stmt,""}` | Orders import, definition, and function body; faithful. |
| Y3 | `semantic.k:11-14` | `Stmt ::= ImportFrom \| FuncDef(3-field) \| FuncDef(5-field) \| Return` | Submitted AST uses import, 5-field function, and return. The 3-field form is unused compatibility syntax. |
| Y4 | `semantic.k:16` | `Strings ::= List{String,","}` | Represents imported names and empty free-variable list; faithful. |
| Y5 | `semantic.k:17` | `Params ::= Params(Strings)` | Submitted parameter `"numbers"`; faithful. |
| Y6 | `semantic.k:18` | `CellVars ::= CellVars(Strings)` | Parses translator metadata; no runtime role is needed here. |
| Y7 | `semantic.k:19` | `FreeVars ::= FreeVars(Strings)` | Parses translator metadata; exact submitted value is empty. |
| Y8 | `semantic.k:21` | `Exprs ::= List{Expr,","}` | Parses the one count argument and comprehension predicates. |
| Y9 | `semantic.k:22-27` | `Expr ::= Name \| Int \| Attribute \| Call \| Compare \| ListComp` | Exactly the expression forms in `solution.mpy`; all used except no standalone source integer beyond predicate `1`. |
| Y10 | `semantic.k:28` | `CmpOps ::= List{CmpOp,","}` | Parses the one equality comparison. |
| Y11 | `semantic.k:29` | `CmpOp ::= CmpOp(String,Expr)` | Exact submitted `CmpOp("==",Int(1))`. |
| Y12 | `semantic.k:30` | `CompFors ::= List{CompFor,""}` | Parses the one generator. |
| Y13 | `semantic.k:31` | `CompFor ::= CompFor(Expr,Expr,Exprs)` | Exact generator target, iterable, and predicate. |
| Y14 | `semantic.k:39` | `Ints ::= List{Int,","}` | Finite integer-list runtime and symbolic representation; matches the intended input domain. |
| Y15 | `semantic.k:40-42` | `PyVal ::= intValue \| boolValue \| listValue` | Runtime values needed by this program; faithful and intentionally partial outside the subset. |
| Y16 | `semantic.k:44-45` | `Env ::= emptyEnv \| bind` | Lexically ordered environment; sufficient for `numbers` and shadowing by `number`. |
| Y17 | `semantic.k:47-48` | `Function ::= noFunction \| closure` | Single entry closure required by the harness. |
| Y18 | `semantic.k:61` | `KItem ::= execModule \| startEntry` | Module-loading control. |
| Y19 | `semantic.k:72` | `KItem ::= execFunction` | Function-body control. |
| Y20 | `semantic.k:81-82` | `KItem ::= walkComp \| emitComputed` | Explicit list-comprehension iterator and emission; exercised by the submitted body. |
| Y21 | `semantic.k:95` | `Ints ::= ifCons(Bool,Int,Ints) [function]` | Conditional stable prepend. Truthfully defined by S12-S13. |
| Y22 | `semantic.k:100` | `PyVal ::= eval(Expr,Env) [function]` | Pure evaluator. Truthfully defined on every expression form reached by the submitted program. |
| Y23 | `semantic.k:115` | `Int ::= asInt(PyVal) [function]` | Partial type projection; reached only on `intValue`. |
| Y24 | `semantic.k:116` | `Ints ::= asInts(PyVal) [function]` | Partial type projection; reached only on `listValue`. |
| Y25 | `semantic.k:117` | `Bool ::= asBool(PyVal) [function]` | Partial type projection; reached only on `boolValue`. |
| Y26 | `semantic.k:123` | `Int ::= count(Int,Ints) [function]` | Python integer-list count. Ground behavior is fixed exhaustively by S23-S25. |
| Y27 | `semantic.k:134` | `PyVal ::= collect(Ints,String,Expr,Expr,Env) [function]` | Pure one-generator comprehension evaluator; not used by the special return transition, but sound on the modeled pure subset. |
| Y28 | `semantic.k:142` | `PyVal ::= prependIf(Bool,Int,PyVal) [function]` | Conditional prepend for `collect`; truthfully defined by S28-S29. |
| Y29 | `verification.k:9-10` | `Ints ::= removeRepeated \| removeRepeatedOnto [function]` | Result-bearing mathematical specification, exhaustively defined on finite ground lists by V1-V3. |

There are ten local `[function]` symbols: `ifCons`, `eval`, `asInt`, `asInts`,
`asBool`, `count`, `collect`, `prependIf`, `removeRepeated`, and
`removeRepeatedOnto`. There are no `[total]` or `[functional]` declarations, no
priority attributes, no simplification rules, no macros or aliases, and no
proof-local ordinary operational rules. The three `count` equations alone use
`[concrete]`. No local symbol is wholly opaque. `count` is intentionally left
unreduced for nonground symbolic lists, but every finite ground `Ints` value is
covered by its disjoint recursive equations.

## Configuration

`semantic.k:50-57` declares exactly five state cells:

| Cell | Initial value / role | Decision |
|---|---|---|
| `<k>` | submitted `$PGM:Pgm` | Actual translated module is the entry computation. |
| `<input>` | supplied `$INPUT:PyVal` | Entry claim restricts it to `listValue(INPUT)`, exactly the intended list-of-integers domain. |
| `<function>` | `noFunction` | Receives the registered closure. |
| `<env>` | `emptyEnv` | Becomes the parameter binding at entry. |
| `<output>` | `listValue(.Ints)` | Accumulator/result, initially a fresh empty list. |

No heap, exception, I/O, or call-stack cell is needed for this pure, single-call
program. The absence of those cells excludes Python behaviors outside the exact
submitted body; it does not erase an observable effect of this body.

## Semantic rules

| ID | Source | Rule effect | Static decision |
|---|---|---|---|
| S1 | `semantic.k:62` | `Module(SS) => execModule(SS)` | Faithful module-entry step. |
| S2 | `semantic.k:63` | Empty module scan starts the entry. | Faithful after the exact function has been registered; malformed/empty modules can merely get stuck later. |
| S3 | `semantic.k:64` | Schedules the first statement before the remaining module scan. | Preserves source order. |
| S4 | `semantic.k:65` | Erases `ImportFrom`. | Sound for the submitted `typing.List` import because annotations are absent from the runtime AST and the import has no observable use. |
| S5 | `semantic.k:67-68` | Registers a 3-field `remove_duplicates` closure if none exists. | Unused by the trusted translator output; reasonable compatibility rule, no influence on the target proof. |
| S6 | `semantic.k:69-70` | Registers the exact 5-field translated closure if none exists. | Faithful for the sole submitted definition. Re-definition semantics is outside the target construct set. |
| S7 | `semantic.k:73-76` | Starts the closure and binds its parameter to the supplied input. | Faithful harness for the single entry invocation; preserves input and writes only environment/control. |
| S8 | `semantic.k:83-85` | Turns a leading `Return(ListComp(...))` body into `walkComp`. | Faithful for the exact body. Discarding `_REST` matches Python's abrupt return, where trailing statements are unreachable. |
| S9 | `semantic.k:87` | Empty `walkComp` consumes itself. | Correct base case; continuation is preserved by the cell frame. |
| S10 | `semantic.k:88-91` | Recurses on the tail, then emits the current item using the captured original environment. | Pure predicate/value evaluation may be scheduled after the tail without observation here; tail-first execution plus head-prefix emission preserves source order. |
| S11 | `semantic.k:92-93` | Consumes `emitComputed` and conditionally prefixes its integer to output. | Correct state footprint: only `<k>` and `<output>` change. |
| S12 | `semantic.k:96` | `ifCons(true,I,IS) => I,IS` | True Boolean equation. |
| S13 | `semantic.k:97` | `ifCons(false,_,IS) => IS` | True Boolean equation; disjoint from S12. |
| S14 | `semantic.k:101` | Evaluates integer AST to `intValue`. | Faithful. |
| S15 | `semantic.k:102` | Matching head binding lookup returns the value. | Faithful lexical lookup. |
| S16 | `semantic.k:103-104` | Unequal-name lookup continues through the environment. | Guard is disjoint from S15 and recursion descends. Missing-name behavior is intentionally unmodeled and unreachable here. |
| S17 | `semantic.k:106-107` | Evaluates `E.count(A)` as integer-list `count`. | Faithful for the exact list receiver and integer argument. Receiver/argument expressions are pure names in this body. |
| S18 | `semantic.k:109-110` | Evaluates one `==` integer comparison to a Boolean. | Faithful for the submitted equality. |
| S19 | `semantic.k:112-113` | Evaluates a one-generator comprehension with `collect`. | Sound on the modeled pure subset; S8 is the rule reached by the submitted return, so S19 is not proof-critical. |
| S20 | `semantic.k:118` | `asInt(intValue(I)) => I`. | True projection on its matched domain. |
| S21 | `semantic.k:119` | `asInts(listValue(IS)) => IS`. | True projection on its matched domain. |
| S22 | `semantic.k:120` | `asBool(boolValue(B)) => B`. | True projection on its matched domain. |
| S23 | `semantic.k:127` | `count(_,[]) => 0 [concrete]`. | Correct base equation. |
| S24 | `semantic.k:128` | Equal head contributes one, then recurses `[concrete]`. | Correct and strictly descends on the finite list. |
| S25 | `semantic.k:129-130` | Unequal head contributes zero, then recurses `[concrete]`. | Correct, guarded disjointly from S24, and strictly descends. Together S23-S25 cover all finite ground integer lists. |
| S26 | `semantic.k:135` | Empty `collect` returns an empty list. | Correct base case. |
| S27 | `semantic.k:136-140` | Evaluates the head predicate/value and recursively collects the tail. | Correct stable pure comprehension; recursion descends. |
| S28 | `semantic.k:143` | True `prependIf` prefixes the value. | True equation. |
| S29 | `semantic.k:144` | False `prependIf` leaves the list unchanged. | True equation; disjoint from S28. |

S10 reverses predicate-evaluation time relative to CPython, but all expressions
it reorders in the submitted body are total, pure reads of immutable integer
lists. Therefore the target result, control, and every modeled state cell agree.
It would not be a general semantics for side-effecting or exception-raising
comprehensions; those constructs are not present in the submitted program.

## Verification equations

| ID | Source | Rule effect | Static decision |
|---|---|---|---|
| V1 | `verification.k:11-12` | Initializes `removeRepeatedOnto(INPUT,ORIGINAL,[])`. | Truthful definitional expansion. |
| V2 | `verification.k:13` | Empty traversal returns the supplied suffix. | Correct base equation. |
| V3 | `verification.k:14-17` | For each head, prefixes it iff `count(head,ORIGINAL) == 1`, then processes the tail. | Exactly the stable unique-occurrence filter. It descends and, with S23-S25, covers every finite ground intended input. |

The guards/constructor patterns for V2 and V3 are disjoint. These equations do
not replace program execution; they define the postcondition value. Their use
of the same truthfully defined `count` symbol as the semantics is not an
unconstrained oracle: S23-S25 fix every ground occurrence count, and the
opposite ground outcomes were rejected in
`stage5_count_singleton_opposite.log` and
`stage5_count_duplicate_opposite.log`.

## Reachability claims

| ID | Source | Classification and decision |
|---|---|---|
| C1 | `spec.k:8-24`, `walk-correct` | Derived iterator lemma. For arbitrary finite `INPUT`, original list, existing output suffix, and arbitrary continuation `KREST`, it consumes exactly `walkComp`, preserves `KREST`, and prefixes the stable-filter result onto the suffix. It was independently proved before being trusted compositionally. The fixed-versus-composed observable-continuation checks both closed. |
| C2 | `spec.k:28-60`, `program-correct` | Exact entry theorem. Its AST is token-for-token the structure in regenerated `solution.mpy`; its initial state is the generated configuration restricted to an integer list. It consumes the computation and constrains the output to `removeRepeated(INPUT,INPUT)` while also constraining closure registration and parameter binding. |

## Construct-to-rule map for `solution.mpy`

| Submitted construct | Declaration(s) | Executed rules |
|---|---|---|
| `Module(ImportFrom ... FuncDef ...)` | Y1-Y7 | S1-S7 |
| `Return(ListComp(...))` | Y3, Y9, Y12-Y13 | S8-S11 |
| generator `number in numbers` | Y9, Y13, Y16 | S10, S15-S16, S20-S22 |
| `numbers.count(number)` | Y9, Y26 | S17, S23-S25 |
| `... == 1` | Y9-Y11 | S14, S18 |
| stable list construction | Y14-Y15, Y20-Y21 | S9-S13 |
| claimed result | Y29 | V1-V3 plus S12-S13 and S23-S25 |

Every source AST constructor has both a declaration and a reached semantic
path. No rule encodes a fixed answer, bypasses the submitted body, fabricates a
result for an unmodeled used construct, or permits a false result on a
satisfying intended input. Accordingly, this inventory makes no unsoundness
finding and needs no false-conclusion witness against a candidate rule.
