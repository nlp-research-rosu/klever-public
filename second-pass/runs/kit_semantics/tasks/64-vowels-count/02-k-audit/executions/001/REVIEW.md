# Independent adversarial review: HumanEval/64 `vowels_count`

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I did not reuse any candidate
kompiled directory or accept candidate prose, traces, or prior `#Top` output as
proof. All executable checks used source copied to
`/tmp/audit-work/reconstruction`; reviewer-authored artifacts and bounded logs
are under [`evidence/`](/audit-output/evidence).

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`problem_id = 64-vowels-count`, and
`semantics_mode = SUPPLIED_SEMANTICS`. The mode is consistent with the
presence of `/reference/reference-semantics`.

I read and checked all required pipeline-v3 records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the JSONL structured trace below
  `/generation-evidence/codex-trace/`.

The full large-record scan covered 1,932,906 bytes / 62,187 lines of
`codex-output.log` and all 632 valid JSON trace records. These records claimed
successful generation, but I used that only as historical context. See
[`generation-record-scan.log`](/audit-output/evidence/generation-record-scan.log).

Independent integrity results:

- The campaign block in `/audit-input.json` is structurally identical to
  `/audit-campaign-lock.json`, whose recomputed SHA-256 is the recorded
  `ad5dfcc...d745`.
- Every launcher-recorded single-file SHA-256 recomputed to the recorded value:
  the campaign lock, canonical, prompt, translator, run/task/result/invocation
  manifests, metrics/runtime/usage records, prompt, terminal output, and each
  declared trace file.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- A recursive, type-aware, per-entry SHA-256 manifest of
  `/candidate/reference-semantics` is identical to the independently generated
  manifest of `/reference/reference-semantics`. There are no missing,
  additional, changed, mistyped, special, or symlinked entries. This also
  independently checks the content represented by the launcher's aggregate
  tree-hash claims without relying on its private tree-serialization format.
- All required candidate proof artifacts are regular files, and no symlink was
  found anywhere under the candidate semantics tree.

The complete check and all recomputed hashes are in
[`integrity-check.log`](/audit-output/evidence/integrity-check.log), generated
by [`integrity_check.py`](/audit-output/evidence/integrity_check.py). There is
no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for the number of ordinary vowels `a/e/i/o/u` in a
word, with terminal `y` also counted. Although the prose lists lowercase
letters, the required example `"ACEDY" -> 3` establishes case-insensitive
ordinary vowels and terminal `Y`.

The trusted canonical computes membership in `"aeiouAEIOU"` over the full
string and then inspects the final character for `y/Y`. The submitted
implementation uses a loop, accumulates the same membership Boolean, remembers
the last character, and then adds the two mutually exclusive `last == "y"` and
`last == "Y"` bits.

### Translation identity

Running the trusted `/reference/py2mpy.py` against the scratch copy of
`solution.py` produced a file byte-identical to submitted `solution.mpy`; both
MPY files have SHA-256
`15b4504912d6edf0e463ce0d876a63e10251fb85ee7e8473bb3e1c27fe394200`.
See
[`translator-regeneration.log`](/audit-output/evidence/translator-regeneration.log).

### Independent differential test

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted canonical and submitted implementation through independent,
explicit module paths. It checked:

- both documented examples;
- one-character vowel/non-vowel/`y`/`Y` boundaries;
- terminal versus internal `y/Y`;
- all-vowel and no-vowel strings, punctuation, digits, and representative
  non-ASCII characters;
- all 2,954 nonempty strings of length 1 through 3 over a 14-character branch
  alphabet; and
- 10,000 deterministic generated strings of lengths 1 through 64 over a
  broader alphabet.

All 12,975 nonempty inputs matched. The exact input-generation scope, seed,
command, output, and exit `0` are in
[`differential-test.log`](/audit-output/evidence/differential-test.log).

For the explicitly tested empty boundary, canonical raises `IndexError` while
the submitted implementation returns `0`. This does not narrow the prompt's
domain: “word” supports the canonical's nonempty precondition, while if empty
text is admitted, zero is the mathematically correct vowel count. The
candidate proof covers empty input in addition to every nonempty semantic
string.

