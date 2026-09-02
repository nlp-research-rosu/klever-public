# Independent adversarial audit — 14-all-prefixes

The candidate's two positive K claims do reconstruct successfully and the proof
is pinned to the submitted translated program. Nevertheless, the generated
language semantics is materially false for valid Python `str` inputs: it models
Python string length and slicing with byte-oriented K string primitives. A
concrete satisfying input, `"🙂x"`, makes the semantic rules conclude length
`5` and first prefix `"\xf0"`, whereas both real Python implementations conclude
length `2` and first prefix `"🙂"`. Because the formal proof can therefore
establish a result that is false of the real generated program on the intended
domain, the candidate is not a legitimate partial-correctness proof of that
program.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, as required. I did not search for, infer, or use any hidden
reference semantics. This is not an infrastructure-breach case.

The exact type/hash/symlink check and its exit status are in
[`evidence/stage1/integrity.log`](evidence/stage1/integrity.log). All of these
required candidate artifacts are regular files:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and one structured JSONL trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `solution-program.k`, `verification.k`,
  `verified-lemma.k`, `loop-spec.k`, and `spec.k`.

There are no symlinks anywhere under `/candidate`; no required artifact is
missing or mistyped. Candidate `prompt.py` is byte-identical to
`/reference/prompt.py` (SHA-256
`f4eca2c1c9ceb5ca5b0b0885dfd75fb4f768967fd2e53640176e413a499cc165`).
Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

The candidate also contains extra untrusted execution artifacts:
`verification-kompiled/`, `verified-lemma-kompiled/`, `__pycache__/`, and
`kore-exec.tar.gz`. These are not required source artifacts and were not used.
`embed_mpy.py`, `prove.sh`, and two run fixtures are source/helper artifacts and
were inspected but not trusted.

