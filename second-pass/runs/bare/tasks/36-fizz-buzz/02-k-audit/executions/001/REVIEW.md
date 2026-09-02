# Independent adversarial audit: 36-fizz-buzz

## Decision

**CONCERNS / LEGIT.** The candidate contains a freshly reconstructable,
result-constraining partial-correctness proof of the actual submitted
`solution.mpy`. The source/IR link is exact, all three positive claims close
from fresh definitions, every local rule is accounted for, the proof is
body-sensitive, and a fresh false result obligation is rejected.

The concerns do not make a false conclusion provable for this program:

1. The generated semantics maps Python `%` and `//` to K's truncating `%Int`
   and `/Int`. That is correct for every reachable dividend in this program,
   which is nonnegative, but it is over-broad as a model of those Python
   operators for other accepted programs with negative dividends.
2. The final bridge from the transparent arithmetic definition
   `fizzFrom(0,N)` to the human phrase “digit 7 appears” is an audited informal
   mathematical argument supported by finite differential testing, not a
   separately machine-checked theorem about CPython string conversion.

These are limitations of the model/intent bridge, not material adequacy gaps
for the submitted program on its integer input domain.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
`canonical.py`, `prompt.py`, and `py2mpy.py`; it does **not** contain
`/reference/reference-semantics`. The mount therefore agrees with the rendered
mode, and no hidden or inferred reference semantics was used.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the 143-record JSONL generation trace only as untrusted
claims. They claim a successful generated run, three claims, examples
`0/2/3`, and a 263-input differential. None of those claims was credited
without reconstruction.

Integrity results:

- Candidate `prompt.py` and trusted `/reference/prompt.py` have identical
  SHA-256
  `9ca3d814d8f4c88fc35c6286cf046f39b0903222b094a800926eead370bcf4bb`
  and `cmp` exit 0.
- Candidate `py2mpy.py` and trusted `/reference/py2mpy.py` have identical
  SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
  and `cmp` exit 0.
- Required source artifacts `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and `prove.sh`, plus the four generation
  metadata/log artifacts, are present as regular files. The structured trace
  is also a regular JSONL file.
- No candidate symlinks exist. No required artifact is missing, changed,
  mistyped, or symlinked. There are no additional candidate helper K files.
- Extra candidate artifacts are `semantic-kompiled/`,
  `verification-kompiled/`, and `__pycache__/`. They are generated build/cache
  products, were treated as untrusted extras, and were neither copied nor used.
  Absence of candidate `PROOF.md` or `spec-vacuity.k` is not an integrity
  failure because neither was a required generation deliverable.

Commands, statuses, hashes, file types, trace summary, and bounded untrusted-log
extracts are in
[provenance.log](/audit-output/evidence/stage1/provenance.log) and its
reviewer scripts
[check_provenance.sh](/audit-output/evidence/stage1/check_provenance.sh) and
[trace_summary.py](/audit-output/evidence/stage1/trace_summary.py).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for integer `n`, return the total number of
occurrences of decimal digit `7` in the ordinary decimal representations of
all integers `i < n` that are divisible by 11 or 13. The trusted canonical
implementation realizes “integers less than `n`” as `range(n)`, so negative
and zero `n` produce an empty iteration and result zero. The documented
examples are `fizz_buzz(50)=0`, `fizz_buzz(78)=2`, and
`fizz_buzz(79)=3`.

The candidate uses a different but faithful arithmetic algorithm: it scans
`i=0..n-1`, filters by the two divisibility tests, and repeatedly divides a
qualifying nonnegative `i` by 10 while counting remainder 7. For negative
`n`, its outer loop is empty, matching `range(n)`.

Fresh translation used `/reference/py2mpy.py`, not the candidate copy. The
regenerated file and submitted `solution.mpy` are byte-identical, both with
SHA-256
`19e2e2121b4f89efdc54d5e6cd45db27f2a50ad2788d7f4471088778dd5706d2`.

The independent differential script loads `/reference/canonical.py` and the
clean scratch copy of candidate `solution.py` with separate import modules. It
does not reuse K summary equations. It tested:

- all documented examples;
- negative, zero, empty, and exclusive-range boundaries;
- just-before/at/after boundaries for multiples of 11, 13, and both;
- qualifying values with one or several digit sevens;
- every integer from -25 through 512;
- 256 deterministic generated integers from -500 through 10,000; and
- representative larger inputs through 20,000.

All 797 distinct inputs and selected results are printed in
[fidelity.log](/audit-output/evidence/stage2/fidelity.log). Mismatch count is
zero. The preserved oracle/test code is
[differential.py](/audit-output/evidence/stage2/differential.py), invoked by
[run_fidelity.sh](/audit-output/evidence/stage2/run_fidelity.sh). This is finite
bridge evidence, not a universal proof.

## 3. Clean proof reconstruction

All source needed for execution was explicitly copied to fresh directories
below `/tmp/audit-work`. No candidate `*-kompiled` directory or cache was
copied. K tool versions were independently recorded as v7.1.293.

Fresh builds:

- `semantic.k` compiled with the LLVM backend using main module `SEMANTIC` and
  syntax module `MPY-SYNTAX`; exit 0.
- `verification.k` compiled separately with the Haskell backend using main
  module `VERIFICATION` and syntax module `MPY-SYNTAX`; exit 0.

The freshly generated semantics concretely executed the submitted
`solution.mpy` for `N = -100, -1, 0, 1, 50, 78, 79, 118, 144, 771, 7778`.
Every `krun` exited 0; extracted K results matched both trusted canonical
Python and candidate Python. This covers empty negative/zero behavior,
documented examples, branch changes, a number with multiple sevens, and a
larger case.

The original `spec.k` as a three-claim set returned `#Top`, exit 0. A
reviewer-only labeled copy then selected each positive claim separately:

- inner claim: only the inner claim was retained; `#Top`, exit 0;
- outer claim: the already independently proved inner helper was marked
  trusted for dependency selection; `#Top`, exit 0;
- entry claim: the already independently proved inner and outer helpers were
  marked trusted; `#Top`, exit 0.

Thus the audit-time `--trusted` flags do not introduce unproved assumptions:
each dependency was separately proved, and the unmodified original claim set
also closes in one run.

Exact build, concrete execution, proof commands, output, and statuses are in
[reconstruction.log](/audit-output/evidence/stage3/reconstruction.log). The
reproducible script is
[run_reconstruction.sh](/audit-output/evidence/stage3/run_reconstruction.sh);
the labeled claims are
[spec-labeled.k](/audit-output/evidence/stage3/spec-labeled.k).

## 4. Adequacy and real-program pinning

### Claim meanings

The inner-loop claim says: for any `X >= 0`, starting at the exact submitted
inner loop with `x=X` and `count=C` consumes the loop, leaves the arbitrary
continuation `REST` in place, sets `x=0`, preserves `i` and `n`, and sets
`count=C+digitSevens(X)`.

The outer-loop claim says: for `0 <= I <= N`, starting at the exact submitted
outer loop with `i=I`, `n=N`, `x=0`, and `count=C` consumes the loop, leaves
`REST`, sets `i=N` and `x=0`, preserves `n=N`, and sets
`count=C+fizzFrom(I,N)`.

The end-to-end entry claim has no `requires` clause and therefore covers every
K integer `N`. Starting with the exact translated module, `<input>N</input>`,
empty environment, and result zero, partial correctness constrains a terminal
state to:

- `<k>.K</k>`;
- `count = result = fizzFrom(0,N)`;
- `i = fizzEnd(N)`, which is 0 for negative `N` and `N` otherwise;
- `n=N` and `x=0`.

The return value is not free, existential, tautological, or guarded by a
one-way implication. Both the environment's `count` and the observable
`result` cell are constrained to the same defined mathematical function.

### Actual-program pinning

The entry claim uses two macros only for readability. I parsed:

1. the submitted `solution.mpy`; and
2. the claim's `Module(FuncDef(... OUTER-LOOP ...))` program term,

under the fresh proof definition with `--expand-macros`. Their emitted KORE is
byte-identical; both hashes are
`ada0fa4a4fff5a8bafa2d2c6c20a68b70dfb6773e850e3b8bfbfdbd06d7b3122`.
Combined with trusted translator regeneration, this pins the claim to the real
submitted generated program rather than a substituted body.

