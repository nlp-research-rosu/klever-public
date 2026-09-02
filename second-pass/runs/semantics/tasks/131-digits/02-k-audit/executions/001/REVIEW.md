# Independent adversarial audit — 131-digits

## Outcome

The submitted proof is legitimate under the supplied semantics. A fresh build
proves the loop circularity and the two-claim proof set, the entry claim
symbolically executes the submitted function body, all proof-local equations
are sound on their guards, and a fresh false postcondition is rejected for the
expected reason.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two
non-fatal limitations:

1. the candidate omits all four requested generation/provenance records; and
2. `oddDigitProduct` is declared `[total]` over all `Int` values while its
   equations only cover zero and positive first arguments. Negative cases are
   unused by both claims and by all recursive calls, so this does not enable a
   false conclusion on the intended domain, but the declaration is broader than
   its equations.

No trusted-mount contradiction occurred. This is a candidate verdict, not an
`AUDIT_ERROR`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted
`/reference/reference-semantics` directory is present as required.

I built type-and-content manifests for both semantics trees. The recursive
manifest comparison exited 0. There are no missing, additional, changed,
mistyped, or symlinked entries in the candidate's `reference-semantics/` tree.
`find -P /candidate -type l` also found no candidate symlinks. The manifests
are [candidate-semantics.manifest](evidence/candidate-semantics.manifest) and
[trusted-semantics.manifest](evidence/trusted-semantics.manifest); the exact
commands and statuses are in
[stage1_integrity.log](evidence/stage1_integrity.log).

The candidate prompt and translator are byte-identical to the trusted files:

- `prompt.py`: SHA-256
  `4a1c555a3cd7fb8a1b3a2786b00cb13d927f9a5509630d781ee1e2e0fdd8767c`;
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The following requested untrusted provenance artifacts are missing from
`/candidate`:

- `run-input.json`;
- `metrics.json`;
- `codex-last.txt`;
- `codex-output.log`.

No structured generation trace is present. There is also no candidate
`PROOF.md`. The candidate's `kprove.stdout`, `prove.sh`, concrete tests, and
`.pyc` were treated only as untrusted claims and were not used as reconstructed
proof evidence. All execution used fresh source copies under
`/tmp/audit-work/audit-131-digits`.

## 2. Program fidelity and candidate-versus-canonical checks

The contract in `/reference/prompt.py` is: for a positive integer `n`, return
the product of its odd decimal digits; return zero if it has no odd digit. The
documented examples are `digits(1) == 1`, `digits(4) == 0`, and
`digits(235) == 15`.

The canonical implementation converts the positive integer to decimal text,
multiplies odd digits, counts them, and returns zero when the count is zero.
The candidate instead scans from right to left using division by ten. It tests
`n % 2`, which equals the parity of the last decimal digit, uses zero as a
sentinel, and multiplies by `n % 10`. Since every odd digit is nonzero, the
sentinel is unambiguous. This is a different but equivalent algorithm for
positive integers.

Regenerating `solution.mpy` from `solution.py` with the trusted translator
produced byte identity. Both files have SHA-256
`bcbb57c135a74bccedb80630923f77d64b987486df74b8b389ce80f84c15d066`.
The regenerated file is
[regenerated-solution.mpy](evidence/regenerated-solution.mpy), and the command
record is [stage2_fidelity.log](evidence/stage2_fidelity.log).

The independent differential oracle imports
`/reference/canonical.py:digits`; it does not reuse the K summary equations.
It tested:

- all three documented examples;
- zero as the empty-digit/boundary behavior, while recording that it is outside
  the formal positive domain;
- explicit branch boundaries for even/odd last digits, the zero sentinel,
  subsequent multiplication, embedded zeroes, all-even inputs, and multiple
  digits;
- every integer from 1 through 20,000;
- `10**k - 1`, `10**k`, and `10**k + 1` for `k = 1..80`;
- 2,000 deterministic random positive integers of 1 through 120 decimal
  digits.

After deduplication this was 22,180 intended-domain inputs, with zero
mismatches. The complete input set is
[differential_inputs.json](evidence/differential_inputs.json), the independent
runner is [differential_test.py](evidence/differential_test.py), and its bounded
results are in [stage2_fidelity.log](evidence/stage2_fidelity.log).

For completeness, `0` returns zero in both implementations. Negative integers
are outside the stated domain: the canonical implementation raises
`ValueError` on the minus sign while the candidate returns zero. The formal
entry precondition correctly excludes these values.

## 3. Clean proof reconstruction

