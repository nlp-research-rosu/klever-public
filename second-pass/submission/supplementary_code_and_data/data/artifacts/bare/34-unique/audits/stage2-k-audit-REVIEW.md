# Independent adversarial audit: HumanEval/34 `unique`

## Conclusion

The submitted Python program is faithful to the trusted canonical program, and
the reconstructed K claims are sound, body-sensitive, and non-vacuous for
finite lists represented entirely by `VInt` values. They do **not**, however,
prove the source contract as written.

The trusted prompt annotates only `l: list` and says “elements”; it does not
restrict elements to integers. The trusted canonical program terminates
normally on other hashable, mutually orderable values. For example,
`unique(["b", "a", "b"])` returns `["a", "b"]` in both Python
implementations. The generated semantics has no string expression/value
production and its only equality/order helpers are `dedupInts`, `removeInt`,
`sortInts`, and `insertInt`.

More decisively, the entry claim's unconstrained `L:List` can be instantiated
with raw K string items. The original post shape then closes with `#Top`, but
only at the stuck term
`VList(sortInts(dedupInts(ListItem("b") ListItem("a") ListItem("b"))))`.
A cleanly built claim for the required value
`VList(ListItem("a") ListItem("b"))` fails with precisely that residual. Thus
the nominally universal postcondition is not a returned-value specification on
a valid part of the source domain.

Under the Kit terminology this is a sound-but-limited integer-list theorem.
The benchmark prompt explicitly maps material HumanEval source-domain narrowing
to `FAIL / NOT_LEGIT`, not to `CONCERNS`.

## 1. Input and provenance integrity

The launcher record declares:

- problem `34-unique`;
- condition `bare`;
- layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference semantics.

The absence of `/reference/reference-semantics` therefore satisfies, rather
than violates, the generated-semantics boundary. `runtime-metrics.json` is
absent, but that record is not required for `legacy-selected-stage1`;
`usage.json` is present and was inspected.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, all required
`/generation-evidence` records, the 5,998-line plain generation log, and all
131 JSONL records in the structured trace. The trace contained 23 tool calls
and 23 outputs. The earlier generation log claimed success but also recorded
four `WarnTrivialClaim` warnings; this was treated only as untrusted history.
See:

- `/audit-output/evidence/logs/02-trace-inventory.log`
- `/audit-output/evidence/logs/03-generation-log-inventory.log`

Independent checks established:

- the campaign-lock JSON is exactly equal to the campaign block in
  `audit-input`;
- all required mounts and all eight required candidate proof artifacts are
  real files/directories with no symlink or unsupported entry;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- every declared file SHA-256 matches, including all generation-evidence leaf
  hashes;
- the independently recomputed retained-candidate tree digest is
  `2f7a374bdcdc710640ea62e9878e29a88d7aca2710fb95f5899e9059cec5d103`,
  matching both `generation-result.json` and `invocation.json`;
- the independently recomputed trace tree digest is
  `7e394359bd353d41d1624d809643d96b71943e0b307872872b2eb7af78b28b5e`,
  matching `usage.json`;
- task-manifest input hashes link to the mounted trusted prompt, translator,
  and generation prompt.

The audit-input launcher tree-digest fields and the independently verified
pipeline tree digests are both recorded in the bounded provenance log. A final
repeat after all experiments produced the same results:

- `/audit-output/evidence/logs/01-provenance.log`
- `/audit-output/evidence/logs/24-final-provenance.log`

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: return the sorted unique elements of the supplied
list. The documented example maps
`[5,3,5,2,3,3,9,0,123]` to `[0,2,3,5,9,123]`.
The trusted canonical body is `sorted(list(set(l)))`; the candidate body is
`sorted(set(l))`. Passing a set directly to `sorted` is behaviorally
equivalent to first converting that set to a list.

Using the trusted translator on the scratch copy produced
`solution.regenerated.mpy`. It is byte-identical to the submitted
`solution.mpy`; both hashes are
`7c0cfa7a98969b3f9b780674f2e26b0a959757bae15d017b1ec0ee8479f84b72`.
Exact command and status are in
`/audit-output/evidence/logs/04-regenerate-mpy.log`.

