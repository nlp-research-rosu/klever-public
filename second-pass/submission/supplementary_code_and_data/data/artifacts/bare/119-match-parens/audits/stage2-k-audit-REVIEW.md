# Independent adversarial review: 119-match-parens

The candidate is **not a legitimate proof of the full HumanEval contract**.
Fresh reconstruction does produce `#Top`, and the formal postcondition is
non-vacuous, but closure depends on two proof-only priority rules that replace
the program-defined helper and entry function with their desired mathematical
answers. Neither has the required bridge-free universal execution theorem; both
are false over their complete match domains. Independently, the recursive
Python rewrite raises `RecursionError` on valid unrestricted-domain inputs for
which the canonical implementation returns `"Yes"`, while the generated
semantics has no recursion-limit or exception behavior.

These are independent fatal grounds. The first invalidates the reachability
argument even inside the supplied K theory's intended execution story. The
second materially narrows/mis-models the source-contract domain and is a
`FAIL / NOT_LEGIT` under the benchmark-specific decision rule.

## 1. Input and provenance integrity

Status: **PASS; no audit infrastructure breach.**

I read `/audit-input.json` first. It declares:

- problem `119-match-parens`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- candidate mount `/candidate`;
- trusted files `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py`.

The complete independent check is
[provenance_check.py](/audit-output/evidence/provenance_check.py), with exact
command and results in
[stage1-provenance-final.log](/audit-output/evidence/stage1-provenance-final.log).
It checked real-file/real-directory types with `lstat`, rejected linked or
unsupported tree entries, independently hashed file contents and trees, and
exited 0.

The launcher campaign object is exactly equal to
`/audit-campaign-lock.json`, whose SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`. All recorded direct hashes match for the run
manifest, task manifest, stage-1 result, invocation, generation metrics,
generation output, generation last message, generation prompt, usage record,
trusted prompt, translator, and canonical implementation. The sole structured
trace file has the exact SHA-256 declared by both the invocation and stage
result. An independent path/type/size/content tree digest reproduces:

- trace digest
  `04f132bd59e80f6cb2320b6da367dbe38c57f73c385dccfe570386d2b768e624`
  from `usage.json`; and
- candidate workspace digest
  `f41e8aac9be65e7370e1586ed72a4db62fdb096faae5c867f1f854be4b4a0c80`
  from `invocation.json`.

`/audit-input.json` additionally records legacy-selection tree digests under a
different launcher convention. Those values are printed in the evidence log;
they were not incorrectly compared with the documented path/type/size/content
digest. The content-bound stage records, every leaf digest, and the complete
entry inventory all agree.

As required for `legacy-selected-stage1`, I read `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, the present `usage.json`,
and every JSONL event under `codex-trace/`. The parser read all 234 trace
events and the entire 903,610-byte console log; the bounded structural summary
is in
[stage1-generation-records.log](/audit-output/evidence/stage1-generation-records.log).
Those generation records were treated only as untrusted claims. Historical
runtime metrics were not recorded in this legacy layout and are not required.

Candidate `prompt.py` and `py2mpy.py` are regular files and byte-identical to
their trusted mounts. No `/reference/reference-semantics` exists, as required
for `GENERATED_SEMANTICS`, and the candidate does not smuggle in a
`reference-semantics/` tree. Every required candidate proof artifact is a
regular file. There were no candidate-provided K compiled definitions to
reuse; the Python `__pycache__` was ignored.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **FAIL on the unrestricted source-contract domain.**

The trusted prompt says the input is a list of exactly two strings over `(` and
`)`. The function must return `"Yes"` exactly when one of the two concatenation
orders is a balanced-parentheses string, otherwise `"No"`. It states no length
bound.

The trusted canonical function iterates over each concatenation with an integer
balance, rejects a negative prefix, and accepts only final balance zero.
Candidate `solution.py` computes the same predicate recursively by slicing off
one character per call, first testing `lst[0] + lst[1]` and then the reverse.

Trusted regeneration was exact:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`8dbd9d8ccd21ca1bc99a1eb0aad2aa0eb7873eedc7d449b423bb12a5d8548e5b`;
see
[stage2-translation.log](/audit-output/evidence/stage2-translation.log) and
[regenerated-solution.mpy](/audit-output/evidence/regenerated-solution.mpy).

The independent differential script is
[differential_test.py](/audit-output/evidence/differential_test.py). It imports
the trusted canonical entry point and candidate entry point separately. It
tests the two examples, empty inputs, first-order and second-order-only cases,
negative-prefix and unmatched-positive boundaries, every pair whose two
components each have length at most six (16,129 pairs), and recursion-boundary
nested strings. The first 16,141 named/small checks agree. The complete run
checks 16,153 cases and reports seven long-input mismatches, exiting 1 as
recorded in
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).

