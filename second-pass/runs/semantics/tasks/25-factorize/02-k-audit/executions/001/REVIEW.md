# Independent adversarial review: 25-factorize

## Outcome

The reconstructed K proof is legitimate and result-constraining, and it is
pinned to the submitted generated program. The candidate earns
`CONCERNS / LEGIT`, rather than `PASS`, for two auditability/adequacy limits:

1. the K postcondition names a transparently defined trial-division sequence
   `primeFactors(N)`, but it does not state or machine-prove predicates for
   primality, nondecreasing order, multiplicity, and product; the bridge from
   that recursive definition to the natural-language contract remains an
   ordinary mathematical argument supported by finite differential evidence;
2. the expected untrusted generation records (`run-input.json`,
   `metrics.json`, `codex-last.txt`, `codex-output.log`, and a structured trace)
   are absent, so the generation history cannot be audited.

Neither limitation makes a false conclusion provable. Fresh builds, both
positive claims, pinning, continuation sensitivity, body sensitivity, and
non-vacuity all behaved as an honest proof should.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The mount is consistent with that
mode: `/reference/reference-semantics` exists as a real directory. There is no
infrastructure contradiction, so a candidate verdict is appropriate.

I recursively compared `/candidate/reference-semantics` with the trusted
`/reference/reference-semantics` using type-sensitive, non-symlink-following
`diff`. The trees have identical entries and bytes, contain no symlink, and
have no missing or additional entry. The candidate `prompt.py` and
`py2mpy.py` are byte-identical to `/reference/prompt.py` and
`/reference/py2mpy.py`. Evidence:

- `evidence/01-candidate-tree.txt`
- `evidence/02-reference-tree.txt`
- `evidence/03-semantics-integrity.txt` (exit 0)
- `evidence/04-prompt-identity.txt` (exit 0)
- `evidence/05-translator-identity.txt` (exit 0)
- `evidence/30-provenance-presence-and-hashes.txt`

The required source/proof artifacts `solution.py`, `solution.mpy`, `spec.k`,
and `verification.k` are present as ordinary files. The scratch copies have
the same hashes as the candidate files. No candidate symlink exists.

Missing provenance evidence is reported explicitly:

- `/candidate/run-input.json`: missing
- `/candidate/metrics.json`: missing
- `/candidate/codex-last.txt`: missing
- `/candidate/codex-output.log`: missing
- structured trace (`*trace*` or `*.jsonl` at candidate top level): none

The candidate also contains untrusted ancillary items `prove.sh`,
`concrete_tests.py`, `concrete-tests.mpy`, and
`__pycache__/solution.cpython-310.pyc`. I inspected the text items only as
claims and did not execute their script or reuse the bytecode. No `PROOF.md`
or candidate-built definition was present or used.

All executable sources were copied to
`/tmp/audit-work/25-factorize-audit`. The semantics copy came from the trusted
reference tree. Every build in this review created a new output definition in
scratch. K version and tool locations are recorded in
`evidence/00-toolchain.txt` (K v7.1.337).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and source inspection

The trusted prompt asks `factorize(n)` to return the prime factors of the input
in nondecreasing order, including repeated factors with their multiplicities,
such that their product is the input. The examples require:

- `8 -> [2,2,2]`
- `25 -> [5,5]`
- `70 -> [2,5,7]`

The natural factorization domain is positive integers. `n=1` has the empty
factor sequence (empty product 1). Zero cannot satisfy the stated product-of-
prime-factors property, and negative inputs are not handled by the trusted
canonical implementation because it calls `sqrt(n)`. The formal domain
`N >=Int 1` is therefore aligned with the meaningful/canonical domain.

The trusted canonical implementation trial-divides only through the square
root and appends the remaining factor. The generated `solution.py` instead
increments a divisor from 2 until the repeatedly reduced `n` reaches 1. On
positive integers this is a different but valid trial-division algorithm. Its
divisible branch appends the divisor and divides `n`; its other branch
increments the divisor. It preserves multiplicity by retaining the divisor
after division.

### Translation identity

