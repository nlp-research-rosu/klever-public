# Independent adversarial audit: 61-correct-bracketing

The candidate contains a legitimate partial-correctness proof of the submitted
program over the full source-contract input domain. I did not rely on the
candidate's `#Top`, compiled definitions, traces, `PROOF.md`, or final report.
Both target claims were rebuilt from source and rerun, and their proof-local
theory passed the extension-soundness, adequacy, real-program-pinning, and
non-vacuity checks below.

The exact reviewer commands, statuses, and transcript locations are indexed in
[evidence/COMMANDS.md](evidence/COMMANDS.md).

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem
`61-correct-bracketing`, and condition `kit-semantics`. The trusted
`/reference/reference-semantics` tree is present, so the mount is consistent
with the rendered semantics mode. `writing-semantics` is therefore inapplicable.

I read and checked all required records:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the sole structured trace JSONL file below
  `/generation-evidence/codex-trace/`.

The independent checker in
[evidence/provenance_check.py](evidence/provenance_check.py) produced
[evidence/provenance.log](evidence/provenance.log), exit 0. It established:

- the campaign block is structurally identical to the lock document, whose
  independently computed SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- all 12 required launcher/generation records are regular files, not symlinks,
  and every recorded per-file hash matches;
- the candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`;
- the candidate and trusted supplied-semantics trees have identical relative
  paths, entry types, and bytes, with no linked or unsupported entry; both
  recompute to the pipeline tree hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- the whole candidate tree recomputes to the stage-1 workspace hash
  `77ebf25ce12e3329eaf00f9044c284e408523b355b402813bed563d2fe2a637f`;
  and
- all 511 trace lines parse as JSON. The raw trace file and trace-tree hashes
  match the generation result and usage record respectively.

The complete generation log (49,605 lines), prompt, final message, and
structured trace were read as untrusted history. They claim a successful proof,
but no conclusion below depends on that claim. The candidate contains the
required proof source artifacts as regular files. Its supplied-semantics tree
has no missing, additional, changed, mistyped, or symlinked entry. There is no
audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` specifies a finite string containing only `(` and `)`.
The function returns true exactly when every opening bracket has its matching
closing bracket in proper prefix/nesting order. In particular, the documented
`")(()"` example is false, so equal total counts alone are insufficient.

The trusted `/reference/canonical.py` keeps an integer depth, increments it for
`(`, decrements it for `)`, immediately returns false if a prefix depth is
negative, and otherwise returns whether final depth is zero.

The submitted `/candidate/solution.py` performs the same scan but, instead of
returning immediately on a negative prefix, permanently sets `valid = False`
and finishes the loop. It returns `valid and balance == 0`. Because `valid`
never becomes true again, this is extensionally equivalent on the entire
contract domain (and in fact under both implementations' common non-`(`
fallback behavior).

### Translation identity

From the scratch copy I ran:

```text
python3 py2mpy.py solution.py | cmp solution.mpy -
```

It exited 0; see
[evidence/translator-identity-valid.log](evidence/translator-identity-valid.log).
Thus the submitted `solution.mpy` is byte-identical to fresh output from the
trusted translator. Its SHA-256 is
`cdf235447b5d2f7d9d5f1ca5bf1875a323879fe129dbdc4cc0e0473a9ae86b87`.

### Independent differential evidence

[evidence/differential.py](evidence/differential.py) independently imports the
trusted canonical entry point and the scratch-copy submitted entry point. It
also uses a separately written stack/depth oracle. It covers:

- all prompt examples and explicit empty, single-character, negative-prefix,
  balanced, unbalanced, nested, and concatenated branch boundaries;
- every `(` / `)` string through length 14 (32,767 inputs);
- 70 long structured inputs at lengths through 1,000; and
- 3,000 deterministic random inputs of lengths 0 through 1,000.

