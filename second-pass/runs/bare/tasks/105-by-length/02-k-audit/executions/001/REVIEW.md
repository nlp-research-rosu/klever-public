# Independent adversarial audit: 105-by-length

## Audit conclusion

The candidate contains a legitimate K partial-correctness proof of the submitted
generated program under its generated, task-sized semantics. I reconstructed both
definitions from source, independently ran the sole positive claim, checked that
the proof constant is structurally identical to the trusted-translator output,
reviewed all 19 local rules, and obtained a meaningful failure from a fresh false
result mutation.

The verdict is `CONCERNS / LEGIT`, not `PASS`, because the K theorem's result is a
count/multiplicity characterization and the final equivalence of that
characterization to the prompt's sort-filter-reverse-name description is an
ordinary mathematical/informal bridge supported by finite differential evidence,
not a separate K theorem. Also, `spec.k:4` calls the claim “total-correctness,”
while the reachability proof supplied here is a partial-correctness proof. Neither
limitation allows a false result on the intended finite-integer-list domain.

All candidate files, candidate logs, traces, and prior `#Top` reports were treated
as untrusted. Candidate-built `.kbuild*` directories and Python caches were not
used.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount is consistent:

- `/reference/canonical.py`, `/reference/prompt.py`, and
  `/reference/py2mpy.py` are ordinary regular files.
- `/reference/reference-semantics` is absent, as this mode requires.
- No hidden or inferred reference semantics was sought or used.

The boundary check exited 0. See
[stage1_inventory.log](evidence/stage1_inventory.log).

### Candidate artifact inventory

The following required or audit-requested candidate artifacts are present as
ordinary, non-symlink files:

- provenance: `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and one structured JSONL generation trace;
- trusted-input copies: `prompt.py` and `py2mpy.py`;
- generated deliverables: `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and executable `prove.sh`.

There are no missing, mistyped, or symlinked required artifacts. Candidate
`prompt.py` is byte-identical to `/reference/prompt.py`, and candidate
`py2mpy.py` is byte-identical to `/reference/py2mpy.py`; both `cmp` commands
exited 0. Their SHA-256 values are, respectively,
`7610e97e9e03b58b9d2f83c6ffb2e08c7a8827a982645a091f53b347cdfa7a5b`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Extra candidate material consists of `.kbuild`, `.kbuild2`, `.kbuild3`,
`.kbuild4`, `__pycache__`, and the negative probe `mutation-spec.k`. These were
identified, excluded from reconstruction, and do not alter the source-integrity
result. There are no additional candidate helper `.k` files.

I read the provenance records only as claims. `run-input.json` identifies
problem `105-by-length`, condition `bare`, and the same prompt/translator hashes.
`metrics.json` reports a successful, non-timeout generation. `codex-last.txt`,
`codex-output.log`, and the trace claim that concrete tests, a negative mutation,
and `kprove #Top` succeeded. None of those claims was credited without fresh
reconstruction. The 154-line JSONL trace and both JSON files parse completely;
see [stage1_provenance_parse.log](evidence/stage1_provenance_parse.log). The
initial inventory log also records an unavailable `jq` command; the
reviewer-authored standard-library parser
[parse_provenance.py](evidence/parse_provenance.py) replaced that auxiliary
parsing step successfully.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

From `/reference/prompt.py` and `/reference/canonical.py`, the intended domain is
a finite array/list of integers. The function:

1. retains only values from 1 through 9;
2. orders the retained digits from 9 down to 1, preserving multiplicity; and
3. replaces each digit with its English name.

It returns an empty list for an empty input and ignores integers outside 1..9.

Candidate `solution.py` computes the same result by concatenating, in descending
digit order, a singleton name list repeated by `arr.count(digit)`. This is a
different algorithm from sorting, but for finite integer lists it has the same
content and multiplicity.

### Translation identity

In scratch, I ran:

```text
python3 /reference/py2mpy.py solution.py > /tmp/audit-work/runs/regenerated-solution.mpy
```

