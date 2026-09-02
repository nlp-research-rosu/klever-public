# Independent adversarial audit: 49-modp

## Executive finding

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the actual submitted `solution.mpy` program under the supplied MPY semantics.
Fresh reconstruction closes the only positive claim with exit status 0 and
`#Top`. The proof-local rules are three result-preserving definitional
equations; none bypasses execution, introduces an oracle, or changes control or
state. A body mutation and an independent false-postcondition mutation are both
rejected.

The result is not an unqualified pass. The submitted direct-expression rewrite
is not extensionally identical to the trusted canonical implementation at the
satisfying boundary input `(n=0, p=1)`: the canonical returns `1`, while both
the submission and its proved specification return the mathematically expected
`0`. The prompt does not explicitly state the proof's restrictions
`n >= 0, p > 0`, and the two Python implementations also differ on several
excluded integer inputs. In addition, four named generation-record artifacts
and the structured trace are absent. These are adequacy and provenance
limitations, not a defect in the reconstructed K theorem about the submitted
program.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. The rendered mode is
`SUPPLIED_SEMANTICS`, `/reference/reference-semantics` exists as a directory,
and the K tools are available. The recorded versions are K 7.1.337 for
`kompile`, `kprove`, and `krun`
([`evidence/00-infrastructure.log`](evidence/00-infrastructure.log)).
Consequently there is no infrastructure breach and a candidate verdict is
appropriate.

The full candidate inventory is in
[`evidence/01-candidate-inventory.log`](evidence/01-candidate-inventory.log).
All submitted source and proof artifacts used here are regular files. No
symlink occurs in the candidate semantics tree. The candidate also contains
`__pycache__/solution.cpython-310.pyc`; that generated cache was ignored and
not copied into the clean reconstruction.

The following untrusted generation-record artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any top-level structured trace or JSONL trace

There was therefore nothing to read from those artifacts as a candidate claim.
Their absence limits provenance auditability but does not prevent independent
reconstruction. The exact checks are recorded in
[`evidence/02-provenance.log`](evidence/02-provenance.log).

The candidate prompt and translator are byte-identical to the trusted mounts:

- `prompt.py`: SHA-256
  `e66b53fb6c885a4c550b997add2be1d3229f04eabfca6e66e7a2d1e2845b164f`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

A recursive, no-symlink-following comparison of
`/candidate/reference-semantics` with
`/reference/reference-semantics` exited 0. There are no missing, additional,
changed, mistyped, or symlinked entries in that tree. This establishes
integrity against the selected fixed semantics; it does not bless the
proof-specific rules in `verification.k`.

