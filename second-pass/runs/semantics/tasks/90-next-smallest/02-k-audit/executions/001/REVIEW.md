# Independent adversarial audit: 90-next-smallest

## Audit conclusion

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program, but the proof-to-intent bridge has documented
limitations. The cleanly rebuilt loop and entry claims both close with exit 0
and `#Top`; the entry claim loads a KORE-identical expansion of the submitted
`solution.mpy`; an exact, bridge-free theorem independently validates the
installed loop rule; and a fresh false result mutation builds and fails on the
expected unmet equality.

The concerns are:

1. the universal K claim ranges over the proof-only
   `list(intVals(INPUT))` representation, not the supplied semantics' native
   `.ValSeq`/`vCons` list representation. Its iterator rules are a sound
   nil/cons isomorphism for every operation this program uses, and concrete
   native-list execution plus Python differential testing agree, but the
   representation-to-Python-list bridge remains an informal structural
   argument rather than a successful universal K theorem;
2. the formal postcondition is `nsScan(INPUT,0,0,0)`. Its exhaustive equations
   plainly compute the second distinct minimum, but no separate K theorem
   equates it to `sorted(set(lst))[1]`; that last summary-to-natural-language
   step is ordinary mathematical review plus finite differential evidence;
3. all four required generation-provenance files and the structured trace are
   absent.

These are evidence and intent-bridge limitations. They do not enable a false
conclusion about the candidate's stated formal domain, so they warrant
`CONCERNS / LEGIT`, not `FAIL`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` tree is present, so the mounts do not
contradict the mode and there is no infrastructure breach.

I recursively compared `/candidate/reference-semantics` with the trusted tree
using `diff --no-dereference --recursive`, then independently inventoried entry
types, modes, sizes, link targets, and file hashes. There are no missing,
additional, changed, mistyped, or symlinked entries in the candidate semantics
tree. The prompt and translator also compare byte-for-byte with their trusted
versions. Exact commands and statuses are in:

- [candidate manifest](evidence/01-candidate-manifest.log) and
  [reference manifest](evidence/02-reference-manifest.log);
- [prompt comparison](evidence/04-prompt-integrity.log) and
  [translator comparison](evidence/05-translator-integrity.log), both exit 0;
- [recursive semantics diff](evidence/06-semantics-tree-diff.log), exit 0;
- [typed semantics manifests and hashes](evidence/07-semantics-manifests.log),
  exit 0.

The following required provenance artifacts are missing:

- `/candidate/run-input.json`;
- `/candidate/metrics.json`;
- `/candidate/codex-last.txt`;
- `/candidate/codex-output.log`;
- any structured generation trace.

The exact presence check is
[03-required-provenance.log](evidence/03-required-provenance.log). Candidate
`__pycache__`, prior five-byte proof outputs, and all candidate prose/scripts
were ignored as proof authority. No candidate-built definition or cache was
copied into the scratch build.

The independently installed live toolchain is K v7.1.337. `kup` is absent, but
`kompile`, `krun`, and `kprove` all run; see
[08-toolchain.log](evidence/08-toolchain.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a finite list of integers, return the second **distinct** smallest integer.
Return `None` when fewer than two distinct integers occur. The trusted canonical
implementation expresses this as `sorted(set(lst))[1]` when the deduplicated
list has length at least two.

The submitted implementation maintains:

- `count = 0` before any value has been seen;
- `count = 1` with `smallest` equal to the only known distinct minimum;
- `count = 2` with `smallest` and `second` equal to the two least distinct
  values seen so far.

Its branches correctly initialize the minimum, shift the old minimum when a
new minimum arrives, ignore duplicate minima, and lower the second minimum when
an intermediate distinct value arrives. The final `count == 2` test returns
`second`, otherwise `None`.

### Trusted translation

I regenerated the scratch `solution.mpy` from `solution.py` with the trusted
`/reference/py2mpy.py`. `cmp --verbose` exits 0, and both files have SHA-256
`3565a16362b57637308ceb199fecae16d8def8cd4fbbfe991823a80691bec553`.
See [09-translate-solution.log](evidence/09-translate-solution.log),
[10-translation-byte-identity.log](evidence/10-translation-byte-identity.log),
and [11-translation-hashes.log](evidence/11-translation-hashes.log).

### Independent differential testing

[differential_test.py](evidence/differential_test.py) loads the trusted
canonical and candidate entry points directly from their independently copied
paths. It covers:

- all four documented examples;
- empty, singleton, all-equal, negative, zero, duplicate, and arbitrary-size
  integer cases;
- witnesses for every candidate branch boundary;
- every list of lengths 0 through 6 over `{-2,-1,0,1,2}` (19,531 inputs);
- 5,000 deterministic generated lists of lengths 0 through 100, including very
  large positive and negative integers.

The run reports `mismatches=0` and exits 0:
[12-python-differential.log](evidence/12-python-differential.log). This is
finite evidence for the implementation-to-canonical bridge, not a replacement
for the K proof.

## 3. Clean proof reconstruction

Only source artifacts were copied into `/tmp/audit-work/candidate`. Runtime and
proof definitions were rebuilt under distinct new output directories.

### Concrete definition

The supplied runtime was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled
```

