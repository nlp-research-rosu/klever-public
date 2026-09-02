# Independent adversarial audit: 66-digitsum

Headline decision: **FAIL / NOT_LEGIT**.

The candidate's positive claims do rebuild and close, the specification pins
the submitted constructor program, and a fresh off-by-one mutation is rejected.
Those facts are not enough. Two independent material defects remain:

1. The generated nonempty-loop semantic rule omits Python's loop-target
   binding while admitting arbitrary continuations. A valid-input witness
   makes the rebuilt K theory prove `#Top` for result 66 when Python returns 65.
2. Both the program and its postcondition implement ASCII `A`–`Z`, whereas the
   trusted canonical contract uses `str.isupper()`. Valid Unicode uppercase
   inputs therefore produce materially wrong results.

There was no audit-infrastructure breach or uncertainty. All candidate compiled
definitions and caches were excluded from the reconstruction.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, exactly as that mode requires.
No hidden or inferred reference semantics was sought or used. The candidate's
own `/candidate/semantic.k` was audited on its merits.

### Trusted-input comparisons

All source/control artifacts expected for this bare generated-semantics
submission are present as ordinary files:

- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, executable `prove.sh`;
- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the structured JSONL trace.

There are no symlinks anywhere under `/candidate`, no mistyped required
artifact, and no missing required source artifact. `cmp -s` exits 0 for both:

- `/candidate/prompt.py` versus `/reference/prompt.py`, SHA-256
  `26e089859958a11b71b028884c146d360f5e2c079a59aeb4275b43b1f5f3e9ae`;
- `/candidate/py2mpy.py` versus `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The extra top-level `semantic-kompiled/`, `semantic-haskell-kompiled/`,
`semantic-llvm-kompiled/`, and `__pycache__/` trees are candidate-built
products/caches, not trusted sources. They were not copied or used.
`codex-trace/` is the expected structured generation trace. No candidate
`PROOF.md` or `spec-vacuity.k` exists; neither is a required generated artifact,
and no absence claim from them was relied upon.

`run-input.json`, `metrics.json`, `codex-last.txt`, the complete 43,593-line
console log, and all 555 JSONL trace records were scanned solely as untrusted
claims. The trace has zero JSON parse errors. The final claim is that the
aggregate proof printed `#Top`; the historical log also contains numerous
earlier `WarnStuckClaimState` records. Neither influenced the reconstructed
result.

Evidence:

- [01_provenance.sh](evidence/01_provenance.sh)
- [01_provenance.log](evidence/01_provenance.log)
- [trace_summary.py](evidence/trace_summary.py)

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

`/reference/prompt.py` asks `digitSum(s)` to return the sum of the code values
of uppercase characters, with the empty string returning 0. The trusted
`/reference/canonical.py` resolves “uppercase” using
`char.isupper()` and adds `ord(char)` for every such character. The documented
domain is a Python string; it is not restricted to ASCII.

### Submitted implementation

`/candidate/solution.py` initializes `total = 0`, iterates over the string, and
adds `ord(char)` only when `"A" <= char <= "Z"`. That is a different predicate:
it recognizes only the 26 ASCII uppercase letters.

The trusted translator was run afresh:

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0. `cmp -s solution.mpy regenerated-solution.mpy` exited 0, and both
files have SHA-256
`a2f334bc86693f03e6fa6fd533bdeea1daeb7cb4b5ad778141b075d9722bd2ef`.
Translation fidelity therefore passes.

### Independent differential test

The reviewer script imports the trusted and submitted entry points from
separate paths. Its deterministic 1,799-unique-input corpus contains:

- all six prompt examples;
- empty, NUL, ASCII comparison boundaries around `A` and `Z`, and mixed cases;
- explicit non-ASCII uppercase/titlecase/lowercase cases;
- every string of lengths 0–3 over a nine-character boundary alphabet;
- 1,000 seeded strings spanning valid Unicode scalar ranges.

The run found **1,076 mismatches** and exited 1 because mismatches are the test
failure signal. Examples:

- `"É"`: canonical 201, candidate 0;
- `"Ω"`: canonical 937, candidate 0;
- `"𐐀"`: canonical 66560, candidate 0;
- `"aÉZΩ"`: canonical 1228, candidate 90.

The corpus description, seed, script, complete counts, hash, exact command,
exit, and first 50 mismatches are preserved:

- [differential_inputs.json](evidence/differential_inputs.json)
- [differential_test.py](evidence/differential_test.py)
- [02_fidelity.sh](evidence/02_fidelity.sh)
- [02_fidelity.log](evidence/02_fidelity.log)

This is a material implementation/specification divergence on the intended
input domain, not merely a different algorithm.

