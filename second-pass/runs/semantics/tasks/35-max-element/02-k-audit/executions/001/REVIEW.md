# Adversarial audit: 35-max-element

## Decision

The candidate contains a legitimate, non-vacuous partial-correctness proof for
the exact submitted translated program on **non-empty finite lists of
integers**. The proof is result-constraining, executes the submitted function
body under the supplied semantics, and survives clean reconstruction without
candidate caches.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
scope/evidence reasons:

1. The prompt annotates only `list` and does not expressly restrict elements to
   integers, while the theorem covers only non-empty integer lists. The Python
   implementation and canonical implementation also agree on sampled strings
   and floats, but that broader behavior is not proved in K.
2. All four requested generation/provenance files (`run-input.json`,
   `metrics.json`, `codex-last.txt`, and `codex-output.log`) and any structured
   generation trace are absent. This does not undermine the independently
   reconstructed source proof, but it limits provenance auditability.

The empty-list boundary is outside the formal precondition and has no maximum.
It also exposes a concrete implementation difference: the canonical function
raises `IndexError`, while the submitted `return max(l)` raises `ValueError`.

The complete evidence index is
[`evidence/EVIDENCE_INDEX.md`](/audit-output/evidence/EVIDENCE_INDEX.md).

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted directory
`/reference/reference-semantics` is present. There is therefore no mount/mode
contradiction and no infrastructure breach.

I compared the candidate semantics recursively without following symlinks. The
reviewer-authored checker compares relative entry sets, `lstat` types, symlink
status, executable bits, and SHA-256 file contents. It reported:

```text
integrity_failures=0 entries_compared=25
[exit_status] 0
```

Thus the candidate `reference-semantics/` has no missing, additional, changed,
mistyped, executable-bit-changed, or symlinked entry relative to the trusted
tree. See
[`check_tree_integrity.py`](/audit-output/evidence/check_tree_integrity.py) and
[`02-supplied-semantics-integrity.log`](/audit-output/evidence/02-supplied-semantics-integrity.log).
This integrity result does not bless the separate proof-local rules in
`verification.k`; those are reviewed in stage 5.

### Prompt, translator, and artifact inventory

Both `/candidate/prompt.py` and `/candidate/py2mpy.py` are regular files and
byte-identical with `/reference/prompt.py` and `/reference/py2mpy.py`. The
candidate proof sources `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are regular files, not symlinks. The candidate contains no
kompiled definition directory.

The following requested untrusted provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any top-level structured trace (`*trace*` or `*.jsonl`; count reported as
  zero)

The complete candidate inventory also includes `prove.sh`,
`concrete-tests.py`, `concrete-tests.mpy`, and a `__pycache__` directory. I did
not execute or reuse the cache or treat the candidate tests/script as proof
evidence. The inventory, versions, byte comparisons, and missing-file results
are preserved in
[`01-toolchain-and-inventory.log`](/audit-output/evidence/01-toolchain-and-inventory.log)
and
[`03-provenance-comparison.log`](/audit-output/evidence/03-provenance-comparison.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and source behavior

`/reference/prompt.py` asks `max_element(l)` to return the maximum element of
the list. `/reference/canonical.py`:

1. reads `l[0]` into an accumulator;
2. scans every element;
3. replaces the accumulator exactly when `e > m`; and
4. returns the accumulator.

Consequently, the canonical return contract is meaningful for a non-empty
finite list of mutually comparable values. On the integer subdomain proved by
the candidate, it returns the mathematical maximum. Empty input does not
satisfy that natural precondition and raises `IndexError`.

The submitted implementation is:

```python
def max_element(l: list):
    return max(l)
