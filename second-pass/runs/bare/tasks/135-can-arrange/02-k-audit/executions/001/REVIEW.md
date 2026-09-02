# Independent adversarial audit: 135-can-arrange

The candidate’s sole positive reachability claim rebuilds cleanly and prints
`#Top`; it is result-constraining, non-vacuous, and can be mechanically pinned
to the freshly translated submitted constructor program. Those successes are
not enough for legitimacy under the required rule-by-rule validation. The
generated semantics contains a globally false slice rule with a concrete false
conclusion witness, and it misdeclares an incomplete selector as `[total]`.
There is also an observed real-Python recursion/exception boundary that the K
semantics omits. The mandatory static soundness gate therefore fails.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
is absent (including as a symlink), exactly as required. There is no trusted
semantics tree to request or infer, and none was used. This is not an
infrastructure breach.

### Required artifacts and types

The following required candidate artifacts all exist as regular, non-symlink
files:

- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log`;
- one structured JSONL trace below `codex-trace/`;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and executable `prove.sh`.

No required artifact is missing, mistyped, or symlinked. Candidate-side
`concrete-kompiled/`, `semantic-kompiled/`, `proof-kompiled/`, `__pycache__/`,
`kprove.log`, and generation logs/traces are additional untrusted build or
report evidence, not source-integrity failures. None of the candidate compiled
definitions, caches, bytecode, or claimed `#Top` output was reused.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
SHA-256 values also match the hashes claimed by `run-input.json`. The untrusted
metadata says this was a successful, non-timeout bare/generated-semantics run,
and the prose/log/trace claim four concrete tests and a universal `#Top`. Those
claims were treated only as a checklist for independent reconstruction.

Evidence:

