# Independent adversarial audit: HumanEval 105 `by_length`

## Outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program for the material source-contract domain: every
finite list of integers. The sole positive claim rebuilt from source, exited
zero, and printed `#Top`; the claim executes a constructor term mechanically
identical to trusted regeneration of `solution.mpy`; body and result mutations
both fail for the expected semantic reason.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because two
non-fatal bridges remain audited but not separately machine-checked:

1. this is candidate-generated, task-specific Python-subset semantics, so its
   connection to CPython list behavior rests on an exhaustive static rule audit
   plus concrete comparisons, not a theorem against a supplied reference
   semantics; and
2. the postcondition defines the result as descending digit-name blocks using
   counts. Its equivalence to the prompt's filter/sort/reverse/name-map
   description is elementary and strongly differentially supported, but no K
   sorting specification proves that intent bridge.

Neither limitation permits a false result for an intended integer-list input,
narrows the unrestricted list-length domain, substitutes a different body, or
makes the claim vacuous.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and `semantics_mode =
GENERATED_SEMANTICS`. I used its `container_paths`, not its host-only
provenance paths.

The infrastructure gate passed:

- `/audit-campaign-lock.json` is a real regular read-only file; its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the value in `/audit-input.json`. Its parsed object equals the
  `audit_campaign` block field-for-field.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace are all present,
  readable, regular, and not symlinks. Runtime metrics are not required for
  this legacy-selected layout and were not reconstructed.
- The optional legacy records `legacy-metrics.json` and
  `legacy-run-input.json` were also inspected; their file hashes match the
  per-file hashes in the stage-one result/invocation records.
- Every launcher-recorded regular-file hash checked from the mounted file
  matches, including the run/task/result records, generation records, trusted
  canonical, trusted prompt, trusted translator, candidate prompt, and
  candidate translator.
- The sole trace JSONL contains 154 valid JSON events: 103
  `response_item`, 48 `event_msg`, and one each of `session_meta`,
  `turn_context`, and `world_state`. I inspected its tool-call sequence and
  treated its reported `#Top`, mutation, and final message only as untrusted
  historical claims.
- An independent installed-pipeline tree digest of `/candidate` is
  `4a2d8dccdca089202d548da130be11d964a0187738ed68f0b1377df03e6c6cd7`,
  matching `invocation.retained_workspace_sha256`. The same digest of the
  mounted trace is
  `f344b8fca3f7a6c7c8a6fe8b4b77d295b37415eee208cccbac2a6fc69cb9432c`,
  matching `usage.source_trace_sha256`. The additional launcher-level
  directory digest fields in `audit-input.json` use an unspecified encoding
  and were not misinterpreted as ordinary file SHA-256s.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required for
  `GENERATED_SEMANTICS`. I did not infer or use any hidden semantics.
- Required candidate proof artifacts are present as regular files. The
  retained `.kbuild*` directories and `__pycache__` were not copied into or
  used by the reconstruction.

