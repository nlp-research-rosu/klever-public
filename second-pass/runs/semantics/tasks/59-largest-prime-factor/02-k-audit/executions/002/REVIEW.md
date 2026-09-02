# Independent adversarial review: 59-largest-prime-factor

## Executive conclusion

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program over the full source-contract domain, but the proof
package is not strong enough for an unqualified pass.

Fresh builds close both submitted claims. Trusted regeneration pins the
constructor term to `solution.py`, the entry post-state mechanically matches
the loop claim's pre-state, a body mutation breaks the entry proof, and a fresh
false result mutation is rejected on the expected arithmetic obligation.
Moreover, reviewer-authored bridge-free claims establish all five proof
accelerators on the exact scope shape reachable in the target loop.

There are two non-fatal audit limitations:

1. The priority-40 accelerators in `verification.k` are syntactically broader
   than the exact reachable contexts for which bridge-free connection claims
   were obtained. An attempted theorem over their complete abstract-map match
   domain gets stuck in the supplied semantics' symbolic closure-cell
   branches. No satisfiable false-result witness was found, and fixed and
   extended execution agree on all exercised reachable states, so this is an
   evidence/context-containment gap rather than demonstrated unsoundness.
2. The K postcondition is the fully defined recurrence `lpfSpec(N, 2)`, not a
   formal primality/divisibility predicate. Ordinary number theory shows that
   recurrence equals the largest prime factor on composite `N > 1`, and 4,390
   differential cases support the bridge, but that final intent theorem is
   informal rather than machine-checked in K.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `59-largest-prime-factor`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and all records required by the
declared legacy-selected-stage1 layout:

- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json` (present, so inspected);
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the sole 361-line JSONL trace below
  `/generation-evidence/codex-trace/`.

Historical runtime metrics are not required for this layout and were not
reconstructed. The generation records were treated only as untrusted claims.
The trace is valid JSONL; its event inventory and a bounded extraction of every
tool/message event are preserved in
[02_generation_trace_summary.log](/audit-output/evidence/02_generation_trace_summary.log).

### Hashes, campaign lock, types, and supplied semantics

Independent SHA-256 calculations match the launcher-recorded hashes for the
campaign lock, run/task/result records, generation prompt/metrics/usage/output,
canonical function, trusted prompt, and trusted translator. The
`audit_campaign` object equals `/audit-campaign-lock.json` structurally, and
the lock's actual SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

The candidate prompt and translator are byte-identical to their trusted
mounts. A recursive, no-dereference comparison between
`/candidate/reference-semantics` and
`/reference/reference-semantics` exits 0. Both trees contain the same regular
files and directories, and no candidate semantics entry is a symlink. A
reviewer-defined normalized content-manifest hash is
`06160f82a2076306c4a3074692c5615b898a13fa1c7c888b1dc7cb20944fff1e`
for each semantics tree.

The manifest retains both legacy and current semantics hash forms; their
different values reflect different recorded hash schemes, not different
mounted contents. The recursive file/type comparison is exact.

Evidence:

- [01_integrity.log](/audit-output/evidence/01_integrity.log)
- [01b_tree_hashes.log](/audit-output/evidence/01b_tree_hashes.log)
- [02_generation_trace_summary.py](/audit-output/evidence/02_generation_trace_summary.py)

There is no infrastructure breach, so the candidate audit proceeds to a
verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks:

> For an integer `n > 1` that is not prime, return its largest prime factor.

The documented examples are `13195 -> 29` and `2048 -> 2`. The intended
domain is therefore every composite mathematical integer greater than one;
there is no collection-valued empty case. The smallest boundary value is 4.

The trusted canonical function enumerates divisors and tests primality. The
submitted function instead performs trial division:

1. start `factor = 2`;
2. while `n > factor`, divide `n` by `factor` when divisible;
3. otherwise increment `factor`;
4. return `factor`.

A different algorithm is permitted. On the stated composite domain this
algorithm is extensionally correct.

### Translator identity

I ran:

```text
python3 /reference/py2mpy.py /tmp/audit-work/59-lpf/solution.py \
  > /tmp/audit-work/59-lpf/reviewer-regenerated-solution.mpy
