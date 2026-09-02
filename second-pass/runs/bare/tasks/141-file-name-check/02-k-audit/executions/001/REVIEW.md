# Adversarial audit — 141-file-name-check

## Outcome

The candidate is **FAIL / NOT_LEGIT** as a proof of the real generated Python
program over its stated string domain.

The fresh Haskell reconstruction does close the sole claim with `#Top`, the
claim is result-constraining, the checked-in program term exactly matches the
trusted-translator output, and both a false-postcondition mutation and a body
mutation fail as they should. Those facts rule out a substituted or simply
vacuous theorem.

The decisive failure is in the candidate-generated language semantics. Its
`If` rule constructs executable terms for both branches, while numerous
partial helpers are declared `[function,total]`. On the intended input `""`,
the real Python function returns `"No"` at the first `if`, but a fresh LLVM
execution evaluates the later, unreachable string subscript and aborts on
`substrString("",0,1)`. The same source returns `"No"` under the Haskell
backend. This concrete backend-dependent control/partiality witness means the
generated semantics does not soundly model the real program on a required
boundary input. It is a candidate semantic defect, not an audit infrastructure
failure.

All execution and mutation work was done from source in
`/tmp/audit-work/reconstruction`. Candidate-provided compiled definitions and
caches were not reused.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent:
`/reference/reference-semantics` is absent, as required by
`GENERATED_SEMANTICS`. There is therefore no infrastructure breach and no
hidden/supplied semantics was sought or used.

The following candidate/trusted pairs are byte-identical:

- `prompt.py`: SHA-256
  `1346cfd15de72531685d9c4a09fb6a7b459df3852a0d84cd6a0632a0a1c32e5b`.
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

All required source and provenance artifacts are present as ordinary regular
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, the 200-record structured JSONL trace, `prompt.py`,
`py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, and `spec.k`. A recursive check found zero candidate
symlinks. No required artifact is missing, mistyped, changed, or symlinked.

The candidate also contains extra untrusted artifacts:
`semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`,
`kprove.out`, `mutation-kprove.out`, `mutation-spec.k`, and `prove.sh`.
They are permitted generation byproducts/evidence, not trusted inputs, and the
compiled/cache artifacts were ignored.

`run-input.json`, `metrics.json`, `codex-last.txt`, the selected terminal
claims in `codex-output.log`, and the first/final structured trace records were
read only as candidate claims. Their claim that `#Top` and a mutation failure
were previously obtained was not used as proof evidence.

Evidence:

- [Stage 1 integrity and untrusted-claim log](/audit-output/evidence/stage1_integrity.log)
- [Stage 1 reproducer](/audit-output/evidence/run_stage1.sh)

The independently available K toolchain was:

```text
K version: v7.1.293
Build date: Fri Oct 03 13:32:35 CDT 2025
```

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an input Python string, return `"Yes"` exactly when:

1. the whole filename contains at most three ASCII digits `0`–`9`;
2. it contains exactly one dot;
3. the portion before the dot is nonempty and begins with an ASCII Latin
   letter `A`–`Z` or `a`–`z`; and
4. the portion after the unique dot is exactly `txt`, `exe`, or `dll`.

Otherwise return `"No"`.

The candidate implementation counts the ten ASCII digits, checks one dot,
checks a nonempty/ASCII-letter first character, and checks one of the three
final suffixes. Given the one-dot condition, `endswith(".txt" | ".exe" |
".dll")` makes the text after that dot exactly an accepted suffix. Counting
digits over the whole filename is equivalent to counting the stem because the
accepted suffixes contain no digits. Thus `solution.py` matches the prompt's
explicit contract.

The trusted canonical has a separate, real discrepancy with that prose:
`str.isalpha()` and `str.isdigit()` are Unicode-aware, whereas the prompt
explicitly names ASCII Latin letters and ASCII digits. For example:

- `"é.txt"`: canonical `"Yes"`, prompt/candidate `"No"`;
- `"A١٢٣٤.txt"`: canonical `"No"`, prompt/candidate `"Yes"`.

