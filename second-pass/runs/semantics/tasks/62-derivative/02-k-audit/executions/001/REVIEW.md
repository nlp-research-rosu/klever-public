# Independent adversarial audit — 62-derivative

## Executive decision

The Python program is faithful to the trusted canonical implementation, the
submitted MPY is faithful to the Python source, all submitted positive claims
rebuild and print `#Top`, and a fresh false-result mutation is rejected.
Nevertheless, the proof is **not legitimate**: the proof-local symbolic
`enumerate` simplification in `/candidate/verification.k:40` is inconsistent
with the supplied semantics on the intended integer-list domain. The candidate
theory proves a false universal statement, with the empty integer sequence as a
concrete witness. The positive proof materially relies on that bridge.

This is a candidate soundness failure, not an infrastructure failure.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`.
`/reference/reference-semantics` is present, so the trusted mounts do not
contradict the rendered mode. A recursive, no-dereference comparison of
`/candidate/reference-semantics` against the trusted tree exited 0 with no
differences. The candidate tree contains no symlink, missing entry, extra
entry, changed entry, or mistyped entry. See
[stage1_integrity.log](evidence/stage1_integrity.log) and the reviewer script
[stage1_integrity.sh](evidence/stage1_integrity.sh).

The candidate `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The required proof sources
`solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular files.

### Missing provenance artifacts

The following requested untrusted provenance artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. I did not infer any claim from
those absent files. The candidate also contains `__pycache__`, candidate
concrete tests, and `prove.sh`; none was used as authoritative evidence. No
candidate-built K definition was present or reused.

There is no infrastructure breach: the trusted semantics mount exists exactly
when required and matches the candidate copy.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a finite coefficient list
`xs = [a0, a1, ..., an]` representing
`a0 + a1*x + ... + an*x^n`, return the coefficient list of its derivative:
`[1*a1, 2*a2, ..., n*an]`. Empty and singleton inputs return `[]`. The trusted
examples require:

- `[3, 1, 2, 4, 5] -> [1, 4, 12, 20]`
- `[1, 2, 3] -> [2, 6]`

The trusted canonical program computes all `i*x` pairs using `enumerate` and
drops index 0. The candidate uses an explicit loop and appends `i*x` only when
`i > 0`. These algorithms agree on finite coefficient lists.

### Translation fidelity

Using the trusted translator copied from `/reference/py2mpy.py`, the exact
command `python3 py2mpy.py solution.py` regenerated the submitted MPY
byte-for-byte:

- submitted and regenerated SHA-256:
  `2bcf05dc954c38635670b7d9f29e97af284ef97a270195c950960bb4d7b4d042`
- `cmp` exit status: 0

See [stage2_mpy_fidelity.log](evidence/stage2_mpy_fidelity.log) and
[stage2_mpy_fidelity.sh](evidence/stage2_mpy_fidelity.sh).

### Independent differential test

The reviewer-authored test imports the trusted canonical and candidate entry
points from byte-preserving scratch copies. It covered documented examples,
empty and singleton cases, index-0/index-1 branch boundaries, zeros,
negatives, large integers, representative finite floats, every list of
length 0 through 6 over `{-3,-1,0,1,2,7}`, and 1,000 seeded integer lists of
length 0 through 40.

The exact run tested 57,001 inputs and reported:

```text
DOCUMENTED_EXPECTED_FAILURES: 0
MISMATCH_COUNT: 0
```

Evidence:
[differential_test.py](evidence/differential_test.py),
[differential_cases.json](evidence/differential_cases.json), and
[stage2_differential.log](evidence/stage2_differential.log).

This is finite program-fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

### Scratch isolation and toolchain

All source artifacts needed for execution were copied into
`/tmp/audit-work/62-derivative`. The supplied semantics was copied from the
trusted `/reference` tree, not from a candidate cache. All definitions were
built from source. The available standalone tools report K
`v7.1.337`; `kup` is absent, but `kompile`, `krun`, and `kprove` are installed
and functional. See [stage3_toolchain.log](evidence/stage3_toolchain.log).

### Fresh builds

Both required builds exited 0:

```text
timeout 600 kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

timeout 600 kompile verification.k \
  --backend haskell --main-module VERIFICATION \
  --syntax-module VERIFICATION \
  --output-definition verification-kompiled