A minimal observed witness is:

```text
lst = ["(" * 498 + ")" * 498, ""]
trusted canonical: returns "Yes"
candidate: raises RecursionError("maximum recursion depth exceeded in comparison")
```

This is a valid documented-domain input. The mismatch starts at constructed
length 996 under the recorded CPython 3.10.12 recursion limit of 1000. It is
not a finite-test conjecture: this one concrete exception is already a material
result divergence, and there is no source-contract size restriction that
excludes it.

## 3. Clean proof reconstruction

Status: **machine closure PASS under the candidate theory; real-program
validation FAIL.**

All work occurred in the fresh scratch directory recorded by
[scratch-path.txt](/audit-output/evidence/scratch-path.txt). I copied source
artifacts only, used newly named output definitions, and did not reuse any
candidate cache or compiled definition. The observed toolchain is K
v7.1.293; see
[stage3-toolchain.log](/audit-output/evidence/stage3-toolchain.log).

Fresh concrete build:

```text
kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled
```

It exited 0
([stage3-kompile-semantic.log](/audit-output/evidence/stage3-kompile-semantic.log)).
The independent K/Python comparison
[k_python_compare.py](/audit-output/evidence/k_python_compare.py) runs the
actual regenerated `solution.mpy` under that definition on 12 normal and
boundary cases. Empty, both prompt examples, first-order, second-order-only,
early-negative, unmatched-positive, and nested cases all agree with both
Python functions, with zero mismatches and exit 0
([stage3-k-python-compare.log](/audit-output/evidence/stage3-k-python-compare.log)).
Individual full configurations are also preserved in the `stage3-krun-*.log`
files.

An optional 996-character concrete K stress run ended when `kore-exec` was
killed with exit 137
([stage3-krun-long-996.log](/audit-output/evidence/stage3-krun-long-996.log)).
That resource failure is **not** used as candidate evidence or converted into
a verdict. The recursion-model defect is established instead by the concrete
CPython witness and by static absence of any recursion/exception state in the
generated semantics.

Fresh proof build and positive proof:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-VERIFICATION \
  --output-definition audit-verification-kompiled
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

The build exited 0
([stage3-kompile-verification.log](/audit-output/evidence/stage3-kompile-verification.log)).
The unfiltered `SPEC` module contains all three positive claims; `kprove`
exited 0 and printed `#Top`
([stage3-kprove-positive.log](/audit-output/evidence/stage3-kprove-positive.log)).
This establishes closure only under `verification.k`, whose two decisive
extensions fail Stage 5.

## 4. Adequacy and real-program pinning

Status: **constructor pinning PASS; theorem-to-real-execution adequacy FAIL.**

The claims mean:

1. Universal claim (`spec.k:8-13`): from an empty environment/function map,
   execute `solutionProgram` on an arbitrary two-element
   `ListExpr(PStr(A),PStr(B))`; terminate with empty `<k>` and result exactly
   `strVal(contractAnswer(A,B))`.
2. First example (`spec.k:16-21`): the same start for `["()(", ")"]` must end
   with exactly `yesString`.
3. Second example (`spec.k:23-28`): the same start for `[")", ")"]` must end
   with exactly `noString`.

There are no `requires` clauses. The universal precondition is satisfiable,
for example by `A = .PString`, `B = .PString`; the expected result is
`yesString`. Another satisfying substitution is `A = rp .PString`,
`B = lp .PString`, whose reverse order is balanced and also yields
`yesString`. Fresh K configurations for both are in
[stage4-entry-witness-empty.log](/audit-output/evidence/stage4-entry-witness-empty.log)
and
[stage4-entry-witness-second-order.log](/audit-output/evidence/stage4-entry-witness-second-order.log).
They agree with both Python implementations at these concrete sizes. The
postcondition constrains the result; the existential final function map does
not make the result free.

Program-term pinning is genuine. In addition to trusted byte regeneration, I
parsed actual `solution.mpy` and independently parsed `solutionProgram` under
the proof definition. After accounting for the generated top-cell
initialization step, one `solutionProgram` rewrite yields a byte-identical KORE
configuration to the actual parsed module. Both SHA-256 values are
`191ddbd0f1790a62ec1e0d4196408a4287ccb48062d027c238ba21a2e7e95565`;
see
[stage4-program-pinning-depth-adjusted.log](/audit-output/evidence/stage4-program-pinning-depth-adjusted.log).
The two earlier logs preserve the harmless diagnostic attempts that exposed
the needed initialization-depth offset.

