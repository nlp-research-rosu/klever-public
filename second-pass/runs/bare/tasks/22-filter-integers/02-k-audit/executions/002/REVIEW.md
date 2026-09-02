# Independent adversarial review: 22-filter-integers

The candidate reconstructs successfully and its two full-program ground claims
are honest, body-sensitive executions of the submitted constructor term.
Nevertheless, it does **not** contain a partial-correctness theorem for the
HumanEval contract's unrestricted input-list domain. Its remaining claims are
one-step characterizations or fixed-length examples. The missing arbitrary-list
entry theorem gets stuck when stated against the candidate definition.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
"legacy-selected-stage1"` and `semantics_mode = "GENERATED_SEMANTICS"`.
The mounted inputs agree with that declaration:

- `/reference/reference-semantics` is absent, as GENERATED_SEMANTICS requires.
- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, `/generation-result.json`, the invocation and metrics records,
  `usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the
  structured trace are all non-symlink regular files/directories as applicable.
  The historical `runtime-metrics.json` is absent, but is not required for this
  legacy-selected layout.
- The campaign lock JSON equals the `audit_campaign` object in
  `/audit-input.json`, and its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- Every declared per-file hash checked in the audit manifest and invocation
  output map matches independently. This includes the run/task/result records,
  invocation, metrics, usage, prompt, full Codex log, last message, legacy
  records, and the sole trace JSONL.
- The independently recomputed pipeline tree digest of `/candidate` is
  `1cf472d8a83dc118b03b0a096c8975ef8dae12a62c579727778a39799a55661c`;
  it equals both the invocation's retained-workspace digest and the generation
  result's workspace digest. The trace tree digest is
  `3d229df72362c10ac83ef206fd5e631611145e62bec28772e688ddb8969850c9`,
  equal to the usage record's source-trace digest.
- All 316 structured trace lines parse. The trace file set and file digest
  equal the invocation output map. The generation reports and prior `#Top`
  statements were treated only as untrusted claims.
- The candidate tree contains no symlink or unsupported entry. Its
  `__pycache__` was ignored, and no candidate-built K definition or cache was
  copied into the clean build.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  `/reference` versions.

The exact checks, hashes, trace scan, commands, and statuses are in
[`evidence/provenance.log`](/audit-output/evidence/provenance.log); the
reviewer script is
[`evidence/provenance_inspect.py`](/audit-output/evidence/provenance_inspect.py).
No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks `filter_integers(values: List[Any])` to return, in
original order and with duplicates preserved, exactly those values for which
Python's `isinstance(value, int)` is true. The trusted canonical implementation
is:

```python
return [x for x in values if isinstance(x, int)]
```

Consequently, Python booleans and instances of user-defined `int` subclasses
are included. The list may have any finite length and its elements are not
restricted to the examples' built-in types.

The candidate uses the same algorithm, with only the bound variable renamed.
Running the trusted translator on the scratch copy produced a `solution.mpy`
with SHA-256
`2c9616677b79795d1805d8100b5fabfb5a915713692b441027cef321ab554607`,
byte-identical to the submitted file.

The independent differential test imports the trusted canonical entry point and
the candidate entry point separately. It covers the two documented examples,
empty/singleton lists, both predicate outcomes, booleans, zero and negative
integers, very large integers, infinities/NaN, duplicates/order, custom
`int` subclasses, and heterogeneous non-integers, followed by 1,000 seeded
generated lists of lengths 0 through 30. All 1,011 cases agree, with zero
mismatches. This is finite fidelity evidence, not a universal proof.

Artifacts and exact statuses:

- [`evidence/differential_test.py`](/audit-output/evidence/differential_test.py)
- [`evidence/fidelity.log`](/audit-output/evidence/fidelity.log)

Both trusted regeneration/byte comparison and the differential run exited 0.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/candidate-src`; all
definitions were rebuilt under K v7.1.293 into fresh directories below
`/tmp/audit-work`.

The concrete definition command was:

```text
kompile semantic.k --main-module MPY --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition /tmp/audit-work/semantic-kompiled
```

It exited 0. Fresh `krun` executions covered the first prompt example, an empty
list, the bool boundary, all modeled runtime constructors, and large repeated
positive/negative integers. Every run exited 0, consumed `<k>` to `.K`, and had
the exact `<return>` value independently produced by both Python
implementations.

The proof definition and all submitted positive claims were run with:

```text
kompile verification.k --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition /tmp/audit-work/verification-kompiled

