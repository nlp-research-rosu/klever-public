# Independent adversarial review: 27-flip-case

The candidate has a reproducible, non-vacuous K reachability proof of an
ASCII-only `swapcase` model, and its claim mechanically pins the submitted
program body. It does **not** prove partial correctness of that Python program
over the HumanEval `str` domain. The used supplied-semantics rule chain leaves
every non-ASCII code unchanged, whereas the real submitted program and trusted
canonical use Unicode-aware `str.swapcase()`. This is a material source-contract
domain/semantics gap and therefore maps to `FAIL / NOT_LEGIT` under the benchmark
decision rule.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, and the expected
`problem_id = 27-flip-case`. The supplied-semantics mount required for this mode
is present. There is no mode/mount contradiction and hence no infrastructure
breach.

I independently inspected all required pipeline-v3 records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- all 201 JSONL events in the structured trace under
  `/generation-evidence/codex-trace/`.

All required paths are real regular files or real directories. The structured
trace has one regular JSONL file and parses completely. Generation prose,
reported `#Top`, and the candidate's `PROOF.md` were treated only as untrusted
claims.

The audit campaign lock parses to exactly the `audit_campaign` object in
`/audit-input.json`; its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record. Direct hashes of every required record, prompt,
canonical, translator, and individual trace file match their launcher or
pipeline-v3 entries.

Using an independent reimplementation of the pipeline-v3
path/kind/size/content tree digest:

- mounted `/candidate` is
  `5b70c5e08d1887218f0001526d74dd4d599dcc6037a144818bde83fd6ea6bd8c`,
  exactly the workspace digest in both the invocation and stage result;
- the mounted trace tree is
  `4811068993eb0cac2c4adaa07411ea9ed15f6ce2c4ae8e480f6802c1faa87877`,
  exactly `usage.json`'s source-trace digest; and
- both candidate and trusted reference-semantics trees are
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  exactly the task-manifest semantics digest.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounts. A recursive lstat/type/name/content comparison between
`/candidate/reference-semantics/` and
`/reference/reference-semantics/` found zero differences: no missing,
additional, changed, mistyped, unsupported, or symlinked entry. Required
candidate proof artifacts are regular files.

Evidence:

- [provenance checker](evidence/audit_provenance.py) and
  [complete result](evidence/01-provenance.log);
- [structured-trace parser](evidence/summarize_generation_trace.py) and
  [bounded chronological index](evidence/01-generation-trace.log).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt (`/reference/prompt.py:3`) requires
`flip_case(string: str) -> str`: for a given string, lowercase characters become
uppercase and uppercase characters become lowercase. It gives
`flip_case("Hello") == "hELLO"`. There is no ASCII precondition.

The trusted canonical (`/reference/canonical.py:7`) returns
`string.swapcase()`. Python `str` values are Unicode strings, and the canonical
operation can change non-ASCII code points and can change string length.

The submitted `/candidate/solution.py` is:

```python
def flip_case(string: str) -> str:
    return string.swapcase()
```

It is the canonical algorithm with only the docstring omitted. Its input domain
is the full annotated Python `str` domain.

### Translation identity

In scratch, the trusted `/reference/py2mpy.py` regenerated `solution.mpy`.
`cmp` reported byte identity with the submitted file. Both translated files
have SHA-256
`f34d90ab871c6106c87ea64aa17e5ae4da5bfd5e86ca7ce805959554f8ae8620`.
The exact command and exit 0 are in
[02-translation.log](evidence/02-translation.log).

### Independent differential test

The reviewer-authored test imports the trusted canonical and submitted
implementation as separate modules. It covers:

- the documented example and empty input;
- ASCII case-branch boundaries immediately before, at, and after `A-Z` and
  `a-z`;
- the complete 128-character ASCII range, punctuation, digits, NUL, and
  newline;
- non-ASCII witnesses including `é`, `ß`, `İ`, Greek sigma forms, Cyrillic,
  titlecase, Deseret, and an emoji;
- 500 deterministic generated multi-character strings; and
- all 1,114,112 possible one-code-point Python strings, including surrogate
  code points.

There were zero mismatches. This establishes strong finite/exhaustive
single-character evidence that the submitted Python function matches the
trusted canonical. It does not establish that the K semantics matches either
Python implementation.