```

Logs:
[stage3_build_runtime.log](evidence/stage3_build_runtime.log) and
[stage3_build_verification.log](evidence/stage3_build_verification.log).

The fixed runtime build reported pre-existing non-exhaustiveness warnings for
some unused supplied total functions. The proof build succeeded. These
warnings are not the candidate failure identified below.

### Every positive target claim

Each positive obligation was run independently with a 600-second bound. The
loop invariant was first proved without trust; each entry claim was then run
separately with only that already-proved loop claim marked trusted.

| Obligation | Exact proof selection | Exit | Required signal |
|---|---|---:|---|
| Loop invariant | `kprove spec.k --definition verification-kompiled --claims loop-invariant` | 0 | `#Top` |
| Empty entry | `kprove spec.k --definition verification-kompiled --claims loop-invariant,entry-empty --trusted loop-invariant` | 0 | `#Top` |
| Nonempty entry | `kprove spec.k --definition verification-kompiled --claims loop-invariant,entry-cons --trusted loop-invariant` | 0 | `#Top` |

Logs:
[stage3_prove_loop.log](evidence/stage3_prove_loop.log),
[stage3_prove_entry_empty.log](evidence/stage3_prove_entry_empty.log), and
[stage3_prove_entry_cons.log](evidence/stage3_prove_entry_cons.log).

These runs establish closure only under the submitted extended theory. Stage 5
shows that theory is unsound.

### Fresh fixed-semantics execution

A reviewer-authored MPY program containing the exact candidate function plus
normal and boundary assertions was regenerated with the trusted translator and
run under the fresh LLVM definition. `krun` exited 0 with `<k> .K </k>`,
`NoExc`, empty stack, and the expected result lists in the heap. See
[stage3_concrete.py](evidence/stage3_concrete.py),
[stage3_concrete_run.sh](evidence/stage3_concrete_run.sh), and
[stage3_concrete_run.log](evidence/stage3_concrete_run.log).

No generated-semantics-only test was applicable in
`SUPPLIED_SEMANTICS` mode.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable preconditions

**`loop-invariant`.** If `N > 0`, the current computation is the real loop
over a lazy sequence representing the remaining integer coefficients
`INPUT`, starting at original index `N`. The local frame contains the real
`xs`, a reference to one result object, and integer `i`/`x` bindings. If that
result object initially contains `ACC`, loop completion returns to the
arbitrary continuation and changes the object to
`derivativeAcc(ACC, INPUT, N)`. Other mapped state is preserved, and final
`i`/`x` values merely have to be integers.

A satisfying and reachable-shaped instance is the state after index 0 of
input `[3,2]`: `N=1`, `INPUT=ivCons(2,.IntVals)`, `ACC=.ValSeq`,
`i=0`, `x=3`, `xs=list(vCons(3,vCons(2,.ValSeq)))`, and a fresh result
heap location containing the empty list. Map freshness side conditions are
satisfied by choosing distinct scope and heap locations.

**`entry-empty`.** Starting in the exact module frame with
`"derivative" |-> derivativeClosure`, builtins as parent, empty heap and
stack, `noRet`, and `NoExc`, call the function on the bare empty list. The
returned reference must point to a heap list equal to
`derivativeSeq(.IntVals)`, which reduces to `.ValSeq`. This precondition is
satisfied by the literal configuration written in the claim, with exit code
0 in the framed cell.

**`entry-cons`.** Under the same exact initial configuration, call the
function on an arbitrary head integer and arbitrary finite integer tail. The
returned reference must point to
`derivativeSeq(ivCons(HEAD,TAIL))`. Empty and cons are exhaustive for
`IntVals`, so the two entry claims cover every finite integer list.

### Real body and result constraint

The `<k>` entries call `Name("derivative")`; the scope binds that name to
`derivativeClosure`. The macro at `/candidate/verification.k:73` expands to
the exact constructor tree in submitted `solution.mpy`: docstring, fresh
empty result, `for i,x in enumerate(xs)`, the `i > 0` append, and
`Return(Name("result"))`. The target and body macros at lines 54 and 58 also
match the real subtrees. The used-rule trace is in
[stage5_used_constructs.md](evidence/stage5_used_constructs.md).

`?RESULT` is not a free answer variable: the same existential location is the
returned `ref` and the key whose heap value is constrained to the derivative
list. `?REST` permits only additional heap garbage and `?NEXT` permits the
advanced allocation counter. There is no tautological `ensures` or one-way
implication standing in for result equality.

### Concrete substitutions

Reviewer-authored ground claims directly require:

- `derivative([]) -> []`
- `derivative([3,1,2,4,5]) -> [1,4,12,20]`

Both independently exit 0 and print `#Top`; the same results are produced by
both Python implementations. See [spec-ground.k](evidence/spec-ground.k),
[stage4_ground_proofs.sh](evidence/stage4_ground_proofs.sh), and
[stage4_ground_proofs.log](evidence/stage4_ground_proofs.log).

### Adequacy limitation