The trusted and candidate sources used for the audit were copied as source
only to `/tmp/audit-work/49-modp`; no candidate K definition, cache, proof log,
or `.pyc` was reused. The exact copy inventory is in
[`evidence/04-scratch-copy.log`](evidence/04-scratch-copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt says: return `2^n` modulo `p`, with examples
`(3,5)->3`, `(1101,101)->2`, `(0,101)->1`, `(3,11)->8`, and
`(100,101)->1`. It gives integer type annotations but no explicit sign or
nonzero restrictions.

The trusted canonical implementation starts with `ret = 1` and performs
`ret = (2 * ret) % p` once for every element of `range(n)`. Thus it implements
repeated modular doubling when the loop executes. For `n <= 0`, the loop is
empty and the canonical returns the un-reduced initial value `1`.

The submitted implementation is a different, direct algorithm:

```python
return (2 ** n) % p
```

For the ordinary modular-exponentiation domain `n >= 0, p > 0`, this directly
computes the stated mathematical value. The K proof adopts exactly that domain.

### Translation identity

I regenerated `solution.mpy` from the submitted `solution.py` with the copied
trusted translator:

```text
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s submitted-solution.mpy regenerated-solution.mpy
```

Both files have SHA-256
`decfb64de0df0629e829ffe7ab9b401825c0462c98ffb57019f5d3657006cf7c`;
`cmp` exited 0. See
[`evidence/05-translation-identity.log`](evidence/05-translation-identity.log).

### Independent differential test

[`evidence/differential_modp.py`](evidence/differential_modp.py) independently
imports the trusted canonical entry point and submitted entry point. The exact
inputs are preserved in
[`evidence/differential-inputs.json`](evidence/differential-inputs.json). The
scope was:

- all five documented examples;
- explicit zero, one, modulus-one, parity, and large-exponent boundaries;
- the full grid `n=0..32`, `p=1..33`;
- 256 deterministic generated pairs with seed `490049`,
  `n=0..2048`, `p=1..1000`;
- nine separately labelled diagnostics outside the proof domain.

After deduplication, 1,351 inputs were compared inside `n >= 0, p > 0`.
There was exactly one mismatch:

```text
input (0, 1):
  trusted canonical -> int 1
  submitted solution -> int 0
```

The script therefore exited 1 by design. The command, result, and status are in
[`evidence/06-differential.log`](evidence/06-differential.log). This is a
material canonical-equivalence boundary because `n=0` is explicitly exemplified
and `p=1` is allowed by both the ordinary positive-modulus convention and the
formal precondition. Mathematically, however, `2^0 mod 1` is `0`, so this
finding is a discrepancy between the trusted canonical algorithm and the
natural-language formula, not evidence that the submitted direct expression
violates that formula.

The outside-domain diagnostics also show why the formal restriction matters.
For negative `n`, the canonical returns integer `1` while the submission uses
negative exponentiation and returns a float. At `(0,0)` the canonical returns
`1` without taking a modulus, while the submission raises
`ZeroDivisionError`. At `(0,-7)` the canonical returns `1` and the submission
returns `-6`. These cases are not claimed by the K theorem, but the prompt
itself does not explicitly exclude them.

## 3. Clean proof reconstruction

The supplied semantics and proof were rebuilt from source in the scratch copy.
Every K command was bounded by an external timeout and logged with its exact
arguments and exit status.

The concrete definition was built with:

```text
timeout 600s kompile reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0
([`evidence/07-kompile-runtime.log`](evidence/07-kompile-runtime.log)).
The compiler reported non-exhaustive-totality warnings for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None is reachable from
this integer-only program; they are accounted for in stages 5 and 7 rather than
silently treated as proof facts.

The five candidate examples then concretely executed to a final `.K` state with
exit status 0
([`evidence/08-concrete-examples.log`](evidence/08-concrete-examples.log)).
Reviewer-authored boundary assertions, including `(0,1)->0`, also executed to a
final `.K` state with exit status 0. The source and translation are
[`evidence/concrete-boundaries.py`](evidence/concrete-boundaries.py) and
[`evidence/concrete-boundaries.mpy`](evidence/concrete-boundaries.mpy); the
command is in
[`evidence/09-concrete-boundaries.log`](evidence/09-concrete-boundaries.log).

The proof definition was freshly built with:

```text
timeout 600s kompile verification.k \
  --backend haskell --main-module MODP-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0
([`evidence/10-kompile-verification.log`](evidence/10-kompile-verification.log)).

The exhaustive inventory found one and only one positive reachability claim,
in `spec.k`, and no helper or loop claims. It was independently run as:

```text
timeout 600s kprove spec.k \
  --definition verification-kompiled \
  --spec-module MODP-SPEC
```

`kprove` exited 0 and printed `#Top`
([`evidence/11-kprove-positive.log`](evidence/11-kprove-positive.log)). The
backend emitted repeated `DecidePredicateUnknown` warnings during symbolic
simplification, but completed successfully; no warning is being substituted
for the actual success condition.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

There is one entry claim. Its precondition is:

- symbolic K integers `N` and `P` satisfy `N >= 0` and `P > 0`;
- the computation first loads the submitted module term and then calls
  `modp(N,P)`;
- the environment is module scope `0`;
- scope `0` is empty with the fixed builtins scope at `-1`;
- scope/heap allocators are at `1` and `0`;
- heap and call stack are empty;
- return state is `noRet`, exception state is `NoExc`, and exit code is `0`.

Its postcondition is:

- the `<k>` cell contains `specModp(N,P) ~> .K`;
- `specModp(N,P)` reduces, under the same guard, to
  `pyMod(2 ^Int N, P)`;
- module scope `0` contains the loaded `modp` closure with the exact submitted
  body and builtins scope remains unchanged;
- allocator positions, heap, stack, return state, exception state, and exit
  code have their claimed restored/unchanged values.

Thus the returned value is not free, existential, or constrained by a one-way
implication. It is the concrete post-state `<k>` term determined by the
universally quantified inputs.

### Exact program pinning

The claim does not invoke a substituted summary of `modp`. It executes
`#loadAll(modpProgram)` and then performs an ordinary `Call(Name("modp"), ...)`.
The two readability aliases expand as follows:

- `modpProgram` is exactly
  `Module(FuncDef("modp", Params("n","p"), modpBody))`;
- `modpBody` is exactly the submitted translated sequence
  `Expr(Str("Return 2^n modulo p."))`
  followed by
  `Return(BinOp("%", BinOp("**", Int(2), Name("n")), Name("p")))`.

Comparison with the byte-verified `solution.mpy` shows no omitted, additional,
or changed AST node. The body then executes through the supplied statement,
lookup, call, operator, integer, return, and frame rules. There is no helper
claim or loop to match because the submitted program contains no loop.

### Satisfying states and concrete substitution

[`evidence/claim_witnesses.py`](evidence/claim_witnesses.py) and
[`evidence/16-claim-witnesses.log`](evidence/16-claim-witnesses.log) preserve
two ground states satisfying the entry precondition:

- `N=3, P=5`: claimed value `3`, submitted value `3`, canonical value `3`;
- `N=0, P=1`: claimed value `0`, submitted value `0`, canonical value `1`.

The second witness simultaneously establishes precondition satisfiability,
result constraint, agreement between the K contract and the actual submission,
and the canonical-equivalence concern.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/rule-inventory.md`](evidence/rule-inventory.md) is the exhaustive,
source-indexed inventory generated by
[`evidence/inventory_k.py`](evidence/inventory_k.py). It contains the complete,
whitespace-normalized text and source line range of every local top-level
configuration, syntax declaration, context, rule, and claim in all supplied K
files plus `verification.k` and `spec.k`. Its totals are:

- 26 K source files;
- 1 configuration;
- 230 syntax statements;
- 5 contexts;
- 698 rules;
- 1 claim;
- 149 entries containing function declarations, 107 containing `total`;
- no `functional` declaration and no simplification rule;
- 45 priority entries, 26 `owise` entries, and 35 entries containing concrete
  attributes;
- 25 `symbol` declarations, of which 22 use `no-evaluators`.

The inventory includes per-file counts and every individual row, so the
following disposition groups cover every inventoried item rather than only the
rules that happened to appear in a proof trace.

### Declarations, configuration, and used-rule mapping

`semantics/syntax.k` declares every submitted AST constructor: `Module`,
`FuncDef`, `Params`, `Expr`, `Str`, `Return`, `BinOp`, `Int`, `Name`, and
`Call`. `BinOp` is `seqstrict(2,3)`, `Return` and `Expr` are strict, and call
evaluation is explicitly routed callee-first and then argument-left-to-right.
There is no missing used construct and no fabricated rule for an unmodelled
used construct.

The one configuration in `semantics/core.k` has exactly the cells named by the
claim. Its load and sequence rules expose the real module statements.
`FuncDef` in `semantics/functions.k` installs the exact closure into the current
scope. `Call` in `semantics/call.k` resolves `Name("modp")`, evaluates both
integer arguments, creates one fresh call frame, binds `n` and `p`, executes
the stored body, and preserves the caller continuation in the stack.

The docstring goes through the ASCII `Str` rules in `semantics/str.k` and the
`Expr(Val) => .K` discard rule in `semantics/controls.k`. All characters used
are covered. The return expression evaluates left-to-right:

- `Int(2)` becomes K integer `2`;
- `Name("n")` and `Name("p")` resolve to the freshly bound parameters;
- the integer power rule rewrites `applyBin("**", 2, N)` to `2 ^Int N` under
  exactly the claimed guard `N >= 0`;
- the modulo rule rewrites to `pyMod(2 ^Int N,P)`;
- for positive `P`, the sole `pyMod` equation
  `((I %Int P) +Int P) %Int P` is the ordinary normalized/Python remainder;
- `Return` records the resulting value, discards only the remaining function
  body as Python return requires, and `#pop` restores the exact caller
  continuation and state.

The operator-string cases and value sorts on this path are disjoint. The
relevant functions are structurally descending or single-step. There is no
overlap with a different right-hand side, no totalization assumption on
`pyMod`, and no zero-divisor case because `P > 0`.

### Priorities, unused modules, opaque values, and proof imports

All 45 priority entries were checked against the reachable term shapes. The
special calls for `math`, `hashlib`, methods, sorted values, and concrete keyed
sorts cannot match `Call(Name("modp"), ...)`. The reference/cell lookup,
heap-reference, list, dictionary, float, assertion, and slicing priority rules
cannot match the integer-only values and plain non-cell scopes on this path.
Therefore no priority rule preempts the execution described above.

The rules in `assert.k`, `bool.k`, `builtins.k`, `comprehension.k`,
`dict.k`, `float.k`, `iter.k`, `list.k`, `methods.k`, `range.k`, `set.k`,
`sort.k`, `subscript.k`, and `tuple.k` were inspected through the exhaustive
inventory and source. Except for declarations/import dependencies and the
builtins scope constant, their operation-specific left-hand sides are
unreachable from this submitted AST and cannot contribute to claim closure.
They remain part of the selected supplied subset semantics; this audit does
not claim full CPython coverage for unused constructs or invalid arguments.
No false conclusion about the intended `modp` input domain can be obtained
from an unused rule merely by its presence.

The proof-side opaque/symbolic primitives in the supplied tree are:
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None appears in a reachable
configuration, branch, result, or postcondition for this claim. The six fresh
compile-time totality warnings likewise concern unused functions. They are a
narrow off-path coverage/evidence limitation, not an unsound-rule finding for
this proof.

`semantics/concrete.k` is imported only by `MPY-KRUN`. The Haskell proof imports
`MPY`, so its concrete-only equality and keyed-sort rules are absent from the
proof theory.

### Proof-local rules

`verification.k` contributes exactly three syntax declarations and three
equations:

1. `modpBody` is a definitional name for the exact submitted statement
   sequence.
2. `modpProgram` is a definitional name for the exact submitted module.
3. `specModp(N,P)` is a definitional mathematical summary
   `pyMod(2 ^Int N,P)` under the same `N >= 0, P > 0` guard as the claim.

These equations have one defining case each, no overlap, no recursion, no
priority, no simplification attribute, no `total`/`functional` assertion, and
no opaque result. The first two name syntax and do not replace execution. The
third names the expected value after the fixed semantics has independently
executed the program. There is no operational bridge, no program-derived
oracle, and no circular use of a fresh symbol in execution and postcondition.

### Body sensitivity

As an independent execution-sensitivity check, I changed only the submitted
body's base from `2` to `3`, left the expected base `2`, built a separate proof
definition, and reran the analogous claim. The mutation sources are
[`evidence/verification-body-mut.k`](evidence/verification-body-mut.k) and
[`evidence/spec-body-mut.k`](evidence/spec-body-mut.k). Compilation exited 0
([`evidence/17-kompile-body-mutation.log`](evidence/17-kompile-body-mutation.log)).
Proof exited 1 on a residual configuration containing `3 ^Int N mod P`, rather
than closing against `2 ^Int N mod P`
([`evidence/18-kprove-body-mutation.log`](evidence/18-kprove-body-mutation.log)).
This confirms body sensitivity and rules out an execution-bypassing summary.

I make no claim that an inventoried rule is materially unsound on the intended
domain; accordingly there is no unsupported “unsound rule” label requiring a
false-conclusion witness. The narrower off-path coverage and totality evidence
gaps are stated above.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied upon. I created the independent ground
mutation
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k). It uses the
satisfying input `N=3, P=5`, for which the real result is `3`, and changes the
result-constraining postcondition to demand `specModp(3,5) +Int 1`, namely `4`.

