# Exhaustive local syntax and rule inventory

Source hashes:

- `semantic.k`: `ba5b90011ca2cd389b5c6527d98e58d599580c775dde389828a6ab36552c9c0c`
- `verification.k`: `c7d813e2121ef99ac42df3f6c9829eb3058d76313b5b3b731296097f75371a2c`
- `spec.k`: `0fbfb675c47fe10dda5362e3b3e669b393fb2d18eb06ee9a5a342f2db96be4cf`

There are no generated helper K files besides these sources. There are no
local priority rules, `[simplification]` rules, opaque declarations, or
auxiliary reachability claims. The only `[total]` declarations are
`isUpperChar` and `isLowerChar`. All five `ref*` symbols are K functions but
are not declared total. `StrongestProgram` is a macro.

## 1. `MPY-SYNTAX` declarations (`semantic.k` lines 7–38)

| Lines | Production / attribute | Used by `solution.mpy` | Review |
|---|---|---:|---|
| 12 | `Program ::= Module(Stmts)` | yes | Exact translated module wrapper. |
| 14 | `Stmts ::= List{Stmt,""}` | yes | Models concatenated statement sequencing, including `.Stmts`. |
| 15 | `Params ::= Params(String,String)` | yes | Exact two-parameter entry point only. |
| 16 | `Exprs ::= List{Expr,","}` | yes | Only `.Exprs` is used for zero-argument method calls. |
| 17 | `CmpOps ::= List{CmpOp,","}` | yes | Only one `>` comparator is used. |
| 19 | `FuncDef(String,Params,Stmts)` | yes | Exact function binding syntax. |
| 20 | `Assign(Expr,Expr) [strict(2)]` | yes | RHS evaluated; program targets are simple names. |
| 21 | `AugAssign(Expr,String,Expr) [strict(3)]` | yes | RHS evaluated; program targets are simple integer variables. |
| 22 | `If(Expr,Stmts,Stmts) [strict(1)]` | yes | Guard evaluated before branch selection. |
| 23 | `For(Expr,Expr,Stmts) [strict(2)]` | yes | Iterable evaluated before iteration; targets are names. |
| 24 | `Return(Expr) [strict]` | yes | Return expression evaluated. |
| 26 | `Int(Int)` | yes | Integer literals 0 and 1. |
| 27 | `Str(String)` | yes | Delimiter `"."`. |
| 28 | `Name(String)` | yes | All source variable accesses. |
| 29 | `BinOp(String,Expr,Expr) [strict(2,3)]` | yes | String concatenation only in the submitted body. Because operands are pure lookups/literals here, the non-`seqstrict` order has no observable effect. |
| 30 | `Compare(Expr,CmpOps) [strict(1)]` | yes | Left score is evaluated; the only right operand is handled by the specialized rule below. |
| 31 | `Subscript(Expr,Expr) [strict(1)]` | yes | Container evaluated; only literal `[0]` and literal `[1:]` indices occur. |
| 32 | `Slice(Bound,Bound,Bound)` | yes | Exact `Slice(Int(1),NoBound,NoBound)`. |
| 33 | `Attribute(Expr,String) [strict(1)]` | yes | Receiver evaluated before binding a method. |
| 34 | `Call(Expr,Exprs) [strict(1)]` | yes | Callee evaluated; calls have no arguments. |
| 36 | `CmpOp(String,Expr)` | yes | Exact `CmpOp(">",Name(...))`. |
| 37 | `Bound ::= Expr \| NoBound` | yes | Covers `Int(1)` and omitted slice bounds. |

## 2. Runtime declarations and configuration (`semantic.k` lines 40–75)

| Lines | Declaration | Review |
|---|---|---|
| 49–54 | `Value`: integer, string, list, boolean, bound string method | Every runtime kind reached by the body is explicit. No opaque value exists. |
| 54 | `Values ::= List{Value,";"}` | Represents the input extension list. |
| 55–56 | `KResult ::= Value`; `Expr ::= Value` | Standard value/result injections. |
| 58 | `Function ::= function(Params,Stmts)` | Stores the exact translated body. |
| 59 | `Result ::= noResult \| returned(Value)` | Observable return cell. |
| 61–69 | `<py>` configuration | `<k>`, local environment, function map, two input cells, and result are all used. No heap, exceptions, I/O, or call stack are modeled because the submitted body needs none on its successful paths. |
| 71–75 | `exec`, `setVar`, `loopValues`, `loopString`, `#start` | Internal control terms, all exercised by concrete runs. |

## 3. Operational rules (`semantic.k` lines 78–152)

