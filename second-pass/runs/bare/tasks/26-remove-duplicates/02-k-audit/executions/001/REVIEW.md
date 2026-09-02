# Independent adversarial audit: 26-remove-duplicates

The candidate contains a legitimate partial-correctness proof of the exact
submitted translated program. I rebuilt both definitions from source, proved
the iterator claim independently, then proved the entry claim compositionally
with that already-proved claim. The generated semantics is narrow, but every
construct reached by this program is modeled soundly. The output is constrained
to a recursively defined stable unique-occurrence filter; it is neither free
nor supplied by an execution-bypassing oracle.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`, and the mount satisfies its required
boundary: `/reference/reference-semantics` is absent. There is therefore no
infrastructure-mode contradiction and no hidden/supplied semantics was used.

All trusted inputs and all required candidate source/provenance artifacts are
regular files, not symlinks. No required artifact is missing or mistyped. The
candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
`/reference/prompt.py` and `/reference/py2mpy.py`:

| Artifact pair | SHA-256 / result |
|---|---|
| prompt | `7823eea9be9599563c786fa16e792f3da2482016607d75ee06ca40b2d33c7dca`, identical |
| translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`, identical |

The complete type, symlink, root-entry, and hash check is in
[`evidence/stage1_integrity.log`](evidence/stage1_integrity.log). The candidate
has two additional generated-cache directories, `semantic-kompiled/` and
`verification-kompiled/`. They are not source artifacts or integrity failures,
but they are untrusted extra evidence; I did not copy or execute either one.
The structured generation trace is present as one regular JSONL file. No
candidate `reference-semantics/` exists, and no extra helper K source file is
present.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace only as candidate claims. They
claim a bare/generated-semantics run, exit 0, and two successful proof stages.
The bounded extraction is preserved in
[`evidence/stage1_untrusted_claims.log`](evidence/stage1_untrusted_claims.log).
None of those claims, nor the candidate's prior compiled definitions, was used
to establish the verdict.

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires:

> For a finite list of integers, remove every value that occurs more than once,
> and retain the surviving values in their original order.

The trusted canonical implementation counts all input occurrences and returns,
in input order, each traversed `n` whose count is at most one. Since every
traversed element occurs at least once, `count(n) <= 1` is equivalent to
`count(n) == 1`.

The candidate implementation is:

```python
return [number for number in numbers if numbers.count(number) == 1]
```

It therefore implements the same result on the intended domain. Its repeated
linear `list.count` calls make it quadratic rather than the canonical linear
`Counter` implementation, but that is not a partial-correctness divergence.

I regenerated the translation from the scratch-copied `solution.py` using the
trusted translator. The regenerated and submitted `solution.mpy` files are
byte-identical, both with SHA-256
`c745517cfe05839db8c2e7141662dd5e1e362a2c688f1a6a1857526d13cd3833`;
see [`evidence/stage2_translate.log`](evidence/stage2_translate.log).

The independent differential test imports the trusted canonical entry point
and scratch-copied candidate entry point by file path. Its documented input
scope is:

- 12 fixed examples and boundaries, including empty, singleton, exactly two
  occurrences, more than two occurrences, interleaving, negatives, large
  integers, high multiplicity, and all-unique input;
- all 19,531 lists of lengths 0 through 6 over `{-2,-1,0,1,2}`;
- 2,000 deterministic generated lists of lengths 0 through 30 over `[-9,9]`.

All 21,543 comparisons agreed, with zero mismatches. The executable and result
are [`evidence/differential_test.py`](evidence/differential_test.py) and
[`evidence/stage2_differential.log`](evidence/stage2_differential.log).
This is finite fidelity evidence, not a substitute for the K proof.

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

I copied only `semantic.k`, `verification.k`, `spec.k`, `solution.py`,
`solution.mpy`, and `prove.sh` into `/tmp/audit-work/candidate-src`. All
reviewer builds went under `/tmp/audit-work/build`; no candidate-provided
compiled definition or cache was copied. The scratch hashes and layout are in
[`evidence/scratch_manifest.log`](evidence/scratch_manifest.log).

The live toolchain was K v7.1.293 and Python 3.10.12
([`evidence/toolchain_versions.log`](evidence/toolchain_versions.log)).
Fresh Haskell definitions built successfully:

| Definition | Exact build evidence | Exit |
|---|---|---:|
| concrete `MPY` from `semantic.k` | [`stage3_kompile_semantic.log`](evidence/stage3_kompile_semantic.log) | 0 |
| proof `VERIFICATION` from `verification.k` | [`stage3_kompile_verification.log`](evidence/stage3_kompile_verification.log) | 0 |

Fresh concrete execution reached `.K` with these outputs:

| Input | K output | Python/canonical output |
|---|---|---|
| `[]` | `[]` | `[]` |
| `[0]` | `[0]` | `[0]` |
| `[0,0]` | `[]` | `[]` |
| `[0,0,0]` | `[]` | `[]` |
| `[1,2,3,2,4]` | `[1,3,4]` | `[1,3,4]` |
| `[-1,0,-1,2]` | `[0,2]` | `[0,2]` |
| `[1,2,3,1,4,2,5]` | `[3,4,5]` | `[3,4,5]` |

The representative K logs are
[`stage3_krun_example.log`](evidence/stage3_krun_example.log),
[`stage3_krun_empty.log`](evidence/stage3_krun_empty.log),
[`stage3_krun_singleton.log`](evidence/stage3_krun_singleton.log),
[`stage3_krun_thrice.log`](evidence/stage3_krun_thrice.log),
[`stage3_krun_negative.log`](evidence/stage3_krun_negative.log), and
[`stage3_krun_order.log`](evidence/stage3_krun_order.log); the corresponding
independent ground comparisons are in
[`evidence/stage4_ground_substitution.log`](evidence/stage4_ground_substitution.log).
One parallel `[0,0]` execution encountered a transient Java-version detection
failure (`stage3_krun_twice.log`, exit 2) while six sibling processes ran
normally. The exact sequential rerun
[`stage3_krun_twice_rerun.log`](evidence/stage3_krun_twice_rerun.log) reached
`.K`, returned `[]`, and exited 0. This isolated, nonsemantic process-launch
failure is not candidate evidence.

Every positive claim was then run:

| Obligation | Command shape | Result |
|---|---|---|
| `walk-correct` alone | `kprove ... --claims walk-correct` | `#Top`, exit 0 |
| `program-correct` with the proved iterator claim loaded and trusted | `kprove ... --trusted walk-correct` | `#Top`, exit 0 |

The exact outputs are
[`evidence/stage3_kprove_walk.log`](evidence/stage3_kprove_walk.log) and
[`evidence/stage3_kprove_program_composed.log`](evidence/stage3_kprove_program_composed.log).
Trusting `walk-correct` in the second run is legitimate composition because the
same source claim closed independently in the first run.

For diagnostics, I also tried
`--claims program-correct --trusted walk-correct`. It failed with the expected
recursive `walkComp` residual because `--claims` removed `walk-correct` from
the loaded claim set before it could be trusted; see
[`evidence/stage3_kprove_program.log`](evidence/stage3_kprove_program.log).
That diagnostic is not the compositional positive command and does not
contradict its `#Top`.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claim meanings

`walk-correct` has no explicit `requires` clause. Its effective precondition is
any finite integer-list `INPUT`, any finite original integer list `ORIGINAL`,
any current output suffix, and any continuation `KREST`, with the exact
submitted predicate environment at the front of `<k>`. Its postcondition
consumes only the iterator, preserves `KREST`, and changes the output from
`SUFFIX` to:

```text
removeRepeatedOnto(INPUT, ORIGINAL, SUFFIX)
```

That function stably prefixes precisely those values from `INPUT` whose count
in `ORIGINAL` equals one.

`program-correct` also has no explicit `requires` clause. Its effective
precondition is the generated initial configuration with:

- the exact submitted module AST in `<k>`;
- `<input> listValue(INPUT) </input>` for an arbitrary finite K integer list;
- no registered function, an empty environment, and an empty output list.

Its postcondition consumes `<k>`, preserves the input, registers the exact
closure, binds `"numbers"` to the input, and requires:

```text
<output>
  listValue(.Ints) => listValue(removeRepeated(INPUT, INPUT))
</output>
```

The output is therefore result-constraining. `removeRepeated` is not a
right-hand-side fresh variable, existential, tautology, or one-way condition.

### Actual-program identity

The entry claim spells the submitted AST exactly:

```text
Module(
  ImportFrom("typing","List")
  FuncDef("remove_duplicates",
    Params("numbers"), CellVars("numbers"), FreeVars(.Strings),
    Return(ListComp(Name("number"),
      CompFor(Name("number"), Name("numbers"),
        Compare(
          Call(Attribute(Name("numbers"),"count"), Name("number")),
          CmpOp("==",Int(1))))))))
```

This is the structure of the byte-verified `solution.mpy`. It executes through
module scanning, closure registration, entry binding, return, and explicit
`walkComp` transitions. The helper claim starts at the recurring control state
created by the real cons iterator rule and uses the real predicate, captured
original list, generator binding, output accumulator, and continuation.

Satisfying states are concrete and abundant. Examples include the generated
initial configuration with `INPUT = .Ints`, and the iterator configuration for
`INPUT = 1,.Ints`, `ORIGINAL = 1,.Ints`, empty output, and any continuation.
The empty and singleton concrete runs exhibit them.

