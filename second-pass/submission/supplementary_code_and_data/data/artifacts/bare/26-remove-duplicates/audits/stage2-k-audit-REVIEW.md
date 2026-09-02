# Independent adversarial review: 26-remove-duplicates

The candidate contains a legitimate partial-correctness proof of the submitted
generated program. I rebuilt both definitions from source, reran both positive
proof stages, checked the generated semantics concretely, mechanically pinned
the entry claim to the trusted-regenerated program term, reviewed every local K
declaration and rule, and rejected an independently written false result
mutation.

Kit gate summary:

| Gate | Result | Basis |
|---|---|---|
| A — real-program soundness | PASS | Exact program pinning, sound local rules, separately proved iterator lemma, continuation witness, body sensitivity, and a rejecting false-postcondition mutation |
| B — intent adequacy | PASS | Unrestricted finite lists of mathematical integers; stable removal of every value with multiplicity greater than one |
| C — trust/evidence auditability | PASS | Fresh logs, scripts, source inventory, explicit trust ledger, and bounded empirical checks |

## 1. Input and provenance integrity

### Declared layout and mounts

`/audit-input.json` declares:

- problem `26-remove-duplicates`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- no mounted reference-semantics tree.

The trusted `/reference/reference-semantics` tree is absent, as required for
this mode. I did not infer or seek a hidden semantics.

All records required by `legacy-selected-stage1` are present, readable,
regular, and non-symlinked:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, and the present
  `usage.json`;
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one-file structured trace under
  `/generation-evidence/codex-trace/2026/07/22/`.

The campaign object in `/audit-input.json` equals
`/audit-campaign-lock.json` exactly. Its independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the recorded lock hash.

Every recorded individual-file hash checked in `audit-input.json` matches the
mounted bytes: the canonical implementation, trusted and candidate prompts,
trusted and candidate translators, run/task/result manifests, generation
invocation and metrics, usage, prompt, last message, and output log. Every
generation-evidence file hash declared by `generation-result.json`, including
the JSONL trace, also matches.

The candidate contains eight regular files and no directories, links, device
nodes, or other unsupported entries. The trace contains three regular
directories and one regular JSONL file, with no links or unsupported entries.
The pipeline's length-delimited tree digest independently recomputes to
`ff6e6d4139746883e23e50bba9499a63e85fa1e851622be9c68a3ea9e87aa3c6`
for `/candidate`, exactly the `workspace_sha256` recorded by both
`generation-result.json` and `invocation.json`. The same digest recomputes to
`ce37f7eed2567b4c3fe4f80b3556ab03d4ca705c6b52b155edcec486f69ee151`
for the trace, exactly its `usage.json` `source_trace_sha256`.
`audit-input.json` also carries separately produced aggregate-tree values
whose canonicalization is not recorded there; I did not compare those numbers
as though they used the pipeline digest. The constituent hashes and the
generation-record tree digests pin the mounted bytes without a contradiction.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
mounted versions. Their hashes are respectively
`7823eea9be9599563c786fa16e792f3da2482016607d75ee06ca40b2d33c7dca`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

I parsed every one of the structured trace's 254 JSONL records, read all
613,880 decoded characters of `codex-output.log`, and inspected all other
generation records. They are treated only as historical claims. The trace
shows the author introduced `[concrete]` count rules to obtain symbolic proof
closure and ultimately claimed two `#Top` runs; this history did not substitute
for any fresh audit result.

Evidence:

- `evidence/integrity_check.py`
- `evidence/01-integrity.log`
- `evidence/01-copy.log`
- `evidence/01-copy-reference.log`

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For a list of integers, return the elements whose total multiplicity in the
original list is exactly one, retaining their original relative order. Thus
every occurrence of a value appearing twice or more is removed. The documented
example maps `[1,2,3,2,4]` to `[1,3,4]`.

The trusted canonical implementation builds a `collections.Counter` and keeps
an element when its count is at most one. Because the comprehension iterates
only over elements already in the input, their counts are at least one, so
`<= 1` is equivalent to `== 1`.

