# Independent adversarial audit: 75-is-multiply-prime

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted `solution.mpy` for the intended integer domain
`a < 100`. The proof was rebuilt from source and all eleven positive target
modules independently closed with exit status 0 and `#Top`. The submitted MPY
program is byte-identical to a fresh translation with the trusted translator,
and the program term embedded in `verification.k` is identical after parsing.
A fresh false result mutation for input 75 was rejected with the expected
`true` versus `false` residual.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two evidence
limitations that do not undermine proof soundness:

1. `run-input.json`, `metrics.json`, `codex-last.txt`, and
   `codex-output.log` are absent, and no structured generation trace is
   present. This prevents provenance review of the generation process.
2. The K postcondition represents the natural-language predicate as an
   exhaustive truth table for 2 through 99 plus a symbolic false result below
   2. Equivalence of that table to “a product of three primes” is independently
   and exhaustively checked for the finite positive portion, but is not itself
   stated as a prime-factor predicate and proved inside K.

All candidate files were treated as untrusted. Candidate-built definitions and
caches were not used.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, as required, so there is no
infrastructure-mode contradiction.

The candidate and trusted semantics trees were compared recursively with
`diff --no-dereference -r`. They have identical entry sets, file types, and
bytes. Neither tree contains a symlink. The candidate therefore passes the
supplied-semantics integrity boundary; this comparison does not bless the
candidate's separate `verification.k`.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. Root inventory also confirms
that `solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and `prove.sh`
are regular files. See
[stage1-integrity.log](evidence/stage1-integrity.log) and the reviewer script
[stage1_integrity.sh](evidence/stage1_integrity.sh).

### Missing and additional artifacts

The following requested provenance artifacts are missing:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any structured generation trace

Consequently, there were no untrusted generation claims in those artifacts to
compare against the reconstructed evidence. This is an auditability concern,
not a substitute for or defect in the reconstructed K proof.

Additional candidate root entries are `smoke.py`, `smoke.mpy`, `prove.sh`, and
`__pycache__/solution.cpython-310.pyc`. They were not used as proof evidence.
The bytecode and all candidate-produced caches were ignored.

The relevant trusted and candidate source text is preserved in
[stage1-source-inspection.log](evidence/stage1-source-inspection.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For an integer `a < 100`, `is_multiply_prime(a)` must return true exactly when
`a` is the product of three prime numbers. The three primes need not be
distinct: the canonical implementation independently ranges over `i`, `j`,
and `k`, so values such as `8 = 2 * 2 * 2` are true.

The trusted canonical program enumerates prime triples. The submitted program
uses trial division, incrementing `factor_count` once for each prime factor
removed, including multiplicity, and returns whether that count is three. For
`a < 2`, its loop and final positive-remainder increment are skipped and it
returns false.

### Trusted translation

The scratch regeneration command was:

```text
python3 /tmp/audit-work/75-prime/trusted/py2mpy.py \
  /tmp/audit-work/75-prime/candidate/solution.py \
  > /tmp/audit-work/75-prime/regenerated-solution.mpy
```

It exited 0. The regenerated and submitted files are both 751 bytes and have
the same SHA-256:

```text
23a0c4bb78ab970ac38d92b0bb40a53cee89553a69e0ef1e345a9f445f1670ba
```

`cmp` exited 0. Exact commands and statuses are in
[stage2-regenerate.log](evidence/stage2-regenerate.log), with the generating
script in [stage2_regenerate.sh](evidence/stage2_regenerate.sh).

### Independent differential test

[stage2_differential.py](evidence/stage2_differential.py) imports the trusted
canonical and submitted generated modules from separate paths. It also contains
an independently implemented trial-division oracle. It tests:

- every integer from -64 through 99;
- representative farther points in the unbounded negative tail:
  -100, -101, -1000, and -1000000;
- the documented example 30;
- all small and positive branch boundaries, because every value 2 through 99
  is included.

There is no meaningful empty-input case for the scalar integer contract.

All 168 tested inputs agreed, with Boolean result types and zero mismatches.
The accepted values below 100 were:

```text
8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50, 52,
63, 66, 68, 70, 75, 76, 78, 92, 98, 99
```

The exact input list and result summary are in
[stage2-differential.log](evidence/stage2-differential.log). This is finite
intent-bridge evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/75-prime`. No compiled definition was copied from the
candidate. The supplied semantics source in scratch had already passed the
recursive identity check.

