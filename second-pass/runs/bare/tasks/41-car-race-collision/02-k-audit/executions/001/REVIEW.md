# Independent adversarial audit: 41-car-race-collision

## Decision summary

The candidate contains a legitimate, result-constraining reachability proof of
the exact submitted `solution.mpy` term under its freshly reconstructed
generated semantics. The candidate's compiled definition was not used. A fresh
Haskell build succeeded, the only positive target claim exited 0 with `#Top`,
and independent false-result and source-body mutations both reached meaningful
stuck implications and exited 1.

I found no semantic or verification rule that can produce a false result on the
claimed domain of nonnegative integers. The generated semantics executes the
actual name lookups and integer multiplication; it has no proof-specific
shortcut, result oracle, helper claim, simplification, or task-answer rewrite.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because two
bridges remain outside the K theorem: the deliberately tiny generated semantics
is connected to CPython's behavior for this used fragment by rule inspection
and finite concrete tests, and the interpretation of `n*n` as the collision
count is a simple but informal pair-counting argument corroborated by the
trusted canonical implementation. Neither limitation permits the K proof to
establish a false program result.

All evidence cited below is reviewer-authored or a bounded record of an exact
command. The principal reproducibility drivers are
`evidence/run_audit.sh` and `evidence/supplemental_checks.sh`.

## 1. Input and provenance integrity

### Rendered semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` does not exist, exactly as this mode requires.
There is therefore no infrastructure contradiction and no hidden or inferred
reference semantics was used. See `evidence/provenance.log`.

### Required inputs and candidate artifacts

I read the candidate's `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the 85-record structured JSONL trace only as untrusted
generation claims. Their bounded claims are recorded in
`evidence/untrusted_claims.log`. In particular, the generation report claimed
that `./prove.sh` exited 0, concrete inputs 0, 3, and 10 produced 0, 9, and 100,
and `kprove` printed `#Top`. None of those claims was used as proof evidence.

The following required artifacts are present as regular files, not symlinks:

- `prompt.py`, `py2mpy.py`
- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`, `prove.sh`
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`
- `codex-trace/2026/07/22/rollout-...jsonl`

The trace parsed as 85 valid JSON records. The full file-type, byte-size, and
SHA-256 inventory is in `evidence/provenance.log`. There are no missing,
mistyped, changed, or symlinked required artifacts.

The candidate also contains an extra `verification-kompiled/` directory. It is
recognizable as generated build output, not additional source. It was treated
as untrusted evidence, was never copied into scratch, and was never passed to
`krun` or `kprove`. No extra helper K source exists. A candidate `PROOF.md` or
`spec-vacuity.k` is absent, but neither is a required generation artifact and
the fresh mutation required by this audit was created independently.

### Trusted-input comparisons

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their hashes
also match the claims in `run-input.json`:

- prompt:
  `d4a9a6f17e6f65f8fa63bffa89d863ca691859fab85fff3f60f378d9340cc489`
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

These comparisons and JSON checks exited 0 in `evidence/provenance.log`.

### Isolation

Only explicit source inputs were copied to `/tmp/audit-work/race41`. Candidate
build products and caches were excluded. The copied candidate source hashes
match the originals, and the submitted and regenerated MPY terms share SHA-256
`8878b8488943a7fc31808899d00a3cbf433c48b524f0f1515c79f92c10e6e659`.
See `evidence/scratch_copy.log`, `evidence/scratch_manifest.log`, and
`evidence/source_hashes.log`.

Stage 1 result: pass.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and intended domain

The trusted prompt describes two groups of `n` cars moving in opposite
directions on a line, with collisions not changing either trajectory. For a
nonnegative integer number of cars, every car in the first group meets every
car in the second group exactly once. There are therefore `n * n` cross-group
pairs and collisions. With no cars (`n = 0`), the result is 0.

The trusted canonical entry point returns `n**2`. The candidate returns `n*n`.
For Python integers these are equivalent. The specification's `N >=Int 0`
matches the natural domain of a car count. Although Python annotations are not
runtime-enforced and the canonical expression also happens to work for negative
integers, negative car counts are outside the stated physical problem.

The mounted prompt contains no explicit input/output examples. Consequently,
there were no documented examples to replay. The program has no branches or
loops, so there are no internal branch boundaries; 0 and 1 are the material
empty/small boundaries.

