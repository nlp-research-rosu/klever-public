# Independent adversarial review: 59-largest-prime-factor

## Decision

The candidate contains a legitimate partial-correctness proof of the submitted
program, but not a fully self-contained K proof of the natural-language
largest-prime-factor characterization. Fresh builds and both positive claims
close; the proof is non-vacuous; the program term is exact; and no proof-local
rule was found to enable a false conclusion on the intended domain.

The limitations supporting `CONCERNS` are:

1. the mathematical bridge from `lpfSpec(N, 2)` to “the largest prime factor of
   composite `N`” is an informal argument supported by finite differential
   testing, not a K theorem;
2. the five operational accelerator rules are directly derivable from the
   supplied rules on their match domains, but the candidate provides no
   bridge-free universal connection claims;
3. the final result theorem is split between an administrative entry claim and
   an exactly matching result-bearing loop claim rather than stated as one
   combined entry-to-result claim; and
4. all requested generation-provenance files are absent.

These are auditability and intent-bridge limitations. They are not witnessed
semantic contradictions, result oracles, substituted execution, or vacuity.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount exists as a regular directory, so there
is no mode/mount infrastructure contradiction.

`/candidate/reference-semantics` contains 24 regular files under the same two
directories as the trusted tree, contains no symlink, and has no missing or
additional entry. A recursive no-dereference diff exits 0. The candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted counterparts.
See `evidence/stage1_integrity.log`.

The following requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace is present. There is also no candidate `PROOF.md` or
candidate vacuity artifact. The root contains an untrusted `__pycache__`, which
was ignored, and no candidate-built definition was copied or reused. These
absences limit provenance review but do not contradict the supplied-semantics
mount.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical program specify: for an integer `n > 1` that
is composite, return its largest prime factor. The examples are
`13195 -> 29` and `2048 -> 2`.

The submitted `solution.py` uses increasing trial division. It repeatedly
divides the current residual by the current factor when divisible and otherwise
increments the factor; it returns the factor when the residual is no greater
than it.

Trusted retranslation was performed from the scratch copy:

```text
python3 trusted/py2mpy.py candidate-src/solution.py > regenerated-solution.mpy
```

It exits 0, and `cmp` against the submitted `solution.mpy` exits 0. Both files
have SHA-256
`04b02d758323fc3c09e54fb1baa77273f697e186215cfb9d06ab51385e1a74db`.

The reviewer-authored `evidence/differential_test.py` separately imports the
trusted canonical source and scratch candidate source. It checks:

- both documented examples;
- composite boundary/branch cases `4, 6, 8, 9, 12, 15, 25, 49`;
- every composite from 4 through 500; and
- a deterministic generated set of products up to 9500.

There are 529 distinct intended-domain inputs and zero mismatches. Scalar input
has no meaningful empty case; `0` and `1` were tested as out-of-contract
robustness observations and differ (`candidate=2`, `canonical=1`). Inputs 2, 3,
5, and 7 agree but are also outside the stated composite domain. The full input
list and results are in `evidence/stage2_program_fidelity.log`.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/review-59/candidate-src`. No compiled definition, cache, or
candidate `pyc` was copied.

Toolchain evidence is in `evidence/toolchain.log`: K v7.1.337 and Python
3.10.12.

Fresh concrete definition:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. The non-exhaustiveness warnings concern unused float, string, subscript,
and builtin domains. The fresh trusted-translation concrete assertion program
then exits 0 under `krun`, with `.K`, `NoExc`, and exit code 0. See
`evidence/stage3_kompile_llvm.log` and
`evidence/stage3_krun_concrete.log`.

Fresh proof definition:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0. Each positive claim was then selected and run independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.lpf-loop
#Top
exit=0

kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.largest-prime-factor-entry
#Top
exit=0
```

The complete two-claim run also prints `#Top` and exits 0. Exact bounded logs
are `evidence/stage3_kprove_lpf_loop.log`,
`evidence/stage3_kprove_entry.log`, and
`evidence/stage3_kprove_all.log`.

## 4. Adequacy and real-program pinning

### Entry claim

`spec.k:35` has precondition `N > 1` with the default module/builtin scopes,
empty heap and stack, `NoExc`, and exit code 0. Its postcondition says that:

- the exact module has been loaded;
- `largest_prime_factor` resolves to the exact submitted function body;
- a call frame at location 1 binds `n` to `N` and `factor` to 2; and
- execution has reached the real `while` head followed by the real
  `Return(Name("factor"))` and `#endcall`.

This claim is an administrative prefix theorem, not by itself a returned-value
theorem.

### Loop claim

`spec.k:8` assumes a current residual `N > 1`, factor `F > 1`, a fresh positive
callee location `L`, the exact real loop body and return continuation, and a
matching call frame. It states that execution finishes the loop, evaluates the
return, pops the callee, restores the caller environment/scope location, and
places exactly `lpfSpec(N, F)` before the saved caller continuation.

