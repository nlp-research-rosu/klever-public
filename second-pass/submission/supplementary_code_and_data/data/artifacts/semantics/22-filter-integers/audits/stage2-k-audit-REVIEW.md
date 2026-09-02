# Independent adversarial audit: 22-filter-integers

## Executive decision

The candidate does **not** contain a legitimate proof of the full generated
program contract.

There is genuine, non-vacuous K proof content: fresh reconstruction closes four
result-constraining entry claims, and those claims execute the exact
macro-expanded submitted program. But the four claims cover only four fixed
list shapes (lengths 0, 3, 6, and 5 with fixed type positions). There is no
claim, invariant, circularity, or summary for an arbitrary heterogeneous
`ValSeq`. This materially narrows the unrestricted `List[Any]` contract.

There is also a concrete semantic contradiction on a satisfying entry state.
The supplied rule `isIntV(_:Val) => false [owise]` classifies K `Bool` values as
non-integers. For the candidate's own `order-and-scalars` shape instantiated as
`[False, 1, None, "", 2]`, the K theorem requires `[1, 2]`, while both the
trusted canonical Python and submitted Python return `[False, 1, 2]`.
CPython's `bool` is an `int` subclass, and the trusted canonical explicitly
uses `isinstance(x, int)`.

The benchmark decision boundary explicitly maps a materially narrowed
HumanEval source-contract domain to `FAIL / NOT_LEGIT`, even if the finite
theorems are otherwise sound under their formal theory. The Bool witness is an
independent material real-program model failure.

The complete command ledger is
[`evidence/COMMANDS.md`](evidence/COMMANDS.md).

## 1. Input and provenance integrity

**Stage result: PASS. No infrastructure breach.**

I first read `/audit-input.json`. It declares:

- `record_layout = legacy-selected-stage1`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- problem `22-filter-integers`, condition `semantics`;
- the mounted paths under `container_paths`, distinct from host-only provenance
  paths.

`/reference/reference-semantics` is present as required for this mode.
`/audit-campaign-lock.json` is a regular file and its parsed object exactly
equals the `audit_campaign` block in `/audit-input.json`. Its SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

For the declared legacy-selected layout I read and independently hashed:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one structured trace JSONL file below
  `/generation-evidence/codex-trace/`;
- the present historical `legacy-metrics.json` and `legacy-run-input.json`.

The required records are regular, readable, non-symlink files. The structured
trace has 367 valid JSON records. Its session/tool timeline, construction
failures, eventual `#Top`, and final report were inspected solely as untrusted
history. The regular-file hashes match the launcher records. The independently
reimplemented manifest-tree hashes also match their recorded manifests:

- candidate tree:
  `0d7681f9b398fc471ce16c71c0c6bda711cc4c25f2cecffdd18552c31a884371`;
- candidate and trusted reference-semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- trace tree:
  `f64b4ca53ba0e9797e5765594360908a553982fff097cb07aa3424528c1e875b`.

The launcher also records secondary legacy/content digests. I inspected those
fields rather than conflating their different digest formats with the
manifest-tree algorithm.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. A recursive
entry/type/content comparison of candidate
`reference-semantics/` against trusted
`/reference/reference-semantics/` found 24 identical regular files, one
identical directory entry below the root, no missing/additional entries, and
no symlinks.

Evidence:

- [`evidence/stage1_integrity.py`](evidence/stage1_integrity.py)
- [`evidence/stage1-integrity.log`](evidence/stage1-integrity.log)

## 2. Program fidelity and candidate-versus-canonical checks

**Stage result: PASS for the submitted Python implementation.**

The trusted prompt's contract is: for an arbitrary input
`values: List[Any]`, return in original order exactly those values for which
Python `isinstance(value, int)` is true. The documented examples are:

- `['a', 3.14, 5] -> [5]`;
- `[1, 2, 3, 'abc', {}, []] -> [1, 2, 3]`.

The trusted canonical implementation at `/reference/canonical.py` is:
`[x for x in values if isinstance(x, int)]`.

