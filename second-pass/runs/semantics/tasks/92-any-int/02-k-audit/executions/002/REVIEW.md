# Independent adversarial review: 92-any-int

## Conclusion

The candidate contains a legitimate, result-constraining K reachability proof for
the submitted function over the material HumanEval contract domain: unbounded K
integers and modeled non-integer numeric values. I rebuilt both backends from
source, proved the four target claims together and separately, mechanically
pinned the proof body to the trusted regeneration of `solution.mpy`, audited all
three proof-local rules, and obtained the expected stuck residual from fresh
postcondition and body mutations.

The verdict is `CONCERNS / LEGIT`, rather than an unqualified pass, because the
integrity-locked supplied semantics intentionally models `Bool` as not being an
`int`. CPython, the trusted canonical implementation, and the submitted Python
implementation all treat `bool` as an `int` subclass. Consequently,
`any_int(True, False, True)` is `true` in both Python implementations but
`false` in the supplied K model. Boolean truth values are not a material case of
the prompt's stated three-number integer/float domain, so this is not a material
HumanEval-domain narrowing and does not make the proof illegitimate. It is,
however, a concrete language-model boundary that must remain visible.

All commands below were run against fresh source copies in
`/tmp/audit-work/92-any-int`. Candidate-provided caches and compiled definitions
were neither copied nor reused. Exact commands, exit statuses, and bounded
outputs are in `evidence/`.

## 1. Input and provenance integrity

### Launcher record and campaign lock

`/audit-input.json` declares:

- problem `92-any-int`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance;
- a mounted trusted semantics tree.

The mounted `/reference/reference-semantics` is present, as required for this
mode. The campaign block in `/audit-input.json` is byte-for-byte equivalent as
parsed JSON to `/audit-campaign-lock.json`, and the lock's SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

The independent integrity script checked regular-file types, symlinks, recorded
hashes, and required layout records. It found no failure:
[script](evidence/verify_integrity.py) and
[log](evidence/01-integrity.log).

### Required generation records

I read and checked the hashes of:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- the structured JSONL trace.

The legacy-selected invocation has one trace file. Its SHA-256 is
`48fff8b7986a40f5ea578c99e8d9a6e0e988c42c178cb02543c9556b8b4830e3`,
matching `invocation.json`. All 175 JSONL records parse, their session id is
consistent, and their event-type counts agree with the retained transcript.
The bounded independent parse is in
[23-generation-trace-summary.log](evidence/23-generation-trace-summary.log).
The trace and prior `KPROVE_PASSED` report were treated only as untrusted
historical claims. Historical runtime metrics were not recorded for this legacy
layout and are not required.

### Mounted-source identity

The candidate's `prompt.py` and `py2mpy.py` exactly match their trusted mounted
versions. Their SHA-256 values are respectively:

- `1d19b808783c5f57c39df1de99cec4193d4b59538aa48ed22d6ca85c727a51e2`;
- `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The candidate and trusted `reference-semantics/` trees each contain the same 25
relative entries. Every entry has the same kind and, for files, the same content
hash. There are no missing, additional, mistyped, non-regular, or symlinked
entries. Thus the candidate did not modify the supplied semantics. This
integrity fact does not bless `verification.k`; its local rules are reviewed in
Stage 5.

All required candidate proof artifacts are regular files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`.
Source and launcher hashes are preserved in
[26-source-hashes.log](evidence/26-source-hashes.log). The live tools are K
7.1.293 and Python 3.10.12
([00-toolchain.log](evidence/00-toolchain.log)). There is no infrastructure
breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks for `any_int(x, y, z)`: return true exactly when all
three supplied numbers are integers and one is the sum of the other two;
otherwise return false. Its examples cover a true sum, a false integer triple,
a negative true sum, and a non-integer false case.

The trusted canonical implementation first tests all three arguments with
`isinstance(_, int)`, then tests:

```text
x + y == z  OR  x + z == y  OR  y + z == x
```

The submitted `solution.py` uses the same type gates and sum disjunction in one
short-circuit expression. It is a different surface layout but the same
algorithm and result.

