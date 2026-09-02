# Independent adversarial audit: 43-pairs-sum-to-zero

## Audit conclusion

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the exact submitted `solution.mpy` under its generated mathematical MPY
semantics. A clean Haskell reconstruction of the submitted target prints
`#Top` and exits 0. The proof does not replace execution with an answer oracle:
the submitted body executes, the recursive K state returns to the entry-claim
shape, and the proof-local `hasZeroPair` function is defined by truthful,
disjoint, exhaustive, descending equations.

The result is **CONCERNS / LEGIT**, not PASS, because the bridge from that
unbounded MPY semantics to the natural-language promise about the actual Python
function is limited. On this audit runtime, `solution.py` raises
`RecursionError` for no-pair lists of 1,000 and 1,100 positive integers, while
the canonical implementation and K semantics return `False`. The theorem is
explicitly partial correctness and does not prove normal termination or freedom
from resource exceptions, so this is not a counterexample to its Boolean
postcondition on normally returning executions. It is nevertheless a material
implementation/intent and language-model limitation on an intended-domain
input, and prevents PASS.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount contains only:

- `/reference/canonical.py`
- `/reference/prompt.py`
- `/reference/py2mpy.py`

`/reference/reference-semantics` is absent, including as a symlink. The mount
therefore agrees with the rendered mode; there is no infrastructure breach and
the audit proceeds to a candidate verdict. The exact inventory, file types,
permissions, sizes, SHA-256 hashes, and mode check are in
[01-integrity-inventory.log](evidence/01-integrity-inventory.log).

### Candidate artifacts

The required source artifacts are present as regular, non-symlink files:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`.
The candidate also supplies `prove.sh`, prompt/translator copies, run metadata,
logs, a structured trace, and a prebuilt `semantic-kompiled/` tree. No
candidate-provided compiled definition or cache was copied or used.

The candidate's `/candidate/prompt.py` is byte-identical to
`/reference/prompt.py`, and `/candidate/py2mpy.py` is byte-identical to
`/reference/py2mpy.py`. Their respective SHA-256 values are:

- prompt: `f20511ba41a7533e3f9593f29edff94e9190de6b789e91155c06a6b40eb83917`
- translator: `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

There are no changed, mistyped, or symlinked required source artifacts. The
extra `semantic-kompiled/` tree is an untrusted build product, not an integrity
substitute; it was ignored. No candidate `PROOF.md` or `spec-vacuity.k` exists.
Neither absence prevents reconstruction, and Stage 6 uses a fresh
reviewer-authored mutation.

### Untrusted generation claims

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured JSONL trace only as claims. They say the
generation was bare/generated-semantics, exited successfully, passed seven
concrete cases, printed `#Top`, and passed a 2,000-case randomized Python test.
The claimed randomized test script and inputs were not preserved by the
candidate, so that claim is not accepted as evidence. The structured trace has
202 valid JSONL records and zero parse errors. Relevant extracted claims and
the complete source listing are in
[01-source-and-claims-review.log](evidence/01-source-and-claims-review.log).
All substantive claims were checked independently below.

All execution source was copied to `/tmp/audit-work/candidate-src`; trusted
Python inputs were copied separately to `/tmp/audit-work/trusted`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires: for a list of integers, return `True` exactly when
there exist two distinct positions whose values sum to zero; otherwise return
`False`.

The trusted canonical function checks every pair of indices `i < j`. The
candidate uses the equivalent recursive decomposition:

1. the empty list has no pair;
2. for a nonempty list, return `True` if the additive inverse of the head is in
   the tail;
3. otherwise recurse on the tail.

The tail restriction enforces distinct positions, including the important
facts that `[0]` is false and `[0, 0]` is true.

### Trusted translation

I regenerated MPY with:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
cmp /tmp/audit-work/regenerated-solution.mpy \
    /tmp/audit-work/candidate-src/solution.mpy