`run-input.json` claims problem `14-all-prefixes`, condition `bare`, and no
supplied semantics. `metrics.json` claims a successful, non-timeout generation.
`codex-last.txt` and `codex-output.log` claim two prior `#Top` results. The
structured trace is valid JSONL with 280 records and contains the same claims.
They were treated only as untrusted provenance. The bounded extracted claims
are in [`metadata_claims.log`](evidence/stage1/metadata_claims.log), and the
complete structured-record traversal and clipped command/output summary are in
[`trace_summary.log`](evidence/stage1/trace_summary.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a Python string, return every nonempty prefix from shortest to longest.
Thus `"abc"` maps to `["a", "ab", "abc"]`; the empty string maps to `[]`.

The trusted canonical implementation iterates `i` over
`range(len(string))` and appends `string[:i+1]`. The submitted implementation
starts `i` at 1, repeatedly appends `string[:i]` while
`i <= len(string)`, and increments `i`. These algorithms are equivalent on the
intended Python `str` domain, including the zero-iteration empty case.

### Trusted retranslation

I ran:

```text
python3 /reference/py2mpy.py /tmp/audit-work/src/candidate/solution.py > /tmp/audit-work/reconstruction/trusted-regenerated-solution.mpy
cmp -s /tmp/audit-work/reconstruction/trusted-regenerated-solution.mpy /tmp/audit-work/src/candidate/solution.mpy
```

`cmp` exited 0. Both files have SHA-256
`c0ecfda3a494d3a984bae3c41e23a58eb8d3eae4517868f08341afbe4419a5f6`.
The exact recorded command and status are in
[`translation_identity.log`](evidence/stage2/translation_identity.log).

### Independent differential test

[`differential_test.py`](evidence/stage2/differential_test.py) independently
imports `/reference/canonical.py:all_prefixes` and the scratch copy of the
submitted `solution.py:all_prefixes`. Its inputs are defined by
[`differential_inputs.json`](evidence/stage2/differential_inputs.json):

- the documented `"abc"` example;
- empty, one-character, loop-boundary, whitespace, NUL, combining-character,
  non-ASCII, and emoji cases;
- every string of lengths 0 through 5 over `["a", "b", "🙂"]`;
- 500 deterministic generated strings of lengths 0 through 40 over a wider
  ASCII/Unicode alphabet.

After stable de-duplication, 846 Python strings were executed. Each result was
also compared with the direct contract
`[s[:i+1] for i in range(len(s))]`. There were zero mismatches. The executed
input list, its SHA-256, command, exit 0, and results are in
[`differential.log`](evidence/stage2/differential.log).

This establishes strong finite evidence that the submitted Python
implementation matches the trusted implementation. It does not validate the K
language semantics.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work`; no
candidate-provided compiled definition, bytecode, cache, or log was copied into
the proof build. K was independently available as version `v7.1.293`; see
[`tool_versions.log`](evidence/stage3/tool_versions.log).

### Fresh concrete definition

The generated semantics compiled from source with:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/reconstruction/semantic-llvm-kompiled
```

It exited 0
([`kompile_semantic_llvm.log`](evidence/stage3/kompile_semantic_llvm.log)).
The run terms were independently wrapped around the trusted-regenerated
`solution.mpy` by
[`make_run_term.py`](evidence/stage3/make_run_term.py), not copied from the
candidate's fixtures.

Fresh LLVM `krun` results:

| Input | K result | Python result | Comparison |
|---|---|---|---|
| `""` | `listVal(vnil)` | `[]` | match |
| `"a"` | `["a"]` | `["a"]` | match |
| `"abc"` | `["a","ab","abc"]` | same | match |
| `"abcdef"` | six ordinary prefixes | same | match |
| `"🙂x"` | five byte prefixes: `"\xf0"`, `"\xf0\x9f"`, `"\xf0\x9f\x99"`, `"🙂"`, `"🙂x"` | `["🙂","🙂x"]` | **mismatch** |

The exact `krun` commands and outputs are
[`krun_empty.log`](evidence/stage3/krun_empty.log),
[`krun_a.log`](evidence/stage3/krun_a.log),
[`krun_abc.log`](evidence/stage3/krun_abc.log),
[`krun_abcdef.log`](evidence/stage3/krun_abcdef.log), and
[`krun_unicode.log`](evidence/stage3/krun_unicode.log). Both independent Python
functions return `["🙂", "🙂x"]`; all exact Python results are in
[`python_concrete.log`](evidence/stage3/python_concrete.log).

### Fresh proof definitions and every positive claim

The loop proof definition was built and proved with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/reconstruction/verification-kompiled
kprove loop-spec.k --definition /tmp/audit-work/reconstruction/verification-kompiled --spec-module LOOP-SPEC
```

Both commands exited 0; `kprove` printed `#Top`. See
[`kompile_verification_haskell.log`](evidence/stage3/kompile_verification_haskell.log)
and [`kprove_loop.log`](evidence/stage3/kprove_loop.log).

The entry proof definition was then built and proved with:

```text
kompile verified-lemma.k --backend haskell --main-module VERIFIED-LEMMA --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/reconstruction/verified-lemma-kompiled
kprove spec.k --definition /tmp/audit-work/reconstruction/verified-lemma-kompiled --spec-module SPEC
```

Both commands exited 0; `kprove` printed `#Top`. See
[`kompile_verified_lemma_haskell.log`](evidence/stage3/kompile_verified_lemma_haskell.log)
and [`kprove_entry.log`](evidence/stage3/kprove_entry.log).

Thus the candidate's positive formal claims do close under its supplied theory.
The failure verdict is not based on a timeout, parser failure, missing
toolchain, or failed reconstruction.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

`spec.k` quantifies a K `String` `S`. Its precondition is
`0 <=Int lengthString(S)`, which is satisfied by every finite K string. Starting
with empty variable and function environments, it executes
`Run(solutionProgram, Call(Name("all_prefixes"), Str(S)))`. It requires the
final `<k>` result to be exactly `listVal(allPrefixes(S))`, restores the
variable environment to empty, and existentially permits any final function
environment.

This is result-constraining, not a free-result or implication-only claim.

### Loop claim in plain language

`loop-spec.k` starts at the exact submitted loop, followed by the exact
`exec(Return(Name("result"))) ~> restoreEnv(OLD)` continuation. Its environment
binds:

- `"string"` to `strVal(S)`;
- `"result"` to `listVal(pacc(S,N))`;
- `"i"` to `intVal(I)`.

It assumes `0 <= lengthString(S)`, `0 <= N <= lengthString(S)`, and
`I = N+1`. It concludes that the loop/return reaches
`listVal(allPrefixes(S))` and restores `OLD`.

A concrete satisfying loop state is
`S="abc", N=0, I=1, OLD=emptyEnv`, with any function environment. A concrete
satisfying entry state is `S="abc"` (or `"🙂x"`) with the configuration's empty
initial state.

### Exact program and control-flow pinning

An independent wrapper reconstruction proves that `solutionProgram` expands
byte-for-byte to the trusted-regenerated submitted `solution.mpy`. Both wrapper
files have SHA-256
`3eaf083860f0ff3d0517ace61d36dd3ed5095d465320dca7a8fc859b9a5cd19a`;
see [`program_pinning.log`](evidence/stage4/program_pinning.log).

The semantics then:

1. executes the submitted module and exact function definition;
2. registers `all_prefixes`;
3. invokes the stored submitted body;
4. performs its two real assignments;
5. reaches the exact real `While` body and exact return/restore continuation.

The priority-30 rule in `verified-lemma.k` is an operational bridge, but it is
not a free oracle. It is exactly the `N=0, I=1` instance of the separately
proved `LOOP-SPEC`: `pacc(S,0)` is `vnil`, and all remaining loop-claim guards
discharge. Its matched loop syntax, continuation, bindings, environment
restoration, function cell, and returned value are no broader than that proved
instance.

### Concrete substitution into the claimed result

Under the proof definition:

- `S=""` produces `listVal(pacc("",0))`;
- `S="abc"` produces `listVal(pacc("abc",3))`;
- `S="🙂x"` produces `listVal(pacc("\xf0\x9f\x99\x82x",5))`.

These exact executions are in
[`claimed_result_empty.log`](evidence/stage4/claimed_result_empty.log),
[`claimed_result_abc.log`](evidence/stage4/claimed_result_abc.log), and
[`claimed_result_unicode.log`](evidence/stage4/claimed_result_unicode.log).
The base/step accumulator equations and proved loop claim connect `pacc` to the
candidate K execution, so this is a genuine formal constraint rather than an
unconstrained result symbol.

For ASCII `"abc"`, direct K execution and both Python implementations agree on
three prefixes. For `"🙂x"`, which also satisfies every formal entry
precondition, the claimed summary uses K length 5 and the direct K semantics
returns five byte prefixes, while both Python implementations return two
code-point prefixes. The proof therefore pins the submitted syntax but not the
real Python meaning of that syntax over its intended domain.

## 5. Rule-by-rule static soundness review

The exhaustive reconstructed inventory is
[`evidence/stage5/rule_inventory.md`](evidence/stage5/rule_inventory.md), with
the source-declaration extraction in
[`source_declarations.log`](evidence/stage5/source_declarations.log). It
enumerates all local syntax, configuration cells, 39 `semantic.k` rules, every
proof/helper rule, both claims, all `[function]` declarations, the sole
`[simplification]` rule, the sole priority rule, and the absence of any local
`[total]` or `[functional]` declaration.

### Syntax, cells, functions, and used-construct coverage

The local syntax declares `Module`/`Run`; statement lists; `ImportFrom`,
`FuncDef`, `Assign`, `While`, expression statements, and `Return`; parameters;
names, integers, strings, lists, binary operations, comparisons, calls,
attributes, subscripts, slices, and bounds. Runtime sorts model values, linked
variable/function environments, functions, and the `exec`, `loop`,
`restoreEnv`, `returning`, and `invoke` control items. The three-cell
configuration contains `<k>`, `<env>`, and `<functions>`.

The submitted `solution.mpy` uses every one of these relevant paths:
`Module`, `ImportFrom`, `FuncDef`, `Params`, name assignments, empty list,
integer, `While`, one `<=` comparison, `len`, `append`, prefix slice, integer
`+`, and `Return`. Every used construct has a declaration and applicable
rules. No used construct is silently unmodeled.

Local `[function]` symbols are `lookup`, `update`, `flookup`, `snoc`, `eval`,
`addVal`, `lenVal`, `lessEqVal`, `prefixVal`, `appendVal`, `truth`,
`solutionProgram`, and `allPrefixes`. `pacc` is the only new opaque/result-
bearing constructor.

### All 39 semantic rules

- R1-R2 (`lookup`), R3-R5 (`update`), and R6-R7 (`flookup`) are structurally
  descending linked-environment operations. Hit/miss guards are disjoint.
  Lookups are partial on empty environments, but all target-path names and the
  target function are present.
- R8-R9 implement ordinary list `snoc` correctly.
- R10-R13 correctly evaluate integer/string/name/empty-list syntax as far as
  representation permits.
- R14 and R18 implement the target's pure integer `+`; R16, R20, and R23
  implement integer `<=` and Boolean truth. K integers agree with Python's
  unbounded integers here.
- R15 dispatches target `len` to R19. R19 is materially unsound as Python
  semantics.
- R17 dispatches the exact target prefix slice to R21. R21 is materially
  unsound as Python semantics.
- R22 delegates list append to the truthful `snoc` rules.
- R24-R27 correctly schedule `Run`, module execution, and statement sequences
  left-to-right.
- R28 ignores `from typing import List`. This is sound for result behavior of
  this target: annotations were omitted by the trusted transliteration and the
  imported name is never used. It is deliberately incomplete as a general
  Python import semantics.
- R29 registers the exact one-parameter function. The separate function
  environment is adequate here because the body needs no program global or
  closure.
- R30 evaluates a name-assignment RHS in the old environment and then updates
  the binding, matching the target.
- R31 specializes `Name(X).append(E)`. On this target path, `X` is the
  unaliased list `result`, `E` is pure, and all operations are defined; it
  preserves the target's observable behavior. It would be over-broad for a
  general Python language, but I found no false conclusion witness for the
  submitted program on its intended inputs.
- R32-R34 implement while lowering and complementary true/false branches.
- R35-R36 implement the exact one-argument named call with a fresh local
  environment and restoration frame; this is sufficient for the target body.
- R37-R39 evaluate return, discard remaining statement execution, restore the
  caller environment, and expose the returned value. Nested-loop returns are
  incompletely modeled, but that unused context is not the submitted control
  flow.

### Concrete false-conclusion witnesses for the unsound rules

`semantic.k:102` contains:

```text
rule lenVal(strVal(S)) => intVal(lengthString(S))
```

For the intended Python input `S="🙂x"`, a fresh direct probe reduces this to
`intVal(5)`. Real Python gives `len("🙂x") == 2`. The exact probe source is
[`unicode-probe.k`](evidence/stage5/unicode-probe.k) and the successful output
is [`krun_unicode_len_probe.log`](evidence/stage5/krun_unicode_len_probe.log).

`semantic.k:104` contains:

```text
rule prefixVal(strVal(S), intVal(I)) => strVal(substrString(S, 0, I))
```

For the intended input `S="🙂x", I=1`, a fresh direct probe reduces this to
`strVal("\xf0")`. Real Python gives `"🙂x"[:1] == "🙂"`. See
[`krun_unicode_prefix_probe.log`](evidence/stage5/krun_unicode_prefix_probe.log).

The full program witness in [`krun_unicode.log`](evidence/stage3/krun_unicode.log)
shows the consequence: the loop executes five times and fabricates partial
UTF-8-byte strings that the Python program never returns. These are concrete
false conclusions on a valid intended-domain input, not merely missing
evidence or an unused-language gap.

### Proof/helper rules

- `solutionProgram` is a truthful `[function]` expansion of the exact
  submitted term (P1).
- `pacc(S,0) => vnil` is the truthful accumulator base (V1).
- The sole `[simplification]` rule says appending prefix `N+1` to
  `pacc(S,N)` produces `pacc(S,N+1)` (V2). It is a definitional proof summary,
  not an operational bypass. It is truthful on the loop claim's guarded
  `0 <= N < lengthString(S)` domain. Its written guard is broader than that
  interpretation; this is a narrow reuse/evidence gap, not the basis of the
  verdict, because no false conclusion on the intended entry domain was found.
- `allPrefixes(S) => pacc(S,lengthString(S))` names the formal summary (V3).
  It inherits the R19 byte-length defect.
- The priority-30 loop rewrite (L1) is an exact operational bridge derived
  from the independently successful loop claim, as analyzed in Stage 4. It
  does not admit an arbitrary continuation or omit an observable cell. It
  nonetheless returns the byte-based formal summary because its underlying
  semantic theory is already wrong.

The built-in K integer/Boolean/string operations are a normal low-level trust
boundary. The illegitimate step is not trusting K's implementation of its own
`lengthString`/`substrString`; it is using those byte-oriented operations as
unqualified models of Python's code-point `len` and slicing.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created a fresh mutation in
scratch and preserved it as
[`evidence/stage6/spec-vacuity-audit.k`](evidence/stage6/spec-vacuity-audit.k).
It changes the result-bearing postcondition to claim that every call returns
`listVal(vnil)`. This is demonstrably false for the satisfying input `S="a"`;
both Python functions and fresh K concrete execution return `["a"]`.

The mutation first built successfully:

```text
kprove spec-vacuity-audit.k --definition /tmp/audit-work/reconstruction/verified-lemma-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run
```

Exit status was 0
([`mutation_dry_run.log`](evidence/stage6/mutation_dry_run.log)).

The actual proof command:

```text
kprove spec-vacuity-audit.k --definition /tmp/audit-work/reconstruction/verified-lemma-kompiled --spec-module SPEC-VACUITY-AUDIT
```

exited 1 with `WarnStuckClaimState`. Its residual has
`listVal(pacc(S,lengthString(S)))` in `<k>`, which cannot unify with the mutated
`listVal(vnil)` destination. This is the expected unmet result obligation, not
a parser error, missing import, timeout, or unrelated crash. See
[`mutation_proof.log`](evidence/stage6/mutation_proof.log).

The positive proof is therefore non-vacuous and result-discriminating. That
does not make its generated language semantics faithful to Python.

## 7. Proven versus assumed accounting

### Precisely what the K proof establishes

Under the candidate's `MPY` rules, its proof-local accumulator equations, and
the derived loop rewrite, the reconstructed reachability proof establishes:

- for every K `String` `S`, if the exact submitted `solutionProgram` invocation
  terminates under that theory, its `<k>` result is
  `listVal(pacc(S,lengthString(S)))`;
- the local variable environment is restored to `emptyEnv`;
- the function environment may contain the registered function;
- the exact loop satisfies the stated `pacc(S,N)` invariant and reaches the
  same summary under its formal guards.

This is a genuine, non-vacuous partial-correctness theorem about the candidate
K transition system. It is not a correct theorem about all executions of the
real Python program because that transition system gives used Python string
constructs the wrong meaning.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, LLVM/Haskell backends, reachability prover | All dynamic evidence and both `#Top` results | Ordinary toolchain trust boundary; fresh builds agree and no infrastructure symptom occurred. |
| Trusted `/reference/py2mpy.py` | Program AST identity | Acceptable. Retranslation is byte-identical. |
| K integer and Boolean primitives | Increment, comparison, loop guards | Acceptable for this program; matches Python behavior. |
| K `String`, `lengthString`, `substrString` | Loop count, every prefix, `pacc`, `allPrefixes`, loop lemma, entry theorem | **Illegitimate Python bridge.** Concrete Unicode witnesses disprove it on the intended domain. |
| Candidate variable/function/call/control rules | Real-program execution path | Sound for the exact target path after exhaustive static review; intentionally incomplete unused constructs are not relied upon. |
| `pacc` base/step interpretation | Meaning of formal result summary | Acceptable definitional abstraction within K's byte-string theory; loop claim connects it to exact execution. It does not repair the Python/K string mismatch. |
| Manually installed priority-30 loop lemma | Entry proof | Exact instance of the separately reconstructed successful loop claim; context and cells are contained. |
| 846-input Python differential test | Submitted-Python to canonical/contract bridge | Strong finite evidence only, not a universal proof. It includes Unicode and supports the Python implementation, while exposing no implementation defect. |
| Five concrete Python/K comparisons | Generated-semantics adequacy | Finite evidence; one explicit Unicode mismatch is sufficient to refute the claimed universal Python bridge. |
| Informal termination argument | Use of a reachability result as an accelerating loop rule | The target loop terminates because an integer starts at 1, increases by 1, and is bounded by finite K length. The requested theorem is partial correctness in any event. |

### Gate results and decision

- Real-program soundness (Gate A): **FAIL**. R19 and R21 enable concrete false
  results for valid Python `str` input `"🙂x"`.
- Intent adequacy (Gate B): **FAIL**. The natural contract is over Python
  strings, not byte-prefix strings.
- Trust/evidence auditability (Gate C): **PASS for the reconstructed audit
  record**. Exact sources, commands, statuses, positive results, mutation
  residual, and counterexample are preserved.

Clean `#Top`, exact program pinning, and non-vacuity cannot compensate for a
materially unsound generated semantics. The candidate proves the behavior of a
different byte-string program and is therefore not a legitimate proof of the
real generated Python program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