First, the exact dry run:

```text
timeout 120s kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module MODP-SPEC-VACUITY-AUDIT \
  --dry-run
```

exited 0, demonstrating that the mutation parses and builds
([`evidence/19-vacuity-dry-run.log`](evidence/19-vacuity-dry-run.log)).

The real mutated proof:

```text
timeout 120s kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module MODP-SPEC-VACUITY-AUDIT \
  -w none
```

exited 1 with `WarnStuckClaimState`. The residual final configuration visibly
contains `<k> 3 ~> .K </k>`, which cannot unify with the false destination `4`
([`evidence/20-vacuity-proof.log`](evidence/20-vacuity-proof.log)). This is the
expected unmet result obligation, not a parser error, missing import, timeout,
or unrelated crash.

## 7. Proven versus assumed accounting

### What the K proof establishes

Relative to the supplied MPY semantics and K's mathematical integer primitives,
the successful claim establishes this partial-correctness statement:

> For every K integer `N >= 0` and `P > 0`, starting in the specified clean
> module configuration, loading the byte-pinned submitted module and calling
> its `modp(N,P)` function executes the submitted direct-expression body and,
> if it terminates, leaves `pyMod(2 ^Int N,P)` as the returned computation,
> with the claimed scope, heap, stack, allocator, return, exception, and exit
> cells restored or preserved.

