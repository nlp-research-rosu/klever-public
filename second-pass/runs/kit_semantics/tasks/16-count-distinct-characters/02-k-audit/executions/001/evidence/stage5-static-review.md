# Stage 5 static soundness review

## Exhaustive inventory scope

`build_rule_inventory.py` reads the fresh copied `reference-semantics/semantics.k`,
all 23 files under `reference-semantics/semantics/`, `verification.k`, and
`spec.k`. It emits 1,096 source records to `rule-inventory.tsv` and
`rule-inventory.md`: modules, imports/requires, configuration, contexts, every
local `syntax` block, every local rule, and the entry claim.

The classified declaration/rule counts are:

- 589 ordinary rules, 26 `owise` rules, 45 priority rules, and 35 concrete
  rules;
- 77 plain syntax blocks, 38 function blocks, 85 function+total blocks,
  22 function+total+`no-evaluators` blocks, and five macro/strictness blocks;
- one configuration, five contexts, one claim;
- zero local `[simplification]` rules and zero `[functional]` declarations.

Each inventory row has a source location, normalized full source text,
relationship to the submitted execution path, and review disposition. Entries
marked `NO_TASK_FALSE_WITNESS` are not being declared universally Python-faithful:
they are outside this program's reachable terms, contribute no equation or
rewrite to the target closure, and no false conclusion witness for this task was
identified. The narrower evidence limitation is retained rather than calling
such a rule unsound without a witness.

## Candidate-local extension audit

`verification.k` has only a `requires`, module declaration, and `imports MPY`.
It defines no syntax, function, total/functional symbol, opaque symbol,
priority rule, semantic rule, simplification, or claim. `spec.k` adds only the
single reachability claim. Thus the candidate introduces no operational bridge,
result-bearing abstraction, theorem-specific equation, or oracle.

## Used-rule review

`used-construct-map.md` maps every submitted constructor to its declaration and
runtime rules. The target follows ordinary fixed execution:

1. exact-name lookup selects the exact closure in scope 0;
2. the generic call route evaluates the callee and argument left-to-right;
3. closure dispatch allocates a temporary frame and binds `string`;
4. strict `Return` evaluates `string.lower()`, `set(...)`, then `len(...)`;
5. the return/pop rules restore the environment, scope location, scopes, stack,
   and return cell.

No heap object is allocated by this expression: strings and `setV` are
unboxed values in the selected rules. `heap`, `heapLoc`, `exc`, and
`exit-code` remain unchanged.

Within the fixed model:

- `mapLower` and `isLen` recurse on a strict `IntSeq` tail;
- `codeIn`, `dedupFrom`, and `snocCode` recurse on strict sequence tails;
- the two `dedupFrom` guards are complementary and their result is exactly the
  first-seen set of codes;
- `lowerC`'s ASCII-uppercase guard and `owise` case do not overlap;
- the builtin dispatch names are fixed by `builtinsScope`, so user-function,
  bound-method, `set`, and `len` routes cannot be confused;
- priority rules for heap references and closure cells do not match this
  unboxed input and plain (non-cell) frame.

The 22 `no-evaluators` opaque symbols concern float operations, sorting, and
MD5. None occurs in the program, entry claim, result expression, cells, guards,
or any selected rule. They therefore cannot influence this proof's control or
result. Fresh LLVM warnings identify non-exhaustive `mapStrVS`, float helpers,
`joinCodes`, and `valSeqAt`; none is reachable from the submitted term.

## Material false-conclusion witness

The used fixed rule at `semantics/methods.k:143`,

```k
rule lowerC(C:Int) => C [owise]
```

is false as a model of CPython `str.lower` on valid source-domain Unicode code
points. It directly affects the theorem's result.

- For source input `"éÉ"` (`CS = iCons(233, iCons(201, .IntSeq))`), the fixed
  model preserves both codes, so `isLen(dedupCodes(mapLower(CS))) = 2`.
  CPython lowers both characters to code 233, and both the trusted canonical
  and submitted Python functions return 1.
- For source input `"İ"` (`CS = iCons(304, .IntSeq)`), the fixed model preserves
  one code and returns 1. CPython lower expands it to code points 105 and 775,
  and both Python functions return 2.

The freshly built LLVM semantics produced the model results 2 and 1, and the
independent Python witness produced 1 and 2 respectively. These are satisfying
inputs to the unrestricted entry precondition, not unreachable or ill-typed
states. The ASCII-only literal conversion rules at `semantics/str.k:13-17` are
an additional language-model coverage boundary, though the entry claim itself
injects `str(CS)` directly.

Accordingly, the K claim is structurally sound under the supplied model but can
establish the wrong return value for valid inputs to the real generated Python
program.
