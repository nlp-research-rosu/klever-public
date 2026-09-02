# Independent adversarial audit: 15-string-sequence

This audit treats every item under `/candidate` as untrusted evidence. All
compilation and execution used source-only copies under
`/tmp/audit-work/rebuild`; candidate-provided `semantic-kompiled/`,
`verification-kompiled/`, bytecode, and caches were not used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
`/reference/prompt.py`, `/reference/canonical.py`, and
`/reference/py2mpy.py`; `/reference/reference-semantics` does not exist. This is
the required mount shape, so there is no infrastructure contradiction. See
[trusted_tree.log](/audit-output/evidence/trusted_tree.log).

### Candidate artifacts and untrusted generation claims

The following required generation artifacts are present as regular files, not
symlinks or mistyped entries: `run-input.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, the structured JSONL trace, `prompt.py`,
`py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`,
`spec.k`, and executable `prove.sh`. The original generation prompt did not
require `PROOF.md`; its absence is not a missing deliverable. `NOTES.md` was
conditional on a blocked proof and is likewise not required here.

The complete artifact/type listing is in
[provenance_tree.log](/audit-output/evidence/provenance_tree.log). Additional
candidate-built definitions, `__pycache__`, and cache/compiled files are present.
They are extra untrusted artifacts, were reported here, and were excluded from
the reconstruction.

The candidate prompt is byte-identical to the trusted prompt, and the candidate
translator is byte-identical to the trusted translator. Both `cmp` commands
exit 0 in [prompt_identity.log](/audit-output/evidence/prompt_identity.log) and
[translator_identity.log](/audit-output/evidence/translator_identity.log).
Their SHA-256 values also match the values claimed by `run-input.json`:

- prompt:
  `1eb46648867a6e499ee7e4fa6500b594937f325209204606d7391c8cad9df9c4`
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

See [provenance_hashes.log](/audit-output/evidence/provenance_hashes.log) and
[run_input.log](/audit-output/evidence/run_input.log). The separate instruction
prompt hash in `run-input.json` cannot be checked because that instruction file
is not a trusted mount; it is not used as proof evidence.

I read `run-input.json`, `metrics.json`, both prose logs, and all 172 JSONL trace
records solely as claims. Bounded summaries are preserved in
[untrusted_generation_summary.log](/audit-output/evidence/untrusted_generation_summary.log)
and
[generation_trace_summary.log](/audit-output/evidence/generation_trace_summary.log).
The prior reports claim successful `krun`/`kprove`; none of those claims was
relied upon.

Result: no missing, changed, mistyped, or symlinked required artifact, and no
semantics-mode infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks for `string_sequence(n: int) -> str`: return the
space-delimited decimal integers from `0` through `n`, inclusive. The examples
are `0 -> "0"` and `5 -> "0 1 2 3 4 5"`. The trusted canonical implementation
is `' '.join(str(x) for x in range(n + 1))`; consequently negative integers
produce the empty string.

`solution.py` implements the same behavior with a negative branch, accumulator
`"0"`, and a loop from `i = 1` while `i <= n`. Its branch boundaries are:

- `n < 0`: return `""` immediately;
- `n = 0`: skip the loop and return `"0"`;
- `n >= 1`: append exactly `" " + str(i)` for `i = 1..n`.

I regenerated the MPY term from the copied `solution.py` using the trusted
translator:

`python3 py2mpy.py solution.py > regenerated-solution.mpy`

The command exits 0, and `cmp -s regenerated-solution.mpy
submitted-solution.mpy` exits 0. Both files have SHA-256
`11366253bbb1d88f6881db189674885fb00045eb3fa69b16ad69c45d07077774`.
See [regenerate_mpy.log](/audit-output/evidence/regenerate_mpy.log),
[mpy_byte_identity.log](/audit-output/evidence/mpy_byte_identity.log), and
[mpy_hashes.log](/audit-output/evidence/mpy_hashes.log).

The independent differential harness imports the trusted canonical entry point
and the copied candidate entry point. It covers the documented examples,
negative/zero/one-iteration boundaries, decimal-width boundaries, every integer
in `[-128, 256]`, and 500 deterministic generated integers in `[-1000, 1000]`.
There were 738 distinct inputs and zero mismatches. The executable harness and
full input construction are
[differential_test.py](/audit-output/evidence/differential_test.py); the exact
command, scope, exit 0, and summary are in
[differential_test.log](/audit-output/evidence/differential_test.log).

Result: the Python implementation agrees with the trusted canonical on all
independently tested intended inputs, and the submitted MPY is the exact trusted
translation of that implementation.

## 3. Clean proof reconstruction

The toolchain used was K v7.1.293 and Python 3.10.12; exact paths and versions
are in [toolchain_versions.log](/audit-output/evidence/toolchain_versions.log).

### Fresh concrete definition

From the source-only scratch copy I ran:

`kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-llvm-kompiled`

It exits 0; see
[kompile_semantic_llvm.log](/audit-output/evidence/kompile_semantic_llvm.log).
Fresh `krun` executions of the regenerated real program were then compared
automatically with both Python implementations at `n = -3, -1, 0, 1, 5, 12`.
All six K runs exit 0 and all values agree, including the negative return, the
zero-iteration loop, a one-iteration loop, the documented example, and a
multi-digit result. See
[concrete_semantics_compare.py](/audit-output/evidence/concrete_semantics_compare.py)
and
[concrete_semantics_compare.log](/audit-output/evidence/concrete_semantics_compare.log).

Two initially parallelized `krun` launches produced transient K temporary
parser/Java-launcher failures. They are preserved in
`krun_neg3_parallel_failure.log` and `krun_0_parallel_failure.log`. Sequential
reruns both exit 0, and the later six-input sequential comparator also exits 0.
Those transient launcher results are not treated as candidate evidence or a
candidate defect.

### Fresh proof definition and positive claims

I ran:

`kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-haskell-kompiled`

It exits 0; see
[kompile_verification_haskell.log](/audit-output/evidence/kompile_verification_haskell.log).
The original, unchanged `spec.k` then produces `#Top` and exit 0:

`kprove spec.k --definition verification-haskell-kompiled --spec-module SPEC`

See [kprove_all_claims.log](/audit-output/evidence/kprove_all_claims.log).

I also isolated the claims with
[positive-claims.k](/audit-output/evidence/positive-claims.k). The loop claim
was run alone. Each entry claim was run with the exact loop claim it depends on
as a circularity. Every command prints `#Top` and exits 0:

| Target | Evidence |
|---|---|
| Loop invariant | [kprove_loop_claim.log](/audit-output/evidence/kprove_loop_claim.log) |
| Universal entry | [kprove_universal_entry.log](/audit-output/evidence/kprove_universal_entry.log) |
| `n = 0` entry | [kprove_example_zero.log](/audit-output/evidence/kprove_example_zero.log) |
| `n = 5` entry | [kprove_example_five.log](/audit-output/evidence/kprove_example_five.log) |

An earlier auditor-created split omitted the loop circularity and was
interrupted while unrolling; that diagnostic is preserved as
`kprove_universal_without_loop_interrupted.log`. It is not a failure of any
candidate claim: the original specification includes the dependency, and the
correctly isolated universal entry plus that dependency closes.

Result: the clean concrete reconstruction works, and every positive target
claim closes independently with its actual dependencies.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each claim

1. **Loop claim (`spec.k:6`)**: from a state with integer `i = I >= 1`,
   integer `n = N >= 0`, and string accumulator `S`, executing the exact target
   `while i <= n` loop reaches its continuation. It preserves `n`, the rest of
   the environment, functions, and stack; sets `i` to the first reached integer
   greater than `N`; and appends the decimal strings for `I..N` to `S`.
2. **Universal entry (`spec.k:26`)**: for every mathematical K integer `N`,
   running the target module from empty environment/function/stack cells returns
   `sequence(N)` and installs exactly the target function.
3. **Example entry (`spec.k:35`)**: at `N = 0`, it returns `"0"`.
4. **Example entry (`spec.k:45`)**: at `N = 5`, it returns
   `"0 1 2 3 4 5"`.

### Pinning to the submitted MPY

The entry claim does not use an oracle for the body. `targetProgram()` rewrites
to `Module(FuncDef("string_sequence", Params("n"), targetBody()))`, and
`targetBody()` rewrites to the complete submitted statement sequence. Comparing
`verification.k:29-53` with the numbered submitted term in
[numbered_solution_mpy.log](/audit-output/evidence/numbered_solution_mpy.log)
shows exact constructor identity: negative `If`, both initial assignments,
the precise `While` condition and two-statement body, and final `Return`.
The trusted translation identity established in stage 2 pins that term to
`solution.py`.

