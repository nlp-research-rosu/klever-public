# Exhaustive local declaration and rule inventory

Scope: the frozen `semantic.k`, `verification.k`, and `spec.k` copied to
`/tmp/audit-work/29-filter-by-prefix/candidate-src`. Imported K built-ins are
listed separately as trust boundaries; they are not candidate-authored rules.

## Local syntax and configuration

- `semantic.k:8-9`: `StrList` constructors `nil` and `cons(String, StrList)`.
- `semantic.k:11-14`: `Module`, separator-free `Stmts`, comma-separated
  `Strings`, and `Params`.
- `semantic.k:16-22`: statement constructors `ImportFrom`, `FuncDef`,
  `Assign`, `For`, `If`, expression-statement `Expr`, and `Return`.
- `semantic.k:24-28`: `Val` is an `Expr`; expression constructors `Name`,
  `ListExpr`, `Attribute`, and one-argument `Call`.
- `semantic.k:30-38`: values `strVal`, `listVal`, `boolVal`, `noneVal`,
  `boundString`, and `boundRef`; `function`; and `Output` (`noOutput` or a
  `Val`).
- `semantic.k:48-56`: one top cell with `k`, `env`, `functions`, immutable
  external `input`, immutable external `prefix`, and `output`.
- `semantic.k:58-68`: administrative `KItem`s `launch`, `assignTo`,
  `startFor`, `loop`, `choose`, `discard`, `bindStartsWith`, `callArg`,
  `apply`, `doReturn`, and `functionEnd`.
- `semantic.k:70`: function `appendOne`.
- `semantic.k:74`: total function `startsWith`.
- `verification.k:6-7`: postcondition functions `filterAcc` and
  `filterByPrefix`.
- `verification.k:21-22`: nullary definitional functions `loopBody` and
  `solutionProgram`.

There are no local aliases, contexts, priorities, `owise` rules, opaque
declarations, or `[functional]` declarations. `startsWith` is the sole
`[total]` declaration. The two guarded `filterAcc` recursive rules are the
sole `[simplification]` rules.

## `semantic.k` rules (33)

1. `71`: `appendOne(nil,S) = cons(S,nil)`. True list append base case.
2. `72`: append to `cons(H,T)` preserves `H` and recurses on `T`. True and
   structurally descending.
3. `75-76`: `startsWith(S,P) = false` when `|P|>|S|`. True.
4. `77-78`: otherwise compare the leading substring of length `|P|` with
   `P`. True for K strings, with valid substring bounds. Rules 3-4 have
   disjoint, exhaustive integer guards.
5. `81`: unpack a module into its statement list followed by `launch`.
6. `82`: left-to-right statement-list sequencing.
7. `83`: empty statement list is empty computation.
8. `84`: erase an import. Target-sound only because the submitted import is
   `from typing import List`, whose runtime effects do not influence this
   translated body. The match is intentionally broader than that fact.
9. `85-86`: register each translated function body under its name.
10. `89-93`: select the registered two-argument `filter_by_prefix`, bind the
    externally supplied list and prefix to its two formal parameter names,
    and execute the body followed by `functionEnd`.
11. `96-97`: read a name from the environment map.
12. `98`: an empty list expression allocates the abstract value
    `listVal(nil)`.
13. `99-100`: evaluate the receiver of `Name(X).startswith` before binding
    the method.
14. `101`: bind `startswith` to the evaluated string value.
15. `102`: bind `Name(X).append` to the environment reference `X`. This is
    adequate for the target's unaliased `result`; it is not a general Python
    heap/descriptor semantics.
16. `103`: evaluate a call's callee first.
17. `104`: evaluate its sole argument after the callee.
18. `105-106`: apply bound `startswith` using the defined `startsWith`
    function.
19. `107-108`: append a string by replacing the referenced environment list
    with `appendOne` and return `noneVal`. Adequate for the target's
    unaliased local accumulator.
