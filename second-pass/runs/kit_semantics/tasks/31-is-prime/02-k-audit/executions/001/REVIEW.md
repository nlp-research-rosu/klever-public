# Independent adversarial review: 31-is-prime

The candidate contains a legitimate K partial-correctness proof of the
submitted program over the intended integer domain. I reconstructed the
definitions from source, obtained fresh `#Top` results, mechanically pinned the
claim body to the trusted regeneration of `solution.mpy`, exhaustively
inventoried the K sources, and obtained meaningful failures from both an
independent body mutation and an independent false-result mutation.

I did not use the candidate's `PROOF.md`, compiled definitions, caches, traces,
or saved result logs as proof evidence.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- record layout: `pipeline-v3`;
- problem: `31-is-prime`;
- generation condition: `kit-semantics`;
- semantics mode: `SUPPLIED_SEMANTICS`; and
- a mounted trusted semantics tree at
  `/reference/reference-semantics`.

The mode and mounts are consistent. The trusted semantics tree is present, as
required in supplied-semantics mode.

I read all pipeline-v3 records required by the prompt:

- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/runtime-metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`; and
- the JSONL trace below `/generation-evidence/codex-trace/`.

All required mounts and records are regular files or directories of the
expected kind and are readable. The trace contains one file and 543 valid JSON
records. Its SHA-256,
`d1241b5afe6891ab1b1c7196cf3417348dff1210e018185ca5dffdd5521dad02`,
matches both generation manifests. The reviewer-readable chronological
extraction is in `evidence/01_trace_inspection.log`. The generation records
claim prior success, but I treated those claims as untrusted.

The campaign lock passes both required checks:

- parsed `/audit-campaign-lock.json` is exactly equal to the
  `audit_campaign` object in `/audit-input.json`; and
- its byte SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

Every launcher-recorded regular-file hash independently checked in
`evidence/01_integrity_checks.log` matches: run/task/result/invocation
manifests, all generation text/metrics/usage records, the canonical program,
the trusted and candidate prompts, and the trusted and candidate translators.
The mounted run has the declared condition and config and contains this
problem. The task's stage agrees with the result and invocation records.

The embedded `audit-input.manifest` is an enriched view rather than literal
JSON equality with `/task.json`: it contains a `config` field absent from the
mounted task record. This does not alter the problem, stage, condition, or
input hashes; the mounted task's exact hash is correct. It is not a missing or
mutated provenance artifact.

Candidate input integrity passes:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`;
- neither the candidate nor trusted semantics tree contains a symlink;
- recursive `diff -qr --no-dereference` reports no missing, additional,
  mistyped, or changed semantics entry; and
- independent type/path/content tree digests of the two semantics trees are
  equal:
  `d487e6421bb2645e44a09c1f94cab57e265a58beec6d413a0715477e2c245703`.

The candidate's required proof sources—`solution.py`, `solution.mpy`,
`verification.k`, and `spec.k`—are present and regular. There is no audit
infrastructure breach.

