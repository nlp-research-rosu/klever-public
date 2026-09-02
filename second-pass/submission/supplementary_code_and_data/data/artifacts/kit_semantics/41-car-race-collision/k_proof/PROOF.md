VALIDATED

## What is proven

Under the supplied `MPY` semantics, for every symbolic K integer `N`, loading
the exact translated definition

```python
def car_race_collision(n: int):
    return n * n
```

and calling `car_race_collision(N)` reaches the result `N *Int N`.
The reachability claim also requires the call to restore `env`, `scopeLoc`,
`heap`, `heapLoc`, `stack`, and `ret`, to leave `exc` as `NoExc` and the exit
code as `0`, and to retain only the expected loaded function binding in the
module scope. This is a partial-correctness result in the Kit sense.

## Formal claim

`spec.k` contains one positive target claim, `SPEC.car-race-collision`. Its
left-hand side includes the complete `Module(FuncDef(...))` term emitted in
`solution.mpy`, followed by a call with `Int(N:Int)`. Its right-hand side is
`N *Int N`; there is no `requires` clause, so the formal domain is every K
`Int`.

Program boundary: exact module load, name lookup, argument evaluation,
parameter binding, translated function body, multiplication, return, and frame
pop.

Observable final state: the returned integer and every cell in the supplied
MPY configuration.

Intended property: for a meaningful car count `n >= 0`, every one of the `n`
left-to-right cars meets every one of the `n` right-to-left cars exactly once,
so there are `n * n` cross-direction collisions.

## Proof-extension inventory

There are no proof extensions.

- `verification.k` only requires the supplied semantics and imports `MPY`.
- It declares no syntax, function, equation, simplification rule, rewrite,
  priority rule, opaque term, operational bridge, lemma, or trusted claim.
- `spec.k` contains only the positive target claim.
- The two mutation claims are separate expected-failure audit artifacts and
  are not imported by the positive proof.

Consequently, the extension contract has no definitional summaries, derived
lemmas, operational bridges, or trusted primitives to classify. All
program-defined code executes through the fixed semantics.

## Exact commands and actual outputs

The executable record is `prove.sh`. The final complete run was:

```bash
./prove.sh
```

Actual final script result: exit `0`.

Identity and translation checks:

```text
function_ast_equal: True
translated_program_in_spec: True
```

Concrete LLVM build and execution:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-smoke.mpy --definition runtime-kompiled
```

Actual results: both exited `0`; `krun` finished with `<k> .K </k>`,
`<exc> NoExc </exc>`, and `<exit-code> 0 </exit-code>`.

Positive symbolic build and target proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results: compilation exited `0`; `kprove` printed `#Top` and exited `0`.
This is the only required positive target-proof command.

False-postcondition probe:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1`, `WarnStuckClaimState`, with the failed implication
`N *Int N +Int 1 #Equals N *Int N`. `prove.sh` reported
`EXPECTED FAILURE: false-postcondition mutation`.

Body-sensitivity probe:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1`, `WarnStuckClaimState`, with the failed implication
`N +Int N #Equals N *Int N`. `prove.sh` reported
`EXPECTED FAILURE: changed-body mutation`.

Tool versions:

```text
kompile/krun/kprove: K v7.1.293 (build 2025-10-03)
python3: Python 3.10.12
```

Relevant SHA-256 identities at validation time:

```text
d4a9a6f17e6f65f8fa63bffa89d863ca691859fab85fff3f60f378d9340cc489  prompt.py
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16  py2mpy.py
b0c65c90f2f255fcbae2bf1a4ef2dfb91ded7bbbc5e93a3d15bd7e33ee8d16ed  solution.py
8878b8488943a7fc31808899d00a3cbf433c48b524f0f1515c79f92c10e6e659  solution.mpy
ef48556fde781a8ca6e4e1986b701ccdf330897621c6658bd831ff4c17516ab4  verification.k
05893b02e1120b09047a560972c890beebb77d8491aaabed0d5918c172bad952  spec.k
57e8f9f3178639bbb87f95e5cc596bbaa91a6463f965b1965911eff9a0269f97  reference-semantics/semantics.k
```