cmp reviewer-regenerated-solution.mpy /candidate/solution.mpy
```

Both commands exit 0. The regenerated and submitted MPY files have the same
SHA-256:
`04b02d758323fc3c09e54fb1baa77273f697e186215cfb9d06ab51385e1a74db`.

### Independent differential test

[03_differential.py](/audit-output/evidence/03_differential.py) imports the
trusted canonical entry point and the submitted Python entry point. Its oracle
is a separately implemented descending search for the greatest prime divisor;
it does not reuse either implementation or the K recurrence.

The input set contains:

- both documented examples;
- explicit branch boundaries 4, 6, 8, 9, 10, 12, 15, 25, 27, and 49;
- every composite integer from 4 through 5,000 (4,330 cases);
- 250 deterministic seeded products of primes;
- 4,390 unique intended-domain inputs in total.

There are zero mismatches among candidate, canonical, and independent oracle.
Exact commands and statuses are in
[03_fidelity.log](/audit-output/evidence/03_fidelity.log).

This establishes program fidelity empirically on the tested set; it is not
used as a substitute for the K proof.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/59-lpf`. Candidate-provided compiled definitions and caches
were not used. The fresh toolchain reports K v7.1.293.

The following fresh commands were run:

| Purpose | Command summary | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0 |
| Concrete assertions | `krun concrete-tests.mpy --definition audit-runtime-kompiled` | exit 0, final `<k> .K </k>`, exit-code cell 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | exit 0 |
| Loop claim only | `kprove ... --claims SPEC.lpf-loop` | exit 0, `#Top` |
| Entry claim only | `kprove ... --claims SPEC.largest-prime-factor-entry` | exit 0, `#Top` |
| All claims | `kprove ... --spec-module SPEC` | exit 0, `#Top` |

The complete bounded outputs are:

- [04_runtime_kompile.log](/audit-output/evidence/04_runtime_kompile.log)
- [04_concrete_krun.log](/audit-output/evidence/04_concrete_krun.log)
- [04_verification_kompile.log](/audit-output/evidence/04_verification_kompile.log)
- [04_kprove_lpf_loop.log](/audit-output/evidence/04_kprove_lpf_loop.log)
- [04_kprove_entry.log](/audit-output/evidence/04_kprove_entry.log)
- [04_kprove_all.log](/audit-output/evidence/04_kprove_all.log)

The compiler's non-exhaustiveness warnings concern unused supplied-semantics
operations such as symbolic float/list helpers. They do not occur in the
submitted program's constructor path and did not prevent any required build or
proof.

Dynamic reconstruction therefore passes. The prior generation `#Top` was not
trusted.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`largest-prime-factor-entry` has precondition `N > 1`. It starts in the exact
empty module configuration, loads `solutionModule`, calls
`largest_prime_factor(N)`, binds the real closure and parameter, executes
`factor = 2`, and reaches the exact loop-head configuration. Its postcondition
does not itself state the returned value.

`lpf-loop` starts at that loop head with:

- current integer values `n = N` and `factor = F`;
- `N > 1`, `F > 1`;
- a fresh callee scope `L >= 1`;
- the real `while` condition and body;
- the real `Return(Name("factor"))` and `#endcall`;
- the caller continuation and frame.

It reaches `lpfSpec(N, F)` in the restored caller continuation, removes the
callee frame, restores the environment and scope allocator, and leaves the
return state as `noRet`.

### Mechanical constructor identity

[06_pinning.py](/audit-output/evidence/06_pinning.py) removes only whitespace
and compares balanced K constructor terms. It establishes:

- `solutionModule` is exactly the trusted regenerated `solution.mpy` module;
- `lpfCondition` is exactly the condition subterm in that module;
- `lpfStep` is exactly the loop-body subterm in that module.

The normalized full module and macro are both 314 characters and are equal.
This is constructor-level pinning, not reliance on the name of a source file.