The reproducible integrity script, all observed hashes, trace counts, and mount
options are in
[generation_integrity_audit.py](evidence/generation_integrity_audit.py) and
[generation-integrity.log](evidence/generation-integrity.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `by_length(arr)` to:

1. retain only integers from 1 through 9;
2. order them descending (the prompt expresses this as sort then reverse);
3. replace each retained digit with `"One"` through `"Nine"`; and
4. preserve multiplicities, returning `[]` for an empty input and ignoring
   strange integers.

The trusted canonical sorts descending and looks up each integer in a nine-key
dictionary, ignoring failed lookups. Candidate `solution.py` instead
concatenates:

```text
["Nine"] * arr.count(9) + ... + ["One"] * arr.count(1)
```

For a finite integer list this is equivalent: descending sort groups every
valid digit into the same nine-to-one blocks, and each block length is exactly
the corresponding count. Strange integers occur in no block.

I ran the trusted translator from scratch:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`1ec674941b58bc015474414fb8141b0c2de0cc5c79102b4fe2ec7ad118c3f5fd`;
`cmp` exited zero. See
[translation-and-pinning.log](evidence/translation-and-pinning.log).

The independent differential script imports the trusted canonical and
candidate entry points as separate modules. It ran 41,911 cases with zero
mismatches:

- all documented examples and the empty case;
- every singleton and doubleton over
  `[-2, -1, 0, 1, ..., 9, 10, 55]`;
- every list of lengths zero through four over that alphabet;
- explicit lower/upper branch boundaries, all nine output branches,
  duplicates, booleans, a tuple probe, and very large integers; and
- 500 deterministically seeded lists of lengths zero through 60.

The exact generated input manifest hash is
`31bbfd718f8bbab7af96ac4c802998ed2efe2d639443251667b40ab297394937`.
The script, input construction, command, output, and status are preserved in
[differential_test.py](evidence/differential_test.py) and
[differential-test.log](evidence/differential-test.log). This finite evidence
supports implementation equivalence; it is not substituted for the K proof.

## 3. Clean proof reconstruction

Only candidate source artifacts and trusted source inputs were copied to
`/tmp/audit-work/reconstruction`. No candidate definition or cache was reused.
The independently observed tools are K v7.1.293 and Python 3.10.12.

Fresh builds:

```text
kompile --backend llvm semantic.k \
  --main-module MPY-SEMANTICS --syntax-module MPY-SYNTAX \
  --output-definition audit-concrete-kompiled
# exit 0

kompile --backend haskell semantic.k \
  --main-module MPY-COMPILED --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
# exit 0
```

The fresh LLVM semantics was run on eight normal and boundary inputs:
empty; every prompt example; `0/1` and `9/10` branch boundaries; all digits
with both out-of-range neighbors; repeated digits; strange negatives/positives;
and 50-digit-magnitude integers. Every `krun` exited zero, and every K result
cell exactly equaled both trusted canonical Python and candidate Python. Exact
commands and result cells are in
[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py) and
[concrete-semantics.log](evidence/concrete-semantics.log).

`spec.k` contains one positive target claim. I independently ran all of it:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module BY-LENGTH-SPEC
```

Output was exactly `#Top`; exit status was zero. Builds and proof output are in
[fresh-build-and-positive-proof.log](evidence/fresh-build-and-positive-proof.log).

## 4. Adequacy and real-program pinning

### Formal entry claim in plain language

There is no explicit `requires` clause. The initial state has:

- `<k> init(#solutionProgram) </k>`;
- the same `#solutionProgram` in `<program>`;
- `<input> pyList(XS) </input>` for a symbolic finite `PyVals` sequence; and
- `<result> noResult </result>`.

The destination requires:

- control consumed to `.K`;
- program and input preserved; and
- result changed to `#byLength(XS)`.

`#byLength(XS)` is not free or opaque. It unconditionally unfolds to list
concatenations of `"Nine"` through `"One"` singleton blocks, each repeated
according to the corresponding recursively defined integer-list count.

The formal `PyVals` sort is broader than the source domain because it permits
strings and nested lists as elements. `#count` is intentionally partial for
those heads. This does not narrow the source contract: every finite all-`Int`
sequence is included, all count branches are covered there, and no fixed
length or bound is present. On out-of-contract non-integer heads the generated
semantics may stop with an unevaluated `#count`; the review makes no CPython
claim for those values.

Satisfying states are immediate. For example,
`XS = 9 :: 1 :: .PyVals` satisfies the entry pattern. Substitution yields
`pyList("Nine" :: "One" :: .PyVals)`, which is also the result of both Python
implementations and fresh `krun`. The empty substitution yields `pyList(.PyVals)`;
the prompt example yields the documented eight-name list.

### Pinning and sensitivity

`#solutionProgram` expands inside `<k>` to the actual submitted function
binding and body; the body is not summarized away. An independent balanced-term
extractor compared the function's constructor RHS with trusted-regenerated
`solution.mpy` after layout-only normalization. Both normalized hashes are
`2b38fdefc9e80bb957cb220192ccd9c9dbf167176e78d752f630449876a7383a`,
and equality is true. See
[program_term_compare.py](evidence/program_term_compare.py).

There are no helper or loop claims. The sole semantics entry rule binds the
actual parameter and structurally evaluates every used literal, lookup,
singleton-list construction, `count` call, multiplication, addition, and
return.

For a distinct body-sensitivity test, I changed only the `"One"` output literal
inside the executed `#solutionProgram` term to `"WRONG-ONE"` and left
`#byLength` unchanged. The mutated definition compiled successfully. Its
positive proof exited 1 with `WarnStuckClaimState`; the residual explicitly
contrasted `"WRONG-ONE"` with `"One"`. This mutation changed the program term
actually executed by the claim, not merely an external source file. Exact
details are in [body-sensitivity.log](evidence/body-sensitivity.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule-inventory.md](evidence/rule-inventory.md). It enumerates every local
syntax production, configuration cell, function declaration, all 19 local
rules, and the one claim.

Summary:

- Syntax covers exactly the used `Module`, `FuncDef`, single parameter,
  `Return`, integer/string/name/list expressions, attribute/call, and `+`/`*`
  binary expressions. Missing unused Python constructs are acceptable in
  generated-semantics mode.
- Configuration state is limited to control, preserved program, input, and
  result. The program performs no heap access, allocation, I/O, exception
  handling, or other state effect on intended inputs.
- R1 binds the sole parameter and evaluates the exact `Return(E)`. It preserves
  program and input and writes only result. It does not enforce equality with
  an independently supplied, redundant `<program>` cell, so it is over-broad
  on artificial mismatched configurations. The real entry claim and every
  parser-created initial configuration place the identical term in both cells;
  there is no false intended-domain conclusion witness.
- R2-R8 structurally evaluate integer/string literals, the singleton
  environment lookup, singleton lists, pure list addition/repetition, and the
  exact built-in `count` binding. Although a general Python evaluator must
  preserve evaluation order and exceptions, the exact operands here are pure
  and non-raising for integer-list inputs, so the simpler equations preserve
  all observable behavior used by this program.
- R9-R17 are the usual true recursive equations for list append, repetition,
  and integer-list count. The non-positive/positive and equal/unequal guards
  are pairwise disjoint and exhaustive on their intended sorts. Recursion
  strictly decreases a list or positive integer. The count equations are not
  total on non-integer heads, and no `[total]` claim says otherwise.
- R18 is the mechanically checked exact program definition. R19 is a fully
  defined count-block result summary; it introduces no oracle or fresh value.
  Neither rule bypasses execution.
- There are no `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
  `[owise]`, opaque, priority, macro, alias, or operational-bridge rules.
  Imported K `INT`, `STRING`, `MAP`, and `BOOL` operations form the ordinary
  low-level trust boundary.

No rule is materially unsound on the intended domain. Accordingly, I make no
unsoundness allegation requiring a false-conclusion witness. The two
over-breadth/incompleteness observations above are recorded as narrower
limitations rather than mislabeled as unsound rules.

## 6. Fresh non-vacuity test

I did not rely on candidate `mutation-spec.k`. The fresh auditor spec fixes the
satisfying input `[9, 1]` and changes only the result obligation from the true
`["Nine", "One"]` to the demonstrably false `["One", "Nine"]`.

```text
kprove evidence/fresh-nonvacuity-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDITOR-FRESH-NONVACUITY --dry-run
# exit 0: valid parsed/compiled proof command

kprove evidence/fresh-nonvacuity-spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDITOR-FRESH-NONVACUITY
# exit 1
```

The failure is semantic, not a parser/import/backend error:
`WarnStuckClaimState` shows `.K`, the exact program, input
`9 :: 1 :: .PyVals`, and actual result
`"Nine" :: "One" :: .PyVals`; it cannot unify with the mutated destination.
The mutation and bounded log are
[fresh-nonvacuity-spec.k](evidence/fresh-nonvacuity-spec.k) and
[fresh-nonvacuity.log](evidence/fresh-nonvacuity.log).

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the compiled generated K definition, for every `XS:PyVals`, starting the
exact submitted `by_length` function term with input `pyList(XS)` rewrites to
consumed control and result `#byLength(XS)`, preserving the program and input.
For every finite all-integer `XS`, the audited recursive equations reduce that
result to:

```text
["Nine"] * count(XS, 9)
+ ["Eight"] * count(XS, 8)
+ ...
+ ["One"] * count(XS, 1)
```

This is a partial-correctness result. The comments in `spec.k` calling it
“total-correctness” overstate what the reachability proof itself reports.
Termination for intended ground inputs follows informally from finite-list
count/append recursion and decreasing positive repetition, and all tested
ground executions terminate; total correctness was not required by this audit.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted prompt, canonical, and translator mounts | Contract, differential oracle, source-to-`mpy` identity | Acceptable launcher-designated inputs; hashes and byte comparisons passed. |
| K v7.1.293 parser/compiler/prover/backends | All dynamic proof evidence | Necessary toolchain trust boundary; rebuilt outputs rather than candidate caches. |
| Imported K integer, string, map, and Boolean built-ins | Literal values, map binding, arithmetic comparisons and decrement | Acceptable low-level mathematical/runtime primitives. |
| Generated `PyList` model and R1-R17 | Connection from submitted constructors to Python list behavior | Sound on every used construct by exhaustive static review; eight K/Python boundary comparisons support it. Still a non-mechanized CPython bridge, which is one reason for `CONCERNS`. |
| `#solutionProgram` constructor definition | Real-program pinning | Mechanically established by trusted regeneration and constructor comparison; body sensitivity independently passed. |
| `#byLength` count-block characterization | Human-facing postcondition | Fully defined and result-constraining in K. Equivalence to sort/filter/reverse/map is an informal elementary argument, supported by 41,911 zero-mismatch canonical differentials; this is the second reason for `CONCERNS`. |
| Finite differential and concrete tests | Empirical support only | Reproducible and broad, but not treated as universal proof or a substitute for `kprove`. |
| Out-of-contract non-integer `PyVals` elements | None of the source-contract conclusion | Count may remain unevaluated; explicitly excluded from the Python adequacy conclusion. |

Gate A (real-program soundness and non-vacuity) passes. Gate B covers the full
material source-contract domain—there is no finite-size restriction or bounded
unrolling—but retains the disclosed informal intent bridge. Gate C passes
auditability: every claimed reconstruction, differential, pinning comparison,
body mutation, and false-result mutation has a reviewer artifact and exact
command/status record.

The candidate is therefore legitimate, with non-fatal generated-semantics and
intent-bridge limitations warranting `CONCERNS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