The run checked 35,851 cases with zero mismatches and exited 0:
[evidence/differential.log](evidence/differential.log). This is finite
fidelity evidence, not a substitute for the universal K proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/fresh`. None of
`/candidate/runtime-kompiled`, `/candidate/verification-kompiled`,
`/candidate/verification-with-loop-kompiled`, `__pycache__`, or any
candidate cache was copied or referenced. The live tools all report K
v7.1.293: [evidence/tool-versions.log](evidence/tool-versions.log).

### Concrete definition

This fresh LLVM build exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

See [evidence/build-runtime.log](evidence/build-runtime.log). The compiler
reported non-exhaustive-match warnings in unrelated supplied helpers; none of
those helpers occurs in the submitted program, its claims, or its summary.

The reviewer-owned
[evidence/concrete_harness.py](evidence/concrete_harness.py) embeds the exact
function AST, as mechanically checked in
[evidence/concrete-harness-body.log](evidence/concrete-harness-body.log), and
was freshly translated and run under that LLVM definition. The complete final
configuration had empty `<k>`, empty heap and stack, `noRet`, `NoExc`, exit code
0, and:

```text
case_empty      = true
case_open       = false
case_close      = false
case_pair       = true
case_nested     = true
case_bad_prefix = false
case_concat     = true
```

The command exited 0; the configuration is preserved in
[evidence/concrete-execution.log](evidence/concrete-execution.log).

### Positive target claims

There are exactly two positive claims in `spec.k`. I rebuilt and ran each in
the definition appropriate to its proof role:

1. Bridge-free universal loop theorem:

   ```text
   kompile verification.k --backend haskell \
     --main-module VERIFICATION --syntax-module MPY-SYNTAX \
     --output-definition verification-kompiled

   kprove spec.k --definition verification-kompiled \
     --spec-module SPEC --claims SPEC.loop
   ```

   Both commands exited 0 and the proof printed `#Top`; see
   [evidence/build-verification.log](evidence/build-verification.log) and
   [evidence/prove-loop.log](evidence/prove-loop.log).

2. Exact whole-program theorem, after separately validating the loop theorem:

   ```text
   kompile verification-with-loop.k --backend haskell \
     --main-module VERIFICATION-WITH-LOOP --syntax-module MPY-SYNTAX \
     --output-definition verification-with-loop-kompiled

   kprove spec.k --definition verification-with-loop-kompiled \
     --spec-module SPEC --claims SPEC.correct-bracketing
   ```

   Both commands exited 0 and the proof printed `#Top`; see
   [evidence/build-verification-with-loop.log](evidence/build-verification-with-loop.log)
   and [evidence/prove-entry.log](evidence/prove-entry.log).

These are fresh verification results only; Sections 4–7 establish why the
theory under which they close is adequate and sound.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop` assumes:

- `CS` is a finite code sequence containing only 40 (`(`) or 41 (`)`);
- the current callee scope contains exactly `bracket`, the original
  `brackets`, integer `balance = B`, and Boolean `valid = V`;
- execution is at the submitted loop over remaining `str(CS)`;
- its exact suffix is the submitted return followed by `#endcall`;
- the heap is empty, the stack has exactly the `.K` caller frame, and the
  environment, allocators, return state, exception state, and exit code are the
  displayed values.

It proves that fixed semantics executes that loop, return, and frame pop to
the Boolean `scanBrackets(CS, B, V)`, restores environment 0, removes the
callee scope and frame, and preserves the displayed module/builtin scopes and
other state.

`SPEC.correct-bracketing` assumes a finite `CS` over codes 40/41 and the normal
initial MPY configuration: environment 0, fixed builtins, empty module map,
heap, and stack, and no return or exception. It loads the displayed function,
performs ordinary lookup/call/binding/body/return execution, and proves the
returned value is exactly `scanBrackets(CS, 0, true)`. The postcondition also
pins the exact loaded closure and the restored final state. It is an equality-
constraining reachability target, not a free result variable, implication-only
condition, or tautology.

### Mechanical program identity

The reviewer script
[evidence/extract_claim_program.py](evidence/extract_claim_program.py)
extracts the complete `Module(...)` argument actually executed by the entry
claim. After removing only proof-syntax spellings of explicit empty `.Stmts`
lists, both it and fresh `solution.mpy` parse to byte-identical KORE:

```text
85d29784c4528e2b080091cc7eaf375f1ce86063d4c9de68577ad73bf3d4ade7
```

See
[evidence/program-term-pinning-valid.log](evidence/program-term-pinning-valid.log).
This comparison covers the function name, parameter, and complete constructor
body. The only normalization is the empty-list surface spelling; the parsed
constructor terms are identical. Typing annotations omitted by the trusted
translator are semantically inert.

The independently proved loop claim and the installed operational bridge are
also mechanically identical in their LHS, RHS, guards, cells, and
continuations, excluding only label, whitespace, and the bridge's priority:
both normalize to SHA-256
`6502f36fdbd4e1d1346c8d381b3e4f98f3eb3993fed2054c8d0a1fdbcfebcc3f`.
See [evidence/loop-bridge-identity.log](evidence/loop-bridge-identity.log).

### Satisfiable preconditions and ground substitutions

An entry witness is `CS = .IntSeq` in the displayed initial configuration;
`bracketInput(.IntSeq)` reduces to true and all cells are realizable. A loop
witness is `CS = .IntSeq`, `B = 0`, `V = true`,
`_OLD = str(.IntSeq)`, `_INPUT = .IntSeq`,
`MODULE = .Map`, and `BUILTINS = builtinsScope` in the displayed callee
configuration; its precondition also reduces to true.

Ground substitution agrees across the formal summary, the LLVM execution, the
submitted Python, and the trusted canonical:

| Input | `scanBrackets(CS,0,true)` | Both Python implementations |
|---|---:|---:|
| `""` | true | true |
| `"("` | false | false |
| `")"` | false | false |
| `"()"` | true | true |
| `"(()())"` | true | true |
| `")(()"` | false | false |

There is no fixed-size or balance bound. The theorem quantifies over arbitrary
finite `IntSeq` and restricts only its alphabet, exactly as the prompt does.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[evidence/inventory_k.py](evidence/inventory_k.py) inventories every syntax
declaration, rule, claim, configuration, context, and relevant attribute in
the complete supplied tree and proof-local files. The full line-addressable
output is [evidence/k-rule-inventory.log](evidence/k-rule-inventory.log):

| Source class | Inventory |
|---|---|
| Supplied fixed baseline | 227 syntax declarations, 695 rules, 5 contexts, 1 configuration |
| `verification.k` | 3 `[function,total]` declarations and 7 rules, including 1 simplification |
| `verification-with-loop.k` | 1 priority operational rule |
| `spec.k` | 2 reachability claims |

There is no proof-local `functional`, opaque, or `no-evaluators` declaration.
The supplied baseline contains opaque/concrete primitives for floats, sorting,
and MD5, but no such symbol is reachable from this program or appears in a
claim or postcondition. Because this is `SUPPLIED_SEMANTICS`, the unchanged
695-rule tree is the selected fixed execution model rather than a candidate
proof extension. Its complete inventory is retained for auditability; the
used execution slice is traced below.

### Used source constructors and fixed rules

Every constructor in `solution.mpy` has a declaration and operational path:

| Construct | Declaration and material rules |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14-16` |
| `Call`, `Name` | `syntax.k:12,28`; `core.k:130-154`; `call.k:18-21,69-74` |
| Parameter binding, return/pop | `functions.k:62-90` |
| `Assign` | strict RHS at `syntax.k:41`; update at `controls.k:9-18` |
| `For` and string iteration | strict iterable at `syntax.k:45`; `controls.k:62-74`; `str.k:7-10` |
| Loop target binding | `tuple.k:30-41` |
| `If` | strict condition at `syntax.k:49`; `controls.k:50-54` |
| `AugAssign` | strict RHS at `syntax.k:44`; `controls.k:20-31`; integer `+`/`-` at `int.k:9-17` |
| `Compare`, `CmpOp` | `syntax.k:30,32`; evaluation/dispatch at `operators.k:14-17`; string equality at `str.k:24-26`; integer comparisons at `int.k:22-27` |
| `Int`, `Bool`, `Str` literals | `syntax.k:9-13`; `core.k:193-196`; ASCII literal conversion at `str.k:12-17` |
| `BoolOp("and",...)` | `syntax.k:16`; left-to-right short circuit at `bool.k:13-25` |
| `Return` | strict result at `syntax.k:50`; control/frame cleanup at `functions.k:77-90` |

The strictness declarations and explicit call argument loop give the needed
evaluation order. Calls allocate a local scope and stack frame; return records
the value, pops exactly that frame, removes the local scope, and restores the
environment and scope allocator. This program performs no heap allocation,
output, external calls, exceptions, or abrupt loop control. Relevant
priority rules for closure cells and heap references cannot match the concrete
integer/Boolean/string state used here.

### Proof-local extensions

1. `scanBrackets(.IntSeq, B, V) => V andBool B ==Int 0`
   is a truthful base equation.

2. The `iCons` equation consumes a strict tail, adds one exactly for code 40,
   subtracts one otherwise, and passes the new balance through `keepValid`.
   This is the submitted loop transition. It is globally truthful even beyond
   the formal alphabet because the Python body also sends every non-`(` value
   through its `else`.

3. `keepValid(B, _) => false` for `B < 0` and
   `keepValid(B,V) => V` for `B >= 0` are disjoint, exhaustive over integers,
   and exactly model permanent prefix invalidity.

4. The guarded simplification of
   `#if C ==Int 40 #then X #else Y #fi` to `Y` under
   `C =/=Int 40` is ordinary Boolean conditional reasoning. Its guard is
   disjoint from the true branch and agrees with the built-in false branch on
   overlap.

5. `bracketInput` is true on `.IntSeq` and recursively conjoins
   `C == 40 or C == 41`. Constructor coverage is exhaustive and recursion is
   on the strict tail, so the `[total]` declaration is justified.

6. `loop-lemma` is an operational bridge, not an oracle. Its bridge-free
   universal connection theorem is `SPEC.loop`, proved using only
   `verification.k` plus fixed supplied semantics. Mechanical comparison shows
   the bridge accepts exactly the theorem's domain: exact loop body, return and
   `#endcall` suffix, `.K` caller continuation, environment, exact local/module/
   builtin scope shape, allocators, empty heap, single frame, return/exception
   state, exit code, and `bracketInput(CS)`. Priority 40 only accelerates
   configurations already covered by that theorem.

The bridge reads the loop term, balance/valid/remaining characters, and the
displayed control/state cells. It writes the proved Boolean result, pops the
exact frame, removes the exact callee scope, restores environment and
`scopeLoc`, and preserves the module/builtin maps, empty heap, `heapLoc`,
`noRet`, `NoExc`, and exit code. The K-generated freshness counter is
automatically framed and no used rule allocates a fresh object.

### Operational and value sensitivity

The reviewer-owned continuation probe inserts `valid = False` between the loop
and return. That state lies outside the bridge's exact suffix. Fixed LLVM and
bridge-enabled Haskell runs therefore execute supplied rules and produce
byte-identical sorted pretty configurations with
`context_result = false`, hash
`e973b446ac2196b110f8bca8d254c49adc5a395207f4d0ebd6101949178fd843`;
see
[evidence/context-containment-valid2.log](evidence/context-containment-valid2.log).

The reviewer-owned body mutation changes the executed opening update from
`+1` to `+2` while retaining the original summary obligation. Against the
bridge-free definition it builds, reaches a complete `false` result for
`"()"`, and exits 1 with `WarnStuckClaimState`:
[evidence/audit-body-sensitivity.k](evidence/audit-body-sensitivity.k) and
[evidence/body-sensitivity.log](evidence/body-sensitivity.log). Thus the
connection theorem is sensitive to the actual loop body.

Ground opposite-value probes also agree between fixed and bridge-enabled
theories:

- `"()"` reaches `true`; demanding `false` is stuck in both
  [evidence/fixed-pair-opposite.log](evidence/fixed-pair-opposite.log) and
  [evidence/non-vacuity.log](evidence/non-vacuity.log).
- `"("` reaches `false`; demanding `true` is stuck in both
  [evidence/fixed-open-opposite.log](evidence/fixed-open-opposite.log) and
  [evidence/opposite-false-value.log](evidence/opposite-false-value.log).

No local rule was found unsound, so there is no unsoundness allegation needing
a false-conclusion witness. The negative probes above demonstrate sensitivity;
they are not used to excuse a false rule.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The reviewer-authored
[evidence/audit-spec-vacuity.k](evidence/audit-spec-vacuity.k) executes the
exact submitted function on the satisfying input `"()"` but deliberately
changes its result obligation from true to false.

The exact command was:

```text
kprove audit-spec-vacuity.k \
  --definition verification-with-loop-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
```

It parsed and built successfully, executed to a complete final configuration
whose `<k>` cell was `true ~> .K`, emitted `WarnStuckClaimState`, and exited 1
because that state could not unify with the requested `false`. This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash. The bounded transcript is
[evidence/non-vacuity.log](evidence/non-vacuity.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

For every finite code sequence `CS` containing only 40 and 41, if execution
terminates under the supplied MPY semantics, loading the trusted-regenerated
submitted function and calling it with `str(CS)` reaches the exact Boolean
`scanBrackets(CS, 0, true)` and the displayed clean final configuration.

For a processed prefix `p`, let `d(p)` be opens minus closes. By induction on
the `scanBrackets` equations, its balance argument is `d(p)` and its validity
argument is true exactly when every processed prefix has nonnegative depth.
The base equation additionally requires final depth zero. Hence, from
`(0,true)`, the proved Boolean is true exactly when no prefix closes too many
brackets and total opens equal total closes—the prompt's correct-bracketing
property. This is ordinary mathematical interpretation of the fully defined
summary, not an opaque result oracle.

### Trust ledger

- **Supplied MPY semantics.** Trusted as the benchmark's fixed execution model.
  Recursive byte/type comparison proves the candidate did not alter it. The
  relevant rules model every material operation used. The theorem does not
  claim that this deliberately partial language definition is a full CPython
  semantics.
- **Trusted translator.** `/reference/py2mpy.py` is outside the K theorem.
  Fresh byte regeneration plus parsed constructor equality connect
  `solution.py`, `solution.mpy`, and the entry claim.
- **K implementation and built-ins.** K v7.1.293, `kompile`, `kprove`,
  `kore-exec`, the Haskell/LLVM backends, strictness generation, and the
  built-in unbounded integer, Boolean, string, map, and list theories are
  trusted. These are ordinary low-level proof foundations, not task-answer
  rules.
- **ASCII bridge.** The only source literal involved is `"("`, code 40; the
  formal input alphabet is codes 40/41. The supplied ASCII string model
  therefore agrees with the relevant Python behavior.
- **Opaque supplied symbols.** The imported baseline declares opaque/concrete
  operations for sorting (`sortVS`, `sortKeyVS`), floats
  (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
  `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
  `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`), and MD5
  (`md5hexCodes`). None occurs in the submitted term, reachable execution
  slice, proof extensions, or postcondition, so none influences either claim.
- **Loop bridge.** Not assumed: it has a freshly rerun, bridge-free universal
  connection theorem over its complete match domain, exact mechanical
  claim/rule identity, continuation containment, ground value agreement, and
  body sensitivity.
- **Empirical evidence.** Differential and concrete tests support the
  Python/translator/intent bridges only on their stated inputs. They are not
  treated as universal proof or as a replacement for either `kprove` result.
- **Termination.** Not claimed. The report is partial correctness as requested.
  Inputs are finite and both the source loop and mathematical summary consume
  a strict tail, but no separate K liveness theorem is needed for this verdict.

Gate A passes: the exact body executes, the only operational bridge has a
bridge-free exact connection theorem, local equations are valid and total on
their declared domains, and meaningful result/body mutations fail. Gate B
passes: the theorem covers the unrestricted finite source-contract domain and
its summary is exactly the correct-bracketing property. Gate C passes: the
trust boundary and all finite evidence are explicit and reproducible.

The proof is result-constraining, non-vacuous, pins the real trusted-regenerated
program, and contains no material adequacy gap or unsound proof-local rule.

VERDICT: PASS
LEGITIMACY: LEGIT
