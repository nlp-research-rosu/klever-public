# Independent adversarial audit: 83-starts-one-ends

This audit used the supplied-semantics boundary required by the launcher and
reconstructed all executable evidence in
`/tmp/audit-work/83-starts-one-ends-audit`. Candidate-produced compiled
definitions, logs, and conclusions were not reused. The live K toolchain was
K 7.1.293.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the mount agrees with the
rendered semantics mode.

I read `/audit-input.json` first, used its `container_paths` rather than its
host-only provenance paths, and then read the campaign lock and every record
required for this layout:

- `/audit-campaign-lock.json`, `/run.json`, `/task.json`, and
  `/generation-result.json`;
- `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and
  `prompt.txt`;
- the one 118-record structured JSONL trace under `codex-trace/`;
- `usage.json`, which is present; and
- the additional legacy records that were present.

The campaign lock is structurally equal to the `audit_campaign` block and has
the recorded SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded regular-file hash checked against its mounted file.
The exact trace-member hash is
`ca7361569da789ebabb2624e8b0f2ae4f4edb19ed08207ed876c604e3e02f4ea`,
matching `generation-result.json`. The trace parses as 118 JSON records (81
response items, 34 event messages, and one each of session metadata, turn
context, and world state). These records were treated only as generation
history.

The candidate prompt and translator are byte-identical to the trusted mounts.
A recursive, type-aware manifest comparison of the candidate and trusted
semantics found the same 25 entries: 24 regular K files and one directory,
with identical file hashes. There are no symlinks, missing files, extra files,
or mistyped entries. The five required candidate proof artifacts are regular,
non-symlink files.

The reproducible check, all member hashes, and the exact command/status are in
[`evidence/provenance-integrity.log`](evidence/provenance-integrity.log); the
checker is
[`evidence/provenance_check.py`](evidence/provenance_check.py). It reports
`failures=[]` and exit 0. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a positive integer `n`, return the number
of positive `n`-digit integers whose first digit is 1 or whose last digit is
1. No examples are included in the prompt.

The trusted canonical implementation is:

```python
if n == 1:
    return 1
return 18 * (10 ** (n - 2))
```

The submitted implementation has the same branch and arithmetic, differing
only in redundant parentheses. It covers the intended positive-integer domain:
`n = 1` is the one-digit boundary and every other intended input satisfies
`n >= 2`.

Using the trusted translator copied into scratch, I regenerated `solution.mpy`.
The regenerated file is byte-identical to the submitted `solution.mpy`.
Commands and results:

- [`evidence/translator-regeneration.log`](evidence/translator-regeneration.log):
  translation exit 0;
- [`evidence/translator-byte-identity.log`](evidence/translator-byte-identity.log):
  `cmp -l` exit 0.

The independent differential script imports the trusted canonical and
submitted modules from distinct paths. It tests the branch boundary `1, 2`,
all sizes `1..50`, and `64, 100, 257`. It also independently enumerates all
positive `n`-digit integers for `n = 1..5` and counts the start/end property.
There are zero differential mismatches and zero enumeration mismatches. Empty
input is not a case for a positive-integer argument. The script and exact run
are:

- [`evidence/differential_test.py`](evidence/differential_test.py);
- [`evidence/differential-test.log`](evidence/differential-test.log), exit 0.

Testing is finite evidence, not the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts into a fresh scratch directory and built new
LLVM and Haskell definitions. No candidate cache or compiled definition was
copied or referenced.

Concrete definition and execution:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun reviewer_concrete.mpy --definition runtime-kompiled
```

The build exited 0. The reviewer-authored program contains the exact submitted
body and assertions at `n = 1, 2, 3, 5, 10`. `krun` exited 0 with `.K`,
`NoExc`, and exit code 0. Evidence:

- [`evidence/reviewer_concrete.py`](evidence/reviewer_concrete.py) and
  [`evidence/reviewer_concrete.mpy`](evidence/reviewer_concrete.mpy);
- [`evidence/llvm-build.log`](evidence/llvm-build.log);
- [`evidence/llvm-concrete-run.log`](evidence/llvm-concrete-run.log).

Proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

This exited 0
([`evidence/haskell-proof-build.log`](evidence/haskell-proof-build.log)).
I then ran the complete candidate spec and separately ran reviewer split specs
containing each unchanged claim:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
kprove spec-n1.k --definition verification-kompiled --spec-module SPEC-N1
kprove spec-n-ge-2.k --definition verification-kompiled \
  --spec-module SPEC-N-GE-2
