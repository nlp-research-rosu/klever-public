# Independent adversarial review: 103-rounded-avg

The candidate has a reproducible, non-vacuous K proof under its own generated
theory, and the proof executes the submitted constructor program. It is not a
legitimate proof of the real Python program over the stated domain. The
generated semantics replaces Python integer true division and its binary64
result with exact rational division. The four universal claims have no upper
bound, so they prove results that are false for valid positive Python integers.

The smallest concrete witness is `n = m = 9007199254740993` (`2**53 + 1`).
Both the trusted canonical implementation and `solution.py` return the binary
string for `9007199254740992`, because the division result is a Python
binary64 float. Freshly rebuilt K execution returns
`binVal(9007199254740993)`. At `n = m = 10**309`, both Python implementations
raise `OverflowError`, while K returns normally. These are candidate semantics
defects, not infrastructure failures.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `103-rounded-avg`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- container-mounted paths for every trusted and generation artifact.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, the required
`/generation-evidence/{invocation.json,metrics.json,codex-last.txt,codex-output.log,prompt.txt}`,
the present `usage.json`, the supplemental legacy records, and all 106 JSONL
events in the structured trace. `runtime-metrics.json` is absent, which is
permitted for this legacy-selected layout and was not reconstructed.
Generation records were treated only as untrusted claims. They report a
successful generation run and a collective `#Top`; all proof results used for
this review were reconstructed independently.

The campaign-lock JSON object is exactly equal to the `audit_campaign` block,
and its file SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every directly recorded file hash matches, including the run/task/result and
invocation records, canonical source, trusted prompt and translator,
generation prompt/log/last-message/metrics/usage, and the trace JSONL file.
The candidate prompt and translator are byte-identical to the trusted mounts.
There are no symlinks in the candidate, reference, or generation-evidence
trees.

An independent tree walk produced retained-workspace hash
`60fa315587a7ee7dcd8e9ccad0cf4187272eadc3c942c8878df9c91c780dba84`,
matching both `invocation.json` and `generation-result.json`. The analogous
trace-tree hash
`7bdee4f214191a1f6882deb2f98f44346d27a2ea82e2998885904f122836775b`
matches `usage.json`, and the single trace file matches its invocation-record
hash. The launcher-level tree digests in `audit-input.json` use a separate,
undeclared encoding; I did not substitute them for this independently
recomputed and cross-recorded pipeline hash.

The generated-semantics boundary is consistent: there is no
`/reference/reference-semantics` path, while candidate `semantic.k` is a real
regular file. No infrastructure-stop condition was found. Full checks and
per-file hashes are in
[01-integrity.log](evidence/01-integrity.log), with the checker in
[integrity_check.py](evidence/integrity_check.py).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says: for positive integers `n` and `m`, compute the
average of every integer in the inclusive range `n..m`, round to the nearest
integer using Python's behavior, and return its binary representation; if
`n > m`, return `-1`.

The trusted canonical implementation sums the inclusive range and evaluates
`bin(round(summation / (m - n + 1)))`. Candidate `solution.py` instead returns
`bin(round((n + m) / 2))` after the same reversed-range check. For an
arithmetic progression, the mathematical average is `(n+m)/2`, so the
different algorithm is appropriate.

Using the trusted `/reference/py2mpy.py` on the scratch copy regenerated a
297-byte `solution.mpy` with SHA-256
`9822e532b080a85f474e143358b95a1698466e969412d6aa5d951f35aaa544df`.
It is byte-identical to the submitted file. See
[02-regeneration.log](evidence/02-regeneration.log).

