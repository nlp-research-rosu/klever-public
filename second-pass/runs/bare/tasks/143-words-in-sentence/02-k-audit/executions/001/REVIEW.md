# Independent adversarial audit: 143-words-in-sentence

This audit used the required `using-kit`, `writing-semantics`, and
`validating-proof` workflows. Everything from `/candidate` was treated as
untrusted evidence. Candidate-built definitions were never used. Source inputs
needed for execution were copied explicitly to `/tmp/audit-work/rebuild`, and
all rebuilt definitions were created there.

Headline decision: **CONCERNS / LEGIT**. The proof reconstructs, constrains the
return value, is non-vacuous, and can be pinned to the byte-regenerated submitted
program. I found no local rule that enables a false conclusion for a satisfying
input in the intended domain. The concerns are limitations in the bridge from a
small, program-specialized generated semantics to Python/natural-language
intent, one over-broad totality annotation outside all theorem uses, and
unreproducible candidate-supplied testing claims. Those limitations do not
substitute an oracle for the program or make the reconstructed theorem false.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist; `/reference` contains only `canonical.py`, `prompt.py`, and
`py2mpy.py`. This is the required trusted-mount shape, so there is no
infrastructure breach. Evidence: `evidence/36-provenance-integrity.log`.

### Required artifacts and types

The following are present as regular, non-symlink files:

- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and the JSONL generation trace;
- `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

There are no symlinks anywhere below `/candidate`. The candidate also contains
extra generated state—`__pycache__/`, `semantic-kompiled/`, and
`verification-kompiled/`. Those entries are not source integrity failures, but
they were ignored and not copied. Their definitions, caches, traces, and
reported outputs played no role in reconstruction.

Candidate `prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256 `85e7c088...ca8e1`). Candidate `py2mpy.py` is byte-identical to
`/reference/py2mpy.py` (SHA-256 `406485ea...db16`).

The structured trace has 299 valid JSON lines and no malformed line. The
metadata, trace, `codex-last.txt`, and `codex-output.log` claim a successful run,
two prompt examples, 2,000 randomized checks, and three `#Top` proof stages.
They also contain earlier stuck-claim records. None was trusted. In particular,
there is no candidate test/differential/random script supporting the claimed
2,000 checks, so that claimed evidence receives no credit. The audit replaced it
with an independent script and input record.

The complete hashes, artifact types, trace summary, metadata values, and
candidate final claim are preserved in:

- `evidence/36-provenance-integrity.log`
- `evidence/inspect_provenance.py`
- `evidence/01-scratch-setup.log`

No required source artifact is missing, changed relative to a trusted mounted
counterpart where such a counterpart exists, mistyped, or symlinked.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py`, the function receives a sentence of length 1–100,
consisting of words/letters separated by spaces. It must retain exactly the
words whose lengths are prime, preserve their order, and return them joined by a
single space. The examples require:

- `"This is a test"` → `"is"`
- `"lets go for swimming"` → `"go for"`

The trusted canonical implementation uses `sentence.split()`, determines
compositeness by divisibility, treats length 2 as prime, appends selected words,
and joins them with one space.

The submitted `solution.py` uses `split(" ")` and the explicit prime-length
table from 2 through 97. On the intended length bound, that table is complete.
Empty pieces from repeated spaces have length zero and are not selected, so even
that diagnostic behavior agrees with the canonical result. Tabs/newlines and
other whitespace are outside the stated “separated by a space” domain.

### Trusted translation and byte identity

The trusted translator was run on the scratch copy:

```text
python3 /tmp/audit-work/rebuild/py2mpy.py \
  /tmp/audit-work/rebuild/solution.py \
  > /tmp/audit-work/rebuild/regenerated-solution.mpy
