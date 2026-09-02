# Independent adversarial audit: 18-how-many-times

This is a completed seven-stage audit of the immutable candidate under
`SUPPLIED_SEMANTICS`. Candidate prose, logs, traces, and prior `#Top` results
were treated only as untrusted claims. All executable reconstruction and
mutations were performed from source copies below `/tmp/audit-work`; no
candidate-provided kompiled definition or cache was used.

The candidate is not a legitimate proof of the generated program. Its positive
claims do reconstruct and are result-constraining, and its macro is
constructor-identical to the submitted program body. However,
`/candidate/verification.k:106` installs a priority-30 operational bridge that
turns the exact closure call directly into a separately authored overlap-count
machine. It skips parameter binding, lookup, slicing, recursion, calls,
returns, and the submitted body. There is no bridge-free connection theorem.
Two independent witnesses show that the rule can fabricate a result and that
the proof is insensitive to a material change in the body.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `18-how-many-times`;
- condition `semantics`;
- record layout `legacy-selected-stage1`;
- semantics mode `SUPPLIED_SEMANTICS`;
- `mount_reference_semantics: true`.

I read `/audit-input.json`, its `record_layout`, `container_paths`, hashes, and
integrity fields before using the candidate. I also read:

- `/audit-campaign-lock.json`;
- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the JSONL trace below `/generation-evidence/codex-trace/`.

The historical layout does not contain `runtime-metrics.json`; that record is
not required for `legacy-selected-stage1`. The one trace file contains 271
parseable JSON events. The recorded generation report claims `#Top` and 945
tests, but neither claim was relied upon.

### Hashes, types, and campaign lock

The campaign lock is a regular non-symlinked file, has SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and parses to exactly the `audit_campaign` object in `/audit-input.json`.
Every launcher-declared container path exists and is non-symlinked. All
launcher-recorded file hashes for the run/task/result records, invocation,
metrics, usage, generation prompt/output/last message, trusted prompt,
translator, canonical, candidate prompt, and candidate translator matched.
Every per-file evidence hash recorded by `/generation-result.json`, including
the JSONL trace, also matched.

Because the launcher does not declare its aggregate tree-hash serialization,
the reviewer additionally computed an independent kind/path/content digest and
recorded every candidate file SHA-256. This is not compared as if it were the
same serialization. The integrity decision rests on matching declared file
hashes, complete per-file inventories, and direct recursive comparison.

### Supplied-semantics integrity

The trusted `/reference/reference-semantics` mount is present, as required by
the rendered mode. Recursive type/path/content comparison found exactly 25
entries in each of the trusted and candidate semantics trees, zero mismatches,
and zero symlinks or other special entries. There are no missing, additional,
mistyped, changed, or symlinked semantics files.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
The candidate mount contains all five required proof deliverables:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`.

Stage 1 therefore passes; there is no infrastructure breach.

Evidence:

- [stage1_integrity.py](/audit-output/evidence/stage1_integrity.py)
- [stage1_integrity.log](/audit-output/evidence/stage1_integrity.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks `how_many_times(string: str, substring: str) -> int`
to count all occurrences of `substring` in `string`, including overlapping
occurrences. The documented results are `0` for `("", "a")`, `3` for
`("aaa", "a")`, and `3` for `("aaaa", "aa")`.

The trusted canonical scans every starting boundary from zero through
`len(string) - len(substring)`. Consequently, the empty pattern occurs at all
`len(string) + 1` boundaries. The source contract states no length bound.

### Generated implementation and translation

The submitted implementation uses:

1. `len(string) + 1` when `substring == ""`;
2. `0` when the string is empty and the pattern is nonempty;
3. otherwise, the current `startswith` indicator plus a recursive call on
   `string[1:]`.

As a mathematical recurrence over finite strings, this is the overlapping
occurrence count. Trusted regeneration with

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

exited 0. Both `.mpy` files have SHA-256
`834583ae32fd1dd0b9cf76e7b3aa3fc0e9e1878fce4cda8acbddc80193bb0ae7`.

### Independent differential test

The reviewer loaded the trusted canonical and generated entry points from
separate source files and exercised 4,954 pairs:

- all prompt examples;
- both empty/empty and one-sided-empty boundaries;
- first-position match and non-match;
- longer pattern, equal strings, and self-overlap cases;
- Unicode, emoji, and embedded-NUL cases;
- all 3,937 `ab` pairs with source length at most 6 and pattern length at most
  4;
- 1,000 deterministic generated pairs with source length at most 80 and
  pattern length at most 12;
- three 1,200-character recursion-boundary cases.

There were two mismatches. For `"a" * 1200` with pattern `"a"` or `"z"`, the
canonical returns `1200` or `0`, while the generated recursive Python raises
`RecursionError` under the recorded CPython recursion limit of 1,000. The
long-string empty-pattern case returns directly and agrees.

This is a material generated-program/source-contract discrepancy on the
unrestricted `str, str` domain. It also identifies a language-model boundary:
the supplied K semantics models unbounded call recursion and does not model
CPython's resource exception.

Evidence:

- [differential.py](/audit-output/evidence/differential.py)
- [stage2_commands.sh](/audit-output/evidence/stage2_commands.sh)
- [stage2_commands.log](/audit-output/evidence/stage2_commands.log)

## 3. Clean proof reconstruction

The candidate proof sources and the trusted supplied semantics were copied to
`/tmp/audit-work/fresh`. Candidate caches and built definitions were not
copied. The absence of `runtime-kompiled` and `verification-kompiled` was
checked before building.

The fresh commands and results were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
# exit 0

krun concrete-tests.mpy --definition runtime-kompiled
# exit 0; final <k> .K and <exit-code> 0

kompile verification.k --backend haskell \
  --main-module HOW-MANY-TIMES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
# exit 0

kprove spec.k --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC
# #Top; exit 0
```