kprove spec.k --definition /tmp/audit-work/verification-kompiled \
  --spec-module SPEC
```

Both commands exited 0 and `kprove` printed `#Top`, so all 17 submitted claims
close freshly. The prover also emitted `WarnTrivialClaim` for 15 of the 17
claims: they simplify to their destinations without an operational rewrite.
That warning does not invalidate those claims, but it accurately reflects their
limited role. The two full entry executions are the nontrivial claims.

Full commands, configurations, bounded outputs, comparisons, and statuses are
in [`evidence/clean_rebuild.log`](/audit-output/evidence/clean_rebuild.log).
Tool versions are in
[`evidence/tool_versions.log`](/audit-output/evidence/tool_versions.log).

## 4. Adequacy and real-program pinning

### Entry claims

There are exactly two claims containing `<program> solutionModule() </program>`.
Neither has a logical `requires` clause.

1. `/candidate/spec.k:86` starts with `bootstrap` followed by invocation on
   `VList(VString("a"), VFloat("3.14"), VInt(5))`, an empty function store and
   environment, and `noResult`. It requires termination at `.K`, the expected
   loaded function and argument binding, and the exact return
   `result(VList(VInt(5)))`.
2. `/candidate/spec.k:104` has the analogous pre-state for
   `[1, 2, 3, "abc", {}, []]` and requires the exact return
   `result(VList(VInt(1), VInt(2), VInt(3)))`.

Each precondition is satisfiable by the ordinary initial configuration with its
displayed ground input. Substitution is already ground; both trusted canonical
Python and candidate Python produce `[5]` and `[1, 2, 3]`, respectively.
Neither postcondition contains a free result variable or a one-way property:
each constrains the exact returned list.

### Program identity and sensitivity

The reviewer mechanically tokenized the regenerated `solution.mpy` constructor
tree and the right-hand side of `solutionModule()`. Both contain 62 constructor
tokens and have identical token digest
`19848bb007d407679fd3500d6edabf2e141bf425c6f970ceca09f3543fa78a5f`.
Thus the two entry claims execute the actual translated binding and body; the
typing import is present in both terms.

A separate body-sensitivity definition changed the term actually expanded by
`solutionModule()` to a function whose body is `Return(ListExpr(.Exprs))`.
That definition built successfully. The prompt-one result claim then failed
with a meaningful stuck terminal state whose return was
`result(VList(.PyVals))`, rather than `[5]`. This is a mutation of the executed
program term, not merely of an external Python file.

Evidence:

- [`evidence/pinning.log`](/audit-output/evidence/pinning.log)
- [`evidence/body-mutant-verification.k`](/audit-output/evidence/body-mutant-verification.k)
- [`evidence/body-sensitivity-spec.k`](/audit-output/evidence/body-sensitivity-spec.k)
- [`evidence/adequacy_probes.log`](/audit-output/evidence/adequacy_probes.log)

### Missing general claim

The other 15 claims do not supply the required entry theorem:

- Claims 1-9 expose at most one `comprehend` step. Their right-hand sides still
  contain `comprehend` on the arbitrary tail; they neither terminate the
  computation nor relate that tail's final result to the mathematical model.
- Claims 10 and 13-17 use fixed list lengths. Claim 15 has symbolic payloads,
  but exactly nine positions.
- Only claims 11-12 load and invoke the complete submitted module, and both
  inputs are ground examples.

There is no claim with arbitrary `VS:PyVals` that executes
`invoke("filter_integers", VList(VS))` to
`result(VList(onlyIntegerInstances(VS)))`.
[`evidence/universal-entry-spec.k`](/audit-output/evidence/universal-entry-spec.k)
states that missing theorem without adding any proof rule. Against the fresh
candidate definition, it exits 1 with `WarnStuckClaimState`; the residual is
the symbolic result
`comprehend(VList(VS), "value", Name("value"), ...)`. Therefore the submitted
one-step claims are not a machine-checked structural induction to the intended
terminal result.