### Candidate implementation

`/candidate/solution.py` is:

```python
def remove_duplicates(numbers: List[int]) -> List[int]:
    return [number for number in numbers if numbers.count(number) == 1]
```

It is a different but contract-equivalent algorithm on the intended
`List[int]` domain. It preserves order and does not mutate the input.

I regenerated the translated term with the trusted translator:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
cmp /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
```

`cmp` exited 0. Both files have SHA-256
`c745517cfe05839db8c2e7141662dd5e1e362a2c688f1a6a1857526d13cd3833`.

The independent differential script imports the trusted canonical entry point
and the candidate entry point from explicit scratch paths. It checks:

- 12 documented, empty, singleton, all-unique, duplicate, triplicate,
  interleaved, negative, and very-large-integer boundary cases;
- every list of length 0 through 6 over `{-2,-1,0,1,2}`;
- 1,000 deterministic lists of length 0 through 40 over integers `[-20,20]`.

All 20,543 comparisons agreed; mismatch count was zero. These finite tests
support source fidelity but are not used as the universal K proof.

Evidence:

- `evidence/differential_test.py`
- `evidence/02-differential.log`
- `evidence/02-regenerate-mpy.log`

## 3. Clean proof reconstruction

I copied only the eight candidate source artifacts to
`/tmp/audit-work/candidate-src` and then copied only the five build inputs
needed by K into `/tmp/audit-work/rebuild`. No candidate kompiled definition or
cache exists in `/candidate`, and none was reused.

The observed toolchain is K `v7.1.293` for `kompile`, `kprove`, and `krun`,
matching the campaign lock.

### Generated semantics build and execution

Fresh command:

```text
kompile semantic.k --backend haskell \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition semantic-kompiled
```

It exited 0. Nine independently scripted `krun` executions covered empty,
singleton, all-unique, duplicate, triplicate, mixed negative, interleaved, and
very-large-integer inputs. Every execution exited 0, consumed `<k>` to `.K`,
and matched both Python implementations. Examples include:

- `[] -> []`;
- `[1,1] -> []`;
- `[1,2,3,2,4] -> [1,3,4]`;
- `[-1,0,-1,2] -> [0,2]`;
- a 31-digit positive/negative case -> the two unique values.

Evidence: `evidence/03-kompile-semantic.log`,
`evidence/concrete_semantics_compare.py`, and
`evidence/03-concrete-compare.log`.

### Proof-definition build and positive claims

Fresh command:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0.

Both candidate positive proof stages then reconstructed:

| Positive target | Exact relevant command | Exit | Output |
|---|---|---:|---|
| General iterator lemma | `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims walk-correct` | 0 | `#Top` |
| End-to-end theorem, using the separately proved lemma | `kprove spec.k --definition verification-kompiled --spec-module SPEC --trusted walk-correct` | 0 | `#Top` |

The second command loads both claims, marks only `walk-correct` trusted, and
proves the remaining `program-correct` claim. This is sound composition because
the first command independently proved the exact same lemma.

For diagnosis I also tried selecting only `program-correct` while naming
`walk-correct` trusted. K's claim filter then omitted the lemma from the loaded
set and produced a genuine stuck residual. That command is not the candidate's
positive target and does not undermine the exact successful compositional run;
it is preserved at `evidence/03-kprove-program-correct.log` to avoid concealing
the distinction.

Evidence:

- `evidence/03-kompile-verification.log`
- `evidence/03-kprove-walk-correct.log`
- `evidence/03-kprove-compositional-exact.log`

Clean reconstruction passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`walk-correct` has no explicit `requires`. For arbitrary finite integer lists
`INPUT`, `ORIGINAL`, and `SUFFIX`, and an arbitrary continuation `KREST`, it
starts from the exact comprehension iterator for the submitted expression and
captured `numbers = ORIGINAL` binding. It reaches that same `KREST`, preserving
the omitted configuration cells, and changes output from `SUFFIX` to the
stable-filter result for `INPUT` prepended onto `SUFFIX`.

