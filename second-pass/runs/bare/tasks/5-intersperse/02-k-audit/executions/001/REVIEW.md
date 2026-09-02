# Independent adversarial review: 5-intersperse

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof for
the exact submitted constructor program under its generated, integer-list
value semantics. Fresh compilation and proof reconstruction succeeded, the
entry claim is result-constraining, the parsed program in the claim is exactly
the submitted `solution.mpy`, and neither `semantic.k` nor `verification.k`
contains an answer oracle or execution-bypassing proof rule.

The verdict is `CONCERNS / LEGIT`, not `PASS`, because the generated semantics
models lists only as integer sequences and recursion as unbounded. It therefore
does not model Python object identity/allocation or CPython recursion-limit
exceptions. These are observable limitations: `solution.py` aliases its input
on empty/singleton cases whereas the canonical implementation returns a fresh
list, and on this audit runtime the candidate raises `RecursionError` at list
lengths 1000 and 1200 while the iterative canonical implementation returns.
Neither limitation makes the claimed normal-return sequence equality false,
but both make the candidate's comment “Total functional correctness for every
finite integer list” too strong.

All candidate files, logs, traces, and prior compiled definitions were treated
as untrusted. Scratch reconstruction used K v7.1.293 under
`/tmp/audit-work/reconstruction`. Reviewer scripts and bounded logs are under
`/audit-output/evidence/`.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
the three expected regular files:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` does not exist, as this mode requires. There
is no trusted-mount contradiction, so an audit verdict is appropriate.

The candidate's required source deliverables are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. Its `prompt.py` and `py2mpy.py` are byte-identical to the trusted
versions:

- prompt SHA-256:
  `388474ac71e5b893802f5971102df2e4ea82ddf2f916a4a55361c19370f54012`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
- both `cmp -s` and both `diff -u` commands exited 0.

No candidate entry found by the recursive provenance scan is a symlink. The
candidate additionally contains `semantic-kompiled/`,
`verification-kompiled/`, Python bytecode, and concrete-run inputs. Those are
extra generated evidence, not source-integrity failures; none was copied into
or reused by the reconstruction.

The untrusted provenance claims were inspected as follows:

- `run-input.json`, `metrics.json`, `codex-last.txt`, and the bounded head of
  `codex-output.log` are recorded in `evidence/provenance.log`.
- The complete 1,288,132-byte, 11,544-line `codex-output.log` and complete
  403,874-byte, 189-record JSONL trace were streamed and structurally
  summarized by `evidence/summarize_untrusted_generation.py`. All 189 JSON
  records parsed. Hashes, event counts, and bounded terminal events are in
  `evidence/provenance-large-untrusted.log`.
- The prior report claims `KPROVE_PASSED`; that claim was not relied upon.

No required artifact is missing, mistyped, changed, or symlinked. Detailed
commands and exit statuses are in `evidence/run_provenance.sh`,
`evidence/provenance.log`, `evidence/run_provenance_large.sh`, and
`evidence/provenance-large-untrusted.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt requires
`intersperse(numbers: List[int], delimeter: int) -> List[int]`: return the input
integers in order with `delimeter` inserted between each adjacent pair. The
empty result is `[]`; the documented nonempty example maps `[1,2,3], 4` to
`[1,4,2,4,3]`. The trusted canonical implementation builds a fresh result
iteratively.

The candidate uses the equivalent normal-return recurrence:

- if `len(numbers) <= 1`, return `numbers`;
- otherwise return `[numbers[0], delimeter]` concatenated with the recursive
  result for `numbers[1:]`.

This is value-correct for ordinary finite integer-list calls. Unlike the
canonical implementation, it returns the input object itself at lengths zero
and one and consumes one Python stack frame per recursive list element.

### Translator fidelity

The exact reconstruction command

`python3 /tmp/audit-work/reconstruction/py2mpy.py /tmp/audit-work/reconstruction/solution.py | cmp - /tmp/audit-work/reconstruction/solution.mpy`

exited 0. Thus the committed `solution.mpy` is byte-identical to output from
the trusted translator.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and candidate entry point. It exercises:

- both documented examples;
- lengths 0, 1, 2, and 3 and duplicate/negative/delimiter-equals-element cases;
- every list of lengths 0 through 6 over `{-2,0,3}`, with four delimiters;
- 1,000 deterministic generated lists of lengths 0 through 40;
- deep-recursion outcome cases at lengths 900, 1000, and 1200.

