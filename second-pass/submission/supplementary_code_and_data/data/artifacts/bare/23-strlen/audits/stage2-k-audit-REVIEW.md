# Independent adversarial review: 23-strlen

The candidate has a clean, non-vacuous K reachability proof of a theorem about
its own generated model, but it does not establish the unrestricted HumanEval
contract. The model relies on K's incomplete backend representation of Unicode
strings. Normal concrete input `"😀"` is represented as four byte-valued K
characters and returns `4`, while the trusted canonical and submitted Python
program both return `1`. This materially narrows the `str` domain and is
verdict-determinative under the benchmark's decision boundary.

## 1. Input and provenance integrity

The launcher record declares:

- problem `23-strlen`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- no mounted reference semantics.

I inspected `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required generation records, the
present `usage.json`, both legacy-import records, the 133-record structured
trace, and bounded relevant portions of the 1,237,834-byte generation log.
Generation claims such as the earlier `#Top` were not reused as proof evidence.

The independent checker
[provenance_check.py](evidence/provenance_check.py) establishes that every
launcher-declared mount and every record required by
`legacy-selected-stage1` is readable and has the required real file/directory
type. It recursively rejects symlinks and unsupported nodes. There are no
symlinks in the candidate, reference, or generation trees. The candidate's
required proof artifacts are present as regular files.

The campaign lock is JSON-identical to the `audit_campaign` block and has the
declared SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded file digest checked by the script matches, including
the run/task/result/invocation manifests, canonical, trusted prompt and
translator, generation prompt/metrics/usage/log/last-message, and candidate
prompt and translator. The candidate prompt and translator are byte-identical
to their trusted mounts.

An independent pipeline tree digest of `/candidate` is
`7fd1909a9dce579eb8e6a42b0d866e411a175612715ff95a1a28d9d771c5a4c8`,
matching both the generation result and invocation's retained workspace hash.
The corresponding trace digest is
`59cc1acfa0f5a9dd4ccd100668187dcf8f5ab0bbc3ab5ff6fd4e6661e1e2feea`,
matching `usage.json`; each trace file also matches the per-file hash in the
generation result. The launcher-level tree values recorded under its separate
tree-hash convention were also recorded by the checker.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist, the audit manifest says not to
mount it, and all corresponding trusted/candidate hashes are null. The absent
`runtime-metrics.json` is expected for this legacy-selected layout and is not a
defect.

Evidence:

- [stage1-provenance.log](evidence/stage1-provenance.log), exit 0;
- [stage1-trace-summary.log](evidence/stage1-trace-summary.log), exit 0;
- [stage1-generation-log-summary.log](evidence/stage1-generation-log-summary.log),
  exit 0.

There is no infrastructure breach, so the candidate audit continues.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires:

```text
strlen(string: str) -> int
Return the length of the given string.
Examples: strlen("") == 0 and strlen("abc") == 3.
```

The trusted canonical is `return len(string)`. The submitted
`solution.py` has the same annotated signature and exactly the same executable
body. Omitting the canonical docstring has no behavioral effect.

I regenerated the IR with:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
```

The command exited 0. `cmp` exited 0, and the submitted and regenerated files
both have SHA-256
`508c92dec7b8810291f0fa18ef567c25d5e8f398d62952cff2bd359697d6aebf`.
See [stage2-translation.log](evidence/stage2-translation.log).

The independent differential script imports the two functions from separate
paths. It covers both documented examples, empty and one-character boundaries,
NUL, newline, quote/backslash values, Latin-1, combining characters, astral
Unicode, a ZWJ sequence, a lone surrogate at the Python layer, a length-4096
string, and 500 deterministic generated strings. The implementation has no
branches, so there are no internal branch boundaries beyond the empty/nonempty
length boundary. All 514 cases agree:

```text
total_cases=514 mismatches=0
```

Evidence:

- [differential_test.py](evidence/differential_test.py);
- [stage2-differential.log](evidence/stage2-differential.log), exit 0.

The Python implementation is faithful to the canonical over the tested source
domain. This finite test is not used as a substitute for the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts to
`/tmp/audit-work/23-strlen.30KKVy/work`. No candidate-provided K compiled
definition or cache was copied or used.

The generated semantics was freshly compiled for concrete execution:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
```

