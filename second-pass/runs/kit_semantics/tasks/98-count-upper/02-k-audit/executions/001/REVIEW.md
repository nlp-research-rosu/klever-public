# Independent adversarial review: 98-count-upper

The candidate contains a legitimate partial-correctness proof of the generated
program under the supplied MPY semantics. I did not use the candidate's compiled
definitions, `prove.log`, `PROOF.md`, mutation files, or generation report as
proof. All executable checks below used trusted inputs and fresh definitions
under `/tmp/audit-work/98-count-upper`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `98-count-upper`, and condition
`kit-semantics`. The mounted inputs agree with that declaration:

- `/reference/reference-semantics` exists as required. There is no semantics-mode
  contradiction.
- `/audit-campaign-lock.json` is a regular file, has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its JSON object is exactly the `audit_campaign` block in
  `/audit-input.json`.
- All 14 launcher-declared `container_paths` resolve to real regular files or
  real directories of the declared kind.
- The required pipeline-v3 records were present and readable:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace. All recorded
  per-file SHA-256 values matched.
- The one structured trace file is regular JSONL. All 530 records parsed
  (`session_meta=1`, `turn_context=1`, `world_state=1`, `event_msg=158`,
  `response_item=369`). The generation prose and trace were treated only as
  untrusted historical claims.
- Independent pipeline-v3 tree digests were
  `4e06397a...e3789f` for the trusted semantics,
  `7c1b091e...677af` for the candidate workspace, and
  `709621a9...7b8` for the trace; these match the task/result/usage records that
  specify that digest format. The additional launcher-owned aggregate values
  recorded in `/audit-input.json` were read but were not substituted for direct
  inspection.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounts. Candidate and trusted `reference-semantics/` inventories are
  identical across all 25 entries. Every corresponding file hash matches, there
  are no missing or additional entries, and neither tree contains a symlink or
  unsupported entry.
- All six required candidate deliverables are real, nonempty regular files.

The authoritative check and complete hashes are in
`evidence/01_integrity.py` and `evidence/01_integrity_final.log` (exit 0).
Earlier `01_integrity.log` records a reviewer-script assertion that was too
strict about an audit-only `config` field; the corrected check is retained in
the final log. There is no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks: for an arbitrary string `s`, return the number of
characters that are uppercase vowels (`A`, `E`, `I`, `O`, `U`) at zero-based
even indices. The trusted canonical implementation loops over indices
`0, 2, 4, ...` and increments on membership in `"AEIOU"`.

The submitted `solution.py` is a different but equivalent algorithm. It keeps
the unprocessed suffix in `remaining`; while nonempty, it tests
`remaining[0]`, adds the resulting Boolean to the integer accumulator, and
replaces `remaining` by `remaining[2:]`.

I regenerated the constructor program with the trusted translator:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/98-count-upper/solution.regenerated.mpy
cmp /candidate/solution.mpy \
  /tmp/audit-work/98-count-upper/solution.regenerated.mpy
```

Both files have SHA-256
`224a6e85200c1f37897eca76417f136b18c8fd5d1c2eefe0027bf51c3b817ba2`;
`cmp` exited 0.

The independent differential script imports the trusted canonical and generated
entry points from their separate files. It checks:

- all three documented examples;
- empty, one-character, two-character, odd/even length, true/false membership,
  and parity-placement boundaries;
- exhaustive strings of lengths 0 through 4 over
  `AEIOUaeiouBZ🙂`;
- 20,000 deterministic strings of lengths 0 through 128 drawn from NUL, ASCII,
  BMP, astral, maximum Unicode, and lone-surrogate code points;
- two long inputs of lengths 10,000 and 10,001.

There were 50,962 cases and zero mismatches. The input stream digest was
`fe9cdfb2...c6ed7`. Script, exact command, scope, results, and exit 0 are in
`evidence/02_differential.py`, `evidence/02_fidelity.sh`, and
`evidence/02_fidelity.log`.

## 3. Clean proof reconstruction

Only source artifacts were copied to scratch: the trusted semantics, translator,
prompt, canonical implementation, and candidate `solution.py`, `solution.mpy`,
`verification.k`, and `spec.k`. Candidate `runtime-kompiled/`,
`verification-kompiled/`, caches, and logs were not copied or used.

The toolchain was K v7.1.293 and Python 3.10.12
(`evidence/00_toolchain.log`). The fresh commands and outcomes were:

| Purpose | Exact command (working directory `/tmp/audit-work/98-count-upper`) | Exit | Relevant output |
|---|---|---:|---|
| LLVM definition | `kompile --backend llvm reference-semantics/semantics.k --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-fresh-kompiled` | 0 | fresh definition built |
| Concrete execution | `krun 03_concrete_cases.mpy --definition runtime-fresh-kompiled` | 0 | `.K`, `NoExc`, exit code 0 |
| Haskell definition | `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-fresh-kompiled` | 0 | fresh definition built |
| Loop claim | `kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC --claims SPEC.loop-invariant` | 0 | `#Top` |
| All positive claims | `kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC` | 0 | `#Top` |
| Ground entry witnesses | `kprove audit-ground.k --definition verification-fresh-kompiled --spec-module AUDIT-GROUND` | 0 | `#Top` |