Evidence: `evidence/01_integrity_checks.sh`,
`evidence/01_integrity_checks.log`,
`evidence/01_trace_inspection.py`, and
`evidence/01_trace_inspection.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and source comparison

The trusted prompt asks `is_prime(n)` to return true exactly when the given
integer is prime, and false otherwise. Its examples include the boundary
`1`, composites `4` and `6`, and primes `11`, `61`, `101`, and `13441`.
The canonical implementation returns false below two and otherwise searches
integer divisors.

The submitted implementation also returns false below two. For `n >= 2`, it
initializes `divisor = 2` and `result = True`, checks every divisor while
`divisor < n`, sets `result = False` when a divisor is found, increments by
one, and returns the accumulator. It differs operationally from the canonical
implementation by not returning early and by checking through `n - 1`, but
those differences do not change the Boolean result. The extra `n - 1` check
cannot divide an integer `n > 2`; the small cases `2` and `3` are also
handled correctly.

The intended domain is mathematical integers. A scalar integer input has no
valid “empty collection” case. Python values such as strings or floats are not
part of the primality contract, and the canonical implementation itself uses
integer `range`. Python's `bool` subclassing is not treated as a separate
mathematical primality domain.

### Trusted translation

I copied sources to `/tmp/audit-work/prime31` and regenerated with:

```text
python3 /reference/py2mpy.py /tmp/audit-work/prime31/solution.py
```

The command exited 0. The regenerated and submitted MPY files are byte
identical and share SHA-256
`7988144e47963a7e330eba1089c31a8c0b0244228b7e56bd8c891814e9335db2`.

### Independent differential test

The reviewer-authored test imports the trusted canonical function and the
generated Python function using separate module loaders. It also uses an
independently written square-root trial-division oracle. It covers:

- every documented example;
- negative, zero, one, two, three, and both sides of each control boundary;
- early and late composites and representative primes;
- every integer from `-50` through `600`;
- a large negative boundary; and
- 200 deterministic generated values from `-500` through `3000`.

There were 829 distinct inputs and zero mismatches:

```text
input_count=829
mismatches_json=[]
RESULT=PASS
```

The complete input list is preserved in the log.

Evidence: `evidence/02_fidelity.sh`, `evidence/02_fidelity.log`, and
`evidence/02_differential.py`.

## 3. Clean proof reconstruction

I ignored `/candidate/runtime-kompiled`,
`/candidate/verification-kompiled`, and every candidate cache. The scratch
tree contains only copied source inputs and reviewer-generated definitions.
The available `kompile`, `krun`, `kast`, and `kprove` are K v7.1.293
(`evidence/03_tool_versions.log`).

### Fresh concrete definition

The LLVM command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

It exited 0. A reviewer-authored MPY driver then ran with `krun` and exited 0.
For inputs `[-7, 0, 1, 2, 3, 4, 6, 9, 11, 25, 31, 61, 101, 997]`,
Python and K produced the same sequence:

```text
[False, False, False, True, True, False, False,
 False, True, False, True, True, True, True]
```

The K final configuration has an empty computation, no exception, exit code
zero, restored module environment, and exactly this Boolean list in the heap.

### Fresh proof definition and positive claims

The Haskell command was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

It exited 0. The positive target run was:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`. This run checks both positive claims:
`SPEC.prime-loop` and its dependent entry theorem `SPEC.is-prime`.
I also selected the loop claim independently:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC --claims SPEC.prime-loop
```

That command also exited 0 and printed `#Top`.

For completeness, I diagnosed `--claims SPEC.is-prime` by itself. That selector
removes the auxiliary circularity required by the unbounded symbolic loop, so
the prover continued unrolling until reviewer interruption. This is not a
failed target claim; it is the expected consequence of filtering out the
claim's proof dependency. The diagnostic and SIGINT status are documented in
`evidence/03_filtered_entry_diagnostic.md`. The clean all-claims target and
isolated helper runs were repeated by `evidence/03_positive_proofs.sh`, which
exited 0 with `RESULT=PASS`.

Compiler warnings concern unused variables in unrelated supplied string rules
and unchanged framed variables in the loop claim. They do not change either
success signal.

Evidence: `evidence/03_clean_rebuild.sh`,
`evidence/03_clean_rebuild.log`, `evidence/03_kompile_llvm.log`,
`evidence/03_krun_concrete.log`, `evidence/03_kompile_haskell.log`,
`evidence/03_positive_proofs.log`,
`evidence/03_positive_all.log`, and
`evidence/03_positive_prime_loop.log`.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.prime-loop` starts at the fixed semantics' real internal `#while`
configuration. Its precondition says:

- `n` is the integer `N`;
- `divisor` is `D`;
- `result` is the Boolean accumulator `A`;
- `2 <= D <= N`;
- the current environment is the callee frame;
- the module and local scopes have the real parent relationship;
- the heap is empty;
- there is exactly one caller frame;
- return/exception/exit state is normal; and
- the active condition and body are exactly those of the submitted loop.

It consumes the loop, changes `divisor` from `D` to `N`, and changes `result`
from `A` to `A andBool primeScan(N,D)`, while preserving the framed K suffix,
module scope, heap, allocation counters, caller frame, return state, exception
state, and exit code.