### Translator fidelity

I regenerated MPY from the scratch copy of `solution.py` using the trusted
mounted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/race41/solution.py \
  > /tmp/audit-work/race41/solution.regenerated.mpy
```

The command exited 0, and `cmp -s` between the regenerated and submitted MPY
files exited 0. See `evidence/regenerate_mpy.log` and
`evidence/mpy_byte_identity.log`.

The exact submitted term is:

```text
Module(
  FuncDef("car_race_collision", Params("n"),
    Return(BinOp("*", Name("n"), Name("n")))))
```

### Independent differential test

`evidence/differential_test.py` independently loads the trusted
`/reference/canonical.py` entry point and the scratch copy of the submitted
`solution.py`; it does not reuse a K equation or candidate test harness. Its
input specification is preserved in `evidence/differential_inputs.json`.

The test covered:

- explicit values 0, 1, 2, 3, 10, 41, 100, 999, 1,000,000, and 1,000,000,000;
- every integer from 0 through 200;
- 1,000 deterministic pseudorandom integers from 0 through 1,000,000,000,
  using seed 410041.

The run made 1,211 comparisons over 1,204 unique inputs, found zero mismatches,
and exited 0. See `evidence/differential.log`. This is finite fidelity evidence,
not a universal proof; universal equivalence of `n*n` and `n**2` is the ordinary
integer identity used in the adequacy argument.

Stage 2 result: pass.

## 3. Clean proof reconstruction

The available tools were K v7.1.293 and Python 3.10.12
(`evidence/tool_versions.log`).

### Fresh concrete definition

From the copied `semantic.k`, I built a new LLVM definition at
`/tmp/audit-work/race41/semantic-llvm-kompiled`:

```text
kompile /tmp/audit-work/race41/semantic.k \
  --backend llvm \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/race41/semantic-llvm-kompiled
```

It exited 0 (`evidence/kompile_llvm.log`). Fresh `krun` executions of the actual
submitted MPY term produced:

| `N` | K result | trusted canonical | submitted Python |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 3 | 9 | 9 | 9 |
| 10 | 100 | 100 | 100 |
| 41 | 1681 | 1681 | 1681 |

Every `krun` exited 0 with an empty `<k>` cell. Exact commands and complete
bounded configurations are in `evidence/krun_n_0.log`,
`evidence/krun_n_1.log`, `evidence/krun_n_3.log`,
`evidence/krun_n_10.log`, and `evidence/krun_n_41.log`. The independent parser
and three-way comparison exited 0 with zero mismatches in
`evidence/concrete_comparison.log`.

### Fresh proof definition and every positive claim

I separately built a new Haskell proof definition from `verification.k` and
the required copied `semantic.k`:

```text
kompile /tmp/audit-work/race41/verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/race41/verification-kompiled
```

It exited 0 (`evidence/kompile_haskell.log`).

`spec.k` contains exactly one positive target claim and no helper claims. I ran
it independently with an explicit spec module:

```text
kprove /tmp/audit-work/race41/spec.k \
  --definition /tmp/audit-work/race41/verification-kompiled \
  --spec-module SPEC
```

The command exited 0 and printed exactly `#Top`; see
`evidence/kprove_positive.log`. No candidate-provided compiled definition,
cache, proof log, or prior `#Top` contributed to this result.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

There is one entry claim in `/candidate/spec.k`.

Its precondition is:

- `N` is a mathematical K integer satisfying `N >= 0`;
- `<k>` contains the exact AST term for the submitted function definition,
  followed by `run("car_race_collision", N)`;
- the function and environment maps are empty;
- the result cell is initially 0.

Its postcondition is:

- `<k>` is empty;
- the function map contains the exact submitted binding from
  `"car_race_collision"` to parameter `"n"` and the exact multiplication body;
- the environment contains `"n" |-> N`;
- the result has changed from 0 to `N *Int N`.

This is equality-bearing state rewriting, not a free right-hand variable,
tautology, or one-way implication. The actual return value is constrained to
the square.

### Pinning the submitted program

`kprove` does not read `solution.mpy` by filename; the claim embeds its parsed
term. That embedded term is constructor-for-constructor identical to the
submitted `solution.mpy`, and the trusted translator regeneration is
byte-identical to it. Thus the theorem is pinned syntactically to the submitted
program rather than to a substitute or summary.