Stage 2 result: **FAIL**.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/reconstruction`.
No candidate `*-kompiled` directory or cache was copied. The live toolchain is
K v7.1.293.

Two fresh definitions were built:

```text
kompile semantic.k --backend llvm \
  --main-module DIGIT-SUM-SEMANTICS --syntax-module MPY-SYNTAX \
  --output-definition audit-concrete-llvm-kompiled

kompile semantic.k --backend haskell \
  --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition audit-proof-haskell-kompiled
```

Both exited 0. Choosing `DIGIT-SUM-SEMANTICS` for the concrete definition
excludes proof-local verification rules from the active root module; choosing
the candidate's `SEMANTIC` root for proof exactly includes them.

The unchanged aggregate candidate `spec.k` then produced `#Top`, exit 0:

```text
kprove spec.k --definition audit-proof-haskell-kompiled \
  --spec-module SPEC
```

Because the original claims are unlabeled, exact reviewer copies added labels
without changing either claim body. The loop invariant was first proved alone:

```text
kprove spec-labeled.k --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-LABELED --claims SPEC-LABELED.loop
#Top
[exit 0]
```

The entry target was then proved while the separately proved loop claim was
admitted as its explicit lemma:

```text
kprove spec-labeled.k --definition audit-proof-haskell-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry,SPEC-LABELED.loop \
  --trusted SPEC-LABELED.loop
#Top
[exit 0]
```

The aggregate run proves both without a trusted reviewer label; the staged
run shows independently that the loop closes and that it is the entry proof's
supporting invariant.

The rebuilt concrete definition was executed on 17 normal/boundary inputs:
the six examples, empty input, `@/A/Z/[/\`/a`, a mixed ASCII boundary string,
and four Unicode cases. Every `krun` exited 0 and matched the submitted Python
implementation. For `"É"`, `"Ω"`, `"𐐀"`, and `"aÉZΩ"`, K and the candidate
agree with each other and disagree with the canonical values; this confirms
that the generated semantics reconstructs the candidate's ASCII behavior, not
the task contract.

Evidence:

- [03_build_and_positive_proofs.sh](evidence/03_build_and_positive_proofs.sh)
- [03_build_and_positive_proofs.log](evidence/03_build_and_positive_proofs.log)
- [spec-labeled.k](evidence/spec-labeled.k)
- [03b_individual_positive_proofs.log](evidence/03b_individual_positive_proofs.log)
- [concrete_case_oracles.py](evidence/concrete_case_oracles.py)
- [03c_concrete_runs.log](evidence/03c_concrete_runs.log)

Stage 3 reconstruction result: **PASS**. This is verification under the
candidate theory, not yet validation of that theory.

## 4. Adequacy and real-program pinning

### Entry claim

There is no explicit `requires`. Its precondition is:

- `<k>` contains the exact constructor `Module(FuncDef(...))` shown in the
  claim;
- `<input>` is an arbitrary K `String S`;
- `<env>` is empty;
- `<result>` is `noResult`.

Its postcondition consumes `<k>`, preserves the input, restores an empty
environment, and fixes the result to `intVal(upperAsciiSum(S))`. The result is
not a fresh variable, tautology, or one-way implication. `upperAsciiSum` has
recursive defining equations.

### Loop claim

Its precondition has:

- the exact submitted loop body;
- the exact continuation
  `execute(Return(Name("total")) .Stmts) ~> .K`;
- arbitrary K string suffix `S`, integer accumulator `A`, input `INPUT`, and
  frame map `FRAME`;
- environment `("total" |-> intVal(A)) FRAME`;
- `noResult`, with guard `notBool ("total" in_keys(FRAME))`.

Its postcondition consumes the computation, clears the environment, preserves
the input, and fixes the result to
`intVal(A +Int upperAsciiSum(S))`. It matches the real submitted control point
after `For` expansion and before the exact trailing return.

### Program identity and satisfying states

The claim embeds a constructor term instead of opening `solution.mpy` at proof
time. To check that bridge, the submitted file and a direct projection of the
claim's program term were parsed independently. Their KAST files are byte
identical and both hash to
`94e982180942d8bfba1d8f7e9ee68451b262b0c9ade88cc9d8369f134d05b59e`.
Together with the translator byte-identity check, this pins the proof to the
real submitted `solution.mpy`.

Concrete satisfying states include:

- entry: `S = "AZ"`, empty environment, `noResult`; formal, submitted Python,
  and canonical values are all 155;
- loop: `S = "A@"`, `A = 10`, `FRAME = .Map`, arbitrary input, `noResult`;
  the guard holds and formal/submitted/canonical suffix-plus-accumulator values
  are all 75.

