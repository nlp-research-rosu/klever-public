# Independent adversarial audit: 100-make-a-pile

The candidate program and its generated small-step semantics behave correctly
on the audited inputs, and all five submitted K claims can be freshly made to
print `#Top`. The candidate nevertheless does **not** contain a legitimate
proof of the real generated program. Its entry theorem never executes the
submitted term in `<k>`. Instead, `verification.k` defines a second cell-free
evaluator whose loop has no operational equations, then supplies a
task-specific simplification rule that directly rewrites that loop to the
desired final result. The loop and whole-program claims are consequences of
that trusted rule. A fresh body-sensitivity test changed the small-step
multiplication behavior enough to make `n = 3` return `[5,6,7]`; the unchanged
functional claim still printed `#Top`. This is a decisive real-program pinning
failure.

All candidate material was treated as untrusted evidence. Source execution and
builds used only copies under `/tmp/audit-work/100-make-a-pile`; no
candidate-provided compiled definition or cache was reused. Exact, bounded
command records are under `evidence/logs/`, and reviewer-authored scripts and
mutations are under `evidence/`.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` does not exist. The absence check exited 0, so
there is no infrastructure breach and no hidden/supplied semantics was sought
or used (`evidence/logs/01-integrity.log`).

The following required candidate artifacts are present as regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. One structured generation trace is
present at
`/candidate/codex-trace/2026/07/22/rollout-2026-07-22T06-21-50-019f898f-7d0b-7103-9d04-17f2a2a90f02.jsonl`.
An exhaustive `find -P /candidate -type l` found no symlink. No required
source artifact was missing, mistyped, or symlinked.

The candidate also contains `__pycache__`, four candidate-built `*kompiled`
trees, `kore-exec.tar.gz`, and related caches. These are additional untrusted
generation evidence, not trusted source inputs; all were ignored during
reconstruction. `PROOF.md` and a candidate vacuity spec are absent, but neither
was a required deliverable in the recorded generation request.

Byte comparisons establish:

- `/candidate/prompt.py` equals `/reference/prompt.py`; both have SHA-256
  `bec48d3dcd0c53db5bf1a185da2df8f0b1d58608c9c953c96f090d38e8fb0a98`.
- `/candidate/py2mpy.py` equals `/reference/py2mpy.py`; both have SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The exact comparisons, source hashes, tool paths, and K version
(`v7.1.293`) are in `evidence/logs/01-integrity.log`.

`evidence/inspect_provenance.py` read and structurally validated the two JSON
records, the complete structured trace (282 JSONL records), `codex-last.txt`,
and the complete 22,571-line `codex-output.log`, emitting a bounded summary in
`evidence/logs/02-provenance.log`. As untrusted claims, those records say the
run was the bare/no-supplied-semantics condition, exited 0, built a cell-free
big-step proof layer after cell-based difficulties, and obtained `#Top`. None
of those claims was used in place of reconstruction.

Stage result: integrity passes; no infrastructure error.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every positive integer `n`, return a list of `n` levels. Index `i`
(zero-based) contains `n + 2*i`; equivalently, the list is
`[n, n+2, ..., n+2(n-1)]`. Thus every value has the parity of `n`, and each
level is the next odd number when `n` is odd or the next even number when `n`
is even. The documented example is `make_a_pile(3) == [3,5,7]`.

The trusted canonical implementation at `/reference/canonical.py` is exactly
`[n + 2*i for i in range(n)]`.

The candidate initializes `i = n-1`, repeatedly prepends `n+2*i`, decrements
`i`, and exits after processing `i = 0`. For positive `n`, prepending in
descending-index order yields the canonical ascending-index list. For `n <= 0`
(outside the stated domain) the loop has zero iterations and returns `[]`,
also matching the canonical implementation.

### Translation fidelity

The trusted translator was run on the scratch copy:

```text
python3 reference/py2mpy.py source/solution.py > build/regenerated-solution.mpy
```

The command exited 0. `cmp` also exited 0, and both regenerated and submitted
terms have SHA-256
`40fe8a33eb00f4b494b665af35e35e0da0fd3280a3c345acd004bdaca512136c`
(`evidence/logs/03-translation-identity.log`). The submitted `solution.mpy`
therefore is the trusted translation of the submitted `solution.py`.

### Independent differential testing

`evidence/differential_test.py` independently imports
`/reference/canonical.py:make_a_pile` and
`/candidate/solution.py:make_a_pile`. It covers:

- the documented `n = 3` example;
- `n = -3, -1, 0, 1, 2` as empty/out-of-domain and lower-bound witnesses;
- odd, even, one-iteration, and multi-iteration representatives
  `3, 4, 5, 6, 17, 100, 1000`;
- 36 deterministic generated positive integers in `[1,250]`.

All 49 comparisons matched, and the positive cases also satisfied length,
first-value, step-2, and parity checks. The exact input list and every result
are in `evidence/logs/04-differential.log`; exit status was 0. This is finite
program-fidelity evidence, not a K proof.

Stage result: program and translation fidelity pass.

## 3. Clean proof reconstruction

Only regular source copies in `/tmp/audit-work/100-make-a-pile/source` were
used. Output definitions were newly created beneath
`/tmp/audit-work/100-make-a-pile/build`.

### Fresh concrete semantics

Fresh LLVM compilation used:

```text
timeout 300s kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition ../build/semantic-llvm-kompiled
```

It exited 0 (`evidence/logs/05-build-semantics-llvm.log`). Independent `krun`
commands for `n = -1, 0, 1, 3, 6` all exited 0 with `.K` and results
`[]`, `[]`, `[1]`, `[3,5,7]`, and `[6,8,10,12,14,16]` respectively
(`evidence/logs/06-krun-n-neg1.log` through
`evidence/logs/10-krun-n6.log`).

`evidence/k_python_compare.py` additionally invoked that fresh definition for
`n = -1, 0, 1, 2, 3, 6, 10`, parsed the `<result>` cell, and compared it with
both trusted canonical Python and submitted Python. All seven matched, exit 0
(`evidence/logs/11-k-python-compare.log`). The zero-iteration and
one-or-more-iteration paths together exercise every syntactic construct and
small-step rule used by the submitted term.

### Fresh proof definition and each target claim

Fresh Haskell compilation used:

```text
timeout 300s kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition ../build/verification-haskell-kompiled
```

It exited 0 (`evidence/logs/12-build-verification-haskell.log`). The aggregate
proof and each labeled positive claim were then run independently:

| Claim selection | Exit | Required output | Evidence |
|---|---:|---|---|
| all claims | 0 | `#Top` | `logs/13-kprove-all.log` |
| `SPEC.invariant-initialization` | 0 | `#Top` | `logs/14-kprove-initialization.log` |
| `SPEC.invariant-preservation` | 0 | `#Top` | `logs/15-kprove-preservation.log` |
| `SPEC.invariant-exit` | 0 | `#Top` | `logs/16-kprove-exit.log` |
| `SPEC.loop-invariant` | 0 | `#Top` | `logs/17-kprove-loop.log` |
| `SPEC.functional-correctness` | 0 | `#Top` | `logs/18-kprove-functional.log` |

Every run also emitted `WarnTrivialClaim: Claim proven without rewriting`.
Thus the mechanical reconstruction requirement is met, but the warning is
material: source inspection below shows that definition-time function and
simplification equations normalize each claim to its destination before
reachability reasoning.

Stage result: fresh builds and positive commands pass mechanically. This does
not establish legitimacy.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfying states

| Claim | Precondition | Claimed effect | Ground satisfying witness |
|---|---|---|---|
| initialization | `N > 0` | The first two assignments produce `i=N-1`, preserve `n=N`, and set `result=pileFrom(N,N)=[]`. | `N=1` gives `{i:0,n:1,result:[]}`. |
| preservation | `N>0`, `0 <= I < N` | From accumulator suffix `pileFrom(N,I+1)`, one body execution prepends `N+2I` and decrements `i`, producing `pileFrom(N,I)`. | `N=3,I=1`: `[7]` becomes `[5,7]`, `i` becomes 0. |
| exit | `N > 0` | Returning from invariant state `i=-1,result=pileFrom(N,0)` returns that list unchanged. | `N=1` returns `[1]`. |
| loop invariant | `N>0`, `-1 <= I < N` | Starting with `i=I` and suffix `pileFrom(N,I+1)`, finish the loop and trailing return with `i=-1` and result `pileFrom(N,0)`. | `N=3,I=2` returns `[3,5,7]`. |
| functional correctness | `N > 0` | The exact displayed AST returns `pileFrom(N,0)` and final bindings `i=-1,n=N,result=pileFrom(N,0)`. | `N=3` claims `[3,5,7]`. |

`evidence/claim_witnesses.py` concretely checks all five witnesses and compares
result-bearing ones with both Python implementations; all pass
(`evidence/logs/26-claim-witnesses.log`).

### Pinning failure

No claim contains a K configuration or a `<k>` cell. The functional claim's
source term is:

```text
goal(proof(evalEntry(Module(FuncDef(...exact AST...)), N)))
```

It is not:

```text
<k> Module(FuncDef(...)) => .K </k>
```

and it neither reads `solution.mpy` nor reaches the small-step
`<k>/<env>/<result>` configuration. The embedded AST happens to be textually
identical to the submitted term, as Stage 2 established, but it is evaluated
only by duplicate functions in `verification.k`.

The decisive sensitivity experiment copied the sources, changed only the
small-step multiplication rule from `L *Int R` to `L +Int R`, and freshly
built both definitions. With positive satisfying input `n=3`:

- fresh mutated concrete execution returned `[5,6,7]`, exit 0
  (`evidence/logs/20-sensitivity-krun-n3.log`);
- the unchanged `SPEC.functional-correctness` still printed `#Top`, exit 0,
  and again warned that it was proven without rewriting
  (`evidence/logs/22-sensitivity-kprove-functional.log`).

The mutation is preserved as
`evidence/mutations/semantic-wrong-multiply.k`; its build logs are
`logs/19-sensitivity-build-llvm.log` and
`logs/21-sensitivity-build-proof.log`. This is not an allegation that the
submitted multiplication rule is false. It is an operational-sensitivity
witness showing that the alleged proof is independent of the real operational
behavior it claims to verify.

The returned value is syntactically constrained in the cell-free destination,
and Stage 6 confirms that an off-by-one return is rejected. The defect is
therefore not a free destination variable or an unsatisfiable precondition; it
is the unproved substitution of a second evaluator and a result-installing
loop bridge for actual execution.

