# Independent adversarial review: 82-prime-length

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program. I rebuilt both definitions from source, obtained a fresh `#Top` for
the complete positive claim set, mechanically pinned the claimed closure and
loop to the trusted regeneration of `solution.mpy`, reviewed every local K
declaration/rule, and observed a fresh false-result mutation fail for the
expected semantic reason. No proof-local rule bypasses execution or introduces
an oracle.

The formal result is over every semantic string `str(CS:IntSeq)`. The
postcondition is the exact Boolean
`primeNat(isLen(CS))`; the four proof-local equations define this as trial
division over all candidates from 2 through `N-1`. This covers the HumanEval
string domain and does not impose a finite-size restriction.

## 1. Input and provenance integrity

### Launcher and record layout

I read `/audit-input.json` first and used its `container_paths`, not its
host-only provenance paths. It declares:

- problem `82-prime-length`;
- condition `kit-semantics`;
- `record_layout: pipeline-v3`;
- `semantics_mode: SUPPLIED_SEMANTICS`;
- `mount_reference_semantics: true`.

The trusted `/reference/reference-semantics` tree is present, so the mount is
consistent with the rendered semantics mode. There is no infrastructure stop
condition.

`/audit-campaign-lock.json` is a regular file. Its parsed JSON object is exactly
the `audit_campaign` object in `/audit-input.json`, and its independently
computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

All required `pipeline-v3` records are present, readable regular files:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, and `prompt.txt`. I also parsed all 371 JSON records in the
structured trace. Its one JSONL file has SHA-256
`416404de1b66da876f40d13c25873180f8d567cf971b306b2d95ebbeafafd5f5`,
matching both the invocation and generation-result records. The trace has no
symlinks or unsupported entries.

Every launcher-declared regular-file hash checked independently matched,
including the run/task/stage result, invocation, all required evidence
records, canonical source, trusted prompt/translator, and candidate
prompt/translator. The generation records say the untrusted run succeeded and
claimed `VALIDATED`; I did not use that claim as proof evidence. The bounded
record inspection is in
[stage1-generation-summary.log](/audit-output/evidence/stage1-generation-summary.log).

### Candidate and supplied-semantics integrity

The candidate prompt is byte-identical to `/reference/prompt.py` (SHA-256
`ed81b55d...28fa`), and its translator is byte-identical to
`/reference/py2mpy.py` (SHA-256 `406485ea...db16`).

I recursively compared `/candidate/reference-semantics` with
`/reference/reference-semantics` by relative path, node type, and file bytes.
The trees match exactly: 24 regular files, one subdirectory, no missing or
additional entries, no changed types or bytes, and no symlinks. The
reviewer-defined path/type/content digest of either tree is
`dde4cec993f522f90ecf100f5de2c1512cd9c74398379a1d965e7a90318e8fe3`.

The required candidate proof artifacts (`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`) are regular files.
Candidate-built `runtime-kompiled` and `verification-kompiled` directories were
not copied or used. Exact hashes, record checks, trace schema counts, and the
full-candidate reviewer digest are preserved in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log), generated
by [stage1_integrity.py](/audit-output/evidence/stage1_integrity.py).

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks for `prime_length(string)`, returning true exactly when
the string length is prime. Its examples require true for lengths 5 and 7 and
false for length 6.

The trusted canonical implementation computes `l=len(string)`, rejects 0 and
1, and rejects any divisor in `range(2,l)`. The candidate computes the same
property with a Boolean accumulator:

1. `n = len(string)`;
2. initialize `divisor=2` and `prime=(n>=2)`;
3. for every integer divisor below `n`, set `prime=false` when it divides `n`;
4. return the accumulator.

Continuing the loop after finding a divisor does not change the result because
the program never sets `prime` back to true.

### Trusted regeneration

In scratch I ran:

```text
python3 /tmp/audit-work/proof/py2mpy.py /tmp/audit-work/proof/solution.py \
  > /tmp/audit-work/proof/solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`82ebcade958aa41bb808c354ea5b6018f15b1b6bacd19806d7489499a2759b2f`;
`cmp` exited 0. See
[stage2-translation.log](/audit-output/evidence/stage2-translation.log).

### Independent differential test

[stage2_differential.py](/audit-output/evidence/stage2_differential.py)
imports the trusted canonical and candidate entry points independently and
also uses a separately implemented square-root trial-division oracle. It tests:

- all four documented examples;
- 19 explicit empty, branch-boundary, composite/prime, NUL, combining-mark,
  non-ASCII, and emoji cases;
- two strings at every length 0 through 300 (ASCII and non-ASCII);
- 250 deterministically generated mixed-Unicode strings, seed 820082.

All 875 cases agreed with both oracles. The serialized generated-input digest is
`6b7f76bfdf7244fbfe9f97725a469550651726c199635534ee9e86e56548cc3f`.
The exact command exited 0 with zero mismatches; see
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).

Stage 2 result: **PASS**.

## 3. Clean proof reconstruction

I copied only candidate source artifacts and the already integrity-checked
supplied semantics to `/tmp/audit-work/proof`. I did not copy or reference a
candidate kompiled directory or cache. The observed K tools are all v7.1.293;
see [stage3-tool-versions.log](/audit-output/evidence/stage3-tool-versions.log).

### Fresh concrete definition

This clean build exited 0:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

The warnings concern non-exhaustive functions in unused float, collection, and
subscript paths. The exact build output is
[stage3-kompile-llvm.log](/audit-output/evidence/stage3-kompile-llvm.log).

I translated the reviewer-authored
[stage3_concrete.py](/audit-output/evidence/stage3_concrete.py) with the trusted
translator. It contains the exact candidate function and assertions at lengths
0, 1, 2, 3, 4, 5, 6, 7, 11, and 12. Running its `.mpy` in the fresh LLVM
definition exited 0 with `<k>.K</k>`, `NoExc`, and exit code 0; see
[stage3-krun-concrete.log](/audit-output/evidence/stage3-krun-concrete.log).

### Fresh proof definition and positive claims

This Haskell build exited 0:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

See
[stage3-kompile-haskell.log](/audit-output/evidence/stage3-kompile-haskell.log).

The helper claim selected independently closed:

```text
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
```

Output `#Top`, exit 0:
[stage3-kprove-loop.log](/audit-output/evidence/stage3-kprove-loop.log).

The required complete positive set then closed:

```text
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC
```

Output `#Top`, exit 0:
[stage3-kprove-all.log](/audit-output/evidence/stage3-kprove-all.log). This run
proves both the helper and entry claims and makes the helper available as the
entry proof's circularity.

For transparency, selecting only `SPEC.prime-length` while deliberately
excluding its loop claim does not close: after unrolling to divisor 8, the
backend reports `DecidePredicateUnknown`. That diagnostic is preserved in
[stage3-kprove-entry.log](/audit-output/evidence/stage3-kprove-entry.log). It
does not contradict the submitted proof architecture: the entry claim is
explicitly dependent on the loop claim, and the unfiltered target command above
includes and freshly proves that dependency.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` says: in a real function-local scope with
`n=N`, `divisor=D`, and `prime=P`, where `N>=0` and `D>=2`, executing the exact
candidate `#while` terminates (when it terminates under partial correctness)
with `prime=trialPrime(N,D,P)`. It leaves the exact final divisor existential,
which is acceptable because divisor is local and not observable in the entry
result.

`SPEC.prime-length` says: starting with the builtins scope and module scope that
binds `prime_length` to the pinned closure, calling it with any semantic string
`str(CS)` reaches the exact Boolean `primeNat(isLen(CS))`, with environment,
module scope, heap, allocator, stack, return state, exception state, and exit
code restored/preserved as specified.

The entry precondition `isLen(CS)>=0` excludes no finite `IntSeq`; it follows
structurally from the two `isLen` equations. Therefore the theorem is not
bounded to examples or fixed sizes. Non-string inputs are outside the prompt.

### Mechanical pinning

[stage4_pinning.py](/audit-output/evidence/stage4_pinning.py) extracts the
single `FuncDef("prime_length",Params("string"),...)` from the trusted
regeneration and compares its constructor body with the closure in the entry
claim. The only normalization is K's equivalent spellings for an omitted
empty statement list and explicit `.Stmts`. Binding name, parameter, closure
parent, complete body, and the loop condition/body all match. This is a
constructor-level comparison, not a source-text assertion.

