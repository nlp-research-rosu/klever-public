# Independent adversarial audit: 140-fix-spaces

The candidate reconstructs a genuine, result-constraining reachability proof of
its submitted recursive program under its generated K semantics. It does not,
however, prove the trusted HumanEval reference behavior on the full intended
domain. The generated program, its `fixRef` postcondition, and the K execution
all return `"__"` on the valid input `"  "`, while the trusted canonical entry
point returns `"_"`. This is a material implementation/specification
disagreement, so the candidate is not a legitimate proof of the requested
target despite the sound local K theorem.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = GENERATED_SEMANTICS`. I independently inspected
`/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, and all required records under
`/generation-evidence/`: `invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
Historical runtime metrics are not required for this layout.

The integrity gate passes:

- The campaign block in `/audit-input.json` is exactly equal to
  `/audit-campaign-lock.json`, and the lock's SHA-256 is the recorded
  `ad5dfc...d745`.
- Every required record is a readable regular non-symlink. All launcher-recorded
  file hashes checked by the audit match.
- The retained candidate tree has the generation pipeline digest
  `4f81f3...e318`, exactly matching `invocation.json`'s retained-workspace
  digest. The trace tree digest is `587fdd...4c1d`, exactly matching
  `usage.json`.
- The one JSONL trace file has 178 valid structured records and no parse
  errors. I inspected its command/result events and the generation log; their
  prior `#Top` and success report were treated only as untrusted claims.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`. The trusted canonical,
  prompt, and translator hashes match the launcher record.
- All eight candidate deliverables are regular files; the candidate tree has
  no symlinked or mistyped entry.
- `/reference/reference-semantics` is absent, as required for
  `GENERATED_SEMANTICS`. There is no supplied or inferred hidden semantics.

The complete checks, mounted file hashes, generation evidence hashes, and trace
inventory are in `evidence/01_integrity.log`; the checker is
`evidence/01_integrity_check.py`. The provenance is intact, so this is a
candidate verdict rather than `AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The prompt says that ordinary spaces become underscores and a run of more than
two consecutive spaces becomes one hyphen. Its four examples exercise no
space, one internal space, leading/ordinary spaces, and a three-space internal
run.

The trusted canonical implements an additional observable boundary behavior:
an internal run of one or two spaces produces that many underscores, but a
terminal run of one or two spaces produces only one underscore
(`/reference/canonical.py`, lines 32-35). Thus:

```text
canonical.fix_spaces("  ") == "_"
```

The generated recursive implementation converts each member of a one- or
two-space run to an underscore, including at the end, and collapses runs of at
least three spaces to one hyphen:

```text
generated.fix_spaces("  ") == "__"
```

This generated behavior is a defensible literal reading of the prose, but it
is not the behavior of the trusted HumanEval canonical. Both artifacts were
required inputs to this audit; the concrete canonical disagreement cannot be
silently replaced by the candidate's preferred interpretation.

### Trusted regeneration and differential evidence

Running the trusted translator from the scratch copy produced
`regenerated-solution.mpy` with SHA-256
`1cf1f5...8fd01`, byte-identical to the submitted `solution.mpy`.

The independent differential test imports the trusted canonical and generated
entry points under separate module names. It covers all four documented
examples, 25 explicit empty/branch/boundary/Unicode cases, all 3,280 strings
over `{" ", "a", "é"}` of lengths 0 through 7, and 4,000 seeded random strings.
Among 7,116 unique inputs:

- generated-versus-canonical mismatches: **313**;
- generated-versus-an-independent literal run-based reading of the prose:
  **0**.

The first mismatch is the valid boundary input `"  "`; other witnesses include
`"a  "` (`"a_"` canonical versus `"a__"` generated) and `"a   b  "`
(`"a-b_"` versus `"a-b__"`). The script deliberately exits 1 when a canonical
mismatch exists. See `evidence/02_program_checks.log`,
`evidence/02_program_checks.sh`, and `evidence/02_differential.py`.

This is a material intended-result divergence, not a translation discrepancy
or a finite-domain restriction.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work`, used the trusted translator
there, and did not copy or use any candidate-built definition or cache. With K
v7.1.293, the following fresh commands all succeeded:

```text
kompile --backend haskell /tmp/audit-work/candidate/semantic.k \
  --main-module MPY-SEMANTIC --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-kompiled

kompile --backend haskell /tmp/audit-work/candidate/verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/verification-kompiled

kprove /tmp/audit-work/candidate/spec.k \
  --definition /tmp/audit-work/build/verification-kompiled \
  --spec-module SPEC
```

The two positive claims are mutually recursive and are submitted together in
the one `SPEC` module; the fresh command proves both. It exited 0 and printed
`#Top`. Exact commands and outputs are in
`evidence/03_reconstruct.log`; the driver is
`evidence/03_reconstruct.sh`.

