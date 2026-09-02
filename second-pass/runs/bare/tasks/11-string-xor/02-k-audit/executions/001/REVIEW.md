# Independent adversarial review: 11-string-xor

## Executive decision

The candidate's positive K runs reconstruct cleanly, the claims are
result-constraining, the embedded program is the submitted translated program,
and a fresh false-result mutation is rejected. Those facts are necessary but
not sufficient.

The proof is not legitimate. Its closure depends on three priority-40 rules in
`/candidate/verification.k` that intercept
`exec(solutionBody, ...)` and directly assert the same base/base/recursive XOR
recurrence used by the postcondition. The submitted program body is present in
the rules' pattern, but the proof never establishes—under the unextended
semantics—that executing that body has the asserted transition. There is no
candidate connection claim or derivation. This is an answer-bearing
operational bridge, not a low-level primitive. The successful `#Top` is
therefore conditional on the central correctness step that needed proof.

I found no concrete false instance of those bridges on the intended finite
bit-string domain: their guards are disjoint, their equations agree with a
manual one-unfold analysis, and fresh ground fixed-versus-extended tests agree.
Accordingly, I do **not** call the bridge equations semantically false. The
decisive defect is narrower: the candidate assumes the theorem's
result-bearing execution summary as a high-priority proof rule, with no
universal connection proof. Finite tests cannot fill that gap.

There is also an independent real-Python adequacy problem. At a valid
1,100-bit input, the trusted canonical implementation returns a 1,100-bit
answer while `solution.py` raises `RecursionError`. The generated semantics has
no recursion-depth or exception state and instead models ideal unbounded
recursion.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as required. There is no mount
contradiction and hence no infrastructure breach. I did not infer or use a
hidden semantics.

Evidence: `/audit-output/evidence/01-provenance.log` (exit 0).

### Required files and trusted comparisons

All of the following candidate artifacts are ordinary, non-symlink regular
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
No required source artifact is missing or mistyped.

