# Independent adversarial audit: 108-count-nums

## Executive decision

The candidate is **FAIL / NOT_LEGIT**.

Fresh reconstruction confirms that all nine reachability claims close and that
an off-by-one postcondition does not. Those facts do not rescue the submission:

1. The entry claim never loads or executes `solution.mpy`. It applies a
   hand-written `countNumsClosure` macro whose body duplicates the current
   program. Changing the real program's count increment from 1 to 2 leaves the
   proof definition and final `#Top` unchanged.
2. Several priority-40 operational summaries accept a materially larger state
   domain than their auxiliary claims prove. Two fresh witnesses show the
   extended definitions proving a normal integer result where the preceding,
   bridge-free layer gets stuck at the exact omitted-state dependency.

The first defect is a substituted-program/real-program-pinning failure. The
second is a proof-theory soundness failure. Either independently crosses the
problem's `FAIL / NOT_LEGIT` boundary.

## 1. Input and provenance integrity

The declared mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount exists as a real directory, so the mount
does not contradict the rendered mode. The audit therefore continued normally;
this is not an infrastructure error.

The recursive comparison found:

- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256 `c2e8f36f104159515ac39779538568114e45da57511596c007abc0da04875981`).
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Every candidate `reference-semantics/` entry has the same relative path,
  regular-file/directory type, and bytes as the trusted tree. There are no
  missing, additional, changed, mistyped, or symlinked semantics entries.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
  regular files. No candidate symlinks were found.

The following required generation records are all missing:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace was present. The candidate additionally contains
untrusted `prove.sh`, `prove.log`, concrete-test files, and a Python bytecode
cache; none was used for reconstruction. The missing records are a provenance
integrity failure, although the decisive verdict below does not depend on them.

Evidence: [stage1_integrity.log](evidence/stage1_integrity.log),
[stage1_integrity.sh](evidence/stage1_integrity.sh), and
[scratch_copy.log](evidence/scratch_copy.log).

The live tools were independently available as K
`v7.1.337` (`kompile` and `kprove` from `/usr/bin`).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite array of integers, count the elements whose signed decimal digit
sum is positive. For a negative integer, only the most significant digit has a
negative sign: for example, `-123` contributes `-1 + 2 + 3 = 4`.

The submitted implementation uses three helpers:

- For nonnegative `n`, repeatedly add `n % 10` and replace `n` with `n // 10`.
- For a negative original value, process its nonnegative magnitude while at
  least two digits remain, then subtract the final leading digit.
- Increment the array count exactly when the resulting signed digit sum is
  greater than zero.

This is extensionally consistent with the trusted canonical implementation over
the intended integer-list domain.

### Translation identity

The trusted translator regenerated `solution.mpy` byte-for-byte. Both files
have SHA-256
`047da4fbb79a015327f8843735ad63ab646bbbf86b1c9530e2652b9b2f43b808`.

Evidence: [translation_regeneration.log](evidence/translation_regeneration.log).

### Independent differential execution

The reviewer-authored test imports the trusted canonical and generated entry
points independently. It covers:

- all three documented examples;
- empty, zero, sign, one-digit/two-digit, and loop-boundary cases;
- all arrays of lengths 0 through 3 over 17 values surrounding `-10`, `0`, and
  `10` (5,220 generated cases);
- 2,000 deterministic random arrays of lengths 0 through 12, including integers
  up to 80 decimal digits.

After deduplication, all 7,001 cases matched and the mismatch count was zero.
The complete generated inputs are preserved.

Evidence: [differential_test.py](evidence/differential_test.py),
[differential_test.log](evidence/differential_test.log), and
[differential_inputs.jsonl](evidence/differential_inputs.jsonl).

This finite evidence supports current-program/canonical agreement. It is not a
universal K proof and does not pin the proof claim to `solution.mpy`.

## 3. Clean proof reconstruction

All candidate-built definitions and caches were ignored. Sources needed for
execution were copied to `/tmp/audit-work/audit-108`, with the semantics copied
from the trusted reference tree.

