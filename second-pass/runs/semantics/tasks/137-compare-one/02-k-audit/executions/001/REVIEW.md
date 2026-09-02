# Independent adversarial audit: 137-compare-one

The candidate is **not a legitimate proof of the requested comparison
function**. Fresh reconstruction confirms that all nine submitted claims close,
but they close only after candidate-local priority rules replace decimal
conversion and float equality with two unconstrained, result-bearing symbols.
No connection theorem gives either symbol its claimed meaning. Fresh opposite
interpretations make the extended K theory prove two concrete results that both
the trusted canonical implementation and the submitted Python implementation
contradict. Independently, the submitted implementation diverges from the
trusted canonical implementation on valid integer inputs at the binary64
precision boundary.

This is a candidate failure, not an infrastructure finding. K v7.1.337 was
available; both definitions rebuilt from clean source; every positive claim ran;
and the fresh false-result mutation failed for the expected semantic reason.

## 1. Input and provenance integrity

### Trusted-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode. The candidate tree was recursively compared with
the trusted tree using `lstat`-based type checks and SHA-256 hashes, without
following symlinks:

- candidate and trusted semantics each contain 25 entries;
- there are zero missing, additional, changed, mistyped, or symlinked entries;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- `solution.py`, `solution.mpy`, `spec.k`, `verification.k`,
  `concrete.mpy`, and `prove.sh` are regular files, not symlinks.

The exact inventory, hashes, and comparison are in
[`stage1-integrity.log`](evidence/stage1-integrity.log) and
[`stage1-candidate-inventory.log`](evidence/stage1-candidate-inventory.log).
This integrity result trusts the supplied semantics tree; it does **not** bless
the proof-specific rules in `verification.k`.

### Missing and extraneous provenance records

The following named records are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace

There is no candidate `PROOF.md` or `spec-vacuity.k`. The candidate also contains
an untrusted Python bytecode cache and `kore-exec.tar.gz`; neither was used.
These are provenance/evidence limitations. They are not the primary reason for
the verdict because the source proof could still be independently reconstructed.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt admits two arguments that are integers, floats, or strings
representing real numbers; a string may use `.` or `,` as its decimal separator.
The function returns the original argument whose numeric value is larger,
preserving its original type, and returns `None` when the numeric values are
equal.

The trusted canonical implementation first replaces commas in strings, converts
**both** normalized operands with `float`, compares those binary64 values, and
returns one of the original arguments. The submitted implementation converts
only strings; integer and float arguments are compared by Python's native mixed
numeric comparison.

### Translation fidelity

Running the trusted translator from the isolated scratch copy produced
`regenerated-solution.mpy` with the same SHA-256 hash as the submitted
`solution.mpy`:

```text
9f84dacfa99a22ea539c1e8b97d3e483a50265ec4243a70c68f0ccc08b35ab37
```

The `cmp` exit status is 0. Command and output:
[`stage2-translate.log`](evidence/stage2-translate.log).

### Independent differential result

[`differential_compare.py`](evidence/differential_compare.py) imports the
trusted and submitted entry points independently. It covers the four documented
examples, explicit equality/less/greater boundaries, zero and signed zero,
comma and dot forms, empty/malformed robustness cases, values around `2**53`,
very large integers, and a seed-137 cross-product of representative generated
values. It ran 14,663 pairs and found 11 divergences
([`stage2-differential.log`](evidence/stage2-differential.log), exit 1).

One material in-domain divergence is:

```text
a = 9007199254740992
b = 9007199254740993
canonical -> None
submitted -> 9007199254740993
```

Both arguments are valid integers under the stated domain. The canonical
implementation converts them to equal binary64 values; the submitted function
compares them as exact Python integers. Extremely large integers also diverge:
the canonical conversion raises `OverflowError`, whereas the submitted function
returns an integer. A different algorithm would be acceptable if materially
equivalent on the intended domain; this one is not equivalent to the trusted
canonical behavior.

## 3. Clean proof reconstruction

All execution occurred in `/tmp/audit-work` from copied source artifacts.
Candidate-provided compiled definitions, caches, and the tar archive were not
used.

### Toolchain and concrete definition

The installed `kompile`, `kprove`, and `krun` are K v7.1.337
([`stage3-toolchain.log`](evidence/stage3-toolchain.log)).

The concrete definition was freshly built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Build exit: 0. The compiler emitted several baseline non-exhaustiveness warnings
for unused helpers; none blocked the build. See
[`stage3-runtime-build.log`](evidence/stage3-runtime-build.log).

`krun concrete.mpy --definition runtime-kompiled` exited 0. All six assertions
were consumed and the final `<k>` was `.K`
([`stage3-concrete-run.log`](evidence/stage3-concrete-run.log)).

### Proof definition and every positive claim

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Build exit: 0
([`stage3-proof-build.log`](evidence/stage3-proof-build.log)).