The loop-only command and the all-claims command are the candidate's two intended
positive proof commands. The latter independently includes and closes both
`SPEC.loop-invariant` and `SPEC.count-upper`; thus every positive target claim
was reconstructed.

The reviewer concrete harness uses the exact submitted function body and 15
normal/boundary assertions. Its source and trusted translation are
`evidence/03_concrete_cases.py` and `evidence/03_concrete_cases.mpy`.
Command logs are `03_runtime_build.log`, `03_concrete_run.log`,
`03_verification_build.log`, `03_prove_loop.log`, `03_prove_all.log`, and
`04_ground_prove.log`.

The LLVM compiler emitted supplied-semantics exhaustiveness warnings for
unrelated helpers such as `mapStrVS`, float helpers, and `valSeqAt`; the
Haskell/proof runs emitted only unused-variable warnings in the fixed `strLt`
rules and for the deliberately framed `ORIGINAL` variable. No warning identifies
a proof-local coverage or soundness problem.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` has no `requires` clause. Its starting state contains the
exact internal `#while` generated from the submitted body, environment location
1, and an exact ordinary local frame:

- `s = str(ORIGINAL)`;
- `count = ACC`;
- `remaining = str(CODES)`.

It says normal loop completion consumes that `#while`, changes `remaining` to
the empty string, and changes `count` to
`ACC + countUpperEven(CODES)`. It preserves `s`, the arbitrary continuation
framed by `<k> ... </k>`, all other scopes, and every omitted configuration
cell.

`SPEC.count-upper` also has no `requires` clause, so its formal string domain is
all `CODES:IntSeq`, with no length, ASCII-input, nonempty, or finite enumeration
restriction. It starts from an exact call to `count_upper`, with the module
binding fixed to the exact parameter and closure body, and with the supplied
semantics' initial environment, scopes, allocation counters, empty heap/stack,
return state, exception state, and exit code. It says the call returns exactly
`countUpperEven(CODES)` while restoring/preserving those cells.

### Mechanical program identity

Trusted regeneration establishes source-to-constructor identity. The independent
pinning script then:

1. parses `solution.py` with CPython's AST and verifies the sole entry function,
   argument, and four-statement shape;
2. extracts the regenerated `FuncDef` constructor body;
3. requires the entry scope to contain exactly the corresponding
   `closureVal(("s", .ParamNames), BODY .Stmts, 0)` once;
4. requires the loop claim's `#while` condition and body constructors to match
   the `While` constructor exactly; and
5. verifies the entry result is constrained to `countUpperEven(CODES)`.

`evidence/04_pinning.py` and `04_pinning.log` record all checks passing. This is
the permitted direct-function-binding form: the theorem need not replay module
loading because it executes the same mechanically matched binding and body.
Fresh concrete module execution separately confirms that module loading creates
that closure.

### Satisfiable states and substituted results

Both entry and loop preconditions are satisfiable. For the loop, take
`ORIGINAL=CODES=.IntSeq` and `ACC=0` in the displayed frame. For the entry,
each ground claim in `evidence/04_ground.k` is a complete satisfying
configuration:

- empty codes return 0;
- codes for `"aBCdEf"` return 1;
- codes for `"AEIOU"` return 3.

The fresh K ground proof closed with `#Top`. Both Python implementations return
the same respective values. The universal claim covers arbitrary length; the
ground claims are witnesses and sensitivity evidence, not substitutes for the
universal theorem.