The entry post-state unifies with the loop claim's pre-state using:

```text
N_loop = N_entry
F = 2
L = 1
SC = the module and builtins scopes with keys {-1, 0}
CALLER = 0
CONT = .K
REST = .List
```

All loop preconditions then follow from the entry precondition. Reachability
transitivity therefore composes the two checked claims into:

```text
load exact module; call largest_prime_factor(N)
  => lpfSpec(N, 2)
```

The candidate does not provide this composition as a single end-to-end
`kprove` claim. The exact state unifier makes the composition valid, but the
absence of the single assembled target is a minor auditability limitation.

### Satisfying states and concrete substitutions

An explicit entry witness is `N = 4` with the exact initial cells stated in
the claim. The corresponding loop witness uses `F = 2`, `L = 1`,
`SC.keys = {-1, 0}`, caller 0, empty continuation, and empty frame tail. Every
precondition is true.

Concrete substitutions agree:

| N | `lpfSpec(N,2)` | trusted canonical | submitted Python |
|---:|---:|---:|---:|
| 4 | 2 | 2 | 2 |
| 2048 | 2 | 2 | 2 |
| 13195 | 29 | 29 | 29 |

These results are recorded in
[06_pinning.log](/audit-output/evidence/06_pinning.log).

### Body sensitivity

The reviewer changed the `AugAssign` inside `solutionModule` from 1 to 2 while
leaving `lpfStep` and the entry target unchanged. This changes the constructor
term actually loaded by the claim. The mutated definition compiles, but the
entry claim exits 1 with `WarnStuckClaimState`; the residual closure visibly
contains `Int(2)` where the target still contains `Int(1)`.

Evidence:

- [06_verification-body-mutation.k](/audit-output/evidence/06_verification-body-mutation.k)
- [06_body_mutation_kprove.log](/audit-output/evidence/06_body_mutation_kprove.log)

### Summary-to-intent bridge

The formal return is constrained to `lpfSpec`, not a fresh symbol. Its three
equations exactly define the same trial-division recurrence. On the reachable
domain `F > 1`, their guards are disjoint and exhaustive:

- return `F` when `N <= F`;
- divide `N` by `F` when `N > F` and divisible;
- otherwise increment `F`.

For completeness, the ordinary number-theory argument that
`lpfSpec(N,2)` is the largest prime factor is:

1. At each loop head, the current `N` has no divisor in `[2,F)`.
2. If `F` divides current `N`, then `F` is prime; otherwise a proper divisor
   of `F` would be a smaller divisor of `N`. Dividing preserves the
   no-smaller-divisor invariant, and the quotient is at least `F`.
3. If `F` does not divide current `N`, incrementing `F` preserves the
   invariant.
4. When `N <= F`, the quotient/lower-bound invariant gives `N = F`. This
   remaining `F` is prime, and all removed prime factors are at most `F`.
   Therefore it is the largest prime factor of the original composite input.

This bridge covers the unrestricted composite domain, but it is not itself
encoded as a K theorem. That is one reason for the concern-level verdict.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[05_rule_inventory.txt](/audit-output/evidence/05_rule_inventory.txt) is a
147,207-byte source-span inventory. It enumerates every module,
configuration, local syntax declaration, context, rule, claim, and relevant
attribute in all 25 supplied K modules plus `verification.k` and `spec.k`.
Totals are:

| Item | Count |
|---|---:|
| Modules | 27 |
| Configuration declarations | 1 |
| Local syntax declarations | 231 |
| Context declarations | 5 |
| Rules | 707 |
| Claims | 2 |
| Function declarations | 147 |
| `total` declarations | 108 |
| `functional` declarations | 0 |
| `no-evaluators` declarations | 22 |
| Symbol declarations | 25 |
| Priority-bearing rules | 50 |
| `owise` rules | 26 |
| Concrete rules | 35 |
| Simplification rules | 1 |
| Circularity claims | 1 |

Of the 707 rules, 695 belong to the byte-identical supplied semantics and 12
are in candidate `verification.k`.

### Supplied-semantics modules

