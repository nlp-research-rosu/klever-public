# Independent adversarial audit: 28-concatenate

The candidate contains a legitimate, result-constraining K reachability proof
of the submitted generated program over arbitrary finite lists of modeled
strings. I reconstructed both proof targets from source, checked exact
constructor-level program pinning, audited every local rule, and obtained the
expected rejection of two independent false mutations.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
generated semantics takes K's backend-hooked `String`/`+String` as the bridge to
Python `str` without a universal connection theorem. K's own bundled
documentation warns that its Unicode string implementation is incomplete
beyond Latin-1, although the used concatenation operation succeeded on the
audited Unicode cases. In addition, K rejects lone-surrogate input escapes that
CPython can store in a `str`. This is a non-fatal representation/trust-boundary
limitation, not evidence of an incorrect result on the material ordinary
`List[str]` domain. I found no false-rule witness reachable from the fixed
submitted program on that domain.

## 1. Input and provenance integrity

`/audit-input.json` is a regular read-only file declaring:

- problem `28-concatenate`;
- condition `bare`;
- record layout `legacy-selected-stage1`; and
- semantics mode `GENERATED_SEMANTICS`.

The complete independent check is recorded in
`evidence/provenance_check.py` and `evidence/provenance.log`.

The `audit_campaign` object in `/audit-input.json` equals the parsed contents of
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the launcher-recorded hash.

