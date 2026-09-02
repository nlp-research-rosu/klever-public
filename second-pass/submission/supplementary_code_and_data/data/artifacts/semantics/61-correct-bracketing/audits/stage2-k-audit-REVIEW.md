# Independent adversarial review: 61-correct-bracketing

The candidate does not contain a K partial-correctness proof of the submitted
program entry point. Its sole reachability claim is a sound, non-vacuous loop
suffix lemma, but it begins in a manually constructed active function frame
after function binding, parameter binding, both initialization assignments, and
call setup. Those omissions are material execution, not inert normalization.
The required real-program pinning gate therefore fails even though the helper
claim cleanly reconstructs to `#Top`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1` and `semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mount agrees with the
rendered mode; there is no infrastructure breach.

The independent checker in `evidence/integrity_check.py` established:

- `/audit-campaign-lock.json` is a regular file, has SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object exactly equals the `audit_campaign` block in
  `/audit-input.json`.
- Every launcher-declared container mount exists. All records required by the
  legacy-selected-stage1 layout are readable regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the JSONL trace. `usage.json` is also
  present and valid. Historical `runtime-metrics.json` was not recorded and is
  not required for this layout.
- The independently computed SHA-256 values of the lock, canonical source,
  prompt, translator, run/task/result manifests, invocation, metrics, usage,
  generation prompt, last message, output log, and individual trace file match
  their launcher-recorded values.
- All 1,044 JSONL trace events parse. The complete 1,830,082-byte generation
  output and all other text records decode and were read. Their `SUCCEEDED`,
  `KPROVE_PASSED`, and `#Top` statements were treated only as untrusted claims.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounted counterparts.
- Recursive, no-dereference comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` found identical paths, entry types, and file
  bytes. Neither tree contains a symlink; there are no missing, additional,
  mistyped, or changed entries.
- All five required proof artifacts are present as regular files. The
  candidate tree contains no symlink.

The exact checks, hashes, file inventory, and exit 0 are in
`evidence/stage1-integrity.log`. A bounded semantic summary of every generation
record and the fully parsed trace is in
`evidence/stage1-generation-record-summary.log`. Notably, the untrusted trace
itself says that an attempted public-call claim was removed in favor of the
loop invariant; the immutable submitted files, not that explanation, determine
the finding below.

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py` is: for an unrestricted finite
string whose characters are only `(` and `)`, return true exactly when every
prefix has at least as many opening as closing parentheses and the final counts
are equal. The trusted `/reference/canonical.py` implements this with an integer
depth, early false on a negative prefix, and final equality to zero.

`/candidate/solution.py` implements the same algorithm with `balance` and
initializes `bracket = ""` before the loop. That extra local initialization
does not alter the returned value.

The trusted command

```text
python3 /reference/py2mpy.py /tmp/audit-work/proof/solution.py > /tmp/audit-work/proof/regenerated.mpy
```

exited 0. Both submitted and regenerated constructor files have SHA-256
`9022bba7a15313c42602d1d5dc7f84072698d274da99fa12267e5ada75508e51`;
`cmp -s` exited 0.

The independent differential test imports the trusted canonical and candidate
functions separately. It covers all four documented examples, empty input,
each branch boundary, all parenthesis strings of lengths 0 through 12, 1,000
deterministically generated strings of lengths 0 through 512, and three
length-10,000 cases. There were 9,212 comparisons, including true results,
negative-prefix failures, and nonnegative-prefix/final-positive failures, with
zero mismatches. The script, exact construction, digest of the ordered cases,
results, command, and exit 0 are in
`evidence/differential_test.py` and
`evidence/stage2-fidelity-differential.log`.

This is strong finite evidence that the Python implementation is correct; it
is not a substitute for a K theorem.

Stage 2 result: PASS.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/proof`. The candidate
`kore-exec.tar.gz`, `__pycache__`, and any candidate-built definition or cache
were not copied or used. Before building, the scratch root contained no
`*-kompiled` directory.

The independently installed tools report K version 7.1.293. The following
fresh commands were run:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. An audit smoke program consisting of the exact submitted function plus
normal/boundary assertions was regenerated with the trusted translator and run:

```text
krun audit_smoke.mpy --definition runtime-kompiled
```

Exit 0, final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.

The proof definition was then rebuilt:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit 0. `spec.k` contains exactly one claim, label `loop`. Its positive target
command was:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims loop
```

