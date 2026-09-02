# Independent adversarial audit: 61-correct-bracketing

This review treats every candidate artifact and every generation record as
untrusted evidence. I used the mandated Kit workflow in order: `using-kit`,
`validating-proof`, and, because the declared mode is
`GENERATED_SEMANTICS`, `writing-semantics`. All execution and generated
artifacts were made under
`/tmp/audit-work/61-correct-bracketing-audit`; no candidate-provided compiled
definition or cache was reused.

The reconstructed proof is legitimate and covers the unrestricted HumanEval
source-contract domain. The benchmark verdict is `CONCERNS / LEGIT`, rather
than `PASS`, because the generated semantics has two non-result-bearing
limitations: it preinitializes the dead loop variable on an empty iterable,
and `bracketSpec` is declared `[total]` although its equations omit an
unreachable negative-depth case. Neither limitation can change or fabricate
the proved return value on the intended domain.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, problem
`61-correct-bracketing`, and `semantics_mode =
GENERATED_SEMANTICS`. I used its `container_paths` entries, not the host-only
provenance paths.

I inspected all records required by that layout:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- all 420 JSON records in the structured trace
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T05-19-20-019f8956-4685-7661-ba53-109c262b4998.jsonl`.

The records are generation claims only. In particular, I did not accept their
`KPROVE_PASSED`, prior `#Top` output, or final report as proof evidence.

Integrity results:

- `/audit-campaign-lock.json` is a regular file, its SHA-256 is
  `ad5dfc...d745`, and its parsed object exactly equals
  `audit-input.json.audit_campaign`.
- Every required record is a readable regular file. No symlink occurs anywhere
  under `/candidate`, `/generation-evidence`, or `/reference`.
- All individual evidence hashes listed by `invocation.json` and
  `generation-result.json` equal the mounted files. The structured trace file,
  for example, is `4c1284...b862`.
- An independent pipeline tree digest of `/candidate` is
  `d129ca...9ffadf`, equal to the input, output, retained-workspace, and
  stage-result workspace digests. The independently computed trace-tree digest
  is `d515c2...63e1`, equal to `usage.json.source_trace_sha256`.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`f900fc...1bb`), and candidate `py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (`406485...b16`).
- `/reference/reference-semantics` does not exist, as required for
  `GENERATED_SEMANTICS`. I did not search for or use any hidden reference
  semantics.
- Required candidate proof sources—`solution.py`, `solution.mpy`,
  `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`—are present as
  regular files. Candidate `__pycache__` and `kore-exec.tar.gz` were ignored
  and not copied into the clean build.

There is no infrastructure breach. Exact hashes, type checks, trace counts,
and commands are preserved in
[`evidence/01_provenance.log`](/audit-output/evidence/01_provenance.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt says the argument is a string consisting of `(` and `)`.
The function must return true exactly for correctly bracketed strings: no
prefix may contain more closes than opens, and the final unmatched-open count
must be zero. The trusted canonical implementation maintains `depth`, rejects
as soon as it becomes negative, and finally tests `depth == 0`.

Candidate `solution.py` implements the same algorithm with `count`: `(` adds
one; on `)`, zero causes an immediate false return and otherwise one is
subtracted; the final result is `count == 0`. It does not narrow the prompt's
input domain or bound input length.

### Trusted regeneration

I regenerated the IR using the trusted mounted translator:

```text
python3 /tmp/audit-work/61-correct-bracketing-audit/reference/py2mpy.py \
  /tmp/audit-work/61-correct-bracketing-audit/candidate/solution.py \
  > /tmp/audit-work/61-correct-bracketing-audit/regenerated.mpy
cmp -s regenerated.mpy candidate/solution.mpy
```

Both commands exited 0. Both files have SHA-256
`6679593a8ad6af41affa3fe98fe9acd62e1d00f49f869df85c6d414ade518969`;
they are byte-identical. See
[`evidence/02_regeneration.log`](/audit-output/evidence/02_regeneration.log).

### Independent differential test

[`evidence/02_differential.py`](/audit-output/evidence/02_differential.py)
loads the trusted canonical and generated entry points under distinct module
names. It checks:

- the four documented examples plus empty, one-character, branch-boundary,
  nested, sequential, unmatched, and bad-prefix cases;
- every string over `(` and `)` through length 12;
- 1,000 seeded strings of lengths 13 through 256;
- four 2,000-character long cases.

The command exited 0 after 9,211 comparisons with zero mismatches. Full scope
and boundary results are in
[`evidence/02_differential.log`](/audit-output/evidence/02_differential.log).
This is finite fidelity evidence, not a substitute for the K proof.

Stage 2 result: **pass**.

## 3. Clean proof reconstruction

Only the copied source files were placed in scratch. Fresh K 7.1.293
definitions were built with:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition concrete-kompiled

kompile verification.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition proof-kompiled
```

