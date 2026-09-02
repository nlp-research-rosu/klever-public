# Adversarial audit review — 46-fib4

The candidate has two machine-closing K claims, and the fixed-input claim really
executes the submitted program body. It does **not**, however, prove the
HumanEval contract over its material domain. The only entry-like claim checks
the thirteen constants `0` through `12`; the other claim proves one arbitrary
loop-body transition without an invariant or any connection to the Fib4
sequence. Under the benchmark's explicit decision rule, this finite
specialization is not a legitimate proof of the unrestricted task.

All candidate and generation records were treated as untrusted evidence. The
review used a clean tree at `/tmp/audit-work/46-fib4-review` and newly built
definitions named `reviewer-runtime-kompiled` and
`reviewer-verification-kompiled`.

## 1. Input and provenance integrity

### Record layout and required mounts

`/audit-input.json` declares:

- problem `46-fib4`;
- condition `semantics`;
- record layout `legacy-selected-stage1`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- `mount_reference_semantics: true`.

That mode agrees with the mounts: `/reference/reference-semantics` exists.
Every launcher record required for `legacy-selected-stage1` was present and
readable: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, the structured trace, and the present
`usage.json`. The optional legacy records were also parsed. Historical runtime
metrics are not required for this layout and were not reconstructed.

The campaign object in `/audit-input.json` is structurally equal to
`/audit-campaign-lock.json`. The lock hash is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the recorded value. Independently computed SHA-256 values for the
run/task/result/invocation records, generation prompt, logs, metrics, usage,
trusted prompt, translator, canonical solution, and trace file all equal their
launcher-recorded hashes. The trace contains 660 valid JSONL records and no
parse errors.

Evidence:

- `/audit-output/evidence/inspect_generation.py`
- `/audit-output/evidence/stage1-integrity-rerun.log`
- `/audit-output/evidence/hash_mounted_trees.py`
- `/audit-output/evidence/stage1-tree-hashes.log`

The earlier `/audit-output/evidence/stage1-integrity.log` records an initial
reviewer command failure because `jq` is unavailable. The Python rerun replaced
that check and passed; this was not attributed to the candidate.

### Trusted-artifact comparisons

The following independent checks all exited 0:

```text
cmp -s /candidate/prompt.py /reference/prompt.py
cmp -s /candidate/py2mpy.py /reference/py2mpy.py
diff -r --no-dereference /reference/reference-semantics /candidate/reference-semantics
```

The recursive semantics comparison found exactly the same 25 entries, entry
types, and contents. The reviewer manifest digest for each semantics tree is
the same (`b7abdfcb700ea6de1e5e857448cfc2d6fa815a2b718cfe7b5f5c1fe0b5423209`).
No symlinks, missing entries, extra entries, or mistyped entries were found in
either tree. Every individual semantics-file hash is recorded in
`stage1-tree-hashes.log`.

The generation report's `KPROVE_PASSED` marker, its prose, and its retained
logs were read only as claims. There is no infrastructure breach, so the audit
continues to a candidate verdict.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt defines the nonnegative-index Fib4 sequence:

```text
fib4(0) = 0
fib4(1) = 0
fib4(2) = 2
fib4(3) = 0
fib4(n) = fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4)
```

It asks for the `n`-th element, efficiently and without recursion, and gives
examples at `n = 5, 6, 7`. There is no upper bound. The material source domain
is therefore all nonnegative integer indices, not a finite prefix. An “empty”
case is inapplicable to a single integer argument.

The trusted canonical implementation maintains the most recent four values in
a list. The candidate implements the same recurrence with integer variables
`a`, `b`, `c`, and `d`, starts `i` at 4, rotates the state after computing the
sum, and returns `d`. It is iterative and nonrecursive.

### Trusted regeneration

The exact reconstruction commands and statuses are in
`/audit-output/evidence/stage2-fidelity.log`. In particular:

```text
python3 /tmp/audit-work/46-fib4-review/py2mpy.py \
  /tmp/audit-work/46-fib4-review/solution.py \
  > /tmp/audit-work/46-fib4-review/solution.regenerated.mpy
# exit 0

cmp -s solution.regenerated.mpy solution.mpy
# exit 0
```

Both files have SHA-256
`3fd876f2abd77d05fc6fd0e4a185520584d51f12b0f3efd4136daba1b561c47d`.
Thus the submitted MPY program is byte-for-byte the output of the trusted
translator on the submitted Python source.

### Independent differential test

`/audit-output/evidence/differential_fib4.py` imports the trusted canonical and
candidate entry points from separate files. It checks:

- all branch boundaries `0, 1, 2, 3, 4`;
- all documented examples `5, 6, 7`;
- every integer from 0 through 200; and
- 100 fixed-seed generated integers in `[201, 2000]`.

The exact command exited 0 with 296 unique intended-domain inputs and zero
mismatches. Selected larger observations include `fib4(50)`,
`fib4(200)`, `fib4(1000)`, and `fib4(2000)`. Negative probes are explicitly
reported as outside the sequence-index domain; they do not support the theorem.
This test is finite evidence of source-level fidelity, not a universal proof.

## 3. Clean proof reconstruction

No candidate-provided compiled definition or cache was copied. K 7.1.293 was
used, matching the campaign lock. The full command log is
`/audit-output/evidence/stage3-reconstruction.log`.

The fresh concrete build and execution were:

```text
timeout 900 kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
# exit 0

timeout 300 krun concrete-tests.mpy \
  --definition reviewer-runtime-kompiled
# exit 0
```

`krun` reached `.K` with `NoExc` and exit code 0. The final module scope holds
the submitted `fib4` closure. Compiler non-exhaustiveness warnings concern
unused semantics functions and do not change the exit status.

The fresh proof build was:

```text
timeout 900 kompile verification.k \
  --backend haskell --main-module FIB4-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
# exit 0
```

Each positive claim was then run separately:

```text
timeout 900 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.loop-step --output pretty
# output: #Top
# exit 0

timeout 900 kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC \
  --claims FIB4-SPEC.operational-cases --output pretty
# output: #Top
# exit 0
```

Fresh reconstruction therefore verifies the two claims that were actually
submitted. It does not establish that those claims are adequate for the task.

## 4. Adequacy and real-program pinning

### `loop-step`

The precondition is the displayed loop-body computation, an environment
location `L`, and a scope at `L` containing arbitrary integer bindings:

```text
a=A, b=B, c=C, d=D, next_value=E, i=I
```

There is no `requires` clause. The postcondition is `.K` with those bindings
updated to:

```text
a=B, b=C, c=D, d=A+B+C+D,
next_value=A+B+C+D, i=I+1
```

The state is satisfiable. A recorded witness is
`A=0, B=0, C=2, D=0, E=999, I=4`, producing
`a=0, b=2, c=0, d=2, next_value=2, i=5`.

This is a sound one-step statement about the real assignment sequence. It is
not a loop invariant, does not mention `n`, does not connect the four variables
to prior Fib4 values, and is not used by the separately selected
`operational-cases` proof. Consequently it supplies no induction over input
size.

### `operational-cases`

The precondition is one exact, realizable module configuration:

- module scope 0 binds `fib4` to a closure;
- the closure takes parameter `n`, has defining scope 0, and contains the
  submitted function body;
- the builtins scope is at `-1`;
- heap and stack are empty;
- return and exception states are `noRet` and `NoExc`; and
- exit code is 0.

The `<k>` cell contains thirteen sequential assertions:

```text
fib4(0)=0, fib4(1)=0, fib4(2)=2, fib4(3)=0,
fib4(4)=2, fib4(5)=4, fib4(6)=8, fib4(7)=14,
fib4(8)=28, fib4(9)=54, fib4(10)=104,
fib4(11)=200, fib4(12)=386.
```

The postcondition requires `.K` while the displayed non-`k` cells remain at
their stated values. A false assertion would change `<exc>` to
`AssertionError` and `<exit-code>` to 1, so this claim genuinely constrains all
thirteen fixed results.

Program pinning for this finite claim is strong. The reviewer extracted the
closure term from the claim with balanced constructor delimiters, normalized
only explicit `.Stmts` list units to MPY surface list syntax, and parsed both
the extracted term and `solution.mpy` with K's `kast`. The JSON KAST files are
byte-identical and share SHA-256
`07a02e4ffe003767cfccd1571a6fbd74177b67e97cc25beea017771e7c0038b0f`.
See:

- `/audit-output/evidence/extract_claim_program.py`
- `/audit-output/evidence/check_claim_scope.py`
- `/audit-output/evidence/stage4-adequacy-rerun.log`

The thirteen expected values also equal both Python implementations. The
earlier `stage4-adequacy.log` contains reviewer-script/parser errors; the fixed
rerun is the authoritative evidence.

### Fatal adequacy gap

