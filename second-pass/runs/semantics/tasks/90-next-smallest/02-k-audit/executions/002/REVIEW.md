# Independent adversarial audit: HumanEval 90 `next_smallest`

Overall finding: **CONCERNS / LEGIT**. Fresh reconstruction proves that the
submitted program returns the recursively defined value `nsScan(INPUT,0,0,0)`
for every finite list of mathematical integers. The proof executes the
constructor term of the submitted `solution.mpy`, covers empty and unbounded
finite inputs, and rejects both a material body mutation and a false result
claim. No candidate-local rule has a false-conclusion witness.

The concerns are non-fatal. First, the candidate's own loop claim existentially
forgets the final scope map, while its installed operational rule states an
exact scope deletion. I independently closed the stronger bridge-free theorem
after adding the standard finite-Map identity that deleting a freshly added key
restores the original map. Second, the proof's postcondition is the truthful
streaming summary `nsScan`, not a separately formalized theorem equating that
summary to `sorted(set(input))[1]`; that final intent bridge rests on exhaustive
equation review plus finite differential evidence.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `90-next-smallest`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`.

There is no mode/mount contradiction: `/reference/reference-semantics` is
present as a real directory. All launcher-required mounts and records for the
declared layout are present, readable, and not symlinks. The present optional
`usage.json` was inspected. Historical runtime metrics are not required for
this legacy layout.

The campaign object in `/audit-campaign-lock.json` is JSON-equal to the
`audit_campaign` object in `/audit-input.json`; its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly as recorded. All recorded regular-file hashes match. The schema-v2
pipeline tree digest of `/candidate` is
`48bc9aebf0624918c39655838ed89c020036409719f8ee53521e48b4b8ff4947`,
matching both the generation result and invocation. The trace's pipeline tree
digest and its sole JSONL file hash match `usage.json` and
`generation-result.json`, respectively.

The complete untrusted generation record set was structurally scanned:
`codex-output.log` has 34,376 lines, and the sole structured trace has 505
successfully parsed JSON events. Its prior `#Top` and `KPROVE_PASSED` statements
were not used as proof evidence. See
`evidence/00-generation-record-scan.log`,
`evidence/generation_record_scan.py`, `evidence/01-provenance.log`, and
`evidence/provenance_check.py`.

The candidate and trusted prompt and translator are byte-identical. Recursive
`diff --no-dereference` of the candidate and trusted semantics trees exits 0;
both tree digests are
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
and neither tree contains a symlink. There are no missing, additional,
mistyped, changed, or linked supplied-semantics entries. See
`evidence/04-semantics-integrity.log`. No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for the second smallest **distinct** integer in a list,
or `None` when fewer than two distinct integers exist. The distinctness
interpretation is fixed by the `[1,1] -> None` example and by the trusted
canonical implementation:

```python
distinct = sorted(set(lst))
return None if len(distinct) < 2 else distinct[1]
```

The submitted implementation maintains zero, one, or two known distinct
minimum values in a single pass. It does not mutate its argument.

Running the trusted translator over the scratch copy of `solution.py` produced
SHA-256
`3565a16362b57637308ceb199fecae16d8def8cd4fbbfe991823a80691bec553`;
the submitted `solution.mpy` has the same hash and is byte-identical. The exact
command and exit 0 are in `evidence/03-regenerate-mpy.log`.

The independent differential test imports `/reference/canonical.py` and the
scratch-copied generated entry point through separate module loaders. It covers
the four prompt examples, empty and singleton cases, equality on the minimum
and second minimum, every branch transition, ascending and descending inputs,
negative values, duplicates, newly discovered minima, values between/equal
to/above the current second minimum, and very large Python integers. It then
checks 20,000 deterministic generated lists. All 20,020 inputs have input-set
SHA-256
`1692911e714d3508ef8e914cedcebdec7d7d7b50cb3f0fb4d1814f91d66e8dbe`.
There were zero result mismatches and zero input mutations. See
`evidence/differential_test.py` and `evidence/02-differential.log`.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/proof`; candidate
`__pycache__`, proof outputs, and any compiled definitions were not reused.
The observed K version is 7.1.293.

Fresh LLVM reconstruction:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exits 0 (`evidence/05-kompile-runtime.log`). Fresh `krun` of
`solution.mpy` reaches `.K`, `NoExc`, and exit code 0
(`evidence/06-krun-solution.log`). Fresh execution of all submitted concrete
assertions does the same (`evidence/07-krun-concrete-tests.log`). Compiler
non-exhaustiveness warnings concern unused fixed-semantics float, string,
method, and subscript functions; none occurs on this integer program's proof
path.

Fresh positive loop target:

```text
kompile verification.k --backend haskell \
  --main-module NEXT-SMALLEST-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled \
  --spec-module NEXT-SMALLEST-LOOP-SPEC
