# Independent adversarial audit: 156-int-to-mini-roman

## Executive conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
generated program over the complete source-contract domain
`1 <= number <= 1000`.

The decision does not rely on the candidate's compiled definitions, generation
report, or prior `#Top`. From source-only copies, K 7.1.293 rebuilt a standalone
Haskell semantics definition and a separate Haskell proof definition. The sole
positive target claim then exited 0 with `#Top`. Trusted translation is
byte-identical, the claim's expanded program is constructor-identical to that
translation, all 1,000 allowed Python inputs agree with the trusted canonical
implementation, 27 independently selected K executions agree with both Python
implementations, a changed executable body invalidates the old theorem, and a
fresh false result obligation is rejected for the expected semantic reason.

The proof-local `miniRoman` function is not an oracle or operational bridge. It
is a one-equation abbreviation for the exact digit-table expression produced by
normal execution. The actual program body still executes under the generated
semantics. The exhaustive local rule review found no false or execution-
bypassing rule on the intended domain.

## 1. Input and provenance integrity

### Record layout and required records

`/audit-input.json` declares:

- problem `156-int-to-mini-roman`;
- condition `bare`;
- record layout `pipeline-v3`;
- semantics mode `GENERATED_SEMANTICS`; and
- `mount_reference_semantics: false`.

Every required pipeline-v3 record is a real regular file, and the candidate,
generation root, and structured-trace root are real directories. This includes
`/run.json`, `/task.json`, `/generation-result.json`, all seven required
generation-evidence files, the structured trace, and all three trusted
reference files. There are no symlinks anywhere under `/candidate`,
`/reference`, or `/generation-evidence`. As required for generated semantics,
`/reference/reference-semantics` does not exist.

The campaign-lock JSON is exactly equal as a JSON object to the campaign block
embedded in `/audit-input.json`; its raw SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Run/task/config/problem/session/invocation/status/output fields are coherent.

The independent checker recomputed every launcher-recorded file hash. It also
recomputed the pipeline-v3 tree digest of the mounted candidate as
`88d32ed87cae8c8a0b2c01040bf93bb7b49ff1e25839af5d8687197ef49d1e43`,
exactly the workspace digest in both the generation result and invocation.
Likewise, the structured trace's pipeline tree digest is
`387f37016cdb87a7cbe7cdcfad8bb4779229c135d358b42e64932706787a59c9`,
exactly `usage.json`'s source-trace digest. The trace contains one regular
JSONL file, 253/253 lines parse as JSON, and its raw digest matches the
per-file generation result.

`/audit-input.json` also records launcher-side aggregate tree values
`ef2f...` for the candidate and `c1ab...` for the trace without declaring that
serialization. I did not equate those opaque aggregate values to the separately
defined pipeline-v3 tree algorithm. Mounted content identity is independently
established by the matching pipeline workspace/source-trace digests and every
per-file generation-evidence digest.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounts. The required proof sources `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh` are all present as regular files.
Candidate-provided `semantic-kompiled/`, `verification-kompiled/`, and
`__pycache__/` were treated only as untrusted debris and never used.

### Generation evidence inspection

I read the run/task/result/invocation/metrics/runtime/usage records, the
generation prompt and last message, bounded portions plus a proof/action index
of the 513,087-byte output log, and a structural index of every structured
trace record. Those records claim a successful generation and prior `#Top`,
but no later audit conclusion relies on that claim.

Evidence:

- `evidence/integrity_check.py`
- `evidence/integrity.log` — all checks pass
- `evidence/run_generation_records.sh`
- `evidence/generation_records.log`
- `evidence/inspect_generation.py`
- `evidence/generation_trace_inspection.log`

Stage result: **PASS; no infrastructure breach**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt and canonical source require
`int_to_mini_roman(number)` to return the lowercase Roman-numeral equivalent of
a positive integer, with the explicit restriction `1 <= number <= 1000`.
Documented examples are `19 -> "xix"`, `152 -> "clii"`, and
`426 -> "cdxxvi"`.

The candidate is a different but valid algorithm. It indexes standard
thousands, hundreds, tens, and ones tables using:

```text
thousands[number // 1000]
+ hundreds[(number % 1000) // 100]
+ tens[(number % 100) // 10]
+ ones[number % 10]
```

For the stated domain, the thousands index is 0 or 1 and every other index is
0 through 9, so every lookup is in range.

### Trusted regeneration

Exact command:

```text
python3 ../trusted/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exit 0. Both terms have SHA-256
`90b1a4e45486fbbd3a5be66547e7bc69e2c73314fe305a1da1c5e4bc992a2f38`.
Thus submitted `solution.mpy` is the byte-exact output of the trusted translator
on submitted `solution.py`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical entry point and
the candidate entry point independently. It checks:

- all three prompt examples;
- contract endpoints 1 and 1000;
- all digit/subtractive boundaries around 4, 5, 9, 10, 40, 50, 90, 100,
  400, 500, 900, and 1000;
- 100 deterministic representative generated inputs; and
- exhaustively every integer from 1 through 1000.

There are zero mismatches in 1,000/1,000 contract cases. The complete result
mapping has digest
`cd2c90e0b5e4b37f04abaead85ff5ca3e6f97ca72eee551e58d9b6f8528bcd2d`.
An “empty” case is not meaningful for an integer-valued contract; the evidence
records that explicitly rather than inventing a widened type domain. Inputs 0
and 1001 are retained only as excluded-domain diagnostics and do not support
the theorem.

Evidence:

- `evidence/differential_inputs.json`
- `evidence/differential_test.py`
- `evidence/run_source_fidelity.sh`
- `evidence/source_fidelity.log`

Stage result: **PASS; exact translation and full finite-domain behavioral
agreement**.

## 3. Clean proof reconstruction

Only the six candidate source artifacts and the trusted translator were copied
to `/tmp/audit-work/final-reconstruction`. No candidate compiled definition or
cache was copied. The logged clean commands were:

```text
kompile semantic.k --backend haskell \
  --main-module MINI-PYTHON \
  --syntax-module MINI-PYTHON-SYNTAX \
  --output-definition semantic-audit-kompiled

kompile verification.k --backend haskell \
  --main-module ROMAN-VERIFICATION \
  --syntax-module MINI-PYTHON-SYNTAX \
  --output-definition verification-audit-kompiled

kprove spec.k \
  --definition verification-audit-kompiled \
  --spec-module ROMAN-SPEC
```

Both builds exit 0. Source inspection finds exactly one positive claim,
`int-to-mini-roman-correct`. Its independent `kprove` run exits 0 and prints
exactly `#Top`.

The separately built standalone semantics was exercised on 27 normal and
boundary inputs. Every `krun` exits 0, ends with `<k> .K </k>`, and returns the
same lowercase string as both Python implementations. These inputs include 1,
3, 4, 5, 8, 9, 10, all decimal/subtractive transition points, all prompt
examples, 944, 999, and 1000.

One portability observation is retained rather than suppressed: a fresh LLVM
build succeeds, but LLVM `krun` exits 113 at the first `tupleAt(..., 0)` because
the helper equations are marked as simplifications. The submitted workflow
explicitly selects Haskell for execution and proof, and the separately built
Haskell semantics executes successfully. This is an LLVM-backend portability
limitation, not a failure of the reconstructed Haskell theorem or a narrowing
of the source-contract domain.

Evidence:

- `evidence/run_reconstruction.sh`
- `evidence/reconstruction.log`
- `evidence/concrete_semantics_test.py`
- `evidence/run_concrete_semantics.sh`
- `evidence/concrete_semantics.log`
- `evidence/run_llvm_portability_probe.sh`
- `evidence/llvm_portability.log`

Stage result: **PASS for the candidate's declared Haskell execution/proof
backend**.

## 4. Adequacy and real-program pinning

### Claim in plain language

The sole entry claim starts with:

- `<k>` equal to `romanProgram`;
- an arbitrary K integer `N` in `<input>`;
- exactly an empty map in `<env>`;
- exactly `noResult` in `<result>`; and
- precondition `1 <= N <= 1000`.

It requires execution to reach:

- an empty computation `.K`;
- the same input `N`;
- an existentially arbitrary final map; and
- exactly `result(vStr(miniRoman(N)))`.

The free final environment is harmless because the source contract constrains
only the return value. The result cell is not free, framed away, or related by
a one-way implication; it is fixed to the result summary for the same input.
The precondition is plainly satisfiable, for example by `N=1`, `N=19`, and
`N=1000`.

For the satisfying witness `N=19`, substitution into the defining equation
gives the thousands/hundreds entries `""`, tens entry `"x"`, and ones entry
`"ix"`, hence `"xix"`. Fresh K execution, candidate Python, and trusted
canonical Python all return `"xix"`. The same checks give `"i"` for 1 and
`"m"` for 1000.

### Mechanical program identity