The `<k>` cell therefore reduces the helper to the same MPY AST before `init`
executes it; it is an exact syntax name, not a substituted algorithm or
result-bearing abstraction. As an additional finite check, I built a separate
LLVM executable whose syntax includes the verifier helpers and concretely ran
`targetProgram()` at `-1`, `0`, and `5`. Its final function body and results are
the same as the actual MPY runs. See
[kompile_verification_exec_llvm.log](/audit-output/evidence/kompile_verification_exec_llvm.log)
and `krun_target_program_neg1.log`, `krun_target_program_0.log`, and
`krun_target_program_5.log`.

The first helper-execution attempt used the proof definition's deliberately
restricted `MPY-SYNTAX` runtime parser, which cannot parse the reviewer-only
`targetProgram()` token; that parser failure is preserved in
`krun_target_program_mpy_parser_expected_failure.log`. Recompiling the same
source with `VERIFICATION` as the syntax module made the helper parse and
execute. This was a test-harness parser choice, not a target execution failure.

### Satisfiable witnesses and result constraint

Every starting condition is realizable:

| Claim | Satisfying starting state | Claimed/concrete result |
|---|---|---|
| Loop | `<k> exec(While(...)) ~> .K`, env `i=1, n=0, result="0"`, empty rest/functions/stack | zero iterations; `i=1`, result `"0"` |
| Universal | `N=-1`, empty env/functions/stack | `sequence(-1)=""`; both Python implementations return `""` |
| Example 0 | exact initial cells at `N=0` | `"0"` in K and both Python implementations |
| Example 5 | exact initial cells at `N=5` | `"0 1 2 3 4 5"` in K and both Python implementations |

The universal destination is the concrete value
`SVal(sequence(N))`; `sequence` has disjoint equations fixing a string for both
`N < 0` and `N >= 0`. There is no right-only free result variable, tautological
postcondition, or one-way implication. The functions cell is also constrained
to contain the exact function, while the empty caller environment and stack are
restored.

Result: all preconditions are satisfiable, helper/control-flow claims match the
real program, and the theorem constrains the intended returned value.

## 5. Rule-by-rule static soundness review

The source inventory with line numbers is preserved in
[numbered_semantic_k.log](/audit-output/evidence/numbered_semantic_k.log),
[numbered_verification_k.log](/audit-output/evidence/numbered_verification_k.log),
[numbered_spec_k.log](/audit-output/evidence/numbered_spec_k.log), and
[local_declaration_inventory.log](/audit-output/evidence/local_declaration_inventory.log).
There are no additional candidate helper K source files.

### Local syntax and configuration inventory

`MPY-SYNTAX` declares every source constructor used by the submitted term:

- `Module(Stmts)` and the empty-delimiter `Stmts` list;
- statements `FuncDef`, `Assign`, `If`, `While`, and `Return`;
- one-string `Params`;
- expressions `Int`, `Str`, `Name`, `BinOp`, `Compare`, and `Call`;
- `CmpOp(String, Expr)`.

`MPY` declares all runtime data and continuations:

- values `IVal`, `SVal`, and `BVal`;
- `function(String, Stmts)` and `frame(Map, K)`;
- K items `init`, `run`, `exec`, `eval`, `store`, `binLeft`, `binRight`,
  `cmpLeft`, `cmpRight`, `ifGuard`, `whileGuard`, `call`, `toStr`,
  `returning`, and `functionEnd`.

The configuration has exactly the state needed here: computation `<k>`, local
bindings `<env>`, function definitions `<functions>`, and call frames `<stack>`.
No heap, allocation, I/O, or exception cell is needed by this program.

`verification.k` adds exactly eight `[function]` symbols:
`sequenceFrom`, `sequence`, `indexAfter`, `loopCondition`, `loopBody`,
`targetBody`, `targetFunction`, and `targetProgram`. There are no `[total]`,
`[functional]`, opaque, priority, simplification, macro, or `owise`
declarations in local source. Attributes therefore do not smuggle a proof
equation.

### All 31 operational rules in `semantic.k`