### Fresh definitions

The concrete definition was built with:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. The compiler reported non-exhaustive total-function warnings for
some unused general-language helpers and unused-variable warnings in `strLt`;
none is on this program's execution path. Full output is in
[stage3-kompile-concrete.log](evidence/stage3-kompile-concrete.log).

The proof definition was built with:

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

It exited 0. See
[stage3-kompile-proof.log](evidence/stage3-kompile-proof.log).

### Positive claims

Each target was run independently as:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module MODULE
```

The following modules all exited 0 and printed `#Top`:

| Module | Evidence |
|---|---|
| `SPEC-NEGATIVE` | [log](evidence/stage3-kprove-SPEC-NEGATIVE.log) |
| `SPEC-02-11` | [log](evidence/stage3-kprove-SPEC-02-11.log) |
| `SPEC-12-21` | [log](evidence/stage3-kprove-SPEC-12-21.log) |
| `SPEC-22-31` | [log](evidence/stage3-kprove-SPEC-22-31.log) |
| `SPEC-32-41` | [log](evidence/stage3-kprove-SPEC-32-41.log) |
| `SPEC-42-51` | [log](evidence/stage3-kprove-SPEC-42-51.log) |
| `SPEC-52-61` | [rerun log](evidence/stage3-kprove-SPEC-52-61-rerun.log) |
| `SPEC-62-71` | [log](evidence/stage3-kprove-SPEC-62-71.log) |
| `SPEC-72-81` | [log](evidence/stage3-kprove-SPEC-72-81.log) |
| `SPEC-82-91` | [log](evidence/stage3-kprove-SPEC-82-91.log) |
| `SPEC-92-99` | [log](evidence/stage3-kprove-SPEC-92-99.log) |

An initial parallel invocation of `SPEC-52-61` failed before proof execution
with a transient local diagnostic saying Java 17 could not be detected and
showing an empty detected version. That unrelated exit 2 remains visible in
[stage3-kprove-SPEC-52-61.log](evidence/stage3-kprove-SPEC-52-61.log). A
sequential rerun immediately closed with `#Top`; the transient diagnostic is
not a candidate-proof failure.

## 4. Adequacy and real-program pinning

### Claim meanings

Every claim starts from the same concrete, realizable clean state:

- module environment location 0;
- empty module map with parent builtins scope -1;
- next scope location 1;
- empty heap at location 0;
- empty stack;
- `noRet`, `NoExc`, and exit code 0.

`SPEC-NEGATIVE` has symbolic precondition `A:Int` and `A <Int 2`. Its
postcondition is the exact Boolean `false`, with all other listed cells restored
to the same clean values.

Each remaining module has no symbolic precondition. It runs ten ground inputs
(eight in the last module), immediately checkpoints each returned Boolean with
`#expect`, and ends with `.K` and the same clean cells. The true entries are:

| Claim | Ground domain | Entries constrained to true |
|---|---:|---|
| `SPEC-02-11` | 2–11 | 8 |
| `SPEC-12-21` | 12–21 | 12, 18, 20 |
| `SPEC-22-31` | 22–31 | 27, 28, 30 |
| `SPEC-32-41` | 32–41 | none |
| `SPEC-42-51` | 42–51 | 42, 44, 45, 50 |
| `SPEC-52-61` | 52–61 | 52 |
| `SPEC-62-71` | 62–71 | 63, 66, 68, 70 |
| `SPEC-72-81` | 72–81 | 75, 76, 78 |
| `SPEC-82-91` | 82–91 | none |
| `SPEC-92-99` | 92–99 | 92, 98, 99 |

