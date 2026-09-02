# Independent adversarial review: 95-check-dict-case

## Outcome

The candidate contains a sound, non-vacuous partial-correctness proof of the
actual submitted `solution.mpy` over the complete source-valid domain represented
by the supplied MPY model. The proof was reconstructed from source, not from the
candidate's compiled directories or claimed logs. Its only operational bridge
has a bridge-free arbitrary-continuation connection proof, and the target result
is constrained by an independently proved unbounded loop invariant.

The review is not a clean `PASS` because the supplied read-only semantics has a
documented Unicode representation/behavior gap. Its string-literal conversion
is ASCII-only and its `islower`/`isupper` predicates recognize only ASCII case.
For the concrete boundary witness U+00E9, CPython and the submitted Python
program return `True` for `{"é": 1}`, while the fixed model's manual
`str(iCons(233, .IntSeq))` representation makes both `islower` and the proved
summary `False`; translating and executing the Unicode literal also fails in
the fixed LLVM model. This originates entirely in the supplied semantics. The
symbolic theorem covers every source-valid input the fixed model represents,
and the submitted Python program is faithful on the gap. Campaign amendment v2
exception 1 therefore maps this limitation to `CONCERNS / LEGIT`, not to
`FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. I independently inspected the launcher
record, its `container_paths`, recorded hashes, integrity fields, and the
following required pipeline records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- invocation, metrics, runtime metrics, usage, final response, output log, and
  prompt below `/generation-evidence`;
- the structured 2,109-line trace, including its session metadata, user task,
  359 function calls, 122 custom tool calls, selected usage event, patched
  targets, and final claim.

All required launcher records and provenance mounts are present, regular where
required, and readable. Every directly recorded SHA-256 digest matches the
mounted bytes. The trace member's independently calculated digest is
`d0a0e0de...5f6ed3`, exactly the value in `generation-result.json`.
The `audit_campaign` object is structurally equal to
`/audit-campaign-lock.json`, whose SHA-256 is the value recorded in
`audit-input.json`. There is no infrastructure breach.

The candidate prompt and translator are byte-identical to their trusted mounts.
The trusted and candidate `reference-semantics/` trees each contain exactly 24
regular files and two directories, contain no symlinks, and have no missing,
additional, mistyped, or changed entry under recursive no-dereference
comparison. Their independently generated per-file hash manifests are
identical. This establishes integrity only; it does not bless
`verification.k`.

Candidate-built `runtime-kompiled`, `verification-kompiled`,
`connection-kompiled`, bytecode, and caches were not used. A source-only copy
was made below `/tmp/audit-work/case95`.

Evidence:

- `evidence/stage1_integrity.sh`
- `evidence/stage1_integrity.log`
- `evidence/candidate-file-hashes.txt`
- `evidence/trusted-semantics-file-hashes.txt`
- `evidence/candidate-semantics-file-hashes.txt`
- `evidence/stage1_trace_summary.py`
- `evidence/stage1_trace_summary.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The docstring requires `check_dict_case(d)` to return `False` for an empty
dictionary, and otherwise return `True` exactly when either:

1. every key is a string in lower case; or
2. every key is a string in upper case.

Mixed case, uncased strings, and any non-string key make both alternatives
false. Dictionary values are immaterial. The five examples are mutually
consistent.

### Submitted program

`solution.py` initializes lower/upper accumulators to true and a nonempty flag
to false. For every key, it records nonemptiness, checks stringness, and
conjoins the corresponding `islower` and `isupper` results. It returns
nonempty-and-(all-lower-or-all-upper). This is a direct implementation of the
docstring, with normal CPython Unicode behavior.

Running the trusted `/reference/py2mpy.py` on the scratch copy of
`solution.py` produced SHA-256
`cd80fd23c17f732a7cd612ed1bc149fced7078f2f452f4906704e18e75c720e4`.
The submitted `solution.mpy` has the same digest and is byte-identical.

The independent differential imports both the trusted canonical entry point
and the submitted entry point. Its oracle was separately written from the
docstring. It covered:

- all five documented examples;
- 21 explicit empty, case, type, uncased, digit, punctuation, and Unicode
  boundaries;
- every insertion sequence through length four over a 17-value branch-oriented
  key pool, including real dictionary de-duplication;
- 5,000 deterministic generated dictionaries.

Across 93,767 cases the candidate had zero oracle mismatches. The canonical
helper had 7,190 mismatches because its control flow breaks after a second key
that continues the established case and can ignore a bad third key. For
example, canonical returns `True` for `{"a": 0, "b": 0, 8: 0}`, while the
docstring and candidate require `False`. Under campaign amendment v3 this is
not a candidate defect: canonical is a helper witness, and the candidate
satisfies the docstring.

Evidence:

- `evidence/stage2_translation.log`
- `evidence/stage2_differential.py`
- `evidence/stage2_differential.log`

## 3. Clean proof reconstruction

K version 7.1.293 was available independently. All definitions were built
under fresh names in the source-only scratch tree.

The following fresh commands exited zero:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kompile --backend haskell connection.k \
  --main-module CONNECTION --syntax-module MPY-SYNTAX \
  --output-definition audit-connection-kompiled
```

The LLVM build emitted supplied-semantics non-exhaustiveness warnings for
unrelated operations such as float conversion, `joinCodes`, and out-of-bounds
subscript. None is reached by this program. The proof builds emitted only
unused-variable warnings from the supplied string order rules.

Every positive proof artifact was then run:

```text
kprove connection-spec.k --definition audit-connection-kompiled \
  --spec-module CONNECTION-SPEC
Exit 0, output #Top

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop
Exit 0, output #Top

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop,SPEC.target \
  --trusted SPEC.loop
Exit 0, output #Top
```

Trusting `SPEC.loop` only in the composition command is legitimate here because
the exact same loop claim was first proved separately without being trusted.
The connection run proves all three claims in `CONNECTION-SPEC`.

The trusted translator also regenerated the smoke term. Fresh fixed LLVM and
extended Haskell executions reached `.K`, empty stack, `NoExc`, exit code zero,
identical heap and allocation cells, and the six expected results. Their full
final configurations were byte-identical, with common SHA-256
`db2f54a4...f4be25f8`.

Evidence:

- `evidence/stage3_kompile_runtime.log`
- `evidence/stage3_kompile_verification.log`
- `evidence/stage3_kompile_connection.log`
- `evidence/stage3_kprove_connection_all.log`
- `evidence/stage3_kprove_loop.log`
- `evidence/stage3_kprove_target.log`
- `evidence/stage3_smoke_runtime_diff.log`

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop` starts at the real `#loop(list(KS), Name("key"), body)` cutpoint,
with arbitrary current Boolean accumulators and an exact
`Return(checkDictReturn()) ~> #endcall` suffix. For an arbitrary finite,
non-reference key suffix it executes the real loop body and updates:

- `all_lower` to its prior value conjoined with lower-case stringness of every
  remaining key;
- `all_upper` analogously;
- `seen_key` by whether the remaining suffix is nonempty.

`SPEC.target` starts from the initial MPY configuration, loads a module
containing the complete submitted function binding, calls it on an arbitrary
symbolic `dictV(KS, VALUES)`, and reaches `.K` with:

- the exact loaded closure still bound;
- `result |-> checkCaseSummary(true, true, false, KS)`;
- the expected one allocated key-list object;
- empty stack, `noRet`, `NoExc`, and exit code zero.

Its precondition is `notBool hasRefVS(KS)`. This excludes only `ref` keys in an
initially empty heap. In the fixed model such values are dangling or represent
mutable list objects, which are not valid CPython dictionary keys. Direct
strings, integers, booleans, tuples, dictionaries, closures, builtins, and all
other direct `Val` constructors remain covered. There is no size bound.
Ill-formed symbolic `dictV` values with duplicate keys or mismatched value
lengths are even included; because this program reads only `keys()`, that
overbreadth does not falsify the theorem.

