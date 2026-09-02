# Submitted-program construct map

All `reference-semantics` locations below refer to the fresh scratch copy that
was byte-identical to the trusted supplied tree. The complete 945-row
declaration/rule inventory is `k-inventory.tsv`.

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, statement sequencing | `semantics/syntax.k:61`; `semantics/core.k:124-127` (`#loadAll`, head/tail sequencing, empty statements) |
| `FuncDef`, parameters, call, return | `semantics/syntax.k:28,50,53,57,60`; `semantics/functions.k:14-16,63-66,78-90`; `semantics/call.k:19-24,69-75` |
| `Name` lookup and local assignment | `semantics/syntax.k:12,41`; `semantics/core.k:130-154`; `semantics/controls.k:9-18` |
| Integer and string literals | `semantics/syntax.k:9,13`; `semantics/core.k:194`; `semantics/str.k:13-17` |
| Empty and populated dictionaries | `semantics/syntax.k:18,33-34`; `semantics/dict.k:20,23-54` |
| Dictionary key read | `semantics/dict.k:62-66,101-103` (`applyIndexD`, `dGet`) |
| Dictionary subscript assignment | `semantics/dict.k:68-92` (`dictSet`, `#dsetK`, `dPutK`, `dPutV`) |
| `dict.keys()` | `semantics/call.k:16,19-24`; `semantics/dict.k:56-60` (fresh list allocation) |
| `str.split()` | `semantics/call.k:16,19-24`; `semantics/methods.k:70-86` (`splitWS`, `flushTok`, whitespace predicate) |
| `for` loops | `semantics/syntax.k:45`; `semantics/controls.k:62-74,104-108`; `semantics/list.k:8-10`; `semantics/tuple.k:30-41` (`#bindTgt`) |
| `if` | `semantics/syntax.k:49`; `semantics/controls.k:50-54`; `semantics/core.k:198-205` (`truthy`) |
| Membership `in` on `counts.keys()` | `semantics/operators.k:14-17`; `semantics/list.k:57-67` |
| Integer `+`, `>`, `==` | `semantics/syntax.k:15,30,32`; `semantics/operators.k:10-17`; `semantics/int.k:9,22-27` |
| Assertion and dictionary equality | `semantics/assert.k:6-15`; `semantics/dict.k:94-103` |
| Allocation and cells changed by the path | `semantics/core.k:44-60,117-121`; list objects from `split()` and `keys()` are allocated in `<heap>/<heapLoc>`; function call/return changes `<env>`, `<scopes>`, `<scopeLoc>`, `<stack>`, and `<ret>` through `call.k:69-75` and `functions.k:78-90` |
| Candidate `histogramCheck` | `verification.k:14-47`; macro-expands to the submitted `FuncDef` plus `Assert(histogram(INPUT) == EXPECTED)` |
| Candidate symbolic split | `verification.k:9-10`; adds `tokenText(ValSeq)` to `IntSeq` and defines `splitWS(tokenText(TS), .IntSeq, .ValSeq) = TS` |

Evaluation order is supplied by the syntax attributes and explicit contexts:
assignment evaluates its RHS first, binary operands use `seqstrict(2,3)`,
attributes evaluate their receiver, calls evaluate the callee and arguments
left-to-right, `For` evaluates its iterable once, and `If` evaluates its guard
before selecting exactly one branch.

No submitted claim uses a loop invariant, auxiliary loop claim, simplification
lemma, or opaque numeric/sorting primitive. The loops are executed by the fixed
iterator/control rules for lists of concrete or synthetically supplied bounded
length.