```

This is a different algorithm but is behaviorally appropriate on non-empty
comparable lists. The exact reviewed sources are reproduced with line numbers
in
[`04-source-review.log`](/audit-output/evidence/04-source-review.log).

### Trusted translation identity

I copied only source artifacts into `/tmp/audit-work/35-max-element`, copied the
trusted translator separately, regenerated the MPY file, and compared it with
the submission:

```text
$ python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
b040afa3...  solution.mpy
b040afa3...  regenerated-solution.mpy
translation_byte_identity=PASS
[exit_status] 0
```

The full hashes and command are in
[`06-translation-identity.log`](/audit-output/evidence/06-translation-identity.log).
The submitted `solution.mpy` is therefore byte-identical to trusted translation
of the submitted Python source.

### Independent differential test

The reviewer-authored differential test imports the trusted canonical entry
point from `/reference/canonical.py` and the copied submitted entry point from
scratch using separate `importlib` modules. It does not reuse K equations. Its
scope is:

- both documented examples;
- empty input;
- negative, zero, positive singleton cases;
- explicit greater, equal, and less branch boundaries at the first and later
  positions;
- duplicates and all-negative lists;
- signed 64-bit boundary values and arbitrary-precision integers;
- every list of lengths 1 through 5 over `[-2,-1,0,1,2]`;
- 2,000 deterministic generated integer lists of lengths 1 through 40 with
  values up to 40 decimal digits;
- one comparable-float list and one comparable-string list.

The recorded result is:

```text
seed=350035
formal_integer_cases=5920
formal_integer_mismatches=0
out_of_formal_cases=3
out_of_formal_mismatches=1
empty_boundary=canonical:{... 'type': 'IndexError' ...}
               generated:{... 'type': 'ValueError' ...}
[exit_status] 0
```

The sole mismatch is the exception class on empty input. The script is
[`differential_test.py`](/audit-output/evidence/differential_test.py), every
input and both outcomes are preserved in
[`differential-inputs.jsonl`](/audit-output/evidence/differential-inputs.jsonl),
and the command/summary are in
[`07-differential.log`](/audit-output/evidence/07-differential.log).
These are finite bridge evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

### Isolation and toolchain

All builds and mutations occurred under `/tmp/audit-work/35-max-element`.
Only candidate source files were copied; no candidate-built definition or cache
was copied. The scratch manifest is in
[`05-scratch-copy.log`](/audit-output/evidence/05-scratch-copy.log).

The independently installed tools are K version `v7.1.337` (build date
2026-06-18). `kup` is absent, but `kompile`, `krun`, and `kprove` are available
at `/usr/bin` and ran successfully, so no installation fallback was needed.

### Fresh builds

The concrete and proof definitions were built from source with these exact
commands:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled

kompile verification.k --backend haskell \
  --main-module MAX-ELEMENT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Both exited 0. Logs:
[`09-build-runtime.log`](/audit-output/evidence/09-build-runtime.log) and
[`10-build-proof.log`](/audit-output/evidence/10-build-proof.log).

The LLVM build warned that several supplied, unrelated `[total]` functions are
not syntactically exhaustive (`mapStrVS`, `floorFI`, `toF`, `ceilF`,
`joinCodes`, and `valSeqAt`). None is reachable from this program/proof slice.
The Haskell proof build emitted only unused-variable warnings in supplied
`strLt` rules. These warnings are addressed more precisely in stage 5; none is
being recharacterized as an unsound rule without a false-conclusion witness.

### Positive proof claims

The original four-claim candidate spec was first run unchanged:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module MAX-ELEMENT-SPEC
#Top
[exit_status] 0
```

See
[`11-kprove-all-positive.log`](/audit-output/evidence/11-kprove-all-positive.log).

I then made a reviewer copy that adds labels but does not change any claim
term, cell, precondition, or postcondition. Every positive target was selected
separately. The universal entry claim was selected together with its declared
max-accumulator auxiliary claim, because filtering the auxiliary out would
change the proof dependency set.

| Target | Selection | Result |
|---|---|---|
| Max-accumulator auxiliary | `MAX-ELEMENT-SPEC-LABELED.max-acc` | exit 0, `#Top` |
| Universal entry plus its auxiliary | `max-acc,universal-entry` | exit 0, `#Top` |
| Prompt example `[1,2,3]` | `example-one` | exit 0, `#Top` |
| Eleven-element prompt example | `example-two` | exit 0, `#Top` |