The entry post-state exactly instantiates the loop pre-state with `F=2`,
`L=1`, `CALLER=0`, and `CONT=.K`. Thus standard transitivity of reachability
gives a composed entry result `lpfSpec(N, 2)`. The absence of a single explicit
combined claim is a presentation/evidence concern, not a free-result gap:
`lpfSpec` is functional and its three guarded equations fix the result throughout
the proof domain.

### Real-program identity

`verification.k:16-27` expands `solutionModule` to the same constructor tree as
the byte-checked `solution.mpy`. `lpfCondition` and `lpfStep` expand to the exact
condition and body at `solution.mpy:4-9`. No alternate function or uninterpreted
program result is invoked.

### Satisfiable witnesses and ground substitutions

For the entry claim, choose `N=12` and the literal default configuration shown
in the claim. For the loop claim, use the entry post-state: `N=12`, `F=2`,
`L=1`, caller 0, continuation `.K`, a scope remainder whose keys are 0 and -1,
and the singleton saved frame. All preconditions hold, and the expected result
is 3.

Reviewer ground checks also use 2048 and 13195. The recurrence, trusted
canonical Python, and submitted Python respectively produce:

```text
12:    3, 3, 3
2048:  2, 2, 2
13195: 29, 29, 29
```

Configuration-form ground K claims print `#Top`; the independent Python
comparison has zero mismatches. See
`evidence/stage4_ground_instances.log`. An earlier bare-functional-claim attempt
was rejected by the backend as unsupported and is preserved separately in
`evidence/stage4_ground_instances_attempt_functional.log`; it is not used as
evidence.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.tsv`, generated by
`evidence/k_inventory.py`, inventories every top-level local configuration,
syntax declaration, context, rule, and claim in the supplied semantics,
`verification.k`, and `spec.k`. It contains 946 items:

- 1 configuration
- 231 syntax declarations
- 5 evaluation contexts
- 707 rules
- 2 claims

It records source location, attributes, program relevance, disposition, guards,
cells, and the folded declaration text. It includes 146 function-bearing
declarations, 108 `total` declarations, no `functional` declaration, 25 symbol
declarations, 22 `no-evaluators` declarations, 50 priority rules, 35 concrete
rules, 26 `owise` rules, 7 macro declarations, one macro-rec declaration, and
the one proof-local simplification. The category run is preserved in
`evidence/stage5_inventory.log`.

All opaque/no-evaluator symbols occur in supplied float, sort, or MD5 support
unused by `solution.mpy`. They cannot affect this proof's value, control, state,
or postcondition. The remaining unused supplied rules implement other
constructs and are inert for this constructor tree; none refers to this task,
`largest_prime_factor`, or `lpfSpec`.

### Used construct mapping

| Submitted construct | Declaration and fixed behavior |
|---|---|
| `Module`, `Stmts` | `syntax.k:56-61`; `core.k:124-127` loads and sequences statements |
| `FuncDef`, `Params`, call | `syntax.k:53-60`; `functions.k:14-16`; `call.k:20-21,69-75` resolves, evaluates arguments, allocates a frame, and binds `n` |
| `Name`, `Int` | `syntax.k:9-13`; `core.k:130-154,194` performs current/parent lookup and literal evaluation |
| `Assign`, `AugAssign` | `syntax.k:41-45`; `controls.k:9-31` evaluates the RHS then updates the current scope |
| `While`, `If` | `syntax.k:46-49`; `controls.k:51-54,65-85` evaluates guards, selects the branch, and returns to the loop head |
| `BinOp`, `Compare`, `CmpOp` | `syntax.k:14-16,30-32`; `operators.k:12-17`; `int.k:9-26` supplies `+`, `%`, `//`, `>`, and `==` |
| `Return` | `syntax.k:50`; `functions.k:78-90` evaluates the expression, records it, pops the frame, restores the caller, and deallocates the callee scope |

The configuration cells are `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`,
`<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`. The program performs
no heap allocation. Strictness/contexts enforce RHS, comparison, guard, and
return-expression evaluation before their consumers. The call/return rules
preserve the caller continuation and restore its environment. The proof claims
pin the initially empty heap, no exception, and exit code 0; omitted cells in
the loop claim are framed unchanged.

### Proof-local extension inventory

| Extension | Classification and disposition |
|---|---|
| `verification.k:9-11` map-delete simplification | True identity: deleting the unique `L` entry from `(L |-> V) M`, guarded by `L` absent from `M`, yields `M`. This is exactly the symbolic form needed by `#pop`. |
| `solutionModule`, `lpfCondition`, `lpfStep` macros | Exact aliases for the byte-checked submitted program; they add no behavior. |
| `lpfSpec` and its three equations | Definitional summary. On `N>1,F>1`, guards partition `N<=F`, divisible `N>F`, and non-divisible `N>F`. Recursive steps reproduce the real loop update and preserve positive `N,F`. |
| condition accelerator at `verification.k:58` | Direct current-frame lookup of integer `n` and `factor`, followed by the supplied integer `>` comparison. It reads no other cell and preserves the continuation. |
| modulus-test accelerator at `verification.k:72` | Direct lookups, supplied `pyMod`, and supplied integer equality. On the claim domain `F>1`, modulo is defined. |
| division-assignment accelerator at `verification.k:88` | Exact supplied evaluation of `n // factor` as `(N-pyMod(N,F))/F`, followed by the same current-scope update. Other bindings and cells are preserved. |
| increment accelerator at `verification.k:104` | Exact supplied `factor += 1` update for an integer binding. |
| return accelerator at `verification.k:119` | Direct lookup of integer `factor`, the same `retV(F)` update, and the same `#pop` control effect as `functions.k:78-90`. The fixed return semantics intentionally discards the remainder of the callee body while `#pop` restores the saved caller continuation. |

