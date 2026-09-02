# Independent adversarial audit: 41-car-race-collision

The candidate contains a legitimate partial-correctness proof of the submitted
generated program. I rebuilt both execution and proof definitions from source,
ran the only positive claim independently, mechanically pinned its executed
constructor term to the trusted regeneration of `solution.py`, reviewed all
local declarations and rules, and rejected two independent false mutations.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `41-car-race-collision`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- no mounted reference semantics.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and every record required for the
declared legacy-selected layout: `invocation.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, the structured JSONL trace,
and the present `usage.json`. I also inspected the optional imported
`legacy-metrics.json` and `legacy-run-input.json`. The generation logs and trace
were treated only as untrusted historical claims.
Historical runtime metrics were not recorded for this legacy-selected run, are
not required by this layout, and were not reconstructed or treated as a defect.

The campaign object in `/audit-input.json` is exactly equal as parsed JSON to
`/audit-campaign-lock.json`, whose independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded lock hash. All required mounts and records are regular,
readable, non-symlinked files or real directories. No symlink occurs anywhere
under `/candidate`, `/generation-evidence`, or `/reference`.

Independent direct hashes match the launcher records for the campaign lock,
run and task manifests, stage-one result and invocation, trusted canonical,
prompt and translator, generation prompt, metrics, usage, final answer, output
log, and the sole trace JSONL file. In particular:

- the mounted candidate's standard `pipeline_contract.sha256_tree` is
  `466f421e4955133ed76d488ded0f8c1d10dc513c04b492d43d06ecbae7e4f934`,
  exactly the retained-workspace/output digest in `invocation.json` and
  `generation-result.json`; and
- the trace's standard digest is
  `f855927a2d4f7f1a3cf165ebc1d3867f6f405e6667cb8433005e606bb24a6a99`,
  exactly `usage.json`'s `source_trace_sha256`; its sole file also matches the
  recorded per-file digest.

The two audit-input fields named `candidate_tree_sha256` and
`generation_codex_trace_sha256` use a launcher-specific tree encoding not
identified in the record and therefore are not numerically comparable to
`pipeline_contract.sha256_tree`. The independently mounted bytes are
nevertheless bound by the matching direct and generation-standard hashes above;
there is no evidence of a changed mount.

The generated-semantics boundary is intact:
`/reference/reference-semantics` is absent, as required. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to `/reference/prompt.py` and
`/reference/py2mpy.py`. No required candidate proof artifact is missing.

Evidence: `evidence/stage1_integrity.sh` and
`evidence/stage1_integrity.log`.

**Stage result: PASS.** There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt describes two groups of `n` cars moving in opposite
directions on a line, continuing through collisions. Every car in one group
meets every car in the other group once, so the collision count is
`n * n`. Since `n` is a number of cars, the material natural-language input
domain is the non-negative integers. The prompt contains no literal test
examples. The empty boundary is `n = 0`; the smallest nonempty boundary is
`n = 1`; there are no implementation branches.

The trusted canonical function returns `n ** 2`. Candidate `solution.py`
returns `n * n`. These expressions agree for arbitrary Python integers and in
particular for the intended non-negative count domain.

### Trusted regeneration

From the scratch copy I ran:

```text
cd /tmp/audit-work/candidate &&
python3 /tmp/audit-work/trusted/py2mpy.py solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

The command exited 0. `cmp` exited 0, and both submitted and regenerated files
have SHA-256
`8878b8488943a7fc31808899d00a3cbf433c48b524f0f1515c79f92c10e6e659`.
Thus submitted `solution.mpy` is byte-identical to trusted regeneration.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and candidate entry point. It tested:

- fixed intended cases `0, 1, 2, 3, 10, 41, 100, 10^6, 10^20, 10^100`;
- 1,000 deterministic generated non-negative integers using seed `410041`;
  and
- 104 representative negative integers as an additional, out-of-contract
  observation.

The script exited 0 over 1,114 cases with `mismatch_count=0`. This is finite
fidelity evidence, not a replacement for the K theorem.

Evidence: `evidence/stage2_program_fidelity.sh`,
`evidence/stage2_program_fidelity.log`, and
`evidence/differential_test.py`.

**Stage result: PASS.**

## 3. Clean proof reconstruction