| # | Lines | Rule | Classification and soundness review |
|---:|---|---|---|
| 1 | 78 | `Module(S) => exec(S)` | Operational semantics; faithful module entry for the submitted one-function module. |
| 2 | 79 | `exec(.Stmts) => .K` | Sequencing base case; sound. |
| 3 | 80 | `exec(S SS) => S ~> exec(SS)` | Left-to-right statement sequencing; sound. |
| 4 | 82–83 | `FuncDef` installs `function(P,BODY)` | Faithfully installs the exact program body under its name for this subset. |
| 5 | 87–92 | `#start` looks up `Strongest_Extension`, binds both parameters, replaces `<env>` | Task-specific call entry. The exact binding and body are selected from `<functions>`. It is broader than a reusable Python call semantics, but every claim starts with empty maps and the exact module, so no false conclusion was found on a submitted-program state. |
| 6 | 95 | `Int(I) => intVal(I)` | Literal conversion; sound. |
| 7 | 96 | `Str(S) => strVal(S)` | Literal conversion; sound. |
| 8 | 97–98 | `Name(X)` environment lookup | Reads the selected binding; sound for present variables. |
| 9 | 100–101 | assignment to a name | Map update; sound for simple local assignment. |
| 10 | 102–103 | `setVar` map update | Internal loop-target assignment; sound. |
| 11 | 105–106 | integer `+=` | Correct integer update for the program's simple name target. |
| 12 | 107–108 | integer `-=` | Correct integer update for the program's simple name target. |
| 13 | 111 | nonempty-list index zero | Returns the first item; sound on its complete match domain. No rule models the empty-list exception. |
| 14 | 112–113 | nonempty-list slice `[1:]` | Returns the tail; sound on its complete match domain. |
| 15 | 117 | lower list `for` to `loopValues` | Faithful lowering. |
| 16 | 118 | empty list-loop terminates | Sound. |
| 17 | 119–120 | nonempty list-loop executes body then recurs | Preserves sequential control and updates the loop target; sound. |
| 18 | 122 | lower string `for` to `loopString` at index zero | Faithful shape, conditional on K string indexing matching Python iteration. |
| 19 | 123–124 | string-loop termination at `I >= lengthString(S)` | Mathematical base case for K strings. |
| 20 | 125–128 | string-loop step uses `substrString(S,I,I+1)` | Implements K-string slicing, not an established CPython Unicode-iteration bridge. This becomes materially wrong in combination with the ASCII classifiers below; concrete witness recorded in `stage3/concrete-execution.log`. |
| 21 | 132–134 | `[function,total] isUpperChar(S)` is ASCII range 65–90 | Truthful as an ASCII predicate, but unsound as the implementation of Python `str.isupper()` on unrestricted source strings. False-conclusion witness: Python `"É".isupper()` is true, while this rule yields false because `ordChar("É") = 201`. For `("C",["A","ÉÉ"])`, both trusted and submitted Python return `C.ÉÉ`, while fresh K execution returns `C.A`. The `[total]` annotation is also broader than the demonstrated one-character call domain because `ordChar` is only meaningful for a single character; no claim reaches an empty or multi-character argument directly, so that separate totality concern is not labeled an additional unsoundness. |
| 22 | 133,135 | `[function,total] isLowerChar(S)` is ASCII range 97–122 | Same Unicode modeling defect for Python `str.islower()`. Separate false-conclusion witness: Python `"é".islower()` is true. On `("C",["a","éé"])`, both Python implementations return `C.a`, while K assigns score zero to `"éé"` and returns `C.éé` (`unicode-lower-witness.log`). The rules' uppercase/lowercase ranges are disjoint. |
| 23 | 137 | bind any string attribute to a method name | The used names are exact; unknown names merely become stuck when called, so this does not fabricate a result on a used path. |
| 24 | 138–139 | call bound `"isupper"` via `isUpperChar` | Operational bridge from source method call to the ASCII predicate. It enables the false Unicode conclusion witnessed above, and no bridge-free universal connection theorem justifies it over all Python strings. |
| 25 | 140–141 | call bound `"islower"` via `isLowerChar` | Same defect for lowercase Unicode, witnessed by `("C",["a","éé"])` above. |
| 26 | 143 | true `If` executes then-branch | Sound. |
| 27 | 144 | false `If` executes else-branch | Sound; mutually exclusive with rule 26. |
| 28 | 146 | integer `BinOp("+",...)` | Sound K-integer addition (not materially used by this body). |
| 29 | 147 | string `BinOp("+",...)` | Sound K-string concatenation for the body's result. |
| 30 | 148–149 | specialized `>` comparison reads right name from `<env>` | Exact used shape; integer comparison is sound and binding is explicit. |
| 31 | 151–152 | `Return(V)` clears itself and sets the result | Correct on the actual body because return is the terminal top-level statement. As a reusable Python rule it would fail to discard an arbitrary trailing continuation, but no such continuation or nested return is reachable in this program; therefore this is recorded as a scope limitation, not as a witnessed false conclusion on the intended program domain. |

