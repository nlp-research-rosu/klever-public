# HumanEval/3 `below_zero`: prompt to machine-checked proof

This is one complete pass through the kit_semantics pipeline, on one of the
simplest tasks in the campaign. A coding agent received a Python function
stub and its docstring, wrote an implementation, and proved it correct in the
K framework (a system for defining language semantics and proving that
programs reach specified end states). Two independent adversarial audits and
a deterministic export to the Lean 4 proof assistant followed. Final verdict:
**PASS**. Every linked file is a real artifact from the run, starting with
the agent's full [instruction prompt][instructions], recorded
verbatim in the run.

## 1. The task

The agent received only [prompt.py][prompt] — the docstring below, verbatim
(typo included) — the only description of the problem it got. It was
never given HumanEval's canonical solution or hidden tests.

```python
def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account fallls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """
```

## 2. What the agent wrote

The session ran under the stage-1 proof prompt (recorded verbatim:
[prompt.txt][instructions]); its final campaign revision is [kit-
semantics.md][kit-prompt].

The implementation in [solution.py][solution] is the obvious running-balance
loop: add each operation to the balance and return `True` the moment the
balance goes negative.

```python
def below_zero(operations: List[int]) -> bool:
    balance = 0
    operation = 0
    for operation in operations:
        balance += operation
        if balance < 0:
            return True
    return False
```

## 3. The theorem

The agent then stated what "correct" means as a K reachability claim in
[spec.k][spec]: starting from a fresh program state, loading this exact
function and calling it on any finite list `INPUT` must end in the value
`belowFrom(0, INPUT)` — a recursively defined summary that is `true` exactly
when some running prefix of the list sums below zero. The `requires` clause
is the precondition (every element is an integer); the right side of `=>` is
the postcondition. The audited call bridge lives in
[verification.k][verification].

```k
  claim [below-zero]:
    <k>
      #loadAll(Module(
        ImportFrom("typing", "List")
        FuncDef("below_zero", Params("operations"),
          …
          Return(Bool(false)))))
      ~> Call(Name("below_zero"), list(INPUT:ValSeq))
      => belowFrom(0, INPUT)
    </k>
    …
    requires allInts(INPUT)
```

The list length and every element are symbolic: this is one theorem about
all finite integer lists, not a batch of test cases.

## 4. The K proof

[prove.sh][prove] drives K's prover, `kprove`, over the claim (plus loop
lemmas, a smoke test, a 139,257-case differential test, and two mutation
probes that are required to fail). `kprove` printing `#Top` means the proof
is fully discharged — no unproven branch remains.

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

The recorded result in [PROOF.md][proofmd] — the agent's own proof report,
headlined `VALIDATED` — is "Actual result: `#Top`, exit 0", along with the
full inventory of every helper rule the proof introduced.

## 5. Independent K audit

A second, independent agent then tried to break the proof: it rebuilt
everything from source in a clean room, re-proved each claim, pinned the
submitted program byte-for-byte against a trusted regeneration,
matched the proved claim term to it constructor-for-constructor (one
parser-equivalent spelling normalization recorded), and injected a fresh
deliberately-false postcondition to confirm the prover rejects it. The
session ran under the stage-2 audit prompt (recorded verbatim:
[prompt.txt][s2-prompt]); its final campaign revision is [audit.md][audit-prompt]. Its [report][stage2] concludes:

> The candidate contains a legitimate partial-correctness proof of the
> submitted program for every finite list of mathematical integers.

and its verdict line reads:

> VERDICT: PASS

("Partial correctness" means: whenever the call terminates, the result is
right; termination itself is not part of the reachability claim.)

## 6. Lemma classification

Next, every one of the 14 helper rules the proof added was classified to make
the trust boundary explicit — the exact set of mathematical facts the K proof
relies on without proving them inside K. The session — a continuation of the
stage-1 proof session — ran under the
stage-3 lemma-discovery prompt (recorded verbatim: [prompt.txt][s3-prompt]);
its final campaign revision is [lemma-discovery.md][lemma-prompt]. [DISCOVERY.md][discovery] records
the split — 8 definitions, 1 operational call bridge, and 5 domain lemmas —
and the frozen result is [validated-trust-boundary.json][boundary].