The script also exhibits satisfying states:

- entry: `CS=iCons(97,iCons(98,.IntSeq))`, with `isLen(CS)=2`;
- loop: `N=4,D=2,P=true,S=str(.IntSeq)`.

It substitutes lengths 0, 1, 2, 4, and 5 into `primeNat`; each result agrees
with both trusted canonical and candidate Python. Exact output is in
[stage4-pinning.log](/audit-output/evidence/stage4-pinning.log).

As a machine check of concrete substitutions,
[stage4-ground.k](/audit-output/evidence/stage4-ground.k) executes the exact
closure with result-constraining destinations at lengths 0, 2, and 4. All three
ground claims produced `#Top`, exit 0; see
[stage4-ground-kprove.log](/audit-output/evidence/stage4-ground-kprove.log).

### Result adequacy

For `N<2`, `primeNat(N)` starts with false and has no candidate divisors, so it
is false. For `N>=2`, it starts true and scans every integer in `[2,N)`,
changing the accumulator to false exactly when a divisor is found and never
changing it back. A natural number at least 2 is prime exactly when no integer
in that interval divides it. Thus `primeNat(isLen(CS))` is equivalent to the
prompt property, not merely a name shared by execution and postcondition.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

### Inventory

I read all supplied K sources and the proof/spec sources. The exhaustive,
line-addressed inventory is
[stage5-rule-inventory.txt](/audit-output/evidence/stage5-rule-inventory.txt),
generated by
[stage5_inventory.py](/audit-output/evidence/stage5_inventory.py). It contains:

- 26 files and 1,111 inventoried constructs;
- 229 local syntax declarations;
- 699 local rules;
- five evaluation contexts and one configuration;
- 148 function declarations, including 108 marked `total`;
- 22 fixed-semantics `no-evaluators` opaque symbols;
- 45 priority, 35 concrete, and 26 owise rules;
- zero simplification rules and zero `functional` declarations;
- the two positive claims.

Each item includes its full source block, exact line range, classification, and
audit disposition. Detailed reasoning, the complete used-constructor map, and
explicit witnesses for fixed-semantics scope limitations are in
[stage5-static-review.md](/audit-output/evidence/stage5-static-review.md).

### Active operational path

The used rules faithfully implement:

- exact scope lookup through local, module, then builtins frames;
- callee-before-argument and left-to-right argument evaluation;
- exact closure selection, one-parameter binding, frame push/pop, and return;
- string length as structural `IntSeq` length;
- mathematical integer addition/comparison and Python modulo for
  `N>=0,D>=2`;
- strict condition evaluation, Boolean truthiness, assignment, `If`, and the
  recurring `#while` control term;
- preservation/restoration of all observable cells.

All fixed priority rules were checked against the complete active
configuration. Their patterns or guards require refs, closure cells,
math/hashlib calls, collection operations, or sorting and are disjoint here.
No rule preempts lookup, `len`, modulo, the loop, or return.

### Proof-local extensions

`verification.k` declares only:

```text
trialPrime(Int,Int,Bool) [function]
primeNat(Int) [function,total]
```

and four pure equations. It adds no k-cell rewrite, operational bridge,
priority, simplification, concrete rule, or opaque symbol.

The `trialPrime` guards are exhaustive and pairwise disjoint on every use:
`D>=N` versus `D<N`, and then `pyMod(N,D)==0` versus nonzero. `D>=2` excludes
division by zero; the recursion advances `D` and decreases `N-D`. Its equations
exactly describe one candidate-divisor iteration of the real loop.
`primeNat(N)` truthfully initializes that fold with `D=2` and `N>=2`.

The loop claim is a derived reachability circularity over the exact recurring
program term. It does not become an operational rule accepting a broader
context. The entry theorem supplies the bridge-free universal connection from
fixed execution to the summary.

### Supplied-semantics boundary

The unused supplied semantics is intentionally a Python subset, not universal
CPython. The full review found and witnessed out-of-slice limitations such as
ASCII-only string predicates, simplified encoding/import behavior,
`isinstance(True,int)`, bool-versus-int collection equality, multi-character
`int(str)` validation, and an explicit no-escaping-closure assumption. Those
rules cannot match this program or affect its returned value. Likewise, all 22
opaque float/sort/MD5 symbols are unreachable.