There is no source-domain narrowing. The semantics' `str(IntSeq)` is a sequence
of mathematical integer codes, which contains every Python string representation
needed here (and a harmless larger set). The only source literal translated by
the body is ASCII `"AEIOU"`, within the supplied literal rules.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.md`, generated by
`evidence/05_inventory.py`, contains one row with source lines, normalized
text, attributes, and disposition for every local declaration in the supplied
semantics, `verification.k`, and `spec.k`. It inventories:

- 698 rules, 228 syntax declarations, 5 contexts, 1 configuration, and 2 claims;
- every `[function]`, `[total]`, `[functional]`, `[simplification]`,
  `[priority]`, `[owise]`, `[concrete]`, `[symbol]`, `[no-evaluators]`, macro,
  strictness, and sequencing attribute;
- 22 fixed opaque declarations, all target-unreachable; and
- every module/import/require edge.

The supplied tree is fixed trusted input in this condition, not a candidate
extension. I nevertheless traced every row by top symbol, operand sort, and
guard. The inventory marks 114 declarations/rules on the concrete-load or
target-proof path. The remaining fixed rows cannot match a target term (for
example float, sort, dict, list, set, comprehension, method, range, MD5, or
unrelated builtin operations). K rewriting does not gain an `ex falso` principle
from an unreachable LHS. The task-text screen found no occurrence of
`count_upper`, `countUpperEven`, `AEIOU`, or the task's `remaining` name in the
fixed semantics.

### Used constructs and fixed-rule path

The constructor map is:

- `Module`, `FuncDef`, `Params`, statement sequencing, and closure creation:
  `syntax.k:41-61`, `core.k:49-60,123-127`,
  `functions.k:8-16`;
- `Call`, callee lookup, left-to-right argument evaluation, exact closure
  dispatch, frame allocation, parameter binding, return, and pop:
  `core.k:129-191`, `call.k:18-21,69-75`,
  `functions.k:62-90`;
- `Assign`, `AugAssign`, `While`, loop re-entry, and local-scope writes:
  `controls.k:8-31,65-85`, with generated strictness from
  `syntax.k:41-50`;
- `Name`, `Int`, string truthiness, integer-plus-Boolean:
  `core.k:129-154,193-210`, `int.k:9-12`;
- ordered `Compare` evaluation and string membership:
  `operators.k:14-17`, `str.k:28-41`;
- string literal construction:
  `str.k:12-17` (the used literal is ASCII);
- string index 0 and slice `[2:]`:
  `subscript.k:16-19,25-42,43-121`, using only step `1`, an in-bounds
  index on the nonempty branch, and the truthful `isLen`, `clampHi`, and
  `buildIS` cases.

Configuration/state analysis agrees with the claims. The call pushes a frame,
uses fresh scope 1, binds `s`, updates only `count` and `remaining`, records the
return transiently, then pops the frame and restores environment, scope
counter, stack, and return state. No target operation allocates heap objects,
prints output, mutates external state, or can raise a modeled exception under
the invariant. The loop condition is reevaluated each time; indexing occurs
only after nonempty string truthiness has selected the body.

Priority/overlap checks also pass:

- specialized math/hashlib `Call` rules do not match `Name("count_upper")`, so
  the generic `[owise]` call route is selected;
- cell-variable lookup/write rules require a `"$cells"` binding absent from
  the exact ordinary frame;
- reference-specific assignment, comparison, subscript, and while rules cannot
  match the target's `Int`, `Bool`, and `str` values;
- the nonempty and empty `strPrefix`, `strContains`, slice, and loop guards are
  disjoint or have agreeing results.

The reproducible searches and overlap list are in
`evidence/05_static_checks.sh` and `05_static_checks_rerun.log` (exit 0).
The earlier `05_static_checks.log` records a reviewer regex typo and is not a
candidate finding.

### Proof-local extensions, individually

1. `countUpperEven(.IntSeq) => 0` is the truthful base case.
2. The guarded nonempty `countUpperEven(CODES)` rule adds 1 exactly when the
   first one-code string is contained in `"AEIOU"`, then recurses on precisely
   the `[2:]` suffix. For length 1, `clampHi(2,1,1)=1`; for length at least 2,
   the start is 2. Thus its recursive argument is strictly shorter. Empty and
   nonempty cases are disjoint and exhaustive over constructor `IntSeq`s, so the
   `[function,total]` declaration is justified on every target use. This is a
   definitional result summary, not an operational bridge.
3. `(A +Int B) +Int C => A +Int (B +Int C)` is integer associativity. It is
   globally true, has no guard overlap, touches no cell or control term, and
   terminates as a right-association normalization because it reduces the
   left-nested spine.
4. `SPEC.loop-invariant` is a reachability circularity rather than a rewrite in
   the executable definition. Its match and justification domains have the
   same exact loop, local frame, arbitrary continuation, and framed cells. The
   empty branch is immediate; the nonempty branch performs the real body,
   reaches the same loop head with the suffix, and closes using items 1-3.
5. `SPEC.count-upper` is the bridge-free universal connection theorem: fixed
   call/name/binding/frame/body/return rules execute the exact program and use
   the loop claim. It does not intercept or replace a program term.

There are no proof-local priority rules, opaque symbols, trusted primitives,
concrete-only rules, call interceptions, abrupt-control bridges, or
unconstrained result oracles. No unsound candidate rule was identified, so
there is no false-conclusion witness to report against a purported unsound rule.

The mathematical meaning of `countUpperEven` follows by structural induction:
the empty sequence contributes zero; a nonempty sequence contributes the
membership indicator for index 0 and recurses after dropping two positions.
Those recursive heads are exactly the original positions 2, 4, 6, and so on.

## 6. Fresh non-vacuity test

I ignored the candidate's mutation files and authored two new specifications.

The required false-result mutation is
`evidence/06_false_result.k`. Its complete precondition is the satisfiable
entry state for `"A"`, while its destination deliberately requires 0 rather
than 1.

```text
kprove audit-false-result.k --definition verification-fresh-kompiled \
  --spec-module AUDIT-FALSE-RESULT --dry-run
