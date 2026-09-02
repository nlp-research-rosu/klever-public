# Independent adversarial audit: 83-starts-one-ends

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof for the submitted function over its stated domain of positive integers.
The proof was rebuilt from source and both entry claims independently closed
with exit status 0 and `#Top`. The proof-local rules expand the exact submitted
function body and route a fresh entry marker into the supplied call semantics;
they do not replace the result-bearing arithmetic with an oracle.

The verdict is `CONCERNS / LEGIT`, not `PASS`, for three auditability
limitations that do not make a false conclusion provable:

1. `run-input.json`, `metrics.json`, `codex-last.txt`, and
   `codex-output.log` are absent, and there is no structured generation trace.
2. The submitted target claims begin from an exact post-module-load entry state
   rather than executing the `Module(FuncDef(...))` term in the same claim. I
   independently proved that load-to-entry connection, but the connection
   claim is reviewer-authored rather than candidate-supplied.
3. The bridge from the returned formula to the English counting problem is a
   mathematical argument plus finite enumeration/differential evidence, not a
   K formalization of decimal digit sets.

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode, so this is a candidate audit, not an `AUDIT_ERROR`.

## 1. Input and provenance integrity

### Mode boundary and supplied semantics

`/reference/reference-semantics` is present as required. It and the candidate
tree each contain 24 regular files and two directories. There are no symlinks
under the candidate. A recursive, no-dereference comparison exited 0 with no
differences:

```text
diff --no-dereference -r /reference/reference-semantics /candidate/reference-semantics
exit 0
```

Evidence: [command](evidence/01_reference_semantics_diff.command),
[status](evidence/01_reference_semantics_diff.status), and
[tree entry types](evidence/24_tree_types.log). This establishes that the
candidate did not add, remove, mistype, symlink, or alter a supplied-semantics
entry. It does not bless `verification.k`, which is reviewed separately below.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounts. Both `cmp` commands exited 0
([prompt](evidence/02_prompt_cmp.command),
[translator](evidence/03_translator_cmp.command)). The matching SHA-256 pairs
are recorded in [23_source_hashes.log](evidence/23_source_hashes.log).

### Missing and extra artifacts

The following requested provenance artifacts are missing:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured trace was found. The exact check is in
[00_candidate_artifacts.log](evidence/00_candidate_artifacts.log). Because
these artifacts would themselves be untrusted claims and all proof sources
needed for reconstruction are present, their absence limits provenance and
auditability but does not invalidate the reconstructed theorem.

An extra `/candidate/__pycache__/solution.cpython-310.pyc` cache exists outside
the supplied-semantics tree. It was ignored and removed only from the scratch
copy. The candidate also includes `prove.sh`, `concrete_tests.py`, and
`concrete_tests.mpy`; none was accepted as proof evidence without independent
reconstruction. No candidate-built K definition was present or reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and algorithm

The trusted prompt says: for a positive integer `n`, return the number of
`n`-digit positive integers whose first digit or last digit is `1`.

The trusted canonical and submitted Python entry-point ASTs are identical
([25_ast_fidelity.log](evidence/25_ast_fidelity.log)). Their algorithm is:

- if `n == 1`, return `1`;
- otherwise return `18 * 10 ** (n - 2)`.

This matches the English contract. For `n = 1`, the only one-digit positive
integer satisfying the property is `1`. For `n >= 2`, inclusion-exclusion gives:

```text
starts with 1:                 10^(n-1)
ends with 1:                 9*10^(n-2)
starts and ends with 1:        10^(n-2)
union:            10^(n-1) + 8*10^(n-2) = 18*10^(n-2)
```

The intended domain excludes zero, negative integers, non-integers, and a call
with no argument.

### Translation identity

I regenerated the MiniPython AST using the trusted translator:

```text
python3 /reference/py2mpy.py solution.py > ../regenerated-solution.mpy
cmp regenerated-solution.mpy source/solution.mpy
```

