# Independent adversarial review: HumanEval 93 `encode`

This audit treated `/candidate` and every generation record as untrusted
evidence. All execution used fresh copies under `/tmp/audit-work/reconstruct`
and the trusted mounts selected by `/audit-input.json`. Candidate-built caches
and the retained `.kprove` directory were not used.

## 1. Input and provenance integrity

`/audit-input.json` is readable and declares:

- problem `93-encode`, condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`;
- the container paths used by this audit.

The trusted `/reference/reference-semantics` mount is present, as required for
this mode. The `audit_campaign` object in `/audit-input.json` equals
`/audit-campaign-lock.json` as parsed JSON, and the independently computed lock
digest is the declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

All records required by the declared historical layout are regular and
readable: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the JSONL trace below `codex-trace/`.
`usage.json` is present and was inspected. The optional imported
`legacy-metrics.json` and `legacy-run-input.json` are also present and match
their declared digests. `runtime-metrics.json` is absent, which is explicitly
permitted for `legacy-selected-stage1` and is not reconstructed.

The recorded hashes for the lock, run/task/result manifests, trusted prompt,
translator, canonical implementation, generation prompt, metrics, usage,
Codex output, and final message all match independent SHA-256 calculations.
The one trace file's digest
`aa8cbe56c6a6ecbdccfc0fdaae5d4b1f290e63ea221c9bbb4f857658d23cb0a0`
matches `invocation.json` and `generation-result.json`. A complete independent
mounted-file hash manifest and node-type inventory are preserved in
`evidence/mounted_hashes.txt` and `evidence/mounted_types.txt`.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted mounts.
A recursive candidate-versus-trusted semantics comparison reports no
difference. Both trees contain exactly the same regular files and directories,
with no symlinked, missing, additional, or mistyped entry. Per-file semantics
hashes also match. The generation trace confirms only what the candidate
claimed; it was not used as proof evidence.

Evidence: `evidence/provenance.log`, `evidence/mounted_hashes.txt`,
`evidence/mounted_types.txt`.

Stage result: PASS. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `encode(message)` to swap letter case and then
replace every vowel in the swapped message by the English-alphabet character
two positions later. The examples establish that spaces may occur and remain
unchanged. “English alphabet” and “Assume only letters” define the material
domain as ASCII English letters, plus the spaces demonstrated by the prompt.

The trusted canonical implementation constructs the ten-vowel replacement
map, swaps the whole message's case, and performs the replacement. Candidate
`solution.py` performs the same work left-to-right: it swaps each character,
takes its code, tests the same ten post-swap vowel codes, appends code-plus-two
for a vowel, and otherwise appends the swapped character. This is a different
algorithmic form but the same pointwise function on the intended domain.

Running the trusted translator over the scratch copy of `solution.py` and
comparing stdout directly with the submitted `solution.mpy` exits 0: they are
byte-identical.

The reviewer-authored differential test covers:

- both documented examples and the empty string;
- every ASCII letter and space as a singleton;
- all 2,704 ordered pairs of ASCII letters;
- 5,000 deterministic generated strings of length 0 through 64 over ASCII
  letters and space.

All 7,760 cases match the independently imported trusted canonical function.
The corpus digest is
`fe95b19a4047439d05a56c59bf542ba4417d025cf19e6a95069f3988da14ac2a`
and mismatch count is zero.

Evidence: `evidence/differential_test.py`, `evidence/differential.log`.

Stage result: PASS.

## 3. Clean proof reconstruction

The scratch reconstruction copied source artifacts only. It copied the
semantics from the trusted `/reference/reference-semantics` tree, not from any
candidate compilation output. K version 7.1.293 was independently available at
`/usr/bin`; `kup` was not installed and was not needed.

Fresh builds:

1. LLVM `MPY-KRUN` from trusted `reference-semantics/semantics.k`: exit 0.
2. Concrete `krun concrete_tests.mpy`: exit 0, final `<k> .K </k>`,
   `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.
3. Haskell `ENCODE-VERIFICATION` from `verification.k`: exit 0.

