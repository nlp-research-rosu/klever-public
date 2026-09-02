# HumanEval 55: the Fibonacci function, proved correct end to end

Everyone knows the Fibonacci numbers. This page walks through how a
coding agent's Fibonacci implementation was proved correct by machine —
not tested on examples, but proved for every valid input at once — and
then confirmed by two independent adversarial audits backed by
machine-checked evidence.
Every excerpt links to the real artifact in this repository. The final
verdict, from the strictest gate in the pipeline, is PASS.

## 1. What the agent was given

The agent received the verbatim HumanEval prompt [prompt.py] — a
signature, a docstring, and three examples — and nothing else about the
problem: no reference solution and no hidden tests. The session ran under
the stage-1 proof prompt (recorded verbatim:
[prompt.txt]); its final campaign revision is [kit-semantics.md].

```python
def fib(n: int):
    """Return n-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """
```

## 2. The agent's solution

The agent wrote the standard iterative solution [solution.py]: hold
two consecutive Fibonacci numbers `a` and `b`, and step them forward
`n` times. Each trip around the loop turns the pair `(a, b)` into
`(b, a + b)` and counts `n` down by one.

```python
def fib(n: int):
    a = 0
    b = 1
    while n > 0:
        b = a + b
        a = b - a
        n = n - 1
    return a
```

## 3. The theorem — and the loop invariant

The theorem lives in [spec.k], written in K — a framework for defining
programming-language semantics and proving programs against them. It is
a reachability claim ("execution from this state reaches that state"),
and it says: calling `fib` on any integer `N >= 0` produces
`fibFrom(0, 1, N)`, the N-th Fibonacci number (0, 1, 1, 2, 3, ...). It
is a partial-correctness theorem: it pins down the result of every run
that completes.

```k
  claim [fib-call]:
    <k>
      Call(Name("fib"), Int(N:Int))
      => fibFrom(0, 1, N)
    </k>
    …
    requires N >=Int 0
```

Proving a `while` loop for all `N` at once needs a loop invariant — a
fact about the loop's variables that holds on entry and keeps holding
after every iteration. Here the invariant quantity is
`fibFrom(a, b, n)`: "the value `a` will hold after `n` more steps of
the pair update `(a, b) -> (b, a + b)`". One iteration changes
`(a, b, n)` into `(b, a + b, n - 1)`, and the defining equations below
take exactly the same step — so the quantity never changes while `n`
counts down to zero, where `fibFrom(a, b, 0) = a` is the answer. The
invariant lives in [verification.k] as the summary function `fibFrom`
plus one algebraic lemma:

```k
  rule fibFrom(A, _B, N) => A
    requires N <=Int 0

  rule fibFrom(A, B, N) => fibFrom(B, A +Int B, N -Int 1)
    requires N >Int 0

  rule (A:Int +Int B:Int) -Int A => B [simplification]
```

The last line is the single arithmetic fact the proof assumes:
`(A + B) - A = B`, which is what makes the assignment `a = b - a`
recover the old `b`. The invariant is asserted over the actual loop by
the `loop-inv` claim in [spec.k]: started at the loop head with
`n = N`, `a = A`, `b = B`, the loop ends with `n = 0` and
`a = fibFrom(A, B, N)`.

```k
      1 |-> scope(
        "n" |-> (N:Int => 0)
        "a" |-> (A:Int => fibFrom(A, B, N))
        "b" |-> (B:Int => ?BFinal:Int),
        parent(0)
      )
```

Instantiated at the real entry values `a = 0, b = 1`, that is exactly
the theorem.

## 4. The K proof runs to `#Top`

[prove.sh] compiles the semantics and runs `kprove`, K's prover, which
symbolically executes the program — running it on the unknown `N`
rather than on any particular number — until every claim is
discharged. `#Top` is K's proof-complete signal: nothing is left to
prove. [PROOF.md] records the results under the headline `VALIDATED`:

```text
loop-inv: #Top   exit 0
all claims: #Top exit 0
```

The script also checks that two deliberately broken variants — a false
postcondition ([spec-vacuity.k]) and a mutated body — its
initialization `a = 0` changed to `a = 1`
([spec-body-mutation.k]) — both fail to prove, confirming the proof
genuinely constrains the program and its answer.

## 5. The independent K audit

Stage 2 hands everything to a separate adversarial session that
rebuilds the proof from source and tries to break it: it re-runs the
prover in a clean room, re-derives every provenance hash, mutates the
program body, and reviews all 698 rules in scope — 695 from the
supplied semantics plus three proof-local rules. The session ran under
the stage-2 K-audit prompt [audit.md] (final campaign revision; the
exact copy served to this session: [prompt.txt][s2-prompt]).
Its conclusion, from [stage2-k-audit-REVIEW.md]:

> The successful proof is sound, result-constraining, non-vacuous, and
> mechanically pinned to the regenerated submitted program. There is no
> material adequacy gap.
>
> VERDICT: PASS

