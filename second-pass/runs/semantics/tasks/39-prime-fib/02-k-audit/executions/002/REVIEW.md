# Independent adversarial review: 39-prime-fib

The candidate contains a sound, non-vacuous, source-pinned K proof of eleven
ground executions. It does **not** contain the requested partial-correctness
proof over the source contract's positive-integer domain. `spec.k` fixes
`n` separately to 1 through 11 and fixes each answer to a constant. This is a
material domain restriction, not a minor evidence limitation. Under the
benchmark-specific decision rule, the otherwise `SOUND-BUT-LIMITED` result is
therefore `FAIL / NOT_LEGIT`.

No candidate verdict is based on the old logs, old compiled artifacts, a
timeout, or an alleged unsound rule. I rebuilt and exercised the sources
independently.

## 1. Input and provenance integrity

The launcher record `/audit-input.json` declares:

- problem `39-prime-fib`, condition `semantics`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- the mounted paths under `container_paths`, rather than the host-only
  provenance paths.

The mounted `/reference/reference-semantics` exists, as required for this mode.
There is no rendered-mode contradiction and hence no infrastructure breach.

I read `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, the invocation and metrics records, `usage.json`,
`prompt.txt`, `codex-last.txt`, `codex-output.log`, both retained legacy JSON
records, and the complete structured trace. `runtime-metrics.json` is absent,
but it is not required by `legacy-selected-stage1`. The sole trace file has
804 valid JSONL records and zero parse failures. These generation records were
treated only as untrusted historical claims.

Independent checks found:

- the campaign lock is structurally identical to `audit_campaign` and its
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- every launcher-recorded regular-file hash checked in
  `/audit-input.json` and `/generation-result.json` matches its mounted file,
  including the run/task/result/invocation records, generation prompt, usage,
  metrics, output log, final message, and trace JSONL;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- the candidate and trusted semantics trees each contain the same 25 entries.
  Every relative path, entry type, and file SHA-256 matches. Their independently
  serialized per-entry manifests also have the same digest,
  `5878475d5f42b9ebb418f0e27a98f3ef48274d51f1ab2901cb150b034cb49f38`;
- there are no symlinks anywhere in the candidate, trusted-reference, or
  generation-evidence trees;
- all required candidate proof deliverables (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, and `prove.sh`) are present and regular.

Detailed hashes, entry types, the full supplied-semantics file manifest, and
the trace parse are preserved in:

- `/audit-output/evidence/provenance_check.py`
- `/audit-output/evidence/provenance.log`
- `/audit-output/evidence/trace_inspect.py`
- `/audit-output/evidence/trace-inspection.log`

Stage result: infrastructure and provenance integrity pass.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py:3-15` requires `prime_fib(n: int)` to return the
`n`-th number that is both Fibonacci and prime. The ordinal and the examples
make the intended material domain positive integers (`n >= 1`); the prompt
does not impose an upper bound. `/reference/canonical.py:23-36` generates
Fibonacci values, tests primality, decrements `n` for each prime Fibonacci
value, and returns when the count reaches zero.

`/candidate/solution.py:1-41` implements trial-division primality, with truthful
fast-path constants for eleven prime and six composite Fibonacci values.
`prime_fib` at lines 44-67 is a general search: it advances the Fibonacci pair,
increments `found` exactly when `_is_prime(first)` is true, and returns when
`found == n`.

### Trusted regeneration

In the clean scratch copy I ran the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both translated files have SHA-256
`5b5767149db4eb45167fdd64d6388b0c19a3d7dca232656816ce67ad31073d26`;
`cmp` exited 0. See `/audit-output/evidence/regeneration.log`.

### Independent differential test

`/audit-output/evidence/differential_test.py` independently imports the trusted
canonical entry point and candidate entry point. It tests:

- all documented examples;
- every submitted claim input, 1 through 11;
- positive input 12, which is beyond the submitted theorem;
- the outer-loop boundary and both outcomes;
- 420 helper inputs covering every cached value, below-two values, divisibility
  branches, the trial-loop entry/exit boundary, seeded values, and factor
  branches, against an independent `isqrt` trial-division oracle;
- `n = -1` and `n = 0` as explicitly labelled observations outside the
  positive ordinal domain.

The exact command exited 0 with no in-domain mismatch. Both Python programs
returned `99194853094755497` for `n = 12`. The helper had zero mismatches.
Outside the intended domain, the programs differ (`n = 0` gives canonical 1
and candidate 0; `n = -1` timed out in the canonical process while the
candidate returned 0). Those observations are not used against a positive-
integer contract. See `/audit-output/evidence/differential.log`.