This is a theorem about the submitted program, not about execution of the
canonical loop. It is result-constraining and non-vacuous.

### Trust and assumption ledger

- **Trusted mounted inputs:** `/reference/prompt.py`,
  `/reference/canonical.py`, `/reference/py2mpy.py`, and the entire supplied
  semantics tree. Their role is fixed by the audit instructions. Candidate
  copies of prompt, translator, and semantics were integrity-checked before
  use.
- **K implementation and backend:** K 7.1.337, the Haskell reachability backend,
  its SMT integration, parser/kompiler, and the semantics of K maps, lists,
  strings, booleans, and integers are in the machine-checking trust base.
- **Arithmetic primitives:** unbounded `^Int`, `%Int`, comparisons, and ordinary
  integer operations are low-level trusted mathematical primitives. They are
  appropriate here because the source computation itself uses Python integer
  power and remainder; no task answer is hidden in a custom oracle.
- **Supplied language rules:** module loading, binding, evaluation, calls,
  return, and state cells are part of the selected supplied semantics. The
  candidate added no operational bridge over them. Exact tree identity makes
  this the intended fixed semantics, though equivalence of the whole MPY subset
  to all of CPython is not proved by this candidate.
- **Opaque symbols:** the 25 names listed in stage 5 are trusted/opaque parts of
  the supplied wider semantics. They have no dependent branch, result, state,
  or claim here, so the theorem does not rely on an interpretation of any of
  them.