It exits 0; see
[13-kompile-runtime.log](evidence/13-kompile-runtime.log). Fresh `krun` of the
translated concrete assertions exits 0 with final `.K`, `NoExc`, and exit code
0; see [14-krun-concrete-tests.log](evidence/14-krun-concrete-tests.log).

### Loop definition and claim

The base Haskell definition was freshly compiled with:

```text
kompile verification.k --backend haskell --main-module NEXT-SMALLEST-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

The build exits 0
([15-kompile-loop-definition.log](evidence/15-kompile-loop-definition.log)).
The positive loop proof command is:

```text
kprove spec.k --definition verification-kompiled --spec-module NEXT-SMALLEST-LOOP-SPEC
```

It exits 0 and prints `#Top`
([16-kprove-loop.log](evidence/16-kprove-loop.log)).

### Entry definition and claim

The entry definition was freshly compiled with:

```text
kompile verification.k --backend haskell --main-module NEXT-SMALLEST-WITH-LOOP-LEMMA --syntax-module MPY-SYNTAX --output-definition entry-verification-kompiled
```

The build exits 0
([17-kompile-entry-definition.log](evidence/17-kompile-entry-definition.log)).
The positive entry proof command is:

```text
kprove spec.k --definition entry-verification-kompiled --spec-module NEXT-SMALLEST-ENTRY-SPEC
```

It exits 0 and prints `#Top`
([18-kprove-entry.log](evidence/18-kprove-entry.log)). These are the only two
positive target claims in `spec.k`.

## 4. Adequacy and real-program pinning

### Loop claim

In plain language, the loop claim assumes:

- any finite remaining `INPUT:Ints`;
- arbitrary integer accumulator values `SMALLEST`, `SECOND`, and `COUNT`;
- environment 1 is a function scope containing exactly `value`, `lst`,
  `smallest`, `second`, and `count`, over a disjoint remainder map `SC`;
- scope location 2, a caller frame `frame(CONT,0,1)`, `noRet`, and arbitrary
  heap, heap location, exception, and exit-code cells.

The side condition is `1` not in `SC`. It executes the real loop body, the real
post-loop return sequence, and `#endcall`. The postcondition is the result
`nsScan(INPUT,SMALLEST,SECOND,COUNT)` followed by the saved `CONT`, with caller
environment/control restored and all unrelated observable cells preserved.
The candidate claim leaves the final scopes map existential; the installed
lemma fixes its exact deletion form. That exact state issue is independently
validated in Stage 5.

A concrete satisfying state takes
`INPUT = consInts(1,consInts(2,nilInts))`, all accumulator/old values 0,
`SC` equal to the ordinary caller/module scopes with no key 1,
`LST = list(intVals(INPUT))`, `CONT = .K`, empty heap and rest stack,
`NoExc`, and exit code 0.

### Entry claim

The entry precondition is the supplied initial configuration: environment 0,
module scope 0, builtins scope -1, scope location 1, empty heap/stack, `noRet`,
`NoExc`, and exit code 0. It has no additional guard and accepts every finite
`INPUT:Ints`. It loads `solutionModule` and calls `next_smallest` on
`list(intVals(INPUT))`.

