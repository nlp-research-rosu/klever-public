# Independent adversarial review: 162-string-to-md5

The candidate's two K claims can be rebuilt and proved from clean source, and
they are non-vacuous. They nevertheless do not constitute a legitimate proof
of the real generated Python program over the source-contract domain. There
are two material failures:

1. `solution.py` uses `encode("utf-8")`, while the trusted canonical uses
   `encode("ascii")`. The prompt states no ASCII-only precondition. On every
   tested non-ASCII string the canonical raises `UnicodeEncodeError` and the
   candidate returns a digest.
2. More fundamentally, the used supplied-semantics rule
   `applyMethod(str(CS), "encode", str(_), .Vals) => str(CS)` treats every
   encoding as code-sequence identity. For the actual candidate and input
   `"é"`, K sends the singleton code sequence `[233]` to the MD5 oracle, but
   Python UTF-8 sends bytes `[195, 169]`. Those byte sequences have different
   MD5 digests. A ground K instance of the erroneous execution summary still
   proves `#Top`.

Thus the reconstructed `#Top` is a theorem of an inadequate transition system,
not a partial-correctness proof of the real program.

## 1. Input and provenance integrity

`/audit-input.json` is readable and declares:

- record layout `pipeline-v3`;
- problem `162-string-to-md5`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- candidate mount `/candidate`;
- trusted mounts `/reference/canonical.py`, `/reference/prompt.py`,
  `/reference/py2mpy.py`, and `/reference/reference-semantics`.

The mode/mount boundary is consistent: the trusted reference-semantics tree is
present. There is no infrastructure breach.

I read the required pipeline-v3 records: `/run.json`, `/task.json`,
`/generation-result.json`, all four JSON records under
`/generation-evidence/`, both Codex text logs, the generation prompt, and all
208 events in the one structured JSONL trace. The generation record's final
claim was that the combined proof printed `#Top`; I treated that only as an
untrusted claim and reconstructed it independently below. The structured trace
also records earlier command, parser, and shell-check failures before the
candidate's final successful run.

The campaign block in `/audit-input.json` equals
`/audit-campaign-lock.json` as a JSON object. The mounted lock's SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the audit-input value. Direct SHA-256 checks also match the recorded
values for the run manifest, task manifest, stage-one result, invocation,
metrics, runtime metrics, usage, prompt, logs, canonical, trusted prompt, and
translator.

An independently implemented path/kind/size/content tree hash produced:

- trusted semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- candidate semantics:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- candidate workspace:
  `e1dce0ac8f612cd7370e10c2116edde43f27bb0f850f630c24fca762c52961fa`;
- structured trace tree:
  `ea53f1ad7e254005c90c5a2c3067cd1da00b39deb0fee13e95ab2219ce1da02a`.

These respectively match the task/reference manifest, stage-one workspace
output, and usage source-trace hash. A recursive `diff -r --no-dereference`
between candidate and trusted semantics was empty. Neither tree contains a
symlink. Candidate `prompt.py` and `py2mpy.py` are byte-identical to their
trusted mounts. The required proof artifacts are real regular files. Candidate
compiled definitions and caches exist, but were not copied or used.

Evidence:

- [provenance commands and direct hashes](/audit-output/evidence/01_provenance.log)
- [independent tree-hash implementation](/audit-output/evidence/01_tree_hashes.py)
  and [results](/audit-output/evidence/01_tree_hashes.log)
- [structured-trace reader](/audit-output/evidence/01_trace_summary.py) and
  [complete compact rendering](/audit-output/evidence/01_trace_summary.log)

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for a string `text`, return its MD5 hash as a
string; return `None` for the empty string. The documented example is
`"Hello world" -> "3e25960a79dbc69b674cd4ec67a72c62"`.
The trusted canonical implements the nonempty case as
`hashlib.md5(text.encode("ascii")).hexdigest()`.

The candidate implements the same empty branch but uses
`text.encode("utf-8")`. This is not a harmless rewrite over unrestricted
Python strings:

- for ASCII strings, ASCII and UTF-8 bytes coincide;
- for non-ASCII strings, canonical ASCII encoding raises, while candidate
  UTF-8 encoding returns a digest.

Using the trusted translator in scratch:

```text
python3 py2mpy.py solution.py > solution.generated.mpy
# exit 0
cmp -s solution.generated.mpy solution.submitted.mpy
# exit 0
```

Both files have SHA-256
`152cecedd3cd0922513b15497b91fba41fa85541f0278d70a42749676cb75011`.
Thus submitted `solution.mpy` faithfully represents submitted `solution.py`.

The independent differential imported both trusted canonical and generated
entry points. It exercised the example, empty and one-character branch
boundaries, NUL, DEL, embedded NUL, whitespace, MD5 block-length boundaries,
deterministically generated ASCII strings, explicit non-ASCII boundaries, and
generated mixed-Unicode strings. Result: 27 cases, 18 matches, 9 mismatches.
Every mismatch was a non-ASCII case. Examples:

```text
input='é'
canonical=('raise', 'UnicodeEncodeError')
generated=('return', '66ddcd97cfdeabb2f6fb8a999b4bc76f')

input='🙂'
canonical=('raise', 'UnicodeEncodeError')
generated=('return', '5c8d6d302301d0e25c0e051418dff305')
```

The prompt contains no precondition restricting `text` to ASCII. This is a
material implementation-versus-canonical discrepancy on the intended string
domain, not merely thin test coverage.

Evidence:

- [scratch-copy commands](/audit-output/evidence/02_prepare_scratch.log)
- [differential source](/audit-output/evidence/02_differential.py)
- [translation and differential log](/audit-output/evidence/02_fidelity.log)

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/proof-162`, using the
trusted semantics tree. Before building, both `runtime-kompiled` and
`verification-kompiled` were absent. No candidate compilation output or cache
was reused.

Fresh build results:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# exit 0

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# exit 0
```

I split the original two claims into semantically identical, labeled audit
modules to run each target independently:

```text
kprove spec-empty.k --definition verification-kompiled \
  --spec-module SPEC-EMPTY
#Top
# exit 0

kprove spec-nonempty.k --definition verification-kompiled \
  --spec-module SPEC-NONEMPTY
#Top
# exit 0
```

The untouched combined candidate spec also closes:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
#Top
# exit 0
```

Fresh LLVM execution of the empty branch terminates with
`"audit_result" |-> noneV`, exit 0. A nonempty `"Hello world"` execution
reaches `md5hexCodes(iCons(72, iCons(101, ...)))`; LLVM then exits 113 because
the supplied `md5hexCodes` deliberately has no evaluator. This is a documented
primitive boundary, not a proof-reconstruction failure.

Evidence: [complete fresh build/proof/concrete log](/audit-output/evidence/03_rebuild_and_prove.log)
and [reconstruction script](/audit-output/evidence/03_rebuild_and_prove.sh).

## 4. Adequacy and real-program pinning

### Entry claims in plain language

The empty claim starts with an empty module scope, the supplied builtins scope,
empty heap/stack, and `#loadAll(solutionModule)` followed by a call to
`string_to_md5("")`. It says execution reaches `noneV`, restores all explicitly
mentioned runtime cells, and leaves the function closure in module scope.

The nonempty claim starts in the same state with an arbitrary `CS:IntSeq`
satisfying `CS =/=K .IntSeq`. It says a call with `str(CS)` reaches exactly
`str(md5hexCodes(CS))`, with the same explicitly mentioned final state.

Both preconditions are satisfiable. Concrete witnesses are the empty string
and `CS = [72,101,108,108,111,32,119,111,114,108,100]` for `"Hello world"`.
A ground specialization of the latter printed `#Top`, exit 0. Python canonical
and candidate both return
`3e25960a79dbc69b674cd4ec67a72c62` on that ASCII witness; both return `None`
on the empty witness.

