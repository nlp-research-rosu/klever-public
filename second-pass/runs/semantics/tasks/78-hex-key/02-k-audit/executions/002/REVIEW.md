# Independent adversarial audit: 78-hex-key

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over the full source-contract input domain. I
did not rely on the retained `#Top`, candidate logs, compiled artifacts, or
generation report. I rebuilt the supplied semantics and proof definition from
source in `/tmp/audit-work/hex-key-audit`, reproduced the submitted constructor
program with the trusted translator, proved the positive claims afresh, audited
all source rules, and required fresh body-sensitivity and false-result
mutations to fail.

## 1. Input and provenance integrity

`/audit-input.json` is a regular file with SHA-256
`d8539a12f4b1309464b5b8554bd60bc1ca5c463154f2b523dbf99eec52ccc455`.
It declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The required trusted
`/reference/reference-semantics` mount is present, so the mount state agrees
with the rendered semantics mode.

All launcher-declared container paths exist with the required regular-file or
directory type. The required legacy-selected-stage1 records are readable:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The optional historical legacy records are also present. No audited candidate,
reference, or generation-evidence entry is a symlink.

The campaign block in `/audit-input.json` is structurally equal to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded ordinary-file hash checked in `stage1-integrity.log` matches,
including the canonical, prompt, translator, manifests, result, invocation,
metrics, usage, retained output, retained last message, and generation prompt.
The launcher pipeline tree hashes also match:

- candidate mount:
  `8f836f571d09156d18504ec31d539ccdd85610d0ceb389cb7e0bb2e18ba0fab9`;
- trusted semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace:
  `a446081461407656e8604b4a33e05a0c77d12ea58381b2ab827ffa096c7b03c4`.

The candidate and trusted `prompt.py` are byte-identical, as are the candidate
and trusted `py2mpy.py`. Recursive type/path/content comparison of
`/candidate/reference-semantics` and
`/reference/reference-semantics` found 25 entries in each and no difference.
An additional independent canonical manifest digest is
`a81671cf50ee4947d460a3c8396a39cf0c31bd9a56a95d127f4e92d796b4a410`
for both trees. There are no missing, additional, changed, mistyped, or linked
supplied-semantics entries.

I read the complete retained generation record as untrusted history. The
structured trace has 332 valid JSON lines and no malformed line. The 16,649-line
`codex-output.log` contains intermediate parse/proof failures as well as the
eventual claimed success; none was used as proof evidence. The full record
summary and all 75 retained tool calls are in
`evidence/generation-record-inspection.log`. Provenance integrity passes; there
is no audit infrastructure breach.

Evidence: `evidence/stage1_integrity.py`,
`evidence/stage1-integrity.log`,
`evidence/inspect_generation_record.py`, and
`evidence/generation-record-inspection.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a correct uppercase hexadecimal string,
or the empty string, return the number of characters whose hexadecimal digit
value is prime. Exactly `2`, `3`, `5`, `7`, `B` (11), and `D` (13) count.
There is no stated length bound.

The trusted canonical loops by index over `num` and increments for membership
in the tuple `('2', '3', '5', '7', 'B', 'D')`. The candidate loops directly
over the same string and increments for membership in `"2357BD"`. These are
equivalent on the intended domain. Initializing `digit = ""` before the loop
only fixes Python's post-loop local value on empty input; it does not affect the
return.

I ran the trusted translator from scratch:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

The command exited 0. Both constructor files have SHA-256
`38b240e2fa272c61074e88862eb2e90f8c2f8721ebd883d3976c5b466d3e6d7a`.
Thus the submitted `solution.mpy` is byte-identical to trusted regeneration.

The independent differential test loads the copied trusted canonical and
candidate by separate module paths and also computes the contract directly. It
checks:

- all five documented examples;
- empty input;
- each of the 16 singleton hex digits, covering both membership branches;
- repeated all-counting and no-counting inputs;
- mixed orderings and a 4,096-character boundary input;
- every valid string of length 0 through 3 (4,369 generated strings);
- 5,000 deterministic random valid strings of length 0 through 256.

All 9,397 comparisons agreed; mismatch count was zero. This finite evidence is
not substituted for the K proof.

Evidence: `evidence/translator-reproduction.log`,
`evidence/differential_test.py`, and
`evidence/differential-test.log`.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/hex-key-audit`; I did not
copy or reuse candidate kompiled definitions, caches, `krun.out`, or
`kprove.out`. The live tools report K version 7.1.293.

