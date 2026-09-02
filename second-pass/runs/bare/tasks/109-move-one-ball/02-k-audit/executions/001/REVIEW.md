# Independent adversarial audit: 109-move-one-ball

## Decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program. Fresh builds and fresh proofs close,
the claim is pinned to the byte-reproduced translator output, every used
construct has sound semantics, and the task-specific loop acceleration was
independently proved equivalent to generic small-step loop execution.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
related auditability limitations:

1. The candidate placed the main loop summary directly in `semantic.k` and did
   not provide a separate connection theorem. This audit supplied and proved
   that theorem against a version of the semantics with the summary removed,
   so the gap does not remain a soundness defect.
2. `rotationSortable` transparently means “the number of strict cyclic
   descents is at most one.” Its equivalence to the prompt’s existential
   sorted-right-rotation property for unique lists is correct ordinary
   mathematics and is strongly supported by the trusted-canonical
   differential, but the equivalence is not itself stated and proved as a K
   theorem.

No candidate rule was found to enable a false conclusion on the intended
domain. Accordingly, there is no unsoundness witness to report.

Tool versions and paths are recorded in
`/audit-output/evidence/tool_versions.log`.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as required. There is no
infrastructure contradiction and no hidden/supplied semantics was sought or
used. See `/audit-output/evidence/stage1_integrity.log`.

### Required and untrusted artifacts

The following required candidate artifacts are present as ordinary regular
files:

- provenance/runner evidence: `run-input.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, and one structured JSONL trace under
  `codex-trace/`;
- trusted-input copies: `prompt.py` and `py2mpy.py`;
- source deliverables: `solution.py`, `solution.mpy`, `mpy-syntax.k`,
  `semantic.k`, `verification.k`, `spec.k`, and executable `prove.sh`.

No symlink exists anywhere under `/candidate` or `/reference`. No required
source artifact is missing or mistyped. Candidate extras are three compiled
definition trees (`semantic-kompiled`, `semantic-llvm-kompiled`, and
`semantic-haskell-kompiled`) plus `__pycache__`; all were treated as untrusted
build output and ignored.

The candidate prompt is byte-identical to `/reference/prompt.py`:
SHA-256
`e68cbac960bfb695527850d504ec27806e0f41a7711920d0a9e3152369179146`.
The candidate translator is byte-identical to `/reference/py2mpy.py`:
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Both `cmp` commands exited 0.

`run-input.json` identifies problem `109-move-one-ball`, condition `bare`, and
the same trusted prompt/translator hashes. `metrics.json` claims an exit-0,
non-timeout generation. `codex-last.txt`, `codex-output.log`, and the complete
282-record structured trace claim successful concrete runs, `#Top`, and 5,914
Python/oracle cases. These claims were not relied upon. The entire structured
trace and 20,495-line text log were independently streamed and summarized by
`/audit-output/evidence/extract_untrusted_trace.py`; hashes, every recorded tool
command, relevant outputs, and final claims are preserved in
`/audit-output/evidence/untrusted_trace_extract.log`.

Stage result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

From trusted `/reference/prompt.py`: given a finite list of unique integers,
return whether some number (including zero) of cyclic right shifts makes it
non-decreasing; return true for the empty list.

Trusted `/reference/canonical.py` returns true for empty input. Otherwise it
rotates the list so its minimum is first and compares that rotation with
`sorted(arr)`.

Candidate `solution.py` returns true for empty input. For nonempty input it
starts `previous` at the last element, walks the list, counts strict cyclic
descents `previous > value`, and returns whether the count is at most one. For
unique elements, a circular ordering can be cut into increasing order exactly
when it has at most one strict cyclic descent. This is a different but correct
algorithm.

### Trusted translation

The audit ran:

```text
python3 /tmp/audit-work/source/py2mpy.py /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/source/solution.regenerated.mpy
cmp -s /tmp/audit-work/source/solution.mpy \
       /tmp/audit-work/source/solution.regenerated.mpy
```

Both commands exited 0. Both files have SHA-256
`e646b542620bbc9d7ed94850d6eac6b5a9d4b15e6b4d989667fd6e13c35e7e66`.
See `/audit-output/evidence/stage2_translate.log`.

### Independent differential

`/audit-output/evidence/differential_test.py` imports the trusted canonical
entry point directly from `/reference/canonical.py` and the generated entry
point from the scratch copy of `solution.py`. It does not reuse any K equation.
It tests:

- both documented examples;
- empty, singleton, length-two, sorted, rotated, and multiple-descent boundary
  cases;
- negative and arbitrary-precision integers;
- every permutation of `range(n)` for `n = 0..7` (5,914 inputs);
- 500 additional deterministic random distinct-list inputs (seed 109).