Each target claim was then selected and run independently:

| Claim | Exit | Output |
|---|---:|---|
| `int-int` | 0 | `#Top` |
| `int-float` | 0 | `#Top` |
| `int-str` | 0 | `#Top` |
| `float-int` | 0 | `#Top` |
| `float-float` | 0 | `#Top` |
| `float-str` | 0 | `#Top` |
| `str-int` | 0 | `#Top` |
| `str-float` | 0 | `#Top` |
| `str-str` | 0 | `#Top` |

The summary and individual exact commands are in
[`stage3-all-claims-summary.log`](evidence/stage3-all-claims-summary.log) and
`evidence/stage3-claim-*.log`.

This establishes verification under the submitted theory. It does not establish
that the submitted theory truthfully models decimal conversion or float
equality; stages 4 and 5 reject that inference.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

All nine claims have the same initial cells: module environment 0, an empty
module scope whose parent is the supplied builtins scope, fresh scope location
1, empty heap and stack, `noRet`, `NoExc`, and exit code 0. There is no
`requires` clause. Their only difference is the Cartesian product of argument
sorts:

- `Int × Int`
- `Int × Float`
- `Int × str(IntSeq)`
- `Float × Int`
- `Float × Float`
- `Float × str(IntSeq)`
- `str(IntSeq) × Int`
- `str(IntSeq) × Float`
- `str(IntSeq) × str(IntSeq)`

Each claim says that `runCompare(A,B)` reaches `expectedCompare(A,B)`, with the
other cells restored to their initial values. `IntSeq` is unrestricted, so the
formal string domain is actually broader than the prompt's numeric strings.
There are no loop or helper claims.

[`stage4_satisfying_inputs.py`](evidence/stage4_satisfying_inputs.py) supplies a
ground witness for each of the nine sort pairs. On those nine selected inputs,
the intended ground result and both Python implementations agree
([`stage4-satisfying-inputs.log`](evidence/stage4-satisfying-inputs.log)).
Thus no entry precondition is vacuous.

### What executes in `<k>`

The claims do not load or execute `solution.mpy`. They start from the fresh
constructor `runCompare`, whose rule expands to `#applyK(toCall(closureVal(...)))`
containing a manually embedded copy of the translated function body. The copy
is textually exact, and normal call/frame rules then bind arguments, execute
assignments and branches, and pop the frame on return. This is good informal
correspondence evidence, but it is not a K-level body-identity or module-loading
claim.

The body-sensitivity experiment makes the limitation concrete. A scratch
`solution.py`/`solution.mpy` was changed so `compare_one(1,2)` returns 1. The
definition rebuilt and `int-int` still proved `#Top`, because neither build nor
claim reads the mutated program artifact. See
[`solution-body-mutation.py`](evidence/solution-body-mutation.py),
[`stage5-body-mutation-python.log`](evidence/stage5-body-mutation-python.log),
and [`stage5-body-mutation-proof.log`](evidence/stage5-body-mutation-proof.log).
For the actual unmutated submission, byte equality plus the manual AST check
partially bridges this gap, but the theorem itself is not source-sensitive.

### Result constraint

For `Int × Int`, `expectedCompare` reduces to a concrete integer comparison. A
fresh ground claim `runCompare(1,2) => 2` closes.

For float and string cases, the destination is not the intended concrete result:

- normalized strings become candidate-defined `commaDecimal(CS)`;
- float/float equality becomes candidate-defined `sameFloat(A,B)`;
- mixed equality and ordering may retain supplied opaque primitives such as
  `eqF`, `gtF`, and `intToF`.

