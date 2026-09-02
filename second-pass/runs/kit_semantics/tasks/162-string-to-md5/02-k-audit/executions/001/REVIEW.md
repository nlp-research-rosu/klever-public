# Independent adversarial audit: 162-string-to-md5

## Audit outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program under the supplied K model. Fresh reconstruction proves
both exhaustive modeled-string branches, the claims execute the exact trusted
translation of `solution.py`, and independent false-result and body mutations
are rejected for the intended obligations.

The result is `CONCERNS / LEGIT`, rather than `PASS`, for two explicit supplied
trust/model boundaries:

1. `md5hexCodes` is an evaluator-free supplied primitive. The K theorem proves
   that the real program path returns that exact primitive application; its
   interpretation as the lowercase MD5 digest is conditional on the supplied
   primitive's external contract.
2. The supplied `encode` rule is identity on `IntSeq`, whereas CPython UTF-8
   expands non-ASCII code points to bytes. The candidate did not create or
   narrow around this gap: it proves every `IntSeq` admitted by the model,
   documents the divergence with `π`, and its Python implementation uses
   CPython UTF-8 correctly.

The second item satisfies all four conditions of campaign amendment v2's
documented supplied-model representation-gap exception. It therefore maps to
`CONCERNS / LEGIT`, not `FAIL / NOT_LEGIT`. There is no candidate-caused domain
restriction and no docstring/canonical contradiction.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `162-string-to-md5`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `pipeline-v3`;
- candidate `/candidate`;
- trusted prompt, canonical, translator, and supplied-semantics mounts under
  `/reference`.

All required pipeline-v3 records were present, readable, and of the expected
regular-file/directory type:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace;
- `/candidate`, `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`.

The corrected integrity run is
`evidence/stage1-integrity-rerun.log`; the reviewer script is
`evidence/stage1_integrity.sh`. Its exit status is 0. An earlier preserved run,
`evidence/stage1-integrity.log`, used unavailable `jq` for JSON field
extraction and is invalid for those field comparisons. It did not modify any
input; the corrected run uses Python JSON parsing.

### Campaign lock and hashes

The JSON object in `/audit-campaign-lock.json` exactly equals
`.audit_campaign` in `/audit-input.json`. Its actual SHA-256 is
`053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`,
which matches the launcher record.

Every launcher-recorded regular-file hash checked independently matched,
including the canonical, prompt, translator, run/task/result manifests, all
generation records, and generation prompt/logs. Independent file manifests
for the candidate sources, trusted semantics, candidate semantics, and trace
are in the same integrity log.

No symlink exists below `/candidate`, `/reference`, or
`/generation-evidence`. Both supplied-semantics trees contain exactly 24
regular files and two directories, with no other file types. Recursive
`diff -qr --no-dereference` between
`/candidate/reference-semantics` and
`/reference/reference-semantics` exits 0. Thus there are no missing,
additional, changed, mistyped, or symlinked candidate semantics entries.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.

### Generation evidence inspection

The generation records were treated only as untrusted claims. The structured
trace contains 245 valid JSON lines, zero parse errors, and 48 matched
tool-call/tool-output pairs. The full trace call inventory and complete-file
scan of the 19,852-line raw output are in
`evidence/stage1-generation-summary.log`, produced by
`evidence/stage1_generation_summary.py` with exit 0.

The trace claims three successful positive proofs and two rejected mutations,
but none of those generation-time outcomes was used as reconstruction
evidence. No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Docstring contract

The trusted docstring at `/reference/prompt.py:4` requires:

- input is a string `text`;
- return its MD5-hash-equivalent string;
- return `None` for the empty string;
- for `"Hello world"`, return
  `3e25960a79dbc69b674cd4ec67a72c62`.

The docstring does not prescribe an encoding for non-ASCII strings or error
behavior for exotic text. Under campaign amendment v3, a defensible encoding
choice is acceptable.

The submitted `/candidate/solution.py:4`:

```python
def string_to_md5(text):
    if text == "":
        return None
    return hashlib.md5(text.encode("utf-8")).hexdigest()
```

This meets every docstring-determined behavior. Equality with `""` and
truthiness coincide over the stated ordinary-string domain. UTF-8 is a
standard, defensible interpretation for non-ASCII text.

The trusted canonical uses ASCII encoding. It is a valid helper witness on
ASCII but raises `UnicodeEncodeError` on non-ASCII values such as `π`.
Because the docstring does not select an encoding, this canonical divergence
is not a candidate defect.

### Trusted translation

The exact command was:

```text
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/162-string-to-md5/regenerated-solution.mpy
```