```

`cmp` exits 0. Both files have SHA-256
`7620bbe22dae64260e7de1666540d5f6f1e198346d814eb3dc6664832b6e63c6`.
See [02-translator-byte-identity.log](evidence/02-translator-byte-identity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) loads the trusted
canonical entry point and candidate entry point from separate absolute paths.
Its deterministic inputs are fully preserved in
[differential-inputs.jsonl](evidence/differential-inputs.jsonl), SHA-256
`2352d49199ce463f108cfeb7d176a8891e1987913a13535b7ee1d77202fe4ea0`.
The scope is:

- all five documented examples;
- 16 curated boundaries covering empty, singleton, double zero, both head-pair
  orders, pair only in the tail, no-pair recursion, duplicate values,
  arbitrary-size integers, and recursion-depth boundaries;
- all 137,257 lists of length 0 through 6 over integers `-3..3`;
- 5,000 seeded lists of lengths 0 through 50 with values in
  `[-10^12, 10^12]`.

The exact command is recorded in
[02-python-differential.log](evidence/02-python-differential.log). It tests
142,278 inputs. There are no Boolean-result mismatches among the 142,276 cases
where both implementations return. There are two material execution
divergences:

- `[1] * 1000`: canonical returns `False`; candidate raises `RecursionError`.
- `[1] * 1100`: canonical returns `False`; candidate raises `RecursionError`.

The 950-element boundary returns normally. The differential command therefore
exits 1 intentionally and honestly records both mismatches. This is judged as
an implementation-to-intent and Python-to-MPY termination/exception
limitation, not hidden as a passing differential.

## 3. Clean proof reconstruction

### Toolchain and clean builds

The independently available live tools are K
`v7.1.293` (build date 2025-10-03); exact version output is in
[03-tool-versions.log](evidence/03-tool-versions.log).

No candidate build output was reused. I built an LLVM concrete definition:

```text
kompile semantic.k --backend llvm \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

This exits 0. It warns that `hasZeroPair`, `first`, and `rest` are declared
`[total]` without exhaustive equations in `semantic.k`; these warnings are
assessed in Stage 5. See
[03-kompile-concrete.log](evidence/03-kompile-concrete.log).

I built the exact submitted Haskell proof definition from `semantic.k`:

```text
kompile semantic.k --backend haskell \
  --main-module MPY-SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-proof-kompiled
```

This exits 0; see
[03-kompile-proof-exact.log](evidence/03-kompile-proof-exact.log). As an
additional cross-check, compiling `verification.k` as the definition main
module also exits 0
([03-kompile-proof.log](evidence/03-kompile-proof.log)), but the exact submitted
route is the basis for the verdict.

### Every positive target claim

`spec.k` contains exactly one unlabeled positive claim. I ran:

```text
kprove spec.k \
  --definition semantic-proof-kompiled \
  --spec-module SPEC
```

It exits 0 and prints exactly `#Top`; see
[03-kprove-spec-exact.log](evidence/03-kprove-spec-exact.log). There are no
other positive candidate claims to run.

### Fresh concrete generated-semantics execution

[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py) runs
the freshly compiled LLVM semantics and independently executes `solution.py`.
The ten preserved cases in
[concrete-inputs.jsonl](evidence/concrete-inputs.jsonl) include empty,
singletons, duplicate zero, a head pair, a pair only in the tail, recursive
false, a documented true case, zero-not-self-pair, and a 100-digit integer
pair. All ten K runs exit 0 and agree with Python; complete configurations and
results are in
[03-concrete-semantics-compare.log](evidence/03-concrete-semantics-compare.log).

The separate 1,000-element all-ones K run exits 0 with `pyBool(false)`;
[05-recursion-model-witness.log](evidence/05-recursion-model-witness.log)
contrasts with the Python exception recorded in Stage 2.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The sole entry claim has no explicit `requires`. Its precondition is every
finite `L:ISeq`, with:

- `<k>` holding `run` of the exact submitted module on `L`;
- `<program>` holding that same exact module;
- `<env>` equal to `.Map`.

Its postcondition requires:

- `<k>` to be exactly `pyBool(hasZeroPair(L))`;
- `<program>` unchanged;
- `<env>` again `.Map`.

There is no right-only variable, existential result, ellipsis around the
result, tautological implication, or unconstrained Boolean. It is an exact
result equality.

### Exact submitted-program identity

I extracted the entry claim's first `Module(...)` term and parsed it in K rule
mode, then parsed the submitted `solution.mpy` in program mode. Their normalized
KORE is byte-identical, with common SHA-256
`e10b6d40559e54579b177eefb86d4a6e7f607bc84668be863a530202e0c97379`.
The command, hashes, and extracted term are in
[04-program-pinning-structural.log](evidence/04-program-pinning-structural.log);
the extracted artifact is
[spec-entry-program.mpy](evidence/spec-entry-program.mpy).

The same literal program appears in `<program>`. The recursive-call rule checks
that the called name equals the function stored in that cell before re-entry.
After a false membership test, real execution reaches exactly
`run(the-same-program, rest(L))` with empty environment, which is the main
claim's circularity shape. There is no substituted helper/loop program.

### Satisfiable witnesses and concrete substitution

Every concrete `ISeq` with the exact program and empty environment satisfies
the precondition. For example:

```text
L = 0 :: 0 :: .ISeq
```

`hasZeroPair(L)` reduces to `true`; both trusted canonical and candidate Python
return `True`, and fresh K execution returns `pyBool(true)`. A reviewer-authored
ground claim replacing the symbolic input/result with this concrete
state/result prints `#Top` and exits 0; see
[spec-ground-true.k](evidence/spec-ground-true.k) and
[04-ground-witness-kprove-exact.log](evidence/04-ground-witness-kprove-exact.log).