The independent differential test imports the trusted canonical and generated
entry points from separate paths. It covers the four documented examples,
minimum and equal-endpoint cases, both sides of the `n > m` boundary, all four
integer/half-integer parity patterns, selected values around `2**53`, and
1,000 deterministic generated positive pairs. All 1,017 cases agree, including
return types and exception observations; the exact input/result list is in
[03-differential.log](evidence/03-differential.log), and the generator/oracle
is [differential_test.py](evidence/differential_test.py). This is finite
implementation evidence, not a proof of the K/Python bridge.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/reconstruction`. Candidate bytecode caches were ignored, and
no candidate-compiled definition or cache was reused. The live tools are
K `v7.1.293`; `kup` is absent, but the independently installed `kompile`,
`kprove`, and `krun` all run. See
[04-toolchain.log](evidence/04-toolchain.log).

Fresh builds succeeded:

- LLVM concrete semantics:
  `kompile --backend llvm semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition concrete-kompiled`
  exited 0 ([05-kompile-concrete.log](evidence/05-kompile-concrete.log)).
- Haskell proof definition:
  `kompile --backend haskell verification.k --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled`
  exited 0 ([06-kompile-proof.log](evidence/06-kompile-proof.log)).

Every positive claim was then selected and proved independently. `reversed`,
`integral-midpoint`, `half-even-down`, `half-even-up`, all four example
claims, and all three renderer claims each exited 0 and printed `#Top`.
The collective command also exited 0 with `#Top`. The renderer claims emit
`WarnTrivialClaim` because their function terms simplify before rewriting;
this is not used as non-vacuity evidence. Exact outputs are in
[08-kprove-reversed.log](evidence/08-kprove-reversed.log),
[09-kprove-individual-claims.log](evidence/09-kprove-individual-claims.log),
and [10-kprove-all.log](evidence/10-kprove-all.log).

Fresh concrete `krun` executions agree with independent Python execution on
normal, reversed, singleton, and all four rounding-boundary cases. They
disagree on three valid large cases:

| Input | Python `solution.py` | Fresh K execution |
|---|---|---|
| `n=m=2**53+1` | `binVal(9007199254740992)` after decoding the returned string | `binVal(9007199254740993)` |
| `n=m=2**53+3` | `binVal(9007199254740996)` | `binVal(9007199254740995)` |
| `n=m=10**309` | raises `OverflowError` | returns `binVal(10**309)` |

The exact `krun` commands, complete terminal configurations, Python outcomes,
and statuses are in
[07-k-concrete-compare.log](evidence/07-k-concrete-compare.log); the
independent driver is
[k_concrete_compare.py](evidence/k_concrete_compare.py).

Thus clean proof reconstruction succeeds syntactically and proves all claims
under the candidate's theory, but clean semantics reconstruction falsifies the
required real-program bridge.

## 4. Adequacy and real-program pinning

The four universal entry claims say:

| Claim | Plain-language precondition and postcondition | Satisfying witness |
|---|---|---|
| `reversed` | Positive `N,M` and `N>M`; return `-1` | `(2,1)` |
| `integral-midpoint` | Positive `N<=M` and even `N+M`; return exact `(N+M)/2` as `binVal` | `(1,5)` |
| `half-even-down` | Positive ordered inputs, odd sum, even lower neighbor; return that lower neighbor | `(2,3)` |
| `half-even-up` | Positive ordered inputs, odd sum, odd lower neighbor; return the upper neighbor | `(1,2)` |

For those witnesses, substitution gives respectively `-1`, `"0b11"`,
`"0b10"`, and `"0b10"` in both Python implementations. The four ground
example claims use realizable initial states and give the documented results.
The three renderer claims give concrete strings for payloads 3, 15, and 26.
There is therefore no inconsistent precondition or free result variable.

The claims also pin the submitted constructor program. I extracted the
`roundedAvgProgram` rule RHS, normalized only the K list unit `.Stmts` to the
concrete grammar's omitted empty list, parsed both it and the trusted
regeneration with the fresh definition, and compared their full JSON KASTs.
They have identical hash
`bb9f94113908c6461c4d12be276076e8db014f9268c1fdbf36b2a202298749ea`.
See [11-program-pinning.log](evidence/11-program-pinning.log) and
[program_pinning.py](evidence/program_pinning.py).

Body sensitivity also holds. A scratch-only mutation changed the denominator
inside the term actually returned by `roundedAvgProgram` from `Int(2)` to
`Int(3)`. The mutated definition built successfully, and
`SPEC.example-1-5` failed with a reachable terminal result `binVal(2)` rather
than the required `binVal(3)`. The preserved mutation and output are under
[body-mutation](evidence/body-mutation/) and
[12-body-sensitivity.log](evidence/12-body-sensitivity.log).

Nevertheless, the unrestricted `integral-midpoint` precondition is also
satisfied by `N=M=9007199254740993`. Its K postcondition requires
`binVal(9007199254740993)`, while both real Python implementations return the
string for `9007199254740992`. The claim therefore constrains a result, but
constrains it to a false real-program result. The formal domain does not
narrow the source contract; instead, the generated semantics overclaims the
whole domain.