The independent 311-case differential run covered the two documented examples,
empty input, dot-count boundaries, suffix boundaries, the three/four-digit
boundary, every ASCII first-character range boundary, Unicode probes, NUL, and
a deterministic Cartesian sample. It found:

```text
CASE_COUNT=311
CANONICAL_MISMATCH_COUNT=20
PROMPT_MISMATCH_COUNT=0
EXIT_STATUS: 0
```

All 20 canonical mismatches are preserved, not hidden. They are attributable
to the documented prompt/canonical Unicode conflict rather than a violation of
the prompt's stated ASCII rules. They limit the canonical-to-intent bridge.

The trusted translator independently regenerated the submitted program:

```text
python3 /tmp/audit-work/reconstruction/trusted/py2mpy.py \
  /tmp/audit-work/reconstruction/candidate-source/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
# exit 0

cmp -s regenerated-solution.mpy candidate-source/solution.mpy
# exit 0
```

Both files have SHA-256
`8b599b1860c8633b4dbb68bce7b2fcf8b276139506a85bcb7df42801e4969883`.

Evidence:

- [Differential script](/audit-output/evidence/differential_test.py)
- [Complete differential inputs/results](/audit-output/evidence/stage2_differential.log)
- [Translation and byte-identity log](/audit-output/evidence/stage2_translation.log)
- [Stage 2 reproducer](/audit-output/evidence/run_stage2.sh)

## 3. Clean proof reconstruction

Fresh source copies, not candidate kompiled directories, were used.

### Fresh generated-semantics build

```text
kompile semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --backend llvm \
  --output-definition /tmp/audit-work/reconstruction/fresh-semantic-kompiled
# exit 0
```

The build succeeded, but emitted material non-exhaustiveness warnings for
helpers declared total, including `runProgram`, `eval`, `lookupVal`, `exec`,
`asBool`, `compareVals`, `addVals`, `subscriptVal`, `boolOp`,
`resultValue`, and `getString`.

### Fresh concrete execution

Twenty of 21 normal/boundary inputs agreed with Python. Empty input did not:

```text
COMMAND: krun .../solution.mpy --definition .../fresh-semantic-kompiled \
  -cINPUT=""
KRUN_EXIT_STATUS=255
terminate called after throwing an instance of 'std::invalid_argument'
what(): [error_on_end_substr]: Invalid string slice:
        Requested end index 0 is greater than string length 0
CASE 02 input='' python='No' k=None match=False
MISMATCH_COUNT=1
EXIT_STATUS: 1
```

This is the required boundary comparison, and it fails for a candidate reason.
It is not a timeout, parser failure, missing tool, malformed mount, or resource
failure. Normal inputs and all other boundaries executed, while the error
identifies the later unreachable subscript precisely.

For diagnostic separation, the same 21-case suite was run with the freshly
built Haskell proof definition. It produced 21/21 Python matches, including
`"" -> "No"`. The backend disagreement is further evidence that the candidate
combined partial functions and speculative branch terms unsafely; it does not
erase the required LLVM boundary failure.

Evidence:

- [Fresh semantics build](/audit-output/evidence/stage3_semantic_build.log)
- [LLVM concrete comparison, including empty failure](/audit-output/evidence/stage3_concrete.log)
- [Concrete comparison script](/audit-output/evidence/concrete_semantics_test.py)
- [Haskell concrete diagnostic](/audit-output/evidence/stage5_haskell_concrete.log)

### Fresh proof build and every positive claim

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition /tmp/audit-work/reconstruction/fresh-verification-kompiled
# exit 0

kprove spec.k \
  --definition /tmp/audit-work/reconstruction/fresh-verification-kompiled \
  --spec-module SPEC
# output includes: #Top
# exit 0
```

`spec.k` contains exactly one claim, so this executes every positive target.
The prover also emitted `WarnTrivialClaim: Claim proven without rewriting`.
Inspection shows that definitional simplification normalizes the functional
evaluator and the parallel `contractResult` decision tree to the same term.
The warning is not by itself vacuity: the fresh result mutation and program-body
mutation both fail in later stages. It does show that `#Top` is conditional on
the candidate equations and totality declarations rather than an independent
validation of those equations.

Evidence:

- [Fresh proof build](/audit-output/evidence/stage3_proof_build.log)
- [Fresh positive proof, exact output and exit](/audit-output/evidence/stage3_positive_proof.log)
- [Stage 3 reproducer](/audit-output/evidence/run_stage3.sh)

Stage 3 therefore has a successful positive proof reconstruction but a failed
required generated-semantics boundary execution.

## 4. Adequacy and real-program pinning

The entry claim has no `requires` clause. Its precondition is simply that
`S` has K sort `String`; it therefore admits every modeled string, including
empty input. Its postcondition says that the only configuration cell becomes
`contractResult(S)`, an explicitly defined `"Yes"`/`"No"` decision tree.
There is no free RHS variable, existential result, one-way implication, framed
state, helper claim, or loop claim.

The `<k>` cell starts with:

```text
runProgram(solutionProgram, S:String)
```

`runProgram` matches the exact function name and parameter, binds `file_name`
to `S`, and calls `exec` on the full body. `solutionProgram` expands to a
complete AST literal. An independent normalization that removes only
whitespace and the explicit spelling of empty `.Stmts` found:

```text
VERIFICATION_LITERAL_NORMALIZED_LENGTH=1486
SOLUTION_MPY_NORMALIZED_LENGTH=1486
IDENTITY_MATCH=True
EXIT_STATUS: 0
```

This, combined with trusted-translator byte identity, pins the claim to the
submitted `solution.mpy`; it is not a substituted program.

The claim is body-sensitive. A scratch-only mutation changed the AST's success
return from `"Yes"` to `"No"` while leaving `contractResult` and `spec.k`
unchanged. The mutated definition built successfully, but `kprove` exited 1
with `WarnStuckClaimState` and a `VStr("No")` residual under the acceptance
branch.

`"A.dll"` is a concrete state satisfying the claim's entire precondition.
Substitution yields `contractResult("A.dll") = VStr("Yes")`. The trusted
canonical, submitted Python, fresh Haskell `krun`, and a fresh ground K claim
all returned/proved `"Yes"`:

```text
kprove audit-ground-spec.k --definition ... --spec-module AUDIT-GROUND-SPEC
#Top
# exit 0

krun solution.mpy --definition ... -cINPUT='"A.dll"'
<k>
  VStr ( "Yes" ) ~> .K
</k>
# exit 0
```

This demonstrates satisfiability and result constraint. It does not repair the
empty-input semantic mismatch.

Evidence:

- [Program identity checker](/audit-output/evidence/program_identity_check.py)
- [Pinning, satisfying witness, and ground proof log](/audit-output/evidence/stage4_pinning.log)
- [Ground witness claim](/audit-output/evidence/audit-ground-spec.k)
- [Body mutation patch](/audit-output/evidence/body-sensitivity.patch)
- [Body-sensitivity build/proof log](/audit-output/evidence/stage5_body_sensitivity.log)

## 5. Rule-by-rule static soundness review

The complete inventory is preserved in
[rule_inventory.md](/audit-output/evidence/rule_inventory.md). It enumerates
every local syntax declaration, all 20 `[function,total]` helpers, the sole
`[concrete]` rule, all 42 `semantic.k` rules, all six `verification.k`
rules, the configuration, and the sole claim. There are no generated helper K
files, explicit `[functional]` declarations, priority rules,
`[simplification]` rules, proof-local ordinary rewrites, auxiliary claims, or
loop claims.

### Construct coverage

Every construct in `solution.mpy` has a declaration and a used rule path:

| AST construct | Semantic path |
|---|---|
| `Module`, `FuncDef`, `Params` | exact `runProgram` entry |
| statement list, `Assign`, `If`, `Return` | `exec` plus `continue` |
| `Name`, `Int`, `Str` | `eval`, environment lookup, value injections |
| nested `BinOp("+")` | `eval` then integer `addVals` |
| `UnaryOp("not")` | Boolean projection and `notBool` |
| two/three-operand `BoolOp` | candidate `boolOp` equations |
| `Compare` with `==`, `!=`, `>`, string `<=` | exact `compareVals` equations |
| `Subscript(...,0)` | `subscriptVal` / `substrString` |
| `Call(len(...))` | `lengthString` |
| `Call(Attribute(...,"count"),...)` | `occurrences` |
| `Call(Attribute(...,"endswith"),...)` | `endsWith` |