`program-correct` also has no explicit `requires`; its sort is its domain
restriction. For arbitrary `INPUT:Ints`, it starts in the generated initial
configuration with:

- the complete module term;
- input `listValue(INPUT)`;
- `noFunction`, `emptyEnv`, and empty output.

It consumes the module to `.K`, registers the exact closure, binds `numbers` to
the input, and returns
`listValue(removeRepeated(INPUT, INPUT))`.

`removeRepeated` structurally traverses the original order and keeps an integer
iff `count(integer, ORIGINAL) == 1`. The return is therefore constrained to the
intended stable filter; it is neither a fresh existential nor an implication
that could ignore the actual result.

### Constructor-level program identity

`evidence/program_term_compare.py` extracts the `Module(...)` term directly
from the entry claim, parses it and `solution.mpy` with the fresh generated
definition, and compares their JSON KASTs. The only normalization is the
surface spelling of the empty generated string list:
`FreeVars(.Strings)` to `FreeVars()`. Both parse to SHA-256
`d16fb448d2a0ef6937c5e52e6cbc88d0bc45c57acfa59bfaa00b8ebe15852fba`;
the constructor ASTs are identical.

Thus the claim executes the trusted-regenerated submitted function binding and
body. It does not prove a substituted program.

### Satisfying states and concrete substitution

Every finite constructor `Ints` value satisfies the entry domain. In
particular, the generated initial state with
`INPUT = (1,2,3,2,4)` is realizable. A separate concrete K reachability claim
executes the exact module from that state and requires the literal final output
`listValue(1,3,4)`; it builds and proves with `#Top`. Both Python
implementations also return `[1,3,4]`.

Evidence:

- `evidence/04-program-term-compare.log`
- `evidence/spec-concrete-witness.k`
- `evidence/04-concrete-post-witness.log`

There is no automatic source-to-claim generator, which is an artifact
maintenance observation only. Identity of this immutable candidate is
mechanically established.

### Body sensitivity

`evidence/spec-body-mutation.k` changes both occurrences of the executed
program body predicate from `count == 1` to `count == 2`, while retaining the
original expected result `[7]` for the satisfying input `[7]`. Its dry run exits
0. Its proof exits 1 with `WarnStuckClaimState`; execution reaches `.K` with
empty output rather than `[7]`. This changes the actual claim term, not merely
an external source file, and establishes theorem sensitivity to the body.

## 5. Rule-by-rule static soundness review

The complete numbered source and machine-extracted declaration inventory are
in `evidence/05-static-source-inventory.log`. There are no generated helper K
files beyond `semantic.k`, `verification.k`, and `spec.k`.

### Local syntax and configuration inventory

`MPY-SYNTAX` declares every local source constructor:

- `Pgm`: `Module(Stmts)`;
- `Stmts`: juxtaposition-separated `Stmt` list;
- `Stmt`: `ImportFrom`, two `FuncDef` shapes, and `Return`;
- `Strings`, `Params`, `CellVars`, and `FreeVars`;
- `Exprs`;
- `Expr`: `Name`, `Int`, `Attribute`, `Call`, `Compare`, and `ListComp`;
- `CmpOps`, `CmpOp`, `CompFors`, and `CompFor`.

`MPY` declares:

- integer list `Ints`;
- `PyVal`: `intValue`, `boolValue`, and `listValue`;
- `Env`: `emptyEnv` and `bind`;
- `Function`: `noFunction` and `closure`;
- control terms `execModule`, `startEntry`, `execFunction`, `walkComp`, and
  `emitComputed`;
- function symbols `ifCons`, `eval`, `asInt`, `asInts`, `asBool`, `count`,
  `collect`, and `prependIf`.

`VERIFICATION` adds the function symbols `removeRepeated` and
`removeRepeatedOnto`.

The sole configuration has `<k>`, `<input>`, `<function>`, `<env>`, and
`<output>` cells. Every cell is read or written by submitted-program execution:
`input` supplies the argument, `function` stores the closure, `env` stores the
binding, `output` accumulates the result, and `k` carries control. No heap,
allocation, I/O, or exception cell is required by this immutable, pure,
integer-list program.

