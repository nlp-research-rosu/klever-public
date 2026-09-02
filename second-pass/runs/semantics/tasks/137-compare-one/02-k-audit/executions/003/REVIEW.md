# Independent adversarial audit: 137-compare-one

The candidate is not a legitimate proof of the requested HumanEval contract. A
clean reconstruction does produce `#Top` for all nine target claims, and the
entry rule mechanically embeds the submitted `solution.mpy` body. The closure is
nevertheless obtained through two proof-local, result-bearing opaque symbols
that replace decimal parsing and float equality and then reappear in the
postcondition. There is no bridge-free connection theorem fixing either
symbol's value. Admissible opposite interpretations make the extended K theory
prove concrete results that the real submitted Python program does not return.
The submitted Python also materially diverges from the trusted canonical on
unrestricted integer/float inputs.

## 1. Input and provenance integrity

The launcher record is intact and does not present an audit-infrastructure
breach.

- `/audit-input.json` declares `record_layout =
  legacy-selected-stage1`, `semantics_mode = SUPPLIED_SEMANTICS`, problem
  `137-compare-one`, and condition `semantics`.
- `/audit-campaign-lock.json` is a real regular file. Its JSON object exactly
  equals the `audit_campaign` block in `/audit-input.json`; its independently
  recomputed SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
  `/audit-prompt.md` also matches the campaign's recorded prompt hash.
- Every mandatory `legacy-selected-stage1` record is present, regular, and
  readable: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. `usage.json` is present and was also
  checked. Historical `runtime-metrics.json` is not required for this layout.
- All recorded file hashes match. The retained candidate workspace manifest
  digest is
  `07bf5a2a17a104c5651ea0c562f259e2a36f85a0ca6fc593db4cd71f3faf1b35`;
  the independently recomputed digest matches both the invocation and result
  records. The trace contains one regular JSONL file with 221 valid records;
  its individual file hash and manifest-tree hash match the generation records.
  The complete 597,011-byte generation log was read. These generation records
  were treated only as provenance claims.
- The mode boundary is consistent: `/reference/reference-semantics` exists.
  Recursive type, path, and byte comparison found the candidate and trusted
  semantics trees identical (26 inventory entries, including the root and
  directory). There are no missing, additional, changed, mistyped, symlinked,
  or unsupported entries.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted mounts. No candidate-tree entry is a symlink or unsupported node.
  All required candidate proof artifacts are present as regular files.

Full commands, recomputed hashes, record types, trace event counts, and statuses
are in [01-integrity.log](evidence/01-integrity.log); the independent checker is
[check_integrity.py](evidence/check_integrity.py).

Stage result: integrity passed; audit continued.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From `/reference/prompt.py`, `compare_one(a, b)` accepts integers, floats, or
strings representing real numbers. A string may use `.` or `,` as its decimal
separator. It must return the original argument having the larger numeric value,
preserving that argument's type, or `None` when the numeric values are equal.
No magnitude or finite-size restriction is stated.

The trusted canonical normalizes commas and then calls `float` on both
operands before both equality and ordering
(`/reference/canonical.py:18-22`). The submission converts only strings and
compares non-string integers and floats directly
(`/candidate/solution.py:2-14`).

### Translation identity

I regenerated the program with the trusted command:

```text
python3 /reference/py2mpy.py /tmp/audit-work/137-compare-one/solution.py
```

The regenerated and submitted `solution.mpy` files are byte-identical, both
with SHA-256
`9f84dacfa99a22ea539c1e8b97d3e483a50265ec4243a70c68f0ccc08b35ab37`.
See [02-translation-identity.log](evidence/02-translation-identity.log).

### Independent differential execution

[differential.py](evidence/differential.py) independently imports the trusted
canonical and the scratch copy of the submission. It covers all four documented
examples, equality/less/greater boundaries for every type pairing, zero and
negative values, `2**53` precision boundaries, very large integers, decimal
comma/dot/exponent strings, infinities/NaN as extended cases, empty strings, and
invalid strings. It then takes a documented cross-product over the preserved
value list.

Results:

- 1,769 unique pairs executed;
- 1,094 pairs were classified in the stated integer/finite-float/numeric-string
  domain;
- all four documented examples agreed;
- 139 intended-domain pairs diverged;
- 24 extended or invalid pairs diverged.

