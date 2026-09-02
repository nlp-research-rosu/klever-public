# Independent adversarial review — 112-reverse-delete

## Outcome

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program for the full source-contract domain of finite
strings. I reconstructed all definitions from source, proved the loop theorem
again with the loop bridge physically absent, proved the entry claim, checked
constructor-level program identity, and obtained the expected failure from an
independently authored false-result mutation.

The candidate's ordinary `prove.sh` invocation of `LOOP-SPEC` uses the
bridge-enabled main definition, so that invocation alone is not acceptable as
the bridge-free connection theorem. This audit closed that evidence gap by
compiling `MPY-VERIFICATION-BASE` as a separate main definition. The bridge
source location is absent there and the same universal loop claim still
produces `#Top`. Thus the observation is about the candidate's validation
command, not a remaining soundness or adequacy defect.

## 1. Input and provenance integrity

Status: pass; no audit-infrastructure breach.

`/audit-input.json` declares:

- problem `112-reverse-delete`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The required `/reference/reference-semantics` mount exists, as required in
this mode. The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, and the lock's SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
See [stage1_campaign_match.log](evidence/stage1_campaign_match.log) and
[stage1_record_hashes.log](evidence/stage1_record_hashes.log).

All records required for `legacy-selected-stage1` were present, readable,
regular, and non-symlinked:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the JSONL trace at
  `/generation-evidence/codex-trace/2026/07/23/rollout-2026-07-23T04-41-55-019f8e5a-6131-77e3-8772-dbb3ca59fac7.jsonl`.

The optional `usage.json` was present and inspected. Historical runtime
metrics are not required by this layout. Regular-file and directory checks
are in [stage1_required_file_records.log](evidence/stage1_required_file_records.log)
and [stage1_required_directory_records.log](evidence/stage1_required_directory_records.log).

The independently computed file hashes match the recorded values for the
campaign lock, canonical source, trusted prompt and translator, run/task/result
records, invocation and metrics records, usage record, generation prompt,
Codex last/output records, and the trace file. Independently computed pipeline
tree hashes also match the manifest-era hashes:

- candidate tree:
  `3c3537a0dada32706f815e6f55c87e5fe9f3347678a128926ce3ae1c9a4ac67e`;
- trusted and candidate supplied-semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace tree:
  `9a1fc9ceca14a5a1dd40f9722bdf5846831a9cfb43291f5e5e9ed7590c849834`.

These are respectively the retained workspace hash in the generation records,
the trusted semantics manifest hash in the audit record, and the source-trace
hash in `usage.json`. See
[stage1_recorded_tree_hashes.log](evidence/stage1_recorded_tree_hashes.log).
Per-file manifests independently cover every semantics file:
[stage1_trusted_semantics_manifest.log](evidence/stage1_trusted_semantics_manifest.log)
and [stage1_candidate_semantics_manifest.log](evidence/stage1_candidate_semantics_manifest.log).

There are no symlinks anywhere in `/candidate`, `/reference`, or
`/generation-evidence`. Recursive `diff --no-dereference` reports no missing,
additional, mistyped, or changed candidate semantics entry. The candidate
prompt and translator are byte-identical to their trusted versions. See
[stage1_no_symlinks.log](evidence/stage1_no_symlinks.log),
[stage1_semantics_diff.log](evidence/stage1_semantics_diff.log),
[stage1_prompt_diff.log](evidence/stage1_prompt_diff.log), and
[stage1_translator_diff.log](evidence/stage1_translator_diff.log).

The structured trace was parsed in full as 311 valid JSONL records: one
session record, 89 event records, 219 response records, one world-state record,
and one turn-context record. It contains 56 function calls and outputs, 11
custom patch calls and outputs, six agent messages, and the final untrusted
`KPROVE_PASSED` claim. The parser and extracted record inventory are
[trace_inventory.py](evidence/trace_inventory.py) and
[stage1_trace_inventory.log](evidence/stage1_trace_inventory.log). The
16,677-line Codex output was also inspected for edits, commands, failed proof
iterations, final `#Top` reports, and the final candidate claim. None of those
generation reports was used as proof evidence.

## 2. Program fidelity and candidate-versus-canonical checks

Status: pass.