This exited 0. See
[stage3-build-concrete.log](evidence/stage3-build-concrete.log).

The proof definition was freshly compiled:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0. See [stage3-build-proof.log](evidence/stage3-build-proof.log).

There is exactly one positive claim. I independently ran:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`. See
[stage3-positive-proof.log](evidence/stage3-positive-proof.log).

Fresh concrete execution is where the material defect appears. Eleven
normal/boundary values were compared directly with Python:

| Input | Python | Rebuilt K |
|---|---:|---:|
| `""` | 0 | 0 |
| `"abc"` | 3 | 3 |
| `"é"` | 1 | 1 |
| `"e\u0301"` | 2 | 3 |
| `"😀"` | 1 | 4 |
| `"a😀é"` | 3 | 6 |
| `"👩‍💻"` | 3 | 11 |

The complete run reports `TOTAL_CASES=11 MISMATCHES=4` and exits 1 because
the test correctly treats these as semantic mismatches. Both the independently
built LLVM definition and the fresh Haskell definition produce the same
Unicode failures. The Haskell result cell for `"😀"` is `Int(4)`, and the local
value is printed as `Str("\xf0\x9f\x98\x80")`.

Evidence:

- [concrete_semantics_test.py](evidence/concrete_semantics_test.py);
- [stage3-concrete-execution.log](evidence/stage3-concrete-execution.log),
  expected audit-test exit 1 with four mismatches;
- [stage3-haskell-concrete.log](evidence/stage3-haskell-concrete.log), all
  `krun` commands exit 0 and reproduce the wrong values.

Thus clean proof closure is real, but the freshly rebuilt generated semantics
does not agree with the real Python program on the full intended domain.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

Precondition:

- `S` is any K `String`;
- `<k>` contains the translated `strlen` module followed by invocation of that
  binding on `Str(S)`;
- the function and local maps are empty;
- the result is `noResult`.

Postcondition:

- `<k>` is empty;
- the exact `strlen` function binding has been installed;
- the local `"string"` is bound to `Str(S)`;
- the result is `Int(lengthString(S))`.

There is no additional guard or finite-size bound. A satisfying state exists,
for example `S = "abc"` with the exact empty cells above. Ground source
execution gives 3 in both Python implementations. For normal Unicode input
`"😀"`, both Python implementations give 1 while concrete generated-semantics
execution gives 4.

### Program identity

The mechanical constructor parser independently extracted the `Module(...)`
tree from regenerated `solution.mpy` and the claim. The trees are exactly
equal, including:

```text
FuncDef("strlen", Params("string"),
  Return(Call(Name("len"), Name("string"))))