### Trusted regeneration

Running the trusted translator on the scratch copy of `solution.py` exited zero,
and `cmp -s` found byte identity with the submitted `solution.mpy`:

- [translation log](evidence/02-regenerate-mpy.log);
- [byte-identity log](evidence/03-mpy-byte-identity.log).

Thus the submitted `.mpy` is the trusted translation of the submitted Python
source.

### Independent differential test

[differential.py](evidence/differential.py) imports the trusted canonical and
submitted generated entry points independently. It checks:

- all four documented examples;
- all three equality branches;
- zero and all-zero boundaries;
- negative and very large arbitrary-precision integers;
- non-integers in each argument position;
- Boolean edge cases;
- the full Cartesian product of 14 representative values, 2,744 calls;
- 5,000 additional deterministic generated triples.

All 7,762 calls had identical value and result type, with zero mismatches
([04-differential.log](evidence/04-differential.log)). There is no collection
input for which an “empty” case applies; `(0, 0, 0)` and `(0, 0, 1)` exercise
the numeric zero boundaries. Wrong arity is outside the three-argument contract.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/92-any-int`; the trusted
semantics was copied from `/reference`, not from a candidate-built definition.

### Concrete definition and execution

The fresh command was:

```bash
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0
([09-kompile-llvm.log](evidence/09-kompile-llvm.log)). The compiler reported
non-exhaustiveness warnings in unrelated general-purpose supplied functions
such as `mapStrVS`, `floorFI`, `joinCodes`, and `valSeqAt`. None can match a
construct in this program or a symbolic target claim.

[concrete_audit.py](evidence/concrete_audit.py) contains a function AST
identical to `solution.py` and 13 assertions covering the examples, every
integer branch, zero, negatives, a large integer, and each float short-circuit
position. Its trusted translation ran to `.K` with `NoExc`, exit code 0, and an
empty heap/stack
([10-krun-concrete-audit.log](evidence/10-krun-concrete-audit.log)).

### Proof definition and all positive claims

The fresh proof definition command was:

```bash
kompile verification.k --backend haskell \
  --main-module ANY-INT-VERIFICATION \
  --syntax-module ANY-INT-VERIFICATION \
  --output-definition verification-kompiled
```

It exited 0
([13-kompile-haskell.log](evidence/13-kompile-haskell.log)). The exact submitted
`spec.k` then proved as a whole with exit 0 and `#Top`
([14-kprove-all.log](evidence/14-kprove-all.log)).

To ensure that one closing claim did not hide another failed target, I made
mechanically split copies containing one unchanged claim each. Every independent
run exited 0 and printed `#Top`:

| Claim | Evidence |
|---|---|
| all three arguments are `Int` | [15-kprove-int.log](evidence/15-kprove-int.log) |
| first argument is non-`Int` | [16-kprove-nonint-x.log](evidence/16-kprove-nonint-x.log) |
| first is `Int`, second is non-`Int` | [17-kprove-nonint-y.log](evidence/17-kprove-nonint-y.log) |
| first two are `Int`, third is non-`Int` | [18-kprove-nonint-z.log](evidence/18-kprove-nonint-z.log) |

The split claim sources are preserved as `evidence/spec-int.k` and
`evidence/spec-nonint-{x,y,z}.k`.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

All claims begin from the clean module configuration: module environment 0,
empty module scope whose parent is the fixed builtins scope, fresh scope
location 1, empty heap, empty stack, no pending return or exception, and exit
code 0.

1. For arbitrary, unbounded K integers `X`, `Y`, and `Z`, executing the function
   reaches the Boolean `sumCondition(X,Y,Z)`.
2. For arbitrary K values where `X` is not an `isIntV`, execution reaches
   `false`, without needing to inspect `Y` or `Z`.
3. Where `X` is an integer but `Y` is not, execution reaches `false`.
4. Where `X` and `Y` are integers but `Z` is not, execution reaches `false`.