The result is constrained, not a free variable or tautological implication:
`noneV` is required on empty input, and the exact opaque digest term is
required on nonempty input. Stage 6 confirms discrimination.

### Mechanical program identity

I parsed and macro-expanded both the submitted `solution.mpy` and the claim's
`solutionModule` using the fresh verification definition. The two KAST files
are byte-identical and share SHA-256
`14f908914feb54788a743a3ee1d420468945a63c3371427367f1609f9351cd34`.
This demonstrates constructor-level identity, including import, binding,
condition, encoding literal, nested calls, and return body. The candidate does
hard-code this macro rather than regenerating it automatically, but for this
immutable artifact that is only a maintenance observation.

I also changed the program term actually executed by the claim: the nonempty
return body was replaced with `Return(NoneVal)`. The mutant definition built,
but its nonempty claim failed with `WarnStuckClaimState`; the residual `<k>`
cell contained `noneV`. This demonstrates body sensitivity.

Evidence:

- [submitted expanded KAST](/audit-output/evidence/04_submitted_program.kast)
  and [claim expanded KAST](/audit-output/evidence/04_claim_program.kast)
- [pinning, ground proof, and body-mutant log](/audit-output/evidence/04_pinning_and_body_sensitivity.log)

### Adequacy failure despite pinning

Pinning is not the failing gate. The claim executes the submitted UTF-8 body.
The failure is that the supplied rules through which that body executes do not
model UTF-8 encoding for non-ASCII inputs, while the claim's precondition
admits every nonempty `IntSeq` without an ASCII guard.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The complete source inventory covers every K file in the supplied semantics,
plus `verification.k` and `spec.k`. It records every declaration/rule start,
source line, file SHA-256, and attribute occurrence. Totals are:

- 230 syntax declarations;
- 698 rules;
- 5 contexts;
- 1 configuration;
- 2 claims;
- 149 `[function]`, 110 `[total]`, 25 `[symbol]`,
  22 `[no-evaluators]`, 45 priority, 26 `owise`, 36 `concrete`,
  8 macro, and 1 macro-rec attribute occurrences;
- no `functional` declaration and no `simplification` rule.

The full 1,005-line index is
[05_inventory.txt](/audit-output/evidence/05_inventory.txt), generated by
[05_inventory.py](/audit-output/evidence/05_inventory.py).

The three proof-local declarations and their three rules are only macros:
`stringToMd5Body`, `solutionModule`, and `stringToMd5Closure`. They add no
function, totality axiom, ordinary operational rewrite, priority rule, opaque
symbol, lemma, or simplification. Their expansions are exact, as established
in stage 4. They are sound definitional factoring.

All supplied rules not reachable from this program's constructor and call
slice were dispositioned as outside this theorem's execution: numeric,
float, range, list, tuple, set, dict, comprehension, subscript, sort, assert,
and unrelated builtin/method rules cannot match a state on this run. I found
no false-conclusion witness involving those rules on the intended
`string_to_md5` input domain, so I do not label them unsound here. Their opaque
float and sorting symbols are also not theorem dependencies.

### Mapping of every used construct