I also freshly executed the generated semantics on 12 normal and boundary
inputs: empty; all four prompt examples; runs of one, two, three, and four
spaces; trailing two spaces; a mixed internal/trailing case; and Unicode.
Every `krun` exited 0 and agreed with the generated Python. On `"  "`,
`"a  "`, and `"a   b  "`, K also visibly disagreed with the canonical in the
same way as the generated Python. See
`evidence/03_concrete_compare.log` and
`evidence/03_concrete_compare.py`.

Two earlier reviewer-parser attempts for the Unicode pretty-print decoder are
retained as `evidence/03_concrete_compare_attempt1.log` and
`attempt2.log`; they were corrected and are not counted as candidate failures.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC` contains no `requires` clauses.

1. For every structural string `S`, arbitrary continuation `K`, arbitrary
   input/environment/result cells, and the fixed function table
   `solutionFuns`, calling `fix_spaces(S)` reduces to
   `pyStr(fixRef(S))`, preserving `K` and the framed cells.
2. Under the same conditions, calling `_drop_spaces(S)` reduces to
   `pyStr(dropRef(S))`.

These are result-constraining claims: the returned values are the explicit
functions `fixRef(S)` and `dropRef(S)`, not fresh variables, tautologies, or
one-way predicates. The arbitrary continuation is preserved rather than
discarded.

A concrete state satisfying each precondition is
`S = .PString`, `K = .K`, input `""`, environment `.Env`, result `.K`, and
functions `solutionFuns`. The first claim then requires the empty structural
string and the second does likewise. Another satisfying substitution is
`S = sp sp .PString`; the first claimed result reduces to `"__"`, exactly the
generated Python result but not the canonical `"_"`. For the auxiliary claim,
`S = sp sp ch("a") .PString` reduces to `"a"`, matching the generated
`_drop_spaces("  a")`. Concrete witness runs are in
`evidence/04_claim_witnesses.log`.

### Mechanical pinning

The claim starts at the function call rather than at the complete `Module`
term, so I independently checked the function binding and body:

1. the trusted translator regenerated the submitted module byte-for-byte;
2. a probe semantics retained the function cell after executing the trusted
   regenerated module;
3. a second execution loaded `solutionFuns` and retained that function cell;
4. canonical JSON for both parsed KAST function cells was exactly identical:
   22,385 bytes and SHA-256
   `6afc6c...c3d7`.

This is a constructor-level comparison of both function names, parameters,
bodies, and their collection order. See
`evidence/04_pinning_and_sensitivity.log`,
`evidence/04_pinning_compare.py`, and the probe
`evidence/pinning-verify-empty.mpy`.

The theorem therefore executes the actual submitted functions through the
ordinary interpreter rules. The manually duplicated constructor term is an
artifact-maintenance risk, but not an identity gap for this immutable
candidate.

### Body sensitivity

I changed the embedded `fix_spaces` empty-case body in the term actually used
by the claims from `return ""` to `return "X"`. The mutated definition built,
concretely returned `"X"` on the empty structural input, and the original
proof no longer closed (exit 1). The proof backend reported an undecidable
predicate rather than the clean residual required for non-vacuity, so this run
is used only as body-sensitivity evidence. The mutation and logs are
`evidence/verification-body-mutation.k`,
`evidence/spec-body-mutation.k`,
`evidence/04_body_mutation_concrete.log`, and
`evidence/04_pinning_and_sensitivity.log`.

## 5. Rule-by-rule static soundness review

The exhaustive line-numbered inventory is
`evidence/05_rule_inventory.log`, generated by
`evidence/05_inventory.py`. It contains all declarations and complete rule
blocks:

- `semantic.k`: 30 syntax declarations, one configuration, 72 rules;
- `verification.k`: four syntax declarations and 13 rules;
- `spec.k`: two claims;
- attributes: eleven semantic `[function]` declarations, three verification
  `[function]` declarations, and one semantic `[owise]` rule;
- no `[total]`, `[functional]`, `[simplification]`, `[concrete]`, opaque
  symbol, lemma rule, or explicit priority rule.

The single `[owise]` is the non-space fallback for `decodeChar`; it is a
priority mechanism, not a truth assumption.

### Construct coverage

Every constructor in `solution.mpy` is declared and modeled:

- module/function structure: `Module`, `FuncDef`, `Params`, and statement
  lists;
- statements: `If` and `Return`;
- expressions: `Name`, `Str`, `Int`, `BinOp`, `Compare`, `Call`, and
  `Subscript`;
- auxiliaries: `CmpOp`, `Slice`, and `NoBound`.

There are no assignments, loops, mutable objects, heap operations, I/O,
exceptions, or allocation in the submitted source. Missing rules for those
unused Python constructs are therefore not a generated-semantics defect.

### Disposition of every semantic rule

The rule IDs below are the IDs in `evidence/05_rule_inventory.log`.

- **R01-R02 (module load and final result): sound on their exact contexts.**
  R01 collects the submitted definitions and invokes the required binding on
  decoded input. R02 fires only when the whole `<k>` cell is a top-level
  `pyStr`, writes its encoding to the initially empty result, and clears the
  function table. It cannot preempt a value in a continuation.
- **R03-R06 (decode/decodeChar): sound.** Empty and positive-length String
  cases are disjoint and descending. The exact-space rule and `[owise]`
  non-space rule partition the character result.
- **R07-R09 (encode): sound structural equations** for empty, space, and
  character nodes.
- **R10-R11 (definition collection): sound** list recursion preserving source
  order.
- **R12-R13 (function lookup) and R14-R15 (environment lookup): sound.**
  Equal-name and guarded unequal-name cases are disjoint; first binding wins,
  as required by the represented tables.
- **R16-R18 (call, enter, return): sound for the one-argument used subset.**
  The selected closure comes from the actual function table; `enter` binds the
  parameter in a fresh local environment and pushes `finishCall(OLD)`; the
  result restores the caller environment without dropping its continuation.
- **R19-R24 (statement concatenation, return, if/choose): sound.** Concatenation
  is structurally descending. Conditions evaluate before branch selection.
  `Return` discards only the remaining statements in the current `exec` term;
  it does not discard the surrounding `finishCall` or caller continuation.
- **R25-R27 (name/string/int evaluation): sound** for the represented values.
- **R28-R30 (binary evaluation and string `+`): sound.** They enforce
  left-before-right evaluation and structural concatenation. Only the used
  string/string `+` case is admitted.
- **R31-R35 (comparison evaluation): sound.** They enforce left-before-right
  evaluation; the three apply rules model used string equality, integer
  greater-than, and `len(string) > integer`.
- **R36-R39 (calls and `len`): sound on used bindings.** The exact `"len"`
  built-in case is disjoint from the guarded user-call case. No program binding
  shadows `len`; user arguments are evaluated before calls.
- **R40-R43 (subscript/slice): sound on all reachable submitted-program
  paths.** Base evaluation precedes the literal index/slice operation.
  `pindex(0)`, suffix slices at 1 or 3, and `[0:3]` use the corresponding
  structural helpers. The source's empty and length guards make each used
  index and bound safe. The semantics deliberately has no fabricated fallback
  for an out-of-range used operation.
- **R44-R53 (`decideEq`): sound and exhaustive** over the three PString
  constructors. Empty/nonempty, space/character, equal-character recursion,
  and guarded unequal-character cases are disjoint or agree.
- **R54-R58 (`decideLonger`): sound.** For the only reachable nonnegative
  comparison bound, empty is false, nonempty at zero is true, and positive
  bounds recurse by one. Zero and positive guards are disjoint.
- **R59-R61 (`pconcat`), R62-R64 (`pdrop`), R65-R68 (`ptake`), and R69-R72
  (`pindex`): sound structural equations** over the reachable nonnegative
  indices. All recursive rules descend. These functions are intentionally
  partial outside their modeled domains and are not declared `total`; no
  negative index is reachable from this program.

The configuration has exactly the state the program needs: computation,
concrete input, local environment, function table, and output result. Rule
footprints preserve or restore all relevant cells. The evaluator models all
material binding, left-to-right evaluation, recursive call/return, branch, and
result effects used by the program. General CPython exceptions and resource
limits are outside this deliberately minimal subset; all program-level
index/slice safety obligations are discharged by reachable guards.

`PString`'s comment says `ch(C)` is non-space, but the sort itself does not
enforce single, non-space `C`. The claims consequently quantify over some
noncanonical structural values. This does not narrow the intended domain or
make a false intended-input result provable: every decoded concrete input is
in the canonical representation image, and the theorem is simply stronger
over extra abstract values.

### Disposition of every verification rule and claim

- **Verification R01-R02 (`Verify`/`VerifyDrop`): sound initialization rules.**
  They install `solutionFuns` and invoke the named function. The positive
  claims start after this initialization, so these rules are useful probes but
  not proof shortcuts.
- **Verification R03 (`solutionFuns`): sound definitional constant.** It does
  not replace a call or compute a result; it supplies the mechanically pinned
  submitted function table.
- **Verification R04-R10 (`fixRef`): mathematically sound, disjoint structural
  equations** for the candidate's transformation: empty/non-space recursion,
  one- and two-space runs to one/two underscores, and at least three spaces to
  a hyphen followed by `dropRef`.
- **Verification R11-R13 (`dropRef`): mathematically sound, disjoint structural
  equations** that discard leading spaces and resume `fixRef` at the first
  non-space.
- **Claims C01-C02:** their mutually recursive circular uses are guarded by
  genuine interpreter progress, and recursive calls receive strict suffixes.
  Fresh `kprove` closes both. They are the reachability theorem, not ordinary
  semantic axioms.

`fixRef` and `dropRef` are result specifications, not operational bridges:
no rule rewrites a program call to either function. There is no program-derived
opaque result, oracle, task-answer rule in the execution semantics, or
proof-local simplification that bypasses the submitted body.

I claim no local K rule is unsound on the intended reachable domain and
therefore assert no false-conclusion witness against a local rule. The concrete
`"  "` witness is instead an adequacy failure: the sound `fixRef` equations
state the wrong trusted-canonical target result.

## 6. Fresh non-vacuity test

The final reviewer-authored mutation is a ground instance of the target call
at a satisfiable state:

```text
call("fix_spaces", pyStr(.PString))
  => pyStr(ch("X") .PString)
