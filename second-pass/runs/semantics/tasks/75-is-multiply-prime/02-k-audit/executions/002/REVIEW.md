# Independent adversarial audit: 75-is-multiply-prime

## Outcome

The candidate contains a legitimate partial-correctness proof for the submitted
program over the intended integer contract `a < 100`.

The proof was rebuilt from source without candidate caches. All eleven positive
target modules exited 0 and printed `#Top`. The proof harness mechanically pins
the exact trusted-translator output, executes the ordinary supplied call/loop/
integer semantics, and constrains every result through an equality checkpoint.
It covers the unbounded `A < 2` tail symbolically and covers each integer 2
through 99 exactly once. A fresh false-result mutation built successfully and
became stuck at the expected reachable mismatch.

The `validating-proof` extension audit has Gate A (real-program soundness), Gate
B (intent adequacy), and Gate C (trust/evidence auditability) all passing. No
candidate-local oracle, task-answer rewrite, body replacement, materially
narrowed domain, or false semantic rule contributes to closure.

## 1. Input and provenance integrity

Status: PASS.

I first read `/audit-input.json`. It declares:

- problem `75-is-multiply-prime`;
- condition `semantics`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- `record_layout: legacy-selected-stage1`;
- complete launcher provenance and a `container_paths` map.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` exists as a real directory, as required in
this mode. The campaign lock is a regular non-symlinked file. Its actual
SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the recorded hash, and its parsed JSON is structurally identical
to the `audit_campaign` block.

All launcher-declared container mounts exist, are readable, and are
non-symlinked. All records required by `legacy-selected-stage1` are regular
readable files (or, for the trace, a real readable directory):

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`
- `/generation-evidence/usage.json`, which is present and was inspected

The optional imported `legacy-metrics.json` and `legacy-run-input.json` were
also inspected. There is no `runtime-metrics.json`; that historical record is
not required for this declared layout, so its absence is not a defect.

Every launcher-recorded leaf-file hash checked by the reviewer matches,
including the run/task/result/invocation/metrics/usage records, prompt,
canonical, translator, generation log, last message, and campaign lock. The
generation-result evidence map and invocation evidence map are identical, and
each listed evidence file has the declared hash. The structured trace consists
of one regular JSONL file under real directories; the declared and actual file
sets and file hash match. Independent same-format aggregate hashes match the
recorded generation workspace, supplied-semantics manifest, and structured
trace hashes.

The full candidate tree contains only regular files and real directories—no
symlink or special entry. Its required proof artifacts `solution.py`,
`solution.mpy`, `verification.k`, `spec.k`, and `prove.sh` are all present as
regular files.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. I recursively compared all 25 entries in the candidate and trusted
`reference-semantics/` trees by relative path, entry type, and file SHA-256.
They are exactly identical: no missing, additional, changed, mistyped, or
symlinked entry exists.

The generation log and structured trace claim a successful eleven-part proof,
but those claims were not used as proof evidence. The commands were
independently reconstructed below.

Evidence:

- `evidence/stage1/provenance-integrity.log`
- `evidence/stage1/verify_provenance.py`
- `evidence/stage1/required-records.log`
- `evidence/stage1/json-records.log`
- `evidence/stage1/inspect_records.sh`
- `evidence/stage1/optional-legacy-records.log`

No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

### Contract and implementation

The trusted prompt asks for `is_multiply_prime(a)` to return true exactly when
the given number is a product of three prime numbers, with `a < 100`; the
example is `30 = 2 * 3 * 5`. Prime numbers and the canonical implementation
make the intended input domain integers. Repetition is allowed: the canonical
triple loops can choose the same prime more than once.

The candidate uses trial division. It repeatedly divides out one prime factor,
counting multiplicity, then counts a remaining factor greater than one and
tests whether the final count is three. Mutating its local parameter `a` does
not alter the caller-visible integer input.

### Trusted translation

I copied only source artifacts to
`/tmp/audit-work/75-is-multiply-prime`, using the trusted supplied-semantics
tree rather than any candidate build output. Running:

```text
python3 /tmp/audit-work/75-is-multiply-prime/py2mpy.py \
  /tmp/audit-work/75-is-multiply-prime/solution.py
```

produced SHA-256
`23a0c4bb78ab970ac38d92b0bb40a53cee89553a69e0ef1e345a9f445f1670ba`,
identical to the submitted `solution.mpy`; `cmp` exited 0.

### Independent differential test

The reviewer-authored script imports `/reference/canonical.py` and the scratch
copy of the submitted `solution.py`. It also uses an independently written
prime-factor-count oracle. The input set contains:

- every integer from -128 through 99;
- the documented example 30;
- named witnesses for every source branch and boundary, including negative,
  0, 1, loop initially false, first loop entry, divisible/remainder branches,
  repeated factors, and final true/false cases;
