# Independent adversarial review: 16-count-distinct-characters

The candidate has a real, non-vacuous reachability proof of its exact function
body under the supplied K definition. It does **not** prove the HumanEval
contract over the real Python `str` domain. The supplied definition models
lowercasing as ASCII `A`–`Z` plus 32, while CPython `str.lower()` performs
Unicode lowercasing, including mappings that merge characters and mappings
that expand one character into several. The unrestricted symbolic claim
therefore establishes results that are false of the submitted Python program
on valid source-contract inputs.

This is the benchmark's explicit material-domain-narrowing case: the natural
Kit status would be sound-but-limited relative to the fixed semantics, but the
required benchmark verdict is `FAIL / NOT_LEGIT`.

The evidence index is
`/audit-output/evidence/README.md`. Every command log begins with the exact
shell-escaped command and ends with its exit status.

## 1. Input and provenance integrity

Status: PASS; no infrastructure breach.

I read `/audit-input.json` first. It declares:

- problem `16-count-distinct-characters`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- a complete provenance record and the launcher container-path map.

`/reference/reference-semantics` is present, as required for this rendered
mode. The contrary generated-semantics condition is not present.

The reviewer checker at
`/audit-output/evidence/provenance_check.py` used `lstat`, independent SHA-256
hashing, JSON parsing, and a length-delimited tree-manifest digest. Its exact
run is `/audit-output/evidence/stage1-provenance.log`:

- `/audit-campaign-lock.json` is a real regular file, its JSON object equals the
  `audit_campaign` block byte-for-value, and its SHA-256 is the recorded
  `ad5dfc...d745`.
- All required `legacy-selected-stage1` records are real regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`.
- The structured trace is a real directory containing one regular JSONL file.
  All 99 JSONL records parse. The trace manifest hash
  `46660867...fb9c` equals the independently computed value recorded by
  `usage.json`.
- Every directly recorded file hash checked in the log matches, including the
  run/task/result/invocation manifests, generation prompt, metrics, usage,
  last/output logs, trusted canonical, prompt, and translator.
- The independently computed candidate workspace manifest hash
  `d1b150d8...fa8df` equals both the stage result and invocation records.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- Recursive comparison of candidate and trusted `reference-semantics/`
  found exactly the same 25 entries, entry kinds, and file bytes. There are no
  symlinks or additional/missing entries. Both independently produce the
  recorded pipeline-v2 semantics manifest hash
  `4e06397a...3789f`.
- The evidence hashes embedded in both `generation-result.json` and
  `invocation.json` match the mounted evidence files.

I also read the present legacy records `legacy-metrics.json` and
`legacy-run-input.json`. A historical `runtime-metrics.json` is absent, which
the prompt expressly permits for `legacy-selected-stage1`; it is not a defect.

The complete trace was parsed, and a bounded event/tool inventory was generated
at `/audit-output/evidence/stage1-trace-inventory.log`. It records 14 tool
calls and outputs, the prior build and `#Top` claims, and the final
`KPROVE_PASSED` report. Those records were treated only as untrusted historical
claims. None substitutes for the reconstruction below.

## 2. Program fidelity and candidate-versus-canonical checks

Status: PASS.

The trusted contract in `/reference/prompt.py` is: for an input Python string,
return the number of distinct characters without regard to case. The examples
require `xyzXYZ -> 3` and `Jerry -> 4`. The trusted implementation in
`/reference/canonical.py` is:

```python
return len(set(string.lower()))
```

`/candidate/solution.py` has the required entry-point signature and exactly the
same executable expression. For the intended typed domain, ordinary Python
strings, it is faithful to the canonical implementation.