The command exited 0. The regenerated artifact is byte-identical to submitted
`solution.mpy`; both have SHA-256
`1ec674941b58bc015474414fb8141b0c2de0cc5c79102b4fe2ec7ad118c3f5fd`.
See [stage2_fidelity.log](evidence/stage2_fidelity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) imports the trusted
canonical entry point directly from `/reference/canonical.py` and the candidate
entry point from the scratch copy. It tests:

- all three documented examples;
- explicit empty, singleton 1..9, invalid-neighbor, duplicate, mixed-order, and
  long boundary cases;
- every integer list of length 0 through 4 over
  `[-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,55]`; and
- 503 deterministic generated/large cases with seed 105.

It executed 54,767 cases with zero mismatches and exit 0. Every input is
preserved in
[differential_inputs.jsonl](evidence/differential_inputs.jsonl), SHA-256
`e294d97e03802068ef66b6828a3528571b7925c2d4ad2c975a60a98f12349495`.
This is broad finite evidence, not a universal proof of intent equivalence.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/source`. No candidate
definition, `compiled.bin`, `definition.kore`, cache, scanner, or Python bytecode
was copied or referenced.

### Fresh builds

The following definitions were created at previously absent scratch paths:

```text
kompile semantic.k --backend llvm \
  --main-module MPY-COMPILED --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/concrete-kompiled

kompile semantic.k --backend haskell \
  --main-module MPY-COMPILED --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/proof-kompiled
```

Both commands exited 0. The installed K tools report version v7.1.293. See
[stage3_build.log](evidence/stage3_build.log).

### Positive claims

There is exactly one positive reachability claim, at `spec.k:7`; the corrected
source search and exit 0 are in
[stage3_claim_inventory.log](evidence/stage3_claim_inventory.log). An earlier
auxiliary grep in the proof log used an over-escaped boundary and exited 1; it
did not affect compilation or proof execution.

I independently ran:

```text
kprove spec.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module BY-LENGTH-SPEC
```

It printed exactly `#Top` and exited 0. See
[stage3_positive_proof.log](evidence/stage3_positive_proof.log).

### Fresh generated-semantics execution

The fresh LLVM definition executed submitted `solution.mpy` on eight normal and
boundary inputs: the documented nonempty case, empty input, documented invalid
integers, every valid digit in ascending and descending order, invalid
neighbors, duplicates mixed with invalid values, and arbitrary-precision large
integers. Each `krun` exited 0, and each `<result>` exactly matched both
independent Python implementations. The comparison reports eight successes and
zero failures in
[stage3_concrete_compare.log](evidence/stage3_concrete_compare.log); complete
per-case commands and K configurations are in `evidence/krun_case_*.log`.

## 4. Adequacy and real-program pinning

### Formal entry claim in plain language

The claim has no explicit `requires`, so its sorted precondition is:

- `<k>` contains `init(#solutionProgram)`;
- `<program>` contains the same `#solutionProgram`;
- `<input>` is `pyList(XS)` for an arbitrary K term `XS:PyVals`; and
- `<result>` is `noResult`.

Its postcondition requires:

- `<k>` to be empty;
- `<program>` and `<input>` to remain unchanged; and
- `<result>` to be exactly `#byLength(XS)`.

There are no loop claims, helper reachability claims, existential result
variables, `ensures` implications, or omitted result constraints. The result is
therefore not free or tautological.

### Actual-program identity

`#solutionProgram` is not an opaque program oracle. Its sole equation expands to
a complete constructor AST. The reviewer script
[program_pinning.py](evidence/program_pinning.py) independently parses that AST
and trusted-translator `solution.mpy` into constructor trees. Their tree hashes
are both
`092d1ba399e16b6ffb2659cf1fb179c2057f1c14c80b9c39dd493bae7026bdc3`;
structural identity is true and the check exits 0. Thus the term executed from
the claim's `<k>` cell is the actual submitted translated program, not a
substitute. See [stage4_adequacy.log](evidence/stage4_adequacy.log).

