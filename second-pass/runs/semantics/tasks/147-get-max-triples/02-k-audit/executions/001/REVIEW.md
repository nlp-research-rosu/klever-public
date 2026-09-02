# Independent adversarial review: 147-get-max-triples

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated function under the supplied MPY semantics. The clean
proof executes the exact translated function body and constrains its result to
an explicit arithmetic expression. It does not replace execution with an
oracle, and both a body mutation and a false-result mutation are rejected.

The appropriate result is nevertheless **CONCERNS / LEGIT**, not PASS. The main
K theorem establishes that the implementation returns `tripleCount(N)`, but no
K claim connects `tripleCount` to enumeration of the triples in the original
contract. The three residue claims are true, but the main claim closes when
selected alone and does not use them. The remaining bridge is a convincing
informal combinatorial argument plus finite differential evidence, rather than
a reachability theorem. The candidate also lacks all four named generation
metadata files and any structured trace, reducing provenance auditability.

I followed the `using-kit` live-tooling route and the `validating-proof` Gate A
checks. All candidate content was treated as evidence only. Builds and
mutations used the clean copy at `/tmp/audit-work/reconstruction`; no
candidate-provided compiled definition or cache was copied or used.

## 1. Input and provenance integrity

Semantics-mode boundary: the rendered mode is `SUPPLIED_SEMANTICS`, and the
trusted `/reference/reference-semantics` directory is present. There is no
infrastructure contradiction.

The independent recursive inventory compared entry names, types, and SHA-256
hashes without following symlinks:

- `/candidate/prompt.py` is a regular file and byte-identical to
  `/reference/prompt.py` (SHA-256
  `d1dd4daedba3670f782bbac1a37a9c1e97e18079d4fb18cf53a18977426075b7`).
