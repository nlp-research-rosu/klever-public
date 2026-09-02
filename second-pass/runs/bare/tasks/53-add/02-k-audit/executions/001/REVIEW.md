# Independent adversarial audit: 53-add

## Executive decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated program for arbitrary integer inputs. I
rebuilt the generated semantics and proof definition solely from copied source,
ran the only positive claim independently, audited every candidate-authored K
rule, checked exact program pinning, and rejected a fresh off-by-one
postcondition mutation for the expected semantic reason.

The candidate's own compiled definition, caches, prose, logs, trace, and prior
`#Top` outputs were not used as proof authority.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` does not exist, as required. I did not search
for or infer any hidden reference semantics. There is no infrastructure breach.

Evidence: `evidence/01-integrity.log`.

### Required artifacts and types

All required candidate artifacts are present as regular, non-symlink files:

- `run-input.json`, `metrics.json`, `codex-last.txt`, and
  `codex-output.log`;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

One structured trace is present at
`/candidate/codex-trace/2026/07/22/rollout-2026-07-22T05-08-16-019f894c-22de-71e0-ad3a-08dd200c2e23.jsonl`.
There are no candidate helper K source files beyond the three K files listed
above. No required artifact is missing, changed, extra within a
mode-constrained semantics tree, mistyped, or symlinked.

The candidate also contains `__pycache__/` and `verification-kompiled/`.
These are generated caches/build output, not source artifacts. They were
explicitly excluded and never copied into or used by the reconstruction.

The candidate's `prompt.py` is byte-identical to `/reference/prompt.py`:

`37ae93665c1512f10b22de3b438a4310a63dabf773891ef3120880a8f2dc7217`

The candidate's `py2mpy.py` is byte-identical to
`/reference/py2mpy.py`:

`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

Those hashes also match the claims in `run-input.json`.

### Untrusted generation record

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and all readable records in the structured JSONL trace
only as untrusted claims. They claim a non-timeout exit 0 run and a final
`KPROVE_PASSED`; the long output also contains earlier compiler errors followed
by later `#Top` claims. The trace has 180 records, including readable messages,
35 tool calls and outputs, nine patch events, and one completion record.
Encrypted reasoning payloads are opaque and confer no evidentiary value.
None of these claims substitutes for the fresh results below.

Evidence: `evidence/01-untrusted-generation-summary.log` and reviewer script
`evidence/summarize_untrusted_generation.py`.

### Isolation

Only source artifacts needed for execution were copied to
`/tmp/audit-work/53-add`. The trusted translator, prompt, and canonical
implementation were copied from `/reference`, not from candidate claims. The
scratch hashes are recorded in
`evidence/03-scratch-source-manifest.log`.

Stage 1 result: pass.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt declares:

`add(x: int, y: int)` returns the addition of the two integer inputs.

The examples require `add(2, 3) == 5` and `add(5, 7) == 12`. The trusted
canonical implementation is exactly `return x + y`. The intended domain is
pairs of Python integers; Python integers and K `Int` values are unbounded
mathematical integers for the operation used here.

### Source inspection

The candidate implementation is:

```python
def add(x: int, y: int):
    return x + y
```

It preserves the requested entry-point signature and is materially identical
to the canonical body. It has no branches, loops, state effects, helper calls,
or exceptional path on the stated integer domain.

### Trusted regeneration

Running the trusted translator in scratch produced
`reviewer-regenerated-solution.mpy`. `cmp` returned 0 against the submitted
`solution.mpy`; both have SHA-256:

`67c61c16675c9cff80240867fcd0afd5bbbc0cdcd75147d9acb520ce116c98ee`

Exact command and status: `evidence/02-translation-identity.log`.
Reviewer driver: `evidence/regenerate_and_compare.sh`.

### Independent differential test

`evidence/differential_test.py` separately imports the scratch copy of the
trusted canonical entry point and the scratch copy of the generated entry
point. It records every input in
`evidence/differential-inputs.json`.

The test covered:

- both documented examples;
- eight additive-zero and sign-boundary cases;
- five magnitude boundaries, including the signed 64-bit transition and
  100-digit integers;
- 256 seeded integer pairs in `[-10^12, 10^12]`;
- 64 seeded signed 512-bit integer pairs.

There is no empty collection case for scalar integer parameters; `(0, 0)` and
the one-sided zero cases cover the relevant additive boundary. There are no
branch boundaries because both implementations are branch-free.

The command exited 0 after 335 cases with `MISMATCH_COUNT: 0`. This is finite
fidelity evidence, not a substitute for the K proof.

Evidence: `evidence/02-differential.log`,
`evidence/differential-inputs.json`, and
`evidence/differential_test.py`.

