# Independent adversarial audit — 95-check-dict-case

The candidate contains a cleanly reconstructible, non-vacuous K proof of the
submitted `solution.py` under the supplied MPY model. It is nevertheless not a
legitimate proof of the benchmark’s canonical program: the submitted algorithm
materially differs from the trusted canonical implementation on ordinary,
model-representable dictionaries. The campaign’s canonical-vs-docstring
exception does not apply because the candidate is faithful to the docstring,
not to canonical, and did not report the contradiction.

All commands below ran from a fresh source copy in
`/tmp/audit-work/95-check-dict-case`. Candidate kompiled directories, caches,
logs, `PROOF.md`, and prior traces were not used as proof results. The bounded
command logs and reviewer-authored sources are in
[evidence](/audit-output/evidence).

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, and the expected problem and condition.
The supplied reference semantics exists, as required by that mode.

The independent checker
[provenance_check.py](/audit-output/evidence/provenance_check.py) verified:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, and every required pipeline-v3 generation record
  are readable regular files, not symlinks.
- The campaign lock exactly equals the `audit_campaign` object in
  `/audit-input.json`; its recorded SHA-256 is also exact.
- Direct SHA-256 values for canonical, prompt, translator, run/task/result
  manifests, invocation, metrics, runtime metrics, usage, prompt, final
  message, output log, and trace file all equal the recorded values.
- The mounted candidate pipeline tree hashes to
  `6b93908f729b96bb55ac6d21f30ffef5122702aac9718800a9045e4fac816752`,
  exactly the stage-1 `workspace_sha256`.
- The trusted semantics pipeline tree hashes to
  `4495a50f2231cf6231a75f82531d6d4f9b2397fbede6509e4a6dc42c2dd29ad1`,
  exactly the task/launcher manifest hash.
- Candidate [prompt.py](/candidate/prompt.py) and
  [py2mpy.py](/candidate/py2mpy.py) are byte-identical to the trusted
  [prompt.py](/reference/prompt.py) and
  [py2mpy.py](/reference/py2mpy.py).
- A recursive path/type/content comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` found the same 25 entries and no symlink,
  additional, missing, mistyped, or changed entry. An independently encoded
  manifest hash was identical on both trees.
- Every required candidate proof source is a regular non-symlink.

The checker parsed all 2,109 structured-trace JSONL records and scanned all
66,437 generation-output lines. Those records make untrusted claims including
prior `#Top` results; none was substituted for reconstruction. Full results are
in [stage1-provenance.log](/audit-output/evidence/stage1-provenance.log).
There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted [prompt.py](/reference/prompt.py:2) says:

> Return `False` for an empty dictionary. Otherwise return `True` exactly when
> either every key is a string satisfying `islower()`, or every key is a string
> satisfying `isupper()`.

The trusted [canonical.py](/reference/canonical.py:18) implements a state
machine. Its `else: break` at line 38 stops after the second key when that key
agrees with the current case. Consequently it can ignore a later contradictory
or non-string key.

The submitted [solution.py](/candidate/solution.py:1) instead maintains
`all_lower`, `all_upper`, and `seen_key` and scans every key. That is faithful
to the docstring contract, but not to canonical.

### Translation identity

The trusted translator regenerated `solution.mpy` byte-for-byte:

```text
cd80fd23c17f732a7cd612ed1bc149fced7078f2f452f4906704e18e75c720e4
```

for both submitted and regenerated files. See
[stage2-translation.log](/audit-output/evidence/stage2-translation.log).

### Independent differential

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and scratch candidate independently. It tested all five
examples, explicit empty/branch/late-key boundaries, every key sequence of
length 0 through 4 over a 14-key mixed pool, and 500 seeded generated cases:
41,897 cases total.

Results:

```text
documented_expected_mismatch_candidate = 0
documented_expected_mismatch_canonical = 0
candidate_vs_contract                  = 0
candidate_vs_canonical                 = 2536
canonical_vs_contract                  = 2536
```

A concrete ordinary-domain witness is:

```python
d = {"A": 0, "B": 1, "c": 2}
candidate(d) == False
canonical(d) == True
```

After seeing `"A"` and `"B"`, canonical takes its line-38 `break` and never
examines `"c"`. This is a material result divergence, not a model
representation issue. The differential deliberately exits 1 when such a
candidate/canonical mismatch exists; it is a controlled test result, not a
tool failure. Complete scope and examples are in
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).

Campaign amendment v2 exception 2 is inapplicable. Although canonical and the
docstring do contradict, the exception requires the candidate to be faithful
to canonical and to report the contradiction. This candidate does neither.