Evidence: [differential_test.py](evidence/differential_test.py) and
[02-differential.log](evidence/02-differential.log).

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/27-flip-case`. Candidate-provided `runtime-kompiled/`,
`verification-kompiled/`, caches, bytecode, and logs were neither copied nor
used.

The live tools independently report K v7.1.293:

```text
kompile --version  -> K version v7.1.293
krun --version     -> K version v7.1.293
kprove --version   -> K version v7.1.293
```

The exact version command is in [03-toolchain.log](evidence/03-toolchain.log).

### Fresh concrete definition

Command:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. Fresh `krun` executions of the exact submitted `solution.mpy` and
a reviewer-authored concrete suite covering `"Hello"`, empty, ASCII case
boundaries, digits, and punctuation both exited 0 with final `.K`, `NoExc`, and
exit code 0.

Evidence:
[03-kompile-llvm.log](evidence/03-kompile-llvm.log),
[03-krun-solution.log](evidence/03-krun-solution.log), and
[03-krun-ascii.log](evidence/03-krun-ascii.log).

### Fresh proof definition and all positive claims

Command:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0. `spec.k` contains exactly one positive target claim. Its independent
run was:

```bash
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`. The four unused-variable warnings come from the
trusted `semantics/str.k` and do not change that result.

Evidence:
[03-kompile-haskell.log](evidence/03-kompile-haskell.log) and
[03-kprove-positive.log](evidence/03-kprove-positive.log).

Stage 3 result: **PASS under the supplied K theory**. This is verification
closure, not yet a proof that the supplied theory describes the real Python
program over its intended domain.

## 4. Adequacy and real-program pinning

### Formal precondition and postcondition

The sole claim has no `requires` clause. Its precondition is therefore:

- an arbitrary symbolic `CS:IntSeq`;
- `<k>` containing module load of one function binding whose body is
  `return string.swapcase()`, followed by a call on `str(CS)`;
- module environment 0;
- an empty module scope with the supplied builtins parent;
- scope allocator 1, empty heap and stack, heap allocator 0, `noRet`, `NoExc`,
  and exit code 0.

Its destination requires:

- the returned value to be exactly `str(mapSwap(CS))`, not a free value,
  implication-only condition, or tautology;
- the exact `flip_case` closure to be added to module scope 0;
- the temporary function frame to be removed;
- environment, allocators, heap, stack, return state, exception state, and exit
  code to have the displayed final values.

Thus the formal theorem is result-constraining and also constrains all material
configuration cells exposed by this semantics.

### Program identity

The claim's `FuncDef` is constructor-identical to trusted regeneration of
`solution.mpy`. The only surface difference is the K list syntax sugar
`Call(..., )` versus explicit empty `.Exprs`; both normalize to the same
constructor. The mechanical comparison prints identical normalized
constructors. This is real constructor-level pinning, not an informal
source-name association.

Evidence:
[program_pinning.py](evidence/program_pinning.py) and
[04-program-pinning.log](evidence/04-program-pinning.log).

### Satisfying witnesses and concrete substitutions

The fixed initial state displayed in the claim is realizable; fresh ground
claims instantiate it. Both of these close with `#Top`:

- input code 65 (`"A"`) reaches code 97 (`"a"`);
- input code 233 (`"é"`) reaches code 233 under the supplied K model.

Evidence:
[spec-ground-ascii.k](evidence/spec-ground-ascii.k),
[04-ground-ascii-kprove.log](evidence/04-ground-ascii-kprove.log),
[spec-ground-unicode.k](evidence/spec-ground-unicode.k), and
[04-ground-unicode-kprove.log](evidence/04-ground-unicode-kprove.log).

The first substitution agrees with both Python implementations. The second does
not:

| Input | Supplied K result | Trusted canonical | Submitted Python |
|---|---|---|---|
| `"A"` / `[65]` | `[97]` / `"a"` | `[97]` / `"a"` | `[97]` / `"a"` |
| `"é"` / `[233]` | `[233]` / `"é"` | `[201]` / `"É"` | `[201]` / `"É"` |
| `"ß"` / `[223]` | `[223]` / `"ß"` | `[83,83]` / `"SS"` | `[83,83]` / `"SS"` |

The Python results and code points are independently recorded in
[ground_witnesses.py](evidence/ground_witnesses.py) and
[04-ground-python.log](evidence/04-ground-python.log).

A fresh claim demanding the real `"é" -> "É"` result builds and runs but exits
1 with `WarnStuckClaimState`; its actual terminal K result is code 233 while the
destination requires code 201. See
[spec-ground-unicode-real.k](evidence/spec-ground-unicode-real.k) and
[05-unicode-real-postcondition.log](evidence/05-unicode-real-postcondition.log).

### Body sensitivity

A reviewer-authored mutation changes the program term actually executed by the
claim to `return string` while still demanding `"A" -> "a"`. It builds, executes
the identity body, and exits 1 with a stuck terminal result of code 65. This
confirms that the positive proof depends on the submitted body.

Evidence:
[spec-audit-body-mutation.k](evidence/spec-audit-body-mutation.k) and
[04-body-sensitivity.log](evidence/04-body-sensitivity.log).

### Adequacy decision

