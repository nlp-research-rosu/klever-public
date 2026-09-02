# Independent adversarial audit: 70-strange-sort-list

The reconstructed K claims are real, sound, result-constraining proofs of the
submitted program for their stated bounded inputs. They are not a proof of the
HumanEval contract over its intended domain: symbolic coverage stops at list
length 4, followed by only two concrete length-5 examples. No claim covers an
arbitrary finite integer list. That is a material adequacy failure, so the
candidate is not a legitimate proof of the requested task.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains exactly
the expected regular files:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` does not exist. This is the required boundary
for generated semantics; there is no trusted or inferred hidden language
definition and no infrastructure contradiction. See
[01-input-integrity.log](evidence/01-input-integrity.log).

### Candidate artifacts

All required candidate source artifacts are present as regular files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. The submitted `prompt.py` and `py2mpy.py` are also regular files.
There are no symlinked, mistyped, missing, or additional helper-K source
entries. Byte comparisons establish:

- candidate `prompt.py` equals `/reference/prompt.py`;
- candidate `py2mpy.py` equals `/reference/py2mpy.py`.

The candidate additionally contains `verification-kompiled/`. It is a generated
cache, not a source integrity failure, and it was neither copied nor used.
Candidate provenance material (`run-input.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, and the 200-line JSONL structured trace)
was read only as untrusted claims. It reports a final `#Top`, but also records
earlier parse, backend, and stuck-claim failures. None of it is used as proof
evidence. The bounded provenance extraction is
[02-provenance-claims.log](evidence/02-provenance-claims.log).

No required artifact integrity failure was found. `PROOF.md` is absent, but it
was not a deliverable in the recorded generation prompt and is not treated as a
missing source artifact.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `strange_sort_list(lst)` for a finite list of
integers. It must repeatedly take the minimum remaining element, then the
maximum remaining element, alternating until the list is empty. Duplicate
values remain separate occurrences. Examples are:

- `[1,2,3,4] -> [1,4,2,3]`;
- `[5,5,5,5] -> [5,5,5,5]`;
- `[] -> []`.

The trusted canonical implementation performs exactly that selection/removal
loop. It mutates the list object supplied to it. The generated implementation
instead sorts to a fresh list and recursively emits its first and last
elements. The prompt constrains the returned list, not input-object mutation,
so this side-effect difference is outside the stated result contract. The
generated algorithm terminates on every finite list because each recursive
call removes two elements.

### Translator identity

Running the trusted translator on the scratch copy of `solution.py` produced a
file byte-identical to the submitted `solution.mpy`; both have SHA-256
`0ec499bdee9f96aded681f7547ca22fe4b235b9c7375449a658c75dad26e3628`.
The translator and `cmp` both exited 0. See
[03-translation-identity.log](evidence/03-translation-identity.log).

### Independent differential reconstruction

[differential.py](evidence/differential.py) independently imports the trusted
canonical entry point and the scratch candidate entry point. Its complete
deterministic input corpus is preserved in
[differential-inputs.json](evidence/differential-inputs.json), SHA-256
`d7a0fa504ca2b4c05e5782781f388876eb5d0b33df98a6e0a0a7303bd07205df`.
The corpus covers:

- all prompt examples;
- lengths 0, 1, and 2 and both odd/even recursion boundaries;
- duplicates, negative integers, and arbitrary-precision integers;
- every tuple over `[-2,2]` through length 6;
- 500 deterministic generated cases with lengths through 20.

