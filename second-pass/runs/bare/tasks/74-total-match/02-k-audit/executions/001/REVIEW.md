# Independent adversarial audit: 74-total-match

The candidate's K claims reconstruct successfully and are non-vacuous, and the
proof term is exactly the submitted translated program.  Nevertheless, the
generated semantics does not faithfully execute the real Python program over
the stated domain of lists of strings.  Its unrestricted bridge from Python
`len` to K's `lengthString` produces a different selected list for valid
Unicode input under both fresh concrete definitions.  Because the prompt does
not restrict strings to Latin-1, this is a material real-program semantics
failure rather than a thin-testing concern.

All candidate files were treated as untrusted and `/candidate` was not written.
Source was copied to `/tmp/audit-work`; no candidate-provided compiled
definition or cache was used.  Reviewer scripts and bounded logs are in
`/audit-output/evidence/`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:

- `/reference/reference-semantics` does not exist, as required for
  `GENERATED_SEMANTICS`.
- `/reference/prompt.py`, `/reference/canonical.py`, and
  `/reference/py2mpy.py` are regular trusted files.
- Every required candidate artifact is a regular file:
  `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
  `verification.k`, `spec.k`, and `prove.sh`.
- There are no symlinks anywhere under `/candidate`.
- Candidate `prompt.py` is byte-identical to trusted `/reference/prompt.py`
  (SHA-256
  `9662ed6743a83d0c34963151a98c5cdc9d33053cf3b26212adb7ff8abf9e3617`).
  Candidate `py2mpy.py` is byte-identical to the trusted translator (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
  These hashes also agree with the claims in `run-input.json`.

The complete checks, types, hashes, candidate inventory, and exit status are in
[stage1_integrity.log](evidence/stage1_integrity.log).  The scratch-copy hashes
are in [scratch_copy.log](evidence/scratch_copy.log).

`run-input.json` claims problem `74-total-match`, condition `bare`, and no
supplied semantics.  `metrics.json` claims generation exit 0 without timeout.
`codex-last.txt`, `codex-output.log`, and the structured trace claim five
successful concrete runs and a prior `#Top`.  The trace is valid JSONL with 177
records; its bounded extraction is
[generation_trace_extract.log](evidence/generation_trace_extract.log).
These are provenance claims only and were not used as proof evidence.

The candidate also contains `semantic-kompiled/`, `verification-kompiled/`,
`__pycache__/`, and the generation trace.  These are additional generated
build/cache/provenance artifacts, not trusted source.  Both compiled
definitions and all caches were ignored.  There is no candidate `PROOF.md` or
`spec-vacuity.k`; neither was a required generation deliverable, and a fresh
mutation was authored in stage 6.

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for two finite Python lists of strings, sum Python
`len` over each list; return `lst1` if its total is less than or equal to the
other total (including ties), otherwise return `lst2`.

Candidate `solution.py` is:

```python
def total_match(lst1, lst2):
    return lst1 if sum(map(len, lst1)) <= sum(map(len, lst2)) else lst2
```

On the intended built-in list/string domain this is algorithmically equivalent
to the trusted loop-based canonical implementation.  It also returns the
selected original list object, not a newly constructed list.

Running the trusted translator on the scratch copy produced SHA-256
`ac960b8284baa46acbba3e4283e333c889d6966fa5437803c59e000ab3e21766`,
byte-identical to submitted `solution.mpy`.  See
[stage2_translation.log](evidence/stage2_translation.log) and the preserved
[regenerated-solution.mpy](evidence/regenerated-solution.mpy).

The independent differential script imports the trusted and candidate entry
points separately.  Its complete deterministic input set contains:

- all five documented examples;
- 14 empty, tie, strict-boundary, long-string, NUL, and Unicode cases;
- all 961 pairs of lists of length at most two over
  `["", "a", "bb", "é", "🙂"]`;
- 1,000 seeded generated pairs.

All 1,980 cases agreed in value and selected input-list identity.  The branch
distribution was 864 first-list-strict, 337 ties, and 779
second-list-strict, with zero mismatches.  See
[differential_test.py](evidence/differential_test.py),
[differential_inputs.json](evidence/differential_inputs.json), and
[differential_test.log](evidence/differential_test.log).