The labeled source and exact logs are
[`spec-labeled.k`](/audit-output/evidence/spec-labeled.k),
[`12-kprove-max-acc.log`](/audit-output/evidence/12-kprove-max-acc.log),
[`13-kprove-universal-with-lemma.log`](/audit-output/evidence/13-kprove-universal-with-lemma.log),
[`14-kprove-example-one.log`](/audit-output/evidence/14-kprove-example-one.log),
and
[`15-kprove-example-two.log`](/audit-output/evidence/15-kprove-example-two.log).

### Independent concrete execution

I translated a fresh assertion harness with the trusted translator and ran it
against the freshly built LLVM definition. It covers both prompt examples,
singletons, increasing/decreasing/equal transitions, the stage-4 witness, and
signed 64-bit boundaries. `krun` ended with:

```text
<k> .K </k>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
[exit_status] 0
```

Sources and logs:
[`concrete_semantics_tests.py`](/audit-output/evidence/concrete_semantics_tests.py),
[`16-generate-concrete-harness.log`](/audit-output/evidence/16-generate-concrete-harness.log),
and
[`17-krun-concrete-harness.log`](/audit-output/evidence/17-krun-concrete-harness.log).

## 4. Adequacy and real-program pinning

### Plain-language meaning of each candidate claim

1. **Max-accumulator auxiliary (`spec.k:7`)**: for any integer accumulator
   `ACC`, finite integer sequence `REST`, and arbitrary continuation `CONT`,
   executing the supplied builtin-max continuation over the proof
   representation of `REST` produces the left-fold maximum
   `maxOf(ACC, REST)` and preserves `CONT`.
2. **Universal entry (`spec.k:13`)**: from the ordinary initial module state,
   load the exact submitted module and call `max_element` on a semantic list
   whose first element is integer `FIRST` and whose finite integer tail is
   `REST`. The returned K value is exactly `maxOf(FIRST, REST)`. The call
   restores environment location 0, scope location 1, empty heap/stack,
   `noRet`, and `NoExc`; only the final scope map is existentially framed.
3. **First example (`spec.k:30`)**: the same actual module/call returns exactly
   `3` for `[1,2,3]`.
4. **Second example (`spec.k:46`)**: the same actual module/call returns exactly
   `123` for the eleven-element example.

There is no free result variable, tautological implication, or merely
one-directional relation. The right-hand side of `<k>` is the exact result
term.

### Exact program execution

`verification.k:9-12` expands `maxElementProgram` to:

```text
Module(
  FuncDef("max_element", Params("l"),
    Return(Call(Name("max"), Name("l")))))
```

This is byte-for-byte the submitted `solution.mpy` AST. The claim begins with
`#loadAll(maxElementProgram)`, so the fixed supplied rules execute:

- module statement sequencing and `FuncDef` closure installation;
- lookup of the `max_element` closure;
- argument binding in a fresh call frame;
- the real `Return(Call(Name("max"), Name("l")))` body;
- normal lookup of `max` through the builtin scope;
- left-to-right argument evaluation;
- the supplied builtin `max` iterator fold; and
- return/frame restoration.

There is no rule that directly rewrites a `max_element` call to its desired
answer.

### Satisfying state and concrete substitution

One satisfying universal precondition is:

```text
FIRST = 2
REST  = iCons(-1, iCons(9, iCons(9, iCons(0, .IntSeq))))
input = [2, -1, 9, 9, 0]
```

with the initial cells shown in the candidate claim. The expected
`maxOf(FIRST,REST)` is 9.

The reviewer ground K claim closes with exit 0 and `#Top`; both trusted
canonical Python and submitted Python return 9. Evidence:
[`spec-ground-witness.k`](/audit-output/evidence/spec-ground-witness.k),
[`18-kprove-ground-witness.log`](/audit-output/evidence/18-kprove-ground-witness.log),
and
[`19-python-ground-witness.log`](/audit-output/evidence/19-python-ground-witness.log).