| Program construct | Declaration and active rules | Assessment |
|---|---|---|
| `Module`, `Import`, `FuncDef`, `Params` | `syntax.k:42,53,57,61`; `core.k:124-127`; `float.k:61`; `functions.k:14-16` | Loading/sequencing and closure binding are deterministic. The import rule is inaccurate as noted below. |
| outer function call and parameter | `syntax.k:28`; `call.k:20-21,69-74`; `core.k:131-154,189-191`; `functions.k:63-75` | Left-to-right evaluation, binding, frame creation, and lookup match this one-parameter flow. |
| `If(UnaryOp("not", Name("text")),...)` | strictness in `syntax.k:14,49`; `operators.k:10`; `bool.k:8`; `core.k:199-205`; `controls.k:51-54` | Empty versus nonempty structural branch is correctly guarded and disjoint for `str(CS)`. |
| `NoneVal`, `Return` | `core.k:196`; strictness in `syntax.k:50`; `functions.k:78-90` | Empty return, abrupt removal of the remainder of the body, pop, and frame restoration match this flow. |
| `Str("")`, `Str("utf-8")` | `syntax.k:13`; `str.k:13-17` | Both literals are ASCII, so the guarded literal conversion is sound on these uses. |
| `text.encode("utf-8")` | generic attribute/call rules in `call.k:16,20-24`; `methods.k:58` | **Unsound on admitted non-ASCII inputs.** The rule ignores both encoding name and code-to-byte conversion. |
| `hashlib.md5(...).hexdigest()` | no-op import `float.k:61`; priority bridge `builtins.k:279-285`; generic outer attribute/method dispatch `call.k:16,20-24` | The bridge bypasses import binding and name lookup. Its result is the opaque external primitive `md5hexCodes`. |
| proof macros | `verification.k:8-30` | Exact constructor-level factoring; no semantic shortcut. |

Relevant rule guards are disjoint where needed: empty/nonempty truthiness,
true/false branch rules, ordinary versus priority MD5 call routing, and return
versus fall-through. Parameter and code-sequence recursions descend. No
relevant proof-local totalization, overlap, or simplification exists.

### Materially unsound used encoding rule

`reference-semantics/semantics/methods.k:58` is:

```k
rule applyMethod(str(CS:IntSeq), "encode", str(_:IntSeq), .Vals) => str(CS)
```

Although the nearby comment says `S.encode('ascii')`, the rule:

- accepts every encoding-name string;
- has no `0 <= code < 128` guard;
- treats Unicode code points as output bytes;
- matches the submitted `"utf-8"` call.

Concrete false-conclusion witness on a satisfying intended input:

```text
text='é'
K/source code points:       [233]
actual Python UTF-8 bytes:  [195, 169]
candidate actual digest:    66ddcd97cfdeabb2f6fb8a999b4bc76f
MD5 of identity byte [233]: 3406877694691ddd1dfb0aca54681407
```

The candidate returns the first digest. Under the semantics' named contract
that `md5hexCodes(CS)` is MD5 of the passed code sequence, the K claim instead
passes `[233]` and denotes the second digest. The digests differ. If
`md5hexCodes` is left wholly uninterpreted, the K theorem establishes no MD5
meaning at all; either interpretation fails to prove the intended result.

This rule is exercised, not merely present off path. A ground claim starting
with `str(iCons(233,.IntSeq))` and ending with
`str(md5hexCodes(iCons(233,.IntSeq)))` prints `#Top`. The exact concrete and K
results are preserved in
[05_encoding_witness.log](/audit-output/evidence/05_encoding_witness.log);
the independent witness source is
[05_encoding_witness.py](/audit-output/evidence/05_encoding_witness.py).

This is the required false-conclusion witness for the soundness finding.

### Import/name-resolution state mismatch

`reference-semantics/semantics/float.k:61` rewrites every `Import(_)` to `.K`,
and the priority rule at `builtins.k:280` recognizes the syntax
`Name("hashlib")` without looking up its binding. In real Python, executing the
submitted top-level import binds `hashlib` in the module globals. The candidate
claims instead end with a module map containing only the function closure.

The concrete witness reports `hashlib_in_module_globals=True` and a module
binding in Python
([05_import_state_witness.log](/audit-output/evidence/05_import_state_witness.log));
the clean LLVM final scope in
[03_rebuild_and_prove.log](/audit-output/evidence/03_rebuild_and_prove.log)
contains the function and audit result but no `hashlib`. The priority bridge
therefore skips an observable state change and admits no environment/binding
guard. For this exact unshadowed program the selected real binding would be the
same library function, so this mismatch is secondary to the encoding witness,
but it is not a faithful complete-state model.

### Opaque MD5 trust boundary

