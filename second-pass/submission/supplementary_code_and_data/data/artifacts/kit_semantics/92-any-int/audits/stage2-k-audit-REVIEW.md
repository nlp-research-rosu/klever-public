# Independent adversarial audit: 92-any-int

The reconstructed theorem is legitimate under the supplied MPY model and pins
the submitted program. The only material limitation is a documented
supplied-model representation gap: CPython numeric classes such as `complex`,
`Decimal`, `Fraction`, user-defined `int` subclasses, and third-party numeric
scalars are not all representable by the fixed translator/semantics. The
candidate introduces no additional restriction, and its Python implementation
agrees with the trusted canonical implementation on those values. Under
campaign amendment v2, that fixed-model boundary maps to `CONCERNS / LEGIT`.

I treated every candidate report, compiled directory, trace, and prior `#Top`
as untrusted. All executable evidence below was independently produced from
source in `/tmp/audit-work/92-any-int-audit`, using the trusted translator and
trusted supplied-semantics tree.

## 1. Input and provenance integrity

### Launcher and campaign records

`/audit-input.json` declares:

- problem `92-any-int`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- a mounted supplied-semantics baseline.

The required supplied tree is present at
`/reference/reference-semantics`. The campaign object in
`/audit-input.json` is exactly equal as parsed JSON to
`/audit-campaign-lock.json`, and the lock's independently computed SHA-256 is
the declared
`e71e1d695e6ffbbdc115800a2770522f00df366ef4b9637b1edf96107de40d0e`.

All required `pipeline-v3` records are regular, readable files:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- the JSONL trace beneath `/generation-evidence/codex-trace/`

Every launcher-recorded individual file hash matches. The one trace file has
SHA-256
`836b71a2968e3b7ff50847a09f54f467492c9c84786763ac08a711d0a15ee102`,
matching the generation result; all 379 JSONL records parse. Generation prose
claims success, but I did not use that claim as proof evidence.

The generation `run.json` names a generation-time Kit commit different from
the audit-campaign Kit commit. The prompt only requires the locked audit
campaign object to match `/audit-input.json`, which it does. The generation
record is untrusted historical metadata, not an input to the reconstructed
theorem, so this observation does not create an infrastructure or candidate
failure.

### Candidate and trusted-source integrity

Independent byte comparisons establish:

- `/candidate/prompt.py` equals `/reference/prompt.py`;
- `/candidate/py2mpy.py` equals `/reference/py2mpy.py`; and
- all 25 recursively inventoried entries under
  `/candidate/reference-semantics` equal the trusted tree in type, mode, path,
  and content.

No candidate entry is a symlink or special file. Every required candidate
deliverable is present as the expected regular file or directory. Candidate
kompiled directories were ignored.

Reproducible evidence:

- [integrity checker](/audit-output/evidence/01_integrity.py)
- [exact integrity commands](/audit-output/evidence/01_integrity.sh)
- [integrity output and statuses](/audit-output/evidence/01_integrity.log)

Stage 1 result: **PASS**. There is no audit-infrastructure breach and no
candidate provenance-integrity defect.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for `any_int(x, y, z)` over three numbers. It must
return true exactly when all three are integers and one equals the sum of the
other two; it returns false otherwise. The trusted canonical implementation
realizes “integer” as `isinstance(value, int)`, so CPython `bool` values are
accepted as integers and contribute `0` or `1`.

The candidate uses the equivalent short-circuit expression:

```python
isinstance(x, int)
and isinstance(y, int)
and isinstance(z, int)
and (x + y == z or x + z == y or y + z == x)
```

This preserves the canonical type-test order, arithmetic order, Boolean return
type, and short-circuit behavior. There is no canonical-versus-docstring
contradiction in this task.

### Trusted regeneration