Ground substitution into the formal postcondition gives:

| Input | `removeRepeated(INPUT,INPUT)` | Canonical | Candidate |
|---|---|---|---|
| `[]` | `[]` | `[]` | `[]` |
| `[0]` | `[0]` | `[0]` | `[0]` |
| `[0,0]` | `[]` | `[]` | `[]` |
| `[1,2,3,2,4]` | `[1,3,4]` | `[1,3,4]` | `[1,3,4]` |
| `[-1,0,-1,2]` | `[0,2]` | `[0,2]` | `[0,2]` |

The complete executable substitution record is
[`evidence/ground_substitution.py`](evidence/ground_substitution.py) with
[`evidence/stage4_ground_substitution.log`](evidence/stage4_ground_substitution.log).

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`evidence/rule_inventory.md`](evidence/rule_inventory.md). It enumerates and
decides all 29 local syntax declarations, all configuration cells, all 29
semantic rules, all three verification equations, all ten `[function]`
symbols, both claims, and the complete construct-to-rule map.

There are no `[total]` or `[functional]` declarations, priority rules,
simplification rules, macros, aliases, or proof-local ordinary operational
rules. No symbol is wholly opaque. The only deliberately nonground-neutral
symbol is `count`: its three equations carry `[concrete]`, so symbolic calls can
remain unreduced, but empty/equal-head/unequal-head equations are disjoint,
strictly descending, mathematically correct, and exhaustive for every finite
ground integer list.

The rule groups and conclusions are:

| Rules | Role | Decision |
|---|---|---|
| S1-S4 | module scan/import | Correct for the exact module; erasing `typing.List` has no runtime effect after annotations are translated away. |
| S5-S7 | closure registration/entry binding | Correct for the sole exact function and explicit input harness. |
| S8-S11 | return and explicit comprehension control | Correct control and state footprint. Tail-first iteration followed by head-prefix emission preserves result order. |
| S12-S13 | Boolean conditional list construction | True, disjoint equations. |
| S14-S19 | literals, lookup, count call, equality, pure comprehension evaluator | Correct on all expression shapes reached by the program; lookup hit/miss guards are disjoint. |
| S20-S22 | value projections | Correct partial projections on their matched domains; no false totality claim. |
| S23-S25 | integer-list count | Correct, disjoint, descending, and ground-exhaustive. |
| S26-S29 | pure `collect`/`prependIf` | Correct stable comprehension equations; the special return path uses `walkComp`, so these are not an execution shortcut in the entry proof. |
| V1-V3 | `removeRepeated` specification | Correct stable filter by count in the original input; base/cons patterns are disjoint and recursion descends. |

The translator AST's `Module`, import, five-field function definition, return,
list comprehension, generator, names, attribute call, equality comparison, and
integer literal all map to a declared syntax constructor and a reached rule
path. Configuration, evaluation order, closure binding, input preservation,
output updates, and continuation behavior are covered. The semantics does not
claim general Python coverage; missing exceptions, mutation, arbitrary calls,
multiple definitions, and side effects are unused constructs and not defects
under the generated-semantics boundary.

One modeling choice warrants explicit review: S10 processes the tail before it
emits the current head, whereas CPython evaluates a comprehension left to
right. In this exact program all reordered computations are total, pure reads
of an immutable finite integer list. The tail-first schedule plus head-prefix
output therefore has the same result and no different modeled side effect or
control behavior. It would not be adequate for a side-effecting predicate, but
no such construct is submitted.

### Extension and sensitivity checks

`walk-correct` is a derived reachability lemma, not an unproved result oracle.
Its complete match domain includes the exact predicate/environment, arbitrary
finite iterator/original lists, arbitrary output suffix, and arbitrary
continuation. It was proved at that same generality. Both fixed execution and
trusted-lemma composition close for an observable continuation that emits
`99`; both produce `[99,1]`. This detects continuation discard or unwinding:

- [`evidence/spec-context.k`](evidence/spec-context.k)
- [`evidence/stage5_context_fixed.log`](evidence/stage5_context_fixed.log)
- [`evidence/stage5_context_composed.log`](evidence/stage5_context_composed.log)

Ground value sensitivity also rejects the opposite interpretations of the
result-bearing `count` operation. A singleton forced to be dropped gets stuck
with actual output `[7]`; a duplicated value forced to be kept gets stuck with
actual output `[]`:

- [`evidence/spec-count-opposite.k`](evidence/spec-count-opposite.k)
- [`evidence/stage5_count_singleton_opposite.log`](evidence/stage5_count_singleton_opposite.log)
- [`evidence/stage5_count_duplicate_opposite.log`](evidence/stage5_count_duplicate_opposite.log)

