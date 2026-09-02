# Independent adversarial audit: 127-intersection

## Audit outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted translated function under the supplied MPY semantics.
The source reconstruction is clean, both positive claims close with fresh
definitions, the exact translated body is pinned into the called closure, and a
fresh false result mutation is rejected at the expected returned value.

The outcome is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the K
postcondition characterizes primality using Wilson's congruence and the
equivalence to the prompt's word “prime” is an external mathematical argument,
not a theorem proved inside K. The equivalence is standard and true for every
integer `N >= 2`, so this is not a soundness defect and does not permit a false
K conclusion. The independently checked source/canonical differential gives
finite supporting evidence only.

The command ledger is
[`evidence/COMMANDS.md`](/audit-output/evidence/COMMANDS.md), and hashes of all
preserved evidence are in
[`evidence/SHA256SUMS`](/audit-output/evidence/SHA256SUMS).

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mounts do not
contradict the mode and there is no infrastructure breach.

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the one JSONL structured trace only as candidate
claims. Their claims include `KPROVE_PASSED`, `VALIDATED`, two positive
`#Top` results, and expected mutation failures. None was used as proof
evidence. A complete structural summary of those records is preserved in
[`evidence/untrusted-claims.log`](/audit-output/evidence/untrusted-claims.log).

The independent provenance checker found:

- all required metadata, prompt, translator, solution, spec, and verification
  artifacts are regular files, not symlinks;
- candidate `prompt.py` is byte-identical to `/reference/prompt.py`
  (`aaebd5df...d5db1c`);
- candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`
  (`406485ea...db16`);
- the candidate and trusted semantics manifests each contain the same 25
  entries (including the directory entry), with identical path, type, and file
  bytes;
- no required artifact or semantics entry is missing, additional, changed,
  mistyped, or symlinked.

The full file/type/hash comparison and exit status are in
[`evidence/provenance.log`](/audit-output/evidence/provenance.log). Candidate
`runtime-kompiled`, `verification-kompiled`,
`verification-mutant-kompiled`, Python caches, archives, and candidate logs
were not copied into or used by the clean reconstruction.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two closed integer intervals `(A,B)` and `(C,D)`, each satisfying
`A <= B` and `C <= D`, let

```text
N = min(B,D) - max(A,C).
```

The prompt's examples establish that “length” is this geometric difference,
not the number of contained integer points. The required result is `"YES"` iff
the intersection length is prime; disjoint, touching, zero-length,
length-one, and composite-length intersections return `"NO"`.

### Submitted implementation

`solution.py` computes the maximum start and minimum end by two branches,
returns `"NO"` for `N < 2`, computes `(N-1)!` with a while loop, and applies
Wilson's congruence:

```text
(N-1)! mod N = N-1.
```

For integer `N >= 2`, Wilson's theorem makes this equivalent to primality. The
early return prevents modulo by zero or a negative divisor. The program uses
only two-element tuple indices `0` and `1`, integer arithmetic/comparison, a
while loop, and ASCII string results, all within the supplied subset.

### Translation identity

I regenerated `solution.mpy` from the scratch `solution.py` using the trusted
translator. The regenerated and submitted files are byte-identical and have
the same SHA-256:

```text
f8760cc52952bc8aabca43d3dcd5cc3d6ebf6c0c24fc3ba16960e8e143312981
```

The translator and `cmp` both exited `0`; see
[`evidence/translation.log`](/audit-output/evidence/translation.log) and the
preserved
[`evidence/regenerated-solution.mpy`](/audit-output/evidence/regenerated-solution.mpy).

### Independent differential

[`evidence/differential_test.py`](/audit-output/evidence/differential_test.py)
imports `/reference/canonical.py` and the scratch candidate as distinct
modules. It covers all three prompt examples; disjoint/touching/point
intervals; equality on each endpoint-selection boundary; lengths
`0,1,2,3,4,5,6`; containment and coincident intervals; negative endpoints;
large prime/composite lengths; every ordered pair of well-formed intervals
whose endpoints lie in `[-8,8]`; and 4,000 deterministic generated interval
pairs with endpoints in `[-200,200]`.

The run covered 27,430 cases with zero mismatches and exited `0`. Its complete
scope and special-case results are in
[`evidence/differential.log`](/audit-output/evidence/differential.log).
This is strong finite evidence, not a universal proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/127-intersection`. No candidate-compiled definition or cache
was reused. The toolchain was K v7.1.293 and Python 3.10.12
([`evidence/toolchain.log`](/audit-output/evidence/toolchain.log)).