### Satisfiability and grounded results

For example, this is a satisfying entry state:

```text
<k> init(#solutionProgram) </k>
<program> #solutionProgram </program>
<input> pyList(1 :: 9 :: 9 :: .PyVals) </input>
<result> noResult </result>
```

Substitution into `#byLength` yields
`pyList("Nine" :: "Nine" :: "One" :: .PyVals)`. Both Python implementations
return `["Nine", "Nine", "One"]`, and the fresh K semantics reaches that same
result (the fresh mutation residual in Stage 6 displays this exact state).
Stage 3 additionally grounds empty, documented, invalid, duplicate, and boundary
instances.

The formal `PyVals` sort is broader than integer lists because `Value` also
contains strings and nested `PyList` values. Rules intentionally become stuck
on unmodeled non-integer `count` inputs, and no `[total]` declaration fabricates
a value. This over-broad symbolic sort does not remove or strengthen away any
intended integer input. The theorem audited here remains partial correctness,
despite the inaccurate “total-correctness” source comment.

## 5. Rule-by-rule static soundness review

The complete numbered sources and generated inventory are preserved in
[stage5_static_inventory_corrected.log](evidence/stage5_static_inventory_corrected.log).
It finds 19 rules, eight `[function]` productions, one claim, and zero `[total]`,
`[functional]`, simplification, priority, `owise`, or opaque declarations.

### Local syntax and configuration inventory

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmt)`;
- `Stmt`: `FuncDef(String, Params, Stmt)` and `Return(Expr)`;
- `Params`: `Params(String)`;
- `Expr`: `Int`, `Str`, `Name`, `ListExpr`, `Attribute`, `Call`, and `BinOp`
  constructor forms;
- `Value`: builtin `Int`, builtin `String`, or `PyList`;
- `PyList`: `pyList(PyVals)`; and
- `PyVals`: `.PyVals` or `Value :: PyVals`.

Every constructor production has only a parser/symbol role; none rewrites or
asserts a result. `MPY-SEMANTICS` adds `init(Program)` and `noResult`. The
configuration has exactly the state needed here: `<k>`, inert program record,
input list, and result. There is no heap, output, exception, or allocation cell
whose state could be silently changed.

The eight function productions are `#eval`, `#add`, `#multiply`, `#count`,
`#appendVals`, `#repeatVals`, `#solutionProgram`, and `#byLength`. No one is
declared total, so unsupported unused terms stop visibly.

### Used-construct coverage

`solution.mpy` contains `Module` (1), `FuncDef` (1), `Params` (1), `Return`
(1), `BinOp` (17: eight additions and nine multiplications), `ListExpr` (9),
`Str` (9), `Call` (9), `Attribute` (9), `Name` (9), and `Int` (9). Coverage is:

- `Module`/`FuncDef`/`Params`/`Return`: the entry rule at `semantic.k:51`;
- `Int`, `Str`, and `Name`: `#eval` rules at lines 56–58;
- `ListExpr`: line 59;
- `BinOp("+",...)` and `BinOp("*",...)`: lines 60–63;
- the exact used `Call(Attribute(BASE,"count"),ARG)` form: lines 64–65; and
- list addition, repetition, append, and count: lines 73–88.

No used constructor is interpreted by a catch-all, oracle, or result-fabricating
fallback.

### All 19 local rules

