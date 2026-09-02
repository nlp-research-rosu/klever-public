# Stage 5 static review notes

The exhaustive source inventory is `stage5-rule-inventory.txt`: 26 K source
files, 229 local syntax declarations, 699 local rules, five contexts, one
configuration, and two positive reachability claims. It records the exact
source block and an audit disposition for every item. There are 148
function-bearing syntax declarations, 108 `[total]` declarations, 22
`[no-evaluators]` opaque declarations, 45 priority-bearing rules, 35
`[concrete]` rules, 26 `[owise]` rules, and **zero** `[simplification]` or
`[functional]` declarations.

## Used constructor/rule map

The submitted `solution.mpy` uses:

| Program construct | Declaration/evaluation rules |
|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `syntax.k:53,56-61`; concrete module load `core.k:124-127`; concrete def binding `functions.k:14-16` |
| `Call(Name("prime_length"), ...)` | `call.k:20-21`, `core.k:131-154`, `core.k:189-191`, and closure entry `call.k:69-75` |
| parameter binding and frame lifecycle | `functions.k:63-66,78-90` |
| the ASCII docstring expression | `str.k:13-17` and `controls.k:48` |
| assignments and integer/Boolean literals | `controls.k:9-11`; `core.k:194-195` |
| `len(string)` | ordinary name/call path plus `builtins.k:17,20-26`; `core.k:227-229` |
| `BinOp("+",...)`, `BinOp("%",...)` | strict/seqstrict syntax, `operators.k:12`, `int.k:9,15,19-20` |
| integer `<`, `>=`, and `==` | `operators.k:15-17`; `int.k:22,25-26` |
| `If` | strict condition, `controls.k:51-54`; Boolean truthiness `core.k:199-205` |
| `While` and its recurring `#while` term | `controls.k:65-67,77-85` |
| `Return` | strict expression and `functions.k:78-90` |

The exact initial closure in the reachability claim bypasses only module
loading/`FuncDef` construction. `stage4_pinning.py` mechanically proves that
the pinned binding, parameter, body, and loop are the corresponding
constructor terms in the trusted regeneration.

## Used-path soundness

- Lookup selects the exact `prime_length` closure in scope 0. The callee and
  sole argument evaluate left-to-right; `len` is found only after following
  parents 1 -> 0 -> -1. No cell/ref priority rule can match because the pinned
  maps contain no `$cells` and values are not refs.
- Closure entry allocates local scope 1, pushes the exact `.K` continuation,
  binds `string`, and increments `scopeLoc`. `Return` sets `retV`, discards the
  remaining local continuation as Python return does, and `#pop` restores
  environment 0, deletes local scope 1, restores `scopeLoc=1`, empties the
  stack, and resets `ret=noRet`. Heap, `heapLoc`, exception, and exit code are
  unchanged.
- `seqLen(str(CS)) = isLen(CS)` and the two `isLen` equations count one
  semantic character per `iCons`. These equations are exhaustive and
  descending. Thus `n` is nonnegative on every formal input.
- Strictness/contexts implement the needed evaluation order. Integer
  comparison and addition are direct mathematical integer operations.
  `pyMod(N,D)=((N %Int D)+D)%Int D` equals Python modulo throughout the proof
  domain `N>=0,D>=2`; divisor zero and negative-divisor behavior are
  unreachable.
- The `If` rules branch on the exact Boolean comparison result. The `While`
  rules evaluate the guard, run the exact body when true, and return to the
  exact `#while`; `#loopLbl` re-enters it. There is no break/continue or heap
  effect.
- All priority rules in the fixed semantics were checked for overlap with
  this path. Their guards/shapes (refs, cells, math/hashlib calls, collection
  operations, or keyed sorting) are disjoint. The generic `[owise]` call and
  compare routes therefore implement the path above without preemption.

## Proof-local declarations and rules

`verification.k` has only two pure functions and four equations. It adds no
operational, priority, concrete, simplification, or opaque rule.

- `trialPrime(N,D,P)` base (`D>=N,D>=2`) returns the accumulated flag.
- Its divisor step (`D<N,D>=2,pyMod(N,D)=0`) advances to `D+1` with `false`.
- Its nondivisor step uses the disjoint condition `pyMod(N,D)=/=0`, advances
  to `D+1`, and preserves `P`.
- `primeNat(N)` starts the fold at `D=2` with `N>=2`.

On `D>=2`, `D>=N` versus `D<N` is exhaustive and disjoint; in the latter
case the modulo equality/inequality split is exhaustive and disjoint. The
divisor is nonzero, and `N-D` decreases. `trialPrime` is intentionally partial
outside `D>=2`, but every proof use establishes that guard. `primeNat` is
truthfully total for all integers because it always starts at 2. These
equations are a definitional result summary; none can rewrite a program term.

The loop claim is an exact circularity over the real recurring `#while`.
For arbitrary `N>=0,D>=2,P`, one fixed-semantics iteration performs the same
modulo split and updates represented by `trialPrime`; the circularity then
applies at `D+1`. The destination existentially leaves final `divisor`
unobserved but fixes final `prime` exactly. The entry claim executes lookup,
call, every material body operation, return, and frame pop and fixes the
returned Boolean to `primeNat(isLen(CS))`.

## Supplied-semantics rules outside the dependency slice

Every remaining fixed rule is tagged `FIXED-SUPPLIED-SEMANTICS-UNREACHED` in
the inventory. These rules define the selected supplied language but cannot
match any term/cell on this program's proof path. They are not silently treated
as a universal model of CPython. Representative explicit scope limitations
found during the full review include:

- `builtins.k:156-160` accepts every length-at-least-two code sequence as an
  integer numeral. Witness: semantic `int("a0")` computes 490, while CPython
  raises `ValueError`.
- `builtins.k:291-297` does not model `bool` as a subclass of `int`. Witness:
  semantic `isinstance(True,int)` is false; CPython's result is true.
- `list.k:27` and `tuple.k:18` use constructor equality for elements. Witness:
  semantic `[True] == [1]` is false, whereas CPython returns true.
- `methods.k:58` represents `s.encode(...)` as the same semantic string.
  Witness: CPython `"a".encode("ascii")` returns bytes `b"a"`, not `"a"`.
- `methods.k:13-16,112-138` are ASCII predicate models. Witness: semantic
  `str(iCons(201,.IntSeq)).isupper()` is false while CPython `"É".isupper()`
  is true.
- `controls.k:36` and `float.k:61` intentionally erase unsupported imports.
  Witness: `import sys; return sys.version` binds/returns a value in CPython,
  while the supplied subset does not bind `sys`.
- `functions.k:85-90` deallocates a function frame under an explicit
  no-escaping-closure subset assumption. A function returning a nested
  closure would violate that assumption, but this candidate defines no nested
  closure and returns only a Boolean.

These are concrete limitations of unused portions of the fixed supplied
semantics, not proof-local rules and not routes to the candidate result. The
22 opaque fixed symbols (float operations, sorting, and MD5) are likewise
unreachable. The theorem's only active primitive theories are K maps/lists,
mathematical integers/Booleans/strings, and the supplied operational rules
listed in the used map.
