# Independent adversarial audit: 82-prime-length

The candidate is **not a legitimate partial-correctness proof of the real
generated Python program over its intended source-contract domain**. A clean
reconstruction does produce `#Top`, the translated program is pinned exactly,
and the claim is non-vacuous. The decisive defect is in the generated language
semantics: `semantic.k:84` implements Python `len(str)` with K
`lengthString`. On valid Python Unicode inputs this K operation uses a different
length measure. Fresh execution gives K lengths 8 for `"😀😀"` and 6 for
`"你好"`, while both Python strings have length 2. The trusted canonical and
candidate Python functions therefore return `True`, but the candidate K
semantics returns `False`. This is a concrete false-conclusion witness for a
rule that affects the theorem's result.

All untrusted candidate compiled definitions, `.kore` files, caches, prose, and
generation claims were excluded from the reconstruction.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `82-prime-length`;
- condition `bare`;
- `record_layout: legacy-selected-stage1`;
- `semantics_mode: GENERATED_SEMANTICS`;
- no mounted reference semantics.

I inspected `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the invocation and metrics records,
`usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and all 198
JSON records in the structured trace. Historical runtime metrics are not
required for this legacy-selected layout.

The independent checker and complete transcript are:

- `/audit-output/evidence/stage1_provenance.py`
- `/audit-output/evidence/stage1_provenance.log`

The checker exited 0. All required mounts and records are readable real files or
real directories. There are no symlinks or unsupported entries in `/candidate`
or the trace tree. Relevant independent checks include:

- campaign-lock SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`
  matches `/audit-input.json`, and its JSON object exactly matches the embedded
  campaign block;
- `/run.json`, `/task.json`, `/generation-result.json`, invocation, metrics,
  usage, last-message, output-log, generation-prompt, canonical, trusted
  prompt, and translator hashes all match their recorded values;
- the pipeline workspace tree digest of the mounted candidate is
  `55b41c0dcca0fbd126e329f2a8ee77d0547652182cfee228c092989a2d53880a`,
  matching the generation result and invocation records;
- the pipeline trace-tree digest is
  `31a04d9ea28b9d4aece0eae953f3f52732c97f02f1feec9b0b4df6fe5cb6c536`,
  matching `usage.json`; its sole JSONL file hash also matches the result and
  invocation manifests;
- candidate `prompt.py` is byte-identical to `/reference/prompt.py`;
- candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- `/reference/reference-semantics` is absent, as
  `GENERATED_SEMANTICS` requires.

The intact candidate contains all required proof artifacts:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. Submitted `solution.kore`, `specified-solution.kore`, and
`__pycache__` were inventoried but not trusted or copied into the clean build.
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py` is: given a Python string,
return `True` exactly when its length is prime, otherwise `False`. It contains
no ASCII or other encoding restriction. `/reference/canonical.py` computes
Python `len(string)`, rejects lengths 0 and 1, and searches for a divisor from
2 through `length - 1`.

Candidate `solution.py` computes:

```python
n = len(string)
return n >= 2 and all(n % i != 0 for i in range(2, n))
```

This is an equivalent algorithm for every finite Python string. It terminates
and returns a real `bool`.

Using the trusted translator copied to scratch, the exact command recorded in
`stage2_regeneration.log` regenerated `solution.mpy`, compared it with the
submitted file, and exited 0. Both hashes are:

```text
d1228a6510b7b7b80112c0b2b55ea1ab564682c421757a9af789432390dec86d
```

The independent differential oracle is
`/audit-output/evidence/stage2_differential.py`; its command and results are in
`stage2_differential.log`. It imports separately copied trusted canonical and
candidate modules and covers:

- all four documented examples;
- empty, lengths 1 and 2, the first prime/composite transitions, and later
  divisor boundaries;
- every length from 0 through 300;
- Unicode and control-character strings;
- 200 seeded generated strings of lengths 0 through 2000.

It exited 0 with 529 cases and zero mismatches. This is finite implementation
evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/rebuild`. No submitted
definition, cache, or `.kore` output was reused. Tool versions were K 7.1.293
and Python 3.10.12.

Fresh commands and outcomes:

| Command | Exit/result | Evidence |
|---|---:|---|
| `kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-kompiled` | 0, with five non-exhaustive-function warnings | `stage3_kompile_concrete.log` |
| `kompile semantic.k --backend haskell --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-haskell-kompiled` | 0 | `stage3_kompile_concrete_haskell.log` |
| `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled` | 0 | `stage3_kompile_proof.log` |
| `kprove spec.k --definition proof-kompiled --spec-module SPEC` | 0, `#Top` | `stage3_kprove_positive.log` |