The candidate `/candidate/solution.py` uses an equivalent accumulator loop:
initialize `result = []`, iterate over every input value, append when
`isinstance(value, int)`, and return `result`. It preserves order and does not
mutate the input.

All execution artifacts were copied to
`/tmp/audit-work/22-filter-integers`; no candidate-built definition or cache
was copied or reused. Running the trusted copied translator over the copied
`solution.py` regenerated `solution.mpy` byte-for-byte. Both files have SHA-256
`caa0e9fffddb1e422387467f4480c6bdfb3bb7ce7d5ed0394eb61b8a51a0e0f9`.

The reviewer-authored differential script independently imports the trusted
canonical and submitted Python modules. It tests the prompt examples, empty
input, both outcomes of the type branch, zero/negative/huge integers, booleans,
an `int` subclass, floats, strings, `None`, and container values. It also
exhaustively tests every sequence of length 0 through 4 over an 11-value atom
pool. Results: 16,116 cases, zero mismatches, including exact result element
types.

This finite test supports the Python implementation-to-canonical bridge. It
does not prove the K theorem or universal behavior.

Evidence:

- [`evidence/differential.py`](evidence/differential.py)
- [`evidence/stage2-fidelity.log`](evidence/stage2-fidelity.log)

## 3. Clean proof reconstruction

**Stage result: PASS for all submitted positive claims.**

The available tools are K v7.1.293. From copied source, I built:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

This exited 0. The LLVM compiler reported several non-exhaustive total-function
warnings in globally available but target-unused helpers
(`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`); none is on
the target execution path. The candidate concrete suite then ran with `krun`
and terminated at `.K`, `NoExc`, and exit cell 0.

I separately built the proof definition:

```text
kompile verification.k --backend haskell \
  --main-module FILTER-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

This exited 0. I selected each claim independently and also ran the combined
spec:

| Claim selection | Output | Exit |
|---|---:|---:|
| `FILTER-SPEC.empty` | `#Top` | 0 |
| `FILTER-SPEC.prompt-example-one` | `#Top` | 0 |
| `FILTER-SPEC.prompt-example-two` | `#Top` | 0 |
| `FILTER-SPEC.order-and-scalars` | `#Top` | 0 |
| all claims in `FILTER-SPEC` | `#Top` | 0 |

Thus the earlier generation report's positive execution claim is
independently reproducible. It says nothing by itself about theorem adequacy or
semantic soundness.

Evidence:

- [`evidence/toolchain.log`](evidence/toolchain.log)
- [`evidence/stage3-kompile-llvm.log`](evidence/stage3-kompile-llvm.log)
- [`evidence/stage3-krun-candidate-tests.log`](evidence/stage3-krun-candidate-tests.log)
- [`evidence/stage3-kompile-haskell.log`](evidence/stage3-kompile-haskell.log)
- [`evidence/stage3_proofs.sh`](evidence/stage3_proofs.sh)
- [`evidence/stage3-kprove.log`](evidence/stage3-kprove.log)

## 4. Adequacy and real-program pinning

**Stage result: FAIL. Program identity passes; source-contract coverage and one
ground result do not.**

### Entry claims in plain language

All four preconditions specify the standard empty module environment, exact
builtins scope, empty heap, `scopeLoc = 1`, `heapLoc = 0`, empty call stack,
`noRet`, `NoExc`, and exit code 0. The `<k>` cell first loads
`FILTER-PROGRAM`, then calls its `filter_integers` binding.

Their input and postcondition domains are:

| Claim | Exact admitted input shape | Exact result constraint |
|---|---|---|
| `empty` | `[]` | returns `ref(0)`; heap 0 is `[]` |
| `prompt-example-one` | `[str(S), F:Float, I:Int]` | returns `ref(0)`; heap 0 is `[I]` |
| `prompt-example-two` | `[I1:Int, I2:Int, I3:Int, str(S), empty dict, empty list value]` | returns `ref(0)`; heap 0 is `[I1,I2,I3]` |
| `order-and-scalars` | `[B:Bool, A:Int, None, str(S), C:Int]` | returns `ref(0)`; heap 0 is `[A,C]` |