### Concrete definition and execution

An LLVM definition was built from the fresh trusted semantics with main module
`MPY-KRUN` and syntax module `MPY-SYNTAX`. The actual copied `solution.py` was
combined with reviewer assertions, translated by the trusted translator, and
run through `krun`.

Assertions covered every helper loop boundary and the documented/representative
entry cases. Execution ended with `.K`, `NoExc`, empty stack, and exit code 0.

Evidence:
[build_concrete_llvm.log](evidence/build_concrete_llvm.log),
[prepare_concrete_harness.py](evidence/prepare_concrete_harness.py),
[concrete_harness_suffix.py](evidence/concrete_harness_suffix.py), and
[run_concrete_harness.log](evidence/run_concrete_harness.log).

### Haskell definitions and positive claims

The candidate's intended layered proof was independently rebuilt:

| Fresh definition main module | Spec module(s) proved | Claims |
|---|---|---:|
| `COUNT-NUMS-VERIFICATION-BASE` | `POSITIVE-LOOP-SPEC`, `NEGATIVE-LOOP-SPEC` | 2 |
| `DIGIT-LOOP-LEMMAS` | `POSITIVE-FUNCTION-SPEC`, `NEGATIVE-FUNCTION-SPEC` | 2 |
| `DIGIT-FUNCTION-LEMMAS` | `SIGNED-FUNCTION-SPEC` | 1 |
| `SIGNED-DIGIT-LEMMA` | `COUNT-LOOP-WITH-N-SPEC` | 1 |
| `COUNT-LOOP-WITH-N-LEMMA` | `COUNT-LOOP-SPEC` | 2 |
| `COUNT-LOOP-LEMMA` | `COUNT-NUMS-SPEC` | 1 |

All six definitions compiled. All eight `kprove` invocations exited 0 and
printed exactly one `#Top`; the invocation covering `COUNT-LOOP-SPEC` checked
both claims, for nine positive claims total.

Evidence: [reconstruct_proofs.sh](evidence/reconstruct_proofs.sh), the individual
`build_*.log` and `prove_*.log` files, and
[positive_proof_summary.log](evidence/positive_proof_summary.log).

Compiler warnings concerned unused variables and supplied-semantics functions
outside this program's path. No build, backend, timeout, or container failure
occurred.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfying states

Each precondition is satisfiable:

| Claim | Precondition | Postcondition | Example satisfying data |
|---|---|---|---|
| Positive while loop | Local `n=N`, `total=A`; `N >= 0` | Loop is removed; `n=0`, `total=positiveFold(N,A)` | `L=1, N=12, A=4` |
| Negative while loop | Local `n=N`, `total=A`; `N >= 0` | Loop is removed; `n=leadingDigit(N)`, `total=negativeTotal(N,A)` | `L=1, N=1203, A=0` |
| Positive helper | Clean full state; integer `N >= 0` | Applying the synthetic helper closure returns `positiveDigitSum(N)` | `N=1203`, result 6 |
| Negative helper | Clean full state; integer `N >= 0` | Applying the synthetic helper closure returns `negativeDigitSum(N)` | `N=1203`, result 4 |
| Signed helper | Clean state with the three helper bindings; any integer `N` | Synthetic signed closure returns `signedDigitSum(N)` | `N=-1203`, result 4 |
| Count loop with old `n` | `L != 0`, integer sequence `VS`, local `arr`, `count=C`, `n=OLD`, correct helper scope | Loop is removed; count becomes `countFold(VS,C)` and `n` becomes the last element or `OLD` | `VS=[-12,10], C=0, OLD=7` |
| Empty count loop without old `n` | `L != 0`, local `arr` and `count` | Empty iteration is removed and does not create `n` | `VS=[]`, `C=0` |
| Nonempty count loop without old `n` | `L != 0`, integer head/tail, local `arr` and `count` | Count becomes the sequence fold; `n` becomes the last element | `VS=[-12,10]`, `C=0` |
| Final count function | Clean state, correct helper scope, finite `VS` satisfying `allInts(VS)` | Synthetic count closure returns `countPositive(VS)` | `VS=[-12,-11,0,10]`, result 2 |

