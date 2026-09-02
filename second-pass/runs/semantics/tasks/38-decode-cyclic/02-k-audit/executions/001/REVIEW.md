# Independent adversarial audit: 38-decode-cyclic

## Decision

The candidate contains a sound, non-vacuous partial-correctness proof of the
submitted decoder under the supplied MPY semantics. The proof executes the
exact translated `decode_cyclic` body, constrains its returned string to a
fully defined recursive specification, and survives a clean rebuild. There is
no proof-local operational shortcut or opaque result oracle.

The outcome is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two
documented limitations:

1. The Python implementation is recursive while the canonical implementation
   is iterative. On this audit environment, valid encoded strings of length
   3000 and above make the candidate raise `RecursionError` while the
   canonical implementation returns the decoded string. The supplied MPY
   semantics has an unbounded semantic call stack and does not model this
   CPython resource exception. This is a real implementation-to-intent and
   language-model adequacy gap, although it does not invalidate partial
   correctness for normally returning executions in the selected semantics.
2. Four requested provenance records and any structured generation trace are
   absent. Fresh reconstruction makes the proof result independently
   reproducible, but the original generation process is not auditable.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present as a real directory, so the trusted
mount does not contradict the rendered mode. The candidate
`reference-semantics/` tree was recursively compared with it by entry name,
entry type, symlink target, and file bytes:

- no missing, additional, changed, mistyped, or symlinked semantics entry was
  found;
- the candidate tree is therefore byte-identical to the trusted supplied
  semantics;
- this identity does not bless the proof-specific rules in
  [verification.k](/candidate/verification.k).

The candidate [prompt.py](/candidate/prompt.py) and
[py2mpy.py](/candidate/py2mpy.py) are regular files and byte-identical to
their trusted mounted versions. `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are also regular, non-symlink files.

### Missing provenance

The following requested candidate records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was found. Consequently there were no such
claims to trust or read. The candidate also supplied no `PROOF.md`; no
candidate prose was used as proof evidence. The Python `__pycache__` entry was
ignored.

Evidence: [integrity checker](/audit-output/evidence/stage1_integrity.sh) and
[integrity log](/audit-output/evidence/stage1-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt defines `encode_cyclic` as follows: split a Python string
into consecutive groups of at most three characters; rotate each complete
three-character group left (`abc` becomes `bca`); preserve a final group of
length one or two. `decode_cyclic` must invert that encoding.

The trusted canonical implementation computes `encode_cyclic` twice. On each
complete input triple this rotates right (`bca` becomes `abc`), while a final
short group is unchanged. Chunk rotation is bijective, so every Python string
is in the image of `encode_cyclic`; the phrase “string encoded with
encode_cyclic” does not impose a smaller set of strings.

The submitted [solution.py](/candidate/solution.py) implements the same
per-chunk result recursively:

- length below three: return the suffix unchanged;
- otherwise return `s[2] + s[:2] + decode_cyclic(s[3:])`.

This covers both branches at lengths 0/1/2 versus 3 and all three residues
modulo three.

### Trusted regeneration

In the scratch copy, the command

```text
python3 /reference/py2mpy.py /tmp/audit-work/38-decode-cyclic/candidate/solution.py > /tmp/audit-work/38-decode-cyclic/candidate/solution.regenerated.mpy
```

exited 0. `cmp -s` against the submitted `solution.mpy` exited 0. Both MPY
files have SHA-256
`33e04dde6676394955f4f478f5d0734059c07ff5e143dcc8c8a055af49958d1f`.

Evidence: [regeneration script](/audit-output/evidence/stage2_regenerate.sh)
and [regeneration log](/audit-output/evidence/stage2-regeneration.log).

### Independent differential tests

The reviewer-authored test imports the trusted canonical module and the
scratch copy of the candidate module using separate explicit paths. It does
not reuse K proof equations. It exercised:

- 15 explicit empty, boundary, residue, multi-frame, whitespace, NUL, and
  Unicode cases;
- all 3,280 strings of lengths 0 through 7 over `{"a", "b", "🧪"}`;
- 2,000 deterministic random strings of lengths 0 through 80 over ASCII,
  whitespace, NUL, accented, CJK, and supplementary Unicode characters.

There were zero mismatches in 5,295 direct canonical/candidate comparisons and
zero failures in 5,295 `candidate.decode(canonical.encode(x)) == x` checks.
The complete deterministic inputs are preserved.

Evidence:
[test](/audit-output/evidence/differential_test.py),
[inputs](/audit-output/evidence/differential-inputs.json), and
[results](/audit-output/evidence/stage2-differential.log).

### Material large-input divergence

The unrestricted Python contract has a resource-bound counterexample. With
the environment's recursion limit of 1000:

- lengths 2800 through 2990 in the selected probe returned and matched;
- lengths 3000, 3010, 3100, and 6000 returned normally from the canonical
  implementation but raised `RecursionError` in the candidate.

For example, take the length-3000 source string generated by the preserved
script and pass its `canonical.encode_cyclic` result to both decoders. This is
a satisfying intended-domain input. The canonical result has length 3000;
the candidate raises `RecursionError: maximum recursion depth exceeded while
calling a Python object`.

Evidence: [large-input probe](/audit-output/evidence/long_input_test.py) and
[results](/audit-output/evidence/stage2-long-input.log).

This is not a false K rule: it is precisely the gap between the supplied
unbounded MPY call semantics and resource-bounded CPython execution.

## 3. Clean proof reconstruction

All candidate sources needed for execution were copied to
`/tmp/audit-work/38-decode-cyclic`; trusted sources were copied separately.
No candidate K definition or cache was copied or reused. The only candidate
cache was an irrelevant Python bytecode cache.

Working directory for the following commands was
`/tmp/audit-work/38-decode-cyclic/candidate`.

### Concrete definition

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-audit-kompiled
```