Thus the Python implementation is faithful to the canonical implementation.
This finite differential evidence does not validate the K semantics.

## 3. Clean proof reconstruction

The live toolchain was K v7.1.293; versions and clean source-directory check
are in [tool_versions.log](evidence/tool_versions.log).

Fresh definitions were built from the copied `.k` sources:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled
```

Both exited 0.  Exact records are
[build_semantic_llvm.log](evidence/build_semantic_llvm.log) and
[build_verification_haskell.log](evidence/build_verification_haskell.log).

The original combined proof command exited 0 and printed `#Top`; the first two
definitional claims were reported as trivial:
[kprove_original_all.log](evidence/kprove_original_all.log).
For independent per-claim execution, I copied the five unchanged claims into
a labeled audit module and selected each label separately.  Every run exited 0
and printed `#Top`:

| Claim | Evidence |
|---|---|
| empty character total | [kprove_claim_empty_total.log](evidence/kprove_claim_empty_total.log) |
| cons character total | [kprove_claim_cons_total.log](evidence/kprove_claim_cons_total.log) |
| first list when no greater | [kprove_claim_first_no_greater.log](evidence/kprove_claim_first_no_greater.log) |
| second list when smaller | [kprove_claim_second_smaller.log](evidence/kprove_claim_second_smaller.log) |
| first list on tie | [kprove_claim_first_tie.log](evidence/kprove_claim_first_tie.log) |

The generated semantics was then executed from both fresh definitions.  Ten
normal and ASCII/Latin-1 boundary cases agreed with both Python
implementations, including empty lists, empty strings, strict branches, and
ties.  Two valid Unicode cases did not.  The decisive witness is:

```text
lst1 = ["🙂"]       Python total = 1
lst2 = ["ab"]      Python total = 2

trusted canonical result: ["🙂"]
candidate Python result:  ["🙂"]
fresh LLVM K result:       ["ab"]
fresh Haskell K result:    ["ab"]
```

Both `krun` commands exited 0.  Exact commands and output are in
[unicode_bridge_witness.sh](evidence/unicode_bridge_witness.sh) and
[unicode_bridge_witness.log](evidence/unicode_bridge_witness.log).
The complete 12-case runs and per-case commands are in
[compare_k_python_llvm_escaped_results.json](evidence/compare_k_python_llvm_escaped_results.json)
and
[compare_k_python_haskell_escaped_results.json](evidence/compare_k_python_haskell_escaped_results.json).
Those comparison commands exited 1 solely because each reported two semantic
mismatches.

A standalone fresh probe shows that concrete K evaluates
`lengthString("🙂")` as 4 and `lengthString("e\u0301")` as 3, while Python
reports 1 and 2 respectively
([run_string_measure_emoji.log](evidence/run_string_measure_emoji.log),
[run_string_measure_combining.log](evidence/run_string_measure_combining.log),
and [python_string_length_probe.log](evidence/python_string_length_probe.log)).
The installed K domain documentation explicitly says the Unicode-string
implementation is incomplete beyond the first 256 code points; the preserved
text is
[k_string_domain_documentation.log](evidence/k_string_domain_documentation.log).

There is also a proof-source/concrete-hook discrepancy: a ground proof-source
literal `"\U0001f642"` simplifies to length 1
([kprove_string_length_one.log](evidence/kprove_string_length_one.log)), and a
ground claim for length 4 fails
([kprove_string_length_four.log](evidence/kprove_string_length_four.log)).
Likewise, the ground claim for the real Python result closes while the
opposite ground claim fails
([kprove_unicode_actual_python_result.log](evidence/kprove_unicode_actual_python_result.log)
and
[kprove_unicode_false_python_conclusion.log](evidence/kprove_unicode_false_python_conclusion.log)).
This does not repair the concrete semantics or the unrestricted bridge; it
further limits the trust that can be placed in the imported String hook across
proof-source and runtime representations.

The divergence is reproducible on two cleanly built backends and is documented
by the selected primitive.  It is not a timeout, malformed mount, or transient
container failure.

## 4. Adequacy and real-program pinning

The five formal claims say:

1. `totalChars` of the empty sequence is zero.
2. `totalChars` of a cons sequence is the K string length of its head plus the
   tail total.