It exited 0. `cmp` between the regenerated artifact and
`/candidate/solution.mpy` exited 0; both have SHA-256
`4e62b5a7f20269d1b22445b21aa9fe3f53ea3cd1d93b02726b5fc857d11b1d84`.
See `evidence/stage2-fidelity.log`.

### Independent differential

`evidence/stage2_differential.py` imports both the trusted canonical and the
submitted entry point. It exercises:

- empty and one-character branch boundaries;
- the documented example;
- NUL, whitespace, and standard MD5 vectors;
- lengths around MD5 block boundaries 55, 56, 63, 64, and 65;
- lengths 255 and 256;
- composed and decomposed Unicode, emoji, and CJK;
- 250 seeded generated ASCII strings and 100 seeded generated Unicode strings.

Exact command and result:

```text
python3 /audit-output/evidence/stage2_differential.py
exit 0
TOTAL_CASES=376
GENERATED_CONTRACT_FAILURES=0
CANONICAL_ASCII_MISMATCHES=0
CANONICAL_UNICODE_OBSERVATIONS=92
```

The submitted result also agrees with an independent OpenSSL UTF-8 oracle on
every nonempty tested case. The prompt example and empty result are exactly
correct. The corpus and deterministic seed are preserved in the script; its
corpus SHA-256 is
`0392c745e0e7a2b3cc067086c006971e49d9568765b81f54fb86799879322a55`.

These are finite fidelity checks, not substitutes for the K proof.

## 3. Clean proof reconstruction

### Scratch isolation

Only source artifacts were copied to
`/tmp/audit-work/162-string-to-md5`. Candidate `runtime-kompiled`,
`verification-kompiled`, caches, bytecode, logs, and compiled definitions were
not copied or reused. The semantics copy came from the trusted
`/reference/reference-semantics`, not from a candidate-built definition.

The live tools report K version `v7.1.293`; see
`evidence/stage3-prebuild.log`.

### Fresh concrete definition

Exact build:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

Exit 0; log: `evidence/stage3-kompile-llvm.log`.

The trusted-translated empty harness:

```text
krun audit-empty.mpy --definition runtime-audit-kompiled
```

exits 0 with `.K`, `result |-> noneV`, empty heap/stack, `NoExc`, and exit
code 0 (`evidence/stage3-krun-llvm-empty.log`).

The nonempty LLVM harness exits 113 at the evaluator-free term
`md5hexCodes(iCons(72,...))`
(`evidence/stage3-krun-llvm-nonempty.log`). This is the expected fixed
primitive limitation, not a failed positive proof or infrastructure failure.

### Fresh proof definition and positive claims

Exact build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit 0; log: `evidence/stage3-kompile-haskell.log`.

A Haskell concrete run on the nonempty harness exits 0 and reaches:

```text
result |-> str(md5hexCodes(iCons(72,...)))
<k> .K </k>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
```

See `evidence/stage3-krun-haskell-nonempty.log`.

Every positive target claim was then run independently:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.empty-input
#Top
exit 0

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.nonempty-input
#Top
exit 0

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
#Top
exit 0
```

Logs:

- `evidence/stage3-kprove-empty.log`;
- `evidence/stage3-kprove-nonempty.log`;
- `evidence/stage3-kprove-combined.log`.

All were produced from the fresh definition. The compiler's unused-variable
warnings in `strLt` do not affect these claims.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.empty-input` starts with the standard initial machine state, loads the
submitted module body, calls `string_to_md5` on `str(.IntSeq)`, and requires
termination of that harness with:

- the loaded closure retained in module scope;
- `result |-> noneV`;
- environment restored to module scope;
- no allocated heap, call frame, pending return, exception, or nonzero exit.

`SPEC.nonempty-input` does the same for arbitrary `CS:IntSeq` under
`notBool (CS ==K .IntSeq)` and requires:

```text
result |-> str(md5hexCodes(CS))
```

with the same complete clean final state.

Empty and nonempty are exhaustive for every modeled `str(IntSeq)`. The
nonempty claim is symbolic and has no size bound or finite unrolling.
Non-string arguments are correctly outside the docstring's stated domain.

### Mechanical constructor identity

`evidence/stage4_pinning.py` extracts the `Import` plus `FuncDef` prefix from
both claims, normalizes only the two equivalent spellings of typed empty K
lists, parses each with the fresh definition, and compares its constructor
AST to the trusted regenerated `solution.mpy`.

Final successful run: `evidence/stage4-pinning-final.log`, exit 0. For the
trusted translation and both claim bodies the constructor-AST SHA-256 is:

```text
5226c9e401af90e7cced9874ce5e1cd1f36a5f709cabcc8872e426343418988d
```

Thus the claims execute the exact function binding and body, with only an
appended harness assignment. Two earlier preserved pinning logs show
reviewer-script errors (first explicit-empty surface parsing, then a whitespace
assertion); the AST comparisons themselves were not adverse and the final
corrected script exits 0.

### Control flow and result constraint

The real fixed-semantics path is:

1. `#loadAll` sequences `Import`, `FuncDef`, and harness `Assign`.
2. `Import("hashlib")` takes the supplied import abstraction.
3. `FuncDef` binds the exact closure in scope 0.
4. `Call(Name("string_to_md5"), ...)` performs name lookup, left-to-right
   argument evaluation, frame allocation, parameter binding, and body
   execution.
5. `Compare(text, "==", "")` evaluates both operands and uses the string
   equality rule.
6. Empty input takes the first `Return`, whose abrupt return correctly discards
   the remainder of the function body but restores the saved caller
   continuation.
7. Nonempty input takes the empty else sequence, then executes the second
   `Return`; encode, MD5 construction, `hexdigest`, frame pop, and harness
   assignment all execute.

The postconditions constrain the returned value, the closure body, and all
machine cells; no RHS result is free.

Concrete satisfying witnesses:

- empty: `str(.IntSeq)`, with candidate and canonical both returning `None`;
- nonempty: `str(iCons(97,.IntSeq))`, with candidate and canonical both
  returning `0cc175b9c0f1b6a831c399e269772661`.

The fixed-model claimed nonempty result is the exact term
`str(md5hexCodes(iCons(97,.IntSeq)))`; the concrete digest is its trusted
primitive interpretation. These substitutions are recorded in
`evidence/stage4-pinning-final.log`.

### Independent body sensitivity

`evidence/spec-audit-body-mutation.k` changes the program term actually
executed by the claim: the nonempty return becomes `Return(Str("wrong"))`,
while input `"a"` retains the original digest obligation.

Its dry run builds successfully with exit 0
(`evidence/stage4-body-mutation-dry-run.log`). Its proof exits 1 with
`WarnStuckClaimState`; the residual has concrete result `"wrong"` and the
unmet equality to `md5hexCodes([97])`
(`evidence/stage4-body-mutation-proof.log`). The theorem is therefore
body-sensitive.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The final exhaustive inventory is
`evidence/stage5-rule-inventory-final3.log`, generated by
`evidence/stage5_inventory.py` with exit 0. It covers all 24 supplied K files,
the assembler, `verification.k`, and `spec.k`:

```text
1183 top-level entries
764 rules
244 syntax declarations
5 contexts
1 configuration
2 claims
27 modules / 27 endmodules
88 imports
25 source requires
```

Attribute-bearing blocks include 160 function declarations, 113 `total`
declarations, 27 explicit symbols, 24 `no-evaluators` declarations, 60
`concrete` blocks, 48 priority blocks, 28 `owise` blocks, three macros, and no
local `simplification` or `functional` declaration.

Every inventoried entry is printed with file, exact line span, attributes, full
flattened text, and one of these dispositions:

- exact program path;
- supplied import-binding boundary;
- supplied encoding boundary;
- supplied MD5 boundary;
- unreachable fixed declaration;
- unreachable fixed opaque declaration;
- fixed definition/module structure;
- candidate wrapper with no extension;
- target claim/spec structure.

Earlier inventory logs are retained but are superseded: the first split rule
guards into separate entries, and the next two refined guard grouping and
attribute extraction. `stage5-rule-inventory-final3.log` is the authoritative
inventory.

### Candidate-local theory

`/candidate/verification.k` contains only:

```text
requires "reference-semantics/semantics.k"
module VERIFICATION
  imports MPY
endmodule
```

There is no candidate-local syntax, function, totality assertion, opaque
symbol, priority, equation, ordinary rewrite, simplification, operational
bridge, lemma, or auxiliary circularity. Consequently, there is no
candidate-added rule that encodes the answer, substitutes a program, or
bypasses execution.

The two declarations in `spec.k` are target claims, not semantic rewrite rules
or loop circularities.

### Used syntax and operational rules

The constructor coverage is complete:

- `Module`, `Stmts`, `Import`, `FuncDef`, `Params`, `If`, `Compare`,
  `CmpOp`, `Name`, `Str`, `Return`, `NoneVal`, `Call`, `Attribute`, and
  `Assign` are declared in `semantics/syntax.k`.