The original spec contains two positive claims. A reviewer-labeled,
otherwise-identical copy was used to decompose the proof graph:

- the accumulator claim alone printed `#Top` and exited 0;
- the entry claim printed `#Top` and exited 0 when the separately proved
  accumulator claim was marked trusted for that single-target replay.

Running the entry claim with the helper removed does not represent the
candidate's proof graph and was stopped after it continued symbolic unrolling;
this diagnostic is not a candidate failure. The original unmodified two-claim
module had already closed.

Fresh reconstruction therefore confirms verification under the submitted
extended theory. It does not validate that theory.

Evidence:

- [stage3_commands.sh](/audit-output/evidence/stage3_commands.sh)
- [stage3_commands.log](/audit-output/evidence/stage3_commands.log)
- [stage3_individual_claims.sh](/audit-output/evidence/stage3_individual_claims.sh)
- [stage3_individual_claims.log](/audit-output/evidence/stage3_individual_claims.log)

## 4. Adequacy and real-program pinning

### Claims in plain language

The first claim has no side condition. For every source sequence `S`,
nonempty pattern `PC :: PS`, integer accumulator `A`, and continuation
`CONT`, it says that running the fresh proof item
`#overlapAcc(S, PC :: PS, A)` produces
`A + overlapCount(S, PC :: PS)` and then resumes `CONT`.

The entry claim quantifies over all `IntSeq` sources and patterns. It starts at
a direct call of a closure with:

- parameter names exactly `("string", "substring")`;
- body `howManyTimesBody`;
- defining scope 0;
- two string arguments;
- a module-scope binding of `how_many_times` to that same closure;
- the supplied builtins scope at -1;
- normal return/exception/exit cells;
- a `NEXT` scope location absent from the scope map.

It claims the call returns exactly `overlapCount(S, P)` and resumes an arbitrary
continuation, with the listed cells unchanged at the claim boundary.

### Satisfiable preconditions and ground substitution

A concrete entry state satisfies the precondition with `S = P = .IntSeq`,
`env = 0`, module scope 0 containing only the stated closure, builtins scope
-1, `scopeLoc = 1`, empty heap and stack, `ret = noRet`, `exc = NoExc`, and
exit code 0. The claimed result is 1. A second witness uses `"aaaa"` and
`"aa"` and has claimed result 3. Ground K claims printed `#Top`; the trusted
canonical and generated Python both returned 1 and 3 for these two small
witnesses.

Evidence:

- [ground_witness_commands.sh](/audit-output/evidence/ground_witness_commands.sh)
- [ground_witness_commands.log](/audit-output/evidence/ground_witness_commands.log)

### Mechanical constructor identity

Trusted translator regeneration first pins `solution.py` to `solution.mpy`.
For the source-to-claim comparison, the reviewer formed a complete module term
whose function binding uses `howManyTimesBody`. Both that term and the
submitted `solution.mpy` were parsed with the freshly built verification
definition and `--expand-macros`, then emitted as KORE. `cmp` exited 0 and both
expanded terms have SHA-256
`1c133d3a0323c5205af76674b0115878f616b7295665211a5e84dd09866c5fed`.

Thus the closure body named in the entry claim is constructor-identical to the
submitted function body. Beginning at an already constructed direct closure
call is acceptable in principle because the module binding and body are pinned.

Evidence:

- [pinning_commands.sh](/audit-output/evidence/pinning_commands.sh)
- [pinning_commands.log](/audit-output/evidence/pinning_commands.log)

### Execution is nevertheless bypassed

Constructor identity is not execution identity. The rule at
`/candidate/verification.k:106-118` is:

```text
<k> #applyK(toCall(closureVal(
       ("string", "substring"), howManyTimesBody, 0)),
     (str(S), str(P), .Vals)) ~> CONT
 => #overlapEval(S, P) ~> CONT </k>
[priority(30)]
```

It replaces the closure invocation before the fixed closure-call rule can
allocate a frame, bind parameters, evaluate either guard, resolve `len`,
resolve `startswith`, slice, resolve the recursive binding, recurse, return,
or pop the frame. The term is pinned, but no material operation in its body is
executed in the successful entry proof.

### Body-sensitivity false-conclusion witness

In a separate scratch definition, the actual macro body used by both the claim
and bridge was materially changed to `Return(Int(999))`. This changes the
program term that the claim invokes; it is not an edit to an ignored external
source file.

Under the fixed LLVM semantics:

- an assertion that the mutated function returns 999 passed with exit 0;
- an assertion that it returns 1 for `("", "")` failed with `AssertionError`
  and exit 1.

The mutated Haskell proof definition built successfully, yet the unchanged
specification still printed `#Top` and exited 0. For the satisfiable empty/empty
entry state, that proof asserts overlap result 1 for a body that concretely
returns 999. This is a concrete false result and demonstrates that the
successful theorem is insensitive to the body semantics.

Evidence:

- [body_sensitivity_commands.sh](/audit-output/evidence/body_sensitivity_commands.sh)
- [body_sensitivity_commands.log](/audit-output/evidence/body_sensitivity_commands.log)

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated inventory contains every top-level sentence in
`reference-semantics/semantics.k`, all 24 supplied helper K files,
`verification.k`, and `spec.k`. It records source span, kind, attributes,
special flags, decision, reason, and normalized sentence.

The 1,110 inventoried sentences comprise:

- 705 rules;
- 230 syntax declarations;
- 5 contexts;
- 1 configuration;
- 2 claims;
- 25 `requires`, 88 imports, 27 modules, and 27 endmodules.

Flagged sentences include 146 functions, 108 total declarations, 46 priority
rules, 38 concrete rules, 26 `owise` rules, 25 symbols, 22
`no-evaluators` declarations, 5 macros, 1 recursive macro, 2 strict and 1
sequence-strict declarations. There are no local `functional` or
`simplification` declarations.

All 1,087 sentences originating in the recursively verified trusted semantics
tree are classified as the selected fixed-semantics baseline. The 22 opaque
symbols belong to fixed float, MD5, and sorting support. None occurs in the
submitted program, `overlapCount`, the proof machine, or either claim. Missing
semantics for unrelated constructs is therefore irrelevant.

The full per-sentence decision is preserved rather than collapsed into an
uncheckable prose assertion:

- [rule_inventory.py](/audit-output/evidence/rule_inventory.py)
- [rule-inventory.tsv](/audit-output/evidence/rule-inventory.tsv)

### Used fixed-semantics map