Exact commands and results are in
[02_fidelity.log](/audit-output/evidence/02_fidelity.log). In particular:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
Exit: 0
cmp -s regenerated-solution.mpy /candidate/solution.mpy
Exit: 0
```

Both files have SHA-256
`f637e45fc0c6da706b0a5481b60953133849f72bc16bdd1f01c3c9e5d384c26c`.
Thus the submitted `solution.mpy` is exactly the trusted translation of the
submitted `solution.py`.

### Independent differential execution

The auditor-authored
[differential script](/audit-output/evidence/02_differential.py) imports the
trusted canonical and submitted entry points independently. It covers:

- all four prompt examples;
- zero, negative, large arbitrary-precision, and neighboring false cases;
- a case uniquely exercising each of the three equality branches;
- every small combination of Int, Bool, and float boundary values, including
  negative zero, infinities, and NaN;
- 5,000 deterministic integers up to 1,024 bits, with planted true cases in
  each equality position;
- `complex`, `Decimal`, `Fraction`, an `int` subclass, invalid values, and
  call-arity errors.

Result:

```text
SUMMARY total=8404 mismatches=0
Exit: 0
```

Exact commands are in
[02_fidelity.sh](/audit-output/evidence/02_fidelity.sh).

Stage 2 result: **PASS**. The submitted Python program is faithful to the
trusted canonical implementation over the tested intended domain, and no
material source divergence was found.

## 3. Clean proof reconstruction

### Fresh definitions

Only source artifacts were copied to scratch. The supplied semantics came from
`/reference/reference-semantics`, and translation used
`/reference/py2mpy.py`. The initial scratch check found no `*-kompiled`
directory. The following definitions were then built from source:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
Exit: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
Exit: 0
```

The LLVM build emits supplied-semantics warnings about partial pattern
coverage for `mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and
`valSeqAt`. None is reachable from this program; they are accounted for in
Stage 5. The Haskell build succeeds.

### Independent concrete execution

The auditor-authored K smoke program includes the prompt examples, zero,
negative, huge integer, all three equality branches, Bool-as-int boundaries,
and float rejection in every argument position. It succeeds under independent
Python execution, translates with the trusted translator, and terminates under
the fresh LLVM definition with:

```text
<k> .K </k>
<heap> .Map </heap>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

Artifact:
[03_concrete_audit.py](/audit-output/evidence/03_concrete_audit.py).

### Every positive target claim

Each label was selected in a separate `kprove` invocation against the fresh
Haskell definition:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.<label>
```

All 15 commands exit 0 and each per-label log contains exactly one `#Top`:

| Claim family | Labels | Result |
|---|---|---|
| Int/Bool combinations | `int-int-int`, `int-int-bool`, `int-bool-int`, `int-bool-bool`, `bool-int-int`, `bool-int-bool`, `bool-bool-int`, `bool-bool-bool` | 8/8 `#Top`, exit 0 |
| Earliest float at position 1 | `float-any-any` | `#Top`, exit 0 |
| Earliest float at position 2 | `int-float-any`, `bool-float-any` | 2/2 `#Top`, exit 0 |
| Float at position 3 | `int-int-float`, `int-bool-float`, `bool-int-float`, `bool-bool-float` | 4/4 `#Top`, exit 0 |

The summary is:

```text
POSITIVE_CLAIM_SUMMARY: total=15 failures=0
```

Reproducible evidence:

- [reconstruction commands](/audit-output/evidence/03_reconstruct.sh)
- [combined reconstruction log](/audit-output/evidence/03_reconstruct.log)
- [LLVM build log](/audit-output/evidence/03_kompile_llvm.log)
- [Haskell build log](/audit-output/evidence/03_kompile_haskell.log)
- [concrete K output](/audit-output/evidence/03_krun.log)
- per-label `03_kprove_*.log` files in `/audit-output/evidence/`

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Plain-language claims

All claims share the following initial-state precondition: environment location
0; module scope 0 containing only the exact `any_int` closure and parent
builtins scope -1; next scope location 1; empty heap and stack; heap location
0; `noRet`; `NoExc`; and exit code 0. There is no `requires` clause beyond the
K sorts shown below.

Let `ι(False)=0`, `ι(True)=1`, and let `S(a,b,c)` mean
`a+b=c or a+c=b or b+c=a`.

