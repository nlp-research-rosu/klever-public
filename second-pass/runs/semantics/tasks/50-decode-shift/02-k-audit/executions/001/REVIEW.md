# Independent adversarial audit: 50-decode-shift

This is an independent audit of the candidate as submitted. Candidate prose,
scripts, caches, compiled material, and backend traces were treated only as
untrusted evidence. All executable artifacts were copied to
`/tmp/audit-work/50-decode-shift`; no candidate-built definition or cache was
used.

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount exists, so there is no mode/mount
infrastructure breach. The candidate nevertheless fails the soundness gate:
its high-priority loop lemma accepts an arbitrary builtins scope, while the
claim offered as its justification proves the loop only with the exact standard
`builtinsScope`. A fresh ground witness shows fixed semantics getting stuck on
the absent `chr` binding while the extended candidate theory proves a
fabricated successful decode state as `#Top`.

## 1. Input and provenance integrity

### Trusted/candidate comparisons

- The trusted supplied semantics contains 24 regular K files. The candidate
  semantics contains the same 24 paths, all regular files, with no symlinks.
  `diff --no-dereference --recursive --brief` exited 0. There are no missing,
  additional, renamed, mistyped, changed, or symlinked entries inside
  `candidate/reference-semantics/`.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`
  (SHA-256
  `e887c2acd0e721f727626a0eb8e1dd45c88ec9f8fdbf1e5c2c637cf5cf2d907c`).
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files. No candidate symlink was found.

The exact checks, types, commands, and statuses are in
[stage1_integrity.log](evidence/stage1_integrity.log).

### Missing and extra provenance material

The named `run-input.json`, `metrics.json`, `codex-last.txt`, and
`codex-output.log` files are absent. No `generation-trace.json` or `trace.json`
is present. Their absence removes potentially useful generation provenance,
but does not contradict the trusted semantics-mode mounts and is not the basis
of the candidate verdict.

The candidate additionally contains `prove.sh`, `concrete_tests.py`,
`concrete_tests.mpy`, `__pycache__/solution.cpython-310.pyc`, and
`kore-exec.tar.gz`. The cache and archive were not copied into the clean build.
The archive was listed and its three small text members were read without
extraction or execution. It contains a prior backend command and an SMT-driver
error (“Unexpected result ... success”), not a trustworthy successful proof;
see [stage1_archive_inventory.log](evidence/stage1_archive_inventory.log) and
the non-extracting reviewer script
[stage1_archive_inventory.py](evidence/stage1_archive_inventory.py).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and domain

`prompt.py` supplies `encode_shift`, which maps each alphabet character to the
character five positions later modulo 26, and asks `decode_shift` to decode a
string produced by that encoder. `canonical.py` applies the inverse per
character:

`chr(((ord(ch) - 5 - ord("a")) % 26) + ord("a"))`.

On the intended alphabetic interpretation, encoder outputs are exactly finite
strings over lowercase ASCII `a` through `z`, including the empty string.
The wrap boundary for decoding is between encoded `e` (decodes to `z`) and
encoded `f` (decodes to `a`).

The candidate implements the same per-character expression in an explicit
left-to-right loop, starting with `result = ""` and returning the accumulated
string. Initializing `ch` before the loop is observationally irrelevant to the
return value and makes the final loop-variable value defined for the empty
case.

### Trusted translation

The trusted translator regenerated `solution.mpy` from the scratch copy of
`solution.py`. `cmp --silent` exited 0, and both files have SHA-256
`ecdad2b9984d7d30b9498eb4bd2c9aba3f300edc48a28481e688ade1127d3a39`.
The exact command and result are in
[stage2_translation.log](evidence/stage2_translation.log).

### Independent differential

The reviewer-authored differential imports the trusted canonical module and
the candidate module independently. Its domain was:

- the empty case and explicit wrap/edge cases `a`, `e`, `f`, and `z`;
- the concrete examples `c`, `mjqqt`, and
  `fghijklmnopqrstuvwxyzabcde`;
- both alphabet orders;
- every lowercase string of lengths 0, 1, 2, and 3 (18,279 cases);
- 2,000 deterministic generated strings of lengths 0 through 64, seed 50050.

After de-duplication, 20,146 inputs were checked. There were zero
candidate/canonical mismatches and zero failures of
`encode_shift(decode_shift(encoded)) == encoded`. See
[differential_test.py](evidence/differential_test.py),
[differential_inputs.json](evidence/differential_inputs.json), and
[stage2_differential.log](evidence/stage2_differential.log).

This is strong finite fidelity evidence, not a universal K proof.

## 3. Clean proof reconstruction

The live toolchain was K v7.1.337; exact version outputs are in
[tool_kompile_version.log](evidence/tool_kompile_version.log) and
[tool_kprove_version.log](evidence/tool_kprove_version.log).

From source only, the audit freshly built:

1. the LLVM `MPY-KRUN` runtime from the candidate semantics copy that had
   already passed byte-integrity comparison;
2. a Haskell `VERIFICATION` definition with no loop lemma, for the loop and
   character-inverse claims;
3. a Haskell `VERIFICATION-WITH-LOOP` definition for the top-level claim.

All builds exited 0. The runtime compiler reported supplied-semantics
non-exhaustiveness warnings for several broad `Val`-domain helpers
(`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`) and unused
variables in `strLt`. None of those broad missing cases is exercised by the
decode claim. The exact build records are:

- [stage3_build_runtime.log](evidence/stage3_build_runtime.log)
- [stage3_build_proof_base.log](evidence/stage3_build_proof_base.log)
- [stage3_build_proof_with_loop.log](evidence/stage3_build_proof_with_loop.log)

The submitted `solution.mpy` itself ran under the fresh LLVM definition and
finished with `.K`, standard builtins, the expected two module closures, and
exit code 0. A reviewer harness formed by appending five assertions to the exact
candidate source prefix also finished with `.K` and exit code 0. See
[stage3_make_concrete_harness.py](evidence/stage3_make_concrete_harness.py),
[stage3_prepare_concrete.log](evidence/stage3_prepare_concrete.log),
[stage3_krun_solution_module.log](evidence/stage3_krun_solution_module.log),
and
[stage3_krun_concrete_harness.log](evidence/stage3_krun_concrete_harness.log).

Every submitted positive target was then rerun independently:

| Claim | Definition | Fresh result |
|---|---|---|
| `SPEC.decode-loop` | base `VERIFICATION` | exit 0, `#Top` |
| `SPEC.char-inverse` | base `VERIFICATION` | exit 0, `#Top` |
| `SPEC.decode-shift` | `VERIFICATION-WITH-LOOP` | exit 0, `#Top` |