`spec.k` contains exactly one positive target claim, so every positive claim
was rerun.

Generated-semantics execution was compared with both Python functions by
`stage3_concrete_compare.py`. The first run used the writing-semantics skill's
LLVM smoke-test path. Lengths 0 and 1 completed, but every input reaching
`noDivisors` exited 113 with a residual such as
`noDivisors ( 2 , 2 , 2 )`; see `stage3_concrete_compare.log`. The candidate's
`[concrete]` rules are not executable there.

The second run used the Haskell backend selected by the candidate. All ASCII
normal/boundary cases matched, but two valid Unicode cases failed the
cross-model comparison:

| Input | Python length/result (canonical and candidate) | Fresh K state/result |
|---|---|---|
| `"😀😀"` | 2 / `True` | `n = 8` / `VBool(false)` |
| `"你好"` | 2 / `True` | `n = 6` / `VBool(false)` |

The Haskell comparison intentionally exits 1 because it detects these two
mismatches; this is candidate evidence, not an audit-infrastructure error. The
full commands, exit statuses, and final K configurations are in
`stage3_concrete_compare_haskell.log`.

Thus fresh `#Top` is real under the submitted theory, but that theory is not a
sound semantics of the real Python program on its stated domain.

## 4. Adequacy and real-program pinning

The sole claim has no `requires` clause. In plain language its precondition is:
for any K `String` `S`, start with the exact `solutionProgram`, argument
`VStr(S)`, empty environment, and `noResult`.

Its postcondition requires:

- empty `<k>`;
- environment entries `"string" |-> VStr(S)` and
  `"n" |-> VInt(lengthString(S))`;
- return value
  `VBool(isPrime(lengthString(S)))`.

This is result-constraining, not a free variable, tautology, or implication.
The initial state with `S = "ab"` is a concrete satisfying state. Substitution
gives K length 2 and result `True`, matching both Python functions. `S =
"orange"` gives length 6 and `False`, also matching. The Unicode witnesses
above satisfy the same unrestricted entry precondition but make the formal
result disagree with both Python implementations.

The program term itself is pinned correctly. Fresh `kast --expand-macros`
outputs for regenerated `solution.mpy` and `solutionProgram` compare
byte-identically, both with hash:

```text
1a81cc0563915ca1faff783814e18fedc9949f6139ba00b3be631fb33995c534
```

See `stage4_program_pinning.log`. The claim executes the actual translated
function binding and body through `run`; its assignment and return follow the
real constructor control flow.

I also changed the constructor term actually executed by the claim from
`n >= 2` to `n >= 3`, rather than merely editing an external source file.
`verification-body-mut.k` and `spec-body-mut.k` built successfully. The proof
then exited 1 with `WarnStuckClaimState` and the expected residual comparing
`lengthString(S) >= 2` with `lengthString(S) >= 3`; see
`stage4_body_mutation_build.log` and `stage4_body_mutation_kprove.log`. The
proof is body-sensitive.

Adequacy nevertheless fails: exact AST pinning under an incorrect
`len(str)` semantics is not real-program pinning at the behavioral level.

## 5. Rule-by-rule static soundness review

The complete declaration scan and exhaustive inventory are:

- `/audit-output/evidence/stage5_declaration_scan.log`
- `/audit-output/evidence/stage5_rule_inventory.md`

The inventory enumerates all 23 local syntax/function/macro declarations, the
configuration, all 19 `semantic.k` rules, both `verification.k` rules, and the
claim. There are no local priority, `[functional]`, `[owise]`, or `anywhere`
rules.

The submitted constructor coverage is complete:

```text
Module → FuncDef/Params/CellVars/FreeVars → Assign → Name/Call(len)
→ Return → BoolOp(and) → Compare(>=) and Call(all) → GenExp
→ Compare(!=) → BinOp(%) → CompFor/Call(range)/Bool(true)
```

Rule findings, using the IDs in the inventory:

- S1–S3 specialize entry dispatch, assignment, and return. They preserve the
  binding and control needed by this one pure body.
