# Independent adversarial audit: 2-truncate-number

The reconstructed K proof is legitimate for the submitted program on positive,
finite CPython binary64 inputs. It executes the exact translated function body
and constrains the returned fractional part. I assign `CONCERNS / LEGIT`,
rather than an unqualified pass, because the generated semantics uses an
exact-rational input model and an unguarded `int` primitive whose correctness is
established only on the entry precondition. The bridge from that model to
CPython binary64 is mathematically credible and strongly tested here, but it is
not itself a machine-checked K connection theorem.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The trusted mount
`/reference/reference-semantics` is absent. This is the required state, so
there is no infrastructure breach and no hidden or inferred reference
semantics was used.

### Required artifacts and types

The following required candidate artifacts are present as regular, non-symlink
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. No required artifact is missing, changed in type, or symlinked.

The candidate also contains:

- a structured 152-record JSONL generation trace;
- `mutation-spec.k`;
- a candidate-built `verification-kompiled/` directory.

These additional items are not integrity failures. The compiled directory and
all candidate logs/traces were treated only as untrusted claims and were not
used for reconstruction.

The candidate `prompt.py` is byte-identical to `/reference/prompt.py`
(SHA-256
`fecb9ddd4f103f1c3e9d9c7d6c3b948a4b1285b50c3498437c85a9d604d957eb`).
The candidate `py2mpy.py` is byte-identical to
`/reference/py2mpy.py` (SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).

`run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the JSONL trace were read only as provenance claims.
They claim a successful generation and proof. The trace was independently
parsed as 152 valid JSON records, but none of those claimed proof results was
accepted without reconstruction.

Evidence:

- [integrity check and full candidate tree](evidence/provenance/01-integrity.log)
- [untrusted metadata, log, and trace summary](evidence/provenance/02-untrusted-claims.log)
- [trace summarizer](evidence/provenance/summarize_untrusted_trace.py)

All source needed for execution was copied to `/tmp/audit-work`; no
candidate-provided cache or compiled definition was copied into either fresh
definition.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` asks for the decimal/fractional part of a positive
floating-point number after separating its integer part. The trusted
`/reference/canonical.py` disambiguates this as `number % 1.0`. On the
decomposable intended domain, this is a result in `[0,1)`, with exact integers
mapping to `0.0`.

The decomposition in the prompt implies finite inputs. Negative numbers, zero
under the strict-positive wording, NaN, and infinity are outside the audited
domain. This matters: the generated implementation differs from the canonical
implementation on negatives and non-finite values. Those excluded probes are
recorded in
[excluded-domain probes](evidence/differential/02-excluded-domain-probes.log).

### Implementation and translation

The candidate implementation is:

```python
def truncate_number(number: float) -> float:
    return number - int(number)
```

For positive finite floats, `int(number)` is the nonnegative integer part and
the subtraction returns the required remainder.

I regenerated the constructor program using the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/build/regenerated-solution.mpy
cmp /tmp/audit-work/build/regenerated-solution.mpy \
    /tmp/audit-work/source/solution.mpy
```

`cmp` exited 0. Both files have SHA-256
`e6e7d0d86c096c41a28fb0a9484ca5eba52d16a0e173de1bfa782f769552f26b`.
See [translator identity](evidence/provenance/03-translator-identity.log).

### Independent differential test

The reviewer-authored
[differential test](evidence/differential/differential_test.py) imports the
trusted canonical entry point and candidate-generated entry point independently.
It compares exact binary64 output bits, not a tolerance.

The 4,510 unique positive finite cases include:

- the prompt example;
- smallest/largest subnormal and smallest normal values;
- values immediately below, at, and above 1 and 2;
- both sides of integer truncation boundaries through 128 and selected larger
  boundaries;
- the `2**52` precision boundary, `2**53`, a large finite value, and maximum
  finite binary64;
- 4,096 deterministic random positive finite bit patterns (seed `44113175`).

There is no collection “empty” case because the input is a scalar float. The
test exited 0 with `mismatches=0`. Every input and result is preserved in
[the complete differential log](evidence/differential/01-python-differential.log).
This is strong finite evidence, not a universal proof.

## 3. Clean proof reconstruction

### Toolchain and fresh builds

The independently installed K tools are version `v7.1.293`. `kup` is absent,
but `/usr/bin/kompile`, `/usr/bin/krun`, and `/usr/bin/kprove` are available
and ran successfully. See [toolchain log](evidence/rebuild/01-toolchain.log).

From copied source in `/tmp/audit-work/build`, I built two new definitions:

```text
kompile --backend llvm semantic.k \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition semantic-kompiled
```

This concrete build exited 0:
[concrete build log](evidence/rebuild/02-kompile-concrete.log).

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition verification-kompiled
```

