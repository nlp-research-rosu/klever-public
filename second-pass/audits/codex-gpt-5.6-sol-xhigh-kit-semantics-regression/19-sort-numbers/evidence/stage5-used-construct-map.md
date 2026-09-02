# Submitted-program construct map

This map is independent of the candidate's prose. Locations are in the scratch
copy whose semantics tree was first established byte-identical to the trusted
mount.

| Submitted construct | Syntax declaration | Rules on the proof path | Audit result |
|---|---|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `reference-semantics/semantics/syntax.k:53-61` | `core.k:124-127`, `functions.k:14-16` | The exact translated module loads a `closureVal` at scope 0. The fresh `AUDIT-PINNING` claim proves that this is the entry claim's binding. |
| `Return` | `syntax.k:50` (`strict`) | `functions.k:78-90` | Its expression evaluates before return; `#pop` restores env, scope stack, return state, and continuation. |
| `Call` and argument lists | `syntax.k:28`, `syntax.k:37` | `call.k:20-21`; `core.k:185-191` | Callee first, then arguments left-to-right through one accumulator. No proof-local call interception exists. |
| `Name("sort_numbers")`, `Name("numbers")`, `Name("sorted")`, `Name("word")` | `syntax.k:12` | `core.k:130-154`, `core.k:157-181` | Lookup follows the pinned current scope and parent chain. The entry scope pins the submitted function; `sorted` resolves from the fixed builtins scope. |
| `Str` and `Int` literals | `syntax.k:9-13` | `str.k:13-17`, `core.k:194-196` | ASCII strings become code sequences; all numeral words and the separator are ASCII. Integers become K `Int`. |
| `Attribute(..., "split")` and `Attribute(..., "join")` | `syntax.k:29` (`strict(1)`) | `call.k:16`, `call.k:24`, `call.k:56-67` | Receiver evaluates first and becomes a bound method. Heap receivers/arguments are read without mutation. |
| no-argument `split()` | `Call`, `Attribute` above | `methods.k:72-86`, `core.k:117-121` | It executes the fixed splitter and allocates heap object 0. The candidate's sole simplification rule only summarizes `splitWS` on the guarded single-space/numeral domain. |
| `KwArg("key", Lambda(...))` | `syntax.k:25-26` | `core.k:95-102`, `functions.k:50-60` | The key remains a tagged argument. The annotated lambda has no cell/free variables and evaluates to the exact `closureValC` used in the postcondition. |
| `DictExpr(Entry(...))` | `syntax.k:18`, `syntax.k:33-34` | `dict.k:23-54` | Keys and values evaluate left-to-right. `dPutK`/`dPutV` build the ten-entry insertion-ordered dictionary; the keys are distinct. |
| dictionary `Subscript(..., Name("word"))` | `syntax.k:22`, `syntax.k:38`; contexts `subscript.k:27-28` | `dict.k:63-66`, `dict.k:101-103` | Dictionary priority 45 preempts generic positional indexing; `dGet` returns the mapped integer for each valid word. Each of the ten exact key execution claims closes separately. |
| `sorted(list, key=...)` | `Call`, `KwArg` above | `sort.k:49`, `sort.k:61-62` | Proof execution allocates heap object 1 containing opaque `sortKeyVS(VS, keyClosure)`. This faithfully follows the supplied proof semantics but assumes, rather than proves, stable keyed sorting and key-call behavior. |
| concrete keyed sort used for bridge testing | Internal syntax in `concrete.k:25-27` | `concrete.k:28-59` | LLVM execution calls the real key closure for every element and stably insertion-sorts integer keys. Fresh concrete tests terminated normally. These rules are not imported into the Haskell proof. |
| `" ".join(sorted_result)` | `Attribute`, `Call`, `Str` above | `methods.k:26-31`, `call.k:63-67` | The sorted heap object is dereferenced, `joinCodes` folds the separator between string elements, and no new heap allocation occurs. |
| allocation and final cells | Internal `#alloc` in `core.k:117-121`; call frames in `call.k:69-94` and `functions.k:78-90` | same | Exactly two lists are allocated, at 0 and 1; `heapLoc` becomes 2. The function frame is removed; stack, ret, exc, and exit code are restored as claimed. |

## Proof-local inventory conclusions

- `sortNumbersBody`, `sortNumbersFunction`, and `numberKeyFunction` are macros:
  syntactic abbreviations only. Their expansions match `solution.mpy`; they add
  no equations.
- `isNumberWord` has one string-constructor equation plus an `owise` case.
  The cases are disjoint and cover `Val`.
- `validNumberWords` has the two `ValSeq` constructors as cases and structurally
  descends on `REST`; it is total and terminating.
- The sole simplification rule is
  `splitWS(joinCodes(space, VS), empty, empty) => VS` under
  `validNumberWords(VS)`. It has no cells or continuation and therefore no
  state/control footprint. The induction is: empty is immediate; a valid head
  has a nonempty whitespace-free code sequence; `joinCodes` inserts exactly one
  ASCII space; `splitWS` accumulates the head, flushes at that space, and the
  induction hypothesis handles the tail. Baseline ground probes cover empty,
  two-token, and comma-boundary configurations.
- There are no candidate priority rules, ordinary operational K-cell rules,
  other simplifications, or proof-local opaque symbols.

## Totality and overlap notes

The fresh compilers reported the supplied semantics' existing non-exhaustive
`total` declarations for `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`. On this program path, `joinCodes` receives strings and its used
cases are covered; the other warned functions are unreachable. Their uncovered
cases remain abstract terms rather than yielding a false equality. This is a
coverage limitation of the fixed supplied model, not a witnessed unsound rule.

Proof-local guarded rules have no conflicting overlap. The split bridge can
overlap a baseline split reduction only after a concrete `joinCodes` reduces;
on its guard the baseline result is the same sequence, as the induction and
baseline probes show.