All 6,428 comparisons agreed; mismatch count was zero. The exact generated
input specification and all random cases are in
`/audit-output/evidence/differential_inputs.json`; command, explicit results,
scope, and exit 0 are in
`/audit-output/evidence/differential_test.log`.

This is finite evidence for the source-to-intent bridge, not a replacement for
the K proof.

Stage result: **PASS**.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/source`. The trusted
translator replaced the candidate translator copy. No candidate compiled
definition, cache, scanner, interpreter, or KORE file was copied or used.

### Fresh builds

These independently rebuilt definitions all exited 0:

- LLVM candidate semantics:
  `kompile semantic.k --backend llvm --main-module HUMAN-EVAL
  --syntax-module HUMAN-EVAL-SYNTAX --output-definition
  /tmp/audit-work/build/semantic-llvm-kompiled`
  (`/audit-output/evidence/kompile_semantic_llvm.log`);
- Haskell proof definition:
  `kompile semantic.k --backend haskell --main-module HUMAN-EVAL
  --syntax-module HUMAN-EVAL-SYNTAX --output-definition
  /tmp/audit-work/build/proof-haskell-kompiled`
  (`/audit-output/evidence/kompile_proof_haskell.log`);
- LLVM and Haskell generic-loop variants with candidate rule M12 removed
  (`/audit-output/evidence/kompile_semantic_generic_llvm.log` and
  `/audit-output/evidence/kompile_semantic_generic_haskell.log`).

The reviewer-authored generic variant is preserved at
`/audit-output/evidence/semantic-generic.k`.

### Fresh concrete generated-semantics execution

`/audit-output/evidence/concrete_semantics_test.py` compares three executions:
CPython, the rebuilt candidate semantics (with M12), and the rebuilt generic
semantics (without M12). Seventeen final-result/full-state checks cover the
submitted program, an observable continuation that returns
`previous + drops`, and a body mutation that increments by two. Empty,
singleton, both Boolean outcomes, prompt examples, negative integers, and
large integers are included. The final run reports 17 checks, zero mismatches,
and exit 0 in
`/audit-output/evidence/concrete_semantics_test_v2.log`.

An earlier diagnostic in
`/audit-output/evidence/concrete_semantics_test.log` used an unmodeled `<`
operator and became visibly stuck. It was not counted as validation evidence;
the supported `+2` body-sensitivity mutation replaced it.

### Positive target claims

Fresh proof results:

```text
kprove spec.k --definition /tmp/audit-work/build/proof-haskell-kompiled \
  --spec-module HUMAN-EVAL-SPEC
#Top
EXIT_STATUS: 0
```

The full command/output is
`/audit-output/evidence/kprove_all_claims.log`. Each claim was also copied
unchanged into its own labeled module and run independently:

- empty claim: `#Top`, exit 0
  (`/audit-output/evidence/kprove_empty_claim.log`);
- nonempty universal claim: `#Top`, exit 0
  (`/audit-output/evidence/kprove_nonempty_claim_retry.log`).

A first parallel launch of the isolated nonempty proof transiently failed
before K startup because its Java-version probe returned blank
(`/audit-output/evidence/kprove_nonempty_claim.log`). The same artifact
immediately succeeded sequentially; the all-claims proof and the isolated
empty proof also succeeded. This was an audit-host process-launch event, not a
candidate failure.

### Independent loop-bridge reconstruction

Candidate M12 skips the exact loop body and writes a recursive mathematical
summary. To avoid trusting it circularly, the audit:

1. removed M12 while retaining generic rules M13–M14;
2. rebuilt that generic semantics with the Haskell backend;
3. stated two universal reachability claims covering entry maps with and
   without an existing `value` binding;
4. used only two transparent K `Map`-update normalization equations;
5. proved the complete result/control/state transition.

The successful command exited 0 and printed `#Top`; see
`/audit-output/evidence/kprove_loop_connection_v4.log` and the preserved
`/audit-output/evidence/loop-connection-spec.k`. Earlier attempts v1–v3 are
also preserved and show progressively exposed symbolic `Map` normalization
obligations, not an accepted false result.

Stage result: **PASS**.

## 4. Adequacy and real-program pinning

### Claim C1: empty input

Precondition: `<k>` begins with `theSolution`, `<input>` is `.IList`, and
`<env>` is empty.

Postcondition: execution terminates with exactly `bVal(true) ~> .K`; input is
unchanged; the environment is exactly
`"arr" |-> listVal(.IList)`.

This precondition is satisfiable by the explicit initial configuration just
described.

### Claim C2: nonempty input