No candidate-built definition or cache was copied. With K
`v7.1.337`, I freshly built:

- the LLVM definition from the supplied `semantics.k`, using
  `MPY-KRUN` and `MPY-SYNTAX`; and
- the Haskell proof definition from `verification.k`, using
  `DIGITS-VERIFICATION` and `MPY-SYNTAX`.

Both `kompile` commands exited 0. The regenerated program and an independent K
assertion harness both executed under the LLVM definition with exit status 0.
The harness source and translation are
[reviewer-concrete-tests.py](evidence/reviewer-concrete-tests.py) and
[reviewer-concrete-tests.mpy](evidence/reviewer-concrete-tests.mpy).

Fresh proof results were:

| Run | Result |
|---|---|
| `DIGITS-SPEC.digits-loop` selected alone | exit 0, `#Top` |
| complete submitted `DIGITS-SPEC` claim set | exit 0, `#Top` |
| `DIGITS-SPEC.digits-correct` selected while deleting the loop claim from the proof set | exit 1, genuine `WarnStuckClaimState` |

The third run is an important dependency diagnostic, not a failure of the
submitted two-claim proof. K reachability loop invariants are circularity
claims. `--claims DIGITS-SPEC.digits-correct` removes
`DIGITS-SPEC.digits-loop` from the proof set rather than merely hiding its
output, so the entry proof is expected to lose its only loop summary. The
complete positive claim set proves both claims together, while the separate
loop run confirms that the helper itself closes.

All commands, warnings, output, and exit statuses are preserved in
[stage3_rebuild.log](evidence/stage3_rebuild.log). The compiler's
non-exhaustive-match warnings concern unused portions of the supplied baseline
and do not occur in the integer/control dependency slice used by this program.

As an additional pinning check, I wrote a fresh claim whose `<k>` cell starts
with the exact translated `Module(FuncDef(...))`, executes `#loadAll`, and then
calls `digits(N)`. It preserves all relevant cells and reaches
`oddDigitProduct(N, 0)` for `N > 0`. It builds and proves with exit 0 and
`#Top`. See [program-pinning.k](evidence/program-pinning.k) and
[stage4_program_pinning.log](evidence/stage4_program_pinning.log).

## 4. Adequacy and real-program pinning

### `digits-loop`

The precondition is `N >= 0` and `A >= 0`. At a real loop head, local `n`
contains `N` and local `product` contains `A`. The claim executes the exact
translated while condition and body. On completion it requires local `n` to be
zero and local `product` to equal `oddDigitProduct(N, A)`, while preserving the
continuation and the function/module scopes.

The claim is not tautological: it rewrites both local bindings to concrete
result expressions and consumes the loop. Its continuation is framed, which is
appropriate because a normally terminating loop continues with that exact
suffix.

### `digits-correct`

The precondition is exactly `N > 0`, matching the natural-language domain. The
claim starts from the post-module-load configuration, looks up and calls the
`digits` closure, binds `n`, executes the submitted assignment, loop, and
return, restores the caller frame, and constrains the returned integer to
`oddDigitProduct(N, 0)`. The heap, stack, return state, exception state, and
exit code are pinned.

The translated file, the closure body copied into `spec.k`, and the closure
shown by fresh `krun solution.mpy --output pretty` agree exactly modulo K's
explicit empty-list form. The reviewer `program-pinned` claim additionally
machine-checks the module-load-to-call connection instead of relying only on
that textual observation.

A satisfying entry witness is `N = 235`. A satisfying, reachable loop witness
is the state immediately after `digits(235)` binds `n = 235` and executes
`product = 0`. Substitution gives:

```text
oddDigitProduct(235, 0) = 15
canonical.digits(235)    = 15
solution.digits(235)     = 15
```