The real control flow is also exercised:

1. the module rule records the submitted function body;
2. `run` retrieves that same body and binds its actual parameter;
3. `Return` schedules evaluation and result completion;
4. the left `Name("n")` is looked up;
5. the right `Name("n")` is looked up;
6. K integer multiplication computes the return value;
7. the return completion writes that value to `<result>`.

There is no helper or loop claim to cross-check because the program has no
helper or loop.

### Satisfiable witness and concrete substitution

Take `N = 3`. It is a K integer and satisfies `N >= 0`; the initial state with
the exact term, empty maps, and result 0 is the default configured state.
Substitution gives the claimed result `3 * 3 = 9`. The fresh K execution, the
trusted canonical Python implementation, and the submitted Python
implementation all produced 9 (`evidence/krun_n_3.log` and
`evidence/concrete_comparison.log`). The boundary witness `N = 0` similarly
produced 0 in all three.

### Body sensitivity

As an additional real-program sensitivity check, I replaced the body in a
separate claim with `Return(Int(0))` while retaining the square
postcondition. The mutated function executed to result 0, and `kprove` exited 1
with a failed implication `0 #Equals N *Int N`. This is genuinely false at the
satisfying input `N = 2`, where 0 differs from 4. See
`evidence/spec-body-mutation.k` and
`evidence/kprove_body_mutation.log`. The proof therefore depends on the actual
body rather than only on the function name or claimed result.

Stage 4 result: pass.

## 5. Rule-by-rule static soundness review

The complete reviewed source, with line numbers, is preserved in
`evidence/reviewed_source_listing.log`. There are no generated helper K files.
`verification.k` merely requires `semantic.k` and imports `SEMANTIC`; it adds no
syntax, functions, claims, rewrites, or simplifications.

### Declaration inventory

The local source declarations are exhaustive below.

| Source | Declaration | Role and review |
|---|---|---|
| `semantic.k:5` | `Pgm ::= Module(Stmt)` | Parses the one-statement submitted module. |
| `semantic.k:7-9` | `Stmt ::= FuncDef(String, Params, Stmt) \| Return(Expr)` | Covers the exact function definition and return statement. |
| `semantic.k:11` | `Params ::= Params(String)` | Covers the single submitted parameter. |
| `semantic.k:13-16` | `Expr ::= Int(Int) \| Name(String) \| BinOp(String, Expr, Expr)` | Covers names and multiplication in the submission; `Int` is a truthful additional literal case. |
| `semantic.k:24` | `run(String, Int)` | Internal entry computation supplied by the configuration. |
| `semantic.k:25` | `definition(String, Stmt)` | Data stored in the function map. |
| `semantic.k:26` | `execute(Stmt)` | Internal statement execution marker. |
| `semantic.k:27` | `evaluate(Expr)` | Internal expression evaluation marker. |
| `semantic.k:28` | `multiplyRight(Expr)` | Continuation preserving the unevaluated right operand. |
| `semantic.k:29` | `multiplyBy(Int)` | Continuation preserving the evaluated left integer. |
| `semantic.k:30` | `finishReturn` | Continuation that writes the evaluated return value. |