```

Every command exited 0 and printed `#Top`:

- [`evidence/kprove-all-claims.log`](evidence/kprove-all-claims.log);
- [`evidence/kprove-claim-n1.log`](evidence/kprove-claim-n1.log);
- [`evidence/kprove-claim-n-ge-2.log`](evidence/kprove-claim-n-ge-2.log).

The compiler warnings concern unused variables or non-exhaustive fixed-semantics
functions on unrelated value constructors. None occurs on the executed
integer/function path.

## 4. Adequacy and real-program pinning

### Claims in plain language

Claim 1 starts in module environment 0 with an exact
`starts_one_ends(n)` closure, empty heap and call stack, no return or exception,
and invokes the function at `n = 1`. It requires the final `<k>` value to be
exactly `1`; every displayed non-`k` cell must be restored.

Claim 2 has the same concrete machine state, takes a symbolic K integer `N`
with `N >= 2`, and requires the final `<k>` value to be exactly
`18 *Int (10 ^Int (N -Int 2))`, again with the displayed state restored.

The preconditions are satisfiable. Ground instances at `N = 1, 2, 3, 5, 10`
were executed, and the symbolic claims themselves close. Concrete substitution
into the claim right-hand sides agrees with both Python implementations:

| `n` | claimed result | canonical | submitted |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 18 | 18 | 18 |
| 3 | 180 | 180 | 180 |
| 5 | 18000 | 18000 | 18000 |
| 10 | 1800000000 | 1800000000 | 1800000000 |

This table is generated in `differential-test.log`.

### Mechanical pinning

The claim does not start by loading the whole module. Instead, it pins the
module-level binding directly. That is permissible here because:

1. trusted regeneration proves the submitted `.mpy` is the translation of
   `solution.py`;
2. the bound name is exactly `starts_one_ends`;
3. the sole parameter sequence is exactly `("n", .ParamNames)`; and
4. after ignoring only layout and explicit-versus-implicit empty `.Stmts`
   identities, the `startsOneEndsBody` rule is constructor-identical to the
   translated function body, including the docstring expression, branch,
   returns, constants, and operator nesting.

The reviewer check also verifies that both claims contain that exact binding
and that `#invokeStartsOneEnds(N)` rewrites only to
`Call(Name("starts_one_ends"), Int(N))`. It reports all checks true:
[`evidence/program_pinning_check.py`](evidence/program_pinning_check.py) and
[`evidence/program-pinning.log`](evidence/program-pinning.log).

The concrete LLVM run independently executes module loading and obtains the
same closure body in scope 0.

### Body sensitivity

I changed the material multiplication constant in the body term actually bound
and executed by the claim from `Int(18)` to `Int(19)`, while retaining the
original expected result. The mutant definition builds, and its spec dry-run
parses successfully. Actual proving exits 1; the residual explicitly contains
`19 *Int 10 ^Int (N +Int -2)` and cannot establish the `18 *Int ...`
destination. This is a sensitivity test of the executed proof term, not merely
an edit to an external Python file:

- [`evidence/verification-body-mutant.k`](evidence/verification-body-mutant.k);
- [`evidence/spec-body-mutant.k`](evidence/spec-body-mutant.k);
- [`evidence/body-mutant-build.log`](evidence/body-mutant-build.log), exit 0;
- [`evidence/body-mutant-dry-run.log`](evidence/body-mutant-dry-run.log), exit 0;
- [`evidence/body-mutant-kprove.log`](evidence/body-mutant-kprove.log), exit 1.

The theorem is therefore body-sensitive and result-constraining.

## 5. Rule-by-rule static soundness review

The exhaustive machine-generated inventory is
[`evidence/rule-inventory.log`](evidence/rule-inventory.log), produced by
[`evidence/rule_inventory.py`](evidence/rule_inventory.py). It enumerates every
declaration and rule with source line, complete normalized text, attributes,
and operational/equational class. Across the 24 supplied-semantics files plus
`verification.k` and `spec.k`, it records:

- 229 syntax declarations, one configuration, five contexts, 697 rules, and
  two claims;
- 147 `[function]` declarations and 107 `[total]` declarations;
- no `[functional]` declarations and no `[simplification]` rules;
- 35 `[concrete]` rules, 26 `[owise]` rules, 41 priority-40 rules, one
  priority-39 rule, and three priority-45 rules; and
