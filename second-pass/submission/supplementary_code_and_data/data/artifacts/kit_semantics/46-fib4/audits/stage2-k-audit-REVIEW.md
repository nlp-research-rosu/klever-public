# Independent adversarial audit: 46-fib4

## Audit result

The candidate contains a legitimate partial-correctness proof of the submitted
program for every nonnegative integer sequence index. I independently rebuilt
the supplied semantics and proof definition from source, obtained `#Top` for
the loop claim and complete spec, mechanically matched the claimed closure body
to trusted regeneration of `solution.mpy`, reviewed every local K declaration
and rule, and rejected a fresh false result mutation with the expected concrete
residual.

The candidate's `PROOF.md`, compiled definitions, logs, and generation report
were treated only as untrusted claims. No candidate-built definition or cache
was used.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `46-fib4`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`;
- `mount_reference_semantics: true`.

The trusted `/reference/reference-semantics` tree is present, so the mount does
not contradict the rendered mode. `/audit-campaign-lock.json` is byte-hashed to
the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and its parsed object exactly equals the `audit_campaign` block in
`/audit-input.json`.

I read all required pipeline-v3 records: `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the JSONL trace. Every recorded per-file SHA-256 checked
against the mounted bytes. The one trace file matches the hash recorded in
`generation-result.json`; all 408 JSONL records parse, with 86 tool calls and 86
outputs. The 34,541-line Codex output was independently scanned. These records
claim success but were not used as proof evidence.

The candidate prompt and translator are byte-identical to their trusted mounts.
The candidate reference-semantics tree has exactly the same 25 entries
(including directories), types, and file hashes as the trusted tree: no
missing, additional, changed, mistyped, special, or symlinked entry. The six
required candidate deliverables are regular, non-symlink files. An independent
inventory of all 777 candidate entries found no special entries.

Evidence:

- `evidence/stage1-integrity.log`
- `evidence/stage1_integrity.py`
- `evidence/stage1-trace-review.log`
- `evidence/trace_review.py`
- `evidence/stage1-codex-output-review.log`
- `evidence/stage1-codex-output-scan.log`

Stage 1 result: PASS. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt defines a nonnegative-indexed Fib4 sequence:

- `fib4(0) = 0`;
- `fib4(1) = 0`;
- `fib4(2) = 2`;
- `fib4(3) = 0`;
- for `n >= 4`, `fib4(n)` is the sum of the preceding four values.

It asks for efficient computation without recursion and gives the examples
`fib4(5) = 4`, `fib4(6) = 8`, and `fib4(7) = 14`. “The n-th element” and the
definition beginning at index zero make nonnegative integers the material
source-contract domain. Incidental Python negative-index behavior of the
canonical list implementation is not a definition of negative Fib4 values.

`solution.py` is a nonrecursive, constant-register loop. At loop index `i`, the
registers `a,b,c,d` hold four consecutive sequence values; the loop shifts them
and places their sum in `d`. It performs `n` iterations for `n >= 0` and returns
`a`.

Using only the trusted `/reference/py2mpy.py`, I regenerated the MPY program in
scratch:

```text
COMMAND: python3 py2mpy.py solution.py > regenerated-solution.mpy
TRANSLATE_EXIT_STATUS=0
COMMAND: cmp -s regenerated-solution.mpy solution.mpy
CMP_EXIT_STATUS=0
```

Both files have SHA-256
`65781c343e34babd0bf415a2607f9bc5d9cb27bc2544cd7d9fb7ae90b4f3c457`.

The independent differential script imports the trusted canonical entry point
and candidate entry point under distinct module names. It also uses a separately
written stored-prefix recurrence oracle. It tests:

- zero-iteration/boundary input `0`;
- base and branch boundaries `0,1,2,3,4,5`;
- all documented examples;
- every input `0..64`;
- 100 deterministic generated inputs in `0..500` using seed `46004`.

There were 141 unique inputs, maximum 499, zero documented-example failures,
and zero mismatches among canonical Python, candidate Python, and the recurrence.
There is no collection-valued “empty” input; `n=0` is the relevant empty/zero-
iteration boundary.

Evidence:

- `evidence/differential_test.py`
- `evidence/stage2-fidelity.log`