Every local syntax production has only a `[symbol(...)]` attribute. There are
zero local `[function]`, `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, opaque, macro, anywhere, or priority declarations. There are no
local equational functions, no totality or overlap obligations for functions,
and no proof-local operational bridges. The only claim is the target theorem in
`spec.k`.

The imported `INT` and `MAP` modules are standard K primitives and form an
explicit trust boundary discussed in stage 7.

### Configuration and cells

`semantic.k:32-38` defines exactly the state used by this program:

- `<k>` initially contains the parsed program followed by
  `run("car_race_collision", $N:Int)`;
- `<functions>` records the one function definition;
- `<environment>` records the local parameter binding;
- `<result>` records the observable return value and begins at 0.

There is no heap, allocation, I/O, exception, object, or call-stack cell because
the submitted body uses none of those features. The source type annotation is
intentionally absent from MPY under the trusted translator, but `$N:Int` pins
the modeled input to an integer.

### Ordinary semantic rules

There are exactly nine ordinary rules.

1. **Module/function registration (`semantic.k:40-41`).**  
   `Module(FuncDef(F, Params(P), BODY))` is consumed and the initially empty
   function map becomes `F |-> definition(P, BODY)`. On the only configured
   source shape this faithfully records the exact submitted name, parameter,
   and body. It neither evaluates nor fabricates a result.

2. **Function invocation (`semantic.k:43-45`).**  
   `run(F, I)` can proceed only when the function map contains the matching
   definition. It executes that retrieved `BODY` and replaces the local
   environment with `P |-> I`. On the actual path, `F`,
   `P`, and `BODY` came directly from rule 1 and the prior environment is empty,
   so binding and body selection agree with the top-level one-argument Python
   call.

3. **Return setup (`semantic.k:47`).**  
   `execute(Return(E))` schedules `evaluate(E)` before `finishReturn`. This
   preserves the requirement to evaluate the return expression before writing
   the result.

4. **Integer literal evaluation (`semantic.k:49`).**  
   `evaluate(Int(I)) => I` is the ordinary meaning of an integer literal. The
   submitted body does not use an integer literal, but the rule is true for the
   declared fragment and was also exercised by the body-sensitivity probe.

5. **Name lookup (`semantic.k:51-52`).**  
   `evaluate(Name(X))` becomes the integer mapped at `X`. Both submitted
   lookups are for `"n"`, and the exact environment contains only
   `"n" |-> N`; binding ambiguity is impossible on the entry path.

6. **Multiplication start (`semantic.k:54-55`).**  
   Only `BinOp("*", L, R)` is handled. It evaluates `L` and saves `R`, giving
   Python's left-to-right operand order. An unsupported operator remains visibly
   stuck rather than being assigned a guessed meaning.

7. **Right-operand sequencing (`semantic.k:57-58`).**  
   Once the left operand is an integer `I`, the rule evaluates `R` while saving
   `I`. This preserves both the evaluated value and operand order.

8. **Primitive multiplication (`semantic.k:60`).**  
   After the right operand evaluates to `J`, the rule computes `I *Int J`.
   This is a generic semantics rule for the multiplication operator actually in
   the source, not a rewrite from the function name or input directly to the
   task answer. Its correctness relies only on the standard K integer primitive.

9. **Return completion (`semantic.k:62-63`).**  
   The final integer before `finishReturn` consumes that continuation and writes
   the same integer into `<result>`. On the exact configured invocation there is
   no trailing computation or call frame to discard.

### Coverage, order, state, and overlap checks

Every submitted syntactic construct maps to both a declaration and an
operational path: `Module`, `FuncDef`, `Params`, `Return`, `BinOp("*",...)`, and
two `Name("n")` terms. The configuration-injected `run` term and every internal
continuation are also consumed. The clean runs end with `.K`, demonstrating no
used construct is silently unmodeled.

The rule heads are pairwise non-overlapping by their leading constructor or
their distinct continuation (`multiplyRight`, `multiplyBy`, or
`finishReturn`). The expression cases `Int`, `Name`, and `BinOp("*",...)` are
disjoint. There are no competing priorities. The left operand is fully
evaluated before the right. The selected body and both names are map-bound, and
the only state change affecting the theorem is the final result write.

For integer inputs, neither Python name lookup nor integer multiplication can
raise an exception, allocate, perform I/O, or mutate external state. K `Int` and
Python integers are both arbitrary precision, so there is no overflow-model
gap on the claimed domain.

### Narrow scope and soundness conclusion

The semantics is not a model of general Python. In particular, it supports only
one top-level, one-parameter definition, a return statement, integer literals,
integer names, and multiplication. Its invocation rule replaces any prior
modeled environment, and its return completion is not a general Python
call-stack unwinder. Those internal rules would need narrowing or more cells
before this semantics could justify arbitrary nested calls or arbitrary
continuations. Such states are outside both the source grammar exercised by the
submission and the exact entry claim; on the only reachable entry path the
prior environment is empty and no continuation follows the call. This is an
evidence/scope limitation, not a false conclusion witness on the intended
domain.

I do not label any inventoried rule unsound. Accordingly, there is no claimed
unsound rule for which a false-conclusion witness is required. No rule encodes
`car_race_collision`'s answer, bypasses its body, introduces an unconstrained
value, or silently fabricates behavior for an unmodeled used construct.

Stage 5 result: pass, with the stated reuse limitation.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact. I independently created
`evidence/spec-vacuity.k`, preserving the exact source term and precondition but
changing the result-constraining postcondition from `N *Int N` to
`(N *Int N) +Int 1`.

This mutation is demonstrably false at the satisfying boundary input `N = 0`:
the real K/Python result is 0 while the mutated destination requires 1. It is
also false for every satisfying integer.

The exact command was:

```text
kprove /tmp/audit-work/race41/spec-vacuity.k \
  --definition /tmp/audit-work/race41/verification-kompiled \
  --spec-module SPEC-VACUITY
