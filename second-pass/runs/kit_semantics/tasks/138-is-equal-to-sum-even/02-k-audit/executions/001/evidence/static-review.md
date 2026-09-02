# Static soundness review

This review was performed against the fresh source copy in
`/tmp/audit-work/138-audit/candidate`, not against either candidate-provided
kompiled directory. The exhaustive line-addressable inventory is
`rule-inventory.md`: 26 K files, 929 items, comprising 227 syntax declarations,
695 rules, five contexts, one configuration, and one reachability claim.

## Candidate-local extensions

`verification.k` imports `MPY` and has no syntax, function, totality or
functionality declaration, opaque symbol, priority rule, ordinary rule,
simplification rule, macro, lemma, or auxiliary claim. `spec.k` contributes
only `SPEC.is-equal-to-sum-even`, which is the target proof goal and is not
imported as an axiom. There are therefore no proof-local operational bridges,
summaries, or oracles.

## Material construct-to-rule map

| Program construct | Declaration and execution rules |
|---|---|
| `Module` / module load | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, `Params`, function body | `syntax.k:53-60`; `functions.k:14-16` |
| `Call` and `Name` lookup | `syntax.k:28`; `core.k:130-154`; `call.k:19-21,69-74` |
| argument `Int(N)` and parameter binding | `syntax.k:9`; `core.k:186-196,213-215`; `functions.k:63-75` |
| `Return` and frame restoration | `syntax.k:50`; `functions.k:78-90` |
| `BoolOp("and", ...)` | `syntax.k:16`; `bool.k:16-25`; `core.k:199-205` |
| `Compare >=` and `Compare ==` | `syntax.k:30-32`; `operators.k:15-17`; `int.k:25-26` |
| `BinOp("%", ..., Int(2))` | `syntax.k:15`; `operators.k:12`; `int.k:15,19-20` |

Execution is left-to-right. Module loading installs the exact function closure
in scope 0. Callee lookup selects that closure, `Int(N)` evaluates before frame
entry, and `#bindP` installs `n |-> N` in fresh scope 1. The first comparison
is evaluated and can short-circuit the `and`; only its true branch evaluates
`pyMod(N,2) == 0`. `Return` sets `retV`, `#pop` restores environment 0 and
scope location 1, deletes scope 1, empties the stack, and yields the Boolean.
No heap allocation, output, exception, or loop is involved.

## Target-reachable rule decisions

The inventory identifies 77 target-reachable semantic/declarative items plus
the target claim. All 77 are sound on the complete formal domain `N:Int`:

- Grammar and contexts faithfully describe the submitted constructor term and
  enforce the needed evaluation order.
- `#loadAll`, sequencing, definition, lookup, call, binding, return, and pop
  preserve the complete configuration footprint constrained by the claim.
- Applicable overlaps are either constructor-disjoint or guard-disjoint.
  Cell-aware lookup/binding priority rules cannot apply because the ordinary
  frame has no `"$cells"` entry. Plain and annotated closure-call rules are
  constructor-disjoint. Boolean `and` branches use complementary `truthy`
  guards. Integer comparison rules are operator-disjoint.
- `pyMod(N,2) = ((N %Int 2) +Int 2) %Int 2` is a defined mathematical
  function, not an opaque summary. Because the divisor is the fixed nonzero
  positive integer 2, it equals Python's modulo for every mathematical
  integer, including negative integers.
- The path is finite and has no missing used construct. No exception rule is
  needed: both comparisons are total on integers and the modulo divisor is 2.

No target-reachable rule encodes the requested answer, skips the body, or
introduces a fresh result-bearing value. The destination repeats the
fully-defined `pyMod` value produced by actual execution; it does not share an
unconstrained oracle with a bridge.

## Exhaustive dormant-rule disposition

The remaining 851 items were read and inventoried. They cannot unify with any
term reachable from this module-and-call program:

- 177 are declarative syntax/configuration/context items.
- 33 are `[concrete]` rules visible only in the independent LLVM definition,
  not the Haskell proof module.
- 619 are operational rules for unused values or constructs (collections,
  strings, floats, loops, imports, builtins, comprehensions, assertions,
  slicing, dictionaries, sorting, and hashing).
- 22 are explicitly opaque `[function,total,symbol,no-evaluators]` boundaries:
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
  `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
  `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`, `sortKeyVS`,
  and `md5hexCodes`.

No simplification rule or `[functional]` declaration exists. The inventory
records all 29 priority rules and 28 `[owise]` rules; none can introduce a
target result. Total functions used by the target (`builtinsScope`,
`appendVal`) have constructor-complete, disjoint equations. Compiler
non-exhaustiveness warnings concern dormant `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`.

The supplied semantics is deliberately partial and contains broad behavior
outside this theorem's fragment. Examples of narrower evidence gaps are:

- `valSeqAt` is total but deliberately underspecified out of bounds.
- String `encode` ignores the encoding name; for example CPython
  `"A".encode("utf-16")` is not the one-code sequence modeled by the broad
  rule.
- Multi-character `int(str)` does not guard every character as a digit; the
  semantic rules compute 539 for the code sequence for `"aa"`, whereas CPython
  raises `ValueError`.
- `isIntV(true)` is false in this model, while CPython treats `bool` as an
  `int` subclass.
- Symbolic float, sorting, and MD5 operations cross named opaque boundaries
  without universal K connection theorems in this tree.

These are not false-conclusion witnesses for the submitted theorem: the real
program accepts a K integer and constructs none of those operations or values,
so no intended input can reach the listed rules. They are retained as explicit
global trust/coverage limitations of the supplied partial language rather than
misreported as candidate-local proof rules.

STATIC_REVIEW=TARGET_FRAGMENT_SOUND