Every other ground entry in those ranges is constrained to false. Thus the
claims cover every K integer below 100, not merely examples.

### Program identity

`#runIsMultiplyPrime` rewrites to:

1. `#loadAll` of an inline `Module`;
2. an ordinary `Call(Name("is_multiply_prime"), Int(A))`;
3. `#forgetEntryPoint` after return.

The reviewer extracted the inline `Module`, parsed both it and the submitted
`solution.mpy`, and compared KORE. The only source normalization was replacing
the single internal K spelling `.Stmts` with the external parser's empty-list
spelling. The normalized terms have identical SHA-256:

```text
5f7079cc87f76343261bd06e98cf142dd9da6b4b5bd8060f3e420e2042ca4167
```

See [stage4_pinning.py](evidence/stage4_pinning.py) and the successful
[stage4-pinning-rerun2.log](evidence/stage4-pinning-rerun2.log). Two earlier
logs preserve the expected parser rejection of internal `.Stmts` in external
program syntax; they did not alter the proof or supply evidence for the final
comparison.

The inline program contains the actual docstring, assignments, while loop,
both if statements, both division branches, and return comparison. There is no
substituted helper body or summary.

### Result constraint and witnesses

The checkpoint rule is:

```k
rule <k> B:Bool ~> #expect(B) => .K ... </k>
```

The same `B` occurs in the actual result and expected checkpoint. A different
ground Boolean cannot match. The prover must execute the function to produce
the Boolean; the rule does not create one.

`#forgetEntryPoint` applies only after a Boolean return and removes only the
temporary module binding. It preserves the result and restores the clean
module map needed between checkpoints.

Satisfying witnesses include:

- `A = -7` for `SPEC-NEGATIVE`, which satisfies `A < 2` and yields false;
- `A = 0` for the same symbolic claim, also false;
- `A = 75` for `SPEC-72-81`, which yields true.

Both Python implementations agree on all three. See
[stage4-witness.log](evidence/stage4-witness.log). These are exact equality
postconditions, not free variables, tautologies, or one-way implications.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[stage5-rule-inventory.md](evidence/stage5-rule-inventory.md) is the
reviewer-generated row-by-row ledger. It retains complete source blocks,
guards, cells, continuations, and attributes for every local statement in the
supplied semantics, `verification.k`, and `spec.k`.

The verified inventory totals are:

- 1 configuration;
- 228 syntax declarations;
- 5 evaluation contexts;
- 698 rules;
- 11 claims;
- 37 modules and 37 endmodules;
- 98 imports and 25 top-level requires.

Attribute/class counts include 146 function-bearing declarations, 107 total
declarations, 25 symbol declarations, 22 `no-evaluators` declarations,
45 priority-bearing blocks, 36 concrete-bearing blocks, 26 `owise` blocks,
4 macro-bearing blocks, and 663 ordinary semantic rules. There are no local
`functional` or `simplification` declarations. Counts, generation command, and
the inventory SHA-256 are in
[stage5-inventory-rerun.log](evidence/stage5-inventory-rerun.log).

Every row in the ledger records one of these decisions:

- declaration or assembly checked;
- evaluation-order/configuration checked;
- faithful on reachable submitted-program states;
- excluded from the Haskell proof definition (`concrete.k`);
- or unreachable from the submitted program and therefore unable to influence
  this theorem's result.

### Construct-to-rule map for the actual program