Exit 0. The compiler emitted non-exhaustiveness warnings for several supplied
functions outside the target slice (`mapStrVS`, float helpers,
`joinCodes`, and `valSeqAt`) and unused-variable warnings in `strLt`; these
were warnings, not build failures. None is reachable from the decoder claims.

Fresh execution:

```text
krun concrete_tests.mpy --definition runtime-audit-kompiled
```

Exit 0 with final `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.

Evidence:
[LLVM build](/audit-output/evidence/stage3-kompile-concrete.log) and
[concrete run](/audit-output/evidence/stage3-krun-concrete.log).

### Proof definition and positive claims

```text
kompile verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-audit-kompiled
kprove spec.k --definition verification-audit-kompiled --spec-module SPEC
```

Both commands exited 0. The full proof printed `#Top`; this run contains and
closes both positive claims in `SPEC`.

The helper claim was also copied unchanged into an isolated module and proved
independently:

```text
kprove spec-helper-only.k --definition verification-audit-kompiled --spec-module SPEC-HELPER-ONLY
```

It exited 0 and printed `#Top`.

As a diagnostic dependency test, the entry claim was then run after removing
the helper claim. That reviewer-created artifact exited 1 at the nested
recursive body, with a `WarnStuckClaimState`. This is expected and is not a
failed candidate target: it removes the circularity on which the candidate's
two-claim proof deliberately depends. The residual shows a second active
decode frame and `buildIS(CS, 3, isLen(CS), 1)`. Thus the full `#Top` is not
from an entry-only shortcut; it uses the real helper claim.

Evidence:
[Haskell build](/audit-output/evidence/stage3-kompile-proof.log),
[full proof](/audit-output/evidence/stage3-kprove-full.log),
[helper-only spec](/audit-output/evidence/spec-helper-only.k),
[helper-only proof](/audit-output/evidence/stage3-kprove-helper.log),
[entry-only diagnostic](/audit-output/evidence/spec-entry-only.k), and
[dependency residual](/audit-output/evidence/stage3-kprove-entry.log).

## 4. Adequacy and real-program pinning

### Claims in plain language

The helper claim at [spec.k:8](/candidate/spec.k:8) says:

- execution begins at the exact `decode_cyclic` body followed immediately by
  `#endcall`;
- the active local scope `L` binds `s` to `str(CS)`, its parent is module scope
  0, module scope 0 binds the exact decoder closure, and scope -1 is the
  supplied builtins scope;