The proof is adequately pinned for its two ground examples, but its theorem
domain is materially narrower than the source contract.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule/claim ledger is
[`evidence/rule_inventory.md`](/audit-output/evidence/rule_inventory.md). It
enumerates every local syntax production, all 23 `semantic.k` rules, all 16
`verification.k` equations, both `[total]` helper families, both `[owise]`
priority cases, and every submitted claim.

The constructs used by `solution.mpy` map as follows:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `ImportFrom`, `FuncDef`, `Return`, `Params` | `semantic.k:8-15`; bootstrap/load/invoke/return rules S1-S7 |
| `Name` and environment binding | `semantic.k:17`, rules E4-E5 |
| `Call(Name("isinstance"), ..., Name("int"))` | `semantic.k:22`, E7, and constructor cases T1-T3 |
| `ListComp` and its single `CompFor` | `semantic.k:23-26`, E8, C1-C2, K1-K2, P1 |
| Heterogeneous input and result lists | `semantic.k:30-38` and the `<program>`, `<functions>`, `<env>`, `<return>` cells |

Important static findings:

- Module loading is sequential; the typing-only import is skipped, and the one
  function is bound before invocation. Skipping runtime `List`/`Any` bindings
  is inert for this translated program because annotations are omitted and the
  names are never evaluated.
- The only invocation rule selects the stored binding, resets the local
  environment, and binds its sole parameter. The exact submitted module has one
  function and one parameter, so no wider lookup/call behavior is needed.
- The return body and list-comprehension rules match the real AST exactly.
  Unsupported statements, multi-generator comprehensions, missing names, and
  non-list iteration remain visibly stuck instead of fabricating a result.
- `pythonIsInteger` is `[function,total]`: `VInt` and `VBool` map to true, and
  the lower-priority `[owise]` case maps every other `PyVal` constructor to
  false. The cases cover the K algebra and do not disagree on an overlap.
- `onlyIntegerInstances` is `[function,total]`, has an empty equation and one
  disjoint descending equation for each of the eight `PyVal` constructors.
  `containsOnlyIntegerInstances` is likewise complete, with an `owise` non-int
  cons case. There is no non-descent or inconsistent overlap.
- `solutionModule`, `filterExpression`, and `filterCondition` are complete
  nullary definitional functions. The program constant is mechanically pinned.
- There are no local `[simplification]` rules, explicit priority attributes,
  K opaque symbols, `[functional]` declarations, operational bridges, result
  oracles, or state-changing proof rules in `verification.k`. `VOpaque(String)`
  is a runtime data constructor, not an opaque K function.
- `onlyIntegerInstances` is a legitimate mathematical summary inside the
  constructor algebra and does not replace program execution. The defect is
  that no universal reachability claim connects it to full program execution.

I found no concrete false conclusion enabled by a local equation when its K
constructors are interpreted as declared, so I do **not** label any inventoried
rule unsound. The narrower issue is an unproved and incomplete representation
bridge: the artifacts never define how every CPython `Any` value maps to
`PyVal`. A user-defined `int` subclass is a concrete source-domain witness.
CPython retains that original object. Encoding it as `VOpaque` makes T3 discard
it; encoding it as `VInt(I)` erases its subtype/object distinction. This is
reported as a source-domain/model gap rather than as a false K equation, because
the candidate never states an encoding contract for `VOpaque`.

## 6. Fresh non-vacuity test

The candidate did not provide a `spec-vacuity.k`; none was trusted or needed.
The reviewer created
[`evidence/false-result-spec.k`](/audit-output/evidence/false-result-spec.k),
which changes the prompt-one return obligation from `[5]` to `[6]`. The initial
state is the same satisfiable ground state used by the successful entry claim,
and both Python implementations establish that `[6]` is false.

The mutation was first compiled with:

```text
kprove .../false-result-spec.k \
  --definition /tmp/audit-work/verification-kompiled \
  --spec-module FALSE-RESULT-SPEC --dry-run
```

