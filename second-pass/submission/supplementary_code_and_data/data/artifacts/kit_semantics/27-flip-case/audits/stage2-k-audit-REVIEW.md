# Independent adversarial audit: 27-flip-case

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the actual submitted `solution.mpy` under the supplied fixed semantics. The
required claim was rebuilt from source and independently returned `#Top` with
exit 0. The proof definition adds no proof-local syntax, equation, lemma,
rewrite, priority, summary, bridge, or oracle. A constructor-level comparison
shows that the complete `Module(FuncDef(...))` loaded by the claim is exactly
the trusted regeneration of the submitted Python program.

This is not a clean `PASS` because the supplied string model implements
ASCII-only case conversion while the HumanEval/CPython string domain is
Unicode. For example, the model returns internal code point 233 unchanged for
`é`, while both the trusted canonical and submitted Python programs return code
point 201 (`É`). This is precisely the documented supplied-model
representation/behavior-gap exception in campaign amendment v2: the gap comes
from the immutable supplied semantics, the claim covers every `IntSeq` value
that model admits without candidate-added narrowing, the candidate records the
boundary and a concrete witness in its trust ledger, and the submitted Python
program is behavior-AST-identical to the canonical implementation after
discarding only the canonical docstring. The correct mapping is therefore
`CONCERNS / LEGIT`.

The evidence index is [evidence/README.md](evidence/README.md).

## 1. Input and provenance integrity

### Launcher records and campaign lock

`/audit-input.json` declares:

- problem `27-flip-case`;
- condition `kit-semantics`;
- `record_layout = pipeline-v3`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `mount_reference_semantics = true`; and
- the mounted locations through `container_paths`, rather than the host-only
  provenance paths.

Every record required for `pipeline-v3` is a readable regular file or real
directory: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the structured trace. The one trace file contains 201 valid
JSONL records. The complete generation log has 14,201 lines. I read these only
as untrusted generation history; none was used as proof evidence.

The parsed `/audit-campaign-lock.json` object is exactly equal to
`audit_input["audit_campaign"]`, and its independently computed SHA-256 is the
recorded
`e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`.
All recorded hashes with mounted file counterparts match, including the
canonical source, prompt, translator, run/task/result/invocation records, all
generation records, and the individual trace. The independently reimplemented
pipeline-v3 manifest digest of the mounted candidate is
`5b70c5e08d1887218f0001526d74dd4d599dcc6037a144818bde83fd6ea6bd8c`,
equal to both the stage result and invocation output bindings. See
[stage1-integrity.log](evidence/stage1-integrity.log) and
[generation-record-summary.log](evidence/generation-record-summary.log).

### Trusted-source and supplied-semantics identity

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Recursive comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` found the same 25 entries (one directory and
24 regular files), the same names and types, and identical bytes. There are no
missing, additional, mistyped, unsupported, or symlinked entries. The
independent semantics manifest digest is the recorded
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
The supplied-semantics mount is present as required, so there is no rendered
mode/mount contradiction and no infrastructure breach.

The candidate includes all required proof artifacts. Candidate-provided
`runtime-kompiled/`, `verification-kompiled/`, bytecode, logs, `PROOF.md`, and
negative probes were treated as untrusted and were not reused. Only source
artifacts and the trusted semantics were copied to
`/tmp/audit-work/rebuild`; the bounded copy inventory is
[scratch-copy.log](evidence/scratch-copy.log).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires:

> Given a string, change lowercase characters to uppercase and uppercase
> characters to lowercase.

The documented example is `flip_case("Hello") == "hELLO"`. The trusted
canonical implementation is `return string.swapcase()`. The submitted
`solution.py` has the same signature and the same return expression. A
mechanical AST comparison found identical signature and behavioral body after
removing only the canonical function docstring; see
[source-fidelity.log](evidence/source-fidelity.log).

### Translation identity

Using the trusted translator in clean scratch:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

exited 0. `cmp -s solution.regenerated.mpy solution.submitted.mpy` also exited
0. Both terms have SHA-256
`f34d90ab871c6106c87ea64aa17e5ae4da5bfd5e86ca7ce805959554f8ae8620`.
The generated term is:

```text
Module(
  FuncDef("flip_case", Params("string"),
    Return(Call(Attribute(Name("string"), "swapcase"), ))))