## 5. Rule-by-rule static soundness review

The mechanical declaration/rule/claim scan is preserved in
[13-rule-inventory-raw.log](evidence/13-rule-inventory-raw.log), and the full
classification with guards, overlaps, state footprints, and the concrete
unsoundness witness is in
[static-rule-analysis.md](evidence/static-rule-analysis.md). The exhaustive
source inventory is summarized here.

### Declarations and construct coverage

`MPY-SYNTAX` locally declares `Module`; `Stmts`; the `FuncDef`, `If`, and
`Return` statements; `Params` and `Strings`; the `Int`, `Name`, `UnaryOp`,
`BinOp`, `Compare`, and `Call` expressions; `Exprs`; `CmpOp`; and `CmpOps`.
`SEMANTIC` declares values `intVal`, `boolVal`, `ratVal`, and `binVal`;
results `noResult`/`result`; K items `boot`, `exec`, `execStmt`, `choose`, and
`doReturn`; and `[function]` symbols `eval`, `unary`, `binary`, `compare`,
`callBuiltin`, and `roundValue`. Its configuration consists exactly of
`<k>`, `<env>`, and `<result>` under `<py>`.

`verification.k` adds the `[function]` constant `roundedAvgProgram` and
`[function]` observers `renderBinary` and `unsignedBits`. There are no local
`[total]`, `[functional]`, `[simplification]`, priority, or opaque
declarations. Every constructor in `solution.mpy` is declared and has a
reachable rule path; no unused language feature is required in this
generated-semantics mode.

### All 24 semantic rules

1. `boot` binds the two actual inputs to the exact function's formal names and
   starts its body; faithful for this singleton module.
2. Empty `exec` terminates sequencing; faithful.
3. Nonempty `exec` schedules head before tail; faithful.
4. `If` evaluates its guard in the current environment then schedules
   `choose`; faithful for the submitted pure expressions.
5. True `choose` selects the then branch; faithful.
6. False `choose` selects the else branch; faithful and disjoint from rule 5.
7. `Return` evaluates its expression then schedules `doReturn`; faithful.
8. `doReturn` discards the remaining continuation and writes `<result>`.
   This is faithful for the only top-level call modelled; there is no caller,
   heap, output, or exception cell to preserve.
9. `eval(Int)` injects an integer; faithful.
10. `eval(Name)` reads its unique map binding; faithful for `n` and `m`.
11. `eval(UnaryOp)` recursively evaluates its operand; faithful here.
12. `eval(BinOp)` recursively evaluates both operands. Python is
    left-to-right, but the submitted operands are pure, so the unspecified
    functional simplification order has no observable effect before division.
13. Single-comparison `eval(Compare)` evaluates both operands; faithful for
    the submitted single `>`.
14. Unary `Call(Name(F),E)` evaluates the argument and dispatches by builtin
    name. It pins standard `round`/`bin` rather than modelling general Python
    name lookup; that is sound for this function, whose local environment
    cannot shadow either name.
15. Unary `-` is ordinary integer negation; faithful.
16. Binary `+` is arbitrary-precision integer addition; faithful.
17. Binary `/` maps two integers to exact `ratVal(I,J)` for `J != 0`.
    **Unsound.** Python `/` produces binary64 or raises. The satisfying
    `2**53+1` and `10**309` witnesses above show, respectively, a false
    returned value and a fabricated normal return.
18. Integer `>` is ordinary comparison; faithful.
19. `callBuiltin("round",V)` dispatches to `roundValue`. It is locally a
    dispatcher, but receives the invalid exact-rational result from rule 17
    instead of a Python float and therefore participates in the witnessed
    false conclusion.
20. `callBuiltin("bin",intVal(I))` returns abstract `binVal(I)`. This is sound
    on the reachable nonnegative path conditional on the observer definition.
21. Rational remainder below one half rounds to the quotient.
22. Rational remainder above one half rounds to quotient plus one.
23. Exact half with even lower neighbor rounds down.
24. Exact half with odd lower neighbor rounds up.

Rules 21–24 are ordinary exact-rational nearest-even mathematics on reachable
`I>0,D=2`. Their guards are disjoint and exhaustive: doubled remainder is
less than, greater than, or equal to `D`, with equality split by quotient
parity. They do not justify substituting an exact rational for Python's float.
All sequencing, branch, and evaluator rules are constructor-disjoint where
they overlap by symbol; the Boolean and rounding families have disjoint
guards. State changes are limited to boot-time environment binding and the
return result, matching the material state used by this program.