- `/candidate/py2mpy.py` is a regular file and byte-identical to
  `/reference/py2mpy.py` (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- The trusted and candidate `reference-semantics/` trees each contain 25
  entries. There are zero missing, additional, type-changed, byte-changed, or
  symlinked entries.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files. No required proof source is symlinked.
- `/candidate/run-input.json`, `/candidate/metrics.json`,
  `/candidate/codex-last.txt`, and `/candidate/codex-output.log` are all
  missing. No structured JSON/JSONL or trace-named generation trace is
  present. Consequently, there were no such untrusted claims to inspect.
- `/candidate/__pycache__/solution.cpython-310.pyc` is a candidate cache. It
  was deliberately excluded from scratch. `prove.sh`, `concrete_tests.py`, and
  `concrete_tests.mpy` were read as untrusted evidence but not used as proof
  results.

Reproduction: [integrity checker](/audit-output/evidence/01_integrity.py),
[command wrapper](/audit-output/evidence/01_run_integrity.sh), and
[complete output](/audit-output/evidence/01_integrity.log).

Stage result: provenance of the prompt, translator, and supplied semantics is
clean. The missing generation metadata is an auditability concern, not a
semantic counterexample or proof-reconstruction failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

For a positive integer `n`, define `a[i] = i*i - i + 1` for indices
`1 <= i <= n`. The required result is the number of index triples
`i < j < k` whose three array values sum to a multiple of 3. The documented
example is `n=5`, result `1`.

The trusted canonical implementation constructs the array and enumerates every
ordered index triple. The submitted [solution.py](/candidate/solution.py:1)
uses the closed form

```text
z = floor((n + 1) / 3)
return C(z, 3) + C(n - z, 3)
```

where each `C(c,3)` is computed as `c*(c-1)*(c-2)//6`.

The arithmetic is correct on the stated positive domain. For an index modulo
3, `i*i-i+1` has residue `1,1,0` for `i` congruent to `0,1,2`.
Every array value therefore has residue 0 or 1. Three such residues sum to 0
modulo 3 exactly when all three are 0 or all three are 1. Among `1..n`, the
number in the residue-2 index class is `floor((n+1)/3)`, and the other class
has size `n-z`, producing the submitted formula.

### Trusted translation identity

The exact command

```text
python3 /reference/py2mpy.py /tmp/audit-work/reconstruction/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

exited 0. `cmp -s` exited 0, and both regenerated and submitted files have
SHA-256
`5a0b502c9645b094e28af71a4accb31a8ac0ec8fd5c81947ca3fa6c994b63979`.
Thus [solution.mpy](/candidate/solution.mpy:1) is byte-for-byte the output of
the trusted translator.

### Independent differential execution

The independent test loads `/reference/canonical.py` and the scratch copy of
the generated `solution.py` through separate Python modules. It covers:

- the documented `n=5` example;
- `n=0` as an explicitly labeled empty extension outside the positive domain;
- every `n` from 1 through 12, covering residue-class transitions and the
  `C(c,3)` population thresholds;
- 36 deterministic, seed-147 generated values from 13 through 220.

All 49 exact inputs and outputs are printed in the log. There were zero
mismatches. This is finite bridge evidence, not a universal proof. Negative
integers were not included because they are outside the stated domain and the
K entry precondition.

Reproduction: [differential script](/audit-output/evidence/02_differential.py),
[translation/test wrapper](/audit-output/evidence/02_run_fidelity.sh), and
[results](/audit-output/evidence/02_fidelity.log).

Stage result: program and translation fidelity pass on the intended domain.

## 3. Clean proof reconstruction

The toolchain was K v7.1.337, build date 2026-06-18. All definitions were built
from the copied source tree. The candidate contained no compiled definition
that was reused.

### Concrete definition

This fresh command exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled
```

The reviewer-authored translated test program exercised `n=0,1,2,3,4,5,6,8,20,201`.
`krun` exited 0 in a final configuration with `.K`, `NoExc`, and exit code 0.
The source is [03_k_concrete_tests.py](/audit-output/evidence/03_k_concrete_tests.py).

The LLVM build emitted non-exhaustive-totality warnings for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None of these symbols
is reachable from the submitted program or its postcondition. They are
accounted for as unused supplied-semantics trust gaps in stages 5 and 7, not
silently treated as proof evidence.

### Proof definition and each positive claim

The proof build

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled -I .
```

exited 0. Every positive claim was then selected and run separately:

| Claim | Exit | Required output |
|---|---:|---|
| `SPEC.residue-0` | 0 | `#Top` |
| `SPEC.residue-1` | 0 | `#Top` |
| `SPEC.residue-2` | 0 | `#Top` |
| `SPEC.get-max-triples-correct` | 0 | `#Top` |

The three residue claims were reported as trivial after arithmetic
simplification. The main proof printed several
`DecidePredicateUnknown` diagnostics during intermediate simplification but
closed with `#Top` and exit 0; there was no stuck state.

Exact commands, statuses, and bounded complete output are in
[03_rebuild_and_prove.sh](/audit-output/evidence/03_rebuild_and_prove.sh) and
[03_rebuild_and_prove.log](/audit-output/evidence/03_rebuild_and_prove.log).

Stage result: clean reconstruction passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

- `residue-0`: for every mathematical integer `Q`,
  `(3Q)^2 - 3Q + 1` modulo 3 is 1.
- `residue-1`: for every `Q`,
  `(3Q+1)^2 - (3Q+1) + 1` modulo 3 is 1.
- `residue-2`: for every `Q`,
  `(3Q+2)^2 - (3Q+2) + 1` modulo 3 is 0.
- `get-max-triples-correct`: for every mathematical integer `N > 0`, start
  from the exact module/builtins state shown in the claim, invoke the
  one-argument `get_max_triples` closure, and reach `tripleCount(N)` while the
  explicitly listed environment, scope, heap, stack, return, exception, and
  exit-code cells satisfy the unchanged claim pattern.

There are no loop or helper reachability claims because the submitted
implementation is straight-line arithmetic.

### Exact body pinning

The entry claim begins after module loading, with a closure installed in scope
0. This is not a substituted algorithm:

1. `getMaxTriplesBody` in
   [verification.k](/candidate/verification.k:8) expands to the exact statement
   AST in the byte-verified submitted `solution.mpy`.
2. Fresh `krun solution.mpy` reached a module scope containing
   `get_max_triples |-> closureVal(("n", .ParamNames), <that exact AST>, 0)`,
   which is the closure used by the claim.
3. The claim then executes ordinary `Call`, lookup, argument evaluation,
   parameter binding, assignment, integer-operation, return, and frame-pop
   rules. There is no proof-local `<k>` rewrite that intercepts any program
   operation.
4. A separately compiled mutation changed only the body return to
   `zero_triples + one_triples + 1` while leaving the postcondition unchanged.
   That proof exited 1 with `WarnStuckClaimState` at the expected equality.
   This rules out body-insensitive closure or summary substitution.

The whole-file pinning and satisfying-ground evidence is in
[04_pinning_and_ground.log](/audit-output/evidence/04_pinning_and_ground.log).
The body mutation, build, and residual are
[05_verification_body_mutated.k](/audit-output/evidence/05_verification_body_mutated.k),
[05_body_mutation_spec.k](/audit-output/evidence/05_body_mutation_spec.k), and
[05_body_sensitivity.log](/audit-output/evidence/05_body_sensitivity.log).

### Satisfiable witnesses and concrete substitution

The residue claims have no preconditions; `Q=0` is a satisfying valuation for
each. For the main claim, `N=5` satisfies `N > 0`, and the exact state printed
in the claim is realizable by loading `solution.mpy`.

The reviewer-authored ground claim replaces the postcondition with the concrete
value `1`; it exited 0 with `#Top`. Independently:

```text
N 5
PRECONDITION_N_GT_0 True
CANONICAL 1
GENERATED 1
FORMAL_TRIPLE_COUNT 1
```

See [04_ground_spec.k](/audit-output/evidence/04_ground_spec.k) and
[04_pinning_and_ground.log](/audit-output/evidence/04_pinning_and_ground.log).

### Adequacy limitation

The returned value is constrained; it is not a free variable, tautology, or
one-way implication. However, the K theory does not define the original array,
index triples, or a count of triples, and no claim proves
`tripleCount(N)` equivalent to that count. The independently selected main
claim closes without the residue claims. The informal argument in stage 2
fills this intent bridge convincingly, but it remains outside the machine
proof. This is the material reason for CONCERNS rather than PASS.

Stage result: real-program pinning and result constraint pass; the
formal-summary-to-natural-language bridge is limited.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source-complete inventory covers every K source in the supplied tree,
`verification.k`, and the four spec claims. It records the source hash, start
line, full declaration/rule text, attributes, submitted-path classification,
and an audit decision for each entry.

Totals:

- 940 inventoried entries;
- 699 rules, 231 syntax declaration blocks, 5 contexts, 1 configuration, and
  4 claims;
- declaration blocks include 149 `function`, 107 `total`, 25 `symbol`,
  22 `no-evaluators`, 29 `priority`, 26 `owise`, 32 `concrete`, 4 `macro`,
  1 `macro-rec`, 2 `strict`, and 1 `seqstrict` attributes;
- no `functional` declaration and no simplification rule occurs.

The per-file counts and all 940 decisions are in
[05_rule_inventory.py](/audit-output/evidence/05_rule_inventory.py) and
[05_rule_inventory.log](/audit-output/evidence/05_rule_inventory.log).
This avoids relying on comments or a candidate-generated inventory.

### Construct-to-rule map for `solution.mpy`

| Submitted construct | Declaration and execution route |
|---|---|
| `Module`, `FuncDef`, `Params`, statement list | `syntax.k`; `core.k` `#loadAll`/statement sequencing; `functions.k` installs the closure |
| `Call(Name(...), args)` | `syntax.k`; `core.k` scope-chain lookup and left-to-right `#evalArgs`; `call.k` callee and closure dispatch |
| parameter `n` | `functions.k` `#bindP`, into the fresh call scope |
| `Assign(Name, rhs)` | strict RHS from `syntax.k`; ordinary current-scope write in `controls.k` |
| `Int` and `BinOp` | integer literal in `core.k`; left-then-right `seqstrict` evaluation; `operators.k` dispatch; `int.k` `+`, `-`, `*`, `//`, and `pyMod` |
| `Return` | strict expression evaluation; `functions.k` stores the value, pops the frame, restores environment and scope location, and resumes the saved continuation |

The exact entry state has no cell variables, references, heap objects, method
calls, imports, floats, containers, exceptions, loops, or builtins. Therefore,
the high-priority cell/ref alternatives cannot overlap the used plain rules.
The generic `Call` rule is `[owise]`, but there is no candidate-local
interception that can preempt it.

Evaluation and state effects are faithful on the matched domain:

- the callee is looked up before arguments, and arguments are evaluated
  left-to-right;
- each binary operation evaluates its left operand then its right;
- assignments update only the fresh callee scope;
- the call pushes one frame and allocates scope 1;
- return records the computed integer, removes the callee scope, restores
  environment 0 and scope location 1, clears the return cell, and leaves the
  empty heap and the other observable cells unchanged.

All divisions in this program use positive denominators 3 or 6. The MPY
definition `(x - pyMod(x,d)) /Int d` matches Python floor division for these
denominators. For `N>0`, `zeroResidues(N)` and `N-zeroResidues(N)` are
nonnegative, so the `chooseThree` interpretation is used only on its documented
population-count domain.

### Proof-local extensions

`verification.k` has exactly four syntax/function declarations and four
equations:

1. `getMaxTriplesBody`: a definitional AST alias. It executes no redex and is
   byte/AST matched to the submitted translation.
2. `chooseThree(C)`: a terminating one-equation mathematical definition using
   K integer arithmetic and `pyMod`.
3. `zeroResidues(N)`: a terminating one-equation definition of
   `floor((N+1)/3)` for the positive-divisor operation used by the program.
4. `tripleCount(N)`: a terminating composition of the preceding definitions.

Each has one sort-complete equation, so there are no overlapping guards or
conflicting right-hand sides. None is marked `total`, `functional`, `symbol`,
`priority`, `simplification`, `concrete`, or `owise`. Most importantly, none is
an operational bridge: no rule has a `<k>` cell or replaces program execution.
The summary functions occur on the destination side after ordinary execution.
There is no fresh result-bearing or unconstrained program-derived symbol.

The definitions do encode the desired arithmetic in the postcondition, which
is legitimate specification rather than answer-smuggling because execution
independently computes the same value and the body-sensitivity mutation fails.

### Supplied opaque and totalized boundaries

The 25 supplied `symbol(...)` declarations are:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

None is reachable from the submitted term, the entry result, or the residue
claims. The non-exhaustive-totality compiler warnings likewise concern unused
constructs. I found no symbolic or concrete false-conclusion witness by which
any of these unused declarations can affect this theorem, so I do not label
them unsound. The narrower conclusion is that the supplied semantics has
globally opaque/totalized areas outside this program's semantic slice; they
remain fixed trust boundaries, not evidence for the proof.

No candidate-local rule bypasses execution, fabricates a used construct,
introduces an oracle, or enables a false result on the intended domain. There
is therefore no claimed unsound rule requiring a false-conclusion witness.

Stage result: static soundness passes for the theorem's complete reachable
rule slice; unused supplied-semantic opacity is explicitly bounded.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so no candidate mutation was
trusted or reused.

The fresh mutation changes only the result obligation from
`tripleCount(N)` to `tripleCount(N) +Int 1`, preserving the exact entry state
and `N > 0` precondition. `N=5` is a concrete satisfying witness: the actual
and original formal result is 1, while the mutation demands 2.

The `kprove --dry-run` command exited 0, proving the mutated spec parsed and
compiled against the clean definition. The actual proof exited 1 with
`WarnStuckClaimState`; the residual explicitly shows failure of the implication
between the computed count and that same count plus 1. This was not a parser
error, missing import, timeout, or unrelated crash.

Artifacts:
[false-result spec](/audit-output/evidence/06_spec_false_result.k),
[wrapper with exact commands](/audit-output/evidence/06_run_nonvacuity.sh), and
[complete residual](/audit-output/evidence/06_nonvacuity.log).

Stage result: non-vacuity passes.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the exact supplied MPY semantics, for every mathematical integer
`N > 0`, execution of the exact translated `get_max_triples` closure from the
entry configuration reaches the integer

```text
z = floor((N + 1) / 3)
C3(c) = floor(c * (c - 1) * (c - 2) / 6)
C3(z) + C3(N - z)
```

with the framed configuration restored as specified. This is a
result-constraining reachability/partial-correctness statement about the real
submitted function body. Separately, the three residue claims prove the
displayed modular arithmetic identities for all integer `Q`.

The proof does **not** internally formalize arrays, `i<j<k`, triple
enumeration, or the theorem that the closed form equals the natural-language
count. It also makes no claim for `N<=0`.

### Trust and evidence ledger

| Boundary | Influence | Assessment and support |
|---|---|---|
| K v7.1.337 parser, kompiler, Haskell prover, LLVM runtime, and built-in Int/Bool/Map/List/String theory | All parsing, execution, and proof closure | Necessary low-level trust boundary; versions and fresh commands recorded |
| Trusted mounted MPY semantics | Program binding, evaluation, state, call/return, and integer operations | Acceptable selected-semantics boundary; candidate tree is byte/type identical; used slice statically audited |
| MPY opaque/totalized symbols listed in stage 5 | Potentially floats, sorting, MD5, and unused collection operations | Concerning globally but irrelevant here; no data/control/result dependency |
| Proof-local `getMaxTriplesBody` | Identity of executed function body | Not assumed: exact translator identity, whole-file closure state, and rejected body mutation support the connection |
| Proof-local arithmetic functions | Destination value only | Fully defined, terminating equations; no operational replacement or opacity |
| Closed-form-to-contract combinatorics | Meaning of `tripleCount` as the requested count | Informal, not K-proved; supported by the residue argument and independent canonical comparison |
| Differential Python evidence | Generated/canonical bridge on 49 inputs | Zero mismatches; finite evidence only |
| Concrete K evidence | MPY behavior on 10 boundary/normal inputs and exact whole-file load | Zero assertion failures and normal final states; finite evidence only |
| Missing generation metadata/trace | Provenance narrative only | Auditability limitation; does not alter reconstructed source proof |

`PROOF.md`, generation prose, prior traces, and prior `#Top` output played no
role in the decision. The status rests on fresh reconstruction, exhaustive
source inventory, result/body sensitivity, and explicitly bounded informal
evidence.

### Final rationale

Gate A (real-program soundness and non-vacuity) passes. Gate B has a documented
formal intent-bridge limitation: the closed-form combinatorial equivalence is
not a K theorem, although it is mathematically sound and well supported. Gate C
is adequate for a legitimate proof but not pristine because the named
generation metadata is absent and the intent bridge has only finite executable
corroboration. Under the requested decision boundary, this is
**CONCERNS / LEGIT**.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