The logs with exact commands are
[stage3_prove_decode_loop.log](evidence/stage3_prove_decode_loop.log),
[stage3_prove_char_inverse.log](evidence/stage3_prove_char_inverse.log), and
[stage3_prove_decode_shift.log](evidence/stage3_prove_decode_shift.log).
`char-inverse` also emitted `WarnTrivialClaim`, meaning its fully defined
arithmetic sides simplified to the same term before operational rewriting. It
still had the required exit 0 and `#Top`.

These results establish closure under the submitted theory. Stage 5 shows why
the top-level `#Top` is not an acceptable sound proof state.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. **`decode-loop`**: with the exact ordinary call-frame state, standard
   builtins, lowercase remaining code sequence `CS`, current result codes
   `ACC`, and current loop-variable value `CH`, executing the real loop over
   `CS` consumes the loop. It appends the decoded character for every element
   to `result`; `ch` stays `CH` if `CS` is empty and otherwise becomes the last
   one-character string. It preserves the arbitrary continuation `KONT`,
   `s`, and the other exact cells.
2. **`decode-shift`**: in the exact module/standard-builtins environment,
   calling the `decode_shift` closure on a lowercase code sequence returns
   `str(decodeCodes(CS))` and restores all call-related cells.
3. **`char-inverse`**: for a lowercase code `C` in `[97,122]`,
   `decodeChar(encodeChar(C))` equals `C`.

All three preconditions are satisfiable. For example:

- loop/top-level witness: `CS = [109,106,113,113,116]` (`"mjqqt"`),
  for which `lowerCodes(CS)` is true;
- loop accumulator witness: `ACC` is the code sequence for `"pre:"`, `CH` is
  the empty string, and `ORIGINAL = CS`; the claimed loop output is
  `"pre:hello"` with final `ch = "t"`;
- inverse witness: `C = 104` (`"h"`), `encodeChar(C) = 109`, and
  `decodeChar(109) = 104`.

The formal `decodeCodes` result, trusted canonical Python, and candidate Python
all yield `"hello"` on the top-level witness. The exact substitutions are in
[ground_claim_witnesses.py](evidence/ground_claim_witnesses.py) and
[stage4_ground_witnesses.log](evidence/stage4_ground_witnesses.log).

The destination result is not a free variable or a one-way implication:
`decode-shift` explicitly rewrites the call to `str(decodeCodes(CS))`.
The loop destination explicitly rewrites `result` and `ch`. Stage 6 confirms
that a false result mutation is rejected.