The K precondition does not textually restrict `CS` to ASCII; instead, the used
case table silently gives non-ASCII inputs the wrong behavior. The prompt does
not restrict strings to ASCII, the trusted canonical selects Python's
Unicode-aware `str.swapcase()`, and `"é"` and `"ß"` are ordinary satisfying
inputs in the material source-contract domain. This is not a minor literal
parser limitation or a thin-testing concern. It is a false result for the real
program, including a case where the real result changes length.

Real-program pinning: **PASS**. Result constraint: **PASS**. Source-contract
adequacy: **FAIL**.

Under generic Kit terminology, the fixed-theory theorem would be
`SOUND-BUT-LIMITED`; because the limitation materially excludes/mismodels the
HumanEval string domain, the benchmark explicitly maps it to
`FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventory enumerates every source entry in all supplied K files,
`verification.k`, and `spec.k`, with source line, kind, attributes, role
decision, entry digest, and a bounded source preview. It contains:

- 227 syntax declarations;
- 695 ordinary rules;
- 5 contexts;
- 1 configuration;
- 1 reachability claim; and
- all 280 module/import/require/end-module structure entries,

for 1,209 inventoried entries total.

The complete inventory is
[05-rule-inventory.tsv](evidence/05-rule-inventory.tsv), generated by
[rule_inventory.py](evidence/rule_inventory.py). The independently generated
attribute and constructor summary is
[05-static-theory-summary.log](evidence/05-static-theory-summary.log).

`/candidate/verification.k` contains no syntax declaration, function,
`total`/`functional` declaration, opaque symbol, priority rule, ordinary rule,
simplification, or auxiliary claim. It only imports the supplied `MPY` module.
`spec.k` adds only the target claim. There are therefore no proof-local
operational bridges or program-result oracles.

Across the fixed semantics, the summary found 22 actual `[no-evaluators]`
symbols (float, sort, and MD5 boundaries). Every one is unused by this program
and target claim. There are no local `[simplification]` or `[functional]`
declarations. Priority, concrete-only, total, and owise declarations are all
line-addressed in the inventory.

### Construct coverage and exact execution slice

The submitted program uses only `Module`, `FuncDef`, `Params`, `Return`, `Call`,
`Attribute`, and `Name`, plus the empty `Exprs`/statement lists. Their
declarations and behavior map as follows:

| Construct | Declaration | Material behavior |
|---|---|---|
| `Module` | `syntax.k:61` | `core.k:124-127` loads and sequences statements |
| `FuncDef` | `syntax.k:53` | `functions.k:14-16` binds the exact closure |
| `Params` | `syntax.k:57,60` | `call.k:69-74`, `functions.k:63-66` allocate frame and bind left-to-right |
| `Return` | `syntax.k:50 [strict]` | `functions.k:78-90` records result and restores caller |
| `Call` | `syntax.k:28` | `call.k:20-24,69-74` evaluates callee/args and dispatches |
| `Attribute` | `syntax.k:29 [strict]` | `call.k:16` binds method to the evaluated receiver |
| `Name` | `syntax.k:12` | `core.k:130-154` performs scoped lookup |
| `"swapcase"` | method dispatch | `methods.k:21,112-164` computes the returned string |

The exact call path evaluates the function binding, evaluates the argument,
allocates scope 1, pushes the caller continuation, binds `string`, evaluates the
receiver before method dispatch, returns, removes scope 1, and restores the
caller. No output, exception, heap allocation, or mutable state operation is
skipped. The destination cells agree with this footprint.

Eighteen handwritten rules on this slice are faithful for the exact
configuration: module sequencing, binding/lookup, call evaluation, frame
creation, parameter binding, return, and pop. Their guards and priorities do
not overlap incorrectly on this ground control shape. The structural
`mapSwap` recursion decreases on the sequence tail.

The remaining 669 ordinary rules are exhaustively enumerated as
`UNUSED_FIXED_BASELINE_NO_TARGET_INFLUENCE`. They concern values, constructors,
continuations, or modules that cannot occur on this program's typed control
path (lists, dicts, loops, arithmetic, floats, sorting, MD5, and so on). This
classification is a claim-influence decision, not an endorsement of those
rules as a complete Python semantics. No alleged unsoundness of an unused rule
is needed for this verdict.

### Material false rule family and required witness

The eight used entries marked
`USED_FALSE_FOR_REAL_UNICODE_PYTHON` form one result-bearing rule family:

1. `methods.k:21` rewrites `str.swapcase()` to `str(mapSwap(CS))`.
2. `methods.k:113` and `:116` recognize only ASCII uppercase 65-90 and
   lowercase 97-122.
3. `methods.k:150-152` add/subtract 32 for those ranges and use `[owise]` to
   leave every other integer unchanged.
4. `methods.k:163-164` apply that one-code-to-one-code function structurally.

The rules are guard-disjoint and total as ordinary integer equations, but that
does not make them a valid summary of the real program's `str.swapcase()`.

Concrete false-conclusion witness: let the claim's unconstrained
`CS = iCons(233, .IntSeq)`. This is the valid Python string `"é"` and satisfies
the entry precondition. Both ASCII guards are false, so the `[owise]`
`swapC(233) => 233` rule fires. The rule family therefore enables the positive
K conclusion `flip_case("é") = "é"`; fresh `kprove` confirms that conclusion
with `#Top`. The trusted canonical and submitted Python instead return `"É"`
(code 201). This is exactly the required intended-domain false conclusion.