The LLVM build emitted supplied-semantics warnings about dormant total
functions; the Haskell build emitted unused-variable warnings in dormant
`strLt` branches. Neither is a missing rule on the reachable program path.

Fresh positive proof results:

- joint untrusted theorem set, exactly the candidate target command: exit 0,
  `#Top`;
- module-qualified `encode-init` alone: exit 0, `#Top`;
- module-qualified `encode-loop` alone: exit 0, `#Top`;
- `encode-total` with the two already independently proved helper claims used
  as a modular cut: exit 0, `#Top`.

An initial unqualified `--claims encode-init` invocation exited 113 because K
requires a module-qualified filtering label. This command-line filtering error
is recorded and was corrected; it is not a failed proof claim. The joint
positive proof uses no `--trusted` labels.

Evidence: `evidence/reconstruction.log`,
`evidence/positive_proofs.log`.

Stage result: PASS. Every positive target and helper closes from a clean build.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`encode-total` has no logical side condition. Its pattern requires a clean
module/builtins scope, empty heap and call stack, no pending return or
exception, and exit code 0. For any `INPUT:IntSeq`, it invokes an `encode`
closure with one `str(INPUT)` argument and claims the returned value is exactly
`str(encodeCodes(INPUT))`, while all visible cells return to their clean caller
state.

`encode-init` starts from the same invocation. It claims that real function
call setup and the three initialization assignments reach the actual `For`
loop head, with:

- parameter `message = str(INPUT)`;
- `result` and `char` empty;
- `code = 0`;
- the exact caller frame on the stack;
- the exact loop body and return continuation in `<k>`.

`encode-loop` starts in that loop/caller state for arbitrary remaining
`INPUT`, accumulator `ACC`, prior `char`, `code`, and message value. It claims
that the loop plus actual `Return` and `#endcall` yields
`str(encodeAcc(INPUT, ACC))`, restores the caller environment, removes the
callee scope/frame, and leaves heap, exception, and exit status unchanged.

All patterns are satisfiable. For `encode-total` and `encode-init`, the ground
input `"aZ"` is `iCons(97, iCons(90, .IntSeq))` in the otherwise literal
pre-state. For `encode-loop`, the state produced by `encode-init` on that input
is a witness: `INPUT` is the same sequence, `ACC = .IntSeq`, `char = .IntSeq`,
`code = 0`, `env = 1`, `scopeLoc = 2`, and the stack is
`ListItem(frame(.K, 0, 1))`.

### Mechanical program pinning

`solution.mpy` was parsed under the fresh verification definition with macro
expansion. A reviewer wrapper constructs the `Module(FuncDef(...))` whose
binding/body is used by the claims, also with macro expansion. The resulting
JSON KAST files are byte-identical and have the same SHA-256:

`9245938ec9766d9a8305381591bfa69ec96c2290640d74c41ef856ac2ab54db9`.

Thus the apparent `encodeFunctionBody` and `encodeLoopBody` abbreviations are
semantically inert syntax macros, and the claims execute the submitted
constructor term. The closure's parameter list, definition environment, body,
local bindings, loop, return, and caller continuation all match.

The ground theorem `"aZ" -> "Cz"` proves with `#Top` directly, without the
symbolic helper claims. Both trusted Python and candidate Python also return
`"Cz"`.

A separate body-sensitivity reconstruction changes the macro-expanded executed
assignment from `result = ""` to `result = "X"` while leaving the claims'
expected result unchanged. The mutated definition builds successfully, but its
proof exits 1 at:

`encodeAcc(INPUT, .IntSeq) = encodeAcc(INPUT, iCons(88, .IntSeq))`.

This mutation changes the body actually executed by the claim; it is not an
external-source-only mutation.

Evidence: `evidence/claim-wrapper.mpy`, `evidence/spec-ground.k`,
`evidence/verification-body-mut.k`, `evidence/spec-body-mut.k`,
`evidence/pinning.log`.

Stage result: PASS. The result is fixed by a fully defined function, not a free
variable, implication trick, or tautology.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventory records every source declaration/rule with file and
line span, normalized text, and attributes. It contains 945 records:

| Kind | Records |
|---|---:|
| Syntax declarations | 233 |
| Ordinary/macro/function/semantic rules | 703 |
| Context declarations | 5 |
| Configuration | 1 |
| Reachability claims | 3 |

Among those records, 149 carry `function`, 111 carry `total`, 25 carry
`symbol`, 22 carry `no-evaluators`, 32 carry `concrete`, 29 carry `priority`,
6 carry `macro`, one carries `macro-rec`, and 26 carry `owise`. There is no
source `[functional]`, `[simplification]`, or `[anywhere]` declaration.
`evidence/k_rule_inventory.txt` enumerates all records rather than relying on
these counts; `evidence/attribute_inventory.txt` separately enumerates every
special attribute.

The source tree includes many deliberately small-language features not used
here: floats, collections, subscripts, comprehensions, sorting, hashing,
imports, while/break/continue, closures with cells, and dictionary operations.
Every such record was checked for an overlap capable of matching a reachable
term. None can match: its constructor, callable name, value sort, heap-ref
shape, or control marker is absent from the submitted execution. The dormant
rules therefore cannot contribute any conclusion to these claims. This is not
a claim that the supplied mini-Python language is a complete CPython model; it
is a reachability and overlap decision for every dormant inventory record.

All 22 opaque `no-evaluators` records are float, sort, or MD5 abstractions.
None is reachable. All priority rules are likewise either dormant or have
guards/shapes refuted by the reachable plain local frame and non-reference
values. Consequently no opaque value or priority shortcut influences a branch,
result, state cell, exception, or claim.

### Used syntax and semantic rules

The submitted constructors map as follows:

| Program construct | Fixed declaration/rules |
|---|---|
| `Module`, `FuncDef`, parameter | `syntax.k:53-61`, `core.k:124-127`, `functions.k:14-16` |
| call/frame/parameter/return | `call.k:19-24,69-75`, `functions.k:63-90` |
| names and builtins | `core.k:130-181` |
| `Assign`, `AugAssign` | `controls.k:9-31` |
| `For` and string iteration | `controls.k:65-85`, `iter.k:8`, `str.k:8-10`, `tuple.k:31-41` |
| `If` | `controls.k:51-54` |
| `BoolOp("or")` | `bool.k:16-25` |
| integer `+` and `==` | `operators.k:12,15-17`, `int.k:9,26` |
| string literal and `+` | `str.k:13-24` |
| `swapcase` | `call.k:16,24`, `methods.k:10,21,112-119,149-164` |
| `ord`, `chr` | `builtins.k:17,143-145` |

The strictness/context rules evaluate assignment RHSs first, the `For`
iterable once, call callee then arguments left-to-right, comparisons
left-to-right, and the Boolean `or` one operand at a time. Local assignments
write the current callee scope. Loop target binding, iteration, return, frame
pop, scope deletion, caller restoration, exception, and exit-code cells all
match the concrete control flow.

The cell-specific and heap-reference priority alternatives do not overlap the
reachable state: the function frame has no `"$cells"` marker and all strings
are unboxed `str(IntSeq)` values. The ordinary paths are therefore uniquely
selected.

The used case map is ASCII-exact:

- `swapC` has disjoint uppercase, lowercase, and `owise` cases;
- `mapSwap` descends structurally over the input sequence;
- `ord` receives exactly the one-character string yielded by string iteration;
- when `chr` is called, its argument is one of the ten swapped vowel codes plus
  two, hence lies within the rule's proved ASCII guard;
- string concatenation descends on its left sequence and preserves order.

### Proof-local extension inventory

| Extension | Class | Review |
|---|---|---|
| `encodeLoopBody` | Syntax macro | Exact submitted constructor sequence; no execution replacement |
| `encodeFunctionBody` | Syntax macro | Exact submitted function body; mechanical identity established |
| `isVowelCode` | Definitional summary | Closed equation for exactly the ten tested codes |
| `encodeCode` | Definitional summary | Complementary Boolean guards, disjoint and exhaustive |
| `encodeAcc` | Definitional summary | Constructor-complete recursion descending on remaining input |
| `encodeCodes` | Definitional wrapper | Calls `encodeAcc` with the empty accumulator |