Fresh concrete reconstruction:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0. The candidate concrete test module was independently regenerated
with the trusted translator and byte-compared before execution. Then:

```text
krun concrete_tests.regenerated.mpy --definition runtime-kompiled
```

exited 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.

Fresh proof reconstruction:

```text
kompile verification.k --backend haskell \
  --main-module HEX-KEY-VERIFICATION \
  --syntax-module HEX-KEY-VERIFICATION \
  --output-definition verification-kompiled
```

exited 0. I selected the auxiliary positive claim directly:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC --claims loop-lemma
```

It exited 0 and printed `#Top`. I then ran the complete target spec, which
contains exactly the loop lemma and entry-point theorem:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC
```

It exited 0 and printed `#Top`. This dependency-aware run proves every positive
claim, including the entry theorem using the independently closing loop
circularity.

For diagnostic completeness, filtering to `entry-point` alone removes its
induction lemma and did not finish within a 30-second diagnostic bound. That
run is not a target-proof failure and is not used as success evidence; the
submitted positive command is the complete two-claim spec and closes quickly.

Evidence: `evidence/toolchain-version.log`, `evidence/kompile-llvm.log`,
`evidence/krun-concrete.log`, `evidence/kompile-proof.log`,
`evidence/kprove-loop-lemma.log`, `evidence/kprove-all.log`, and
`evidence/kprove-entry-point-without-loop-diagnostic.log`.

## 4. Adequacy and real-program pinning

### Claim meanings

The `loop-lemma` claim says: starting at the real `#loop` for an arbitrary
finite string code sequence `CS`, with integer accumulator `ACC` and plain
locals `digit` and `num`, execution consumes the loop before an arbitrary
continuation. It increases `count` by `hexCount(CS)`, sets `digit` to its old
value for empty input or to the final one-character string otherwise, preserves
`num`, and preserves every framed scope, heap, stack, return, exception, and
exit-code component.

The `entry-point` claim says: from the standard module configuration, load a
module defining `hex_key(num)` with `hexKeyBody`, look up and call that function
on arbitrary `str(CS)`, and return exactly `hexCount(CS)`. It also constrains
the final module binding and all other cells. There is no explicit `requires`;
the many-sorted term itself requires an `IntSeq` string, and it includes all
uppercase hexadecimal strings and the empty string. It is broader than the
source domain, not narrower.

Both preconditions are satisfiable. For example, `CS = .IntSeq` with the exact
initial entry configuration is a ground state and returns 0. A second ground
state uses codes `[50,65,51,68]` (`"2A3D"`) and returns 3.

### Mechanical real-program pinning

Trusted regeneration connects `solution.py` to `solution.mpy`. I then parsed
both the regenerated module and the claim's macro-bearing module with the
fresh proof definition using `kast --expand-macros --output json`. The two JSON
AST files are byte-identical, each with SHA-256
`89e95772bfbfe1df3d202abc4932fe8eb2d76f13aa7fb70e1f00b9d5bdb8121e`.
This is a constructor-level comparison of the function binding, parameter, and
entire executed body, not a textual assertion.

The entry claim begins with `#loadAll(Module(FuncDef(...)))`; it therefore
executes definition loading, name lookup, argument evaluation, frame creation,
parameter binding, every assignment, the real loop and branch, return, and
frame pop. The macros only expand syntax and introduce no execution rule.

The two concrete K witness claims (`"" => 0` and `"2A3D" => 3`) built and
proved together with `#Top`. Both Python implementations and the direct
contract give the same values. The entry postcondition is a concrete function
of the input, not a free result variable, tautology, or one-way implication.