### Body sensitivity

To test whether the theorem was insensitive to the submitted body, I created a
distinct reviewer definition changing only the function body to
`return l[0]`. That definition built successfully. The original maximum
obligation on `[2,-1,9,0]` then failed with a meaningful stuck state:

```text
<k> 2 ~> .K </k>
destination: 9
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
[exit_status] 1
```

This is direct evidence that the positive proof pins and depends on the actual
submitted body. See
[`verification-body-mutated.k`](/audit-output/evidence/verification-body-mutated.k),
[`spec-body-sensitivity.k`](/audit-output/evidence/spec-body-sensitivity.k),
and logs
[`25-build-body-mutated.log`](/audit-output/evidence/25-build-body-mutated.log)
through
[`27-body-sensitivity-expected-failure.log`](/audit-output/evidence/27-body-sensitivity-expected-failure.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The line-addressed inventory covers every local configuration, syntax
declaration, context, rule, and claim in the selected semantics tree,
`verification.k`, and `spec.k`. It contains 940 declarations:

```text
configuration=1
syntax=230
context=5
rule=700
claim=4
```

An independent textual cross-check found 151 `[function]` attribute
occurrences, 116 `[total]`, zero `[functional]`, 25 `symbol(...)`, 47
`[priority(...)]`, zero `[simplification]`, 40 `[concrete]`, and 29 `[owise]`.
Every declaration is reproduced in a single line with source path, line,
category, attributes, and normalized body in
[`20-rule-inventory.tsv`](/audit-output/evidence/20-rule-inventory.tsv).
The generator and cross-check are
[`inventory_k.py`](/audit-output/evidence/inventory_k.py) and
[`28-inventory-cross-check.log`](/audit-output/evidence/28-inventory-cross-check.log).

Per-file declaration counts are:

| File | Config | Syntax | Context | Rules | Claims |
|---|---:|---:|---:|---:|---:|
| `semantics/assert.k` | 0 | 0 | 0 | 3 | 0 |
| `semantics/bool.k` | 0 | 0 | 1 | 13 | 0 |
| `semantics/builtins.k` | 0 | 38 | 0 | 137 | 0 |
| `semantics/call.k` | 0 | 3 | 0 | 21 | 0 |
| `semantics/comprehension.k` | 0 | 3 | 0 | 7 | 0 |
| `semantics/concrete.k` | 0 | 5 | 0 | 16 | 0 |
| `semantics/controls.k` | 0 | 3 | 0 | 34 | 0 |
| `semantics/core.k` | 1 | 37 | 0 | 46 | 0 |
| `semantics/dict.k` | 0 | 12 | 0 | 28 | 0 |
| `semantics/float.k` | 0 | 34 | 0 | 121 | 0 |
| `semantics/functions.k` | 0 | 4 | 0 | 15 | 0 |
| `semantics/int.k` | 0 | 1 | 0 | 16 | 0 |
| `semantics/iter.k` | 0 | 1 | 0 | 0 | 0 |
| `semantics/list.k` | 0 | 5 | 0 | 27 | 0 |
| `semantics/methods.k` | 0 | 27 | 0 | 75 | 0 |
| `semantics/operators.k` | 0 | 0 | 2 | 10 | 0 |
| `semantics/range.k` | 0 | 2 | 0 | 6 | 0 |
| `semantics/set.k` | 0 | 6 | 0 | 12 | 0 |
| `semantics/sort.k` | 0 | 6 | 0 | 19 | 0 |
| `semantics/str.k` | 0 | 5 | 0 | 28 | 0 |
| `semantics/subscript.k` | 0 | 15 | 2 | 40 | 0 |
| `semantics/syntax.k` | 0 | 16 | 0 | 0 | 0 |
| `semantics/tuple.k` | 0 | 4 | 0 | 21 | 0 |
| assembled `semantics.k` | 0 | 0 | 0 | 0 | 0 |
| `verification.k` | 0 | 3 | 0 | 5 | 0 |
| `spec.k` | 0 | 0 | 0 | 0 | 4 |

The assembled `semantics.k` contains the `MPY` and `MPY-KRUN` module/import
assembly rather than local declarations. The totals above account for all
local declarations. There are 695 supplied-semantics rules and five
proof-local rules.

### Disposition of the supplied rules

In `SUPPLIED_SEMANTICS` mode the byte-identical trusted reference tree is the
selected fixed semantic level. Accordingly, each of the 695 baseline rules is
classified in the inventory as part of that fixed model, not as a
candidate-proposed proof axiom. `semantics/concrete.k` is imported by the LLVM
`MPY-KRUN` module but not by the Haskell proof module `MPY`; its 16 rules cannot
contribute to `kprove`.

I reviewed the complete fixed-semantics execution slice used by the program,
not merely rule names. Source is retained in
[`22-execution-slice-source.log`](/audit-output/evidence/22-execution-slice-source.log).
The used constructs map as follows:

| Submitted construct/value | Declaration and executing rules |
|---|---|
| `Module(Stmts)` | `syntax.k:61`; `core.k:124-127` loads and sequences statements |
| `FuncDef` / `Params` | `syntax.k:53,57,60`; `functions.k:14-16` installs the exact closure |
| `Return` | `syntax.k:50 [strict]`; `functions.k:78-90` records the value, pops, restores continuation and cells |
| `Call` | `syntax.k:28`; `call.k:20-21` evaluates callee then arguments |
| `Name` | `syntax.k:12`; `core.k:131-154` performs scoped lookup |
| function call frame | `call.k:69-74`; `functions.k:63-66,78-90` binds, executes, and returns |
| builtin `max` binding | `core.k:157-181`, specifically `"max" <- builtinV("max")` |
| builtin `max` dispatch | `call.k:29` to `#maxAcc0` |
| integer iterable maximum | `builtins.k:75-84`, using first-element seeding, `#iterNext`, `isInt`, and `maxInt` |
| list/value sequence | `core.k:13-29`; fixed list iterator `list.k:9-10` |
| integer arithmetic | imported trusted K `INT` theory, particularly `maxInt` |

Control is deterministic on the formal domain: `FIRST` seeds the maximum,
every `IntSeq` element satisfies the `isInt` guards, and the non-empty
precondition avoids the baseline's intentionally unmodeled empty-`max`
exception. Argument evaluation is left-to-right; lookup observes ordinary
shadowing; the call allocates then removes its local scope; no heap allocation
is needed for the bare read-only semantic list input; and return restores the
caller continuation rather than bypassing it.

The 25 explicit `symbol(...)` declarations are:

```text
sortVS sortKeyVS
intFloatDiv divII floatMod floatLt absF floorFI toF ceilF
subF divF addF mulF powF gtF eqF decStrToF divFloatIntV intToF
truncF roundF roundFN sqrtF
md5hexCodes
```

The supplied tree also deliberately leaves terms such as symbolic `strLt` or
out-of-bounds/opaque `valSeqAt` unreduced. None of these symbols occurs in the
submitted AST, formal input, `maxOf`, `intVals`, or any proof path. The exact
opaque/trusted/priority scan is
[`21-opaque-and-priority-scan.log`](/audit-output/evidence/21-opaque-and-priority-scan.log).
They have no value, control, state, exception, or postcondition influence here.

The compiler's non-exhaustiveness warnings concern unused supplied symbols.
Because no concrete or symbolic false conclusion witness exists on this
theorem's non-empty integer-list domain, I do **not** label those baseline
warnings unsound. The narrower finding is an unused whole-language coverage
gap outside the current execution slice.

### Exhaustive proof-local extension review

`verification.k` adds exactly three syntax declarations and five rules:

| Extension | Class and complete domain | Soundness decision |
|---|---|---|
| `maxElementProgram : Module [function,total]` | Definitional nullary constant | Its sole rule expands to the exact trusted translation of `solution.py`. Complete, disjoint, and no state/control effect. |
| `intVals(IntSeq) : ValSeq` | Proof-only structural representation | It introduces no unconstrained result or oracle. Its only observable behavior used by this program is exhaustively fixed by the two iterator rules below. |
| `maxOf(Int,IntSeq) : Int [function,total]` | Mathematical fold summary | Base rule returns the accumulator on `.IntSeq`; step rule applies `maxInt` and strictly recurses on `R`. The constructors are exhaustive and disjoint, the recursion descends, and there is no overlap. |
| `maxElementProgram => Module(...)` | Definitional rule | Exact AST identity is independently checked. It names the body but does not replace its execution. |
| `maxOf(M,.IntSeq) => M` | Definitional equation | Ordinary fold base; true over its complete constructor case. |
| `maxOf(M,iCons(I,R)) => maxOf(maxInt(M,I),R)` | Definitional equation | Ordinary fold step; true over its complete constructor case. |
| empty `intVals` iterator rule | Representation transition over exactly `intVals(.IntSeq)` and arbitrary continuation | Produces `#iterDone`, matching fixed list iteration on the corresponding `.ValSeq`. Reads/writes only `<k>`, preserves `CONT`, all other cells, stack, return, and exceptions. |
| cons `intVals` iterator rule | Representation transition over exactly `intVals(iCons(I,R))` and arbitrary continuation | Yields exactly integer `I` and the representation of `R`, matching fixed list iteration on `vCons(I,...)`. Same state/control footprint as the fixed rule. |

The two `[priority(40)]` iterator rules have disjoint constructor guards. They
do not overlap the supplied `.ValSeq` or `vCons` list-iterator patterns, so
priority cannot preempt a fixed-semantics transition. Neither rule introduces
return, exception, frame popping, allocation, or state mutation.

`intVals` is not a submitted-language construct and does not replace a program
body. It is a specification-side way to quantify over an arbitrary finite
integer tail. Nevertheless, because it affects the final result, I checked its
connection to ordinary fixed-semantics lists independently. A separate
definition expands an `IntSeq` structurally to ordinary `.ValSeq`/`vCons` and
adds **no** `#iterNext` rule. Two bridge-free claims then cover the complete
empty/cons match domain:

```text
#iterNext(list(.ValSeq)) => #iterDone
#iterNext(list(vCons(I,expandIntVals(R))))
  => #iterYield(I,list(expandIntVals(R)))
```

Both preserve arbitrary `CONT`; both closed together with exit 0 and `#Top`
using only the supplied list iterator. See
[`connection-verification.k`](/audit-output/evidence/connection-verification.k),
[`connection-step-spec.k`](/audit-output/evidence/connection-step-spec.k),
[`29-build-bridge-free-connection.log`](/audit-output/evidence/29-build-bridge-free-connection.log),
and
[`31-kprove-bridge-free-step-connection.log`](/audit-output/evidence/31-kprove-bridge-free-step-connection.log).
By structural induction on the exhaustive `IntSeq` constructors, this is the
same sequence of fixed iterator observations used by builtin `max`.

The four `spec.k` claims are proof obligations/circularities, not ordinary
semantic rules. The max-accumulator auxiliary follows the actual builtin-max
control flow one iterator step at a time; the three entry claims start from
real module load/call configurations. No simplification rule, candidate opaque
symbol, priority overlap, totality hole, fabricated result, or
execution-bypassing call rewrite was found. Therefore I make no unsound-rule
finding and have no false-conclusion witness to report.

## 6. Fresh non-vacuity test

I ignored any candidate vacuity evidence (none was present) and created a fresh
module that retains the max-accumulator auxiliary but changes the universal
postcondition from:

```text
maxOf(FIRST, REST)
```

to:

```text
maxOf(FIRST, REST) +Int 1
```

This is false for every satisfying input; the stage-4 witness should return 9,
not 10. `kprove --dry-run` built the mutation successfully with exit 0. The
actual proof then exited 1 with `WarnStuckClaimState`, and the residual showed
the exact unmet result obligation:

```text
#Not ( {
  maxOf ( FIRST , REST ) +Int 1
#Equals
  maxOf ( FIRST , REST )
} )
[Error] Prover: backend terminated because the configuration cannot be
rewritten further.
[exit_status] 1
```

This is a semantic proof failure, not a parse error, missing import, timeout, or
unreachable mutation. Source and exact logs:
[`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k),
[`23-vacuity-dry-run.log`](/audit-output/evidence/23-vacuity-dry-run.log), and
[`24-vacuity-kprove-expected-failure.log`](/audit-output/evidence/24-vacuity-kprove-expected-failure.log).

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Under the supplied MPY semantics and imported K integer theory, for every
`FIRST:Int` and finite `REST:IntSeq`, starting from the stated clean module
configuration and executing the exact submitted MPY module's `max_element`
function on the semantic list `[FIRST] ++ REST` returns:

```text
maxOf(FIRST, REST)
```

with normal return (`noRet` restored), no modeled exception, empty call stack,
restored environment/scope location, and the result in `<k>`. `maxOf` is the
left fold of mathematical `maxInt`, so ordinary induction identifies it with
the maximum of a non-empty integer sequence. The two prompt examples are also
separately proved.

This is partial correctness over finite non-empty integer lists. It does not
prove behavior for empty lists, floats, strings, mixed or incomparable values,
NaNs, infinite iterables, custom comparison methods, or Python exception
classes.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| Trusted supplied semantics tree | Defines all program execution, control, state, and builtin `max` behavior | Required by `SUPPLIED_SEMANTICS`; candidate copy is exactly identical. Used slice statically reviewed and concretely exercised. |
| K parser/compiler/Haskell prover and LLVM runtime | Establish build, symbolic closure, and concrete execution | Standard proof checker/runtime trust boundary; fresh K 7.1.337 runs and exact statuses recorded. |
| Imported K `INT`, `BOOL`, `MAP`, `LIST`, string theories, especially `maxInt` | Fixes arithmetic, maps, lists, and the fold comparison | Low-level selected-semantics primitive. `maxInt` is the only result-bearing imported math primitive here. |
| Trusted translator `/reference/py2mpy.py` | Connects `solution.py` to submitted AST | Explicit trusted input; regeneration is byte-identical. |
| `maxElementProgram` definitional constant | Pins the entry claims to the submitted body | Exact AST identity plus body-sensitivity failure. Not an oracle. |
| `maxOf` equations | Names the postcondition value | Exhaustive, disjoint, descending equations over `IntSeq`; ordinary maximum fold. |
| `intVals` representation rules | Supply iterator observations for an arbitrary symbolic integer tail | Exhaustive empty/cons rules, fixed state/control footprint, bridge-free fixed-list step claims, concrete/ground witnesses. Not a free or opaque value. |
| Python builtin `max` / canonical-Python bridge | Connects modeled MPY behavior to actual Python executions | Finite empirical support over 5,920 formal-domain inputs with zero mismatches; not treated as a universal proof. |
| Prompt-to-formal-domain interpretation | Determines whether integer-only theorem covers all intended inputs | Main documented concern: prompt says `list`, while formal theorem says non-empty integer sequence. |
| Missing generation telemetry | Affects provenance/history only | Concerning auditability gap, but no dependency of the reconstructed proof result. |

### Gate summary

- Real-program soundness: **pass**. Exact program executes; proof-local
  equations are sound on complete domains; fixed-list connection closes;
  satisfying witness exists; body and false-result mutations are rejected.
- Intent adequacy: **pass with limitation**. Exact maximum is proved for
  non-empty integer lists, which covers all documented examples but is narrower
  than an unconstrained reading of `list`.
- Trust/evidence auditability: **pass with concern**. Commands, outputs, source,
  inputs, and mutations are reproducible, but candidate generation telemetry is
  absent and the Python bridge remains finite empirical evidence.

No timeout, malformed mount, unavailable required tool, or other infrastructure
uncertainty was converted into a candidate verdict.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