20. `111`: evaluate the RHS of assignment before storing.
21. `112-113`: update the named environment binding with the evaluated value.
22. `115`: evaluate the `for` iterable once.
23. `116`: turn the evaluated list into the internal loop.
24. `117`: an empty loop terminates.
25. `118-119`: bind the head to the loop variable, execute the body, then
    recurse on the tail. This preserves order and leaves the last loop
    binding, as the target Python loop does.
26. `121`: evaluate an `if` guard before branch selection.
27. `122-123`: choose the then branch for `true`.
28. `124-125`: choose the else branch for `false`. Rules 27-28 are disjoint
    and exhaustive for `Bool`.
29. `127`: evaluate an expression statement before discarding.
30. `128`: discard an evaluated value.
31. `130`: evaluate a return expression before return control.
32. `131-132`: put the return value in `output` and discard the remaining
    continuation. On the submitted body the only remainder is exactly
    `functionEnd ~> .K`; the wildcard is broader than the context validated
    here.
33. `133-134`: a function reaching its end without output returns `noneVal`.
    It does not overlap rule 32 on the submitted explicit-return execution.

Each construct in `solution.mpy` is covered: `Module` (5), `ImportFrom` (8),
`FuncDef` (9-10), `Assign`/`ListExpr` (12,20-21), `For` (22-25), `Name`
(11), `If` (26-28), `Call`/`Attribute` (13-19), expression statement (29-30),
and `Return` (31-32). The configuration accounts for the only material state:
bindings, registered function body, fixed inputs, and returned output.

## `verification.k` rules (6)

1. `9`: define `filterByPrefix(INPUT,PREFIX)` as
   `filterAcc(INPUT,PREFIX,nil)`.
2. `10`: filtering no remaining items returns the accumulator.
3. `11-13`: for a matching head, append it to the accumulator and recurse.
4. `14-16`: for a nonmatching head, preserve the accumulator and recurse.
   Rules 3-4 are disjoint and exhaustive because `startsWith` is total
   Boolean; both structurally descend on `REST`.
5. `24-27`: `loopBody()` expands to the exact translated conditional append
   body.
6. `29-35`: `solutionProgram()` expands to the exact translated module,
   formal names, body, loop helper, and return.

Rules 1-4 are mathematical postcondition definitions and do not rewrite the
program in `<k>`. Rules 5-6 are syntax-naming definitions; they expand to
program constructors and skip no operation.

## `spec.k` claims (2)

1. `5-16`, `loop-correct`: from the exact loop head, accumulator and prefix
   bindings, `noOutput`, and the exact trailing return/function-end context,
   execution reaches `.K` with output
   `listVal(filterAcc(INPUT,PREFIX,ACC))`. Other final environment content is
   deliberately existential.
2. `19-26`, `program-correct`: from the exact named program, empty initial
   maps, arbitrary `INPUT:StrList` and `PREFIX:String`, and `noOutput`,
   execution reaches `.K` with
   `listVal(filterByPrefix(INPUT,PREFIX))`. Environment and registered
   functions are not asserted after execution; input and prefix cells are
   preserved.

Neither claim is trusted in the combined proof. The loop claim is a progressing
circularity: a nonempty case executes one concrete loop iteration before
reaching the smaller tail instance.

## Imported trust boundary

`BOOL`, `INT`, `STRING`, and `MAP-SYMBOLIC` supply Boolean equality, integer
comparison, `lengthString`, `substrString`, string equality, and finite map
lookup/update. These are K distribution primitives, not candidate-authored
lemmas. `startsWith` reduces them with exhaustive guards; it is not opaque.

No target-domain false conclusion witness was found for a local rule. Rules 8,
15, 19, and 32 have match domains broader than the exact submitted execution;
they therefore limit reuse as a general Python semantics. Their problematic
contexts (side-effecting imports, descriptors/aliases, or caller/cleanup
continuations) are absent from the mechanically pinned target. They are
classified as target-sound overbreadth, not as globally justified Python rules.