```

Both commands exit 0, and `kprove` prints `#Top`; see
`evidence/08-kompile-loop.log` and `evidence/09-kprove-loop.log`.

Fresh positive entry target:

```text
kompile verification.k --backend haskell \
  --main-module NEXT-SMALLEST-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition entry-verification-kompiled
kprove spec.k --definition entry-verification-kompiled \
  --spec-module NEXT-SMALLEST-ENTRY-SPEC
```

Both commands exit 0, and `kprove` prints `#Top`; see
`evidence/10-kompile-entry.log` and `evidence/11-kprove-entry.log`. Thus every
candidate positive target closes under a fresh build.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim starts at the real `for`-loop head with:

- any finite `Ints` remainder;
- arbitrary integer values for `smallest`, `second`, `count`, and old `value`;
- the exact function-local bindings and call-frame shape;
- arbitrary caller continuation, heap, heap location, exception, and exit code;
- a side condition that frame location 1 is fresh in the framed map.

It says fixed semantics reaches the recursively calculated
`nsScan(INPUT,SMALLEST,SECOND,COUNT)`, restores the caller environment and stack,
preserves heap/heap-location/exception/exit-code, and existentially permits the
final scope map.

The entry claim starts in the semantics' pristine module configuration with an
arbitrary `INPUT:Ints`. It loads `solutionModule`, calls the public
`next_smallest` binding with `list(intVals(INPUT))`, and constrains the returned
value to `nsScan(INPUT,0,0,0)`, while restoring the observable initial cells.
There is no length bound or example-only restriction. `Ints` inductively
represents every finite list of mathematical integers, including the empty
list; K `Int` is unbounded, matching the material Python-integer behavior here.

### Mechanical program identity

Using the fresh entry definition, I parsed and macro-expanded both submitted
`solution.mpy` and the claim's `solutionModule`. Their JSON KAST files are
byte-identical, length 16,839, with SHA-256
`43b20ee28c43469fe95b19366ec1fdbaa29dea862f37137cb9a665b82e890748`.
See `evidence/12-program-term-identity.log`. The claim therefore executes the
same function binding, parameter, statements, branches, loop body, and returns
as the trusted regeneration of the submitted source.

### Satisfiability and concrete substitution

`INPUT = [3,1,2,1]` satisfies the entry precondition. Ground K evaluation gives
`nsScan(...,0,0,0) = 2` and closes with `#Top`
(`evidence/witness-spec.k`,
`evidence/14-ground-witness-kprove.log`). Both trusted canonical Python and
generated Python return 2 on the same list
(`evidence/15-ground-witness-python.log`). An earlier attempted raw `krun
--term` diagnostic used a `Val` where a top configuration was required and is
discarded; its sort error is preserved in `evidence/13-ground-result.log` and
is not treated as evidence for or against the proof.

### Operational bridge validation

The entry definition contains one priority-40 operational bridge: it replaces
the exact loop/return/`#endcall` region with `nsScan`, restores environment 0,
deletes frame 1, pops the exact frame that contains arbitrary `CONT`, and
preserves heap, heap location, return, exception, and exit-code cells.

The candidate's separately proved loop claim establishes the value, control,
and all other cells but existentially forgets final scopes. A stronger
bridge-free connection claim with the bridge's exact scope RHS initially
failed only on equality of two symbolic maps after deleting fresh key 1; see
`evidence/16-bridge-connection-kprove.log`. I added the ordinary K finite-map
identity

```text
((SC 1 |-> S) [1 <- undef]) = SC  when 1 is not in keys(SC)
```

as a simplification lemma, not as an execution bridge. Against a definition
that imports fixed semantics and this Map identity but not the candidate
bridge, the stronger universal connection theorem prints `#Top` and exits 0.
It quantifies over arbitrary caller continuation and every framed state cell.
See `evidence/bridge-validation.k`,
`evidence/bridge-connection-spec.k`,
`evidence/17-kompile-bridge-validation.log`, and
`evidence/18-bridge-connection-with-map-lemma.log`.

