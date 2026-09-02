# Independent adversarial audit: 109-move-one-ball

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied semantics. I independently reconstructed both K
definitions, proved the loop claim and the complete specification from source,
checked constructor-level program identity, reviewed the full rule inventory,
and rejected fresh body and result mutations for the expected semantic reasons.
I did not rely on the candidate's compiled definitions, logs, `#Top` text, or
`PROOF.md`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem `109-move-one-ball`, and
condition `kit-semantics`. The trusted `/reference/reference-semantics` mount is
present, as this mode requires.

I inspected all pipeline-v3 records required by the prompt:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the sole structured trace
  `codex-trace/2026/07/25/rollout-2026-07-25T01-54-31-019f980d-d50d-7c42-9721-224995fefc44.jsonl`.

All are readable regular files, not symlinks. The trace contains 576 valid JSON
lines and no parse errors. Its direct SHA-256 is
`addced4fbc7c0c1f85778f7b078c8a0d869890cc6921c0e400389905a9f82c22`,
which matches the stage-1 record. The other directly recorded hashes all match,
including the run, task, invocation, generation result, metrics, usage,
runtime metrics, prompt, final output, and final-message records. The candidate
deliverables `solution.py`, `solution.mpy`, `verification.k`, `spec.k`,
`prove.sh`, and `PROOF.md` are also readable regular non-symlink files.

The complete object in `/audit-campaign-lock.json` equals the
`audit_campaign` block in `/audit-input.json`; its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The mounted audit image ID, K version 7.1.293, campaign ID, prompt hash, Kit
lock, and toolchain lock are consistent across the records.

The candidate prompt and translator are byte-identical to their trusted
mounts:

- prompt:
  `e68cbac960bfb695527850d504ec27806e0f41a7711920d0a9e3152369179146`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

I recursively compared `/candidate/reference-semantics` with
`/reference/reference-semantics`, including entry names, entry types, and file
bytes. There are no missing, additional, changed, mistyped, symlinked, or
special entries. An independent reviewer tree digest over type, relative path,
and bytes is
`12c7a1ebdee5da7e7f812db5de9d889389434ee7197fd38bbf209c5990161c40`
for both trees. The same independent algorithm gives
`4c388fbb3a46b9022f4b982beb62a7b3bdc051509c870d71286a917d3a6ea144`
for the full 797-entry candidate tree; it contains no symlinks or special
entries.

Evidence:
[provenance checker](evidence/check_provenance.py),
[checker log](evidence/07b-independent-provenance-check.log),
[manifest inspection](evidence/01-provenance-manifests.log),
[mounted inventory](evidence/02-mounted-file-inventory.log), and
[generation-trace inspection](evidence/05-generation-trace-inspection.log).
The generation records were treated only as untrusted historical claims.
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of unique integers, return `True` exactly when some number of
right shifts (equivalently, some cyclic rotation) places the elements in
non-decreasing order. Return `True` for the empty list.

The trusted canonical implementation finds the minimum element, rotates at its
index, and compares the result with `sorted(arr)`. The candidate instead counts
strict descents around the cycle:

1. it returns `True` immediately for an empty list;
2. for a nonempty list it scans adjacent pairs, accumulating
   `current < previous`;
3. it also checks the wraparound edge with `first < previous`; and
4. it returns whether the count is at most one.

This is correct on the contract domain. If a sorted cyclic rotation exists,
only its wraparound edge can be a strict descent. Conversely, with unique
elements, zero descents is possible only for length at most one; with one
descent, cutting immediately after that edge produces the increasing cyclic
rotation. Any cut can be implemented by a number of right shifts.

### Trusted regeneration

In the clean scratch directory I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited 0. The submitted and regenerated MPY files have the same
SHA-256:
`a1e6096bb2ef0c2037f8125aed71c38e423da67cac29b794d361a1b57c77d82e`.
See [the regeneration log](evidence/09-mpy-regeneration.log) and the preserved
[regenerated MPY](evidence/solution.regenerated.mpy).