This proof build exited 0:
[proof build log](evidence/rebuild/03-kompile-proof.log).

### Positive claims

The exact submitted spec was proved with:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`:
[complete spec proof](evidence/rebuild/04-kprove-spec-all.log).

`spec.k` has two positive claims. To check each separately, I placed each
unchanged claim body in a reviewer module:

- the universal claim separately exited 0 and printed `#Top`:
  [source](evidence/rebuild/claim-universal.k),
  [log](evidence/rebuild/07-kprove-universal-alone.log);
- the prompt-example claim separately exited 0 and printed `#Top`:
  [source](evidence/rebuild/claim-example.k),
  [log](evidence/rebuild/08-kprove-example-alone.log).

### Fresh generated-semantics executions

The exact regenerated `solution.mpy` was concretely run under the fresh LLVM
definition. The prompt representation `num(3,5,10)` terminated with
`num(0,5,10)`:
[prompt execution](evidence/rebuild/05-krun-prompt.log).

The reviewer-authored
[concrete comparison script](evidence/rebuild/concrete_compare.py) then ran
nine exact K cases: 3.5, the smallest positive subnormal, immediately below 1,
1, immediately above 1, immediately below `2**52`, `2**52`, a representative
large fractional value, and maximum finite binary64. Every `krun` exited 0,
each K rational result equaled the exact `Fraction` of the trusted Python
result, and both Python implementations returned identical binary64 bits.
The run ended with `failures=0`; commands, inputs, outputs, and statuses are in
[the concrete comparison log](evidence/rebuild/06-concrete-compare.log).

There was no timeout, container error, malformed mount, or other infrastructure
uncertainty.

## 4. Adequacy and real-program pinning

### Universal entry claim

In plain language, the first claim starts with the exact submitted constructor
tree and invokes its defined function on `num(I,F,S)`. Its precondition is:

```text
S > 0
I >= 0
0 <= F < S
I > 0 or F > 0
```

Under the documented interpretation `num(I,F,S) = I + F/S`, this is a strictly
positive number in canonical integer-plus-proper-fraction form.

The destination requires:

- all computation consumed (`<k> .K </k>`);
- the local binding to contain the input;
- the result to be exactly `num(0,F,S)`;
- that result to satisfy `validFraction`.

This is an equality-constraining postcondition. It contains no fresh result
variable, existential oracle, tautology, or implication that could accept an
arbitrary return.

A satisfying state is `I=3, F=1, S=2`, representing 3.5. Its expected
substitution is `num(0,1,2)`. Fresh K execution returns that value, and both
Python functions return exactly `0.5`; this case is in the concrete comparison
log. The alternative candidate encoding `I=3, F=5, S=10` also satisfies the
precondition and is proved by the second claim.

### Prompt-example claim

The second claim has the fixed input `num(3,5,10)` and fixed output
`num(0,5,10)`. It has no symbolic precondition; its concrete starting state is
therefore trivially realizable. Both Python implementations return `0.5`.

### Pinning and body sensitivity

The `<k>` term in both claims is exactly:

```text
Module(FuncDef("truncate_number", Params("number"),
  Return(BinOp("-", Name("number"),
    Call(Name("int"), Name("number"))))))
```

This is byte-for-byte the trusted translator output in `solution.mpy`.
The rules enter that function, bind `"number"`, evaluate the left operand,
evaluate the `int` call on the right, subtract, and commit the returned value.
There is no rule that replaces the complete function with a summary.

As an independent sensitivity check, I translated a changed body,
`return number`, and ran it under the same fresh semantics on 3.5. Its K result
changed to `num(3,1,2)`, rather than the original `num(0,1,2)`. See the
[mutation source](evidence/static/body-mutated-solution.py) and
[body-sensitivity execution](evidence/static/01-body-sensitivity.log).
Thus proof closure depends on the submitted body.

There are no helper or loop claims. Every claim matches the real straight-line
control flow.

## 5. Rule-by-rule static soundness review

The exhaustive source with line numbers is preserved in
[numbered sources](evidence/static/00-numbered-sources.log), and the full
declaration/rule analysis is in the
[reviewer rule inventory](evidence/static/rule-inventory.md).