| Location | Rule/classification | Soundness decision |
|---|---|---|
| `semantic.k:51-53` | Ordinary entry semantics | Matches the only modeled module/function/return shape, binds its sole parameter to `<input>`, consumes `init`, and writes only `<result>`. The claim pins the exact function body and name. Sound for this execution harness. |
| `semantic.k:56` | `#eval(Int)` | Returns the represented K integer. Sound. |
| `semantic.k:57` | `#eval(Str)` | Returns the represented K string. Sound. |
| `semantic.k:58` | `#eval(Name)` | Looks up the exact singleton map created by the entry rule. Sound for the sole parameter environment; unsupported environments do not match. |
| `semantic.k:59` | `#eval(ListExpr)` | Creates the used singleton list after evaluating its element. Sound for this AST subset. |
| `semantic.k:60-61` | `#eval` of `+` | Delegates to modeled value addition. Both operands are pure here, so the absence of observable Python left-to-right effects is immaterial. Sound on every used call. |
| `semantic.k:62-63` | `#eval` of `*` | Delegates to modeled list repetition. Sound on the used list-by-integer calls. |
| `semantic.k:64-65` | `#eval` of `.count` call | Evaluates base and integer argument and delegates to `#count`. The exact attribute name prevents accidental treatment of another method as count. Sound on every used call. |
| `semantic.k:73` | `#add` | Concatenates two `PyList` sequences via `#appendVals`. Sound. Other value combinations remain unsupported. |
| `semantic.k:74` | Append base | Empty left sequence returns the right sequence. Sound. |
| `semantic.k:75` | Append step | Preserves the head and recursively appends the tail. Sound and structurally descending. |
| `semantic.k:77` | `#multiply` | Repeats a `PyList` by an integer. Sound for Python list multiplication. |
| `semantic.k:78` | Repeat nonpositive branch | Returns empty for `N <= 0`, matching Python list repetition. |
| `semantic.k:79-80` | Repeat positive branch | Appends one copy and recurses on `N-1`; guard is disjoint from line 78 and recursion descends. Sound. |
| `semantic.k:82` | Count empty base | Returns zero. Sound. |
| `semantic.k:83-85` | Count equal-head branch | Adds one and recurses when integer head equals target. Sound. |
| `semantic.k:86-88` | Count unequal-head branch | Skips the head and recurses when unequal. The two nonempty guards are disjoint and exhaustive for integer heads. Sound. |
| `verification.k:8-37` | Definitional `#solutionProgram` | Expands once to the exact submitted AST. Structural identity is independently checked; it neither skips nor summarizes execution. Sound. |
| `verification.k:43-60` | Definitional `#byLength` | Expands once to nine descending singleton-name blocks, each repeated by the truthful semantic `#count`. It fixes every result-bearing value and has no overlap. It appears only as the postcondition summary, not as a rewrite of program execution. Sound. |

The ordinary semantic rules are pure on the intended domain. Consequently,
different internal evaluation ordering cannot affect bindings, control, state,
exceptions, or result. Count and repeat recursion are structurally/numerically
descending. Guard pairs do not overlap. The imported arbitrary-precision K
integer operations align with Python integers for the operations used.

Python allocates mutable list objects, while the semantics returns algebraic
list content. No later alias, mutation, identity test, exception handler, or
observable allocation exists in this function or its property, so this
abstraction preserves all relevant behavior. Likewise, the single-step
call/return harness is adequate because the submitted module contains exactly
one top-level function with one parameter and a single return expression.

There are no operational bridges in `verification.k`: `#solutionProgram` is a
literal program definition, and `#byLength` is a result specification connected
to fixed semantic execution by the main reachability claim. There are no
proof-local opaque values, priorities, simplifications, helper claims, or loop
circularities. I found no unsound rule; therefore no unsoundness label or false
conclusion witness is asserted.

## 6. Fresh non-vacuity test

Candidate `mutation-spec.k` was inspected only as untrusted evidence and was not
used. I created the new scratch mutation preserved at
[audit-vacuity.k](evidence/audit-vacuity.k). For the satisfiable input
`[1,9,9]`, it changes the result obligation from the true
`["Nine","Nine","One"]` to the false `["Nine","One"]`.

First:

```text
kprove audit-vacuity.k \
  --definition /tmp/audit-work/proof-kompiled \
  --spec-module AUDIT-VACUITY-SPEC --dry-run
```

