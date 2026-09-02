# Independent adversarial audit: 131-digits

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program for the stated domain of positive
integers. The proof was reconstructed from source with K v7.1.293, both claims
closed, the closed proof-side program was pinned to a trusted regeneration of
`solution.mpy`, and a fresh false-result mutation was rejected for the expected
reason.

The verdict is `CONCERNS / LEGIT`, rather than `PASS`, because this is an
individually generated minimal Python semantics, not a supplied or
machine-verified Python semantics. Its correspondence to Python is established
by exhaustive source-rule review plus finite execution evidence. In addition,
the locally declared `%` and `//` rules are broader than the theorem needs and
do not model Python correctly for negative operands. No negative operand is
reachable from the entry precondition `N > 0`, so this limitation cannot make a
false conclusion provable on the intended domain and is not a legitimacy
failure.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree. `/reference` contains exactly the
three expected regular files:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` does not exist and is not a symlink. Therefore
there is no infrastructure contradiction and no hidden reference semantics was
used.

All required candidate deliverables and audit-record inputs are present as
regular files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, one structured JSONL trace, `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. There are no symlinks anywhere under `/candidate`. The candidate
also contains compiled definitions and a Python cache; those are untrusted
extra build outputs, not source-integrity defects, and none was copied into or
used by the audit reconstruction.

The candidate prompt and translator are byte-identical to their trusted
mounts:

| Artifact | Trusted and candidate SHA-256 | `cmp` |
|---|---|---|
| `prompt.py` | `4a1c555a3cd7fb8a1b3a2786b00cb13d927f9a5509630d781ee1e2e0fdd8767c` | exit 0 |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | exit 0 |

The metadata, prose, logs, and trace were inspected only as untrusted claims.
They claim a successful prior run, but no conclusion below relies on that
claim. Exact inventory, hashes, metadata boundaries, commands, and statuses are
in [01_provenance.log](evidence/01_provenance.log), produced by
[01_provenance.sh](evidence/01_provenance.sh).

Stage 1 result: pass.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every positive integer `n`, return the product of its odd base-10 digits.
Return zero when no odd digit occurs. The trusted examples are `digits(1) = 1`,
`digits(4) = 0`, and `digits(235) = 15`.

The trusted canonical program converts `n` to decimal text, scans digits from
most significant to least significant, counts odd digits, and multiplies them.
The submitted `solution.py` repeatedly takes `n % 10` and `n // 10`, so it
scans the same digits in the opposite order. Its accumulator uses zero as the
“no odd digit yet” sentinel. A decimal odd digit is one of
`{1,3,5,7,9}`, hence never zero; after the first odd digit the accumulator is
nonzero. Because integer multiplication is associative and commutative, the
opposite scan order returns the same product. If every digit is even, the
sentinel remains zero.

### Trusted regeneration

The audit copied source files only to `/tmp/audit-work/131-digits` and ran:

```text
python3 /reference/py2mpy.py /tmp/audit-work/131-digits/solution.py \
  > /tmp/audit-work/131-digits/solution.regenerated.mpy
```

The command exited 0. Submitted and regenerated trees both have SHA-256
`2896980468c0242ec42a548502e6d02a49ccf9d6e86596c4a0483aa950519b80`,
and `cmp -s` exited 0. The preserved trusted regeneration is
[02_solution_regenerated.mpy](evidence/02_solution_regenerated.mpy).

### Independent differential run

[02_differential.py](evidence/02_differential.py) independently loads
`/reference/canonical.py:digits` and the scratch copy of the generated
`solution.py:digits`. It covers:

- all three documented examples;
- zero as an explicitly out-of-domain, zero-iteration boundary;
- branch boundaries for zero/one/multiple loop iterations, even/odd digits,
  first/subsequent odd digits, embedded zeroes, and all-even inputs;
- every integer from 1 through 10,000;
- powers of ten, one-less-than-powers of ten, and repeated-digit values through
  100 decimal digits; and