## 3. Clean proof reconstruction

I copied only source artifacts to scratch. Candidate
`runtime-kompiled`, `connection-kompiled`, `verification-kompiled`,
`__pycache__`, and other generated caches were neither copied nor used.

The independently observed toolchain is K v7.1.293 and Python 3.10.12
([`toolchain-versions.log`](/audit-output/evidence/toolchain-versions.log)).

Fresh builds:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

This exited `0`; see
[`kompile-llvm.log`](/audit-output/evidence/kompile-llvm.log). Its
non-exhaustiveness warnings concern fixed helpers `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and out-of-bounds `valSeqAt`, none reachable from this
program.

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

This exited `0`; see
[`kompile-haskell-verification.log`](/audit-output/evidence/kompile-haskell-verification.log).

A fresh concrete probe containing the exact function body and 12 assertions
translated with the trusted translator and ran to `<k> .K </k>`,
`NoExc`, exit code `0`. It includes empty input, both examples, all
single-character branches, internal/final `y`, all uppercase vowels, and a
digit suffix case. See
[`concrete_probe.py`](/audit-output/evidence/concrete_probe.py),
[`concrete-probe-translate.log`](/audit-output/evidence/concrete-probe-translate.log),
and [`krun-concrete-probe.log`](/audit-output/evidence/krun-concrete-probe.log).

Every positive target claim closed under the fresh Haskell definition:

- `kprove ... --claims SPEC.loop-inv` printed `#Top` and exited `0`
  ([`kprove-loop-inv.log`](/audit-output/evidence/kprove-loop-inv.log)).
- `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC`
  proved the complete two-claim specification, printed `#Top`, and exited `0`
  ([`kprove-full-spec.log`](/audit-output/evidence/kprove-full-spec.log)).

For transparency, I also tried selecting only `SPEC.vowels-count`. That
selection removes its `SPEC.loop-inv` circularity from the proof
specification, causing unbounded symbolic loop unrolling; I interrupted that
non-target diagnostic with status 130. It is recorded separately in
[`kprove-vowels-count.log`](/audit-output/evidence/kprove-vowels-count.log)
and has no bearing on the successful complete-spec proof.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`SPEC.loop-inv` starts at the actual `#loop` over remaining string codes `CS`
inside the real function call. The callee has arbitrary integer accumulator
`COUNT`, remembered code sequence `LAST`, current `char`, original `s`,
arbitrary caller continuation and remaining stack, and explicitly framed
heap/return/exception/exit cells. Its continuation is exactly the two final
`y/Y` augmentations, the actual return, and `#endcall`. It reaches
`COUNT + vowelsTail(CS,LAST)`, restores the caller, removes the callee scope
and frame, and preserves all framed state.

`SPEC.vowels-count` has no side condition on `INPUT:IntSeq`. It starts from
the MPY initial configuration, loads the submitted function definition, calls
it with `str(INPUT)`, and reaches the exact integer
`vowelsTail(INPUT,.IntSeq)`. It pins the final module closure, empty
heap/stack, restored environment and scope allocation, `noRet`, `NoExc`, and
exit code zero.

### Mechanical program pinning

[`program_pinning.py`](/audit-output/evidence/program_pinning.py) mechanically
extracts the `Module(...)` below the entry claim's `#loadAll`, parses both it
and submitted `solution.mpy` with the fresh definition, and compares normalized
KORE constructor trees. The only normalization removes explicit `.Stmts`
terminators required in rule syntax but inserted implicitly by the MPY program
list parser. Both normalized terms are 4,550 bytes and byte-identical. See
[`program-pinning.log`](/audit-output/evidence/program-pinning.log).

Thus the entry theorem executes the same binding, parameters, body, literals,
loop, and return as trusted-regenerated `solution.mpy`; it is not a
substituted program or external oracle.

### Satisfying witnesses and result constraint

The entry precondition is satisfiable with:

```text
INPUT = iCons(97,iCons(98,iCons(99,iCons(100,iCons(101,.IntSeq)))))
env=0
scopes=0|->scope(.Map,parent(-1)) -1|->builtinsScope
scopeLoc=1 heap=.Map heapLoc=0 stack=.List
ret=noRet exc=NoExc exit=0
```

This is `"abcde"`, and the claimed term, trusted canonical, and submitted
Python function all equal `2`.

A reachable loop witness after consuming `"a"` has `COUNT=1`,
`CS="bcde"`, `LAST="a"`, `CHAR="a"`, callee environment 1,
`scopeLoc=2`, and the corresponding caller frame. The loop postcondition and
both Python functions again equal `2`. A second ground substitution,
`"ACEDY"`, equals `3` in all three interpretations. Exact constructor terms
and cell values are in
[`claim-witnesses.log`](/audit-output/evidence/claim-witnesses.log).

The RHS is not a free variable, tautology, or one-way implication:
`vowelsTail` is constructor-defined to a unique integer.

## 5. Rule-by-rule static soundness review

[`rule-inventory.md`](/audit-output/evidence/rule-inventory.md) inventories
every top-level item in the supplied `semantics.k`, all supplied helper K
files, `verification.k`, and `spec.k`:

```text
933 total
697 ordinary semantic/proof rules
228 syntax declarations
5 contexts
1 configuration
2 reachability claims
```

It separately flags every `function`, `total`, `[concrete]`,
`[no-evaluators]`, `owise`, priority, strictness, and macro attribute. There
are no explicit `functional` or simplification declarations. Each row states
whether it is in the target dependency cone and gives its rule-level decision.
The generating reviewer script and counts are
[`make_rule_inventory.py`](/audit-output/evidence/make_rule_inventory.py) and
[`rule-inventory-generation.log`](/audit-output/evidence/rule-inventory-generation.log).

The constructor-to-rule map in
[`used-rule-map.md`](/audit-output/evidence/used-rule-map.md) covers module
loading, syntax heating/cooling, function definition, lookup, call and
argument order, frame allocation and cleanup, assignment, iteration and
target binding, string literals/iteration/membership/equality, Boolean-to-int
addition, return, and every proof-local item.

### Proof-local inventory and decision

`verification.k` adds exactly:

1. `vowelsTail(IntSeq,IntSeq) [function,total]`;
2. a base equation for `.IntSeq`; and
3. a step equation for `iCons(C,REST)`.

This is a definitional summary, not an operational bridge. The equations are
constructor-disjoint and exhaustive in the recursive argument. The step
strictly descends to `REST`. The base adds one exactly for remembered `y` or
`Y`; these equalities cannot both hold. The step uses the fixed, truthful
one-character `strContains` predicate over the exact ten-character vowel
literal. No fresh or opaque result is admitted, and no rule bypasses a
program term.

`SPEC.loop-inv` is a machine-checked connection theorem over its full match
domain. It has the actual body and exact post-loop/return continuation,
quantifies over the caller continuation it preserves, and explicitly accounts
for every live cell. It executes fixed semantics; it is not installed as a
broader priority rewrite. `SPEC.vowels-count` then uses that circularity to
prove the exact entry execution.

### Fixed-rule overlaps, state, and opaque boundaries

- Relevant priority alternatives for closure cells and heap references have
  concrete guards that are false for this unannotated function's integer and
  string locals and empty heap. Ordinary assignment/lookup/call rules
  therefore apply without ambiguous state effects.
- Callee and argument evaluation is left-to-right; `s` is iterated once; each
  iteration binds `char`, updates `count`, then assigns `last`; return performs
  the exact abrupt-control and frame-pop transition.
- The proof-local theory adds no priority rule, simplification, `owise`,
  opaque symbol, `[concrete]` equation, or unproved primitive.
- The fixed supplied theory has 22 `no-evaluators` symbols and 35
  concrete-only equations, but constructor reachability places every one
  outside these claims. The six LLVM totality warnings are likewise outside
  the dependency cone.
- The supplied ASCII literal conversion is adequate here because every source
  literal is ASCII. Symbolic input is already represented as `str(IntSeq)` and
  is not passed through literal conversion.