### Independent differential test

The reviewer-authored [differential test](evidence/differential_test.py)
imports the trusted canonical and candidate entry points independently and
also uses a direct existential rotation oracle. It covers:

- both prompt examples;
- empty, singleton, two-element, sorted, rotated, signed, and arbitrary-size
  integer cases;
- the one-versus-two circular-descent branch boundary;
- all 46,234 permutations through length 8; and
- 800 deterministic generated unique-integer lists of lengths 9 through 40.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py
```

Exit status was 0. All 47,045 cases agreed; mismatch count was zero. See
[the differential log](evidence/10-differential-test.log). This is finite
bridge evidence, not a substitute for the K proof.

Stage 2 result: pass.

## 3. Clean proof reconstruction

I copied only source artifacts and the trusted semantics into
`/tmp/audit-work/problem-109-independent`. No candidate `*-kompiled` directory,
cache, binary, log, or trace was copied or used.

The installed tools report K version 7.1.293. I rebuilt the concrete definition
with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-audit
```

Exit status was 0. The warnings concern unused or deliberately partial
operations outside this program. See
[the LLVM build log](evidence/12-llvm-kompile.log).

I independently combined the exact submitted function with seven concrete
assertions covering empty, singleton, both prompt examples, signed
two-element rotations, and a false two-descent case. I translated it and ran:

```text
python3 py2mpy.py concrete_audit.py > concrete_audit.mpy
krun concrete_audit.mpy --definition runtime-kompiled-audit
```

Both statuses were 0. The final configuration has `<k> .K </k>`,
`<stack> .List </stack>`, `<ret> noRet </ret>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`. The source, translated input, and bounded log are
[concrete_audit.py](evidence/concrete_audit.py),
[concrete_audit.mpy](evidence/concrete_audit.mpy), and
[13-fresh-concrete-execution.log](evidence/13-fresh-concrete-execution.log).

I rebuilt the proof definition with:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
```

It exited 0. See [the Haskell build log](evidence/14-haskell-kompile.log).

The specification has two positive claims. I first isolated the auxiliary
loop claim:

```text
kprove spec.k --definition verification-kompiled-audit \
  --spec-module SPEC --claims SPEC.scan-loop
```

It exited 0 and printed `#Top`; see
[15-kprove-scan-loop.log](evidence/15-kprove-scan-loop.log).

I then proved the complete specification, retaining the loop circularity while
proving the entry claim:

```text
kprove spec.k --definition verification-kompiled-audit \
  --spec-module SPEC
```

It exited 0 and printed `#Top`; see
[16-kprove-all-positive-claims.log](evidence/16-kprove-all-positive-claims.log).
Thus every positive claim closes in the fresh definition.

Stage 3 result: pass.

## 4. Adequacy and real-program pinning

### Plain-language claims

`scan-loop` assumes that:

- the next computation is the fixed semantics' real
  `#loop(list(VS), Name("current"), scanBody)`;
- the current scope has the five actual locals, with `previous = current = P`
  and `drops = D`;
- `P` is an integer and all remaining `VS` elements are integers.

It concludes that the loop is consumed, both `previous` and `current` equal
`lastAfter(P, VS)`, and `drops` equals the left fold `scanDrops(D, P, VS)`.
The arbitrary surrounding scope map and omitted cells are framed. A satisfying
witness is `VS = .ValSeq`, `P = D = 0`, `L = 1`, an otherwise empty scope map,
and arbitrary well-sorted values for `arr` and `first`.

`move-one-ball` assumes a clean initial call state:

- the function name resolves in module scope 0 to a closure with parameter
  `arr`, exact body `moveOneBallBody`, and defining scope 0;
- the argument is `list(VS)`, with every element a K `Int`;
- heap and stack are empty, scope and heap locations are initial, and there is
  no pending return, exception, or nonzero exit.