The formal entry domain is finite lists of mathematical K integers. The prompt
annotates only `list`, not an element type, and both Python functions also
operate on ordinary finite float coefficient lists. Thus the proof would, even
if sound, establish less than the broadest natural reading of “polynomial
coefficients.” This is a documented scope limitation; it is not the decisive
failure.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The inventory covers the byte-pinned `semantics.k` tree, every helper K file,
`verification.k`, and `spec.k`. It contains 950 line-indexed items:

```text
claim=3
configuration=1
context=5
rule-concrete=35
rule-ordinary=600
rule-owise=26
rule-priority=45
rule-simplification=1
syntax=234
```

Every row records the source line, normalized declaration/rule, attributes,
and audit disposition. See the complete
[stage5_rule_inventory.md](evidence/stage5_rule_inventory.md), generated by
[inventory_k.py](evidence/inventory_k.py), with command evidence in
[stage5_rule_inventory.log](evidence/stage5_rule_inventory.log).

All entries under `reference-semantics/` are byte-pinned parts of the selected
semantics level, not candidate proof extensions. Their configuration,
evaluation order, calls, returns, allocation, mutation, control, integer
operations, and iteration rules used by this program were traced explicitly
in [stage5_used_constructs.md](evidence/stage5_used_constructs.md). Unused
supplied opaque symbols are accounted for in Stage 7.

### Proof-local rule decisions

The `IntVals` datatype and `asValSeq` equations are structurally exhaustive,
disjoint, and descending. The `derivativeSeq`/`derivativeAcc` equations
faithfully encode dropping index 0 and appending `N*I` thereafter.
`derivativeAcc` is intentionally not total for negative `N`; no reachable use
has negative `N`. The three macros are exact program syntax and do not bypass
execution.

The two `#iterNext(list(enumIntSeq(...)))` rules are locally the expected empty
and cons iterator steps and syntactically preserve the arbitrary continuation
and every non-`<k>` cell. They do not, however, justify the global
representation rewrite that creates `enumIntSeq`.

### Decisive false-conclusion witness

The rejected extension is:

```k
syntax ValSeq ::= enumIntSeq(IntVals, Int)
rule enumVS(asValSeq(VS:IntVals), N:Int)
  => enumIntSeq(VS, N)
  [simplification]
```

For a symbolic `VS`, the submitted theory normalizes:

```text
truthy(list(enumVS(asValSeq(VS), 0)))
=> truthy(list(enumIntSeq(VS, 0)))
=> true
```

The last step follows because `enumIntSeq(VS,0)` and `.ValSeq` are distinct
constructors, while supplied `truthy(list(S))` tests `S =/=K .ValSeq`.
Accordingly, the reviewer-authored universal claim “the enumeration is always
nonempty” exits 0 and prints `#Top`; K also warns that symbolic `VS` became
unused. See
[spec-bridge-symbolic-false.k](evidence/spec-bridge-symbolic-false.k) and
[stage5_symbolic_false_witness.log](evidence/stage5_symbolic_false_witness.log).

This conclusion is false on the intended domain at the concrete witness
`VS = .IntVals`, representing `xs=[]`. Under the supplied semantics:

```text
asValSeq(.IntVals) => .ValSeq
enumVS(.ValSeq, 0) => .ValSeq
truthy(list(.ValSeq)) => false
```

The same candidate theory independently proves that ground result `false`
with `#Top`; see
[spec-bridge-ground-candidate-false.k](evidence/spec-bridge-ground-candidate-false.k)
and [stage5_ground_contradiction.log](evidence/stage5_ground_contradiction.log).
Thus the extended theory admits both the false universal `true` result and its
empty-instance `false` result. This is the required concrete/symbolic false
conclusion witness, not merely an unproved concern.

The fixed-semantics ground context also reduces to `false`; attempting the
opposite ground result under the candidate leaves the explicit residual
`false`. See
[stage5_bridge_context_witness.log](evidence/stage5_bridge_context_witness.log).

### Material dependence and additional bridge evidence

The positive proof uses `enumIntSeq` in the loop invariant while the real
`enumerate` semantics produces `enumVS`; the rejected simplification is the
connection between them. In a reviewer-authored bridge-free reconstruction,
the definition builds, but the loop invariant fails with a stuck residual
requiring the symbolic fixed `enumVS(asValSeq(INPUT),N)` to equal the empty
sequence. See
[verification-no-bridge.k](evidence/verification-no-bridge.k),
[spec-no-bridge.k](evidence/spec-no-bridge.k), and
[stage5_no_bridge_proof.log](evidence/stage5_no_bridge_proof.log).
This does not show that no sound proof could exist; it shows that the submitted
closure is materially using the rejected bridge.

A separate bridge-free attempt to prove a universal eager-enumeration
characterization builds but remains stuck rather than closing. It is preserved
as an evidence gap, not mislabeled as unsoundness:
[verification-connection.k](evidence/verification-connection.k),
[spec-connection.k](evidence/spec-connection.k), and
[stage5_connection_proof.log](evidence/stage5_connection_proof.log).