Ground claims for `runCompare(3.0,3.0) => noneV` and
`runCompare(1,"2,3") => "2,3"` do not close. The logs expose unresolved
`sameFloat`/`commaDecimal` conditions and missing Haskell float hooks:
[`stage4-ground-float-equal.log`](evidence/stage4-ground-float-equal.log) and
[`stage4-ground-int-str.log`](evidence/stage4-ground-int-str.log). Those backend
hook errors are diagnostic only and are not used as a verdict basis. The
independent model witnesses in stage 5 establish the substantive unsoundness
without relying on those failures.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule_inventory.py`](evidence/rule_inventory.py) generated
[`rule-inventory.tsv`](evidence/rule-inventory.tsv), one source-preserving record
per declaration/rule/claim. Its SHA-256 is
`16bff16be73ab74e577f4e4170788ffd1d9c5b16301c98f04d384adfe8c12cf2`.
The 956 records comprise:

- 234 syntax declarations;
- 707 rules: 241 operational and 466 equational;
- 9 reachability claims;
- 5 contexts;
- 1 configuration.

Attribute counts, which overlap, are 150 `function`, 109 `total`, 27 `symbol`,
24 `no-evaluators`, 47 priority, 35 `concrete`, 26 `owise`, four macro, two
strict, and one seqstrict. There are no local `simplification` or `functional`
declarations. Full per-file counts are in
[`rule-inventory-summary.json`](evidence/rule-inventory-summary.json).

[`annotate_rule_inventory.py`](evidence/annotate_rule_inventory.py) attaches a
review disposition and, where applicable, a false-conclusion witness to every
one of the 956 records. The result is
[`rule-review.tsv`](evidence/rule-review.tsv), with zero unclassified records.
The 928 supplied-semantics records are byte-identical to the trusted tree: 175
are on the real entry path and 753 are unused by this program. Unused rules were
not treated as proof assumptions or labeled unsound without a witness.

### Used supplied-semantics path

The submitted body uses `Module`/`FuncDef` only outside the claim adapter, then
`Params`, `Assign`, `Name`, `If`, `Call`, `Attribute`, `Str`, `Compare`,
`CmpOp`, `Return`, and `NoneVal`.

- `syntax.k` declares all those AST forms. Strictness/contexts give assignment
  RHS and `If` condition evaluation, while the two comparison contexts evaluate
  left then right.
- `core.k` declares the value sorts and complete cells. Name lookup follows the
  local scope to builtins; argument accumulation is left-to-right; literals
  cool to `Val`.
- `call.k` invokes closures by allocating scope 1, pushing the caller frame,
  binding both parameters, executing the body, and appending `#endcall`.
- `functions.k` binds the parameters, records a returned value, restores
  environment 0, deletes the callee scope, resets the scope allocator, and
  empties the stack.
- `controls.k` writes `a_value` and `b_value` in the callee scope and dispatches
  each `If` on `truthy(Bool)`.
- `builtins.k` implements the sort-disjoint `isinstance(_, str)` test.
- `methods.k` defines `replace` by the total, descending `replaceC`; its equal
  and unequal guards are disjoint and exhaustive on code lists.
- `operators.k`, `int.k`, and `float.k` route equality and greater-than after
  operands are values. The relevant supplied float helpers (`eqF`, `gtF`,
  `intToF`, and `decStrToF`) are explicit no-evaluator/concrete-twin trust
  boundaries.

No list, tuple, dictionary, set, range, comprehension, subscript, iteration,
sort, allocation, output, mutation, or exception rule is on the submitted
function path. `MPY-CONCRETE` is not imported into the proof module. The
priority rules on the used supplied path have disjoint guards or agreeing
right-hand sides; repeated mixed-float equations agree. No baseline overlap
explains the candidate's success.

### Exhaustive candidate-local review

`verification.k` contributes seven syntax declarations and twelve rules:

1. `commaDecimal(IntSeq)` at lines 11–12 is declared
   `[function, total, symbol, no-evaluators]` but has no defining equation.
   It is a result-bearing, program-derived oracle.
2. `#commaDecimal` at line 13 is only an internal continuation tag.
3. The priority-40 rule at lines 14–18 preempts the normal call semantics for
   the exact `float(E.replace(",", "."))` shape. It evaluates only `E`, skips
   lookup of the `float` binding and execution of `replace`, and accepts any
   continuation and cells because none are constrained.
4. The rule at line 19 turns the evaluated string into
   `commaDecimal(CS)`. No bridge-free universal claim proves
   `commaDecimal(CS) = decStrToF(replaceC(CS,44,46))`.
5. `sameFloat(Float,Float)` at lines 24–25 is also total and result-bearing but
   has no defining equation.
6. The priority-40 rule at lines 26–28 preempts supplied float equality after
   both operands are evaluated and replaces it with `sameFloat`. No bridge-free
   claim proves equality with the supplied float comparison.
7. `runCompare` at lines 34–57 is an exact-body wrapper. Its frame/state
   footprint follows the supplied call semantics, but it has the source-pinning
   gap described in stage 4.
8. `numericValue` at lines 60–63 has truthful, sort-disjoint equations for the
   three entry forms. It is partial on other `Val` constructors, which the
   entry claims do not use.
9. `numericEqual` at lines 65–69 has four sort-disjoint equations. Its shape
   mirrors execution but remains conditional on fixed opaque float primitives
   and candidate `sameFloat`.
10. `expectedCompare` at lines 73–81 is a sound if/then/else expression only
    relative to those symbols. It does not establish that the symbols denote
    real-number conversion or equality.

The two priority rules do preempt the generic `Call` and `Compare` rules; rule
priority supplies no equivalence proof. There are no auxiliary or connection
claims anywhere in `verification.k` or the supplied tree
([`stage5-connection-claim-search.log`](evidence/stage5-connection-claim-search.log)).

### Required false-conclusion witnesses

The following witnesses are both within the intended argument domain:

1. For `(1.0, 2.0)`, admit `sameFloat(1.0,2.0) = true`. The bridge takes the
   equality branch and returns `noneV`. Supplied concrete float equality is
   false, and both Python implementations return `2.0`.
2. For `("2,3", 0.0)`, admit `commaDecimal("2,3") = 0.0` and the truthful
   `sameFloat(0.0,0.0) = true`. The bridge returns `noneV`. Real normalization
   produces 2.3, and both Python implementations return the original `"2,3"`.

These are not merely hypothetical prose models.
[`oracle-witness-verification.k`](evidence/oracle-witness-verification.k) adds
the admitted ground interpretations without changing the candidate bridge or
body. Its clean Haskell build exits 0. Both false ground reachability claims in
[`oracle-witness-spec.k`](evidence/oracle-witness-spec.k) then exit 0 with
`#Top`:

- [`stage5-wrong-same-float.log`](evidence/stage5-wrong-same-float.log)
- [`stage5-wrong-comma-decimal.log`](evidence/stage5-wrong-comma-decimal.log)

The independently executed Python outcomes are recorded in
[`stage5-oracle-witness-python.log`](evidence/stage5-oracle-witness-python.log).
This demonstrates exactly what the unconnected oracles permit: a false
task-level conclusion while the oracle-relative proof closes.

Accordingly, the `commaDecimal` and `sameFloat` declarations and their
operational bridges are materially illegitimate. The narrower issue is not that
an uninterpreted symbol is inherently inconsistent; it is that these
program-derived values control the return and occur again in the postcondition
without a universal connection theorem.

## 6. Fresh non-vacuity test

[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) is reviewer-authored and
does not reuse candidate vacuity evidence. It changes the result obligation for
the satisfying input `(1,2)` from the actual integer result 2 to `noneV`.
Both Python implementations return 2.

The dry run:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --claims false-int-result --dry-run
```

exits 0, establishing that the mutation parses and builds
([`stage6-vacuity-dry-run.log`](evidence/stage6-vacuity-dry-run.log)).

The proof command without `--dry-run` exits 1 with
`WarnStuckClaimState`. Its final configuration contains `<k> 2 ~> .K </k>`,
which does not unify with the mutated `noneV` destination
([`stage6-vacuity-proof.log`](evidence/stage6-vacuity-proof.log)).

This is valid non-vacuity evidence for the concrete integer result obligation.
It does not validate the float/string claims, whose RHS deliberately shares the
unconstrained symbols.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the supplied semantics plus all candidate rules, for each of the nine
argument-sort pairs and the exact initial configuration, if execution from the
fresh `runCompare` wrapper terminates, the returned K value is the term
`expectedCompare(A,B)` and the call frame is cleaned up. This is a
partial-correctness statement about an embedded body and an oracle-relative
summary.

For `Int × Int`, that summary reduces to exact K integer equality/order. For
float and string cases, it is conditional on opaque fixed primitives and on
the candidate's unconstrained `commaDecimal`/`sameFloat`. The proof does not
establish that those candidate symbols mean decimal parsing or float equality.
It therefore does not establish the natural-language result for the full
claimed domain.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.337 compiler, LLVM backend, Haskell prover | all machine results | Ordinary toolchain trust; available and reproducible. |
| Trusted supplied semantics tree | all execution | Acceptable selected semantics boundary; candidate copy is exact. |
| Supplied `eqF`, `gtF`, `intToF`, `decStrToF` and other concrete-twin float symbols | mixed/float/string paths | Explicit low-level fixed-semantics boundary. Symbolic theorems using them remain conditional; LLVM examples give finite evidence only. |
| Trusted translator | Python-to-MPY correspondence | Acceptable; regenerated MPY is byte-identical. |
| Manual embedded-body equality | `runCompare` entry | Informal bridge only; body mutation shows no formal source sensitivity. |
| Candidate `commaDecimal` | every string claim and returned branch | Illegitimate program-derived oracle; no equations, universal connection theorem, or faithful opposite-interpretation rejection. |
| Candidate `sameFloat` | float/float equality and related string paths | Illegitimate program-derived oracle; no equations or connection theorem. |
| Concrete smoke assertions | six examples | Finite evidence only, not a proof or connection theorem. |
| Reviewer differential testing | canonical/implementation bridge on 14,663 pairs | Finite evidence; it actually finds material divergence. |
| Missing generation records | provenance narrative | Evidence limitation; not needed to reproduce the decisive failures. |

### Decision

Fresh closure and a successful non-vacuity mutation cannot rescue a theorem
whose result-bearing semantics is circular. The candidate-specific bridge
symbols appear both in execution and in `expectedCompare`, so `#Top` proves
agreement with the same unfixed oracle rather than agreement with real numeric
conversion and comparison. The two machine-checked opposite interpretations
are concrete false-conclusion witnesses. The independent canonical divergence
and source-pinning limitation are additional adequacy failures.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