- 256 deterministic generated large negative integers.

There is no collection-valued “empty” input in this integer contract; zero is
the relevant neutral/boundary case. The run checked 485 inputs and found zero
canonical/generated/mathematical mismatches. This is finite empirical evidence,
not a substitute for the K proof.

Evidence:

- `evidence/stage2/source-inspection.log`
- `evidence/stage2/scratch-and-translation.log`
- `evidence/stage2/differential_test.py`
- `evidence/stage2/differential-test.log`

## 3. Clean proof reconstruction

Status: PASS.

No candidate `*-kompiled` directory or cache was copied. The fresh scratch
directory initially contained no compiled definition. The independently
installed tools report K version 7.1.293 for `kompile`, `krun`, and `kprove`;
Python is 3.10.12.

### Concrete definition

The fresh LLVM build command was:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. A freshly translated concrete harness then ran under that
definition and terminated with `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. This is only a concrete check.

The LLVM compiler reported non-exhaustive warnings in unused float, string,
subscript, and map helpers. Those helpers do not occur in the submitted
program's proof dependency slice. The proof build itself reported only unused
variable warnings in two supplied string-order rules.

### Proof definition

The fresh Haskell build command was:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

It exited 0.

I then invoked `kprove` independently for every positive target module:

| Module | Formal input portion | Result |
|---|---|---|
| `SPEC-NEGATIVE` | symbolic `A:Int`, `A <Int 2` | exit 0, one `#Top` |
| `SPEC-02-11` | 2–11 | exit 0, one `#Top` |
| `SPEC-12-21` | 12–21 | exit 0, one `#Top` |
| `SPEC-22-31` | 22–31 | exit 0, one `#Top` |
| `SPEC-32-41` | 32–41 | exit 0, one `#Top` |
| `SPEC-42-51` | 42–51 | exit 0, one `#Top` |
| `SPEC-52-61` | 52–61 | exit 0, one `#Top` |
| `SPEC-62-71` | 62–71 | exit 0, one `#Top` |
| `SPEC-72-81` | 72–81 | exit 0, one `#Top` |
| `SPEC-82-91` | 82–91 | exit 0, one `#Top` |
| `SPEC-92-99` | 92–99 | exit 0, one `#Top` |

Each individual log records its exact working directory, shell-escaped command,
bounded output, and exit status.

Evidence:

- `evidence/stage3/toolchain.log`
- `evidence/stage3/kompile-llvm.log`
- `evidence/stage3/concrete-smoke.log`
- `evidence/stage3/kompile-haskell.log`
- `evidence/stage3/run_positive_claims.sh`
- `evidence/stage3/positive-claims/`

## 4. Adequacy and real-program pinning

Status: PASS.

### Plain-language claim meanings

Every entry claim begins in the explicit standard state: module scope 0 with
parent builtins scope -1, empty heap and stack, `scopeLoc` 1, `heapLoc` 0,
`noRet`, `NoExc`, and exit code 0.

`SPEC-NEGATIVE` says: for any K integer `A < 2`, load the submitted function,
call it with `A`, and finish with exactly Boolean `false`, restoring the
harness state. A concrete satisfying witness is `A = -7`; both Python
implementations return false.

Each other module has a ground, hence satisfiable, initial configuration and
sequences ordinary calls with equality checkpoints. Together they say: for
each integer 2 through 99, the submitted function returns the listed exact
Boolean, and all calls finish with the state restored. There is no implication
whose consequent can be avoided and no free result variable.

A mechanical parser found 98 concrete checkpoints, with 98 unique inputs in
the exact order 2 through 99. Every listed result agrees with both Python
implementations.

### Mechanical program identity

The rule for `#runIsMultiplyPrime` expands to:

1. `#loadAll(Module(...))`;
2. ordinary `Call(Name("is_multiply_prime"), Int(A))`;
3. a ghost cleanup marker.

The reviewer mechanically extracted the exact `Module(...)` argument from
`verification.k` lines 19–46. The only external-parser normalization replaces
one explicit internal empty-list spelling `.Stmts` with the equivalent blank
external list syntax. Parsing both that extracted term and the freshly
regenerated `solution.mpy` as sort `Module` produced KORE files with identical
SHA-256:

`5f7079cc87f76343261bd06e98cf142dd9da6b4b5bd8060f3e420e2042ca4167`.

`cmp` exited 0. Thus the claim executes the same constructor-level function
binding and body as the trusted translator output; it is not a substituted
program or a result summary.

### Result and body sensitivity

The checkpoint rule is:

```text
rule <k> B:Bool ~> #expect(B) => .K ... </k>
```