It printed `#Top` and exited 0. Thus every submitted positive target claim
closes from a clean reconstruction. Compiler warnings about several broad
supplied-semantics total functions and unused claim variables are accounted for
in Stage 5; none changes these exit results.

The exact commands and bounded output are in
`evidence/stage3-positive.sh` and
`evidence/stage3-clean-build-positive.log`.

Stage 3 result: PASS for reconstruction of the submitted claim.

## 4. Adequacy and real-program pinning

### The formal claim

In plain language, `/candidate/spec.k:10` assumes:

- a current function frame at environment location 1;
- local `balance = B`, an old string value for `bracket`, and an arbitrary
  `brackets = str(INPUT)`;
- the exact loop body and final return constructor appearing in the submitted
  source suffix;
- an arbitrary remaining iterable `str(S)`;
- a stack frame which will return to arbitrary continuation `CONT`;
- `NoExc`, `noRet`, exit code zero, and `B >= 0`.

It proves that executing that already-active `#loop` and final return pops the
frame and produces `correctCodes(S, B) ~> CONT`, with the caller environment
restored. `correctCodes` returns true exactly when the remaining codes, starting
at balance `B`, never force an early close and finish at balance zero.

The precondition is satisfiable. One concrete state uses
`S = .IntSeq`, `B = 0`, `INPUT = .IntSeq`, `OLD = str(.IntSeq)`,
empty globals/heap, `HLOC = 0`, and `CONT = .K`. Concrete substitutions for
`""`, `"()"`, `"("`, `")"`, `"())"`, and the suffix `")"` at `B = 1`
all give the same result under `correctCodes`, the trusted canonical, and the
candidate Python function. These checks are recorded in
`evidence/stage4-pinning-witnesses.log`.

The result is genuinely constrained: it is neither a free variable nor a
tautology. Stage 6 independently confirms this.

### Material pinning failure

Trusted regeneration proves the submitted constructor module is
`/candidate/solution.mpy:1-12`. Mechanical constructor comparison found that
the target, loop body, and final return embedded in the claim match the
`For`-body and return suffix, after only normalizing explicit versus empty
`.Stmts`.

But the claim LHS contains none of the following submitted terms:

- `Module(...)`;
- `FuncDef("correct_bracketing", Params("brackets"), ...)`;
- the binding of the name `correct_bracketing`;
- `Assign(Name("balance"), Int(0))`;
- `Assign(Name("bracket"), Str(""))`;
- lookup/argument evaluation, parameter binding, call-frame creation, or a call
  to the generated function.

The formal variable `INPUT` is unrelated to `S` and is unused after the
manually selected loop state. Although a real entry proof could instantiate
`S = INPUT` and `B = 0` after executing the omitted prefix, no submitted claim
performs or proves that reachability transition.

These are not typing-only imports, syntax macros, or other demonstrated
semantically inert normalization. They are the function binding, body prefix,
input binding, and control setup required to establish that this particular
submitted function reaches the proved loop configuration. A sound theorem
about a hand-constructed mid-function state is not, by itself, a K proof of the
real generated program.

The mechanical comparison and omitted-term checks are preserved in
`evidence/pinning_and_witnesses.py` and
`evidence/stage4-pinning-witnesses.log`.

Stage 4 result: FAIL. This is the decisive candidate defect.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 24 supplied-semantics K files,
`verification.k`, and `spec.k`. It enumerates 697 ordinary rules, 228 syntax
declarations, the configuration, all contexts and imports, 146
function-bearing declarations, 108 `total` declarations, 22
`no-evaluators` declarations, 45 priority-attribute occurrences, all macros
and concrete rules, no `functional` declarations, and no simplification rules.
Line-count cross-checks agree with the inventory.

The complete source-location inventory is
`evidence/stage5-rule-inventory.log`; its generator is
`evidence/k_inventory.py`. The per-module decision for every inventoried rule,
the used-constructor mapping, evaluation/control/state analysis, and
proof-extension record are in `evidence/stage5-static-assessment.md`.

The material used path is:

```text
string iteration -> bind loop target -> string equality ->
integer balance update -> integer negative test ->
early return or next #loop -> final integer equality -> frame pop
```

The supplied rules preserve order and the relevant cells along this path.
String literals `""` and `"("` are within the supplied ASCII literal rule.
K integers give the unbounded integer behavior needed here. The proof build
imports `MPY`, not the LLVM-only `MPY-CONCRETE`.