It concludes that the call's returned K value is exactly `moveSpec(VS)`. The
postcondition has no free result variable and no one-way implication. A
satisfying entry witness is `VS = .ValSeq` with the exact cells shown in the
claim.

### Mechanical source-to-claim comparison

I parsed trusted-regenerated `solution.mpy` and the proof macros with the fresh
definition and macro expansion:

```text
kast solution.mpy --definition verification-kompiled-audit \
  --module MPY-SYNTAX --expand-macros --output json \
  --output-file solution-kast.json
kast --expression "moveOneBallBody" \
  --definition verification-kompiled-audit --module VERIFICATION \
  --sort Stmts --expand-macros --output json \
  --output-file body-kast.json
kast --expression 'closureVal("arr", moveOneBallBody, 0)' \
  --definition verification-kompiled-audit --module VERIFICATION \
  --sort Val --expand-macros --output json \
  --output-file closure-kast.json
/audit-output/evidence/check_program_pinning.py
```

All four statuses were 0. The parsed module has exactly one function named
`move_one_ball`; its parameter constructor is exactly `arr`; the claim closure
has the same parameter sequence, body constructor tree, and parent scope 0; and
the `For` body is constructor-identical to the submitted loop body. See
[the checker](evidence/check_program_pinning.py) and
[its log](evidence/17b-mechanical-program-pinning.log).

The claim therefore pins the real submitted function even though it begins at
its exact call configuration instead of reloading the whole module. The
macros are semantically inert constructor aliases and expand before execution.

For ground substitution, `moveSpec` reduces to `true` on the empty list and
`[3,4,5,1,2]`, and to `false` on `[3,5,4,1,2]`. Wrapped configuration claims
for all three returned `#Top` with exit 0; the Python implementations and
direct oracle gave the same values. See
[the ground spec](evidence/spec-ground-results.k) and
[18b-ground-postcondition-evaluation.log](evidence/18b-ground-postcondition-evaluation.log).
An earlier diagnostic using bare functional claims was rejected because this
Haskell backend does not support that claim form; it was replaced by the
successful configuration claims and is not used as evidence.

### Body sensitivity

The fresh [body-sensitivity spec](evidence/spec-body-sensitivity-audit.k)
changes the actual closure's reachable final statement to `Return(Bool(false))`
for the nonempty prompt-true input while retaining a `true` obligation. Exact
command:

```text
kprove spec-body-sensitivity-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-BODY-SENSITIVITY-AUDIT
```

The command exited 1 with `WarnStuckClaimState`. The residual contains the
mutated closure and final `<k> false ~> .K </k>` against `true`, proving that
the changed program term was executed and that the original proof is
body-sensitive. See
[20-body-sensitivity-mutation.log](evidence/20-body-sensitivity-mutation.log).

Stage 4 result: pass.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored [inventory script](evidence/inventory_k_rules.py)
enumerates each declaration, rule, guard, and attribute block from
`semantics.k`, every helper K file, `verification.k`, and `spec.k`. Its final
bounded output is
[19c-exhaustive-k-rule-inventory.log](evidence/19c-exhaustive-k-rule-inventory.log).
It records:

- 233 syntax/declaration blocks, one configuration, and five contexts;
- 707 rules: 660 ordinary, 45 priority, and 2 simplification rules;
- 147 function-bearing declaration blocks, 109 `total` blocks, no
  `functional` or `anywhere` rules, and 26 `owise` rules;
- 25 `symbol` declarations, 22 with `no-evaluators`, and 35 concrete-only rule
  blocks; and
- two reachability claims.

The per-file inventory comprises: assembly (0 blocks), `assert` (3), `bool`
(14), `builtins` (175), `call` (24), `comprehension` (10), runtime-only
`concrete` (21), `controls` (37), `core` (84), `dict` (40), `float` (155),
`functions` (19), `int` (17), `iter` (1), `list` (32), `methods` (102),
`operators` (12), `range` (8), `set` (18), `sort` (25), `str` (33),
`subscript` (57), `syntax` (16), `tuple` (25), `verification` (18), and
`spec` (2). This artifact is the exhaustive rule-level record; the following
is the audit decision by semantic role.

