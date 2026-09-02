# Candidate-local rule assessment

This is the rule-by-rule assessment corresponding to the machine-generated
inventory in `stage5-rule-inventory.log`. The 24 supplied-semantics files are
the fixed, integrity-checked baseline. Their 928 inventoried declarations,
contexts, and rules are classified in that inventory; the materially exercised
path is mapped below. This document assesses every one of the candidate's nine
syntax declarations, 18 rules, and three claims.

## Material fixed-semantics path

| Program construct | Fixed declaration/rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` load/sequencing; `functions.k` closure creation |
| `Call`, `Attribute`, argument order | `syntax.k` strictness; `core.k` `#evalArgs`; `call.k` callee/bound-method/closure dispatch |
| `Assign`, `Name`, `Return` | `controls.k` assignment; `core.k` scope lookup; `functions.k` return/frame pop |
| `ListExpr`, `append` | `list.k` allocation and heap-mutating append |
| `For`, iterator protocol | `controls.k` `For/#loop/#loopStep`; `iter.k`; iterable-specific `#iterNext` rules |
| whitespace `split` | `methods.k:72-86`: split allocates a list, recursively applies `splitWS`, and updates heap/heapLoc |
| `lower`, `count` | `methods.k:19`, `methods.k:34-44`, and `methods.k:140-156` |
| `len`, integer subtraction/equality | `builtins.k` `len/seqLen`; `operators.k`; `int.k:13,26` |
| `If` | `controls.k` strict guard and `#branch` |

All other supplied modules/rules are unused by this program. They remain part
of the selected fixed semantics but do not contribute to closure of these
claims.

## Nine candidate syntax declarations

1. `WordSeq` (`.WordSeq`, `keepWord`, `skipWord`) is an initial-algebra tag
   language, not a theorem that a concrete split has those tags. The tags carry
   no guard relating `W` to `N`.
2. `inputWords` and `countedWord` extend trusted `IntSeq` with artificial
   constructors. Neither is a real translated string-code sequence, and there
   is no projection or connection theorem.
3. `wordIter` is an artificial iterable. It is acceptable only conditional on
   an absent theorem connecting it to trusted `splitWS`.
4. `consonantCount` is `[function,total,symbol,no-evaluators]`. It is
   result-bearing and program-derived, but has no defining coverage for
   `.IntSeq`, `iCons`, or `inputWords`; `[total]` is unjustified.
5. `selectedWords` is a structurally total filter over the tag algebra. It is
   internally defined, but its meaning is conditional on the unproved tags.
6. `#expectList` is an exact proof-harness observer of a list reference. It is
   result-constraining and is not itself a shortcut through program execution.
7. `selectLoopBody` is a macro. Its expansion matches the submitted loop body.
8. `selectFunctionBody` is a macro. Its expansion matches the submitted
   function body.
9. `selectWordsModule` is a macro. Fresh `kast --expand-macros` output is byte
   identical to the parsed submitted `solution.mpy` module.

## Eighteen candidate rules

1. Split bridge (`verification.k:22-26`): **illegitimate operational bridge**.
   It preempts `methods.k:72-74` but has no bridge-free connection theorem. It
   also skips the fixed rule's `#alloc`, heap write, and heapLoc increment.
   A boundary witness is
   `N=0, WS=.WordSeq, heap=.Map, heapLoc=0` with any continuation. The local
   rule yields `wordIter(0,.WordSeq)` with heap/heapLoc unchanged; the fixed
   rule yields `#alloc(list(splitWS(inputWords(...),...)))`, then a `ref(0)`,
   heap entry 0, and heapLoc 1. Result, state, and continuation input differ.
2. Empty `wordIter` rule (`:28-29`): internally faithful to the artificial
   iterator algebra, but conditional on the failed split bridge.
3. `keepWord` iterator rule (`:30-31`): **result-bearing oracle**. It rewrites
   every `W` to `countedWord(N,W)` without proving that `W` has count `N`.
   Witness: `N=0, W=codes("b")`; both Python implementations return `[]` for
   `"b",0`, while the tagged formal path selects the wrapped `"b"`.
4. `skipWord` iterator rule (`:32-33`): **result-bearing oracle**. It forces
   count `N+1` for every `W`. Witness: `N=0, W=codes("a")`; both Python
   implementations return `["a"]`, while the tagged formal path omits it.
5. Arithmetic-to-`consonantCount` simplification (`:40-47`): names the real
   arithmetic result but replaces its evaluation with an opaque symbol. There
   is no fixed-semantics connection theorem; the same symbol is then fixed by
   rule 6, making the reasoning circular.
6. `consonantCount(countedWord(C,W)) => C` (`:48`): **unconstrained value
   oracle**. The concrete false-intent witness is `C=0,W=codes("b")`, whose
   real consonant count is 1. It also supplies no equations for most of the
   declared total domain.
7. `selectedWords(.WordSeq,N)` (`:53`): true by the tag-filter definition.
8. `selectedWords(keepWord(...),N)` (`:54-55`): true by that definition but
   circular relative to the source contract. It returns
   `str(countedWord(N,W))`, not the original `str(W)`; no unwrap/equivalence
   theorem exists.
9. `selectedWords(skipWord(...),N)` (`:56-57`): true by the tag-filter
   definition but circular relative to the source contract.
10. `valSeqConcat` associativity (`:61-63`): valid by induction over the first
    trusted `ValSeq` argument.
11. `valSeqConcat(A,.ValSeq) => A` (`:64-65`): valid right identity by the
    same induction.
12. `$cells` membership peeling (`:70-73`): valid for finite K Maps under its
    `X != "$cells"` guard.
13. Update-key membership (`:74-75`): valid; a map update at `X` contains `X`.
14. Explicit-key lookup (`:76-77`): valid for well-formed K Maps, whose keys
    are unique.
15. `#expectList` observer (`:82-83`): exact, state-preserving observation of
    a heap list at the returned reference.
16. `selectLoopBody` macro equation (`:87-118`): constructor-faithful.
17. `selectFunctionBody` macro equation (`:121-127`):
    constructor-faithful.
18. `selectWordsModule` macro equation (`:130-135`):
    constructor-faithful.

The operational/value witnesses for rules 1, 3, and 4/6 are concrete or
symbolic false conclusions, not merely missing tests. No unsoundness is claimed
for rules 2, 7-18; their limitation is the missing connection from the
artificial tag algebra to real strings.

## Three claims

1. `select-loop` is satisfiable (for example `N=0, WS=.WordSeq`,
   `ACC=.ValSeq` in the displayed frame) and proves an internally consistent
   fold over `wordIter`, conditional on the oracles above.
2. `select-loop-entry` is similarly satisfiable and establishes the first
   iteration's local-variable shape before depending on `select-loop`.
3. `select-words-correct` has a syntactically exact loaded function body and a
   result-constraining `#expectList`, but its only string arguments are
   `str(inputWords(N,WS))`. No concrete source string has that `IntSeq`
   constructor, and no theorem maps arbitrary concrete strings to `WS` or
   validates the tags. Therefore it proves only the substituted oracle model,
   not the HumanEval input domain.