## 6. What does the proof trust?

Stage 3 classifies every rule the proof added against a trust boundary
— an explicit ledger of what the proof assumes rather than proves. The
session — a continuation of the stage-1 proof session — ran under the
stage-3 lemma-discovery prompt (recorded verbatim: [prompt.txt][s3-prompt]);
its final campaign revision is [lemma-discovery.md].
Per [DISCOVERY.md], the two `fibFrom` equations are definitions (they
name a mathematical value and cannot touch the running program), and
exactly one rule is a domain lemma: the arithmetic identity
`(A + B) - A = B`, an assumed mathematical fact that must now be proved
somewhere else.

## 7. One obligation, exported to Lean and proved

Stage 4 deterministically exports that single domain lemma out of K
into Lean — an independent proof assistant with a small, well-studied
trusted kernel — as exactly one obligation (this stage is a mechanical
translation: no model, no prompt), stated in [Lemmas.lean]:

```lean
(∀ (A : SortInt) (B : SortInt), («_-Int_» («_+Int_» A B) A : SortInt) = (B : SortInt))
```

In plain terms: for all integers A and B, `(A + B) - A = B`. Stage 5's
[Proof.lean] fills in the two operators as honest integer subtraction
and addition and proves the statement with a two-step rewrite:

```lean
theorem final :
    Klean55Fib.Lemmas.targetStatement «_-Int_» «_+Int_» := by
  unfold Klean55Fib.Lemmas.targetStatement
  intro A B
  change A + B - A = B
  rw [Int.add_comm A B, Int.add_sub_cancel]
```

The session — a continuation of the stage-1 proof session — ran under the
stage-5 Lean-proof prompt (recorded verbatim: [prompt.txt][s5-prompt]); its
final campaign revision is [klean-prove.md].

The full generated Lean project is in [Base/]; the shipped copy was
rebuilt with `lake build` under the pinned toolchain during packaging.

## 8. The adversarial Lean audit — final verdict

Stage 6, the strictest gate, runs in another independent session. It
rebuilds the project from a clean copy, confirms the theorem depends on
no axiom beyond Lean core's standard `propext`, and even constructs a
dishonest definition of `+` and `-` that could have gamed the target —
verifying this candidate did not take that shortcut. The session ran under
the stage-6 Lean-audit prompt (recorded verbatim:
[prompt.txt][s6-prompt]); its final campaign revision is [klean-audit.md]. Quoting
from [stage6-lean-audit-REVIEW.md]:

> …the Stage 5 candidate cleanly proves that exact target with fully
> faithful integer-operation bindings and no unrecorded trust escape.
>
> VERDICT: PASS

## 9. The complete raw record

Everything above is the curated copy. The complete raw record — all
six stage directories with their hashes and machine verdicts — is
[the run directory], and the stage-1 agent's full session log (every
command it ran while writing the solution and proof) is in
[invocations/].

[kit-semantics.md]: ../second-pass/prompts/kit-semantics.md
[audit.md]: ../second-pass/prompts/audit.md
[s2-prompt]: ../second-pass/runs/kit_semantics/tasks/55-fib/02-k-audit/executions/001/prompt.txt
[lemma-discovery.md]: ../second-pass/prompts/lemma-discovery.md
[s3-prompt]: ../second-pass/runs/kit_semantics/tasks/55-fib/03-lemma-discovery/invocations/001-initial/prompt.txt
[klean-prove.md]: ../second-pass/prompts/klean-prove.md
[s5-prompt]: ../second-pass/runs/kit_semantics/tasks/55-fib/05-lean-proof/invocations/001-initial/prompt.txt
[klean-audit.md]: ../second-pass/prompts/klean-audit.md
[s6-prompt]: ../second-pass/runs/kit_semantics/tasks/55-fib/06-lean-audit/executions/001/prompt.txt
[prompt.py]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/prompt.py
[solution.py]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/solution.py
[spec.k]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/spec.k
[verification.k]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/verification.k
[prove.sh]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/prove.sh
[PROOF.md]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/PROOF.md
[spec-vacuity.k]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/spec-vacuity.k
[spec-body-mutation.k]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/k_proof/spec-body-mutation.k
[stage2-k-audit-REVIEW.md]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/audits/stage2-k-audit-REVIEW.md
[DISCOVERY.md]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/classification/DISCOVERY.md
[Lemmas.lean]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/lean_proof/Base/Klean55Fib/Lemmas.lean
[Proof.lean]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/lean_proof/Proof.lean
[Base/]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/lean_proof/Base
[stage6-lean-audit-REVIEW.md]: ../second-pass/submission/supplementary_code_and_data/data/artifacts/kit_semantics/55-fib/audits/stage6-lean-audit-REVIEW.md
[the run directory]: ../second-pass/runs/kit_semantics/tasks/55-fib
[invocations/]: ../second-pass/runs/kit_semantics/tasks/55-fib/01-k-proof/invocations