Stage 2 result: PASS.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/46-fib4`, using the trusted
prompt, canonical implementation, translator, and trusted semantics tree. I
did not copy or reference `runtime-kompiled`, `verification-kompiled`,
`__pycache__`, or any other candidate cache.

The exact fresh commands and statuses were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-fresh-kompiled
EXIT_STATUS=0

krun solution.mpy --definition runtime-fresh-kompiled
EXIT_STATUS=0

krun concrete_checks.mpy --definition runtime-fresh-kompiled
EXIT_STATUS=0

kompile verification.k --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-fresh-kompiled
EXIT_STATUS=0

kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
#Top
EXIT_STATUS=0

kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC
#Top
EXIT_STATUS=0
```

The focused command proves the auxiliary circularity. The complete command
proves both claims together, including `SPEC.fib4-correct` with the circularity
available. Thus every positive claim is included in a successful independently
reconstructed run.

The concrete reviewer program contains the exact candidate function plus
assertions at `n = 0,1,2,3,4,5,6,7,10`; both Python and fresh LLVM execution
exit zero. Loading the actual submitted `solution.mpy` also exits zero and
produces the expected `fib4` closure in module scope with empty computation,
empty heap, no exception, and exit code zero.

The build warnings concern unused variables in supplied `str.k`, supplied
total functions outside this program, and intentionally unobserved existential
loop variables. None is a proof failure or a rule capable of affecting this
integer-only path.

Evidence:

- `evidence/stage3_reconstruct.sh`
- `evidence/concrete_checks.py`
- `evidence/stage3-reconstruction.log`
- `evidence/stage3-kompile-llvm.log`
- `evidence/stage3-krun-solution.log`
- `evidence/stage3-krun-concrete.log`
- `evidence/stage3-kompile-haskell.log`
- `evidence/stage3-kprove-loop.log`
- `evidence/stage3-kprove-complete.log`

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` starts at the exact internal `#while` guard/body. Its
precondition is `0 <= I <= N`; the active local scope contains:

```text
n = N
i = I
a = fib4Spec(I)
b = fib4Spec(I + 1)
c = fib4Spec(I + 2)
d = fib4Spec(I + 3)
e = arbitrary Int
```

It says the loop is consumed, `i` becomes `N`, and `a` becomes
`fib4Spec(N)`. Final `b,c,d,e` are existential because the function neither
returns nor exposes them. The continuation and other cells are framed and
preserved. A satisfying state is `N=7`, `I=4`, `a=2`, `b=4`, `c=8`, `d=14`,
`e=0`, with an ordinary local scope.

`SPEC.fib4-correct` has precondition `N >= 0`. It starts with
`Call(Name("fib4"), Int(N))` in an exact caller configuration whose `fib4`
binding is the submitted closure, and it requires the resulting `<k>` value to
be exactly `fib4Spec(N)`. The module/builtin scopes, allocators, heap, stack,
return state, exception state, and exit code are fixed. `N=0` is an immediate
satisfying entry witness.

### Mechanical program identity

The entry claim need not re-execute module loading because it pins the binding
produced by module loading. A reviewer constructor parser compared trusted
regeneration of `solution.mpy` with the closure in `spec.k`:

- exactly one translated function named `fib4`;
- exact one-parameter binding `n`;
- exact defining environment `0`;
- exact function body after whitespace-only normalization;
- exact real `While` guard/body against the helper claim's `#while` guard/body.

The normalized translated and claimed body hashes are both:

```text
152fb4e4684217a67bdf765f39329c753e302aab9bc4aee84db7d02a800c9bd1
```

The source AST also contains exactly one `fib4`, one `while`, and no recursive
call. Fresh concrete module loading confirms that the supplied `FuncDef` rule
creates this same closure. Omitted module loading is therefore demonstrated
semantically inert normalization, not substitution of a different program.

The result is not free or tautological: `fib4Spec` is fixed by exhaustive
equations, and the target requires equality to it. Ground substitutions at
`N=0,1,2,3,4,5,7,10` agree with candidate Python and canonical Python
(`0,0,2,0,2,4,14,104` respectively).

Evidence:

- `evidence/stage4_adequacy.py`
- `evidence/stage4-adequacy.log`
- fresh LLVM closure output in `evidence/stage3-krun-solution.log`

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

I inventoried `semantics.k`, all 23 helper files below `semantics/`,
`verification.k`, and `spec.k`. The inventory contains:

- 228 local syntax declarations;
- 700 local rules;
- 5 contexts;
- 1 configuration;
- 2 claims;
- 936 total items across 26 files.