Precondition: `<k>` begins with `theSolution`, `<input>` is an arbitrary
nonempty integer `IList` `I :: IS`, and `<env>` is empty. There is no hidden
uniqueness assumption; the theorem is stronger than required because it
faithfully characterizes the program for lists with duplicates too.

Postcondition: execution terminates with exactly
`bVal(rotationSortable(I :: IS)) ~> .K`; input is unchanged; the final
environment is fully fixed:

- `arr` retains the input;
- `drops = cyclicDrops(input)`;
- `previous = last(input)`;
- `value = last(input)`.

`rotationSortable` is not a free or opaque variable. V11 reduces it to the
Boolean `cyclicDrops(input) <=Int 1`, and the recursive equations reduce
`cyclicDrops` to the exact strict-descent count. The claim is equivalence-like
and result-constraining, not a tautology or one-way implication.

A satisfying ground state is `I = 3`,
`IS = 4 :: 5 :: 1 :: 2 :: .IList`. Substitutions recorded in
`/audit-output/evidence/ground_claim_witnesses.log` show:

- empty: claimed/canonical/generated are all true;
- `[3,4,5,1,2]`: `cyclicDrops = 1`, all three results true;
- `[2,1,3]`: `cyclicDrops = 2`, all three results false.

### Exact submitted program

`theSolution` has one total zero-arity equation whose right side is the full
constructor tree in submitted `solution.mpy`. Trusted regeneration is
byte-identical. In addition,
`/audit-output/evidence/entry_pinning_test.py` concretely runs both
`solution.mpy` and a program consisting only of `theSolution`; their complete
final configurations are byte-identical for empty, true-nonempty, and
false-nonempty inputs. See
`/audit-output/evidence/entry_pinning_test.log`.

The only loop bridge matches the real loop body constructor-for-constructor.
Its independent connection theorem frames the arbitrary continuation and
preserves every configuration cell and every unrelated environment binding.

Stage result: **PASS**.

## 5. Rule-by-rule static soundness review

The full exhaustive inventory, per-rule decision, attribute inventory,
construct-coverage map, and imported trust boundary are in
`/audit-output/evidence/rule_inventory.md`.

### Inventory totals

- `mpy-syntax.k`: all local source/IR syntax; one zero-arity
  `[function,total]` symbol (`theSolution`) and one equation.
- `semantic.k`: three value constructors, 16 control/evaluation KItems, three
  configuration cells, and 36 operational rules.
- `verification.k`: six mathematical functions and 11 equations. Five
  functions are declared total; `last` is correctly partial.
- `spec.k`: exactly two entry claims and no auxiliary claim.
- Special attributes: one `[priority(40)]` rule (M30), one `[owise]` rule
  (M13), and no local simplification, concrete, opaque, fresh, or
  `[functional]` declarations.

### Construct coverage

Every constructor in `solution.mpy` is declared and has an execution path:
module/function syntax, statement sequencing, `If`, name assignment, `For`,
`Return`, name/int/Boolean evaluation, unary minus, integer addition,
comparisons `==`, `>`, and `<=`, `len`, and subscript `[-1]`. Missing semantics
for other Python constructs is not a defect in this minimal generated mode.

### Material static checks

- **Configuration and state:** all cells have a role. Rules frame `<input>` and
  unrelated `<env>` bindings. Assignment and loop binding use K `Map` update.
- **Evaluation/control:** statements are sequential; expressions used by the
  program evaluate left-to-right; guards choose disjoint branches; return
  discards the remaining function-body continuation, which is correct for the
  only active function and does not cross an unmodeled call frame.
- **Loop rules:** M12 and M13 overlap syntactically, but `[owise]` makes M13 the
  complement. M12 matches the full body, not merely a function name or loose
  suffix. It returns no opaque value and has a machine-checked independent
  connection theorem.
- **Priority:** M30 structurally evaluates `len(E) == 0`. The lower-priority
  generic comparison route computes `length(E) ==Int 0`; both conclusions
  agree for every ground `IList`. The priority resolves symbolic shape, not
  truth.
- **Functions/totality:** `length`, `dropsFrom`, and `cyclicDrops` split on
  empty/cons and structurally descend. `dropBit` guards `>` and `<=` are
  disjoint and exhaustive on integers. `rotationSortable` has one exhaustive
  equation. `last` covers exactly nonempty lists and is reached only after the
  nonempty branch.
- **Binding:** the entry rule is intentionally narrow and treats the sole
  unary module definition as the invoked entry point. The submitted tree has
  exactly that shape and name. Shadowing of textual `len`, calls, exceptions,
  general indexing, and multi-function modules are outside the modeled
  program and cannot affect this claim.
- **No oracle:** all result-bearing functions are transparent and recursive.
  No fresh value, uninterpreted Boolean, external result, or task-answer axiom
  remains.