The expanded `romanProgram` macro and the freshly parsed submitted
`solution.mpy` each produce a 7,086-byte KAST with identical SHA-256
`ed918df70996fb9d225d7ed47e3be97c7b7e932c83305ef191da8c6538222905`.
Their byte comparison exits 0. Combined with trusted byte regeneration, this
mechanically pins the claim to the submitted function binding and complete
body.

The macro is a parse-time name, not a runtime rule that summarizes execution.
All assignments, literals, arithmetic, lookups, concatenations, and return
control remain in the term executed by the fixed generated semantics.

### Body sensitivity

The reviewer body mutation changes the actual executable constructor term:
the ones-table entry for index 9 becomes `"wrong"` while the result obligation
continues to demand the unmutated `miniRoman(9)` (`"ix"`). The mutated
definition builds successfully. Its ground proof exits 1 with a final
configuration containing:

```text
<result> result ( vStr ( "wrong" ) ) </result>
```

and cannot unify with the destination. This is genuine body sensitivity, not a
change to an external source file that leaves the theorem's term untouched.

Evidence:

- KAST identity in `evidence/reconstruction.log`
- `evidence/verification-body-mutation.k`
- `evidence/spec-body-mutation.k`
- body-mutation portion of `evidence/mutations.log`

Stage result: **PASS; satisfiable, result-constraining, and mechanically pinned
to the real generated program**.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is in `evidence/RULE_INVENTORY.md`. Its counts match
the source lexically: 24 `semantic.k` rules, 2 `verification.k` rules, and 1
`spec.k` claim. It enumerates every local syntax declaration and alternative,
the four-cell configuration, each control frame, both semantic functions, the
macro, the proof-local result function, every rule guard/attribute, and the
claim.

### Construct coverage

Every constructor used by `solution.mpy` is declared and mapped:

- module/function/parameter and statement lists;
- assignment and return;
- names, integer and string literals;
- string-literal tuples;
- binary `//`, `%`, and `+`;
- tuple subscript; and
- the evaluation/control frames needed for their order.

There are no locally declared `total` or explicit `functional` symbols, opaque
symbols, priority or `owise` rules, anywhere rules, heating/cooling contexts, or
auxiliary/circular claims.

### Semantic helper equations

`tupleStrings` has a true empty equation and a structurally descending
string-literal equation. It is used only on the submitted program's pure
`Str(...)` tuple elements.

`tupleAt` has two disjoint rules: index zero returns the head, and a positive
index recurses on the tail with index minus one. The recursion descends. On the
entry precondition:

```text
N / 1000                    is in 0..1
(N mod 1000) / 100          is in 0..9
(N mod 100) / 10            is in 0..9
N mod 10                    is in 0..9
```

against tables of respective lengths 2, 10, 10, and 10. Therefore R03/R04
truthfully and completely define every result-bearing use. Negative tuple
indexes, out-of-range exceptions, tuples with effectful/non-string elements,
and multi-function modules are deliberately outside this individually
generated subset; none is reachable from the submitted term under a satisfying
entry input.

### Evaluation, state, and control

The entry rule binds the sole parameter to `<input>` in the initially empty
environment and begins the exact body. Sequencing is left to right.
Assignments evaluate before updating the map. Name lookup is guarded by
membership. Binary expressions evaluate left before right and preserve the left
value; subscripts evaluate the base before the index. Return evaluation
discards the remaining entry-function continuation, then changes only
`noResult` to `result(V)` and ends at `.K`. This is the correct control footprint
for the call-frame-free, single-entry-function subset used here.

K `/Int`, `modInt`, `+Int`, and `+String` are standard imported primitives.
All source divisors are positive constants and all source operands are
nonnegative under the precondition, so K division/modulo coincide with Python's
floor-division/modulo behavior. String concatenation preserves order. The
unused integer-addition rule is also mathematically true.

### Verification extensions

`romanProgram` is only the constructor-identical macro audited in stage 4.
It does not preempt an operational rule.

`miniRoman(N)` has one unconditional defining equation whose right-hand side is
the exact four lookup-and-concatenate expression that fixed execution produces.
It introduces no fresh value and has no overlapping equation. It is a
definitional summary, not an operational bridge: the function body still
executes, and the body-sensitivity mutation fails. Although the equation
contains the task's Roman tables, it cannot prove a substituted result because
normal execution independently constructs those same table values and indexes.

No rule inventory item enables a false conclusion on an intended input. Thus
there is no candidate unsoundness allegation requiring a false-conclusion
witness. The separately recorded LLVM limitation concerns executable placement
of simplification equations in another backend, not the validity of an equation
or the Haskell proof.

