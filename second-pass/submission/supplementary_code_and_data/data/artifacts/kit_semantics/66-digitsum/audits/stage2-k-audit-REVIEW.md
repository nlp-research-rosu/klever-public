# Independent adversarial review: 66-digitsum

## Outcome

The candidate contains a sound, non-vacuous partial-correctness proof of the
submitted translated program under the unmodified supplied K semantics. The
entry claim covers every finite `IntSeq` admitted by that symbolic model, the
proof-local summary is connected to actual execution by the loop reachability
claim, and the result is constrained.

The qualification is a supplied-model representation/behavior gap, not a
candidate restriction: concrete string literals are ASCII-only in the supplied
semantics, and its case predicates classify only ASCII `A` through `Z`.
CPython is Unicode-aware. The candidate program itself is faithful to the
trusted canonical program on that gap. A concrete witness is `"À"` (U+00C0):
both Python functions return `192`, the recursive K summary for
`iCons(192, .IntSeq)` is `0`, and the concrete supplied semantics cannot reduce
the translated literal past `strToCodes("\xc3\x80")`. This meets campaign
amendment v2's documented supplied-model-gap exception and therefore maps to
`CONCERNS / LEGIT`.

The candidate's `PROOF.md` names the ASCII/Unicode boundary but does not name a
particular Unicode witness. This review supplies and preserves one. That is a
documentation limitation, not a proof-theory defect or candidate-caused domain
narrowing.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- record layout `pipeline-v3`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- problem `66-digitsum`; and
- a mounted trusted reference-semantics tree.

The supplied-semantics mount is present, so the rendered mode and trusted mounts
do not conflict. There is no audit-infrastructure breach.

Independent checks in
[`04-provenance-check.log`](/audit-output/evidence/04-provenance-check.log)
established all of the following:

- The JSON value in `/audit-campaign-lock.json` exactly equals the
  `audit_campaign` block in `/audit-input.json`.
- The lock SHA-256 is
  `e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`,
  exactly the recorded value.
- The mounted canonical, trusted/candidate prompt, trusted/candidate
  translator, run manifest, task manifest, stage result, invocation record,
  generation metrics, runtime metrics, usage, prompt, last message, output log,
  and structured trace all match their recorded hashes.
- Every launcher-required `pipeline-v3` path is present with the required file
  or directory type.
- There are no symlinks anywhere below `/candidate`, `/reference`, or
  `/generation-evidence`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions.
- Candidate and trusted `reference-semantics/` each have 25 entries and have
  zero relative-path, type, or content differences. There are no additional or
  missing semantics entries.

The required generation records were read as untrusted history. The structured
trace has 412 JSONL records; the rendered output has 31,533 lines. The
reviewer-authored parser read all of both and preserved event/tool summaries in
[`generation-trace-summary.txt`](/audit-output/evidence/generation-trace-summary.txt)
and
[`generation-output-keylines.txt`](/audit-output/evidence/generation-output-keylines.txt).
The trace claims a prior `#Top` and successful validation, but neither claim was
used as proof evidence.

Relevant artifacts:

- [`01a-audit-input.log`](/audit-output/evidence/01a-audit-input.log)
- [`02-record-sizes.log`](/audit-output/evidence/02-record-sizes.log)
- [`03-record-contents.log`](/audit-output/evidence/03-record-contents.log)
- [`05-generation-parse.log`](/audit-output/evidence/05-generation-parse.log)
- [`provenance_check.py`](/audit-output/evidence/provenance_check.py)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks for `digitSum(s)`, returning the sum of `ord(char)` for
characters for which `char.isupper()` is true. The stated input is a string, with
no length bound. The trusted canonical implementation special-cases the empty
string and otherwise uses:

```python
sum(ord(char) if char.isupper() else 0 for char in s)
```

The candidate uses the same computation as an explicit loop. Its
`char = ""` assignment only initializes the loop local and does not alter any
result.

### Translation identity