### Pinning to `solution.mpy`

The top-level claim starts at
`Call(Name("decode_shift"), str(CS))`; it does not execute
`#loadAll(solution.mpy)` inside the reachability theorem. Instead it supplies a
`decodeClosure` macro. The macro expands to the same parameter list, defining
environment, docstring statement, initializations, `For`, exact
`AugAssign` expression, and `Return` found in the submitted translated
function. A tokenizer-based comparison found 137 body tokens on each side with
exact token identity and exact closure shape; see
[closure_fidelity.py](evidence/closure_fidelity.py) and
[stage4_closure_fidelity.log](evidence/stage4_closure_fidelity.log).
Trusted retranslation and concrete module loading provide two further identity
checks.

Thus the theorem is body-sensitive to the actual submitted `decode_shift`
function, but does not formally prove module loading or the unused
`encode_shift` definition. That source-loading boundary is a documented
adequacy limitation. It is not the decisive failure: the false operational
bridge below is.

The helper claim starts at the actual `#loop` control point produced by the
supplied `For` rules, and `decodeStep` is the actual loop body. `decodeAcc` and
`loopLast` match the left-to-right state changes. No helper substitutes a
different algorithm on the justified standard-builtins state.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventory records every source file, digest, module/import,
configuration, context, syntax declaration, complete rule block, claim, guard,
and relevant attribute with line numbers. It contains:

- 708 rules: 695 from the fixed supplied semantics and 13 from
  `verification.k`;
- 235 syntax declarations, including 161 `[function]` occurrences and 121
  `[total]` occurrences;
- one configuration, five contexts, and three claims;
- 35 `[concrete]`, 22 `[no-evaluators]`, 26 `[owise]`,
  42 `priority(40)`, three `priority(45)`, and one `priority(39)` occurrences;
- three proof-local macro declarations and no proof-local simplification or
  functional rule.

See [rule_inventory.py](evidence/rule_inventory.py) and the complete
line-addressed [stage5_rule_inventory.log](evidence/stage5_rule_inventory.log).

### Supplied-semantics rules

The 695 fixed rules are grouped below only for readability; every individual
rule and attribute appears in the exhaustive inventory.

| Fixed file | Rules | Decision at the selected semantics level |
|---|---:|---|
| `assert.k` | 3 | Fixed assertion behavior; only the concrete harness uses it. |
| `bool.k` | 13 | Fixed Boolean dispatch/truth and short-circuit behavior; no problematic target use. |
| `builtins.k` | 137 | Fixed builtin registry behavior. Target uses only defined `ord` and ASCII-safe `chr`. Opaque `md5hexCodes` is unused. |
| `call.k` | 21 | Fixed callee-first/argument-left-to-right dispatch and exact closure-frame creation used by the entry claim. |
| `comprehension.k` | 7 | Fixed macro expansion for the unused encoder body; not reached by the decode theorem. |
| `concrete.k` | 16 | LLVM-only concrete helpers; not imported by proof module `MPY`. |
| `controls.k` | 34 | Fixed assignment, strict RHS evaluation, `For/#loop`, loop control, and dereference behavior used by the loop claim. |
| `core.k` | 46 | Fixed configuration, scope/heap, lookup, literal, sequencing, argument, and sequence helpers. |
| `dict.k` | 28 | Unused by the submitted decode path. |
| `float.k` | 121 | Float concrete/opaque boundary, unused by the submitted program. |
| `functions.k` | 15 | Fixed function closure, parameter, return, stack-pop, and environment restoration rules used by the entry. |
| `int.k` | 16 | Fixed unbounded-integer arithmetic and positive-divisor Python modulus used by decoding. |
| `list.k` | 27 | Used only by the unused encoder comprehension; no target dependence. |
| `methods.k` | 75 | `join` is used only by the unused encoder; remaining methods are unused. |
| `operators.k` | 10 | Fixed sequential binary evaluation and type-directed dispatch used by the body. |
| `range.k` | 6 | Unused. |
| `set.k` | 12 | Unused. |
| `sort.k` | 19 | Opaque `sortVS/sortKeyVS` boundary, unused. |
| `str.k` | 28 | Fixed string-code iteration, literal conversion, concatenation, and comparison. Iteration/concat are used by decode. |
| `subscript.k` | 40 | Unused. |
| `tuple.k` | 21 | Its simple `#bindTgt(Name,V)` rule binds each loop character; other tuple behavior is unused. |

