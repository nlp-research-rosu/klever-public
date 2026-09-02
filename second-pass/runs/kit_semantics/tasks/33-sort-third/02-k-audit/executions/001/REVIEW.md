# Independent adversarial review: 33-sort-third

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed both definitions from
source, reran all positive claims, mechanically pinned the entry claim to the
regenerated program, reviewed every proof-local declaration and rule, and
rejected fresh false-result and actual-body mutations for the expected reasons.
The result-bearing `sortVS` operation is an explicit primitive of the trusted
supplied semantics, not a candidate-created oracle.

## 1. Input and provenance integrity

The launcher declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, condition `kit-semantics`, and problem
`33-sort-third`. The trusted `/reference/reference-semantics` tree is present,
as the rendered mode requires.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required JSON and text record
under `/generation-evidence`, and all 534 JSONL events in the structured trace.
The generation records were treated only as claims. The candidate's final
generation claim was `KPROVE_PASSED`, but none of the findings below relies on
that claim.

The independent checker and full output are
[`integrity_check.py`](evidence/integrity_check.py) and
[`01-integrity-check.log`](evidence/01-integrity-check.log). Its material
results were:

- The campaign-lock JSON object exactly equals the `audit_campaign` block, and
  the lock's SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every pipeline-v3 required record and every launcher-declared container path
  is present, readable, of the expected kind, and not a symlink.
- All directly recorded file hashes match, including the run, task,
  generation-result, invocation, metrics, runtime metrics, usage, prompt,
  output log, last message, canonical implementation, trusted prompt, and
  translator.
- An independent reimplementation of the pipeline-v3 tree digest gives
  `02d2439095e3821e7de05e91a6a05ad55ee6f496fc92b22741c8506c584f787a`
  for `/candidate`, exactly matching
  `generation-result.json.outputs.workspace_sha256`.
- The candidate and trusted semantics both give pipeline tree digest
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  exactly matching the task manifest.
- The structured-trace tree gives
  `8da9a97e2e00d586f6e58ddebfaa61cdf27477efb182bfa13499055a67a52b17`,
  exactly matching `usage.json.source_trace_sha256`; the sole JSONL file also
  matches its independently recorded file hash.
- A recursive entry-by-entry comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` found zero missing, additional, changed,
  mistyped, unsupported, or symlinked entries. Both contain 24 regular files
  and one subdirectory.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounted versions.
- All required candidate proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`) are regular,
  readable, non-symlinked files. Candidate-provided compiled directories,
  logs, and prose were not reused for reconstruction.

[`generation_record_summary.py`](evidence/generation_record_summary.py) and
[`01b-generation-record-summary.log`](evidence/01b-generation-record-summary.log)
record the complete record/trace traversal and untrusted final generation
claim. No infrastructure contradiction or breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an input list `l`, return a list of the same length. At every index not
divisible by three, retain `l[i]`. Take the subsequence at indices
`0, 3, 6, ...`, sort that subsequence in ascending order, and put its elements
back at those same indices in order. The prompt examples are:

```text
[1, 2, 3]                 -> [1, 2, 3]
[5, 6, 3, 4, 8, 9, 2]    -> [2, 6, 3, 4, 8, 9, 5]
```

The trusted canonical implementation copies the list, performs
`l[::3] = sorted(l[::3])`, and returns the copy. The submitted implementation
computes `thirds = sorted(l[::3])`, then visits every index and appends either
`thirds[i // 3]` or `l[i]`. For ordinary finite lists on which `sorted` returns
normally, these algorithms have the same result and neither mutates the input.

### Trusted translation

I copied only source artifacts to `/tmp/audit-work/33-sort-third`; no candidate
compiled definition or cache was copied. Regeneration used the trusted mounted
translator:

```bash
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both MPY files have SHA-256
`eaed1237d6241da329e0d8513182cf00d88f1f3f8d51b994247b3e669f9feba5`;
`cmp` exited 0. See [`02-regenerate-mpy.log`](evidence/02-regenerate-mpy.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and generated entry points independently. It covers both documented
examples, empty/singleton and all three length residues around branch
boundaries, negative values, duplicates, booleans, floats, strings, every
integer sequence of lengths 0 through 6 over `[-2,2]`, every string sequence of
lengths 0 through 5 over `abc`, and 2,000 seeded integer lists of lengths 0
through 100.

```text
total_cases=21914
input_mutations=0
mismatches=0
```

The command exited 0; see
[`03-differential.log`](evidence/03-differential.log). This is finite evidence
for the Python implementation bridge, not a substitute for the symbolic proof.

## 3. Clean proof reconstruction

K v7.1.293 and Python 3.10.12 are recorded in
[`00-tool-versions.log`](evidence/00-tool-versions.log).

I built fresh definitions in scratch, from the trusted source semantics and
candidate K source:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

Both exited 0. The bounded logs are
[`04-kompile-llvm.log`](evidence/04-kompile-llvm.log) and
[`06-kompile-haskell.log`](evidence/06-kompile-haskell.log). The warnings are
pre-existing supplied-semantics warnings about several total functions and
unused string-rule variables; there was no build failure.

A reviewer-authored eight-case concrete MPY suite was translated with the
trusted translator and executed against the fresh LLVM definition. It reached
`.K`, `NoExc`, and `<exit-code> 0`. The source and log are
[`k_concrete_test.py`](evidence/k_concrete_test.py) and
[`05-krun-concrete.log`](evidence/05-krun-concrete.log).

Every positive claim was then rerun:

```bash
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
# #Top, exit 0

kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC
# #Top, exit 0
```

The complete logs are [`07-kprove-loop.log`](evidence/07-kprove-loop.log) and
[`08-kprove-all.log`](evidence/08-kprove-all.log). The full run proves both
claims together, allowing the entry claim to consume the loop circularity.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` starts at the exact `#while` loop head. Its precondition
pins:

- `0 <= I <= N` and `N = vsLen(VS)`;
- local bindings `i = I`, `l = list(VS)`, `result = ref(OUT)`, and
  `thirds = ref(THIRD)`;
- heap objects `OUT |-> list(A)` and `THIRD |-> list(SV)`;
- the function-to-module-to-builtins scope chain; and
- absence of a module binding named `len`.

Its postcondition preserves the framed continuation, sets `i` to `N`, and
changes the result list to
`A ++ mergeThirdFrom(VS, SV, I, N)`. Other cells and map entries are framed.
Map definedness makes the explicitly mentioned heap locations distinct.

`SPEC.sort-third` has no `requires` clause or length bound. It starts from the
normal empty module configuration, loads the function, and calls it on the
arbitrary finite `list(VS)`. Its postcondition requires:

- returned K value `ref(2)`;
- the exact loaded closure and cleaned-up callee scope;
- heap location 0 equal to the `l[::3]` slice;
- heap location 1 equal to `sortVS` of that slice;
- heap location 2 equal to `sortThirdResult(VS)`;
- `heapLoc` advanced from 0 to 3; and
- restored environment, scope location, empty stack, `noRet`, `NoExc`, and
  exit code 0.

Thus the result is not a free variable, implication-only observation, or
tautology.

### Mechanical program identity

The raw MPY program uses surface list sugar, whereas the K claim spells out
`.Exprs`, `.Stmts`, and `.ParamNames`. I therefore compared normalized
constructor trees rather than text. The reviewer extractor took the exact
`Module(...)` under the first `#loadAll` in `SPEC.sort-third`; `kast` parsed the
regenerated MPY as a program and the extracted term as rule syntax. The two
KAST trees are exactly equal:

```text
translated_sha256=98db451109c949fc6f00b6e0f976ec49b53fdd0bfc7fa1ec7771e4e42c3ea798
claimed_sha256=98db451109c949fc6f00b6e0f976ec49b53fdd0bfc7fa1ec7771e4e42c3ea798
constructor_tree_exact_equal=True
translated_kapply_nodes=80
claimed_kapply_nodes=80
```

See [`extract_claim_program.py`](evidence/extract_claim_program.py),
[`compare_program_kast.py`](evidence/compare_program_kast.py), and
[`09c-program-term-identity.log`](evidence/09c-program-term-identity.log).
Earlier parser-interface experiments in `09-program-term-identity.log` and
`09b-program-term-identity-kprove.log` failed because surface-program and
rule-internal list syntax use different parser entry points; they are not proof
runs. The final KAST comparison uses the correct entry point for each syntax.