- **Intent bridge:** interpreting the prompt as `n >= 0, p > 0` is informal.
  It is conventional for modular exponentiation and includes all documented
  examples, but the prompt does not state it. The K proof does not cover other
  integer arguments.
- **Canonical bridge:** finite differential evidence cannot establish universal
  equivalence, and in fact refutes equivalence at `(0,1)`. No claim of
  canonical equivalence is accepted.
- **Concrete execution:** the example/boundary `krun` checks are finite evidence
  for the selected semantics and exact AST. They do not substitute for the
  reachability proof.
- **Translation bridge:** byte identity proves that this submitted `solution.mpy`
  is exactly what the trusted translator emits for this `solution.py`. It does
  not prove the translator correct for every Python program.
- **Generation provenance:** the missing run input, metrics, last-output,
  output-log, and trace files prevent auditing the candidate's generation
  narrative. Fresh reconstruction makes them unnecessary for the theorem but
  their absence remains an auditability concern.

### Gate assessment and decision

- Real-program soundness: passes. The fixed semantics executes the exact body;
  there is no proof-local bridge or oracle; the postcondition constrains the
  result; body sensitivity and false-result mutation both reject false
  alternatives.
- Intent adequacy: concern. The theorem's domain is not explicit in the prompt,
  and the submission differs from the trusted canonical implementation at
  `(0,1)` inside the theorem domain. The submission nevertheless matches the
  literal mathematical formula on that witness.
- Evidence auditability: concern, because the named candidate generation
  records and trace are absent. The reviewer-authored reconstruction,
  inventory, tests, witnesses, and mutations are reproducible and preserved.

The adequacy and provenance limitations justify `CONCERNS`, while the sound,
freshly reconstructed, result-constraining proof of the real submitted program
justifies `LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