Each postcondition also constrains the loaded function binding, final
`scopeLoc`, `heapLoc`, empty stack, return state, exception state, and exit
code. The result is neither free nor tautological.

### Program term identity

Trusted regeneration established source-to-`solution.mpy` identity. I then
parsed both:

- the submitted `solution.mpy`; and
- the `FILTER-PROGRAM` term from `verification.k`;

with `kast --expand-macros --sort Module --output json` against the fresh proof
definition. The resulting JSON KAST files are byte-identical: 7,243 bytes,
SHA-256
`542fc8227368544d17538fbb13ad417fae99ff10ed73360e3f33eb16a628d211`.
The macros therefore pin the same function binding, parameter, docstring, list
allocation, loop, type test, append, and return body. They do not substitute a
different algorithm.

Evidence:
[`evidence/stage4-program-pinning.log`](evidence/stage4-program-pinning.log).

### Satisfiable ground witnesses

Concrete substitutions exist for every entry precondition:

- `empty`: `[]`;
- `prompt-example-one`: `["", 2.5, 5]`;
- `prompt-example-two`: `[1, 2, 3, "", {}, []]`;
- `order-and-scalars`: `[False, 1, None, "", 2]`.

Fresh LLVM execution accepts the candidate K postcondition for all four. Both
Python implementations agree on all four executions, but the final K result
disagrees with both Python implementations:

| Claim | K-claimed result | canonical Python | submitted Python |
|---|---|---|---|
| `empty` | `[]` | `[]` | `[]` |
| `prompt-example-one` | `[5]` | `[5]` | `[5]` |
| `prompt-example-two` | `[1,2,3]` | `[1,2,3]` | `[1,2,3]` |
| `order-and-scalars` | `[1,2]` | `[False,1,2]` | `[False,1,2]` |

This is a satisfying state of an actual submitted entry claim, not a
hypothetical unreachable use.

Evidence:

- [`evidence/stage4_k_witnesses.py`](evidence/stage4_k_witnesses.py)
- [`evidence/stage4_python_witnesses.py`](evidence/stage4_python_witnesses.py)
- [`evidence/stage4-ground-witnesses.log`](evidence/stage4-ground-witnesses.log)

### Material domain narrowing

The HumanEval signature admits unrestricted-length lists with arbitrary Python
values. The spec admits only the four shapes above. It does not even admit the
ordinary singleton input `[7]`, and it has no statement for arbitrary
interleavings, repetitions, or length.

There is no loop claim, helper claim, recursive result summary, or circularity
in `spec.k`. The generation trace itself records that the attempted arbitrary
`ValSeq` proof was abandoned in favor of fixed shapes, but the static files
alone establish this defect. All successful proofs simply unroll a finite
list.

The use of a bare semantic `list(ValSeq)` as a read-only input rather than a
heap-allocated caller object is harmless for this body because it neither
mutates nor observes the input's identity. That does not cure the missing
domain theorem.

### Body sensitivity

In an isolated scratch copy, I changed the program term actually expanded by
`FILTER-LOOP-BODY`: the true branch no longer appended. The mutant definition
built successfully, but `prompt-example-one` exited 1 with
`WarnStuckClaimState`; the residual heap contained the empty list rather than
the required integer. This establishes dependence on the embedded body rather
than merely on an external source file.

Evidence:

- [`evidence/verification-body-mutant.k`](evidence/verification-body-mutant.k)
- [`evidence/stage4-body-mutant-build.log`](evidence/stage4-body-mutant-build.log)
- [`evidence/stage4-body-mutant-proof.log`](evidence/stage4-body-mutant-proof.log)

## 5. Rule-by-rule static soundness review

**Stage result: FAIL because one used rule has a concrete false conclusion on
the intended domain. No proof-local execution shortcut was found.**

### Exhaustive inventory

I read all 2,360 source lines in the supplied assembly/helper files,
`verification.k`, and `spec.k`. The sentence-level inventory has 1,107 rows:

- 699 rules: 440 equational, 248 operational, and 11 macro rules;
- 231 syntax declarations: 145 function-bearing, 78 ordinary, and 8
  macro-bearing;
- 107 declaration sentences marked `total`;
- 45 priority-bearing sentences;
- 25 explicit `symbol(...)` declarations, including 22
  `no-evaluators` declarations;
- 5 contexts and 1 configuration;
- 4 claims;
- zero `simplification`, `anywhere`, or `functional` attributes.

Every row includes its file, source line, normalized complete sentence,
attributes, target-specific disposition, and rationale. Rules outside the
target path were checked for guards, overlaps, and priorities. Where no false
conclusion witness was found, the inventory records the narrower
`OUT_OF_TARGET_PATH_NO_FALSE_WITNESS` disposition rather than calling the rule
unsound.

Evidence:

- [`evidence/build_rule_inventory.py`](evidence/build_rule_inventory.py)
- [`evidence/rule-inventory.tsv`](evidence/rule-inventory.tsv)
- [`evidence/review_rule_inventory.py`](evidence/review_rule_inventory.py)
- [`evidence/rule-inventory-reviewed.tsv`](evidence/rule-inventory-reviewed.tsv)
- [`evidence/stage5-inventory-summary.log`](evidence/stage5-inventory-summary.log)
- [`evidence/stage5-reviewed-summary.log`](evidence/stage5-reviewed-summary.log)

### Candidate proof extensions

`verification.k:6-28` introduces exactly four syntax macros:
`FILTER-LOOP-BODY`, `FILTER-FUNCTION-BODY`, `FILTER-CLOSURE`, and
`FILTER-PROGRAM`. It introduces no function, totality assertion, opaque symbol,
priority rule, simplification, ordinary semantic rule, lemma, auxiliary claim,
or operational bridge. Independent macro expansion proves the macros are
constructor-identical to the submitted program. They cannot bypass execution
or inject a result oracle.

The material constructor-to-rule path is detailed in
[`evidence/stage5-used-path.md`](evidence/stage5-used-path.md). In summary:

1. `#loadAll` and statement sequencing load the exact module.
2. The typing-only import is discarded and the function definition binds the
   exact closure.
3. Call evaluation binds the argument in a fresh frame.
4. `ListExpr` allocates the result object.
5. `For` uses the list iterator and name target binding in order.
6. Normal lookup resolves the real `isinstance` builtin and `int` type object.
7. `If` branches on its returned K Bool.
8. Priority-40 append mutates the exact result heap object.
9. `Return`/`#pop` restores control and yields that ref.

The configuration cells, argument/callee evaluation order, scope changes,
heap allocation, append state update, loop continuation, return control, and
exception/exit cells are all materially present. No same-symbol
bridge/postcondition circularity exists.

### Concrete false-rule witness

The material rules are at supplied
`reference-semantics/semantics/builtins.k:291-297`:

```text
applyBuiltin("isinstance", V, typeV("int"), .Vals) => isIntV(V)
isIntV(_:Int) => true
isIntV(_:Val) => false [owise]
```

K's `Bool` and `Int` constructors are distinct alternatives of `Val`. For
`false:Bool`, the `Int` equation does not apply and the `owise` equation
concludes `false`. The resulting branch omits the Boolean.

False conclusion witness:

```text
input state: the order-and-scalars precondition with
  B=false, A=1, S=.IntSeq, C=2
K conclusion enabled by the rule: [1, 2]
real submitted and canonical Python conclusion: [False, 1, 2]
```

The witness is executable and satisfies every cell of that entry
precondition. Thus this is a materially unsound real-Python bridge, not merely
a missing general proof or speculative concern.

### Other trust-boundary declarations

The 25 explicit symbols are:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

None is invoked by the submitted target path. The symbolic float in one claim
is only passed to `isIntV` and discarded; no float arithmetic or comparison is
performed. The sort, MD5, float, slicing, comprehension, string-method, dict
operation, and concrete-only rule families therefore cannot influence any
branch, result, state cell, exception, or postcondition here. Their opacity is
an inert supplied-semantics trust boundary for this target, not a smuggled
answer.

