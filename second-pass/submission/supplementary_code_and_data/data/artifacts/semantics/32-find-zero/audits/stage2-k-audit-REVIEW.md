# Independent adversarial audit — 32-find-zero

The candidate is **not a legitimate partial-correctness proof of the generated
program**. A fresh build does reproduce `#Top`, and the submitted Python program
is faithful to the trusted canonical implementation at the numeric-result
level. However, the K claims succeed only because two priority rules replace
both real loops with unconstrained result-bearing constructors. The entry
configuration also omits the submitted module's `poly` binding. An independently
built bridge-free variant gets stuck at `#look("poly", -1)`, exactly where the
missing global binding is needed. Finally, the claimed postcondition is made
`true` solely by recognizing the same opaque constructor produced by the loop
shortcut; it is never connected to polynomial evaluation or to a numeric zero.

All mutations and builds were made only in `/tmp/audit-work`. Reviewer-authored
scripts, K variants, and bounded command transcripts are in
`/audit-output/evidence/`. The exact command ledger is
`evidence/COMMANDS.md`.

## 1. Input and provenance integrity

Result: **PASS (audit infrastructure intact).**

`/audit-input.json` declares:

- problem `32-find-zero`;
- condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the recorded value.

All launcher-declared container mounts and all records required for
`legacy-selected-stage1` are regular/readable at the declared paths:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and `codex-trace/`. `usage.json` is present
and was also inspected. The historical records explicitly mark runtime/container
facts as unknown legacy data; no missing historical runtime metrics were
reconstructed.

The complete structured trace contains one JSONL file, 311 valid records, and
zero parse errors. The complete `codex-output.log` was consumed: 930,273 bytes,
25,183 lines, and no decoding replacements. These generation records claim a
successful proof, but were treated only as untrusted history.

Every recorded single-file and generation-evidence hash checked by
`evidence/integrity_check.py` matches. In particular:

- candidate and trusted prompt:
  `17c137edab480f3be30b47bb48eea2748f23b120a73b2bb80c7901112e1b223f`;
- candidate and trusted translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- trusted canonical:
  `118ac96004a8df10bb50df65bc9ec9e6864cff602b488575893c4b96e18790a7`;
- generation output:
  `5f5b53b2ec2c9c6aa24446b8659c879c92e6328c820f5c19a4e55af43cd7ef29`;
- trace JSONL:
  `98b6f452b0df3ea3b2a2a662e8752128f2ace1bef0cb93709e2dda8663b4d457`.

The trusted `/reference/reference-semantics` mount is present, as required for
the rendered mode. Recursive lstat/type/path/content comparison found 25
entries in each tree, no missing or additional entries, no symlinks or special
files, and byte identity for every file. Both independent sorted
kind/path/content-hash manifests have SHA-256
`384ff8b252040525e5db052b228ab3d75b43b2887056df427482d93a3cc2c1f0`.
Thus there is no semantics-mode contradiction or infrastructure stop condition.

Evidence: `stage1-integrity.log`,
`stage1-generation-inspection.log`, `integrity_check.py`, and
`inspect_generation.py`.

## 2. Program fidelity and candidate-versus-canonical checks

Result: **PASS for implementation fidelity, with a non-material return-type
observation.**

The trusted prompt says that `xs` is a polynomial's coefficient list, that the
list has an even number of coefficients, and that its highest-degree
coefficient is nonzero. On the intended numeric domain this makes the degree
odd and supplies a real root. `find_zero` must return a zero (operationally, the
canonical implementation bisects until the bracket width is at most `1e-10`
and returns its lower endpoint). The documented examples are `[1, 2] -> -0.5`
and `[-6, 11, -6, 1] -> 1.0` after rounding to two decimals.

`/candidate/solution.py` implements the same expansion-and-bisection algorithm
as `/reference/canonical.py`. Its only material-looking source difference is
that the initial endpoints and multipliers use integer literals (`-1`, `1`,
`2`) rather than float literals (`-1.`, `1.`, `2.0`).