The independent `ß` witness is even stronger structurally: the pointwise K map
must preserve one element as code 223, while real Python returns two elements,
codes 83 and 83. No interpretation of the pointwise ASCII helper as the actual
Unicode operation can repair that mismatch.

Static theory result: **FAIL for real-program semantics**, despite the absence
of proof-local extensions and despite internally consistent ASCII equations.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation keeps the
exact submitted body and satisfying initial state, fixes input to `"A"`, and
changes only the result-constraining destination from the true code 97 (`"a"`)
to false code 98 (`"b"`).

Command:

```bash
kprove spec-audit-false-result.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-AUDIT-FALSE-RESULT
```

The spec parsed and executed successfully, then exited 1 for the expected proof
obligation. It emitted `WarnStuckClaimState`; the terminal residual contains
`str(iCons(97, .IntSeq))`, which cannot unify with the demanded code 98. This
is not a parser error, timeout, missing import, unrelated crash, or unreachable
mutation.

Evidence:
[spec-audit-false-result.k](evidence/spec-audit-false-result.k) and
[06-false-result.log](evidence/06-false-result.log).

Stage 6 result: **PASS**. The proof is non-vacuous and result-discriminating
inside the supplied model.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the exact supplied MPY theory, from the fixed initial cells in `spec.k`,
for every finite algebraic `CS:IntSeq`, executing the exact submitted
`flip_case` binding reaches:

```text
str(mapSwap(CS))
```

with the displayed closure installed, call frame removed, caller state restored,
heap unchanged, no exception, and exit code 0. `mapSwap` is defined by the
supplied ASCII case equations. The proof is unbounded in sequence length and
does not rely on examples or bounded unrolling.

It does **not** establish that `mapSwap(CS)` equals Python
`str.swapcase()` for every Python string. That missing bridge is precisely the
human-facing correctness property, and the bridge is false.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell prover, LLVM runtime, and K builtins | All build, execution, and proof results | Ordinary machine-checking TCB; versions and fresh runs recorded |
| Trusted `py2mpy.py` | Connects submitted Python syntax to `solution.mpy` | Acceptable here: trusted mount, candidate byte match, fresh byte-identical regeneration |
| Submitted constructor term versus claim term | Determines which body executes | Discharged mechanically; exact modulo empty-list syntax sugar |
| Supplied binding/call/return/configuration rules | Control and state footprint | Acceptable for this exact straight-line path; no proof-local bridge |
| Supplied `mapSwap`/`swapC` rule family | Entire returned value | Illegitimate as a bridge to the real program on the full `str` domain; concrete `"é"` and `"ß"` counterexamples |
| 22 fixed opaque float/sort/MD5 symbols | Could affect other programs | Unused and non-influential here; fully listed in static evidence |
| Canonical-versus-candidate differential testing | Python implementation fidelity | Strong finite/exhaustive-single-codepoint evidence only; it does not prove K/Python semantic equivalence |
| K `IntSeq` interpreted as Python `str` | Formal-to-source domain bridge | Only valid for the modeled subset; arbitrary integers are broader than valid code points, while valid non-ASCII code points are materially mishandled |

There is no proof-local primitive, fresh symbol, opaque result, empirical
summary, lemma, or rewrite on which claim closure depends. The fatal assumption
is instead the unproved and refuted interpretation of the supplied ASCII case
table as the real program's Unicode behavior.

### Gate and benchmark accounting

- Fresh dynamic reconstruction: **PASS**.
- Program identity/body sensitivity: **PASS**.
- Result constraint and non-vacuity: **PASS**.
- Proof-local extension soundness: **PASS** (there are no extensions).
- Real-program language-model/intent adequacy: **FAIL**.
- Evidence auditability: **PASS**.

The candidate's `#Top` is a legitimate proof of the narrower fixed-theory
statement, but not a legitimate partial-correctness proof of the real generated
program over the HumanEval source-contract domain. The material Unicode
restriction/mismatch is specifically a benchmark `FAIL`, not a non-fatal
`CONCERNS` outcome.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
