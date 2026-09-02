# Independent adversarial audit: 16-count-distinct-characters

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted program under the supplied MPY semantics. The proof covers every
`IntSeq` admitted by that fixed model and adds no proof rules. The one material
limitation is a supplied-model Unicode lowercase gap that the candidate
explicitly documented with a concrete U+0130 witness. Under campaign amendment
v2, that is a non-fatal concern rather than candidate-caused domain narrowing.

## 1. Input and provenance integrity

`/audit-input.json` declares `pipeline-v3`,
`SUPPLIED_SEMANTICS`, problem `16-count-distinct-characters`, and the expected
container mounts. I read it before treating any candidate record as evidence.
The campaign object is exactly equal to `/audit-campaign-lock.json`, whose
independent SHA-256 is
`e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`,
the value recorded in the audit input.

All pipeline-v3 records were present and readable with the required types:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace tree. Every
independently checked file hash matched its corresponding manifest field. The
pipeline tree hash of `/candidate` was
`349f2b23a3e3e16a757f53cc73dfed7f2b0914ad2d803b9381b03b4f33eab46a`,
matching `generation-result.json`; the trace tree hash matched
`usage.json`; and the trace's sole JSONL file matched its recorded file hash.
See [stage1-provenance.log](evidence/stage1-provenance.log),
[stage1-hash-assertions.log](evidence/stage1-hash-assertions.log), and
[generation-record-inspection.md](evidence/generation-record-inspection.md).

The trusted prompt and candidate prompt are byte-identical, as are the trusted
and candidate translators. `/reference/reference-semantics` is present as
required by the rendered mode. A recursive, no-dereference comparison of it
against `/candidate/reference-semantics` reported no missing, additional,
changed, mistyped, or symlinked entry. The proof deliverables are regular
files. No infrastructure breach was found.

The generation transcript and trace claim prior build, proof, mutation, and
test successes. I treated those only as untrusted history. No candidate
compiled definition, cache, `PROOF.md` conclusion, or old `#Top` was reused.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for any Python `str`, return the number of distinct
characters in `string.lower()`, so case distinctions are ignored according to
CPython lowercase behavior. The examples require 3 for `"xyzXYZ"` and 4 for
`"Jerry"`. The trusted implementation is:

```python
return len(set(string.lower()))
```

`/candidate/solution.py:1-2` uses exactly that return expression and signature.
Omitting the canonical docstring is semantically inert.

I regenerated the constructor program in scratch using
`/reference/py2mpy.py`. The regenerated and submitted `solution.mpy` files were
byte-identical, both with SHA-256
`2e97b9f354373f39763938a074e4f09fb6a259868fdc704ed07b670ed65ccfc9`.
See [stage2-regeneration.log](evidence/stage2-regeneration.log).

The independent differential script
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and scratch candidate modules separately and also uses a list-based
oracle that does not call `set`. It tested:

- both documented examples;
- 20 empty, singleton, duplicate, ASCII branch-boundary, NUL, punctuation, and
  Unicode cases;
- all 1,555 strings of lengths 0 through 4 over `aA0!zZ`; and
- 500 seeded generated strings of lengths 0 through 64 over mixed ASCII,
  Unicode, control, and supplementary-plane characters.

All 2,077 cases matched. In particular, canonical and candidate both return 2
for U+0130 `"İ"`, 6 for `"Straße"`, 2 for `"Σσς"`, and 1 for
`"𐐀𐐨"`. See
[stage2-differential.log](evidence/stage2-differential.log). Thus the submitted
Python is faithful to canonical even where the supplied K model later
diverges.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/candidate-src`, using the
trusted reference semantics tree rather than candidate-built definitions. A
pre-build search found no `*-kompiled` directory there. The live tools were K
v7.1.293 and Python 3.10.12.

The fresh LLVM command was:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. Its warnings concerned non-exhaustive helpers for unrelated
features such as `mapStrVS`, float conversions, `joinCodes`, and `valSeqAt`;
none is selected by this program. The reviewer-authored concrete K program
[audit-concrete.mpy](evidence/audit-concrete.mpy) then exited 0 and produced:

```text
empty_result       = 0
documented_one     = 3
documented_two     = 4
case_boundary      = 1
model_gap_u0130    = 1
```

The complete configuration is in
[stage3-concrete.log](evidence/stage3-concrete.log); the clean build record is
[stage3-toolchain.log](evidence/stage3-toolchain.log).

The fresh Haskell definition was built with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0. `spec.k` contains exactly one positive target claim. Independently
running

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

printed `#Top` and exited 0. See
[stage3-proof-build.log](evidence/stage3-proof-build.log) and
[stage3-positive-proof.log](evidence/stage3-positive-proof.log). The clean
dynamic reconstruction gate therefore passes.