For the ground state `[3,1,2,1]`, the bridge-free and bridge-enabled definitions
both reach result 2 with identical empty frame, environment, scope, heap,
return, exception, and exit-code cells. Both proofs print `#Top`; see
`evidence/operational-witness-base-spec.k`,
`evidence/operational-witness-bridge-spec.k`,
`evidence/22-operational-witness-base.log`, and
`evidence/23-operational-witness-bridge.log`.

A material mutation changes the executed loop-body assignment of `second` to
the literal 999 while leaving `nsScan` unchanged. The mutated definition builds
successfully, but its bridge-free loop theorem exits 1 with
`WarnStuckClaimState`; the residual explicitly distinguishes
`nsScan(...,999,2)` from `nsScan(...,intsHead(INPUT),2)`. See
`evidence/body-mutant-verification.k`,
`evidence/body-mutation-spec.k`, `evidence/19-kompile-body-mutant.log`, and
`evidence/20-kprove-body-mutant.log`. This changes the program term actually
executed by the claim and confirms body sensitivity.

## 5. Rule-by-rule static soundness review

`evidence/static_inventory.py` exhaustively scans the supplied semantics and
`verification.k`; its full 196 KB result is
`evidence/21-static-inventory.log`. It enumerates 1,123 entries:

- 714 rules (695 supplied fixed-semantics rules and 19 candidate rules);
- 237 syntax declarations;
- one configuration and five contexts;
- all modules, imports, and required files;
- 149 `[function]`, 111 `[total]`, 46 priority, 26 `owise`, 35 `concrete`,
  25 `symbol`, 22 `no-evaluators`, seven macro, and one macro-rec occurrence;
- no local `[functional]` or `[simplification]` declaration in the immutable
  candidate/supplied source.

Every supplied rule and declaration is marked
`SELECTED_TRUSTED_FIXED_SEMANTICS`. That is the trusted semantic level selected
by `SUPPLIED_SEMANTICS`, not evidence blessing the candidate extensions. I
reviewed every candidate entry separately:

| Candidate extension | Static decision |
|---|---|
| Four macro symbols and four expansion rules for loop body, return tail, function body, and module | Semantically inert naming; mechanical expanded-term comparison proves exact identity with submitted `solution.mpy`. |
| `nilInts`, `consInts`, and `intVals` | Free inductive carrier for all finite integer lists; it does not assert a result. |
| `intsEmpty` (two equations), `intsHead`, and `intsTail` | Constructor equations are true and non-overlapping. Head/tail are underspecified on `nilInts` despite `[total]`, but every use is guarded by proven non-emptiness, so the unspecified case cannot affect branch, result, or state. |
| Two `#iterNext(list(intVals(...)))` rules | Disjoint on empty/nonempty `Ints`; exact homomorphism to the supplied iterator protocol. Their new `intVals` constructor cannot overlap the supplied `.ValSeq`/`vCons` list rules. |
| `nsScan` plus eight equations | Definitional summary, not an oracle. Empty guards split `count == 2` from its complement. On nonempty input, integer trichotomy and the count guards give complete, pairwise-compatible coverage. Every recursive RHS consumes exactly one `Ints` constructor, so it terminates. |
| Priority-40 loop rule | Operational bridge. Its match is the exact loop body, return tail, `#endcall`, frame, bindings, allocation counters, and caller continuation. The independent bridge-free universal theorem establishes its complete value/control/state transition. |

The `nsScan` equations are the same exhaustive accumulator transition as the
real program: first distinct value sets the minimum; a new lower value shifts
the old minimum to second; an equal minimum is ignored; the first greater
distinct value initializes second; and later values replace second exactly
when strictly between minimum and second. End-of-input returns second exactly
for count 2, otherwise `None`. There are no inconsistent overlaps,
non-descending recursions, task-answer constants, fresh result-bearing symbols,
or unconstrained oracles.

Material source constructs map to fixed rules as follows:

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; module sequencing in `core.k`; closure binding in `functions.k` |
| public `Call` and argument | callee/left-to-right argument routing in `call.k` and `core.k`; exact frame allocation/binding in `call.k`/`functions.k` |
| `Assign`, `Name`, `Int`, `NoneVal` | strict syntax; lookup/literals in `core.k`; writes in `controls.k` |
| `For` and target binding | loop protocol in `controls.k`; `#bindTgt(Name,...)` in `tuple.k`; candidate's constructor-faithful iterator rules |
| nested `If` | strict condition syntax and branch rules in `controls.k` |
| `==`, `!=`, `<` on integers | comparison contexts/dispatch in `operators.k`; mathematical cases in `int.k` |
| short-circuit `or` | head-only context and value-preserving branch rules in `bool.k` |
| `Return` and fall-through | strict return, `#endcall`, and exact frame pop in `functions.k` |