There is no claim with a symbolic input `n`, no precondition such as
`n >= 0`, and no postcondition characterizing the recurrence or canonical
Fib4 value for arbitrary `n`. The largest tested theorem input is 12. A
standalone transition lemma plus thirteen examples cannot prove an
unrestricted sequence function. The manually embedded program is the right
program, but the theorem is only a finite test theorem.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/build_rule_inventory.py` independently generated
`/audit-output/evidence/rule-inventory.md`. It contains the exact source chunk,
file, line, kind, subtype, and attributes for every local item:

```text
227 syntax declarations
695 rules
5 contexts
1 configuration
2 claims
930 total records
```

The inventory covers `semantics.k`, all 23 files below
`reference-semantics/semantics/`, `verification.k`, and `spec.k`.
The per-file counts and generation command are in
`/audit-output/evidence/stage5-static-review-rerun.log`.

Every semantics item is part of the launcher-supplied, byte-matched fixed
semantics. There is no syntax, function, rule, lemma, priority, simplification,
or opaque symbol in candidate `verification.k`; it only imports `MPY`.
Searches also find no occurrence of `fib4` in the semantics or verification
module. Thus there is no proof-local task-answer rule, operational bridge,
oracle, or alternate call route to audit.

The fixed semantics contains no `[simplification]` or `[functional]`
declaration. Its 25 explicitly named opaque/symbol boundaries are:

- `md5hexCodes`;
- `sortVS` and `sortKeyVS`; and
- the float boundaries `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`.

None occurs in `solution.mpy`, either claim's executed Fib4 body, or the
integer-only assertion path. They cannot affect a branch, state update,
return, exception, or result in these proofs.

### Used-construct mapping and decisions

| Program construct | Declaration and operative fixed rules | Audit decision |
|---|---|---|
| `Module`, statement list | `syntax.k:56,61`; `core.k:124-127` | Loads and sequences every statement left-to-right. |
| `FuncDef`, `Params` | `syntax.k:53,57,60`; `functions.k:14-16` | Binds exactly the submitted body as a closure in scope 0. |
| `Name`, integer literal | `syntax.k:9,12`; `core.k:130-154,193-196` | Scope-chain lookup and mathematical integer value are direct. |
| `Call` | `syntax.k:28`; `call.k:19-21,69-75`; `core.k:183-191` | Callee and argument evaluation, new frame allocation, binding, and continuation are preserved. |
| `Return` | `syntax.k:50`; `functions.k:78-90` | Evaluates the value, records it, pops exactly the callee frame, and restores the caller continuation. |
| `Assign` | `syntax.k:41`; `controls.k:9-18` | RHS strictness precedes a current-scope update. Cell-reference priority rules are inapplicable because the frames have no `$cells`. |
| `If` | `syntax.k:49`; `controls.k:51-54`; `core.k:198-205` | Strict condition evaluation followed by the truthful integer truthiness branch. |
| `While` | `syntax.k:46`; `controls.k:65-85` | Re-evaluates the guard, sequences the real body, and loops through `#loopLbl`; no body is bypassed. |
| `BinOp("+")` | `syntax.k:15`; `operators.k:12`; `int.k:9` | Sequential operand evaluation and exact unbounded integer addition. |
| `Compare("==","<=")` | `syntax.k:30,32`; `operators.k:15-17`; `int.k:23,26` | Left/right evaluation contexts and ordinary integer comparisons. |
| `Assert` in the spec | `syntax.k:51`; `assert.k:6-15` | Truth deletes the assertion; falsehood records `AssertionError` and exit code 1, making the postcondition unreachable. |

The complete configuration footprint was checked: calls change and restore
`<env>`, allocate/delete a scope, and push/pop `<stack>`; assignments change
only the active scope map; the program never allocates heap objects; returns
use `<ret>` transiently; assertions preserve `NoExc`/0 only on success.
Evaluation order follows the strict/seqstrict declarations and explicit
contexts. The priority rules for references, closure cells, floats, methods,
sorting, dictionaries, and sequences have unsatisfied constructor/guard
patterns on this path.

The remaining fixed-semantics rules are exhaustively listed in the inventory
but are unreachable from this integer-only program and claim. Review found no
overlap on the used path that produces disagreeing right-hand sides, no
unmodeled used construct, and no rule that can fabricate a Fib4 result. No
rule is labeled unsound, so no false-conclusion witness is asserted.

### Body sensitivity

As a separate execution-fidelity probe, the reviewer changed the return value
inside the closure actually executed by the claim from `fib4(2)=2` to
`fib4(2)=3`, leaving the expected assertion at 2. The command:

```text
timeout 900 kprove spec-body-mutation.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC-BODY-MUTATION \
  --claims FIB4-SPEC-BODY-MUTATION.operational-cases \
  --output pretty
```

exited 1 with `WarnStuckClaimState`; the residual shows the mutated closure,
`AssertionError`, and exit code 1. This changes the executed theorem term, not
merely an external source file. Evidence is in
`/audit-output/evidence/make_body_mutation.py` and
`/audit-output/evidence/stage5-static-review-rerun.log`.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`. The reviewer created
`spec-vacuity-review.k` from scratch by changing only the result-constraining
assertion for `n=12` from 386 to the demonstrably false 387. The closure body
was unchanged. Both Python implementations return 386 for the satisfying
input.

The mutation first built successfully:

```text
timeout 300 kprove spec-vacuity-review.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC-VACUITY \
  --claims FIB4-SPEC-VACUITY.operational-cases \
  --dry-run --output pretty
# exit 0
```

The live proof command:

```text
timeout 900 kprove spec-vacuity-review.k \
  --definition reviewer-verification-kompiled \
  --spec-module FIB4-SPEC-VACUITY \
  --claims FIB4-SPEC-VACUITY.operational-cases \
  --output pretty
```

exited 1 with `WarnStuckClaimState`. Its residual has `.K` but
`<exc> AssertionError </exc>` and `<exit-code> 1 </exit-code>`, which cannot
unify with the destination's unchanged `NoExc`/0 cells. This is the expected
unmet result obligation, not a parse error, timeout, or unrelated crash.

Evidence:

- `/audit-output/evidence/make_vacuity_mutation.py`
- `/audit-output/evidence/stage6-nonvacuity.sh`
- `/audit-output/evidence/stage6-nonvacuity.log`

This demonstrates non-vacuity for the finite claim. It cannot enlarge that
claim's input domain.

## 7. Proven versus assumed accounting

### What the K proof establishes

Conditional on the supplied MPY semantics and K toolchain, the successful
reachability proofs establish exactly:

1. For arbitrary integer bindings in the displayed scope, one execution of
   the submitted six-assignment loop body performs the stated rotation, sum,
   and index increment.
2. Starting from the exact displayed module configuration, the submitted
   closure evaluates successfully and returns the asserted values at each
   fixed input `0, 1, ..., 12`, leaving no exception and exit code 0.

The result constraints are real, the preconditions are satisfiable, and the
finite operational claim pins the submitted MPY body.

### What is not proven

The proof does not establish:

- `fib4(n)` for arbitrary nonnegative integer `n`;
- that the loop state represents four consecutive Fib4 values;
- preservation and termination of a sequence invariant from `i=4` through an
  arbitrary `n`;
- universal equivalence of the candidate and canonical Python functions; or
- the HumanEval contract outside the thirteen constants in the claim.

Partial correctness would not itself require a termination theorem, but it
still requires a universally quantified result theorem over the stated input
domain. That theorem is absent.

### Trust ledger

- **K 7.1.293, Haskell/LLVM backends, and builtin Int/Bool/Map/List hooks.**
  These are the ordinary machine-checking and mathematical trust boundary.
  Every closing and failing run was reconstructed with this locked version.
- **Supplied MPY semantics.** This is the selected fixed semantics mandated by
  the task, not a candidate-generated language model. Candidate and trusted
  trees are recursively identical. The used integer/control/call footprint
  was statically reviewed. Its unused opaque float/sort/MD5 symbols have no
  dependent claim here.
- **Trusted translator.** Byte-identical regeneration proves that
  `solution.mpy` is the translator's output. General Python-to-MPY semantic
  preservation is not proved in this candidate; source fidelity is supported
  by inspection and finite differential testing.
- **Canonical Python implementation.** It is a trusted problem input and is
  used only as an executable differential oracle, never as a K axiom.
- **KAST extraction normalization.** Removing explicit `.Stmts` empty-list
  units is justified by the identical K parser output; the resulting KAST
  equality mechanically supports body identity.
- **Differential bridge.** The 296 zero-mismatch tests support the
  implementation-to-contract bridge only on those inputs. They do not repair
  the missing universal reachability claim.

### Decision

The submitted finite claims are sound and non-vacuous under the fixed
semantics, and one of them pins the real generated body. Gate A therefore
passes for the theorem actually written. Intent adequacy fails materially:
thirteen fixed sizes are substituted for an unbounded HumanEval input domain.
The benchmark prompt explicitly maps this kind of `SOUND-BUT-LIMITED` domain
narrowing to `FAIL / NOT_LEGIT`, not to `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