Evidence:

- `evidence/RULE_INVENTORY.md`
- `evidence/inventory_counts.log`

Stage result: **PASS; no unsound semantic or proof rule on the real
program/domain**.

## 6. Fresh non-vacuity test

The reviewer-authored mutation leaves the executable program, precondition, and
all semantics unchanged, but changes the required result to:

```text
result(vStr(miniRoman(N) +String "!"))
```

It is demonstrably false for every satisfying input; for the explicit witness
`N=1`, the real result is `"i"` rather than `"i!"`.

The mutation is a valid parsed/built spec: `kprove` begins semantic execution
and reaches the final implication. It then exits 1 with
`WarnStuckClaimState`. The residual explicitly compares the real four-table
concatenation with that same concatenation plus `"!"`. This is the expected
unmet result obligation, not a parser error, missing import, timeout, backend
crash, or unreachable mutation.

Exact command:

```text
kprove spec-false-result.k \
  --definition verification-audit-kompiled \
  --spec-module ROMAN-SPEC-FALSE-RESULT
```

Evidence:

- `evidence/spec-false-result.k`
- `evidence/run_mutations.sh`
- `evidence/mutations.log`

Stage result: **PASS; the proof is discriminating and non-vacuous**.

## 7. Proven versus assumed accounting

### Precisely proven

Under the submitted generated K semantics plus its imported K builtins, for
every K integer `N` satisfying `1 <= N <= 1000`, execution of the exact
trusted-translator-generated program from an empty environment and `noResult`
reaches `.K` with:

```text
result(vStr(
  thousands[N / 1000]
  + hundreds[(N mod 1000) / 100]
  + tens[(N mod 100) / 10]
  + ones[N mod 10]
))
```

where the four tables are exactly the lowercase tables in the submitted body.
The final environment is intentionally unconstrained. This is a
result-constraining reachability/partial-correctness theorem about the actual
submitted program term, not about an external source filename or a substituted
summary program.

### Trust and evidence ledger

| Boundary | Dependents | Status and support |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell backend and reachability logic | All machine-checked conclusions | Standard proof-engine trust boundary; version logged and clean builds rerun. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, list syntax, and `BASIC-K` primitives | Arithmetic, strings, bindings, sequencing | Standard low-level semantics boundary. Their use is direct; no candidate redefinition. |
| CPython AST translator | Python-to-`solution.mpy` bridge | Trusted mounted translator; fresh byte-exact regeneration. |
| `romanProgram` macro identity | Real-program pinning | Mechanical expanded-KAST identity, not an informal assertion. |
| Generated entry adapter and subset semantics versus Python | Meaning of the K execution | Exhaustive static construct/rule audit plus 27 fresh K/Python comparisons across all material boundaries. |
| `tupleAt` and `miniRoman` equations | Result value and postcondition | Truthful, descending/definitional equations with complete coverage for all actual index ranges; no opaque interpretation. Body and result mutations reject the opposite behavior. |
| Trusted canonical Python and the natural-language Roman intent | Summary-to-contract bridge | Independent canonical implementation; exhaustive zero-mismatch comparison for all 1,000 allowed integers, plus direct standard-table inspection. This evidence is not substituted for the K proof. |
| Haskell backend choice | Concrete execution and proof | Explicit candidate choice and successful clean reconstruction. LLVM placement of simplification equations is not claimed. |

### Excluded behavior

The theorem does not cover integers outside 1..1000, non-integer Python inputs,
negative/out-of-range tuple indexing, Python exceptions, arbitrary tuple
elements, multiple functions, general Python module execution, I/O, heap
objects, or another K backend. Those exclusions do not narrow the stated
HumanEval contract or omit any construct/control effect used by this submitted
program on a satisfying input.

### Gate accounting and decision

- Real-program soundness/non-vacuity: **PASS**.
- Intent/domain adequacy: **PASS**; the formal domain is exactly the explicit
  1..1000 source domain, not a finite under-approximation of an unrestricted
  contract.
- Trust/evidence auditability: **PASS**; sources, scripts, exact commands,
  statuses, bounded logs, exhaustive Python inputs, K executions, and both
  mutations are preserved.

The LLVM portability note is not a material adequacy gap because neither the
candidate nor this reconstruction claims an LLVM proof/execution result. The
Haskell semantics used by the theorem is independently executable on the
contract boundaries. No fatal or non-fatal soundness limitation remains in the
claimed theorem itself.

VERDICT: PASS
LEGITIMACY: LEGIT