The independent differential script imports the trusted canonical entry point
and generated entry point from separate files. It exercised:

- the documented example, empty/singleton/all-equal lists;
- equality and ordering branch boundaries;
- sorted, reverse-sorted, negative, and 100-digit integer cases;
- valid strings, tuples, floats, booleans, and mixed boolean/integer cases;
- unhashable and incomparable exception cases;
- 250 deterministic generated integer lists, lengths 0 through 64.

All 266 outcomes matched: 264 returns, two matching `TypeError` outcomes, and
zero mismatches. This is finite program-fidelity evidence, not a proof:

- script: `/audit-output/evidence/differential_test.py`
- log: `/audit-output/evidence/logs/05-python-differential.log`

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/candidate`; the submitted
`kore-exec.tar.gz`, `__pycache__`, and every candidate-built definition/cache
were excluded.

Fresh concrete definition:

```text
kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition semantics-kompiled
```

This exited 0
(`/audit-output/evidence/logs/06-kompile-semantics.log`). The Haskell backend
was used because the locked K installation supports concrete execution and
proof there.

Six concrete executions of the actual regenerated/submitted `solution.mpy`
covered the example, empty and singleton boundaries, all-equal values, both
equality/order branches, negatives, and arbitrary-size integers. Every `krun`
exited 0 and agreed with both Python implementations:

- script: `/audit-output/evidence/concrete_semantics_test.py`
- successful log: `/audit-output/evidence/logs/07b-concrete-semantics.log`

The preserved earlier
`/audit-output/evidence/logs/07-concrete-semantics.log` is a reviewer harness
bug: its regular expression failed to extract visibly correct `VInt` output.
The corrected extractor changed no candidate or K artifact.

Fresh proof definition:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

This exited 0
(`/audit-output/evidence/logs/08-kompile-verification.log`).

The original combined proof and independently isolated copies of each positive
claim all exited 0 and printed `#Top`:

| Target | Evidence |
|---|---|
| Original two-claim `SPEC` | `/audit-output/evidence/logs/09-kprove-original-spec.log` |
| Universal entry claim only | `/audit-output/evidence/logs/10-kprove-entry.log` |
| Ground example claim only | `/audit-output/evidence/logs/11-kprove-example.log` |

All three logs also report `WarnTrivialClaim`: K's function simplifier reduces
the execution and postcondition to the same term before transition rewriting.
That warning is not itself a defect, but makes Stages 4–6 essential.

## 4. Adequacy and real-program pinning

### Plain-language claims

1. **Entry claim.** With `<k>` exactly
   `apply(submitted-unique-module, VList(L))` and no side condition, reach
   `VList(uniqueSpec(L))`, where
   `uniqueSpec(L) = sortInts(dedupInts(L))`.
2. **Example claim.** With `<k>` exactly `run` of the same module on the
   documented integer literal list, reach the documented concrete result.

There are no framed or omitted state cells: the generated configuration has
only `<k>`.

### Program identity

A reviewer-authored constructor parser independently parsed the trusted
regenerated MPY term and extracted the first program argument from each claim.
All three constructor trees have SHA-256
`81427cc60cffe82441b6b6e9aa20ad4c4dd3348b62c6f9eaf7068c4c51683090`
and are structurally identical, including binding name, parameter, return,
call nesting, and `sorted`/`set`/`l` names:

- `/audit-output/evidence/pinning_check.py`
- `/audit-output/evidence/logs/12-constructor-pinning.log`

This is a constructor-level comparison backed by trusted regeneration; no
source-to-proof assumption is needed.

### Satisfiability, concrete substitution, and body sensitivity

The entry precondition is satisfiable. For
`L = [VInt(2), VInt(1), VInt(2)]`, a ground instance proves
`[1,2]` with `#Top`
(`/audit-output/evidence/logs/13-kprove-ground-witness.log`), and Stage 3 shows
the same result in both Python implementations.

A body mutation changed the term actually executed by the claim from
`Return(sorted(set(l)))` to `Return(l)`. Concrete K execution returned
`[2,1,2]`; retaining the old `[1,2]` postcondition produced
`WarnStuckClaimState` and exit 1. Thus the proof is sensitive to the submitted
body, not merely to an external file:

- `/audit-output/evidence/logs/14-krun-body-mutation.log`
- `/audit-output/evidence/logs/15-kprove-body-mutation.log`

### Material adequacy failure

The formal result is meaningful and fully reducible for finite lists of
`VInt`. It is not a value-level specification over the full source contract:

1. `krun` cannot even parse `ListExpr(Str("b"), Str("a"), Str("b"))` because
   `MPY-SYNTAX` has no `Str` production
   (`/audit-output/evidence/logs/16-unsupported-string-domain.log`).
2. Raw string items nevertheless inhabit K's generic `List`, so they satisfy
   the entry claim's apparent `L:List` precondition. The original post shape
   builds and prints `#Top`
   (`/audit-output/evidence/logs/20-string-summary-dry-run.log` and
   `/audit-output/evidence/logs/21-string-summary-proof.log`), but only by
   retaining the partial integer helper term.
3. A spec for the true Python value `["a","b"]` builds successfully, then exits
   1 with a residual equality between that value and
   `sortInts(dedupInts(["b","a","b"]))`
   (`/audit-output/evidence/logs/22-string-intended-dry-run.log` and
   `/audit-output/evidence/logs/23-string-intended-proof.log`).

The preserved probes are:

- `/audit-output/evidence/spec-string-summary.k`
- `/audit-output/evidence/spec-string-intended.k`

This is not a thin-testing concern. It is a ground witness showing that a valid,
terminating source input is outside the meaningful theorem.

## 5. Rule-by-rule static soundness review

The machine inventory found 18 local syntax declarations comprising 25
productions, 11 local `[function]` symbols, 23 local rules, one configuration,
and two claims. It found no `[total]`, `[functional]`, `[simplification]`,
`[owise]`, opaque, priority, or local lemma declaration:

- `/audit-output/evidence/static_inventory.py`
- `/audit-output/evidence/logs/17b-static-inventory.log`
- exhaustive annotated inventory:
  `/audit-output/evidence/rule_inventory.md`

The 23 rules were reviewed as follows:

- R1 (`apply`) faithfully selects the exact singleton function/parameter/body
  used by the claim. Ignoring the function-name field is over-broad for a
  reusable Python module semantics but does not alter this exact binding.
- R2–R6 model integer literals, the sole parameter lookup, list expressions,
  and the ordinary `set`/`sorted` builtins. They preserve the submitted pure
  evaluation dependency (`set(l)` before `sorted`) but intentionally omit
  rebinding and noninteger/exception behavior.
- R7–R9 cover empty, singleton, and multiple expression lists. Their recursion
  descends; any singleton/list-tail syntactic overlap agrees on the result.
- R10 and R12–R16 implement integer duplicate elimination. Equality and
  inequality guards are disjoint and exhaustive for `Int`; both recursions
  shorten finite lists.
- R17–R21 implement insertion sort. Empty/step equations descend, and `<=Int`
  versus `>Int` guards are disjoint and exhaustive.
- R11 sorts the list representation of `VSet`. Every `VSet` reachable from the
  submitted program has already been deduplicated by R10. The raw syntax also
  admits a synthetic `VSet([1,1])`, for which R11 would retain duplicates.
  Because no intended source input reaches that representation directly, this
  is recorded as an over-broad representation-invariant gap, not labeled an
  unsound rule on the submitted path.
- R22's dummy binding is sound for actual ground list-literal arguments, which
  contain no name lookups. It is over-broad for arbitrary `Name` arguments.
- R23 defines `uniqueSpec` as the exact
  `sortInts(dedupInts(L))` computation. It is neither opaque nor an oracle and
  does not preempt execution. It does mean that the K theorem establishes an
  exact computational summary; the claim does not separately prove sortedness
  and uniqueness predicates. Those properties follow from the audited
  deduplication and insertion equations for integers.

Every material constructor in `solution.mpy` maps to syntax and a rule:
`Module`/`FuncDef`/`Params`/`Return` to R1, `Name` to R3, the two `Call`s to
R5–R6, and runtime `ListExpr`/`Int` arguments to R2/R4/R7–R9. R10–R21 cover the
two material builtins. The pure configuration needs no heap, stack, I/O, or
mutation cell for this body.