Both exited 0. Tool versions and build logs are in
[`evidence/03_build.log`](/audit-output/evidence/03_build.log).

### Concrete generated-semantics reconstruction

[`evidence/03_semantics_differential.py`](/audit-output/evidence/03_semantics_differential.py)
embedded the freshly regenerated `solution.mpy` in each `Run` term and launched
the fresh LLVM definition. It compared each K result with both Python
implementations over 108 runs: 16 boundaries/examples, every string through
length 5, 25 seeded longer strings, and four length-200 cases. Every `krun`
exited 0 and all three results agreed. The normal, empty-loop, both-branch,
early-return, unmatched-suffix, nested, and long paths were exercised. See
[`evidence/03_semantics_differential.log`](/audit-output/evidence/03_semantics_differential.log).

### Positive target claims

The loop claim was proved independently:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC -I . \
  --claims SPEC.loop
#Top
exit=0
```

The candidate's exact second positive command then reused that exact claim as
the trusted lemma and proved every remaining claim:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC -I . \
  --trusted SPEC.loop
#Top
exit=0
```

I additionally selected `SPEC.main` together with `SPEC.loop`, trusted only the
already-proved loop label, and obtained `#Top`, exit 0. Each of the four ground
example claims was also selected independently and produced `#Top`, exit 0.
The complete record is
[`evidence/03_positive_claims.log`](/audit-output/evidence/03_positive_claims.log).

One diagnostic invocation selected `SPEC.main` but filtered `SPEC.loop` out
before trying to trust it; it kept unrolling and was interrupted. A concurrent
example launch also saw a transient Java startup error. Neither is a candidate
proof command, and both affected obligations were rerun successfully with the
proper selected claim set. They are retained transparently in
[`evidence/03_diagnostics.log`](/audit-output/evidence/03_diagnostics.log).

Stage 3 result: **pass**.

## 4. Adequacy and real-program pinning

### Claims in plain language

- `SPEC.loop`: for any K string suffix `S` and any nonnegative current count
  `N`, start at the real loop head with the exact real loop body and the real
  final return as continuation. Execution returns exactly
  `boolVal(bracketSpec(N,S))`. The function map is preserved and only the final
  local map is existential.
- `SPEC.main`: for every K string `S`, start from empty function and local
  maps, load and invoke `solutionProgram`, and return exactly
  `boolVal(bracketSpec(0,S))`.
- The four example claims require the exact Booleans for `"("`, `"()"`,
  `"(()())"`, and `")(()"`.

The return is never free, existential, or merely implied. Existential variables
occur only in the final `<functions>` and `<env>` cells.

### Satisfying states and concrete substitution

Every entry is satisfiable:

- For `SPEC.main`, choose `S = ""` and the literal empty initial maps.
- For `SPEC.loop`, choose `N = 0`, `S = ""`, current/original strings `""`,
  any function map (for example `.Map`), and the exact three-entry local map
  required by the claim. This satisfies `N >= 0`.
- Every example has its displayed ground string and literal empty initial
  maps.

Concrete substitution gives:

| `S` | `bracketSpec(0,S)` | canonical Python | generated Python | fresh K |
|---|---:|---:|---:|---:|
| `""` | true | true | true | true |
| `"("` | false | false | false | false |
| `")"` | false | false | false | false |
| `"()"` | true | true | true | true |
| `"(()())"` | true | true | true | true |
| `")(()"` | false | false | false | false |

The `bracketSpec` values follow directly from its four descending equations;
the three executable columns are recorded in the stage 2 and 3 differential
logs.

### Mechanical pinning

There are two independent links:

1. trusted translation regenerated `solution.mpy` byte-for-byte;
2. K's parser parsed the regenerated file as a `Pgm`, parsed the exact
   right-hand side of the unique `solutionProgram` equation as a K rule RHS,
   and JSON-compared the complete constructor trees.

[`evidence/04_program_pinning.py`](/audit-output/evidence/04_program_pinning.py)
reported `constructor_ast_identical: true`, exit 0. This comparison handles the
claim notation `.Stmts` and the translator's omitted empty list through K's
actual parsers; it is not a whitespace comparison. See
[`evidence/04_program_pinning.log`](/audit-output/evidence/04_program_pinning.log).