Raw declaration-start counts cross-check for every file. Attribute-bearing
items include 147 functions, 108 total declarations, 45 priority rules, 26
`owise` rules, 35 concrete rules, and 22 `no-evaluators` declarations. There
are no local `[functional]` declarations and no simplification rules. Every
item, its complete rule text/guards/attributes, and its reachability decision is
listed in `evidence/stage5-rule-inventory.md`.

### Used-constructor mapping

| Submitted construct | Declaration and fixed rules |
|---|---|
| `Module`, statement list | `syntax.k:56,61`; `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14-16` |
| `Call(Name("fib4"), Int(N))` | `call.k:19-21,69-75`; `core.k:130-134,189-194`; `functions.k:63-66` |
| `Assign(Name, RHS)` | strict declaration `syntax.k:41`; `controls.k:9-18` |
| `Name` | `syntax.k:12`; `core.k:130-154` |
| `Int` | `syntax.k:9`; `core.k:194` |
| integer `+` | sequential strictness `syntax.k:15`; `operators.k:12`; `int.k:9` |
| integer `<` | compare contexts `operators.k:15-17`; `int.k:22` |
| `While` | `syntax.k:46`; `controls.k:65-82,85` |
| `Return` | strict declaration `syntax.k:50`; `functions.k:78-90` |

The strict/seqstrict declarations and explicit comparison contexts enforce the
needed evaluation order. Call evaluates the selected binding and argument
before allocating a fresh local scope; the one parameter is bound there. All
assignments are sequential writes to that local map. The exact loop has no
break, continue, return, exception, heap operation, output, or allocation, so
the helper claim's arbitrary trailing continuation and framed cells are safe.
`Return` records the integer, discards the remaining callee continuation as a
real return must, pops the exact frame, restores the caller environment, and
deallocates the local scope.

The higher-priority cell/heap cases cannot match this state: its local bindings
are plain integers, it has no `"$cells"` marker, and the heap is empty. The
math/hash/sort call interceptions are constructor-disjoint from
`Call(Name("fib4"), ...)`. The generic call and integer rules therefore execute
the material path without preemption.

### Proof-local extensions

`verification.k` adds one declaration and five ordinary equations:

| Extension | Static decision |
|---|---|
| `fib4Spec(Int) [function,total]` | Pure definitional result summary; it never matches a program configuration or replaces execution. |
| `N <= 0 -> 0` | True totalization; target uses only `N >= 0`. |
| `1 -> 0`, `2 -> 2`, `3 -> 0` | Exact prompt base cases. |
| `N >= 4 -> sum of N-1..N-4` | Exact prompt recurrence and strictly descending. |

The guard regions `N<=0`, `N=1`, `N=2`, `N=3`, and `N>=4` are exhaustive and
pairwise disjoint over K integers. No priority, overlap, unguarded
totalization, simplification, concrete-only rule, opaque symbol, or operational
bridge is present locally.

The loop claim is a derived reachability circularity, not an ordinary rewrite.
On the false guard, `I<=N` and `not(I<N)` imply `I=N`. On the true guard, one
real body iteration moves
`fib4Spec(I),...,fib4Spec(I+3)` to the next four consecutive values using the
`fib4Spec(I+4)` recurrence, increments `I`, and reaches the same loop-head shape
after material progress. Its exact body contains no abrupt control, so it does
not discard an admitted continuation. The target then executes initializers,
instantiates the loop claim at `I=0`, reads `a`, and executes the real return/pop
path.

### Supplied opaque and partial boundaries

The supplied semantics contains opaque float operations, `sortVS`,
`sortKeyVS`, and `md5hexCodes`, plus concrete-only LLVM twins and many rules for
unused syntax. All are inventoried. None can influence a branch, value, state,
exception, control transfer, summary, or postcondition here: the submitted
program constructs only integers, names, assignments, a comparison, addition,
a while loop, a call, and return. `MPY-CONCRETE` is not imported by the Haskell
proof module at all.

The supplied language is intentionally partial outside used constructs. I found
no concrete or symbolic false-conclusion witness that any supplied off-path
rule can enable for a satisfying `fib4` entry state, so I do not label those
rules unsound. Their narrower status is an irrelevant fixed-semantics boundary,
not a proof-local correctness assumption.

Evidence:

- `evidence/stage5_inventory.py`
- `evidence/stage5-rule-inventory.md`
- `evidence/stage5-inventory-command.log`

Stage 5 result: PASS. No unsound rule or adequacy shortcut was found.

## 6. Fresh non-vacuity test

I inspected the candidate mutation only as untrusted evidence and authored a
new mutation, `AUDITOR-NONVACUITY.auditor-wrong-n4`. It uses the exact submitted
closure and satisfying input `n=4`, but changes the result-constraining
obligation from the correct value `2` to `3`. This reaches the real loop rather
than using only a zero-iteration case.

```text
COMMAND: kprove auditor-nonvacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module AUDITOR-NONVACUITY --dry-run
DRY_RUN_EXIT_STATUS=0

COMMAND: kprove auditor-nonvacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module AUDITOR-NONVACUITY
PROOF_EXIT_STATUS=1
```

The proof failure is the expected unmet obligation:

```text
Warning (WarnStuckClaimState)
<k>
  2 ~> .K
</k>
```

This is not a parser error, missing import, timeout, unreachable mutation, or
unrelated crash. The artifact builds successfully, executes to the correct
result, and fails solely because `2` does not unify with demanded `3`.

Evidence:

- `evidence/auditor-nonvacuity.k`
- `evidence/stage6_nonvacuity.sh`
- `evidence/stage6-nonvacuity-dry-run.log`
- `evidence/stage6-nonvacuity-proof.log`
- `evidence/stage6-nonvacuity-summary.log`

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Formally proven

Under the freshly built supplied MPY semantics and the five truthful
`fib4Spec` equations, for every K integer `N >= 0`, executing
`Call(Name("fib4"), Int(N))` from the exact pinned caller/closure state has the
partial-correctness result `fib4Spec(N)`. The proof includes real lookup,
argument evaluation, local-scope allocation, parameter binding, all six
initializers, every material comparison/addition/assignment in the loop,
return, frame pop, and restoration of every caller-visible cell constrained by
the claim.

This is a universal symbolic theorem over unbounded nonnegative K integers, not
finite unrolling or a collection of examples. It is partial correctness: it
does not separately formalize termination, resource exhaustion, or asymptotic
complexity. Source inspection shows a monotonically incrementing loop and no
recursion, satisfying the requested implementation shape, but that inspection
is not promoted to a K liveness/complexity theorem.

### Assumptions and trust boundaries

1. **Supplied reference semantics.** The relevant MPY rules are the fixed model
   selected by the benchmark. Their exact candidate copy was integrity-checked,
   and their used execution path was statically reviewed and concretely tested.
   Both K claims depend on this boundary. It is acceptable for
   `SUPPLIED_SEMANTICS`.
2. **Trusted translator.** Byte-identical regeneration proves artifact fidelity,
   not a general theorem that CPython AST and MPY are equivalent. Mechanical
   constructor pinning and finite Python/K tests support the bridge actually
   used by this program. This is an acceptable named input boundary.
3. **K infrastructure.** K v7.1.293, the Haskell and LLVM backends, builtin K
   integer/Boolean/map theories, SMT discharge, and host execution are trusted.
   This is the normal proof-checker boundary.
4. **Contract-domain reading.** Fib4 is interpreted on the nonnegative sequence
   indices explicitly rooted at 0. This is the material HumanEval domain, not a
   strengthening to finitely many sizes.
5. **Finite empirical evidence.** The 141-input differential test and nine-input
   K concrete test support translator/semantics/CPython alignment only on those
   inputs. They are not used in place of the universal reachability proof.

There is no program-derived opaque value, empirical result oracle, operational
bridge, task-answer rewrite, or informal summary-to-result equality on which
claim closure depends. Lack of an automatic source-to-spec generator is only an
artifact-maintenance observation; trusted regeneration plus constructor-level
comparison pins this immutable candidate.

### Gate and verdict mapping

- Gate A (real-program soundness): PASS.
- Gate B (intent adequacy): PASS; full nonnegative index domain, exact
  recurrence, and nonrecursive implementation.
- Gate C (trust/evidence auditability): PASS; all assumptions and reproducible
  evidence are recorded.

The successful fresh proofs, result constraint, exact program pinning, full
material source domain, and absence of an unsound proof extension satisfy the
benchmark's `PASS / LEGIT` boundary.

VERDICT: PASS
LEGITIMACY: LEGIT
