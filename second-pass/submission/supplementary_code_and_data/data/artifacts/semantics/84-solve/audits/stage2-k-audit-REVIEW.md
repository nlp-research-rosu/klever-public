# Independent adversarial audit — HumanEval 84 `solve`

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over the complete stated domain. The proof
reconstructs cleanly and is non-vacuous. The concern is validation strength:
the sole proof-local operational bridge is a true string-slice identity, but
the candidate does not contain a bridge-free universal K connection theorem.
A reviewer-authored attempt exposes the fixed semantics' symbolic
`isLen/buildIS` limitation. This is not a witnessed unsoundness and does not
permit a false result; it is a non-fatal evidence/trust-boundary limitation.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, problem `84-solve`, condition `semantics`, and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mount agrees with the
rendered mode.

The reviewer read the required launcher records:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`,
  `legacy-metrics.json`, and `legacy-run-input.json`; and
- all 228 JSON records in the one structured trace file below
  `/generation-evidence/codex-trace`.

Historical `runtime-metrics.json` is not present and is not required for this
legacy-selected-stage1 layout. Every required record is a readable regular
file, the trace contains no symlink and every trace line parses as JSON.
`codex-output.log` contains 10,177 lines and was read in full by the bounded
review script. Generation claims, including its prior `#Top`, were not used as
proof evidence.

The campaign block equals `/audit-campaign-lock.json` structurally, and the
lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded value. All independently recomputed ordinary-file hashes
match the launcher record: canonical, trusted/candidate prompt,
trusted/candidate translator, run/task/result/invocation manifests, generation
metrics, last message, output log, generation prompt, usage, and the trace file.
The invocation's hashes also match all seven listed evidence artifacts.

The candidate and trusted prompt are byte-identical, as are the candidate and
trusted translator. A recursive lstat/content manifest found exactly the same
25 entries (one subdirectory and 24 regular files) in the candidate and trusted
semantics trees. Their reviewer digests are both
`9594eb5afb0eec46c785e5dc0d013db263c443eecc54e86d7e6e373d53dc8e55`.
There are no missing, additional, changed, mistyped, or symlinked semantics
entries. All required candidate proof artifacts are readable regular files and
the candidate tree contains no symlink.

Evidence:

- `evidence/integrity_audit.py`
- `evidence/stage1-integrity.log` (exit 0)
- `evidence/trace_audit.py`
- `evidence/stage1-trace-summary.log` (all 228 trace records; exit 0)
- `evidence/generation_log_audit.py`
- `evidence/stage1-generation-text-rerun.log` (exit 0)

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for an integer `N` with `0 ≤ N ≤ 10000`, sum its
decimal digits and return that sum as a binary numeral string without a `0b`
prefix. Examples are `1000 ↦ "1"`, `150 ↦ "110"`, and
`147 ↦ "1100"`. Although the prose says “positive,” its explicit constraint
includes zero; the candidate includes zero rather than narrowing the domain.

The trusted canonical implementation is
`bin(sum(int(i) for i in str(N)))[2:]`. The submitted implementation sums the
five possible decimal places using `%` and `//`, then returns
`bin(digit_sum)[2:]`. Five places are sufficient and necessary on the bounded
domain, including `N=10000`.

In clean scratch space, running the trusted translator on the copied
`solution.py` produced a file byte-identical to submitted `solution.mpy`
(`cmp` exit 0). A mechanical constructor-token comparison found that the
`Module(...)` inside the entry claim's `#loadAll` has the same 185 tokens as
`solution.mpy`, and the following computation is `Call(Name("solve"), Int(N))`.

The independent differential test imports the trusted canonical entry point and
the submitted entry point separately. It checks the three documented examples,
28 lower/upper and decimal/binary transition boundaries, then all 10,001
integers in `0..10000`. There are zero mismatches. This exhaustive finite-domain
test supports source-contract alignment but is not substituted for the K proof.

Evidence:

- `evidence/differential_test.py`
- `evidence/program_pinning.py`
- `evidence/stage2-fidelity.log` (all commands exit 0)

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/reconstruction`; no
candidate kompiled directory or cache was copied. The semantics copy came from
the trusted reference mount. K tools report version 7.1.293.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled
```

This exits 0. The reviewer-authored K harness covers normal values, examples,
zero, all decimal place boundaries, and the upper bound:

```text
krun audit-concrete.mpy --definition runtime-audit-kompiled --output pretty --statistics
```

It exits 0 after 1,374 steps with `.K`, an empty heap and stack, `noRet`,
`NoExc`, and exit code 0.

Fresh proof build:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled
```

This exits 0. `spec.k` contains one positive target claim. Independently running
it with an explicit spec module:

```text
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC --output pretty
```

prints `#Top` and exits 0. Compiler warnings concern unused variables in the
unchanged supplied `strLt` rules; no target build/proof command fails.

Evidence:

- `evidence/k_concrete_harness.py`
- `evidence/stage3-toolchain.log`
- `evidence/stage3-kompile-llvm.log`
- `evidence/stage3-krun-concrete.log`
- `evidence/stage3-kompile-haskell.log`
- `evidence/stage3-kprove-positive.log`

## 4. Adequacy and real-program pinning

The single entry precondition is:

- `N` is a K integer satisfying `0 <=Int N andBool N <=Int 10000`;
- execution begins with the exact submitted module followed by `solve(N)`;
- environment 0 has an empty module scope whose parent is the fixed builtins
  scope; heap and stack are empty; allocation counters, return state, and
  exception state are their initial values.

The postcondition says that execution reaches:

```text
binaryNumeral(decimalDigitSum(N))
```

where `decimalDigitSum` is the sum of the units, tens, hundreds, thousands, and
ten-thousands digits, and `binaryNumeral(S)` is `str(binCodes(S))`. It also
requires the real `solve` closure, with its exact body, to remain installed in
the module scope; restores `scopeLoc` to 1; leaves heap and stack empty; and
ends with `noRet` and `NoExc`. Thus the return is not a free variable,
tautology, or one-way implication.

The claim mechanically pins the actual program:

- trusted regeneration is byte-identical;
- the loaded constructor term is token-for-token identical to `solution.mpy`;
- the fixed loader creates the exact closure shown on the RHS;
- ordinary name lookup selects that closure, not a textual-name summary;
- its body executes assignment, integer operations, builtin lookup/call,
  slicing, return, and frame pop.

The states with `N=0,1,147,9999,10000` are explicit satisfying witnesses.
For each, a reviewer model of the formal equations gives respectively
`"0"`, `"1"`, `"1100"`, `"100100"`, and `"1"`, equal to both Python
implementations.

A distinct body-sensitivity mutation changes the actually loaded units-place
operation from `% 10` to `% 9` in both the executable module and the expected
installed closure, while leaving the result specification unchanged. `N=9`
then yields `"0"` instead of required `"1001"`. The mutation is well formed;
`kprove` exits 1 with `WarnStuckClaimState` on the `% 9` versus `% 10`
binary-code equality. Failure is therefore sensitive to the executed body, not
to an external source file.

Evidence:

- `evidence/adequacy_witness.py`
- `evidence/stage4-witnesses.log`
- `evidence/spec-body-mutation.k`
- `evidence/stage4-body-sensitivity.log`