## 4. Adequacy and real-program pinning

The sole entry claim in `/candidate/spec.k:6-39` has no `requires` clause. In
plain language, its precondition is:

- `CS` is any finite `IntSeq`;
- `<k>` contains a call of `count_distinct_characters` on `str(CS)`;
- scope 0 binds that exact name to a one-argument closure with environment 0
  and the submitted return body;
- the builtins frame, allocation counters, heap, stack, return state,
  exception state, and exit code are the model's pristine values.

Its postcondition is that `<k>` becomes
`isLen(dedupCodes(mapLower(CS)))` and every other explicitly shown cell is
restored or preserved. This is an equality-constraining result, not a free
variable, implication, or tautology. `CS = .IntSeq` is an immediate satisfying
state and yields 0.

Trusted regeneration plus
[program_pinning_check.py](evidence/program_pinning_check.py) mechanically
extracts and normalizes the `Return` constructor from regenerated
`solution.mpy` and from the closure in `spec.k`. The constructor strings are
identical:

```text
Return(Call(Name("len"),Call(Name("set"),
Call(Attribute(Name("string"),"lower"),))))
```

The comparison also checks the public name, sole parameter, closure environment
0, and `str(CS:IntSeq)` entry argument. Its successful output is
[stage4-pinning.log](evidence/stage4-pinning.log).

Although the target claim starts after module loading, that setup is pinned
rather than substituted. The fresh auxiliary claim
[audit-load-pinning.k](evidence/audit-load-pinning.k) executes
`#loadAll(Module(FuncDef(...)))` under fixed semantics and proves that it
creates exactly the scope binding embedded in the target claim. It printed
`#Top` and exited 0
([stage4-load-pinning-proof.log](evidence/stage4-load-pinning-proof.log)).
The source-to-claim link is therefore mechanical and machine-checked; lack of
an automatic spec generator is only a maintenance observation.

Concrete substitutions of `""`, `"xyzXYZ"`, `"Jerry"`, `"aA"`,
`"ABCabc"`, and NUL agree among the formal postcondition's fixed-model
interpretation, trusted canonical, and submitted Python. The U+0130
substitution records the deliberate boundary: model result 1 versus
canonical/candidate result 2. See
[stage4-ground-substitutions.log](evidence/stage4-ground-substitutions.log).

Finally, the independent body-sensitivity artifact
[audit-body-mutation.k](evidence/audit-body-mutation.k) changes the actual
closure body executed by the claim to `Return(Int(0))`. It did not prove:
`kprove` exited 1 with `WarnStuckClaimState` and the unmet equality
`0 = isLen(dedupFrom(mapLower(CS), .IntSeq))`. A concrete counterexample is
`CS = iCons(65,.IntSeq)`, whose required result is 1. See
[stage4-body-mutation-proof.log](evidence/stage4-body-mutation-proof.log).

## 5. Rule-by-rule static soundness review

The exhaustive inventory
[k-rule-inventory.tsv](evidence/k-rule-inventory.tsv), generated by
[inventory_k.py](evidence/inventory_k.py), contains 929 records:

- 77 ordinary syntax declarations, 124 function declarations, 4 macro
  declarations, and 22 opaque `no-evaluators` declarations;
- 1 configuration, 5 contexts, 238 operational rules, 425 equations, and 32
  concrete-only rules; and
- the one target claim.

It records exact file, line, attributes, complete flattened declaration,
target dependency, and disposition for every item. This includes 107 records
with `total`, 29 priority rules, and 26 `owise` rules. There are no local
`simplification` rules and no `functional` declarations.
`reference-semantics/semantics.k` only assembles modules, and
`verification.k` only imports `MPY`; each has zero local rule/declaration
records. Thus the candidate added no function, equation, lemma, priority rule,
opaque symbol, trusted primitive, or operational bridge.

The target-path mapping and per-class assessment are in
[target-path-static-review.md](evidence/target-path-static-review.md). The
execution is:

1. normal name lookup selects the exact closure;
2. normal call machinery evaluates callee and arguments and pushes a frame;
3. parameter lookup and bound-method dispatch select the exact `"lower"`
   equation;
4. the exact `"set"` builtin invokes `dedupCodes`;
5. the exact `"len"`/`setV` branch invokes `isLen`; and
6. fixed `Return`/`#pop` rules restore the caller configuration.