## 3. Clean proof reconstruction

The observed toolchain was Python 3.10.12 and K 7.1.293; see
[toolchain.log](/audit-output/evidence/toolchain.log).

### Fresh builds

All definitions were rebuilt from trusted/candidate source in scratch:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
Exit 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
Exit 0

kompile --backend haskell connection.k \
  --main-module CONNECTION --syntax-module MPY-SYNTAX \
  --output-definition audit-connection-kompiled
Exit 0
```

Logs:
[fixed LLVM](/audit-output/evidence/stage3-build-fixed-llvm.log),
[verification Haskell](/audit-output/evidence/stage3-build-verification-haskell.log),
and
[connection Haskell](/audit-output/evidence/stage3-build-connection-haskell.log).
LLVM reported several non-exhaustiveness warnings in unrelated supplied-model
helpers. None is in this program’s execution cone; the Haskell proof builds
succeeded.

### Concrete execution

Reviewer-authored normal and boundary cases executed to `.K`, empty stack,
`NoExc`, and exit code 0. Results included empty `false`, lower `true`, upper
`true`, mixed `false`, late-mixed `false`, late-non-string `false`, and uncased
`false`. See the
[input](/audit-output/evidence/reviewer-sources/audit-concrete.py),
[Python output](/audit-output/evidence/stage3-concrete-translate-and-python.log),
and [fixed K output](/audit-output/evidence/stage3-fixed-concrete.log).

Fixed-semantics and bridge-enabled outputs were byte-identical:

```text
7d6973f3118a82cb1a3f0c0207e5b27b4d71f589411533b79ded9aee35ffcd7c
```

for each output; see
[stage3-fixed-vs-extended.log](/audit-output/evidence/stage3-fixed-vs-extended.log).

### Positive claims

Every positive proof claim was run independently against fresh definitions.
Each command exited 0 and printed `#Top`:

| Claim | Evidence |
|---|---|
| `CONNECTION-SPEC.isinstance` | [log](/audit-output/evidence/stage3-proof-connection-isinstance.log) |
| `CONNECTION-SPEC.islower` | [log](/audit-output/evidence/stage3-proof-connection-islower.log) |
| `CONNECTION-SPEC.isupper` | [log](/audit-output/evidence/stage3-proof-connection-isupper.log) |
| `SPEC.loop` without trusting it | [log](/audit-output/evidence/stage3-proof-loop.log) |
| `SPEC.target`, composing the separately proved loop claim | [log](/audit-output/evidence/stage3-proof-target.log) |

The target command marks `SPEC.loop` trusted only for composition after the
separate untrusted proof closes. Thus the target run’s trust flag is discharged
by the preceding proof under the same rebuilt definition.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop` starts at the real MPY list-loop cutpoint with:

- an arbitrary finite remaining key sequence `KS`;
- arbitrary current Boolean accumulators `AL`, `AU`, and `SEEN`;
- the actual translated loop body and exact
  `Return(checkDictReturn()) ~> #endcall` suffix;
- a concrete function frame location `L >= 1`; and
- `notBool hasRefVS(KS)`.

It consumes the loop, updates `all_lower` to `foldLowerKeys(AL, KS)`,
`all_upper` to `foldUpperKeys(AU, KS)`, and `seen_key` to
`SEEN orBool hasAnyKey(KS)`, leaving the real return and call teardown to
execute. The final `key` and `is_string` locals are existential because they
are unobservable and do not influence the return after the loop.

`SPEC.target` starts from the MPY initial configuration, loads
`check_dict_case`, calls it with `dictV(KS, VALUES)`, and proves final module
binding:

```text
"result" |-> checkCaseSummary(true, true, false, KS)
```

with empty stack, `noRet`, `NoExc`, and the expected `.keys()` list allocation.
Its only logical premise is `notBool hasRefVS(KS)`. `VALUES` is arbitrary and
unused. The summary is:

```text
nonempty(KS)
and
(foldLowerKeys(true, KS) or foldUpperKeys(true, KS))
```

so the result is constrained, not free, existential, tautological, or merely
one-way implied.

### Mechanical program pinning

[program_pinning_check.py](/audit-output/evidence/program_pinning_check.py)
balanced and normalized the K constructor terms, treating only the trusted
translator’s blank empty-`Exprs` spelling and K’s `.Exprs` unit spelling as
equivalent. It established:

- regenerated `FuncDef` equals the target’s loaded `FuncDef`;
- the target and postcondition closure contain the same body;
- recursively expanded `checkDictBody` equals the translated body;
- `checkDictLoopBody` equals the actual `For` body; and
- `checkDictReturn` equals the actual returned expression.