```

The submitted and regenerated files both have SHA-256
`616c3c91...bc10e`; `cmp` exited 0. Evidence:
`evidence/02-regenerate-mpy.log`.

### Independent differential test

`evidence/differential_test.py` independently loads
`/reference/canonical.py` and `/tmp/audit-work/rebuild/solution.py`. It does not
reuse any K equation or proof summary. It records every input and both outputs
in `evidence/differential-inputs.jsonl`.

Scope:

- both documented examples;
- empty input as an out-of-contract diagnostic;
- minimum length, all-skipped, first-selected, skipped-before-selected,
  selected-before-skipped, and multiple-selected accumulator branches;
- every single word length 0–100;
- every adjacent length pair 1/2 through 99/100;
- repeated/leading/trailing spaces as diagnostics;
- the 97, 98, 99, 100 and whole-sentence length-100 boundaries;
- 5,000 deterministic generated ASCII-letter sentences of total length at most
  100 (seed `14320260723`).

Result: 5,215 cases, zero mismatches, exit 0. Evidence:
`evidence/03-differential.log` and the 5,215-line JSONL input record.

Conclusion: the submitted Python implementation is materially equivalent to
the trusted canonical function on the intended domain.

## 3. Clean proof reconstruction

### Toolchain and clean builds

The independently available tools are `/usr/bin/kompile`, `/usr/bin/krun`, and
`/usr/bin/kprove`, all K `v7.1.293`. Evidence:
`evidence/44-toolchain-version.log`.

Only source copies in `/tmp/audit-work/rebuild` were used. Fresh Haskell
definitions were built into new audit-named directories:

| Definition | Command log | Exit |
|---|---|---:|
| concrete/executable `audit-semantic-kompiled` | `evidence/04-kompile-semantic.log` | 0 |
| proof `audit-verification-kompiled` | `evidence/05-kompile-verification.log` | 0 |

The Haskell backend supports both concrete execution and proof. An additional,
non-required LLVM portability experiment failed at compile time because LLVM
rejects RHS-only `SY`/`SZ` variables in the unused generic concatenation rule
(`semantic.k` lines 139–143); see `evidence/43-kompile-semantic-llvm.log`.
This does not invalidate the successful fresh Haskell concrete definition or
the proof backend, but it is a portability concern.

### Concrete generated-semantics reconstruction

The actual regenerated `solution.mpy` was passed to `krun`, rather than the
proof-side `solutionProgram` abbreviation. Final `<result>` cells agree with
independent CPython results:

| Input | Python result | Fresh K evidence |
|---|---|---|
| `"This is a test"` | `"is"` | `evidence/07-krun-example-1.log` |
| `""` | `""` | `evidence/09-krun-empty.log` |
| `"a"` | `""` | `evidence/10-krun-minimum-1.log` |
| `"  aa   bbb  "` | `"aa bbb"` | `evidence/11-krun-repeated-spaces.log` |
| length-100 `aa` + space + 97 `b`s | the whole sentence | `evidence/12-krun-length-100-2-plus-97.log` |
| 100 `a`s | `""` | `evidence/15-krun-length-100-composite-pretty.log` |

The independent Python values for the same boundary set are in
`evidence/08-python-concrete-expected.log`.

Two discarded audit diagnostics are preserved for transparency:
`evidence/06-krun-example-1.log` used the wrong split form of `-cNAME=VALUE`
and was corrected by log 07; `evidence/13-krun-length-100-composite.log`
encountered pretty macro expansion on a separately hand-entered string and was
replaced by the exact submitted boundary string in logs 14–15. Neither was a
candidate execution failure.

### Positive claims

Every claim in `spec.k` was run independently. A claim was accepted only when
the command exited zero and printed `#Top`.

| Claim | Log | Result |
|---|---|---|
| `loop-invariant` | `evidence/16-kprove-loop-invariant.log` | `#Top`, exit 0 |
| `symbolic-contract` using the separately proved loop lemma | `evidence/17-kprove-symbolic-contract.log` | `#Top`, exit 0 |
| `example-one` | `evidence/18-kprove-example-one.log` | `#Top`, exit 0 |
| `example-two` | `evidence/19-kprove-example-two.log` | `#Top`, exit 0 |
| `length-boundaries` | `evidence/20-kprove-length-boundaries.log` | `#Top`, exit 0 |
| `composite-hundred` | `evidence/21-kprove-composite-hundred.log` | `#Top`, exit 0 |

The symbolic command marks `loop-invariant` trusted only after the same source
claim has independently closed in log 16. This is proof composition, not an
unproved candidate assumption.

## 4. Adequacy and real-program pinning

### Plain-language preconditions and postconditions

1. `loop-invariant` (`spec.k` lines 8–18):
   the front of `<k>` is the submitted loop body over any finite `WordSeq`;
   `result` and `word` hold arbitrary strings; the remainder map contains
   neither key; functions, result cell, and following computation are framed.
   The postcondition consumes the loop, preserves the framed cells and
   continuation, and replaces the environment by `loopEnv`, which selects all
   remaining qualifying words and leaves `word` at its final iteration value.

2. `symbolic-contract` (lines 22–32):
   there is no `requires` clause. For any K string `S`, empty function/local
   stores and `NoneVal` result execute program load, invocation, and the
   result-preserving cleanup harness. The final computation and stores are empty
   and the returned value is exactly
   `selectedWords(splitWords(S), "")`.