A terminating intended-domain counterexample is:

```text
a = 9007199254740993
b = 9007199254740992.0
trusted canonical -> None
submitted solution -> 9007199254740993
```

The canonical converts `a` to the rounded float `9007199254740992.0`; the
submission performs Python's direct int/float comparison. Similar divergences
occur for two large integers because the canonical converts both to float. The
contract does not bound integers below the exact-float threshold, so this is a
material source-domain disagreement, independently sufficient to prevent a full
contract proof. Exact scope, an observation digest, bounded mismatch witnesses,
and exit status 1 are in
[02-differential.log](evidence/02-differential.log).

Stage result: translation fidelity passed, behavioral fidelity to the trusted
canonical failed on the unrestricted source domain.

## 3. Clean proof reconstruction

Only candidate source artifacts and the trusted translator/semantics were copied
to `/tmp/audit-work/137-compare-one`. Candidate compiled definitions,
`__pycache__`, `kore-exec.tar.gz`, and caches were not copied or reused.

The installed tools are K 7.1.293
([03-toolchain.log](evidence/03-toolchain.log)). Fresh reconstruction performed:

1. LLVM compilation of the trusted `MPY-KRUN` semantics, exit 0
   ([03-kompile-llvm.log](evidence/03-kompile-llvm.log)).
2. Concrete execution of the candidate's `concrete.mpy`, exit 0, final
   `<k> .K </k>`, `<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`
   ([03-krun-concrete.log](evidence/03-krun-concrete.log)).
3. Haskell compilation of `verification.k` as module `VERIFICATION`, exit 0
   ([03-kompile-haskell.log](evidence/03-kompile-haskell.log)).
4. One combined `kprove` invocation for `SPEC`, which printed exactly `#Top`
   and exited 0 ([03-kprove-all.log](evidence/03-kprove-all.log)).
5. Nine independent `kprove --claims` invocations for `int-int`, `int-float`,
   `int-str`, `float-int`, `float-float`, `float-str`, `str-int`,
   `str-float`, and `str-str`. Every command printed `#Top` and exited 0.
   [03-positive-summary.log](evidence/03-positive-summary.log) indexes the nine
   individual logs and the combined log.

Thus the candidate satisfies the mechanical positive-proof condition under its
extended theory. This does not validate that theory or the meaning of its
postcondition.

Stage result: clean reconstruction passed.

## 4. Adequacy and real-program pinning

### Entry claims

The nine claims in `/candidate/spec.k:6-130` have no `requires` clauses. Their
preconditions are exactly the Cartesian type pairs over K `Int`, K `Float`, and
`str(IntSeq)`, together with a fixed clean module/builtins configuration:
environment 0, empty module map, builtins at scope -1, empty heap and stack,
`noRet`, `NoExc`, and exit code 0. In particular, the string claims quantify
over every `IntSeq`; they do not restrict strings to valid real-number syntax.

Every claim says, in plain language:

> Running `runCompare(A, B)` from that clean state reaches
> `expectedCompare(A, B)` and restores all displayed cells.

There are no helper or loop claims.

One realizable witness for every precondition was executed against both Python
implementations:

| Claim | Witness | Both Python results |
|---|---|---|
| int-int | `(1, 2)` | `2` |
| int-float | `(1, 2.5)` | `2.5` |
| int-str | `(1, "2,3")` | `"2,3"` |
| float-int | `(2.5, 1)` | `2.5` |
| float-float | `(1.0, 1.0)` | `None` |
| float-str | `(3.0, "3,0")` | `None` |
| str-int | `("1", 1)` | `None` |
| str-float | `("2,5", 2.0)` | `"2,5"` |
| str-str | `("5,1", "6")` | `"6"` |

The complete outputs are in
[04-entry-witnesses-python.log](evidence/04-entry-witnesses-python.log).
Reviewer-authored assertions for the same nine witnesses were translated and
run through the fresh LLVM definition, again ending in `.K`, `NoExc`, exit 0
([04-ground-witnesses-translate.log](evidence/04-ground-witnesses-translate.log),
[04-ground-witnesses-krun.log](evidence/04-ground-witnesses-krun.log)).
These finite checks support only those ground cases.

### Program pinning