```

See [pinning_check.py](evidence/pinning_check.py) and
[stage4-pinning.log](evidence/stage4-pinning.log). This is not a substituted
body. The claim also executes module loading, function lookup, local lookup,
the call, and return rules rather than jumping directly to its postcondition.

### Result and body sensitivity

The result is constrained, not free or tautological. A fresh body mutation
changed the actual claim term and final installed binding to
`Return(Int(0))`, while retaining the length postcondition. It parsed with
`--dry-run` (exit 0), then the proof exited 1 with the expected unmet
obligation:

```text
0 #Equals lengthString(S)
```

`S = "a"` is a concrete false witness. See
[spec-body-mutation.k](evidence/spec-body-mutation.k) and
[stage4-body-sensitivity.log](evidence/stage4-body-sensitivity.log).

The pinning and non-bypass checks therefore pass. Adequacy fails at the
result-bearing Python-string/K-string bridge, not at program identity or claim
vacuity.

## 5. Rule-by-rule static soundness review

The candidate has exactly three K sources: `semantic.k`, `verification.k`, and
`spec.k`; there are no generated helper K files. The numbered exhaustive source
and declaration/rule extraction is preserved in
[stage5-rule-inventory.log](evidence/stage5-rule-inventory.log).

### Local syntax and declarations

`MPY-SYNTAX` declares every one of the following:

1. `Pgm ::= Module(Stmt)`;
2. `Stmt ::= FuncDef(String, Params, Stmt)`;
3. `Stmt ::= Return(Expr)`;
4. `Params ::= Params(String)`;
5. `Expr ::= Value`;
6. `Expr ::= Name(String)`;
7. `Expr ::= Call(Expr, Expr)`;
8. `Value ::= Str(String)`;
9. `Value ::= Int(Int)`.

`MPY` additionally declares:

10. `KItem ::= invoke(String, Value)`;
11. `KItem ::= callLen`;
12. `KItem ::= finishReturn`;
13. `Function ::= function(String, Stmt)`;
14. `Result ::= noResult`;
15. `Result ::= Value`.

`VERIFICATION` declares:

16. `Bool ::= strlenPost(Value, Value) [function, total]`.

There are no local `functional`, opaque, simplification, priority, or `owise`
declarations. There are no local syntax macros or strictness-generated rules.

The configuration has only the state needed by the submitted program:
`<k>`, `<functions>`, `<locals>`, and `<result>`. It creates the exact
program-then-invocation sequence. No heap, allocation, I/O, exception, or loop
state is needed for this straight-line program on a valid `str`.

### Used-construct map

| Submitted constructor/control | Declaration and behavior |
|---|---|
| `Module` | syntax item 1; rule 1 unwraps it |
| `FuncDef` and `Params` | syntax items 2/4; rule 2 installs the exact binding |
| `Return` | syntax item 3; rules 7/8 evaluate and expose the result |
| `Call(Name("len"), ...)` | syntax items 6/7; rules 4/5/6 evaluate the argument and length |
| input `Str` and output `Int` | syntax items 8/9; configuration and rules 3/6/8 |
| function invocation/local binding | items 10/13; rule 3 |

Every submitted constructor has a declaration and a rule path; there is no
silent unmodeled used construct.

### Operational and verification rules

1. `Module(S) => S`: correct for this one-statement translated module and
   preserves the invocation continuation.
2. `FuncDef(...) => .K` with map update: correct for the exact top-level
   definition and body.
3. `invoke(F,V) => BODY` with binding lookup and fresh one-entry locals:
   correct in the reachable top-level invocation. It lacks a call stack and
   would be too broad for nested user calls, but no such call is constructible
   by the submitted body; there is no intended-domain false witness for this
   task.
4. `Name(X) => V` under local lookup: correct for `"string"`.
5. `Call(Name("len"), E) => E ~> callLen`: preserves argument-first
   evaluation. The submitted module has no global/shadow binding for `len`, so
   the selected binding is the Python builtin on the real path.
6. `Str(S) ~> callLen => Int(lengthString(S))`: internally executes K's
   `STRING.length` hook, but it is not a sound fully validated interpretation
   of Python `len(str)` through this semantics' input interface. This is the
   verdict-determinative rule/representation boundary, detailed below.
7. `Return(E) => E ~> finishReturn`: correct evaluation order.
8. `V ~> finishReturn` sets `<result>` and ends computation: correct because
   this return is the whole body and has no caller continuation. The generic
   rule would not model arbitrary Python stack unwinding, but that broader
   context is unreachable in the submitted program.
9. `strlenPost(Str(S), Int(N)) => N ==Int lengthString(S)`: a truthful
   restatement of the K-level postcondition for its one matched shape, but it
   inherits the Python/K bridge limitation if interpreted as the HumanEval
   contract. Its `[total]` declaration has no equations for other
   `Value × Value` shapes, so its reusable totality coverage is unsupported.
   It is not referenced by the target claim. A fresh definition with the
   entire declaration/rule removed still compiles and proves `#Top`; see
   [stage5-unused-extension-check.log](evidence/stage5-unused-extension-check.log).
   I therefore do not attribute a false target conclusion to this unused
   annotation.

The reachable operational rules have disjoint heads or distinct continuation
markers. There are no priority interactions, overlapping equations, recursive
functions, or totalization guards on the target path.

### Concrete false-conclusion witness for the Unicode boundary

The installed K documentation explicitly says its backend Unicode string
implementation is incomplete and does not fully support encodings or code
points beyond the first 256 Basic-Latin/Latin-1 points. It identifies
`lengthString` as the total hook `STRING.length`. The exact text is preserved
in [stage5-k-string-boundary.log](evidence/stage5-k-string-boundary.log).

Two independent literal forms beyond Latin-1 reproduce the mismatch:

```text
U+0100: Python len("Ā") = 1; rebuilt K result = 2
U+1F600: Python len("😀") = 1; rebuilt K result = 4
```