The configuration contains only `<k>`. Environment updates are persistent
shadow bindings; there is no heap, allocation, I/O, exception, or other state
in this pure target. Return correctly discards the statement tail.

### Rules that are sound on the target path

Literal evaluation, lookup hit/miss, integer addition and comparisons, string
comparison, string length, guarded suffix extraction, assignment, sequential
fall-through, and return have truthful equations on all target-reachable
well-typed terms. Their overlaps are disjoint or agree:

- lookup hit versus guarded miss;
- `true` versus `false` selectors;
- sufficient-length versus shorter-string `endsWith`.

The two- and three-operand Boolean rules evaluate all operands instead of
modeling general Python short-circuit effects. For this submitted AST, every
Boolean operand is a pure, terminating comparison or suffix check, so no
target-domain false value witness exists; this is a narrow unused-language
limitation, not a separate unsoundness finding.

Most non-exhaustive `[total]` helpers also have missing cases outside the
submitted program's reachable typed terms. Generated semantics may be minimal,
so those unused cases are recorded but are not independently treated as
defects.

### Opaque/trusted counting primitive

`occurrences(S,N)` has only:

```text
rule occurrences(S, NEEDLE) =>
  countAllOccurrences(S, NEEDLE) [concrete]
```

It is opaque for symbolic `S`, but is a fixed external string primitive rather
than a program-defined helper. The program and `contractResult` depend on the
same term, so the K theorem is interpretation-parametric in it. Its intended
meaning is supplied by the K string library on ground inputs and is supported
finitely by the differential/concrete tests. This does not independently prove
universal equivalence to Python `str.count`, and that limitation is included in
the trust ledger.

### Material unsound semantic rule and witness

The critical rule is `semantic.k:86-91`:

```text
exec(If(E,THEN,ELSE) SS,RHO)
  => IfExec(asBool(eval(E,RHO)),
            continue(exec(THEN,RHO),SS),
            continue(exec(ELSE,RHO),SS))
```

`semantic.k:95-96` similarly distributes a continuation into both symbolic
branches. These are function terms, and helpers such as `subscriptVal` and
`startsWithAsciiLetter` are declared total even though their empty-string slice
is partial.

Concrete false operational witness on the intended domain:

1. Let `S = ""`.
2. The real submitted Python evaluates `file_name.count(".") != 1` as true and
   immediately returns `"No"`.
3. The candidate rule constructs the nonselected continuation containing
   `first = file_name[0]`.
4. Fresh LLVM execution forces that continuation and calls
   `substrString("",0,1)`.
5. It aborts with exit 255 instead of returning `"No"`.

Thus the rule enables the false conclusion that code after a taken return is
evaluated, and produces a materially different control/termination outcome.
The fact that Haskell selects the `IfExec` branch first and returns `"No"`
shows the source is backend-sensitive; it is not a justification over the
rule's complete execution domain.

### Verification definitions

- `digitCount`, `startsWithAsciiLetter`, and `hasAcceptedSuffix` are explicit
  mathematical summaries.
- `validFileName` directly states the prompt conjunction, but is unused by the
  entry claim.
- `contractResult` is a fully defined decision tree, not an unconstrained
  oracle. Its equivalence to `validFileName` is plausible ordinary Boolean
  reasoning but is not a K theorem in this submission.
- `solutionProgram` is the exact AST pin, verified structurally and by body
  sensitivity.

There is no task-answer rewrite that bypasses `exec`, and no proof-local
operational bridge. The failure is instead in the generated base semantics'
control/totality interaction.

## 6. Fresh non-vacuity test

The candidate's `mutation-spec.k` was inspected only as untrusted evidence and
was not reused. The fresh mutation used a different satisfying input:

```text
claim <k> runProgram(solutionProgram, "A.dll")
        => VStr("No")
      </k>
```

This is demonstrably false because both Python implementations and fresh
Haskell K execution return `"Yes"`.

The mutation first built/parsed successfully:

```text
kprove audit-false-spec.k --definition ... \
  --spec-module AUDIT-FALSE-SPEC --dry-run
DRY_RUN_EXIT_STATUS: 0
```

The actual proof then failed for the expected unmet result:

```text
kore-exec: Warning (WarnStuckClaimState):
  The configuration's term doesn't unify with the destination's term ...
<k>
  VStr ( "Yes" ) ~> .K
</k>
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
PROOF_EXIT_STATUS: 1
```

This is valid non-vacuity evidence: it is not a parser error, missing import,
timeout, crash, or unreachable mutation.

Evidence:

- [Fresh false mutation](/audit-output/evidence/audit-false-spec.k)
- [Mutation parse/proof log](/audit-output/evidence/stage6_false_mutation.log)
- [Stage 6 reproducer](/audit-output/evidence/run_stage6.sh)

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the candidate's Haskell-kompiled K equations, totality declarations, and
imported K built-ins, for every symbolic K `String S`, simplifying the exact
submitted AST through the functional evaluator yields the same
`contractResult(S)` decision tree. It is a partial-correctness reachability
claim and does not prove termination.

The proof is result-constraining, program-pinned, body-sensitive, and
non-vacuous. It is not a proof that the generated semantics is a faithful
Python semantics, nor a machine-checked theorem that `contractResult` is
equivalent to the prose predicate.

### Trust and assumption ledger

| Boundary | Dependents | Status |
|---|---|---|
| K v7.1.293 compiler, parser, Haskell/LLVM backends, and reachability kernel | all build/execution/proof results | Necessary toolchain trust. The observed backend disagreement is attributed to candidate partial/total equations because the LLVM diagnostic names their invalid slice. |
| K `BOOL`, `INT`, and `STRING` primitives, including `lengthString`, `substrString`, arithmetic, equality, and lexicographic comparison | evaluator, suffix, start-letter test, all branches | Acceptable low-level semantic trust in the supported well-defined cases. Invalid slicing is not hidden: it is the concrete failure witness. |
| `countAllOccurrences` behind symbolic-opaque `occurrences` | dot count, digit count, `contractResult`, entry proof | Acceptable as an explicitly conditional external primitive, with ground equations and finite support. It is not a universal Python equivalence theorem. |
| Trusted `py2mpy.py` | Python-to-AST identity | Strong provenance bridge: candidate copy is trusted-byte-identical and regenerated AST is byte-identical. |
| Structural normalization of `solutionProgram` | claim-to-submitted-AST pin | Independently checked exact identity; additionally supported by body mutation. |
| Candidate `contractResult` equation | formal postcondition | Explicit and constraining, but program-specific. Its equivalence to unused `validFileName` and the prose is informal Boolean reasoning plus testing, not a K claim. |
| Python differential testing over 311 strings | implementation/canonical/prompt bridge | Finite evidence only. Zero prompt-oracle mismatches; 20 preserved canonical Unicode mismatches. |
| Concrete K/Python testing | generated-semantics bridge | Finite evidence and **failed** on LLVM empty input; therefore it cannot support the required universal real-program bridge. |
| Termination | all practical calls | Not proved; partial correctness only. The real Python terminates for these finite strings, while candidate LLVM semantics actually aborts at `""`. |

### Gate accounting

- Real-program soundness (Gate A): **FAIL**. Exact false operational witness
  `S=""` demonstrates that the generated semantics can execute an unreachable
  post-return subscript and abort.
- Intent adequacy (Gate B): the Python implementation matches the prompt's
  explicit ASCII contract in the independent suite, but the trusted canonical
  disagrees on Unicode and the `contractResult`/`validFileName` equivalence is
  not machine-checked.
- Evidence auditability (Gate C): **PASS as evidence accounting**. Commands,
  statuses, complete bounded logs, scripts, mutations, and the exhaustive rule
  inventory are preserved. This cannot override Gate A.

Because a proof about the real generated program requires a faithful generated
semantics on every admitted intended input, the empty-string control/partiality
failure is material. A Haskell `#Top`, finite Python correctness evidence, and
successful non-vacuity do not convert that theorem into a legitimate K proof of
the real program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