### Satisfiable witnesses and substitution

An entry witness is
`VS = [5,6,3,4,8,9,2]` in the claim's normal initial configuration. A
corresponding loop witness takes `L=1`, `I=0`, `N=7`, `A=[]`,
`SV=[2,4,5]`, distinct `OUT=2` and `THIRD=1`, the actual module scope without a
`len` key, and the actual heap bindings. All arithmetic and map constraints are
satisfied.

I grounded the complete entry claim at that input and replaced its symbolic
result with the explicit expected sequence. The grounded claim and the general
loop claim together produced `#Top`, exit 0; see
[`make_concrete_substitution_spec.py`](evidence/make_concrete_substitution_spec.py)
and
[`11-concrete-substitution-kprove.log`](evidence/11-concrete-substitution-kprove.log).
Both Python implementations also return the identical explicit result:

```text
formal_substitution=[2, 6, 3, 4, 8, 9, 5]
trusted_canonical=[2, 6, 3, 4, 8, 9, 5]
generated_solution=[2, 6, 3, 4, 8, 9, 5]
```

See [`12-ground-witness-python.log`](evidence/12-ground-witness-python.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`static_inventory.py`](evidence/static_inventory.py) generated
[`static_inventory.txt`](evidence/static_inventory.txt), a 966-line inventory
of all 26 K source files used in the concrete/proof builds. It enumerates 229
syntax declarations, 702 rules, five contexts, one configuration, both claims,
and attributes including `function`, `total`, `no-evaluators`,
`simplification`, `priority`, `owise`, `macro`, and `concrete`.

The candidate adds exactly two syntax declarations and seven rules in
`verification.k`; it adds no other helper K file, priority rule, operational
interception, `trusted` claim, or semantic configuration.

### Candidate-local declarations and rules

1. `mergeThirdFrom(ValSeq, ValSeq, Int, Int)` is `[function,total]`.
   Its `I >= N` rule returns empty. For `I < N`, two rules partition the domain
   by `pyMod(I,3) == 0` versus `=/= 0`; they append respectively
   `SV[I/3]` and `VS[I]`, then recurse at `I+1`. The guards are exhaustive and
   disjoint, divisor 3 is nonzero, and `N-I` strictly decreases on every
   recursive application. The entry path additionally has `I >= 0`, so K's
   integer division agrees with Python floor division.

2. `sortThirdResult(ValSeq)` is `[function,total,no-evaluators]`. It is not an
   unconstrained result oracle. The universal folding simplification equates
   the exact complete merge
   `mergeThirdFrom(VS, sortVS(buildVS(VS,0,vsLen(VS),3)),0,vsLen(VS))`
   with `sortThirdResult(VS)`. The empty-result rule applies when
   `vsLen(VS) <= 0`; then the complete merge also immediately takes its
   `I >= N` base case. The overlap is consistent.

3. The associativity rule for `valSeqConcat` is valid by structural induction
   on `A`: the empty case reduces to `B ++ C`, and the constructor case reduces
   both sides to `vCons(head, ...)` and uses the induction hypothesis on the
   tail.

4. The right-identity rule is valid by the same induction: `[] ++ [] = []`,
   and `(v::r) ++ [] = v::(r ++ []) = v::r`.

The associativity orientation reduces left nesting and right identity removes
a constructor, so neither introduces a simplifier cycle. Their overlaps with
the supplied two defining `valSeqConcat` equations agree. An exploratory
attempt to express these as bare functional reachability claims was rejected
by this Haskell backend as unsupported, and a configuration wrapper did not
cause it to synthesize structural induction; those diagnostics are preserved
in `14-kprove-fixed-lemmas.log` and `14b-kprove-fixed-lemmas.log`. They were
not used as validation evidence. The explicit inductions above establish the
ordinary mathematical lemmas over the two-constructor `ValSeq` datatype.

### Fixed-semantics execution path