All six comparisons passed with matching normalized SHA-256 values; see
[stage4-program-pinning.log](/audit-output/evidence/stage4-program-pinning.log).

There is no automatic source-to-claim generator, but that is an immutable
artifact-maintenance observation, not a pinning defect here.

### Satisfiable witnesses and concrete substitution

The target precondition is satisfiable. Examples include:

- `KS = .ValSeq`, `VALUES = .ValSeq`: formal summary, candidate, and canonical
  are all `false`.
- `KS = ["a", "b2"]`: formal summary, candidate, and canonical are all `true`.
- `KS = ["A", "B", "c"]`: the premise holds because there is no reference;
  formal summary and candidate are `false`, while canonical is `true`.

Ground K summary claims for these cases returned `#Top`; see
[empty](/audit-output/evidence/stage4-summary-empty.log),
[all-lower](/audit-output/evidence/stage4-summary-all-lower.log), and
[late-mixed](/audit-output/evidence/stage4-summary-late-mixed.log).

A separate body-sensitivity artifact changes the actual loaded `FuncDef` body
to `return True` while preserving an empty-input `result = false` obligation.
It dry-runs successfully, then exits 1 with `WarnStuckClaimState` and a
completed state containing `result = true`. See the
[source](/audit-output/evidence/reviewer-sources/audit-body-mutation.k),
[dry run](/audit-output/evidence/stage4-body-mutation-dry-run.log), and
[proof residual](/audit-output/evidence/stage4-body-mutation-proof.log).
The theorem therefore depends on the program term actually executed.

### Domain

The formal domain is unbounded in key-sequence and string length. Excluding
top-level `ref` keys does not impose a finite bound. In this supplied model,
program-created references denote mutable list objects; those are not valid
CPython dictionary keys. Bare tuple values remain included. The target also
accepts some model values that CPython would reject as keys, which is an
over-approximation rather than candidate-caused narrowing.

The pinning and result constraint are sound for the submitted candidate.
Adequacy nevertheless fails at the benchmark boundary because that submitted
candidate is not canonical.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[k_inventory.py](/audit-output/evidence/k_inventory.py) produced the complete
243,283-byte
[inventory](/audit-output/evidence/stage5-k-inventory.txt), with source
locations and full text for every declaration. It contains:

```text
31 files
253 syntax declarations
1 configuration
5 contexts
789 rules
10 claims
```

Of the 789 rules, 764 are in the byte-identical supplied semantics and 25 are
candidate-local (19 in `proof-theory.k`, 6 in `verification.k`). The inventory
also identifies all `function`, `total`, `symbol`, `no-evaluators`,
`concrete`, `priority`, `owise`, `strict`, `seqstrict`, `macro`, and
`simplification` attributes. No local declaration uses `functional`.

Every supplied rule has an exact inventory entry. The per-module disposition
is:

| Supplied module | Rules | Static disposition |
|---|---:|---|
| assert | 3 | Constructor-disjoint from this program |
| bool | 16 | Short-circuit rules used and checked; remaining numeric/ref cases inert |
| builtins | 154 | `isinstance` rules used and checked; other builtin heads inert |
| call | 21 | Callee/argument/builtin/method/closure paths used and checked |
| comprehension | 7 | Constructor-disjoint |
| concrete | 26 | Not imported by the proof main module |
| controls | 34 | Assignment and `For/#loop` paths used and checked; others inert |
| core | 51 | Configuration/load/sequence/lookup/literals/allocation/helpers used and checked |
| dict | 28 | `.keys()` allocation used and checked; other dict operations inert |
| float | 146 | Float operation heads inert; a float key only reaches the checked type discriminator |
| functions | 15 | definition, parameter binding, return, stack and frame pop used and checked |
| int | 19 | Operator heads inert; an integer key only reaches the checked type discriminator |
| iter | 0 | Protocol declarations only |
| list | 27 | list iteration and `hasRefVS` used and checked; other heads inert |
| methods | 75 | `islower`/`isupper` and ASCII predicates used and checked; other methods inert |
| operators | 10 | Constructor-disjoint |
| range | 6 | Constructor-disjoint |
| set | 12 | Operation heads inert; a set value key only reaches the type discriminator |
| sort | 25 | Constructor-disjoint |
| str | 28 | String value representation used; operator heads inert |
| subscript | 40 | Constructor-disjoint |
| syntax | 0 | Sixteen parser declarations, including every submitted AST constructor |
| tuple | 21 | Operation heads inert; tuple values can be opaque keys |

