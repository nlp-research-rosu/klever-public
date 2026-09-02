VALIDATED

## What is proven

This is a machine-checked partial-correctness proof under the supplied MPY
semantics.  For every finite MPY string whose character codes are only 40
(`(`) or 41 (`)`), the exact `correct_bracketing` definition translated from
`solution.py`, when loaded into the initial MPY configuration and called with
that string, returns:

```k
scanBrackets(CS, 0, true)
```

The theorem observes the returned Boolean and the complete final MPY
configuration: environment 0, the module binding for the exact closure, restored
scope allocator, empty heap, empty call stack, `noRet`, `NoExc`, and exit code
0.  Callee-local state is deallocated by the fixed function semantics.

`scanBrackets` has the following direct meaning.  `balance` starts at zero,
increases for `(`, and decreases for `)`.  `keepValid` permanently records
whether every processed prefix has nonnegative balance.  At the end,
`scanBrackets` is true exactly when that prefix property still holds and the
final balance is zero.  Thus each opening bracket is closed, no closing bracket
appears before its opening bracket, and nesting is proper.

## Formal claims

`SPEC.loop` is a universal loop theorem over symbolic remaining input `CS`,
symbolic balance `B`, and symbolic validity flag `V`.  Its precondition is
`bracketInput(CS)`.  It starts at the actual `#loop` representation with the
exact one-statement `Return(...) .Stmts` continuation and proves the returned
value and complete frame-pop transition.

`SPEC.correct-bracketing` loads the exact translated function body, performs
normal name lookup, argument evaluation, parameter binding, body execution,
return, and frame cleanup.  Its precondition is also `bracketInput(CS)`, and its
postcondition is the mathematical result above.

The three invariant obligations are discharged as follows:

1. Empty suffix: fixed semantics exits the loop and the return expression
   reduces to `V andBool B ==Int 0`, the base equation of `scanBrackets`.
2. Nonempty suffix: fixed semantics binds the next one-character string,
   executes the source branch and validity update, and returns to the same loop
   configuration over the strict tail.  The recursive equation is exactly that
   state transition.
3. Entry: fixed semantics loads and calls the exact closure.  After the first
   iteration establishes the `bracket` local, the proved loop theorem applies;
   empty input exits directly.

## Proof-extension inventory

### `scanBrackets`

- Class: definitional summary.
- Semantic role: names the mathematical result; it does not rewrite an MPY
  program term or replace execution.
- Domain and coverage: all finite `IntSeq`, all integer balances, and both
  Boolean flags.  `.IntSeq` and `iCons` are disjoint and exhaustive.  Recursive
  calls use the strict tail.
- Matched context and state footprint: none; it reads or changes no MPY cell.
- Value influence: its Boolean is the loop theorem and entry theorem result.
- Value justification: its base and step equations are the exact accumulator
  transition performed by `solution.py`.
- Dependents: `SPEC.loop`, `SPEC.correct-bracketing`, and `loop-lemma`.
- Validation: bridge-free universal loop proof, fixed/bridge comparisons, two
  opposite-value probes, and exhaustive differential testing through length 10.

### `keepValid`

- Class: definitional summary.
- Domain and coverage: every `Int` and `Bool`.  Guards `B <Int 0` and
  `B >=Int 0` are disjoint and exhaustive.
- Semantic role and state footprint: mathematical only; no operational term or
  state cell is replaced.
- Value influence: supplies the validity argument of `scanBrackets`.
- Value justification: it is exactly
  `if balance < 0: valid = False`, including persistence of an earlier false.
- Dependents: `scanBrackets` and both positive claims.

### `bracketInput`

- Class: definitional summary.
- Domain and coverage: total over finite `IntSeq`; true exactly when every code
  is 40 or 41.  The recursion strictly descends.
- Semantic role and state footprint: precondition only; no execution is
  replaced.
- Value influence: limits the theorem to the domain stated by `prompt.py`.
- Dependents: both claims and the operational lemma.

### Symbolic conditional simplification