Trusted regeneration used:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate/solution.py
```

The regenerated and submitted `solution.mpy` are byte-identical: 1,317 bytes,
SHA-256
`fd0e785aa1efde54eeeaa27bd282112b62a98223aadb7e03b486dbf0ea4984c9`.

The independent differential script imports the trusted canonical module and
the candidate module under distinct module names. It ran 124 cases:

- both documented examples;
- empty/all-zero/zero-leading invalid boundaries;
- roots at `-1`, `0`, and `1`;
- tolerance-adjacent roots;
- one and many interval expansions;
- a degree-five boundary;
- 90 seeded integer polynomials of degrees 1, 3, and 5;
- 20 seeded float-coefficient cubics.

There were 121 source-contract-valid cases, three deliberately invalid
boundaries, and **zero material numeric or exception mismatches**. There were
14 exact-observation differences: when the root is an exact integer endpoint,
the candidate can return an `int` while the canonical returns the numerically
equal `float` (for example `-1` versus `-1.0`). The prompt specifies a numeric
zero and no return type, so this is not a material result divergence.

Evidence: `stage2-fidelity.log`, `stage2-differential.log`,
`fidelity_check.py`, and `differential_test.py`.

## 3. Clean proof reconstruction

Result: **the candidate claims reproduce `#Top`, but this is only verification
under the candidate's extended theory.**

No candidate kompiled definition or cache was copied into the reconstruction.
The only source artifacts were copied to `/tmp/audit-work/candidate`; fresh
definitions were named `audit-runtime-kompiled` and
`audit-verification-kompiled`. The live tools are K 7.1.293 at
`/usr/bin/kompile`, `/usr/bin/krun`, and `/usr/bin/kprove`.

Fresh LLVM build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

Exit 0. The candidate's two-example concrete module and separate expansion
module both ran under that fresh definition with exit 0:

```text
krun concrete_tests.mpy --definition audit-runtime-kompiled --output none
krun expansion_test.mpy --definition audit-runtime-kompiled --output none
```

Fresh Haskell proof build:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Exit 0. The complete candidate spec then exited 0 and printed `#Top`:

```text
kprove --definition audit-verification-kompiled \
  --spec-module SPEC spec.k
```

To make the per-claim result explicit, exact reviewer-owned splits of the two
candidate claims were also run. `AUDIT-SPEC-RESULT` and
`AUDIT-SPEC-APPROX` each exited 0 and printed `#Top`. Compiler warnings were
limited to unused variables and supplied-semantics exhaustiveness warnings;
there was no build or proof infrastructure failure.

Evidence: `stage3-kompile-runtime.log`, `stage3-krun-examples.log`,
`stage3-krun-expansion.log`, `stage3-kompile-verification.log`,
`stage3-kprove-all-claims.log`, `stage3-kprove-result-claim.log`,
`stage3-kprove-approx-claim.log`, and the preserved split specs.

## 4. Adequacy and real-program pinning

Result: **FAIL. The body text is pinned, but the binding/execution and result
property are not.**

### Plain-language claims

Both claims start from the same exact cell configuration and require the
uninterpreted Boolean condition `validPolynomial(VS)`.

1. `spec.k:8-28` directly constructs
   `closureVal(("xs", .ParamNames), findZeroBody, 0)`, calls it with
   `list(VS)`, and claims the returned value is the fresh term
   `bisectLow(VS, bracketLow(VS), bracketHigh(VS))`.
2. `spec.k:31-52` runs the same call followed by `#checkApprox(VS)` and claims
   the result is `true`.

The formal precondition is not the source precondition. `validPolynomial` is
declared `[function, total, symbol, no-evaluators]` at
`verification.k:78-79`, with no equation defining even length or nonzero last
coefficient and no theorem showing that any source-contract input satisfies
it. It is logically satisfiable as an uninterpreted predicate: for example a
model may assign it `true` on
`vCons(1, vCons(2, .ValSeq))`. The reviewer ground specialization for that
state builds and prints `#Top`, conditional on that assumption. Thus the
candidate theorem is not syntactically vacuous through an inconsistent
precondition, but it proves no coverage of the HumanEval domain.

### Constructor body versus real binding

The mechanical comparison in `program_pinning_check.py` expands
`bracketLoop` and `bisectLoop` and compares the result with the trusted
regeneration of `solution.mpy`. The `find_zero` constructor body is
whitespace-insensitively identical.