The only local attributes are `[function]` on the ten named functions and
`[concrete]` on the three `count` equations. There are no `[total]`,
`[functional]`, `[simplification]`, priority, `owise`, macro, opaque, or
proof-local ordinary operational rules.

### Operational rules

| Lines | Rules | Review |
|---|---|---|
| `semantic.k:62-65` | Enter module, handle empty/cons statement sequence, ignore translated typing import | Sequential control is preserved. Ignoring `typing.List` is inert because the translator erased annotations and the imported value is never used. |
| `semantic.k:67-70` | Register either supported exact `remove_duplicates` definition shape when no function exists | Selects the submitted binding and stores its real body. The candidate has exactly one matching definition and one parameter. |
| `semantic.k:73-76` | Start the registered closure from the input cell and bind its parameter | Correct argument binding and environment initialization for the harness's single entry call. |
| `semantic.k:83-85` | Execute a return whose value is the exact one-generator filtered list comprehension | It discards later statements only as Python `return` does. The submitted body has no later statement. |
| `semantic.k:87-93` | Empty/cons iterator and output emission | Structural descent on the finite list guarantees progress. Tail-first traversal followed by head-prepend yields original order. `KREST` remains framed. Output is the only observable state changed. |

No operational-rule overlaps produce inconsistent right-hand sides. Empty and
cons list shapes are disjoint; the two function-definition forms are
constructor-distinct; and the submitted return has one exact matching rule.

The iterator rule carries both predicate and element evaluations as pure
function terms. A general Python list comprehension would evaluate the element
only when the predicate is true, but this submitted element is the total,
side-effect-free lookup `Name("number")`. Any eager simplification is therefore
observationally identical for every intended input. Likewise, receiver,
argument, and comparison subexpressions in the submitted predicate are pure.
This generated semantics is intentionally program-scoped and remains sound for
every construct use in `solution.mpy`.

### Function equations

| Lines | Functions/equations | Review |
|---|---|---|
| `semantic.k:95-97` | `ifCons(true/false,...)` | Exhaustive and disjoint over Bool; faithfully conditionally prepends. |
| `semantic.k:100-113` | `eval` for Int, environment lookup, list `count` call, integer equality, and one-generator list comprehension | Lookup hit and recursive miss guards are disjoint. Every expression shape used by the submitted term has a rule. Receiver and argument types are checked by the partial `as*` projections. |
| `semantic.k:115-120` | `asInt`, `asInts`, `asBool` | Truthful, disjoint projections. They are deliberately partial on wrong value variants; actual typed execution always supplies the matching variant. |
| `semantic.k:123-130` | `count` on empty, equal-head, and unequal-head integer lists | For every ground finite integer list, the equations are exhaustive, pairwise disjoint, and structurally descending. They exactly implement Python integer-list multiplicity. `[concrete]` limits symbolic application but does not add an equation or an arbitrary result. |
| `semantic.k:134-144` | `collect` and `prependIf` | Correct stable filter with lexical shadowing. `eval(ListComp)`/`collect` is not reached by the specialized submitted return rule, but its equations are nevertheless truthful and descending. |
| `verification.k:9-17` | `removeRepeated` and `removeRepeatedOnto` | The wrapper initializes an empty suffix; base returns the suffix; cons conditionally prepends the head to the recursive tail result. Shapes are disjoint and recursion descends. The result is precisely stable-filter(input) concatenated with suffix. |

No function is declared total, so there is no unsupported totality obligation.
All functions that influence this program's result reduce on intended ground
arguments. There are no overlapping guarded equations with disagreeing
right-hand sides and no non-descending recursive equation.