For 5,380 ordinary cases, value and input-mutation mismatches were zero. There
were 58 return-identity differences, all caused by the candidate returning its
input for lengths zero or one. At length 900 both implementations returned the
same summarized value. At lengths 1000 and 1200 the canonical implementation
returned but the candidate raised `RecursionError`. The script therefore
exited 1 deliberately after reporting two exception/return outcome
mismatches. This is candidate behavior, not an audit-infrastructure failure.

The exact cases, outputs, and statuses are in
`evidence/stage2-fidelity.log`. The divergence limits total-correctness and
full-Python claims. It does not refute the normal-return sequence property that
the K reachability claim establishes as a partial-correctness result.

## 3. Clean proof reconstruction

Only source files were copied to scratch. Candidate `*-kompiled` directories
and caches were neither copied nor referenced. Fresh definitions were written
to distinct `semantic-fresh-kompiled` and
`verification-fresh-kompiled` directories.

The exact principal commands and outcomes were:

| Command | Exit | Relevant result |
|---|---:|---|
| `kompile semantic.k --backend llvm --main-module MPY --syntax-module MPY-SYNTAX --output-definition semantic-fresh-kompiled` | 0 | Fresh concrete definition built |
| `krun run-empty.mpy --definition semantic-fresh-kompiled` | 0 | `VList([.Ints])` |
| `krun run-single.mpy --definition semantic-fresh-kompiled` | 0 | `VList([7])` |
| `krun run-pair.mpy --definition semantic-fresh-kompiled` | 0 | `VList([7,99,8])` |
| `krun run-example.mpy --definition semantic-fresh-kompiled` | 0 | `VList([1,4,2,4,3])` |
| `krun run-negative.mpy --definition semantic-fresh-kompiled` | 0 | `VList([-1,-9,2,-9,-3,-9,4])` |
| `kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-fresh-kompiled` | 0 | Fresh proof definition built |
| `kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC` | 0 | `#Top` |

Python execution of the same five inputs produced the same integer sequences.
`spec.k` contains exactly one positive entry claim, so every target claim was
independently run. Full commands and outputs are in
`evidence/run_stage3.sh` and `evidence/stage3-reconstruction.log`.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no explicit `requires`. Its sort constraints and source pattern
are its precondition:

- `IS` is any finite K `Ints` sequence, hence any finite sequence of
  mathematical integers;
- `D` is any mathematical K integer;
- `KONT` is any K continuation;
- the invoked Pgm is the exact module containing the submitted `ImportFrom`,
  `FuncDef`, condition, base return, list construction, slice, and recursive
  call;
- the invocation arguments are exactly `VList([IS]), VInt(D)`.

The postcondition says execution reaches
`VList([intersperseSpec(IS,D)]) ~> KONT`: the returned sequence is precisely the
three-equation intersperse recurrence, and the incoming continuation is
preserved. The return is not a fresh RHS variable, tautology, implication-only
condition, or unconstrained oracle.

There is no separate helper or loop claim. The real recursive call re-enters
the same parsed `Invoke` term with the list tail and same delimiter. Because
the entry claim quantifies over `KONT`, it matches that call underneath the
pending concatenation continuation and supplies the legitimate circularity.

### Exact program identity

Textually, the translator spells the empty `else` statement list as a blank
argument while `spec.k` spells the same K list unit as `.Stmts`. To avoid
mistaking surface layout for substitution, the submitted Pgm and the Pgm
compiled from the entry claim were separately converted to KORE. The extracted
terms are each 4,387 bytes and byte-identical.

The pinning procedure and KORE artifacts are:

- `evidence/program_pinning.py`
- `evidence/kore_pinning.py`
- `evidence/submitted-program.kore`
- `evidence/spec-dry-run.kore`
- `evidence/stage4-pinning.log`

### Satisfying state and ground substitution

One satisfying state is `IS = 7,8`, `D = 99`, and `KONT = .K`. Substitution in
the RHS gives `[7,99,8]`. A separate ground reachability claim over the exact
Pgm proved `#Top` with exit 0, concrete K execution returned `[7,99,8]`, and
both Python implementations returned `[7,99,8]`. Commands and outputs are in
`evidence/stage4-pinning.log`.

## 5. Rule-by-rule static soundness review

The exhaustive declaration and rule record is
`evidence/rule-inventory.md`; source-with-line-numbers and mechanical
attribute/rule searches are in
`evidence/stage5-static-and-sensitivity.log`.

### Complete local declaration inventory