3. `example-one` and `example-two` (lines 34–54):
   the same empty initial stores with fixed prompt strings must finish with
   results `"is"` and `"go for"` respectively.

4. `length-boundaries` (lines 58–69):
   the same empty initial state with a 100-character `2 + 1 + 97` input must
   return that entire two-word input.

5. `composite-hundred` (lines 71–81):
   the same empty initial state with one 100-character word must return the
   empty string.

All preconditions are satisfiable. A ground loop state with `WS = WNil`,
`A = ""`, `OLD = "old"`, `RHO = .Map`, empty functions, and `NoneVal` result
satisfies the helper claim and closes in
`evidence/33-kprove-empty-loop-witness.log`. The concrete entry state
`S = "aa bbbb ccc"` satisfies the symbolic entry claim and returns `"aa ccc"`
in `evidence/32-kprove-concrete-entry-witness.log`; both Python
implementations return the same value. The four fixed candidate claims
themselves exhibit satisfying entry states.

### Program identity

The candidate entry claims use `load(solutionProgram)`, not a filesystem read.
That is acceptable only if the abbreviation is pinned to the submitted term.
The audit established the connection in three independent steps:

1. trusted translation is byte-identical to submitted `solution.mpy`
   (`evidence/02-regenerate-mpy.log`);