Both preconditions are satisfiable. Examples include `L = 1, KS = .ValSeq` for
the loop and `KS = VALUES = .ValSeq` in the initial target configuration.

### Mechanical identity and result constraint

A reviewer script extracted the first target `FuncDef` by balanced
constructor delimiters. It performed only the list-syntax normalization
`.Exprs` to the program parser's empty position, then parsed both terms through
K's own parser. The trusted-regenerated module and target-extracted module
produced byte-identical KORE with SHA-256
`69360b76...3307e73`. Thus the target loads the submitted function name,
parameters, and body, not a substituted algorithm.

Five concrete summaries—empty, one lowercase key, one uppercase key, mixed
case, and a non-string key—closed together with `#Top`. Their claimed Boolean
results exactly matched both Python implementations. The target result is not
free: it is the explicit summary term in the final module scope.

A body-sensitivity mutation changed `all_lower` from true to false in both the
program term actually executed and the closure body required on the RHS, while
leaving the claimed original result summary unchanged. It parsed and executed
but `kprove` exited 1 with `WarnStuckClaimState`; the residual exposes the
changed `foldLowerKeys(false, KS)` against the old result obligation. This is
body-sensitive evidence, not a mutation of an unused external source file.

Evidence:

- `evidence/stage4_extract_target.py`
- `evidence/stage4_pinning_and_concrete_v2.log`
- `evidence/stage4_summary_spec.k`
- `evidence/stage4_kprove_summary_instances.log`
- `evidence/stage4_concrete_compare.py`
- `evidence/stage4_body_mutation.k`
- `evidence/stage4_body_mutation_proof.log`

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-authored inventory enumerates every top-level `requires`, module,
import, configuration, syntax declaration, context, rule, and claim in all 24
supplied K files plus `semantics.k`, `proof-theory.k`, `verification.k`,
`connection.k`, `connection-spec.k`, and `spec.k`. It contains 1,383 records,
including 253 syntax declarations, 789 rules, five contexts, one
configuration, and five claims. It separately identifies every occurrence of
`function`, `functional`, `total`, `symbol`, `no-evaluators`, `priority`,
`simplification`, `concrete`, `owise`, `macro`, `strict`, and `seqstrict`.

The proof-local portion is small enough to account for directly:

- `proof-theory.k`: six syntax-declaration groups and 19 rules, defining 12
  total helper symbols; one opaque symbol (`stringCodes`); six simplification
  rules; one `owise` discriminator rule.
- `verification.k`: three total zero-argument AST aliases and six rules; two
  guarded method simplifications; one priority-40 operational bridge.
- No local `functional`, `concrete`, macro, exception, allocation, return,
  frame-pop, loop-skip, or result-writing rule exists.

Evidence:

- `evidence/stage5_inventory.py`
- `evidence/stage5_rule_inventory.log`
- `evidence/stage5_fixed_attributes.txt`
- `evidence/stage5_local_attributes.txt`

### Used-construct mapping