I copied source artifacts into `/tmp/audit-work/candidate` and did not copy or
reuse any candidate-compiled definition or cache. The submitted candidate mount
contained no compiled definition. I independently built:

```text
timeout 600s kompile semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition concrete-kompiled
```

This exited 0. Fresh LLVM executions of the exact submitted `solution.mpy`
produced:

| `N` | K result | canonical Python | candidate Python |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 3 | 9 | 9 | 9 |
| 10 | 100 | 100 | 100 |
| 41 | 1681 | 1681 | 1681 |
| -1 (observational) | 1 | 1 | 1 |

Every `krun` exited 0 with `.K` in `<k>`, and the comparison script reported
zero mismatches.

I then built the proof definition:

```text
timeout 600s kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition proof-kompiled
```

This exited 0. `spec.k` contains one and only one positive target claim. I ran:

```text
timeout 600s kprove spec.k \
  --definition proof-kompiled \
  --spec-module SPEC
```

It exited 0 and printed exactly `#Top`.

Evidence: `evidence/stage3_reconstruction.sh`,
`evidence/stage3_reconstruction.log`, and
`evidence/concrete_compare.py`.

**Stage result: PASS.**

## 4. Adequacy and real-program pinning

### Entry claim in plain language

Precondition:

- `N` is a K integer and `N >= 0`;
- `<k>` begins with the module constructor for a single function named
  `car_race_collision`, whose parameter is `n` and whose exact body is
  `return n * n`, followed by `run("car_race_collision", N)`;
- the functions and environment maps are empty; and
- the result cell initially contains `0`.

Postcondition:

- all computation has been consumed (`<k> .K </k>`);
- the function map contains exactly the submitted function binding and body;
- the environment maps `n` to `N`; and
- the result is exactly `N *Int N`.

The result is not free, existential, tautological, or guarded only by a one-way
implication. It is an exact cell rewrite to the intended expression.

### Program identity

`evidence/pinning_check.py` tokenizes K constructors, strings, integers, commas,
and parentheses. It compared the entire regenerated/submitted `solution.mpy`
term with the program prefix executed by the claim. Both sides contained the
same 30 tokens in the same order and
`constructor_terms_equal=True`. The subsequent `run` term is supplied by the
language configuration/harness and invokes the just-installed binding by the
same function name.

This is a constructor-level identity check, not an assumption that editing
`solution.py` would automatically update the immutable claim.

### Satisfiability, substitution, and body sensitivity

`N = 3` satisfies the precondition. Substitution gives result `3 * 3 = 9`;
fresh K execution, trusted canonical Python, and candidate Python all returned
`9`. The same agreement is recorded for other satisfying cases including the
empty boundary `N = 0`.

I also created `evidence/spec-body-mutation.k`, changing the term actually
executed by the claim to `return n * 0` while retaining the original `n * n`
result obligation and changing the recorded function body consistently. This
is not a source-file-only mutation. `kprove` parsed and executed the changed
constructor term, then exited 1 with `WarnStuckClaimState` and the expected
failed implication:

```text
N *Int 0 #Equals N *Int N
```

`N = 1` is a concrete satisfying counterexample. This demonstrates that the
positive theorem is sensitive to the submitted body.

Evidence: `evidence/stage4_pinning.log`,
`evidence/spec-body-mutation.k`, and
`evidence/stage4_body_mutation.log`.

**Stage result: PASS.**

## 5. Rule-by-rule static soundness review

### Exhaustive local declaration inventory

`semantic.k` imports trusted K `INT`/`INT-SYNTAX`, `STRING-SYNTAX`, and `MAP`.
Its complete local syntax inventory is:

| ID | Declaration | Role |
|---|---|---|
| D1 | `Pgm ::= Module(Stmt)` | module wrapper |
| D2 | `Stmt ::= FuncDef(String, Params, Stmt)` | one-parameter function definition |
| D3 | `Stmt ::= Return(Expr)` | returned expression |
| D4 | `Params ::= Params(String)` | one parameter |
| D5 | `Expr ::= Int(Int)` | integer literal |
| D6 | `Expr ::= Name(String)` | variable reference |
| D7 | `Expr ::= BinOp(String, Expr, Expr)` | binary-operation constructor |
| D8 | `KItem ::= run(String, Int)` | entry invocation |
| D9 | `KItem ::= definition(String, Stmt)` | stored parameter/body |
| D10 | `KItem ::= execute(Stmt)` | statement execution |
| D11 | `KItem ::= evaluate(Expr)` | expression evaluation |
| D12 | `KItem ::= multiplyRight(Expr)` | saved right operand |
| D13 | `KItem ::= multiplyBy(Int)` | saved evaluated left integer |
| D14 | `KItem ::= finishReturn` | result-delivery continuation |