The empty witness similarly reduces to `hasZeroPair(.ISeq) = false`, and both
Python implementations and concrete K return false. These witnesses cover both
result values and demonstrate that the universal precondition is realizable.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule record is
[rule-inventory.md](evidence/rule-inventory.md). Its source cross-check is
[05-inventory-crosscheck.log](evidence/05-inventory-crosscheck.log). It
enumerates:

- all 31 local syntax productions;
- the three configuration cells;
- all 12 `[function]` declarations and five `[total]` attributes;
- all 32 ordinary semantic rules;
- all three proof-local simplification rules;
- the one entry claim;
- every submitted-AST construct and its executing rules.

There are no local priority rules, separate `functional` declarations, opaque
attributes, fresh result symbols, or helper K files.

### Operational semantics

The generated semantics is a recognizable AST interpreter for the exact MPY
subset used. It models statement sequencing, pure expression evaluation,
environment lookup, list truthiness, integer negation, index zero, slice
`[1:]`, integer membership, branch selection, literal Boolean returns, and the
exact tail-recursive self-call. Each construct in `solution.mpy` maps to a
declaration and a reachable rule.

Bindings are pinned: entry binds the sole argument to the declared parameter,
and recursive re-entry requires the literal call name to equal the function in
`<program>`. Expression evaluation is atomic but pure, so no source evaluation
order or side effect is lost. Returns discard the remaining function
continuation and clear the local environment, matching the submitted control
flow. List slicing is represented by the `ISeq` tail rather than allocating a
new Python list; because this program has no mutation or identity observation,
that is observationally sound.

The call rule performs unbounded tail re-entry without a call-stack or
exception cell. Relative to the selected mathematical MPY level, it is a
coherent operational rule. Relative to concrete CPython, it omits recursion
resource failure. The required witness is the 1,000-element all-ones input: K
concludes `pyBool(false)`, while candidate Python raises `RecursionError`.
Because this affects whether there is a normal result rather than changing a
Boolean result of a normally returning run, it is classified as Gate B
language-model adequacy, not a smuggled Gate A correctness rule.

The unused fall-through rule yields `pyNone` without clearing `<env>` and is
not a reusable full Python frame model. It is unreachable in the submitted
function: the empty branch returns, the membership-true branch returns, and the
remaining path tail-returns. Under the generated-semantics boundary, incomplete
or thin behavior for unused constructs is not a defect.

### Functions, totality, overlap, and descent

`isEmpty` and `member` are genuinely total, constructor-disjoint, and
descending. `hasZeroPair` has no concrete equation in `semantic.k`, producing
the LLVM warning, but it is not executed by the program. In the proof theory,
the two equations in `verification.k` cover empty and nonempty `ISeq`
disjointly and exhaustively, with recursion on the strict tail.

`first` and `rest` are incorrectly marked `[total]` over all `ISeq` despite
having only nonempty equations. The fresh compiler exposes this directly. No
submitted execution or proof branch evaluates either on `.ISeq`: source
indexing/slicing is dominated by `if not l`, and the summary equation calls
them only under `notBool isEmpty(L)`. I therefore record the over-broad
attributes as a static modeling concern/evidence gap, not an unsoundness claim:
there is no reachable intended-input witness by which these attributes enable
a false result.

All other partial functions cover their sole reachable argument sorts/shapes.
Applicable equations are pairwise disjoint or agree; there is no priority
preemption.

### Proof-local extensions

The proof-local inventory is:

1. `notBool notBool B => B [simplification]`: true Boolean algebra.
2. `hasZeroPair(L) => false` when `L` is empty.
3. For nonempty `L`,
   `hasZeroPair(L) => member(-first(L), rest(L)) orBool
   hasZeroPair(rest(L))`.

Items 2 and 3 are a definitional mathematical summary, not operational
bridges. They touch no cells and replace no program term. Their recurrence is
the exhaustive partition of a distinct-position zero-sum pair: it either uses
the head and a later inverse or lies wholly in the tail. The equations
terminate structurally.

Removing the summary equations does not leave a freely interpreted oracle that
can close the proof. The resulting spec builds, then fails with
`false = hasZeroPair(L)` unmet on the empty branch; see
[spec-no-summary.k](evidence/spec-no-summary.k),
[05-no-summary-dry-run.log](evidence/05-no-summary-dry-run.log), and
[05-no-summary-kprove.log](evidence/05-no-summary-kprove.log).

### Body sensitivity

I independently changed both pinned copies of the source body's empty-list
return from `false` to `true`, leaving the original result obligation
unchanged. The mutated spec builds successfully, then proof exits 1 with a
reachable empty-list residual containing `pyBool(true)` instead of the required
false summary. See
[spec-body-mutation.k](evidence/spec-body-mutation.k),
[05-body-mutation-dry-run.log](evidence/05-body-mutation-dry-run.log), and
[05-body-mutation-kprove.log](evidence/05-body-mutation-kprove.log). This shows
the proof is sensitive to the executed body.