- 500 deterministic random positive integers of 1–100 decimal digits using
  seed 131.

The run performed 10,845 checks, found zero return/exception mismatches, and
exited 0. The full random input list, group definitions, samples, command, and
status are in [02_program_fidelity.log](evidence/02_program_fidelity.log);
the driver is [02_program_fidelity.sh](evidence/02_program_fidelity.sh).
This is finite evidence, not a universal proof.

Stage 2 result: pass.

## 3. Clean proof reconstruction

Only candidate source and the trusted inputs were copied. Candidate
`semantic-kompiled`, `verification-kompiled`, caches, traces, and Python bytecode
were excluded. K reported version v7.1.293.

### Fresh concrete definition

The audit ran:

```text
kompile /tmp/audit-work/131-digits/semantic.k \
  --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --backend llvm \
  --output-definition /tmp/audit-work/131-digits/semantic-fresh-kompiled
```

It exited 0. Fresh `krun` executions of the trusted-regenerated program were
compared with separately executed canonical and generated Python functions for
`0, 1, 4, 10, 11, 22, 235, 2468, 10203, 13579`, and a 40-digit all-ones
integer. Every `krun` command exited 0 and every answer matched. These cases
exercise zero iterations, the smallest positive input, even-only inputs, first
and repeated odd digits, embedded zeroes, multiple loop iterations, and a large
integer. Complete configurations and comparisons are in
[03_rebuild_and_prove.log](evidence/03_rebuild_and_prove.log).

### Fresh proof definition and positive claims

The audit ran:

```text
kompile /tmp/audit-work/131-digits/verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --backend haskell \
  --output-definition /tmp/audit-work/131-digits/verification-fresh-kompiled
```

It exited 0. The exact submitted specification then produced:

```text
timeout 300s kprove /tmp/audit-work/131-digits/spec.k \
  --definition /tmp/audit-work/131-digits/verification-fresh-kompiled \
  --spec-module SPEC
#Top
[exit 0]
```

For independent claim accounting, the audit made
[03_spec_labeled.k](evidence/03_spec_labeled.k), which differs semantically only
by module/claim labels. The loop theorem alone exited 0 with `#Top`. The entry
theorem depends on that loop theorem, so a modular run retained both claims,
marked only the already independently proved loop theorem trusted for that
invocation, and discharged the remaining entry obligation:

```text
timeout 300s kprove .../03_spec_labeled.k \
  --definition .../verification-fresh-kompiled \
  --spec-module SPEC-LABELED \
  --claims SPEC-LABELED.entry-contract,SPEC-LABELED.loop-invariant \
  --trusted SPEC-LABELED.loop-invariant
#Top
[exit 0]
```

All completed positive commands and statuses are in
[03b_proof_targets.log](evidence/03b_proof_targets.log). An earlier exploratory
selection filtered out the needed loop theorem and was interrupted rather than
misreported as a candidate failure; it is fully disclosed in
[03_filtered_entry_diagnostic.md](evidence/03_filtered_entry_diagnostic.md).

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim says: from the exact submitted loop head, for any nonnegative
remaining `N`, any current accumulator `A`, any scratch digit `D`, any answer
cell, and any continuation `CONT`, running the loop consumes exactly the loop,
preserves `CONT` and the answer, sets `n` to zero, extends `A` with all odd
decimal digits of `N`, and records the last processed digit in the scratch
cell.

The entry claim says: for every positive `N`, start with the standard empty
state and invoke the exact closed `digits` program. If execution terminates, it
consumes the whole computation, leaves `n = 0`, puts `oddProduct(N)` in both the
accumulator and observable answer, and gives the exact final scratch digit.
The result is an explicit function of the input; it is neither a fresh
variable, a tautology, nor a one-way implication.

### Satisfiable witnesses