`/audit-output/evidence/ground_math_witness.py` independently enumerates the
first eleven Fibonacci primes with integer trial division. It confirms the
claim sequence and records Fibonacci indices 3, 4, 5, 7, 11, 13, 17, 23, 29,
43, and 47. It also gives an explicit factor for every cached composite. See
`/audit-output/evidence/ground-math.log`.

These are finite fidelity and arithmetic checks. They do not turn the eleven
ground K claims into a universal theorem.

Stage result: the candidate program and translated term are faithful on the
material tested positive domain; no implementation divergence was found.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/prime-fib-audit`. No candidate kompiled directory or cache was
copied or used. The active K binaries are version 7.1.293; paths and versions
are in `/audit-output/evidence/toolchain.log`.

### Concrete definition

The first logging wrapper attempted to use an unavailable optional
`/usr/bin/time` and exited 127 before invoking K. I retained that record and
immediately reran the actual build command directly:

```text
timeout 900s kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The direct clean build exited 0. Its warnings concern non-exhaustive total
functions on value forms not reached by this program; they are accounted for
in Stage 5. See `/audit-output/evidence/kompile-concrete.log`.

Reviewer-generated MPY harnesses then executed the regenerated module under
this definition. `krun` exited 0 and left:

- `"answer" |-> 2` for `n = 1`;
- `"answer" |-> 2971215073` for `n = 11`;
- `"answer" |-> 99194853094755497` for `n = 12`.

The full configurations and commands are in
`/audit-output/evidence/krun-concrete.log`.

### Proof definition and every positive claim

The clean proof build was:

```text
timeout 900s kompile verification.k \
  --backend haskell \
  --main-module PRIME-FIB-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

It exited 0. See `/audit-output/evidence/kompile-proof.log`.

I then invoked `kprove` independently for every one of `pf1` through `pf11`,
not merely as one aggregate claim selection. Every invocation exited 0 and
printed one exact `#Top`. The summary is:

```text
CLAIM pf1..pf11: each EXIT=0 TOP_LINES=1
OVERALL EXIT: 0
```

The exact batch driver is
`/audit-output/evidence/run_positive_proofs.sh`, the summary is
`/audit-output/evidence/kprove-positive-summary.log`, and each claim has its
own bounded `/audit-output/evidence/kprove-pfN.log`.

Stage result: clean reconstruction passes for all eleven submitted positive
claims.

## 4. Adequacy and real-program pinning

### Plain-language claims

Every claim has no symbolic `requires` condition. Its precondition is one exact
ground state:

- `<k>` contains `Call(Name("prime_fib"), Int(N))`;
- the active environment is module scope 0;
- scope 0 binds `_is_prime` and `prime_fib` to the two aliases in
  `verification.k`, with the trusted builtins scope as parent;
- heap and stack are empty, allocation counters are at their initial values,
  return/exception state is clear, and exit code is 0.

Its postcondition is the same framed state with the `<k>` call replaced by one
fixed integer:

| Claim | Input | Required result |
|---|---:|---:|
| `pf1` | 1 | 2 |
| `pf2` | 2 | 3 |
| `pf3` | 3 | 5 |
| `pf4` | 4 | 13 |
| `pf5` | 5 | 89 |
| `pf6` | 6 | 233 |
| `pf7` | 7 | 1597 |
| `pf8` | 8 | 28657 |
| `pf9` | 9 | 514229 |
| `pf10` | 10 | 433494437 |
| `pf11` | 11 | 2971215073 |

Each precondition is satisfiable: it is a fully ground post-module-load
configuration, and the concrete and symbolic executions above exhibit such
states. The differential and arithmetic evidence substitute every ground
input into both Python implementations and the intended values.

### Mechanical program pinning

The claims normalize away only module loading. They do not normalize away the
function bodies:

- `isPrimeClosure` at `/candidate/verification.k:12-71` expands to a
  `closureVal` containing the complete translated `_is_prime` body;
- `primeFibClosure` at lines 73-92 expands to a `closureVal` containing the
  complete translated `prime_fib` body;
- the function-call rules in the supplied semantics bind arguments, allocate
  real call frames, execute those bodies, handle nested helper calls, and pop
  the frames.

`/audit-output/evidence/extract_pinning_terms.py` independently extracted each
`FuncDef` body from the regenerated `solution.mpy`, constructed the closure
that module loading produces, extracted the corresponding verification-rule
right-hand side, and parsed both with the clean definition. The only print
normalization was explicit `.Stmts` versus the standalone parser's omitted
empty list. The resulting KORE files compare byte-identically:

- `_is_prime` closure:
  `14dbc275e6637e55b72d38608476ab27d72315ad01be93caca51199db53c2a6e`;