Every inventoried supplied rule was classified. The following module groups
state the decision for all declarations and rules in each named file:

- `semantics.k` and `syntax.k`: assembly/imports and AST constructors. Accepted.
  The submitted MPY uses only declared constructors.
- `core.k`: configuration, module sequencing, literals, name lookup, scopes,
  allocation, argument order, and shared helpers. Accepted on the used path.
  The `<env>`, `<scopes>`, `<scopeLoc>`, `<stack>`, `<ret>`, heap, exception,
  and exit cells used by the claims match this configuration.
- `iter.k`, `range.k`, `str.k`, `set.k`, `list.k`, `tuple.k`,
  `subscript.k`, `dict.k`, `comprehension.k`, `methods.k`, `builtins.k`,
  `sort.k`, `float.k`, and `concrete.k`: reviewed and inert with respect to
  the positive symbolic target except for imported sort/function
  declarations. None of their list/string/dict/range/float/sort/MD5
  constructors is produced by `solution.mpy`. Their opaque values therefore
  cannot affect a branch, result, state cell, or postcondition in this proof.
  `concrete.k` is present only in the LLVM `MPY-KRUN` build.
- `operators.k` and `int.k`: accepted. They implement left-to-right
  evaluation and the used integer `>`, `==`, `+`, `%`, and `//` cases.
  `pyMod(N,F) = ((N %Int F)+F)%Int F` and
  `(N-pyMod(N,F))/Int F` are Python's floor-modulo/floor-division formulas;
  the proof maintains `F > 1`, excluding zero division.
- `bool.k`: its short-circuit rules are unused; the used Boolean values flow
  through `truthy` in `core.k`. Accepted.
- `controls.k`: accepted. Assignment evaluates the RHS before updating the
  current scope; `If` evaluates one guard and selects one branch; `While`
  evaluates the condition on every iteration and installs `#loopLbl`.
- `functions.k` and `call.k`: accepted. Callee and arguments evaluate in
  order, calls allocate and push the exact frame, `Return` discards the
  remaining callee continuation, and `#pop` restores caller state.
- `assert.k`: used only by concrete smoke programs, not by either target
  claim. Its success/failure rules correctly set the modeled exception and
  exit code.

The supplied semantics contains opaque proof-domain primitives:

```text
intFloatDiv, divII, floatMod, floatLt, absF,
floorFI, toF, ceilF,
subF, divF, addF, mulF, powF, gtF, eqF,
decStrToF, divFloatIntV, intToF, truncF, roundF, roundFN, sqrtF,
sortVS, sortKeyVS, md5hexCodes
```

All are inert for this integer-only program. Consequently none is a
result-bearing oracle for the target theorem.

### Used-construct coverage

| Program construct | Declaration and fixed rules | Proof treatment |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k`; `core.k` load/sequence; `functions.k` closure binding | Executes in entry claim |
| `Call`, argument `Int(N)`, parameter binding | `call.k`, `core.k`, `functions.k` | Executes in entry claim |
| `factor = 2` | `controls.k`, integer literal in `core.k` | Executes in entry claim |
| `While` | `controls.k` `#while/#whileCond/#loopLbl` | Circular loop claim |
| `n > factor` | `operators.k`, `int.k`, name lookup in `core.k` | Exact accelerator plus bridge-free connection |
| `n % factor == 0` | `operators.k`, `int.k`/`pyMod` | Exact accelerator plus connection |
| `n = n // factor` | `controls.k`, `int.k` | Exact accelerator plus connection |
| `factor += 1` | `controls.k`, `int.k` | Exact accelerator plus connection |
| `If` | `controls.k` | Fixed branch rules execute |
| `Return(factor)` and call pop | `functions.k`, lookup in `core.k` | Exact accelerator plus connection; fixed `#pop` executes |

No used construct is silently fabricated or left unmodeled.

### Candidate `verification.k` extensions

All 12 rules are accounted for:

1. **Map-deletion simplification.**  
   `((L |-> V) M)[L <- undef] => M` under `L not in_keys(M)`. This is a
   derived Map identity. It only simplifies the fixed `#pop` scope deletion
   and does not invent a return value. Accepted.