These four cases partition the modeled `Val × Val × Val` domain because
`isIntV` is true exactly on the K `Int` subsort. There is no finite size bound
or bounded unrolling.

### Mechanical program pinning

[check_program_pinning.py](evidence/check_program_pinning.py) parses the
submitted `.mpy` constructor tree and the proof's `anyIntBody` term. It checks:

- function name `any_int`;
- exact parameter constructor `Params("x","y","z")`;
- exact structural equality of the entire `Return(BoolOp(...))` body;
- exact construction of `closureVal(("x","y","z"), anyIntBody, 0)`.

All checks pass
([05-program-pinning.log](evidence/05-program-pinning.log)). The ordinary
supplied `FuncDef` rule would bind exactly that parameter/body/environment
triple as a closure in module scope 0. The proof harness starts the same closure
call directly. Omitting the module-load step and the unused global
`"any_int"` binding is semantically inert for this capture-free body: every
body name is either a parameter or is resolved through the unchanged builtins
parent. No material operation, argument evaluation, lookup, short circuit,
addition, comparison, call, return, or frame effect is skipped.

The body macro is hand-maintained rather than automatically regenerated. That
is an artifact-maintenance observation, not a failure for this immutable
candidate, because trusted regeneration and mechanical constructor comparison
pin the present artifacts.

### Result constraint and witnesses

The destination `<k>` cells contain a definite Boolean, not a free variable,
tautology, or one-way implication. All other observable cells are also fixed.

[claim_witnesses.py](evidence/claim_witnesses.py) exhibits satisfiable entry
states and compares each instantiated formal result with both Python
implementations:

- integer true: `(5,2,7)` gives `true`;
- integer false: `(3,2,2)` gives `false`;
- non-integer `x`: `(3.5,2,7)` gives `false`;
- non-integer `y`: `(5,2.5,7)` gives `false`;
- non-integer `z`: `(5,2,7.0)` gives `false`.

Every comparison agrees
([20-claim-witnesses.log](evidence/20-claim-witnesses.log)).

### Supplied-semantics Boolean boundary

There is one concrete cross-model disagreement:

```text
canonical.py: any_int(True, False, True) == True
solution.py:  any_int(True, False, True) == True
supplied K:   any_int(Bool(true), Bool(false), Bool(true)) == false
```

The Python observation is in
[12-python-bool-model-boundary.log](evidence/12-python-bool-model-boundary.log).
The fresh LLVM run of the exact function body under the supplied semantics
successfully asserts the opposite K result in
[11-krun-bool-model-boundary.log](evidence/11-krun-bool-model-boundary.log).
The cause is the fixed
`isIntV(_:Int) => true` / `isIntV(_:Val) => false [owise]` definition in
`semantics/builtins.k`; K `Bool` is a distinct `Val`, whereas CPython `bool`
subclasses `int`.

This is a false-conclusion witness if one extends the intended domain to Python
truth values. The prompt, however, specifies three numbers and illustrates the
integer/non-integer distinction with integers and floats. Boolean truth values
are not a material source-contract numeric case. I therefore treat this as a
non-fatal supplied-language trust limitation, not a substituted program or a
material domain restriction.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[rule-inventory.tsv](evidence/rule-inventory.tsv), generated by
[inventory_k.py](evidence/inventory_k.py), inventories every `configuration`,
`syntax`, `context`, `rule`, and `claim` statement in all imported supplied K
files plus `verification.k` and `spec.k`. It records attributes including
`function`, `total`, `macro`, `owise`, `priority`, `concrete`,
`no-evaluators`, `symbol`, and strictness. There are:

- 695 supplied ordinary rules;
- 227 supplied syntax declarations;
- 5 supplied contexts and 1 configuration;
- 3 candidate-local rules and 3 candidate-local syntax declarations;
- 4 target claims;
- 938 inventoried statements total.

The inventory gives every row a disposition. The used-slice classification is
deliberately conservative for overloaded symbols such as `applyBin` and
`applyCmp`; rules whose operator, sort, or constructor guard cannot match the
executed term are still retained in that superset. No simplification rules or
`functional` declarations exist. The fixed tree contains 22 opaque
`no-evaluators` declarations, chiefly float/sort abstractions, but none reaches
this proof's branch, result, state, or postcondition.