In the isolated reconstruction directory, the trusted translator was run as:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.mpy solution.regenerated.mpy
```

Both commands succeeded, and both files have SHA-256
`2e97b9f3...fc9`; see
`/audit-output/evidence/stage2-translation.log`.

The independent differential oracle
`/audit-output/evidence/differential_test.py` separately imports the trusted
canonical entry point and submitted entry point. It tested:

- the documented examples and empty string;
- ASCII case-map boundaries around `A`, `Z`, `a`, and `z`;
- digits, punctuation, NUL, whitespace, and repeated characters;
- Unicode sigma, dotted capital I, sharp S, composed/decomposed accents,
  supplementary-plane letters, and emoji;
- every string of length at most three over a 12-character ASCII/Unicode
  boundary alphabet;
- 3,000 deterministic generated strings.

There were 4,624 unique inputs and zero mismatches. The complete corpus is
`/audit-output/evidence/differential-cases.json`; command and result are in
`/audit-output/evidence/stage2-differential.log`. This confirms Python
implementation fidelity only; it is not evidence of a universal K-to-Python
semantics bridge.

## 3. Clean proof reconstruction

Status: PASS under the supplied K theory.

All source needed for execution was copied to
`/tmp/audit-work/count-distinct-audit/reconstruction`. The fixed semantics came
from `/reference/reference-semantics`, not from a candidate cache. Before
building, the clean check confirmed that neither `runtime-kompiled` nor
`verification-kompiled` existed; see
`/audit-output/evidence/stage3-clean-check.log`.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0. The trusted translator regenerated `concrete_tests.mpy`
byte-identically, and `krun concrete_tests.regenerated.mpy --definition
runtime-kompiled` exited 0 with `.K`, `NoExc`, and exit code 0. Evidence:
`stage3-kompile-llvm.log`, `stage3-concrete-translation.log`, and
`stage3-krun-candidate-tests.log`.

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0; see `stage3-kompile-proof.log`. The exact unmodified candidate
specification then passed:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
#Top
EXIT_STATUS: 0
```

To require each claim to stand alone, I copied the two candidate claims
verbatim into reviewer modules `spec-load-only.k` and `spec-call-only.k`.
Each independent `kprove` invocation printed `#Top` and exited 0. Evidence:

- `/audit-output/evidence/stage3-kprove-all.log`
- `/audit-output/evidence/stage3-kprove-load.log`
- `/audit-output/evidence/stage3-kprove-call.log`
- `/audit-output/evidence/spec-load-only.k`
- `/audit-output/evidence/spec-call-only.k`