The trusted translator was run afresh:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
cmp /candidate/solution.mpy \
    /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

Both commands exited zero. Submitted and regenerated terms have the same
SHA-256,
`9f2518ca2b5e8280467e32d1c5c64b727cb10b84e84dab2cb45f0d7f4911a86a`.
See
[`09b-translation-identity.log`](/audit-output/evidence/09b-translation-identity.log).

### Independent differential

[`differential_check.py`](/audit-output/evidence/differential_check.py)
imports the trusted canonical and candidate functions independently. It checked:

- all six documented examples;
- empty and ASCII classification boundaries around `A` and `Z`;
- NUL, newline, the maximum Unicode code point, and surrogate-containing
  strings;
- 200 deterministic random strings of lengths from 0 through 1024; and
- every one-character Python string for all 1,114,112 code points.

There were zero candidate/canonical mismatches. The script also compared the
canonical result with the fixed ASCII model and found 1,885 one-code-point
model divergences; the first is U+00C0 `"À"`:

```text
candidate_mismatch_count=0
single_codepoint_first_mismatch=None
model_gap_first_witness=(192, "'À'", 192, 0, True)
```

Command, exit zero, and full bounded result are in
[`10-python-differential.log`](/audit-output/evidence/10-python-differential.log).
Thus the gap is model-versus-CPython, not program-versus-canonical.

## 3. Clean proof reconstruction

All required source files were copied to
`/tmp/audit-work/reconstruction`. No candidate compiled definition or cache was
copied or used; the pre-build inventory proves that both fresh output
directories were absent
([`11-clean-scratch.log`](/audit-output/evidence/11-clean-scratch.log)).

The available tools are K v7.1.293 and Python 3.10.12
([`02-toolchain.log`](/audit-output/evidence/02-toolchain.log)).

### Proof definition

Fresh command:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Exit status: `0`. The only output was unused-variable warnings in trusted
`str.k`; see
[`12-clean-kompile.log`](/audit-output/evidence/12-clean-kompile.log).

The loop claim was also selected independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.digitSum-loop
```

Exit status: `0`; output begins `#Top`
([`13-proof-loop.log`](/audit-output/evidence/13-proof-loop.log)).

The target dependency set consists of the entry claim and its loop circularity.
The complete submitted spec was therefore run:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Exit status: `0`; output begins `#Top`
([`14-proof-full.log`](/audit-output/evidence/14-proof-full.log)).
This is the positive target run that checks both claims with the loop
circularity available. Selecting only the entry label removes that circularity
from K's proof set and is not the submitted proof's dependency structure.

### Concrete definition

Fresh command:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit status: `0`; warnings concern unrelated partial fixed-semantics functions
([`15-clean-llvm-kompile.log`](/audit-output/evidence/15-clean-llvm-kompile.log)).

The reviewer-authored ASCII smoke program covers empty, both branch boundaries,
and examples. Its translated execution exits zero with `.K`, `NoExc`, and exit
code zero
([`17-clean-ascii-concrete-run.log`](/audit-output/evidence/17-clean-ascii-concrete-run.log)).

The separate `"À"` probe exits `113` and stops specifically at
`strToCodes("\xc3\x80")`; it is preserved as model-boundary evidence, not
misclassified as a candidate proof failure
([`16-clean-concrete-run.log`](/audit-output/evidence/16-clean-concrete-run.log)).

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.digitSum-loop` says: starting at the fixed semantics' loop head with an
arbitrary finite remaining code sequence, arbitrary integer accumulator,
arbitrary current loop variable, the exact submitted loop body, the exact
`Return(total) ~> #endcall` continuation, the concrete caller/callee frame
layout, and all active cells pinned, execution returns to the caller with
`TOTAL + digitSumIS(CODES)`. It also requires the real function-frame pop,
callee-scope removal, caller-environment restoration, and stack restoration.