`verification.k` contributes exactly one symbol and two equations:
`correctCodes(IntSeq, Int)`. Classification:

- definitional summary, not an operational bridge;
- pure, with no state footprint;
- empty and cons equations are disjoint and exhaustive on finite `IntSeq`;
- recursion strictly descends on the tail;
- code 40 implements `"("`; every other code takes the same `else` as the
  submitted program;
- the cons rule’s zero-balance early false exactly matches the program’s
  post-decrement negative test;
- no opacity, priority, simplification, or unconstrained oracle is introduced.

No local rule bypasses the loop or encodes a result without execution. No
unsound-rule finding is made, so no false-conclusion witness is asserted. The
broad supplied semantics does contain unused, explicit trust/coverage
boundaries—especially opaque float, sort, MD5, and underspecified out-of-bounds
operations—but no result or branch in this proof depends on any of them.
Compiler-noted non-exhaustive total functions are likewise off path and are an
evidence limitation rather than a false equation for this theorem.

Stage 5 result: PASS for rule-level soundness on this claim and intended input
domain. It does not cure the Stage 4 theorem-scope failure.

## 6. Fresh non-vacuity test

The audit created a new spec module, `SPEC-AUDIT-VACUITY`, by changing only the
result-constraining destination:

```text
correctCodes(S, B)
```

to:

```text
notBool correctCodes(S, B)
```

This is demonstrably false for the satisfying state `S = .IntSeq`, `B = 0`:
the loop/final return produces true, while the mutated destination requires
false.

The mutation diff is in `evidence/stage6-vacuity.log`. A `kprove --dry-run`
against the clean proof definition exited 0, establishing successful parsing
and KORE generation. The actual proof exited 1 with
`WarnStuckClaimState`; its residual explicitly has `S = .IntSeq`,
`B >= 0`, and the failed implication between `B ==Int 0` and
`notBool B ==Int 0`. It then reports that the configuration cannot be rewritten
further. This is the expected unmet result obligation, not a parse error,
timeout, missing import, or unrelated crash.

The script, full bounded log, and raw prover residual are
`evidence/stage6-vacuity.sh`, `evidence/stage6-vacuity.log`, and
`evidence/stage6-vacuity-prover-raw.log`.

Stage 6 result: PASS. The loop lemma is non-vacuous.

## 7. Proven versus assumed accounting

### What is machine-checked

Conditional on the supplied K definition and K backend, the successful
reachability proof establishes partial correctness of the manually initialized
loop configuration: for every finite code sequence `S`, every integer
`B >= 0`, and the framed cells described by the claim, executing the exact
loop-and-return suffix yields `correctCodes(S, B)` and restores the stated
caller frame. The proof is universal in `S`; it is not a finite unrolling.

### Trust and evidence boundaries

- K 7.1.293, its Haskell reachability backend/circularity mechanism, and K's
  built-in integer, Boolean, string, map, and list theories are trusted.
- The mounted MPY semantics is supplied rather than candidate-generated. Its
  integrity was independently established, and every local rule was
  inventoried. The specific execution path used here has no unresolved opaque
  result.
- The CPython-AST translator is trusted. Byte-identical regeneration connects
  `solution.py` to `solution.mpy`.
- The ordinary mathematical reading of `correctCodes` as the balanced-prefix
  predicate is supported by its exhaustive equations and by differential
  evidence, but there is no separate K theorem formalizing the English phrase
  “corresponding closing bracket.” This would be a non-fatal intent bridge if
  the program entry were proved.
- The Python differential test is finite empirical evidence only.
- No float, sort, MD5, out-of-bounds, or other opaque supplied symbol affects
  the claim’s branches or result.
- Termination is outside partial correctness, although all tested finite
  executions terminate and the summary recursion structurally descends.

### Missing theorem, not an acceptable assumption

There is no machine-checked connection from loading the submitted
`Module(FuncDef(...))`, selecting its `correct_bracketing` binding, evaluating
an input argument, entering its frame, and executing the two initialization
assignments to the claim’s manually supplied `#loop` state. Treating that
material program-defined execution as an informal “entry case” would replace
the required real-program theorem with an assumption.

The clean `#Top`, source differential agreement, and successful non-vacuity
test all validate the narrower loop lemma. None supplies the missing
real-program reachability claim. Under the benchmark decision boundary, a
proof of a substituted mid-function configuration rather than the actual
submitted program is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