The translated program uses `Module`, `FuncDef`, `Params`, statement
sequencing, `If`, `Return`, `Compare`, `Name`, `Str`, `Int`, `BinOp`, `IfExp`,
`Call`, `Attribute`, `Subscript`, `Slice`, and `NoBound`.

Their material rules are supplied by:

- `syntax.k`: constructor declarations and evaluation strictness;
- `core.k`: configuration, values, statement sequencing, name lookup,
  left-to-right argument evaluation, literals, `isLen`, and builtins scope;
- `functions.k` and `call.k`: closure creation, closure dispatch, parameter
  binding, return, and frame pop;
- `controls.k`: `If` and `IfExp`;
- `operators.k`, `int.k`, and `str.k`: comparison and addition;
- `builtins.k`: `len`;
- `methods.k`: `startswith` and its total `startsWith` helper;
- `subscript.k`: evaluation and construction of the `string[1:]` slice.

For this used subset, the fixed rules preserve left-to-right evaluation and
normal frame control. The relevant guarded equations are disjoint and
descending. `startsWith` covers empty pattern, empty source with nonempty
pattern, and two nonempty sequences. The slice rules evaluate all three bounds
and build the suffix with step 1. No opaque result influences the body.

The fixed semantics is intentionally not full CPython. In particular it does
not model CPython recursion limits; that limitation is material here because
the generated implementation is recursively linear in source length.

### Proof-local extension inventory

The ten rules in `verification.k` are decided as follows.

1. **`howManyTimesBody` macro, lines 9-27 — accepted as syntax pinning only.**
   Macro expansion is mechanically identical to `solution.mpy`. It supplies no
   semantic theorem.

2. **Three `overlapCount` equations, lines 32-41 — accepted mathematical
   definition.** The cases are disjoint and total: empty pattern; empty source
   with nonempty pattern; and two nonempty sequences. The recursive case removes
   one source element. Its prefix indicator and recursion exactly count every
   starting position, including overlaps.

3. **Three `#overlapEval` rules and two `#overlapAcc` rules, lines 49-101 —
   accepted internal proof machine.** These operate only on fresh proof-local
   K items. Their bases agree with `overlapCount`; each accumulator step removes
   one source element and adds the current prefix indicator. The nonempty
   pattern restriction is preserved from construction to the accumulator
   claim. These rules characterize the separately authored summary machine,
   not the Python body.

4. **Closure-call rule, lines 106-118 — rejected operational bridge.** It is
   the only proof-local priority rule and the only extension that replaces
   fixed execution. It has no guard beyond exact closure/argument syntax, reads
   no configuration cell other than `<k>`, accepts arbitrary continuation and
   arbitrary environment/scopes/heap/stack/return/exception state, and
   preserves every omitted cell. Fixed execution instead creates a frame,
   changes `env`, `scopes`, `scopeLoc`, and `stack`, binds parameters, evaluates
   body operations through the scope chain, and later returns and pops.

The bridge has no bridge-free universal connection theorem over its match
domain. The accumulator claim proves only the fresh machine's recurrence; it
does not connect that machine to fixed closure execution. Reusing
`overlapCount` in the bridge target and entry postcondition is circular.
Priority 30 merely ensures the shortcut wins; it supplies no justification.

### Actual-rule context witness

The bridge's complete match domain is demonstrably broader than fixed
execution. With the actual submitted body and valid empty string inputs, choose
an otherwise empty scope map. The bridge-enabled definition proves return value
1 and prints `#Top`. A separately rebuilt fixed-only definition, containing
the same macro but not the bridge, gets as far as
`#look("len", 0)` and fails with `WarnStuckClaimState`; the absent builtin
binding cannot be fabricated.

This is a concrete operational false-conclusion witness for the rule as
submitted: its accepted context returns a value where fixed semantics cannot
perform the lookup or return. The body-sensitivity witness above separately
shows a false value even in a well-formed module/builtins context after a
material body change.

Evidence:

- [bridge_context_commands.sh](/audit-output/evidence/bridge_context_commands.sh)
- [bridge_context_commands.log](/audit-output/evidence/bridge_context_commands.log)
- [bridge-fixed-only.raw.log](/audit-output/evidence/bridge-fixed-only.raw.log)

Gate A fails. The candidate's reconstructed `#Top` is unusable as a proof of
the real program.