The `count` function is a semantics-level model of the fixed external Python
primitive, not an oracle for the task answer. Its three ground equations
determine both distinct outcomes needed by the program—one occurrence and
multiple occurrences—and the normal/boundary concrete comparisons exercise
empty, equal-head, and unequal-head branches. In the symbolic proof,
`[concrete]` leaves some `count(I, ORIGINAL)` patterns unexpanded, but the
formal result remains explicitly conditional on this fully stated primitive
contract. No wrong ground interpretation is admitted on the intended domain.

### Construct-to-rule map

| Submitted constructor | Declaration and behavior |
|---|---|
| `Module` and translated `ImportFrom("typing","List")` | `Pgm`/`Stmt`; module sequencing and inert typing import at lines 62-65 |
| `FuncDef`, `Params`, `CellVars`, `FreeVars`, `Return` | `Stmt` and wrapper declarations; registration at 67-70, invocation at 73-76, return at 83-85 |
| `ListComp`/`CompFor` | `Expr`/`CompFor`; submitted return becomes `walkComp` at 83-93 |
| `Name("numbers")`, `Name("number")` | `Expr`; environment hit/miss equations 102-104 |
| `Attribute(...,"count")` and `Call` | `Expr`; fixed count-call evaluator 106-107 and count equations 127-130 |
| `Compare`, `CmpOp("==", Int(1))` | `Expr`/`CmpOp`; integer equality evaluator 109-110 |

Every material operation and control effect in the submitted term executes.
Unsupported unused Python constructs stop visibly because no syntax/rule exists;
that is permissible in `GENERATED_SEMANTICS`.

### Proof claims and extension classification

| Extension | Class and domain | State/value justification |
|---|---|---|
| `walk-correct` | Derived reachability lemma; exact submitted iterator expression, arbitrary `INPUT`, `ORIGINAL`, `SUFFIX`, and arbitrary continuation `KREST` | First positive proof establishes the complete match domain using the fixed generated semantics. It reads the expression's embedded environment, rewrites `<k>`, and updates `<output>`; all omitted cells are framed. Its value is fixed by `removeRepeatedOnto`, whose equations match each iterator step. |
| `program-correct` | Entry reachability theorem, not a semantic rewrite | Executes the exact module. It depends on the separately proved `walk-correct` lemma and the truthful summary equations. |

There is no fresh opaque or existential result and no priority rule that
preempts real execution. The same program-derived computation is not replaced
by an unconstrained symbol.

Because `walk-correct` accepts arbitrary `KREST`, I tested an observable
continuation rather than assuming context irrelevance. Starting with input
iterator `[1]`, existing output suffix `[8]`, and immediate continuation
`emitComputed(true,9)`, fixed semantics proves final output `[9,1,8]`.
The version with `walk-correct` loaded as the trusted, separately proved lemma
also proves `[9,1,8]`. Both print `#Top`. This matches the lemma's universal
justification domain and confirms that control/output after the summarized
region are preserved.

Evidence:

- `evidence/spec-context-witness.k`
- `evidence/05-context-fixed.log`
- `evidence/05-context-bridge.log`
- `evidence/05-body-mutation-dry-run.log`
- `evidence/05-body-mutation-proof.log`

The initially authored context witness used a singleton `Ints` surface spelling
that parsed as an injected `Int` and did not match `walkComp`; those diagnostic
non-proofs are preserved as `05-context-*-initial-shape.log` and are not counted
as validation. The corrected `(1, .Ints)` witness is the successful evidence.

I found no unsound local rule. Consequently there is no claimed unsoundness for
which a false-conclusion witness is required.

## 6. Fresh non-vacuity test

I did not rely on a candidate-provided vacuity artifact; none exists.
`evidence/spec-vacuity.k` is reviewer-authored. It retains the exact program and
the separately proved iterator lemma but changes the entry result to require a
leading zero:

```k
<output>
  listValue(.Ints) => listValue(0, removeRepeated(INPUT, INPUT))
</output>
```

This is meaningfully false. The realizable satisfying input `INPUT = .Ints`
returns the empty list, while the mutation demands `[0]`.