### Concrete definition and execution

The supplied source semantics was freshly compiled with LLVM:

```bash
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

Compilation exited `0`
([`evidence/kompile-llvm.log`](/audit-output/evidence/kompile-llvm.log)).
The reviewer-generated concrete harness contains the exact submitted function
source followed by ten normal/boundary assertions. The trusted translator
produced
[`evidence/concrete-harness.mpy`](/audit-output/evidence/concrete-harness.mpy)
from
[`evidence/concrete-harness.py`](/audit-output/evidence/concrete-harness.py).

Fresh `krun` execution exited `0` with `<k> .K </k>`, `<exc> NoExc </exc>`,
and `<exit-code> 0 </exit-code`; see
[`evidence/krun-concrete.log`](/audit-output/evidence/krun-concrete.log).

### Proof definition and positive claims

The Haskell proof definition was freshly built from `verification.k`:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

It exited `0`
([`evidence/kompile-haskell.log`](/audit-output/evidence/kompile-haskell.log)).
The loop claim was then run separately:

```bash
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.factorial-loop
```

It exited `0` and printed `#Top`
([`evidence/kprove-factorial-loop.log`](/audit-output/evidence/kprove-factorial-loop.log)).
The complete target was also run, keeping the proved loop circularity
available to the entry claim:

```bash
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
```

It exited `0` and printed `#Top`
([`evidence/kprove-all.log`](/audit-output/evidence/kprove-all.log)). This
complete run proves both positive claims; selecting the entry claim while
removing its loop circularity would not be the submitted proof obligation.

Compiler warnings concerned unused variables in the supplied `strLt` rules and
non-exhaustive total functions in unrelated float/map/out-of-bounds domains.
They did not prevent a build and none of those warned terms is reachable on
this program's proof path. They are accounted for again in Stage 5.

## 4. Adequacy and real-program pinning

### Claim `SPEC.factorial-loop`

In plain language, its precondition says execution is at the exact submitted
while-loop head; the current local frame contains integer `length=N`,
`i=I`, and `factorial=F`; `1 <= I <= N`; and
`F = fact(I-1)`. Return and exception state are clear. Other named locals,
the parent, trailing computation, heap, allocation counter, stack, and exit
code are universally framed.

Its postcondition consumes the loop, changes `i` to `N`, changes `factorial`
to `fact(N-1)`, and preserves every other cell and continuation. This matches
the real loop: a true iteration maps `(I,F)` to
`(I+1,F*I)`, preserving the invariant, and a false guard plus `I <= N`
implies `I=N`. The loop body has no abrupt control or state effect beyond the
two local assignments.

A satisfying complete state is exhibited with `L=1`, `I=1`, `N=2`, `F=1`,
the seven listed locals, `scopeLoc=2`, empty heap/stack, `noRet`, `NoExc`, and
exit code `0`. The precondition and expected terminal values are recorded in
[`evidence/adequacy-witness.log`](/audit-output/evidence/adequacy-witness.log).

### Claim `SPEC.intersection`

Its precondition starts with an exact call to `intersection` on the two
concrete integer tuples `(A,B)` and `(C,D)`. The module scope binds that name
to `intersectionClosure`; the builtins scope, allocation state, heap, stack,
return, exception, and exit cells are exact; and the only logical input
restriction is `A <= B and C <= D`.

Its postcondition requires the returned `<k>` value to be exactly
`intersectionResult(overlapLength(A,B,C,D))`. This is equality to a
result-bearing function, not a free existential, tautology, implication, or
unconstrained oracle. All non-`<k>` entry cells are preserved.

The submitted `.mpy` file is a `Module(FuncDef(...))`, whereas the entry
claim starts in the exact post-load state and invokes the installed closure.
It therefore does not re-execute `#loadAll`/`FuncDef` inside the claim.
This is not a substituted-program gap: the fixed `FuncDef` rule installs
exactly `closureVal(params,body,0)`, and the reviewer independently compared
the trusted translation, submitted bytes, parameter list, complete normalized
body, and defining environment against `intersectionClosure`. Every character
matches; see
[`evidence/body-pinning.log`](/audit-output/evidence/body-pinning.log) and
[`evidence/body_pinning.py`](/audit-output/evidence/body_pinning.py). Once
called, ordinary MPY lookup, argument evaluation, parameter binding, body
execution, return, and frame pop all run; there is no proof-local call rewrite.

Concrete satisfying substitutions include:

- `(-3,-1),(-5,5)`: `N=2`, formal result `"YES"`, both Python results `"YES"`;
- `(1,2),(2,3)`: `N=0`, formal result `"NO"`, both Python results `"NO"`;
- `(0,4),(-1,5)`: `N=4`, formal result `"NO"`, both Python results `"NO"`.

The exact calculations are in
[`evidence/adequacy-witness.log`](/audit-output/evidence/adequacy-witness.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/rule-inventory.tsv`](/audit-output/evidence/rule-inventory.tsv)
enumerates every declaration and rule in the 24 supplied K source files,
`verification.k`, and `spec.k`, with source line, normalized full declaration,
attributes, category, and audit disposition. Its 947 items comprise:

- 233 syntax declarations, including 127 function declarations and 25
  `symbol/no-evaluators` opaque declarations;
- 116 declarations mentioning `total`, 0 mentioning `functional`;
- 706 ordinary rules, 0 simplification rules;
- 34 rule/declaration blocks mentioning priority, 48 concrete blocks, and 29
  `owise` blocks;
- five contexts, one configuration, and two reachability claims.

The item-level dispositions distinguish proof-local reviewed rules, supplied
rules exercised by the entry path, supplied syntax, and supplied rules whose
left-hand constructs cannot occur in this proof. Because this is
`SUPPLIED_SEMANTICS`, the byte-identical reference tree is the selected fixed
semantics. Unused reference rules are not silently treated as evidence about
full Python: they are accepted as the fixed language level and classified
inert for this theorem. There are no imported simplification rules that could
rewrite unrelated terms, and the unused rules/opaque symbols have distinct
left-hand constructors absent from the program, claims, and summaries.

The complete used-constructor-to-rule map is
[`evidence/used-construct-map.md`](/audit-output/evidence/used-construct-map.md).
It covers configuration/cells, evaluation order, lookup, tuple creation and
indexing, assignments, integer operators, branches, the loop, calls, returns,
scope allocation/removal, and ASCII result construction.

### Proof-local rules in `verification.k`

Every proof-local extension was inspected:

1. `fact`: `fact(N)=1` for `N<=0` and
   `fact(N)=N*fact(N-1)` for `N>0`. Guards are disjoint and exhaustive over
   integers; positive recursion strictly descends. All result-bearing uses have
   nonnegative arguments, so the negative totalization does not affect the
   theorem.
2. `overlapStart`: selects `C` iff `C>A`, otherwise `A`; this is exactly
   `max(A,C)`. Guards are disjoint/exhaustive and match the source branch.
3. `overlapEnd`: selects `D` iff `D<B`, otherwise `B`; this is exactly
   `min(B,D)`. Guards are disjoint/exhaustive and match the source branch.
4. `overlapLength`: subtracts those exact endpoint summaries. It replaces no
   execution and has one unconditional equation.
5. `intersectionResult`: returns `"YES"` exactly for `N>=2` satisfying
   Wilson's congruence, and `"NO"` for `N<2` or for the complementary
   `N>=2` case. The three guards are pairwise disjoint and exhaustive.
   `pyMod` is used only with divisor `N>=2`.
6. `intersectionClosure`: a nullary definitional AST abbreviation. Its sole
   equation is the exact trusted translation's parameters, complete body, and
   defining environment. It does not intercept a call or skip body execution.

There are no proof-local priorities, simplification rules, concrete rules,
opaque symbols, or operational bridges. In particular, no rule rewrites
`Call`, `While`, `Return`, or another fixed-semantics program term to a summary.
The loop claim is a derived reachability circularity over the exact real loop,
not an ordinary operational rule.

### Fixed-semantics path

The relevant supplied rules implement:

- left-to-right callee/argument, binary-operand, comparison, tuple-element, and
  subscript evaluation;
- lookup of the exact module closure followed by parameter binding into a fresh
  local scope;
- tuple indices `0` and `1`, both in bounds;
- integer `+`, `-`, `*`, comparisons, and Python-style modulo;
- branch selection from exact Boolean comparisons;
- guard re-evaluation, sequential loop-body assignments, and loop
  continuation;
- abrupt `Return`, frame pop, caller restoration, and local-scope removal.

The call temporarily changes environment, scope map, scope counter, stack, and
return state, then `#pop` restores them. The program performs no heap
allocation, output, exception, or exit-code mutation. The claim's framed cells
therefore match the full observable footprint.

All 34 supplied priority cases were checked against the path. They concern
heap references/cells, list/dict/sort operations, float/math interception,
assert dereferencing, or other absent constructors and cannot preempt a used
rule. All 25 opaque symbols belong to float, sort, or MD5 domains and influence
no branch, state, or result here.

LLVM warned that several unrelated `[total]` functions do not cover values
such as `cellsMark`, and that `valSeqAt` is underdefined out of bounds. This is
a narrow coverage limitation, not an asserted false equation. The entry uses
only integer tuples and indices `0,1` into length-two tuples, and none of the
warned float/map functions is reachable. I therefore do not label any such
rule unsound. No unsoundness is claimed in this audit, so no false-rule witness
is required.

## 6. Fresh non-vacuity test

I inspected but did not rely on the candidate's `spec-vacuity.k`. The fresh
reviewer mutation is
[`evidence/reviewer-vacuity.k`](/audit-output/evidence/reviewer-vacuity.k).
It uses the satisfying input `(-3,-1),(-5,5)`, whose overlap length is `2`,
and changes the result obligation from true `"YES"` to false `"NO"`.

The dry run:

```bash
kprove reviewer-vacuity.k --definition fresh-verification-kompiled \
  --spec-module REVIEWER-VACUITY --dry-run
```

exited `0`, establishing successful parse/build
([`evidence/vacuity-dry-run.log`](/audit-output/evidence/vacuity-dry-run.log)).
The actual proof command exited `1` with `WarnStuckClaimState`. Its residual
has the fully executed value
`str(iCons(89,iCons(69,iCons(83,.IntSeq))))` (`"YES"`) while the destination
requires the `"NO"` code sequence. The backend then reports that the
configuration cannot be rewritten further. This is the intended unmet result
obligation, not a parser error, missing import, timeout, unrelated crash, or
unreachable mutation; see
[`evidence/vacuity-proof.log`](/audit-output/evidence/vacuity-proof.log).

## 7. Proven versus assumed accounting

### Precisely proven

Under the supplied MPY semantics and the equations in `verification.k`, the
successful reachability proof establishes:

1. for every loop state satisfying `1<=I<=N` and
   `F=fact(I-1)`, the exact submitted while loop reaches its continuation with
   `i=N` and `factorial=fact(N-1)`, preserving all other cells; and
2. for all mathematical integers `A,B,C,D` satisfying
   `A<=B` and `C<=D`, calling the exact submitted closure on the two
   two-element tuples reaches exactly
   `intersectionResult(min(B,D)-max(A,C))`, with the entry state restored.

Expanding `intersectionResult`, the proved output is `"YES"` exactly when
`N>=2` and `(N-1)! mod N=N-1`, and `"NO"` otherwise. This is a
partial-correctness result under the Kit convention; it is not reported as a
separate liveness/termination theorem.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell prover, LLVM runtime, and built-in integer/Boolean/map theories | All machine results | Foundational tool trust; acceptable and versioned in evidence. |
| Byte-identical supplied MPY semantics | All operational execution | Required trusted semantics level. Every used rule was statically reviewed; unused incomplete Python domains are excluded from the theorem. |
| Trusted `/reference/py2mpy.py` | Source-to-MPY bridge | Required trusted input. Regeneration is byte-identical, so no candidate translator decision is trusted. |
| Exact post-load closure initialization | Real-program pinning | The entry claim does not execute module load, but the fixed `FuncDef` rule and exact syntactic body/parameter/environment comparison establish the same closure state. Acceptable; no behavior is summarized or skipped after invocation. |
| `fact`, endpoint, length, and result equations | Loop invariant and final value | Proof-local, exhaustive, non-overlapping, terminating where recursive, and reviewed above. No opacity. |
| Wilson's theorem for integers `N>=2` | Bridge from formal congruence to natural-language “prime” | True standard mathematics, but not machine-checked in this K development. This is the documented concern that prevents a `PASS` verdict. |
| Trusted canonical implementation plus 27,430 differential cases | Finite implementation/intent support | Reproducible empirical evidence only; it does not replace either K proof or Wilson's universal theorem. |
| 25 supplied opaque float/sort/MD5 symbols | None | Unused by syntax, control, state, summaries, and postcondition; acceptable inert boundary for this theorem. |
| Termination | Not part of the reported theorem | Excluded by the requested partial-correctness interpretation. |

Gate A (real-program soundness) passes: the exact body executes under fixed
semantics, state/control are preserved, summaries are defined rather than
opaque, the result is constrained, and the false mutation is rejected. Gate B
is extensionally adequate to the prompt conditional on the standard Wilson
theorem; the theorem's external status is the documented limitation. Gate C
passes for auditability: commands, inputs, finite evidence, source inventory,
exit statuses, and residuals are preserved. Candidate prose, traces, and prior
compiled artifacts were never substituted for these checks.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