- `L` is neither reserved location 0 nor -1, all explicit and residual scope
  keys are below the next fresh location, and `NEXT` is positive;
- if this body normally reaches its return boundary, the continuation is
  `#pop` and `<ret>` is exactly `retV(str(decodeCodes(CS)))`;
- heap, heap counter, caller stack, exception, and exit-code cells are framed
  unchanged.

The entry claim at [spec.k:30](/candidate/spec.k:30) says:

- from a clean module-level state with exactly the decoder closure and builtins,
  calling it on any semantic string `str(CS)` produces exactly
  `str(decodeCodes(CS))`;
- environment, scopes, allocation counters, stack, return state, exception,
  and exit code remain in the stated clean form.

`CS:IntSeq` ranges over finite semantic code sequences. There is no hidden
content or length restriction.

### Satisfiable preconditions and ground substitutions

The entry precondition is satisfied by `CS = .IntSeq` in exactly the written
clean state. A helper witness is `L=1`, `NEXT=2`, `SC=.Map`, empty heap and
stack, `HNEXT=0`, and `CODE=0`; all inequalities and `keysBelow` hold.

Six explicit substitutions, including every base length and multiple recursive
frames, were evaluated against an independently written `decodeCodes`
recurrence and both Python implementations. All agreed. In particular:

- `CS=[98,99,97]` (`"bca"`) gives `[97,98,99]` (`"abc"`);
- `CS=[98,99,97,101,102,100,103]` (`"bcaefdg"`) gives
  `[97,98,99,100,101,102,103]` (`"abcdefg"`).

Evidence:
[witness script](/audit-output/evidence/claim_witness.py) and
[ground results](/audit-output/evidence/stage4-ground-witnesses.log).

### Real-body pinning

`decodeBody` in [verification.k:7](/candidate/verification.k:7) is the exact
translated statement body in the freshly regenerated `solution.mpy`.
`decodeClosure` at [verification.k:26](/candidate/verification.k:26) is exactly
the closure created by the supplied `FuncDef` rule: parameter `s`, that body,
and defining scope 0. The helper begins at that exact body and its recursive
application occurs at the real nested call frame.

A fresh concrete load of the submitted `solution.mpy` terminated successfully
and installed that identical decoder closure. It also installed the unrelated
`encode_cyclic` binding. The entry claim starts after module load and omits
that unused extra binding. This reduction from the complete loaded module
state to an exact call state is checked by source/AST comparison and by the
fixed lookup rules, not by a separate candidate reachability theorem. It is a
minor manual pinning bridge: the absent `encode_cyclic` key cannot affect
lookup, control, state, or the decoder's result.

Evidence:
[fresh module load](/audit-output/evidence/stage4-krun-solution-load.log).

### Result constraint

`decodeCodes` is not free or opaque. Its two guards are disjoint and exhaustive
because `isLen(CS)` is a non-negative integer:

- length below three returns `CS`;
- length at least three constructs code 2, then codes 0 and 1, then recursively
  processes the slice starting at 3.

The helper claim is the bridge-free universal connection theorem from exact
body execution to this fully defined result. No proof rule replaces a
`<k>`-cell computation with `decodeCodes`. The false-result mutation in stage
6 confirms that the entry result is genuinely constrained.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The bounded line-addressable inventory covers `semantics.k`, every imported
supplied helper K file, `verification.k`, and `spec.k`. It contains:

- 946 total records: 231 syntax declarations, 707 rules, 5 contexts, 1
  configuration, and 2 claims;
- 928 supplied-semantics records, 16 proof-local records, and 2 positive
  claims;
- 147 `function`, 108 `total`, 45 `priority`, 26 `owise`, 35 `concrete`,
  6 `simplification`, 6 `macro`, 1 `macro-rec`, 2 `strict`, and 1
  `seqstrict` declarations/attributes;
- no `functional` declaration;
- 25 explicitly named symbolic declarations, of which 22 use
  `no-evaluators`.

Every row records source file, line, kind, attributes, source class, static
decision, and a bounded rendering. `ACCEPT_FIXED_RULE_UNUSED_BY_TARGET` means
accepted for this theorem's reachable slice, not a claim that the intentionally
minimal supplied MPY model implements all of Python.