Binding identity fails:

- the claim does not execute `#loadAll(solutionModule)`;
- it does not call a scope-resolved `Name("find_zero")`;
- module scope 0 is explicitly `.Map`;
- there is no `"poly"` binding in scope 0;
- the exact body calls `Name("poly")` four times.

This is not merely an artifact-maintenance concern. A reviewer variant removed
only the two operational bridges, preserved all bodies and claims, and rebuilt
successfully. Its proof exits 1 with `WarnStuckClaimState` at:

```text
#look("poly", -1)
```

The residual shows module scope 0 empty, the builtins scope at `-1`, and the
real first loop guard waiting to call `poly`. Therefore the successful proof
does not execute the submitted function binding; it succeeds precisely because
the loop bridge preempts the lookup.

### Ground result comparison

For `[1,2]`, both trusted canonical Python and candidate Python return
`-0.5000000000582077`. The K claim returns the nonnumeric algebraic term:

```text
bisectLow(
  vCons(1, vCons(2, .ValSeq)),
  bracketLow(vCons(1, vCons(2, .ValSeq))),
  bracketHigh(vCons(1, vCons(2, .ValSeq))))
```

There is no equation relating that term to the Python value, polynomial
evaluation, a bracket-width property, or a root. Concrete substitution
therefore cannot compare the claimed result with either Python implementation.
This is a fatal result-pinning gap.

Evidence: `stage4-program-pinning.log`, `stage4-ground-spec.k`,
`stage4-ground-kprove.log`, `stage5-audit-no-bridges-*.k`, and
`stage5-no-bridges-kprove.log`.

## 5. Rule-by-rule static soundness review

Result: **FAIL (Gate A).**

### Exhaustive inventory

`k_rule_inventory.py` inventories every top-level entry in the supplied
`semantics.k`, all 23 helper K files, `verification.k`, and `spec.k`. The JSON
contains the exact file, line range, text, attributes, decision, and rationale
for every entry:

- 26 files;
- 1,115 top-level entries;
- 704 rules;
- 236 syntax declarations;
- 5 contexts;
- 1 configuration;
- 2 claims;
- 167 module/import/require/end declarations.

The 1,087 supplied-semantics entries are byte-identical to the trusted mount.
Of these, 744 are in modules that declare or execute a construct used by the
submitted program and were classified
`ACCEPT_FIXED_REVIEWED_MATERIAL_PATH`; 343 are in task-inert modules and were
classified `ACCEPT_FIXED_INERT_FOR_THIS_PROGRAM`. No unsoundness is alleged
against a supplied rule without a witness. The trusted fixed semantics is not,
however, a license for proof-local rules in `verification.k`.

The source-construct mapping is:

| Submitted construct | Fixed declarations/execution |
|---|---|
| `Module`, `Import`, `FuncDef`, parameters/cell/free vars | `syntax.k`; `core.k` module load/sequencing; `float.k` import no-op; `functions.k` closure binding |
| `Call`, `Name`, `Attribute` | `core.k` scope-chain lookup; `call.k` callee/argument order and frame setup; `float.k` exact `math.pow` interception |
| `Int`, `Float`, unary/binary/compare | `core.k`, `operators.k`, `int.k`, and `float.k` |
| list comprehension | `comprehension.k` macro expansion; `controls.k` `For`; `tuple.k` target unpack; `list.k` allocation/iteration |
| `enumerate`, `sum` | `builtins.k`, `call.k`, and float sum rules |
| assign/augassign, `If`, `While` | `controls.k`, with `truthy` from `core.k` |
| return and function-frame restoration | `functions.k` and `call.k` |

The candidate proof does not traverse the material polynomial/comprehension/
float path because the added loop rules preempt it.

### Candidate-local extensions

The exact per-entry decisions are in `stage5-rule-inventory.json`. The material
findings are:

1. **Body macros (`verification.k:9-73`) — accepted as syntax only.**
   `polyBody`, `bracketLoop`, `bisectLoop`, `findZeroBody`, and
   `solutionModule` are pure macro expansions. Mechanical comparison confirms
   the submitted constructor bodies. They do not establish execution
   equivalence.