“Inert” here is a constructor/top-symbol judgment, not an assumption that an
unreviewed rule somehow proves the result. The submitted AST has only
`Module`, `FuncDef`, `Params`, `Assign`, `Name`, `Bool`, `NoneVal`, `For`,
`Call`, `Attribute`, `BoolOp`, and `Return`. The active path is:

```text
#loadAll / sequencing
→ function binding and call frame
→ dict.keys allocation
→ list #iterNext and For/#loop
→ ordered assignments with BoolOp short-circuit
→ normal lookup/callee/argument evaluation
→ isinstance and string-method dispatch
→ Return, frame pop, caller assignment
```

The configuration contains exactly the state that path changes: `k`, `env`,
`scopes`, `scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, and
`exit-code`. The target pins every final material cell. Fixed rules preserve
left-to-right argument evaluation, strict assignment RHS evaluation,
single evaluation of `dict.keys()`, iterator order, normal name binding,
call/return control, allocation, and exception/exit cells.

### Candidate-local declarations and rules

The 25 local rules were assessed individually by exact group:

| Local rules | Count | Class and decision |
|---|---:|---|
| `isStringKey(str(_))`, owise non-string | 2 | Exhaustive definitional twin of fixed `isStrV`; disjoint and true |
| `isStrV(V) => isStringKey(V)` | 1 | Derived simplification; agrees with both fixed constructor cases |
| `stringCodes(str(CS)) => CS` | 1 | Constructor destructor; value fixed on every observing domain |
| `lowerKeyCodes`, `upperKeyCodes` | 2 | Exact names for fixed ASCII method formulas |
| guarded `lowerKey`/`upperKey` branches | 4 | Exhaustive true/false string discriminator branches |
| lower/upper folds | 4 | Structural recursion decreasing on `ValSeq` |
| `allLowerKeys`, `allUpperKeys` wrappers | 2 | Exact fold aliases |
| `hasAnyKey` base/cons | 2 | Exhaustive structural definition |
| `checkCaseSummary` | 1 | Exact nonempty/lower-or-upper mathematical summary |
| three AST aliases | 3 | Exact nullary expansions of translated body/loop/return |
| two guarded `applyMethod` simplifications | 2 | Exact fixed method result on the complete string-constructor domain |
| `isinstance` `<k>` bridge | 1 | Exact post-evaluation bridge, checked below |

`stringCodes` is declared `total`, `symbol`, and `no-evaluators` but has only a
string constructor equation. Its interpretation on non-strings is opaque.
Tracing every use shows that it can influence a branch or result only beneath
`isStringKey(V)`, whose true case forces `V = str(CS)` and activates the
constructor equation. Non-string `lowerKey`/`upperKey` paths return `false`
without observing `stringCodes`. Thus the off-domain interpretation is an
evidence limitation, not a result-bearing oracle and not a concrete false
conclusion witness.

The two `applyMethod` simplifications overlap the fixed rules only on
`str(CS)`, where both sides reduce to exactly the same `hasLower/hasUpper`
formula. They read/write no state cell.

The sole priority bridge matches only:

```text
#applyK(
  toCall(builtinV("isinstance")),
  (V, typeV("str"), .Vals))