| Lines | Rule(s) and decision |
|---|---|
| 64-66 | `init(Module(SS),N)` runs the actual module statements, then calls `string_sequence(N)`. Exact for the selected entry point. |
| 68 | Empty statement sequence becomes `.K`. Sound. |
| 69 | A nonempty sequence executes its head before its tail. Sound left-to-right statement order. |
| 71-72 | `FuncDef` installs the submitted parameter/body in the function map. Sound for a module-level capture-free function. |
| 74 | Assignment evaluates its RHS before storing. Sound. |
| 75-76 | Existing-key store updates that binding. Sound. |
| 77-79 | Absent-key store inserts it, guarded by `notBool (X in_keys(ENV))`. Sound and disjoint from the preceding update rule. |
| 81-82 | `While` evaluates its condition before dispatch. Sound. |
| 83-84 | True loop guard executes the body, then repeats the same loop. Sound. |
| 85 | False loop guard exits. Sound. |
| 87-88 | `If` evaluates its condition first. Sound. |
| 89 | True guard schedules only the then statements. Sound. |
| 90 | False guard schedules only the else statements. Sound. |
| 92 | `Return` evaluates its expression before returning. Sound. |
| 93-95 | A returned value discards remaining callee computation, restores the saved caller environment/continuation, and pops one frame. This matches Python return control for every target path. |
| 97 | `Int(I)` becomes `IVal(I)`. Sound. |
| 98 | `Str(S)` becomes `SVal(S)`. Sound. |
| 99-100 | `Name(X)` looks up the current environment. Sound for all target names. |
| 102 | `BinOp` schedules its left operand first. Sound. |
| 103 | After the left value, it evaluates the right operand. Sound left-to-right evaluation. |
| 104 | Integer `"+"` uses `+Int` with operand order `I1 + I2`. Sound. |
| 105 | String `"+"` uses `+String` with operand order `S1 + S2`. Sound. |
| 107-108 | `Compare` schedules its left expression first. Sound. |
| 109 | `<=` then schedules its right expression. Sound. |
| 110 | `<=` returns `I1 <=Int I2`. Sound. |
| 111 | `<` then schedules its right expression. Sound. |
| 112 | `<` returns `I1 <Int I2`. Sound. |
| 114 | The target's builtin `str` call evaluates its one argument first. Sound for the unshadowed builtin used by this program. |
| 115 | Integer conversion uses fixed K `Int2String`. Sound for target loop indices. |
| 117-119 | A non-`str` user call evaluates its argument only when that function exists. The guard makes it disjoint from the builtin rule. Sound for `string_sequence`. |
| 120-124 | Call activation installs the parameter binding, saves caller environment and exact continuation, and executes the stored body. Sound for the one-argument target function. |

The negative concrete run exercises abrupt return and proves the post-`If`
statements are not accidentally executed. Positive runs exercise insertion and
update stores, both comparison operators, integer and string addition,
`Int2String`, repeated loop control, and normal return. Final configurations show
the caller environment and stack restored.

`functionEnd()` deliberately has no rule. It would visibly stop a function that
falls through, but it is unreachable in the submitted body: the negative branch
returns and every nonnegative path reaches the final return. Likewise, syntax
may parse unsupported operator strings or programs that shadow `str`; those
unused programs can stick or fall outside this target-specific model. No
integer input to the submitted fixed program reaches such a case, so this is
minimal generated-semantics coverage rather than a false conclusion on the
intended domain.

### All 11 proof-helper rules in `verification.k`

| Lines | Rule(s) and decision |
|---|---|
| 15-19 | The two `sequenceFrom` equations append the current decimal integer and increment when `I <= N`, otherwise return `S` when `I > N`. Guards are exhaustive/disjoint over integers; recursion strictly decreases `N-I`. Truthful definitional summary. |
| 21-22 | `sequence(N)` is `""` for `N < 0` and starts at `(1,N,"0")` for `N >= 0`. Guards are exhaustive/disjoint and match the trusted canonical. |
| 24-27 | `indexAfter` increments while `I <= N` and otherwise returns `I`. Exhaustive/disjoint; recursion descends on the same finite distance in every proof use. |
| 29-30 | `loopCondition()` expands to the exact submitted `i <= n` AST. Sound syntax name. |
| 32-39 | `loopBody()` expands to the exact two submitted assignments, in order. Sound syntax name. |
| 41-49 | `targetBody()` expands to the exact complete submitted body. Sound syntax name. |
| 51 | `targetFunction()` is the exact parameter and target body. Sound syntax name. |
| 52-53 | `targetProgram()` is the exact module/function AST. Sound syntax name. |

The result-specific `sequence*` functions never rewrite an executing MPY term.
They occur in the loop/entry destinations, while the left side executes the
ordinary rules above. The loop reachability claim is the machine-checked
connection between real iterations and `sequenceFrom`; using the same summary
in the entry postcondition does not bypass execution.

### Construct coverage, overlap, and trust checks