`MPY-SYNTAX` declares `Pgm`, `Stmts`, `Strings`, `Params`, `Stmt`, `Exprs`,
`Expr`, `CmpOp`, `Bound`, `Index`, `Ints`, `Val`, `Vals`, and `Run`.
Productions cover `Module`; statement lists; string/parameter lists;
`ImportFrom`, `FuncDef`, `If`, and `Return`; expression lists; `Name`, `Int`,
`Call`, `Compare`, `BinOp`, `ListExpr`, and `Subscript`; `CmpOp`; expression
and no-bound slice bounds; expression and slice indices; integer sequences;
integer/boolean/list values; value lists; and `Invoke`.

`MPY` adds `Env` plus the control constructors `exec`, `eval`, `decide`,
`listSecond`, `makePair`, `binopRight`, `concatWith`, `concat`, `prepend`,
`callSecond`, and `callWith`. Its only state is the `<k>` cell.

`VERIFICATION` adds
`intersperseSpec(Ints,Int):Ints [function,total]`. There are no local
`functional`, simplification, concrete, priority, `owise`, `anywhere`, macro,
alias, or opaque declarations.

Every constructor in `solution.mpy` maps to one of these declarations and to
the rules below. Missing behavior is confined to unused variants of the
deliberately wider grammar.

### All 25 operational rules

| IDs | Function and judgment |
|---|---|
| S1 | `Invoke` exposes the pinned body, binds `IS,D`, and retains the same Pgm. Correct on the exact module. Its unconstrained import/parameter subpatterns are broader than justified for reuse, but no wrong transition results for the pinned program. |
| S2-S5 | Return, if dispatch, true branch, and empty-else false branch. Test order and return control are correct on the exact body. S4 discards following statements before executing any true suite, which is too broad for a normally completing arbitrary suite; the submitted true suite is exactly `Return`, so there is no false intended-input conclusion. S5 intentionally leaves nonempty else suites unmodeled. |
| S6-S8 | Look up `numbers`/`delimeter` in the two-field environment and evaluate integer literals. Correct for the pinned binding. |
| S9-S11 | Fused `len(numbers) <= 1` for empty, singleton, and length-at-least-two list shapes. Cases are disjoint and exhaustive over finite `Ints`. |
| S12-S13 | Head indexing and `[1:]` tail slicing on nonempty lists. Both are reached only after the length-at-least-two case and are sequence-correct. Allocation/identity is abstracted. |
| S14-S16 | Evaluate the exact two-element list literal left-to-right and assemble `[I,J]`. Correct for integer elements. |
| S17-S22 | Evaluate `+` left-to-right, dispatch to structural list concatenation, recurse on the left sequence, and prepend saved heads. Empty/nonempty cases are disjoint, recursion decreases, and output order is correct. Allocation/identity is abstracted. |
| S23-S25 | Evaluate recursive-call arguments left-to-right and re-enter the same Pgm. Direct name resolution is hardwired but correct because the pinned source never rebinds `intersperse`. |

Rule heads are disjoint on reachable configurations; there are no guards or
priorities to create hidden overlap. The configuration has no heap,
allocation, output, exception, or recursion-resource cells. That is adequate
for integer-sequence normal-return reasoning but creates the Stage 2/7
limitations.

The broad S1 and S4 patterns are recorded as narrow generated-semantics scope
gaps, not labeled unsound: no concrete or symbolic witness makes them enable a
false conclusion for any intended input to the exact submitted Pgm. In
accordance with the audit standard, no unsupported unsoundness claim is made.

### All three proof-function equations

- V1: `intersperseSpec([],D) = []`.
- V2: `intersperseSpec([I],D) = [I]`.
- V3:
  `intersperseSpec(I,J,REST,D) = I,D,intersperseSpec(J,REST,D)`.

The cases are pairwise disjoint and exhaustive for finite sequences; V3
strictly decreases sequence length. `[function,total]` is therefore justified.
The symbol is only a definitional postcondition summary. It never rewrites an
executing Pgm term, influences a branch, or replaces program-defined
execution. It is not an opaque result-bearing abstraction or smuggled answer
oracle.

### Body sensitivity

`spec-body-mutation.k` changes the actual body to insert the head instead of
the delimiter while retaining the original postcondition. The mutation
dry-ran successfully (exit 0), then `kprove` exited 1 with
`WarnStuckClaimState` and the expected unmet equality `_I = D`. This confirms
that claim closure depends on the source body and not merely on the RHS
summary. Artifact and log:
`evidence/spec-body-mutation.k` and
`evidence/stage5-static-and-sensitivity.log`.