## 6. Fresh non-vacuity test

The reviewer created a distinct spec that preserves the accumulator claim but
changes the entry result from `overlapCount(S, P)` to
`overlapCount(S, P) + 1`. The mutation is false for the satisfiable
empty/empty witness: the required result is 1, while the mutation demands 2.

The mutated spec's `--dry-run` exited 0, confirming successful parsing and KORE
construction. The actual proof exited 1 with `WarnStuckClaimState` and an
implication residual containing:

```text
isLen(S) +Int 1  #Equals  isLen(S) +Int 2
```

The backend then reported that the configuration could not be rewritten
further. This is the expected unmet result obligation, not a parser error,
timeout, missing import, or unrelated crash.

The original theorem is therefore result-constraining and non-vacuous in this
narrow sense. Non-vacuity does not repair the operational bridge that supplies
the constrained result.

Evidence:

- [nonvacuity_commands.sh](/audit-output/evidence/nonvacuity_commands.sh)
- [nonvacuity_commands.log](/audit-output/evidence/nonvacuity_commands.log)
- [nonvacuity-kprove.raw.log](/audit-output/evidence/nonvacuity-kprove.raw.log)

## 7. Proven-versus-assumed accounting

### What the successful reachability proof actually establishes

Under the theory formed by the supplied semantics plus all candidate
verification rules:

1. the fresh `#overlapAcc` machine computes its accumulator plus the recursive
   `overlapCount` definition; and
2. the exact submitted closure-call term rewrites, by the candidate's
   priority-30 axiom, to the fresh `#overlapEval` machine and therefore to
   `overlapCount`.

The successful proof does **not** establish that fixed semantics executes the
submitted body to `overlapCount`. That missing statement is exactly the
bridge-free connection theorem required before the operational bridge could be
used.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Supplied MPY semantics | All fixed execution, state, and control | Trusted selected semantics after recursive candidate/trusted identity check. Used rules were additionally mapped and reviewed. |
| K integer, Boolean, map, list, string, and equality hooks | Mathematical and configuration primitives | Ordinary K trust boundary; no candidate-local replacement. |
| Trusted `py2mpy.py` | Python AST to constructor term | Byte-identical candidate copy; trusted regeneration is byte-identical to `solution.mpy`. |
| `howManyTimesBody` macro | Program identity | Mechanically constructor-identical after macro expansion; acceptable only as syntax pinning. |
| `overlapCount`, `startsWith`, and accumulator equations | Intended mathematical result | Guard-complete, disjoint, descending equations; accepted as mathematics. |
| Fixed opaque float/MD5/sort symbols | Potential values in unrelated programs | Unused by this program and proof; no dependency. |
| Priority-30 closure bridge | Binding, body execution, control, and final value | Illegitimate. It is program-derived, result-bearing, unsupported by a connection theorem, globally broader than fixed execution, and enables the recorded false conclusions. The entry claim depends on it. |
| Differential Python tests | Implementation-to-canonical evidence on 4,954 inputs | Finite empirical evidence only. They do not prove universal equivalence and expose two long-input mismatches. |
| K-versus-CPython recursion resources | Long-input source behavior | Not modeled by supplied semantics; generated Python raises `RecursionError` on valid unrestricted-domain inputs. |

### Gate and decision summary

- Gate A, real-program soundness: **FAIL**. The operational bridge bypasses
  execution and has concrete fixed-versus-extended and body-sensitivity false
  witnesses.
- Gate B, intent adequacy: **FAIL independently** for actual CPython execution
  on unrestricted strings, because the generated recursive implementation
  raises `RecursionError` where the canonical returns normally.
- Gate C, evidence auditability: reviewer evidence is reproducible, but later
  evidence cannot cure Gate A or B.

The clean `#Top`, ground agreement on small cases, constructor identity, and
fresh non-vacuity failure show that this is a carefully constrained theorem
about the extended summary theory. They do not make it a proof of the real
generated program. Under the benchmark decision boundary, an
execution-bypassing, result-bearing rule without a universal connection
theorem is `FAIL / NOT_LEGIT`; the material unrestricted-domain discrepancy is
an additional failure.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