The trusted prompt requires `reverse_delete(s, c)` to remove from string `s`
every character occurring in string `c`, then return the retained string and
whether that string is a palindrome. The documented results are
`("bcd", False)`, `("acdef", False)`, and `("cdedc", True)` for the three
examples.

The trusted canonical function computes the retained characters with a
comprehension and compares the result with `s[::-1]`. The submitted
`solution.py` uses a different but equivalent one-pass algorithm:

1. append each retained character to `result`;
2. prepend that same character to `reversed_result`;
3. return `(result, result == reversed_result)`.

The added initialization `character = ""` is semantically inert for the
returned tuple and makes the empty-loop target value explicit.

Using the trusted `/reference/py2mpy.py` in scratch:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
```

exited 0. Both files have SHA-256
`09c57fd0ede380bbe643760e1cb8402fd153ddd32dfb1d8a97b2c92c6344137e`.
See [stage2_translate_identity.log](evidence/stage2_translate_identity.log).

The independent differential program
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and candidate functions under distinct module names. It preserves
all generated inputs in
[differential_inputs.json](evidence/differential_inputs.json), whose SHA-256
is `e624c8d9a0a7e2cc026f127046ef8b72dddef0676fb1750fb46c7e833421883a`.
The test scope was:

- 20 documented/boundary cases, including both-empty, empty `s`, empty `c`,
  one-character kept/deleted branches, all/none deleted, front/middle/back
  deletion, duplicates in `c`, emoji, accents, combining characters, NUL, and
  line breaks;
- 1,905 exhaustive pairs with `s` length 0–6 and `c` length 0–3 over
  `{a,b}`;
- 2,000 deterministic random pairs (seed 112), with `s` length 0–40 and `c`
  length 0–12 over ASCII, accent, emoji, and NUL characters.

All 3,925 cases agreed; both palindrome outcomes were exercised
(`True`: 2,772, `False`: 1,153). See
[stage2_python_differential.log](evidence/stage2_python_differential.log).
This is finite fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Status: pass.

Only candidate source artifacts and the trusted reference inputs were copied
to `/tmp/audit-work/112-reverse-delete`. Candidate bytecode, compiled K
definitions, caches, logs, and prior traces were not reused. The installed
independent toolchain reports K `v7.1.293`; see
[stage3_tool_versions.log](evidence/stage3_tool_versions.log).

The clean reconstruction commands and outcomes were:

| Purpose | Exact command | Result |
|---|---|---|
| Concrete definition | `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 |
| Concrete tests | `krun concrete_tests.mpy --definition runtime-kompiled` | exit 0; `.K`, `NoExc`, exit code 0 |
| Proof definition | `kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 |
| Loop target | `kprove spec.k --definition verification-kompiled --spec-module LOOP-SPEC` | `#Top`, exit 0 |
| Entry target | `kprove spec.k --definition verification-kompiled --spec-module SPEC` | `#Top`, exit 0 |

The bounded logs are
[stage3_kompile_llvm.log](evidence/stage3_kompile_llvm.log),
[stage3_krun_candidate_tests.log](evidence/stage3_krun_candidate_tests.log),
[stage3_kompile_haskell.log](evidence/stage3_kompile_haskell.log),
[stage3_kprove_loop.log](evidence/stage3_kprove_loop.log), and
[stage3_kprove_entry.log](evidence/stage3_kprove_entry.log).

LLVM compilation warns about non-exhaustive functions in unrelated float,
builtin, method, and subscript fragments. Both backends warn about unused
`strLt` tail variables. None is on the submitted program's execution path and
none contributes to either claim.

## 4. Adequacy and real-program pinning

Status: pass.

### Loop claim

`LOOP-SPEC` has no explicit `requires`; its sort constraints are its
precondition. At any environment location `L`, it starts with:

- `#loop(str(S), Name("character"), exact-loop-body)` at the head of an
  arbitrary framed continuation;
- a scope at `L` containing exactly string bindings `s=ORIG`, `c=C`,
  `result=A`, `reversed_result=RA`, and a value `character=V`;
- an arbitrary parent `P`.

It says the loop consumes all finite `S`, preserves `s`, `c`, and the parent,
sets `result` to `keptAcc(S,C,A)`, sets `reversed_result` to
`reversedKeptAcc(S,C,RA)`, and leaves `character` unchanged on empty `S` or set
to the last iterated one-character string otherwise. Other cells and the
continuation are framed. This matches the real immutable-string loop's full
state footprint.