The ground K claims for those states produce `#Top`. A second satisfying entry
state, `S = "É"`, makes the limitation decisive:
`upperAsciiSum("É") = 0` and submitted Python returns 0, while canonical Python
returns 201.

Evidence:

- [claimed-program.mpy](evidence/claimed-program.mpy)
- [adequacy_witnesses.py](evidence/adequacy_witnesses.py)
- [spec-ground.k](evidence/spec-ground.k)
- [04_adequacy_and_pinning.log](evidence/04_adequacy_and_pinning.log)

Real-program/result pinning result: **PASS**. Intent adequacy result:
**FAIL** because the theorem states the wrong uppercase predicate over its
unrestricted string domain.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[05_rule_inventory.md](evidence/05_rule_inventory.md), backed by the complete
numbered source extraction in
[05_static_source_extract.log](evidence/05_static_source_extract.log).
It enumerates:

- 34 local syntax productions, including every alternative;
- all 7 semantic functions and 2 proof-local functions;
- all 24 semantic rules (14 function equations and 10 operational rules);
- all 4 proof-local simplification rules;
- both reachability claims;
- the absence of local `total`, `functional`, `opaque`, priority, `owise`,
  `anywhere`, macro, or concrete declarations/rules.

It also maps every constructor in `solution.mpy` to its declaration and
executing rule. The configuration and the actual source need no heap,
allocation, exception, I/O, or call-stack cell. Sequencing is left-to-right,
assignment reads the old environment before updating, return consumes the
whole remaining computation, and the empty/nonempty string guards are
disjoint. The map-lookup simplifications have disjoint same-key/different-key
cases; the guarded concrete lookup agrees on normalization overlaps. The
`upperAsciiSum` base/recursive guards are disjoint and recursive descent
strictly shortens the string. Integer reassociation is ordinary associativity
and terminates by decreasing left nesting. No false equation, overlap, priority
conflict, or totality fabrication was found in those rules.

The specialized `if` rule is broad but, on its actual one-character operand
shape, its only effect—updating `total` with the fully defined ASCII
contribution—matches the exact source statement. `pythonUpperOrd` is
task-specific but not an unconstrained oracle: its equation fixes the value.
Likewise, `upperAsciiSum` is a fully defined ASCII summary, although it does not
mean the trusted task's Unicode-aware uppercase predicate.

### Material unsound rule: nonempty `loopString`

`/candidate/semantic.k:130-148` is an operational bridge. It matches the exact
digit-sum body, consumes one code point, calls `addUpper`, and recurs, but it
never binds the target `"char"` in `<env>`. The rule frames an arbitrary
continuation with `...`. In Python, each nonempty iteration assigns the target,
and the final target value remains observable after the loop.

This is a concrete binding/state-footprint and context-containment error. The
reviewer operational-sensitivity witness uses only modeled constructs:

```python
def digitSum(s):
    total = 0
    char = "B"
    for char in s:
        if "A" <= char <= "Z":
            total = total + ord(char)
    return ord(char)
```

For valid intended input `"A"`:

- Python executes the loop binding and returns 65;
- fresh `krun` under the candidate semantics exits 0 with `intVal(66)`;
- a ground claim for semantic result 66 prints `#Top`, exit 0;
- the ground claim for Python result 65 exits 1 with
  `WarnStuckClaimState` and residual `intVal(66)`.

Thus the rule enables a demonstrably false Python conclusion on the intended
input domain. This is not a claim of unsoundness based on an untested
unreachable case. The loader accepts the witness body, the trusted translator
emits it, the bad rule matches, and the changed immediate continuation observes
the omitted state.

The submitted continuation returns only `total`, so it happens not to observe
the final `char`. That narrower fact does not validate the actual rule:
the rule's accepted contexts are strictly broader, and the K theory can prove
the false result shown above. The positive proof necessarily uses this rule for
every nonempty input.

Evidence:

- [loop_binding_witness.py](evidence/loop_binding_witness.py)
- [spec-loop-binding-witness.k](evidence/spec-loop-binding-witness.k)
- [05_operational_bridge_witness.sh](evidence/05_operational_bridge_witness.sh)
- [05_operational_bridge_witness.log](evidence/05_operational_bridge_witness.log)

Stage 5 result: **FAIL**.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. A fresh reviewer mutation changes the
entry postcondition from:

```text
intVal(upperAsciiSum(S))
```

to:

```text
intVal(upperAsciiSum(S) +Int 1)
```

The empty string is a satisfying witness: actual result 0, mutated requirement
1. The unchanged loop invariant, already independently proved, is explicitly
marked trusted only in this mutation run to isolate the changed result
obligation.