2. **Three constructor macros.**  
   `solutionModule`, `lpfCondition`, and `lpfStep` are semantically inert
   abbreviations. Mechanical comparison establishes exact source identity.
   Accepted.

3. **Three `lpfSpec` equations.**  
   This is a definitional summary, not an operational bridge or opaque
   oracle. Its guarded equations are pairwise disjoint and exhaustive for
   every use with `F > 1`. Division decreases `N`; the other recursive branch
   increases `F` toward the base `N <= F`. The unrestricted `[total]`
   declaration leaves values outside the positive-factor use domain
   underspecified (notably `F = 0`), but no target state can reach that
   domain. No intended-domain false conclusion follows.

4. **Five priority-40 operational accelerators.**  
   These cover the two comparisons, floor-division assignment, increment,
   and return. Each reads the current unannotated integer scope, preserves all
   omitted cells, and produces exactly the fixed-semantics value/state
   transition. The return bridge introduces the same abrupt control as
   `functions.k`'s fixed return rule and preserves the saved caller
   continuation through `#pop`.

For the exact reachable scope
`scope(("n"|->N)("factor"|->F), parent(0))`, reviewer-authored claims import
only `MPY`, not `verification.k`, and prove every bridge:

| Connection claim | Result |
|---|---|
| `compare-gt` | exit 0, `#Top` |
| `compare-mod-zero` with `F > 1` | exit 0, `#Top` |
| `assign-floor` with `F > 1` | exit 0, `#Top` |
| `augassign-one` | exit 0, `#Top` |
| `return-factor` with arbitrary callee suffix | exit 0, `#Top` |

See
[08c_bridge-connections-reachable.k](/audit-output/evidence/08c_bridge-connections-reachable.k)
and
[08c_reachable_bridge_connections.log](/audit-output/evidence/08c_reachable_bridge_connections.log).

Fixed semantics and the bridge-enabled proof definition also produce
byte-identical final configurations for inputs 4, 9, 12, and 49 in a program
whose return has both an observable caller continuation and an unreachable
state update immediately after it. See
[07_operational_bridge_checks.log](/audit-output/evidence/07_operational_bridge_checks.log).

The candidate accelerator patterns additionally admit `_REST:Map` and an
arbitrary parent. A bridge-free claim over that full abstract pattern exits 1
on symbolic `$cells` narrowing branches; it does not produce a concrete
counterexample. Concrete maps with integer bindings cannot simultaneously
satisfy the fixed cell-reference guard, so static constructor reasoning still
supports equivalence. Nevertheless, the candidate itself supplies no
complete-match-domain connection theorem, and the reviewer did not obtain
one. This fails the strongest proof-extension auditability requirement but
does not witness an unsound result on the intended domain. The bounded failed
attempt and interruption accounting are in
[08b_bridge_compare-gt.log](/audit-output/evidence/08b_bridge_compare-gt.log)
and
[08_unrestricted_attempt_note.md](/audit-output/evidence/08_unrestricted_attempt_note.md).

### Overlap, priority, totality, and false-witness decision

- The three `lpfSpec` guards do not overlap.
- The five proof accelerators have different leading constructors and do not
  overlap each other.
- Their priority preempts only the corresponding fixed evaluation sequence.
  On every reachable target configuration, the bridge-free claims prove the
  same result and cell footprint.
- The candidate uses no fresh result-bearing opaque symbol.
- No candidate rule encodes a table of task answers, bypasses the real
  function binding/body, or admits an opposite result on a satisfying input.
- No claimed unsound rule is reported because no concrete or satisfiable
  symbolic false-conclusion witness exists. The broader accelerator-domain
  issue is explicitly classified as an evidence gap.

## 6. Fresh non-vacuity test

The candidate supplies no `spec-vacuity.k`; none was trusted. The reviewer
created
[09_spec-vacuity-reviewer.k](/audit-output/evidence/09_spec-vacuity-reviewer.k),
which changes the loop result from `lpfSpec(N,F)` to
`lpfSpec(N,F) +Int 1`.