```

The mutation parsed and built far enough to execute the entire source term. It
then exited 1 with `WarnStuckClaimState` and the expected failed result
implication:

```text
N *Int N +Int 1 #Equals N *Int N
```

The residual configuration had `.K` and actual result `N *Int N`; this was not
a parser error, missing import, timeout, unrelated crash, or unreachable
mutation. The complete bounded output is in
`evidence/kprove_vacuity.log`.

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the freshly built `SEMANTIC` theory, for every mathematical integer
`N >= 0`, the exact submitted constructor term for:

```python
def car_race_collision(n: int):
    return n * n
```

starting with empty function and environment maps and result 0, executes through
the recorded function body and reaches an empty computation whose result is
exactly `N *Int N`. The final function and environment maps are constrained as
well. The proof is body-sensitive and result-sensitive.

This is a theorem about the exact generated semantics and program term. It is
not, by itself, a theorem about all Python programs, CPython internals, physical
motion, or negative/non-integer inputs.

### Trust and assumption ledger

| Boundary | Influence | Evidence and assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, and reachability prover | Establishes all parsing, rewriting, and `#Top` results | Standard unavoidable toolchain trust; fresh dual-backend builds and exact logs make it auditable. Acceptable. |
| Imported K `INT` operations, especially `*Int` and `>=Int` | Fixes the returned value and claim domain | Standard mathematical primitives, not candidate-defined task lemmas. Acceptable low-level trust boundary. |
| Imported K `MAP` matching and update | Selects function/body and local name binding | Standard state primitive; exact singleton-map states make its use straightforward. Acceptable. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` syntax to `solution.mpy` | User-designated trusted input; candidate copy matches it and fresh output is byte-identical. Acceptable. |
| Generated semantic rules as a model of the used Python fragment | Affects body selection, evaluation order, binding, and final value | Exhaustively reviewed above; LLVM executions at five inputs and 1,211 Python differential cases support the bridge. No fixed CPython connection theorem exists, so this remains an informal/empirical bridge. Concerning but legitimate for this transparent fragment. |
| K `Int` versus Python `int` | Affects arithmetic domain | Both are unbounded signed integers for the used multiplication; no overflow or coercion is involved because the claim pins integer inputs. Acceptable. |
| Trusted `/reference/canonical.py` as behavioral oracle | Supports implementation-to-reference alignment | It returns `n**2`; 1,211 differential cases had zero mismatches. Finite testing is evidence, not a proof. The algebraic identity gives the general integer bridge. Acceptable with normal oracle trust. |
| Pair-counting interpretation of the prose | Connects the square to the requested number of collisions | Every one of `n` cars meets each of the other `n` cars once, yielding `n*n`; corroborated by the trusted canonical implementation but not formalized in K. This is the principal documented intent limitation. |
| Domain assumption `N >= 0` and integer input | Determines theorem scope | Natural for a count of cars and consistent with the prompt's `int` annotation. Negative values and non-integers are excluded from the theorem. Acceptable, and explicitly stated. |

There are no candidate-defined opaque values, fresh result symbols, trusted
program helpers, proof-local functions, lemmas, simplifications, or operational
bridges. Consequently, there is no interpretation-parametric oracle or circular
use of the same unconstrained symbol in execution and the postcondition.

### Gate accounting

- Real-program soundness: pass. The exact body executes; bindings, evaluation
  order, cells, and result are pinned; fresh body and result mutations fail.
- Intent adequacy: pass with a documented informal bridge. The formal domain
  matches nonnegative car counts and `n*n` matches the canonical program and
  pair-counting contract, but physical collisions are not themselves modeled.
- Trust and evidence auditability: pass. Commands, inputs, exit statuses,
  complete small outputs, source hashes, and mutation residuals are preserved
  under `evidence/`.

Differential and concrete tests support only the Python/semantics and
implementation/canonical bridges over their recorded finite inputs. They are
not treated as substitutes for the successful K reachability proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
