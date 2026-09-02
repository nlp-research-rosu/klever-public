# Static rule review ledger

`05-static-inventory.log` is the source-complete lexical inventory: 1,093
top-level sentences across every trusted semantics K file, `verification.k`,
`spec.k`, and `lemma-spec.k`. It records each sentence's file, line span,
category, full text, and SHA-256. Its rule count is 700:

- 622 ordinary rules;
- 28 `[owise]` rules;
- 43 `[priority(40)]` rules;
- 4 `[priority(45)]` rules;
- 1 `[priority(39)]` rule;
- 1 combined `[priority(40), owise]` rule; and
- 1 proof-local `[simplification]` rule.

It also records 231 syntax sentences, including all 85
`[function,total]`, 25 `[function,total,symbol]`, 5 macro, 2 token-function,
and 37 other function declarations; 5 contexts; 1 configuration; and all 11
claims. No `[functional]` declaration occurs.

The following ledger assigns every source file's inventoried declarations and
rules a review disposition. “Inactive” means constructor-disjoint from the
expanded submitted program and from every claim precondition/postcondition,
not that it was omitted from the inventory.

| Source | Inventory and disposition |
|---|---|
| `semantics.k` | Two assembly modules and 23 imports; no rules. `VERIFICATION` imports `MPY`, not the concrete-only `MPY-CONCRETE`. Correct module boundary. |
| `semantics/syntax.k` | Fifteen syntax sentences and one comprehension macro production. All submitted constructors are declared with the intended strictness/sequence strictness. Unused syntax is inert. |
| `semantics/core.k` | Configuration; 37 syntax/function declarations; 46 rules (41 ordinary, 3 owise, 2 priority-40). Active rules load/sequence statements, look up the exact closure, evaluate arguments left-to-right, evaluate literals, compute truthiness, and define sequence lengths. Allocation/cell/keyword/list-update rules are constructor-disjoint. `builtinsScope` is a fixed namespace value. No active rule fabricates a result. |
| `semantics/functions.k` | Eight syntax declarations and 15 rules (14 ordinary, 1 priority-40). Active plain-closure rules bind exactly one parameter, push one frame, execute the exact body, implement abrupt `Return`, and restore all caller cells. Annotated-closure/cell rules are inactive. |
| `semantics/call.k` | Three syntax declarations and 21 rules (13 ordinary, 3 owise, 5 priority-40). Active path is `Name` lookup → ordinary closure → left-to-right argument loop. The only active bound-method route is `str.count`; builtin/type/ref/annotated-closure routes are disjoint. Generic `[owise]` call routing is preempted only by named special forms that do not match this program. |
| `semantics/controls.k` | Three syntax declarations and 34 rules (25 ordinary, 2 owise, 6 priority-40, 1 priority-40/owise). Only `If/#branch` is active; its two Boolean cases are exhaustive and disjoint. Assignment, imports, loops, break/continue, and ref dereference are inactive. |
| `semantics/operators.k` | Two contexts and 10 rules (3 ordinary, 1 owise, 6 priority-40). Active values are never refs, so priority dereference rules are disjoint. Unary/binary dispatch and left-then-right comparison evaluation preserve Python order. |
| `semantics/bool.k` | One context and 13 rules (8 ordinary, 5 priority-40). Active `not` and three-operand `or` execute left-to-right with correct short-circuit control. Ref rules are inactive. Guard pairs are Boolean complements. |
| `semantics/int.k` | One function declaration and 16 ordinary rules. Active unary minus, addition, `>`, `!=`, and integer hooks have ordinary mathematical meanings. Division/modulo rules are inactive. |
| `semantics/str.k` | Five function declarations and 28 ordinary rules. Active ASCII literals, equality, membership, prefix, and containment equations are recursive, descending, exhaustive, and non-overlapping modulo complementary guards. `strToCodes` deliberately has only the ASCII nonempty rule; every submitted literal is ASCII. Symbolic input is already an `IntSeq`, so the partial literal encoder does not narrow the claim variable. Ordering is inactive. |
| `semantics/methods.k` | Twenty-seven function declarations and 75 rules (68 ordinary, 4 owise, 1 priority-39, 2 priority-40). Active `str.count` dispatches to `cntSub`; for every nonempty singleton pattern used here, its prefix/non-prefix guards partition the input and recursion strictly consumes input. `dropIS` is total and descending. All other methods and split priority rules are constructor/name-disjoint. |
| `semantics/subscript.k` | Fifteen syntax/function declarations, two contexts, and 40 rules (38 ordinary, 1 priority-40, 1 priority-45). Active index 0 is reached only on nonempty `IntSeq`; active suffix slice uses step 1 and the exhaustive `slStart/slStop/slAdjust/clamp/buildIS` equations. The trusted `[total]` underspecification of `valSeqAt` on opaque/OOB lists is inactive. `intSeqAt` is partial but every active index is in bounds. |
| `semantics/list.k` | Five function/syntax declarations and 27 rules (23 ordinary, 1 owise, 1 priority-40, 2 priority-45). Entirely inactive: submitted execution constructs no lists and uses no list operation. |
| `semantics/tuple.k` | Four declarations and 21 rules (18 ordinary, 3 priority-40). Entirely inactive. |
| `semantics/set.k` | Six declarations and 12 ordinary rules. Entirely inactive. |
| `semantics/range.k` | Two function declarations and 6 ordinary rules. Entirely inactive. |
| `semantics/iter.k` | One protocol declaration, no rules. Inactive. |
| `semantics/comprehension.k` | Three macro declarations and 7 ordinary macro rules. Inactive; no comprehension constructor is in the regenerated program. |
| `semantics/dict.k` | Twelve declarations and 28 rules (24 ordinary, 2 owise, 1 priority-40, 1 priority-45). Entirely inactive. |
| `semantics/builtins.k` | Thirty-eight declarations and 137 rules (126 ordinary, 10 owise, 1 priority-40). No builtin is called by this program. The registry scope is present but only the explicit module binding is selected. The opaque `md5hexCodes` symbol and deliberately limited conversion/eval rules are therefore inactive. |
| `semantics/float.k` | Thirty-four declarations and 121 rules (117 ordinary, 4 priority-40), including 22 opaque `[symbol,no-evaluators]` float functions. No float, math, conversion, or mixed-arithmetic constructor occurs in the program, claims, or proof-local summaries. These symbols cannot influence a branch or result here. Duplicate mixed Int/Float rules have identical right sides. |
| `semantics/sort.k` | Six function declarations and 19 rules (17 ordinary, 1 owise, 1 priority-40). Opaque `sortVS` and `sortKeyVS` are trusted fixed primitives but no `sorted`/`sort` call or dependent term exists here. |
| `semantics/assert.k` | Three rules (2 ordinary, 1 priority-40). Used only by reviewer concrete smoke tests, not by a target proof. The success/failure guards are complementary. |
| `semantics/concrete.k` | Five declarations and 16 rules (12 ordinary, 1 owise, 3 priority-40). Present only in the LLVM definition, absent from `VERIFICATION`; none contributes to `kprove`. |
| `verification.k` | One macro, three single-equation total functions, four ordinary definitional rules, and one simplification. All are active and individually reviewed in `used_construct_map.md`. There is no priority rule, opaque symbol, operational bridge, circularity, or task-answer oracle. |
| `spec.k` | Ten entry claims, fully inventoried. Each executes the same exact closure body and pins all operational cells at the destination. The requires clauses form the empty/nonempty, dot-count, first-character, suffix, and digit-threshold partition. |
| `lemma-spec.k` | One bridge-free arithmetic claim. It imports only fixed `MPY` and establishes the sole simplification's complete guard. |

## Opaque and low-level trust boundaries

The 25 supplied-semantics opaque symbols are the 22 float symbols in
`float.k`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. Dependency tracing from
the expanded body and all ten claim constraints reaches none of them. There is
no proof-local opaque symbol.

The active low-level primitives are K's mathematical integers, Booleans,
strings used only to decode ASCII source literals, maps/lists used as
configuration stores, equality, and the Haskell backend/SMT implication
checker. The submitted input itself is an algebraic `IntSeq`; no opaque
source-string conversion supplies or constrains its value.

## Soundness conclusion

No inventoried active rule permits a false program result on the intended
string domain. Consequently there is no claimed active-rule unsoundness for
which a false-conclusion witness is required. The concrete Unicode-literal
failure is instead the documented partiality of the fixed ASCII source-literal
decoder; it does not rewrite an input to a fabricated value, and it is not
used to construct symbolic inputs in the entry claims.