All are ordinary syntax marked only with `[symbol(...)]`. There are no local
`function`, `total`, `functional`, `opaque`, `simplification`, `concrete`,
priority, or `owise` declarations or rules. `verification.k` adds no syntax,
rule, function, axiom, lemma, abstraction, or operational bridge; it only
imports `SEMANTIC`. There are no helper K files. `spec.k` adds the one
reachability claim already audited.

The configuration has exactly the state used by the target: computation,
function bindings, local environment, and returned result. No unread or
unwritten heap, stack, I/O, allocation, exception, or other state cell is
hidden.

### Exhaustive ordinary-rule inventory

| Rule | Source | Effect and soundness judgment |
|---|---|---|
| R1 | `semantic.k:40` | Consumes the submitted `Module(FuncDef(...))` and installs its exact parameter/body in an initially empty function map. It preserves the continuation. Sound for the single-definition generated subset. |
| R2 | `semantic.k:43` | Looks up the invoked name in the function map, executes that exact body, and binds its sole parameter to the integer argument. The target has no globals or caller frame, so replacing the local environment is exact for this invocation. |
| R3 | `semantic.k:47` | Turns `execute(Return(E))` into evaluation of `E` followed by result delivery. This preserves the active continuation and models the target's only statement. |
| R4 | `semantic.k:49` | Evaluates `Int(I)` to K integer `I`. Truthful; the submitted program does not depend on a literal, though the declaration is sound. |
| R5 | `semantic.k:51` | Evaluates `Name(X)` by exact map lookup. Both occurrences of submitted `Name("n")` resolve to the parameter binding installed by R2. |
| R6 | `semantic.k:54` | For operator string `"*"`, schedules the left operand before saving the right. It does not fabricate behavior for any other operator. |
| R7 | `semantic.k:57` | After the left operand is an integer, schedules the right operand and saves the left value. This implements left-to-right evaluation. |
| R8 | `semantic.k:60` | Multiplies the two evaluated K integers with trusted `*Int`. Operand placement yields the same result as submitted Python integer multiplication. |
| R9 | `semantic.k:62` | Consumes the return marker, writes the evaluated integer to `<result>`, and preserves any following computation. For the target, there is no remaining suffix. |

The front symbols and continuation markers make these rules pairwise
non-overlapping on the target path. No priorities are needed. There are no
guards, equations, recursive helpers, or totality claims whose coverage or
overlap could conceal an inconsistency. Unsupported statements or operator
strings have no rule and therefore stop visibly rather than producing an
oracle result.

### Used-construct coverage and control/data flow

The submitted constructor set is exactly `Module`, `FuncDef`, `Params`,
`Return`, `BinOp`, and `Name`. D1-D4 and D6-D7 declare those constructors;
R1-R3 and R5-R9 execute every material operation:

```text
Module/FuncDef/Params
  -> exact function binding
  -> run same binding with N
  -> execute Return
  -> evaluate left Name("n")
  -> evaluate right Name("n")
  -> *Int
  -> exact result cell
```

The module term precedes `run` in `<k>`, so installation happens before lookup.
Both name evaluations read the same local binding. The multiplication rule is
reached only after both operands are integers. The final rule updates the only
observable returned-result cell. Concrete outputs confirm all relevant final
cells, not only the numeric value.

I found no rule that encodes the task answer, skips a program-defined
computation, introduces an unconstrained result, or asserts a false equation.
Accordingly there is no claimed unsound rule requiring a false-conclusion
witness. The semantics intentionally does not model unused Python constructs;
that is permitted in `GENERATED_SEMANTICS` mode and no used construct is
missing.

Evidence: `evidence/stage5_static_inventory.sh` and
`evidence/stage5_static_inventory.log`.