For all five accelerators, the current environment and current scope are
explicitly matched, both bindings are concrete `Int` values where relevant,
and all framed cells remain unchanged. Their guards and RHSs are pairwise
consistent with the exact supplied rules; priority only selects the equivalent
short path.

The candidate does not include bridge-free universal connection claims. That is
a validation-evidence gap. It is not labeled unsound because direct symbolic
expansion establishes the same binding, evaluation, state, and control
transition, and no false conclusion witness was found. As additional finite
evidence, the fixed LLVM definition and bridge-enabled Haskell definition
produce byte-identical final configurations for the six concrete assertion
cases; see `evidence/stage5_bridge_compare.log`.

`lpfSpec` is marked `total` over all integer pairs even though the equations
are only operationally useful with a nonzero positive factor. Every proof use
starts at `F>1`, and both recursive branches preserve it. No false equality
outside that domain was used or observed; the broader declaration is therefore
an unused scope limitation rather than an unsoundness witness.

No rule was classified as materially unsound. Consequently there is no claimed
unsound rule for which a false-conclusion witness is owed.

## 6. Fresh non-vacuity test

The reviewer-authored `evidence/spec-vacuity.k` changes the loop result from
`lpfSpec(N,F)` to `lpfSpec(N,F) + 1`. The precondition is satisfiable, for
example by `N=12`, `F=2`, `L=1`, and the concrete entry post-state; the real and
claimed unmutated result is 3 while the mutation demands 4.

The mutation is byte-identical to the scratch artifact. Its dry run exits 0,
establishing that it parses and builds. The actual proof exits 1 with
`WarnStuckClaimState` and the expected unmet implication:

```text
F #Equals F +Int 1
```

The backend reports that the configuration cannot be rewritten further. The
review harness exits 0 only because this exact proof failure and marker were
observed. See `evidence/stage6_nonvacuity.log`. A first run with an
over-escaped reviewer marker is preserved as
`evidence/stage6_nonvacuity_attempt_marker.log` and is not relied upon.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics and proof-local extensions:

1. for every K integer `N > 1`, loading the exact submitted module and calling
   `largest_prime_factor(N)` reaches the exact real loop state with
   `n=N` and `factor=2`; and
2. for any real loop state satisfying `N>1` and `F>1`, if execution terminates,
   it returns exactly the recursively defined integer `lpfSpec(N,F)`, pops the
   frame, and restores the caller state described by the claim.

By exact interface matching and reachability transitivity, the submitted call
is partially correct with returned value `lpfSpec(N,2)`.

### Trust and evidence ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 compiler, Haskell prover, LLVM executor, and built-in integer/map/list theories | All machine results | Necessary low-level toolchain trust; versions and fresh commands are recorded. |
| Trusted supplied MPY semantics | Meaning of the constructor program | Required by `SUPPLIED_SEMANTICS`; candidate tree is byte/type identical, and every local item is inventoried. |
| Trusted translator | Python-to-constructor identity | Acceptable: trusted translator was run afresh and gave byte identity. |
| Five proof-local operational accelerators | Symbolic loop closure | Sound by direct rule expansion on their exact domains and supported by ground fixed-versus-extended equality; concerning only because no independent universal K connection claims are supplied. |
| `lpfSpec` mathematical meaning | Natural-language largest-prime-factor conclusion | Informal. Trial division removes every occurrence of smaller divisors before advancing; a composite trial factor cannot divide the remaining residual after its smaller prime factors have been exhausted; termination at `N<=F` therefore leaves the largest prime factor. This argument is not machine-checked in K. |
| Trusted canonical Python plus CPython execution | Differential intent evidence | Finite evidence only: 529 intended-domain inputs, zero mismatches. It does not replace the K reachability proof or a universal number-theory lemma. |
| Requested generation provenance | Audit trail | Missing; no generation trace, metrics, or final generation report can be checked. |

The formal precondition is slightly broader than the prompt because it includes
prime `N>1`; both Python implementations and the recurrence return `N` there.
The requested theorem only needs composite inputs, so this does not weaken or
falsify the intended-domain conclusion.

The proof does not establish total termination, Python behavior for `N<=1`,
behavior for non-integer inputs, or a machine-checked theorem that the recurrence
equals the number-theoretic largest prime factor. Those exclusions and the
missing bridge theorems justify `CONCERNS`, while clean reconstruction,
program identity, result constraint, and non-vacuity justify `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