The dry run exited 0. The actual proof exited 1 with `WarnStuckClaimState`; its
terminal residual has `<return> result(VList(VInt(5))) </return>`, exactly the
unmet result obligation. This is neither a parser error nor an unreachable
mutation. Full output is in
[`evidence/nonvacuity.log`](/audit-output/evidence/nonvacuity.log).

This establishes that the two ground entry results are discriminating. It
cannot supply the absent arbitrary-input theorem.

## 7. Proven versus assumed accounting

### What the reconstructed proof establishes

Under the candidate's generated K semantics:

- each of the eight possible represented head constructors takes the submitted
  one-step filtering transition, leaving the tail computation residual;
- several fixed finite expressions/model examples reduce to the displayed
  values;
- the complete submitted module, on exactly the two prompt inputs, terminates
  with the exact prompt outputs; and
- the fixed seven-element mathematical example contains only represented
  integer instances and has the displayed stable-filter result.

As partial-correctness statements, the two full entry claims say: if either
displayed ground initial configuration terminates, its exact displayed return,
function store, and environment are reached. Fresh concrete execution also
shows termination for those states. No submitted claim says this for an
arbitrary input list.

### Trust ledger

| Boundary / assumption | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, frontend, LLVM/Haskell backends, and imported INT/BOOL/STRING/list machinery | All builds, runs, and proofs | Ordinary low-level trusted toolchain boundary; versions and fresh outputs recorded. |
| Trusted `py2mpy.py` translation | Source-to-constructor identity | Acceptable benchmark trust boundary; trusted regeneration is byte-identical. |
| Mechanical `solutionModule()` constructor equality | Both entry claims | Independently checked, plus a body-sensitivity failure. |
| Typing import has no material effect after annotations are erased | Module-loading fidelity | Acceptable for this exact standard import and body; import binding/side-effect behavior is otherwise outside the generated semantics. |
| `pythonIsInteger` equations model CPython `isinstance(_, int)` | Every filtering result | Truthful for the explicitly represented built-in categories, including bool; no universal CPython-object encoding theorem supports the full `Any` domain. |
| `VFloat(String)`, `VDict`, `VNone`, nested `VList`, and `VOpaque(String)` abstract Python values by category | Cross-language intent | Payload abstraction is adequate for rejected built-in categories, but `VOpaque` has no stated exclusion of custom int subclasses and no identity bridge. |
| `onlyIntegerInstances` equations | Fixed model claims and the intended missing postcondition | Mathematically sound over `PyVals`; not universally connected to execution by a submitted claim. |
| Differential and concrete tests | Python fidelity and finite semantic bridge evidence | Reproducible and zero-mismatch over the recorded scope; finite evidence only, never a substitute for the absent K theorem. |
| Partial-correctness termination premise | Reachability interpretation | Standard. The submitted ground cases also terminate concretely; unrestricted termination is not what repairs the missing result theorem. |

There are no proof-local opaque functions or operational shortcuts to account
for. The essential unproved assumptions are the full CPython-to-`PyVal`
representation and, more decisively, the unstated/unproved induction from the
one-step comprehension cases to an arbitrary terminal result.

### Gate and benchmark decision

- **Gate A, soundness of the claims actually submitted: PASS.** They rebuild,
  are program-pinned where they execute the program, use no unsound extension,
  and reject both an executed-body mutation and a false ground result.
- **Gate B, intent adequacy: FAIL.** The only entry claims are two examples;
  fixed-length and one-step claims do not prove the unrestricted
  `List[Any]` contract. The missing arbitrary modeled-list theorem itself gets
  stuck.
- **Gate C, full-source trust/evidence: FAIL for the intended theorem.** The
  evidence is reproducible, but the CPython-object representation bridge is
  informal/incomplete and finite tests cannot make it universal.

In generic Kit language the sound submitted fragment is
`SOUND-BUT-LIMITED`. The benchmark's explicit decision rule maps a material
narrowing of the HumanEval source-contract domain to `FAIL / NOT_LEGIT`, not to
`CONCERNS`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
