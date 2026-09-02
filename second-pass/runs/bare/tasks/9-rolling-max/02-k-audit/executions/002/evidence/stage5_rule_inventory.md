# Stage 5 exhaustive local declaration and rule inventory

This inventory covers every local declaration and rule in `semantic.k`,
`solution-ast.k`, and `verification.k`. Built-in declarations imported from
`domains.md` are recorded separately as trust boundaries, not relisted.

## Local syntax declarations

| File:line | Declared sort/production | Role and audit result |
|---|---|---|
| `semantic.k:10-11` | `Program ::= Module \| Run(Module,[Ints])` | Module and concrete harness. `Run` covers the submitted invocation form. |
| `semantic.k:13` | `Module ::= Module(Stmts)` | Translated module constructor. |
| `semantic.k:15` | `Stmts ::= List{Stmt,""}` | Statement sequence. |
| `semantic.k:16-22` | `Stmt ::= ImportFrom \| FuncDef \| Assign \| For \| If \| Expr \| Return` | Exactly the statement constructors used by `solution.mpy`; several productions accept a broader subset than is operationally complete. |
| `semantic.k:24` | `Strings ::= List{String,","}` | Import and parameter strings. |
| `semantic.k:25` | `Params ::= Params(Strings)` | Function parameter constructor. |
| `semantic.k:26` | `Ints ::= List{Int,","}` | Concrete harness integer list. |
| `semantic.k:28-34` | `Expr ::= Name \| Int \| Bool \| ListExpr \| Compare \| Call \| Attribute` | Every submitted expression constructor is represented. |
| `semantic.k:36` | `Exprs ::= List{Expr,","}` | Argument/list-expression sequence. |
| `semantic.k:37` | `CmpOp ::= CmpOp(String,Expr)` | Comparison operator/right operand. |
| `semantic.k:38` | `CmpOps ::= List{CmpOp,","}` | Comparison chain sequence. |
| `semantic.k:41-42` | `Val ::= IntVal \| BoolVal \| ListVal \| NoneVal`; `Expr ::= Val` | Runtime values and injection into expressions. |
| `semantic.k:44` | `Function ::= Function(Params,Stmts)` | Stored user-function closure without captured environment. Sufficient for the top-level submitted function. |
| `semantic.k:45` | `Frame ::= Frame(Map)` | Caller-environment frame. |
| `semantic.k:47-59` | `KItem ::= Invoke \| CallKont \| EndCall \| Cleanup \| Store \| Discard \| Branch \| CompareRight \| GreaterThan \| AppendTo \| StartLoop \| Loop \| Bind` | Internal continuations. All are consumed by rules below. |
| `semantic.k:61` | `List ::= intsToList(Ints) [function,total]` | Concrete-input conversion; the only local `total` declaration. |
| `solution-ast.k:8` | `Program ::= OpRunList(Module,List)` | Value-level operational harness. |
| `solution-ast.k:13` | `Stmts ::= ROLLING-LOOP [macro]` | Exact submitted loop-body macro. |
| `solution-ast.k:23` | `Stmts ::= ROLLING-BODY [macro]` | Exact submitted function-body macro. |
| `solution-ast.k:31` | `Module ::= SOLUTION [macro]` | Exact submitted module macro. |
| `solution-ast.k:38-39` | `List ::= #rollingMax(List) [function] \| #scanMax(Int,List) [function]` | Mathematical prefix-max functions. Neither is declared `total`; both cover intended integer lists. |
| `verification.k:8` | `Program ::= VerifyRunList(Module,List)` | Proof harness. |

There are no local `functional` declarations, simplification rules/attributes,
or opaque/uninterpreted result symbols. The only local priority annotation is
the loop bridge at `verification.k:17-28`, `[priority(40)]`.

## `semantic.k` ordinary/function rules

