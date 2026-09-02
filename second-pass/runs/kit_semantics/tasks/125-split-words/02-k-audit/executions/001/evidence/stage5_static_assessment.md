# Stage 5 static assessment

The machine-generated companion inventory, `stage5_rule_inventory.md`, reads
all 2,664 source lines and inventories 1,022 K sentences: 246 syntax
declarations, 766 rules, five contexts, one configuration, and four positive
claims. It also records every `function`, `total`, priority, `owise`,
`concrete`, macro, and `no-evaluators` attribute. There are no explicit
`functional` or `simplification` declarations. The candidate adds exactly two
syntax declarations and two equations, and no operational, priority,
simplification, concrete, opaque, or auxiliary-claim rule.

## Executed source-constructor map

| Program construct | Fixed declaration and execution rules |
|---|---|
| `Call(Name("split_words"), ...)` | `syntax.k:28`; `core.k:130-154`; `call.k:19-24,69-74`; `functions.k:63-90` |
| parameter `txt` | `functions.k:63-66`; `core.k:130-154` |
| statement sequence | `syntax.k:56`; `core.k:124-127` |
| `Assign(Name("parts"), ...)` | `syntax.k:41`; `controls.k:9-18` |
| `Attribute(txt, "split"/"count")` | `syntax.k:29`; `call.k:15-24` |
| call arguments | `core.k:183-191`; `call.k:19-24` |
| no-argument `str.split()` | `methods.k:72-86`; `core.k:117-121`; `list.k:18-20` |
| `txt and ...` | `syntax.k:16`; `bool.k:27-36`; `core.k:199-205` |
| `[txt]` | `syntax.k:17`; `list.k:13-20`; `core.k:117-121,183-191` |
| list `!=` and reference dereference | `operators.k:14-17,33-42`; `list.k:27-28` |
| `If` | `syntax.k:49`; `controls.k:51-54` |
| string literal and comma membership | `syntax.k:13,30,32`; `str.k:13-17,29-41`; `operators.k:14-17` |
| `str.split(",")` | `methods.k:94-102`; `core.k:117-121` |
| thirteen `str.count(singleton)` calls | `methods.k:34-44`; `str.k:32-35`; `core.k:252-254` |
| integer addition | `syntax.k:15`; `operators.k:12`; `int.k:9` |
| `Return` and frame restoration | `syntax.k:50`; `functions.k:77-90` |

## Rule review

- Evaluation order is fixed left-to-right: `Call` evaluates the callee before
  `#evalArgs`; `#evalArgs` walks arguments left-to-right; `BinOp` is
  `seqstrict(2,3)`; comparison uses left-then-right contexts; `Assign`, `If`,
  and `Return` evaluate their value expressions before their semantic rules.
  `BoolOp("and", ...)` evaluates only its head and correctly skips allocation
  of `[txt]` for the empty string.
- The module-load normalization is exact. `FuncDef` at
  `functions.k:14-16`, when executed at module environment 0, installs
  `closureVal(("txt", .ParamNames), BODY, 0)` under `"split_words"`. That is
  exactly the binding in every entry claim. Fresh concrete execution of the
  actual regenerated module produced that same binding.
- Calls allocate one fresh frame, bind the one parameter, execute the expanded
  body, record `retV`, pop only the callee frame, restore environment 0, and
  resume the saved continuation. Constructed lists allocate monotonically in
  the heap. The claims' exact heaps and heap counters match the short-circuit,
  whitespace, comma, and count paths respectively.
- The higher-priority rules used here are containment rules, not proof-local
  shortcuts: reference dereference exposes the heap value before structural
  list comparison, and the two `split` rules allocate the fixed recursive
  `splitWS`/`splitSep` result before the generic bound-method fallback.
  Their receiver, arity, method-name, heap, and continuation effects match the
  modeled operations.
- `splitWS`, `flushTok`, `strPrefix`, `strContains`, `splitSep`, `cntSub`,
  `dropIS`, `seqConcat`, `valSeqConcat`, `appendVal`, and `vals2valSeq` are
  structurally recursive. Constructor cases are exhaustive on the reachable
  algebraic sequences. Paired guards (`isWSC`/`notBool isWSC`,
  equality/inequality, prefix/not-prefix) are disjoint. Recursive arguments
  decrease. The thirteen count patterns are nonempty singletons, so the
  `cntSub` recursion both descends and has Python's non-overlapping-count
  meaning.
- `splitWordsBody` is a transparent nullary AST abbreviation. Fresh KAST
  comparison establishes constructor identity with the regenerated body; it
  does not replace any operation.
- `oddAlphabetCount` is a transparent mathematical expression in the
  postcondition only. Its thirteen singleton codes are exactly ASCII
  `b,d,f,h,j,l,n,p,r,t,v,x,z`. Execution independently reaches the same
  fixed-semantics `cntSub` sum, so this is not an oracle or circular
  operational bridge.
- All 24 supplied `no-evaluators` symbols and every float, sort, digest,
  builtin, collection, subscript, comprehension, loop, and concrete-only rule
  marked inactive in the inventory have heads disjoint from every reachable
  term in this program. None occurs in the claims, proof-local equations, or
  postconditions and none can contribute to claim closure.
- No active rule was found with overlapping disagreeing right-hand sides,
  fabricated state, unconstrained result, abrupt-control mismatch, or an
  answer-bearing shortcut. Consequently there is no false-conclusion witness
  to report for an unsound rule.

## Supplied-model divergence

`methods.k:85-86` defines modeled whitespace as codes 9, 10, 13, and 32.
CPython `str.split()` recognizes additional Unicode whitespace. For concrete
input vertical tab (`U+000B`), fixed-model execution follows the count branch
and returns `0`, while the submitted Python program follows the whitespace
branch and returns `[]`. This is a supplied-model behavior gap, not a false
proof-local rule or a candidate-created restriction. The theorem quantifies
over every `IntSeq`, and the candidate explicitly documents this witness.