`runCompare` at `/candidate/verification.k:34-57` expands into normal
`closureVal`/`#applyK` machinery. A balanced-constructor parser extracted the
submitted `FuncDef` body and the executed closure body, normalized only the
translator's omitted empty statement identity to explicit `.Stmts`, and found
constructor identity (530 normalized characters on each side). See
[check_program_pinning.py](evidence/check_program_pinning.py) and
[04-program-pinning.log](evidence/04-program-pinning.log).

A body-sensitivity mutation changed the actually embedded final
`Return(Name("b"))` to `Return(Name("a"))`. The mutated definition compiled,
but the `int-int` target claim failed with `WarnStuckClaimState` and a residual
returning `A` on the `A < B` path
([verification-mutated-body.k](evidence/verification-mutated-body.k),
[04-body-mutation-kprove.log](evidence/04-body-mutation-kprove.log)).
This confirms the theorem depends on the embedded body rather than merely on an
external source filename.

The program term is therefore pinned. The result property is not: the
right-hand side is `expectedCompare`, whose equality and string-normalization
values reuse the same proof-local opaque symbols that replace execution. It is
not a free variable or syntactic tautology, but it is a circular,
interpretation-parametric summary rather than an independently connected
numeric result.

Stage result: real-program pinning passed; postcondition adequacy failed.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](evidence/inventory_k.py) lexically inventories every module,
import, configuration, context, syntax declaration, rule, and claim, including
multiline bodies and attributes. Counts were independently cross-checked with
`rg`:

- supplied semantics: 227 syntax declarations, 695 rules, 5 contexts, and 1
  configuration;
- proof-local `verification.k`: 7 syntax declarations and 12 rules;
- target `spec.k`: 9 claims;
- supplied attributes include 145 function declarations, 110 total
  declarations, 27 opaque/symbol declarations, 45 priority rules, 36 concrete
  rules, and 29 `owise` rules;
- proof-local attributes include 5 function declarations, 2 total opaque
  symbols, and 2 priority rules; there are no proof-local simplification rules.

Every sentence, exact source span, attributes, normalized hash, and text is in
[05-rule-inventory.json](evidence/05-rule-inventory.json). Every one of the 956
semantically relevant syntax/rule/context/configuration/claim sentences has an
explicit disposition in
[05-rule-assessment.json](evidence/05-rule-assessment.json).

Because this is `SUPPLIED_SEMANTICS` and the candidate tree is byte-identical to
the trusted tree, all 928 supplied declarations/rules/contexts/configuration
sentences are the immutable selected semantics level, not candidate proof
extensions. They were accepted as that fixed baseline. `MPY-CONCRETE` is used
only by the LLVM definition; the Haskell proof imports `MPY`, not
`MPY-CONCRETE`.

### Program-construct coverage under the fixed semantics

All material submitted constructs have declarations and operational routes:

- `Module`, `FuncDef`, `Params`, `Assign`, `If`, `Return`, `Call`,
  `Attribute`, `Compare`, `Name`, `Str`, and `NoneVal` are declared in
  `semantics/syntax.k`.
- Configuration, module statement sequencing, name lookup, builtins scope,
  left-to-right argument evaluation, and literals are in
  `semantics/core.k`.
- Local assignment and condition branching are in `semantics/controls.k`.
- Callee evaluation, builtin/type dispatch, closure frame allocation, and
  parameter binding are in `semantics/call.k`; return, frame pop, scope cleanup,
  and continuation restoration are in `semantics/functions.k`.
- `isinstance(..., str)` dispatch and sort tests are in
  `semantics/builtins.k`.
- Bound-method routing and the complete recursive single-character
  `replaceC` equations are in `semantics/call.k` and
  `semantics/methods.k`.
- Fixed float parsing is `applyBuiltin("float", str(CS), .Vals) =>
  decStrToF(CS)`; the recursive decimal helpers and concrete interpretation are
  in `semantics/float.k`.
- `Compare` evaluates left then right and dispatches through `applyCmp` in
  `semantics/operators.k`; integer comparisons are exact in `semantics/int.k`;
  float/mixed comparisons use the supplied opaque/concrete primitive boundary
  in `semantics/float.k`.

The fixed routes preserve the relevant binding, evaluation order, call/return
control, scope allocation/cleanup, and all displayed state cells. The proof
does not fail because a used source construct lacks a declaration.

