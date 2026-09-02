# Independent adversarial audit: 147-get-max-triples

## Decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the actual submitted `solution.mpy` under its generated semantics. A
fresh Haskell proof reconstruction closed the sole positive claim with `#Top`
and exit status 0. The claim contains the complete submitted program term, not
a surrogate invocation or oracle, and the fresh off-by-one mutation built but
failed on the expected unmet result equality.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two bounded
reasons. First, the K postcondition names and defines the closed-form counting
formula, but the connection from that formula to the prompt's triple-enumeration
property is an informal mathematical argument supported by finite differential
testing, not a machine-checked K theorem. Second, the generated language's
generic floor-division rule disagrees with Python when the divisor is negative.
That behavior cannot occur in this submitted program for any claimed input:
all reachable divisors are the positive constants 3 and 6, with nonnegative
numerators. It therefore does not enable a false target conclusion, but it
limits the semantics' reusable scope.

Audit work used K v7.1.293. Candidate sources were copied to
`/tmp/audit-work/audit147`; candidate-built definitions and caches were neither
copied nor used. Tool locations and versions are recorded in
[toolchain-info.log](evidence/toolchain-info.log).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` does not exist. This is the required mount
state, so there is no infrastructure breach and no hidden or inferred reference
semantics was used. The first check and its exit status are in
[stage1-integrity.log](evidence/stage1-integrity.log).

### Required artifacts

The following required candidate artifacts are present as regular, non-symlink
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
An exhaustive symlink search found none.

The candidate prompt is byte-identical to `/reference/prompt.py`, with SHA-256
`d1dd4daedba3670f782bbac1a37a9c1e97e18079d4fb18cf53a18977426075b7`.
The candidate translator is byte-identical to `/reference/py2mpy.py`, with
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Both `cmp` checks exited 0.

There are no missing, changed, mistyped, or symlinked required source
artifacts. The candidate has additional prebuilt `*-kompiled` directories and
a Python bytecode cache. They are generation byproducts, not trusted source,
and were ignored. There are exactly three candidate-local K source files:
`semantic.k`, `verification.k`, and `spec.k`; there is no hidden helper K file.
There is no candidate `PROOF.md` or `spec-vacuity.k`; neither absence was used
against the candidate because the audit reconstructs proof evidence and creates
its own mutation.

### Untrusted generation claims

`run-input.json` describes problem `147-get-max-triples`, condition `bare`, and
records prompt/translator hashes consistent with the trusted files.
`metrics.json` claims generation exit 0 without timeout.
`codex-last.txt` and `codex-output.log` claim concrete results and `#Top`.
The structured trace is present and every one of its 339 JSONL records parses;
its record-type counts are preserved in the stage-1 log. These files were read
only as provenance claims. None of their reported builds or proof results was
accepted in place of fresh reconstruction.

Evidence:

- [run_stage1_integrity.sh](evidence/run_stage1_integrity.sh)
- [stage1-integrity.log](evidence/stage1-integrity.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a positive integer `n`, define an array indexed from 1 through `n` by
`a[i] = i*i - i + 1`. The required result is the number of index triples
`i < j < k` whose three array values sum to a multiple of 3. The prompt's
example requires result 1 for `n = 5`.

The trusted canonical implementation constructs the array, enumerates every
ordered-by-index triple, filters by divisibility by 3, and returns the count.

### Submitted implementation

The submitted `solution.py` uses the closed form

```text
q = (n + 1) // 3
choose3(q) + choose3(n - q)
```

where its inlined `choose3(x)` is `x*(x-1)*(x-2)//6`.

The formula is mathematically aligned with the contract. For any integer
`i`, `i*i-i+1` is congruent to 0 modulo 3 exactly when `i` is congruent to 2;
otherwise it is congruent to 1. Among `1..n`, the zero-residue class has
`q = floor((n+1)/3)` members and the other class has `n-q`. With only residue
values 0 and 1, a three-term sum is divisible by 3 precisely when all three
residues are 0 or all three are 1. Thus the count is
`C(q,3) + C(n-q,3)`.

### Trusted regeneration

Running

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

in scratch exited 0. The regenerated file and `/candidate/solution.mpy` are
byte-identical and have SHA-256
`023c86c0f1ad0b464ed905d669b2ffba7ab4a37cbe097cd5c374bbd2089415c0`.

### Independent differential test

The reviewer-authored test imports `/reference/canonical.py` and the scratch
copy of the candidate `solution.py` through separate module loaders. It covers:

- the documented `n=5` example;
- the empty-array extension `n=0`;
- all values `0..80`, including the first possible triple and every small
  modulo-3 boundary;
- directed boundaries around 30 and 60; and
- 40 pseudorandom values from `1..120` under recorded seed 147.

There were 97 unique inputs, with zero mismatches. `n=0` is explicitly
reported as an extra boundary extension, not part of the positive-integer
formal domain. The generated solution is branch-free; the selected range
repeatedly exercises every residue-class boundary and the canonical
implementation's divisibility branch.

Evidence:

- [differential_test.py](evidence/differential_test.py)
- [run_stage2_fidelity.sh](evidence/run_stage2_fidelity.sh)
- [stage2-fidelity.log](evidence/stage2-fidelity.log)

## 3. Clean proof reconstruction

Only these copied source artifacts were used: `semantic.k`,
`verification.k`, `spec.k`, `solution.py`, and the translator-regenerated
`solution.mpy`. No candidate `*-kompiled` directory or cache entered scratch.
Fresh output directories were named `fresh-runtime-kompiled` and
`fresh-verification-kompiled`.

### Concrete definition and execution

This source-only command exited 0:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition fresh-runtime-kompiled
```

Fresh `krun` executions for `n = 0,1,2,3,4,5,10,29,30,31` all exited 0.
Their K results matched both independent Python implementations. Representative
results were:

| `n` | K | canonical Python | generated Python |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 4 | 1 | 1 | 1 |
| 5 | 1 | 1 | 1 |
| 10 | 36 | 36 | 36 |
| 31 | 1450 | 1450 | 1450 |

This supplies the generated-semantics normal and boundary execution evidence
required by the rendered mode.

### Proof definition and every positive target claim

This fresh source-only build exited 0:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition fresh-verification-kompiled
```

`spec.k` contains exactly one positive reachability claim. Running the entire
`SPEC` module independently:

```text
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC
```

printed exactly `#Top` and exited 0. There is no auxiliary positive claim left
untested.

Evidence:

- [semantic_concrete_check.py](evidence/semantic_concrete_check.py)
- [run_stage3_reconstruction.sh](evidence/run_stage3_reconstruction.sh)
- [stage3-reconstruction.log](evidence/stage3-reconstruction.log)

## 4. Adequacy and real-program pinning

### Entry claim in plain language

There is one entry claim and no helper or loop claim.

Its precondition is:

- the complete `<k>` term is the submitted one-function `Module` AST;
- `<input>` is the mathematical integer `N`;
- `<env>` is empty;
- `<result>` is `noResult`; and
- `N >= 1`.

Its postcondition is:

- `<k>` is completely consumed as `.K`;
- `<input>` remains `N`;
- `<env>` contains exactly `"n" |-> N`; and
- `<result>` is exactly `result(validTripleCount(N))`.

`validTripleCount` is not an unconstrained symbol: its unguarded defining
equation expands to the same two `choose3` terms as the source, and `choose3`
has its own unguarded arithmetic definition. The postcondition contains no
fresh or existential result variable and no implication that could make the
actual return irrelevant.

### Program identity and control-flow match

A reviewer script extracted the source term from the claim's `<k>` cell and
compared it, modulo insignificant whitespace, with the trusted-translator
regeneration. They match. Combined with the byte identity between regenerated
and submitted `solution.mpy`, this pins the claim to the actual submitted
program.

The claim begins at the real module-loading configuration, evaluates the actual
return expression under the generated language rules, and reaches the real
return rule. There is no loop, helper call, substituted body, summarized
invocation, or execution-skipping bridge.

### Satisfiability and concrete substitution

One explicit satisfying state is:

```text
N = 5, <env> .Map </env>, <result> noResult </result>
```

For this state, `q = (5+1)//3 = 2`, so the claimed result is
`choose3(2)+choose3(3) = 0+1 = 1`. Fresh K execution, trusted canonical Python,
and generated Python all return 1. The same four-way comparison passed for
`N = 1,2,3,4,5,10,31`.

Evidence:

- [claim_adequacy_check.py](evidence/claim_adequacy_check.py)
- [run_stage4_adequacy.sh](evidence/run_stage4_adequacy.sh)
- [stage4-adequacy.log](evidence/stage4-adequacy.log)

## 5. Rule-by-rule static soundness review

The complete reviewer-authored declaration and rule inventory is preserved in
[rule-inventory.md](evidence/rule-inventory.md); numbered source listings,
hashes, and category searches are in
[stage5-inventory.log](evidence/stage5-inventory.log).

### Syntax, attributes, and configuration

`MPY-SYNTAX` declares five local sorts: `Pgm`, `Params`, `Stmt`, `Expr`, and
`Value`. Its productions are exhaustively:

1. `Module(Stmt)`;
2. `Params(String)`;
3. `FuncDef(String, Params, Stmt)`;
4. `Return(Expr) [strict]`;
5. `Int(Int)`;
6. the `Value`-to-`Expr` injection;
7. `Name(String)`; and
8. `BinOp(String, Expr, Expr) [seqstrict(2,3)]`.

`MPY` additionally declares `KResult ::= Value` and the result constructors
`noResult` and `result(Int)`. Its configuration has only the state needed here:
`<k>`, `<input>`, `<env>`, and `<result>`, wrapped by `<mpy>`. Every cell is
read or written by the initial configuration or a rule; there is no unused
heap, call stack, allocator, I/O state, or exception cell.

`Return [strict]` evaluates its expression before returning.
`BinOp [seqstrict(2,3)]` evaluates the left operand before the right operand,
matching Python evaluation order. The program's expressions have no
side-effects, but the declared order is still correct.

There are no local syntax priorities, macro rules, opaque declarations,
functional declarations, simplification rules, concrete rules, or priority
rules.

### Exhaustive operational-rule audit

1. **Module entry/load.** The sole `Module(FuncDef(...))` becomes its body and
   binds its single parameter to the configured input in an empty environment.
   This is an explicit single-entry-function convention rather than full Python
   import/call behavior. It is exact for this submitted module, whose sole
   function has parameter `"n"`. Ignoring the function name cannot select a
   different body because no other definition is representable in this
   program term.
2. **Name lookup.** `Name(X)` becomes `Int(I)` only when the map contains
   `X |-> I`. The only reachable identifier is `"n"` and entry installs that
   exact binding. The rule preserves every cell.
3. **Integer addition.** The rule delegates evaluated operands to K `+Int`,
   matching Python arbitrary-precision integer addition here.
4. **Integer subtraction.** The rule delegates to K `-Int`, with the same
   assessment.
5. **Integer multiplication.** The rule delegates to K `*Int`, with the same
   assessment.
6. **Integer floor division.** For nonzero `J`, the rule delegates to
   `divInt`. On the target's complete reachable domain, every `J` is 3 or 6
   and every divided numerator is nonnegative. It therefore matches Python
   `//` on every target execution. The `J =/= 0` guard is disjoint from the
   unmodeled zero case and never blocks the target.
7. **Return.** `Return(Int(I))` consumes the computation and replaces
   `noResult` with `result(I)`. The submitted function has no trailing
   continuation and no other observable effects. The rule does not discard a
   reachable continuation, pop a frame, or hide an exception.

There are no overlapping candidate-local ordinary rules for the same fully
evaluated term, and no priorities alter which rule applies.

### Division scope witness

The division production is syntactically broader than this program needs. A
preserved probe with the positive input `N=1` but a different expression,
`7 // -3`, yields `-2` under this K rule while Python yields `-3`.
The contrasting positive-denominator probe `-7 // 3` yields `-3` in both.
This is a concrete witness to a reusable-language scope mismatch, not a witness
of a false conclusion for the submitted program: its AST contains no negative
denominator and cannot construct one for any `N >= 1`. Division-by-zero would
stop rather than construct Python's exception, but denominators 3 and 6 make
that omitted behavior unreachable as well.

The probes and exact commands are in
[run_stage4_adequacy.sh](evidence/run_stage4_adequacy.sh) and
[stage4-adequacy.log](evidence/stage4-adequacy.log).

### Exhaustive proof-extension audit

`verification.k` adds exactly two symbols:

1. `choose3(Int) [function, total]`, with the sole unguarded equation
   `X*(X-1)*(X-2) divInt 6`;
2. `validTripleCount(Int) [function, total]`, with the sole unguarded equation
   `choose3((N+1) divInt 3) + choose3(N-((N+1) divInt 3))`.

Both functions have complete coverage because their equations are unguarded.
There is no pairwise overlap, recursion, termination issue, or inconsistent
alternative right-hand side. A product of three consecutive integers is
divisible by 6, so `choose3` denotes an integer-valued polynomial quotient for
all integer arguments; its combinatorial interpretation is used only for the
reachable nonnegative class sizes. `validTripleCount` is a pure definitional
summary of the source formula.

Neither function replaces or preempts program execution. They occur only in
the destination postcondition after the real AST has executed. Consequently
they are definitional summaries, not operational bridges or result-bearing
oracles. There is no same-symbol circularity between an execution shortcut and
the postcondition.

`spec.k` adds exactly one unlabeled reachability claim. It adds no semantic
rule, lemma, circularity, function, priority, opacity, or simplification
equation.

### Construct coverage

The submitted `solution.mpy` uses every declared source-language production:
`Module`, `FuncDef`, `Params`, `Return`, `Int`, `Value` as `Expr`, `Name`, and
`BinOp`. Its operator strings are exactly `+`, `-`, `*`, and `//`; each maps to
the audited rule above. The semantics visibly leaves unmodeled features such as
calls, loops, collections, assignments, multiple definitions, allocation,
I/O, and exceptions. None occurs in the submitted program, so their absence is
acceptable minimal coverage in `GENERATED_SEMANTICS` mode.

No candidate-local rule was found that encodes the answer while bypassing
execution, fabricates a result for a used construct, introduces an
unconstrained oracle, or permits a false conclusion about the target on
`N >= 1`.

Evidence:

- [rule-inventory.md](evidence/rule-inventory.md)
- [run_stage5_inventory.sh](evidence/run_stage5_inventory.sh)
- [stage5-inventory.log](evidence/stage5-inventory.log)

## 6. Fresh non-vacuity test

The candidate did not provide a `spec-vacuity.k`. The reviewer created a fresh
`SPEC-VACUITY` module by changing the result-constraining destination from

```text
result(validTripleCount(N))
```

to the false off-by-one value

```text
result(validTripleCount(N) +Int 1)
```

The source program, starting configuration, and precondition were left
unchanged.

The mutation first built successfully: `kprove --dry-run` exited 0. The real
proof run then exited 1 and emitted `WarnStuckClaimState`. Its residual shows
the final configuration with the actual arithmetic result and a failed
implication equating that value plus 1 to the value itself. This is an unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash.

`N=5` is a concrete satisfying witness: the program returns 1 while the
mutation requires 2. Thus the positive proof discriminates a meaningful false
result.

Evidence:

- [spec-vacuity.k](evidence/spec-vacuity.k)
- [run_stage6_nonvacuity.sh](evidence/run_stage6_nonvacuity.sh)
- [stage6-nonvacuity.log](evidence/stage6-nonvacuity.log)

## 7. Proven versus assumed accounting

### Precisely machine-checked

Relative to the freshly compiled `MPY` semantics, K's imported builtin theory,
and the two audited definitional functions, the successful reachability claim
establishes:

> For every mathematical integer `N >= 1`, starting with the exact submitted
> `solution.mpy` AST, input `N`, an empty environment, and `noResult`, execution
> consumes the computation, binds `"n"` to `N`, and returns exactly
> `choose3((N+1) divInt 3) + choose3(N-((N+1) divInt 3))`.

This is a partial-correctness statement. The actual straight-line target has no
loop or recursive call; all reachable divisors are nonzero, so the reviewed
semantics also concretely reaches a final result on the tested cases. The
report does not elevate that observation into a separate universal termination
theorem.

### Trust and assumption ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 compiler, Haskell prover, LLVM runner, and logical kernel | Proof closure and concrete execution | Trusted tooling boundary. Fresh builds and actual statuses are preserved; candidate binaries were excluded. |
| Imported K `INT`, `STRING`, and `MAP` primitives | Arithmetic, strings, binding map | Trusted fixed primitives. The target uses arbitrary-precision integers, literal strings, one map binding, and positive-denominator division. |
| Candidate-generated `MPY` operational semantics | Binding, order, control, and returned value | Not independently machine-proved against Python. It was exhaustively reviewed rule-by-rule and tested concretely on target executions. Its negative-divisor limitation is explicitly excluded from the theorem bridge. |
| Single-function entry convention | Relates a module term plus configured input to calling the submitted entry point | Informal modeling bridge, acceptable for the exact one-function translated module and exact parameter binding. It does not substitute a body or result. |
| Trusted translator and program identity | Pins Python source to `solution.mpy` and the claim | Byte identity after trusted regeneration, plus an independent claim-term comparison. |
| `choose3` and `validTripleCount` | Fix the formal returned value | Audited total definitional functions with exhaustive, nonoverlapping equations. They do not replace execution and are not opaque. |
| Residue-class argument from the closed form to the prompt's triple count | Natural-language intent | Informally established by elementary modular arithmetic, not by a separate K claim. This is the principal reason for `CONCERNS`. |
| Trusted canonical implementation | Differential oracle | Finite empirical evidence only: 97 unique inputs with zero mismatches. It does not replace the K proof or prove universal equivalence. |

There are no opaque symbols, externally supplied program-result primitives,
proof-local operational bridges, empirical oracles inside the K theory,
auxiliary lemmas, loop invariants, priorities, or simplification assumptions.

### Final judgment

The source-only reconstruction, program-term identity, exact result
postcondition, static rule audit, and meaningful failing mutation establish
Gate A real-program soundness and non-vacuity. The positive-integer
precondition exactly matches the prompt's domain. No implementation versus
canonical discrepancy was found.

The proof is nevertheless limited in what is machine-checked: K proves that
the real generated program returns its closed formula, while the formula's
meaning as the requested triple count remains an audited informal bridge with
finite differential support. The small semantics also should not be reused as
a general model of Python floor division with negative divisors. These are
documented adequacy/evidence limitations, not mechanisms capable of proving a
false result for this program on the intended domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