```

The real execution returns the empty structural string, while the mutation
demands `"X"`. This directly changes the result-constraining obligation.

`kprove --dry-run` on `SPEC-VACUITY-GROUND` exited 0, establishing that the
mutation parses and builds. The actual proof exited 1 with
`WarnStuckClaimState`; its final configuration has an empty `<k>` cell and
result `""`, which does not unify with the false destination. This is the
expected unmet obligation, not a parser error, timeout, missing import, or
unreachable mutation.

The preserved mutation, command, exit statuses, and residual are
`evidence/spec-vacuity-ground.k`,
`evidence/06_nonvacuity.sh`, and
`evidence/06_nonvacuity.log`.

For transparency, `evidence/06_nonvacuity_attempt1.log` is an initial missing
local-import reviewer setup error and `attempt2.log` is a discarded symbolic
mutation that produced `DecidePredicateUnknown`. Neither is used as
non-vacuity evidence.

## 7. Proven versus assumed accounting

### What is formally proved

Under the locally generated K theory, for every finite structural `PString`
and every framed continuation/state satisfying the claims:

- the exact submitted `fix_spaces` body reduces to `pyStr(fixRef(S))`;
- the exact submitted `_drop_spaces` body reduces to `pyStr(dropRef(S))`.

The result is universally constrained and the theorem covers all structural
strings, not finitely many examples or bounded lengths. Via `Module`,
`decode`, the call claim, and `encode`, the generated semantics executes the
submitted module as the corresponding concrete String transformation. The K
proof remains a partial-correctness result.

### Trust ledger

- **K engine and logic:** K v7.1.293, the Haskell backend, circular
  reachability implementation, parser, and compiler are trusted. Every formal
  result depends on this ordinary toolchain boundary.
- **Imported built-ins:** `BOOL`, `INT`, `STRING`, list syntax, `lengthString`,
  `substrString`, `+String`, integer arithmetic/comparison, and String
  equality/disequality are trusted primitives. They model fixed low-level
  operations outside the candidate-defined program and are used by the
  generated semantics; no candidate proof equation redefines them.
- **Translator bridge:** `/reference/py2mpy.py` is a trusted mounted
  transliterator. Byte-identical regeneration establishes the exact
  source-to-constructor artifact used here.
- **Generated-semantics/CPython bridge:** the operational correspondence of
  this intentionally small semantics to Python is supported by the exhaustive
  construct audit and 12 concrete K-versus-generated-Python boundary runs. It
  is not itself proved inside K. General exceptions, recursion resource limits,
  and unused Python constructs are excluded. This would be a non-fatal
  evidence boundary for a theorem whose result matched the trusted contract.
- **`fixRef`/intent bridge:** `fixRef` is fully defined rather than opaque, and
  the K proof establishes equality to it. Its claim to be the HumanEval target
  is an external adequacy obligation. The independent differential test
  refutes equivalence to the trusted canonical on 313 sampled valid inputs,
  with the minimal witness `"  "`.
- **Opaque/oracle accounting:** none. There is no fresh result-bearing symbol,
  uninterpreted oracle, assumed connection theorem, or empirical value injected
  into program execution.

Gate A (real-program soundness, pinning, and non-vacuity) passes. Gate B
(intended-result adequacy) fails because the submitted implementation and
formal postcondition disagree with the trusted canonical on a material valid
input family. The evidence itself is reproducible and auditable, but finite
tests cannot repair that refuted intent bridge.

Accordingly, the successful `#Top` is a sound theorem about the submitted
recursive transformation, not a legitimate proof of the full trusted
HumanEval-140 target. A valid-input result mismatch is material under the
benchmark decision boundary, so the required pairing is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