Higher-priority cell and reference alternatives are disabled by the exact
scope/heap shape. Builtin fold routes are name-disjoint from `"len"` and
`"set"`. `lowerC`'s guarded ASCII branch and its `owise` branch are
disjoint and covering. `dedupFrom`'s `codeIn` and negated guards are
complementary. `mapLower`, `codeIn`, `dedupFrom`, `snocCode`, and `isLen`
all descend structurally over finite sequences. No used construct is skipped,
fabricated, or replaced by an oracle.

All 22 opaque symbols concern MD5, floats, or sorting and are absent from the
claim and its dependency path. `MPY-CONCRETE` is not imported by the Haskell
proof definition. The remaining off-path supplied-subset rules cannot be
selected from the target precondition and provide no false target conclusion
witness. No target-reachable unsound rule was found.

The one target-relevant semantic limitation is explicit in supplied
`methods.k:140-156`: `lowerC` changes only ASCII `A`–`Z` and maps one input
integer to one output integer. CPython Unicode lowercasing can use other
mappings and can expand one character to several code points. This rule is
sound as the fixed supplied model's definition, but not a universal model of
CPython `str.lower`.

## 6. Fresh non-vacuity test

I ignored the candidate's `spec-vacuity.k` as proof evidence and created
[audit-false-postcondition.k](evidence/audit-false-postcondition.k). It keeps
the exact program and precondition but changes the required result to:

```text
isLen(dedupCodes(mapLower(CS))) +Int 2
```

This is demonstrably false at the satisfying witness `CS = .IntSeq`: the
program result is 0 and the mutation requires 2. A `kprove --dry-run` build
exited 0, so this is not parser or import failure
([stage6-mutation-build.log](evidence/stage6-mutation-build.log)). The actual
proof exited 1 with `WarnStuckClaimState`, an implication failure, and the
expected residual equality `result + 2 = result`
([stage6-mutation-proof.log](evidence/stage6-mutation-proof.log)). The mutation
is reachable, result-bearing, and rejected for the intended reason.

## 7. Proven versus assumed accounting and decision

What is formally established is precise: under the supplied MPY theory, for
every finite `CS:IntSeq`, the exact submitted function binding and body,
invoked from the pinned pristine state, reaches
`isLen(dedupCodes(mapLower(CS)))` while restoring/preserving the other shown
cells. This is a partial-correctness result; it is not a separate liveness,
complexity, or full-CPython-semantics theorem.

The trust ledger is:

| Boundary | Influence and status | Evidence |
|---|---|---|
| Supplied MPY semantics | Defines all value, control, state, and result behavior. Acceptable as the required fixed model; its Unicode lowercase gap is the sole concern. | Byte-identical trusted tree, exhaustive inventory, clean builds, concrete run, target proof, mutations. |
| `lowerC`/`mapLower` model-to-CPython bridge | Result-bearing model gap. U+0130 gives fixed-model 1 versus CPython 2. It originates in read-only supplied semantics and is explicitly documented by the candidate. | Candidate `PROOF.md:155-162,174-181`; fresh K/Python witness in stage 3 and stage 4 logs. |
| Trusted `py2mpy.py` | Translation boundary from CPython AST to constructors. It affects program identity, not the mathematical postcondition. | Byte-identical regeneration and mechanical constructor comparison. |
| K v7.1.293, Haskell/LLVM backends, SMT, and imported K builtins | Standard machine-checking and ordinary arithmetic/collection trust. | Fresh versioned builds, proof, concrete run, and discriminating failures. |
| 22 supplied opaque symbols | No influence: none is target-reachable or appears in the claim. | Exhaustive dependency inventory. |
| Trusted canonical/CPython behavior | Benchmark ground truth for implementation fidelity. | Textually identical algorithm and 2,077-case independent differential run. |

Gate A passes: fixed semantics executes the real body, state/control are pinned,
the result is constrained, and both body and postcondition mutations fail.
Gate B covers the full unbounded domain represented by the fixed model, with no
candidate-added narrowing. Gate C passes for reproducibility and honest trust
accounting.

Campaign amendment v2 nevertheless requires a concern because the fixed model
cannot represent full CPython Unicode lowercase behavior. All four exception
conditions hold:

1. the restriction is in supplied read-only semantics;
2. the theorem covers every `IntSeq` the model admits and adds no restriction;
3. the candidate trust ledger explicitly records U+0130 as a concrete
   divergence witness; and
4. the submitted Python agrees with canonical/CPython on that witness and all
   tested inputs.

This is therefore legitimate under the campaign's supplied-model-gap
exception, but not an unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