Finally, I changed the program term actually loaded by the claims from
`AugAssign(..., Int(1))` to `AugAssign(..., Int(2))`, rebuilt a distinct proof
definition successfully, and reran otherwise corresponding claims. The proof
failed with `WarnStuckClaimState` on the expected false equation:

```text
ACC +Int 2 +Int hexCountMutated(R)
  = ACC +Int (hexCountMutated(R) +Int 1)
```

This demonstrates sensitivity to the executed function body.

Evidence: `evidence/claim-program.mpy`,
`evidence/program-term-pinning.log`, `evidence/spec-witness.k`,
`evidence/kprove-concrete-witnesses.log`,
`evidence/verification-body-mutated.k`,
`evidence/spec-body-mutated.k`,
`evidence/kompile-body-mutation.log`, and
`evidence/kprove-body-mutation.log`.

## 5. Rule-by-rule static soundness review

I inventoried the assembled supplied semantics, every helper K file,
`verification.k`, and `spec.k`: 26 files, 944 declarations comprising 703
rules, 233 syntax declarations, five contexts, one configuration, and two
claims. The inventory includes all function/total declarations, all opaque
symbols, all priority and ordinary rules, and all attributes. There are no
`[simplification]` rules and no `[functional]` declarations.

`evidence/rule-inventory.log` contains every declaration with source path,
line, stable ID, attributes, and complete rule block.
`evidence/rule-review.md` gives an exhaustive disposition scheme covering
K0001 through K0944 and a constructor-to-rule dependency map for the submitted
program.

The reachable path is:

```text
#loadAll
  -> FuncDef binding
  -> Name("hex_key") lookup
  -> left-to-right argument evaluation
  -> ordinary closure frame and #bindP
  -> count/digit assignments
  -> evaluate num once
  -> #loop over str
  -> #iterNext head/tail
  -> #bindTgt digit
  -> Compare(character, "2357BD")
  -> strContains/branch
  -> integer AugAssign when true
  -> #loopLbl and recursive loop head
  -> Return/name lookup/#pop
```

The configuration and every material state effect match this path. The heap
stays empty; scope and heap locations are preserved after pop; the caller
continuation is restored; there is no output, exception, break, continue,
allocation, or other control effect.

The candidate-local inventory is small and sound:

- `hexKeyLoopBody` and `hexKeyBody` are exact syntax macros, mechanically
  pinned to the regenerated AST.
- `isPrimeHexCode(C)` is one total equation testing the one-code sequence
  against exactly codes 50, 51, 53, 55, 66, and 68.
- `primeHexBit(C)` maps that Boolean to 1 or 0.
- `hexCount` has disjoint base/constructor equations, covers all `IntSeq`
  values, and structurally descends.
- `finalDigit` likewise has disjoint, covering, descending equations matching
  Python's loop-variable side effect.

None is an operational bridge or opaque oracle. No rule intercepts a program
call, skips a body operation, fabricates a result, encodes a fixed example, or
preempts the supplied execution. The mathematical summary is connected to
the real loop by the loop reachability claim itself.

I inspected all 45 priority rules. They concern heap references, closure cells,
special builtins/methods, or concrete-only sort/deep-equality behavior. The
reachable heap is empty, the exact frame has no `$cells` marker, and the
callee is an ordinary closure; none overlaps a used redex. All 22
`no-evaluators` symbols concern float, sort, or MD5 behavior and are absent
from the program, claims, helper functions, and reachable cells. They cannot
influence control or the result.

The supplied minimal semantics intentionally has unused language-coverage
limits. One explicit example is its string-count helper:
`cntSub(.IntSeq, .IntSeq) => 0`, whereas CPython evaluates
`"".count("")` to 1. Other documented excluded cases include some invalid
indices, zero-step ranges, escaping closures, and unsupported exceptions.
These are fixed-semantics coverage limits, not candidate proof extensions.
The real program never constructs any such term, no such rule overlaps the
reachable dependency graph, and none can enable a false conclusion about
`hex_key` on a valid input. Every material operation used here is modeled and
was checked independently.

No unsound candidate or used semantics rule was found.

Evidence: `evidence/inventory_rules.py`,
`evidence/rule-inventory.log`, and `evidence/rule-review.md`.

