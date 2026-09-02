# Independent adversarial review: HumanEval/9 `rolling_max`

The candidate reconstructs to `#Top`, its Python implementation is correct, and
its claim term is the submitted generated program. It nevertheless does **not**
contain a legitimate proof of that program: the universal result is inserted by
an unproved priority rule that replaces the real loop. That rule also accepts
contexts in which it is concretely not semantics-preserving.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. I independently
read `/audit-input.json`, used only its `container_paths` for mounted inputs, and
checked `/audit-campaign-lock.json` both bytewise by its recorded SHA-256 and as
an exact JSON-object match for the campaign block.

All records required by this layout are regular, readable files:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The two additional legacy records were also read. The sole JSONL trace has 250
valid JSON records. Every single-file hash declared in `/audit-input.json`
matched; every evidence-file hash in `/generation-result.json` matched; the
trace file and trace-tree digests matched their records.

The independently reconstructed pipeline tree digest of `/candidate` is
`7884e0745b98699925dbcb9aa57c1e8a84a5f352bad36bbe39052cdec75d721a`.
It exactly matches both the retained-workspace digest in `invocation.json` and
the output-workspace digest in `generation-result.json`. `/audit-input.json`
also records a launcher-specific `candidate_tree_sha256` value
`cf8b8f71...`; its hashing serialization is not declared, so the reproducible
pipeline tree algorithm is the independent comparison used here.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. No symlink or unsupported entry exists in the candidate, reference, or
generation-evidence trees. `/reference/reference-semantics` is absent, as
required for generated semantics. There is no infrastructure breach.

The generation report's `KPROVE_PASSED` marker and prior logs were treated only
as claims. Reproducible details are in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log) and the
reviewer script
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for every finite list of integers, return a list of the
same length whose item at each position is the maximum of the input prefix
ending there. The empty input returns the empty list. The prompt example maps
`[1,2,3,2,3,4,2]` to `[1,2,3,3,3,4,4]`.

`/candidate/solution.py` implements a different but correct algorithm. It uses
`first` to initialize from the first element, updates `maximum` only when a
later item is larger, and appends the current maximum each iteration. This
correctly handles empty, singleton, equal, decreasing, and all-negative inputs.

Trusted regeneration was exact:

```text
cd /tmp/audit-work/candidate
python3 /tmp/audit-work/trusted-py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

The command exited 0. Both MPY files have SHA-256
`765a7317f571c6faad4c42a3def92b9837dc200a0af941bdfa0be3e2c4dfd056`;
see [stage2-translator.log](/audit-output/evidence/stage2-translator.log).

The independent differential oracle imports `/reference/canonical.py` and the
scratch copy of the candidate entry point. It ran 13 named boundary/branch
cases, every list of length 0 through 6 over `{-2,-1,0,1,2}` (19,531 cases),
and 2,000 deterministic generated cases of lengths 0 through 64, including
arbitrary-precision integers. All 21,544 comparisons matched. Inputs, seed,
oracle, and results are preserved in
[differential_test.py](/audit-output/evidence/differential_test.py),
[stage2_cases.json](/audit-output/evidence/stage2_cases.json), and
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).
This is finite fidelity evidence, not a K proof.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/candidate`; no candidate-built
K definition or cache was reused. K 7.1.293 was present for `kompile`, `krun`,
and `kprove`
([stage3-toolchain.log](/audit-output/evidence/stage3-toolchain.log)).

The generated concrete semantics was freshly built with:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition fresh-semantic-kompiled
```

It exited 0. Nine executions through the actual `Run(Module(...), [Ints])`
parser path covered empty, singleton, increase, equality, decrease,
all-negative, zero-crossing, prompt, and arbitrary-precision cases. Every K
result agreed with both Python functions and terminated with empty
`<functions>`, `<env>`, and `<stack>` cells. See
[stage3-concrete-compare.log](/audit-output/evidence/stage3-concrete-compare.log).
The preserved `attempt1` log is a reviewer-regex error that read nonempty K
lists as empty; the corrected parser and unchanged K executions all pass.

Both proof definitions were then compiled independently:

```text
kompile solution-ast.k --main-module SOLUTION-AST \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition fresh-operational-kompiled
kprove operational-spec.k --definition fresh-operational-kompiled \
  --spec-module OPERATIONAL-SPEC --output pretty

kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition fresh-verification-kompiled
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --output pretty
```

Every build exited 0. Both `kprove` commands exited 0 and printed `#Top`.
Exact commands and bounded output are in
[stage3-kprove-operational.log](/audit-output/evidence/stage3-kprove-operational.log)
and [stage3-kprove-spec.log](/audit-output/evidence/stage3-kprove-spec.log),
with their corresponding `stage3-kompile-*.log` files. Thus dynamic
reconstruction succeeds; legitimacy still depends on the static theory audit.

## 4. Adequacy and real-program pinning

The universal entry claim in `/candidate/spec.k:7-13` says:

- Precondition: `<functions>`, `<env>`, and `<stack>` are empty, and `<k>`
  contains `VerifyRunList(SOLUTION, XS)` for symbolic `XS:List`.
- Postcondition: execution reaches `ListVal(#rollingMax(XS))` with those three
  cells empty.

The other three claims instantiate empty, prompt, and all-negative inputs. Each
entry precondition is satisfiable; for example `XS = .List` is the normal
initial configuration and freshly reaches `ListVal(.List)`. For
`XS = [2,1]`, both Python implementations, fixed K execution, and the
mathematical helper produce `[2,2]`.

The proof does pin the submitted body syntactically. I parsed trusted
`solution.regenerated.mpy` and the claim's `SOLUTION` macro separately with
`kast --expand-macros --output kore`. The two KORE files are byte-identical,
both with SHA-256
`99eccb8c61e984cfd891d5bd96e821463cbf690248731d4685adee1067018355`.
See [stage4-term-identity.log](/audit-output/evidence/stage4-term-identity.log)
and the two preserved `.kore` terms.

An independent run of the candidate's body mutation changed the loop term
actually executed: omitting `first = False` prevented the `ROLLING-LOOP` macro
from matching and made `kprove` exit 1 at the wrong `[2,1]` result. See
[stage4-body-sensitivity.log](/audit-output/evidence/stage4-body-sensitivity.log).
This establishes syntactic body sensitivity, but not the semantic validity of
the rule that summarizes the matching body.

The return is genuinely constrained to `#rollingMax(XS)`, and that helper is
defined by exhaustive, descending equations on integer lists. It is not a free
variable or tautology. The adequacy failure is instead the missing connection
between real loop execution and that result.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[stage5_rule_inventory.md](/audit-output/evidence/stage5_rule_inventory.md);
the source scan is
[stage5-static-scan.log](/audit-output/evidence/stage5-static-scan.log).
It enumerates every local syntax production, all 37 rules in `semantic.k`, all
nine macros/helper equations in `solution-ast.k`, both rules in
`verification.k`, every claim, the sole `total` declaration, both other
functions, and the sole priority rule. There are no local `functional`, opaque,
or simplification declarations.

### Generated language semantics

For the submitted term, `semantic.k` models all material constructs:
typing-only import, function binding and one-argument call, literals and local
state, ordered assignment/evaluation, integer `>`, boolean branches, integer
list append, finite list iteration, final return, frame restoration, and
cleanup. K integers are arbitrary precision, matching Python's relevant integer
model. Fresh concrete and bridge-free ground proofs exercise all branch
behaviors.

The definition is intentionally incomplete outside the submitted subset:
runtime imports, nested user calls, non-integer appends/iterations, and abrupt
return before later statements are unsupported or get visibly stuck. Those
forms are not used by `solution.mpy`, so generated-semantics minimality does not
materially narrow the source contract.

`#rollingMax` and `#scanMax` are truthful mathematical definitions on intended
integer lists. Their two scan guards, `I >Int M` and its boolean negation, are
disjoint and complete; recursion descends on the tail. These equations specify
the desired answer, but do not prove that the submitted loop computes it.

### Fatal operational bridge

`/candidate/verification.k:17-28` adds a priority-40 operational bridge:

```text
For(Name("number"), Name("numbers"), ROLLING-LOOP)
  => .K
```

At the exact initial local environment, it skips every iteration, binding,
comparison, branch, append, and loop exit, and directly writes
`result = #rollingMax(XS)`. This is an operational bridge, not a derived loop
invariant. No bridge-free universal connection claim exists. The three
bridge-free claims in `operational-spec.k` cover only three fixed inputs. The
universal claim imports the bridge and therefore cannot justify it. The same
`#rollingMax` term in the bridge and postcondition is circular as an
execution-to-specification connection.

The bridge also has a demonstrably false complete match domain. Its `<k>` cell
uses `...`, so it admits arbitrary continuations, while its environment rewrite
deletes `first` and `maximum` and omits the final `number` binding that fixed
execution creates. The fresh witness starts from its exact accepted loop-entry
environment for `XS = [2,1]`, then immediately observes `maximum`:

```text
For(..., ROLLING-LOOP) ~> Name("maximum")
```

With fixed `semantic.k`, this terminates at `IntVal(2)` with
`result=[2,2]`, `first=false`, `maximum=2`, and `number=1`. With the candidate
bridge, execution is stuck at `Name("maximum")`; only `numbers` and
`result=[2,2]` remain. Both definitions built and both runs exited normally, so
this is not a parser/backend artifact. The witness sources and outputs are:

- [stage5-context-operational.k](/audit-output/evidence/stage5-context-operational.k)
  and [stage5-context-operational-run.log](/audit-output/evidence/stage5-context-operational-run.log)
- [stage5-context-bridged.k](/audit-output/evidence/stage5-context-bridged.k)
  and [stage5-context-bridged-run.log](/audit-output/evidence/stage5-context-bridged-run.log)

This supplies a concrete false conclusion witness for the rule's claimed
execution replacement. Narrowing it to the submitted continuation would remove
that particular state/control counterexample, but the candidate still provides
no machine-checked universal theorem connecting the exact loop to
`#rollingMax`. An informal invariant comment and finite tests cannot discharge
that obligation.

## 6. Fresh non-vacuity test

I created a new mutation over a satisfiable actual-program input. For `[2,1]`,
the correct result is `[2,2]`; the mutation changes only the postcondition to
demand `[2,1]`:
[stage6-false-spec.k](/audit-output/evidence/stage6-false-spec.k).

The exact proof command was:

```text
kprove /audit-output/evidence/stage6-false-spec.k \
  -I /tmp/audit-work/candidate \
  --definition fresh-verification-kompiled \
  --spec-module REVIEW-FALSE-SPEC --output pretty
```

It parsed/built successfully, reached `ListVal([2,2])`, emitted
`WarnStuckClaimState` because that term did not unify with the false
destination, and exited 1. See
[stage6-false-proof.log](/audit-output/evidence/stage6-false-proof.log).
The proof is therefore result-discriminating and non-vacuous. This passes Stage
6 but cannot validate the operational bridge used to obtain the result.

## 7. Proven versus assumed accounting

What the successful universal `#Top` establishes is precise but conditional on
the extended theory: under `VERIFICATION`, starting from the empty initial
cells, `VerifyRunList(SOLUTION, XS)` reaches
`ListVal(#rollingMax(XS))`. The short derivation works because the priority rule
postulates exactly that loop result. It does **not** establish, under the
bridge-free generated semantics, that arbitrary real loop execution computes
`#rollingMax`.

| Boundary | Role | Assessment |
|---|---|---|
| Trusted prompt, canonical function, and translator | Source contract, differential oracle, Python-to-MPY constructor generation | Acceptable trusted inputs; translator output was byte-checked. |
| K `INT`, `BOOL`, `STRING`, `LIST`, `MAP` domains and `>Int`/`notBool` | Low-level values, collections, and arithmetic | Acceptable standard primitive boundary; none encodes rolling maximum. |
| K parser, kompiler, LLVM/Haskell backends, `kprove` | Toolchain | Standard trusted checker boundary, version recorded. |
| `semantic.k` used subset | Generated operational model | Statically audited and concretely supported for every construct/context used by the submitted program; unsupported unused forms are excluded. |
| `SOLUTION` macros | Claim-to-program identity | Mechanically established by equal expanded KORE terms. |
| `#rollingMax`/`#scanMax` equations | Mathematical desired result | Truthful on intended integer lists; not an execution theorem. |
| Python/K differential executions and three bridge-free K claims | Finite implementation/semantics evidence | Useful finite bridge evidence only; not universal. |
| Priority-40 loop summary V02 | Program-derived result-bearing operational bridge | Illegitimate. It has no bridge-free universal connection theorem and has a concrete state/control counterexample over its admitted domain. All universal correctness claims depend on it. |
| Termination | Outside partial-correctness reachability result | Not proved. The benchmark asks for partial correctness, so this exclusion is not itself a defect. |

Gate A (real-program soundness) fails. Gate B would cover the full intended
finite integer-list domain if the execution connection were valid: there is no
fixed-size bound or material domain narrowing. Gate C evidence is reproducible
and the fresh false postcondition is rejected, but later gates cannot repair
Gate A. Under the benchmark decision boundary, a reconstructed `#Top` that
relies on this materially unsound/unjustified answer-bearing operational bridge
is not a legitimate proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