| Submitted construct | Fixed declaration and execution rules |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll` and sequence rules |
| `FuncDef`, call, parameter, return | `syntax.k`; `functions.k` frame/return rules; `call.k` closure dispatch |
| `Assign`, `Name` | `syntax.k`; `controls.k` assignment; `core.k` scope lookup |
| `Bool`, `NoneVal` | `syntax.k`; `core.k` literal rules |
| `BoolOp("and"/"or")` | `syntax.k`; left-to-right, short-circuit rules in `bool.k` |
| `For` over `dict.keys()` | `controls.k` loop protocol; `dict.k` fresh key-list allocation; `list.k` iterator rules |
| `Call`, `Attribute` | `syntax.k`; callee/argument evaluation and method routing in `call.k` |
| `isinstance(key, str)` | builtin binding/lookup in `core.k`; dispatch in `call.k`/`builtins.k`; exact local bridge |
| `key.islower/isupper()` | bound method routing in `call.k`; fixed formulas and ASCII helpers in `methods.k`; guarded local twins |

This chain executes lookup, callee evaluation, left-to-right arguments,
allocation of the `keys()` list, per-key target binding, short-circuit control,
method calls, assignments, return, frame restoration, and all observable cells.

### Proof-local extension decisions

1. **AST aliases** `checkDictLoopBody`, `checkDictReturn`, and
   `checkDictBody` are definitional summaries. They are zero-argument,
   terminating equations and expand to the literal translated terms. The KORE
   pinning check independently confirms the target's literal body.

2. **`isStringKey`** is a complete constructor discriminator:
   `str(_) => true`, and the disjoint `owise Val => false`. It agrees with the
   fixed `isStrV` equations on every `Val`. Therefore the global
   `isStrV(V) => isStringKey(V)` simplification is a true equation, not an
   answer oracle.

3. **`stringCodes`** is an opaque total destructor with one equation,
   `stringCodes(str(CS)) = CS`. Its value is intentionally unspecified on
   non-strings. That is an evidence boundary, but not a false equation. Every
   result-bearing observation is guarded by `isStringKey(V)`, which reduces the
   domain to `V = str(CS)` where the value is fixed. The non-string branches of
   `lowerKey` and `upperKey` return false without consulting it.

4. **Case predicates and folds** are definitional summaries. `lowerKeyCodes`
   and `upperKeyCodes` copy the fixed method formulas. The string/non-string
   guards of `lowerKey` and `upperKey` are disjoint and exhaustive. The fold
   base/constructor cases are disjoint, structurally descending, and
   exhaustive over `ValSeq`; `hasAnyKey` and `checkCaseSummary` are similarly
   total.

5. **Guarded `applyMethod` simplifications** overlap fixed method rules only
   when `V = str(CS)`. On that complete guard domain, `stringCodes(V) = CS`,
   and each RHS is exactly the fixed method formula. They read no cell and
   affect no control, heap, stack, exception, allocation, or continuation.

6. **The priority-40 `isinstance` bridge** matches only the post-lookup,
   post-argument-evaluation redex
   `#applyK(toCall(builtinV("isinstance")), (V,typeV("str"),.Vals))`.
   Its `notBool isRefV(V)` guard is disjoint from fixed heap dereference. For
   that domain the skipped fixed path is pure: generic builtin dispatch followed
   by `isStrV(V)`. `CONNECTION-SPEC.isinstance`, compiled without importing
   `VERIFICATION`, proves the exact fixed redex reaches `isStringKey(V)` for an
   arbitrary `CONT:K`. The two method connection claims likewise retain
   arbitrary continuations. Thus match context is contained in justification
   context, binding is already resolved, and all state cells are preserved.

The three bridge-free connection claims closed. Fixed-versus-extended ground
execution was byte-identical. Deliberate opposite interpretations
`lowerKey("a") = false`, `lowerKey(8) = true`, and
`stringCodes("a") = []` each parsed and failed with the actual opposite value
in the residual. No candidate-authored rule admits a concrete or symbolic false
conclusion on the theorem domain, so no rule is labeled unsound.

Evidence:

- `evidence/stage5_abstraction_opposites.sh`
- `evidence/stage5_abstraction_opposites.log`
- the three `evidence/stage5_abstraction_opposite_*.k` files

### Supplied-model gap

The fixed files are the campaign's trusted model boundary, not candidate
extensions. Unused fixed opaque float, sort, and MD5 symbols do not occur in
this program or its summary.

Two used fixed rules create a real adequacy limitation:

- `semantics/str.k` converts a literal only while each character code is below
  128;
- `semantics/methods.k` defines case using only ASCII ranges 65–90 and 97–122.

Concrete witness:

```text
CPython/submitted program: {"é": 1} -> True
fixed manual U+00E9 method: str(iCons(233,...)).islower -> False
fixed proved summary for that singleton key -> False
fixed LLVM execution of translated Unicode literal -> exit 113
```