The formal domain is the complete source-contract domain, not finitely many
selected sizes or a bounded unrolling of an unrestricted contract.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.md` is the exhaustive source inventory. It contains
937 entries from all supplied semantics files, `verification.k`, and `spec.k`:
230 syntax declarations, 700 rules, five contexts, one configuration, and one
claim. It records every function/total/symbol/no-evaluators/concrete/macro/
priority/owise attribute and the complete source block. There are no
`simplification` rules or `functional` declarations in the audited sources.

`evidence/rule-assessment.md` assigns every inventoried entry to a decision and
gives the used-construct map. In summary, the material fixed path is:

```text
Module/load → FuncDef → Call/closure frame → bind N
→ left-to-right nested integer +, //, %
→ assign digit_sum → lookup/call fixed bin
→ exact [2:] bridge → Return → pop frame
```

The supplied declarations for the twelve used AST constructors match the
trusted translator. The fixed rules preserve Python's relevant evaluation
order. All division/modulus denominators are positive constants. Module
loading, scopes, call frames, returns, exception state, heap state, and
allocation state match the final claim. The 22 fixed proof-opaque
`no-evaluators` symbols (float/conversion, MD5, and sorting) never occur in the
program, residuals, or postcondition and influence no result, branch, control,
or state here. `MPY-CONCRETE` is absent from the Haskell proof definition.

The proof-local rules are:

1. `decimalDigit(N,1) => pyMod(N,10)`.
2. For `N≥0` and `P>1`,
   `decimalDigit(N,P) => pyMod((N-pyMod(N,P))/P,10)`.
3. On `0≤N≤10000`, `decimalDigitSum` expands to the five place values.
4. `binaryNumeral(N) => str(binCodes(N))`.
5. At priority 40,
   `Subscript(str(iCons(48,iCons(98,REST))), Slice(Int(2),NoBound,NoBound))`
   rewrites to `str(REST)` at the head of any continuation.

Rules 1–4 are terminating definitional summaries. Their guards are disjoint or
their right sides agree, and every target use is inside their covered domain.
The `[total]` declarations permit arbitrary interpretations outside guarded
cases but add no false equality; no out-of-domain term can influence the entry
claim.

Rule 5 is an operational bridge, so it received separate context review. Its
match already contains an evaluated string value with exact `0b` codepoints and
the pure slice syntax `[2:]`. The fixed path evaluates only literal/absent
bounds, chooses step 1, and builds the suffix at indices 2 through the string
length. For every finite algebraic `REST:IntSeq`, that suffix is exactly
`REST`. It reads/writes no other cell, allocates nothing, raises nothing, and
does not introduce return or unwinding. Consequently its arbitrary
continuation is contained: fixed execution would resume the same continuation
with the same value and every other cell unchanged. The RHS is the exact
structural tail, not an opaque/fresh oracle, so an opposite result
interpretation is not admitted.

Independent sensitivity evidence:

- Removing only the bridge and rebuilding succeeds, but the main proof exits 1
  specifically on the fixed `buildIS(...binCodes(...))` equality. This confirms
  that the successful proof depends on the rule rather than silently avoiding
  slicing.
- Fresh fixed and bridge-enabled LLVM definitions produce byte-identical final
  configurations for all values 0..45, a conservative superset of all binary
  values reachable from the five digit terms. Each slice is followed by an
  assertion continuation, testing both value and continuation preservation.

The limitation is universal machine evidence. A fresh bridge-free definition
builds successfully, but a reviewer universal connection spec exits 1: the
backend leaves symbolic `clampHi/isLen/buildIS` opaque. A helper functional
claim is also reported unsupported by this backend. This residual corroborates
why the bridge is needed; it does not refute the elementary structural
identity. The candidate contains no separate universal connection theorem.

No inventoried rule was labeled unsound: there is no concrete or symbolic false
conclusion witness on the intended input domain. The missing connection theorem
is reported narrowly as an evidence gap, as required.

Evidence:

- `evidence/rule_inventory.py`
- `evidence/rule-inventory.md`
- `evidence/rule-assessment.md`
- `evidence/verification-no-bridge.k`
- `evidence/spec-no-bridge.k`
- `evidence/stage5-kompile-no-bridge.log`
- `evidence/stage5-proof-without-bridge.log`
- `evidence/slice-connection-spec.k`
- `evidence/stage5-kompile-fixed-haskell.log`
- `evidence/stage5-slice-connection.log`
- `evidence/slice_ground_harness.py`
- `evidence/stage5-kompile-extended-llvm.log`
- `evidence/stage5-slice-ground-comparison.log`

## 6. Fresh non-vacuity test

The reviewer-created `spec-vacuity.k` changes only the result obligation to:

```text
binaryNumeral(decimalDigitSum(N) +Int 1)
```

`N=0` satisfies the entry precondition. Actual execution returns `"0"` while
the mutated postcondition requires `"1"`.

The exact dry-run command:

```text
kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY --dry-run
```

exits 0, establishing that the mutation parses and builds. The actual proof
command:

```text
kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY --output pretty
```

exits 1 with `WarnStuckClaimState`; its residual compares actual
`binCodes(decimalDigitSum(N))` against the off-by-one binary construction.
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6-vacuity.log`

## 7. Proven versus assumed accounting

What the reconstructed K proof establishes:

For every K integer `N` in `0..10000`, execution of the exact regenerated
submitted module followed by its actual `solve(N)` call reaches the prefix-free
binary representation of the sum of its five decimal place digits, with the
claimed final scope, heap, allocation, stack, return, and exception cells. This
is a universal reachability result under the supplied K theory, not a finite
collection of proof cases.

Trust and evidence ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler, Haskell prover, SMT/integer hooks | `#Top`, arithmetic side conditions | Standard low-level proof-tool trust; versions and clean commands recorded. |
| Byte-verified supplied semantics | All program execution | Required trusted semantics level. Candidate copy is recursively exact. Only its relevant integer/call/scope/bin/slice behavior is material. |
| Trusted `py2mpy.py` translation | Source-to-`Module` identity | Trusted input; regenerated bytes and constructor-level claim comparison independently checked. |
| Proof-local decimal summaries | Postcondition meaning | Ordinary exact arithmetic on the full bounded domain; guarded equations cover every use. Complete-domain differential testing gives zero mismatches. |
| Proof-local `[2:]` operational bridge | Final returned string and positive `#Top` | Structurally and contextually sound, no oracle and no false witness. Ground fixed/extended comparison covers a conservative superset of reachable values. Universal bridge-free K theorem is absent/does not close, which is the reason for `CONCERNS`. |
| Canonical Python implementation and CPython execution | Human-facing contract bridge | Trusted oracle input plus an exhaustive 10,001-case differential check. This supports, but is not substituted for, the K reachability theorem. |
| Fixed opaque symbols | None | All are unreachable and absent from the postcondition; no assumption about their interpretation is needed. |
| Candidate prose, prior definitions, logs, traces, and prior `#Top` | None | Treated only as untrusted claims; not used to establish the verdict. |

There is no domain restriction, substituted program, free result, task-answer
oracle, bounded proof of an unrestricted contract, or materially unsound rule.
The failed bridge-free connection proof is a real but non-fatal auditability
limitation. Under the benchmark decision boundary, this yields
`CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