`SPEC.digitSum-entry` says: in the ordinary module/builtins state, calling the
module binding `"digitSum"` on any `str(CODES:IntSeq)` reaches exactly
`digitSumIS(CODES)`. It has no length bound or value constraint beyond the
`IntSeq` sort.

### Constructor-level identity

[`adequacy_check.py`](/audit-output/evidence/adequacy_check.py) extracts the
trusted regenerated `FuncDef` constructor body and every `closureVal` term in
`spec.k`. It normalizes only K list-unit spelling (`.Exprs`, `.Stmts`) and the
equivalent empty trailing comma. Results:

```text
translated_function_count=1
spec_closure_count=3
closure_constructor_equalities=[True, True, True]
entry_call_exact=True
entry_result_exact=True
```

See
[`18b-adequacy-pinning.log`](/audit-output/evidence/18b-adequacy-pinning.log).
The exact parameter, initializations, loop target, iterable, branch, method call,
`ord` call, augmentation, and return occur in all three claim copies.

The entry claim starts after module loading, but trusted regeneration plus this
comparison and the fixed `FuncDef` rule show that the preloaded binding is
exactly the one the submitted module establishes. No material source operation
is omitted. Lack of automatic claim regeneration is only a maintenance
observation for this immutable candidate.

### Satisfiable witnesses and result substitution

The explicit entry configuration is realizable with
`CODES = .IntSeq`; the loop configuration is realizable with, for example,
`CODES = .IntSeq`, `TOTAL = 7`, `INPUT = .IntSeq`, and
`CHAR = str(.IntSeq)`. Substitution checks record:

```text
entry_witness=empty codes=[] digitSumIS=0 candidate=0 canonical=0
entry_witness=both-branches codes=[64, 65, 90, 91] \
  digitSumIS=155 candidate=155 canonical=155
entry_witness=supplied-model-gap codes=[192] \
  digitSumIS=0 candidate=192 canonical=192
```

The first two establish concrete agreement inside the model. The last is the
explicit model boundary. The postcondition is an exact returned integer, not a
free variable, implication, or tautology.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`build_rule_inventory.py`](/audit-output/evidence/build_rule_inventory.py)
enumerates every top-level item in `semantics.k`, all 23 files below
`reference-semantics/semantics/`, `verification.k`, and `spec.k`.
[`rule-inventory.tsv`](/audit-output/evidence/rule-inventory.tsv) contains the
source path, line, module, category, attributes, relevant constructor hits, code,
and full flattened source for every item.

The 1,277 inventoried items comprise:

| Category | Count |
|---|---:|
| ordinary rules | 736 |
| syntax declarations | 242 |
| rule guards / top-level `requires` records | 149 |
| imports | 88 |
| modules / endmodules | 54 |
| contexts | 5 |
| configurations | 1 |
| claims | 2 |

There are 163 function-declaration items, 121 total declarations, 55
priority-bearing items, 32 `owise` items, four macro items, and one recursive
macro item. There are no proof-local simplification rules, `functional`
declarations, priorities, macros, or opaque symbols.

[`assess_rule_inventory.py`](/audit-output/evidence/assess_rule_inventory.py)
adds an explicit decision and reason to every row in
[`rule-assessment.tsv`](/audit-output/evidence/rule-assessment.tsv). The grouped
counts and all proof-dependent/opaque rows are in
[`rule-assessment-summary.txt`](/audit-output/evidence/rule-assessment-summary.txt).
Unused rules were not assumed correct merely because they are supplied: they
are classified as non-dependent only when their LHS constructor, callee,
operator, or value sort cannot occur on this submitted path.

### Used construct map