Finally, changing the submitted predicate from `count == 1` to `count == 2`
changes the trusted-translator AST and changes generated-semantics execution on
the documented input from `[1,3,4]` to `[2,2]`. This shows that execution is
body-sensitive rather than hardcoded to the task answer:

- [`evidence/body_sensitivity_solution.py`](evidence/body_sensitivity_solution.py)
- [`evidence/stage5_body_mutation_translate_check.log`](evidence/stage5_body_mutation_translate_check.log)
- [`evidence/stage5_body_mutation_krun.log`](evidence/stage5_body_mutation_krun.log)

No candidate rule is unsound on a satisfying intended input, so there is no
unsoundness finding requiring a false-conclusion witness. The narrower
limitations above are explicit out-of-scope language coverage, not mechanisms
that enable a false theorem for this program.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created a fresh reviewer mutation
without relying on generation evidence. It preserves the exact entry program
and proven iterator lemma but changes the result obligation to require an
additional leading zero:

```text
listValue(.Ints)
  => listValue(0, removeRepeated(INPUT, INPUT))
```

`INPUT = .Ints` is a satisfying witness. The K execution, trusted canonical,
and candidate Python implementation all return `[]`, while the mutation
requires `[0]`.

The mutation is preserved as
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k). Its `kprove --dry-run`
successfully generated the KORE proof command and exited 0
([`evidence/stage6_vacuity_dry_run.log`](evidence/stage6_vacuity_dry_run.log)).
The actual proof exited 1 with `WarnStuckClaimState`; the residual is the
expected unmet implication:

```text
0 , removeRepeatedOnto(INPUT, INPUT, .Ints)
  == removeRepeatedOnto(INPUT, INPUT, .Ints)
```

See
[`evidence/stage6_vacuity_failure.log`](evidence/stage6_vacuity_failure.log).
This is a reachable result mismatch, not a parser error, missing import,
timeout, or unrelated crash.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the rebuilt K definition, for every finite K list of mathematical
integers used as `INPUT`, execution from the generated initial configuration
containing the exact submitted `solution.mpy` AST reaches an empty `<k>` cell,
preserves the input, registers and enters the submitted closure with the
correct binding, and leaves:

```text
<output> listValue(removeRepeated(INPUT, INPUT)) </output>
```

The recursive specification retains each input element exactly when its count
in the original input is one and otherwise omits it, preserving relative
order. This is a partial-correctness statement for the requested entry point,
not a proof about arbitrary Python programs.

### Trust ledger

| Boundary | Dependents | Status and evidence |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell backend, and reachability logic | All machine-checked results | Standard proof-tool trust boundary; versions and fresh builds recorded. |
| Imported K `INT`, `BOOL`, and `STRING` built-ins, including integer equality/addition and finite-list constructors | Count, comparison, syntax, and every result | Acceptable low-level mathematical/runtime boundary. No candidate rule overrides these operations. |
| Trusted mounted `py2mpy.py` as the lowering from `solution.py` | Real-source-to-AST pinning | Explicitly trusted by the audit setup; byte-identity regeneration proves the submitted AST is its output. |
| Generated module/entry harness and the narrow Python-subset rules S1-S29 | Connection from AST execution to Python behavior | Audited rule by rule, concretely exercised at normal/boundary inputs, continuation-tested, and body-sensitive. Scope excludes unused Python features. |
| `count` on symbolic lists | Predicate and formal result | Not an unconstrained oracle. It is neutral only until lists are ground/split; S23-S25 exhaustively and truthfully fix every finite ground intended input. Distinct ground outcomes and their opposites were tested. |
| `removeRepeated`/`removeRepeatedOnto` | Entry postcondition | Definitional mathematical summary, not an execution bridge. V1-V3 are disjoint, descending, ground-exhaustive equations for the natural stable filter. |
| `walk-correct` trusted during entry composition | Closure of `program-correct` | Acceptable derived lemma because the exact claim independently printed `#Top`; context/state scope is no broader than its proved statement. |
| Natural-language meaning of the recursive postcondition | Human-facing task conclusion | Direct structural-induction argument: base returns the suffix; each cons keeps the head iff its original count is one and recursively preserves tail order. Supported, but not replaced, by 21,543 differential cases and explicit ground reductions. |

There is no fresh opaque program-derived value, empirical bridge substituted
for a universal K execution claim, proof-local operational shortcut, or rule
that fabricates the requested answer. Finite differential evidence is used
only to support the trusted translator/semantics-to-CPython adequacy bridge; it
is not cited as the formal proof.

Gate A (real-program soundness): **PASS**.  
Gate B (intent adequacy): **PASS**.  
Gate C (trust and auditability): **PASS**.

The narrow generated semantics is adequate for every construct the submitted
program uses, and its explicitly excluded general-Python behaviors create no
material gap on the intended list-of-integers domain.

VERDICT: PASS
LEGITIMACY: LEGIT