### Complete local declaration inventory

`SEMANTIC-SYNTAX` declares:

1. `Program`: `Module(Stmt)`.
2. `Stmt`: `FuncDef(String,Params,Stmt)` and `Return(Expr)`.
3. `Params`: `Params(String)`.
4. `Expr`: `Name(String)`, `BinOp(String,Expr,Expr)`, and
   `Call(Expr,Expr)`.
5. `Value`: `num(Int,Int,Int)` and `intValue(Int)`.
6. `Result`: `noResult` and the `Value` subsort.
7. `KItem`: `invoke`, `eval`, `subtractLeft`, `subtractRight`, `applyInt`,
   and `finishReturn`.

The constructor productions carry `[symbol(...)]`. `VERIFICATION` adds only
`validPositive(Value)` and `validFraction(Value)`, each declared
`[function,total]`.

There are no local `[functional]`, `[opaque]`, `[simplification]`,
`[concrete]`, priority, or `owise` declarations/rules. There are no generated
helper K source files. `domains.md` supplies the imported `INT`, `STRING`,
`MAP`, and later `BOOL` primitives.

The configuration has only the needed cells: computation, local environment,
and result, inside a top-level `<python>` cell. All are read or written. No
heap, allocation, I/O, exception, or stack state is used by this program.

Every submitted syntactic construct is declared and covered:
`Module`/`FuncDef`/`Params` by entry, `Return` by return setup and completion,
`Name` by lookup, `BinOp("-")` by the subtraction sequence, and
`Call(Name("int"),...)` by the built-in call rules.

### All nine operational rules

1. **Function entry** matches the same `F` in `FuncDef(F,...)` and
   `invoke(F,V)`, then binds the sole parameter in an empty environment.
   This pins the call to the defined name.
2. **Return setup** evaluates its expression before `finishReturn`.
3. **Name lookup** retrieves the matching map binding without changing state.
4. **Subtraction start** evaluates the left operand first.
5. **After-left transition** saves that value and then evaluates the right
   operand.
6. **Subtraction completion** computes
   `num(I,F,S) - intValue(J)` as `num(I-J,F,S)`, preserving operand order.
7. **`int` call setup** matches exactly `Call(Name("int"),ARG)`.
8. **`int` primitive** maps `num(I,F,S)` to `intValue(I)`.
9. **Return completion** consumes `finishReturn` and changes `noResult` to the
   exact computed value.

The leading constructors and continuation markers are disjoint on the real
path, and there are no priorities or overlaps that can preempt a different
used behavior. The environment and result updates match the required state
footprint.

Rule 8 is correct on every entry-precondition state: `0 <= F < S` and `S>0`
put `I+F/S` in `[I,I+1)`, so positive Python truncation returns `I`. The rule
is syntactically unguarded, however, and is not a reusable definition for every
constructible `num` term. For example, `num(0,3,2)`, informally read as 1.5,
causes the K program to retain `3/2`, while Python returns 0.5. That encoding
fails `F<S` and is not an admissible entry state. The witness and scope are
recorded in
[the over-breadth log](evidence/static/02-outside-precondition-overbreadth.log).
Because no such state satisfies the entry precondition, this is not an
unsoundness witness on the intended domain; it is a documented non-reusability
and trust-boundary concern.

The return rule also frames an arbitrary K suffix and would not by itself model
general Python abrupt return through arbitrary statement continuations. The
local `Stmt` grammar has no sequencing construct, the actual body is the sole
`Return`, and no such continuation is reachable from either entry claim.

### All four verification equations

1. `validPositive(num(I,F,S))` expands to the five entry constraints.
2. `validPositive(intValue(_))` is false.
3. `validFraction(num(I,F,S))` requires integer component zero and a proper
   nonnegative fraction.
4. `validFraction(intValue(_))` is false.

For each total function, the two rules cover the two and only two `Value`
constructors. Their patterns are disjoint, unguarded, nonrecursive, and
mathematically truthful.

### Soundness conclusion

No rule encodes the whole task answer, fabricates a result for an unmodeled used
construct, introduces a fresh result-bearing oracle, or bypasses the submitted
body. There is no false local rule witness reachable from the intended entry
domain.