The dry run exited 0, demonstrating successful parsing and claim compilation.
The proof command was:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --trusted walk-correct
```

It exited 1 with `WarnStuckClaimState`. The residual says the final
configuration unifies with the destination but the implication fails on:

```text
0 , removeRepeatedOnto(INPUT, INPUT, .Ints)
  #Equals
removeRepeatedOnto(INPUT, INPUT, .Ints)
```

This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/06-vacuity-dry-run.log`
- `evidence/06-vacuity-proof.log`

The proof is result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under the candidate's freshly rebuilt generated semantics and the imported K
builtins, for every finite constructor list `INPUT` of arbitrary mathematical
integers:

1. execution begins with the exact trusted-regenerated `solution.mpy` module in
   the generated initial configuration;
2. the actual submitted function definition is registered and invoked with
   `numbers = INPUT`;
3. the translated comprehension executes to `.K`;
4. final output is `removeRepeated(INPUT, INPUT)`;
5. the latter structurally retains, in original order, exactly the input
   elements for which the fixed `count` primitive returns one.

Static inspection of the ground `count` equations establishes that this is
exactly the prompt's “remove all elements occurring more than once” result for
integer lists.

This is a partial-correctness report, consistent with the Kit contract. It does
not claim asymptotic efficiency or correctness outside the modeled intended
domain.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell backend, reachability logic, and kernel | All builds and proof closure | Standard unavoidable proof-checker trust boundary; versions recorded and fresh commands preserved. |
| Imported `INT`, `BOOL`, `STRING`, K sequencing, cells, and list constructors | Arithmetic equality/disequality, booleans, strings, finite integer-list representation, control | Accepted low-level K builtins. No candidate rule changes them. |
| Trusted `py2mpy.py` translation boundary | Maps the submitted Python AST to `solution.mpy` | Launcher-designated trusted input; candidate copy matches it, trusted regeneration is byte-identical, and the claim KAST matches mechanically. |
| Generated semantic rules in `semantic.k` | Binding, control, list iteration, primitive count, and final output | Not assumed from prior prose or `#Top`; every local declaration/rule is inventoried and audited above, with concrete normal/boundary execution. |
| Python `list.count` on integer lists, modeled by `count` | Determines predicate branches and therefore output | Fixed external-language primitive, outside program-defined code. Three truthful, exhaustive, disjoint, descending ground equations state its contract; concrete K/Python comparisons cover distinct outcomes. |
| `walk-correct` in the second proof | Accelerates the actual iterator over arbitrary continuation/output suffix | Machine-proved first with `#Top` over exactly the later trusted domain; fixed/bridge continuation witness agrees. It is not merely assumed from prose. |
| Summary-to-English interpretation of `removeRepeatedOnto` | Connects formal output to stable removal of duplicates | Direct structural induction from its three equations plus the count contract; independently checked examples and differential tests support, but do not replace, that mathematical argument. |
| Python differential tests | Supports source and generated-semantics bridges on tested values | Empirical only: 20,543 source cases and nine K concrete cases, zero mismatches. Not used as universal proof. |

No unproved program-defined helper, oracle, unconstrained opaque value,
proof-local simplification, false totality assertion, or task-answer semantic
rule is trusted.

Excluded behavior is explicit:

- values outside the prompt's finite `List[int]` domain, including objects with
  custom equality or side effects;
- arbitrary Python modules, multiple function definitions, multiple
  parameters, general comprehensions with effectful expressions, exceptions,
  I/O, mutation, or heap aliasing;
- termination/resource complexity as a separate total-correctness or
  performance theorem.

These exclusions do not narrow the HumanEval source-contract domain. The K
domain includes empty lists, arbitrary finite length, negative integers, and
unbounded mathematical integers; it is not a finite-size, example-only, or
bounded-unrolling theorem.

### Decision

The reconstructed claims close, the generated semantics faithfully covers
every construct and material effect used by the real submitted program, the
entry claim is constructor-identical to that program, the formal domain matches
the unrestricted HumanEval integer-list domain, the summary constrains the
intended result, and both body and false-result mutations are rejected for the
expected reason. The candidate is therefore legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