No inventoried rule in the dependency cone permits a false conclusion on the
intended string domain. Therefore this review makes no unsound-rule
allegation and no false-witness obligation arises.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation
[`spec-false-result-audit.k`](/audit-output/evidence/spec-false-result-audit.k)
loads the exact submitted program and calls it on the satisfiable input
`"abcde"`, but changes the result obligation from `2` to the false value `3`.

- A `kprove --dry-run` parsed and built the mutation successfully with exit
  `0`; see
  [`kprove-fresh-false-result-dry-run.log`](/audit-output/evidence/kprove-fresh-false-result-dry-run.log).
- The live proof reached `<k> 2 ~> .K </k>`, emitted
  `WarnStuckClaimState`, and exited `1` because it could not meet `3`; see
  [`kprove-fresh-false-result.log`](/audit-output/evidence/kprove-fresh-false-result.log).

This is the expected unmet result obligation, not a parser failure, timeout,
unreachable mutation, or unrelated crash.

As the separate operational-sensitivity check required by the Kit validation
workflow, I changed the body literal from `"aeiouAEIOU"` to
`"aeioAEIOU"` and executed that mutated closure on `"u"` while retaining
the original obligation `1`. The proof reached result `0`, emitted
`WarnStuckClaimState`, and exited `1`. See
[`spec-body-sensitivity-audit.k`](/audit-output/evidence/spec-body-sensitivity-audit.k)
and
[`kprove-body-sensitivity.log`](/audit-output/evidence/kprove-body-sensitivity.log).
The theorem is therefore sensitive to the body actually executed.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the exact supplied MPY theory, for every finite `INPUT:IntSeq`, starting
from the pinned initial cells and executing trusted-regenerated
`solution.mpy`, if the modeled execution terminates, the returned integer is:

```text
number of codes in INPUT equal to a/e/i/o/u/A/E/I/O/U
+ 1 exactly when the final code is y or Y.
```

The proof includes module loading, binding selection, argument binding,
statement/evaluation order, every loop iteration through a universal
circularity, local state updates, return, stack/frame cleanup, and the pinned
final observable cells.

### Trust ledger

| Boundary | Effect and dependents | Decision |
|---|---|---|
| Supplied MPY semantics | Defines all value, control, scope, stack, heap, and exception behavior used by both claims. | Acceptable fixed language boundary. Candidate copy is recursively identical to the trusted mount; target rules were statically audited and concretely exercised. |
| K v7.1.293, Haskell/LLVM backends, builtin K theories | Compiles and checks the equations and reachability claims. | Standard unavoidable proof-tool trust boundary; fresh builds and independent positive/negative runs behaved discriminatingly. |
| Trusted `py2mpy.py` | Bridges submitted Python AST to MPY constructors. | Accepted launcher-designated translator; fresh output is byte-identical, and the entry claim is mechanically constructor-identical to it. |
| CPython and trusted canonical | Differential adequacy oracle on finite test inputs. | Empirical support only, not used to close the K theorem. It found zero nonempty mismatches and exposed the documented empty-boundary difference. |
| Human-language interpretation of `vowelsTail` | Connects the recursively defined integer to “vowel count.” | Ordinary structural mathematics: exhaustive disjoint equations add exactly one per named vowel and one for final `y/Y`. No empirical or opaque oracle is substituted. |
| Arbitrary `IntSeq` codes | Formal domain includes values that are not Unicode scalar values. | Harmless over-approximation, not narrowing. Only the named ASCII codes contribute. |

There are no candidate-added trusted primitives, opaque symbols, empirical
bridges used as proof rules, operational shortcuts, or informal binding/control
assumptions. The finite differential and concrete tests support only
implementation/semantics adequacy; the successful K proof supplies the
universal program-execution result.

The empty-string behavior is an implementation/canonical boundary observation,
not a material source-contract gap: the canonical presupposes a nonempty
“word,” the submitted program returns the natural count `0`, and the formal
claim covers rather than excludes that extra case.

VERDICT: PASS
LEGITIMACY: LEGIT