V11 defines the formal predicate rather than formalizing rotations and
sortedness. For a unique list, cutting a circle into an increasing linear list
is possible iff the circle has at most one strict descent; uniqueness also
makes “strictly increasing” and the prompt’s “non-decreasing” coincide. This
ordinary argument is correct, but its absence as a K theorem is the principal
documented concern.

No rule was labeled unsound, because no concrete or symbolic false-conclusion
witness exists on the intended domain. The initial unmodeled-`<` stuck run is
a coverage boundary for an unused construct, not a false conclusion.

Stage result: **PASS**, with the documented formal-intent limitation.

## 6. Fresh non-vacuity test

The candidate did not supply a `spec-vacuity.k`; the audit created
`/audit-output/evidence/spec-vacuity.k`. It keeps the original satisfiable
nonempty precondition and exact final environment but changes the returned
Boolean to the negation of `rotationSortable`.

The mutation is demonstrably false at, for example,
`[3,4,5,1,2]`: the actual and original claimed result is true, while the
mutated result is false.

Build-only command:

```text
kprove /audit-output/evidence/spec-vacuity.k \
  --definition /tmp/audit-work/build/proof-haskell-kompiled \
  --spec-module SPEC-VACUITY -I /tmp/audit-work/source --dry-run
EXIT_STATUS: 0
```

See `/audit-output/evidence/vacuity_build.log`.

The actual proof exited 1 with `WarnStuckClaimState`. The residual reaches the
real final `bVal(cyclicDrops <=Int 1)` and fails the implication requiring it
to equal `notBool(cyclicDrops <=Int 1)`. This is the expected reachable unmet
result obligation, not a parse error, missing import, timeout, or unrelated
crash. See `/audit-output/evidence/vacuity_proof.log`.

Stage result: **PASS**.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the rebuilt generated semantics and K standard library:

1. From the empty initial configuration, the exact submitted translated
   program terminates with Boolean true and the claimed final environment.
2. From every nonempty finite `IList` of K integers, the exact submitted
   translated program terminates with Boolean
   `cyclicDrops(input) <=Int 1`, and its `arr`, `drops`, `previous`, and `value`
   bindings have the exact claimed final values.
3. The task-specific loop fold used in that proof is reachability-equivalent,
   over its complete matched state/context domain, to generic small-step
   execution of the actual loop body.

This is a partial-correctness theorem. The modeled list iteration is
structurally finite, and concrete executions terminate, but the status is not
inflated into a separate total-correctness theorem.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K v7.1.293 parser, kompiler, Haskell/LLVM backends, reachability logic, and circularity mechanism | all builds/proofs | Necessary toolchain trust; acceptable and independently rebuilt from source. |
| K `INT` and `BOOL` hooks | arithmetic, comparisons, `dropBit`, result | Acceptable primitive boundary. K arbitrary-precision integers align with Python integers for all used operations. |
| K `MAP` lookup/update/AC matching and sequencing `~>` | environment and control | Acceptable primitive boundary. The loop connection proof used two transparent map-update normalization equations: inserting a fresh key and replacing an existing explicit key. They are ordinary Map identities and do not encode any task result. |
| Trusted `/reference/py2mpy.py` | program identity | Trusted by the audit problem. Regeneration is byte-identical. |
| Generated minimal Python model | source-to-K execution | Audited rule-by-rule and concretely against Python. It intentionally excludes unused Python behavior; used constructs are covered without fabricated fallbacks. |
| Candidate M12 loop fold | universal nonempty claim | Initially concerning because embedded in semantics. Independently connected with `#Top` to generic execution without M12, plus continuation/body-sensitivity concrete checks; acceptable after validation. |
| `rotationSortable(L) = cyclicDrops(L) <= 1` as a transparent definition | formal postcondition | Fully fixed inside K; no opacity. |
| Equivalence of at-most-one cyclic descent to existence of a sorted right rotation for unique inputs | natural-language intent | Correct informal mathematical bridge and empirically supported by zero mismatches against the trusted canonical on 6,428 inputs. Not itself formalized as a K theorem; this is the surviving concern. |
| Trusted `/reference/canonical.py` | differential oracle | Trusted input and independently implemented relative to K equations. Finite tests support, but do not universally prove, the bridge. |

### Gate summary

- Real-program soundness: **PASS**.
- Intent adequacy: **PASS WITH CONCERN** — correct bridge, but not formalized
  inside K.
- Trust/evidence auditability: **PASS** — all commands, statuses, bounded logs,
  mutations, inputs, and reviewer artifacts are preserved below
  `/audit-output/evidence/`.

The proof is therefore legitimate and pins the real generated program, but
the unformalized final intent bridge warrants `CONCERNS` under the requested
decision boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