| Submitted construct / effect | Declaration and operative fixed rules |
|---|---|
| values, scopes, cells, sequencing | `syntax.k`; `core.k` values/configuration and lines 123–191 |
| `Name` lookup and builtin shadowing | `core.k` `#look` and `builtinsScope` |
| assignment / augmentation | `controls.k` `Assign` and `AugAssign`; `int.k` integer `applyBin("+",...)` |
| `for` and target binding | `controls.k` `#loop/#loopStep`; `str.k` `#iterNext`; `tuple.k` `#bindTgt(Name,...)` |
| `if` / truth | strictness from `syntax.k`; `controls.k` `#branch`; `core.k` `truthy` |
| calls and method binding | `call.k` callee/argument evaluation and dispatch |
| `str.isupper()` | `methods.k` `applyMethod`, `hasUpper`, `hasLower`, `isUpperC`, `isLowerC` |
| `ord(one_char)` | `builtins.k` line 143 |
| function call / return | `call.k` frame creation; `functions.k` parameter binding, return, and pop |

The strict/seqstrict attributes generate the expected evaluation order:
receiver before dispatch, call callee before left-to-right arguments, assignment
RHS before store, loop iterable once before iteration, condition before branch,
and returned expression before frame pop.

The relevant priority alternatives are guard-disjoint on the pinned state:
there are no closure cells or heap references, so cell-write/dereference
priority rules do not preempt ordinary local updates. The generic `[owise]`
call dispatcher resolves `"digitSum"` to the exact closure and `"ord"` to the
fixed builtin binding. No candidate rule can intercept a `Call`.

### Proof-local extensions

`verification.k` adds exactly:

```text
digitSumIS(.IntSeq) = 0
digitSumIS(iCons(C, REST)) =
  (if isUpperC(C) and not isLowerC(C) then C else 0)
  + digitSumIS(REST)
```

The constructor domains are disjoint and exhaustive, recursive descent is
strict on `REST`, and totality is justified. For a one-character string, fixed
`isupper()` reduces to
`isUpperC(C) andBool notBool isLowerC(C)`, and fixed `ord()` reduces to `C`.
Thus the equation is mathematically true wherever it applies.

`digitSumIS` is result-bearing, but it is not opaque and never replaces a
program term. `digitSum-loop` is the bridge-free universal connection theorem
over the full remaining-`IntSeq` domain; it executes fixed binding, iteration,
method dispatch, builtin dispatch, arithmetic, update, return, and frame pop.
There is no circular use of a fresh oracle.

The two reachability claims are the only claim extensions. Their continuation,
environment, scopes, scope allocator, heap, heap allocator, stack, return state,
exception state, and exit code are all explicit. There is no ellipsis admitting
an arbitrary continuation or omitted observable cell.

### Fixed opaque and trusted symbols

The imported supplied tree contains 24 opaque declaration items representing
26 names:

`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`floatFinite`, `ltFI`, `ltIF`, `eqIF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, and `sqrtF`.

None appears in `solution.mpy`, either claim, `digitSumIS`, or any reachable
callee/operator/result. They have no dependent target claim and cannot supply
the result. The same is true of unused fixed modules for collections,
comprehensions, ranges, sorting, floats, dicts, sets, and subscripts.

No rule is labeled unsound. The ASCII-only `strToCodes` and case rules are
truthful rules of the selected supplied model but do not model full CPython
Unicode. The concrete false-conclusion/divergence witness for the intended
execution model is `"À"` as recorded above; this is classified as a supplied
representation gap rather than candidate semantic smuggling.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was read only as untrusted evidence. A fresh
reviewer mutation,
[`spec-audit-false.k`](/audit-output/evidence/spec-audit-false.k), was created
without importing the candidate's positive spec. It keeps the exact entry
program/configuration, constrains `CODES ==K .IntSeq`, and changes the required
result from `digitSumIS(CODES)` to `digitSumIS(CODES) +Int 1`.

The empty-string state satisfies the precondition and makes the mutation false:
the real execution result is `0`, while the destination is `1`.

Build-only check:

```text
kprove spec-audit-false.k --definition verification-kompiled \
  --spec-module AUDIT-FALSE --dry-run
```

Exit status: `0`
([`27-false-mutation-dry-run.log`](/audit-output/evidence/27-false-mutation-dry-run.log)).

Proof:

```text
kprove spec-audit-false.k --definition verification-kompiled \
  --spec-module AUDIT-FALSE
```

Exit status: `1`, with `WarnStuckClaimState`, a residual
`<k> 0 ~> .K </k>`, and the expected “cannot be rewritten further” prover
error
([`28-false-mutation-proof.log`](/audit-output/evidence/28-false-mutation-proof.log)).
This is a reachable unmet result obligation, not a parser failure, timeout, or
unrelated crash.

## 7. Proven versus assumed accounting

### What the K proof establishes

Conditioned on the supplied semantics and K toolchain, for every finite
`CODES:IntSeq`, execution of the exact submitted `digitSum` closure from the
entry configuration reaches the integer:

```text
digitSumIS(CODES)
```

That recursive integer is the sum of each code for which the supplied
one-character `isupper()` predicate is true. The theorem has no sequence-length
bound and no candidate-added character-code restriction. It is a
partial-correctness statement; no separate resource-bound theorem is claimed.

### Trust ledger

| Boundary | Influence and dependents | Evidence / judgment |
|---|---|---|
| Unmodified supplied `reference-semantics/` | Defines every used value, binding, order, state, call, loop, return, and result transition | Integrity comparison, clean builds, static inventory, positive proof, and concrete ASCII run. Acceptable fixed-model trust boundary. |
| ASCII string literal and case model (`strToCodes`, `isUpperC`, `isLowerC`) | Changes source-contract behavior for Unicode and affects the theorem result | Concrete witness `"À"`: candidate/canonical `192`, K summary `0`, concrete K literal stuck at `strToCodes`. Supplied-model gap; non-fatal only under campaign amendment v2, hence `CONCERNS`. |
| Trusted `py2mpy.py` | Establishes the Python-AST-to-K-constructor representation | Candidate copy matches trusted hash; fresh output is byte-identical; all claim closure bodies mechanically match. Acceptable. |
| K v7.1.293, Haskell backend, LLVM backend, and K builtin `INT`/`BOOL`/`STRING`/`MAP`/`LIST` theories | Implements compilation, symbolic reachability, concrete execution, integer/string/map operations, and circularity soundness | Version recorded; clean exits and actual outputs preserved. Necessary toolchain trust. |
| Fixed opaque symbols listed in Stage 5 | Could affect other programs' values, control, or results | No target dependent and no reachable occurrence. Imported but irrelevant to this theorem. |
| CPython 3.10 and trusted canonical used by differential tests | Empirical source-fidelity oracle only | Exhaustive one-code-point and deterministic multi-character testing with zero candidate mismatch. It supports the Python bridge but is not substituted for K proof. |
| Constructor-normalization argument | Connects elided `.Exprs`/`.Stmts` syntax to explicit claim syntax | Reviewer script performs extraction and exact normalized equality for all three closures. Narrow, auditable, and semantically inert. |
| `digitSumIS` | Determines the final result | Not assumed: two total equations plus the machine-checked loop connection claim. |

There is no trusted program-local primitive, empirical program-result oracle
inside K, operational bridge, proof-local simplification, unconstrained fresh
symbol, or hidden body substitution.

### Gate results and decision

- Gate A — PASS. The exact program executes, all proof-local equations are
  valid and terminating, fixed control/state is preserved, the result is exact,
  and the fresh false mutation is rejected.
- Gate B — PASS subject to the campaign's supplied-model-gap exception. The
  theorem covers every finite `IntSeq` in the fixed model with no additional
  candidate narrowing. The Python program remains canonical-faithful on
  Unicode, and the divergence witness is explicit.
- Gate C — PASS with a documentation concern. All independent commands,
  scripts, inventories, logs, scopes, and actual outputs are preserved. The
  candidate named the Unicode boundary but omitted a concrete character;
  this review supplies `"À"`.

There is no canonical-versus-docstring contradiction. The sole reason this is
not an unqualified pass is the documented fixed supplied-model
ASCII-versus-Unicode boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