Ground substitution confirms that `countPositive([-12,-11,0,10]) = 2`, and
both trusted canonical Python and submitted Python return 2. Further helper and
entry witnesses also agree.

Evidence: [claim_witnesses.py](evidence/claim_witnesses.py) and
[claim_witnesses.log](evidence/claim_witnesses.log).

### Decisive pinning failure

The final `<k>` cell is:

```k
#applyK(toCall(countNumsClosure), (list(VS), .Vals))
```

It is not `#loadAll(Module(...solution.mpy...))`, does not evaluate the submitted
module, and does not look up the module's actual `count_nums` binding.
`verification.k` manually re-encodes the bodies, closures, and helper bindings.
Neither `spec.k` nor `verification.k` requires or parses `solution.mpy`.

The current manual macro happens to match the current translated body, but
there is no proof dependency. A fresh body-sensitivity experiment changed the
real program's increment from `count += 1` to `count += 2` and regenerated the
mutant `.mpy` with the trusted translator:

- Python and fresh `krun` execution give `count_nums([1]) = 2`.
- The unchanged proof sources compile next to that mutant.
- `COUNT-NUMS-SPEC` still exits 0 with `#Top`, claiming the manually encoded
  one-increment summary (`countPositive([1]) = 1`).

Evidence:
[make_pinning_mutant.py](evidence/make_pinning_mutant.py),
[pinning_mutant_solution.py](evidence/pinning_mutant_solution.py),
[pinning_mutant_solution.mpy](evidence/pinning_mutant_solution.mpy),
[run_pinning_mutant_python.log](evidence/run_pinning_mutant_python.log),
[run_pinning_mutant_krun.log](evidence/run_pinning_mutant_krun.log),
[pinning_reference_search_precise.log](evidence/pinning_reference_search_precise.log),
[build_pinning_mutant_proof.log](evidence/build_pinning_mutant_proof.log), and
[prove_pinning_mutant.log](evidence/prove_pinning_mutant.log).

This is the required material body-change witness: the proof proves the manual
substitute, not the real generated program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory and supplied baseline

The fresh-source inventory contains 1,004 records:

- 252 syntax declarations;
- 737 rules;
- 5 contexts;
- 1 configuration;
- 9 reachability claims.

Of these, 928 records belong to the integrity-checked supplied semantics, 59
are proof-local definitions or syntax macros, 8 are proof-local operational
bridges, and 9 are target claims. The inventory records every function,
`total`, `symbol`/`no-evaluators`, macro, priority, `owise`, strictness,
concrete, and simplification attribute. There are 25 supplied opaque/symbol
declarations and no simplification rules.

Evidence: [rule_inventory.md](evidence/rule_inventory.md) and
[build_rule_inventory.py](evidence/build_rule_inventory.py).

Under the condition-aware boundary, each of the 928 supplied records is the
selected fixed semantics level. Static inspection found that all 25 opaque
float/sort/MD5 declarations are unreachable from this program and from every
proof summary. They cannot affect a branch, state cell, or returned value here.

### Used-syntax map and operational behavior

Every constructor in `solution.mpy` has a fixed declaration and an execution
path:

| Used construct | Declaration | Relevant fixed rules |
|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:61` | `semantics/core.k:124-127` |
| `FuncDef`, `Params`, closures | `syntax.k:53,57`; `core.k:31` | `functions.k:14-16` |
| `Name`, `Int` | `syntax.k:9,12` | `core.k:131-154,194` |
| `Assign`, `AugAssign` | `syntax.k:41,44` | `controls.k:9-31` |
| `While` | `syntax.k:46` | `controls.k:77-82,85` |
| `For` over a list | `syntax.k:45` | `controls.k:69-74`; `list.k:9-10` |
| `If` | `syntax.k:49` | `controls.k:51-54` |
| `BinOp` | `syntax.k:15` | `operators.k:12`; integer `+`, `-`, `%`, `//` in `int.k:9-20` |
| `Compare`, `CmpOp` | `syntax.k:30,32` | `operators.k:15-17`; integer comparisons in `int.k:22-27` |
| `Call` | `syntax.k:28` | `call.k:18-21,69-75`; argument order in `core.k:183-191` |
| `Return` | `syntax.k:50` | `functions.k:77-90` |