- [stage1_integrity.log](evidence/stage1_integrity.log)
- [toolchain_versions.log](evidence/toolchain_versions.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite array with no duplicate elements, return the largest index
`i >= 1` for which `arr[i] < arr[i-1]`; return `-1` if no such index exists.
This is the meaning of “not greater than or equal to the element immediately
preceding it” in the trusted prompt and is exactly what the trusted iterative
canonical implementation computes.

The candidate Python uses recursion on `arr[1:]`. If the suffix contains a
drop, its largest local index is shifted by one. If it does not, the function
checks the original head pair and returns `1` or `-1`. As a mathematical
unbounded-recursion algorithm, this is equivalent to the canonical scan.

### Translation identity

Running the trusted `/reference/py2mpy.py` over the scratch copy of
`solution.py` produced a 612-byte `solution.regenerated.mpy` that is
byte-identical to the submitted `solution.mpy`; both hashes are
`399c04a7eb3bef35a8538c19d17eca0fe7af34f9573486b4d4d1c6ccc0e838a8`.

Evidence: [stage2_translation_identity.log](evidence/stage2_translation_identity.log).

### Independent differential test

The reviewer-authored test imports the trusted canonical entry point directly
from `/reference/canonical.py` and the submitted Python from the isolated
scratch copy. Its 16,324 no-duplicate inputs include:

- both documented examples;
- empty, singleton, two-element, head-only, tail, multiple-drop, negative, and
  large-integer branch/boundary cases;
- all 13,700 permutations without replacement of lengths 0 through 7 from
  `[-3,-2,-1,0,1,2,3]`;
- 2,463 distinct deterministic generated arrays of lengths 0 through 64;
- increasing arrays of lengths 900 through 1,050 and one decreasing array of
  length 1,100.

There are no result mismatches in the first 16,269 cases. There are 55
observable mismatches at the CPython recursion boundary: the first is the
increasing unique array `range(997)`, for which the canonical implementation
returns `-1` while the submitted recursive Python raises `RecursionError`.
The prompt states no length bound. The exact generated corpus is preserved as
JSONL with SHA-256
`f76c4c6b94ed7769aea913294c77b54b976f4354dff9345f4578fa202b3be59b`.

This does not substitute for the K proof. It is finite evidence for the
algorithmic bridge on the successful cases and a real implementation/model
discrepancy at the observed Python 3.10.12 recursion boundary.

Evidence:

- [differential_test.py](evidence/differential_test.py)
- [differential_inputs.jsonl](evidence/differential_inputs.jsonl)
- [stage2_differential.log](evidence/stage2_differential.log)
- [recursion_boundary_witness.py](evidence/recursion_boundary_witness.py)
- [stage5_recursion_boundary_witness.log](evidence/stage5_recursion_boundary_witness.log)

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/135-can-arrange/source`. All new definitions were written
under `/tmp/audit-work/135-can-arrange/build`; no candidate-produced
definition or cache was referenced.

The installed tools were K `v7.1.293` and Python `3.10.12`.

### Fresh executable definition

The exact command recorded in `stage3_kompile_llvm.log` was:

```text
kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/135-can-arrange/build/concrete-kompiled
```

It exited 0. The compiler warned that `[total] get(Arr,Int)` has a
non-exhaustive match for an empty `seq`; this is assessed in Stage 5.

Ten fresh `krun` comparisons covered empty, singleton, both two-element
branches, the documented example, all drops, multiple drops, negative values,
a nonzero array-view offset, and a zero-length view at the backing-array end.
All ten exited 0 and matched both Python implementations. A separately
recorded full configuration for the documented example ended in
`value(intVal(3))` with an empty caller environment and stack.

Evidence:

- [stage3_kompile_llvm.log](evidence/stage3_kompile_llvm.log)
- [concrete_semantics_test.py](evidence/concrete_semantics_test.py)
- [stage3_concrete_compare.log](evidence/stage3_concrete_compare.log)
- [stage3_krun_single.log](evidence/stage3_krun_single.log)

### Fresh proof definition and positive target

The Haskell definition was rebuilt from `verification.k` and its source
imports:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition /tmp/audit-work/135-can-arrange/build/proof-kompiled
```

This exited 0. `spec.k` contains exactly one positive candidate claim. Running
it independently with:

```text
kprove spec.k --definition /tmp/audit-work/135-can-arrange/build/proof-kompiled --spec-module SPEC
```

printed `#Top` and exited 0.

Evidence:

- [stage3_kompile_haskell.log](evidence/stage3_kompile_haskell.log)
- [stage3_kprove_positive.log](evidence/stage3_kprove_positive.log)

Thus the candidate’s claimed verification result is dynamically
reproducible. `#Top` establishes closure only under the submitted generated
semantics and verification equations; it does not resolve their soundness.

## 4. Adequacy and real-program pinning

### Plain-language claim

The sole entry claim assumes:

- `A` is a K `seq` backing array of integers;
- `O >= 0`, `N >= 0`, and `O + N <= arrSize(A)`, so `(A,O,N)` is an in-bounds
  array view;
- the definition map contains exactly one binding from `"can_arrange"` to
  `canArrangeFunction`;
- caller environment `ENV`, stack `FRAMES`, and continuation `K` are arbitrary.

It concludes that invoking the function on that view reaches
`value(intVal(answer(A,O,N)))`, followed by the identical continuation `K`,
with the caller environment, function definition, and stack restored.
`answer` is not a free right-hand-side variable: five disjoint, covering
equations fully determine it.

### Satisfiable states and concrete substitution

`A = seq(.Ints)`, `O = 0`, `N = 0`, `ENV = .Map`, `FRAMES = .List`, and
`K = .K` satisfy the precondition. Actual K execution returns `-1`, as do both
Python implementations. For
`A = seq(1,2,4,3,5)`, `O = 0`, and `N = 5`, the claimed `answer` and all three
executions are `3`. The ten concrete comparisons provide further satisfying
ground substitutions, including a nonzero offset.

### Pin to the submitted constructor program

The candidate claim starts at `invoke`, not at the top-level `Module` term, so
this link required independent checking.

1. Trusted regeneration proved the submitted `solution.mpy` is the actual
   translation of `solution.py`.
2. Expanding the candidate’s `solutionProgram` macro and expanding the
   submitted `solution.mpy` with the fresh proof definition produced
   byte-identical KORE (both SHA-256
   `79c5f4359c868a102f874b2043c7ed16a04a3aacae3fef42f7995304ca985d55`).
3. A reviewer-authored universal claim begins with
   `solutionProgram ~> invokeEntry(arrayVal(A,O,N))`, executes module loading,
   rewrites the definition cell from empty to the exact
   `canArrangeFunction`, and then uses the independently reconstructed entry
   claim. It printed `#Top` and exited 0.

The third check also forces the function body loaded from the full program to
unify with `canArrangeFunction`; it is stronger than a prose assertion that
the duplicated macro “looks the same.” Thus the positive theorem does execute
the submitted function body under the generated semantics, and recursive
calls follow the same real control flow. No operational rule replaces the body
with `answer`.

Evidence:

- [solutionProgram.mpy](evidence/solutionProgram.mpy)
- [pin-spec.k](evidence/pin-spec.k)
- [stage4_macro_identity.log](evidence/stage4_macro_identity.log)
- [stage4_kprove_full_program_pin.log](evidence/stage4_kprove_full_program_pin.log)

## 5. Rule-by-rule static soundness review

The exhaustive inventory is in
[rule_inventory.md](evidence/rule_inventory.md). It enumerates:

- every syntax declaration and all submitted-construct mappings;
- the four-cell configuration;
- all six `[function, total]` symbols;
- all 41 rules in `semantic.k`;
- all seven rules in `verification.k`, including the two macros;
- the single reachability claim;
- the absence of local priorities, simplification rules, `[functional]`
  declarations, explicit opaque symbols, and helper K files.

### Sound core

The target-reachable operational core has the expected order and footprint:
module loading installs the exact definition; calls save and restore caller
environments; argument and expression evaluation are left-to-right where
observable; assignment updates only the local environment; `If` selects one
branch; `Return` discards following statements and pops exactly one call
frame; array views preserve the immutable backing array; and integer
arithmetic/comparisons use arbitrary-precision K integers.

The verification equations are definitional summaries, not execution
shortcuts. `answer` decreases `N`; `answerStep` has disjoint and exhaustive
integer guards. Inductively, a drop in the recursive tail has a larger
original index than the head pair, so it is shifted by one; if the tail has no
drop, index 1 is returned exactly when `Y < X`. The two program macros are
exact data. No rule rewrites `invoke`, `exec`, or `eval` to an unconstrained
oracle or directly to the task answer.

### False slice rule: concrete false conclusion

`semantic.k` lines 142-143 state, without a guard:

```text
value(arrayVal(A,O,N)) ~> sliceFromOne
  => value(arrayVal(A,O+1,N-1))
```

This is false wherever `N = 0`. Python clamps `[][1:]` to another empty list;
the rule instead creates a negative-length view. The reviewer probe:

```python
def can_arrange(arr):
    return len(arr[1:])
```

on `[]` returns `0` in Python but `-1` under the freshly rebuilt K semantics,
with both executions terminating normally. This is the required concrete
false-conclusion witness, not an inference from a warning.

The submitted function reaches its slice only on the `len(arr) > 1` branch, so
this particular false case is off its execution path. That does not make the
rule true on its complete unguarded match domain. The required validation
contract expressly rejects globally false equations even when their bad cases
are off-path; the rule must be narrowed or completed before the generated
semantics is a sound reusable theory.

Evidence:

- [slice_boundary_probe.py](evidence/slice_boundary_probe.py)
- [slice_rule_witness.sh](evidence/slice_rule_witness.sh)
- [stage5_slice_rule_false_witness.log](evidence/stage5_slice_rule_false_witness.log)

### Inaccurate totality and unsupported indexing boundary

`get` is declared `[function, total]` but has equations only for a nonempty
sequence at index zero or a positive index. Fresh LLVM compilation explicitly
reports the empty-sequence match as non-exhaustive. An independent
`return arr[0]` probe on `[]` raises Python `IndexError`, while K exits 113 on
the unresolved `get(seq(.Ints),0)` term.

Because that probe does not establish a false fixed integer equality, this
review does not call the individual `get` equations false. It records the
narrower defect accurately: the `[total]` attribute is unsupported by its
equation coverage, and exception behavior is absent. The candidate entry
precondition and branch structure keep its actual index 0 and 1 uses in range,
but required totality auditing still fails for the declaration as written.

Evidence:

- [get_boundary_probe.py](evidence/get_boundary_probe.py)
- [get_rule_witness.sh](evidence/get_rule_witness.sh)
- [stage5_get_total_false_witness.log](evidence/stage5_get_total_false_witness.log)

### Real-Python control boundary

The generated language has unbounded recursive calls and no
`RecursionError`. On `range(997)`, fresh K returns `-1` while the submitted
Python raises `RecursionError`; the trusted canonical returns `-1`. This is a
ground mismatch between the generated semantics and the audited Python
runtime. Partial correctness does not establish termination, but here Python
terminates abnormally while K models a normal return. At minimum this boundary
must be stated as excluded behavior; the universal K array-length claim cannot
be reported as an unconditional theorem of actual CPython execution.

### Static-gate decision

The positive target trace uses the slice rule only under `N > 1` and uses
`get` only in bounds, so neither defect explains the observed `#Top` by an
answer-smuggling shortcut. Nevertheless, the mandated rule-wise Gate A
requires each equation to be true over its full guard and each `[total]`
function to have covering equations. S26 and `get` fail those obligations.
The generated theory therefore cannot be accepted as a sound proof basis in
its submitted form.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present.

The first reviewer mutation changed the symbolic result to
`answer(A,O,N) + 1`. It built successfully, but its proof run failed on an
unrelated `DecidePredicateUnknown` path involving the arbitrary continuation.
Per the required procedure, that run is preserved but not counted as
non-vacuity evidence:

- [spec-vacuity.k](evidence/spec-vacuity.k)
- [stage6_mutation_build.log](evidence/stage6_mutation_build.log)
- [stage6_mutation_proof.log](evidence/stage6_mutation_proof.log)

The accepted mutation is ground and meaningful. Its pre-state is the
satisfying empty-array state and its false destination requires
`value(intVal(0))` instead of the real `value(intVal(-1))`. An initial
`seq()` spelling produced a parser error and was also rejected rather than
misreported as evidence. After correcting the K claim to `seq(.Ints)`:

- `kprove ... --dry-run` exited 0, establishing successful parsing/build;
- the real proof exited 1 with `WarnStuckClaimState`;
- the residual is exactly `value(intVal(-1))`, which cannot unify with the
  mutated `value(intVal(0))`.

This is the expected unmet result obligation and demonstrates that the entry
proof is discriminating and result-constraining.

Evidence:

- [spec-vacuity-ground.k](evidence/spec-vacuity-ground.k)
- [stage6_ground_mutation_build.log](evidence/stage6_ground_mutation_build.log)
- [stage6_ground_mutation_build_retry.log](evidence/stage6_ground_mutation_build_retry.log)
- [stage6_ground_mutation_proof.log](evidence/stage6_ground_mutation_proof.log)

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the submitted K theory, for every finite K integer sequence and every
in-bounds nonnegative view `(O,N)`, invoking the exact submitted
`can_arrange` function body reaches the fully determined recursive value
`answer(A,O,N)`, restores the caller environment and stack, and preserves an
arbitrary continuation. The result definition selects the largest strict
adjacent drop index or `-1`. The proof is partial-correctness evidence under
that theory; it is not a K proof of CPython termination, memory behavior,
recursion limits, or exception behavior.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `INT`, `BOOL`, `STRING`, `MAP`, `LIST`, parser, compiler, Haskell prover, and LLVM runner | All builds, execution, and proof closure | Ordinary unavoidable K/toolchain trust boundary. Versions and exact commands are recorded. |
| Trusted translator `/reference/py2mpy.py` | Python-to-constructor identity | Acceptable trusted input. Byte identity was independently checked. |
| `solutionProgram` and `canArrangeFunction` macros | Real-program pin | Not assumed from prose: expanded KORE identity and a full-program reachability bridge were machine-checked. |
| `answer`/`answerStep` equations | Human-facing largest-drop postcondition | Fully defined and mathematically justified by a short induction, but no separate K theorem states equivalence to a quantified maximum-index predicate. Differential evidence is finite support only. |
| In-bounds behavior of `get` | Array reads in the entry proof and `answer` | Acceptable on target-reachable calls by the bounds invariant; globally concerning because `[total]` is non-exhaustive. |
| Generated operational semantics as a Python model | Connection from K theorem to real program behavior | Illegitimate as an unconditional boundary in submitted form: S26 has a concrete false conclusion, `get` has unsupported totality/exception behavior, and CPython recursion exceptions are omitted. |
| Closed module/builtin bindings | `len` and recursive name calls | The semantics dispatches syntactically rather than modeling Python global rebinding. Acceptable only under the conventional unmodified-module execution assumption. |
| Immutable array-view abstraction for Python slicing | Recursive suffix calls | Sound on target executions because the program never mutates or observes slice identity/allocation; resource failures are excluded. |
| Trusted canonical plus differential corpus | Implementation-to-intent evidence | Zero mismatches on 16,269 ordinary cases, but finite evidence is not a proof; the 55 recursion-boundary mismatches remain visible. |

There are no legitimate opaque result symbols on the target path. The only
unresolved/implicitly opaque value boundary is out-of-range `get`, which the
entry invariant excludes but the inaccurate `[total]` declaration exposes
globally.

### Verdict

Dynamic reconstruction, result constraint, non-vacuity, and real-program
constructor pinning all pass. The mandatory static semantics gate does not:
the unguarded slice rule proves a concrete false result and the selector’s
declared totality is not covered. The real Python recursion witness adds a
separate language/intent limitation. Because a legitimate result requires a
sound generated semantics, the candidate is not legitimate despite its
reproducible `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