### Entry claim

`SPEC` starts from the exact clean configuration: environment 0, empty module
scope with builtins parent, next scope location 1, empty heap and stack,
`noRet`, `NoExc`, and exit code 0. Its `<k>` cell calls a closure at definition
location 0 with parameters `("s","c")`, symbolic string values `str(S)` and
`str(C)`, and the complete submitted function body.

Its postcondition is the exact returned tuple:

```text
(
  str(keptAcc(S,C,.IntSeq)),
  keptAcc(S,C,.IntSeq) ==K reversedKeptAcc(S,C,.IntSeq)
)
```

and the remaining explicitly mentioned cells return to the exact initial
state. The result is neither free nor implication-only.

The reviewer script [constructor_compare.py](evidence/constructor_compare.py)
extracts the closure from `SPEC`, turns it into a `FuncDef`, parses both it and
`solution.mpy` with the clean K definition, and compares the KAST constructor
trees. Function constructor, name, parameters, and body all match. Both body
trees have SHA-256
`58c3d1e2d0452fb7b4384ddb6ac9a86cce0c21654361b5892f22755beeaa7319`;
the closure definition location is 0. See
[stage4_constructor_compare.log](evidence/stage4_constructor_compare.log) and
the mechanically extracted
[claimed_entry_function.mpy](evidence/claimed_entry_function.mpy).

This is the permitted inert normalization: executing the complete module
would apply the fixed `FuncDef` rule and bind exactly this
`closureVal(params, body, 0)`. The entry claim begins at invocation of that
same closure rather than reloading the module.

Satisfiable witnesses are recorded in
[adequacy_witness.py](evidence/adequacy_witness.py) and
[stage4_adequacy_witness.log](evidence/stage4_adequacy_witness.log). For
example, `S=[97,98]` (`"ab"`) and `C=[]` satisfy the entry precondition.
The claimed summaries are `[97,98]` and `[98,97]`, hence `("ab",False)`;
both Python implementations return exactly that. `"abcde","ae"` and
`"abba",""` exercise a filtered non-palindrome and an unfiltered palindrome.
A concrete loop-head scope with `L=1`, those five bindings, and
`P=parent(0)` witnesses the auxiliary precondition.

The formal domain is all finite `IntSeq` values for `S` and `C`, with no size
bound. This includes every finite Python string under the semantics'
code-point representation. The theorem is actually broader because it does
not restrict integers to Unicode scalar values; that does not narrow or
invalidate the source-contract domain.

For body sensitivity, the fresh
[spec-body-mutation.k](evidence/spec-body-mutation.k) changes the executed
closure body from prepending to `reversed_result` to appending to it. The
bridge no longer matches. `kprove` exits 1 with a reachable residual for two
distinct retained characters: the mutated program returns the forward string
and `true`, while the original postcondition requires the unequal reverse.
See [stage4_body_sensitivity.log](evidence/stage4_body_sensitivity.log).

## 5. Rule-by-rule static soundness review

Status: pass.

The exhaustive machine-readable inventory is
[stage5_k_rule_inventory.log](evidence/stage5_k_rule_inventory.log), produced
by reviewer-authored [k_rule_inventory.py](evidence/k_rule_inventory.py).
Across the root semantics, every helper K file, `verification.k`, and `spec.k`
it contains:

- 704 rules;
- 230 syntax declarations;
- five evaluation contexts;
- one configuration;
- two claims;
- 942 total inventoried sentences.

It records source/line, normalized sentence, function/total/functional,
concrete, simplification, opaque/no-evaluator, priority, strictness, macro, and
`owise` attributes, path relevance, and disposition for every row. Of these,
142 are relevant or proof-local and were checked in detail, two are targets,
22 are imported opaque declarations that are unreachable here, and 776 are
supplied-semantics declarations/rules for constructs absent from the submitted
body. The latter were inspected but have no constructor or rewrite path from
this theorem. No unsoundness finding is made without a reachable false
conclusion witness.

The submitted constructors map as follows:

| Construct | Declaration/rule path | Checked behavior |
|---|---|---|
| `Call(closureVal, args)` | `syntax.k`, `core.k` argument loop, `call.k:20-21,69-74`, `functions.k` | callee then arguments left-to-right; fresh frame; exact parameter binding; return/pop restores caller |
| `Str("")` | `syntax.k`, `str.k:13-17` | empty literal becomes `str(.IntSeq)` |
| `Assign(Name, value)` | strict syntax, `controls.k:9-18` | RHS first; current-frame update |
| `For` / `#loop` | strict syntax, `controls.k:65-74`, `str.k:8-10`, `tuple.k:31-41` | iterable once; one-character yields; target binding; body then next iteration |
| `Compare(...,"not in",...)` | contexts in `operators.k`, `str.k:28-41` | operands evaluated; singleton substring membership and Boolean negation |
| `If` | strict syntax, `controls.k:51-54`, `core.k:199-205` | Boolean condition selects exactly one branch |
| string `+` and `+=` | `controls.k:20-31`, `operators.k`, `str.k:20-26` | immutable concatenation and rebinding in correct order |
| `TupleExpr` and equality | `tuple.k:14-18`, `core.k:183-191` | elements left-to-right; structural sequence tuple; string equality |
| `Return` | strict syntax, `functions.k:78-90` | returned value stored, frame popped, exact caller continuation restored |

Configuration, frame allocation, local scopes, stack, return, exception, heap,
and allocation cells were checked. No material operation allocates or mutates
the heap. The loop touches only `<k>` and the three local bindings identified
by its claim; it preserves all omitted cells.

### Proof-extension inventory

1. `keptAcc(S,C,A)` is a definitional summary. Its empty equation returns `A`.
   Its two cons equations are guarded by `strContains(singleton(X),C)` and its
   Boolean negation, so they are disjoint and exhaustive. Both recurse on the
   strict tail. The retained branch appends `X`, exactly matching `result +=
   character`.
2. `reversedKeptAcc(S,C,A)` is a definitional summary with the same disjoint,
   exhaustive membership split and strict-tail descent. Its retained branch
   prepends `X`, exactly matching `character + reversed_result`.
3. `lastCharacter(S,V)` is a total definitional summary over the two `IntSeq`
   constructors. Empty input returns `V`; cons input descends and records the
   singleton current character.
4. `verification.k:44-79` is an operational bridge, not merely an equation.
   It matches the exact `#loop`, exact body, current environment, exact five
   local bindings, arbitrary parent and continuation, and updates precisely
   the cells stated by the loop theorem. Priority 40 only makes it preempt the
   slower fixed loop; it does not supply its justification.

The normalized body of the operational rule is exactly the normalized body of
`LOOP-SPEC`; both have SHA-256
`d826b2e2d280fbc66567cd979a250f354fca405f7550e1f21c6e3457f4997fa9`.
See [stage5_extension_exactness.log](evidence/stage5_extension_exactness.log).

Most importantly, the universal connection theorem was reconstructed without
the bridge:

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition bridge-free-kompiled

kprove spec.k --definition bridge-free-kompiled \
  --spec-module LOOP-SPEC
```

Both commands exit 0 and the proof prints `#Top`; see
[stage5_kompile_bridge_free.log](evidence/stage5_kompile_bridge_free.log) and
[stage5_kprove_loop_bridge_free.log](evidence/stage5_kprove_loop_bridge_free.log).
The bridge source location count is zero in the bridge-free KORE definition
and two in the bridge-enabled definition; see
[stage5_bridge_definition_membership.log](evidence/stage5_bridge_definition_membership.log).
This rules out circular closure through the installed bridge.

The operational-context probe
[bridge-context-spec.k](evidence/bridge-context-spec.k) uses the ground loop
over `"ab"` and immediately follows it with the observable assignment
`after = "x"`. It constrains forward result, reversed result, final loop
target, the continuation assignment, parent, and control completion. The base
claim closes with the bridge-free definition and the enabled claim closes
with the bridge-enabled definition, both at the same state. See
[stage5_bridge_context_base.log](evidence/stage5_bridge_context_base.log) and
[stage5_bridge_context_enabled.log](evidence/stage5_bridge_context_enabled.log).

No proof-local value is opaque or fresh. The same summaries appear in the
bridge and final postcondition, but their values are fixed by exhaustive
equations and, for the bridge, by the independently proved bridge-free
connection theorem. There is no oracle, answer-encoding rewrite, unconstrained
result, fabricated operation, or overlapping equation with disagreeing
right-hand sides.