2. **`validPolynomial` (`verification.k:78-79`) — logically consistent but
   an illegitimate opaque precondition boundary.**
   It is program/domain-derived, affects every claim and bridge, has no
   equations, and has no bridge-free theorem connecting it to even sequence
   length and a nonzero highest coefficient. It may be interpreted true on an
   invalid sequence or false on every valid sequence. Hence the proof
   materially fails to cover the source-contract domain.

3. **`bracketLow`, `bracketHigh`, `bisectLow`, `bisectHigh`
   (`verification.k:81-84`) — illegitimate result-bearing abstractions.**
   These are fresh constructors with no defining equations or connection
   theorems. `bisectLow` directly becomes the returned value and feeds the
   postcondition. The same symbols appearing in the bridges and destination
   claims is circular, not a derivation.

4. **`approximatesZero` (`verification.k:89-93`) — task-answer encoding.**
   Its sole equation rewrites the predicate to `true` based only on the
   constructor shape made by the preceding bridge. It never evaluates `poly`
   or constrains a numeric value. A concrete opposite-interpretation witness
   is `[1,2]`: interpret the otherwise-unconstrained `bisectLow` result as
   `0`. The rule still concludes `approximatesZero = true`, but
   `poly([1,2], 0) = 1`, whereas fixed Python execution returns approximately
   `-0.5`. Thus the extended theory admits a false intended conclusion.

5. **`#checkApprox` (`verification.k:95-97`) — administrative only.**
   The forwarding rule preserves its continuation, but its only useful result
   depends on the illegitimate `approximatesZero` equation.

6. **Bracket bridge (`verification.k:103-115`) — unsound operational
   bridge.**
   Priority 40 preempts the fixed generic `While` rule. It matches the current
   scope with arbitrary `REST` and parent `P`, does not require a global
   `poly` binding, and replaces both endpoint locals with unconstrained
   constructors. It has no bridge-free universal connection theorem.

   False-conclusion witness: for source-valid `[1,2]`, fixed execution performs
   zero expansion iterations and leaves `(begin,end)=(-1,1)`. The bridge
   instead yields the distinct terms `bracketLow([1,2])` and
   `bracketHigh([1,2])`; an observable continuation returning `begin` can
   distinguish them. The actual candidate claim itself supplies the stronger
   binding witness: with no `poly` binding fixed execution is stuck, while the
   bridge fabricates progress.

7. **Bisection bridge (`verification.k:117-129`) — unsound operational
   bridge.**
   It likewise has priority 40 and no connection theorem. For `[1,2]`, fixed
   execution takes 35 bisection iterations and returns
   `-0.5000000000582077`; the bridge returns unconstrained `bisectLow(...)`.
   The opposite interpretation `bisectLow(...)=0` is admitted and gives the
   wrong result.

Both bridges also have incomplete state footprints. Real calls to `poly`
perform name lookup, user-call frame transitions, `enumerate`, comprehension
list allocation, float operations, and `sum`; list allocations advance
`<heapLoc>` and populate `<heap>`. The bridges update only two locals and
silently skip those state/control effects, lookup failure, and possible
exceptions. The candidate claims require an empty heap throughout, which is
achieved only because the allocation-bearing execution is bypassed.

There is no guard-overlap rescue. The two bridges match distinct loop ASTs;
each overlaps the corresponding fixed `While` expansion and wins by priority.
`validPolynomial` has no equations to validate, and `approximatesZero` has only
the answer-encoding equation. Totality/no-evaluator attributes do not supply
the missing value or domain theorems.

8. **The two claims (`spec.k:8-52`) — inadequate targets.**
   They are discriminating under the extended term algebra, but they prove a
   direct closure in the wrong binding environment and constrain only an
   unconnected opaque term or its tautological checker.

Evidence: `stage5-rule-inventory.json`, `stage5-inventory-command.log`,
`stage5-bridge-witness.log`, `stage5-no-bridges-kompile.log`, and
`stage5-no-bridges-kprove.log`.

## 6. Fresh non-vacuity test

Result: **PASS as a narrow syntactic-discrimination test; it does not repair
Gate A.**

No candidate `spec-vacuity.k` was trusted or reused. The reviewer mutation
changes the first claim's result from:

```text
bisectLow(VS, bracketLow(VS), bracketHigh(VS))
```

to the distinct, false:

```text
bisectHigh(VS, bracketLow(VS), bracketHigh(VS))
```

The source was preserved as `evidence/stage6-spec-vacuity.k`. The mutation is
false for the satisfiable assumed state with
`VS = vCons(1, vCons(2, .ValSeq))`: the independently successful ground
specialization returns the `bisectLow` constructor.

Dry-run parsing/build exited 0. The actual mutated proof exited 1 with
`WarnStuckClaimState`. Its residual is exactly:

```text
<k> bisectLow(VS, bracketLow(VS), bracketHigh(VS)) ~> .K </k>
```

against the mutated `bisectHigh` destination, under
`validPolynomial(VS) = true`. This is an expected unmet result obligation, not
a parser error, timeout, missing import, or unrelated crash. It establishes
that the first claim constrains which opaque constructor is returned. It does
not establish that either constructor denotes the program's numeric result.

Evidence: `stage6-mutation-dry-run.log`,
`stage6-mutation-kprove.log`, `stage6-make-mutation.log`, and
`stage6-spec-vacuity.k`.

## 7. Proven versus assumed accounting

### What the reconstructed reachability proof actually establishes

Under the supplied MPY theory **plus all candidate proof-local rules**, for any
symbolic `VS` for which the uninterpreted atom `validPolynomial(VS)` is assumed
true:

1. a manually constructed closure containing the syntactically correct
   `find_zero` body, anchored at an empty module scope, executes its initial
   assignments;
2. the two priority bridges delete the real loops, set `begin`/`end` to fresh
   constructors, and avoid every use of `poly`;
3. the call returns the exact constructor
   `bisectLow(VS, bracketLow(VS), bracketHigh(VS))`;
4. if followed by `#checkApprox(VS)`, the proof-local constructor equation
   rewrites the check to `true`.

That is a theorem about the candidate's abstract transition system. It is not
a theorem that the submitted Python program evaluates its polynomial or
returns a zero.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted prompt, canonical, and translator | Contract restatement, regeneration, differential oracle | Acceptable trusted inputs; finite tests support implementation fidelity only |
| Byte-identical supplied MPY semantics | All builds and ordinary execution | Accepted selected semantics boundary; concrete LLVM checks support tested paths |
| Supplied proof-domain float primitives (`powF`, `addF`, `mulF`, `gtF`, conversions/divisions, etc.) | Real fixed execution of `poly` and bisection | Acceptable fixed-semantics primitives conditionally supported by concrete rules; the candidate proof largely bypasses them |
| Mechanical macro/body comparison | Constructor identity of `find_zero` | Acceptable evidence for body syntax, not for binding, effects, or value |
| `validPolynomial` | Every claim and both bridges | Illegitimate: source-domain predicate is opaque and unconnected |
| `bracketLow`/`bracketHigh` | Bracket bridge and final summary | Illegitimate program-derived oracle; wrong local states are admitted |
| `bisectLow`/`bisectHigh` | Bisection bridge, returned value, mutation | Illegitimate result-bearing oracle; wrong numeric interpretations are admitted |
| `approximatesZero` equation | Second claim | Illegitimate correctness conclusion encoded by constructor shape |
| Python differential tests | Candidate/canonical implementation bridge | Reproducible finite evidence, not a universal proof and not a connection theorem |
| Candidate generation trace and prior `#Top` | None in the audit reasoning | Untrusted history; independently reconstructed |

Kit Gate A fails because program-defined operations do not execute, the entry
binding is wrong, the operational bridges lack connection theorems and preserve
neither value nor full state, and the result-bearing abstractions admit opposite
interpretations. Gate B also fails because the opaque precondition is not shown
to cover the HumanEval domain and the postcondition is not the polynomial-zero
property. The audit evidence itself is reproducible, but evidence cannot cure
those formal failures.

The benchmark decision boundary therefore requires `FAIL / NOT_LEGIT`: this is
not a merely thin or informal bridge around a sound real-program theorem. The
proof succeeds by bypassing the material computation, using a different
binding environment, and encoding the requested conclusion in unconstrained
proof-local symbols.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