Body sensitivity also passes. I changed the final `Return(Str("No"))` in the
program term actually expanded by `solutionProgram` to
`Return(Str("Yes"))`, without changing the summary's exact body pattern. The
mutated definition built, and its proof failed with a reachable residual
containing the changed body:
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
[stage5-kprove-body-mutation.log](/audit-output/evidence/stage5-kprove-body-mutation.log).

Thus this is not a substituted constructor program. The fatal gap is that
proof execution of its two functions is then preempted by unproved summaries,
and that the underlying language model idealizes away a real exceptional
behavior.

## 5. Rule-by-rule static soundness review

Status: **FAIL.**

The exhaustive declaration/rule inventory is
[RULE-INVENTORY.md](/audit-output/evidence/RULE-INVENTORY.md), supported by the
mechanical declaration scan in
[stage5-declaration-scan.log](/audit-output/evidence/stage5-declaration-scan.log).
It enumerates every local syntax production, configuration cell, function,
partial/opaque symbol, ordinary semantic rule, priority rule, and claim in
`semantic.k`, `verification.k`, and `spec.k`. There are no helper K files, no
local `[total]`, `[functional]`, `[simplification]`, or `[concrete]` rules, and
no unlisted priority rules.

The generated operational semantics has explicit coverage for every
constructor used by `solution.mpy`: module/function loading, `If`, `Return`,
names, literals, two-element lists, left-to-right binary operations and
comparisons, list/string indexing, the exact `[1:]` slice, one/two argument
calls, local-map restoration, and entry/result handling. The inductive
parenthesis operations and equality equations are mathematically truthful on
the used subset. `ptail` is declared `[function]` without equations but is
unused and cannot influence control, state, or result. Missing behavior for
unused constructs is not counted as a defect.

There are two decisive invalid extensions:

### `is_balanced` operational bridge

`verification.k:25-43` has priority 40 and rewrites an invocation of the exact
program-defined closure directly to `boolVal(balanced(S,D))`. It matches an
arbitrary continuation, omits `<functions>` and all other cells, and supplies a
result-bearing value. There is no bridge-free universal connection claim over
its complete match domain. The same `balanced` result is simply used by the
caller reasoning.

This rule is concretely false over its complete domain, even with a valid
parenthesis string. The preserved probe invokes the exact closure with
`S = lp rp .PString`, `D = 0`, and an empty function map:

- fixed `MPY-SEMANTICS` executes until the recursive
  `eval(Name("is_balanced"))` lookup and gets stuck with `noResult`;
- bridge-enabled semantics bypasses that lookup and terminates with
  `boolVal(true)`.

Sources:
[bridge-witness-fixed.k](/audit-output/evidence/bridge-witness-fixed.k) and
[bridge-witness-extended.k](/audit-output/evidence/bridge-witness-extended.k).
Results:
[stage5-krun-bridge-fixed.log](/audit-output/evidence/stage5-krun-bridge-fixed.log)
and
[stage5-krun-bridge-extended.log](/audit-output/evidence/stage5-krun-bridge-extended.log).

### `match_parens` operational bridge

`verification.k:48-65` has priority 40 and rewrites invocation of the exact
entry closure directly to `strVal(contractAnswer(A,B))`—the exact mathematical
postcondition. It is therefore an answer-encoding operational replacement,
not a derived invariant claim. It also omits the required `"is_balanced"`
binding and has no bridge-free connection theorem.

The separate ground probe invokes that closure on two valid empty
parenthesis strings with an empty function map:

- fixed semantics gets stuck at `eval(Name("is_balanced"))` with `noResult`;
- bridge-enabled semantics terminates with `strVal(yesString)`.

Results are in
[stage5-krun-match-bridge-fixed.log](/audit-output/evidence/stage5-krun-match-bridge-fixed.log)
and
[stage5-krun-match-bridge-extended.log](/audit-output/evidence/stage5-krun-match-bridge-extended.log).

The malformed function maps in these probes are not claimed reachable from the
entry precondition, which loads the expected bindings. They are witnesses that
the globally installed rules are false over the rules' own complete match
domains; rule priority and off-path arguments cannot establish soundness. For
reachable entry states, the independently fatal obligation remains: no
bridge-free universal theorem connects either program-defined computation to
its summary. Finite examples do not supply that theorem.

The proof depends on these bridges. I removed both and rebuilt successfully
([verification-no-bridges.k](/audit-output/evidence/verification-no-bridges.k),
[stage5-kompile-no-bridges.log](/audit-output/evidence/stage5-kompile-no-bridges.log)).
The universal proof then exits 1 at the actual recursive helper body with a
`WarnStuckClaimState`, leaving two unexplored branches
([stage5-kprove-no-bridges.log](/audit-output/evidence/stage5-kprove-no-bridges.log)).
There is no auxiliary circularity/connection claim in the candidate that can
replace the invalid rules.