| Submitted construct | Declaration and operational source |
|---|---|
| `Module`, statement list | `syntax.k:56-61`; `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53-60`; `functions.k:14-16` |
| docstring `Expr(Str(...))` | `syntax.k:13,52`; `str.k:13-17`; `controls.k:48` |
| `Assign(Name, Int)` | `syntax.k:9,12,41`; `core.k:131-134,194`; `controls.k:9-18` |
| `While` | `syntax.k:46`; `controls.k:65-67,77-85` |
| `If` | `syntax.k:49`; `controls.k:51-54` |
| `AugAssign` | `syntax.k:44`; `controls.k:20-31` |
| `BinOp` `+`, `*`, `%`, `//` | `syntax.k:15`; `operators.k:12`; `int.k:9,14-20` |
| `Compare` `<=`, `>`, `==` | `syntax.k:30-32`; contexts and dispatch at `operators.k:14-17`; `int.k:23-26` |
| `Return` | `syntax.k:50`; `functions.k:77-90` |
| entry `Call` | `syntax.k:28`; argument sequencing at `core.k:183-191`; call/frame rules at `call.k:18-21,69-75` |

The strictness and context declarations impose the needed evaluation order:
right-hand sides are evaluated before assignment, augmented-assignment values
before update, and integer operands before dispatch. The while condition is
reevaluated each iteration. The if branches are selected by the exact Boolean
comparison result.

### Cells, state, allocation, calls, and returns

Execution first binds the function in module scope 0. The call evaluates its
single integer argument left to right, allocates a temporary scope at location
1, pushes a frame, binds `a`, and executes the actual body. The program uses
only scalar integers and Booleans, so the heap and heap location remain
unchanged.

Ordinary assignment and augmented assignment update the active local scope.
`factor` begins at 2 and only increases; the `//` and `%` divisor is therefore
never zero. Each loop step either divides `a` by a factor and increments the
count or increments the factor. Return stores `retV`, pops the exact frame,
restores environment 0 and scope location 1, and produces the Boolean before
the saved continuation. The harness then removes the module binding. The stack,
return, exception, exit-code, heap, and allocation cells all match the
postcondition.

### Overlaps, priorities, and proof-local extensions

`verification.k` contributes only:

1. syntax for `#runIsMultiplyPrime`, `#forgetEntryPoint`, and `#expect`;
2. the equality checkpoint;
3. the expansion from the harness symbol to the exact submitted program and
   ordinary call;
4. cleanup of the temporary module binding after a Boolean result.

It contributes no function, totality assertion, opaque symbol, priority rule,
simplification, or auxiliary claim. The harness expansion is not an
operational bridge that replaces program execution: it introduces the actual
program execution. The cleanup rule acts after return and does not skip a body,
continuation, exception, allocation, or state change.

The supplied priority rules for closure cells and heap references cannot match
the reachable plain-integer local state, or have guards refuted by the absence
of `"$cells"` and references. The generic user-closure call is selected; none
of the higher-priority math, MD5, method, or concrete-sort interceptions has
the submitted call shape. The two while-condition rules have complementary
`truthy` and `notBool truthy` guards. Integer comparison and arithmetic cases
are sort- and operator-specific. No conflicting reachable right-hand sides
were found.

The expected truth table appears only in reachability postconditions. That is
the property being proved, not a semantic rule available to make it true.

### Opaque and broader-semantics boundaries

The supplied proof definition contains these symbol/opaque primitives:

```text
md5hexCodes,
intFloatDiv, divII, floatMod, floatLt, absF,
floorFI, toF, ceilF,
subF, divF, addF, mulF, powF, gtF, eqF,
decStrToF, divFloatIntV, intToF, truncF,
roundF, roundFN, sqrtF,
sortVS, sortKeyVS
```

None occurs in `solution.mpy`, the embedded program term, the reachable
configuration, or a claim postcondition. They therefore cannot control a
branch or result in this proof. The same is true of the supplied MD5, float,
sort, dict, list, tuple, set, subscript, comprehension, range, method, assert,
and concrete-only rules.