Both commands exited 0. Evidence:
[translation](evidence/04_regenerate_solution.command) and
[byte comparison](evidence/05_solution_mpy_cmp.command). Therefore the
submitted `solution.mpy` is the trusted translation of the submitted Python
source, byte for byte.

### Independent differential and intent checks

The reviewer-authored
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and candidate entry points independently. It checked:

- fixed boundary and representative values
  `1, 2, 3, 4, 5, 9, 10, 25, 100, 250, 512`;
- 200 deterministic generated positive integers in `[1, 512]`, seed `8301`;
- exact value and result type;
- independent brute-force enumeration for digit lengths 1 through 5;
- ground substitutions into both formal postconditions at `n = 1, 2, 7, 10`;
- the excluded empty-call behavior, solely as a robustness probe.

The run exited 0 with 211 intended-domain comparisons, zero mismatches, and
these ground rows:

```text
(1, 1, 1, 1)
(2, 18, 18, 18)
(7, 1800000, 1800000, 1800000)
(10, 1800000000, 1800000000, 1800000000)
```

Evidence: [command](evidence/06_differential.command),
[status](evidence/06_differential.status), and
[output](evidence/06_differential.log). These are finite intent/translation
checks, not substitutes for the K proof.

## 3. Clean proof reconstruction

All work occurred under `/tmp/audit-work/83-starts-one-ends`. I copied source
artifacts there, deleted the copied Python cache, and built new LLVM and Haskell
definitions. The installed tools are `/usr/bin/kompile` and `/usr/bin/kprove`,
both K `v7.1.337`
([22_tool_versions.log](evidence/22_tool_versions.log)).

### Concrete definition

Fresh build:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition ../runtime-kompiled
```

Exit status was 0
([command](evidence/07_build_runtime.command),
[log](evidence/07_build_runtime.log)). A reviewer-authored Python harness was
translated with the trusted translator and executed with the fresh definition.
It asserted results at `n = 1, 2, 3, 5, 10`; `krun` exited 0 with `.K`,
`NoExc`, and exit code 0
([source](evidence/audit_concrete.py),
[translated AST](evidence/audit_concrete.mpy),
[execution](evidence/09_run_audit_concrete.log)).

I also executed the actual submitted `solution.mpy` with the fresh runtime.
The final module scope contains `starts_one_ends` bound to a closure whose body
is exactly the submitted docstring, conditional, and arithmetic return
([14_run_submitted_module.log](evidence/14_run_submitted_module.log)).

The LLVM build emitted six non-exhaustiveness warnings for supplied
`[total]` functions: `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`. None is generated or consumed by this integer-only function. These
warnings are accounted for in Stages 5 and 7.

### Proof definition and every positive target claim

Fresh build:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition ../verification-kompiled
```

Exit status was 0
([command](evidence/10_build_verification.command),
[log](evidence/10_build_verification.log)).

I ran the original combined spec and separately extracted each claim:

| Target | Exact spec invocation | Exit | Required output |
|---|---|---:|---|
| original two claims | `kprove spec.k --definition ../verification-kompiled --spec-module SPEC` | 0 | `#Top` |
| `n = 1` only | `kprove spec-n1.k --definition ../verification-kompiled --spec-module SPEC-N1` | 0 | `#Top` |
| symbolic `N >= 2` only | `kprove spec-nge2.k --definition ../verification-kompiled --spec-module SPEC-NGE2` | 0 | `#Top` |

Evidence:
[combined](evidence/11_prove_combined.log),
[n=1](evidence/12_prove_n1.log), and
[N>=2](evidence/13_prove_nge2.log), with exact commands and statuses in the
corresponding `.command` and `.status` files. The extracted specs are preserved
as [spec-n1.k](evidence/spec-n1.k) and
[spec-nge2.k](evidence/spec-nge2.k).

The only warnings in the Haskell build/proof runs are unused variables in two
ground lexicographic string rules. They do not affect closure or soundness.