Finally, the generated language model has no recursion-depth cell, exception
cell, stack-overflow condition, or `RecursionError` rule. Its call rules
therefore model idealized unbounded recursion. The concrete valid 996-character
Python witness from Stage 2 shows the resulting false source-level conclusion:
the formal claim prescribes `yesString`, while the real candidate terminates by
exception. This is a material semantics-adequacy failure, not missing support
for an unused construct.

## 6. Fresh non-vacuity test

Status: **PASS (but does not cure Stage 5).**

I ignored any candidate narrative and created the fresh mutation
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k). It changes the
universal result obligation to `strVal(yesString)` for every `A,B`. The
satisfying ground witness `A = rp .PString`, `B = rp .PString` is demonstrably
false: fresh concrete execution returns `noString`
([stage6-vacuity-ground-witness.log](/audit-output/evidence/stage6-vacuity-ground-witness.log)).

The mutation compiled to KORE successfully:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit was 0
([stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log)).
The real proof command exited 1 with `WarnStuckClaimState`; the final
configuration unified, but the implication
`yesString == contractAnswer(A,B)` failed
([stage6-vacuity-proof.log](/audit-output/evidence/stage6-vacuity-proof.log)).
This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash.

The claim therefore discriminates a false postcondition. Non-vacuity only says
the postcondition is constrained; it does not validate the execution bridge
that manufactured the original constrained value.

## 7. Proven versus assumed accounting

Status: **the conditional theorem is clear; its decisive assumptions are
illegitimate.**

What `#Top` precisely establishes is:

> In the idealized `MPY-SEMANTICS` machine extended by all rules in
> `MPY-VERIFICATION`, `solutionProgram` started with the claim cells reaches
> the stated result for arbitrary finite inductive `PString` inputs and for the
> two examples.

It does **not** independently establish that executing the program-defined
`is_balanced` closure computes `balanced`, or that executing the
program-defined `match_parens` closure computes `contractAnswer`. Those are the
two priority rewrites added to the theory.

Trust/assumption ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 parser, Haskell backend, reachability engine, and imported `INT`, `BOOL`, `STRING`, `MAP`, `LIST` primitives | All parsing, arithmetic, maps, lists, rewriting | Acceptable low-level trust boundary; version and fresh commands recorded. |
| Trusted prompt, canonical implementation, and translator | Contract, executable oracle, source-to-constructor identity | Acceptable launcher-owned inputs; hashes match and regeneration is exact. |
| `PString` and `PStr` proof-input representation | Universal input values | Acceptable for finite strings over `(` and `)` as a mathematical encoding; concrete boundary cases agree. It does not model CPython recursion limits. |
| `chars`, `pconcat`, string head/tail/equality, and arithmetic equations | Concrete and symbolic value computation | Audited truthful on all reached cases; partial outside the promised/used subset and fail-visible there. |
| `balanced` and `contractAnswer` equations | Mathematical postcondition | Truthful mathematical definitions, but definitions alone do not connect them to program execution. |
| Priority-40 `is_balanced` bridge | Helper result, branches, final result | Illegitimate program-derived operational abstraction: globally false witness, no complete-context bridge-free connection theorem. |
| Priority-40 `match_parens` bridge | Direct final result | Illegitimate and circular answer substitution: globally false witness, no connection theorem, RHS is the postcondition summary itself. |
| Idealized unbounded call semantics | Termination/control for long inputs | Illegitimate for the unrestricted real CPython program; concrete 996-character counterexample. |
| Fresh concrete K tests and Python differential tests | Finite bridge evidence only | Reproducible and useful, but not universal proof. The long Python test is a concrete refutation, while successful small tests cannot justify the summaries. |
| Unused `ptail` function | None | Harmless unused opaque/partial symbol. |

Gate accounting under the Kit validation terminology:

- Gate A (real-program soundness): **FAIL** because of both operational
  bridges and the missing CPython recursion behavior.
- Gate B (intent adequacy): **FAIL** because the unrestricted HumanEval domain
  contains valid inputs on which the candidate raises instead of returning the
  required answer.
- Gate C (auditability): evidence is reproducible, but transparency cannot
  rehabilitate failed Gates A and B.

The candidate's prior `#Top`, generation trace, example runs, and finite
3,969-pair generation test are consistent with the reconstructed evidence but
are not substitutes for the missing connection proofs. The benchmark
explicitly maps material narrowing of the HumanEval source-contract domain to
`FAIL / NOT_LEGIT`; the invalid answer-encoding bridge independently reaches
the same result.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