Compiling the extended theory for LLVM also warns that adding `enumIntSeq` to
`ValSeq` makes numerous inherited `[total]` helpers non-exhaustive, including
`enumVS`, `vsLen`, `valSeqConcat`, and `valSeqAt`; see
[stage5_build_extended_runtime.log](evidence/stage5_build_extended_runtime.log).
Ground fixed/extended continuation probes agree, but ground evaluation does
not exercise the symbolic simplification and is only finite evidence:
[stage5_bridge_probe.py](evidence/stage5_bridge_probe.py) and
[stage5_bridge_probe.log](evidence/stage5_bridge_probe.log).

The false universal witness is enough to reject the proof-local theory.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. The reviewer created a new
`SPEC-VACUITY-AUDIT` claim using the satisfiable exact empty-entry
precondition. The result-bearing postcondition was changed from the true
empty result `[]` to the false result `[1]`.

The mutated source parses and reaches real execution. `kprove` exits 1 with
`WarnStuckClaimState`; its final state returns `ref(0)` with heap location 0
equal to `list(.ValSeq)`, which cannot unify with the required
`list(vCons(1,.ValSeq))`. This is the expected unmet result obligation, not a
parser error, timeout, missing import, or unrelated crash.

Evidence:
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k),
[stage6_vacuity_run.sh](evidence/stage6_vacuity_run.sh), and
[stage6_vacuity.log](evidence/stage6_vacuity.log).

This confirms result sensitivity. Non-vacuity cannot make an inconsistent
proof extension sound.

## 7. Proven versus assumed accounting

### What the successful reachability runs syntactically establish

Under the submitted extended K theory, the loop claim summarizes all finite
`IntVals` tails at positive indices, and the two entry claims say that the
exact closure returns a reference to a heap list equal to the structural
`derivativeSeq` fold for every finite integer coefficient list.

Because the extended theory proves the false enumeration statement exhibited
in Stage 5, these `#Top` results do **not** establish that theorem about the
real program under the supplied semantics.

### Trust ledger

- **Supplied MPY semantics:** The entire byte-pinned
  `/reference/reference-semantics` tree is the authoritative selected
  semantics. Its fixed rules are accepted at that level. The actual program
  uses only module/function/call/frame, name/string/list/tuple, enumerate/loop,
  assignment/append, integer comparison/multiplication, return, and allocation
  paths mapped in the used-construct evidence.
- **K built-ins:** Mathematical integers, booleans, strings, maps, lists, K
  equality, arithmetic, and the K rewrite/proof engine are foundational
  trusted primitives.
- **Unused supplied opaque/symbol boundaries:** The inventory includes
  `sortVS`, `sortKeyVS`, `md5hexCodes`, and the float-related symbols
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
  `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
  `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
  `sqrtF`. None influences the integer-only claims.
- **`derivativeSeq`/`derivativeAcc`:** These are proof-local but not opaque;
  their explicit structural equations determine every value on the reachable
  domain. They influence the postcondition and are mathematically faithful.
- **`enumIntSeq`:** This is a fresh, result/control-bearing program-derived
  abstraction. It determines loop exhaustion, yielded indices/values, and
  therefore the final result. It is illegitimate because its global
  connection simplification is demonstrably inconsistent with fixed
  `enumVS`, and there is no successful bridge-free universal connection
  theorem.
- **Loop invariant:** It is independently proved under the extended theory
  and then trusted only as a circularity for entry proofs. Its use would be
  acceptable if the imported theory were sound.
- **Python-to-MPY bridge:** Byte identity under the trusted translator is
  established, not assumed.
- **Canonical-to-candidate intent bridge:** Supported by direct source
  reasoning and 57,001 finite differential cases. This is empirical support,
  not universal formal proof.
- **Supplied MPY-to-Python behavior:** Fixed-semantics concrete runs support
  the actually used integer path. Broader Python fidelity is outside this
  theorem and remains a named semantics-level assumption.
- **Natural-language domain:** Interpreting all polynomial coefficients as
  integers is narrower than the broadest reading of the prompt; floats are
  excluded from the formal theorem.
- **Missing generation provenance:** No generation trace or requested run
  metadata is available. No conclusion depends on it.

### Decision

Program fidelity, fresh reconstruction, claim result constraint, and finite
concrete evidence all pass. Soundness does not. The proof-local
`[simplification]` rule makes a false statement provable on the empty intended
input and is the submitted connection from real `enumVS` execution to the
loop invariant. Therefore the reconstructed `#Top` is not a legitimate
partial-correctness proof of the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