### Fixed-semantics decision

The submitted term uses only module/function loading, a single exact call,
plain-scope name lookup and assignment, Boolean/list truthiness, integer and
Boolean literals, in-bounds list index 0, list iteration, integer comparison,
integer-plus-Boolean, `if`, and `return`. Their declarations and every rule on
their path are mapped in
[used-construct-map.md](evidence/used-construct-map.md).

The material rule chain is sound:

- `Call` evaluates the named callee and the one argument left-to-right, selects
  the exact closure binding, allocates a fresh plain frame, binds `arr`, pushes
  the caller continuation, and later pops and restores every material cell.
- `If` evaluates `not arr` through the correct empty/nonempty list truthiness.
  The empty branch returns before index 0 is evaluated.
- On the nonempty branch, `valSeqAt(vCons(...), 0)` is the in-bounds head.
  The supplied `total` trust for out-of-bounds or opaque sequences is never
  invoked on a reachable result-bearing path.
- The `For` rule iterates the unmutated bare list one constructor at a time and
  binds the actual `current` target before executing the exact two-statement
  body. No heap-reference or cell-variable priority rule matches the exact
  plain frame.
- The operator layer preserves evaluation order. Fixed integer `<` and `<=`
  rules are mathematical comparisons, and fixed integer-plus-Boolean rules
  map `false` to 0 and `true` to 1, matching Python.
- `Return` evaluates the value, records it, discards the remaining callee body,
  pops precisely the active frame, and restores the clean caller state.

All other supplied modules are task-independent and constructor-disjoint from
the submitted term. `MPY-CONCRETE` is imported only by the fresh LLVM runtime
module, not by `VERIFICATION`. The reduced semantics deliberately has partial
or opaque support for unused operations such as floats, strings, imports,
dicts, methods, keyed sorting, and MD5; none can rewrite or influence a term on
this proof path. No supplied file contains `move_one_ball`, `moveSpec`,
`scanDrops`, `lastAfter`, or task-specific ball/rotation rules.