Every constructor in `solution.mpy` has a supplied declaration in
`semantics/syntax.k`: `Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Call`,
`Subscript`, `Slice`, `NoBound`, `Int`, `ListExpr`, `While`, `Compare`,
`CmpOp`, `BinOp`, `If`, `Expr`, `Attribute`, `AugAssign`, and `Return`.

The material execution path is:

- `core.k` loads and sequences the module, performs scope-chain lookup,
  evaluates call arguments left-to-right, allocates monotonically, and defines
  `vsLen`;
- `functions.k` installs the exact closure and implements return/frame pop;
- `call.k` evaluates the callee before arguments, dereferences builtin list
  arguments, dispatches the exact selected builtin/method/closure, and
  preserves the continuation in the pushed frame;
- `subscript.k` dereferences the source list, evaluates slice bounds in order,
  builds indices `0,3,6,...`, allocates the slice, and performs positional
  reads;
- `sort.k` handles the resolved `"sorted"` builtin and allocates exactly
  `list(sortVS(slice))`;
- `list.k` allocates `result=[]` and performs `append` as an in-place write to
  the exact receiver heap location;
- `operators.k` and `int.k` dispatch `<`, `==`, `%`, `//`, and `+` after their
  operands evaluate in the declared order;
- `builtins.k` resolves `len(list(VS))` to `vsLen(VS)`;
- `controls.k` implements assignment, `If`, `While`, loop continuation,
  `AugAssign`, and effect-discarding expression statements.

The loop circularity matches the actual `#while` term after the source
`While` rule and preserves an arbitrary continuation. It introduces no
`return`, frame pop, exception, break, cleanup, or continuation discard.
On the true path the fixed rules execute lookup, arithmetic, branch selection,
indexing, append, and increment before the circularity can recur. On the false
path fixed semantics removes the while term. Its heap and scope footprint
matches precisely the cells changed by those operations.

Priority analysis found no candidate priority rule. Supplied priority rules on
heap dereference, list allocation/mutation, and cell handling select the
specific behavior before generic dispatch; their guards and receiver/value
sorts match the intended path. Rules for unrelated AST constructors, callee
names, continuations, and value sorts in the exhaustively inventoried supplied
files are pattern-disjoint from reachable configurations here.
`MPY-CONCRETE` is imported only by the LLVM runtime module and is absent from
the proof module, as intended.

### Result-bearing fixed primitive

`sortVS` is declared by the byte-identical supplied `sort.k` as a total,
no-evaluator, symbolic function and is reached only after ordinary name lookup
selects the fixed `"sorted"` builtin. It is an external builtin operation,
not program-defined code and not a candidate-created proof shortcut. The
symbolic theorem is interpretation-parametric in this primitive; the
human-facing ordering conclusion is conditional on the named supplied
contract that `sortVS` is the ascending permutation of its input.

The supplied concrete rules implement insertion sort for integer and string
lists. Reviewer concrete execution, the grounded K theorem, and the
independent Python differential run support that boundary on their finite
domains. They do not purport to prove the universal sort contract.

`valSeqAt` is also a fixed total function. Its constructor equations implement
ordinary in-bounds access; access into symbolic `sortVS(VS)` remains an opaque
value. On intended inputs, the indices used by the loop are in bounds because
`sortVS`'s named permutation contract preserves the slice length. This is part
of the same fixed primitive boundary, not an unconstrained proof-local oracle.

No inventoried candidate-local rule has a false-conclusion witness on the
intended domain. Accordingly, none is labeled unsound.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation grounds
the entry at `[5,6,3,4,8,9,2]` and demands
`[2,999,3,4,8,9,5]`. This is demonstrably false because index 1 is not
divisible by three and must remain 6.

The generated module first passed `kprove --dry-run` with exit 0:
[`15-fresh-false-dry-run.log`](evidence/15-fresh-false-dry-run.log). The real
proof then exited 1 with `WarnStuckClaimState`. Its irreducible actual heap
contains:

```text
2 |-> list(vCons(2, vCons(6, vCons(3, vCons(4,
     vCons(8, vCons(9, vCons(5, .ValSeq))))))))
```

That does not unify with the target containing 999. See
[`make_fresh_false_spec.py`](evidence/make_fresh_false_spec.py) and
[`16-fresh-false-kprove.log`](evidence/16-fresh-false-kprove.log). The failure
is the expected unmet result obligation, not a parser error, timeout,
unreachable claim, or unrelated crash.