> It contains 14 rules in the local `VERIFICATION`/`VERIFICATION-BASE`
> closure.

The 5 domain lemmas (facts about integer projection, guarded addition, and
finite-map deletion) are exactly what gets re-proved independently in Lean.

## 7. Five Lean obligations

A deterministic, hash-locked exporter translated those 5 domain lemmas into
Lean 4 theorem statements — no agent discretion in what must be proved.
This export stage runs no model, so there is no prompt. One
of the five, verbatim from [obligation-map.json][obligmap] (idempotence of
the integer-projection helper):

```lean
∀ (V : SortVal), (projectIntTotal (SortVal.inj_SortInt (projectIntTotal V)) : SortInt) = (projectIntTotal V : SortInt)
```

A proving agent then discharged all five in [Proof.lean][prooflean]: its
`theorem final` splits the exported target into five goals with
`refine ⟨?_, ?_, ?_, ?_, ?_⟩` and closes each one, with no `sorry` (Lean's
placeholder for an unproved gap) anywhere. The session — a continuation of
the stage-1 proof session — ran under the
stage-5 Lean-proof prompt (recorded verbatim: [prompt.txt][s5-prompt]); its
final campaign revision is [klean-prove.md][klean-prove-prompt].

## 8. Adversarial Lean audit

A final independent auditor rebuilt the Lean project from scratch, verified
every hash binding the obligations back to the frozen K rules, re-ran the
build, and checked the proof's foundations. The session ran under the
stage-6 Lean-audit prompt (recorded verbatim:
[prompt.txt][s6-prompt]); its final campaign revision is [klean-
audit.md][klean-audit-prompt]. Lean
itself reports that the proof rests only on Lean's three standard axioms:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The [audit report][stage6] concludes:

> I therefore accept both the proof result and its claimed provenance.

and, like the stage-2 audit, its verdict is:

> VERDICT: PASS

That is the pipeline's final verdict for this task: stage-6 **PASS**.

## 9. The complete raw record

Every stage above, with logs, manifests, and hashes, is preserved unedited in
[the complete raw record][rawrun]; the agent's full session log for the
proof-writing stage is in its [invocations directory][invocations].

[instructions]: ../second-pass/runs/kit_semantics/tasks/3-below-zero/01-k-proof/invocations/001-initial/prompt.txt
[kit-prompt]: ../second-pass/prompts/kit-semantics.md
[audit-prompt]: ../second-pass/prompts/audit.md
[s2-prompt]: ../second-pass/runs/kit_semantics/tasks/3-below-zero/02-k-audit/executions/001/prompt.txt
[lemma-prompt]: ../second-pass/prompts/lemma-discovery.md
[s3-prompt]: ../second-pass/runs/kit_semantics/tasks/3-below-zero/03-lemma-discovery/invocations/001-initial/prompt.txt
[klean-prove-prompt]: ../second-pass/prompts/klean-prove.md
[s5-prompt]: ../second-pass/runs/kit_semantics/tasks/3-below-zero/05-lean-proof/invocations/001-initial/prompt.txt
[klean-audit-prompt]: ../second-pass/prompts/klean-audit.md
[s6-prompt]: ../second-pass/runs/kit_semantics/tasks/3-below-zero/06-lean-audit/executions/001/prompt.txt
[prompt]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/k_proof/prompt.py
[solution]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/k_proof/solution.py
[spec]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/k_proof/spec.k
[verification]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/k_proof/verification.k
[prove]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/k_proof/prove.sh
[proofmd]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/k_proof/PROOF.md
[stage2]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/audits/stage2-k-audit-REVIEW.md
[discovery]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/classification/DISCOVERY.md
[boundary]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/classification/validated-trust-boundary.json
[obligmap]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/lean_proof/Base/obligation-map.json
[prooflean]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/lean_proof/Proof.lean
[stage6]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/3-below-zero/audits/stage6-lean-audit-REVIEW.md
[rawrun]: ../second-pass/runs/kit_semantics/tasks/3-below-zero/
[invocations]: ../second-pass/runs/kit_semantics/tasks/3-below-zero/01-k-proof/invocations/