No task answer is encoded in an operational rule, no property-bearing
computation is replaced by an unconstrained value, and no used construct is
fabricated.

## 6. Fresh non-vacuity test

There was no candidate vacuity artifact to trust. I copied the original spec
in scratch and changed only its result-constraining postcondition:

```text
pyBool(hasZeroPair(L))
```

became:

```text
pyBool(notBool hasZeroPair(L))
```

The mutation is demonstrably false for the satisfying empty-list input:
execution returns `pyBool(false)`, while the mutated postcondition requires
`pyBool(true)`.

The mutation is preserved at
[spec-vacuity.k](evidence/spec-vacuity.k). Its dry run exits 0 and emits a valid
`kore-exec --prove` command
([06-vacuity-dry-run.log](evidence/06-vacuity-dry-run.log)), so it is not a
parser, import, or build failure. The actual proof exits 1 with
`WarnStuckClaimState`; the residual contains the normally terminated
`pyBool(false)` configuration and the reachable condition
`true = isEmpty(L)`. See
[06-vacuity-kprove.log](evidence/06-vacuity-kprove.log). This is the expected
unmet result obligation, establishing non-vacuity.

## 7. Proven versus assumed accounting

### Precisely proven

Under the freshly built `MPY-SEMANTIC` operational theory plus the three
truthful proof simplifications, the successful reachability claim establishes:

> For every finite mathematical integer sequence `L`, whenever the exact
> submitted MPY program executes from its entry configuration and reaches its
> return configuration, the result is exactly
> `pyBool(hasZeroPair(L))`, the program cell is unchanged, and the local
> environment is empty.

The reachability circularity is a partial-correctness argument. It does not
establish termination, complexity, absence of resource failure, or behavior
outside the modeled MPY subset.

By the recursive equations and ordinary induction on `L`,
`hasZeroPair(L)` is true exactly when two distinct sequence positions contain
additive inverses. That summary-to-natural-language induction is mathematically
checked in this audit but is not a separate K reachability claim.

### Trust ledger and limitations

| Boundary | Dependents | Status and support |
|---|---|---|
| K parser/compiler, Haskell prover, LLVM execution backend, and reachability-logic implementation | All machine-checked results | Necessary low-level trusted computing base. Fresh source builds and mutation discrimination reduce, but cannot eliminate, this trust. |
| Imported K `INT`, `BOOL`, `MAP`, and collection primitives | Integer arithmetic, Boolean logic, environment, and list encodings | Acceptable standard-library primitives. No candidate-defined axiom alters them. |
| Trusted `py2mpy.py` maps `solution.py` to `solution.mpy` | Python-to-MPY program identity | Byte-identity regeneration is direct evidence. |
| `ISeq` represents finite Python lists of built-in mathematical integers | Input-domain bridge | Appropriate for the stated ordinary list-of-integers domain. Custom list/int subclasses, mutation, alias/identity behavior, and non-integer entries are excluded. |
| Generated semantics models unbounded calls and no resource/exception state | Python behavior bridge | Concerning but legitimate for this partial-correctness theorem. The exact CPython recursion witness is preserved; total functional correctness for arbitrary list length is not established. |
| `hasZeroPair` equations mean the English existential property | Final intent bridge | Supported by a straightforward exhaustive induction and by the independent canonical differential tests, but not a separate K theorem. |
| Finite concrete and differential tests | Translation/adequacy evidence only | Empirical evidence, never substituted for the K proof. The full input set, exact commands, and mismatches are preserved. |

There is no external opaque result primitive, empirical oracle inside the K
theory, assumed helper claim, or candidate compiled cache in the proof's trust
base.

### Validation gates and verdict rationale

- **Gate A — real-program proof soundness: PASS.** The exact normalized
  submitted AST executes; the summary is defined rather than opaque; the
  recurrence matches real control flow; body and result mutations fail for
  expected reachable obligations.
- **Gate B — intent/language adequacy: LIMITED.** The Boolean relation is right
  on all normally returning tested inputs and matches the contract
  mathematically, but the actual recursive Python implementation and generated
  semantics differ at CPython recursion exhaustion. The theorem is partial
  correctness and does not prove the prompt's apparent total-return promise.
- **Gate C — trust/evidence auditability: PASS.** Fresh commands, statuses,
  source mutations, complete deterministic input sets, and bounded relevant
  outputs are preserved under `evidence/`. Candidate prose and prior `#Top`
  were not used as proof.

The earliest limitation is Gate B, so the proof remains legitimate but carries
material concerns rather than receiving PASS.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