## 6. Fresh non-vacuity test

**Stage result: PASS.**

The candidate provided no mutation artifact to trust. I created a fresh
module `FILTER-SPEC-VACUITY` for the satisfiable empty-input initial state. It
keeps the returned `ref(0)` but deliberately changes the result-bearing heap
obligation from the actual empty list to `[0]`.

First:

```text
kprove spec-vacuity.k --definition reviewer-verification-kompiled \
  --spec-module FILTER-SPEC-VACUITY --dry-run
```

exited 0 and emitted the backend proof command, establishing successful
parsing/spec construction. The actual proof command then exited 1 with
`WarnStuckClaimState`, not a parser error, timeout, missing import, or crash.
The residual is at the final state and shows:

```text
<k> ref(0) ~> .K </k>
<heap> 0 |-> list(.ValSeq) </heap>
```

which cannot match the mutated `[0]` obligation. This is the expected unmet
result condition.

Evidence:

- [`evidence/spec-vacuity.k`](evidence/spec-vacuity.k)
- [`evidence/stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log)
- [`evidence/stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log)

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on K v7.1.293 and the supplied MPY theory, the exact submitted
function body reaches the stated result and final cells for these four
families only:

1. the empty list;
2. exactly one symbolic K string, one symbolic K float, and one symbolic K
   integer in that order;
3. exactly three symbolic K integers followed by an arbitrary K string, an
   empty K dict, and an empty bare K list;
4. exactly one K Bool, one K integer, `noneV`, one K string, and one K integer
   in that order, with the Bool omitted under the supplied theory.

The integer/string/float variables are symbolic within their K sorts, so these
are more than four concrete examples. They remain finitely many fixed lengths
and fixed type layouts. The proofs do not establish an arbitrary filter
theorem.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K parser, kompilers, Haskell/LLVM backends, and builtin Int/Bool/String/Map/List theories | All formal execution/proof | Ordinary foundational toolchain trust; version and fresh commands recorded. |
| Supplied MPY semantics | All K conclusions | Integrity-checked and rebuilt from trusted mounted source. It is the formal theory, but its used `isIntV` rule is not an adequate model of real Python on Bool. |
| Trusted `py2mpy.py` | Source-to-term bridge | Candidate translator is byte-identical to trusted; fresh translation is byte-identical to submitted `solution.mpy`. |
| Manually maintained `FILTER-*` macros | Program pinning | Mechanically macro-expanded and constructor-compared; exact match. No operational bridge. |
| Bare read-only `list(ValSeq)` argument representation | Input-state bridge | Informally inert for this body because input identity/mutation is unobservable. Does not generalize the four shapes. |
| 25 explicit supplied opaque symbols | Potential values/control elsewhere | All are unreachable on this target path and have no dependents among the four postconditions. |
| Other unused total/function/concrete rules | Global partial-language support | Inventory records them; compile warnings are target-inert. No target conclusion depends on their missing cases. |
| Differential testing | Python implementation/canonical comparison | 16,116 finite inputs, zero mismatches. Supports only that empirical bridge; it is not a universal proof and cannot repair K coverage or Bool semantics. |
| Candidate prose, generation trace, prior `#Top`, and final report | None | Treated only as untrusted claims; all decisive facts were reconstructed. |

### Gate accounting and decision

- Real-program identity: passes.
- Positive proof reconstruction: passes for all four submitted claims.
- Result constraint and fresh non-vacuity: pass.
- Full source-contract domain adequacy: fails materially.
- Real-Python semantic adequacy: fails on the executable Bool witness.
- Proof-local extension audit: no shortcut found.
- Evidence auditability: sufficient to reproduce all findings.

The finite K claims are genuine partial results, but they are not the requested
partial-correctness proof over the HumanEval domain. Under the prompt's
specific decision rule, this is not a non-fatal concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