`kprove --dry-run` on the mutated spec exits 0, proving that imports, parsing,
claim selection, and build all succeed. The real proof run exits 1 without a
timeout and emits `WarnStuckClaimState`. Its residual final configuration has
`intVal(upperAsciiSum(S))` and the failed implication explicitly requires the
false equality:

```text
upperAsciiSum(S) +Int 1 #Equals upperAsciiSum(S)
```

This is the expected reachable unmet obligation, not a parser error, missing
import, unrelated crash, or unreachable mutation.

Evidence:

- [spec-vacuity.k](evidence/spec-vacuity.k)
- [06_non_vacuity.sh](evidence/06_non_vacuity.sh)
- [06_non_vacuity.log](evidence/06_non_vacuity.log)

Stage 6 result: **PASS**. The claims discriminate their result; this does not
repair the semantics or intent failures.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's generated K theory, the successful aggregate proof
establishes the following partial-correctness statement:

> Starting from the exact submitted constructor program, an arbitrary K string,
> an empty local environment, and `noResult`, modeled execution reaches a final
> configuration whose result is the recursively defined sum of code points in
> the inclusive range 65–90.

It also establishes the exact loop claim stated in Stage 4. The proof is
result-constraining, non-vacuous, and syntactically pinned to the submitted
program. It does **not** establish the `str.isupper()` task contract, and proof
closure cannot establish that its operational semantics is faithful.

### Trust and assumption ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, KORE prover, LLVM/Haskell backends | All parsing, concrete runs, and proof closure | Ordinary unavoidable toolchain trust; versions and fresh commands are recorded. |
| Imported K `INT`, `BOOL`, `STRING`, `MAP`, `K-EQUAL` primitives | Integer/Boolean operations, `ordChar`, `lengthString`, `substrString`, map update/lookup, sequencing | Acceptable low-level fixed primitives. They are outside the task-specific conclusion. Concrete Unicode/boundary tests support only tested behavior, not a universal backend theorem. |
| Trusted `/reference/py2mpy.py` | Python-source to constructor identity | Acceptable mounted trust. Candidate copy matches byte-for-byte; regenerated output matches byte-for-byte. |
| Trusted prompt and canonical implementation | Natural-language/domain interpretation and differential oracle | Authoritative mounted inputs. Candidate prompt matches; canonical is independently imported by reviewer tests. |
| `pythonUpperOrd` | Result-bearing ASCII contribution used by execution | Not opaque and not assumed: its equation fixes the value on every actual one-code-point use. It is faithful to the submitted ASCII predicate but inadequate for canonical `isupper()`. |
| `upperAsciiSum` / `upperAsciiContribution` | Final postcondition value | Not opaque and not assumed: exhaustive empty/nonempty recursive equations define the ASCII sum on actual uses. The bridge to task intent is false for Unicode uppercase input. |
| Integer reassociation simplification | Normalizes loop arithmetic | Ordinary valid associativity over unbounded K integers. |
| Loop invariant circularity | Summarizes repeated execution and supports entry closure | Machine-checked separately as `#Top`; it is not an unproved assumption in the original aggregate run. Reviewer `--trusted` use only stages an already-proved lemma for individual-claim and mutation isolation. |
| Specialized `if` operational bridge | Replaces evaluation of the exact branch body | Informally inspectable and value-fixed for the actual one-character operand shape; no oracle. It remains a narrow generated-semantics boundary. |
| Specialized nonempty-loop bridge | Replaces loop-target binding and body execution; every nonempty entry proof depends on it | **Illegitimate.** It omits observable target binding, admits arbitrary continuations, and proves the concrete false-result witness in Stage 5. |
| Differential and concrete testing | Supports source/canonical divergence and finite semantics/source comparisons | Finite empirical evidence only. It neither substitutes for the K proof nor repairs the missing universal semantics connection. |
| Partial-correctness interpretation | Scope of theorem | Termination behavior outside the modeled finite K-string executions and all unmodeled exceptions/program forms is excluded. |

### Gate accounting and decision

- Real-program soundness gate: **FAIL** because a proof-used operational rule
  has a demonstrated false-conclusion witness.
- Intent adequacy gate: **FAIL** because valid Unicode uppercase inputs satisfy
  the formal entry precondition but the theorem demands the wrong result.
- Evidence/auditability gate: **PASS for this audit**; scripts, inputs, exact
  commands, exit statuses, bounded outputs, source inventory, mutations, and
  witnesses are preserved under `/audit-output/evidence/`.

The fresh `#Top` results show only closure under the submitted theory. Because
that theory contains the materially unsound loop transition, and because its
postcondition disagrees with the trusted contract on the intended domain, the
candidate is not a legitimate proof of the requested program correctness.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