```k
rule (#if C ==Int 40 #then _X:Int #else Y:Int #fi) => Y
  requires C =/=Int 40
  [simplification]
```

- Class: derived lemma.
- Domain: exactly `C =/=Int 40`; there is no equation outside that guard.
- Justification: the condition of the built-in conditional is false throughout
  the guard, so the result is its else branch.  It overlaps the built-in
  conditional equations consistently.
- Semantic role and state footprint: it simplifies only a summary expression;
  it does not rewrite the MPY source computation or any cell.
- Dependents: the close-bracket inductive branch of `SPEC.loop`.

### `SPEC.loop`

- Class: derived auxiliary reachability theorem.
- Semantic role: reasons about fixed execution.  It is proved against
  `VERIFICATION`, which contains no operational loop bridge.
- Domain: its complete configuration and `bracketInput(CS)`.
- State footprint: the theorem explicitly includes the active continuation,
  local bindings, caller/module scopes, environment, scope allocator, empty
  heap, heap allocator, exact stack frame, return state, exception state, and
  exit code.
- Dependents: it is the universal connection theorem for `loop-lemma`.

### `VERIFICATION-WITH-LOOP.loop-lemma`

- Class: operational bridge.
- Semantic role: accelerates the exact loop, return, and frame-pop execution
  already established by `SPEC.loop`.
- Domain and matched context: identical to the proved `SPEC.loop` left-hand
  side and guard.  In particular, it accepts only environment 1; exactly the
  three scopes at locations -1, 0, and 1; the four exact local bindings;
  scope location 2; empty heap at location 0; one stack frame with continuation
  `.K`, caller 0, and saved location 1; `noRet`; `NoExc`; exit code 0; and the
  exact `(Return(...) .Stmts) ~> #endcall` suffix.  Priority 40 only preempts
  fixed execution inside this already proved domain.
- Justification scope and containment: the bridge-free `SPEC.loop` theorem is
  textually the same complete configuration and guard.  Therefore every bridge
  match is in the theorem's domain; no continuation or cell is framed more
  broadly.
- State footprint: produces the proved Boolean, restores environment and scope
  allocator, removes the callee scope and stack frame, and preserves the
  arbitrary builtins scope and module map.  Empty heap, heap allocator, return,
  exception, and exit-code cells are preserved.
- Value influence: its `scanBrackets` value is the result of the entry claim.
- Value justification: the bridge-free universal `SPEC.loop` proof printed
  `#Top`.
- Control validation: `bridge_context_tests.py` inserts an observable
  `valid = False` continuation.  The narrowed bridge does not match, and fixed
  and bridge-enabled runs produce byte-identical complete configurations with
  `context_result |-> false`.
- Operational sensitivity: changing the displaced opening update from `+1` to
  `+2` makes the bridge-free connection theorem fail with the residual
  `scanBrackets(R, B +Int 2, V)`.
- Value validation: fixed and bridge-enabled executions agree for true and
  false ground results.  The false pair result and true unmatched-open result
  mutations are both rejected.

## Commands and actual outputs

The complete reproducible run is:

```bash
./prove.sh
```

It exited 0.  The script contains the exact compile, execution, proof, and
mutation commands.  The required positive proof commands were:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop
# Output: #Top
# Exit: 0

kprove spec.k \
  --definition verification-with-loop-kompiled \
  --spec-module SPEC \
  --claims SPEC.correct-bracketing
# Output: #Top
# Exit: 0
```

The clean run also reported:

```text
checked=2047 mismatches=0
"case_empty" -> true
"case_open" -> false
"case_pair" -> true
"case_nested" -> true
"case_bad_prefix" -> false
```

The validation probes were:

```bash
kprove spec-vacuity.k \
  --definition verification-with-loop-kompiled \
  --spec-module SPEC-VACUITY
# Exit: 1 (expected)
# Residual result: true; deliberately requested result: false

kprove spec-value-mutation.k \
  --definition verification-with-loop-kompiled \
  --spec-module SPEC-VALUE-MUTATION