| ID | File:line | Rule summary | Static result |
|---|---|---|---|
| S01 | 81 | `intsToList(.Ints) => .List` | True base equation. |
| S02 | 82 | `intsToList(I) => ListItem(I)` | True singleton equation. |
| S03 | 83 | `intsToList(I,IS) => ListItem(I) intsToList(IS)` | True descending equation for two-or-more input integers; complements S01/S02. |
| S04 | 85 | `Run(M,[IS]) => M ~> Invoke(rolling_max,...) ~> Cleanup` | Faithful submitted concrete harness. |
| S05 | 86 | `Module(SS) => SS` | Faithful module-body execution for the modeled subset. |
| S06 | 87 | `S SS => S ~> SS` | Left-to-right statement sequencing. |
| S07 | 88 | `.Stmts => .K` | Empty sequence completion. |
| S08 | 89 | `V ~> .Stmts => V` | Preserves a trailing return value. |
| S09 | 91 | `ImportFrom(_,_) => .K` | Sound for the submitted typing-only import; runtime imports are intentionally unsupported despite the broad syntax. |
| S10 | 92-93 | `FuncDef` stores `Function` in `<functions>` | Correct for submitted top-level definition and overwrite behavior. |
| S11 | 96 | single-argument `Call(Name(F),E)` evaluates `E` first | Correct evaluation order for the modeled user call. |
| S12 | 97 | value plus `CallKont(F)` becomes `Invoke(F,V)` | Correct continuation. |
| S13 | 98-101 | `Invoke` resolves one-parameter body, installs local env, saves caller | Correct for the submitted non-nested call; nested user calls are visibly unsupported because `<stack>` must be `.List`. |
| S14 | 102-104 | `EndCall` restores caller env and returns value | Correct for the modeled one-frame call. |
| S15 | 106-107 | `Cleanup` preserves result and clears functions | Correct terminal harness cleanup. |
| S16 | 110 | `Int(I) => IntVal(I)` | True literal evaluation. |
| S17 | 111 | `Bool(B) => BoolVal(B)` | True literal evaluation. |
| S18 | 112 | empty `ListExpr` becomes empty `ListVal` | Covers the only list literal in the submitted program. |
| S19 | 113 | `Name(X)` map lookup | Correct lookup. |
| S20 | 116 | assignment evaluates RHS before `Store` | Correct evaluation order. |
| S21 | 117-118 | `Store` updates env and yields `.K` | Correct local assignment. |
| S22 | 119 | `Return(E) => E` | Correct only in the submitted final-statement context. It does not implement abrupt return for broader syntax; such contexts get stuck, so this is a visible language-coverage limitation, not an execution shortcut used by the target. |
| S23 | 120 | expression statement evaluates before `Discard` | Correct. |
| S24 | 121 | `Discard` drops a value | Correct. |
| S25 | 124 | comparison begins by evaluating left operand | Correct for the submitted single `>` comparison. |
| S26 | 125 | after left integer, evaluate right operand | Correct left-to-right order. |
| S27 | 126 | `IntVal(I) > IntVal(J)` becomes `BoolVal(I >Int J)` | True integer comparison equation. |
| S28 | 129 | conditional evaluates guard before `Branch` | Correct. |
| S29 | 130 | true guard selects then block | Correct. |
| S30 | 131 | false guard selects else block | Correct. |
| S31 | 134 | named-list `.append` evaluates argument first | Correct for submitted receiver/binding form. |
| S32 | 135-136 | integer append extends bound list and returns `NoneVal` | Correct for submitted integer-list use. |
| S33 | 139 | for-loop evaluates iterable before `StartLoop` | Correct. |
| S34 | 140 | list value initializes `Loop` | Correct. |
| S35 | 141 | empty loop completes | Correct zero-iteration behavior. |
| S36 | 142 | nonempty loop binds head, runs body, recurs on tail | Correct order and descent for finite K lists of integers. |
| S37 | 143-144 | `Bind` updates loop target | Correct. |

The submitted term uses every modeled material operation as follows:
`Module`/`ImportFrom`/`FuncDef` use S05-S10; invocation and return use
S04/S13-S15/S22; initialization uses S16-S21; the loop uses S33-S37; its
branches and comparison use S19/S25-S30; result mutation uses S23-S24/S31-S32.
No used constructor is fabricated when it is unmodeled.

## `solution-ast.k` helper rules

| ID | File:line | Rule summary | Static result |
|---|---|---|---|
| H01 | 9-10 | `OpRunList(M,XS)` executes module, invocation, cleanup | Faithful value-level harness. |
| H02 | 14-21 | `ROLLING-LOOP` macro expansion | Constructor-identical to translated loop body after macro expansion. |
| H03 | 24-29 | `ROLLING-BODY` macro expansion | Constructor-identical to translated function body. |
| H04 | 32-34 | `SOLUTION` macro expansion | Constructor-identical to trusted regenerated module; mechanically checked in Stage 4. |
| H05 | 41 | `#rollingMax(.List) => .List` | True base equation. |
| H06 | 42 | nonempty `#rollingMax` emits head and calls `#scanMax` | True prefix-max decomposition. |
| H07 | 44 | `#scanMax(_, .List) => .List` | True base equation. |
| H08 | 45-47 | if `I > M`, emit/carry `I` | True; guard descends on tail. |
| H09 | 48-50 | if not `I > M`, emit/carry `M` | True; guard is disjoint from and complete with H08 on integer inputs. |

## `verification.k` rules

| ID | File:line | Class | Matched context and footprint | Static result |
|---|---|---|---|---|
| V01 | 9-10 | Harness | `VerifyRunList(M,XS)` under arbitrary continuation; rewrites only `<k>` to module/invocation/cleanup. | Faithful harness, equivalent to H01 by inspection. |
| V02 | 17-28 | Operational bridge, priority 40 | Matches the exact submitted `For` term and exact four-entry loop-entry env, but accepts any continuation and omits `<functions>`/`<stack>`. Replaces all iterations, bindings, branches, comparisons, appends, and loop exit; writes `result=#rollingMax(XS)` while deleting `first` and `maximum` and never producing final `number`. | **Gate A failure.** No bridge-free universal connection theorem exists. H05-H09 define the desired mathematical answer but do not connect it to fixed execution. The same `#rollingMax` occurs in bridge and universal postcondition. Its arbitrary continuation and state footprint are concretely false: Stage 5's `[2,1]` witness ends at `IntVal(2)` with fixed semantics but is stuck at `Name("maximum")` after the bridge deletes the binding. |

## Claims

`operational-spec.k` has three bridge-free concrete claims: empty, prompt, and
all-negative inputs. All freshly close, but they are finite execution tests, not
a universal loop theorem.

`spec.k` has four target claims under `VERIFICATION`: one universal
`XS:List` result claim and three redundant concrete claims (empty, prompt,
all-negative). All freshly close. Every one that reaches a nonempty loop can
use V02. The universal claim is not a bridge-free connection theorem because
it imports V02 itself.

`mutation-spec.k` has one candidate-authored negative body-mutation claim. It
does not test V02's result connection: the altered body no longer matches
`ROLLING-LOOP`, so V02 simply does not apply.

## Built-in trust boundary

The local definition relies on K's `INT`, `BOOL`, `STRING`, `LIST`, and `MAP`
domains, their constructors, matching, map update/lookup, list concatenation,
and `>Int`/`notBool`. These are standard low-level primitives and do not encode
rolling maximum. K's parser, kompiler, LLVM backend, Haskell backend, and
reachability prover are also trusted tooling.