### Candidate-local rules

| Extension | Class and decision |
|---|---|
| `anyIntBody` and its `[function,total]` declaration | A definitional syntax macro. Its only equation is terminating, exhaustive on the nullary symbol, non-overlapping, and constructor-identical to the submitted body. Accepted. |
| `#anyInt(X,Y,Z)` | An entry-harness constructor, not an operational bridge over a submitted program term. It creates the exact closure invocation. It preserves the active continuation through the ordinary call frame and does not directly read, write, omit, or fabricate any state cell. Accepted. |
| `sumCondition(X,Y,Z)` and its `[function,total]` declaration | A definitional mathematical summary used only in the postcondition. Its single equation is exactly the three integer sum equalities. It neither replaces execution nor introduces an opaque value. Accepted. |

There are no candidate-local priority, `owise`, simplification, concrete,
opaque, oracle, or answer-bypass rules. `sumCondition` is not used to rewrite
the program; ordinary execution independently computes the same expression.
Thus there is no circular program-derived abstraction and no connection theorem
obligation hidden behind a shared oracle.

### Used supplied-semantics path

Every submitted constructor maps to a declaration in
`semantics/syntax.k`. The material execution path is:

```text
#anyInt
  -> exact closureVal call
  -> fresh callee scope and call frame
  -> left-to-right parameter binding
  -> Return(BoolOp("and", ...))
  -> name lookup of parameters and fixed builtins
  -> left-to-right callee/argument evaluation
  -> applyBuiltin("isinstance", ...)
  -> isIntV
  -> short-circuit BoolOp
  -> integer BinOp("+") and Compare("==") when all gates pass
  -> Return / #pop
  -> definite Boolean in the original configuration
```

The relevant fixed rules are in:

- `semantics/core.k`: configuration, scope lookup, builtins scope,
  `#evalArgs`, literals, truthiness, and sequencing;
- `semantics/call.k`: callee evaluation, builtin dispatch, and closure-frame
  creation;
- `semantics/functions.k`: parameter binding, `Return`, and frame pop;
- `semantics/builtins.k`: `isinstance` and `isIntV`;
- `semantics/bool.k`: head-only evaluation and complementary short-circuit
  guards;
- `semantics/operators.k` and `semantics/int.k`: operand order, integer
  addition, and equality.

Binding is fixed by the clean scope: local parameters shadow nothing relevant,
the module scope is empty, and `isinstance`/`int` resolve to the known builtins
scope. Arguments are evaluated left-to-right. Each failed type gate prevents
all later gates and arithmetic as Python short-circuit evaluation requires.
Only the all-`Int` branch reaches arithmetic, so overloaded float, Boolean,
collection, sort, md5, loop, mutation, allocation, and exception rules cannot
match. Integer arithmetic is unbounded and the three equality cases have the
same grouping as the Python body.

The call rule allocates one fresh callee scope, saves the exact continuation and
caller environment, and pushes one frame. `Return` sets `retV`, and `#pop`
restores the caller environment, deletes the callee scope, resets `scopeLoc`,
clears the return state, and resumes the saved continuation. The body allocates
no heap object and performs no external state change. The entry claims correctly
require and recover empty stack/heap, `noRet`, and `NoExc`.

The supplied Boolean/CPython disagreement above is the only concrete false
cross-model conclusion found. It is attributable to the integrity-locked
language model, not to a candidate rule. No candidate-local rule admits a false
conclusion witness on the intended integer/float domain.

## 6. Fresh non-vacuity test

I did not rely on a candidate-provided vacuity artifact. The fresh
[spec-vacuity.k](evidence/spec-vacuity.k) changes the result-constraining
integer postcondition from `sumCondition(X,Y,Z)` to
`notBool sumCondition(X,Y,Z)`. It is demonstrably false at the satisfiable
entry state `(X,Y,Z)=(5,2,7)`.