Evidence:
[inventory generator](/audit-output/evidence/k_inventory.py),
[complete inventory](/audit-output/evidence/stage5-rule-inventory.log),
[used-construct map](/audit-output/evidence/used-construct-map.md), and
[symbolic/opaque declarations](/audit-output/evidence/stage7-opaque-symbols.log).

### Supplied semantics and target control flow

The complete program-construct map is preserved in the cited artifact. The
reachable path uses only:

- module/function syntax and the fixed module-loader/closure rules;
- name and builtin lookup;
- left-to-right callee/argument and binary-expression evaluation;
- `len`, integer comparison, truthiness, and branching;
- string indexing, slicing, concatenation, and `IntSeq` length;
- call-frame allocation, binding, return, pop, and scope deallocation.

The configuration carries `<k>`, `<env>`, `<scopes>`, `<scopeLoc>`, `<heap>`,
`<heapLoc>`, `<stack>`, `<ret>`, `<exc>`, and `<exit-code>`. Calls update the
environment, scope map/counter, stack, and return cell in the expected order
and restore them on pop. The decoder neither allocates heap objects nor mutates
the heap. Its exception and exit-code cells remain unchanged.

Relevant guards are disjoint:

- `<` yields a Boolean and selects exactly one `#branch`;
- direct indexing occurs only on the length-at-least-three path;
- slice start/stop normalization gives `0:2` and `3:len` with unit step;
- recursive calls create a fresh scope and pop it before continuing.

Relevant priority rules only preempt generic paths for refs, cells, or call
dispatch. The decoder input is a bare `str(IntSeq)`, not a heap ref or cell, and
the candidate adds no priority rule. No relevant overlap changes binding or
evaluation order.

The 25 supplied symbolic/opaque declarations are:
`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`. None is reachable from either positive claim and
none can influence its branch, result, state, exception, or postcondition.

The LLVM non-exhaustiveness warnings likewise concern unreachable supplied
operations. No false conclusion witness exists through the decoder's intended
input domain, so they are recorded as an unused modeling/evidence boundary,
not mislabeled as an unsound target rule.

### Proof-local rules

The 16 proof-local inventory records at `K0929` through `K0944` were assessed
as follows:

| Records | Classification and decision |
|---|---|
| `K0929-K0930` (`decodeBody`) | Exact compile-time macro for the submitted body. It does not bypass execution. Accepted. |
| `K0931-K0932` (`decodeClosure`) | Exact compile-time macro for the supplied semantics' closure value. Accepted. |
| `K0933-K0935` (`decodeCodes`) | Result-bearing definitional summary. The guards `<3` and `>=3` are disjoint/exhaustive; the recursive suffix is three codes shorter; the equation is the mathematical right rotation of each full triple. Accepted. |
| `K0936` | Derived slice-length lemma. For length at least three and unit step, `buildIS(CS,3,len,1)` has length `len-3`. Accepted. |
| `K0937` | Derived clamp lemma. When `len>=3`, `clampHi(3,len,1)=3`, including equality at length 3. Accepted. |
| `K0938-K0940` (`keysBelow`) | Structural finite-map predicate: true exactly when every scope key is below the bound. Recursive cases terminate and ordering of AC map decomposition cannot change the Boolean truth. Accepted. |
| `K0941` | If every key is below `N`, every key is below `N+1`. Accepted. |
| `K0942` | If every key is below `N`, key `N` is absent. Accepted. |
| `K0943` | Fresh map update equals insertion because `N` is absent under `keysBelow`. Accepted. |
| `K0944` | Removing the explicit fresh `N` entry restores the residual map, whose keys exclude `N`. Accepted. |

There is no proof-local `<k>` rewrite, priority rule, opaque declaration,
unconstrained fresh value, totalized partial oracle, or rule that recognizes
the task and fabricates its answer. `decodeCodes` affects the postcondition,
but exact body execution is independently connected to it by the helper claim.
The same symbol is therefore not used circularly as both an operational oracle
and a specification.