# Exit: 1 (expected)
# Residual result: false; deliberately requested result: true

kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
# Exit: 1 (expected)
# Residual exposes B +Int 2 versus the proved B +Int 1 transition
```

The LLVM build used the required modules:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

The symbolic definitions used the Haskell backend and imported `MPY` without
changing `reference-semantics/`.

## Gate results

### Gate A — PASS

- A1: the exact translated program-defined body executes under fixed semantics.
  `solution.mpy` is checked against fresh translator output.  The loop bridge
  has a bridge-free universal connection theorem.  The `+2` body mutation is
  rejected with exit 1.
- A2: the auxiliary theorem and bridge enumerate the complete state footprint,
  including result, frame removal, environment, stack, scopes, heap, return,
  exception, and exit-code state.
- A3: binding, iteration, branch evaluation, exact continuation, and return/pop
  control are included.  The continuation mutation is outside the bridge match,
  and fixed/extended complete states agree.
- A4: all total functions have disjoint/exhaustive constructors or guards and
  strict recursive descent.  The guarded simplification equation is true on
  its full domain.
- A5: `()` is a realizable input.  Mutating its true result to false is rejected
  with a stuck `true` residual.  The opposite false-to-true bridge probe is also
  rejected.

### Gate B — PASS

- B1: the formal domain is exactly strings containing only `(` and `)`, as
  stated by the prompt.  There is no hidden length or balance restriction.
- B2: these characters are ASCII, so the supplied semantics' ASCII string model
  agrees with the relevant Python behavior.  K integers and Python integers are
  unbounded for all arithmetic used here.  No exceptional operation occurs in
  the formal domain.
- B3: the summary recurrence directly establishes the prefix-balance
  characterization of correct bracketing; it is not merely an opaque execution
  summary.
- B4: the implementation follows that characterization and all prompt examples
  execute as specified.

### Gate C — PASS

- C1: the trust ledger below names all components outside the theorem.
- C2: every claimed proof, mutation, concrete comparison, and differential test
  has an artifact and exact command in `prove.sh`.
- C3: formal results, finite evidence, trust, and exclusions are separated
  here.  Finite tests are not presented as universal proofs.

## Trust boundary

- The supplied, unmodified MPY reference semantics is trusted as the execution
  model.  This proof does not establish that the reference semantics is a
  complete formalization of CPython.
- `py2mpy.py` is supplied and unmodified.  `prove.sh` regenerates the term and
  requires byte equality with `solution.mpy`; the theorem also spells the exact
  translated body.
- K v7.1.293, its Haskell/LLVM backends, SMT reasoning, and their runtime are
  trusted.
- The proof-local equations are part of the checked theory, not external
  primitives.  Gate A audits their coverage and truth.  The only operational
  extension is justified by the independently checked bridge-free theorem.

No opaque value, external function, program-defined helper, or unproved
result-bearing oracle is used.

## Empirical evidence

- `differential_test.py` compares `solution.py` with an independently written
  stack oracle for every bracket string of lengths 0 through 10: 2,047 inputs,
  zero mismatches.
- `concrete_tests.py` is AST-checked to contain the same target function body as
  `solution.py`, then executed by the required LLVM semantics on the empty
  string, one unmatched opening, a pair, a nested example, and a bad prefix.
- `bridge_context_tests.py` is executed under both the fixed LLVM definition and
  the bridge-enabled Haskell definition.  Complete printed configurations are
  required to be identical.

These finite checks support implementation/intent and operational evidence;
they do not replace either universal `kprove` command.

## Excluded behavior

- Inputs containing characters other than `(` and `)` are outside both the
  prompt contract and `bracketInput`.
- The theorem is about the supplied MPY semantics, not arbitrary CPython
  features, Unicode behavior outside this ASCII domain, or changed global
  bindings.
- Following the Kit contract, the formal report is partial correctness; a
  separate liveness theorem is not claimed.  The concrete implementation and
  recursive summary both structurally consume finite input, but that observation
  is not reported as a K termination proof.