I regenerated `solution.mpy` from the scratch copy of `solution.py` using the
trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -l solution.mpy regenerated-solution.mpy
```

The command exited 0 and both files have SHA-256
`59f618a068725a224caa41c6973b799c1b91758d35d264cdfb848013a7912ee4`.
See `evidence/06-regenerate-mpy.txt`.

### Independent differential testing

`evidence/differential_factorize.py` imports the trusted canonical entry point
from `/reference/canonical.py` and the exact scratch copy of the generated
entry point. It does not reuse K summary equations. It checks equality and,
independently, sortedness, primality of every element, and product equality.

The preserved input set contains:

- all positive integers 1 through 1000;
- documented cases 8, 25, and 70;
- explicit loop/branch/multiplicity/prime boundaries, including 1, 2, 3, 4,
  9, 25, 49, 97, 121, 169, 256, 360, and 997;
- 128 deterministic generated inputs in `[1,50000]`, seed 250025.

There were 1125 unique inputs, zero implementation mismatches, and zero
contract failures. The exact generated input list, command, output, and exit 0
are in `evidence/07-differential.txt`. This is finite evidence, not a
universal K theorem.

## 3. Clean proof reconstruction

No candidate cache or compiled definition was copied. The following fresh
reconstruction was performed under `/tmp/audit-work/25-factorize-audit`.

### Concrete definition and execution

The exact command in `evidence/09-kompile-llvm.txt` freshly built
`runtime-kompiled` from trusted source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. Compiler exhaustiveness warnings concerned total helper functions
outside this program’s execution cone; they are accounted for in stages 5 and
7.

`krun solution.mpy` exited 0 and produced a final module scope containing the
exact submitted `factorize` closure (`evidence/10-krun-solution.txt`).

I authored `evidence/concrete_audit.py` independently. Its first 13 lines are
byte-identical to `solution.py`; it adds assertions for 1, 2, 3, 4, 8, 25, 70,
97, and 360. Translation/prefix identity is recorded in
`evidence/08-concrete-harness-identity-and-translation.txt`. Running the
translated harness under the fresh LLVM definition exited 0, with `NoExc`,
exit code 0, and heaps containing the expected lists
(`evidence/11-krun-concrete-audit.txt`).

### Universal loop target

I built a Haskell proof definition with main module
`FACTORIZE-VERIFICATION`, which does **not** import the promoted loop rule:

```text
kompile verification.k --backend haskell \
  --main-module FACTORIZE-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Build exit: 0 (`evidence/12-kompile-loop-proof.txt`).

I then ran the only claim in `FACTORIZE-LOOP-SPEC`:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module FACTORIZE-LOOP-SPEC --output pretty
```

Proof exit: 0; output contains `#Top`
(`evidence/13-kprove-loop.txt`). This is the bridge-free universal connection
proof for the actual loop and its summary.

### Entry target

I independently built the second Haskell definition:

```text
kompile verification.k --backend haskell \
  --main-module FACTORIZE-VERIFICATION-WITH-LOOP-LEMMA \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-with-lemma-kompiled
```

Build exit: 0 (`evidence/14-kompile-entry-proof.txt`).

I ran the only claim in `FACTORIZE-SPEC`:

```text
kprove spec.k --definition verification-with-lemma-kompiled \
  --spec-module FACTORIZE-SPEC --output pretty
```

Proof exit: 0; output contains `#Top`
(`evidence/15-kprove-entry.txt`). Thus every positive target claim closes
freshly with the required exit status and output.

## 4. Adequacy and real-program pinning

### Loop claim in plain language

The loop precondition says:

- `<k>` is the exact internal while loop followed by arbitrary `KONT`;
- current environment is scope location `L`;
- scope `L` contains exactly `n=N`, `divisor=D`, and
  `factors=ref(H)`, with parent 0, plus framed other scopes;
- heap location `H` contains `list(VS)`, plus framed other heap entries;
- `N>=1` and `D>=2`.

The postcondition consumes only the loop, preserves and resumes the same
arbitrary `KONT`, sets `n=1`, sets `divisor` to the recursively defined final
divisor, and replaces the list contents by
`factorLoop(N,D,VS)`. Other scopes, heap entries, and omitted configuration
cells are framed.