`SPEC.is-prime` starts from a clean module-call state with arbitrary K integer
`N`. Scope zero binds `is_prime` to a closure with one parameter `n`, defining
scope zero, and the full submitted body. The claim executes:

```text
Call(Name("is_prime"), (Int(N), .Exprs))
```

and constrains the returned Boolean `?R` by:

```text
ensures ?R ==Bool primeResult(N)
```

Thus `?R` is existential only as an observed execution result; it is not free
in the theorem.

Both preconditions are satisfiable. The exact entry state with `N = 31`
satisfies the entry claim. During the call at `N = 4`, after the two
initializations, the real machine state has `D = 2`, `A = true`, an empty heap,
callee environment 1, the module closure map, and the frame pushed by
`semantics/call.k`; it satisfies the loop claim.

### Constructor-level identity

`evidence/04_program_pinning.py` uses the fresh K parser rather than textual
guessing. It:

1. parses the trusted-regenerated `solution.mpy`;
2. extracts the sole `FuncDef`, parameter list, and body KAST;
3. extracts and parses the closure body embedded in `SPEC.is-prime`;
4. compares those constructor trees; and
5. independently compares the submitted `While` condition/body with the
   helper claim's `#while` condition/body.

The result was:

```text
function_name=is_prime
params_constructor_equal=True
body_constructor_equal=True
loop_condition_constructor_equal=True
loop_body_constructor_equal=True
entry_call_exact=True
RESULT=PASS
```

The common body KAST hash is
`b9adedfd8f30d817a430c453dbd4d6840d6f009ec89db382133f70f87d0c54db`.
This establishes the allowed constructor-level source-to-claim connection;
there is no substituted function body or omitted material operation.

The claim is manually embedded rather than automatically regenerated from the
source. That is an artifact-maintenance observation, not an adequacy failure
for this immutable candidate, because trusted regeneration and mechanical
comparison both pass.

### Ground substitutions and body sensitivity

Ground substitution gives:

- `primeResult(-7) = false`;
- `primeResult(2) = true`;
- `primeResult(4) = false`; and
- `primeResult(31) = true`.

These values agree with both Python implementations. The reviewer also checked
reachable loop states `(N,D,A) = (2,2,true)`, `(4,2,true)`, `(5,3,true)`, and
`(6,3,false)` against `A and primeScan(N,D)`.

The body-sensitivity mutation changes the actual closure term executed by the
claim: `result` is initialized to `false` instead of `true`. At the satisfying
witness `N = 2`, the loop is skipped but the original property requires
`primeResult(2) = true`. The mutation dry-run exited 0; proof exited 1 with
`WarnStuckClaimState` and final `<k> false ~> .K`. This demonstrates dependence
on the program body, not merely an external source filename.

Evidence: `evidence/04_program_pinning.py`,
`evidence/04_program_pinning.log`,
`evidence/04_ground_substitution.py`,
`evidence/04_ground_substitution.log`,
`evidence/04_body_sensitivity_mutation.k`,
`evidence/04_body_sensitivity.log`, and
`evidence/04_body_sensitivity_kprove.log`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.md` enumerates every declaration block in the
fresh supplied semantics, `verification.k`, and `spec.k`, with exact source
location, complete normalized text, attributes, semantic role, and
current-theorem audit disposition. Counts are:

- 1 configuration;
- 228 syntax declarations;
- 5 contexts;
- 701 rules;
- 2 claims;
- 147 function declarations;
- 108 `total` declarations;
- 0 `functional` declarations;
- 25 opaque/symbol declarations;
- 45 priority-bearing rules;
- 35 concrete rules;
- 0 simplification rules; and
- 6 proof-local equations.

This is the exhaustive inventory required by the prompt. Entries not reachable
from this submitted program are marked as current-theorem inactive, not
asserted to be a complete model of all Python. I found no false-conclusion
witness on any satisfying integer input for an inactive rule, so I do not
mislabel those rules as unsound under the prompt's witness requirement.

### Used construct map

| Program construct | Declaration and execution rules | Audit result |
|---|---|---|
| `Call(Name("is_prime"), Int(N))` | `syntax.k` Call/Name/Int; `core.k` lookup and left-to-right argument loop; `call.k` generic call and closure frame rule | Exact binding selected; argument evaluated and bound; no call interception matches |
| `If` and early `Return` | strict `If`; `controls.k` `#branch`; `functions.k` abrupt return and frame pop | Correct truth test, suffix discard on return, and caller-state restoration |
| `Assign` and `Name` | strict assignment; `controls.k` scope update; `core.k` lookup | Writes and reads exact callee scope; no closure-cell or heap-ref priority rule applies |
| `While` | `controls.k` `While => #while`, condition, body, `#loopLbl` recurrence, and exit | Correct re-evaluation, sequencing, continuation preservation, and loop exit |
| integer `<` and `==` | comparison contexts and `applyCmp` dispatch; `int.k` comparison equations | Exact Python/K integer comparisons |
| integer `%` and `+` | sequential binary evaluation; `int.k` `applyBin`, `pyMod`, and addition | Exact for the positive divisors `D >= 2`; division-by-zero cases are unreachable and not assumed |
| Boolean literals/results | `core.k` literal and `truthy(Bool)` rules | Exact branch values and returned sort |