The two manual fixed-model claims close with `#Top`. The Python results also
show that `"É"` and `"ß"` are cased in CPython while the supplied model cannot
faithfully execute those literals. This is model-versus-CPython divergence;
the submitted program is not the source of it.

Evidence:

- `evidence/stage5_unicode_model_witness.py`
- `evidence/stage5_unicode_model_witness.sh`
- `evidence/stage5_unicode_model_spec.k`
- `evidence/stage5_unicode_model_witness_v2.log`

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation copied
the complete target claim, retained the actual loaded program and its
precondition, and changed only the result obligation from
`checkCaseSummary(...)` to its Boolean negation.

`kprove --dry-run` exited zero, proving the mutation parsed and built against
the fresh definition. The live proof then exited 1 with
`WarnStuckClaimState`, not a parser error, crash, or timeout. Its residual gives
the satisfying empty-input branch:

```text
result |-> false
hasAnyKey(KS) = false
hasRefVS(KS) = false
```

The mutated destination requires the negated summary, which is true for that
empty `KS`; the implication therefore fails for the expected unmet result
obligation. This demonstrates that the original theorem discriminates the
return value.

Evidence:

- `evidence/stage6_nonvacuity_mutation.k`
- `evidence/stage6_nonvacuity.log`

## 7. Proven versus assumed accounting

### What the proof establishes

Conditioned on the supplied MPY semantics and K's reachability logic, for every
finite `KS:ValSeq` with no heap-reference key and arbitrary `VALUES:ValSeq`,
execution of the exact trusted-regenerated function body from the initial MPY
configuration has this partial-correctness postcondition:

```text
result =
  nonempty(KS)
  and
  (fold every key through the fixed model's islower predicate
   or
   fold every key through the fixed model's isupper predicate)
```

Non-string keys contribute false. The theorem is unbounded in dictionary and
string length, constrains the terminal return binding, and also constrains
control, exception, stack, heap allocation, and loaded function identity. It
does not merely prove examples or a summary disconnected from execution.

### Trust ledger

| Boundary | Effect and dependents | Assessment and evidence |
|---|---|---|
| K parser, compiler, Haskell/LLVM backends, logical kernel | All builds and reachability results | Standard trusted verification infrastructure; fresh versioned reconstruction |
| Supplied read-only MPY semantics | Meaning of every program constructor and terminal cell | Campaign-authorized fixed model; recursively integrity-checked |
| Trusted `py2mpy.py` | Python AST to `.mpy` constructor bridge | Byte regeneration plus K-parser constructor identity; not itself a semantic proof |
| `SPEC.loop` used trusted in target composition | Summarizes the unbounded loop | Exact claim independently proved first with exit 0 and `#Top` |
| Local `isinstance` bridge | String/non-string branch value | Bridge-free universal exact-redex claim with arbitrary continuation; disjoint reference guard; fixed/extended differential |
| Local method twins | Lower/upper method values | Exact fixed formulas; two bridge-free universal claims; opposite interpretations rejected |
| `stringCodes` outside strings | Arbitrary `IntSeq`, potentially opaque | Does not affect any reachable result or control because every observation is string-guarded; on strings its value is fixed |
| Fixed ASCII string conversion/case model | Unicode literals and non-ASCII casing | Concerning supplied-model gap; concrete U+00E9 divergence and failed literal execution documented |
| Docstring interpretation and CPython bridge | Human-facing meaning of lower/upper string keys | Direct source reasoning plus 93,767-case independent differential; finite testing supports but does not replace the K theorem |
| Trusted canonical helper | Additional behavior witness only | Not a target; its third-key bug is exposed and does not undermine the docstring-faithful candidate |

Gate A (real-program soundness) passes. Gate C (reproducible evidence and
honest accounting) passes. The formal theorem covers the full unbounded,
source-valid domain of the fixed model without candidate-caused narrowing, but
the fixed model cannot faithfully represent CPython Unicode case behavior.
That is the documented supplied-model exception rather than a program or proof
unsoundness. It prevents `PASS`, while amendment v2 exception 1 preserves
legitimacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