2. `evidence/make_program_identity_spec.py` generated a claim whose RHS is the
   regenerated AST (with the parser's omitted empty `Stmts` unit made explicit);
   that claim prints `#Top`, exit 0
   (`evidence/31-kprove-program-identity.log`);
3. changing the first implementation-list element from `Int(2)` to `Int(4)`
   builds successfully but leaves the identity claim stuck
   (`evidence/40-identity-mutation-dry-run.log` and
   `evidence/41-identity-mutation-failure.log`).

The identity claim is reported by K as trivial because definitional function
normalization makes both ASTs identical; that is exactly the equality being
checked. Together with byte regeneration, it pins the proof-side program to the
real submitted `.mpy`.

The loop helper also matches real control flow: the `For` rule produces
`loop("word", splitWords(S), BODY)`, and `BODY` is definitionally the submitted
`solutionLoopBody`. No helper claim replaces invocation or return.

The returned value is not free or existential. Every entry claim rewrites
`<result>` to a fixed concrete string or to the deterministic
`selectedWords(splitWords(S),"")`. `finishProgram` clears only function/local
maps and leaves `<result>` unchanged; it cannot manufacture the claimed value.

## 5. Rule-by-rule static soundness review

The fully expanded inventory, including every local syntax production,
attribute, rule, claim, and construct mapping, is
`evidence/rule-inventory.md`. The following is the exhaustive decision summary.

### Declarations and configuration

`semantic.k` declares:

- `Program`, `Stmts`, the five `Stmt` forms (`FuncDef`, `Assign`, `For`, `If`,
  `Return`), `Params`, `Exprs`, `CmpOps`;
- the four `Value` forms and seven `Expr` forms;
- `CmpOp`, `WordSeq`, `splitWords`, stored `Function`;
- seven computation items (`load`, `invoke`, `exec`, `execStmt`, `loop`,
  `put`, `choose`);
- `memberInt` and `conditionalAppend`;
- configuration cells `<k>`, `<functions>`, `<env>`, and `<result>`.

`verification.k` declares `solutionPrimes`, `solutionLoopBody`,
`solutionBody`, `solutionProgram`, `contractPrimes`, `primeLength`,
`appendSelected`, `selectedWords`, `loopEnv`, `wordEnv`, `finishProgram`,
`wellFormedWords`, and `renderWords`.

There are no local priority, simplification, concrete, owise, macro,
functional, fresh/existential, or explicitly opaque declarations. No generated
helper K file exists beyond these two modules and `spec.k`.

### All 22 semantic rules

| IDs | Decision |
|---|---|
| S1–S2 `splitWords` | Disjoint `findString == -1` / `>= 0` cases; recursive suffix strictly shrinks; preserves empty pieces exactly like `split(" ")`. Sound subject to trusted K string primitives. |
| S3–S5 load/invoke | Correctly load the one definition, look up its body, and initialize the parameter environment. Missing-binding/global/exception cases are outside the submitted program. |
| S6–S8 statement execution and string assignment | Correct sequence order and map update. |
| S9–S12 for/loop/put | Exact submitted split iterator; per iteration, update `word`, execute the body, recur. `put` requires an existing target, which the submitted initialization guarantees. |
| S13–S14 `memberInt` | Correct finite integer membership and descending recursion; intentionally stuck for non-`Int` AST list elements, which never occur. |
| S15 `conditionalAppend` | Exhaustive Boolean rule with exact empty/nonempty accumulator behavior. |
| S16 exact nested `If` | Atomic, program-specialized operational rule. It derives the condition from `lengthString(W)` and the AST-provided `NUMS`; it does not call `contractPrimes` or another answer oracle. Its sole effect is exactly the submitted nested branch's `result` update, with no skipped state/control effect in the modeled fragment. |
| S17–S19 equality `If`/choose | Correct string comparison and branch execution. S16 atomically preempts these for the submitted nested conditional. |
| S20 name assignment | Correct on existing bindings; bypassed by S16 in the real run. |
| S21 concatenation assignment | Guard fixes both operands to strings; exact left-associated AST concatenation. Bypassed by S16. RHS-only guard variables prevent LLVM compilation but are uniquely determined on Haskell/reachable use. |
| S22 return | Correctly writes the tail return value. It would not implement abrupt unwinding for a hypothetical non-tail `Return`; the real return is final, so no intended input reaches such a context. |

S16 is the main trust concern. It is recognizable as the semantics of the exact
used conditional, not a rule encoding “prime word” directly: replacing the
submitted list's `2` with `4` makes both mutated CPython and fresh K return
`""` for `"aa"` (`evidence/37-body-sensitivity-setup.log` and
`evidence/38-krun-body-sensitivity.log`). The proof-side identity mutation also
fails. There is no hidden generic Python reference semantics or bridge-free
universal connection theorem in this mode, so the CPython connection remains
audited reasoning plus finite evidence. No satisfying intended input was found
on which S16 enables a false conclusion.

### All 18 verification rules

| IDs | Decision |
|---|---|
| V1–V4 `solution*` | Exact definitional AST constants; byte regeneration and the identity/mutation claims establish program pinning. |
| V5 `contractPrimes` | Exactly the primes in 0–100. Independent trial division confirms equality (`evidence/42-prime-table-check.log`). |
| V6–V9 selection functions | `primeLength`, `appendSelected`, and both `selectedWords` equations are truthful, exhaustive on their declared inputs/constructors, disjoint, and descending. |
| V10–V12 environment summaries | `wordEnv` base/step and guarded `loopEnv` exactly summarize the loop map shape used by the claim. |
| V13 `finishProgram` | Proof harness, not a Python operation. It clears function/local maps after invocation and preserves result. Acceptable for a return-value theorem; it deliberately proves nothing about those cleared maps. |
| V14–V18 well-formed/render helpers | Structurally truthful, disjoint, descending, and completely unused by all six claims. |

`wordEnv` is marked `[total]`, but its step equation requires an existing
string-valued `"word"` key. For example,
`wordEnv(WCons("x", WNil), .Map)` has no defining equation. This is a real
global totality-coverage gap. It is not used on such a map: the loop
precondition always supplies `"word" |-> Str(OLD)`, and recursion preserves
that shape. I therefore do not label it an intended-domain unsound rule; there
is no false result equality witness for any entry-state input. It remains a
documented concern and should be fixed by removing `[total]` or adding truthful
coverage before reusing the module generally.

The `primeLength` name is mathematically adequate only within the stated
length bound. For 101 it returns false because the finite table stops at 97,
but length 101 is outside the intended domain, and the symbolic theorem itself
faithfully characterizes the submitted implementation rather than asserting
unbounded mathematical primality.

### All six claims and used-construct coverage

The six claims are C1 loop invariant, C2 symbolic entry contract, C3–C4 prompt
examples, and C5–C6 length boundaries. There are no other claims or imported
proof lemmas.

Every constructor in `solution.mpy` is covered:

- `Module`/`FuncDef`/`Params` by load and invoke;
- statement lists and literal assignments by `exec`;
- `For`/`Call`/`Attribute`/`split` by S1–S2 and S9–S12;
- outer `If`/`Compare`/`CmpOp("in")`/`ListExpr`/`Int`/`len` by S13–S16;
- nested equality, name assignment, and `BinOp` by the exact S16 effect (with
  the narrow unused S17–S21 rules also present);
- the final `Return` by S22.

Unsupported variants stop with residual syntax; no fallback fabricates a
result. Evaluation order, loop control, map updates, calls, and returns are
sound for the actual control path. The semantics intentionally does not model
general Python exceptions, globals, arbitrary iterators, non-tail returns, or
non-string operands.

No materially unsound rule was identified, so there is no unsupported
“unsound” label without the false-conclusion witness required by the audit
standard. The narrower coverage and totality gaps above are recorded as such.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists, so none was credited. The audit created
`evidence/spec-vacuity-audit.k` with a fresh concrete mutation:

- satisfying input: `"aa"`;
- truthful result: `"aa"` because length 2 is selected;
- deliberately demanded result: `""`.

The mutation parses and builds successfully under `kprove --dry-run`, exit 0
(`evidence/34-vacuity-dry-run.log`). The actual proof exits 1 with
`WarnStuckClaimState`; its final state has empty computation/stores and
`<result> Str("aa")`, which cannot unify with the false destination
(`evidence/35-vacuity-proof-failure.log`).

This is the expected unmet result obligation, not a parser error, timeout,
missing import, or unrelated crash. It establishes that the positive proof
discriminates the returned value.

The separate program-identity mutation in logs 40–41 is operational/body
sensitivity evidence, not a substitute for this false-postcondition test.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the reconstructed `MPY-SEMANTIC` plus audited verification definitions:

1. for every finite `WordSeq` and every accumulator/environment satisfying the
   loop claim's key-disjointness condition, the submitted loop body transforms
   the environment exactly as `loopEnv`;
2. for every K string `S`, executing the pinned submitted AST from the formal
   empty state and then the cleanup harness terminates with return cell
   `Str(selectedWords(splitWords(S), ""))`;
3. the two examples and two explicit 100-character boundaries have their
   stated concrete results.

This is a result-constraining partial-correctness proof of the modeled program,
not merely a test replay. The loop theorem is universal over algebraic word
sequences; the entry theorem is universal over K strings.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| K toolchain and Haskell backend correctness | all builds/proofs | Necessary low-level trust boundary. Fresh source builds and exact outputs are recorded. |
| Imported `INT`, `STRING`, `BOOL`, `MAP`, `K-EQUAL` operations, especially `lengthString`, `findString`, `substrString`, string concatenation, Boolean/integer equality, and map lookup/update | split, length test, accumulation, environments | Acceptable standard K primitives; not reproved locally. |
| Trusted `py2mpy.py` transliteration | Python-to-`.mpy` identity | Trusted mounted input; candidate copy is identical and fresh output is byte-identical. |
| Generated program-specialized semantics, especially S16 | connection from `.mpy` execution to Python behavior | Audited but not derived from a hidden/full Python semantics. Supported by direct rule analysis, concrete boundaries, body sensitivity, and finite differential testing. This is the principal reason for `CONCERNS`. |
| Finite prime table means mathematical primality for lengths 0–100 | natural-language intent | Ordinary mathematical bridge, independently checked by trial division; not a K theorem. Acceptable on the prompt bound. |
| Sentence-domain interpretation (“letters” organized as space-separated words) | canonical/intent alignment | Informal prompt bridge. Tests use ASCII letters and spaces; tabs/newlines/general Python whitespace are excluded. |
| `finishProgram` cleanup | final empty stores in entry claims | Explicit proof harness. It preserves result and does not support any value conclusion; acceptable but excludes claims about post-call maps. |
| Separate proof of loop claim before `--trusted` reuse | symbolic entry proof | Machine-checked in log 16, then assumed only for theorem composition in log 17. Acceptable. |
| Candidate-reported 2,000 random checks and prior `#Top` | none | Untrusted and not used; no test artifact exists. |
| Reviewer differential/concrete tests | Python/intent/semantics bridges on tested values only | Finite empirical support, not a substitute for the K proof or a universal semantics theorem. |

### Decision

The clean proof succeeds, is non-vacuous, constrains the real returned value,
and is pinned to the byte-regenerated submitted program. The exact conditional
semantics consumes the implementation AST's list and is body-sensitive; it
does not replace the computation with an unconstrained or answer-bearing
oracle. The finite specification table is independently correct on the entire
intended word-length range. No material result divergence or intended-domain
false-rule witness was found.

The proof remains conditional on a small, generated, program-specialized
semantics whose connection to CPython is established by exhaustive static
reasoning for the used fragment plus finite evidence, not by a supplied
language definition or universal connection theorem. The globally over-broad
`wordEnv [total]`, the non-general tail-return model, LLVM portability failure,
and missing candidate random-test artifact further limit reuse/auditability.
These are genuine concerns but do not make the submitted theorem illegitimate
on its intended domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