No candidate rule encodes a fixed task answer, fabricates an unconstrained
result, introduces an opaque branch oracle, or creates a false integer-list
conclusion. The fatal defect is instead missing meaningful semantics for valid
noninteger source inputs. The string witness above is the required concrete
false-adequacy witness; I do not characterize an otherwise truthful integer
equation as globally unsound without such a program-path witness.

## 6. Fresh non-vacuity test

The fresh mutation preserves the exact submitted program and documented input
but changes the final result element from `VInt(123)` to `VInt(124)`:

- `/audit-output/evidence/spec-vacuity.k`

Spec construction/parsing succeeded:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit 0 and the generated `kore-exec --prove` command are recorded in
`/audit-output/evidence/logs/18-vacuity-dry-run.log`.

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual
configuration is the real result ending in `VInt(123)`, which cannot unify with
the mutated post:

- `/audit-output/evidence/logs/19-vacuity-proof.log`

This is a reachable, demonstrably false result obligation—not a parser error,
timeout, crash, or unrelated failure. Non-vacuity passes.

## 7. Proven versus assumed accounting

### Precisely proven

Under the submitted K theory and trusted K backend:

- the exact regenerated function constructor applied to `VList(L)` reaches
  `VList(sortInts(dedupInts(L)))`;
- for every finite ground list consisting of `VInt` items, the local equations
  normalize that term to one copy of each integer in ascending order;
- the documented ground example reaches `[0,2,3,5,9,123]`;
- these results depend on the executed body and reject a false result.

The reachability proof is a partial-correctness theorem. Termination on finite
integer lists is supported by structural descent of `dedupInts`, `removeInt`,
`sortInts`, and `insertInt`; it is not a separate target claim.

### Trust and assumption ledger

| Boundary | Influence | Status and evidence |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell prover | All parsing, simplification, execution, and `#Top` results | Standard toolchain trust; version matches the campaign lock and every definition was rebuilt. |
| Imported K `INT` | Integer literals, equality, `=/=Int`, `<=Int`, `>Int` | Acceptable low-level primitive; mathematical integers align with Python arbitrary-precision integers on the restricted domain. |
| Imported K `LIST` | Finite list construction and matching | Acceptable low-level primitive; list representation is explicit in all claims. |
| Trusted translator | Python AST to constructor identity | Byte-identical translator plus byte-identical regenerated MPY and independent constructor-tree comparison. |
| Ordinary Python builtin bindings | Meaning of names `set` and `sorted` | Conditional assumption: no monkeypatching/rebinding. Appropriate for the benchmark's pure call setting. |
| `VInt` list ↔ Python integer-list bridge | Relates generated semantics to real Python | Audited rule derivation plus six K/Python concrete comparisons and 250 broader Python differential integer cases. Finite tests support but do not replace the rule argument. |
| `uniqueSpec` meaning | Final postcondition for integer lists | Defined by exhaustive, descending local equations; not opaque. Sortedness/uniqueness is an ordinary mathematical argument over insertion sort and duplicate elimination, not a separate K predicate theorem. |
| Noninteger source elements | Full unqualified `list` contract | **Illegitimate exclusion.** Python string/tuple/float/bool returns exist; string K execution/post evidence demonstrates the theorem does not supply the required value. |
| Python exceptions for unhashable/incomparable elements | Exceptional behavior | Not modeled. This is secondary to the stronger defect on normally returning string inputs. |

Differential and concrete tests support only their tested bridges. They are not
used as substitutes for the K reachability proof.

### Validation gates and benchmark mapping

- **Gate A, real-program soundness on the modeled finite-`VInt` domain: PASS.**
  Exact-body pinning, rule validity, satisfying witnesses, body sensitivity, and
  false-result non-vacuity all pass.
- **Gate B, intent adequacy: FAIL.** The proof materially narrows an
  unqualified list-element contract and admits a stuck “summary” where a valid
  source input has a concrete result.
- **Gate C, auditability of the restricted theorem: PASS.** Commands, statuses,
  scripts, mutations, assumptions, and bounded outputs are preserved. This
  does not repair Gate B.

The candidate Python implementation appears correct. The candidate proof is
not a legitimate proof of that program over the real source-contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