No inventoried candidate rule was labeled unsound, so there is no omitted
false-rule witness. The concrete long-input witness from stage 2 concerns
CPython's resource model, not the truth of a K equation.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` existed. The reviewer created a new module that
retains the unchanged helper claim and changes only the entry result to:

```text
str(seqConcat(decodeCodes(CS), iCons(33, .IntSeq)))
```

This demands an extra `!`. It is demonstrably false for the satisfying witness
`CS=.IntSeq`, where the actual and positive claimed result is the empty
sequence.

Command:

```text
kprove spec-vacuity-audit.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY
```

The spec parsed and built far enough to execute the proof. It exited 1 with
`WarnStuckClaimState`, not a parser/import/backend error. The residual reached
the actual result `str(decodeCodes(CS))` and reported the failed implication:

```text
decodeCodes(CS) =/= seqConcat(decodeCodes(CS), iCons(33, .IntSeq))
```

This is the expected unmet result obligation.

Evidence:
[mutation](/audit-output/evidence/spec-vacuity-audit.k) and
[mutation proof log](/audit-output/evidence/stage6-kprove-vacuity.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY definition, for every finite semantic code sequence
`CS`, starting in the exact clean call state of the entry claim:

- the submitted decoder body is selected through its closure and receives
  `str(CS)` as `s`;
- if execution normally completes, it returns
  `str(decodeCodes(CS))`;
- `decodeCodes` preserves suffixes of length below three and right-rotates
  every complete triple;
- recursive frames obey the scope freshness invariant and are popped without
  changing heap, exception, or exit-code state.

The helper claim establishes the same result for an active exact body frame
under its stated scope invariant. As this is a partial-correctness proof, it
does not establish CPython termination, a recursion-depth bound, time, or
memory usage.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K toolchain and Haskell reachability backend (`K v7.1.337`) | Both claims and all symbolic reasoning | Necessary low-level proof checker trust; fresh build and mutation behaved coherently. |
| Byte-identical supplied MPY semantics | Entire proof | Authorized fixed semantics. Relevant rules were reviewed. Its unbounded call stack is the source of the documented CPython recursion limitation. |
| K builtin integer, Boolean, string, map, list, and equality theories | Length arithmetic, guards, scope invariant, sequence construction | Ordinary low-level mathematical trust; no task-specific answer is encoded. |
| Trusted translator as a Python-to-MPY bridge | Identity of `solution.mpy` | The submitted MPY was regenerated byte-for-byte. Correctness of the translator itself is not proved in K, but every target construct and its resulting AST were inspected. |
| Manual body/closure pin | Entry state versus complete module-load state | Exact AST and closure match; fresh module load confirms it. The unused `encode_cyclic` module binding is omitted from the claim. Acceptable but informal. |
| `decodeCodes` meaning | Natural-language decoder result | Equations are transparent ordinary mathematics and the helper formally connects them to execution. Equivalence to the human-facing contract is inspected and finitely differential-tested, not stated as a separate K theorem. |
| 25 supplied symbolic/opaque primitives | None | Unreachable from this program and both claims; no value/control/state dependence. |
| Differential testing | Intent and Python bridge only | 5,295 bounded cases support the bridge but do not prove it. The separate large-input test exposes the CPython limitation. Tests did not substitute for K proof closure. |
| Missing generation provenance | Historical generation audit only | Concerning evidence gap, but not used to establish the theorem because all executable evidence was reconstructed. |

### Gate summary

- Real-program soundness / Gate A: **PASS**. Exact body execution, truthful
  result summary, guarded mathematical lemmas, state fidelity, a satisfying
  precondition, and a rejecting false-result mutation.
- Intent adequacy / Gate B: **LIMITED**. Per-chunk functional behavior agrees,
  but unrestricted CPython execution raises `RecursionError` on valid large
  inputs while the formal MPY model returns.
- Evidence auditability / Gate C: **PASS for the reconstructed audit**. All
  commands, statuses, bounded outputs, scripts, deterministic inputs, and
  mutation are preserved. Original generation provenance remains absent.

The proof is therefore legitimate as a partial-correctness theorem in the
selected supplied semantics, but it should not be reported as an unrestricted
total-correctness or all-CPython-input result.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