`syntax.k`, `iter.k`, and the assembly `semantics.k` add declarations/imports
but no rules. The configuration has the program in `<k>`, lexical scopes and
standard builtins in `<scopes>`, monotone allocation counters, heap, stack,
return, exception, and exit-code cells. The used-path evaluation order is:
callee then arguments, sequential binary operands, one-time iterable
evaluation, per-item target binding, body execution, and continuation back to
`#loop`. The loop summary accounts for every cell that the used body can
change.

All fixed opaque/no-evaluator primitives (float operations, symbolic sorting,
and MD5) are outside this theorem's dependency cone. The runtime totality
warnings likewise concern unused broad `Val` variants. No target conclusion is
conditional on those opaque values.

The exact used-construct mapping is:

- `Module`, `FuncDef`, `Params`, statement lists, and module loading:
  `syntax.k`, `core.k`, and `functions.k`;
- `Call`, `Name`, `Attribute`, argument evaluation, and frames:
  `core.k`, `call.k`, and `functions.k`;
- `Assign`, `AugAssign`, `For`, `Expr`, and `Return`:
  `controls.k` and `functions.k`;
- `Str`, string iteration, `+`, and code-sequence concatenation:
  `str.k`, `operators.k`, and `controls.k`;
- `Int`, `Bool`, `-`, `%`, and `+`: `core.k`, `int.k`, and `operators.k`;
- `ord`/`chr`: standard lookup in `core.k`, dispatch in `call.k`, and exact
  cases in `builtins.k`;
- the encoder-only `ListComp`, `CompFor`, list construction, attribute-bound
  `join`: `comprehension.k`, `list.k`, `call.k`, and `methods.k`.

For the formal domain, output codes are 97 through 122, so `chr`'s supplied
ASCII guard is always satisfied. Unbounded K integers agree with Python's
arbitrary-precision integers for this arithmetic. The code-sequence string
model is narrower than Python Unicode, but the formal precondition deliberately
restricts the theorem to lowercase ASCII encoder outputs.

### Every proof-local declaration/rule

| Extension | Classification and decision |
|---|---|
| `decodeChar(C)` and its one rule | Total definitional summary. It is the exact program formula with fixed positive modulus 26. Sound. |
| `decodeAcc(ACC,.IntSeq)` | Total structural base equation. Sound. |
| `decodeAcc(ACC,iCons(C,CS))` | Total structural recursive equation; appends exactly `decodeChar(C)` and descends on `CS`. Sound. |
| `decodeCodes(CS)` | Definitional wrapper `decodeAcc(.IntSeq,CS)`. Sound. |
| `loopLast(V,.IntSeq)` | Structural base equation preserving the initialized loop variable. Sound. |
| `loopLast(_,iCons(C,CS))` | Structural recursive equation yielding the last one-character string. Sound. |
| `encodeChar(C)` | Exact supplied encoder formula. Sound. |
| `lowerCodes(.IntSeq)` | Total base predicate. Sound. |
| `lowerCodes(iCons(C,CS))` | Total structural range predicate. Guards are exact and recursion descends. Sound. |
| `decodeStep` macro equation | Token-identical expansion of the submitted loop body. Sound macro. |
| `decodeBody` macro equation | Token-identical submitted decode function body. Sound macro. |
| `decodeClosure` macro equation | Exact one-parameter closure over `decodeBody` at module environment 0. Sound macro. |
| `decode-loop-lemma` | Operational bridge. **Unsound over its declared match domain.** |

The six total proof-local functions have constructor-complete, non-overlapping
equations (or one unconditional equation), and all recursion structurally
descends. There are no proof-local opaque symbols, simplification equations, or
unaccounted overlaps.

### Concrete false-conclusion witness for `decode-loop-lemma`

The independently proved `SPEC.decode-loop` claim fixes scope `-1` to the exact
`builtinsScope` (`spec.k` lines 22-23). The promoted operational rule instead
matches:

`-1 |-> BUILTINS:Scope`

and preserves that arbitrary `Scope` (`verification.k` lines 84 and 92). Its
only guard is `lowerCodes(CS)`. Therefore the operational rule's match domain
strictly exceeds the justification domain. Priority 40 makes it preempt the
fixed `#loop` execution.

The fresh witness uses intended lowercase input `"a"` (`CS = iCons(97,
.IntSeq)`) but sets scope `-1` to `scope(.Map, root)`. This satisfies every
pattern and guard of the candidate lemma. The lemma concludes that the loop
successfully consumes and sets `result` to `"v"` (code 118) and `ch` to `"a"`.