The 25 declared symbols are the float bridge symbols
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`; the sort symbols `sortVS` and `sortKeyVS`; and `md5hexCodes`.
None occurs in the submitted body, claims, summaries, guards, or residuals.
The two function symbols with no textual equation at all are `sortKeyVS` and
`md5hexCodes`; they are likewise irrelevant.

### Proof-local extension decision

The 18 proof-local blocks have the following complete classification:

- `scanBody` and `moveOneBallBody` are macro declarations plus constructor
  equations. They expand away and replace no runtime transition. The
  constructor check in Stage 4 establishes their exactness.
- `allInts` is a total structural predicate. Its empty and `vCons` equations
  are disjoint, exhaustive on `ValSeq`, and recursively descend.
- The first `applyCmp("<", A:Val, B:Val)` simplification is guarded by
  `isInt(A) andBool isInt(B)` and is exactly the fixed
  `applyCmp("<", I1:Int, I2:Int) = I1 <Int I2` equation after safe sort
  projection. It does not rewrite a `<k>` computation.
- `scanDrops` is a definitional summary, not an operational bridge. Its base
  and recursive equations are disjoint; the recursive rule strictly shortens
  `ValSeq`; its integer guards cover every use under `allInts`. It is connected
  to real loop execution by the universal `scan-loop` reachability claim.
- `lastAfter` is total, exhaustive, disjoint, and structurally recursive.
- The second `applyCmp` simplification is limited to
  `lastAfter(P, VS)` under integer guards. Those guards make the result an
  integer; it agrees with both the first simplification and the fixed integer
  rule on every overlap.
- `moveSpec` is a definitional postcondition. Its empty and nonempty guards are
  disjoint and cover the formal all-integer domain. The nonempty equation is
  the exact loop fold plus the closing edge and constrains the final Boolean.
- `scan-loop` is the connection theorem for the program-derived summaries;
  `move-one-ball` executes the exact call and body and returns the defined
  result. Neither claim is an axiom or runtime rewrite in the proof
  definition.

There are no proof-local priority rules, opaque symbols, unconstrained oracles,
abrupt-control bridges, task-answer execution rules, or equations with
conflicting overlaps. I found no unsound proof rule and therefore have no false
conclusion witness to report. The changed-body witness instead confirms that
the fixed execution, rather than a summary oracle, determines the result.

Stage 5 result: pass.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh
[spec-false-result-audit.k](evidence/spec-false-result-audit.k) retains the
exact submitted body and exact clean cells, fixes the satisfying nonempty input
`[3,4,5,1,2]`, and changes its actual `true` result obligation to `false`.

First I verified that the mutation parses and builds:

```text
kprove spec-false-result-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-FALSE-RESULT-AUDIT --dry-run
```

It exited 0 and emitted the backend command; see
[21-fresh-false-mutation-build.log](evidence/21-fresh-false-mutation-build.log).

Then I ran the real proof:

```text
kprove spec-false-result-audit.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC-FALSE-RESULT-AUDIT
```

It exited 1 with `WarnStuckClaimState`, not a parser error, timeout, missing
import, or backend crash. The residual contains the exact submitted closure and
final `<k> true ~> .K </k>`; it fails solely because the destination requires
`false`. See
[22-fresh-false-mutation-proof.log](evidence/22-fresh-false-mutation-proof.log).

Stage 6 result: pass.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics, for every finite `ValSeq` whose elements are
K mathematical integers, starting from the exact clean call configuration:

- the actual submitted `move_one_ball` closure executes;
- its loop transforms the real locals according to `lastAfter` and
  `scanDrops`; and
- the call reaches the exact Boolean `moveSpec(VS)`.

For a nonempty sequence, `moveSpec` is true exactly when the count of strict
descents over all adjacent edges plus the last-to-first edge is at most one;
for the empty sequence it is true. This formal domain includes the full source
contract domain and is stronger because it does not require uniqueness.

### Trust and assumptions

- **K implementation:** correctness of K 7.1.293, the Haskell prover, LLVM
  executor, K parser/macro expander, and built-in integer, Boolean, map, list,
  equality, sort-predicate, and projection hooks is the ordinary low-level
  trusted computing base. This is acceptable and unavoidable for a
  machine-checked K proof.
- **Supplied semantics:** the fixed trusted source tree is part of the theorem's
  interpretation. I independently audited every source block and the complete
  material path. Reduced or opaque behavior for unused operations is excluded
  from the theorem and has no result, state, control, or exception influence.
- **Translator bridge:** `/reference/py2mpy.py` is launcher-designated trusted
  input. Byte-identical regeneration and macro-expanded constructor comparison
  establish that the proved body is its translation of the submitted Python.
- **Source-intent bridge:** the equivalence between “at most one strict circular
  descent” and “some cyclic rotation is non-decreasing” on unique integers is
  the elementary mathematical argument given in Stage 2. It is not assumed
  through an opaque proof symbol or a differential oracle.
- **Empirical evidence:** the 47,045 differential cases and fresh concrete K
  run support Python implementation fidelity and used-semantics adequacy only.
  They do not replace either K reachability claim.
- **Partial correctness:** the requested result is conditional on the supplied
  execution semantics. Inputs containing non-integers, malformed `ValSeq`
  terms, out-of-bounds execution, mutation of the iterated list, external
  state, and unused Python features are outside the formal precondition or the
  submitted program.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(auditable trust/evidence) all pass. There is no material domain narrowing,
vacuity, result oracle, substituted body, unproved operational bridge, or
reconstruction failure.

VERDICT: PASS
LEGITIMACY: LEGIT
