# Independent adversarial review: 51-remove-vowels

The candidate contains a legitimate, result-constraining K reachability proof
of the submitted constructor program under its generated semantics. The proof
was rebuilt from source, the sole positive claim independently closed with
`#Top`, real-program pinning is mechanical, and both body- and result-changing
mutations fail meaningfully. The concern is not a false rule on the submitted
execution path: it is that the final HumanEval-intent bridge remains
conditional on K's external String/`replaceAll` implementation and finite
K-versus-CPython evidence. K's own documentation cautions that its Unicode
String implementation is incomplete beyond Latin-1.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `51-remove-vowels`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- complete input provenance; and
- no mounted reference semantics.

I read `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`legacy-metrics.json`, `legacy-run-input.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and all 237 JSONL records in the structured
trace. Historical runtime metrics are not present and are not required for
this layout. The generation report's `KPROVE_PASSED` statement was treated
only as an untrusted historical claim.

The campaign-lock JSON object is exactly equal to the `audit_campaign` object
in `/audit-input.json`, and its bytes hash to the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All declared records are real regular files/directories, not symlinks, and
the launcher mounts are read-only. Recorded hashes for the run, task,
generation result, canonical source, prompt, translator, invocation, metrics,
usage, generation prompt, last message, and output log all match independently
computed SHA-256 values.

The structured trace's only file hashes to the value recorded in
`generation-result.json`; its pipeline tree hash matches
`usage.json:source_trace_sha256`. The mounted candidate's pipeline tree hash is
`8494f5f7fe43be62e36bcc3df3c4c2177959ed878f1d7f8b1e29ca58b6c5c55b`,
matching both the retained workspace and stage-1 result. `/audit-input.json`
also records launcher aggregate digests using an unspecified tree
serialization; I did not compare those values to a differently serialized
pipeline digest. Every constituent mounted file was independently hashed and
inventoried.

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted `/reference` versions. `/reference/reference-semantics` is absent, as
required for generated semantics. All required proof artifacts are present
inside the intact candidate mount. There is no infrastructure breach.

Evidence:

- `evidence/01-integrity.log`
- `evidence/01-mounts.log`
- `evidence/check_integrity.py`

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for an input string, return a string with
the vowels removed, preserving every other character and its order. The
trusted canonical implementation keeps a character exactly when
`character.lower()` is not one of `a`, `e`, `i`, `o`, `u`.

The candidate implementation at `/candidate/solution.py:1` instead performs
ten sequential `str.replace(vowel, "")` operations, covering lowercase and
uppercase ASCII vowels. This is a different algorithm but has the same
behavior on the source-contract domain.

Trusted regeneration:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py
```

produced SHA-256
`1b0f4951b9dbf084dcb7a3542bf3259efff37c566a6322023be96a16d7de0d14`,
byte-identical to submitted `solution.mpy`.

The independent differential program imported both trusted
`/reference/canonical.py` and the scratch candidate. It checked all six prompt
examples, 16 explicit boundary cases, 5,840 deterministic generated strings,
and every one of Python's 1,114,112 one-character strings, including surrogate
code points. It found zero mismatches. The exhaustive singleton run also
confirmed that the canonical implementation removes exactly the ten ASCII
code points `AEIOUaeiou`; there are no additional Unicode characters whose
`lower()` value is one of those one-character strings.

Evidence:

- `evidence/02-regenerate-mpy.log`
- `evidence/differential.py`
- `evidence/02-differential.log`

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/candidate`; no
candidate-provided kompiled definition or cache was reused. The observed tools
are K 7.1.293.

Fresh builds:

```text
kompile semantic.k --syntax-module MPY-SYNTAX --main-module MPY \
  --backend haskell --output-definition semantic-haskell-kompiled

kompile verification.k --syntax-module MPY-SYNTAX \
  --main-module VERIFICATION --backend haskell \
  --output-definition verification-kompiled
```

both exited 0. `spec.k` contains one positive target claim and no helper
claims. Its independent proof command:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

exited 0 and printed exactly `#Top`.

The independently compiled Haskell concrete semantics was then run on all six
examples and normal/boundary inputs: empty, each branch type, all vowels,
mixed endpoints, newlines, NUL/control bytes, Latin-1 and non-Latin-1 text,
combining marks, emoji, and a long input. All 18 K results matched both Python
implementations.

An LLVM definition also built successfully, but its concrete run stopped at
`deleteAll("abcdef","a")` with exit 113 because this candidate expresses the
helper only as a `[simplification]` rule. This is a backend-portability
limitation, not a failed required proof: Haskell is a documented concrete and
proof backend, the candidate's `prove.sh` selects Haskell, and the fresh
Haskell concrete run is successful.

Evidence:

- `evidence/03-toolchain.log`
- `evidence/03-kompile-semantic-haskell.log`
- `evidence/03-kompile-verification-haskell.log`
- `evidence/03-kprove-spec.log`
- `evidence/concrete_compare.py`
- `evidence/03-concrete-compare.log`
- `evidence/03-kompile-semantic-llvm.log`
- `evidence/03-krun-smoke-one.log`