- `str`, `IntSeq`, closures, values, scopes, frames, returns, and all
  configuration cells are declared in `semantics/core.k` and
  `semantics/functions.k`.

The relevant fixed rules are:

- module loading, sequencing, name lookup, argument evaluation, literals, and
  string truthiness in `core.k`;
- comparison evaluation contexts in `operators.k`;
- string literal conversion and equality in `str.k`;
- assignment and `If` branching in `controls.k`;
- closure creation, parameter binding, return, frame pop, and state restoration
  in `functions.k` and `call.k`;
- method binding and dispatch in `call.k`;
- identity encoding in `methods.k`;
- import no-op in `float.k`;
- the MD5 route and primitive in `builtins.k`.

For the actual terms, evaluation order is left-to-right. Closure lookup and
parameter binding are explicit. The call rule stores the caller continuation,
and `#pop` restores it after an abrupt `Return`; it does not discard the
top-level assignment. The exact initial/final cells show no hidden heap,
scope-location, stack, return, exception, or exit-code change.

The relevant overlaps are controlled:

- the priority-40 syntactic MD5 call preempts the generic `[owise]` call route;
- string, integer, Boolean, float, list, tuple, set, and dictionary comparison
  equations are constructor/sort-disjoint on this path;
- cell-write rules overlap ordinary binding only under explicit
  priority-40 cell guards, which are false in the plain function frame here;
- `applyMethod` for `encode` and `hexdigest` has disjoint receivers
  (`str` versus `md5Obj`).

### Supplied operational/value boundaries

Inventory entries `INV-0265` through `INV-0270` are the MD5 boundary:

```text
Call(Attribute(Name("hashlib"), "md5"), (E, .Exprs)) => E ~> #md5
str(CS) ~> #md5 => md5Obj(CS)
applyMethod(md5Obj(CS), "hexdigest", .Vals) => str(md5hexCodes(CS))
md5hexCodes(IntSeq) [function, total, symbol, no-evaluators]
```

It evaluates the argument before construction, preserves the arbitrary active
continuation, changes no other cell, and returns the exact externally named
value. It syntactically fixes the external binding; that is sound for this
source only under the recorded assumption that its preceding import denotes
CPython `hashlib` and is never rebound.

Inventory entry `INV-0867` is the encoding boundary:

```text
applyMethod(str(CS), "encode", str(_), .Vals) => str(CS)
```

It is exact for ASCII in the model but not CPython UTF-8 for non-ASCII. This is
not called a universally sound Python equation. It is the documented supplied
model gap analyzed below.

Inventory entry `INV-0574` is the import boundary:

```text
Import(_) => .K
```

It is over-broad as a general Python import model, but for this immutable source
it combines with the exact external MD5 route and no rebinding. It does not
fabricate a candidate-defined computation.

`evidence/stage5_control_sensitivity.py` adds an observable
`after_digest = 7` continuation immediately after the real function call. The
trusted translation run exits 0 with both:

```text
digest |-> str(md5hexCodes(iCons(97,.IntSeq)))
after_digest |-> 7
```

and with clean control/state cells. See
`evidence/stage5-control-sensitivity.log`.

### Remaining fixed rules

All remaining entries are marked unreachable for this theorem because no
matching top constructor or receiver/value sort can arise on the exact
program path. This includes iteration, ranges, arithmetic, floats,
collections, comprehensions, slicing, sorting, assertions, dictionaries, and
the concrete-only `MPY-CONCRETE` module. `VERIFICATION` imports `MPY`, not
`MPY-CONCRETE`.