This is demonstrably false for the satisfying state `N=4`, `F=2`, `L=1`:
the real result is 2 and the mutation demands 3.

Results:

1. `kprove ... --dry-run` exits 0, establishing successful parsing/build.
2. The actual `kprove` exits 1, without timeout.
3. The residual is a genuine implication failure containing
   `F #Equals F +Int 1` and `WarnStuckClaimState`.

Evidence:

- [09_false_mutation_dry_run.log](/audit-output/evidence/09_false_mutation_dry_run.log)
- [09_false_mutation_kprove.log](/audit-output/evidence/09_false_mutation_kprove.log)

The proof is result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### What the checked reachability claims establish

Under the supplied MPY semantics plus the audited proof-local rules, for every
K integer `N > 1`:

1. loading the exact regenerated module and calling its exact
   `largest_prime_factor(N)` body reaches the exact trial-division loop with
   `factor = 2`;
2. if the loop/call terminates from that state, it returns exactly
   `lpfSpec(N,2)` and restores the caller's modeled environment, stack,
   scopes, scope allocator, and return state.

By the number-theory argument above, for every composite `N > 1` this value is
the largest prime factor. Thus the theorem covers the entire documented
source-contract domain. It does not use finitely many examples, a bounded
unrolling, or a narrowed size range as the formal domain.

The proof is partial correctness. It does not separately prove termination,
although the recurrence and concrete behavior strongly indicate it.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| Trusted CPython-AST-to-MPY translator | Source-to-constructor identity | Accepted benchmark boundary; byte identity independently checked |
| Supplied MPY semantics and K built-ins for unbounded integers, Boolean logic, Maps, Lists, and reachability | Every K execution/proof | Accepted selected-semantics boundary; candidate tree is exact |
| K v7.1.293 parser/compiler/Haskell prover/LLVM executor | `#Top` and concrete runs | Standard toolchain trust |
| Map deletion simplification | Loop claim's final `#pop` | Accepted mathematical Map identity |
| Five proof accelerators | Loop claim closure | Exact reachable-domain bridge-free K theorems plus fixed/extended tests; broader match domain remains a documented concern |
| `lpfSpec` equations | Formal returned value | Fully defined on every target use; no opacity |
| `lpfSpec(N,2)` equals largest prime factor | Human-facing contract | Informal number-theory proof plus finite differential support; concerning because not machine-checked |
| Transitive assembly of entry and loop claims | End-to-end result statement | Exact mechanical unifier; not provided as one K claim |
| 25 supplied opaque/symbolic primitives listed in Stage 5 | None | Inert and irrelevant to this theorem |

### Empirical evidence and its limits

- 4,390 Python differential inputs support implementation-to-contract
  agreement only on those inputs.
- Concrete K smoke tests support the translator/semantics execution bridge on
  their finite cases.
- Fixed-versus-extended operational tests support bridge fidelity on four
  ground executions and observable return contexts.
- Body and false-result mutations establish sensitivity and discrimination.

None of these empirical tests substitutes for the reachability claims or the
bridge-free symbolic claims.

### Excluded behavior

- `N <= 1` is outside both the source contract and entry precondition.
- Prime `N > 1` is outside the source contract, although the formal entry
  precondition is broader and the program returns `N`.
- Non-integer Python values and Python implementation details beyond the
  supplied MPY subset are excluded.
- Zero division is unreachable because `factor` starts at 2 and only
  increases or remains positive.
- Termination is not part of the partial-correctness theorem.

### Verdict rationale

The proof is reconstructed, non-vacuous, result-constraining, source-pinned,
and domain-complete. There is no false-rule witness and no material
source-contract narrowing, so rejection as not legitimate would be
unwarranted. An unqualified pass is also unwarranted because the candidate
does not contain complete-match-domain connection theorems for its broad
accelerator rules and leaves the recurrence-to-prime-factor intent theorem
informal. These are material auditability/trust limitations but do not make a
false intended-domain conclusion provable.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