## 6. Fresh non-vacuity test

The retained reviewer mutation changes the postcondition to
`intersperseSpec(IS, D +Int 1)`, falsely claiming that `D+1` is inserted.

- The mutated spec parsed and dry-ran successfully: exit 0.
- The actual proof exited 1 with `WarnStuckClaimState`.
- The residual is the expected unmet result obligation
  `D #Equals D +Int 1`, in a returned list configuration.
- A satisfying concrete witness is `IS = 7,8`, `D = 99`, `KONT = .K`.
  K, canonical Python, and candidate Python all return `[7,99,8]`; the mutated
  result is `[7,100,8]`.

This is a semantic rejection of a reachable false result, not a parser error,
timeout, missing import, unrelated crash, or unreachable mutation. The
mutation and exact commands/results are in
`evidence/spec-vacuity.k`,
`evidence/run_stage6.sh`, and `evidence/stage6-nonvacuity.log`.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the freshly compiled candidate `MPY` theory, for every finite
mathematical integer sequence `IS`, integer `D`, and K continuation `KONT`,
the exact parsed submitted Pgm invoked with `VList([IS]), VInt(D)` reaches
`VList([intersperseSpec(IS,D)]) ~> KONT`. The proof is partial-correctness
reasoning with the entry claim used coinductively at the recursive call; it
does not establish CPython termination, resource safety, or exceptional
behavior.

Machine evidence also establishes:

- the trusted translator produces the submitted `.mpy` bytes;
- the Pgm embedded in the formal claim is the parsed submitted Pgm;
- the target claim closes with fresh `#Top`;
- a ground satisfying instance closes;
- a supported body change invalidates the theorem;
- a reachable false-result postcondition is rejected.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, LLVM/Haskell backends, K rewriting engine, and builtin mathematical `Int`, `Bool`, `String`, lists, cells, and K sequencing | All machine results | Standard low-level toolchain trust boundary; acceptable and explicitly recorded. |
| Trusted `/reference/py2mpy.py` | Python-AST to Pgm identity | Authority supplied by the audit problem; byte regeneration closes this bridge. |
| Candidate-local rules for parameter binding, direct function-name resolution, fused `len <= 1`, head/slice, list construction/concatenation, return, and recursion | Bridge from Pgm constructors to Python behavior | Audited rule-by-rule and concretely exercised. There is no machine-checked refinement theorem to CPython, so the bridge remains an informal generated-language assumption supported by finite evidence. Acceptable for the exact value-level subset, but a reason for `CONCERNS`. |
| `intersperseSpec` recurrence has the natural-language “delimiter between adjacent elements” meaning | Intent adequacy | Ordinary mathematical argument: empty/singleton bases and the head/delimiter/tail recurrence. It is transparent and exhaustive, not opaque. |
| Differential execution over 5,380 ordinary cases and five K concrete cases | Empirical support for implementation/semantics/intent bridges | Reproducible finite support only; not used as a universal proof. |
| No heap/object-identity/allocation model | Aliasing and freshness | Observable exclusion. Candidate/canonical identity differs at lengths 0/1. The formal theorem asserts sequence values only, so this is concerning but not illegitimate. |
| No exception or recursion-resource model | Deep CPython behavior and totality | Observable exclusion. Candidate raises `RecursionError` for tested lengths 1000/1200. The proof remains a legitimate normal-return partial-correctness proof, but not total correctness for all finite Python lists. |

There are no candidate-local opaque symbols, unconstrained fresh
result-bearing values, empirical oracles in execution rules, proof-only
operational bridges, axiomatic lemmas, or simplification rules. The finite
differential evidence and untrusted prior `#Top` are not substitutes for the K
proof.

### Gate summary and verdict rationale

- Real-program/value-semantics soundness: passes. The exact body executes, the
  only proof extension is a truthful postcondition function, and both body and
  result mutations discriminate.
- Intent adequacy: the normal-return sequence property matches the prompt, but
  Python identity/allocation and recursion exceptions are excluded. The
  candidate's total-correctness prose is unsupported.
- Trust/evidence auditability: passes with all assumptions and empirical scope
  explicit and reproducible.

These limitations do not allow a false normal-return sequence conclusion for
the intended typed inputs, so they do not justify `FAIL / NOT_LEGIT`. They are
material enough to rule out an unqualified `PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