The supplied language is intentionally a subset of CPython outside the used
fragment. Examples include total-but-underspecified out-of-bounds
`valSeqAt`, an ASCII-focused string model, an eager `GenExp` encoding, and
permissive minimal conversion helpers. These are recorded as narrower
language-model gaps, not as unsoundnesses in this candidate theorem: none is
reachable for any intended integer input to this program, so none can enable a
false conclusion here. The concrete-only module is not imported by
`VERIFICATION`.

The used fragment—ground ASCII docstring evaluation, integer arithmetic and
comparison, local maps, deterministic control flow, and frame push/pop—has no
unconstrained value source.

## 6. Fresh non-vacuity test

The reviewer created
[spec-vacuity.k](evidence/spec-vacuity.k), a distinct module with the same
realizable initial configuration and actual harness call for input 75. It
changes the result obligation from the original true result to false:

```k
claim <k> #runIsMultiplyPrime(75) => false </k>
```

First, the mutation was parsed and compiled to a prover invocation with:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

This exited 0; see
[stage6-vacuity-dry-run.log](evidence/stage6-vacuity-dry-run.log).

The actual proof command was:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`. The final reachable configuration has:

```text
<k> true ~> .K </k>
```

which does not unify with the mutated destination `false`. The remaining cells
are the expected restored clean state. This is the intended unmet obligation,
not a parser error, timeout, missing import, or unrelated crash. Full residual:
[stage6-vacuity-proof.log](evidence/stage6-vacuity-proof.log).

## 7. Proven versus assumed accounting

### Formally established by the reconstructed K proof

Conditional on the supplied semantics and K backend, execution of the exact
submitted MPY program from the stated clean configuration:

- returns false for every K integer `A < 2`;
- returns the exact table recorded above for every integer 2 through 99;
- restores the listed control, scope-allocation, heap, stack, return,
  exception, and exit-code cells after each checked call.

Together, this covers every integer below 100. The theorem is
result-constraining and sensitive to a false result. It is a partial-correctness
statement under the supplied MPY semantics.

### Trusted primitives and assumptions

1. **Supplied MPY semantics.** The candidate copy is exactly the trusted
   mounted tree. The proof trusts its mapping of the used MPY fragment to
   Python-like behavior. The used rules were statically checked and contain no
   candidate proof conclusion.
2. **K builtins and backend.** Integer arithmetic/comparison, Boolean logic,
   strings used to consume the ground ASCII docstring, maps, lists, strictness
   generation, matching, and Haskell reachability execution are trusted
   implementation primitives.
3. **Translator bridge.** The trusted Python-AST translator is trusted to
   represent `solution.py` as MPY syntax. Fresh byte identity and parsed KORE
   pinning support this bridge; they do not prove the translator correct in
   general.
4. **Natural-language/table bridge.** The accepted table is argued to equal
   the numbers below 100 with exactly three prime factors counting
   multiplicity. The independent arithmetic oracle and trusted canonical agree
   exhaustively on every positive input 2 through 99. For `a < 2`, every
   product of three primes is positive, so false is the ordinary mathematical
   consequence. This equivalence is not a K lemma.
5. **Opaque supplied symbols.** All 25 names listed in Stage 5 are imported
   trust boundaries for other language constructs. None is a dependent of
   these claims, so their interpretations are irrelevant to this result.

### Empirical and informal evidence

- The differential test is exhaustive for the finite positive portion of the
  formal domain and samples the negative tail. It supports the
  implementation-to-canonical and table-to-prime-product bridges.
- The symbolic K claim, rather than differential testing, establishes the
  submitted program's false result for all integers below 2 under the supplied
  semantics.
- The simple number-theoretic interpretation of the accepted table remains an
  informal intent bridge because `spec.k` does not define primality or
  factorization.

### Excluded behavior and concerns

The proof does not cover inputs `a >= 100`, non-integer Python values, CPython
resource behavior, or general correctness of unused MPY constructs. It also
cannot audit the missing generation provenance files. These limitations justify
`CONCERNS`, but no material soundness, pinning, or non-vacuity gap was found.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