This path preserves evaluation order, bindings, call/return control, frame
allocation and deletion, and every active configuration cell. It performs no
heap allocation or argument mutation. No used construct is unmodeled.

The supplied proof definition includes 25 named opaque/concrete symbols:
`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`. None appears in the submitted constructor
term, the candidate carrier/summary, either positive claim, or any proof
residual. They therefore cannot influence this theorem's control, result, or
state.

## 6. Fresh non-vacuity test

The fresh mutation leaves the real module load and call intact but replaces the
universal result obligation with `noneV` for every input. It is demonstrably
false for the satisfying input `[3,1,2,1]`, whose K summary and both Python
implementations return 2.

`kprove --dry-run` on this distinct module exits 0 and emits a valid
`kore-exec` proof command, establishing that the mutation parses and builds
(`evidence/24-vacuity-dry-run.log`). The actual proof exits 1 with
`WarnStuckClaimState`; its residual is precisely:

```text
#Not ( { noneV #Equals nsScan(INPUT, 0, 0, 0) } )
```

The full mutation and bounded log are
`evidence/spec-vacuity-audit.k` and
`evidence/25-vacuity-kprove.log`. This is the expected unmet result
obligation, not a parser error, timeout, missing import, or unrelated crash.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied semantics and candidate definitions:

1. The fixed-semantics loop region implements `nsScan` for every finite
   `Ints` remainder and every integer accumulator state.
2. From the pristine entry configuration, the exact submitted function body,
   called on any finite list of mathematical integers, returns
   `nsScan(INPUT,0,0,0)` if execution terminates.
3. The installed loop bridge is extensionally equal to fixed execution over
   its complete match domain, conditional only on the standard Map-deletion
   identity explicitly stated above.
4. The proof result depends on both the real body and the postcondition.

### Trust and evidence ledger

- **Supplied MPY semantics:** trusted because it is the exact read-only
  semantics selected by the benchmark. The material subset is additionally
  mapped above. It models unbounded integers and finite lists sufficiently for
  this read-only program; Python behavior outside that subset is not claimed.
- **K builtins and prover:** integer/Boolean/string operations, finite Map/List
  hooks, K equality, heating/cooling, reachability circularity, and the
  Haskell/LLVM backends are the low-level trusted computing base.
- **Translator:** `/reference/py2mpy.py` is trusted; byte-identical
  regeneration and expanded-KAST identity establish the source-to-claim link.
- **Finite-Map identity:** the auditor-added simplification is ordinary finite
  map mathematics and affects only symbolic normalization of scope deletion.
  The candidate did not package this exact-footprint theorem itself, which is
  a reproducibility/maintenance concern, not a false semantic assumption.
- **Candidate carrier and summary:** `Ints` and `nsScan` are locally defined,
  fully reviewed, result-bearing mathematical functions. They are not opaque.
  A generated K differential module checks 341 ground `nsScan` claims whose
  expected results are independently obtained from trusted `canonical.py`;
  all claims close with one final `#Top`
  (`evidence/generate_nsscan_differential_spec.py`,
  `evidence/nsscan-differential-spec.k`,
  `evidence/27-kprove-nsscan-differential.log`).
- **Summary-to-human contract bridge:** the K proof does not contain a
  separate universal theorem defining `sorted(set(INPUT))` and equating its
  second element to `nsScan`. That equivalence is supported by the exhaustive
  transition analysis above, 341 ground K/canonical comparisons, and 20,020
  generated-Python/canonical comparisons. These finite tests do not replace a
  universal theorem; this is the principal reason for `CONCERNS` rather than
  `PASS`.
- **Unused fixed opaque symbols:** the 25 names listed in Stage 5 are part of
  the selected semantics but have no dependency path to this result.

Gate A (real-program soundness) passes: exact body, complete operational
connection, satisfiable witnesses, body sensitivity, and false-result
non-vacuity all hold. Gate B (intent adequacy) covers the full material source
domain with no finite-size restriction; the remaining summary-to-English
equivalence is an explicitly labeled informal mathematical bridge. Gate C
(auditability) passes with exact commands, deterministic input scopes, oracles,
exit statuses, and bounded outputs preserved. Candidate prose, prior logs, and
prior `#Top` claims were not used as substitutes for the reconstructed K proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
