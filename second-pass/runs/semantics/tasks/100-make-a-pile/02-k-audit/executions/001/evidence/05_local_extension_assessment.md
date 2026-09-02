# Candidate-local proof-extension assessment

The complete directive inventory is `05_rule_inventory.tsv`. This focused
table accounts for all 15 directives in `verification.k`; there are no other
candidate-local semantics or proof-helper modules.

| Location | Extension | Class | Complete domain/context | State/value influence | Decision and justification |
|---|---|---|---|---|---|
| `verification.k:6-7` | `pileCondition` | macro abbreviation | Every occurrence expands before execution to `Compare(Name("i"), CmpOp("<", Name("n")))`. | Controls the real while guard; no cells are read or written by the macro itself. | Sound exact abbreviation of the submitted AST. |
| `verification.k:10-17` | `pileLoopBody` | macro abbreviation | Every occurrence expands to the submitted append expression followed by `i += 1`. | Its expansion reaches the fixed call/list/assignment rules and writes heap list 0 and local `i`. | Sound exact abbreviation. The expanded KORE equals the submitted program, and changing `2*i` to `3*i` makes the proof fail. |
| `verification.k:18-24` | `pileBody` | macro abbreviation | Exact full function body: empty-list allocation, `i=0`, while, return. | Determines all program control and state. | Sound exact abbreviation of `solution.mpy`; it does not skip execution. |
| `verification.k:25-26` | `pileClosure` | macro abbreviation | Exact fixed-semantics closure value for parameters `("n", .ParamNames)`, `pileBody`, defining env 0. | Names the value installed by the fixed `FuncDef` rule. | Sound exact abbreviation; no operational rewrite is added. |
| `verification.k:28-31` | `pileModule` | macro abbreviation | Exact one-function module. | Entry program term. | Sound exact abbreviation. `kast --expand-macros` produced byte-identical KORE for this term and `solution.mpy`. |
| `verification.k:34` | `pile(Int,Int)` declaration | definitional summary | All mathematical integers. `[total]` asserts definedness. | Appears only in the postcondition/heap summary; it never rewrites a program construct. | Acceptable result summary. The two equations below are disjoint, exhaustive by integer order, and terminating. |
| `verification.k:35-36` | `pile(N,I) => .ValSeq` if `I >= N` | definitional equation | All integers satisfying `I >= N`. | Fixes the empty suffix. | True by the stated suffix definition. |
| `verification.k:37-40` | `pile(N,I) => vCons(N+2*I,pile(N,I+1))` if `I < N` | definitional equation | All integers satisfying `I < N`. | Fixes each remaining level value. | True by the stated suffix definition; recursion strictly reduces `N-I`. |
| `verification.k:43` | `valSeqConcat(VS,.ValSeq) => VS` | derived mathematical lemma | Every finite algebraic `ValSeq`; no cells/control. | Normalizes the loop heap summary. | Right identity of the fixed recursive concatenation; true by induction on `VS`. |
| `verification.k:44-46` | concatenation associativity | derived mathematical lemma | Every finite algebraic `ValSeq`; no cells/control. | Reassociates the loop heap summary. | Associativity of fixed recursive concatenation; true by induction on `A`. |

There are no candidate-local priority rules, operational bridges, opaque
symbols, `functional` declarations, ordinary semantic rules, or helper claims.
The `pile` summary encodes the desired mathematical sequence, but it is not an
oracle: the actual submitted loop executes under fixed semantics before the
postcondition can be discharged.

The 928 supplied-semantics directives are byte-identical with the trusted
reference tree. The full inventory marks all of them as fixed baseline. The
eight baseline modules whose terms can occur in this program
(`syntax`, `core`, `operators`, `int`, `list`, `controls`, `functions`, and
`call`) were reviewed for evaluation order, allocation, mutation, frames,
return, and overlaps. Directives in the other supplied modules are term- and
sort-disjoint from this AST. All 22 `no-evaluators` opaque declarations and all
35 `[concrete]` equations are in those unused feature paths (float, sorting,
MD5, and related helpers); none occurs in either positive claim or its residual
terms.