The LLVM compiler reported non-exhaustive-totality warnings for unrelated
fixed-semantics functions (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`). None is reachable from this program or appears in
its postcondition. The Haskell build reported only unused variables in
`strLt`. These limitations are recorded rather than converted into candidate
failures.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

The first claim has no `requires` clause. Its precondition is the exact initial
configuration: empty module scope at location 0 with the builtins scope as
parent, allocation counters `scopeLoc = 1` and `heapLoc = 0`, empty heap and
stack, `noRet`, `NoExc`, and exit code 0. It says that executing the exact
function-definition constructor terminates with an empty `<k>` cell and binds
`count_distinct_characters` at module scope to the expected one-argument
closure. All other cells remain as stated.

The second claim also has no `requires` clause. It quantifies over every finite
constructor value `CS:IntSeq`, starts in the same clean state, directly calls
the expected closure on `str(CS)`, and says the returned K value is exactly:

```text
isLen(dedupCodes(mapLower(CS)))
```

The final result is not free, existential, an implication, or a tautology. The
claim also fixes the final environment, scopes, allocation counters, heap,
stack, return state, exception state, and exit code.

### Mechanical source-to-proof identity

`/audit-output/evidence/extract_pinned_program.py` extracted:

1. the `FuncDef` term produced by `#loadCountDistinct`; and
2. the function reconstructed from the parameter list, body, and defining
   scope inside the closure actually invoked by `#callCountDistinct`.

The only normalization was the K list unit: rule bubbles spell an empty
expression list `.Exprs`, while external `.mpy` syntax uses an empty argument
position. Each extracted term and trusted-regenerated `solution.mpy` was parsed
with `kast` to KORE. All three KORE files were byte-identical, with SHA-256
`67d0aa94...0e15`. See
`stage4-pinning-extract-v2.log`, `stage4-pinning-kast-v2.log`, and the
preserved `pinned-*.mpy` terms.

Thus the helper executes the same function binding/body as the submitted
program. It does not merely share a textual function name. The call helper
skips the name lookup for the function itself, but the separate load claim
establishes that exact binding, and the call helper invokes the constructor-
identical closure. Inside the body, normal fixed semantics performs parameter
binding, name lookup, method binding, argument evaluation, builtin dispatch,
return, and frame restoration.

### Satisfying states and concrete substitutions

The exact initial cell state is realizable, and `CS = .IntSeq` is one concrete
satisfying input. Reviewer ground claims also instantiated:

- empty sequence, K result 0;
- code points for `Jerry`, K result 4;
- `[931, 963]` for `Σσ`, K result 2;
- `[304]` for `İ`, K result 1.

All four claims printed `#Top`; see `stage4-ground-kprove.log` and
`spec-ground.k`. The first two results equal both Python implementations.

The latter two expose the decisive adequacy failure:

| Input | Supplied-K claim | Trusted Python | Submitted Python |
|---|---:|---:|---:|
| `Σσ` (`[931,963]`) | 2 | 1 | 1 |
| `İ` (`[304]`) | 1 | 2 | 2 |

For `Σσ`, CPython lowercases both characters to U+03C3, merging two model
codes. For `İ`, CPython lowercases one character to `i` plus U+0307, expanding
one model code into two characters. The exact data are in
`stage4-adequacy-witness.log`.

The mismatch follows directly from fixed
`reference-semantics/semantics/methods.k`: `isUpperC` recognizes only 65–90,
`lowerC` adds 32 only there and otherwise returns its input, and `mapLower`
maps that function pointwise without expansion. Fixed
`reference-semantics/semantics/str.k` separately labels literal translation
“ASCII-only” and only advances while the next code is below 128. The symbolic
claim bypasses literal translation by accepting arbitrary `IntSeq`; it
therefore does not even formally restrict its precondition to ASCII. It simply
uses an ASCII lowercase function on non-ASCII code sequences.

This is not a claim that those fixed rules are inconsistent within the
supplied model. It is a witnessed failure of that model to denote real
`str.lower()` on the source-contract domain.

### Body sensitivity

I materially changed the closure body actually executed by the call claim from
`len(set(string.lower()))` to `len(string.lower())`, leaving the result
obligation unchanged. The mutated definition compiled successfully. Its proof
then exited 1 with `WarnStuckClaimState`, leaving the unmet equality between
plain length and deduplicated length. Evidence:
`verification-body-mutation.k`, `stage4-body-mutation-kompile.log`, and
`stage4-body-mutation-kprove.log`. This confirms that the successful claim
depends on the submitted body rather than only on an external source file or
wrapper name.

## 5. Rule-by-rule static soundness review

The complete lexical inventory is
`/audit-output/evidence/k-inventory-v2.json`. It covers all 25 K source files
used to assemble the concrete/proof definitions: the supplied
`semantics.k`, every supplied helper file, and candidate `verification.k`.
Every sentence includes its file/line identifier, full text, normalized hash,
kind, and parsed attributes.

Inventory totals:

- 697 rules;
- 228 syntax sentences;
- 145 function declarations and 107 `total` declarations;
- 22 opaque `no-evaluators` declarations;
- 45 priority rules;
- 3 macro-bearing syntax sentences;
- 5 contexts and 1 configuration;
- 0 simplification rules.

The per-sentence decision ledger
`/audit-output/evidence/k-classification-v2.json` assigns a decision to all
1,094 inventoried sentences. Counts are:

- 2 proof-local definitional wrapper rules and 5 proof-local structural
  sentences;
- 32 reached fixed rules sound for the modeled values;
- 6 reached fixed rules in the Unicode-lowercase mismatch chain;
- 3 fixed ASCII literal-boundary rules;
- 595 fixed rules not reachable from this target;
- 84 fixed unused total declarations;
- 43 fixed priority rules whose redex/guard does not apply on the target path;
- 22 fixed opaque symbols unreachable from the target;
- 24 concrete-only sentences not in the proof import closure;
- 278 remaining structural or unused declarations.

This classification does not silently pronounce the hundreds of unused
fixed-semantics rules equivalent to all of CPython. They are immutable supplied
semantics, not proof-local extensions, and no target conclusion depends on
them. No unsupported unsoundness allegation is made about an unused rule.

### Construct and execution map

Every constructor in `solution.mpy` is covered:

- `Module`, `FuncDef`, `Params`, `Return`, `Call`, `Name`, and `Attribute` are
  declared in `semantics/syntax.k`.
- `FuncDef` loading is handled by `functions.k:14`.
- Closure invocation/frame allocation is `call.k:69`; ordinary parameter
  binding is `functions.k:63-64`.
- Calls evaluate the callee and arguments through `call.k:20-21` and
  `core.k:189-191`; `appendVal` preserves left-to-right argument order.
- Names start lookup and resolve through the current/parent maps in
  `core.k:131-132,152`; `builtinsScope` fixes the `set` and `len` bindings.
- `Attribute` becomes the bound method in `call.k:16`; method dispatch is
  `call.k:24`.
- Lowercase dispatch and its equations are
  `methods.k:19,113,142-143,155-156`.
- `set(str)` is `builtins.k:41`, with structurally descending, disjoint
  membership/dedup/snoc equations in `set.k:12-27`.
- `len(setV(...))` is `builtins.k:21,25`, with structurally descending `isLen`
  equations in `core.k:228-229`.
- Builtin fallback dispatch is the applicable `call.k:31` owise rule.
- `Return` and `#pop` in `functions.k:78,85` preserve the result, discard the
  remainder of the function body as Python return requires, restore the caller
  continuation/environment, remove the call scope, and restore `scopeLoc`.

For the reached recursive functions, base/constructor coverage is exhaustive,
recursion descends on a proper sequence tail, and branch pairs use a predicate
and its negation. No reached total declaration has the non-exhaustive warnings
seen in unrelated modules. No reached priority rule preempts normal behavior:
the cell-binding priority rule is pruned because the target frame has no
`"$cells"` marker, and the ref-dereference priority rules cannot match the
string/set values on this path.

The two candidate-local rules introduce fresh wrapper syntax. They neither
replace an existing operational redex nor introduce opaque values:

- `#loadCountDistinct` expands to the exact function term.
- `#callCountDistinct(CS)` expands to ordinary fixed-semantics application of
  the exact closure on `str(CS)`.

They have no attributes, guards, priorities, functions, totality assertions,
or simplifications. Their accepted continuation context is safe: the first is
pure expansion, and the second delegates continuation preservation to the
ordinary closure-call/frame rules. Constructor identity and body sensitivity
provide the relevant connection evidence.

The 22 opaque symbols are `md5hexCodes`, 19 float-operation symbols, and
`sortVS`/`sortKeyVS`. None can influence this program's branch, result, state,
exception, or postcondition. Likewise, all 45 priority rules were inspected in
the inventory; none is a target operational bridge. The compiler's unrelated
non-exhaustive-totality warnings are a fixed-semantics evidence limitation, not
a demonstrated false target conclusion. Without such a witness I do not label
those declarations unsound.

The one demonstrated real-language discrepancy is the reached ASCII lowercase
chain. The required false-conclusion witnesses are the concrete `Σσ` and `İ`
rows above.

## 6. Fresh non-vacuity test

Status: PASS.

No candidate vacuity artifact was trusted. I created
`/audit-output/evidence/spec-vacuity.k`, changing the call claim's result to:

```text
isLen(dedupCodes(mapLower(CS))) +Int 1
```

This is demonstrably false at the satisfying input `CS = .IntSeq`: the real
result is 0, while the mutation requires 1.

First, `kprove ... --dry-run` successfully parsed the mutation and generated
the backend command, exiting 0; see `stage6-vacuity-dry-run.log`. The real
proof command then exited 1 with `WarnStuckClaimState`. Its residual explicitly
failed the equality between the cardinality and that cardinality plus one; it
was not a parser error, missing import, timeout, unreachable mutation, or
unrelated crash. See `stage6-vacuity-kprove.log`.

Together with the independent body mutation, this establishes both result
constraint and dependence on the actual body.

## 7. Proven versus assumed accounting

### What is machine-proved

Under K v7.1.293 and the exact supplied definition, from the stated clean
configuration:

1. loading the exact translated function installs the exact closure; and
2. for every constructor `CS:IntSeq`, execution of that exact closure on
   `str(CS)` reaches the exact integer
   `isLen(dedupCodes(mapLower(CS)))`, restoring every stated cell with no
   exception.

This is a universal, unbounded symbolic reachability result over finite
`IntSeq` terms. It is not a bounded unrolling or finite collection of examples.
It is partial correctness: the reachability proof does not separately assert a
termination theorem, although the reached straight-line execution and
structurally recursive functions terminate on finite constructor sequences.

### Trust ledger

- **K toolchain/backend and builtin theories.** Trusted: K parser,
  kompilers, Haskell prover, LLVM runtime, and the imported integer, Boolean,
  string-token, map, list, and K-equality theories. All formal claims depend on
  this normal low-level trust boundary.
- **Immutable supplied semantics.** Trusted as the operational theory for the
  machine proof. The target depends only on the 32 ordinary reached rules and
  six lowercase-model rules enumerated above. The hundreds of unrelated rules,
  opaque float/sort/hash symbols, and concrete-only rules do not affect the
  target result.
- **Proof-local wrappers.** Not assumptions or oracles. Their expansions are
  explicit, constructor-identical to the regenerated program, and
  body-sensitive.
- **`dedupCodes`/`isLen` meaning.** The K proof executes their complete
  equations. The ordinary mathematical bridge—insert a code only when absent,
  then take sequence length—does characterize the number of distinct modeled
  codes. It is not an unconstrained result-bearing abstraction.
- **`IntSeq` to Python `str` bridge.** Unproved and, over the full HumanEval
  domain, false. The model supplies only ASCII lowercase and cannot represent
  length-changing lowercase as a pointwise `Int -> Int` function. Every
  human-facing correctness conclusion depends on this bridge. This boundary is
  illegitimate for the unrestricted source contract.
- **Differential evidence.** The 4,624 Python cases support only that submitted
  Python and trusted canonical Python agree on those inputs. They neither prove
  universal equivalence nor repair the K-to-CPython bridge. The ground K/Python
  comparisons instead falsify that bridge on two valid inputs.
- **Exceptions and dynamic typing.** The theorem starts with a semantic string
  value and clean builtin bindings. That matches the intended typed HumanEval
  domain of ordinary `str` inputs; it does not cover hostile rebinding,
  subclasses with altered behavior, or non-string arguments. Those exclusions
  are not the verdict reason.

### Gate and verdict rationale

- Gate A, fixed-theory soundness/non-vacuity: PASS. The exact body executes,
  no result-bearing oracle or proof-local shortcut is present, both claims
  reconstruct to `#Top`, body mutation changes the obligation, and the false
  postcondition is rejected.
- Gate B, source-contract adequacy: FAIL. Valid unrestricted Python strings
  `Σσ` and `İ` produce theorem results different from both trusted and
  submitted Python.
- Gate C, auditability: PASS as an evidence/accounting gate. Commands, inputs,
  hashes, inventories, positive runs, and negative runs are preserved. This
  does not make the failed semantics bridge acceptable.

The formal proof is therefore meaningful but materially narrower than the
HumanEval source contract. Under the benchmark's decision boundary, that is a
candidate failure, not a non-fatal concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