The postcondition puts the exact term `nsScan(INPUT,0,0,0)` in `<k>` and
preserves every non-scope observable cell; final scopes are existential. The
result is neither free nor tautological: `nsScan` has complete, guarded,
structurally recursive equations.

For a direct pinning check, I parsed both submitted `solution.mpy` and the proof
term `solutionModule` with the freshly built entry definition, expanded macros,
and compared KORE. The files are byte-identical, with SHA-256
`2d8c5a66186efa3dd64a723fb87bff26e07e757553e91a384fe49577821b7ecd`;
see [19-kast-submitted-module.log](evidence/19-kast-submitted-module.log),
[20-kast-proof-module.log](evidence/20-kast-proof-module.log),
[21-kast-module-identity.log](evidence/21-kast-module-identity.log), and
[22-kast-module-hashes.log](evidence/22-kast-module-hashes.log).

[claim-witnesses.k](evidence/claim-witnesses.k) substitutes empty, singleton,
`[1,2]`, the documented permutation, and negative-duplicate inputs into
`nsScan`. The configuration-form claims exit 0 with `#Top`
([24-kprove-claim-witnesses-config.log](evidence/24-kprove-claim-witnesses-config.log)).
For `[1,2]`, K and both Python implementations return 2. The first attempted
functional-form witness was discarded because this backend does not support
functional claims; its exit 113 in
[23-kprove-claim-witnesses.log](evidence/23-kprove-claim-witnesses.log) is not
used as evidence.

### Adequacy limitation

`intVals(Ints)` is a proof-local `ValSeq` form. The candidate supplies only the
iterator observations needed by this program. Nil and cons iteration exactly
mirror the supplied list rules, and the program never asks for length,
truthiness, equality, indexing, or mutation of the input list. Thus the
representation is adequate for this submitted program, but it is not a
general-purpose native list model.

I attempted an additional universal theorem through reviewer-defined
`nativeIntVals(nil)=.ValSeq` and
`nativeIntVals(cons(X,XS))=vCons(X,nativeIntVals(XS))`. It builds, but proof
search leaves constrained branches equating the proof-only and native symbolic
forms and exits 1; see
[34-kompile-native-loop-definition.log](evidence/34-kompile-native-loop-definition.log)
and [35-kprove-native-loop.log](evidence/35-kprove-native-loop.log). This is not
a counterexample: concrete native-list execution succeeds, and the failed
residual does not show differing results. It does mean that a universal native
representation bridge was not machine-established, which is one reason for
the `CONCERNS` verdict.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](evidence/inventory_k.py) inventories the assembled supplied
semantics, every helper K file, `verification.k`, and `spec.k`. Its complete
output is [25-rule-inventory.log](evidence/25-rule-inventory.log):

- 714 rules: 473 equational and 241 operational;
- 237 syntax declarations;
- 150 function declarations and 111 `total` declarations;
- 46 priority rules, 36 concrete equations, and 8 macros;
- 25 `symbol` declarations, of which 22 have `no-evaluators`;
- 5 contexts, 1 configuration, and 2 claims;
- no local `functional` declaration and no simplification rule.

[classify_k_inventory.py](evidence/classify_k_inventory.py) attaches a
disposition and rationale to every configuration, syntax declaration, context,
rule, and claim. All 959 such entries are enumerated in
[33-static-rule-decisions.log](evidence/33-static-rule-decisions.log).
[used-construct-map.md](evidence/used-construct-map.md) maps every constructor
actually present in `solution.mpy` to its declaration and executing rules.

Because the entire reference tree is byte-identical to the selected trusted
semantics, supplied rules are the fixed language boundary. I nevertheless
checked their overlaps against the reachable program terms. All unused
float/string/sort/dict/comprehension/slice/assert/import patterns are disjoint
from this execution. `MPY-CONCRETE` is present only in the LLVM runtime module
and is absent from both Haskell proof definitions.

### Configuration, evaluation, state, calls, and returns

The initial cells match the supplied configuration. Module loading installs the
exact closure at scope 0. Call semantics evaluate the callee and arguments
left-to-right, allocate scope 1, bind `lst`, push `frame(CONT,0,1)`, and run the
body. Assignment strictness evaluates every RHS before the scope write. The
for-loop evaluates its iterable once, binds each yielded integer to `value`,
executes the body, and recurs. Integer comparison equations implement exactly
the used `==`, `!=`, and `<`; `BoolOp("or")` short-circuits in the correct order.
Return records the value, discards the rest of the callee computation, restores
the saved caller continuation/environment, deletes scope 1, and resets
`scopeLoc`.