I separately tested body sensitivity. Both appearances of the actual executed
branch constructor in the entry claim—inside `#loadAll` and the expected
loaded closure—were changed from `i % 3` to `i % 2`, while the original result
obligation was retained. The mutation passed dry-run, then exited 1 with a
residual whose closure contains `Int(2)` and whose actual result is
`[2,6,2,4,4,9,5]`. See
[`make_body_mutation_spec.py`](evidence/make_body_mutation_spec.py),
[`17-body-mutation-dry-run.log`](evidence/17-body-mutation-dry-run.log), and
[`18-body-mutation-kprove.log`](evidence/18-body-mutation-kprove.log). This
changes the program term actually executed by the theorem; it is not merely an
external source-file change.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For an arbitrary finite constructor sequence `VS`, assuming normal execution
under the supplied semantics, the exact submitted function returns a fresh
result list characterized as follows. Let:

```text
T = sortVS(buildVS(VS, 0, vsLen(VS), 3))
```

For each index `i` from 0 to `vsLen(VS)-1`, the result element is
`valSeqAt(T, i/3)` when `i mod 3 = 0`, and `valSeqAt(VS,i)` otherwise. The
proof also establishes the exact three allocations and final control cells
described in Stage 4. The loop claim is symbolic and unbounded; there is no
fixed list length or bounded unrolling.

This is partial correctness. A separate liveness theorem is not claimed,
although concrete and ground executions terminate.

### Trust and evidence ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293, Haskell backend, SMT, and K's builtin Int/Map/List theories | All symbolic closure | Standard accepted proof-tool trusted base |
| Byte-identical supplied MPY semantics | Translation from MPY constructors to scope, heap, control, and value behavior | Required fixed semantics for this condition; integrity checked and material path reviewed |
| Trusted `py2mpy.py` | Bridge from `solution.py` to `solution.mpy` | Accepted transliteration boundary; byte regeneration and normalized constructor identity checked |
| Fixed `sortVS` contract | Determines values at indices divisible by three and supplies the word “sorted” | Acceptable external-builtin boundary; explicitly conditional, not candidate-defined; supported but not universally proved by finite concrete/differential evidence |
| Fixed total `valSeqAt` on an opaque `sortVS` result | Names each selected sorted value | Acceptable as part of the same sort/permutation boundary; constructor access rules are ordinary, intended indices are in bounds |
| Structural-induction arguments for concatenation associativity/right identity | Allows accumulator normalization in the loop proof | Ordinary mathematics over the exhaustive two-constructor datatype; equations and overlaps checked above |
| Positional formula to prompt prose | Human-facing adequacy bridge | Direct index arithmetic: `buildVS` selects exactly `0,3,6,...`, and `i/3` enumerates the sorted slice at those positions |
| Reviewer differential and concrete suites | Supports implementation/primitive bridge on tested cases | Finite empirical evidence only; never substituted for K reachability closure |

Proof-local `sortThirdResult` has `no-evaluators`, but it is not listed as an
assumption: its universal folding equation fixes it to the complete
`mergeThirdFrom` expression, and the fresh wrong-result mutation is rejected.
Other opaque float, keyed-sort, digest, or string helper symbols present in the
supplied semantics are listed in the exhaustive inventory but are unreachable
and have no dependent claim here.

The formal precondition does not materially narrow the HumanEval contract: it
quantifies over an arbitrary finite `ValSeq` and has no size or value bound.
Exceptional heterogeneous comparisons, user-defined comparison side effects,
and other CPython behaviors not represented by the supplied MPY subset are
outside the fixed model rather than restrictions introduced by the candidate.
For the material HumanEval normal-return domain, the claim covers empty and
arbitrarily long finite lists.

Gate A passes: the theory is sound on the real program, result-constraining,
and non-vacuous. Gate B passes: the symbolic domain and positional result match
the full material contract under the fixed `sorted` primitive. Gate C passes:
all assumptions, evidence, commands, and exclusions are reproducible and
separated from what K proves.

VERDICT: PASS
LEGITIMACY: LEGIT