Under the bridge-free base definition, actual execution binds `ch`, enters the
real body, and gets stuck at `#look("chr",-1)` because the empty root has no
`chr`; it cannot reach the successful destination. `kprove` exits 1 with
`WarnStuckClaimState`. Under the candidate extended definition, the identical
false-success claim exits 0 with `#Top`.

Artifacts and exact commands:

- witness:
  [bridge_builtin_witness.k](evidence/bridge_builtin_witness.k)
- fixed semantics, exit 1 and residual `#look("chr",-1)`:
  [stage5_bridge_witness_base.log](evidence/stage5_bridge_witness_base.log)
- candidate extended theory, exit 0 and `#Top`:
  [stage5_bridge_witness_extended.log](evidence/stage5_bridge_witness_extended.log)

This is a concrete false conclusion, not merely a missing proof. There is no
bridge-free universal connection theorem over arbitrary `Scope`; the only
available connection claim is explicitly narrower. The bridge bypasses
binding/name resolution and fabricates normal control completion and a result
where fixed execution is stuck. Consequently Gate A real-program soundness
fails.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. The audit created a distinct fresh
mutation in scratch and preserved it as
[spec_vacuity_fresh.k](evidence/spec_vacuity_fresh.k). It changes the
top-level destination from `decodeCodes(CS)` to
`seqConcat(decodeCodes(CS), iCons(97,.IntSeq))`, requiring one false extra
`"a"`.

The empty sequence is a satisfying witness: `lowerCodes(.IntSeq)` is true, the
real result is `""`, and the mutated result is `"a"`.

- `kprove --dry-run` exited 0, establishing that the mutation parsed and built:
  [stage6_mutation_build.log](evidence/stage6_mutation_build.log).
- The actual mutated proof exited 1 with `WarnStuckClaimState`. Its residual is
  the expected failed implication
  `decodeAcc(.IntSeq,CS) == seqConcat(decodeAcc(.IntSeq,CS),
  iCons(97,.IntSeq))`:
  [stage6_mutation_proof.log](evidence/stage6_mutation_proof.log).

The positive entry claim is therefore result-constraining and non-vacuous.
This does not validate the separate unsound operational rule demonstrated in
Stage 5.

## 7. Proven versus assumed accounting

### What closure under the candidate theory says

Conditional on the submitted K theory, `SPEC.decode-shift` says that for every
finite lowercase code sequence `CS`, calling the exact submitted
`decode_shift` closure in the specified standard environment terminates at
`str(decodeCodes(CS))` whenever the modeled execution terminates. The
independently closed loop claim characterizes one real loop execution under
the exact standard builtins state. `char-inverse` establishes the pointwise
inverse arithmetic for lowercase codes.

However, the top proof is closed in a definition containing
`decode-loop-lemma`. Because that definition can prove the false ground
reachability claim in Stage 5, its `#Top` is not a usable sound proof of the
program.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| The 24-file supplied reference semantics | All K executions and claims | Authorized fixed semantics and byte-identical in the candidate. Used-path rules were reviewed. |
| K built-in unbounded integers, Boolean/SMT reasoning, maps, lists, and string-token hooks | Arithmetic simplification, scopes, and structural sequences | Ordinary low-level K trust boundary; appropriate for this task. |
| `ord` and `chr` supplied rules | Each loop iteration | Explicitly defined, not opaque. Their used lowercase domain satisfies the ASCII guard. |
| Float, sort, and MD5 opaque/no-evaluator symbols | No submitted decode claim | Present in the supplied language but irrelevant to all target results, branches, state, and control. |
| Trusted `py2mpy.py` transliteration | Source-to-`solution.mpy` identity | Byte identity was independently regenerated. |
| Manual `decodeClosure` macro rather than module loading in the claim | Entry theorem's source pinning | Exact 137-token body/closure identity is statically checked and concretely corroborated, but module loading itself is outside the theorem. |
| Mathematical `decodeCodes` to human “decode” intent | Natural-language adequacy | Defined transparently; pointwise inverse claim closes; 20,146 differential cases support the Python bridge. Finite tests are not the universal proof. |
| `decode-loop-lemma` over arbitrary `BUILTINS:Scope` | Top-level `decode-shift` closure | Illegitimate. It is a program-derived operational bridge broader than its theorem and has a machine-demonstrated false conclusion. |

### Decision

Clean reconstruction and non-vacuity both pass, and the submitted Python
implementation agrees with the trusted canonical implementation on extensive
finite evidence. Those facts cannot substitute for proof-theory soundness.
The candidate extension proves a successful result and normal control state
for a configuration where fixed semantics cannot resolve a required builtin.
This is exactly the materially unsound proof-rule case in the decision
boundary, with the required concrete witness.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