Every submitted constructor maps to both syntax and behavior: `Module` to
`init/run`; `FuncDef/Params` to function installation and activation;
`If/Compare(<)` to guarded negative control; `Assign/Name/Int/Str` to
environment and literal rules; `While/Compare(<=)` to repeated guarded control;
`BinOp("+")` to typed integer/string addition; `Call(Name("str"),...)` to
`Int2String`; and `Return` to frame restoration.

Rule overlaps are controlled: store update versus insert is separated by map
membership; boolean branches are disjoint; integer versus string addition is
sort-disjoint; `<` versus `<=` is operator-disjoint; builtin versus user call is
guard-disjoint. The proof functions' integer guards are exhaustive and
pairwise disjoint. There are no priorities or simplifications whose precedence
could conceal an overlap.

No rule encodes the task answer in operational semantics, replaces
program-defined execution with an oracle, fabricates a value for an unmodeled
used construct, or drops an observable target state change. I found no unsound
local rule; therefore there is no claimed unsoundness requiring a false
conclusion witness. The narrower unsupported-language cases described above do
not yield a false conclusion for any intended integer input to this submitted
program.

Result: static soundness gate passes.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k). It retains the exact
loop claim/circularity and changes only the `n = 5` result obligation from the
true `"0 1 2 3 4 5"` to the false `"0 1 2 3 4 6"`. The initial state at
`n = 5` is satisfiable, and both trusted canonical and candidate Python
execution demonstrate why the mutation is false.

First:

`kprove spec-vacuity.k --definition verification-haskell-kompiled --spec-module SPEC-VACUITY --dry-run --output none`

successfully compiles the mutation and exits 0; see
[vacuity_dry_run.log](/audit-output/evidence/vacuity_dry_run.log).

Then the same command without `--dry-run --output none` exits 1 with
`WarnStuckClaimState`. Its residual is the completely executed real program
with `<k> SVal("0 1 2 3 4 5")`, which cannot unify with the mutated destination.
See
[vacuity_false_result.log](/audit-output/evidence/vacuity_false_result.log).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

Result: the proof is fresh-mutation non-vacuous and result-sensitive.

## 7. Proven-versus-assumed accounting

### What the reachability proof establishes

Under the audited MPY semantics and imported K primitives, for every K integer
`N`, if execution of the exact translated target program terminates, it returns:

- `""` when `N < 0`;
- `"0"` followed by `" " + Int2String(i)` for every integer `i` from `1`
  through `N` when `N >= 0`.

It also establishes the loop summary stated in stage 4 and the two ground
examples. This is a partial-correctness theorem; termination itself is not part
of the claimed result, even though the source loop plainly advances toward its
bound for all integer inputs.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| K parser/compiler, Haskell/LLVM backends, and reachability prover | All compiled rules and `#Top` results | Necessary fixed toolchain trust; fresh builds, isolated claims, concrete runs, and false mutation provide independent sensitivity checks. |
| Imported `INT`, `STRING`, `BOOL`, `MAP`, and `LIST` domains | Arithmetic comparisons/addition, decimal conversion, concatenation, environments, function map, and call stack | Acceptable low-level language primitives. No task-specific conclusion is hidden in them. |
| `Int2String` | Every appended decimal value and final result | Fixed external K primitive, used only on positive loop integers. Checked concretely across one- and multi-digit cases and indirectly over 738 Python differential inputs. |
| Trusted `py2mpy.py` | Python-to-MPY syntax bridge | Trusted mounted input; byte identity with candidate copy and regenerated MPY identity are established. It contributes syntax, not the result theorem. |
| Generated MPY semantics | Binding, evaluation, control, and state model | Not assumed merely from candidate prose: rebuilt, exercised on all target constructs/boundaries, and audited rule by rule in stage 5. |
| Natural-language/canonical bridge | Meaning of “0 up to n inclusive,” including negative behavior | The canonical implementation is a trusted input. Source inspection plus the independent 738-input differential test supports the bridge; finite tests are evidence, not a replacement for the K proof. |

There are no opaque symbols, fresh result oracles, assumed proof claims,
trusted task-specific rewrite rules, empirical operational bridges, or
simplification lemmas. `sequence`, `sequenceFrom`, and `indexAfter` are
truthfully defined mathematical functions; the K loop proof, not differential
testing, connects actual execution to them.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(auditability/trust) all pass. The handwritten semantics is intentionally
target-subset semantics rather than full Python, but it soundly covers every
construct and binding exercised by the fixed submitted program on the intended
integer domain. That excluded unused-language surface is not a material
adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