The exact state and result evidence is in
[adequacy_witness.py](evidence/adequacy_witness.py) and
[stage4_adequacy.log](evidence/stage4_adequacy.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The line-addressable inventory contains 939 entries:

- 228 syntax declarations;
- 703 rule declarations;
- 5 evaluation contexts;
- 1 configuration;
- 2 reachability claims.

Across those entries there are 146 `[function]` declarations, 108 `[total]`
declarations, no `[functional]` declaration, 45 priority-bearing rules, 35
`[concrete]` rules, 26 `[owise]` rules, 3 `[simplification]` rules, and 22
`[no-evaluators]` declarations. Attribute categories can overlap.

Every entry, with its full source text, line range, and attributes, is in
[rule_inventory.md](evidence/rule_inventory.md) and
[rule_inventory.json](evidence/rule_inventory.json). Every one of the 939
entries has an explicit audit disposition in
[rule_review.tsv](evidence/rule_review.tsv). The inventory-generation commands,
counts, hashes, and exit statuses are in
[stage5_inventory.log](evidence/stage5_inventory.log).

The supplied semantics is fixed by the problem boundary and byte-identical to
the trusted mount. Unused baseline rules are therefore classified as fixed,
unreachable semantics, not as candidate proof extensions. This classification
does not claim that the supplied subset implements all of Python; it records
that those rules cannot affect this theorem. The 114 entries in the actual
dependency slice were separately checked against the program.

### Used syntax and operational rules

| Program construct | Declaration and operational path |
|---|---|
| `Module`, statement lists | `syntax.k:56-61`; configuration and `#loadAll`/sequencing in `core.k:49-60,124-127` |
| `FuncDef`, parameters | `syntax.k:53,57,60`; closure creation in `functions.k:14-16` |
| `Call(Name("digits"), Int(N))` | lookup in `core.k:130-154`; callee/argument order in `call.k:20-21` and `core.k:185-191`; closure frame in `call.k:69-74` |
| assignment and augmentation | `syntax.k:41,44`; plain local assignment and integer augmentation in `controls.k:9-11,20-23` |
| `While` | `syntax.k:46`; condition/body/loop continuation in `controls.k:77-82` |
| `If` | `syntax.k:49`; truth conversion and branch selection in `controls.k:51-54` |
| `Name`, `Int` | `syntax.k:9,12`; lookup and literal reduction in `core.k:130-154,194` |
| `%`, `//`, `*` | strict `BinOp` evaluation in `syntax.k:15` and `operators.k:12`; integer cases and `pyMod` in `int.k:14-20` |
| `>`, `==` | comparison contexts/dispatch in `operators.k:15-17`; integer relations in `int.k:22-27` |
| `Return` | strict declaration in `syntax.k:50`; return, frame pop, and cell restoration in `functions.k:78-90` |

Evaluation is left-to-right where relevant. The program creates no heap
objects, closures with cells, exceptions, output, or external state. Its
function call allocates one scope frame, binds one integer parameter, mutates
only the two local names, and restores the caller frame on return. The claims
pin every observable cell involved.

All 45 priority rules belong to the supplied baseline. In the used path, the
special priorities concern heap references or closure cells, but this
unannotated integer-only function has neither; the plain name, assignment,
operator, and call rules apply. There is no proof-local priority or operational
bridge that can preempt fixed execution.

### Proof-local extension inventory

`verification.k` contributes only:

1. `oddDigitProduct(Int, Int)` and `oddDigitStep(Bool, Int, Int, Int)`;
2. five defining rules; and
3. three equality simplifiers.

There is no proof-local rule whose left-hand side matches `<k>`, `Call`,
`While`, `Return`, or any other operational term. Consequently there is no
program-body bypass, result-bearing oracle, abrupt control bridge, fabricated
state, or hidden allocation.

The defining equations are disjoint and truthful on the used domain:

- `oddDigitProduct(0, A) = A`;
- for `N > 0`, `D = pyMod(N, 10)` and
  `Q = (N - D) / 10`, followed by a parity dispatch;
- false parity preserves `A`;
- true parity with `A = 0` replaces the sentinel with `D`;
- true parity with `A != 0` multiplies by `D`.

For positive `N`, `Q` is nonnegative and smaller than `N`; `pyMod(N,2)` is
either zero or one. The `oddDigitStep` guards are exhaustive and pairwise
disjoint over `Bool × Int`. The `oddDigitProduct` declaration has the one scope
limitation already noted: negative first arguments have no equation despite
`[total]`. No claim, simplifier, or recursive call admits such an argument, so
I classify this as an off-domain evidence gap rather than an unsound rule. I do
not assert a false-conclusion witness because none was found.

Each simplifier is exactly one guarded unfolding of that recurrence. To avoid
circular validation, I rebuilt
[verification-base.k](evidence/verification-base.k) with all submitted
simplifiers removed and independently proved all three equations in
[extension-lemmas.k](evidence/extension-lemmas.k). Every lemma exited 0 with
`#Top`; see
[stage5_extension_lemmas.log](evidence/stage5_extension_lemmas.log). An initial
attempt to express a Bool value as a top-level reachability configuration hit a
K backend “configuration term must be function-like” error; it is preserved in
[stage5_extension_lemmas_bool_attempt.log](evidence/stage5_extension_lemmas_bool_attempt.log).
Recasting the same equations in standard `<k>` configurations removed that
tooling-shape error without adding any rule.

### Opaque and concrete-only baseline symbols

The proof definition contains these supplied `[no-evaluators]` boundaries:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
`divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, `sortVS`,
and `sortKeyVS`.

`md5hexCodes` and `sortKeyVS` have no directly detected defining rule head in
the proof module; the remaining symbols have concrete-only equations or
concrete legs. None is reachable from `solution.mpy`, the claims, or
`oddDigitProduct`. They cannot influence control, state, or the final result in
this proof and are acceptable unused baseline boundaries.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I created a fresh mutation that changes
only the entry result from:

```k
oddDigitProduct(N, 0)
```

to:

```k
oddDigitProduct(N, 0) +Int 1
```

For the satisfying witness `N = 235`, the original result is 15 and the mutated
obligation demands 16. The mutation is
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k).

`kprove --dry-run` exited 0, establishing that the mutation parses and builds.
The actual proof exited 1 with `WarnStuckClaimState`; its residual contains the
unmet equality between `oddDigitStep(...) +Int 1` and the same
`oddDigitStep(...)`. This is the expected reachable result obligation, not a
parser error, missing import, timeout, or unrelated crash. The exact diff,
witness, commands, statuses, and residual are in
[stage6_nonvacuity.log](evidence/stage6_nonvacuity.log).

## 7. Proven versus assumed accounting

### Formally established

Under the supplied K semantics and the nine proof-local
definition/simplification entries, the successful two-claim reachability proof
establishes:

- for any `N >= 0` and `A >= 0`, if the exact submitted loop terminates from the
  stated loop-head state, it leaves `n = 0` and
  `product = oddDigitProduct(N, A)`; and
- for any `N > 0`, if the submitted `digits(N)` call terminates, it returns
  `oddDigitProduct(N, 0)` with the pinned caller state restored.

The independent `program-pinned` claim also establishes, under the same theory,
that loading the exact translated `Module(FuncDef(...))` and then calling it
reaches the same result. The three simplifier equations were independently
proved without importing those simplifiers. The false `+1` result is rejected.

This is partial correctness. The reachability proof does not itself establish
termination, although the quotient-by-ten argument makes termination
elementary for positive integers.

### Trust ledger and informal/empirical bridges

1. **Supplied semantics:** all 939 inventoried entries are fixed trusted input
   under `SUPPLIED_SEMANTICS`. The candidate copy is exactly identical. The 114
   used entries implement the actual module/call/integer/control path; the
   remainder is unreachable.
2. **K primitives and backend:** mathematical integers, Booleans, strings,
   maps, lists, equality, arithmetic hooks, parsing, generated heating/cooling,
   the Haskell prover, and the LLVM runtime are trusted implementation
   boundaries. The used theorem relies primarily on unbounded integer
   arithmetic, which matches Python's arbitrary-precision integers on the
   stated operations.
3. **Translator:** `/reference/py2mpy.py` is trusted by the problem. The
   candidate translator is identical, and its output is byte-identical to the
   submitted `solution.mpy`.
4. **Unused opaque symbols:** the 22 symbols listed in Stage 5 are proof-side
   or concrete-only baseline boundaries. None has a dependent claim here.
5. **Negative `oddDigitProduct` values:** the `[total]` declaration leaves them
   without equations. This is concerning declaration breadth but has no
   dependent intended-domain state.
6. **Summary-to-English meaning:** the bridge from the recurrence to “product
   of odd decimal digits” uses the ordinary facts that `N % 10` is the last
   digit, `(N - N%10)/10` removes it, and `N % 2` has the same parity as that
   digit. The zero sentinel is safe because odd decimal digits are nonzero.
   This is an informal mathematical adequacy argument, not a second K theorem
   over decimal strings.
7. **Implementation-to-canonical equivalence:** 22,180 differential inputs
   provide finite empirical support only. They do not replace the K proof or
   make a universal claim by themselves.
8. **Provenance:** the missing generation records prevent reconstruction of
   how the candidate was produced. They do not prevent independent
   reconstruction of what the submitted sources prove.

### Gate summary

- Real-program soundness: **pass**. The fixed body executes, no operational
  bridge or oracle exists, the proof-local equations are valid, a satisfying
  witness exists, and the false result is rejected.
- Intent adequacy: **pass** for positive integers. Zero and negative behavior
  is explicitly outside the entry theorem.
- Trust/evidence auditability: **pass with concerns**. All reviewer evidence is
  reproducible, but candidate generation provenance is absent and the
  off-domain `[total]` annotation is broader than its equations.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