### Proof-local extensions

#### `commaDecimal` and `#commaDecimal` (`verification.k:11-19`)

Classification: result-bearing opaque symbol plus operational bridge.

The priority-40 rule accepts the complete call expression
`float(E.replace(",", "."))` under an arbitrary continuation. It evaluates
`E`, but preempts normal lookup of `float`, bound-method construction,
argument evaluation, `replaceC`, type dispatch, decimal parsing, and their
exception behavior. The second rule turns a resulting `str(CS)` into the fresh
`commaDecimal(CS)`. No equation fixes that Float, and no bridge-free universal
claim proves

```text
commaDecimal(CS) =
decStrToF(replaceC(CS, 44, 46))
```

over the bridge's match domain. The symbol affects equality, ordering, the
returned original operand, and the postcondition. Reusing it in
`numericValue(str(CS))` (`verification.k:63`) is circular, not a value
connection.

False-conclusion witness on intended input: the valid numeric string `"1"` and
float `2.0`. The equation-free symbol admits the interpretation
`commaDecimal("1") = 3.0`. With mathematically correct ground facts
`3.0 != 2.0` and `3.0 > 2.0`, the bridge-enabled program returns `"1"`;
real submitted Python returns `2.0`. The diagnostic interpretation builds and
K proves the false ground result as `#Top`, exit 0:
[wrong-decimal-oracle.k](evidence/wrong-decimal-oracle.k),
[spec-wrong-decimal-oracle.k](evidence/spec-wrong-decimal-oracle.k),
[05-wrong-decimal-kompile.log](evidence/05-wrong-decimal-kompile.log), and
[05-wrong-decimal-kprove.log](evidence/05-wrong-decimal-kprove.log).
The actual Python result is preserved in
[05-wrong-oracle-python.log](evidence/05-wrong-oracle-python.log).

This also makes the unrestricted formal string claims false descriptions of the
real program: for example, `"abc"` satisfies the `str-int` sort precondition,
but real Python raises `ValueError` while the bridge fabricates a normal opaque
Float. Invalid strings are outside the natural-language domain, but they expose
the mismatch between the claims' actual precondition and real execution.

Disposition: unsound operational bridge and illegitimate result oracle.

#### `sameFloat` (`verification.k:24-28`)

Classification: result-bearing opaque symbol plus operational bridge.

The priority-40 rule replaces fixed Float equality at any admitted continuation
with `sameFloat(A, B)`. It preserves the framed cells and continuation, but it
has no equations and no bridge-free theorem relating it to the supplied
`A ==Float B` operation. `numericEqual(Float, Float)` then reuses the same
symbol (`verification.k:69`), so execution and postcondition agree under any
interpretation without proving numerical equality.

False-conclusion witness on intended input: `1.0` and `2.0`. The otherwise
unconstrained interpretation `sameFloat(_, _) = true` makes the function return
`None`. The diagnostic interpretation compiled and K proved
`runCompare(1.0, 2.0) => noneV` as `#Top`, exit 0
([wrong-float-oracle.k](evidence/wrong-float-oracle.k),
[spec-wrong-float-oracle.k](evidence/spec-wrong-float-oracle.k),
[05-wrong-float-kompile.log](evidence/05-wrong-float-kompile.log),
[05-wrong-float-kprove.log](evidence/05-wrong-float-kprove.log)).
The real submitted Python result is `2.0`.

Disposition: unsound result-bearing operational bridge.

#### `runCompare` (`verification.k:34-57`)

Classification: entry-term definition. It expands to the exact submitted body
and then uses the supplied closure/call machinery. It does not summarize the
body or bypass its control flow. Constructor identity and body sensitivity were
demonstrated in stage 4.

Disposition: sound and adequately pinned.

#### `numericValue`, `numericEqual`, and `expectedCompare`

- Integer and Float identity equations (`verification.k:61-62`) and integer
  equality (`:66`) are ordinary truthful definitions.
- Mixed equality (`:67-68`) is conditional on the selected semantics'
  `intToF`/`eqF` trusted primitives.
- The string equation (`:63`) and Float/Float equality (`:69`) merely propagate
  the rejected proof-local oracles.