## 4. Adequacy and real-program pinning

### Plain-language claims

Both claims require the same complete entry state:

- environment location 0;
- module scope 0 binds `"starts_one_ends"` to a one-argument closure with
  parent scope 0 and the exact `startsOneEndsBody`;
- builtins scope at `-1`;
- allocation counters at their initial values;
- empty heap and call stack;
- no pending return or exception; exit code 0.

The first claim calls the function at the concrete argument `1` and requires
the final `<k>` value to be exactly `1`.

The second universally quantifies K integer `N`, requires `N >= 2`, calls the
function at `N`, and requires the final `<k>` value to be exactly
`18 *Int (10 ^Int (N -Int 2))`.

These claims partition every positive integer: `1` or `>= 2`. The destination
contains no free result variable, existential oracle, implication-only result,
or unconstrained observable cell. All listed cells must be restored.

### Actual program connection

The target `<k>` cell starts with the fresh harness term
`#invokeStartsOneEnds`, not with the literal submitted `Module(...)`. That is
the principal adequacy limitation. It is nevertheless pinned to the real
submitted function by all of the following:

1. Trusted translation reproduces `solution.mpy` byte-for-byte.
2. `startsOneEndsBody` expands to exactly the `FuncDef` body in that file.
3. Concrete execution of the submitted module produces exactly the closure
   precondition used by the entry claims.
4. A fresh reviewer-authored load connection claim symbolically executes the
   exact submitted `Module(FuncDef(...))` AST into that entry state. It exited 0
   with `#Top`
   ([spec-load-bridge.k](evidence/spec-load-bridge.k),
   [result](evidence/16_prove_load_bridge.log)).
5. Changing only the proof-side body coefficient from 18 to 19 makes that load
   connection fail cleanly; see Stage 6.

Thus the submitted target proof is an exact function-entry theorem rather than
a substituted algorithm. No helper or loop claim summarizes control flow; the
program has no loop.

### Control and state fidelity

After the fresh marker becomes an ordinary `Call`, the fixed supplied rules
perform:

1. module-scope lookup of `starts_one_ends`;
2. left-to-right evaluation of argument `N`;
3. fresh call-frame allocation and binding of local `n`;
4. evaluation and discarding of the docstring expression;
5. evaluation of `n == 1`;
6. the corresponding return branch;
7. for `N >= 2`, subtraction, nonnegative integer exponentiation, and
   multiplication in Python precedence order;
8. return, frame deletion, and restoration of the caller environment and all
   observable cells.

The `N >= 2` guard proves the exponent `N - 2` nonnegative, exactly matching
the guard on supplied integer exponentiation. For `n = 1`, the return rule
discards the later statement before that exponent is evaluated.