After deduplication, all 20,012 inputs were compared. Exit was 0 with zero
mismatches; see [04-differential.log](evidence/04-differential.log). This is
finite evidence for the implementation-to-contract bridge, not a replacement
for a K theorem.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/src`; trusted
inputs were copied separately to `/tmp/audit-work/reference`. Candidate
compiled definitions and caches were excluded. Builds and experiments wrote
only under `/tmp/audit-work` and `/audit-output`.

The independently installed live toolchain is K v7.1.293; `kup` is absent, but
`kompile`, `krun`, and `kprove` are available under `/usr/bin`. See
[00-toolchain.log](evidence/00-toolchain.log).

Fresh reconstruction produced:

1. An LLVM concrete definition from `semantic.k`, main module `SEMANTIC`,
   syntax module `MPY-SYNTAX`: exit 0
   ([05-kompile-concrete.log](evidence/05-kompile-concrete.log)).
2. A Haskell proof definition from `verification.k`, main module
   `VERIFICATION`, syntax module `MPY-SYNTAX`: exit 0
   ([06-kompile-proof.log](evidence/06-kompile-proof.log)).
3. Eight concrete `krun` executions of the submitted `solution.mpy`: empty,
   singleton, length 2, a prompt example, negative/duplicate odd length,
   lengths 6 and 7 outside the formal claim domain, and arbitrary-precision
   integers. Every run exited 0 and matched both Python implementations
   ([concrete_semantics_compare.py](evidence/concrete_semantics_compare.py),
   [07-concrete-semantics.log](evidence/07-concrete-semantics.log)).
4. The candidate has one positive target-proof invocation containing all 39
   unlabeled claims. Fresh `kprove spec.k --definition
   /tmp/audit-work/build/verification-kompiled --spec-module SPEC` printed
   `#Top` and exited 0
   ([08-kprove-positive.log](evidence/08-kprove-positive.log)).

Thus clean reconstruction succeeds. The final verdict is not based on a
timeout, container issue, malformed mount, or tool failure.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the entry claims

Every claim fixes:

- `<program>` to `solutionProgram`;
- `<entry>` to `"strange_sort_list"`;
- `<input>` to an exact `PList` shape;
- `<result>` from `pending` to one exact `pList(...)` value.

Claims 1–34 use the transparent postcondition
`strangeSpec(L) = weaveEnds(sortInts(L))`. In plain language, the program must
return the input sorted and then woven first/last/second/second-last. Claims
35–39 instead state exact ground result lists.

The precondition families are:

- claim 1: empty;
- claim 2: every singleton integer;
- claims 3–4: every length-2 integer list, split by insertion order;
- claims 5–10: every length-3 list, split into six insertion-sort paths;
- claims 11–34: every length-4 list, split into 24 insertion-sort paths;
- claims 35–37: the prompt examples;
- claims 38–39: two particular length-5 inputs.

The symbolic partitions for lengths 2, 3, and 4 are disjoint and exhaustive.
[claim_witnesses.py](evidence/claim_witnesses.py) found a satisfying concrete
state for every one of the 39 preconditions and substituted it into the claimed
result. Each result matched an independent direct implementation of the
natural contract and both Python implementations. The full witnesses are in
[09-claim-witnesses.log](evidence/09-claim-witnesses.log). The additional
partition check found zero uncovered assignments and zero overlaps for all
order/equality patterns tested
([09b-claim-partitions.log](evidence/09b-claim-partitions.log)).

### Execution and program identity

This semantics has no literal `<k>` cell. Its `<result>` cell is
computation-bearing: `pending` rewrites to `invoke(ENTRY,pList(INPUT),PGM)`,
after which the submitted function bodies are looked up and executed. The
absence of `<k>` is a representation choice, not an execution bypass.

The claims do not parse `solution.mpy` at proof time; they use the proof-local
constant `solutionProgram`. I therefore checked that connection explicitly:

1. parse the scratch copy of submitted `solution.mpy` to KORE;
2. evaluate `solutionProgram` under the fresh proof definition;
3. remove only K printer whitespace and `/* Inj: */` comments;
4. byte-compare the normalized KORE.

Both normalized terms have SHA-256
`fbcd66fcdde4f30578755c041016606b22618238bf7131a4e579161a5141e8c9`;
the comparison exited 0
([10b-program-pinning-success.log](evidence/10b-program-pinning-success.log)).
None of the program’s String tokens contains whitespace, so this normalization
does not erase a semantic difference. A fresh body mutation changing
`ordered[0]` to `ordered[999]` parsed successfully and made the same pinning
comparison fail at byte 3090
([solution-body-mutated.mpy](evidence/solution-body-mutated.mpy),
[10c-body-sensitivity.log](evidence/10c-body-sensitivity.log)).