The candidate prompt is byte-identical to `/reference/prompt.py`
(SHA-256
`ab1ec5c88f83f3fd16def18381c88b33bd5109b84f05147a54f50f95eca66c89`).
The candidate translator is byte-identical to `/reference/py2mpy.py`
(SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

`PROOF.md` and `spec-vacuity.k` are absent. Neither is a generation
deliverable in this condition, so their absence is not an integrity failure;
it merely provides no candidate-authored validation evidence.

The top-level extras are `__pycache__` plus ten candidate-produced compiled
definition/cache directories. They are not source-integrity failures in
generated-semantics mode. I ignored every one of them and rebuilt from copied
source.

### Untrusted generation claims

I read the four requested claim/provenance files and all 414 records in the
present JSONL trace. The trace has no malformed JSON records. `metrics.json`
claims exit 0 without timeout; `codex-last.txt`, `codex-output.log`, and the
trace's final message claim that `prove.sh` obtained `#Top`. These were treated
only as untrusted claims. The relevant hashes, bounded contents, trace counts,
and complete top-level inventory are in
`/audit-output/evidence/01-provenance.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For binary strings `a` and `b`, return a string whose characters are the
bitwise XOR of corresponding characters. The trusted canonical implementation
uses `zip(a, b)`, so unequal inputs produce `min(len(a), len(b))` output
characters. The prompt example is `010 XOR 110 = 100`. The prompt imposes no
equal-length or maximum-length precondition.

`solution.py` performs the same recurrence:

1. return empty when either input is empty;
2. prepend `0` when the first characters agree, otherwise prepend `1`;
3. recurse on both tails.

For inputs that complete normally within CPython's recursion limit, this
implements the canonical `zip` behavior, including unequal lengths.

### Translation identity

In the clean scratch copy I ran the trusted translator:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands succeeded, and the submitted and regenerated MPY files have the
same SHA-256:
`12e2885fb62759fac0bb88e5430c70c623344ede51ff6d7d063be2ae61454b7e`.
See `/audit-output/evidence/02-translation.log`.

### Independent differential test

`/audit-output/evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch copy of `solution.py`. Its exact
inputs are preserved in
`/audit-output/evidence/differential-inputs.jsonl`. The run covered:

- the prompt example;
- both-empty and each one-sided-empty boundary;
- both first-bit branches;
- both unequal-length directions;
- all 16,129 pairs with lengths 0 through 6;
- 512 deterministic generated pairs with lengths 0 through 96;
- one valid input just beyond the process recursion limit.

The first 16,649 cases had no mismatch. The last case, with both lengths 1,100,
was a material valid-domain divergence: canonical returned 1,100 `1` bits,
while the candidate raised `RecursionError: maximum recursion depth exceeded
in comparison`. The differential command therefore exited 1 by design. See
`/audit-output/evidence/03-differential.log`.

This is an exceptional-behavior divergence rather than a wrong returned
string. It nevertheless shows that the generated semantics' unbounded
recursion is not the behavior of the real Python implementation over the
prompt's unrestricted domain.

## 3. Clean proof reconstruction

I copied only source artifacts into
`/tmp/audit-work/11-string-xor-audit/source`. No candidate-compiled definition,
cache, or bytecode was copied or referenced.

### Concrete semantics

The fresh LLVM build used:

```text
kompile semantic.k --main-module XOR --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/11-string-xor-audit/semantic-llvm-kompiled
```

It exited 0 (`04-kompile-semantic-llvm.log`). Twenty fresh `krun` executions
then compared the K result with both Python implementations over ten normal
and boundary cases. Every case was run twice: once using `empty/cons` texts
and once using the claims' `segment(length, seed(integer))` representation.
All 20 executions exited 0 and matched, including empty inputs, unequal
lengths, both branch outcomes, the prompt example, and a 12-bit case. The
script, concrete input JSON, exact commands, and results are in:

- `/audit-output/evidence/concrete_semantics_test.py`
- `/audit-output/evidence/concrete-semantics-inputs.json`
- `/audit-output/evidence/06-concrete-semantics.log`

The standalone prompt run is also preserved in
`/audit-output/evidence/05-krun-prompt.log`.

### Proof definition and positive claims

The fresh Haskell build used:

```text
kompile verification.k --main-module XOR-VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition /tmp/audit-work/11-string-xor-audit/verification-haskell-kompiled
```

It exited 0 (`07-kompile-verification-haskell.log`). The submitted complete
spec then exited 0 and printed `#Top` (`08-kprove-all.log`).

I also ran each target separately:

- The exact function-entry helper claim alone exited 0 and printed `#Top`
  (`09-kprove-entry-only.log`).
- The end-to-end claim was run with the already separately proved helper
  marked trusted solely for compositional reuse. That run exited 0 and printed
  `#Top` (`10-kprove-end-only.log`). The executable copy is
  `/audit-output/evidence/spec-end-with-proved-helper.k`.

An end-to-end diagnostic with the recursive helper removed was interrupted
after about 16 seconds because it was unrolling recursion; it is recorded as
exit 130 in `10a-diagnostic-end-without-helper-interrupted.log`. This
reviewer-induced diagnostic is not counted as a candidate proof failure.

Thus the clean-reconstruction gate itself passes: every submitted positive
claim closes under the submitted extended theory.

## 4. Adequacy and real-program pinning

### Claim 1: function-entry helper

Precondition in plain language: `N` and `M` are nonnegative; `a` and `b` are
represented by `segment(N,S1)` and `segment(M,S2)`; execution is at the entry
of the exact `solutionBody`; the global `<args>` cell may contain anything.

Postcondition: the computation returns exactly
`str(xorText(N,M,S1,S2))`, preserving the same trailing K continuation. It is
not a free result or a one-way predicate.

### Claim 2: end-to-end theorem

Precondition in plain language: `N` and `M` are nonnegative; the initial
`<args>` cell contains the two segment strings; and `<k>` contains
`solutionProgram`.

Postcondition: the translated module returns exactly the same
`xorText` value, again preserving any framed continuation. At the ordinary
initial configuration that continuation is `.K`.

### Pinning and satisfying state

The reviewer-authored pinning check confirms:

- `solutionProgram` is a macro with exactly one rule;
- `solutionBody` is a macro with exactly one rule;
- after normalizing the explicit `.Stmts` list units, `solutionProgram` is
  exactly the freshly regenerated MPY term;
- wrapping `solutionBody` in the submitted function/module constructors gives
  that same term.

All checks passed in `/audit-output/evidence/11-pinning.log`; the script is
`/audit-output/evidence/pinning_check.py`.

A concrete state satisfying both entry preconditions is:

```text
N = 3, M = 3, S1 = seed(2), S2 = seed(3)
Args(str(segment(3,seed(2))), str(segment(3,seed(3))))
```

This encodes `a="010"` and `b="110"`. Substitution into the postcondition
reduces `xorText(3,3,seed(2),seed(3))` to the text `100`; the ground K check
prints `#Top` in `/audit-output/evidence/12-ground-witness.log`. Both Python
implementations and both concrete K encodings also return `100` in
`06-concrete-semantics.log`.

The claims therefore pin and constrain the submitted MPY term syntactically.
The remaining problem is how its behavior is established.

## 5. Rule-by-rule static soundness review

The complete numbered sources and mechanically checked counts are preserved in
`/audit-output/evidence/13-rule-inventory.log`. There are no generated helper K
source files. There are no local `functional`, `opaque`, or `simplification`
declarations.

### Syntax, configuration, and construct coverage

`MPY-SYNTAX` declares:

- `Module(Stmts)` and the whitespace-separated `Stmts` list;
- `FuncDef`, `Return`, and `If` statements;
- comma-separated parameter strings and `Params`;
- `Name`, `Str`, `Int`, `BinOp`, `Compare`, `Subscript`, and two-argument
  `Call` expressions;
- `CmpOp`, expression indices, the exact `Slice(Expr,NoBound,NoBound)` form,
  and `NoBound`.

Every constructor in `solution.mpy` is declared, and no used constructor is
left to an oracle. The solution uses exactly one function definition,
returns, three one-armed `If` statements, names `a`, `b`, and `string_xor`,
the string literals empty/`0`/`1`, integers 0/1, equality, string
concatenation, index 0, tail slice `[1:]`, and the recursive two-argument call.

`XOR-SEMANTICS` declares:

- streams `seed(Int)` and functional `next(Stream)`;
- total functional `head(Stream)`;
- text `empty`, `cons(Bool,Text)`, and `segment(Int,Stream)`;
- values `str`, `i`, and `truth`;
- the two-argument `Args`, two-binding `Env`, `normal`/`returned` results,
  and the `KResult`/`Sem` subsorts;
- `eval`, `equal`, `concat`, `index`, `tail`, `call`, `returnValue`,
  `makeReturn`, `exec`, `decide`, and `continue`.

The configuration has only `<k>` and `<args>`. That is sufficient for this
pure, local program; there is no assignment, heap, allocation, I/O, or mutable
global state to model.

Strictness declarations impose evaluation of all equality/concatenation/index
operands, the tail operand, call arguments 1 then 2, return operands, and
control conditions. Python's full evaluation/exception machinery is not
modeled. On the tested pure, nonempty guarded paths, no evaluation-order
counterexample exists; recursion-depth exceptions are a separate documented
gap.

`XOR-VERIFICATION` adds the two exact AST macros, functional `xorText`, and
strict `prependResult`. The only local priority attributes are the three
priority-40 execution bridges discussed below.

### All 35 rules in `semantic.k`

| Rules | Decision |
|---|---|
| `head(seed(I))` and `next(seed(I))` (lines 64–65) | Valid definitions of the least-significant-bit stream representation. Every ground `Stream` term normalizes through `next` to a `seed`. `head` is result-bearing but not unconstrained on ground terms. |
| Module/function entry (71–73) | Valid for the only accepted module: it binds the two supplied values to `a` and `b` and retains the exact body for recursive calls. It deliberately models no general Python name lookup. |
| Name/literal evaluation (75–80) | The six rules correctly implement the two bound names, the only three string literals, and integer literals used by the program. Their deliberately narrow literal/name coverage is acceptable because no other cases are used. |
| Composite evaluation (82–91) | The five rules map exactly the used equality, `+`, integer index, `[1:]` slice, and recursive `string_xor` call into semantic operations. The call rule pins the textual function name and threads the current body. |
| Equality (93–99) | The six rules correctly distinguish empty from concrete nonempty texts, interpret a segment as empty iff its length is zero, and compare the singleton texts produced by index 0. These rules are sufficient for every equality reached by this program. There is no harmful overlap: `empty`, `cons`, and `segment` are distinct constructors. |
| Concatenation (101) | Correct for the only reached form: a one-character literal on the left, prepended to the recursive text. |
| Index (102–104) | Correct for index 0 on a concrete nonempty text or a positive-length segment. The positive guard prevents fabricating a character from an empty segment. |
| Tail (105–107) | Correct for concrete cons text and for a positive-length segment; the latter decrements length and advances the stream. |
| Call and return-value extraction (109–110) | Correct for this closed subset: the evaluated argument values are bound in a fresh term-local environment and a returned value is extracted. It does not model Python stack depth or exceptions. |
| Empty execution, `Return`, and `If` (112–115) | Correct statement sequencing: empty statements finish normally, a return discards the remaining same-body statements, and an `If` evaluates its condition before choosing a branch. |
| Boolean branch choice (116–121) | The true and false guards are disjoint and exhaustive once a `truth(Bool)` is reached. |
| Return construction and continuation (122–124) | Correctly constructs a returned result, propagates it out of an `If`, and resumes the remaining statements only after a normal branch completion. |

No semantic rule silently fabricates a used source construct. The concrete
tests exercise every rule family reached by the program.

The material language-model mismatch is not a single false guarded equation
inside this abstract machine; it is omitted runtime state. Together, the
unbounded `call/exec` model permits a normal 1,100-character result, while the
real CPython witness raises `RecursionError`
(`/audit-output/evidence/03-differential.log`). That concrete witness prevents
treating the generated semantics as a complete model of the unrestricted
Python contract.

### All nine rules in `verification.k`

| Rule | Decision |
|---|---|
| `solutionProgram` macro rule (10–38) | Truthful syntactic abbreviation. Independent normalization pins it to regenerated `solution.mpy`. |
| `solutionBody` macro rule (42–68) | Truthful syntactic abbreviation of the exact function body. |
| Three `xorText` equations (73–80) | Mathematically correct: stop when `N=0`, stop when `N>0` and `M=0`, otherwise prepend the XOR of the two heads and decrement both lengths. Under `N,M >= 0` the guards are disjoint, exhaustive, and recursively descending. The result length is `min(N,M)`. |
| `prependResult` (87) | Correctly prepends a bit after a recursive call returns a string. Its only reached argument form is covered. |
| Priority bridge for `N=0` (89–94) | A static one-step analysis of the base semantics agrees: the first empty check returns empty. Its guard is disjoint from the other bridge guards. |
| Priority bridge for `N>0, M=0` (96–101) | A static one-step analysis agrees: the first empty check is false and the second returns empty. Its guard is disjoint. |
| Priority bridge for `N>0, M>0` (103–113) | Its value is extensionally consistent with the body: both emptiness tests are false, the indexed heads select `0` iff equal and `1` otherwise, tails decrement/advance both segments, and the recursive result is prepended. However, this is precisely the theorem's induction step, installed as an ordinary high-priority operational axiom. |

The three bridge rules overlap the ordinary `exec(If(...) REST,...)` rule and
priority 40 makes the bridge win. They read no cells, write no cells, and
return the same pure term shape on the ground cases tested. The LHS includes
both the exact active body and the exact recursive-body argument, so it does
not match an unrelated function body.

I tested all three guard regions in a continuation context:

```text
exec(solutionBody, ...) ~> observe
```

Fresh bridge-free and bridge-extended LLVM definitions reached identical
`observed(...)` configurations in all three cases. The definitions, script,
commands, and exit-0 log are:

- `/audit-output/evidence/bridge-context-fixed.k`
- `/audit-output/evidence/bridge-context-extended.k`
- `/audit-output/evidence/bridge_context_test.py`
- `/audit-output/evidence/18-bridge-context.log`

These tests support binding, value, state-footprint, and continuation fidelity
for the tested witnesses. They are finite evidence.

The candidate contains no fixed-semantics auxiliary claim proving any bridge
over its complete symbolic guard. Removing all three bridges yields a fresh
definition that compiles (`14-kompile-no-bridges.log`), but a reviewer
diagnostic of the full recursive theorem produced no result in approximately
60 seconds and was interrupted (`15-kprove-no-bridges.log`). That interruption
is not a proof failure and is not used as one. It simply supplies no missing
connection theorem.

Most importantly, bridge 3 states the exact result-bearing XOR recurrence
that `xorText` states, while bridges 1 and 2 state its base cases. The positive
proof can therefore close by matching those asserted recurrences rather than
deriving them from the AST evaluator. The exact body in the pattern provides
syntactic sensitivity but does not prove the body-to-summary connection.
Per the required proof-extension boundary, this is a smuggled correctness
conclusion.

Because the static and finite evidence found no false bridge instance, I make
no claim that these three equations enable a known false result on an intended
finite input. The narrower, decisive finding is that they are unproved
answer-bearing operational assumptions. Accepting them would make any
analogously asserted recurrence a “proof” after only changing the summary and
bridge together.

### The two claims in `spec.k`

Both claim preconditions are satisfiable and cover all nonnegative lengths.
Both postconditions are exact equalities in the rewritten `<k>` content. The
entry helper follows the same recursive shape as the three bridges; the
end-to-end claim first expands the exact program and then uses that helper.
There is no tautology, unconstrained result variable, or implication-only
postcondition.

## 6. Fresh non-vacuity test

The fresh mutation is
`/audit-output/evidence/spec-false-result-mutation.k`. It changes the helper
postcondition from:

```text
returned(str(xorText(N,M,S1,S2)))
```

to the false:

```text
returned(str(cons(true,xorText(N,M,S1,S2))))
```

At the satisfying witness `N=0, M=0`, real execution returns empty while the
mutation demands one leading bit. The same contradiction also holds for the
residual branch shown by the prover, `N>0, M=0`.

The mutation's dry run exited 0 and emitted a valid `kore-exec` command
(`/audit-output/evidence/19-false-mutation-build.log`), proving that the
artifact builds. The actual proof exited 1 with `WarnStuckClaimState`; its
residual contains `returned(str(empty))`, `M = 0`, `N > 0`, and cannot unify
with the demanded result
(`/audit-output/evidence/20-false-mutation-proof.log`). This is a meaningful
unmet result obligation, not a parse error, missing import, timeout, or
unreachable mutation.

The non-vacuity gate passes.

## 7. Proven versus assumed accounting

### What `#Top` establishes

Under the candidate's extended K theory—including all three priority-40
execution bridges—the following partial-correctness statement closes:

> For nonnegative segment lengths `N` and `M`, execution of the exact embedded
> translated module, or entry at its exact body, reaches a returned text
> described by `xorText(N,M,S1,S2)`, with the framed continuation preserved.

That statement is result-constraining and discriminating. It is not,
however, an unconditional theorem of the generated base semantics, because
the body-to-`xorText` induction step is among the assumed rewrite rules.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, LLVM/Haskell backends, reachability engine, built-in Bool/Int/String/List operations | All builds and proofs | Ordinary toolchain trust; acceptable and freshly exercised. |
| Trusted `/reference/py2mpy.py` | MPY identity | Acceptable. Byte identity was independently checked. |
| `seed/head/next` stream representation | Segment execution, `xorText`, claims | Explicit and ground-reducible; concrete segment tests support it. |
| The 35 generated semantic rules | Meaning of `solution.mpy` | Adequate for the constructs used by ordinary finite executions; minimal unused-language coverage is not required. It omits CPython recursion-depth/exception behavior. |
| Exact `solutionProgram` and `solutionBody` macros | Both claims and bridges | Acceptable syntactic abbreviation, independently pinned. |
| Three `xorText` equations | Formal result | Explicit, disjoint, descending mathematical definition; acceptable. The bridge from this definition to the prompt's characterwise XOR is supported by its equations and finite differential evidence. |
| Three priority-40 `exec(solutionBody,...)` rules | Closure of the helper and end-to-end claims | **Illegitimate proof boundary.** They replace the property-bearing program execution with the desired recurrence, and no candidate universal connection proof derives them from fixed semantics. |
| Differential testing | Python implementation-to-canonical bridge | Finite evidence only. It strongly supports small/medium inputs but exposes the 1,100-character recursion exception. |
| Concrete `krun` and bridge-context tests | Generated semantics and bridge witnesses | Finite evidence only; cannot substitute for the missing universal bridge proof. |

There are no declared local opaque symbols. Symbolic `head(S)` can remain
unreduced for a stream variable, but its interpretation is used consistently
and every ground stream term reduces through `seed/next`; it is not an
unconstrained program-result oracle. There is no heap, state mutation,
allocation, output, or exception cell hidden by the bridges.

### Gate summary

- Real-program soundness: **FAIL**. Clean closure relies on unproved,
  answer-bearing operational bridges that preempt execution of the exact body.
- Intent adequacy: **FAIL independently for the unrestricted Python
  contract** because the 1,100-character valid input raises `RecursionError`
  while the K language model has no such behavior. For normally returning
  smaller inputs, the implementation, canonical result, and K executions
  agree in the recorded sample.
- Trust/evidence auditability: the reviewer evidence is reproducible and
  bounded, but finite testing does not repair the first gate.

The successful rebuild and non-vacuity test rule out a missing or vacuous
proof. They do not overcome the assumed correctness recurrence. The candidate
therefore does not contain a legitimate partial-correctness proof of the real
generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
