# Independent adversarial audit: 141-file-name-check

The candidate's six claims can be rebuilt and each prints `#Top`, but the
proof is not legitimate. Its proof-only operational rules replace the three
result-bearing string computations with total opaque symbols. No equation or
bridge-free connection theorem relates those symbols to the supplied
semantics. Worse, the extended theory proves concrete false conclusions:

- `"a.txt"` returns `"No"` when the opaque dot count is interpreted as 0;
- `"a.txt"` returns `"No"` when the dot count is correct but the opaque head
  code is interpreted as 48; and
- `"a.pdf"` returns `"Yes"` when dot, head, and digit observations are correct
  but the opaque suffix predicate is interpreted as `true`.

All three claims build and jointly close with `#Top`; the real candidate and
canonical Python functions have the opposite results on these ASCII inputs.
The decisive evidence is
[`evidence/bridge_false_witnesses.k`](evidence/bridge_false_witnesses.k) and
[`evidence/bridge_false_witnesses.log`](evidence/bridge_false_witnesses.log).

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so there is no
mode/mount contradiction requiring `AUDIT_ERROR`.

The recursive, no-symlink integrity check found:

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `1346cfd15de72531685d9c4a09fb6a7b459df3852a0d84cd6a0632a0a1c32e5b`);
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py` (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`);
- the candidate's entire `reference-semantics/` tree is recursively identical
  to the trusted tree; and
- neither candidate nor trusted input trees contain symlinks.

There are no missing, additional, changed, mistyped, or symlinked entries
inside the candidate semantics tree. See
[`evidence/stage1_integrity.sh`](evidence/stage1_integrity.sh) and
[`evidence/stage1_integrity.log`](evidence/stage1_integrity.log).

Four requested provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. I read the available
`prove.sh`, `kprove.out`, `concrete-run.out`, and candidate tests only as
untrusted claims. In particular, the five-byte candidate `kprove.out`
containing `#Top` was not reused. The candidate's `__pycache__` was ignored,
and no candidate-built definition or cache was copied into scratch.