```

This build-only run exited 0 (`06_false_result_build.log`). The same command
without `--dry-run` exited 1, emitted `WarnStuckClaimState`, and showed the
reachable residual `<k> 1 ~> .K </k>` failing to unify with the destination 0
(`06_false_result_prove.log`). This is the expected unmet result obligation,
not a parser, import, backend, timeout, or unrelated failure.

For body sensitivity, `evidence/06_body_mutation.k` changes the constructor
actually executed by the claim from `Assign(..., Int(0))` to
`Assign(..., Int(1))`, while retaining the original empty-input result 0. Its
dry run exited 0; its proof exited 1 with the same meaningful residual result 1
(`06_body_mutation_build.log`, `06_body_mutation_prove.log`). This confirms
that the theorem depends on the closure body, not an external source filename.

## 7. Proven versus assumed accounting

### Precisely proven

Under the exact supplied MPY theory and the exact initial configuration in
`SPEC.count-upper`, for every constructor string code sequence `CODES`, symbolic
execution of the submitted `count_upper` closure reaches a returned integer
equal to `countUpperEven(CODES)`. The helper definition is exactly the count of
uppercase ASCII vowels at zero-based even positions. The proof also establishes
normal return with restored environment/scope allocation/stack/return state,
unchanged empty heap, `NoExc`, and exit code 0. This is partial correctness;
total termination is not the reachability theorem being claimed.

### Trust ledger

| Boundary | Effect and dependents | Judgment/evidence |
|---|---|---|
| Supplied `reference-semantics` | Defines all value, lookup, state, call, control, string, indexing, slicing, and return behavior used by both claims | Stipulated fixed boundary; candidate copy is recursively identical. Target-path rules were statically traced and concretely exercised. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy`; all program-pinning conclusions depend on it | Translator correctness is not formally proved, but byte regeneration, AST/constructor pinning, concrete MPY execution, and the 50,962-case independent differential support the exact bridge used here. |
| K v7.1.293 Haskell/LLVM backends and host runtime | Compilation, rewriting, reachability, and concrete execution | Standard unavoidable proof-infrastructure trust; fresh independent builds and runs were used. |
| K mathematical primitives | Unbounded integers, Booleans, equality, maps/lists, and string-code primitive operations | Ordinary low-level semantics boundary. The proof-local result is not hidden behind an opaque primitive. |
| Fixed opaque float/sort/MD5 and other total abstractions | None: their top symbols and operand sorts never occur on the target/load path | Imported but target-unreachable; no claim depends on their interpretation. |
| Natural-language adequacy | Identifies the recursive helper with “uppercase vowels at even indices” | Direct structural definition and induction above, plus canonical differential and ground K witnesses; no narrowed domain or empirical-only result oracle. |
| Termination | Not asserted by the K reachability result | Explicitly excluded. Operationally, each loop iteration shortens a finite string by one or two characters, but the audited result is partial correctness. |

Differential and concrete evidence support only source/translator/intent bridges;
they are not substitutes for the successful universal K proof.

Gate A passes: the real body executes, local equations are valid, the result is
constrained, and both result and body mutations are rejected. Gate B passes:
the unrestricted string domain and exact requested result are covered. Gate C
passes: all trust boundaries and finite evidence are explicit and reproducible.
There is no material adequacy gap or non-fatal limitation requiring a concerns
classification.

VERDICT: PASS
LEGITIMACY: LEGIT