Stage 2 result: pass.

## 3. Clean proof reconstruction

### Toolchain and clean builds

The independent toolchain was K version `v7.1.293`. The scratch directory
initially contained no kompiled definitions. I built two new, distinctly named
definitions:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-concrete-kompiled
```

Exit status: 0. Evidence: `evidence/03-build-concrete.log`.

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition reviewer-proof-kompiled
```

Exit status: 0. Evidence: `evidence/03-build-proof.log`.

Tool paths and versions are in `evidence/03-tool-versions.log`. These commands
used only source files copied to `/tmp/audit-work/53-add`; the candidate's
`verification-kompiled/` was not used.

### Generated-semantics concrete execution

The fresh LLVM definition executed the submitted `solution.mpy` on seven
recorded cases: both prompt examples, zero, a negative case, signed
cancellation, a value crossing `2^63`, and a 100-digit cancellation case.
Every `krun` exited 0 with `.K`, and every K result equaled both the trusted
canonical Python result and generated Python result:

| Inputs | K | Canonical Python | Generated Python |
|---|---:|---:|---:|
| `(2, 3)` | 5 | 5 | 5 |
| `(5, 7)` | 12 | 12 | 12 |
| `(0, 0)` | 0 | 0 | 0 |
| `(-8, 3)` | -5 | -5 | -5 |
| `(-1, 1)` | 0 | 0 | 0 |
| `(2^63-1, 1)` | `2^63` | `2^63` | `2^63` |
| `(10^100, -10^100+7)` | 7 | 7 | 7 |

Evidence: `evidence/03-concrete-execution.log`,
`evidence/concrete-semantics-inputs.json`, and
`evidence/concrete_semantics_compare.py`.

### Positive target claims

Static enumeration found exactly one positive claim in `spec.k`; there are no
auxiliary or loop claims. Evidence: `evidence/03-claim-inventory.log`.

The independently run target command was:

```text
kprove spec.k --definition reviewer-proof-kompiled --spec-module SPEC
```

It printed exactly `#Top` and exited 0. Evidence:
`evidence/03-positive-proof.log`.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no `requires` clause. Its sorts therefore give the formal input
domain: arbitrary `X:Int` and `Y:Int`.

Its complete starting condition is:

- `<k>` contains `load` of a module defining `add(x,y)` with the body
  `return x + y`, immediately followed by invocation of that `add` with
  `pyInt(X)` and `pyInt(Y)`;
- `<env>` is the empty map;
- `<functions>` is the empty map;
- `<result>` is zero.

Its destination requires:

- `<k>` is consumed to `.K`;
- `<env>` contains exactly `"x" |-> pyInt(X)` and
  `"y" |-> pyInt(Y)`;
- `<functions>` contains the exact loaded `add` body;
- `<result>` is exactly `X +Int Y`.

Thus the returned/result value is neither free nor existential, and the claim
is not an implication with an unconstrained converse. The result expression
uses only variables fixed on the left-hand side.

### Exact submitted-program identity

After whitespace normalization, the submitted program is:

```text
Module(FuncDef("add",Params("x","y"),
Return(BinOp("+",Name("x"),Name("y")))))
```

That complete term occurs under `load(...)` in the claim, followed by the real
entry invocation. The pinning check passed. Because the spec embeds a K term
rather than reading a filename at proof time, the trusted-regeneration byte
identity from Stage 2 is the necessary source-to-term bridge; it passed.

`verification.k` contains only an import of `SEMANTIC`. It has no rule,
function, lemma, summary, or substitute program. There are no helper or loop
claims to reconcile with control flow.

### Satisfiability and concrete substitution

A satisfying state is `X=2`, `Y=3`, the exact submitted loaded program,
empty environment and function maps, and result cell zero. Substituting this
witness into the destination demands result `2 +Int 3 = 5`. The trusted
canonical Python implementation, generated Python implementation, and concrete
K execution all return 5.

Evidence: `evidence/04-claim-pinning-witness.log` and
`evidence/claim_pinning_witness.py`.

Stage 4 result: pass.

## 5. Rule-by-rule static soundness review

A stand-alone exhaustive inventory is preserved at
`evidence/05-rule-inventory.md`; source enumeration is in
`evidence/05-local-source-inventory.log`.