The LLVM compiler reports incomplete-match warnings for several supplied
`total` helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`). None is reachable here. The declarations do not rewrite a current
term to a false result; on uncovered inputs they leave an abstract application.
This is a narrower fixed-semantics coverage observation, not an unsoundness
claim about the target proof.

The other 23 evaluator-free symbols are float/sort abstractions and are
unreachable. `md5hexCodes` is the only evaluator-free symbol influencing this
postcondition.

No inventoried rule is labeled materially unsound for the intended input
domain. Therefore no unsupported unsoundness allegation or false-conclusion
witness is asserted. The concrete `π` divergence below is instead evidence of
the explicitly allowed supplied-model representation gap.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not trusted. A fresh reviewer mutation is
preserved at `evidence/spec-audit-vacuity.k`.

It executes the exact real body on the satisfying nonempty input `"a"` but
changes the final result obligation from
`str(md5hexCodes(iCons(97,.IntSeq)))` to `noneV`.

Build/parse check:

```text
kprove spec-audit-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --dry-run
exit 0
```

See `evidence/stage6-vacuity-dry-run.log`.

Proof:

```text
kprove spec-audit-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-AUDIT-VACUITY
exit 1
```

The proof produces `WarnStuckClaimState` for the intended unmet result. Its
residual is a completed, clean configuration containing:

```text
result |-> str(md5hexCodes(iCons(97,.IntSeq)))
```

which cannot match `noneV`. There is no parser error, timeout, missing import,
or unrelated crash. See `evidence/stage6-vacuity-proof.log`.

The theorem is non-vacuous and discriminates a false result.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the exact supplied K definition:

- for the empty modeled string, executing the exact translated submitted
  function through module load, lookup, call, branch, return, and assignment
  produces `noneV`;
- for every nonempty modeled `IntSeq CS`, the same execution produces
  `str(md5hexCodes(CS))`;
- both cases finish the harness with the exact expected closure binding and
  clean environment, heap, allocation counters, call stack, return state,
  exception state, and exit code;
- the two cases cover the full unbounded modeled string domain.

This is a reachability/partial-correctness result under the fixed theory. It is
not a proof of MD5 collision resistance, cryptographic security, or a
from-first-principles implementation of the MD5 compression algorithm.

### Trust ledger

| Boundary | Effect and dependents | Status and evidence |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell backend, and reachability logic | All claims | Standard machine-checking trust base; versions and fresh builds recorded. |
| Trusted `py2mpy.py` | Source-to-constructor identity | Launcher hash matches; trusted regeneration is byte-identical; constructor ASTs also match both claims. |
| Supplied operational core | Loading, scopes, lookup, evaluation order, calls, returns, state | Fixed tree is byte-identical to the trusted mount; fresh concrete and symbolic executions traverse the exact source path. |
| `Import(_) => .K` plus syntactic `hashlib.md5` routing | External binding/control for nonempty claim | Conditional supplied binding abstraction. Exact source imports `hashlib` and never rebinds it. Body/control sensitivity and final-state runs support this exact use. |
| `md5hexCodes(CS)` | Entire nonempty returned value/postcondition | Acceptable external trusted primitive: fixed, standard-library behavior outside candidate-defined code; theorem and report remain explicitly conditional on its MD5 meaning. OpenSSL differential gives finite support only. |
| Identity `encode` rule | Bytes/codes passed to the MD5 primitive | Supplied-model representation gap. Exact for ASCII; diverges from CPython UTF-8 on non-ASCII. Candidate does not narrow the theorem and its Python uses UTF-8 correctly. |
| Natural-language bridge from `md5hexCodes` to lowercase MD5 hex | Human-facing task property | Informal external contract plus 376-case program/OpenSSL evidence; not a universal K derivation of MD5. |
| Partial-correctness scope | Termination/error behavior outside successful modeled paths | The report claims only the reconstructed reachability theorem and the source-contract behavior supported by the model/boundary accounting. |

### Supplied-model representation-gap test

All amendment-v2 conditions hold:

1. **Origin:** the restriction comes from
   `/reference/reference-semantics/semantics/methods.k:58`, not from a
   candidate proof rule or precondition.
2. **No candidate narrowing:** the entry claims cover empty plus every
   nonempty `CS:IntSeq`, with no ASCII predicate, size bound, example
   restriction, or unrolling.
3. **Explicit ledger and witness:** `/candidate/PROOF.md:283` records the
   identity-encoding gap and gives `π`, whose modeled code sequence is `[960]`
   while UTF-8 bytes are `[207, 128]`. The independent audit reproduces this
   in `evidence/stage2-fidelity.log`.
4. **Program fidelity:** `/candidate/solution.py` calls
   `text.encode("utf-8")`; the divergence is model-versus-CPython, not
   submitted-program-versus-docstring. OpenSSL testing has zero failures.

This exact campaign exception mandates `CONCERNS / LEGIT`.

### Gate summary

- Dynamic reconstruction: **PASS**.
- Real-program soundness/body sensitivity: **PASS** under the named supplied
  external primitives.
- Intent/domain adequacy: **PASS for every modeled string**, with the
  documented supplied UTF-8 representation gap.
- Non-vacuity: **PASS**.
- Evidence auditability: **PASS**.
- Unqualified equivalence to CPython over non-ASCII encoding and a formally
  evaluated MD5 value: **not established**, and explicitly reported.

The candidate's own `VALIDATED` headline is therefore too strong for this
benchmark's final mapping, but the proof remains legitimate. The limitations
are fixed, documented trust/model boundaries, not candidate-created
shortcuts, vacuity, substitution, or material domain narrowing.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