The mutation compiled to KORE successfully with exit 0 under `--dry-run`
([21-vacuity-dry-run.log](evidence/21-vacuity-dry-run.log)). The real proof run
then exited 1 with `WarnStuckClaimState`, not a parser, import, or backend error.
Its reachable residual contains `true` and the branch condition
`Z #Equals X +Int Y`, exposing exactly the unmet negated result obligation
([22-vacuity-kprove.log](evidence/22-vacuity-kprove.log)).

I also performed independent body sensitivity. In
[verification-body-mut.k](evidence/verification-body-mut.k), the executed body
is materially changed to `Return(Bool(false))`; the postcondition remains the
sum condition in [spec-body-mut.k](evidence/spec-body-mut.k). The mutated
definition builds successfully
([24-kompile-body-mutation.log](evidence/24-kompile-body-mutation.log)), and its
proof exits 1 with an implication failure showing returned `false` against the
sum-equality disjunction
([25-kprove-body-mutation.log](evidence/25-kprove-body-mutation.log)). Therefore
the successful theorem depends on both the actual body and the intended result.

## 7. Proven versus assumed accounting

### What is formally established

Under the exact supplied K definition, from the clean configuration stated in
`spec.k`, execution of the constructor-identical `any_int` closure reaches:

- the disjunction of all three sum equalities for every unbounded K integer
  triple;
- `false` whenever the first non-`Int` argument occurs in any of the three
  positions.

The proof covers the complete modeled value partition and constrains all
observable configuration cells. It uses real lookup, argument evaluation,
short-circuit control, integer arithmetic/comparison, calls, returns, and
frame restoration. It is a partial-correctness reachability theorem under the
supplied operational semantics, not a theorem about arbitrary CPython runtime
contexts or rebindings.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Integrity-locked supplied MPY semantics | All claims | Required trust boundary for `SUPPLIED_SEMANTICS`. Its used integer/float path was reviewed. Boolean-as-integer behavior differs concretely from CPython and causes the stated concern. |
| K's `Int`, `Bool`, map/list, equality, and SMT/backend primitives | Arithmetic, guards, scopes, proof closure | Acceptable low-level K/toolchain trust. No proof-local axioms alter them. |
| Trusted `py2mpy.py` transliteration | Python-to-`.mpy` bridge | Acceptable: mounted hash identity plus byte-identical regeneration. |
| Reviewer constructor comparison | `.mpy`-to-proof-body bridge | Mechanical and complete for this single function; passes. Hand maintenance remains an observation. |
| Python differential testing | Canonical/generated implementation alignment | Finite empirical evidence only: 7,762 calls with zero mismatches. It does not substitute for K proof or universally prove Python/K semantic equivalence. |
| Clean initial module/builtins context | Name binding and result | Explicit theorem precondition and the intended HumanEval evaluation context. Arbitrary global rebinding is excluded. |
| Partial-correctness interpretation | The theorem statement | Termination outside modeled constructs and full CPython exception behavior are not separately proved. This straight-line modeled program does concretely terminate on all tested material cases. |

No candidate-defined opaque value, trusted primitive, empirical oracle,
operational shortcut, lemma, circularity, or simplification contributes to
claim closure.

### Gate and benchmark decision

- Gate A, real-program soundness under the supplied semantics: **PASS**.
  Positive reconstruction, exact body pinning, result mutation, and body
  mutation all behave correctly.
- Gate B, intent adequacy: **PASS with a documented non-material language-model
  limitation**. The unrestricted integer/float source-contract domain is
  covered; Boolean truth values expose the fixed semantics/CPython mismatch.
- Gate C, trust and evidence auditability: **PASS**. All sources, commands,
  witnesses, mutations, statuses, and residuals are preserved.

The benchmark mapping is therefore `CONCERNS / LEGIT`: the candidate is a
genuine proof of the real submitted body over the material contract domain,
with a concrete but non-fatal supplied-semantics limitation. It is not vacuous,
bounded, non-constraining, or based on unsound candidate proof rules.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