The entry function name, parameter binding, entire body, early return, loop,
and final return are therefore the submitted program. `solutionProgram` is
only a name for that term; it does not summarize execution.

### Body sensitivity

[`evidence/04_body_sensitivity.k`](/audit-output/evidence/04_body_sensitivity.k)
changes the constructor actually executed in `<k>` from initial `count = 0` to
`count = 1`, while retaining the original true result obligation for `S = ""`.
It dry-runs successfully, executes to `boolVal(false)`, and fails with
`WarnStuckClaimState`, exit 1. This is the expected semantic difference, not a
parse/build failure. See
[`evidence/04_body_sensitivity.log`](/audit-output/evidence/04_body_sensitivity.log).

Stage 4 result: **pass**.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`evidence/05_rule_inventory.md`](/audit-output/evidence/05_rule_inventory.md).
It enumerates every local syntax alternative, configuration cell, imported
module, all 32 ordinary rules in `semantic.k`, both local function
declarations, all five equations in `verification.k`, every attribute, and all
six claims. There are no generated helper K source files.

### Construct coverage and operational fidelity

Every submitted constructor maps to rules:

- module/function/parameter and statement-list handling: semantic rules
  S01–S06;
- literals, names, assignment: S07–S10 and S19–S21;
- `+` and `-` with left-to-right evaluation: S11–S14;
- integer/string `==`: S15–S18;
- `if`: S22–S24;
- expression evaluation and abrupt continuation discard for `return`:
  S25–S26;
- string `for`, first-character binding, exact body execution, and
  strict-suffix recurrence: S27–S32.

The existing-key/absent-key assignment rules are disjoint. The corresponding
loop-target rules are disjoint. Boolean branches are disjoint and exhaustive
over reachable guards. Integer arithmetic is arbitrary precision, matching
Python on this program. String operations are used only on the prompt's ASCII
alphabet. The only active state changes are function binding and local
binding; the program has no heap, I/O, allocation, nested call, or exception
effect to model.

Return discards the complete remaining continuation. That is exact for both
the nested early return and the final return in this single top-level call;
there is no caller frame in the submitted control flow.

### Verification extensions

`solutionProgram` is a zero-argument definitional summary with one covering,
unguarded equation. It names the mechanically identical AST and never replaces
an operational step.

`bracketSpec` is a result-bearing definitional summary:

- empty suffix: true iff depth is zero;
- leading `(`: remove it and add one;
- a non-`(` at zero: false;
- a non-`(` at positive depth: remove it and subtract one.

The guards are pairwise disjoint, recursion strictly shortens the string, and
the equations cover all states reachable from `N >= 0`. They are the standard
prefix-nonnegative/final-zero checker on the prompt alphabet. They do not
encode a finite test set or a fixed answer.

Most importantly, no operational bridge rewrites the loop or program call to
`bracketSpec`. Fixed semantics executes the exact body. The separately proved
universal `SPEC.loop` reachability claim is the connection theorem over all
`N >= 0`, all string suffixes, the exact continuation, and exact local
bindings. The main claim then reuses that proved theorem. There is no opaque
result symbol, task oracle, priority override, or result-fabricating rule.

### Nonfatal limitations

1. **Dead loop-target initialization.** S28/S29 bind `bracket` to `""` before
   checking whether the iterable is empty. Witness `S = ""`: Python performs
   no assignment to the loop variable, while K has a placeholder binding at
   loop exit. The variable is never read after the loop, each nonempty
   iteration overwrites it before use, and final locals are existential.
   Thus the variance cannot affect the returned Boolean or prove a false
   target conclusion. It is nevertheless an exact-Python state-model
   limitation.
2. **Over-broad `[total]` declaration.** The equations leave
   `bracketSpec(N,S)` without an equation when `N < 0`, `S` is nonempty, and
   its first character is not `(`. The concrete symbolic witness
   `bracketSpec(-1, ")")` remains unconstrained; a reachability claim assigning
   it `false` dry-runs but fails at the unresolved equality. See
   [`evidence/05_totality_probe.k`](/audit-output/evidence/05_totality_probe.k)
   and
   [`evidence/05_totality_probe.log`](/audit-output/evidence/05_totality_probe.log).
   No proof path can reach that gap because `SPEC.loop` requires `N >= 0`, an
   open increments it, a close at zero returns, and a close only decrements
   when `N > 0`.