Concrete satisfying states for all three preconditions are preserved in
[satisfying-states.txt](/audit-output/evidence/stage4/satisfying-states.txt).
For example, the entry witness `N=79` satisfies the unconditional entry
claim and gives `fizzFrom(0,79)=3`; both Python implementations return 3 and
fresh K execution returns 3. Ground substitutions for `N=-100, 0, 79, 771,
7778` produce `0, 0, 3, 37, 498`, respectively, matching both Python
implementations. The macro comparison, ground checks, sources, commands, and
statuses are in
[adequacy.log](/audit-output/evidence/stage4/adequacy.log), driven by
[run_adequacy.sh](/audit-output/evidence/stage4/run_adequacy.sh).

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule-inventory.md](/audit-output/evidence/stage5/rule-inventory.md). It
enumerates:

- all 14 translated-AST syntax productions;
- all 9 local continuation forms;
- the complete `<fizz>/<k>/<input>/<env>/<result>` configuration;
- all 27 operational semantic rules;
- all 4 local `[function,total]` declarations and their 10 equations;
- the one `[simplification]` rule; and
- both `[macro]` productions/rules.

There are no candidate helper K files, local opaque symbols, fresh
result-bearing symbols, `[functional]` or `[concrete]` declarations, priority
rules, or proof-time operational bridges.

### Operational semantics

The loader matches only
`Module(FuncDef("fizz_buzz",Params("n"),BODY))`, so it pins the entry name,
arity, binding, and body. It is a small task-entry harness rather than general
Python call semantics. It initializes exactly the four locals used here.
Preallocating `x=0` is not observable in the submitted control flow: `x` is
assigned from nonnegative `i` before every inner-loop use.

Statement sequencing is left-to-right. Name lookup requires a real map
binding. Assignment evaluates the RHS before update. Binary and comparison
rules explicitly sequence left then right. Boolean `or` short-circuits. `if`
and `while` guard evaluation and branch/loop reconstruction preserve control
order. Return evaluates its expression, writes `<result>`, and discards the
remainder of this single top-level invocation, for which no caller stack
exists. There is no modeled heap, allocation, output, exception, or external
state that could be silently lost.

Every constructor/operator in `solution.mpy` maps to declarations and rules:
`Module`, `FuncDef`, statement lists, `Assign`, `Name`, `Int`, `BinOp` for
`+/%//`, `Compare` for `</>/==`, binary `or`, `If`, `While`, and `Return`.
Unused Python constructs remain unmodeled and would parse-fail or visibly get
stuck; generated-semantics mode permits that minimal coverage.

### Summary equations and proof extensions

`digitSevens` has disjoint/exhaustive cases for `X<=0`, positive last digit 7,
and positive last digit not 7; positive recursion strictly decreases through
division by 10. `fizzContribution` has three disjoint/exhaustive cases for the
11-or-13 predicate. `fizzFrom` has disjoint/exhaustive empty/range-recursive
cases and decreases `N-I`. `fizzEnd` partitions negative/nonnegative integers.
There is no residual oracle interpretation.

The sole simplifier,
`(A+Int B)+Int C => A+Int(B+Int C)`, is true integer associativity and
right-associates a finite term; it does not encode the desired result. The two
macros are compile-time aliases whose exact expansion was mechanically checked
in stage 4.

The inner reachability claim is the machine-checked connection theorem from
fixed small-step inner-loop execution to `digitSevens`. The outer claim
connects fixed outer-loop execution to `fizzFrom`, using that proved inner
theorem. Reuse occurs after real semantic progress at the recurring loop
configuration, not through a rule that skips arbitrary execution.

### Scope limitation, not a false theorem witness

K documents `/Int` and `%Int` as truncating toward zero. CPython `//` floors
and its `%` pairs with floor division. The generated rules are therefore
over-broad for other programs with negative dividends. Reviewer programs
`return n // 10` and `return n % 10` at `n=-3` yield K values `0` and `-3`,
while CPython yields `-1` and `7`. Exact commands and outputs are in
[scope-limitations.log](/audit-output/evidence/stage5/scope-limitations.log).