## 4. Adequacy and real-program pinning

### Formal entry claim

There is no explicit `requires` clause. Its precondition is therefore:

- `INPUT` is any K `String`;
- `<k>` contains the complete submitted `Module(FuncDef(...))` constructor
  term;
- `<input>` contains `INPUT`; and
- `<result>` contains `noResult`.

Its postcondition is:

- `<k>` is exactly `done`;
- `<input>` is preserved; and
- `<result>` is exactly `result(removeVowelsSpec(INPUT))`.

The result is neither free nor existential and there is no one-way `ensures`
that weakens equality. Satisfying initial states are immediate: for example
`INPUT = ""`, `"b"`, or `"aaBAA"`. Fresh concrete runs produce respectively
`""`, `"b"`, and `"B"` in K and in both Python functions.

### Mechanical program identity

A reviewer script removed layout whitespace outside quoted tokens and compared
the regenerated `solution.mpy` term with the term before `=> done` in the
claim's `<k>` cell. Both normalized terms have 508 bytes and are identical.
The exact `remove_vowels` binding, `text` parameter, return body, ten nested
calls, receiver structure, method names, arguments, and order are pinned.
There are no helper or loop claims and no omitted program-defined body.

The generated semantics' direct-entry rule is a small execution adapter:
for this exact one-function module it binds the sole parameter to `<input>`
and evaluates the exact returned expression. This is recognizable,
constructor-level alignment rather than a substituted summary.

### Body sensitivity

`evidence/spec-body-mutation.k` changes the final literal in the actually
executed claim body from `"U"` to `"X"` while leaving the result contract
unchanged. The mutation dry-runs successfully, then `kprove` exits 1 with
`WarnStuckClaimState` on equality between the `"X"`-deletion and
`"U"`-deletion terms. `INPUT = "X"` is a concrete false witness: the mutated
body returns `""`, while the contract returns `"X"`.

Evidence:

- `evidence/pinning_check.py`
- `evidence/04-pinning.log`
- `evidence/spec-body-mutation.k`
- `evidence/04-body-mutation-dry-run.log`
- `evidence/04-body-mutation-kprove.log`

## 5. Rule-by-rule static soundness review

The complete declaration-level inventory is in
`evidence/05-rule-inventory.md`. There are no generated helper K files.
It enumerates all 18 local syntax/function declarations, the configuration,
all ten local equations/semantic rules, and the sole claim. There are no local
priority rules, `owise` rules, strictness attributes, fresh symbols,
allocation rules, exception rules, proof-local operational rules, or
`functional` declarations.

### Target construct coverage

- `Module`, `FuncDef`, `Params`, and `Return` are matched by the direct-entry
  rule at `/candidate/semantic.k:46`.
- `Name` is evaluated by the guarded parameter lookup at line 32.
- `Str` is evaluated by line 34.
- Every exact `Call(Attribute(E,"replace"),Str(OLD),Str(NEW))` is evaluated by
  lines 35–36.
- Each resulting string replacement with `NEW = ""` is evaluated by line 37.
- Concrete deletion is delegated to the fixed K `STRING.replaceAll` hook by
  lines 22–24.
- The exact terminal string value updates the only observable result cell at
  lines 50–51.

All constructors in the regenerated target are covered. Receiver evaluation
is recursive; the arguments are literals and effect-free, so target evaluation
order is preserved. The exact name guard pins the sole parameter. The target
has no mutation, heap, allocation, I/O, exceptions, or abrupt control effects,
so the three-cell configuration is sufficient. The finalization rule matches
an exact `<k>` cell rather than an arbitrary continuation and cannot discard
framed work.

### Per-rule conclusions

| Rules | Conclusion |
|---|---|
| `deleteAll` concrete simplification | A definitional wrapper around documented, total K `STRING.replaceAll`; no overlap. Symbolically opaque by design and classified as an external result-bearing primitive. |
| `eval(Name...)` | Correct single-parameter lookup under exact String equality; disjoint shape and guard. |
| `eval(Str...)` | Correct literal evaluation; disjoint and effect-free. |
| `eval(Call(Attribute(...,"replace"),...))` | Correct for every submitted call shape; recursively evaluates the receiver and pins the method name. |
| `replaceValue(...,OLD,"")` | Correct on every real program use, whose `OLD` is a fixed nonempty one-character vowel. |
| direct module entry | Correct for the exact pinned one-function module; preserves a framed suffix and reads only the input. |
| terminal `strVal` rule | Correctly writes the result only from `noResult` and only with no active continuation. |
| three verification equations | Unconditional, one-step, nonrecursive, complete, pairwise separate definitions. Each `[total]` declaration has one unguarded equation over all K Strings. |

The symbolic `deleteAll` term appears in execution and in the postcondition.
That would be circular if it summarized program-defined computation. Here it
represents external Python/K String replacement, while all ten
program-defined nested calls still execute. The concrete equation grounds
every ground use in K's fixed `replaceAll` hook. It is therefore an explicit
trusted primitive, not an unconstrained program oracle.