## 6. Fresh non-vacuity test

I authored a fresh spec that retains the real program and loop lemma but
changes the entry result from `hexCount(CS)` to the deliberately false
`hexCount(CS) +Int 1`. This is false for the satisfying empty-string state:
the program, trusted canonical, candidate Python, and original theorem all
return 0, while the mutation requires 1.

The mutation first passed a parser/build-only check:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC-VACUITY --dry-run
```

Exit status was 0 and it emitted a valid `kore-exec --prove` command. The real
mutation run:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module HEX-KEY-SPEC-VACUITY
```

exited 1 without timeout. It produced `WarnStuckClaimState` at the mutated
entry destination after reaching actual `<k> hexCount(CS) ~> .K </k>`. The
unmet obligation is exactly:

```text
hexCount(CS) +Int 1 = hexCount(CS)
```

This is a meaningful reachable result failure, not a parser error, missing
import, timeout, or unrelated crash. Non-vacuity passes.

Evidence: `evidence/spec-vacuity.k`,
`evidence/kprove-vacuity-dry-run.log`, and
`evidence/kprove-vacuity.log`.

## 7. Proven versus assumed accounting

### What is formally proven

Under the supplied K semantics, for every finite `IntSeq CS`, if execution of
the exact submitted constructor module from the stated initial configuration
terminates, calling `hex_key(str(CS))` returns

```text
sum over CS of 1 exactly for codes 50, 51, 53, 55, 66, 68, else 0.
```

It leaves the module function binding as specified, restores scope/stack
control state, leaves the heap empty, raises no modeled exception, and leaves
exit code 0. The loop lemma additionally characterizes the accumulator and
final loop variable for any starting accumulator and continuation satisfying
its exact frame pattern.

This is partial correctness. The reachability proof is not reported as an
independent liveness theorem, although concrete finite string iteration
terminates in both Python and the supplied operational rules.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, kompiler, Haskell prover, and builtin integer/Boolean/map/list/string hooks | All machine-checked results | Standard low-level proof/toolchain trust boundary; acceptable and version-recorded. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Acceptable: launcher hash matches, candidate copy is identical, and regeneration is byte-identical. |
| Trusted supplied semantics | Defines the execution model | Acceptable for this theorem: candidate tree is exactly identical; every used declaration/rule was statically checked; fresh LLVM execution agrees. Unused minimal-subset limitations are explicitly excluded. |
| Macro-to-program bridge | Connects claim term to submitted constructor body | Mechanically discharged by macro-expanded `kast` JSON equality, not assumed. |
| Codes 50/51/53/55/66/68 as `2/3/5/7/B/D` | Connects formal summary to the source contract | Directly fixed by the prompt and ordinary ASCII code values used by the supplied string semantics; no opaque symbol. |
| Loop invariant/circularity | Connects actual iteration to `hexCount` | Machine-checked reachability claim, proved independently and exercised by the full entry proof. |
| Python differential test | Supports implementation/intent and semantics bridge on sampled inputs | Finite corroborating evidence only; not used as a universal proof. |
| Opaque float/sort/MD5 and other unused primitives | Imported by the broad fixed semantics | No dependent claim or reachable term; they have no value, control, state, or postcondition influence here. |

There is no candidate-defined trusted primitive, result-bearing opaque symbol,
empirical oracle, operational bridge, or informal value assumption on which
claim closure depends.

### Gate results and decision

- Gate A, real-program soundness: **PASS**. Fresh `#Top`, exact body pinning,
  truthful/covering helper equations, state/control review, body sensitivity,
  satisfying witnesses, and false-result rejection all pass.
- Gate B, intent adequacy: **PASS**. The formal string domain includes the full
  unrestricted valid HumanEval domain and the postcondition is exactly the
  requested count. There is no finite-size or example-only restriction.
- Gate C, trust and evidence auditability: **PASS**. Commands, statuses,
  bounded outputs, scripts, inventories, mutations, and trust boundaries are
  preserved under `/audit-output/evidence`.

The Kit status is therefore `VALIDATED`. Under the benchmark decision mapping,
the candidate is `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