For the loop claim, the concrete configuration with
`N=235, A=0, D=0, CONT=.K, answer=.K` satisfies `N >= 0`. It terminates with
`n=0`, accumulator 15, and scratch digit 2.

For the entry claim, the standard configuration with `N=235` satisfies
`N > 0`. Both trusted canonical Python and generated Python return 15.

[04_ground_witnesses.k](evidence/04_ground_witnesses.k) removes symbolic
summaries from these two concrete obligations. The loop-235 and entry-235
ground executions each proved directly under the rebuilt definition with exit
0 and `#Top`; no symbolic loop claim was present in that file. Commands and
outputs are in
[04_adequacy_and_pinning.log](evidence/04_adequacy_and_pinning.log).

### Actual-program identity and sensitivity

`SolutionProgram` is a constructor macro, not a substituted algorithm. The
proof definition's sound reflexive rule `CheckProgram(P,P) => ProgramsMatch`
was run against the trusted-regenerated `solution.mpy`; `krun` exited 0 and
reached `ProgramsMatch`.

The audit then changed the source body from `n % 10` to `n % 11`, regenerated
that mutated source with the trusted translator, and reran the same structural
check. It stopped with both distinct constructor trees visible and did not
reach `ProgramsMatch`. The mutated Python program also changed `digits(235)`
from 15 to 1. Thus the pin is sensitive to a material body change.

The `<k>` entry term expands as:

```text
Invoke(SolutionProgram, "digits", N)
→ Invoke(Module(FuncDef("digits", Params("n"), submitted-body)), "digits", N)
→ exec(submitted-body)
```

No proof rule rewrites `Invoke`, `loop`, or a program expression directly to
the desired product.

Stage 4 result: pass.

## 5. Rule-by-rule static soundness review

The exhaustive reviewer-authored inventory is
[05_static_inventory.md](evidence/05_static_inventory.md). Numbered source,
attribute searches, the trusted Python AST, and arithmetic witnesses are in
[05_static_checks.log](evidence/05_static_checks.log), produced by
[05_static_checks.sh](evidence/05_static_checks.sh). A first inventory-script
attempt had an auditor regex error and is preserved transparently as
`evidence/05_static_checks_attempt1.log`; the corrected run exited 0 and is the
evidence used here.

### Syntax, configuration, and used-construct coverage

`semantic.k` declares `Program`, `Params`, `Stmt`, `Stmts`, `Expr`, and
`CmpOp`. Source productions cover:

- `Module` and `FuncDef`;
- `Assign`, `While`, `If`, and `Return`;
- `Int`, `Name`, `BinOp`, and single `Compare`;
- `CmpOp`; and
- the top-level `Invoke` harness.

The exact submitted AST uses all and only those productions, with binary
operators `%`, `//`, and `*`, comparison operators `>` and `==`, and variables
`n`, `result`, and `digit`. Each operator and variable has a matching rule.
Empty statement lists and statement sequencing are modeled. No used construct
is missing or fabricated.

The configuration contains `<k>`, `<n>`, `<acc>`, `<digit>`, and `<answer>`.
Every auxiliary cell is used. The submitted program needs no heap, allocation,
I/O, exception state, closures, or caller stack.

### All 31 semantic rules

| IDs | Rules and decision |
|---|---|
| S01 | Exact same-name, one-parameter function invocation; initializes every state cell. Sound for the submitted module. |
| S02–S03 | Empty/cons statement-list execution. Sound sequential order. |
| S04–S07 | Assignment, if, while, and return dispatch. Each schedules required evaluation before its continuation. |
| S08–S11 | Integer literal and exact reads of `n`, `result`/`acc`, and `digit`. Sound and consistently renamed. |
| S12–S13 | Left-to-right binary operand evaluation. Sound. |
| S14 | `%` via `%Int`. Correct on all reachable nonnegative operands. Negative-Python limitation discussed below. |
| S15 | `//` via `/Int`. Correct on all reachable nonnegative operands with divisor 10. Negative-Python limitation discussed below. |
| S16 | Unbounded integer multiplication. Sound. |
| S17–S18 | Left-to-right comparison operand evaluation. Sound. |
| S19–S22 | True/false cases for `>` and `==`. Each pair has disjoint, exhaustive guards and yields the integer truth values consumed by this semantics. |
| S23–S25 | Exact writes to `n`, `result`/`acc`, and `digit`, framing other state. Sound. |
| S26–S27 | Nonzero/zero if branches. Disjoint and exhaustive. |
| S28–S30 | Loop test, body-then-recurrence, and exit. Correct control order and stable recurring loop head. |
| S31 | Return records the value and discards the remaining function-local continuation. In the real execution that suffix is the empty `exec` tail; no caller frame exists in the modeled language. |