This precondition is satisfiable. One explicit witness is
`N=2,D=2,VS=.ValSeq,L=1,H=0` with the scope and heap shown in
`evidence/body-mutation-ground-spec.k`.

### Entry claim in plain language

For any K integer `N>=1`, the entry precondition starts with:

- `Call(Name("factorize"),Int(N))`;
- module environment 0;
- scope 0 binding `factorize` to the exact submitted one-argument body and
  parent `-1`;
- trusted supplied builtins at `-1`;
- next scope location 1, empty heap, next heap location 0, empty call stack,
  `noRet`, and `NoExc`.

The postcondition requires the call result to be exactly `ref(0)`, the only
allocated heap entry to be
`0 |-> list(primeFactors(N))`, and `heapLoc` to be 1. Stack, return, exception,
scope, and scope-location state are constrained, not omitted or replaced by
free result variables. The result is therefore neither tautological nor an
unconstrained oracle.

### Submitted-program pinning

The candidate entry claim begins after module loading, so I did not assume its
handwritten closure matched `solution.mpy`. I authored
`evidence/pinning-spec.k`, whose left side contains the complete literal
submitted `Module(ImportFrom(...),FuncDef(...))` term. Against the
lemma-free proof definition, that literal module loads to exactly the
`factorizeBody` closure and initial scope used by the entry claim. Dry-run
exited 0 (`evidence/28-pinning-dry-run.txt`); proof exited 0 with `#Top`
(`evidence/29-pinning-proof.txt`).

This, together with byte-identical trusted translation, pins the entry theorem
to the real submitted `.mpy`, including its body, parameter, module binding,
and the harmless `typing.List` import.

### Concrete substitutions

`primeFactors` was concretely evaluated in a fresh LLVM definition that
imports the proof equations:

- `N=1 -> .ValSeq`
- `N=2 -> vCons(2,.ValSeq)`
- `N=25 -> vCons(5,vCons(5,.ValSeq))`
- `N=70 -> vCons(2,vCons(5,vCons(7,.ValSeq)))`

The source evaluator, inputs, commands, full configurations, and exit 0
results are in `evidence/ground-eval.k` and
`evidence/18-krun-ground-*.txt`. Every value satisfies `N>=1`.
`evidence/19-ground-python-compare.txt` shows the trusted canonical and
generated Python entry points return exactly the corresponding `[]`, `[2]`,
`[5,5]`, and `[2,5,7]`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_inventory.py` produced
`evidence/16-rule-inventory.txt`, a complete block inventory of all 26 K
sources involved: the supplied assembled semantics and every helper, plus
`verification.k` and `spec.k`. It contains:

- 706 rules;
- 233 syntax declarations;
- five contexts;
- one configuration;
- two reachability claims;
- 149 function records and 107 total records;
- 25 symbol records, including 22 `no-evaluators` records;
- 46 priority and 26 `owise` records;
- no `functional` and no `simplification` records.

`evidence/static-rule-dispositions.md` maps every inventoried source/rule to a
disposition and maps every constructor in `solution.mpy` to its declaration
and dynamic rules. That file is part of this review; the important conclusions
are summarized below.

### Used semantics and state/control behavior

The actual execution path is:

1. `Module` loading treats the type-only `typing.List` import as a no-op and
   installs a closure containing the exact body.
2. `Call` evaluates the callee and integer argument, creates scope 1, binds
   `n`, pushes the continuation frame, and enters the body.
3. `ListExpr()` allocates heap location 0 and increments `heapLoc`.
   Assignments store `factors=ref(0)` and `divisor=2`.
4. `While` evaluates `n>1`; `If` evaluates `n % divisor == 0`.
   Integer `%`/`//` use `pyMod`; the claim invariant keeps `divisor>=2`, so
   division by zero is impossible.
5. The divisible branch dispatches the exact bound `append` mutator. Its
   priority-40 rule updates the same heap list in place, then assigns the
   exact quotient to `n`. The other branch performs integer `divisor+1`.
6. `Return(Name("factors"))` stores the reference, pops scope 1, restores
   environment/scope location, leaves the heap allocation alive, and returns
   `ref(0)`.