## 6. Fresh non-vacuity test

Status: pass.

The reviewer-authored [spec-vacuity.k](evidence/spec-vacuity.k) changes the
entry result string from:

```text
str(keptAcc(S,C,.IntSeq))
```

to the deliberately false value:

```text
str(seqConcat(keptAcc(S,C,.IntSeq), iCons(120,.IntSeq)))
```

That appends `"x"` to every claimed result. The clean satisfying input
`S=.IntSeq`, `C=.IntSeq` returns `("",True)`, so the mutation's
`("x",True)` obligation is demonstrably false.

The exact command:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

successfully parsed and built the spec, reached the prover, then exited 1 with
`WarnStuckClaimState`. Its residual contains the expected unmet implication:

```text
keptAcc(S,C,.IntSeq)
  #Equals
seqConcat(keptAcc(S,C,.IntSeq), iCons(120,.IntSeq))
```

This was not a parser failure, missing import, timeout, unrelated crash, or
unreachable mutation. The bounded output is
[stage6_false_result_mutation.log](evidence/stage6_false_result_mutation.log).

## 7. Proven versus assumed accounting

Status: pass.

### What is formally established

Under the supplied MPY semantics, for every finite input code sequence `S` and
`C`, if the exact submitted `reverse_delete` closure starts in the clean
configuration stated by `SPEC` and terminates, it returns:

```text
tuple(
  str(filter from S every singleton contained in C),
  structural-equality(
    that retained sequence,
    the same retained sequence accumulated in reverse order)))
```

The caller environment, module/builtins scopes, scope counter, heap, heap
counter, stack, return state, exception state, and exit code have the exact
post-state constrained by the claim. The loop theorem universally establishes
the forward accumulator, reverse accumulator, and final loop-target binding.
On finite `IntSeq` inputs the modeled loop also structurally descends, although
the requested theorem classification remains partial correctness.

By the ordinary definitions of filtering and reversal, the second component
is true exactly when the retained string reads the same backward and forward.
Thus the formal result matches the natural-language deletion and palindrome
contract.

### Trust ledger

- **K framework and backend:** K `v7.1.293`, its reachability prover, builtin
  integers/Booleans/strings/maps/lists, generated strictness rules, and `==K`
  structural equality are the foundational proof checker and mathematics
  trust boundary. All claims were rebuilt and rerun with that recorded
  version.
- **Supplied semantics:** the fixed, trusted input is not modified. Its entire
  tree was integrity-checked and every local declaration/rule inventoried.
  The operational rules affecting this body were reviewed for evaluation,
  binding, control, and state fidelity.
- **Translator bridge:** trusted `py2mpy.py` maps the submitted Python AST to
  `solution.mpy`. Byte-identical regeneration and a constructor-level KAST
  comparison support this bridge. The translator is not proved correct by
  the K theorem.
- **Source-to-contract alignment:** the one-pass reverse accumulator is
  mathematically the reverse of the retained accumulator. This is a direct
  inductive reading of the proved summary equations; the 3,925-case
  differential test independently supports, but does not replace, that
  universal reasoning.
- **Imported opaque primitives:** the supplied theory declares opaque or
  proof-opaque float operations (`intFloatDiv`, `divII`, `floatMod`,
  `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
  `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
  `truncF`, `roundF`, `roundFN`, `sqrtF`), digest `md5hexCodes`, and sorting
  `sortVS`/`sortKeyVS`; totalized opaque indexing can also remain symbolic.
  None of these symbols is syntactically present or reachable from the
  submitted closure, none affects control or state here, and neither target
  claim depends on one.
- **Empirical evidence:** the differential suite supports implementation
  fidelity over its recorded finite sample. Concrete LLVM tests support the
  modeled execution for the documented ASCII cases. Neither is counted as
  the reachability proof.

There are no unproved program-derived abstractions, external result oracles,
hidden lemmas, candidate-provided compiled artifacts, or domain bounds in the
proof. Gates A (real-program soundness and non-vacuity), B (intent adequacy),
and C (auditable trust/evidence) all pass.

VERDICT: PASS
LEGITIMACY: LEGIT