The supplied configuration has a module scope, builtins scope, monotone
allocation cells, frame stack, return cell, exception cell, and exit code.
Strict/sequence-strict declarations and the explicit argument loop provide the
needed evaluation order. Function calls allocate a local scope, bind arguments,
push a continuation, and restore state on return. Integer operations are
disjoint by operator string; the proof only divides/mods by positive 10.
Ref-specific priority rules do not overlap the integer-local path. No program
heap mutation occurs except construction of concrete test lists.

### Proof-local functions and macros

The proof-local review covers every declaration and equation at
`verification.k:7-137`:

- The digit quotient and positive/negative folds have disjoint guards,
  recursive descent on nonnegative magnitudes, and the intended base cases.
- `signedDigitSum` branches exhaustively at zero.
- `intValue` is exact on integers and is only consumed under `isInt`.
- `positiveBit`, `allInts`, and `lastOr` have disjoint/exhaustive equations.
- `countFold` descends structurally. Its `[total]` declaration is broader than
  its guarded equation on non-integer heads, but every theorem use is protected
  by `allInts`; it supplies no wrong value on the claimed domain.
- The twelve exact-syntax macros have no opacity and reproduce the current AST
  bodies/closure terms. Their lack of linkage to the file is the Stage 4
  pinning failure.

There are no proof-local opaque or simplification symbols.

Detailed evidence:
[verification_extension_review.md](evidence/verification_extension_review.md).

### Operational bridges and false-conclusion witnesses

All eight operational bridges have priority 40.

| Bridge | Static decision |
|---|---|
| Positive and negative while summaries (`verification.k:145-171`) | Their separately proved loop claims match the loop head, continuation frame, local map update, and guard. Their mathematical folds agree with `% 10` and `// 10`. |
| Positive helper summary (`:177-180`) | **Unsound over its match domain.** The proof claim fixed all cells and `ret=noRet`; the rule omits every cell and accepts any continuation. |
| Negative helper summary (`:182-185`) | **Unsound by the same omitted-return-state pattern.** |
| Signed helper summary (`:191-194`) | **Unsound over its match domain.** The claim fixed the correct helper bindings and all cells; the rule retains only `isInt(V)`. |
| Count-loop-with-old-`n` summary (`:200-214`) | Not justified over its full domain: the claim required `L != 0` and exact scope-0 helper bindings; the rule drops both and all other cells. |
| Empty count-loop summary (`:220-228`) | Extensionally agrees with fixed empty iteration, but its cited claim is narrower than the rule. |
| Nonempty count-loop summary (`:230-243`) | Not justified over its full domain for the same dropped `L != 0` and helper-scope conditions; it also depends on the unsound signed summary. |

Two concrete witnesses use integer 12, an intended-domain value:

1. Positive helper: with `<ret>retV(99)</ret>`, the priority-40 bridge proves
   result 3 and `#Top`. The preceding layer gets stuck at `Return(3)` because
   the supplied Return rule requires `noRet`. The negative rule has the same
   concrete false conclusion with magnitude 12: bridge result 1 versus a fixed
   stuck `Return(1)`.
2. Signed helper: with an empty module scope, the priority-40 bridge proves
   result 3 and `#Top`. The preceding layer executes the real signed body and
   gets stuck at `#look("positive_digit_sum",-1)`.

Evidence:
[bridge_witness.k](evidence/bridge_witness.k),
[positive_bridge_enabled_witness_corrected.log](evidence/positive_bridge_enabled_witness_corrected.log),
[positive_bridge_fixed_comparison_corrected.log](evidence/positive_bridge_fixed_comparison_corrected.log),
[bridge_enabled_witness.log](evidence/bridge_enabled_witness.log), and
[bridge_fixed_comparison.log](evidence/bridge_fixed_comparison.log).