The repeated K variable forces exact Boolean equality. A wrong result remains
stuck.

For an independent body-sensitivity test, I changed the actual embedded body
from `factor_count == 3` to `factor_count == 4`, renamed the verification
module, and rebuilt a separate Haskell definition. The build exited 0. Proving
the true obligation for input 8 then exited 1 with `WarnStuckClaimState` and
the exact residual:

```text
false ~> #expect ( true ) ~> .K
```

This mutation changes the program term actually executed by the claim, not an
external source file.

Evidence:

- `evidence/stage4/program-pinning.log`
- `evidence/stage4/extract_embedded_module.py`
- `evidence/stage4/pinning_check.sh`
- `evidence/stage4/solution-module.kore`
- `evidence/stage4/embedded-module.kore`
- `evidence/stage4/spec_coverage.py`
- `evidence/stage4/spec-coverage.log`
- `evidence/stage4/verification-body-mutant.k`
- `evidence/stage4/spec-body-mutant.k`
- `evidence/stage4/body-mutant-build.log`
- `evidence/stage4/body-mutant-proof.log`

## 5. Rule-by-rule static soundness review

Status: PASS.

### Exhaustive inventory

The reviewer inventoried the trusted supplied semantics, every helper K file,
`verification.k`, and all claims in `spec.k`. Multi-line declarations and
rules were reconstructed as single entries. The inventory contains:

- 1,145 total structural/declaration/rule/claim entries;
- 698 rules;
- 228 syntax declarations;
- 145 function declarations;
- 107 total declarations;
- zero `[functional]` and zero `[simplification]` entries;
- 35 concrete rules;
- 25 symbolic declarations, including 22 `no-evaluators` boundaries;
- 45 priority rules;
- 26 `owise` rules;
- all five syntax macros/macro-recursive declarations;
- all eleven target claims.

Each row records its source, exact line range, complete declaration or rule
including guards/attributes, classification, and decision. The full artifact
is `evidence/stage5/rule-inventory.md`; the generator is preserved alongside
it.

### Submitted-program dependency slice

Every constructor in `solution.mpy` was mapped to its declaration and rules:
`Module`, `FuncDef`, `Params`, docstring `Expr`/`Str`, `Assign`, `Name`, `Int`,
`While`, `If`, `AugAssign`, `BinOp`, `Compare`/`CmpOp`, and `Return`. The
wrapper additionally uses an ordinary `Call`.

The used fixed rules provide:

- module loading and ordered statement sequencing;
- exact closure creation and lexical name lookup;
- left-to-right expression and call-argument evaluation;
- a fresh call frame, parameter binding, stack continuation, return, frame
  deallocation, and environment/scope restoration;
- ordinary integer multiplication, addition, floored remainder/division, and
  comparisons;
- complementary while/if true and false branches;
- strict return-expression evaluation.

The only mutable program state is the fresh call-frame map. The heap stays
empty. `factor` starts at 2 and only increases, so the used `%` and `//`
operations never have a zero divisor. Cell/ref priority alternatives have
false guards because the frame contains plain integers and no `$cells` marker.
The used true/false guards are complementary, and operator-string cases are
disjoint. The generic call rule selects the closure obtained by ordinary name
lookup; there is no name-based call interception.

### Candidate-local extensions

`verification.k` adds one syntax declaration and three rules:

1. `#runIsMultiplyPrime(A)` is a harness expansion, not a body summary. It
   preserves the surrounding continuation and expands to exact module loading,
   ordinary lookup, and ordinary fixed-semantics call execution.
2. `#expect` is an equality checkpoint. It provides no value equation and
   cannot match opposite Booleans.
3. `#forgetEntryPoint` is guarded ghost cleanup after a Boolean return. It
   removes only the harness-installed module binding and preserves every other
   cell and any trailing continuation. It neither fabricates a result nor
   introduces abrupt control.

No candidate-local rule has a function, total, functional, simplification,
concrete, opaque, priority, or `owise` attribute. `verification.k` contains no
prime predicate, factor-count summary, input-result table, loop shortcut,
unconstrained oracle, or task-answer rewrite. Expected Booleans occur only in
the target claims, where they are obligations after actual execution.

### Supplied partial-semantics boundaries

The exhaustive inventory identifies opaque float operators, opaque
`sortVS`/`sortKeyVS`, opaque `md5hexCodes`, concrete-only evaluators,
total-but-partial sequence access, and subset models for unused language
features. None of those symbols or their dispatch paths occurs in the submitted
module, wrapper, or target claims. The proof imports `MPY`, not `MPY-KRUN`, so
`MPY-CONCRETE` is also excluded from symbolic execution.