exited 0, establishing successful parsing/building of the mutation. The actual
proof command, without `--dry-run`, exited 1. It emitted
`WarnStuckClaimState`; its residual has empty `<k>` and the actual result
`pyList("Nine" :: "Nine" :: "One" :: .PyVals)`, which does not unify with the
mutated destination. This is the expected unmet result obligation, not a parser
error, missing import, timeout, or unrelated crash. Exact commands and statuses
are in [stage6_vacuity.log](evidence/stage6_vacuity.log), with raw prover output
in [stage6_vacuity_proof.raw.log](evidence/stage6_vacuity_proof.raw.log).

## 7. Proven versus assumed accounting

### What the successful proof establishes

Under `MPY-SEMANTICS`, for every symbolic `XS:PyVals`, executing the exact
constructor program produced from submitted `solution.py` from the stated entry
configuration reaches empty `<k>` with unchanged program/input cells and result
exactly `#byLength(XS)`. On finite integer lists, that summary is the
concatenation of `"Nine"` through `"One"`, each repeated by the semantic count of
the corresponding integer.

This is partial correctness under the modeled semantics. It does not establish
the source comment's claimed total correctness, resource availability, CPython
object identity/allocation behavior, behavior of non-list inputs, custom
equality, booleans as Python `int` subclasses, or arrays containing non-integer
objects. Those behaviors are outside the prompt's intended finite-integer-list
domain and outside this minimal generated semantics.

### Trust and assumption ledger

| Boundary | Dependents and status |
|---|---|
| K v7.1.293 compiler, LLVM executor, Haskell prover, and reachability logic | Trusted toolchain boundary for both concrete and symbolic results. Acceptable and unavoidable for a K proof audit. |
| Imported K `INT`, `BOOL`, `MAP`, and string primitives | Supply arbitrary-precision arithmetic, integer comparison/equality, singleton map binding, and strings. They affect all semantic functions. Acceptable low-level primitives; none encode this task's answer. |
| Trusted `/reference/py2mpy.py` | Bridges `solution.py` to constructor syntax. Mandated trusted input; fresh regeneration and byte identity pin the submitted artifact exactly. |
| Generated `semantic.k` | Models only the constructs actually used. Its 17 semantic rules were reviewed individually and exercised concretely; no rule is treated as an opaque oracle. The remaining Python-language surface is intentionally excluded. |
| `#solutionProgram` | Not assumed or opaque: fully defined and structurally checked against trusted-translator output. |
| `#byLength` | Not opaque: fully defined by one non-overlapping equation. The main K claim universally connects real modeled execution to this summary. |
| Count characterization equals sort/filter/reverse/name contract | Informal ordinary-mathematics bridge: descending blocks with source multiplicities are exactly the filtered descending sort. Supported by 54,767 canonical differential cases, but not a separate machine-checked K theorem. This is the principal documented concern. |
| Canonical-vs-candidate and Python-vs-K tests | Finite empirical evidence only. They support program-intent and semantics bridges but do not replace the K reachability proof. |

There are no fresh uninterpreted or opaque result symbols, empirical operational
bridges, trusted program-defined helpers, proof-local semantic shortcuts, or
informal arguments used to justify a false semantic rule.

### Decision gates

- Real-program soundness: **pass**. Fresh `#Top`, exact program pinning,
  truthful/non-overlapping local rules, grounded distinct results, and a
  discriminating fresh mutation are all present.
- Intent adequacy: **pass with a documented bridge limitation**. The formal
  count/multiplicity result is equivalent to the intended finite-integer-list
  behavior, but that last equivalence is informal rather than a K lemma.
- Evidence/auditability: **pass**. Reviewer scripts, complete generated inputs,
  exact commands, statuses, bounded build/proof logs, and concrete results are
  preserved under `evidence/`.

The informal intent bridge and inaccurate total-correctness comment warrant
`CONCERNS`, but neither undermines the sound, result-constraining proof of the
real generated program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