Neither limitation is a materially unsound result rule. Both are recorded as
the reason for `CONCERNS` rather than hidden under a `PASS`.

Stage 5 result: **pass for the claimed return property, with the two stated
nonfatal limitations**.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to rely on. I authored
[`evidence/spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k). It executes
the real `solutionProgram` on `S = ""` from the normal empty maps and changes
only the destination from the true result to `boolVal(false)`.

The mutation's `--dry-run` exited 0, so it parses and builds. The proof run
exited 1 with `WarnStuckClaimState` after fixed execution reached:

```text
<k> boolVal ( true ) ~> .K </k>
```

against the false destination. The residual also contains the exact real
function body and reachable locals. This is the expected unmet result
obligation on a satisfying input, not an unrelated error or unreachable
mutation. Exact commands and bounded output are in
[`evidence/06_non_vacuity.log`](/audit-output/evidence/06_non_vacuity.log).

Stage 6 result: **pass**.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the freshly reconstructed K definition:

- for every K string `S`, executing the exact submitted constructor program
  from empty maps returns exactly `boolVal(bracketSpec(0,S))`, if it
  terminates;
- the loop connection holds for every suffix string and every nonnegative
  current count, not merely for fixed lengths or examples;
- on the prompt domain of strings over `(` and `)`, that recursive result is
  true exactly when every prefix has at least as many opens as closes and the
  final counts are equal;
- the four prompt examples have the stated results.

This is an unrestricted-domain partial-correctness proof, not bounded
unrolling. The operational loop and string suffix are symbolic.

### Trust ledger

| Boundary | Influence | Status and evidence |
|---|---|---|
| K 7.1.293 parser, kompilers, Haskell/LLVM backends, and reachability/circularity implementation | All parsing, execution, and proof closure | Necessary fixed toolchain trust. Versions and fresh builds recorded. |
| Imported K `INT`, `BOOL`, `STRING`, `MAP`, `K-EQUAL` primitives | Arithmetic, guards, characters/suffixes, and bindings | Acceptable external primitives. No candidate equation replaces them. Concrete boundary/long runs support their use on this ASCII task. |
| Trusted `/reference/py2mpy.py` | Python source to constructor AST | Launcher-designated trusted input. Fresh regeneration proves this translator produced the submitted bytes; relevant visitor cases map each used AST node directly. Universal translator correctness is outside the K theorem. |
| `solutionProgram` naming equation | Pins the body used by every entry claim | Formally/ mechanically checked constructor identity; body mutation changes execution and invalidates the result. |
| `bracketSpec` equations | Mathematical result named in the postcondition | Truthful descending equations on all reachable states. Exact fixed-execution connection is the separately proved `SPEC.loop` claim. Unreachable totality gap is disclosed. |
| `--trusted SPEC.loop` in the main proof run | Modular reuse of the invariant | The exact same immutable label/text was first selected alone and proved with `#Top`, exit 0. K does not certificate-link the two CLI invocations; the audit's hash/source identity and command ledger provide that link. |
| Natural-language/canonical-property bridge | Interprets `bracketSpec` as correct bracketing | Ordinary induction over the four equations plus inspection of trusted canonical code. The 9,211-case Python differential and 108-case K differential are finite corroboration only. |
| Partial-correctness termination boundary | The requested theorem is conditional on termination | Accepted because the task requests partial correctness. The concrete semantics also strictly removes one character per loop step, but no separate K termination theorem is claimed. |

### Excluded or abstracted behavior

- The source contract does not require non-string arguments or strings outside
  the `(` / `)` alphabet. The K theorem happens to treat every non-`(`
  character as a close, as both Python implementations do, but Unicode and
  out-of-contract exception behavior are not claimed as validated Python
  semantics.
- Final function-local binding identity is intentionally existential; only the
  returned Boolean is the HumanEval observable.
- The generated semantics is intentionally minimal and is not a reusable
  semantics for unrelated Python programs with nested calls, observable
  unbound-local behavior, exceptions, heaps, or I/O.
- Differential tests support fidelity only on their recorded finite scopes;
  they are not substituted for the symbolic K proof.

### Final decision

The reconstructed proof is sound for the result it claims, constrains that
result, executes and pins the real trusted-regenerated program, and covers the
entire material source-contract domain. No answer oracle, execution bypass,
bounded-size restriction, or materially unsound rule was found. The dead-local
initialization variance and unreachable totality gap are real but nonfatal
audit limitations, so the benchmark's `CONCERNS / LEGIT` category is the most
accurate result.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