The concrete module-load state is a satisfying witness for the common entry
precondition. Calling it with `1` witnesses the first claim; calling it with
`2` witnesses the second. The ground result comparison with both Python
implementations is recorded in
[06_differential.log](evidence/06_differential.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored
[build_rule_inventory.py](evidence/build_rule_inventory.py) enumerates every
local K configuration, context, syntax/function declaration, rule, and claim
from the supplied semantics, `verification.k`, and `spec.k`. The line-addressed
inventory has:

- 934 records;
- 697 rules: operational and equational;
- 229 syntax declarations;
- 5 contexts;
- 1 configuration;
- 2 claims.

The complete inventory is
[rule_inventory.tsv](evidence/rule_inventory.tsv), with each full source block
in [rule_inventory_full.txt](evidence/rule_inventory_full.txt) and per-file
counts in
[rule_inventory_summary.txt](evidence/rule_inventory_summary.txt).

| File | Syntax | Function declarations | Operational rules | Equational rules | Other |
|---|---:|---:|---:|---:|---:|
| `assert.k` | 0 | 0 | 3 | 0 | 0 |
| `bool.k` | 0 | 0 | 10 | 3 | 1 context |
| `builtins.k` | 9 | 29 | 35 | 102 | 0 |
| `call.k` | 2 | 1 | 20 | 1 | 0 |
| `comprehension.k` | 3 | 0 | 0 | 7 | 0 |
| `concrete.k` | 2 | 3 | 7 | 9 | 0 |
| `controls.k` | 3 | 0 | 34 | 0 | 0 |
| `core.k` | 22 | 15 | 18 | 28 | 1 configuration |
| `dict.k` | 4 | 8 | 11 | 17 | 0 |
| `float.k` | 8 | 26 | 25 | 96 | 0 |
| `functions.k` | 4 | 0 | 15 | 0 | 0 |
| `int.k` | 0 | 1 | 0 | 16 | 0 |
| `iter.k` | 1 | 0 | 0 | 0 | 0 |
| `list.k` | 2 | 3 | 13 | 14 | 0 |
| `methods.k` | 0 | 27 | 3 | 72 | 0 |
| `operators.k` | 0 | 0 | 8 | 2 | 2 contexts |
| `range.k` | 0 | 2 | 2 | 4 | 0 |
| `set.k` | 1 | 5 | 0 | 12 | 0 |
| `sort.k` | 0 | 6 | 5 | 14 | 0 |
| `str.k` | 0 | 5 | 3 | 25 | 0 |
| `subscript.k` | 2 | 13 | 10 | 30 | 2 contexts |
| `syntax.k` | 16 | 0 | 0 | 0 | 0 |
| `tuple.k` | 3 | 1 | 16 | 5 | 0 |
| `verification.k` | 1 | 1 | 1 | 1 | 0 |
| `spec.k` | 0 | 0 | 0 | 0 | 2 claims |

Attribute inventory: 146 `[function]` declarations, 107 `[total]`,
35 `[concrete]`, 22 `[no-evaluators]` opaque symbols, 26 `[owise]` rules,
45 priority rules, 4 macro declarations, and the strict/seqstrict evaluation
attributes in `syntax.k`. There are no local `[functional]` or
`[simplification]` attributes.

### Submitted syntax-to-rule map

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` `#loadAll`; `functions.k` closure installation. Used by the load connection, while target claims start from its exact result. |
| statement list and `.Stmts` | `core.k` sequencing rules at lines 126–127. |
| `Call`, `Name`, argument `Int(N)` | `call.k` lines 20–21 and 69–74; `core.k` lines 131–134, 189–194. |
| `Expr(Str(...))` | `Expr` strictness and `controls.k` line 48; `str.k` lines 13–17. The constant is ASCII and the value is discarded. |
| `If` | strict condition declaration in `syntax.k`; `controls.k` lines 51–54. |
| `Compare(..., "==", ...)` | left/right contexts and dispatch in `operators.k`; integer equality in `int.k` line 26; Boolean truth in `core.k` line 200. |
| `BinOp("-", ...)` | `seqstrict(2,3)` and dispatch; `int.k` line 13. |
| `BinOp("**", ...)` | same evaluation order; guarded integer power in `int.k` line 17. |
| `BinOp("*", ...)` | same evaluation order; integer multiplication in `int.k` line 14. |
| `Return` | strict result evaluation; `functions.k` lines 78–90 restore the caller state. |
| `#invokeStartsOneEnds` | fresh proof harness in `verification.k`, rewritten to the ordinary `Call`. |
| `startsOneEndsBody` | nullary proof-local function with one exhaustive equation to the exact translated body. |

The exact directly exercised rule rows are marked
`directly-used-reviewed` in the TSV inventory. Generated heating/cooling rules
come solely from the inventoried strictness declarations.

### Proof-local extensions

`startsOneEndsBody` is a definitional syntax abbreviation, not a
result-bearing oracle. Its single unconditional equation covers its complete
nullary domain, terminates immediately, has no overlap, and expands to the
exact translated statements. It affects control and the returned value only
by exposing those statements to fixed execution. The successful load
connection and failed body mutation validate that connection.

`#invokeStartsOneEnds(N)` is an entry harness. Its rule changes only the head
term to `Call(Name("starts_one_ends"), Int(N))`, preserves the arbitrary
continuation denoted by `...`, and reads or writes no state cell. Because the
marker is fresh proof syntax, the rule cannot preempt a source-language
semantic rule. Binding is selected by the fully pinned module scope, after
which ordinary lookup and call rules execute. It neither returns abruptly nor
skips the function body.

There are no proof-local priority rules, opaque symbols, lemmas, assumptions,
totality declarations, or simplification rules.

### Supplied rules, overlaps, totality, and opacity

For the reachable path, guards are exhaustive and non-overlapping:

- lookup finds each pinned name in the current scope;
- the one positional parameter and one argument make both parameter-binding
  base and step cases exact;
- integer equality splits `n = 1` from `n != 1`; the second claim's `N >= 2`
  excludes the first branch;
- integer subtraction, multiplication, and power are sort-specific and do not
  overlap float/string/list cases;
- call allocation and `#pop` preserve the heap, restore environment 0, delete
  the temporary scope, reset `scopeLoc`, empty the stack, and clear `ret`;
- no priority rule for a different head or value sort can preempt these steps.

All other inventoried supplied rules have source heads or value sorts absent
from the submitted program and are marked
`inert-for-submitted-program-reviewed-for-overlap`. I checked that the
reachable rules do not generate any of their heads. In particular, the 22
opaque float/sort/digest symbols never influence control, state, return value,
or either postcondition. `MPY-CONCRETE` is imported only into the fresh LLVM
runtime module, not the Haskell verification module.

The six compiler warnings identify a real global coverage limitation of the
supplied subset's `[total]` annotations. There is no concrete or symbolic
intended-domain witness in which this function generates any warned term, so
the required false-conclusion witness for calling one of these rules unsound is
absent. I therefore record a narrower semantics-coverage concern rather than
mislabel an unreachable rule as an unsound basis for this theorem.

I found no candidate or reachable supplied rule that can enable a false
conclusion on the intended domain, so there is no unsoundness witness to
report. The mutation witnesses in Stage 6 instead show that false result and
body conclusions are rejected.

## 6. Fresh non-vacuity test

The candidate supplies no `spec-vacuity.k`.

I first tried a symbolic coefficient mutation. It parsed successfully, but
the backend stopped with `DecidePredicateUnknown` while checking symbolic
definedness of exponentiation. Because that is not clean non-vacuity evidence,
I did not count it. The attempt is preserved in
[spec-audit-vacuity-symbolic-attempt.k](evidence/spec-audit-vacuity-symbolic-attempt.k)
and the `17a_...`/`18a_...` logs.

The counted mutation is
[spec-audit-vacuity.k](evidence/spec-audit-vacuity.k). It uses the satisfiable
ground entry state at `n = 2` and changes the required result from true value
`18` to false value `19`.

Build/parse check:

```text
kprove spec-audit-vacuity.k \
  --definition ../verification-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --dry-run
exit 0
```

Proof:

```text
kprove spec-audit-vacuity.k \
  --definition ../verification-kompiled \
  --spec-module SPEC-AUDIT-VACUITY
exit 1
```

The proof produced `WarnStuckClaimState`; its residual has actual
`<k> 18 ~> .K </k>` and cannot unify with destination `19`. Evidence:
[dry-run](evidence/17_vacuity_dry_run.log) and
[failed proof](evidence/18_vacuity_proof.log). This is a reachable,
result-constraining failure, not a parser error, missing import, timeout, or
unrelated crash.

As a separate operational-sensitivity test, I changed only the proof-side body
coefficient from 18 to 19
([mutated verification](evidence/verification-body-mutation.k)). The modified
definition built successfully
([19_build_body_mutation.log](evidence/19_build_body_mutation.log)). Then:

- the original `n = 2` obligation failed with actual result 19 against
  destination 18
  ([20_body_sensitivity_proof.log](evidence/20_body_sensitivity_proof.log));
- the module-load connection failed because the submitted module still loads
  the coefficient-18 body while the helper expands to coefficient 19
  ([21_body_mutation_load_bridge.log](evidence/21_body_mutation_load_bridge.log)).

Both failures are clean `WarnStuckClaimState` residuals. This independently
establishes body sensitivity and source-to-helper sensitivity.

## 7. Proven versus assumed accounting

### Precisely what the reachability proof establishes

Under the supplied K semantics and the exact entry configuration, the
translated function:

- returns `1` when invoked with `1`;
- for every mathematical K integer `N >= 2`, returns
  `18 * 10^(N-2)`;
- restores the listed environment, scope store/counter, heap/counter, stack,
  return, exception, and exit-code cells.

The fixed execution is loop-free and reaches the destination in both claims.
At minimum this establishes the requested partial correctness: if the
submitted function terminates on a positive integer, its return value has the
stated form. Resource exhaustion in a real Python runtime is outside a partial
correctness theorem.

The English counting interpretation follows from the inclusion-exclusion
argument in Stage 2. That interpretation is independently supported, but not
universally proved in K, by enumeration for `n = 1..5` and the 211-case
differential run.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied semantics tree | all K executions and claims | Acceptable fixed semantics for this task; candidate tree is recursively identical. Reachable rules were statically audited. Global unused subset limitations are noted. |
| K v7.1.337 parser, compiler, Haskell/LLVM backends, and reachability engine | builds, `krun`, `kprove` | Standard machine-checking trust boundary. Fresh builds avoid candidate caches. |
| K built-in unbounded integers, Boolean theory, maps, lists, strings, and `^Int` | equality, guard reasoning, arithmetic result, cells | Acceptable low-level mathematical/runtime primitives. The nonnegative exponent guard is proved on the symbolic branch. |
| Trusted `/reference/py2mpy.py` | Python-to-MiniPython bridge | Explicitly trusted input; regeneration is byte-identical. |
| Trusted prompt and canonical Python implementation | natural-language intent and differential oracle | Explicitly trusted inputs. AST equality and differential evidence support the bridge. |
| Exact post-load entry-state extraction | connection from submitted `Module` to target claims | Candidate states it manually; reviewer load claim proves it under fixed semantics. Legitimate but a documentation/auditability concern because it is not in the submitted target spec. |
| Inclusion-exclusion argument | formula-to-counting interpretation | Ordinary mathematics and independently enumerated for small cases; informal rather than K-formalized. |
| Finite Python differential/brute-force testing | implementation and intent support | Reproducible finite evidence only; not used as a universal proof. |
| Opaque float, sort, keyed-sort, and MD5 functions in supplied semantics | none | Inert. No path, branch, result, cell, or postcondition depends on them. |
| Missing generation metadata/logs | provenance only | Concerning for traceability, but not a semantic or proof assumption. |

### Gate accounting and exclusions

- Real-program soundness: **pass**. Exact body executes; no result oracle;
  binding, continuation, state, and return behavior are preserved; false
  postcondition and body mutations are rejected.
- Intent adequacy: **pass with an informal bridge**. Formal domain exactly
  covers positive integers, and the formula matches the counting contract.
- Evidence auditability: **concern**. Reconstructed evidence is complete and
  reproducible, but candidate generation metadata is missing and the load
  connection was not candidate-supplied.

Excluded behavior: `n <= 0`, non-integer arguments, missing arguments,
CPython resource limits, and all unrelated MiniPython constructs. For example,
the Python implementation returns a floating result for some excluded
nonpositive inputs because of negative exponentiation; neither prompt nor
formal claims include those cases.

The limitations do not permit a false conclusion on the intended domain and
do not constitute a material adequacy gap. They justify `CONCERNS`, while the
successful reconstruction, static audit, source connection, and mutations
justify `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