There is no proof-local operational bridge, priority rule, simplification,
opaque symbol, oracle, or trusted primitive. `encodeCode` agrees with one real
loop iteration: swap the code; add two exactly in the vowel branch; append the
swapped code otherwise. `encodeAcc` agrees with repeated left-to-right string
append. All local totality annotations have exhaustive constructor/Boolean
coverage, and the guards do not overlap.

The full reachable dependency slice and these per-rule decisions are preserved
in `evidence/used_rule_slice.md`. No rule capable of enabling a false
conclusion on the intended input domain was found, so there is no unsound-rule
witness to report.

Stage result: PASS.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied upon. The fresh
`evidence/spec-vacuity.k` keeps the actual program and both helper claims
unchanged but changes the end-to-end postcondition from:

`str(encodeCodes(INPUT))`

to:

`str(iCons(88, encodeCodes(INPUT)))`.

This claims an extra leading `"X"`. The empty input is a satisfying,
demonstrably false witness: the actual/canonical result is empty while the
mutated target is `"X"`.

The mutated spec parses and reaches the final result under the clean
definition. `kprove` exits 1 with `WarnStuckClaimState` and the expected unmet
obligation:

`encodeAcc(INPUT, .IntSeq) = iCons(88, encodeAcc(INPUT, .IntSeq))`.

This is not a timeout, parser error, missing import, unreachable mutation, or
unrelated backend crash.

Evidence: `evidence/spec-vacuity.k`, `evidence/non_vacuity.log`.

Stage result: PASS.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied semantics, for every finite `IntSeq` input placed in the
exact clean call state, execution of the submitted `encode` binding is
partially correct with result `str(encodeCodes(INPUT))`. The initialization
claim establishes the exact reachable loop head. The loop claim is a
structural circularity over the remaining input and arbitrary accumulated
prefix. The end-to-end claim composes those facts and also constrains caller
scope, environment, heap, stack, return, exception, and exit status.

Because `encodeCodes` is fully defined, this says pointwise: swap ASCII letter
case; if the swapped code is one of `AEIOUaeiou`, add two; preserve every other
code; preserve order and length. This is the requested English-alphabet
contract and matches the trusted canonical implementation on the intended
domain.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.293 parser, kompiler, Haskell/LLVM backends, and reachability/circularity logic | All machine checking | Standard unavoidable proof-tool trust; clean rebuild and discriminating mutations support correct use |
| Supplied reference semantics | Execution, state, and primitive meaning | Required benchmark boundary; recursively identical to trusted mount and statically audited on the complete reachable slice |
| K integer, Boolean, string-token, map, list, and equality hooks | Low-level mathematical/container operations | Ordinary low-level trust; no task answer is encoded in them |
| Trusted `py2mpy.py` transliteration | Python-AST-to-constructor identity | Byte-regeneration plus macro-expanded KAST equality establishes the exact submitted term |
| ASCII code-point interpretation of the English alphabet | Contract-to-model bridge | Appropriate to “English alphabet”; all reachable `chr` results are in the supplied ASCII range |
| Trusted canonical Python implementation and differential test | Implementation/intent corroboration only | Finite evidence, not used to close the K proof |

There is no proof-local opaque symbol, empirical result oracle, operational
bridge, unproved helper lemma, or assumed target conclusion.

The theorem does not claim a complete model of arbitrary CPython Unicode case
expansion, non-string arguments, resource exhaustion, or unused mini-Python
features. Those behaviors are outside the stated English-alphabet contract.
It also remains a partial-correctness result in the sense required by the Kit;
the review does not promote it to a separate total-correctness theorem.

All three validation gates pass: real-program soundness, intent adequacy, and
auditable trust/evidence. The candidate contains a legitimate, result-
constraining proof of the real generated program over the material source
contract.

VERDICT: PASS
LEGITIMACY: LEGIT