There are no local semantic function, total, functional, priority,
simplification, concrete, opaque, fresh, or `owise` declarations.

### All 12 verification rules

| IDs | Class and decision |
|---|---|
| V01–V03 | Total, zero-argument constructor macros for the exact loop condition, loop body, and whole program. Unique equations; verified against trusted regeneration. |
| V04 | Partial reflexive structural checker `CheckProgram(P,P)`. Sound and mutation-sensitive. |
| V05–V07 | `addOddDigit`: even keeps accumulator; first odd replaces zero sentinel; later odd multiplies. Guards are exhaustive and pairwise disjoint. |
| V08–V09 | `oddProductFrom`: nonpositive base and positive decimal decomposition. Guards are exhaustive/disjoint; on positive inputs division by 10 strictly decreases. |
| V10 | `oddProduct(N) = oddProductFrom(N,0)`. Sound definitional summary. |
| V11–V12 | Final scratch-digit base and positive recursion. Exhaustive/disjoint and descending on the claim domain. |

All seven locally declared functions are marked `[function,total]` and have
truthful coverage: `digitsCond`, `digitsLoopBody`, `SolutionProgram`,
`addOddDigit`, `oddProductFrom`, `oddProduct`, and `finalScratchDigit`.
There are no `[functional]`, priority, simplification, concrete, opaque, fresh,
or `owise` extensions. No helper K file exists.

V01–V03 expose constructors and do not skip execution. V05–V12 occur only in
claim destinations; they do not rewrite the operational program. In
particular, `oddProduct` never appears in an operational bridge. It is
therefore a definitional specification summary, not an unconstrained oracle or
a smuggled result.

### Broader negative-integer limitation

Fresh witnesses establish that K evaluates `-3 /Int 2` and `-3 %Int 2` to
`-1` and `-1`, whereas Python evaluates `-3 // 2` and `-3 % 2` to `-2` and
`1`. These results are preserved in `05_static_checks.log`.

I do not classify S14 or S15 as unsound for the theorem under audit. From the
entry precondition `N > 0`, `n` remains nonnegative, `digit = n % 10` is
nonnegative, and all divisors are positive constants 10 or 2. The auxiliary
loop claim likewise requires `N >= 0`. Consequently no satisfying
intended-domain state can reach the false negative case. This is a narrower,
over-broad semantics limitation and contributes to `CONCERNS`, not
`NOT_LEGIT`.

No inventoried rule enables a false conclusion on the intended input domain.

Stage 5 result: pass for proof soundness, with the documented scope concern.

## 6. Fresh non-vacuity test

The candidate did not supply a `spec-vacuity.k`; none was relied upon. The
audit created [06_false_result_mutation.k](evidence/06_false_result_mutation.k).
It preserves the genuine loop theorem and changes only the observable entry
answer from:

```text
oddProduct(N)
```

to:

```text
oddProduct(N) +Int 1
```

`N=235` is a satisfying entry input. Both Python implementations return 15, so
the mutation demands the demonstrably false answer 16.

The mutation first passed `kprove --dry-run` with exit 0, establishing that it
parses and builds. The real proof command then exited 1 with
`WarnStuckClaimState`. Its reachable residual has an empty `<k>`, the genuine
computed answer in `<answer>`, and the failed implication:

```text
oddProductFrom(...) +Int 1 #Equals oddProductFrom(...)
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. Exact commands and complete bounded output
are in [06_nonvacuity.log](evidence/06_nonvacuity.log), produced by
[06_nonvacuity.sh](evidence/06_nonvacuity.sh).

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### What is machine proved

Under the rebuilt candidate semantics and its explicit K definitions:

1. For every integer `N >= 0`, the exact submitted loop transforms
   `(n=N, acc=A, digit=D)` to
   `(n=0, acc=oddProductFrom(N,A),
   digit=finalScratchDigit(N,D))`, preserves the answer and arbitrary
   continuation, and consumes the loop on every covered terminating path.
2. For every integer `N > 0`, the exact submitted `solution.mpy` program,
   started from its standard state, consumes its computation and returns
   `oddProduct(N)`, with the exact final accumulator, `n`, and scratch digit
   also constrained.
3. The result obligation is discriminating: the otherwise identical
   plus-one result is not provable.

This is a partial-correctness statement. The program does in fact decrease
positive `n` by division by 10, but the requested theorem classification remains
partial correctness.

### Trust ledger

| Boundary | Influence | Evidence and assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, reachability logic, and built-in `Int`/`Bool` operations | All parsing, execution, arithmetic, and proof closure | Ordinary low-level trusted computing base. Rebuilt live; no candidate binary reused. Acceptable. |
| Trusted mounted prompt, canonical implementation, and translator | Natural-language intent, executable oracle, and Python-to-constructor identity | Authority-designated inputs. Candidate prompt/translator byte identity and trusted regeneration verified. Acceptable. |
| Candidate-generated minimal semantics | Binding, evaluation order, control, state, and return value of the real program | Every local rule was statically audited and all used constructs were executed on normal/boundary cases. There is no independent machine-checked connection theorem to CPython. Acceptable for legitimacy in `GENERATED_SEMANTICS`, but it is the principal concern. |
| `SolutionProgram`, `digitsCond`, and `digitsLoopBody` constructor macros | Identity of code actually symbolically executed | Exact structural match against trusted-regenerated `solution.mpy`; material body mutation is rejected. No value oracle. Acceptable. |
| `oddProduct`, `oddProductFrom`, `addOddDigit`, and `finalScratchDigit` | Formal postcondition and loop summary | Fully defined, total on declared K integers, non-overlapping, descending where recursive, and absent from operational execution. Their reading as “odd decimal digit product” uses ordinary decimal decomposition and multiplication facts. Acceptable, with an informal intent bridge. |
| Generated-versus-canonical differential evidence | Python implementation-to-intent bridge on tested inputs | 10,845 zero-mismatch finite checks. Strong empirical support, not a universal theorem. Contributes to concerns, not to K proof closure. |
| Nonnegative input restriction | Excludes Python/K negative division and remainder disagreement | Matches the prompt’s “positive integer” contract and the entry claim `N > 0`; loop claim uses `N >= 0`. Acceptable restriction. |

There are no opaque result symbols, fresh values, external calls, empirical
oracles inside the K execution, proof-local operational bridges, task-answer
semantic rules, priority shortcuts, or simplification axioms. Candidate prose,
traces, prior `#Top`, and differential tests were not used as substitutes for
the reconstructed K proof.

### Decision

The proof is sound on its formal domain, constrains the observable result,
executes and is sensitive to the actual trusted-regenerated submitted program,
and survives an exhaustive local-rule audit. It is therefore legitimate.

The remaining limitations are evidence/bridge limitations rather than a false
theorem: the language semantics is individually generated and only connected
to Python by transparent rule inspection and finite tests, and its broadly
written division/remainder rules disagree with Python outside the positive
domain. Those limitations fit `CONCERNS / LEGIT` and do not justify
`FAIL / NOT_LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