**Stage result: PASS.**

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact; none was submitted. I created
`evidence/spec-vacuity.k` from the exact positive claim and changed only the
result obligation from `N *Int N` to `(N *Int N) +Int 1`. The executed program,
function binding, environment, precondition, and termination obligation remain
the same. `N = 0` satisfies the precondition and witnesses the false requirement
`0 = 1`.

First I required successful parsing/building:

```text
timeout 600s kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
```

It exited 0 and emitted a valid `kore-exec ... --prove ...` command. I then ran
the mutation normally:

```text
timeout 600s kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`, after actual execution reached `.K` and
the original result `N *Int N`. The residual was the expected unmet obligation:

```text
N *Int N +Int 1 #Equals N *Int N
```

This is a semantic proof failure, not a parser error, missing import, timeout,
unreachable mutation, or unrelated crash.

Evidence: `evidence/spec-vacuity.k` and
`evidence/stage6_non_vacuity.log`.

**Stage result: PASS.**

## 7. Proven versus assumed accounting

### What the proof establishes

Under the rebuilt candidate semantics and for every K integer `N >= 0`, the
exact constructor term regenerated from submitted `solution.py`:

```text
def car_race_collision(n: int):
    return n * n
```

installs the exact `car_race_collision` binding, binds `n` to `N`, evaluates
both actual `Name("n")` operands in left-to-right order, computes their K
integer product, terminates the modeled computation, and leaves the exact
result `N *Int N`.

This is a universal reachability proof, not a finite-size enumeration. The
formal status requested here is partial correctness. The modeled target is
also a finite straight-line computation with no loop or recursion, but that
termination observation is separate from the reachability theorem's generic
partial-correctness interpretation.

### Trust and assumption ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, and reachability engine | all builds, execution, and `#Top` | Foundational trusted toolchain; independently rebuilt rather than trusting candidate output. Acceptable. |
| Imported K `INT`, `STRING-SYNTAX`, and `MAP`, especially exact unbounded `*Int` | parsing, bindings, multiplication, postcondition | Standard K primitives. They are outside the local theorem but do not encode this task's answer. Acceptable. |
| Trusted `/reference/py2mpy.py` transliteration | Python-source to constructor identity | Launcher-designated trusted input; byte comparison proves the submitted `.mpy` is its exact output. Acceptable. |
| Program-specific generated semantics as a CPython bridge for module binding, one-argument invocation, local lookup, return, and integer multiplication | meaning of the K execution | Not assumed wholesale: all nine local rules were reviewed, used constructs were mapped, concrete boundary/normal executions agreed with both Python functions, and body/result mutations were rejected. Minimal unused-language coverage is acceptable in this mode. |
| Natural-language fact that each of `n` cars in one direction meets each of `n` opposite-direction cars once | identification of `n*n` with the requested collision count | Ordinary combinatorial interpretation of the prompt, supported by the trusted canonical `n**2`. It is not smuggled into a proof rule. Acceptable. |
| Finite differential tests | empirical source/canonical/semantics bridge only | 1,114 Python comparisons and six K/Python comparisons; explicitly not used as the universal proof. Acceptable supporting evidence. |

There are no local opaque symbols, empirical oracles, proof-local
simplifications, derived lemmas, operational bridges, circular summaries,
auxiliary loop claims, or unstated allocation/control effects. Candidate prose,
historical `#Top`, and generation traces played no role in accepting the
reconstructed proof.

The theorem's `N >= 0` precondition matches the natural-language count domain:
a number of cars cannot be negative. Therefore it does not materially narrow
the HumanEval source contract. Negative Python integers were nevertheless
tested observationally and all three executions agree, but that behavior is
not claimed by the K theorem. Non-integer Python values, including booleans as
a Python-specific subclass of `int`, are outside the stated integer-count
contract and the generated syntax.

Kit validation gates:

- Gate A, real-program soundness: **PASS**.
- Gate B, intent adequacy: **PASS**.
- Gate C, trust and evidence auditability: **PASS**.

The proof is sound, result-constraining, constructor-pinned to trusted
regeneration of the real submitted program, and covers the material source
domain. No material adequacy or soundness gap remains.

VERDICT: PASS
LEGITIMACY: LEGIT