No unsound rule is active on the intended input domain, no rule fabricates the
task result, and no proof-local rule encodes or assumes the loop's correctness.

Stage 5 result: **PASS**.

## 6. Fresh non-vacuity test

I ignored the candidate's mutation files and authored
[stage6-false.k](/audit-output/evidence/stage6-false.k). It calls the exact
closure on `"abcde"` (length 5) but deliberately requires `false`. The state
satisfies the entry conditions, and both Python implementations return true.

First, the mutation parsed and compiled to KORE:

```text
kprove stage6-false.k --definition fresh-verification-kompiled \
  --spec-module STAGE6-FALSE --dry-run
```

Exit 0; see [stage6-dry-run.log](/audit-output/evidence/stage6-dry-run.log).

The actual proof command then exited 1 with `WarnStuckClaimState`. Its residual
contains `<k> true ~> .K </k>` against the false destination, while all other
cells are the expected restored entry cells:
[stage6-false-kprove.log](/audit-output/evidence/stage6-false-kprove.log).
This is a reachable, result-bearing unmet obligation—not a parse error,
timeout, missing import, or unrelated crash.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### Formally proven

Conditional on the fresh supplied MPY definition and K backend, the complete
reachability proof establishes:

1. for every finite semantic string `str(CS)` satisfying the structural
   nonnegative-length condition;
2. lookup selects the exact submitted `prime_length` body;
3. the body executes through `len`, initialization, every loop test/body
   operation, return, and frame cleanup;
4. if that execution terminates, its returned Boolean is exactly
   `primeNat(isLen(CS))`;
5. the loop claim establishes the exact `trialPrime` summary for arbitrary
   `N>=0,D>=2,P`.

Ordinary mathematics then identifies `primeNat(N)` with primality of natural
`N`. This intent bridge is transparent and follows directly from the
exhaustive divisor interval; it is not supplied by testing.

### Assumptions and trust ledger

- **Trusted translator:** `/reference/py2mpy.py`. It fixes the Python-to-MPY
  constructor mapping. Dependents: program identity and all formal claims.
  Evidence: byte-identical regeneration and constructor-level pinning.
- **Supplied MPY operational semantics:** exact trusted tree under
  `/reference/reference-semantics`. Dependents: value, evaluation order,
  control, scope, call/return, and state behavior. Its complete active slice
  was statically reviewed and concretely exercised. Equivalence of the whole
  supplied subset to CPython is not itself proved.
- **K v7.1.293, Kore/Haskell prover, LLVM executor, SMT/builtin theories:**
  trusted implementation boundary for reachability, maps/lists, strings,
  integers, and Booleans. Dependents: every machine result. Evidence:
  clean builds, positive proof, ground checks, and discriminating mutation.
- **Semantic-string bridge:** one `iCons` represents one abstract character for
  length. Dependents: relation between `isLen(CS)` and Python `len`. Character
  contents cannot influence this program. Formal input accepts arbitrary
  integer codes, so the ASCII literal restriction does not narrow the theorem.
- **Trusted canonical and CPython execution:** finite validation only.
  Dependents: differential evidence, not universal proof.
- **Prime characterization:** a natural `N>=2` is prime iff no integer
  `2<=D<N` divides it. Dependents: the human-facing interpretation of
  `primeNat`; accepted ordinary mathematics.

There is no active proof-local opaque symbol, unconstrained result, empirical
oracle, operational bridge, or assumed program-defined helper. The fixed
semantics' opaque symbols have no dependents in either positive claim.

### Excluded

The theorem does not cover non-string Python inputs, resource/complexity
bounds, or a formal termination proof. It is partial correctness as requested.
It also does not prove the K implementation or the supplied semantics correct
in isolation. None of these exclusions narrows the material HumanEval source
contract.

Stage 7 result: **PASS**. Gates A (real-program soundness), B (intent adequacy),
and C (trust/evidence auditability) all pass. The recorded entry-only
dependency diagnostic is non-fatal and fully explained; no material evidence
or trust-boundary limitation remains.

VERDICT: PASS
LEGITIMACY: LEGIT