3. If the first K total is no greater, exact program execution returns
   `pyList(LIST1)`.
4. If the first K total is greater, exact program execution returns
   `pyList(LIST2)`.
5. If the totals are equal, exact program execution returns
   `pyList(LIST1)`.

There are no right-only existential result variables, omitted result cells, or
one-way implications.  Each entry claim consumes the computation and fixes the
returned list.  Claims 3 and 4 cover the two ordering branches; claim 5
redundantly makes tie behavior explicit.

The proof uses the `solutionProgram` macro rather than reading
`solution.mpy` during `kprove`.  I expanded both the submitted translated file
and the macro with the fresh proof definition.  Their KAST JSON is
byte-identical with SHA-256
`0649b584e57fa0fdde4000950e2e7a15d3b351e242047142824197dc72692e52`.
See [program_pinning.log](evidence/program_pinning.log),
[program-actual-expanded.json](evidence/program-actual-expanded.json), and
[program-macro-expanded.json](evidence/program-macro-expanded.json).
Together with trusted translation identity, this pins the proof term to the
actual submitted program.

Every precondition is satisfiable.  Ground substitutions were checked against
both Python implementations:

| Claim | Satisfying state | Result |
|---|---|---|
| empty total | `.StrVals` | `0` |
| cons total | `pyStr("a") :: .StrVals` | `1` |
| first/no-greater | `["a"]`, `["bb"]` (1 ≤ 2) | first list |
| second/smaller | `["bb"]`, `["a"]` (2 > 1) | second list |
| first/tie | `["a"]`, `["b"]` (1 = 1) | first list |

The executable record is
[claim_witnesses.log](evidence/claim_witnesses.log).

There are no helper or loop claims.  The direct `run` rule matches the exact
function name, parameter names, and `Return(BODY)`, then evaluates that real
body with both argument bindings.

Adequacy nevertheless fails over the full prompt domain.  `StrVals` permits
unrestricted K `String` values and no claim precondition limits code points to
the primitive's supported Latin-1 range.  The formal K-total ordering can
therefore disagree materially with Python's `len` ordering, as the Unicode
witness demonstrates.

## 5. Rule-by-rule static soundness review

The numbered source and attribute search are preserved in
[static_inventory.log](evidence/static_inventory.log).  There are no generated
helper K source files.

### Syntax and configuration inventory

`semantic.k` declares all of the following local syntax:

- `Program`: `Module(Stmt)`.
- `Params`: exactly two `String` names.
- `Stmt`: `FuncDef(String, Params, Stmt)` and `Return(Expr)`.
- `Expr`: `Name(String)`, one-argument `Call`, two-argument `Call`,
  `IfExp`, and `Compare`.
- `CmpOp`: `CmpOp(String, Expr)`.
- Runtime data: `PyString`/`pyStr`; empty and cons `StrVals`; empty and cons
  `IntVals`; `IntVal`/`pyInt`; `Value` injections for `PyString` and `IntVal`;
  and `pyList`, `pyInts`, `pyBool`, and `builtin`.
- Invocation/binding data: `args(Value, Value)` and `env(Value, Value)`.
- Function syntax: `eval`, `apply1`, `apply2`, `lessEqual`, `ifValue`,
  `mapLengths`, and `sumInts`.
- Computation syntax: `run(Program, Args)`.
- One-cell configuration:
  `<k> run($PGM:Program, $ARGS:Args) </k>`.

`verification.k` adds `solutionProgram [macro]` and
`totalChars(StrVals) [function]`.

No local declaration has `[total]`, `[functional]`, `[opaque]`,
`[simplification]`, or a priority attribute.  There are no local opaque
symbols, priority rules, or simplification rules.  The imported domain
primitives, including `lengthString`, integer arithmetic, comparisons, and
booleans, are part of the low-level trust boundary.

Every syntactic construct in `solution.mpy` is covered:

| Program construct | Declaration | Behavior |
|---|---|---|
| `Module` | `semantic.k:8` | exact entry pattern at lines 95–98 |
| `FuncDef`, `Params`, `Return` | lines 10, 12–13 | exact binding/body pattern at lines 95–98 |
| `Name` | line 15 | lookup/builtin rules at lines 57–61 |
| one-/two-argument `Call` | lines 16–17 | evaluation at lines 63–66; application at lines 72–75 |
| `Compare`, `CmpOp("<=", ...)` | lines 19, 21 | lines 67–68 and 84–89 |
| `IfExp` | line 18 | lines 69–70 and 90–91 |