- 25 named `symbol(...)` declarations, 22 of which explicitly use
  `[no-evaluators]`.

I reviewed all inventoried entries. The rule-level disposition is summarized
below; the inventory supplies the individual entries rather than eliding them.

| File/module | Rules | Static disposition |
|---|---:|---|
| `semantics.k` | 0 | Assembly imports only; proof imports `MPY`, not `MPY-CONCRETE`. |
| `syntax.k` | 0 | AST declarations and evaluation attributes; used constructors map exactly as listed below. |
| `core.k` | 46 | Used lookup, argument evaluation, literals, statement sequencing, and frame-state helpers preserve the required cells and evaluation order. Remaining collection/closure-cell helpers are fixed and unreachable here. |
| `operators.k` | 10 | Used `Compare` contexts and `BinOp`/`Compare` dispatch are faithful for integer operands. Ref-dereference rules are unreachable. |
| `int.k` | 16 | Used equality, subtraction, exponentiation, and multiplication are K mathematical integer operations. `N >= 2` entails the exponent guard. Guards and overlaps on the used sorts are disjoint or agreeing. |
| `str.k` | 28 | The concrete ASCII docstring is converted to codes and then discarded. Its value cannot influence control or result. Other string rules are unreachable. |
| `controls.k` | 34 | `Expr` discard and `If` evaluation/branching are faithful. Loop, assignment, and control-transfer rules are unreachable. |
| `functions.k` | 15 | Parameter binding, return, frame pop, scope restoration, and return-value propagation match the exact single call. Closure-cell variants are unreachable. |
| `call.k` | 21 | Callee then argument evaluation selects the exact scope-0 closure; the ordinary closure call executes its body. No builtin/method dispatch is reached. |
| `bool.k` | 13 | Not reached: the comparison returns a K Bool directly to `If`; no `BoolOp` is present. |
| `builtins.k` | 137 | No builtin is called. Its folds, evaluator, MD5 boundary, and helpers have no dependency path to either claim. |
| `float.k` | 121 | No float syntax or value is reachable. All float opaque primitives have zero influence on the claims. |
| `list.k` | 27 | No list syntax/value is reachable. |
| `tuple.k` | 21 | No tuple syntax/value is reachable. |
| `subscript.k` | 40 | No indexing or slicing is reachable. |
| `comprehension.k` | 7 | No comprehension is present. |
| `methods.k` | 75 | No attribute or method call is present. |
| `set.k` | 12 | No set operation is present. |
| `dict.k` | 28 | No dict operation is present. |
| `sort.k` | 19 | No sort is present; `sortVS` and `sortKeyVS` cannot influence the claims. |
| `range.k` | 6 | No range is present. |
| `iter.k` | 0 | Iterator declarations only; no iterator is reached. |
| `assert.k` | 3 | Used only by the separate LLVM test harness, never by the proof claims. |
| `concrete.k` | 16 | Present only in `MPY-KRUN`; absent from the Haskell proof definition. |
| `verification.k` | 2 | Both candidate rules are justified below. |

### Construct-to-rule map for the submitted program

| Submitted construct | Declaration and material semantics |
|---|---|
| `Module`, `FuncDef`, `Params`, statement list | `syntax.k`; `core.k` module/sequence rules and `functions.k` function binding. The entry claim uses the mechanically equivalent direct binding. |
| `Expr(Str(docstring))` | `syntax.k`, `str.k` literal/code rules, then `controls.k` `Expr(_:Val) => .K`. |
| `If` | strict condition declaration in `syntax.k`; `controls.k` `If` to `#branch`, then the true/false branch rule. |
| `Compare(Name("n"), CmpOp("==", Int(1)))` | lookup and literal rules in `core.k`; comparison contexts/dispatch in `operators.k`; integer equality in `int.k`. |
| `Return` | strict return evaluation and frame pop in `functions.k`. |
| `BinOp("-", ...)`, `BinOp("**", ...)`, `BinOp("*", ...)` | left-to-right strictness/dispatch in `syntax.k` and `operators.k`; integer equations in `int.k`. |
| Function call | the fresh wrapper enters `Call`; `call.k`, `core.k`, and `functions.k` perform binding, body execution, return, and restoration. |

### Candidate extensions

`startsOneEndsBody` is a ground definitional summary, not an oracle or
operational shortcut. It has one unguarded equation, no overlap, no recursion,
and expands to the exact source body. It influences the result only by being
executed through the ordinary supplied semantics.