The compilers also emitted pre-existing warnings in unused portions of the
supplied semantics: LLVM reported several non-exhaustive helper matches and
unused string-rule variables; Haskell reported the unused string-rule
variables. No warning concerns function calls, integer multiplication, or this
claim, and neither build failed.

## Gate results

### Gate A — PASS

- A1: The claim contains the exact regenerated `solution.mpy` module term.
  `prove.sh` checks this mechanically. The fixed `FuncDef`, call, lookup,
  binding, body, and return rules execute. Changing `*` to `+` makes the proof
  fail with `N +Int N #Equals N *Int N`.
- A2: No execution is skipped. The claim constrains every MPY state cell and
  the expected module-scope update.
- A3: Binding, left-to-right argument evaluation, control transfer, return, and
  frame restoration use only fixed semantics. There is no bridge or opaque
  result-bearing abstraction.
- A4: The proof adds no equations or rules, so there are no proof-local
  coverage, overlap, descent, or consistency obligations.
- A5: `n = 3` is a realizable concrete witness and returns `9`; the six-case
  smoke run terminates cleanly. The `+1` postcondition mutation is rejected
  with exit `1`.

### Gate B — PASS

- B1: The formal domain is every K integer. The prompt's meaningful physical
  domain is non-negative integer car counts; the theorem is stronger as an
  implementation equation and imposes no hidden restriction.
- B2: K `Int` and CPython integers are unbounded mathematical integers for the
  multiplication used here. Non-integer Python arguments and Python's
  dynamically unenforced annotation are outside the formal domain.
- B3: The K theorem proves the implementation returns `n * n`. The
  summary-to-property bridge is the direct pair-counting argument: there are
  `n` choices from each direction, and unchanged opposite trajectories make
  each pair collide exactly once.
- B4: The implementation and prompt agree on every meaningful `n >= 0`.

### Gate C — PASS

- C1: The trust ledger below names the complete boundary; there are no hidden
  proof-local assumptions.
- C2: `prove.sh`, `concrete-smoke.py`, `concrete-smoke.mpy`,
  `spec-vacuity.k`, and `spec-body-mutation.k` are present and reproduce the
  positive proof, concrete evidence, and both negative probes.
- C3: Formal proof, finite evidence, intended-model reasoning, and exclusions
  are separated here. `#Top` is reported only as target-proof execution, not
  as the reason for the `VALIDATED` headline.

## Trust boundary

- The user-supplied `reference-semantics/` definition is the fixed language
  model. Its function-call, integer, operator, and core rules affect the target
  claim. Evidence: successful LLVM execution and bridge-free Haskell proof.
- K v7.1.293, its Haskell/LLVM backends, and the underlying solver are trusted
  to implement K reachability correctly.
- CPython 3.10's AST and the fixed `py2mpy.py` translator are trusted for the
  source-to-constructor mapping. Evidence: regeneration plus the exact
  translated-term containment check in `prove.sh`.
- The physical reading of the prompt assumes the stated infinite straight
  road, equal constant speeds, initially separated direction groups, and
  collision-transparent trajectories. Pair counting connects that model to
  `n * n`; this modeling argument is not itself encoded as K dynamics.

## Empirically supported facts

`concrete-smoke.py` uses an AST-identical copy of the solution function and
checks inputs `-4, 0, 1, 2, 3, 10` against independently written expected
constants. It exited `0` under CPython. Its translated MPY program also exited
`0` under `krun`, with no exception. These are finite smoke tests; the universal
integer result comes from `kprove`, not from the samples.

## Excluded behavior

- Non-integer arguments, Python coercions, and enforcement of type annotations.
- A physical interpretation for negative `n`; the implementation equation is
  nevertheless proved for negative K integers.
- Alternate collision physics, finite roads, unequal or changing speeds, car
  destruction, or trajectory changes.
- An independent proof of the supplied semantics, translator, K
  implementation, solver, or total-correctness/liveness beyond the stated
  reachability result.