This ordering and footprint agree with both claims. There is no hidden output,
exception, or allocation in the used fragment. Argument evaluation is
left-to-right. Relevant priority rules are guard-disjoint or deliberately
preempt a generic route with the same semantics.

### Proof-local definitions

The three macro rules reproduce the translated step, body, and definition;
the fresh pinning claim checks the body macro against the literal submitted
module.

`factorLoop` and `factorDivisor` each have:

- a base rule for `N<=1`;
- a divisible rule for `N>1,D>0,pyMod(N,D)=0`;
- a non-divisible rule for `N>1,D>0,pyMod(N,D)!=0`.

The guards are pairwise disjoint and exhaustive on the claim domain. The
divisible equation appends exactly `D` and uses exact integer quotient
`N/D`; the other equation increments only `D`. `primeFactors` transparently
defines the initial state `factorLoop(N,2,.ValSeq)`. These are defined
mathematical summaries, not fresh values or unconstrained result-bearing
symbols.

The priority-40 `factorize-loop-lemma` is the only proof-local operational
bridge. It is textually the same complete configuration, guard, arbitrary
continuation, scope/heap framing, and result as the separately proved
`factorize-loop` claim. The first proof definition does not import this rule,
so the connection proof is not circular.

I also tested the bridge context:

- `evidence/continuation-probe-spec.k` puts an observable assignment
  `marker=9` immediately after the loop.
- Fixed semantics closed with `#Top` and exit 0
  (`evidence/26-continuation-probe-fixed.txt`).
- The lemma-enabled definition also closed with `#Top` and exit 0
  (`evidence/27-continuation-probe-lemma.txt`).

For body sensitivity, I changed the append argument to `divisor+1` in a
separate scratch tree (`evidence/verification-body-mutation.k`). A universal
mutated proof attempt timed out at 300 seconds
(`evidence/23-kprove-body-mutation.txt`); that timeout is **not** treated as
failure evidence. I therefore used the satisfiable ground loop witness
`N=2,D=2,VS=[]`. The mutated definition built/dry-ran successfully, executed
to heap `[3]`, and failed the original `[2]` obligation with
`WarnStuckClaimState`, exit 1
(`evidence/24-body-mutation-ground-dry-run.txt`,
`evidence/25-body-mutation-ground-proof.txt`). This is a valid concrete false
conclusion witness for the mutation and shows the bridge-free connection is
body-sensitive.

### Supplied opaque symbols and warnings

The fixed supplied semantics contains opaque float, sort, and MD5 symbols,
plus deliberately total/underspecified accessors. The complete ledger is in
`evidence/static-rule-dispositions.md`. None is reachable from this program,
from `factorLoop`/`factorDivisor`, from either target claim, or from the loop
lemma. They cannot influence control, the heap list, or the postcondition.

The LLVM compiler warned about non-exhaustive total equations for
`mapStrVS`, `joinCodes`, `floorFI`, `toF`, `ceilF`, and `valSeqAt`. No
submitted term invokes any of them. In supplied-semantics mode these remain
part of the fixed language boundary, not candidate proof extensions.

I found no candidate rule that enables a false conclusion on the intended
domain, so there is no unsound-rule allegation requiring a false witness.
Broad Python-subset behavior outside the submitted constructs is not used to
justify the theorem.

### Intent bridge

The K theorem proves equality with the recursive trial-division sequence. It
does not contain K predicates expressing “each element is prime,” “sequence
is nondecreasing,” or “product equals the original input.”

The ordinary mathematical bridge is credible: at an incremented divisor,
smaller divisors have already failed; if the first dividing candidate were
composite, one of its smaller prime factors would also divide the current
number, a contradiction. Thus each appended divisor is prime. Retaining the
divisor records multiplicity, incrementing only after non-divisibility
preserves order, and replacing `n` by `n/d` while appending `d` preserves
`product(accumulator) * n`. At `n=1`, the accumulator product is the original
input. This bridge is informal rather than machine-checked, which is the main
reason for `CONCERNS` rather than `PASS`.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust or reuse. I authored
`evidence/spec-vacuity.k`. It keeps the complete entry precondition and call
result but changes the heap obligation to append a spurious factor `2`:

```text
list(valSeqConcat(primeFactors(N), vCons(2,.ValSeq)))
```

This is demonstrably false for the satisfying input `N=1`: the real and
summarized result is `[]`, while the mutation requires `[2]`.

The mutated claim parsed and built successfully under `--dry-run`, exit 0
(`evidence/20-vacuity-dry-run.txt`). The actual proof then exited 1 with
`WarnStuckClaimState`. The residual explicitly contains:

```text
factorLoop(N,2,.ValSeq)
  #Equals
valSeqConcat(factorLoop(N,2,.ValSeq),vCons(2,.ValSeq))
```

and reports that the implication check failed
(`evidence/21-vacuity-proof.txt`). This is the expected unmet result
obligation, not a parser error, missing import, unrelated crash, unreachable
mutation, or timeout. The positive proof is non-vacuous and discriminating.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied K semantics, for every K integer `N>=1`, partial
correctness of the exact submitted `factorize` entry point is established:
whenever the call reaches its return, it returns `ref(0)` and heap location 0
contains exactly `factorLoop(N,2,.ValSeq)`. The proof also establishes the
universal loop summary for every `N>=1`, `D>=2`, initial `ValSeq`, matching
scope/heap, and arbitrary continuation. Allocation, call-frame restoration,
exception state, and return state are constrained as described above.

This is a partial-correctness theorem, not a machine-checked termination or
complexity theorem. Termination on positive integers has a simple informal
argument: between divisions, `D` increases no farther than the current `N`
before it divides; every division by `D>=2` strictly decreases `N`.

### Trust ledger

- **K toolchain/backends and K builtins.** Trusted: K v7.1.337, Haskell
  symbolic execution, LLVM concrete execution, integer/boolean/map/list/K
  equality hooks. Every target was rebuilt and rerun, but backend correctness
  is outside the theorem.
- **Trusted supplied semantics.** The exact mounted semantics tree is the
  fixed language model required by `SUPPLIED_SEMANTICS`. Relevant rules were
  statically checked and concretely exercised. Its Python subset and exception
  model, not full CPython, are the theorem’s operational boundary.
- **Trusted translator.** `/reference/py2mpy.py` is an authoritative input.
  Byte-identical regeneration connects `solution.py` to `solution.mpy`; the
  review does not prove the translator correct for all Python.
- **Proof-local summaries.** `factorLoop`, `factorDivisor`, and
  `primeFactors` are not assumed opaque primitives. They have ordinary guarded
  equations, and the bridge-free loop claim connects actual execution to
  them.
- **Promoted loop rule.** Not assumed: its exact universal connection claim
  independently produced `#Top` without the rule. Continuation and
  body-sensitivity evidence further checks its context and value effects.
- **Unused opaque symbols.** The float, sort, MD5, and underspecified total
  accessor symbols listed in stage 5 are fixed-semantics trust boundaries but
  have no dependent target claim and no result/control influence here.
- **Natural-language meaning of `primeFactors`.** Informally justified by the
  trial-division invariant above and empirically supported over 1125 inputs.
  It is not stated as a separate K theorem; this is acceptable for legitimacy
  but remains a documented adequacy concern.
- **Canonical differential bridge.** The canonical implementation is a
  trusted input and independent executable oracle. Differential evidence is
  finite and supports implementation-to-intent alignment only; it is not a
  substitute for either K claim.
- **Generation history.** Unavailable because the four requested records and
  structured trace are missing. No proof conclusion depends on their claims,
  but audit provenance is thinner.

### Excluded behavior

The formal theorem excludes `N<1`, non-integer Python inputs, full CPython
exception/resource behavior, and performance. It does not establish
termination within K or a machine-checked number-theory theorem connecting
the recursive output sequence to explicit prime/product/order predicates.

### Decision

Gate A (real-program soundness): **PASS**.  
Gate B (intent adequacy): **PASS with an informal summary-to-property
bridge**.  
Gate C (trust/evidence auditability): **PASS with concerns** because the
finite bridge is reproducible but generation metadata is absent.

The proof is sound, non-vacuous, result-constraining, and pinned to the real
generated program. The limitations warrant `CONCERNS`, not rejection.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