- `prime_fib` closure:
  `4aac87db440478a443b31587034ea728bdd1823055b0b458b739e90febc7476d`.

Commands and the initially observed standalone-parser spelling issue are kept
in `/audit-output/evidence/program-pinning.log`.

This is sufficient mechanical constructor-level pinning for the immutable
candidate. The manual duplication is an artifact-maintenance risk, but not a
substituted-program defect here. A separate executed-body mutation changed
`Return(Name("first"))` to `Return(Int(0))` inside the proof definition itself.
That mutant built successfully and made the correct `pf1` result fail with
residual 0. See `/audit-output/evidence/body-sensitivity.log`.

### Material adequacy failure

The source contract has no bound at 11. `spec.k:6-9` expressly acknowledges
that it supplies only eleven cases. There is no symbolic entry claim, loop
invariant, helper theorem, or quantified characterization for any other
positive integer. The successful concrete and Python result at `n = 12`
exhibits an ordinary satisfying source-domain input that the theorem omits.

The comment's rationale also conflates total and partial correctness. A
universal partial-correctness claim can be conditional on termination; it does
not establish that infinitely many Fibonacci primes exist. The benchmark asks
for partial correctness, so the open termination/existence question does not
justify replacing the unrestricted positive domain with eleven examples.

Stage result: real-program pinning and result constraint pass for each ground
claim; intent adequacy fails materially.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/rule-inventory.md` inventories the complete supplied
semantics tree, `verification.k`, and `spec.k`, with source line, full
declaration text, attributes, and reachability classification for every item.
The reviewer-generated inventory contains:

- 228 syntax declarations;
- 697 rules;
- 5 contexts;
- 1 configuration;
- 11 claims;
- 942 entries total.

It separately flags 147 function-bearing declarations, 108 `total`
declarations, 45 priority occurrences, 35 concrete occurrences, 26 `owise`
occurrences, all strictness/macro declarations, and all 22
`no-evaluators` opaque symbols. There are no local `simplification` or
`functional` declarations. The inventory build and digest are in
`/audit-output/evidence/rule-inventory-build.log`.

The 22 supplied opaque symbols are the float-operation family
(`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`), `sortVS`, `sortKeyVS`,
and `md5hexCodes`. No submitted program term contains floats, sorting, or MD5,
so none can affect control or a postcondition here.

### Used-construct mapping

The submitted MPY term uses:

- `Module`, two `FuncDef`s, `Params`, statement sequencing, and `Expr(Str(...))`;
- `Call`, `Name`, `Int`, `Bool`, `Return`, `Assign`, and `AugAssign`;
- `If`, `While`, and `BoolOp("or", ...)`;
- `BinOp` for `+`, `*`, and `%`;
- `Compare` for `==`, `<`, and `<=`.

Those map to:

- syntax declarations in `semantics/syntax.k`;
- configuration, module loading/sequencing, lookup, literals, truthiness,
  argument evaluation, and exact integer values in `semantics/core.k`;
- left-to-right operator dispatch in `semantics/operators.k`, integer equations
  in `semantics/int.k`, and short-circuit Boolean evaluation in
  `semantics/bool.k`;
- assignment, branch, while, and loop-continuation rules in
  `semantics/controls.k`;
- callee evaluation and exact closure dispatch in `semantics/call.k`;
- parameter binding, return, stack-frame restoration, and scope deallocation
  in `semantics/functions.k`;
- the ASCII string-literal rule in `semantics/str.k` for the discarded
  docstring. All docstring characters are within its guarded domain.

The used execution has exact unbounded integers, nonzero modulus divisors,
empty heap, concrete guards, ordinary module/helper bindings, and no exceptions
or allocation. Argument and operand strictness is left-to-right. The helper
lookup follows the closure's parent module scope. Calls save their complete
continuation and caller environment; `Return` sets the result and `#pop`
restores environment, scope allocation, stack, and continuation. Both loops
execute through the fixed `#while`, `#whileCond`, body, and `#loopLbl` rules.

I found no overlapping used-path guards with disagreeing right-hand sides, no
unjustified used totalization, no altered evaluation order, and no omitted
material cell effect. In particular, no local rule intercepts `_is_prime`,
`prime_fib`, a loop, or a return with a computed answer.

### Proof-local extensions

The only proof-local declarations are one syntax declaration containing the
two zero-argument aliases and their two equations. They are definitional
summaries, not operational bridges:

- each has one unconditional, terminating equation;
- their domains are singleton constructors and do not overlap;
- their values are exact source-derived closures, as established by the KORE
  comparison;
- they contain no fresh or unconstrained result;
- all eleven claims depend on them only as compact names for the actual
  function values.