`md5hexCodes(IntSeq)` is `[function,total,symbol,no-evaluators]` with no
equations. It directly influences the final result and the postcondition uses
the same symbol. No K theorem establishes 32-character hexadecimal output or
equivalence to standard MD5.

I classify the digest calculation itself as an explicitly named external
primitive: `hashlib.md5` is outside the program-defined wrapper being proved.
It can be a conditional trust boundary if the theorem is honestly read as
"the wrapper returns the result of a trusted MD5 primitive on these exact
bytes." It is not independent verification of MD5. This would be a trust/evidence
limitation rather than a false K equation by itself. The fatal issue is that
the preceding encoding bridge does not deliver the real bytes to that
primitive.

## 6. Fresh non-vacuity test

I created a new ground spec for satisfying input `"a"` and changed the required
result from the digest to `noneV`. Python confirms the real candidate returns
`0cc175b9c0f1b6a831c399e269772661`, not `None`.

The mutated spec parsed and built:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
# exit 0
```

The actual proof then failed for the intended reason:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
# WarnStuckClaimState
# residual k: str(md5hexCodes(iCons(97,.IntSeq)))
# destination: noneV
# exit 1
```

This is a meaningful, reachable unmet result obligation, not a parse failure,
timeout, missing import, or unrelated crash. The original proof is
discriminating. Evidence:
[false mutation and full log](/audit-output/evidence/06_nonvacuity.log) and
[runner](/audit-output/evidence/06_nonvacuity.sh).

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY rewrite theory:

- loading the macro-expanded submitted module and calling the function with
  empty string reaches `noneV`;
- for every structural nonempty `CS:IntSeq`, the same execution reaches
  `str(md5hexCodes(CS))`;
- explicitly mentioned environment, scope, heap, allocation, stack, return,
  and exception cells reach the stated K final pattern.

The proof executes the exact submitted constructor body and constrains its
result. It is body-sensitive and non-vacuous.

It does **not** establish:

- equivalence of `solution.py` to the trusted canonical on all strings;
- correct ASCII failure behavior for non-ASCII canonical inputs;
- correct UTF-8 code-point-to-byte conversion for the submitted program;
- a real `hashlib` import binding or binding-sensitive MD5 call;
- any mathematical or executable characterization of `md5hexCodes`;
- that the opaque result has 32 lowercase hexadecimal characters;
- correspondence of the proved non-ASCII K states to real Python execution.

### Trust ledger

| Boundary | Dependents and influence | Judgment |
|---|---|---|
| K toolchain and builtin Int/Bool/String/Map/List hooks | Parsing, rewriting, guards, frames, all claims | Standard low-level checker boundary; versions independently observed as K 7.1.293. |
| Trusted translator `/reference/py2mpy.py` | Python-to-constructor identity | Acceptable here because fresh regeneration is byte-identical. |
| Three proof-local macros | Exact body/module/closure terms | Acceptable definitional factoring; mechanical expansions match. |
| Supplied operational semantics | Entire execution correspondence | Not acceptable on the used non-ASCII path because `encode` identity has a concrete false-conclusion witness; import state is also omitted. |
| `md5hexCodes` | Entire nonempty return value | Explicit external primitive assumption, not proven MD5. Conditionally acceptable only if its contract and exact byte input are trusted; the exact-byte premise fails here. |
| CPython `hashlib` and trusted canonical | Differential oracle | Useful executable reference. Finite tests do not repair the universal K bridge. |
| Differential sample | 27 documented/boundary/generated inputs | Reproducible finite evidence; it exposes 9 real divergences and is not treated as proof. |

Gate A (real-program soundness) fails because a used operational encoding rule
produces the wrong byte sequence and therefore can close a false execution
summary on `"é"`. Gate B (intent adequacy) fails because the generated program
differs materially from the unrestricted trusted canonical domain. Gate C
evidence is reproducible, and the proof is non-vacuous, but those later facts
cannot rescue Gates A or B.

The benchmark decision boundary therefore requires `FAIL / NOT_LEGIT`, even
though clean `kprove` reconstruction succeeds.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