The entry state's empty heap and plain scopes rule out all ref-dereference,
closure-cell, collection, and allocation priority rules. The callee is
syntactically `Name("is_prime")`, so math and MD5 call interceptors do not
match. The 45 numeric priority rules therefore cannot preempt any material
step. The generic call's `[owise]` rule is selected only after those disjoint
patterns fail.

The call rule pushes the only frame, creates local scope 1 with parent 0, and
increments `scopeLoc`. Parameter binding writes `n`; assignments add
`divisor` and `result`; the loop touches only those bindings. Return stores the
Boolean, pops the frame, removes local scope 1, restores environment and
`scopeLoc`, empties the stack, and resets return state. No operation can alter
heap, exception, or exit code on this path. This matches every cell fixed or
framed by the claims.

### Proof-local extensions

`verification.k` has no operational bridge. No rule matches a Python call,
expression, statement, loop, continuation, scope, or configuration.

`primeScan(Int,Int)` is a definitional mathematical summary:

1. `D < 2` totalizes the helper to false outside the proof-relevant domain.
2. `D >= 2 and D >= N` returns true for the empty interval `[D,N)`.
3. `2 <= D < N` with zero remainder returns false.
4. `2 <= D < N` with nonzero remainder recurs at `D + 1`.

The guards are exhaustive and pairwise disjoint over K integers. Every
remainder call has nonzero positive divisor. The recursive case strictly
decreases the natural measure `N - D`. The `D < 2` definition is never reached
from `primeResult` or the loop invariant and does not assert an operational
Python fact.

`primeResult(Int)` splits exhaustively and disjointly at `N < 2` / `N >= 2`.
It is the postcondition definition, not a shortcut: the fixed program executes
first, and the entry proof must connect the observed return to this function.

`SPEC.prime-loop` is the derived circularity that establishes that connection.
It accepts an arbitrary K suffix and caller frame, and its theorem quantifies
over exactly that context. It does not generalize a narrow connection theorem
into an operational rule. The loop contains no return, break, exception,
allocation, output, or other abrupt effect that could make suffix framing
unsound.

There are no proof-local opaque symbols, trusted primitives, priority rules,
`[concrete]` rules, or simplification axioms. The definitions encode the
requested mathematical property, but they do not encode the program's answer
as an execution rewrite; actual name lookup, calls, arithmetic, branches,
assignments, every loop iteration, return, and frame pop remain under the
supplied semantics.

### Supplied opaque and subset boundaries

The imported supplied semantics contains 25 opaque/symbol declarations:

`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`,
`powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`,
`roundF`, `roundFN`, and `sqrtF`.

None occurs in the submitted MPY body, an active semantic rule, a proof-local
definition, a branch condition, a state update, or a postcondition. The proof
is therefore interpretation-parametric with respect to every one of them.
Likewise, supplied totalizations for unused collections, indexing, strings,
dicts, and sorting cannot introduce a value into this theorem. This is an
acceptable inactive language trust boundary, not a program-derived oracle.