An earlier exploratory attempt to reparse K's pretty-printed internal
`.Stmts` form failed at the MPY scanner and is retained in
[10-program-pinning.log](evidence/10-program-pinning.log). It is a test-harness
format mismatch, not candidate evidence; the decisive direct KORE comparison
above succeeds.

There are no helper or loop claims that replace real control flow. The
recursive `strange_sorted` body is executed through `invoke`, slicing, and
recursive calls. `weaveEnds` and `strangeSpec` occur only in the destination
postcondition.

### Result constraint and material scope gap

Every destination fixes the returned `PList`; there is no right-only free
variable, tautological implication, or unconstrained oracle. The fresh mutation
in stage 6 confirms that the result is discriminating.

However, no claim accepts an arbitrary `L:PList`. Even length 5 is not covered
universally: only `[3,-1,2,3,0]` and `[4,1,7,2,6]` are proved. No input of
length 6 or greater is covered at all. The natural-language domain is every
finite integer list, so the candidate omits infinitely many intended inputs.
Concrete success on such inputs cannot enlarge the theorem. This is the
material adequacy failure underlying the verdict.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[11-static-inventory.md](evidence/11-static-inventory.md). It enumerates all 36
local syntax declarations, the configuration, all 49 semantic rules, all five
verification rules, every `[function]` declaration, and all 39 claims.

There are:

- 21 semantic and three verification `[function]` declarations;
- no `[total]`, `[functional]`, `[simplification]`, `[concrete]`, priority,
  `owise`, `anywhere`, macro, or alias attributes;
- no opaque or fresh result symbol;
- no ordinary proof rule that accelerates or replaces program execution.

### Used-construct mapping

| Submitted construct | Declaration | Executing rules |
|---|---|---|
| `Module`, `FuncDef`, `Params`, statement lists | `semantic.k` 7–15 | startup, `invoke`, `invokeFind`, `exec`, `continue` |
| `If`, `Return` | `semantic.k` 10–13 | `execStmt`, `branch`, return propagation |
| `Name`, `Int`, empty/pair `ListExpr` | `semantic.k` 17–20 | `eval`, Map lookup, `makePair` |
| one-argument `Call` | `semantic.k` 21 | `eval(Call)`, `apply`, recursive `invoke` |
| integer `Compare("==")` | `semantic.k` 22 and 26 | `eval(Compare)`, `equal` |
| list `BinOp("+")` | `semantic.k` 23 | `eval(BinOp)`, `plus`, `append` |
| `UnaryOp("-")` | `semantic.k` 24 | `negate` |
| direct, negative, and slice `Subscript` | `semantic.k` 25, 27–29 | three `index` rules, `nth`, `interior`, `dropLast` |
| builtins `len`, `sorted` | call syntax | `length`, `sortInts`, `insertInt` |

`Assign` has syntax and one semantic rule but is unused. Every actual
constructor is modeled, and unmodeled syntax fails to parse rather than
fabricating a result.

### Control, state, overlap, and mathematics

The only state is a local Map carried through big-step statement execution.
Return propagation discards the remaining statement suffix; fall-through
preserves the updated environment. Both branch outcomes are covered. The
submitted expressions are pure, so the functional representation does not
hide an observable argument-evaluation order, exception, heap mutation,
allocation, or output effect.

Function lookup scans the exact fixed module; its two guards are disjoint.
`apply("len",...)`, `apply("sorted",...)`, and the guarded program-defined call
are disjoint. Insertion guards `I <=Int J` and `I >Int J` are disjoint and
exhaustive. The structural equations for length, append, drop-last, interior,
insertion sort, and weaving all descend on a strictly smaller list. `nth` is
intentionally partial for invalid indices; the program reaches it only with
valid indices. No `[total]` declaration turns a coverage gap into an axiom.

`solutionProgram` is an exact definitional constant, not a substituted
algorithm. `weaveEnds` and `strangeSpec` are transparent, terminating
definitions of the desired result. They share mathematical list primitives
with the semantics, but those primitives have complete ordinary equations on
every reachable use; there is no unconstrained oracle or circular rule of the
form “execute program expression as the postcondition symbol.”