Relevant high-priority cell/ref rules are guard-disjoint because this function
uses no closure cells or heap references. The installed loop rule has priority
40, but its match fixes the exact loop body, exact return suffix, exact
`#endcall`, exact function binding shape, saved frame, and every state cell.

### Proof-local declarations and equations

1. **Program macros (`verification.k:8-45`).** All four macros expand to the
   exact submitted program, as established by the KORE comparison. They do not
   bypass execution.
2. **`Ints`, `intVals`, and selectors (`verification.k:49-57`).**
   `intsEmpty` is exhaustive. `intsHead` and `intsTail` are marked `total` but
   have equations only on `consInts`; their values on `nilInts` are
   underdetermined. Every reachable use is guarded by
   `notBool intsEmpty(IS)`, so those opaque nil cases cannot affect control,
   state, result, or the postcondition.
3. **Iterator rules (`verification.k:58-62`).** The guards partition
   `nilInts`/`consInts`; the yielded head and recursive tail are exactly the
   supplied `.ValSeq`/`vCons` list behavior. They affect only the proof-local
   representation described in Stage 4.
4. **`nsScan` (`verification.k:66-95`).** This is a definitional result summary,
   not an oracle. The two empty cases split `COUNT == 2`. For a nonempty input,
   the remaining rules partition `COUNT == 0`; new minimum; duplicate minimum;
   first second-minimum; intermediate second-minimum; and value at/above the
   current second minimum. Their guards are pairwise disjoint and exhaustive
   by integer trichotomy, and every recursive call descends through
   `intsTail`. The equations mirror the program branches and fully determine
   every target use.
5. **Installed loop rule (`verification.k:104-145`).** This is an operational
   bridge and received the strongest review.

### Operational bridge validation

The candidate first proves loop execution without importing the installed
bridge. Its published loop claim leaves final scopes unconstrained, while the
installed rule writes the exact scope-deletion term. A reviewer-authored
strengthening that matches the rule's complete context is
[audit-loop-connection.k](evidence/audit-loop-connection.k). Against the
unextended base definition it initially sticks only because the backend does
not normalize equality between two maps after deleting the same disjoint key;
see [26-kprove-strengthened-loop-connection.log](evidence/26-kprove-strengthened-loop-connection.log)
and the equivalent normalized attempt in
[27-kprove-normalized-loop-connection.log](evidence/27-kprove-normalized-loop-connection.log).

I then made the ordinary extensional MAP fact explicit:

```text
((I |-> S) M)[I <- undef] = M    when I is not a key of M
```

The reviewer rule is
[audit-map-delete-lemma.k](evidence/audit-map-delete-lemma.k). It is independent
of the program result and is true for the complete guarded domain. Its fresh
definition builds with exit 0
([28-kompile-audit-map-lemma.log](evidence/28-kompile-audit-map-lemma.log)),
after which the complete bridge-free connection theorem exits 0 and prints
`#Top`
([29-kprove-strengthened-with-map-lemma.log](evidence/29-kprove-strengthened-with-map-lemma.log)).
This validates the installed rule's value, continuation, environment, scope,
stack, return, heap, exception, and exit-code footprint.

Operational sensitivity was tested separately from postcondition non-vacuity.
[audit-mutated-verification.k](evidence/audit-mutated-verification.k) changes
the reached inner branch to store `value + 1`. The mutated definition builds
cleanly with exit 0
([31-kompile-loop-body-mutation.log](evidence/31-kompile-loop-body-mutation.log)).
The connection theorem then exits 1 with `WarnStuckClaimState` and the expected
residual equality between scans whose second accumulator is respectively
`head + 1` and `head`
([32-kprove-loop-body-mutation-expected-fail.log](evidence/32-kprove-loop-body-mutation-expected-fail.log)).
An earlier attempt to place new operational syntax directly in a proof module
was structurally rejected and is explicitly not used as sensitivity evidence
([30-kprove-loop-body-mutation.log](evidence/30-kprove-loop-body-mutation.log)).