The answer constants cached in `solution.py` are part of the real generated
program and appear identically in its translated body; they were not added
only to `verification.k`. Their presence may make these ground executions
easier, but it is not a proof-only answer oracle.

### Unused fixed-semantics surface and warnings

The inventory marks 798 entries as unreachable from these submitted ground
terms. They remain part of the supplied-semantics trust boundary, but they
cannot enable a false result in this proof. I therefore do not label them
unsound without a witness.

The LLVM compiler warned that `mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt` have non-exhaustive matches on some broader value
forms. None is reachable here. `MPY-CONCRETE` is present only in the LLVM
definition and its deep-list-equality/keyed-sort rules are likewise unused;
the proof definition imports `MPY`, not `MPY-CONCRETE`.

No false-conclusion witness exists for a used rule or proof-local extension,
and this review does not claim semantic unsoundness. The dispositive defect is
the theorem's restricted domain.

Stage result: the ground proof's rule theory passes the real-program soundness
review; the complete unused language surface is an explicit fixed-semantics
trust limitation, not a cause of this verdict.

## 6. Fresh non-vacuity test

I created `/tmp/audit-work/prime-fib-audit/spec-vacuity-audit.k`, preserved as
`/audit-output/evidence/spec-vacuity-audit.k`, a fresh specification that keeps
`pf1`'s satisfiable exact precondition but changes its result obligation from 2
to 3.

The command was:

```text
timeout 300s kprove spec-vacuity-audit.k \
  --definition proof-kompiled \
  --spec-module PRIME-FIB-SPEC-VACUITY-AUDIT
```

The spec built far enough to execute the proof; this was not a parser/import
failure. `kprove` exited 1 with `WarnStuckClaimState`. The residual `<k>` cell
contains `2 ~> .K`, which is exactly the real result that fails to unify with
the mutated destination 3. Full command, exit status, and residual are in
`/audit-output/evidence/nonvacuity.log`.

The separately compiled body-sensitivity test described in Stage 4 also
failed for the expected semantic reason, with residual 0 after changing the
executed closure body.

Stage result: the submitted ground theorem is result-constraining,
non-vacuous, and sensitive to the executed body.

## 7. Proven versus assumed accounting

### What K actually proves

Conditional on the clean supplied MPY definition and the exact definitional
closure aliases, the reachability proof establishes:

> From each of eleven exact post-module-load configurations, calling the actual
> translated `prime_fib` body on the corresponding constant 1 through 11
> executes through the fixed semantics, terminates with the listed constant in
> `<k>`, and restores all other explicitly framed cells to the claimed state.

It does not establish a theorem containing a free input variable.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 parser, kompilers, Haskell/LLVM backends, and K built-in integer/map/list/string hooks | Proof checking and primitive arithmetic/state operations | Necessary low-level trust boundary; versions and fresh runs recorded |
| Supplied MPY semantics | Binding, evaluation order, loops, calls, returns, and state | Integrity-verified and used-path audited; acceptable for the ground theorem |
| 22 supplied opaque symbols | Potential float/sort/MD5 results in other programs | Unused by every claim; no dependent branch/result here |
| Trusted `py2mpy.py` | Source-to-constructor translation | Byte-identical mounted translator; regeneration is exact, but the translator is not itself formally verified |
| Manual aliases in `verification.k` | Values bound to the two program names | Mechanically KORE-identical to regenerated closure terms; body mutation confirms sensitivity |
| Ground primality/Fibonacci interpretation | Connects exact integers to the English phrase “n-th Fibonacci prime” | Independently trial-divided/enumerated for eleven values; finite arithmetic evidence, not a universal K theorem |
| Python differential test | Candidate/canonical fidelity on tested inputs | Zero mismatches for 1..12 and helper sample; empirical and finite only |

### Missing theorem

Nothing in the K proof establishes, for arbitrary positive `n`, either:

- that `_is_prime(x)` agrees with mathematical primality for all relevant
  integers;
- that the loop result is the `n`-th Fibonacci prime whenever the call
  terminates; or
- any loop invariant or summary from which those facts follow.

The successful `n = 12` executions are useful evidence that the program is
general, but they do not repair the formal scope. Proving only eleven examples
materially narrows an unrestricted HumanEval contract.

### Gate and benchmark decision

- Validation Gate A (real-program soundness of the submitted ground theorem):
  pass.
- Validation Gate B (intent/domain adequacy): fail.
- Validation Gate C (auditability of the ground theorem): pass.

Generic Kit terminology would call the artifact sound but limited. The
benchmark prompt explicitly maps a material HumanEval domain restriction of
this kind to `FAIL / NOT_LEGIT`, rather than `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