- `expectedCompare` (`:74-81`) is a well-formed formal conditional, with no
  overlap or recursion issue, but it uses exactly the same result-bearing
  abstractions as execution. It therefore does not independently establish the
  human-facing numeric property.

The proof-local functions have no pairwise conflicting equations on the uses in
the claims. `numericValue` covers the three claimed sorts; `numericEqual` covers
the four Int/Float pairs after `numericValue`. The decisive defect is value
justification, not syntactic coverage or priority overlap.

Stage result: static soundness failed on both proof-local operational bridges.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation artifact. The fresh mutation
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) uses the satisfying
`int-int` input `(1, 2)` but changes the result obligation to the demonstrably
false `runCompare(1, 2) => 1`.

- Python confirms that the submitted result is `2`, not `1`
  ([06-vacuity-witness-python.log](evidence/06-vacuity-witness-python.log)).
- `kprove --dry-run` parsed and built the mutation successfully, exit 0
  ([06-vacuity-dry-run.log](evidence/06-vacuity-dry-run.log)).
- Actual `kprove` exited 1 with `WarnStuckClaimState`; the residual `<k>` cell
  contains `2 ~> .K`, which cannot unify with destination `1`
  ([06-vacuity-kprove.log](evidence/06-vacuity-kprove.log)).

This is meaningful non-vacuity evidence for the exact integer path and result
cell. It does not validate the float/string oracles, whose opposite
interpretations independently failed Gate A.

Stage result: fresh non-vacuity test passed as an expected rejection.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the supplied MPY theory plus the candidate's extensions, and conditional
on the interpretation of all opaque symbols, the exact submitted function body
started in the displayed clean state reaches `expectedCompare(A, B)` for each of
the nine K sort pairs and restores the displayed control/state cells. For
integer-only inputs, this structurally corresponds to exact K integer equality
and ordering. For Float and string paths, it establishes only consistency with
shared abstract atoms, not the intended numeric meaning of those atoms.

This is partial correctness under the extended theory. It is not a universal
theorem that Python decimal parsing or Float equality produces the values
claimed by the HumanEval contract.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| Trusted translator `/reference/py2mpy.py` | Source-to-constructor bridge | Acceptable trusted input; byte regeneration proves artifact identity, not translator correctness. |
| Byte-identical supplied MPY rules | Execution model for syntax, scopes, calls, state, and primitives | Accepted selected semantics boundary in `SUPPLIED_SEMANTICS` mode. |
| K integer/Boolean/map/list/string hooks | Low-level mathematics and storage | Ordinary trusted K runtime boundary. |
| Supplied `intToF`, `eqF`, `gtF`, `decStrToF`, and related Float primitives | External numeric operations used by mixed/Float comparisons | Explicit fixed-semantics opaque/concrete boundary. Acceptable only conditionally at the selected semantics level; finite LLVM tests do not prove universal Python equivalence. |
| Proof-local `commaDecimal` plus interception rules | Replaces program-used `replace` and `float` execution; affects branches, exceptions, and result | Illegitimate. Program-derived, equation-free, no universal connection theorem; opposite interpretation proves a false intended-domain result. |
| Proof-local `sameFloat` plus interception rule | Replaces program-used Float equality; affects equality branch and result | Illegitimate. Equation-free, no universal connection theorem; opposite interpretation proves a false intended-domain result. |
| `expectedCompare` | Purported contract postcondition | Formally defined but circular because it reuses both rejected execution oracles. |
| Constructor-level body comparison | Connects `runCompare` to submitted `solution.mpy` | Reproducible mechanical evidence; body-sensitivity mutation confirms dependency. |
| Python differential and LLVM ground tests | Finite evidence for implementation/semantics behavior | Reproducible empirical evidence only; it cannot replace the K connection theorems. It also finds a material canonical divergence. |

Gate A (real-program soundness) fails because two program-derived,
result-bearing operational bridges have no value connection and admit concrete
false conclusions. Gate B (intent adequacy) also fails because the postcondition
is circular and the submitted implementation diverges from the trusted
canonical on the unrestricted source domain. Gate C evidence is reproducible,
but reproducibility cannot cure Gates A or B.

Accordingly, the clean `#Top` is not a legitimate partial-correctness proof of
the real generated program against the HumanEval contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