### Local syntax, attributes, and configuration

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmt)`;
- `Stmt`: `FuncDef(String, Params, Stmt)` and `Return(Expr)`;
- `Params`: exactly two string parameters;
- `Expr`: `Int(Int)`, `Name(String)`, and
  `BinOp(String, Expr, Expr)`.

`SEMANTIC` declares constructor-like `pyInt(Int)` and
`function(String,String,Stmt)`, plus the internal K items `load`, `invoke`,
`bind`, `eval`, `plusLeft`, `plusRight`, and `finishReturn`.

The configuration contains only state used by the target: computation,
environment, loaded-function map, and integer result. Its driver loads the
provided program and invokes `add` with two K integer configuration arguments.

There are no local `[function]`, `[total]`, `[functional]`,
`[simplification]`, priority, strictness, macro, or opaque-symbol declarations.
Consequently there are no local equation-coverage, totalization, function
overlap, or simplification consistency obligations.

### Exhaustive ordinary-rule inventory

1. `load(Module(S)) => S` exposes the submitted module's sole statement before
   the existing invocation continuation. This is faithful for the actual
   one-definition module.
2. `FuncDef` stores its exact two formal names and body in an initially empty
   function map without executing the body. The actual program has one
   non-closure function.
3. `invoke` resolves the named stored function, schedules binding of the first
   argument, then the second, then executes the stored body. It neither guesses
   nor summarizes the result.
4. `bind` updates the environment through the trusted K `Map` operation. The
   actual formals are distinct `"x"` and `"y"`, so both bindings remain.
5. `Return(E)` schedules evaluation of `E` followed by `finishReturn`; result
   commitment cannot precede expression evaluation.
6. `eval(Int(I)) => pyInt(I)` is the direct integer-literal rule. The submitted
   body does not use a literal, but the independent literal-body smoke test
   exercised it successfully.
7. `eval(Name(X))` obtains the exact mapped value. Both submitted names are
   bound before evaluation.
8. `eval(BinOp("+",LEFT,RIGHT))` schedules the left operand first. Other
   operator strings do not match.
9. The `plusLeft` rule waits for a left `pyInt`, then schedules the right
   operand while retaining the left integer.
10. The `plusRight` rule waits for the right `pyInt` and produces
    `pyInt(I +Int J)`. This uses trusted mathematical integer addition.
11. `finishReturn` consumes the computed `pyInt`, empties this computation,
    and writes the represented integer to `<result>`.

### Construct coverage and execution order

Every constructor in `solution.mpy` is covered:

- `Module` by syntax and rule 1;
- `FuncDef` and its two-name `Params` by syntax and rules 2–3;
- `Return` by rules 5 and 11;
- `BinOp("+",...)` by rules 8–10;
- both `Name` nodes by rule 7 after rules 3–4 establish bindings;
- string and integer primitives by trusted K builtin syntax.

The actual path is deterministic. Rule fronts do not overlap on it:
`eval(Int)`, `eval(Name)`, and `eval(BinOp("+"))` have disjoint constructors,
and the three `pyInt` continuation rules distinguish `plusLeft`,
`plusRight`, and `finishReturn`. No priorities are needed.

The state footprint is complete for this program. Loading changes only the
function map; invocation and binding change only the environment and
computation; expression rules carry values only in `<k>`; return completion
changes only `<result>` and `<k>`. There is no source allocation, heap, I/O,
exception, recursion, loop, output, or external state to omit.

### Shortcut, oracle, and sensitivity checks

No semantic rule encodes `X +Int Y` as the answer to the task-level program.
The program body is loaded, looked up, bound, and evaluated. The only
result-bearing primitive is the ordinary `+Int` interpretation of source
operator `"+"`; this is the expected low-level operation semantics, not an
unconstrained oracle.

A separate body-sensitivity program changed the body to `Return(Int(7))`.
Fresh concrete execution then returned 7 for inputs `(2,3)`, proving that
the semantics observes the stored body rather than a hard-coded addition
answer. Evidence: `evidence/literal-return.mpy` and
`evidence/05-body-sensitivity.log`.

A program using the syntactically admitted but unmodeled `"-"` operator
stopped visibly at `eval(BinOp("-",...))` with result still zero; no fabricated
value was produced. Evidence: `evidence/unmodeled-minus.mpy` and
`evidence/05-unmodeled-minus.log`.

### Scope limitation

This is deliberately not a reusable general Python semantics. It models a
single two-argument function, one initial call, integer values, and the exact
constructs needed here. It has no general local-call stack or general abrupt
return mechanism for arbitrary synthetic continuations. Those omitted contexts
are not produced by the submitted one-statement function under the configured
entry execution. The rendered generated-semantics boundary explicitly permits
minimal coverage when it soundly covers every used construct.

No inventoried rule enables a false result on the intended input domain:
for every pair of K integers, the reachable path has the exact two distinct
bindings, an empty post-call continuation, and builtin integer addition.
Accordingly there is no unsound-rule witness to report; the narrower
generalization limitation above does not affect this theorem.

Stage 5 result: pass.

## 6. Fresh non-vacuity test

The candidate supplied no mutation that needed to be trusted. I created the
fresh reviewer mutation `evidence/spec-vacuity.k`, copied it into scratch, and
changed only the result-bearing destination from:

```text
X +Int Y
```

to:

```text
(X +Int Y) +Int 1
```

This mutation is demonstrably false for the satisfying witness `X=2`, `Y=3`:
real execution and both Python implementations produce 5, while the mutation
demands 6.

First, the dry-run command:

```text
kprove spec-vacuity.k --definition reviewer-proof-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