### All five verification rules

1. `roundedAvgProgram` is the exact constructor term, not an execution
   shortcut.
2. `renderBinary(binVal(I))`, guarded by `I>=0`, prefixes `unsignedBits(I)`
   with `"0b"`.
3. `unsignedBits(0)` is `"0"`.
4. `unsignedBits(1)` is `"1"`.
5. For `I>=2`, `unsignedBits(I)` recurses on `I/2` and appends the remainder
   digit.

The three `unsignedBits` cases are disjoint, cover all values admitted by the
renderer, and the recursive case strictly descends. These are truthful
binary-rendering equations, not task-answer oracles. The 11 claims comprise
the four symbolic partitions, four ground examples, and three ground
renderers listed in Stage 4; there are no helper claims, semantic priority
rules, simplification lemmas, or hidden opaque results.

The decisive Gate A failure is therefore narrow and concrete: rule 17 is an
operational/value abstraction for a property-bearing used operation, has no
binary64 conversion or exception behavior, and has false conclusions on the
claimed source domain.

## 6. Fresh non-vacuity test

I created a new module, not the candidate's evidence, whose ground `(1,5)`
claim changes only the required result from `binVal(3)` to `binVal(4)`.
The input is plainly realizable and satisfies the original entry domain.

`kprove ... --dry-run` compiled this mutation successfully with exit 0.
The actual proof exited 1 with `WarnStuckClaimState`; the residual is a fully
terminated execution with `result(binVal(3))`, exactly the unmet result
obligation. There was no parse failure, missing import, timeout, or unrelated
crash. The mutation is [spec-vacuity.k](evidence/spec-vacuity.k), and exact
commands/statuses/residual are in
[14-non-vacuity.log](evidence/14-non-vacuity.log).

The proof is therefore result-constraining and non-vacuous under its supplied
theory. This does not cure that theory's false interpretation of `/`.

## 7. Proven versus assumed accounting and decision

What the successful K reachability proof actually establishes is:

- under the locally generated exact-rational semantics;
- for all K integers `N,M > 0`;
- reversed inputs return `intVal(-1)`; and
- ordered inputs return a `binVal` payload equal to exact rational
  nearest-even rounding of `(N+M)/2`, partitioned by sum and quotient parity.

It additionally establishes four ground executions and three ground rendering
equations. It executes the submitted MPY body and is sensitive to that body.

The trust/assumption ledger is:

- Trusted translator: `/reference/py2mpy.py`. Byte-identity regeneration
  supports the source-to-MPY bridge.
- Trusted K primitives: integer arithmetic/comparisons, Boolean operations,
  maps, string concatenation, and `Int2String`. These are an acceptable
  low-level toolchain boundary.
- Generated operational semantics: all 24 rules are candidate-authored and
  must be validated. Most are adequate for the used pure subset, but integer
  `/` as exact `ratVal` is unacceptable because it changes a used operation's
  value and exception behavior.
- Builtin binding: `round` and `bin` are selected directly by name. This is
  acceptable for the exact submitted local environment, but not a general
  Python semantics.
- Abstract output: `binVal(I)` represents Python's binary string, with a
  truthful recursive renderer by inspection. Only three payloads are separately
  proved as concrete strings, so the general representation-to-Python-string
  bridge remains informal. This would be an evidence limitation, not the main
  false-result defect.
- Average identity: replacing the inclusive arithmetic-progression sum by
  `(n+m)/2` is ordinary mathematics; the finite 1,017-case differential run
  supports the candidate/canonical implementation bridge but is not a
  universal K theorem.
- Python binary64 behavior: independently executed CPython is the oracle for
  the concrete witnesses. The mismatches are observable returns/exceptions,
  not performance or termination speculation.

Gate A fails because the generated semantics proves a false real-program
result for satisfying source-domain inputs. Gate B's positive-integer syntax
matches the stated domain, but real-program adequacy fails on that unrestricted
domain. Gate C evidence is reproducible, and the fresh non-vacuity gate passes;
neither can substitute for Gate A.

Under the benchmark decision boundary, a proof that relies on materially
unsound semantics for a used operation is `FAIL / NOT_LEGIT`, even though
fresh `kprove` prints `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