I do not label this a material unsoundness of the submitted theorem because no
satisfying input to the real program can reach a negative dividend: `i` starts
at 0 and increments while `i<n`; `x` is assigned from `i`; and `x//10` occurs
only under `x>0`. Negative `n` skips the loop. Thus the broader mismatch cannot
enable a false result for the actual submitted program, but it justifies
`CONCERNS` rather than an unqualified `PASS`.

### Body sensitivity

A separate reviewer mutation changed the inner body's `count + 1` to
`count + 2` while leaving summaries/postconditions unchanged. At satisfying
input 78, mutated K and mutated Python both return 4, whereas canonical and
unmutated candidate Python return 2. The mutated definition compiled, but
`kprove` exited 1 with `WarnStuckClaimState` and the expected residual
equating additions of 1 and 2. This shows the proof is sensitive to the
property-bearing body and does not obtain its result from an execution-bypassing
oracle. Artifacts and logs are
[verification-body-mut.k](/audit-output/evidence/stage5/verification-body-mut.k),
[solution-body-mut.py](/audit-output/evidence/stage5/solution-body-mut.py), and
[body-sensitivity.log](/audit-output/evidence/stage5/body-sensitivity.log).

No inventoried rule was found that can enable a false conclusion for the real
program on any integer input. Gate A (real-program soundness) passes.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created a fresh reviewer
mutation. It leaves the program, helper claims, final environment, and all
preconditions unchanged, but changes the result obligation from
`fizzFrom(0,N)` to `fizzFrom(0,N)+1`.

`N=79` is a concrete satisfying witness: both Python implementations and fresh
K execution return 3, while the mutation requires 4. The mutated specification
successfully parsed/built with `kprove --dry-run`, exit 0. Its actual proof
then exited 1, not by timeout/parser/import/crash, and emitted
`WarnStuckClaimState` with the unmet residual
`fizzFrom(0,N)+Int 1 == fizzFrom(0,N)`.

The preserved mutation is
[spec-vacuity.k](/audit-output/evidence/stage6/spec-vacuity.k); exact commands,
statuses, and residual are in
[nonvacuity.log](/audit-output/evidence/stage6/nonvacuity.log), produced by
[run_nonvacuity.sh](/audit-output/evidence/stage6/run_nonvacuity.sh). The proof
is discriminating and result-constraining.

## 7. Proven versus assumed accounting

What is formally established is partial correctness under the audited
generated K semantics: for every K integer `N`, if execution of the exact
submitted translated module terminates from the specified initial
configuration, its terminal result/count is `fizzFrom(0,N)` and the remaining
locals have the values stated in stage 4. The two loop summaries are themselves
machine-checked reachability claims over the exact real loop bodies.

The complete ledger is
[trust-ledger.md](/audit-output/evidence/stage7/trust-ledger.md). In summary:

- Trusted low-level primitives: K v7.1.293 tooling/reachability calculus and
  builtin integer, Boolean, string, and map domains. This is the ordinary
  acceptable proof foundation.
- Trusted provenance boundary: mounted `py2mpy.py`. Its candidate copy and
  fresh output were checked byte-for-byte.
- Audited, not blindly assumed: every generated semantic rule, every total
  summary equation, the integer-associativity simplifier, and both macros.
- No opaque symbol, result oracle, fresh value, empirical operational bridge,
  priority override, or unproved program-body summary contributes to closure.
- Machine-proved dependencies: inner claim, outer claim, and entry claim.
- Empirical evidence only: canonical/candidate differential and concrete K
  comparisons. These support source/intent and semantics bridges but do not
  substitute for the K proof.
- Informal bridge: the exhaustive arithmetic equations plainly implement the
  decimal-seven/divisibility description, but this equivalence is not a
  separate K theorem about CPython's string conversion.
- Excluded: total correctness/termination, non-integer inputs, general Python
  module/call semantics, exceptions, and generated-semantics behavior for
  unused constructs. The negative-operand `%`/`//` mismatch is explicitly
  excluded because it is unreachable in this program.

Validation gates: Gate A passes; Gate B passes for the actual integer-domain
program with the documented informal intent bridge and unreachable
negative-arithmetic scope limitation; Gate C passes because every relied-on
test/mutation artifact, command, input scope, oracle, status, and bounded output
is preserved. Under the requested decision taxonomy, those non-material
limitations warrant `CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