Stage result: **fail**. The entry theorem does not pin or execute the real
generated program.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.md` is the exhaustive inventory. It enumerates all 33
local syntax productions/declarations in `semantic.k`, its configuration, all
29 local helper/operational rules, all 10 proof-layer declarations, all 17
proof-layer equations/rules, all five claims, and the submitted-construct
coverage map. The mechanical source scan is
`evidence/logs/27-source-declaration-scan.log`.

### Generated small-step semantics

The local operational model is intentionally narrow but covers every
constructor in `solution.mpy`: module/function loading, one parameter,
statement sequencing, name lookup, integers, empty/singleton lists,
left-to-right `+/-/*`, list concatenation, `>=`, assignment, loop control, and
return. Its state consists of `<k>`, input `<n>`, `<env>`, and `<result>`.

The `vAppend` equations are structurally terminating, disjoint, and exhaustive
over local `Vals`. The guarded `pileFrom` equations are disjoint and exhaustive
over integer `I`, and recursive calls increase `I` toward `N`. Operator rules
are disambiguated by operator tokens and value types. Assignment evaluates its
RHS before map update; while reconstructs the same loop head; return records
the value and discards the remaining top-level continuation. There are no
local priority rules, `total` declarations, or semantic simplification rules.

No materially false candidate small-step rule was found on the submitted
program/domain. The module and return rules are over-broad as a model of full
Python (they assume a sole top-level one-argument function and no call stack),
but those limitations are sound for the exact submitted program. Because no
false conclusion witness was found for them on the intended domain, this
review does not label them unsound.

### Separate proof layer

`verification.k` introduces `evalExpr`, `evalBin`, `evalCmp`, `evalStmts`, and
`evalEntry` as cell-free functions. Their ordinary equations accurately
duplicate the pure target operations, but there is no reachability theorem
connecting any of them to the `<k>` semantics. `evalLoop` is worse: it is a
result-bearing opaque term with no loop-execution equations.

The sole rule that handles it is
`verification.k:47-65`:

```text
proof(evalLoop(exact condition, exact body, exact return, invariant map))
  => proof(Returned(exact desired final map, pileFrom(N,0)))
```

under the invariant guard, with `[simplification]`. This is a task-specific
operational/result bridge and correctness axiom. It directly installs the
postcondition without executing the real `While` rules or even a big-step loop.
The initialization, preservation, and exit claims do not occur as premises and
are not machine-checked derivations of the simplification rule. The loop claim
is closed by the very rule whose truth it should establish; the functional
claim reduces to that same rule after cell-free assignment equations.

The bridge is exactly scoped to the target loop syntax and its mathematical
conclusion happens to be true for the unmodified submitted program. Therefore,
consistent with the required witness discipline, this review does **not**
assert that the guarded equation has a ground false case for the unmodified
program. The narrower but decisive defect is that its truth is assumed as a
trusted simplification, not proved from the selected operational semantics.
The positive-`n=3` sensitivity witness above exhibits the false conclusion the
bridge can enable when the imported operational behavior differs:
operational `[5,6,7]` versus proved `[3,5,7]`.

The exact AST and narrow bridge context prevent an arbitrary-continuation bug,
and no fresh unconstrained oracle value is introduced. Those facts do not cure
the missing universal connection theorem or the direct encoding of the task's
answer.

Stage result: the generated small-step semantics is adequate for this term,
but the proof extension is illegitimate and execution-bypassing.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied on. The reviewer created
`evidence/mutations/spec-vacuity.k`, which keeps the exact functional entry and
final environment but falsely changes the returned value from
`pileFrom(N,0)` to `pileFrom(N,1)`.

The precondition is satisfiable and the mutation is genuinely false:
for `N=1`, `N>0`, the real result is `[1]` while the mutated result is `[]`
(`evidence/logs/23-vacuity-witness-n1.log`).

Compilation/proof parsing succeeded:

```text
kprove spec-vacuity.k --definition ../build/verification-haskell-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0 (`evidence/logs/24-vacuity-dry-run.log`). The real mutation run exited
1 with `WarnStuckClaimState`; its residual explicitly compares
`VCons(VInt(N),pileFrom(N,1))` with `pileFrom(N,1)` in the returned value
(`evidence/logs/25-vacuity-proof.log`). This is the expected unmet result
obligation, not a parser error, timeout, or unrelated crash.

Stage result: the cell-free theorem is result-constraining and passes this
local non-vacuity test. This does not repair the Stage 4/5 real-execution gap.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the compiled theory that already includes the task-specific
`proof(evalLoop(...))` simplification, K establishes that the exact embedded
AST's *cell-free duplicate evaluator* normalizes to the displayed
`Returned(...pileFrom(N,0)...)` term for `N>0`. The three local
initialization/preservation/exit equations also normalize as claimed. The
fresh false-return mutation shows that this extended-theory result is not a
tautology with an unconstrained return.

It does not establish a reachability theorem from the submitted program in
`<k>` to its final `<result>` cell. It does not establish that the duplicate
evaluator is equivalent to `semantic.k`, and it does not derive the loop
summary from the operational loop.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293 frontend, Haskell/LLVM backends, reachability engine | All compilation, concrete runs, and proofs | Ordinary tool trust; fresh builds reduce candidate-cache risk. |
| Imported K `INT`, `BOOL`, `MAP`, `STRING`, generated lists, and K sequencing | Arithmetic, comparison, environment, values, control | Acceptable low-level primitives. K arbitrary-precision `Int` aligns with Python integers on this task. |
| Trusted `/reference/py2mpy.py` | Link from `solution.py` to `solution.mpy` | Acceptable and byte-checked. |
| Trusted canonical Python plus natural-language interpretation | Bridge from `pileFrom(N,0)` to intended list | Source-authoritative for intent; differential and ground evidence supports the implementation link but is finite. |
| Candidate generated `semantic.k` | Meaning of the submitted constructor term | Individually reviewed and concretely tested; minimal coverage is sufficient for this exact term. |
| `vAppend` and `pileFrom` equations | List concatenation and formal result formula | Ordinary truthful mathematics; guards/recursion audited. |
| Cell-free `eval*` equations | All five claims | Concerning duplicate model: locally faithful on ordinary target expressions/statements but has no K connection theorem to `<k>`. |
| Opaque `evalLoop` plus `verification.k:47-65` simplification | Entire loop claim and functional-correctness claim | **Illegitimate.** This is the program's central correctness conclusion installed as a trusted proof rule. The sensitivity test proves body insensitivity. |
| Differential tests and K/Python concrete comparisons | Program-intent and generated-semantics evidence on recorded inputs | Useful empirical bridge only; not universal proof and not a substitute for K reachability. |
| Partial-correctness/termination boundary | The requested theorem | A legitimate proof could exclude termination. Here the summary skips both execution and termination reasoning, so partial correctness does not justify the bridge. |

### Decision

The implementation appears correct, the generated operational semantics is
adequate for it, the rebuilt commands close, and the result mutation is
rejected. Those facts cannot turn an assumed, task-specific loop-result rule
into a proof of the operational program. Because the entry claim substitutes a
disconnected evaluator, bypasses `<k>`, and remains provable after a
result-changing semantic body mutation, the mandatory real-program soundness
and pinning gate fails. This fits `FAIL / NOT_LEGIT`, not `CONCERNS`: the gap is
in what the proof proves, not merely in finite intent evidence.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