Runtime `args`, `pyList`, `StrVals`, and `pyStr` represent the externally
supplied inputs; `env`, builtins, integer lists, integers, and booleans cover
all intermediate values.

### Semantic rule inventory and decisions

1. `eval(Name("lst1"), env(V1, _)) => V1` and
   `eval(Name("lst2"), env(_, V2)) => V2` preserve the exact two parameter
   bindings.  Sound for the matched entry call.
2. The three `eval(Name(...))` rules for `len`, `map`, and `sum` fix the
   standard builtins.  This is an external-binding assumption.  It is
   acceptable for the ordinary HumanEval environment because the submitted
   module defines no shadowing globals, but it excludes monkey-patched
   builtins.
3. The one- and two-argument `eval(Call(...))` rules evaluate the called
   expression and arguments compositionally.  Python's left-to-right order is
   not represented with control frames, but every actual operand is pure and
   exception-free on lists of strings, so no observable ordering difference
   exists for this program.
4. `eval(Compare(... "<=" ...))` delegates both integer-valued sides to
   `lessEqual`.  This matches the only comparison used.
5. `eval(IfExp(...))` delegates to `ifValue`; the true/false rules select only
   the corresponding result.  The actual branches are pure parameter lookups,
   so allocation, state, exceptions, and cleanup are not omitted.
6. `apply1(builtin("len"), pyStr(S)) =>
   pyInt(lengthString(S))` is the material defect.  It is the only value
   bridge for Python string length, and it is asserted for every `S:String`
   without a supported-code-point guard.  Concrete false-conclusion witness:
   for `S = "🙂"`, the selected concrete K primitive yields 4 while Python
   yields 1.  Through the real body this makes
   `total_match(["🙂"], ["ab"])` evaluate to `["ab"]` in both fresh K
   definitions, while both real Python bodies evaluate to `["🙂"]`.  The rule
   therefore enables a false result on the intended input domain.  The
   proof-source literal behavior noted in stage 3 narrows the diagnosis to the
   imported String representation/hook boundary; it does not validate the
   unrestricted concrete bridge.
7. `apply1(sum, pyInts(IS))` and `apply2(map, len, pyList(SS))` correctly model
   the actual pure builtins once the element-length operation is fixed.
   Eager `mapLengths` is observationally equivalent to Python's lazy `map`
   because `sum` immediately consumes it and `len` on built-in strings has no
   side effects.
8. `mapLengths` has exactly empty and cons equations and structurally
   descends.  The list recursion is sound relative to `lengthString`, but it
   propagates the defective Python-length bridge.
9. `sumInts` has exactly empty and cons equations, structurally descends, and
   uses ordinary integer addition.  It is mathematically sound.
10. `lessEqual` has guards `I <= J -> true`, `I == J -> true`, and
    `I > J -> false`.  The equality rule overlaps the first rule, but their
    right-hand sides agree.  The true/false guards cover all integers and do
    not conflict.
11. `ifValue(true, THEN, _) => THEN` and
    `ifValue(false, _, ELSE) => ELSE` are disjoint and complete over
    `pyBool`.
12. `run(Module(FuncDef("total_match", Params("lst1", "lst2"),
    Return(BODY))), args(V1,V2)) => eval(BODY, env(V1,V2))` is an entry
    invocation rule, not an oracle for the result.  It binds both parameters
    and executes the exact submitted body.  The single-cell configuration is
    adequate because this function has no heap mutation, output, allocation
    visible to the contract, exceptions on the stated built-in domain, or call
    stack after entry.

### Verification rule inventory and decisions

1. `solutionProgram` is a macro, not a result-bearing operational shortcut.
   Its expansion is exactly the submitted translated AST, as independently
   established in stage 4.
2. `totalChars(SS) => sumInts(mapLengths(SS))` is a transparent definitional
   summary.  It does not replace source execution and has no overlap or
   recursion.  It is mathematically the K model's total, but its informal
   identification with Python character count inherits the String bridge
   failure.

