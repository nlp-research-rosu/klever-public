VALIDATED

# What is proven

Under the supplied `reference-semantics/` definition, each of the 1,000
permitted integer inputs reaches a final configuration in which
`int_to_mini_roman` returns the canonical lowercase Roman numeral for that
input. This is a partial-correctness result in the Kit sense.

The proof covers exactly the prompt domain `1 <= number <= 1000`. The prompt
examples are included:

- `19 -> "xix"`
- `152 -> "clii"`
- `426 -> "cdxxvi"`

# Formal claim

`spec.k` contains one ground reachability claim for every integer from 1
through 1000. Claim `roman-NNNN`:

1. starts from the complete initial MPY configuration;
2. loads the exact translated function definition;
3. calls it with the claim's ground integer and assigns the value to
   `__result`; and
4. requires `.K`, the canonical ground string, and the expected final values
   of every semantics cell.

The module scope is closed: it contains only the loaded closure and
`__result`. The environment, scope allocator, heap, heap allocator, call
stack, return state, exception state, and exit code are all constrained.

The expected strings are the exhaustive expansion of the conventional
subtractive Roman token sequence:

```text
1000:m, 900:cm, 500:d, 400:cd, 100:c, 90:xc, 50:l,
40:xl, 10:x, 9:ix, 5:v, 4:iv, 1:i
```

# Proof-extension inventory

The inventory was rebuilt from `verification.k` and `spec.k` after the
positive proofs. There are no proof-local runtime functions, totality
declarations, simplification lemmas, concrete rules, priority rules, opaque
values, operational bridges, or auxiliary circularities.

## `intToMiniRomanBody`

- Extension/class: parse-time macro; definitional syntactic summary.
- Semantic role: names the translated `Stmts`; it does not rewrite an active
  configuration or replace execution.
- Domain and matched context: the single macro token in a `Stmts` parse
  position; no continuation, stack, binding, or cell is matched.
- Justification scope: the exact `FuncDef` body in `solution.mpy`.
- Context containment: macro expansion is completed before operational
  semantics begin.
- State footprint: none at macro-expansion time. The expanded body is executed
  by the fixed semantics and may read/write only through those fixed rules.
- Value/control influence: indirect, because it selects the body subsequently
  executed. `validate_artifacts.py` structurally compares the macro expansion
  with the fresh `py2mpy.py` translation.
- Dependents: `solutionCall`, `solutionModule`, and all 1,000 target claims.
- Validation: current identity check exits 0; the material body mutation in
  `solution_mutant.py` exits 1 before proof execution.

## `solutionModule`

- Extension/class: parse-time macro; definitional syntactic summary.
- Semantic role: names `Module(FuncDef(...))`; it does not replace execution.
- Domain/context: one `Module` parse position; no operational context or cells.
- State footprint and value influence: none at macro-expansion time.
- Justification: exact function name, parameter, and `intToMiniRomanBody`.
- Dependents: no target claim (the macro is retained as an identity aid).
- Validation: checked structurally by `validate_artifacts.py`.

## `solutionCall(N)`

- Extension/class: parse-time macro; definitional verification harness.
- Semantic role: expands to the exact function definition followed by
  `Assign(Name("__result"), Call(Name("int_to_mini_roman"), Int(N)))`.
- Domain: any K `Int`; target use is restricted to ground values 1 through
  1000.
- Matched context: one `Module` parse position; there is no active
  continuation, call stack, binding, or framed cell during expansion.
- Justification scope/context containment: exact expansion checked by
  `validate_artifacts.py`; afterward fixed rules perform module load, binding,
  callee lookup, argument evaluation, frame handling, body execution, return,
  pop, and assignment.
- State footprint: the macro itself has none. Each target claim constrains all
  cells affected or preserved by the expanded program.
- Value influence: `__result` is the observed return value and is independently
  fixed to a ground expected string in each claim.
- Dependents: all 1,000 target claims.
- Control/value validation: no bridge comparison is applicable because no
  execution is skipped. Exact-body validation, fixed-semantics execution,
  exhaustive target claims, concrete runs, and the rejected mutations supply
  the evidence.

# Commands and actual results

The executable record is `prove.sh`. It regenerates the translation, validates
artifact identity, builds both definitions, runs concrete MPY examples, runs
all positive target proofs sequentially, and performs the two negative probes.

Core build commands:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 validate_artifacts.py

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

All commands above exited 0. `krun` ended with `.K` and exit code 0. Its module
scope contained:

```text
boundary_1    = i
boundary_1000 = m
sample_19     = xix
sample_152    = clii
sample_426    = cdxxvi
```