- S4–S8 and S10–S13 correctly handle target literals, names, calls, positive
  integer modulo, and comparisons, except that S8 depends on invalid S9.
- **S9, `valueLength(VStr(S)) => lengthString(S)`, is materially unsound as a
  Python semantic bridge.** The false conclusion witness is `"😀😀"` (also
  `"你好"`): it enables the theorem to conclude `False` when the real program
  concludes `True`.
- S14 evaluates `and` eagerly. This is globally broader than Python
  short-circuit semantics, but the submitted RHS is pure and defined for
  lengths 0 and 1. I found no false conclusion witness from eagerness on the
  intended inputs, so I record it as over-broad, not as the material
  unsoundness.
- S16 directly summarizes the exact task-specific
  `all(... for ... in range(...))` pattern as `noDivisors`. S17–S19 give
  truthful, disjoint, descending ground equations for the target divisor
  domain. However, `[concrete]` deliberately leaves the same result-bearing
  `noDivisors` symbol in both execution and the final property during symbolic
  proof. There is no independent general-generator semantics or bridge-free
  universal connection theorem. Because no false ground conclusion was found
  for the matched target pattern, this is recorded as a circular
  evidence/trust-boundary limitation, not mislabeled as a second witnessed
  unsound rule.
- V1 is the exact macro-pinned program. V2 is the standard natural-number
  characterization of primality, conditional on the ground meaning of
  `noDivisors`.

The fresh LLVM compiler reports non-exhaustive matches for `eval`,
`valueLength`, `asInt`, `asBool`, and `noDivisors` despite `[total]`.
`noDivisors(N,0,HI)` also exposes unhandled modulo-zero behavior. Those global
totality attributes are unjustified, though the submitted target starts the
divisor at 2 and stays in the covered coercion cases. The concrete
target-domain false result comes from S9, not these unused cases.

The generated semantics is minimal, which is allowed in this mode, but
minimality does not excuse incorrect behavior for a construct the submitted
program materially uses.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh mutation is
`/audit-output/evidence/spec-vacuity-audit.k`. It changes the return obligation
from `isPrime(lengthString(S))` to its Boolean negation. The initial state is
still satisfiable; for witness `S = "ab"`, actual result is `True` and the
mutated postcondition requires `False`.

Commands and outcomes:

- `kprove spec-vacuity-audit.k --definition proof-kompiled --spec-module
  SPEC-VACUITY-AUDIT --dry-run` exited 0, establishing that the mutation parses
  and builds (`stage6_vacuity_dry_run.log`);
- the same command without `--dry-run` exited 1 with
  `WarnStuckClaimState`. Its residual compares the original Boolean expression
  with `notBool` of that expression (`stage6_vacuity_kprove.log`).

This is the expected unmet result obligation. The proof is discriminating and
non-vacuous under its theory. That does not validate the theory's Python
string model.

## 7. Proven versus assumed accounting

The detailed ledger is `/audit-output/evidence/stage7_trust_ledger.md`.

Precisely, reconstructed `#Top` establishes partial correctness of this
statement under the submitted K semantics:

```text
return VBool(
  lengthString(S) >=Int 2
  andBool noDivisors(lengthString(S), 2, lengthString(S))
)
```

The postcondition's `isPrime` rewrites to that identical expression. The proof
does not establish that K `lengthString` equals Python `len(str)`; fresh
execution refutes the bridge. Nor does it independently derive the specialized
generator summary from a general Python generator semantics.

Accepted low-level trust boundaries are the byte-identical trusted translator,
K 7.1.293's ordinary Boolean/integer/map hooks, and the Haskell backend.
Conditional/informal boundaries are the standard mathematical primality
characterization and the inspected ground `noDivisors` recursion. The
specialized generator bridge has only its truthful equations, static
inspection, and finite ground evidence.

The STRING bridge is illegitimate for this theorem because it changes a
result-bearing operation on valid source inputs. The finite Python
differential test supports only candidate-versus-canonical fidelity; the
K/Python concrete comparison directly disproves generated-semantics fidelity.

Accordingly, the successful reachability claim is a theorem about an
encoding-dependent K byte-string surrogate, not the unrestricted Python-string
program required by the HumanEval contract. This is a material source-domain
and semantics failure, so the benchmark's decision boundary requires
`FAIL / NOT_LEGIT`, not `CONCERNS`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