The semantics is not a general Python semantics. For example, function
resolution hardwires unshadowed `len` and `sorted`, duplicate top-level
definitions would need different lookup behavior, and Python exceptions and
object identity are unmodeled. Those are narrower scope gaps, not unsound-rule
findings: the fixed submitted program has unique definitions, does not shadow
builtins, stays in bounds, and observes only integer-list return values. I found
no false conclusion witness for any rule on the intended input domain and
therefore make no materially unsound rule claim. The verdict is based on
missing theorem coverage, not on an alleged false rule.

## 6. Fresh non-vacuity test

The reviewer-authored mutation is preserved as
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k). For the satisfying ground
input `[1,2,3,4]`, it changes the required second result element from the true
`4` to the false `5`.

First,

`kprove /tmp/audit-work/src/spec-vacuity-audit.k --definition
/tmp/audit-work/build/verification-kompiled --spec-module
SPEC-VACUITY-AUDIT --dry-run`

successfully parsed and built the proof command, exiting 0
([12a-vacuity-build.log](evidence/12a-vacuity-build.log)).

The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its residual final configuration contains the real
`pList([1,4,2,3])`, which does not unify with mutated `pList([1,5,2,3])`.
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash. See
[12b-vacuity-proof.log](evidence/12b-vacuity-proof.log).

The submitted bounded claims are therefore non-vacuous and result-sensitive.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the generated `SEMANTIC` definition and K's builtin theories, invoking
the exact submitted translated program at `strange_sort_list` reaches the
specified `pList` result:

- for every mathematical-integer list of lengths 0 through 4; and
- for the two particular length-5 inputs in claims 38 and 39.

The result is `weaveEnds(sortInts(input))` for the symbolic families and the
stated concrete output for the ground examples. This is a partial-correctness
statement under the candidate semantics. It does not prove the general
arbitrary-length theorem.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 parser, Haskell/LLVM backends, reachability logic | all builds and proofs | Necessary low-level trust; fresh source builds and exact exit/output records make it auditable |
| K builtin `Int`, `Bool`, `String`, and `Map` theories | arithmetic, comparisons, environments | Acceptable primitive trust; K `Int` aligns with arbitrary-precision Python integers |
| Trusted `py2mpy.py` translation | program identity | Byte identity is established, not assumed |
| `solutionProgram` proof constant | all 39 claims | Machine-compared to submitted translated AST; body mutation is detected |
| Generated rules for one-argument calls, returns, and pure expressions | actual program execution | Statically audited and concretely exercised; narrow but sound for the fixed program |
| `len` and integer-list `sorted` models | both functions' results | Transparent `length` and insertion-sort equations; Python/K concrete comparisons support the intended builtin bridge |
| `PList` as Python integer-list values | inputs and results | Acceptable value abstraction for this pure return contract; aliasing, identity, and mutation equivalence are excluded |
| `weaveEnds(sortInts(L))` means alternating min/max removal | postconditions | Transparent mathematical definition plus independent witnesses/differential evidence; not an opaque symbol |
| Python differential testing | implementation/semantics bridges only | Finite empirical evidence (20,012 Python cases and eight K cases), never treated as a universal K proof |
| General termination and correctness for arbitrary list length | full HumanEval task | Not proved and not legitimately assumable |

### Gate accounting and decision

- Real-program soundness for each submitted claim: **PASS**. The actual AST is
  pinned, real bodies execute, equations are sound on reachable states, every
  precondition is satisfiable, and the false result is rejected.
- Intent adequacy: **FAIL**. Exact-length symbolic claims through 4 plus two
  ground length-5 examples do not express the contract for arbitrary finite
  integer lists.
- Evidence auditability: **PASS**. Fresh commands, statuses, scripts, inputs,
  mutation, and bounded logs are preserved under `evidence/`.

The finite claims are legitimate theorems, but they do not constitute the
requested task proof. The missing unbounded entry claim or recursion invariant
is a material theorem omission, not a mere thin-testing concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