```

See [translation.log](evidence/translation.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently loads the
trusted canonical and scratch candidate modules. It covers:

- the documented example and empty string;
- every ASCII branch boundary (`@`, `A`, `Z`, `[`, backtick, `a`, `z`, `{`);
- every ASCII code point 0 through 127 in one input;
- mixed letters, digits, whitespace, punctuation, and embedded NUL;
- non-ASCII simple mappings and expansions (`éÉ`, `ß`, Greek sigma forms,
  Turkish dotted/dotless I, ligature `ﬀ`, emoji, and combining marks); and
- 240 deterministic generated strings of lengths 0, 1, 2, 3, 7, and 31 from a
  mixed ASCII/Unicode alphabet (seed 2700729).

All 259 cases match canonical; all ASCII cases also match an independently
implemented ordinal-range oracle. There are zero mismatches. Complete inputs,
code points, and outputs are preserved in
[differential-results.json](evidence/differential-results.json); the command
and status are in [differential-test.log](evidence/differential-test.log).
Finite testing supports fidelity but is not substituted for the K proof.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

The observed live toolchain is K 7.1.293
([toolchain.log](evidence/toolchain.log)). Both definitions were created under
new names in the source-only scratch tree.

### Concrete definition and execution

The fresh concrete command was:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-fresh
```

It exited 0. The compiler reported non-exhaustive matches in fixed, unused
helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`)
plus four unused variables in unrelated `strLt` rules. These are assessed in
Stage 5. See [llvm-build.log](evidence/llvm-build.log).

Fresh `krun` executions of the regenerated submitted module and an
auditor-authored program containing empty, example, ASCII branch-edge, and
mixed-input assertions both exited 0. Their final configurations have
`<k> .K </k>`, `NoExc`, exit code 0, the expected closure, an empty heap and
stack, and restored allocation counters. See
[krun-solution.log](evidence/krun-solution.log) and
[krun-runtime-cases.log](evidence/krun-runtime-cases.log).

### Proof definition and every positive target

The fresh proof build was:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-fresh
```

It exited 0, with only the four fixed `strLt` unused-variable warnings
([haskell-build.log](evidence/haskell-build.log)). The compiled rule-source
audit confirms zero rules from `MPY-CONCRETE` and zero local rules from
`verification.k`; see
[proof-definition-slice.log](evidence/proof-definition-slice.log).

Parsing `spec.k` finds exactly one positive target claim,
`SPEC.flip-case`. Its independent proof command was:

```text
kprove spec.k \
  --definition verification-kompiled-fresh \
  --spec-module SPEC
```

It exited 0 and printed `#Top`; see
[kprove-target.log](evidence/kprove-target.log). There are no helper, loop, or
other positive claims to reconstruct.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Plain-language claim

The claim has no logical side condition: its parsed `requires` and `ensures`
are both `true`. Its structural precondition is:

- an arbitrary `CS:IntSeq`;
- the exact initial module environment 0;
- an empty module scope whose parent is the fixed builtins scope;
- scope counter 1;
- empty heap and heap counter 0;
- empty call stack;
- `noRet`, `NoExc`, and exit code 0; and
- `<k>` containing `#loadAll` of the submitted one-function module, followed by
  a call of `flip_case` on `str(CS)`.

Its postcondition says the call result is exactly `str(mapSwap(CS))`; the
module scope contains exactly the expected closure with the submitted body;
the caller environment and all control/allocation cells are restored; the
heap and stack are empty; no exception occurred; and exit code remains 0.
This is an equality-style result obligation, not a free variable, tautology,
or one-way implication.

### Program identity

I parsed the trusted regenerated `solution.mpy` with `kast`, compiled the spec
to JSON in dry-run mode, located the unique `#loadAll` module inside the unique
claim, and compared complete constructor trees. Both have normalized
constructor SHA-256
`ce9acfb964ef701947f86f769da35b2567d5ead05df17e52efc0d91fd2403059`;
the trees are equal. Thus the source spelling `Call(..., )` and spec spelling
`Call(..., .Exprs)` normalize to the same zero-argument constructor rather
than denoting different programs. See
[program-pinning.log](evidence/program-pinning.log),
[solution.kast.json](evidence/solution.kast.json), and
[spec-claims.json](evidence/spec-claims.json).

### Satisfiability, concrete substitution, and body sensitivity

The precondition is satisfiable, for example with
`CS = iCons(65, .IntSeq)` (`"A"`). The auditor-authored ground claim for that
state returned `#Top`; `mapSwap` produces code point 97 (`"a"`), and both
Python implementations return `"a"`. See
[concrete-substitution.log](evidence/concrete-substitution.log).

The separate body-sensitivity mutation changes the actual `FuncDef` term
executed by the claim from `return string.swapcase()` to `return string` while
retaining the expected lowercase result. Its dry build exits 0; proof search
exits 1 with a reachable residual containing code point 65 while the
destination demands 97. This tests the theorem's dependence on the executed
body rather than changing an external source file only. See
[body-sensitivity.k](evidence/body-sensitivity.k) and
[body-sensitivity.log](evidence/body-sensitivity.log).

There is no loop in the submitted function and therefore no circular helper
claim to match against control flow.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule-inventory.tsv](evidence/rule-inventory.tsv) inventories every local
declaration in all 24 supplied K files plus `verification.k` and `spec.k`, with
source line range, attributes, full normalized declaration text, and a
theorem-slice assessment for each row. Its independently checked totals are:

| Item | Count |
|---|---:|
| All inventoried declarations | 1,096 |
| Ordinary/equational/operational rules | 695 |
| Syntax declarations | 227 |
| Contexts | 5 |
| Configurations | 1 |
| `function` declarations | 146 |
| `total` declarations | 107 |
| `symbol` declarations | 25 |
| `no-evaluators` declarations | 22 |
| Priority-bearing entries | 45 |
| Concrete-bearing entries | 36 |
| Macro/macro-rec entries | 5 |
| Simplification declarations | 0 |
| `functional` declarations | 0 |
| Claims | 1 |
| Proof-local semantic extensions in `verification.k` | 0 |

The generating script and totals are
[rule_inventory.py](evidence/rule_inventory.py) and
[rule-inventory-summary.txt](evidence/rule-inventory-summary.txt). The
rule-by-rule decisions and detailed transition-cone reasoning are also
summarized in
[static-soundness-analysis.md](evidence/static-soundness-analysis.md).

### Construct-to-rule map for the submitted program

| Used constructor/control | Fixed declaration and rules | Assessment |
|---|---|---|
| `Module`, `#loadAll`, statement sequence | `syntax.k:61`, `core.k:124-127` | Loads and sequences the exact module; no alternate candidate rule. |
| `FuncDef`, `Params` | `syntax.k:53,57,60`, `functions.k:14-16` | Binds the exact body and parameter in scope 0. |
| `Call` | `syntax.k:28`, `call.k:19-24,69-74` | Evaluates callee then arguments, creates/restores a real call frame, and dispatches the exact binding. |
| `Name` | `syntax.k:12`, `core.k:130-154` | Resolves `flip_case` in scope 0 and `string` in scope 1; neither lookup reaches an ambiguous binding. |
| `Attribute` | `syntax.k:29`, `call.k:16` | Evaluates the string receiver and creates the bound `swapcase` method. |
| `Return` | `syntax.k:50`, `functions.k:78-90` | Implements abrupt return, frame pop, state restoration, and value propagation. |
| argument list and sequencing | `core.k:183-191,213-215` | Zero/one-argument cases are exhaustive here and preserve left-to-right order. |
| `str(CS).swapcase()` | `methods.k:10,21` | Exact fixed method equation returns `str(mapSwap(CS))`. |
| `mapSwap`, `swapC` and predicates | `methods.k:112-164` | Structural recursion is descending and constructor-complete; uppercase/lowercase guards are disjoint and the `owise` case is their complement. |

The call layer is intentionally a subset rather than a full Python type/error
model: generic function calls do not globally enforce all possible Python
arity failures, and attributes do not globally model every missing-method
exception. On this claim's complete match state there is exactly one argument
for one parameter and `swapcase` is selected on a primitive `str`. Those
broader fixed rules therefore agree with binding, evaluation, control, result,
and every observable cell on every state admitted by this entry claim.

### Functions, overlap, totality, priorities, and opaque terms

The result-bearing functions on the target path are not opaque:

- `mapSwap(.IntSeq) = .IntSeq`;
- `mapSwap(iCons(C,S)) = iCons(swapC(C), mapSwap(S))`;
- uppercase and lowercase `swapC` cases have disjoint integer intervals; and
- the `owise` equation supplies the complement.

The equations terminate by tail descent and cover every `IntSeq`/`Int`
argument. No fresh symbol is shared circularly between execution and the
postcondition. `mapSwap` is the fixed semantics' defined result, not a
candidate-added summary.

All 45 priority-bearing entries are from the supplied tree; none matches this
target path. All compiler-reported non-exhaustive total functions are also
outside the path. They cannot contribute a result, branch, state update, or
proof step to this theorem. The exhaustive ledger records this narrower fact
rather than asserting that the supplied subset is a universally complete
CPython semantics.

The 25 fixed symbolic/opaque declarations are:

```text
md5hexCodes;
intFloatDiv, divII, floatMod, floatLt, absF, floorFI, toF, ceilF,
subF, divF, addF, mulF, powF, gtF, eqF, decStrToF,
divFloatIntV, intToF, truncF, roundF, roundFN, sqrtF;
sortVS, sortKeyVS
```

None is reachable from the submitted module or appears in its postcondition.
`MPY-CONCRETE` is absent from the fresh Haskell proof definition. There are no
local simplifications, totality declarations, opaque terms, priority rules, or
ordinary rewrites in `verification.k`.

### Model divergence witness

The fixed `swapC` equation leaves code point 233 unchanged. The
auditor-authored positive fixed-model claim for input
`str(iCons(233,.IntSeq))` returns that same value and prints `#Top`
([kprove-model-gap.log](evidence/kprove-model-gap.log)). A second, well-formed
claim demanding CPython's code point 201 builds but is rejected with a residual
at 233; both canonical and candidate Python return 201. See
[model-gap-comparison.log](evidence/model-gap-comparison.log).

That is a concrete false conclusion witness if the supplied ASCII equation
were misrepresented as full CPython Unicode semantics. It is not a
proof-local unsound rule and does not make a false fixed-model conclusion
provable. No candidate-added or target-reachable rule was found for which an
unsoundness witness exists.

Stage 5 result: **PASS for real-program soundness under the supplied model**,
with the documented Unicode adequacy concern carried to the verdict.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh
[spec-auditor-vacuity.k](evidence/spec-auditor-vacuity.k) uses satisfying input
`"A"` but changes the result-constraining destination from the true code point
97 (`"a"`) to code point 98 (`"b"`).

The dry-build command:

```text
kprove spec-auditor-vacuity.k \
  --definition verification-kompiled-fresh \
  --spec-module SPEC-AUDITOR-VACUITY --dry-run
```

exited 0, proving the mutation is syntactically and definition-wise valid. The
same command without `--dry-run` exited 1 with `WarnStuckClaimState`; its
reachable residual contains the true `str(iCons(97,.IntSeq))`, which cannot
unify with the demanded code point 98. The failure is the expected unmet result
obligation, not a parser error, missing import, timeout, unrelated crash, or
unreached branch. Full bounded output is
[non-vacuity.log](evidence/non-vacuity.log).

Stage 6 result: **PASS**.

## 7. Proven-versus-assumed accounting

### What the successful reachability proof establishes

Under the unchanged supplied `MPY` semantics, for every finite constructor
term `CS:IntSeq`, execution from the exact initial state:

```text
#loadAll(exact submitted module) ~>
Call(Name("flip_case"), str(CS))
```

returns exactly `str(mapSwap(CS))`, installs exactly the submitted closure in
module scope, restores the caller/control state, leaves heap and allocation
counters unchanged, raises no modeled exception, and leaves exit code 0. This
is an unbounded symbolic theorem over the fixed model, not a collection of
examples or bounded unrollings.

It is a partial-correctness result in the Kit sense. The report does not turn
it into a separate general liveness theorem or a full formalization of CPython.

### Trust ledger

| Boundary | Influence and dependents | Evidence | Judgment |
|---|---|---|---|
| Supplied `MPY` operational semantics | Defines all binding, evaluation, control, state, and the returned `mapSwap` term for the target | Recursive byte identity; exhaustive inventory; fresh builds; concrete and symbolic executions | Acceptable fixed benchmark semantics, except for the explicit Unicode adequacy gap |
| `mapSwap`/`swapC` equations | Fully determine the target value | Disjoint/exhaustive rule review; `"A"` ground proof; code-point-233 model witness | Sound for the supplied ASCII case model; not full CPython Unicode |
| K builtin theories used on path (`Int`, `Bool`, `Map`, `List`, `String`, K equality/pattern matching) | Arithmetic guards, maps, stacks, tokens, and constructor equality | K 7.1.293 fresh LLVM/Haskell builds and proof | Ordinary low-level tool/logic trust boundary |
| K compiler, LLVM/Haskell backends, and `kore-exec` | Compilation, concrete execution, and proof checking | Exact versions and independent command logs | Necessary machine-checker trust |
| Trusted `py2mpy.py` | Connects `solution.py` to the constructor program | Byte identity plus trusted regeneration and `cmp` | Acceptable; translation is reproducible |
| Canonical Python and CPython execution | HumanEval implementation oracle and model-gap witness | Behavioral AST identity; 259-case differential; explicit Unicode outputs | Strong implementation-fidelity evidence; finite executions are not a K proof |
| All 25 fixed opaque symbols listed in Stage 5 | Potential values for unrelated float, sort, and MD5 programs | Rule-source slice and exhaustive inventory | No dependency from this theorem; no result/control/state influence |
| Candidate `PROOF.md`, generation trace, prior `#Top`, and compiled definitions | Untrusted claims only | Independently ignored/reconstructed | Not part of the trust basis |

### Amendment v2 checklist

All four supplied-model-gap conditions hold:

1. **Supplied origin:** the ASCII literal/`chr`/case rules are in the immutable
   supplied semantics, recursively byte-identical between candidate and
   trusted reference. `verification.k` adds nothing.
2. **No candidate narrowing:** the theorem quantifies over unconstrained
   `CS:IntSeq`, with no length, code-point, ASCII, or other precondition.
3. **Explicit candidate ledger and witness:** candidate `PROOF.md` identifies
   `strToCodes`, guarded `chr`, and ASCII `swapC` as the model boundary,
   records a failing non-ASCII K construction and CPython's `É`, and includes
   the boundary in its trust ledger. The independent audit strengthens this
   with direct internal K claims for code point 233.
4. **Python fidelity on the gap:** submitted `solution.py` and trusted
   `canonical.py` both directly call `string.swapcase()` and return `É` for
   `é`; the divergence is model-versus-CPython, not
   program-versus-canonical.

Gate A (real-program soundness) passes. The theorem has a real Unicode
language-model limitation relative to the full source contract, but it is the
documented supplied-model gap covered by the campaign exception rather than a
candidate-caused domain restriction. Evidence is reproducible, and no other
material adequacy or trust-boundary defect remains.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