parsed and built successfully with exit status 0. Evidence:
`evidence/06-vacuity-build.log`.

Then the actual mutated proof:

```text
kprove spec-vacuity.k --definition reviewer-proof-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`. Its residual shows the executed result cell
as `X +Int Y` and the failed destination implication as equality with
`X +Int Y +Int 1`. This is the expected unmet semantic obligation, not a parser
failure, missing import, timeout, or unrelated crash.

Evidence: `evidence/06-vacuity-proof.log`.

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the candidate-authored generated semantics and trusted K builtin theory,
for every `X:Int` and `Y:Int`, starting in the claim's exact initial
configuration with the exact submitted translated program, execution reaches
`.K`, retains the two argument bindings and loaded function recorded by the
claim, and stores exactly `X +Int Y` in `<result>`.

This is a partial-correctness result at the requested semantics level. It is
not a theorem about floats, strings, booleans as Python objects, overloaded
addition, subclasses, multiple functions, closures, exceptions, or arbitrary
Python programs.

### Trust and assumption ledger

| Boundary | Role and dependents | Evidence and judgment |
|---|---|---|
| Trusted `/reference/prompt.py` and `/reference/canonical.py` | Define natural-language intent and independent executable oracle. They affect the intent bridge, not K claim closure. | They are designated trusted inputs. The implementation is the same branch-free expression as the canonical. Acceptable. |
| Trusted `/reference/py2mpy.py` | Bridges `solution.py`'s CPython AST to the submitted constructor term. The real-program pinning conclusion depends on it. | Candidate copy is byte-identical; fresh translation is byte-identical to `solution.mpy`. This translator is trusted by the audit premise. Acceptable. |
| Candidate `semantic.k` | Gives operational meaning to the translated term and therefore directly determines claim closure. | Not assumed from candidate prose: rebuilt, concretely tested, exhaustively audited, body-sensitive, and complete on the used path. Its direct rules match Python integer lookup/evaluation/addition on this program. Acceptable generated-semantics boundary. |
| K `Int` and `+Int` | Interpret arbitrary signed integers and the source `"+"` operation. The final result depends on `+Int`. | Standard imported K mathematical-integer primitive. This is an ordinary low-level operation semantics, not the task answer or a fresh oracle. Acceptable trusted primitive. |
| K `Map` lookup/update | Implements parameter bindings and function lookup. The name-evaluation and final-state facts depend on it. | Standard imported K builtin; used in its normal finite-map role. Acceptable trusted primitive. |
| K cells, sequencing, parser, compiler, LLVM backend, and Haskell prover | Execute and prove the operational rules. Every machine-checked conclusion depends on toolchain correctness. | Normal unavoidable trusted computing base; fresh version and commands recorded. Acceptable. |
| Python-versus-generated-semantics correspondence | Connects the K theorem to CPython behavior for this restricted expression. | Rule-by-rule inspection gives the universal modeling argument for ordinary integers; 335 Python differential cases and seven K/Python cases are finite supporting evidence only. No proof conclusion is outsourced to those tests. Acceptable for this direct subset. |
| Termination outside the modeled entry path | Not established or claimed. | The report is expressly partial correctness and excludes unsupported programs. Acceptable. |

There are no candidate-authored opaque result symbols, total functions,
proof-local simplifications, derived lemmas, circular loop claims, operational
bridges, empirical oracles, or informal helper summaries. Nothing unproved is
used to substitute for execution of the program-defined body.

### Validation gates and final rationale

- Real-program soundness: pass. The exact body executes, state changes are
  accounted for, there is no bridge or oracle, the precondition is satisfiable,
  and the false result mutation is rejected.
- Intent adequacy: pass. The formal domain matches the `int` signature, the
  exact implementation and canonical both compute ordinary unbounded integer
  addition, and the postcondition fixes that sum.
- Trust and auditability: pass. Every build/proof/test command has a preserved
  exit status and bounded output; finite tests are used only as supporting
  bridge evidence.

The generated semantics is narrow, but that narrowness excludes unused
language features rather than weakening, bypassing, or falsifying the theorem
about this real submitted program. There is no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