The important modeling boundary is that `num(I,F,S)` is an exact rational,
whereas CPython uses binary64. Every positive finite binary64 has an exact
dyadic decomposition satisfying the precondition. For values below `2**52`,
subtracting the integer part yields the representable dyadic fractional part;
at and above `2**52`, binary64 values are integral and the result is zero.
That bridge is mathematically sound and the boundary executions support it,
but it is informal rather than a K theorem connecting CPython execution to
`num`.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `mutation-spec.k`. The fresh reviewer
mutation keeps the universal entry term and original precondition but changes
the required result from `num(0,F,S)` to `num(1,F,S)`:
[fresh false spec](evidence/nonvacuity/fresh-false-spec.k).

The original precondition remains satisfiable; `I=3,F=1,S=2` is a witness, and
the mutation falsely requires integer component 1 for the result of 3.5.

First:

```text
kprove fresh-false-spec.k --definition verification-kompiled \
  --spec-module FRESH-FALSE-SPEC --dry-run
```

exited 0 and produced the backend invocation, establishing successful
parse/build:
[mutation build log](evidence/nonvacuity/01-mutation-build.log).

Then the actual proof command, without `--dry-run`, exited 1 with
`WarnStuckClaimState`. Its residual shows the expected unmet implication
`1 #Equals I -Int I`, while retaining the original satisfiable constraints.
This is a semantic rejection, not a parser error, timeout, missing import, or
unreachable mutation:
[mutation proof log](evidence/nonvacuity/02-mutation-proof.log).

The proof is therefore result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the reconstructed candidate K definition:

> For every `I,F,S` satisfying `S>0`, `I>=0`, `0<=F<S`, and strict
> positivity, every terminating execution of the exact submitted constructor
> program from the specified empty-environment invocation ends with computation
> consumed and result exactly `num(0,F,S)`. Separately, the ground
> `num(3,5,10)` claim has destination `num(0,5,10)`.

This is reported conservatively as partial correctness, in accordance with the
Kit workflow. The fresh concrete executions also show termination for the
normal and boundary witnesses that were run.

The formal domain actually includes canonical decompositions of all positive
exact rationals, including non-dyadic rationals that are not CPython binary64
values. This superset is sound under the exact-rational interpretation; it does
not enlarge the set of Python inputs claimed by the bridge.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 and imported `INT`, `BOOL`, `MAP`, `STRING` hooks | Parsing, integer arithmetic, Boolean constraints, maps, and proof execution | Acceptable low-level toolchain/mathematics boundary |
| Trusted `/reference/py2mpy.py` | Links `solution.py` to the exact K constructor tree in the claim | Acceptable; regeneration is byte-identical |
| `num(I,F,S)` means exact `I+F/S` | Gives semantic meaning to input and result constructors | Concerning but legitimate informal representation bridge |
| Canonical encoding has `S>0` and `0<=F<S` | Makes the `int` primitive return exactly `I` | Mathematically valid on every entry state; the unguarded rule is over-broad outside that state |
| Exact-rational subtraction models CPython binary64 subtraction on positive finite inputs | Connects the K result to the real generated Python program | Informally justified and supported by 4,510 Python cases plus nine K boundary cases; no universal K connection theorem |
| Trusted canonical `number % 1.0` expresses the prompt | Connects implementation behavior to natural-language intent | Trusted input plus zero-mismatch differential evidence |

There are no locally declared opaque symbols, fresh result symbols,
uninterpreted result oracles, auxiliary lemmas, loop circularities, or
proof-local operational bridges. `num` is a data constructor whose external
numeric interpretation is explicit, not a fresh value chosen by the proof.

The differential tests and traces are not substitutes for the K proof. The K
proof establishes the exact-rational reachability theorem; the tests support
only the finite implementation/canonical and model/runtime bridges.

Excluded behavior is negative input, zero under the strict-positive contract,
NaN, infinity, noncanonical `num` encodings, and general Python syntax or
control flow not used by this program. Missing semantics for those unused
constructs is not a generated-semantics defect.

### Decision

- Clean reconstruction: pass.
- Real-program pinning and result constraint: pass.
- Intended positive-finite domain: pass.
- Fresh non-vacuity: pass.
- Static rule validity on every entry-precondition execution: pass.
- Auditability: pass.
- Qualification: the CPython-binary64 bridge is not machine-checked in K, and
  the `int` rule is over-broad outside the precondition.

Those limitations do not make a false conclusion provable for any satisfying
entry state and do not substitute another program. They warrant
`CONCERNS / LEGIT`, not failure.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