```

after callee and arguments have been evaluated. It preserves the arbitrary
continuation and every other cell, returns `isStringKey(V)`, and excludes
references so the fixed heap-dereference path remains active. Priority 40
preempts the general builtin route only in this exact domain.

`CONNECTION-SPEC.isinstance` proves the fixed-semantics redex reaches the same
value for arbitrary non-reference `V` and arbitrary `CONT:K`.
`CONNECTION-SPEC.islower` and `.isupper` prove the fixed string method formulas
for arbitrary code sequences and arbitrary continuations. `connection.k`
does not import `VERIFICATION`; it contains no operational bridge. It does
import the independently checked definitional theory, including the exact
`isStrV` twin equation. This is not circular: that equation is fixed by the two
exhaustive supplied `isStrV` rules, rather than by the target postcondition.

No local rule returns from the function, pops a frame, skips the loop,
fabricates allocation/state, suppresses an exception, or writes `result`.
No candidate-local rule admits a concrete false conclusion on the theorem
domain, so this review does not label any such rule unsound. The failure is
program-to-canonical adequacy, for which the concrete witness is in stage 2.

### Supplied-model case gap

The fixed model defines uppercase and lowercase as ASCII ranges 65–90 and
97–122. Therefore code point 233 (`"é"`) is uncased in MPY, while CPython says
`"é".islower() is True`.

Reviewer evidence makes the divergence concrete:

- [CPython witness](/audit-output/evidence/stage7-unicode-cpython.log):
  candidate and canonical both return `True` for `{"é": 1}`.
- [fixed-model method proof](/audit-output/evidence/stage7-unicode-model-proof.log):
  MPY’s `islower` returns `false` for code 233.
- [fixed-model summary proof](/audit-output/evidence/stage7-unicode-summary-proof.log):
  the formal summary for the one-key dictionary is `false`.
- The source-literal LLVM route itself stops at `strToCodes` on the UTF-8
  literal, another supplied encoding limitation:
  [log](/audit-output/evidence/stage7-unicode-literal-krun-gap.log).

This is a supplied-model-vs-CPython gap; the submitted Python program is
faithful to CPython on the witness. The candidate generally mentions
ASCII-oriented strings and Unicode testing in `PROOF.md`, but it supplies no
concrete model-versus-CPython divergence witness in its trust ledger.
Accordingly amendment v2 exception 1’s documentation condition is not fully
met. This would prevent upgrading the gap to merely `CONCERNS` on its own;
the canonical divergence already independently requires `FAIL`.

## 6. Fresh non-vacuity test

The candidate’s `spec-vacuity.k` was not relied on. The reviewer-authored
[audit-false-mutation.k](/audit-output/evidence/reviewer-sources/audit-false-mutation.k)
executes the real candidate body on `{"a": 1, "b2": 2}` and changes only the
result obligation from the true result to `false`.

The dry run parsed and built successfully with exit 0:
[stage6-false-mutation-dry-run.log](/audit-output/evidence/stage6-false-mutation-dry-run.log).

The proof then exited 1 with `WarnStuckClaimState`. Its residual is a completed
normal configuration with:

```text
<k> .K </k>
"result" |-> true
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

while the destination requires `result = false`. This is the expected unmet
result obligation, not a parser error, timeout, missing import, unreachable
mutation, or unrelated crash. See
[stage6-false-mutation-proof.log](/audit-output/evidence/stage6-false-mutation-proof.log).
The proof is result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditioned on the supplied MPY semantics and the checked local definitional
theory, the reconstructed reachability proof establishes partial correctness
of the submitted candidate for every finite `KS` satisfying
`notBool hasRefVS(KS)` and arbitrary `VALUES`:

```text
if execution reaches normal completion,
result =
  nonempty(KS)
  and
  (every modeled key is a modeled-lower string
   or every modeled key is a modeled-upper string)
```

The actual translated candidate body executes. The sequence length is not
bounded, and the result is exact.

It does **not** establish that the candidate equals trusted canonical. The
ordinary input `{"A": 0, "B": 1, "c": 2}` refutes that bridge.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Supplied read-only MPY semantics | All value/control/state behavior | Required fixed model; integrity checked and rebuilt |
| K parser, compiler, Haskell/LLVM backends, reachability kernel | Proof execution and closure | Toolchain trust boundary, version recorded |
| Trusted `py2mpy.py` | Source-to-constructor translation | Byte regeneration plus constructor-level comparison |
| `isStringKey` and `isStrV` twin equation | Type branch and summary | Exhaustively defined/derived, with bridge-free universal connection |
| `stringCodes` off string domain | Potential `IntSeq` value | Opaque but unreachable from every observing/result-bearing path |
| `lowerKeyCodes`/`upperKeyCodes`, folds, summary | Final result | Truthful terminating mathematical definitions |
| `SPEC.loop` trusted in target composition | Loop summary | Discharged separately with untrusted `kprove` under the same definition |
| No-reference premise | Formal input domain | Excludes model refs for mutable/unhashable list objects; not a finite bound |
| MPY ASCII case and UTF-8 literal handling | Unicode result/encoding | Supplied-model gap; concrete divergence independently exhibited |
| Differential testing | Candidate/canonical and CPython bridges | Finite evidence only; not used as a K proof substitute |
| Canonical equivalence | Benchmark legitimacy | Refuted by 2,536 tested cases and a concrete ordinary-domain witness |

Kit Gate A passes: the proof is sound, pins the submitted program, preserves
the operational bridge’s context/state, constrains the result, and rejects
fresh false mutations. Gate B fails: the proved submitted program is not
canonical, which is the benchmark ground truth. The candidate’s Unicode trust
ledger also lacks the amendment’s required concrete model-divergence witness.
The benchmark decision boundary therefore maps this candidate to
`FAIL / NOT_LEGIT`, despite the honest and technically successful theorem about
the substituted algorithm.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