The earlier similarly named positive-bridge logs without `_corrected` used the
pre-bridge module by mistake and exited nonzero; they are retained rather than
hidden but are not cited as the comparison result. Likewise, the first pinning
search matched a comment; the precise anchored search is the authoritative
one.

These are false operational conclusions, not mere unproved optimizations.
Priority makes them preempt fixed execution. They violate complete-context,
state-footprint, and universal-connection obligations.

## 6. Fresh non-vacuity test

The reviewer-created mutation changes the final result obligation from
`countPositive(VS)` to `countPositive(VS) +Int 1`. It is false for the
satisfying empty-list input: `allInts(.ValSeq)` is true, the actual result is 0,
and the mutated target is 1.

The mutation successfully parsed and generated its backend command under
`--dry-run` (exit 0). The actual proof exited 1 with
`WarnStuckClaimState`; its residual contains the expected impossible equality
between the same count fold and that fold plus 1. This is a reached unmet
result obligation, not a parser/import/backend failure.

Evidence: [spec-vacuity.k](evidence/spec-vacuity.k),
[vacuity_dry_run.log](evidence/vacuity_dry_run.log), and
[vacuity_proof_expected_failure.log](evidence/vacuity_proof_expected_failure.log).

Therefore the synthetic claim is result-constraining and non-vacuous. The
submission fails for soundness and program identity, not because its
postcondition is unconstrained.

## 7. Proven versus assumed accounting

### What the successful reachability run actually establishes

Under the candidate's extended K theory, a manually constructed
`countNumsClosure`, started in a manually constructed clean state with the
three manually constructed helper bindings, is derivable to
`countPositive(VS)` whenever `VS` is a finite internal sequence of integers.
The layered claims also derive the stated helper and loop summaries.

Because the imported theory contains the false operational bridges above, this
is only derivability in that extended theory, not a sound reachability theorem
of the fixed supplied semantics. Because the entry term is synthetic, it is
also not a theorem that executes the submitted `solution.mpy`.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Integrity-checked supplied MPY semantics | Defines parsing, evaluation, scopes, calls, loops, integer operations, and configuration | Acceptable fixed semantics selected by the task. |
| K backend and builtin INT/BOOL/MAP/LIST theories | All symbolic and concrete execution | Ordinary machine-checking trust boundary; no observed infrastructure failure. |
| Trusted `py2mpy.py` | Establishes the submitted `.mpy` bytes correspond to `solution.py` | Acceptable translator boundary for artifact identity; byte equality was checked. |
| Manual body/closure/binding macros | Determine what the proof actually executes | **Illegitimate bridge to the real program.** Textual agreement is reviewer observation, not an execution/link dependency; the body mutant proves insensitivity. |
| Digit/count mathematical folds | Fix the claimed result | Acceptable ordinary integer mathematics on guarded integer sequences; ground tests support, but do not replace, their K connections. |
| Priority-40 function and count summaries | Replace real execution and directly determine branches/results | **Illegitimate.** Complete-state connection theorems are absent; two machine witnesses show false conclusions. |
| Twenty-five supplied opaque float/sort/MD5 symbols | None on this program or proof path | Acceptable/inert for this theorem; inventory confirms no dependency. |
| Canonical differential testing | Supports the current Python implementation-to-intent bridge on 7,001 cases | Finite empirical evidence only, not universal proof and not a substitute for K pinning. |
| Informal decimal-digit argument | Relates base-10 folds to the human phrase “signed digit sum” | Mathematically credible, but downstream of an invalid proof theory and unpinned entry term. |

### Final rationale

Fresh `#Top` reconstruction, concrete execution, current-program differential
agreement, and a successful non-vacuity rejection are all positive evidence.
They do not cure either decisive defect. The proof can survive a material
change to the real generated program, and its proof-local theory admits normal
results that fixed execution demonstrably does not. Accordingly, it is not a
legitimate partial-correctness proof of the real submitted program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