The five `spec.k` items are reachability claims, not semantic or
simplification rules.  The two measure claims unfold truthful definitions.
The three entry claims constrain the actual output and partition the K-total
ordering, with the tie claim consistently overlapping the no-greater claim.

No rule encodes which input list to select independently of executing the
submitted comparison, no free oracle influences the result, and no used
construct is fabricated.  The failure is specifically the unrestricted
external primitive bridge for a used, result-bearing operation.

## 6. Fresh non-vacuity test

I authored
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k).  It preserves the
original `totalChars(LIST1) <= totalChars(LIST2)` precondition but changes the
required result from `pyList(LIST1)` to `pyList(LIST2)`.  The concrete state
`LIST1 = ["a"]`, `LIST2 = ["bb"]` satisfies the precondition (1 ≤ 2) and makes
the mutation false.

The mutation dry run built successfully and exited 0:
[stage6_vacuity_dry_run.log](evidence/stage6_vacuity_dry_run.log).
The actual proof exited 1 with `WarnStuckClaimState`; the residual reached
`pyList(LIST1)` and could not imply `LIST1 == LIST2` under the original
ordering precondition:
[stage6_vacuity_false_proof.log](evidence/stage6_vacuity_false_proof.log).

This is a reachable result-obligation failure, not a parser error, missing
import, timeout, or unrelated crash.  The positive proof is therefore
non-vacuous.  Non-vacuity does not cure the semantics bridge failure.

## 7. Proven versus assumed accounting

What `#Top` establishes is precise and narrower than the Python contract:

> Under the candidate K definition and imported domain theory, executing the
> exact submitted AST on two `pyList(StrVals)` values returns the first K list
> when `sumInts(mapLengths(LIST1)) <=
> sumInts(mapLengths(LIST2))`, returns the second when the first K total is
> greater, and returns the first on equality.

The proof is result-constraining, body-sensitive through ordinary evaluation,
and non-vacuous.  It is not a proof that K's concrete String hook computes
Python `len` for every Python string.

Trust and assumption ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| K integers, addition, comparison, and booleans | totals, guards, every entry claim | Acceptable ordinary mathematical primitives. |
| K `String` and `lengthString` hook | `apply1(len,...)`, `mapLengths`, `totalChars`, branch selection | Illegitimate as an unrestricted Python-`len` bridge.  Installed docs limit support beyond Latin-1 and fresh concrete execution changes the program result. |
| Mapping Python builtins `map` and `sum` to eager K functions | both totals | Acceptable on finite lists of built-in strings; no side effects or exceptional elements occur. |
| Resolution of `len`, `map`, and `sum` to standard builtins | program evaluation | Acceptable for the standard HumanEval execution environment; monkey-patching is excluded. |
| Lists represented structurally without heap identity | input and output lists | Adequate for the value contract; source-side differential tests also confirm selection of the original list object. |
| Direct entry invocation rather than general Python module/call semantics | `run` and all entry claims | Adequate for this pure, exact two-argument function; binding and body are syntactically pinned. |
| Trusted translator | Python-to-`.mpy` connection | Acceptable: trusted translator used and byte identity established. |
| `solutionProgram` macro | every entry claim | Acceptable: expanded KAST identity established, not assumed. |
| Python canonical differential test | implementation-to-contract bridge | Strong finite evidence over 1,980 cases, not a universal proof. |
| K concrete differential test | generated-semantics bridge | Negative evidence: two material Unicode mismatches in 12 targeted cases. |

There are no candidate-local opaque symbols, totality declarations, priority
rules, simplification axioms, or empirical result oracles.  The imported
String hook is the sole material result-bearing trust failure.

Gate summary:

- Dynamic proof reconstruction: pass (`#Top` for all claims).
- Program/translator identity and result constraint: pass.
- Non-vacuity: pass.
- Rule consistency inside the K model: pass except for the external
  Python-`len` bridge.
- Real-program semantics over the stated list-of-strings domain: fail, with
  the concrete Unicode result witness above.
- Evidence auditability: pass.

The candidate would support a legitimate theorem under an explicit domain
restriction compatible with the concrete String primitive, but neither the
prompt nor the formal preconditions contain that restriction.  As submitted,
it is not a partial-correctness proof of the real generated Python program over
the intended domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