The `replaceValue` rule is syntactically broader than the target because it
also admits an empty `OLD`. CPython evaluates `"abc".replace("", "")` to
`"abc"`, while a bounded five-second K probe of that unused case did not
finish. A separate overlapping nonempty-needle probe
`"aaa".replace("aa","")` did match Python and return `"a"`. The timeout is not
a false-conclusion witness, and no satisfying target input can change any of
the ten fixed nonempty needle literals. Following the required witness rule,
this is recorded as a semantics-reuse/evidence gap, not labeled an unsound
target rule.

No candidate-local rule was found that enables a concrete or symbolic false
result for the intended target domain. The rules do not encode a fixed answer,
fabricate a result, skip a program-defined helper, or broaden the theorem to a
free value.

Evidence:

- `evidence/05-rule-inventory.md`
- `evidence/05-k-string-hook.log`
- `evidence/05-k-replace-hook.log`
- `evidence/replace-empty.py`
- `evidence/05-empty-needle-timeout.log`
- `evidence/replace-overlap.py`
- `evidence/05-overlap-replace.log`

## 6. Fresh non-vacuity test

The reviewer-created `evidence/spec-vacuity.k` keeps the complete executed
program unchanged but replaces the result with the false universal obligation
`result("")`. Its concrete satisfying counterexample is `INPUT = "b"`: the
actual and specified vowel-removal result is `"b"`, not empty.

The mutation's `--dry-run` exited 0, proving it builds and reaches the backend.
The actual proof exited 1 with `WarnStuckClaimState`; its residual explicitly
contains the unmet equality between `""` and the nested ten-deletion result.
This is an expected logical failure, not a parse error, missing import,
timeout, or unrelated crash.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/06-vacuity-dry-run.log`
- `evidence/06-vacuity-kprove.log`

## 7. Proven versus assumed accounting

### What the successful proof establishes

Under the candidate's generated MPY semantics, for every K String `INPUT`,
starting the exact regenerated constructor program in the initial three-cell
configuration reaches `done`, preserves `INPUT`, and sets the result to:

```text
removeUpperVowels(removeLowerVowels(INPUT))
```

which expands to the exact ten sequential `deleteAll` applications. This is
an unrestricted symbolic K-String claim, not a finite-size proof, example
list, bounded unrolling, or narrowed character alphabet.

### Trust ledger

| Boundary | Influence | Status and evidence |
|---|---|---|
| K 7.1.293 compiler/prover/backend correctness | Entire machine check | Ordinary proof-tool trust boundary. Fresh builds and runs avoid candidate caches. |
| Trusted `py2mpy.py` transliteration | Program identity | Launcher-trusted input; candidate copy matches; trusted regeneration is byte-identical; claim term mechanically matches. |
| K `String` token/domain | Formal input and result values | Fixed external primitive. K documents Unicode strings but warns support beyond Latin-1 is incomplete. Valid non-Latin-1 cases worked; arbitrary CPython/K Unicode equivalence is not formally proved here. |
| K `STRING.eq` | Parameter lookup guard | Fixed, documented total String equality; only compares the exact parameter-name strings. |
| K `STRING.replaceAll` | Every returned character | Fixed, documented total external primitive. Ground `deleteAll` connects to it; 18 target concrete runs agree with CPython. |
| Symbolic `deleteAll` | Symbolic execution result and postcondition | Intentionally opaque wrapper around the external hook, not a program-defined oracle. The reachability theorem is conditional on this named primitive's interpretation. |
| Direct-entry module adapter | Meaning of “execute the function on INPUT” | Informal semantics-design bridge, supported by exact constructor matching, concrete runs, exact binding, and a failing executed-body mutation. |
| Ten ASCII deletions versus canonical `lower()` filter | HumanEval intent | Not a separate K theorem. Supported by the trusted canonical source, zero differential mismatches, and exhaustive checking of every Python singleton removal decision. |
| Partial correctness / source termination bridge | Python-level conclusion | The K target execution is finite under these rules; the CPython implementation is a fixed finite chain. The proof does not separately formalize CPython's runtime. |

The String/intent boundaries are acceptable enough for legitimacy because they
are fixed external primitives, no program-defined body is abstracted, the
formal domain is unrestricted K String, and no opposite result is admitted by
the target semantics. They nevertheless prevent an unqualified pass: the
symbolic theorem largely proves evaluation to the same deletion primitive used
to state the contract, while its full equivalence to CPython's Unicode String
behavior and the canonical filter remains an audited but non-formal bridge.

Gate A (real-program soundness) passes: exact body, state, binding, result,
body sensitivity, and non-vacuity all check. Gate B (intent adequacy) passes
for the material HumanEval string domain with the stated Unicode-model
limitation; there is no finite bound or alphabet restriction. Gate C
(auditability) passes because every trust boundary and empirical check is
reproducible, while the finite K/CPython bridge remains the reason for the
non-fatal concern.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