No materially unsound local rule was found, so there is no false-conclusion
witness to report. The narrower gaps—proof-only list representation and
guarded underdefinition of `intsHead(nilInts)`/`intsTail(nilInts)`—are recorded
as limitations rather than mislabeled as unsoundness.

## 6. Fresh non-vacuity test

[audit-spec-vacuity.k](evidence/audit-spec-vacuity.k) is reviewer-authored and
changes the entry postcondition from `nsScan(INPUT,0,0,0)` to `noneV`. It keeps
the original satisfiable precondition and real program invocation. The mutation
is demonstrably false for `INPUT = [1,2]`, where the canonical Python,
candidate Python, and K summary all return 2.

The independent dry build:

```text
kprove audit-spec-vacuity.k --definition entry-verification-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run
```

exits 0; see
[36-vacuity-dry-run.log](evidence/36-vacuity-dry-run.log). The actual proof:

```text
kprove audit-spec-vacuity.k --definition entry-verification-kompiled --spec-module AUDIT-SPEC-VACUITY
```

exits 1 with `WarnStuckClaimState`. The residual is precisely
`noneV = nsScan(INPUT,0,0,0)`, not a parser, import, timeout, or unrelated
backend error; see
[37-vacuity-proof-expected-fail.log](evidence/37-vacuity-proof-expected-fail.log).
The proof is therefore non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the supplied semantics and the sound proof-local equations, for
every finite `INPUT:Ints`, execution from the exact initial configuration:

1. loads the submitted `solution.mpy` program (via a KORE-identical macro);
2. calls its actual `next_smallest` closure on `list(intVals(INPUT))`;
3. executes the initialization, real loop body, real return logic, and call
   cleanup; and
4. reaches the exact result `nsScan(INPUT,0,0,0)` without changing heap,
   heap-location, return, exception, exit-code, or caller-control observations
   constrained by the entry claim.

The loop connection is universal over the remaining finite input and arbitrary
integer accumulator values satisfying its concrete frame shape. This is
partial-correctness/reachability evidence under K; it is not a proof about
resource bounds or all of CPython.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied MPY semantics and K built-ins for unbounded `Int`, `Bool`, `Map`, `List`, heating/cooling, and reachability | Both claims | Acceptable and mode-authorized. Candidate tree is exactly the trusted baseline. |
| MAP disjoint-key deletion law used to validate exact scope cleanup | Installed loop bridge | Acceptable ordinary collection mathematics; guarded universally and separated from the task result. |
| `intVals(Ints)` as the symbolic representation of finite integer lists | Loop and entry claims | Sound for the sole used observation, iteration, but not machine-connected universally to native `vCons`; documented concern. |
| `intsHead(nilInts)` and `intsTail(nilInts)` totality | No reachable target path | Concerning in isolation but inert: all uses are guarded nonempty. |
| `nsScan` equations | Final result | Acceptable definitional summary: exhaustive, disjoint, descending, and connected to real loop execution. It is not opaque. |
| Informal theorem that `nsScan(INPUT,0,0,0)` is the second distinct minimum | Natural-language intent | Straightforward invariant/trichotomy argument and strongly differential-tested, but not separately formalized in K; documented concern. |
| Trusted translator and KORE macro identity | Real-program pinning | Strong: byte identity at both translation and parsed-expanded program levels. |
| Python canonical differential test and LLVM smoke execution | Intent/native-execution support | Finite empirical evidence only; never substituted for reachability proof. |
| Missing generation metadata/trace | Provenance | Evidence limitation; trusted source and semantics mounts still permit independent reconstruction. |

The 25 supplied `symbol` primitives are `sortVS`, `sortKeyVS`,
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`. None is reachable from this program or appears in
either target postcondition. There is no proof-local fresh or opaque result
symbol.

### Gate accounting

- Real-program soundness: **PASS**. Exact program identity, complete loop
  connection, body sensitivity, result constraint, and non-vacuity are
  established.
- Intent adequacy: **PASS WITH LIMITATION**. The representation and
  summary-to-property bridges are sound but partly informal.
- Trust/evidence auditability: **PASS WITH LIMITATION**. Reproduction evidence
  is complete, but candidate generation metadata is missing.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