See [unicode_escape_test.py](evidence/unicode_escape_test.py) and
[stage5-unicode-escape-witness.log](evidence/stage5-unicode-escape-witness.log).

The representational failure is also machine-checkably connected to the
universal claim:

1. normal `krun` input `"😀"` becomes
   `Str("\xf0\x9f\x98\x80")` and returns 4;
2. that four-byte K string satisfies the universal claim's `S:String`
   precondition;
3. a ground instance with the exact translated body and that exact K value
   dry-runs successfully and proves `#Top` with result 4;
4. trusted canonical and submitted Python execution both return 1.

See
[spec-unicode-encoded-false-conclusion.k](evidence/spec-unicode-encoded-false-conclusion.k)
and
[stage5-encoded-false-conclusion-witness.log](evidence/stage5-encoded-false-conclusion-witness.log).
This is the required false real-program conclusion witness for the
result-bearing input/length bridge.

For completeness, a K source-level `"\U0001F600"` token constant-folds to
length 1 in the prover, while the same normal value passed through `krun` is
represented as four byte-valued characters. The failed attempted result-4
source-token claim is preserved in
[stage5-source-literal-backend-discrepancy.log](evidence/stage5-source-literal-backend-discrepancy.log).
This does not rescue the candidate: it exposes the absence of a uniform,
validated Python `str` to executable K `String` bridge.

## 6. Fresh non-vacuity test

There is no candidate `spec-vacuity.k`. I created a fresh mutation retaining
the exact submitted body while changing only the result obligation to:

```text
Int(lengthString(S) +Int 1)
```

`S = ""` is a satisfying witness: the actual model result is 0 while the
mutated obligation demands 1.

Commands and results:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
DRY_RUN_EXIT=0

kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
PROOF_EXIT=1
```

The second run emitted `WarnStuckClaimState` on the expected unmet implication:

```text
lengthString(S) +Int 1 #Equals lengthString(S)
```

This is a meaningful proof failure, not a parser error, timeout, missing
import, or unrelated crash. See
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) and
[stage6-false-postcondition.log](evidence/stage6-false-postcondition.log).
The target claim passes non-vacuity.

## 7. Proven versus assumed accounting

### What is formally proven

Under the candidate K definition, for every K `String` term `S`, the exact
translated `strlen` module and invocation rewrite from empty function/local
maps and `noResult` to:

- empty computation;
- the exact installed function body;
- local binding `"string" |-> Str(S)`;
- result `Int(lengthString(S))`.

The proof is universal over its K sort, executes the exact body, is
body-sensitive, and constrains the result. It is not merely examples or bounded
unrolling.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K map update/lookup and K sequencing | loading, binding, evaluation order | Acceptable low-level primitives; exact-path behavior is exercised and uncontroversial |
| K `Int` and equality hooks | result representation and unused `strlenPost` | Acceptable for this nonnegative finite length computation |
| K `STRING.length` plus Python-`str`/K-`String` input representation | rule 6 and the target result | Illegitimate for the unrestricted contract: documented incomplete Unicode support and concrete false witnesses |
| Trusted translator | source-to-IR identity | Mechanically regenerated byte-for-byte |
| IR-to-claim identity | real-program pinning | Mechanically compared as constructor trees; lack of automatic spec generation is only a maintenance observation |
| Python differential testing | implementation/canonical bridge | 514-case finite support only; not used as universal proof |
| `strlenPost [function,total]` | none | Incomplete outside its one equation but demonstrably unused by target closure |

There are no proof-local lemmas, operational shortcuts in `verification.k`,
opaque or fresh result symbols, loop summaries, priorities, or imported
candidate caches. The prior generation trace and `#Top` were not trusted.

### Gate and benchmark decision

- Real-body execution, pinning, result constraint, and non-vacuity: pass.
- Formal closure under the candidate K model: pass.
- Full source-domain language adequacy: fail.
- Reproducibility of the audit evidence: pass.

The internally sound K theorem is limited by a material source-contract domain
failure: only the backend's reliably supported string range can be connected to
normal executable inputs without the demonstrated byte-count divergence.
HumanEval's `str` contract contains no ASCII or Latin-1 restriction. Under the
benchmark's explicit mapping, this kind of `SOUND-BUT-LIMITED` domain
narrowing is `FAIL / NOT_LEGIT`, not a non-fatal concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