The positive target command is instantiated by `run_positive_batch` in
`prove.sh`:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims "$labels"
```

The exact batch invocations and actual results were:

| Invocation | Claim range | Output | Exit |
|---|---:|---:|---:|
| `run_positive_batch 01 1 100` | `roman-0001`–`roman-0100` | `#Top` | 0 |
| `run_positive_batch 02 101 200` | `roman-0101`–`roman-0200` | `#Top` | 0 |
| `run_positive_batch 03 201 300` | `roman-0201`–`roman-0300` | `#Top` | 0 |
| `run_positive_batch 04 301 400` | `roman-0301`–`roman-0400` | `#Top` | 0 |
| `run_positive_batch 05 401 500` | `roman-0401`–`roman-0500` | `#Top` | 0 |
| `run_positive_batch 06 501 600` | `roman-0501`–`roman-0600` | `#Top` | 0 |
| `run_positive_batch 07 601 700` | `roman-0601`–`roman-0700` | `#Top` | 0 |
| `run_positive_batch 08 701 800` | `roman-0701`–`roman-0800` | `#Top` | 0 |
| `run_positive_batch 09 801 900` | `roman-0801`–`roman-0900` | `#Top` | 0 |
| `run_positive_batch 10 901 1000` | `roman-0901`–`roman-1000` | `#Top` | 0 |

The ten `.exit` artifacts in `proof-logs/` all contain `0`; each corresponding
log contains exactly one `#Top`. A post-rebuild focused command also confirmed
the current definition:

```bash
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims SPEC.roman-1000
# Output: #Top
# Exit: 0
```

Artifact/differential validation:

```bash
python3 validate_artifacts.py
```

Actual output, exit 0:

```text
PASS: source translation equals solution.mpy
PASS: verification macros contain the exact translated body and harness
PASS: spec.k contains canonical claims for exactly 1..1000
PASS: CPython exhaustive differential has 0 mismatches over 1..1000
PASS: prompt examples 19, 152, and 426
```

Body-sensitivity probe:

```bash
python3 validate_artifacts.py --solution solution_mutant.py
```

Actual output and status:

```text
FAIL: solution_mutant.py does not transliterate to committed solution.mpy
Exit: 1 (expected)
```

The mutation changes the result at 1000 from `"m"` to `"x"`.

False-postcondition probe:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result:

```text
WarnStuckClaimState
Exit: 1 (expected)
```

The satisfiable witness is input 19; the mutation requires `"xviii"` instead
of the proved `"xix"`.

# Gate results

## Gate A — PASS

- A1: the exact source translation is loaded and executed. No program-defined
  operation is summarized by a runtime rule. The body mutation is rejected.
- A2: there is no operational bridge. Every configuration cell is constrained
  before and after each target computation.
- A3: fixed semantics performs function binding, lookup, argument evaluation,
  tuple construction/indexing, arithmetic, concatenation, return, frame pop,
  and result assignment. No continuation or binding is abstracted.
- A4: there are no proof-local equations or runtime rewrites to create
  overlap, false guards, nontermination, or inconsistency. The three macros are
  exact parse-time aliases.
- A5: every pre-state is concrete and realizable. All 1,000 results are
  constrained, and the false result for input 19 is rejected with a stuck
  claim.

## Gate B — PASS

- B1: the formal domain is exactly the prompt restriction, with no hidden
  strengthening or omitted allowed integer.
- B2: the relevant MPY model uses integers and ASCII code sequences. All
  indices are in bounds on this domain; lowercase Roman characters are ASCII.
  No material Python/K mismatch affects these executions.
- B3: the 1,000 literal postconditions are checked against the documented
  canonical subtractive token oracle. This is not an opaque execution summary:
  each literal is directly compared with fixed program execution.
- B4: the implementation agrees with the prompt contract and all examples.

## Gate C — PASS

- Every positive proof has an existing log and exit artifact.
- Both mutation probes have existing logs, commands, and exit artifacts.
- `validate_artifacts.py` independently checks translation identity, macro
  identity, exact finite-domain claim coverage, the canonical oracle, all 1,000
  CPython results, and the prompt examples.
- `concrete_tests.py`, `concrete_tests.mpy`, and `proof-logs/krun.log` record
  concrete LLVM execution.
- Formal proof, conventional intent mapping, empirical checks, and trust
  assumptions are reported separately.

# Trust boundary

- The supplied `reference-semantics/` files are trusted as the intended MPY
  execution model. All target claims depend on them.
- `py2mpy.py` is the supplied trusted frontend. Its emitted term is checked
  byte-for-byte against `solution.mpy`; the frontend's faithfulness to CPython
  AST meaning remains outside the K theorem.
- K v7.1.293, its Haskell/LLVM backends, Z3, and their runtime libraries are in
  the proof-tool trusted computing base.
- The conventional Roman token table above is the intent bridge from literal
  strings to the phrase “Roman numeral equivalent.” It affects Gate B, not
  operational proof soundness.
- There are no task-added trusted primitives, opaque values, or unproved
  operational bridges.

# Empirically supported facts

- CPython execution agrees with an independently written greedy-token oracle
  on every allowed integer, with zero mismatches.
- LLVM `krun` concretely reaches `.K` with exit code 0 for both boundaries and
  all three prompt examples.
- The empirical checks support frontend/model adequacy. They are not used in
  place of the K reachability proofs.

# Excluded behavior

- Inputs outside `1..1000`, non-integer arguments, Python exceptions for such
  inputs, Unicode beyond the ASCII Roman alphabet, concurrency, I/O, and
  external state are outside the theorem.
- This report does not claim correctness of the supplied semantics, translator,
  K implementation, or solver.
- The Kit result is partial correctness; no separate general liveness theorem
  is claimed.