Evidence: `evidence/05_rule_inventory.py`,
`evidence/05_rule_inventory.md`, and
`evidence/05_attribute_scan.log`.

## 6. Fresh non-vacuity test

I did not rely on `/candidate/spec-vacuity.k`. The reviewer-authored
`evidence/06_false_result_mutation.k` calls the exact original closure at
`N = 31` but changes the result-constraining obligation to:

```text
ensures ?R ==Bool false
```

The state is satisfiable. Trusted canonical Python and generated Python both
return `True` at `31`.

The build-only command was:

```text
kprove audit-false-result.k \
  --definition reviewer-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT --dry-run
```

It exited 0. The proof command without `--dry-run` exited 1. It failed for the
expected reason:

```text
WarnStuckClaimState
The configuration's term unifies with the destination's term, but the
implication check between the conditions has failed.
...
<k> true ~> .K </k>
```

This is a reachable final state and an unmet false result obligation—not a
parser failure, timeout, missing import, or unrelated crash.

Evidence: `evidence/06_nonvacuity.sh`,
`evidence/06_nonvacuity.log`,
`evidence/06_false_dry_run.log`, and
`evidence/06_false_kprove.log`.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the exact supplied MPY semantics and proof-local mathematical
definitions, for every K integer `N`, if the submitted `is_prime` call reaches
its terminal state, its returned Boolean equals:

```text
false                    when N < 2
primeScan(N,2)           when N >= 2
```

For `N >= 2`, `primeScan(N,2)` is true exactly when no integer in `[2,N)`
divides `N`. The K proof establishes this result while executing the exact
submitted closure and preserving/restoring the claimed state cells.

### Trust and informal boundaries

- **Supplied MPY semantics.** Its candidate copy is byte/type identical to the
  trusted tree. I statically checked every active rule and concretely compared
  14 normal/boundary executions. It is trusted as the language model outside
  the proof-local theorem.
- **Trusted translator.** The candidate translator is byte-identical to the
  trusted translator, regeneration is byte-identical, and the claim/MPY body
  comparison is constructor-level. The broader assertion that this translator
  correctly maps the covered Python subset remains a trusted bridge, supported
  by the differential and concrete tests.
- **K primitives.** The proof relies on K's mathematical integer/Boolean
  operations (`+Int`, `<Int`, equality/inequality, `%Int`, Boolean
  connectives), Map/List operations, K equality, rewriting engine, Haskell
  backend, and SMT reasoning. These are standard toolchain trust.
- **Opaque supplied symbols.** All 25 are listed in Stage 5. They have no
  dependents in this program or theorem.
- **Proof-local summaries.** `primeScan` and `primeResult` are not assumptions:
  their equations are explicit, total on all used domains, disjoint, and
  terminating. The loop reachability claim machine-checks the connection from
  fixed execution to those summaries.
- **Primality meaning.** The equivalence between “`N >= 2` and no divisor in
  `[2,N)`” and ordinary integer primality is elementary mathematics stated
  informally rather than a separate K theorem. It introduces no material
  domain or behavior gap.
- **Termination.** The formal result is partial correctness. Termination is not
  a reachability conclusion claimed here. Informally, inputs below two return
  immediately; for `N >= 2`, `divisor` starts at two, increases by one, and the
  natural variant `N - divisor` reaches zero.
- **Finite tests.** The 829-input Python differential and 14-input K concrete
  run support fidelity and the semantics/translator bridge only. They are not
  used as substitutes for the universal K proof.

Gate A passes: the real body executes, there is no operational bridge, the
result is constrained, and independent body/result mutations are rejected.
Gate B passes: all intended mathematical integers are covered, and the
postcondition is exactly the primality criterion. Gate C passes: assumptions,
commands, inputs, statuses, outputs, and reviewer artifacts are preserved.
There is no material adequacy or soundness gap requiring a concern or failure.

VERDICT: PASS
LEGITIMACY: LEGIT