I do not label these unused boundaries globally sound for full Python, nor do I
label them unsound without the required false-conclusion witness. The narrower
finding is that they are unreachable and have no dependent target claim. No
opaque or fresh symbol influences a branch, result, state, exception, or
postcondition in this proof.

No rule contributing to closure admits a false conclusion witness on the
intended domain.

Evidence:

- `evidence/stage5/full-source-review.log`
- `evidence/stage5/source-counts.log`
- `evidence/stage5/rule_inventory.py`
- `evidence/stage5/rule-inventory.md`
- `evidence/stage5/used-fragment-review.md`
- `evidence/stage5/static_dependency_check.sh`
- `evidence/stage5/static-dependency-check.log`

## 6. Fresh non-vacuity test

Status: PASS.

I did not rely on any candidate mutation artifact. The fresh reviewer mutation
keeps the original program and semantics but changes a reachable,
result-constraining obligation:

```text
#runIsMultiplyPrime(8) ~> #expect(false) => .K
```

Input 8 satisfies the original claim's ground precondition and is a product of
three primes (`2 * 2 * 2`); both Python implementations return true.

First, `kprove ... --dry-run` exited 0, demonstrating that the mutation parses
and builds against the reconstructed definition. The actual proof command then
exited 1 with `WarnStuckClaimState`, not a parser error, timeout, missing
import, or unrelated crash. Its residual is:

```text
true ~> #expect ( false ) ~> .K
```

The remaining cells are the expected restored initial cells. This is the
precise unmet result obligation.

Evidence:

- `evidence/stage6/spec-vacuity-audit.k`
- `evidence/stage6/vacuity-dry-run.log`
- `evidence/stage6/vacuity-proof.log`

## 7. Proven versus assumed accounting

Status: PASS.

### What the K proof establishes

Under the exact supplied MPY semantics and explicit initial cells, the
reachability proof establishes partial correctness of the exact submitted
constructor program:

- for every K integer `A < 2`, the call result is exactly `false`;
- for every integer 2 through 99, the result is exactly the Boolean listed in
  `spec.k`;
- each call returns normally through the ordinary closure/frame semantics,
  reaches the equality checkpoint, and restores the specified caller cells.

The true inputs are exactly:

```text
8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50,
52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99
```

An independent definition-level enumeration generated all primes 2 through 99
and all products of three such primes below 100. Its product set is exactly the
spec's true set. Every prime is at least 2, so any product of three primes is at
least 8; this discharges the intended-property bridge for the symbolic `A < 2`
tail by ordinary mathematics. The table bridge is exhaustive for the remaining
finite contract portion, not a sample.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Trusted prompt, canonical, translator, and supplied-semantics mounts | Defines source intent, translation, and fixed execution model | Launcher provenance, hashes, and recursive type/byte comparisons pass. |
| K 7.1.293 parser/compiler, Haskell backend, SMT/rewrite engine, and hooked integer/Boolean/map/list/string primitives | All formal parsing and proof execution | Standard unavoidable machine-checking trust boundary; versions and exact commands recorded. |
| Used MPY operational fragment | Binding, evaluation, state, loop control, call/return, and result | Exhaustively inventoried and traced; no opaque result, unproved connection theorem, or false rule contributes. |
| `#runIsMultiplyPrime`, `#expect`, `#forgetEntryPoint` | Harness execution, result check, and ghost reset | Audited above; exact program KORE identity, body sensitivity, and false-result mutation provide independent validation. |
| Prime-product interpretation of the finite Boolean table | Connects execution results to the human-facing contract | Independently and exhaustively enumerated for 2–99; negative/0/1 conclusion follows from primes being at least 2. |
| Python differential run | Supports implementation/canonical alignment | 485 finite inputs, zero mismatches. It is supporting evidence only and is not used as a substitute for K closure. |

There is no result-bearing opaque primitive, empirical operational bridge, or
informal source-body substitution in the proof.

Evidence for the property bridge:

- `evidence/stage7/contract_table_check.py`
- `evidence/stage7/contract-table-check.log`

### Excluded behavior

The theorem does not claim behavior for integers `a >= 100`, non-integer
objects, Python features outside the supplied MPY subset, full CPython
exception behavior, resource use, or the unused opaque supplied primitives.
Those exclusions agree with the source integer contract and do not narrow its
material domain.

## Decision

Gate A passes: the proof is real-program sound, result-constraining,
body-sensitive, and non-vacuous.

Gate B passes: the formal domain is the full intended integer domain `a < 100`,
including the unbounded negative tail, and its result table exactly matches the
three-prime-product property.

Gate C passes: every actual assumption and evidence artifact is named and
reproducible, and finite testing is not presented as the proof.

Accordingly, the reconstructed proof is sound, pins the real generated
program, and has no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