| Claim | Input domain | Required returned value | Ground witness |
|---|---|---|---|
| `int-int-int` | `Int × Int × Int` | exactly `S(x,y,z)` | `(5,2,7) → true` |
| `int-int-bool` | `Int × Int × Bool` | exactly `S(x,y,ι(z))` | `(1,0,True) → true` |
| `int-bool-int` | `Int × Bool × Int` | exactly `S(x,ι(y),z)` | `(1,True,2) → true` |
| `int-bool-bool` | `Int × Bool × Bool` | exactly `S(x,ι(y),ι(z))` | `(1,False,True) → true` |
| `bool-int-int` | `Bool × Int × Int` | exactly `S(ι(x),y,z)` | `(True,1,2) → true` |
| `bool-int-bool` | `Bool × Int × Bool` | exactly `S(ι(x),y,ι(z))` | `(True,0,True) → true` |
| `bool-bool-int` | `Bool × Bool × Int` | exactly `S(ι(x),ι(y),z)` | `(True,True,2) → true` |
| `bool-bool-bool` | `Bool × Bool × Bool` | exactly `S(ι(x),ι(y),ι(z))` | `(False,False,False) → true` |
| `float-any-any` | `Float × Val × Val` | exactly false | `(1.0,1,2) → false` |
| `int-float-any` | `Int × Float × Val` | exactly false | `(1,1.0,2) → false` |
| `bool-float-any` | `Bool × Float × Val` | exactly false | `(True,1.0,2) → false` |
| `int-int-float` | `Int × Int × Float` | exactly false | `(1,2,3.0) → false` |
| `int-bool-float` | `Int × Bool × Float` | exactly false | `(1,True,2.0) → false` |
| `bool-int-float` | `Bool × Int × Float` | exactly false | `(True,1,2.0) → false` |
| `bool-bool-float` | `Bool × Bool × Float` | exactly false | `(True,True,2.0) → false` |

The existential `?R:Bool` in the first eight claims is not free: the `ensures`
equality fixes it to the complete contract predicate. The remaining seven
claims use literal `false`. Each ground witness agrees with the trusted
canonical and submitted Python functions; see
[04_witnesses.py](/audit-output/evidence/04_witnesses.py) and
[04_pinning.log](/audit-output/evidence/04_pinning.log).

### Mechanical source-to-claim identity

Using the freshly compiled syntax, I expanded:

1. the regenerated `solution.mpy` module;
2. the `anyIntModuleScope` macro; and
3. an `AnyIntCall(...)` macro invocation

to JSON KAST. An independent structural checker found exactly one submitted
`FuncDef`, one installed closure, one map entry, and one call. It established:

- submitted function name, scope key, and expanded call name are all
  `"any_int"`;
- parameter constructor trees are identical;
- body constructor trees are identical;
- closure location is 0 and its parent is builtins scope -1.

The matching constructor hashes are:

```text
parameters: 4bb0e3bb6fdfc7eff686a7b672ae67a08ad257b88f4c28c789893b6bd7e8771e
body:       2d853f7796d8b04201cd69da268e238eed6d5061a88701f68cdb90914748ccad
```

Evidence:
[04_compare_terms.py](/audit-output/evidence/04_compare_terms.py).

Thus the claim does not merely refer to an external `solution.py`; it installs
and executes the same translated binding and body.

### Body sensitivity

The auditor-authored mutation changes the third disjunct in the installed
closure from `y + z == x` to `y + z == z`. It therefore changes the program
term actually executed by the claim. The mutation builds successfully.
For `(13,4,9)`, where only the original third disjunct is true, `kprove` exits
1 with `WarnStuckClaimState` and residual:

```text
<k> false ~> .K </k>
```

Evidence:

- [mutated definition](/audit-output/evidence/04_verification_body_mutant.k)
- [mutation witness claim](/audit-output/evidence/04_spec_body_mutant.k)
- [mutation proof log](/audit-output/evidence/04_body_mutant_kprove.log)

Stage 4 result: **PASS**. The theorem is result-constraining and pins the real
submitted program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The mechanical inventory covers the trusted supplied semantics, every helper
module, candidate `verification.k`, and `spec.k`:

- 26 source files;
- 244 syntax declarations;
- 738 rules;
- 15 reachability claims;
- 1 configuration and 5 context declarations;
- 160 function declarations, including 114 `total` declarations;
- 0 `functional` declarations/rules;
- 24 proof-opaque `symbol(...), no-evaluators` declarations;
- 43 priority rules;
- 433 ordinary equational rules;
- 54 concrete-only equations; and
- 1 simplification rule.

The complete source-located listing is
[05_rule_inventory.md](/audit-output/evidence/05_rule_inventory.md). Every
syntax declaration, rule, claim, configuration, and context also receives an
explicit disposition in
[05_rule_assessment.md](/audit-output/evidence/05_rule_assessment.md). No rule
is categorized as unsound.

### Used syntax and fixed execution path

`solution.mpy` uses `Module`, `FuncDef`, `Params`, `Return`, `BoolOp`, `Call`,
`Name`, `BinOp("+",...)`, `Compare`, and `CmpOp("==",...)`, with Int, Bool, and
Float values supplied at the entry. Their execution is covered as follows:

- `core.k`: values and configuration; ordinary scope lookup; builtins scope;
  left-to-right argument accumulation; `boolAsInt`.
- `call.k`: callee lookup before left-to-right arguments; dispatch by the
  selected `closureVal` or `builtinV`; creation of the callee frame.
- `functions.k`: positional binding, `Return`, default return continuation,
  frame pop, environment/scope restoration.
- `operators.k`: strict binary-operand evaluation and comparison contexts.
- `bool.k`: head-only, value-returning short-circuit for `and`/`or`, plus
  Bool-to-int comparison promotion.
- `int.k`: exact unbounded integer addition, Bool promotion, and equality.
- `builtins.k`: ordinary `isinstance(V, int)` dispatch; `isIntV(Int)` and
  `isIntV(Bool)` are true, with the `owise` non-int case false.
- `float.k`: Float is a `Val`; no float arithmetic, comparison, or truthiness
  operation is reached because `isinstance(Float,int)` returns false first.

The initial map contains no `"$cells"` marker, so the higher-priority
cell-lookup/binding rules are guard-disjoint. Inputs are direct values rather
than heap references, so heap-dereference priority rules are disjoint. Special
call interceptors match `Attribute(...)` forms or other builtin names, not
`Name("any_int")` or `Name("isinstance")`. User-closure and builtin dispatch
are constructor-disjoint. These priority/overlap facts prevent a hidden
execution bypass.

Calls temporarily allocate a scope and push a continuation frame; parameter
bindings live in that scope. `Return` sets `retV`, `#pop` restores the caller
environment, removes the callee scope, restores `scopeLoc`, consumes the stack
frame, and clears the return state. This program performs no heap allocation or
mutation. The claims constrain every observable cell after execution.

### Candidate-local extensions

| Extension | Classification | Static decision |
|---|---|---|
| `AnyIntCall` macro | Exact syntax abbreviation | Accept. Expands to ordinary lookup-based `Call(Name("any_int"),...)`; no runtime rule remains. |
| `anyIntModuleScope` macro | Exact program-binding abbreviation | Accept. KAST comparison proves the installed parameters/body equal trusted regeneration. |
| `boolAsInt(B) => #if B #then 1 #else 0 #fi [simplification]` | Derived lemma | Accept. `Bool` has two constructors; results agree with fixed `true→1` and `false→0` equations on both overlaps. |
| `anySum(X,Y,Z)` equation | Definitional summary | Accept. One terminating unguarded equation covers all `Int³`; it is exactly the contract disjunction and never replaces execution. |

There is no operational bridge, oracle, fresh result-bearing abstraction,
program summary, circularity, auxiliary claim, proof-local opaque symbol, or
candidate priority rule.

### Supplied-model warnings and opaque symbols

The six compiler-highlighted partial/totalized helpers (`mapStrVS`, `floorFI`,
`toF`, `ceilF`, `joinCodes`, and `valSeqAt`) are in the fixed supplied
semantics and are not reachable from any used constructor or postcondition.
Their model limitations cannot enable a false conclusion for any satisfying
entry state of this theorem.

Likewise, all 24 proof-opaque symbols—including float-operation summaries,
`sortVS`, `sortKeyVS`, and `md5hexCodes`—are unreferenced by the program,
claims, or candidate equations. `MPY-CONCRETE` is imported by the independent
LLVM runtime module but not by the Haskell proof module (`VERIFICATION`
imports `MPY`, not `MPY-CONCRETE`).

Some supplied rules deliberately model only a Python subset—for example,
unsupported imports may be no-ops and out-of-bounds indexing is not modeled as
a CPython exception. No such construct occurs here. I therefore do not label
these fixed, unreachable model choices “unsound” for this theorem; there is no
satisfying intended input from which they can enable a false `any_int`
conclusion.

Stage 5 result: **PASS** for real-program soundness. The only material
adequacy boundary is the separately documented value-representation gap,
handled in Stage 7.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation changes
the result obligation for the satisfying input `(5,2,7)` from true to false.
Both trusted canonical and submitted Python return `True`.

The mutated K spec is
[06_false_result_spec.k](/audit-output/evidence/06_false_result_spec.k).
It first builds successfully:

```text
kprove 06_false_result_spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT-SPEC --dry-run
Exit: 0
```

The actual proof then fails for the intended reason:

```text
kprove 06_false_result_spec.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT-SPEC
Exit: 1
WarnStuckClaimState
<k> true ~> .K </k>
```

This is an unmet result obligation, not a parse failure, missing import,
timeout, unreachable mutation, or unrelated backend error.

Evidence:

- [commands and combined log](/audit-output/evidence/06_nonvacuity.log)
- [dry-run log](/audit-output/evidence/06_false_result_dry_run.log)
- [failed proof log](/audit-output/evidence/06_false_result_kprove.log)
- [Python witness](/audit-output/evidence/06_false_witness.py)

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the K proof establishes

Conditional on the supplied MPY semantics and K's logic/backends, the
machine-checked reachability claims establish this partial-correctness theorem:

1. For every unbounded K `Int` and both K `Bool` values in every three-input
   combination, the actual submitted `any_int` closure terminates at a Boolean
   equal to the exact three-equality sum predicate, interpreting Bool as 0/1.
2. For every K `Float`, including all Float values represented by that sort,
   in any argument position, the closure returns false before float arithmetic
   is evaluated.
3. All 27 combinations of the supplied model's three numeric sorts are
   covered by the 15 symbolic claims, with no bound on integer value or size.
4. The final environment, scopes, allocators, heap, stack, return state,
   exception state, and exit code equal the specified initial state.

This is not a separate total-correctness theorem. The function is loop-free
and all reconstructed executions close, but the formal artifact is a
reachability/partial-correctness proof.

### Trust ledger

| Boundary | Effect and dependents | Evidence and decision |
|---|---|---|
| K kernel, parser/compiler, Haskell prover, LLVM runtime, built-in Int/Bool/Map/List theories | All claims and executions | Required proof infrastructure. Fresh builds, 15 independent proofs, and a discriminating mutation support correct use. Accepted. |
| Trusted supplied MPY semantics | Lookup, binding, call order, `isinstance`, Bool control, integer arithmetic, return, and state restoration | Tree integrity is exact; all 738 rules and 244 syntax declarations are inventoried, with used rules statically reviewed. Accepted as the fixed operational model. |
| Trusted `py2mpy.py` | Python-AST-to-MPY syntax bridge and source identity | Candidate translator is byte-identical to trusted; trusted regeneration is byte-identical; KAST body hashes match. Accepted syntactic bridge. |
| Candidate `anySum` | Fixes the eight result postconditions | Fully defined by ordinary K integer/Boolean operations; no execution replacement. Formally acceptable. |
| Candidate symbolic `boolAsInt` simplification | Normalizes mixed-Bool postconditions | Exhaustive constructor reasoning and consistent overlaps with fixed equations. Formally acceptable. |
| Finite CPython/K differential evidence | Supports canonical fidelity and concrete model behavior | 8,404 Python comparisons, independent K boundary smoke execution, 15 ground witnesses. Empirical only; not substituted for the universal K proof. |
| Supplied-model representation gap | Numeric values outside Int/Bool/Float cannot enter the K theorem | Candidate `PROOF.md` explicitly lists `complex`, `Decimal`, `Fraction`, and third-party scalars as excluded fixed-model classes. Auditor witness `any_int(1+0j,1,2)` returns false in both canonical and submitted CPython, while the trusted translator fails explicitly with `Unsupported: Constant complex`. See [gap witness](/audit-output/evidence/05_complex_gap_witness.py) and [translator log](/audit-output/evidence/05_complex_gap_translator.log). This is model-vs-CPython representability, not program-vs-canonical behavior. Non-fatal concern under amendment v2. |

The representation gap originates in the fixed read-only model:
`py2mpy.py` has no complex constant constructor and the supplied `Val` algebra
has Int, Bool, Float, and nonnumeric/container/function values but no Complex,
Decimal, Fraction, numeric-tower subclass, or arbitrary external scalar
representation. The candidate did not add this restriction. It covers every
numeric sort the fixed model does represent, and the independent Python
evidence confirms that its submitted code follows canonical behavior on the
concrete gap witness.

### Final decision

Gates A, B-within-the-fixed-model, and C pass. There is no substituted
program, bounded unrolling, vacuity, non-constraining result, candidate-created
domain narrowing, or unsound proof rule. The supplied-model numeric-class
boundary prevents an unqualified `PASS` under the campaign amendment, but all
four conditions for its non-fatal exception are met. The appropriate mapping
is therefore `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