The clean source copy and exact copy commands are recorded in
[`evidence/prepare_scratch.sh`](evidence/prepare_scratch.sh) and
[`evidence/prepare_scratch.log`](evidence/prepare_scratch.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt says that a string is valid exactly when:

1. it contains no more than three ASCII digits `'0'` through `'9'`;
2. it contains exactly one dot;
3. the nonempty prefix starts with an ASCII Latin letter; and
4. the suffix after the dot is exactly `txt`, `exe`, or `dll`.

The generated `solution.py` implements that literal contract. With exactly
one dot, `len >= 5`, and a last-four-character value in
`.txt/.exe/.dll`, the unique dot must be the suffix separator and the prefix
must be nonempty. The explicit `ord` ranges implement the ASCII-letter
condition, and summing ten one-character `count` calls implements the
ASCII-digit condition over the whole name.

The trusted translator was rerun from the scratch copy:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0, and the regenerated and submitted `solution.mpy` files are byte
identical with SHA-256
`fbf977102870b192415a1efc8f17c21adba0b8aeb4667595e7bc8ab41e58777a`.
See [`evidence/translation_identity.log`](evidence/translation_identity.log).

### Independent differential

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports `/reference/canonical.py` and the clean scratch `solution.py`. It
tests the documented examples, empty strings, dot-count and length
boundaries, all first-letter boundaries, all suffix branches, the three/four
digit boundary, an exhaustive generated family over a mixed ASCII/Unicode
alphabet, and 750 seed-141 random strings.

The exact 3,331 inputs and all results are preserved in
[`evidence/differential_inputs.json`](evidence/differential_inputs.json) and
[`evidence/differential_results.json`](evidence/differential_results.json).
The command exited 0 with:

```text
input_count=3331
candidate_vs_canonical_mismatches=131
candidate_vs_contract_mismatches=0
canonical_vs_contract_mismatches=131
```

The 131 mismatches are a real canonical/intent discrepancy, not a candidate
implementation error relative to the literal prompt. Python's canonical
implementation uses Unicode-wide `isalpha()` and `isdigit()`, while the
prompt explicitly says Latin `a-z/A-Z` and digits `0-9`. For example:

- `"é.txt"`: canonical `Yes`, candidate and literal contract `No`;
- `"Ω.exe"`: canonical `Yes`, candidate and literal contract `No`; and
- `"a١٢٣٤.txt"`: canonical `No`, candidate and literal contract `Yes`.

This finite differential supports program-to-prompt fidelity only on the
tested inputs. It is not used as a K proof or as a universal connection
theorem.

## 3. Clean proof reconstruction

All work was performed below
`/tmp/audit-work/141-file-name-check`. The copied semantics came from the
trusted reference mount, not from a candidate cache. Tool versions and paths
are in [`evidence/tool_versions.log`](evidence/tool_versions.log): K
v7.1.337, Python 3.10.12, and Z3 4.12.1.

### Concrete definition

The supplied semantics was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The build exited 0. The compiler emitted pre-existing non-exhaustive-match
warnings in supplied, mostly unused total functions; none concerns a
candidate-local file. The initial attempt to use a nonexistent
`/home/agent/.nix-profile/bin/kompile` path exited 127; the installed tools
were then resolved at `/usr/bin`, and the clean build succeeded. Both attempts
are visible in [`evidence/concrete_build.log`](evidence/concrete_build.log).

The reviewer-authored ASCII test program exercises every source branch and
both digit boundaries. It was translated with the trusted translator and
executed under the fresh LLVM definition. `krun` exited 0 with `.K`, `NoExc`,
and exit code 0. See
[`evidence/k_concrete_ascii_tests.py`](evidence/k_concrete_ascii_tests.py) and
[`evidence/concrete_ascii_run.log`](evidence/concrete_ascii_run.log).

A second concrete test containing `é` failed at the supplied semantics'
documented ASCII-only `strToCodes` rule, exiting 113. This is a concrete
language-model boundary, not evidence against the ASCII proof cases. The
failed command is preserved in
[`evidence/k_concrete_tests.py`](evidence/k_concrete_tests.py) and
[`evidence/concrete_run.log`](evidence/concrete_run.log).

### Proof definition and all positive claims

The exact copied `verification.k` was freshly compiled with Haskell:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

The command exited 0. See
[`evidence/proof_build.log`](evidence/proof_build.log).

The unmodified `spec.k` was proved as one six-claim module; `kprove` exited 0
and printed `#Top`
([`evidence/positive_all_claims.log`](evidence/positive_all_claims.log)).
For independent per-claim runs, the reviewer added only selection labels; the
complete diff is in
[`evidence/label_positive_claims_v2.log`](evidence/label_positive_claims_v2.log).
Each of the six individually selected claims then exited 0 and printed
`#Top`. The final log audit is
[`evidence/positive_final_status.log`](evidence/positive_final_status.log).

Two of the first six simultaneous individual runs were killed with backend
code 137 under resource pressure. They were rerun sequentially and both
closed; the failed parallel runs and successful retries remain visible in
the evidence. This transient resource event is not used as a candidate
verdict.

Thus the verification gate succeeds under the candidate's extended theory.
The later static gate shows why that theory is invalid for the real program.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Every claim starts with the same realizable empty module state:
environment 0, scope 0 empty with builtins parent -1, no heap or stack,
`scopeLoc` 1, `heapLoc` 0, `noRet`, `NoExc`, and exit code 0.

The six claims say:

1. If opaque `charCount(CS,'.') != 1`, return `"No"`.
2. If that count is 1 but fixed `isLen(CS) < 5`, return `"No"`.
3. If the count is 1, length is at least 5, but
   `latinCode(headCode(CS))` is false, return `"No"`.
4. If the earlier predicates pass but opaque `allowedSuffix(CS)` is false,
   return `"No"`.
5. If the earlier predicates pass but opaque `digitCount(CS) > 3`, return
   `"No"`.
6. If the earlier predicates pass and opaque `digitCount(CS) <= 3`, return
   `"Yes"`.

The destinations explicitly constrain the returned `str` value; they are not
free-variable or implication-only postconditions. They also require all
listed state cells to be restored.

Concrete satisfying witnesses under the intended observation interpretation
are:

| Claim | Witness | Both Python results |
|---|---|---|
| dot-count rejection | `abc.txt.txt` | `No` |
| short rejection | `.txt` | `No` |
| first-character rejection | `1.txt` | `No` |
| suffix rejection | `a.pdf` | `No` |
| digit rejection | `a1234.txt` | `No` |
| acceptance | `a123.txt` | `Yes` |

The exact code sequences, observation values, initial state, and results are
in [`evidence/claim_witnesses.py`](evidence/claim_witnesses.py) and
[`evidence/claim_witnesses.log`](evidence/claim_witnesses.log).

### Program term and control-flow pinning

The entry `<k>` cell does not load `solution.mpy` through the fixed
`#loadAll(Module(...))` rule. It starts at the fresh
`runFileNameCheck(CS)` symbol. That rule directly calls a closure whose body
is extracted from a manually embedded `solutionModule`.

This is not a different current body: parsing the regenerated submitted module
and a source rendering extracted from `solutionModule` to normalized KORE
produced byte-identical terms, both with SHA-256
`45bfcf183b2cb690ce8864c32ce324111fc898b67d9fff086129fa98e5872d2b`.
See
[`evidence/embedded_module_identity_v2.log`](evidence/embedded_module_identity_v2.log).
The body then executes through the supplied closure-call, parameter binding,
statement sequencing, assignment, return, and frame-pop rules.

Nevertheless, the theorem bypasses module loading and the installation of the
`file_name_check` binding in scope 0. There is no auxiliary reachability claim
connecting actual module load plus lookup/call to `runFileNameCheck`. For this
specific nonrecursive function, whose module has no other statements and whose
body does not look up its own global name, I found no concrete false return
caused by that wrapper. I therefore record this as a manual pinning/evidence
gap rather than label the wrapper itself unsound. It is not the basis of the
verdict.

There are no loops or helper-function claims. All five source `if` statements
and six returns occur in the embedded real body. The material adequacy failure
is instead that three branch values are produced by unconstrained oracles.

## 5. Rule-by-rule static soundness review

There is no candidate `semantic.k` and no generated helper K file. The
selected semantics is the recursively verified supplied tree. An extracted
declaration/rule index for that tree is preserved at
[`evidence/reference_semantics_declaration_inventory.txt`](evidence/reference_semantics_declaration_inventory.txt).
The exhaustive candidate-local inventory below is reconstructed from
`verification.k`, not from candidate prose.

### Local syntax, functions, totals, and opaque symbols

| Lines | Declaration and attributes | Assessment |
|---|---|---|
| 9-10 | `charCount(IntSeq,Int):Int [function,total,symbol,no-evaluators]` | Result-bearing opaque symbol; no equations or connection theorem. `[total]` supplies definedness, not string-count meaning. |
| 11-12 | `headCode(IntSeq):Int [function,total,symbol,no-evaluators]` | Result-bearing opaque symbol; no equations or connection theorem. |
| 13 | `suffix4(IntSeq):IntSeq [symbol]` | Opaque result of a skipped real slice. |
| 14-15 | `suffixIs(IntSeq,Int):Bool [function,total,symbol,no-evaluators]` | Result-bearing opaque symbol; no equations, index coverage, or connection theorem. |
| 61 | `latinCode(Int):Bool [function,total]` | One unconditional arithmetic equation; truthful and complete. |
| 66 | `allowedSuffix(IntSeq):Bool [function,total]` | Complete definition as the OR of three `suffixIs` observations, but it inherits their lack of meaning. |
| 70 | `digitCount(IntSeq):Int [function,total]` | Complete definition as the sum of ten `charCount` observations, but it inherits their lack of meaning or nonnegativity. |
| 80 | `solutionModule:Module [function]` | Fresh definitional name for the exact current translated AST; normalized identity checked independently. |
| 169 | `moduleBody(Module):Stmts [function]` | Partial structural projection, used only on the one matching embedded module. |
| 174 | `runFileNameCheck(IntSeq):KItem` | Fresh entry wrapper; it invokes the embedded body rather than the submitted module loader. |

There are no local `[simplification]` rules, `[functional]` declarations,
claims, lemmas, or additional imported proof-local modules. Six rules have
`priority(40)`; no other local rule has a priority.

### Every local rule

| Lines | Rule/classification | Static decision |
|---|---|---|
| 19-23 | Count-call operational bridge | Preempts the supplied bound-method dispatch and recursive `cntSub` calculation at the fully evaluated call redex. It preserves framed cells and continuation, but replaces the result with unconstrained `charCount`. Materially unsound as a real-program bridge. |
| 27-30 | Index-0 operational bridge | Preempts supplied `applyIndex/intSeqAt` when fixed `isLen >= 5`. State/control are preserved, but the returned character is unconstrained `headCode`. Materially unsound as a real-program bridge. |
| 34-38 | `[-4:]` operational bridge | Preempts fixed bound evaluation and `doSlice/buildIS`. The skipped bound is a pure literal `-4`, so no side effect is lost, but the slice value becomes opaque `suffix4` without a connection theorem. It is part of the unsound suffix bridge set. |
| 42-47 | `.txt` equality operational bridge | Replaces fixed structural string equality with unconstrained `suffixIs(CS,0)`. Materially unsound. |
| 48-53 | `.exe` equality operational bridge | Same defect for index 1. |
| 54-59 | `.dll` equality operational bridge | Same defect for index 2. |
| 62-64 | `latinCode` equation | Ordinary, globally true ASCII-range mathematics; no overlap or coverage issue. |
| 67-68 | `allowedSuffix` equation | A nonrecursive, complete definition of a fresh name. It is logically consistent, but it does not connect `suffixIs` to the real suffix. |
| 71-76 | `digitCount` equation | A nonrecursive, complete definition of a fresh name. It is logically consistent, but it does not connect `charCount` to real counts. |
| 81-167 | `solutionModule` equation | Ground, terminating definition. The emitted term matches the trusted translation after parser normalization. |
| 170-172 | `moduleBody` equation | Truthful structural projection on its exact match domain; no `[total]` claim. |
| 175-179 | `runFileNameCheck` operational wrapper | Executes the exact embedded body using supplied call rules. It skips module binding and lacks a universal connection claim, but no false result for the current nonrecursive body was found from that omission. Narrower pinning gap, not an asserted unsound equation. |

The six priority bridges are pairwise separated by redex shape; the three
suffix comparisons have distinct constants. Their intended overlaps are with
the lower-priority/default supplied call, subscript, slice, and comparison
rules that they preempt. Priority selects the shortcuts but provides no
equivalence proof.

### Used-construct mapping and state/control review

[`evidence/program_constructs.log`](evidence/program_constructs.log) inventories
every source AST construct and operator. The used fixed-semantics paths are:

- `Module`, `FuncDef`, and statements are declared in `semantics/syntax.k`.
  Fixed module load and function binding are in `core.k:123-127` and
  `functions.k:13-16`; the entry wrapper bypasses those two steps.
- Closure call, left-to-right argument evaluation, a fresh callee scope,
  parameter binding, return, continuation restoration, and frame deletion are
  in `core.k:183-191`, `call.k:69-75`, and `functions.k:62-90`.
- Name lookup and builtin binding are in `core.k:129-181`.
- `Expr`, `Assign`, and `If` use `controls.k:8-18,46-54`.
- integer and ASCII string literals use `core.k:193-196` and
  `str.k:12-17`.
- generic call/attribute routing uses `call.k:15-32`; fixed string count would
  use `methods.k:33-44`, but the local count bridge preempts it.
- `len` and `ord` use `builtins.k:19-26,142-145`.
- fixed string index and slicing would use `subscript.k:25-69` and
  `subscript.k:108-121`; the two local subscript bridges preempt them.
- `BoolOp`, unary `not`, and unary minus use `bool.k:8-25`,
  `operators.k:10`, and `int.k:7`.
- integer `+`, inequalities, and equality use `operators.k:12-17` and
  `int.k:9-27`. Fixed string equality is `str.k:25-26`, but the suffix
  comparison bridges preempt it.

Evaluation order before count and suffix equality is preserved: receiver,
callee, and arguments have cooled to values before those bridges match. The
slice bridge skips evaluation of the literal `-4` bound, which is pure. The
program allocates no heap objects. The supplied call rule creates scope 1,
binds `file_name`, writes the three locals, then the return/pop rules restore
environment 0, delete the callee scope, restore `scopeLoc` 1, clear `ret`, and
resume the framed continuation. The bridges mention only `<k>`, so heap,
stack, environment, exception, and exit cells are framed. I found no
state/control mismatch for these pure operations. Their result values are the
fatal mismatch.

### Required false-conclusion witnesses

The three bridge defects above are not merely missing evidence. The reviewer
constructed ground claims with the complete candidate configuration:

1. Count witness: for real `"a.txt"`, set only opaque
   `charCount(CS,46) = 0`; the theory proves `"No"` although both Python
   functions return `"Yes"`.
2. Head witness: for `"a.txt"`, keep dot count 1 and fixed length at least 5,
   but set opaque `headCode(CS) = 48`; the theory again proves `"No"` although
   both Python functions return `"Yes"`.
3. Suffix witness: for `"a.pdf"`, keep dot count 1, head code 97, and digit
   count 0, but set `suffixIs(CS,0) = true`; the theory proves `"Yes"` although
   both Python functions return `"No"`.

`kprove` first dry-ran the three-claim module successfully, then exited 0 with
`#Top`. These ground preconditions are satisfiable because they constrain
otherwise unconstrained total symbols; the suffix case is also projected to
QF_UFLIA and Z3 returns `sat` with an explicit model in
[`evidence/oracle_precondition_sat.smt2`](evidence/oracle_precondition_sat.smt2)
and
[`evidence/oracle_precondition_sat.log`](evidence/oracle_precondition_sat.log).
An earlier single `"a.pdf"` witness is retained in
[`evidence/oracle_false_witness.log`](evidence/oracle_false_witness.log).

These are concrete false conclusions on the intended ASCII input domain.
They meet the witness requirement for labeling the result-bearing bridge sets
unsound.

## 6. Fresh non-vacuity test

The candidate did not provide `spec-vacuity.k`. I created a fresh mutation
that keeps the complete acceptance precondition but changes its required
result from `"Yes"` to `"No"`. The concrete input `"a123.txt"` satisfies the
precondition under the intended interpretation, and both Python
implementations return `"Yes"`.

The mutation is
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k). Its `--dry-run` parsed
and built successfully with exit 0
([`evidence/vacuity_dry_run.log`](evidence/vacuity_dry_run.log)). The actual
proof exited 1 with `WarnStuckClaimState`. The residual `<k>` cell is:

```text
str(iCons(89, iCons(101, iCons(115, .IntSeq)))) ~> .K
```

which is `"Yes"`, while the mutated destination requires `"No"`. This is the
expected unmet result obligation, not a parser error, timeout, missing import,
or unrelated crash. See
[`evidence/vacuity_proof.log`](evidence/vacuity_proof.log).

Therefore the claims are result-constraining and non-vacuous within the
extended theory. This stage passes, but it cannot cure the unsound operational
bridges exposed in Stage 5.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the supplied MPY semantics plus the candidate's proof-local rules, the
six claims establish this conditional control-flow fact:

> Starting from the exact empty module-state cells in `spec.k`, the exact
> embedded function body returns the branch result selected by the values of
> `charCount`, `headCode`, and `suffixIs`, and its call frame and local state
> are cleaned up.

The six preconditions partition the possible values of those total symbols,
so the proof characterizes the body relative to one consistent but arbitrary
interpretation of the symbols. It does **not** establish that those values are
the count, first character, and last-four-character suffix of `CS`.

### Trust ledger

| Boundary | Dependents | Status |
|---|---|---|
| Supplied `reference-semantics` and K builtins/backend | All execution and proof steps | Selected trusted semantics level; candidate copy has exact integrity. |
| Trusted `/reference/py2mpy.py` | Source-to-`.mpy` identity | Acceptable trusted input; byte identity was independently regenerated. |
| Manually embedded `solutionModule` | All six entry claims | Normalized AST identity is independently checked, but the proof itself has no file/module-load connection theorem. Limited manual bridge. |
| `charCount` plus count bridge | Dot branch and all digit branches | Illegitimate program-derived oracle; concrete opposite-result witness closes. |
| `headCode` plus index bridge | First-character branch | Illegitimate program-derived oracle; concrete opposite-result witness closes. |
| `suffix4`, `suffixIs`, slice and equality bridges | Suffix branches and final acceptance | Illegitimate program-derived oracle set; concrete opposite-result witness closes. |
| `latinCode`, `allowedSuffix`, `digitCount` equations | Spec preconditions | The equations themselves are consistent definitions, but the latter two inherit illegitimate opaque inputs. |
| Python differential and LLVM tests | Intent/source and finite semantics evidence | Empirical only; they do not repair or replace the missing universal connections. |
| Termination | Partial-correctness interpretation | The theorem is reported only as reachability/partial correctness. The submitted body is straight-line, but termination is not used to justify an opaque result. |

The opaque operations are program-defined computations, not fixed external
primitives outside the theorem. The candidate supplies no bridge-free
auxiliary theorem for any of them. Reusing each same symbol in execution and
the precondition is circular correlation, not a proof of meaning.

### Decision

Clean reconstruction and fresh non-vacuity both succeed, and the currently
embedded body matches the translated source. Nevertheless, the proof-local
theory demonstrably proves false return values for concrete intended-domain
inputs. This is a material Gate A soundness failure and meets the decision
boundary for `FAIL / NOT_LEGIT`. The missing provenance files and Unicode
canonical discrepancy are additional audit limitations, not the reason for
converting a valid proof into a failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