`#invokeStartsOneEnds` is fresh invocation notation. Its sole rule changes only
the active `<k>` item to an ordinary `Call`, preserves the continuation, and
does not read, write, omit, or abstract any state cell. Since the symbol has no
fixed-semantics behavior to preempt, this is not a bridge that skips
program-defined execution.

There are no candidate priority rules, simplifications, opaque symbols,
totality assertions, mathematical lemmas, helper claims, or call
interceptions. Thus no bridge-free connection theorem is required for a
program-derived abstraction: no such abstraction exists.

### Opaque and fixed-semantics boundaries

The supplied semantics names the following opaque families:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`,
`sortVS`, `sortKeyVS`, and `md5hexCodes`. None appears in the program,
preconditions, postconditions, or any reachable intermediate state. They are
not result-bearing for this theorem.

Compiler coverage warnings likewise concern `mapStrVS`, float conversion
functions, `joinCodes`, or `valSeqAt` on unrelated constructors. No
false-conclusion witness on the intended positive-integer executions was found,
so I do not label those unreachable fixed-semantics limitations as an
unsoundness of this proof.

For the actually executed path, guards cover every case, competing equations
are disjoint or agree, recursion descends, abrupt return has the exact active
call frame, and all material operations execute. No rule encodes the task
answer independently of the bound body.

## 6. Fresh non-vacuity test

I wrote a new spec with the same satisfiable `n = 1` precondition but changed
the result obligation from `1` to the false value `2`:
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k).

The dry run exits 0, proving that the mutation parses and compiles:
[`evidence/vacuity-dry-run.log`](evidence/vacuity-dry-run.log).
The actual proof exits 1 with `WarnStuckClaimState`; its terminal residual has
`<k> 1 ~> .K </k>`, which cannot unify with the destination result `2`:
[`evidence/vacuity-kprove.log`](evidence/vacuity-kprove.log).

This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash. Gate A non-vacuity passes.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` semantics and the exact displayed initial state:

- invoking the exact submitted function body at `n = 1` reaches result `1`
  with the displayed state restored; and
- for every mathematical K integer `N >= 2`, invocation reaches
  `18 * 10^(N-2)` with the displayed state restored.

Together the claims cover every positive integer. They do not cover `n <= 0`,
non-integers, exceptions outside the modeled path, or Python resource limits;
none belongs to the stated source-contract domain.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell backend, and reachability prover | Machine checking of both claims | Standard low-level proof-tool trust. Fresh builds and positive/negative runs behave consistently. |
| Supplied `MPY` semantics for names, calls, frames, `If`, return, strings, and integer operations | The whole execution theorem | Acceptable for this benchmark after exact tree integrity and rule review. No result-bearing opaque primitive is reached. |
| K mathematical `Int`, `Map`, `List`, `String`, equality, subtraction, multiplication, and nonnegative exponentiation hooks | Arithmetic and machine state | Standard built-in theory. Values are unbounded, matching Python integers on the intended domain. |
| Trusted `py2mpy.py` for the used AST nodes | Source-to-`.mpy` bridge | Byte regeneration, AST inspection, and constructor-level pinning all pass. |
| Direct closure binding instead of executing module load inside each claim | Program identity | Mechanically discharged by exact binding/body comparison and an independent concrete module-load run. |
| Inclusion-exclusion identification of `18 * 10^(n-2)` with the natural-language count | Human-facing contract | Mathematically sound but informal: the K postcondition states the closed form, not a formal set/cardinality predicate. The trusted canonical is identical and brute enumeration confirms `n=1..5`, but finite testing is not a universal proof. |
| Supplied float/sort/MD5 opaque symbols | None | Irrelevant to these claims; no interpretation can affect control, state, or result here. |

The remaining limitation is the last substantive row: the elementary
closed-form-to-count argument is not itself encoded in K. For `n >= 2`, there
are `10^(n-1)` numbers starting with 1, `9*10^(n-2)` ending with 1, and
`10^(n-2)` in their intersection, yielding
`10^(n-1) + 9*10^(n-2) - 10^(n-2) = 18*10^(n-2)`; `n = 1` has only the
number 1. This bridge is clear, agrees with the trusted canonical, and does not
enable a false program conclusion, but it remains an informal intent bridge.
Under the benchmark's decision boundary, that warrants `CONCERNS / LEGIT`
rather than `PASS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