All records required for `legacy-selected-stage1` are present, readable, and
of the required regular-file or real-directory type:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`

`/generation-evidence/usage.json` is also present and was inspected.
`runtime-metrics.json` is absent, but it is not required by this historical
layout and was not reconstructed.

Every launcher-recorded direct file hash matches the mounted file, including
the run/task/result manifests, invocation and metrics, usage, prompt,
generation output, last message, trusted prompt, trusted translator, and
canonical implementation. Every evidence hash listed by both
`generation-result.json` and `invocation.json` also matches, including the
single structured trace JSONL.

An independently implemented path/type/size/content tree digest of
`/candidate` is
`ed27e8d459b7d9d8b8c73325ef522dc9ba74a54451e4f32cd37e06410244c1e3`.
It matches both the result's workspace digest and the invocation's retained
workspace digest. The corresponding trace-tree digest is
`376c250ce842042db51f657d6d298459bc41a9e00bf82f13719dc1e3cb6c9438`
and matches `usage.json`'s source-trace digest. The audit-input also records
secondary tree hashes without specifying their encoding; I did not substitute
those for the independently reproducible content-tree and per-file checks.

The trace contains one regular JSONL file, 259 valid JSON records, and no
malformed lines. I read the complete generation output and structured trace
through the bounded extractor in `evidence/trace_digest.py`; relevant claims,
commands, failures, later successful `#Top` outputs, and the final report are
preserved in `evidence/trace-digest.log`. They were treated only as historical
claims and not as proof evidence.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. No symlink occurs anywhere
under the candidate, reference, or generation-evidence trees. All required
candidate proof sources (`solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and executable `prove.sh`) are present.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist. I did not infer or use a
hidden reference semantics.

Stage 1 result: PASS; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `concatenate(strings: List[str]) -> str` to return
the input strings concatenated in list order. The empty list returns `""`;
`["a", "b", "c"]` returns `"abc"`. The trusted canonical implementation is
`return ''.join(strings)`.

The candidate uses an equivalent left fold:

1. initialize `result = ""`;
2. iterate over every `string` in order;
3. set `result = result + string`; and
4. return `result`.

There is one control boundary: zero loop iterations versus one or more. There
is no fixed input-size bound.

I regenerated the MPY constructor tree with the trusted translator:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/28-concatenate-audit/solution.py \
  > /tmp/audit-work/28-concatenate-audit/solution.regenerated.mpy
```

`cmp` exited 0. Both submitted and regenerated files have SHA-256
`6a7ae3bc549d9525bebb62f6f7779f4b9a28a4436c1518942ce3a5adfbc65f89`.
See `evidence/translator-regeneration.log`.

The independent differential test is
`evidence/differential.py`, with its exact run in
`evidence/differential.log`. It imports the trusted canonical and candidate
entry points separately. It covers:

- the two documented examples;
- empty, singleton, and multi-element loop boundaries;
- empty components, whitespace, quotes, backslashes, newlines, and NULs;
- Latin-1, Greek, and supplementary-plane characters;
- a 1,024-character component and a 1,000-element list; and
- 528 seeded generated lists, with lengths 0 through 32 and component lengths
  0 through 32.

There were 541 total comparisons and zero mismatches. This is finite fidelity
evidence, not a universal proof.

Stage 2 result: PASS.

## 3. Clean proof reconstruction

I copied only candidate source artifacts and trusted reference inputs into
`/tmp/audit-work/28-concatenate-audit`. I did not copy or reuse any compiled
definition. `evidence/scratch-source-hashes.log` confirms that the semantic,
verification, and spec sources in scratch are byte-identical to the candidate,
that no candidate-named `semantic-kompiled` directory was present, and that
the concrete and proof definitions were newly created.

The observed toolchain was K `v7.1.293` and Python `3.10.12`
(`evidence/toolchain.log`).

Fresh concrete definition:

```text
kompile semantic.k --backend llvm \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

Exit 0; see `evidence/kompile-llvm.log`.

Fresh proof definition:

```text
kompile semantic.k --backend haskell \
  --main-module MPY-SEMANTICS \
  --syntax-module MPY-SYNTAX \
  --output-definition proof-kompiled
```

Exit 0; see `evidence/kompile-haskell.log`.

Fresh LLVM executions consumed the entire computation and restored all
call-local cells. Their result cells were:

| Input | K result |
|---|---|
| `[]` | `sVal("")` |
| `[""]` | `sVal("")` |
| `["a","b","c"]` | `sVal("abc")` |
| `["","hello",""," world"]` | `sVal("hello world")` |
| `["é","λ","🙂"]` | the K printer's escaped representation of their concatenation |
| `["a\0b","\0","c"]` | `sVal("a\0b\0c")` |
| `["🙂","x"]` using a supplementary escape | the escaped representation followed by `x` |

The exact K commands and full final configurations are in
`evidence/krun-empty.log`, `krun-singleton-empty.log`, `krun-abc.log`,
`krun-empty-components.log`, `krun-unicode.log`, `krun-nul.log`, and
`krun-supplementary-escape.log`. The independently executed Python values for
the shared cases are in `evidence/concrete-expectations.log` and agree.

Both positive target-proof commands were rerun independently:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --claims SPEC.concatenate-loop
#Top
EXIT_STATUS: 0

kprove spec.k --definition proof-kompiled --spec-module SPEC \
  --trusted SPEC.concatenate-loop
#Top
EXIT_STATUS: 0
```

See `evidence/kprove-loop.log` and `evidence/kprove-end-to-end.log`. The second
command treats the loop claim as a modular lemma, but that exact claim was
first proved against the same fresh definition and unchanged source. I do not
treat `--trusted` alone as proof of the lemma.

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claim `concatenate-loop`

Precondition in plain language: the machine is at the exact loop used by the
submitted function, with an arbitrary finite remaining `StrList` called
`ITEMS`, accumulator string `ACC`, no published result, and the exact suffix
`Return(Name("result")) ~> cleanup`. The saved function, original argument,
and prior iteration item may have any correctly sorted values.

Postcondition: all computation is consumed, the call-local cells are reset,
and the published result is exactly `concatAcc(ACC, ITEMS)`.

This is not a general oracle rule. It is a reachability claim whose inductive
step executes the real bind, loop body, lookup, left-to-right addition,
assignment, and recursive loop transition before circular reuse.

### Claim `concatenate-correct`

Precondition in plain language: start from the initialized configuration, load
the exact submitted module, and invoke `concatenate` with any finite
`INPUT:StrList`. There is no size, length, character, or example restriction.

Postcondition: execution reaches `.K`, local cells are restored, and the
published result is exactly `sVal(concatAcc("", INPUT))`.

The result is not a free RHS variable, existential, implication-only
condition, or tautology.

Mechanical program pinning is in `evidence/program_pinning.py` and
`evidence/program-pinning.log`. A lexical constructor comparison found 73
tokens in both the submitted `solution.mpy` and the entry claim's `load`
argument, with token-for-token equality. This includes the typing import,
function name, `"strings"` binding, initializer, loop target and iterable,
addition operand order, assignment target, and return expression. Together
with trusted regeneration, this pins the claim to the real generated program.

Both claim preconditions are inhabited. `evidence/claim-witnesses.k` uses:

- loop witness `ACC = "a"`, `ITEMS = ["b","c"]`, empty saved argument, and
  prior current item `""`, producing `"abc"`; and
- entry witness `INPUT = ["a","b","c"]`, producing `"abc"`.

The ground witness proof prints `#Top` and exits 0
(`evidence/claim-witnesses.log`). Both Python implementations also produce
`"abc"` for the entry witness.

Program-body sensitivity was tested separately from postcondition mutation.
`evidence/spec-body-mutation.k` changes the initializer in the constructor term
actually executed by the entry claim from `Str("")` to `Str("!")`, while
retaining the original postcondition. It parses successfully
(`evidence/body-mutation-dry-run.log`) and is rejected with
`WarnStuckClaimState`; the residual requires the false equality
`concatAcc("", INPUT) = concatAcc("!", INPUT)`
(`evidence/body-mutation-proof.log`). Empty input is an immediate concrete
counterexample to the mutation.

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

`evidence/rule-inventory.md` is the exhaustive inventory. It lists all 32
local syntax productions, the six-cell configuration, all 24 ordinary
operational rules, both `concatAcc` equations, and both reachability claims,
with source locations, state footprints, used-construct mapping, and
soundness judgment.

The operational rules divide as follows:

- R1-R6: module loading and ordered statement sequencing;
- R7: exact single-function binding and invocation;
- R8-R16: literal/name evaluation, RHS-before-store assignment, and
  left-before-right string addition;
- R17-R21: iterable evaluation, empty/cons loop cases, left-to-right traversal,
  and loop-variable binding; and
- R22-R24: return-expression evaluation, result publication, and cleanup.

Every constructor in `solution.mpy` maps to a declaration and applicable rule.
The loop consumes one finite `StrList` constructor per iteration. The addition
continuations preserve Python operand order. The invocation rule matches the
stored function name, the `"strings"` formal parameter, its exact body, and the
argument. There is no heap, allocation, I/O, exception, or external state
operation in the submitted function on ordinary `list[str]` inputs.

Rule matches are deterministic on the used terms. Empty and cons list cases
are disjoint; literal-name lookup rules are disjoint; continuation rules have
distinct constructors/sorts. There are no local priority, `owise`, `total`,
`functional`, `simplification`, `concrete`, or opaque declarations. No rule
encodes the expected answer or replaces a program-defined computation with a
fresh value.

The two proof-local equations are a definitional summary:

```text
concatAcc(ACC, .StrList) = ACC
concatAcc(ACC, S :: REST) = concatAcc(ACC +String S, REST)
```

Their constructor domains are disjoint and exhaustive, the recursive call
strictly decreases the list tail, and their value is exactly the accumulator
transition the operational rules execute. `concatAcc` appears only in claim
results; it does not preempt execution.

Two source rules are intentionally broader than their justification as a
general Python semantics:

- R4 erases every `ImportFrom`, although, for example,
  `from definitely_missing import x` would raise `ImportError`.
- R22 does not implement abrupt unwinding for an arbitrary statement after a
  `Return`; a body `Return(Str("x")) Assign(...)` would be observably different
  in Python.

These are concrete outside-scope behavior witnesses, so I do not call the
rules a full Python semantics. They do not yield a false conclusion for the
intended theorem: the pinned import is the unused typing-only import, and the
pinned return is the last statement with the exact empty-list/cleanup suffix.
No entry input can alter those fixed contexts. Under the prompt's generated
semantics boundary, missing behavior for unused constructs is permitted; the
over-breadth remains a non-fatal maintenance concern.

The only result-bearing primitive is imported K `STRING.concat` (`+String`).
It is not program-derived and is not an opaque candidate symbol. The theorem
is conditional on this standard builtin having the intended string
concatenation meaning.

Stage 5 result: PASS for the pinned program; documented limitations prevent
claiming a reusable Python semantics.

## 6. Fresh non-vacuity test

I did not rely on any candidate vacuity artifact. The fresh mutation is
`evidence/spec-vacuity-audit.k`. It executes the exact program from the normal
initialized state on satisfying input `[]`, but changes the result obligation
from `sVal("")` to the demonstrably false `sVal("!")`.

Python independently returns `""` and rejects equality with `"!"`
(`evidence/vacuity-witness-python.log`).

The mutated spec parses and compiles to KORE:

```text
kprove spec-vacuity-audit.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
EXIT_STATUS: 0
```

The actual proof exits 1 with `WarnStuckClaimState`. Its reachable residual has
`.K`, reset local cells, and `<result> sVal("") </result>`, which cannot unify
with the demanded `"!"`. See `evidence/vacuity-dry-run.log` and
`evidence/vacuity-proof.log`.

This is an expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated backend failure.

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Precisely proven

Under the fresh K definition, for every finite `INPUT:StrList`, the exact
constructor tree regenerated from the submitted `solution.py` executes to
completion and publishes:

```text
sVal(concatAcc("", INPUT))
```

while consuming `<k>` and resetting the function, argument, accumulator, and
iteration-item cells. The separately proved loop claim establishes the same
fact from any accumulator and finite remaining list. This is at least partial
correctness and, within the modeled finite-term domain, also establishes
termination of the modeled execution.

Because `concatAcc` is the recursive left-to-right definition of concatenating
the list, the postcondition captures the natural-language property directly.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, reachability logic, and guarded circularity | All execution and proof closure | Standard unavoidable toolchain trust; exact versions and fresh commands recorded |
| K `String` carrier and total hooked `+String` | Every component and final value | Acceptable low-level primitive, but the Python-to-K Unicode representation is not universally proved |
| Trusted `py2mpy.py` | Source-to-constructor identity | Mechanically regenerated byte-for-byte; not assumed from candidate prose |
| Token-level comparison of `solution.mpy` to the claim | Real-program pinning | Mechanical finite check; exact equality obtained |
| Interpretation of `concatAcc` as list concatenation and equivalence to canonical `''.join` | Human-facing intent bridge | Direct structural definition plus 541 zero-mismatch differential cases; the tests alone are not a universal proof |
| Minimal generated language model | Binding, control, and state fidelity | Exhaustively audited for every used construct; not claimed as general Python |
| Ordinary built-in `list[str]` values and absence of resource exhaustion | Source execution model | Consistent with HumanEval typing and partial-correctness practice; custom object protocols and memory failures are outside scope |

There are no candidate opaque symbols, unconstrained fresh results, empirical
oracles inside K, assumed program-defined helpers, proof-local operational
bridges, or unproved simplification lemmas.

### Non-fatal concern behind the verdict

The bundled K documentation, preserved in `evidence/k-string-model.log`,
describes `String` as a Unicode-string implementation but warns that encoding
and code-point support beyond Latin-1 is incomplete. Concrete K executions
successfully handled the Greek, emoji, NUL, and supplementary-escape cases
used here. A lone-surrogate K escape, however, is rejected by the scanner
(`evidence/krun-surrogate.log`), while CPython can store and concatenate such a
`str`.

This does not falsify the reachability theorem, which quantifies over K
`String`, and it does not materially restrict normal Unicode-scalar
HumanEval inputs. It does prevent an unqualified claim that the semantics is a
fully formal model of every exotic CPython `str` representation. Per the
benchmark decision boundary, that is a legitimate proof with a documented
trust/evidence limitation, not a materially bounded or substituted-program
proof.

Gate summary:

- Gate A, real-program soundness and non-vacuity: PASS.
- Gate B, intent adequacy over the material `List[str]` domain: PASS, with the
  exotic-string representation limitation above.
- Gate C, reproducible evidence and explicit trust accounting: PASS.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