Rules 21–25 are the material generated-semantics failure. They implement used
operations and produce a wrong observable return for unrestricted Python
strings, so this is not merely missing coverage for an unused construct.

## 4. `verification.k` declarations and rules

| # | Lines | Declaration/rule | Classification and review |
|---:|---|---|---|
| 1 | 9–40 | `StrongestProgram [macro]` and its macro rule | Semantically inert source abbreviation. Fresh `kast --output kore` comparison with trusted regeneration is byte-identical (`stage4/pinning-and-witnesses.log`). It expands to the full submitted function binding and body and does not bypass execution. |
| 2 | 46 | `refDelta(String) : Int [function]` | Definitional contract summary. |
| 3 | 47 | `refStrength(String) : Int [function]` | Definitional contract summary. |
| 4 | 48 | `refStrengthAt(String,Int) : Int [function]` | Definitional recursive helper. |
| 5 | 49 | `refStrongest(Values) : String [function]` | Definitional nonempty-list selection. |
| 6 | 50 | `refSelect(String,Int,Values) : String [function]` | Definitional fold helper. |
| 7 | 52–53 | `refDelta(S)=>1` when uppercase | Correct relative to local ASCII `isUpperChar`; wrong as an unrestricted Python contract for the same Unicode witness above. |
| 8 | 54–55 | `refDelta(S)=>-1` when not upper and lower | Guard disjoint from rule 7. |
| 9 | 56–57 | `refDelta(S)=>0` when neither | Together, rules 7–9 cover Boolean classifier results and agree on no overlap. |
| 10 | 59 | `refStrength(S)=>refStrengthAt(S,0)` | Sound wrapper. |
| 11 | 60–61 | base `I >= lengthString(S)` gives zero | Correct for reachable nonnegative indices. |
| 12 | 62–65 | recursive `I < lengthString(S)` adds one character and increments | Guard disjoint from rule 11 and descending by remaining length from the only entry index 0. Same K-string/Unicode limitation as operational iteration. |
| 13 | 67–68 | initialize nonempty `refStrongest` from first string | Correct; no empty-list equation exists. Every submitted claim supplies a nonempty fixed list. |
| 14 | 69 | `refSelect` empty-tail base | Correct. |
| 15 | 70–72 | strictly greater candidate replaces best | Correct left-fold rule. |
| 16 | 73–75 | less-than-or-equal candidate retains best | Guard complementary to rule 15; ties retain the first item. |

The `ref*` functions are result-bearing, but they do not rewrite or summarize
program execution. Each positive claim symbolically/concretely executes the
full macro-expanded body and separately reduces the `ref*` postcondition. For
the seven fixed ASCII lists the functions terminate to ground strings and are
not opaque oracles. They nonetheless encode only an ASCII version of the
contract, and the entry claims never quantify over extension lists.

## 5. `spec.k` claims

There are exactly seven ordinary all-path reachability claims and no helper or
loop claims. None has an explicit `requires` condition.

1. Exact class `"Slices"` and exact list
   `["SErviNGSliCes","Cheese","StuFfed"]`.
2. Arbitrary `C:String` and exact list `["AA","Be","CC"]`.
3. Arbitrary `C:String` and exact list `["abc","AB","A-b"]`.
4. Arbitrary `C:String` and exact list `["a-1","--","A!"]`.
5. Arbitrary `C:String` and exact list `["","123","!"]`.
6. Arbitrary `C:String` and exact list `["abcd","a","xy"]`.
7. Arbitrary `C:String` and exact singleton list `["Zz"]`.

Every claim starts with the macro-expanded submitted module followed by
`#start`, exact empty environment/function maps, `noResult`, and the fixed input
cells. Existential final maps frame irrelevant local state. Every postcondition
constrains `<k>` to `.K` and `<result>` to one exact returned string after the
ground `ref*` functions reduce. Thus the claims are non-vacuous and
result-constraining, but their input domain is a finite set of seven extension
lists rather than the source contract's arbitrary nonempty `list[str]`.

## 6. Trusted imports and generated strictness

`domains.md` and imported `INT`, `STRING`, `BOOL`, and `MAP` supply K's ordinary
mathematical primitives, maps, string hooks, and the heating/cooling machinery
generated from the listed strictness attributes. These are toolchain trust
boundaries. No candidate proof-local simplifier, priority rule, or lemma alters
them. The key unproved interpretation bridge is not the K primitive itself; it
is the candidate's identification of ASCII range tests with Python's Unicode
`str.isupper()`/`str.islower()`.
