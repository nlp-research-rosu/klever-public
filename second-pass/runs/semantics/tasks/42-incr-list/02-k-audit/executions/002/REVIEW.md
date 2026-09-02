# Independent adversarial review: 42-incr-list

The candidate has a clean, non-vacuous K proof of a narrower theorem over
arbitrary finite lists of K integers. It does not prove the full source
contract as written: `prompt.py` accepts `l: list` and gives no integer-only
precondition, while the formal entry claim admits only `IntSeq`. Standard,
terminating source cases such as lists of floats and booleans are implemented
by both Python functions but are outside the theorem. Under this audit prompt's
explicit mapping, that material domain restriction makes the candidate
`FAIL / NOT_LEGIT`, even though the integer-list theorem itself reconstructs
and is result-constraining.

All candidate prose, historical logs, and prior `#Top` output were treated only
as untrusted claims. The command ledger is
[`evidence/COMMANDS.md`](/audit-output/evidence/COMMANDS.md).

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `42-incr-list`;
- condition `semantics`;
- record layout `legacy-selected-stage1`;
- semantics mode `SUPPLIED_SEMANTICS`;
- a mounted trusted semantics tree at
  `/reference/reference-semantics`.

I independently inspected `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all required generation records, and the structured
trace. For this legacy-selected layout, `runtime-metrics.json` is historically
unrecorded and not required; `usage.json` is present and was inspected. The
single structured-trace file is a regular 739,332-byte JSONL file with 465
valid records (142 `event_msg`, 320 `response_item`, and three session/context
records). Generation records were not used as proof evidence.

The independent check in
[`provenance-check.log`](/audit-output/evidence/provenance-check.log) established:

- the campaign lock JSON exactly equals the `audit_campaign` block, and its
  SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- every launcher-required record is present, readable, a regular file, and has
  its recorded SHA-256;
- every evidence file listed by `/generation-result.json` has its listed
  digest, including the trace file digest
  `ad8dab29d89318f396e70a68f1fda32cd0082a4bb399ac452a90392b100cac82`;
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`;
- all 35 candidate tree entries are ordinary directories or regular files;
  there are no candidate symlinks or special-file substitutions;
- the candidate and trusted `reference-semantics/` trees have exactly the
  same relative entries, types, and file bytes. Their independently generated
  manifest digests are both
  `e503b4cef294664c4fc2cb2f8e7145e948fc4aa5f631859f7641dd05bc2a5d94`;
- all five required proof deliverables are regular files.

The supplied-semantics mount is present as required. There is no rendered-mode
contradiction and no audit infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt says: given `l: list`, return a list whose elements are each
incremented by 1. Its examples require:

```text
[1, 2, 3] -> [2, 3, 4]
[5, 3, 5, 2, 3, 3, 9, 0, 123]
  -> [6, 4, 6, 3, 4, 4, 10, 1, 124]
```

The trusted canonical implementation is the list comprehension
`[(e + 1) for e in l]`. The candidate in `/candidate/solution.py` allocates an
empty result list, iterates over `l`, appends `x + 1`, and returns the result.
For ordinary lists on which `e + 1` is defined, this is the same algorithmic
behavior and it does not mutate the input list.

### Trusted translation identity

I regenerated the constructor program with the trusted mounted translator:

```text
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
```

`cmp` exited 0. Both the regenerated file and submitted
`/candidate/solution.mpy` have SHA-256
`811ba0bc5a0aa8ce22bfa580e3e6d165e2638b036e676be0f25b8a4acf753125`.
See
[`translation-identity.log`](/audit-output/evidence/translation-identity.log)
and
[`regenerated-solution.mpy`](/audit-output/evidence/regenerated-solution.mpy).

### Independent differential test

[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted canonical entry point and candidate entry point independently. It
tests the two documented examples, empty/singleton and sign boundaries,
repeated values, arbitrary-precision integers, floats, booleans, all lengths
0 through 16, and 100 reproducible generated integer lists up to length 40.
The independently implemented oracle is
`/reference/canonical.py::incr_list`.

The run covered 128 inputs and found zero mismatches; exit status was 0. See
[`differential-test.log`](/audit-output/evidence/differential-test.log).
This is finite implementation evidence, not a universal K proof.

## 3. Clean proof reconstruction

Only source artifacts were copied into `/tmp/audit-work/reconstruction`.
No candidate-built definition, `.kompiled` directory, cache, or proof result
was copied. The selected semantics came from the trusted reference mount.

The live toolchain is K 7.1.293. `kup` is absent, but independently installed
`kompile`, `krun`, and `kprove` are present and operational; this remains the
Kit live-verification path. See
[`toolchain-version.log`](/audit-output/evidence/toolchain-version.log).

Fresh reconstruction results:

| Check | Result | Evidence |
|---|---|---|
| LLVM compile of trusted `MPY-KRUN` | exit 0 | [`llvm-kompile.log`](/audit-output/evidence/llvm-kompile.log) |
| Independent concrete K tests | exit 0; final `.K`, `NoExc`, exit-code 0 | [`llvm-concrete-with-ground-witness.log`](/audit-output/evidence/llvm-concrete-with-ground-witness.log) |
| Haskell compile of scratch `verification.k` | exit 0 | [`haskell-kompile.log`](/audit-output/evidence/haskell-kompile.log) |
| Complete `SPEC` proof | exit 0 and `#Top` | [`kprove-all-positive.log`](/audit-output/evidence/kprove-all-positive.log) |
| Explicit selection of both labels | exit 0 and `#Top` | [`kprove-both-labeled.log`](/audit-output/evidence/kprove-both-labeled.log) |
| `SPEC.incr-loop` alone | exit 0 and `#Top` | [`kprove-incr-loop.log`](/audit-output/evidence/kprove-incr-loop.log) |

The end-to-end claim has `[depends(incr-loop)]`; selecting only
`SPEC.incr-list` removes the required dependency from the proof set and is not
the candidate's positive target command. The complete and explicit two-label
runs independently execute every positive target claim and both satisfy the
Kit success condition: exit 0 plus literal `#Top`.

Kompilation warnings concern unused, fixed-semantics cases such as
`mapStrVS`, `floorFI`, and `valSeqAt`. They are not candidate rules and are not
reachable in this integer-list program.

## 4. Adequacy and real-program pinning

### Claims in plain language

`incr-loop` starts at the real fixed-semantics loop head
`#loop(list(intVals(IS)), Name("x"), incrLoopBody)`. Its precondition requires
the current function scope to contain `l`, a `result` reference to heap
location `H`, and an existing `x` binding; the heap object at `H` contains an
arbitrary prefix. It says that, when the loop reaches its continuation, the
same heap object contains that prefix concatenated with every integer in `IS`
incremented by 1. Other scopes and heap entries are framed, and the final `x`
value is existential because it is irrelevant to the output.

The `x` precondition is consistent with real control flow. On an end-to-end
call, the prover executes the first nonempty iteration concretely, which
creates `x`; the circularity then summarizes the remaining loop. The empty
case terminates directly. There is no size bound.

`incr-list` starts in the supplied default module configuration, loads
`solutionProgram`, calls its `incr_list` binding on
`list(intVals(IS))`, then observes the returned heap object. Its formal input
domain is every finite `IntSeq`, with unbounded K integers and unbounded
length. At the destination, `?RESULT` is not free:

```text
ensures ?RESULT ==K incrVals(IS)
```

`incrVals` is recursively defined as element-wise K integer addition by 1.
The claim also preserves an empty stack, `noRet`, and `NoExc`; final scopes,
heap, and allocation counter are existential because they are not part of the
functional postcondition.

### Satisfiable entry and substituted result

[`ground-witness.k`](/audit-output/evidence/ground-witness.k) instantiates the
entry state with `IS = [1, -2, 0]` and substitutes the result
`[2, -1, 1]`. It exits 0 with `#Top`; see
[`kprove-ground-witness.log`](/audit-output/evidence/kprove-ground-witness.log).
The trusted canonical Python function, candidate Python function, and fresh
concrete fixed-semantics run all produce `[2, -1, 1]`.

### Mechanical program identity

The identity chain is:

```text
candidate solution.py
  --trusted py2mpy, byte identity-->
candidate solution.mpy
  --constructor normalization-->
verification.k::solutionProgram
```

The only normalization is making K list units explicit
(`.Exprs`/`.Stmts`), which is semantically inert. The configuration-form
constructor identity claim in
[`program-identity.k`](/audit-output/evidence/program-identity.k) exits 0 with
`#Top`; the backend reports `WarnTrivialClaim`, meaning the frontend already
normalized the two constructor terms to identity. Earlier parser/functional
claim experiments were rejected and are not counted as evidence. See
[`kprove-program-identity-config.log`](/audit-output/evidence/kprove-program-identity-config.log).

The `<k>` cell therefore loads and calls the actual submitted function binding
and body. The proof does not replace the function call with a result oracle.

### Body sensitivity

I changed the embedded executed body—not merely `solution.py`—from
`BinOp("+", Name("x"), Int(1))` to `Int(2)`, leaving the invariant and
postcondition unchanged. The mutated definition built successfully. Its proof
exited 1 with a reachable `WarnStuckClaimState` showing the precise unmet
obligation:

```text
#Not ( I +Int 1 #Equals I +Int 2 )
```

The residual contains the mutated closure body and a returned singleton
`I +Int 2`. See
[`body-mutated-verification.k`](/audit-output/evidence/body-mutated-verification.k),
[`body-mutation-build.log`](/audit-output/evidence/body-mutation-build.log),
and
[`body-mutation-kprove.log`](/audit-output/evidence/body-mutation-kprove.log).
This establishes material body sensitivity.

### Material adequacy failure

The formal precondition is strictly integer-only:

```text
list(intVals(IS:IntSeq))
```

In the supplied semantics, `Int`, `Bool`, and `Float` are distinct `Val`
constructors. No `IntSeq` instance represents a float or boolean list. The
trusted source prompt says only `l: list`; it does not state an integer-element
precondition. This is not merely a pathological Python extension case:

```text
incr_list([1.5, -2.25, 0.0]) == [2.5, -1.25, 1.0]
incr_list([False, True])      == [1, 2]
```

Both trusted canonical Python and candidate Python produce these results, as
recorded by the independent differential run, but neither case satisfies the
K entry precondition. Standard numeric-list behavior is therefore excluded.
The theorem is universal and unbounded inside the integer subdomain, but it
materially narrows the source-contract domain. The benchmark prompt requires a
Kit `SOUND-BUT-LIMITED` result for this kind of narrowing to map to
`FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule_inventory.py`](/audit-output/evidence/rule_inventory.py) inventories
every directive and complete source block in the trusted semantics,
`verification.k`, and `spec.k`. The complete output is
[`rule-inventory.log`](/audit-output/evidence/rule-inventory.log):

| Kind | Count |
|---|---:|
| Syntax declarations | 231 |
| Rules | 704 |
| Contexts | 5 |
| Configurations | 1 |
| Claims | 2 |
| Total directives | 943 |

Of these, 227 syntax declarations, 695 rules, all five contexts, and the one
configuration are the byte-checked supplied semantics. They are the fixed
semantic level selected by `SUPPLIED_SEMANTICS`, not candidate extensions.
I treated each as a fixed theorem assumption and checked that rules outside the
program's constructor/control path have no matching redex on this proof.
The candidate contributes four syntax declarations and nine rules, reviewed
individually below. There is no candidate `[functional]` declaration, priority
rule, `owise` rule, or opaque result symbol.

The fixed supplied theory contains 25 explicitly symbolic/opaque
`symbol(...)` functions:

```text
sortVS, sortKeyVS,
intFloatDiv, divII, floatMod, floatLt, absF, floorFI, toF, ceilF,
subF, divF, addF, mulF, powF, gtF, eqF, decStrToF,
divFloatIntV, intToF, truncF, roundF, roundFN, sqrtF,
md5hexCodes
```

None is reachable from this program or occurs in either claim or candidate
extension. Thus none influences control, state, result, or postcondition here.

### Used-construct map and fixed-semantics path

| Submitted construct/operation | Declaration and material fixed rules |
|---|---|
| `Module`, statement lists | `syntax.k:56-61`; `core.k:124-127` loads and sequences every statement |
| `FuncDef`, call frame | `syntax.k:53`; `functions.k:14-16`; `call.k:69-75` binds the selected closure and preserves caller continuation |
| Parameter binding, return | `functions.k:63-66,78-90` binds `l`, records the return, restores environment/stack, and resumes the observer |
| `Str` docstring, `Expr` discard | `syntax.k:13,52`; `str.k:13-17`; `controls.k:48` |
| `Assign(result, ListExpr())` | `syntax.k:17,41`; `list.k:13-15`; `core.k:117-121`; `controls.k:9-11` allocates a fresh list and binds its reference |
| `Name` lookup | `core.k:130-154` follows the current lexical scope and selected binding |
| `For` and target bind | `syntax.k:45`; `controls.k:65-74`; `tuple.k:31-34` evaluates the iterable once, requests each element, binds `x`, executes the body, and resumes the loop |
| List iteration | fixed concrete cases `list.k:9-10`; the candidate's exact symbolic representation cases `verification.k:30-32` |
| `Call(Attribute(...append), ...)` | `syntax.k:28-29`; `call.k:16,20-24`; `core.k:185-191`; `list.k:53-55` evaluates callee/argument and mutates the exact `result` heap object |
| `BinOp("+", x, Int(1))` | `syntax.k:9,15`; `core.k:194`; `operators.k:12`; `int.k:9` uses unbounded mathematical integer addition |
| `Return(result)` | `syntax.k:50`; `functions.k:78-90` returns the result reference through the saved continuation |

Evaluation order is preserved: `BinOp` is `seqstrict(2,3)`, the statement
constructs have the relevant strict positions, and calls explicitly evaluate
the callee before arguments, with arguments accumulated left-to-right. Heap
allocation is fresh and monotonic; append updates the same heap location;
return restores call state; the proof observer reads rather than mutates that
location. No material operation or control effect is skipped.

### Candidate declarations

1. `solutionProgram : Module` is `[function,total]` and has one zero-argument
   equation.
2. `intVals(IntSeq)` is a constructor used as the symbolic input sequence
   representation. It is not declared a function or result oracle.
3. `incrVals(IntSeq)` is `[function,total]`.
4. `incrLoopBody : Stmts` is `[function,total]` with one zero-argument
   equation.
5. `#observeResult` is a fresh specification-only `KItem`.

All total declarations have complete, non-overlapping equations over their
declared domains.

### Candidate rules

| Location | Rule and class | Static decision |
|---|---|---|
| `verification.k:8-18` | `solutionProgram => Module(...)`; definitional constant | Exact constructor tree, mechanically checked. It names but does not replace execution. |
| `verification.k:24` | `incrVals(.IntSeq) => .ValSeq`; definitional summary | Correct empty element-wise increment case. |
| `verification.k:25-26` | cons case of `incrVals`; definitional summary | Correctly emits `I +Int 1`, recursively descends on `IS`, and is disjoint from the empty case. |
| `verification.k:30` | empty `intVals` iterator; operational representation bridge | Mirrors fixed `list.k:9` exactly: same complete `<k>` context, arbitrary preserved suffix, no state cells, and `#iterDone`. |
| `verification.k:31-32` | cons `intVals` iterator; operational representation bridge | Mirrors fixed `list.k:10`: yields the head integer, retains the tail representation, preserves the full continuation, and touches no other cell. Empty/cons guards are exhaustive and disjoint, and their distinct constructor prevents overlap with fixed `.ValSeq`/`vCons` rules. |
| `verification.k:35-40` | `incrLoopBody`; definitional constant | Exact constructor subtree of the real `For` body. The body-sensitivity mutation confirms the actual body is used. |
| `verification.k:44-46` | left-to-right reassociation of `valSeqConcat`; derived mathematical lemma | Ordinary associativity of finite sequence concatenation. It decreases left nesting. On overlap with right identity, both reduction paths produce `valSeqConcat(A,B)`. |
| `verification.k:47-48` | right identity of `valSeqConcat`; derived mathematical lemma | Ordinary right identity, derivable by induction for canonical finite `ValSeq`; it removes a concat node and terminates. |
| `verification.k:53-54` | returned-reference observer; trusted specification instrument | Reads the exact heap value at `H`, consumes only the fresh observer tag, preserves any following continuation and every cell, and does not affect program execution before return. |

The iterator equations are the only candidate rules that accelerate a
fixed-semantics operation. Their complete state footprint is only `<k>`, and
their arbitrary continuation matches the equally arbitrary continuation in
the fixed list iterator rules. The ground witness exercises cons and empty
branches with the real loop/body/observer continuation, while the fresh
concrete run executes the corresponding canonical `vCons` list and reaches
the same result and observable state.

There is nevertheless no candidate-supplied, bridge-free universal connection
claim proving that `list(intVals(IS))` denotes the fixed
`list(vCons(...))` encoding for every `IS`. Likewise, the two concat lemmas are
stated over all extended `ValSeq` terms rather than guarded to canonical
prefixes. The equations are truthful under the stated finite-sequence
denotation, and I found no concrete or symbolic false conclusion they enable
on the integer-list entry domain. Per the audit instruction, I therefore
record these as an informal representation/evidence limitation rather than
labeling them unsound. They would prevent claiming a fully self-contained
connection theorem, but they do not smuggle the result: the body, integer
addition, append mutation, and return all execute, and `incrVals` is
independently exhaustively defined.

No rule encodes a fixed answer, introduces an unconstrained result-bearing
oracle, bypasses the function, silently fabricates a used operation, or has a
priority that preempts the real program path.

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`; I created a fresh independent one
in scratch and preserved it as
[`spec-vacuity.k`](/audit-output/evidence/spec-vacuity.k). It keeps the real
program and loop claim but changes the result obligation to:

```text
ensures ?RESULT ==K vCons(0, incrVals(IS))
```

This is demonstrably false for the satisfying empty input: the real result is
`[]`, not `[0]`.

The mutation dry run exited 0, establishing that it parses and builds; see
[`vacuity-dry-run.log`](/audit-output/evidence/vacuity-dry-run.log). The actual
proof exited 1 with `WarnStuckClaimState`, not a parser error, timeout, or
unrelated crash. Its residual specializes `IS == .IntSeq` and shows the
reachable returned `list(.ValSeq)` cannot unify with the demanded leading
zero. See
[`vacuity-kprove.log`](/audit-output/evidence/vacuity-kprove.log).

This test is independent of the body-sensitivity mutation in Stage 4 and
establishes that the original postcondition constrains the returned value.

## 7. Proven versus assumed accounting

### What the successful proof establishes

Conditional on the fixed supplied semantics and the reviewed proof-extension
equations, the successful reachability proof establishes this partial
correctness theorem:

> For every finite `IntSeq IS`, executing the exact submitted `incr_list`
> function from the specified initial K configuration on the symbolic integer
> list represented by `list(intVals(IS))`, if execution reaches the return
> observer, returns a list whose elements are exactly `IS` in order with
> unbounded K integer 1 added to each element, with no exception, an empty
> call stack, and restored return state.

It covers arbitrary integer values and arbitrary finite lengths; it is not a
finite example proof or bounded unrolling.

### Trust ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K 7.1.293 frontend, Haskell backend, reachability/circularity implementation, and K built-in Int/Map/List theories | Both claims and all machine-checking results | Necessary low-level proof-system trust; version and fresh behavior recorded. |
| Byte-identical supplied `MPY` semantics | Meaning of all program constructors and effects | Authorized fixed semantics for `SUPPLIED_SEMANTICS`; not candidate-generated. The theorem is about this subset semantics, not full CPython. |
| `intVals(IS)` denotes the corresponding finite fixed list of K integers | Entry-domain bridge and iterator rules | Informal representation bridge supported by structurally identical iterator equations, ground K evidence, and finite differential/concrete tests; no candidate bridge-free universal connection theorem. Concerning but no false integer-domain witness found. |
| Associativity/right identity of sequence concatenation over the extended symbolic sequence denotation | Loop circularity normalization | Ordinary mathematics; over-broad K guards are an auditability limitation, with agreeing overlaps and no false reachable witness. |
| `#observeResult` means reading the returned heap object by value | End-to-end postcondition | Exact, local specification instrumentation; reads the selected heap entry and does not replace program execution. |
| Trusted translator plus normalized constructor identity | Source-to-K program pinning | Byte equality plus machine-checked constructor identity; body mutation gives independent sensitivity evidence. |
| Python differential run and concrete LLVM runs | Implementation/canonical bridge and ground representation checks | Finite empirical evidence only; not used as universal proof or as a substitute for `kprove`. |

The 25 fixed opaque symbols inventoried in Stage 5 have no dependents in this
theorem. There is no fresh opaque candidate result, empirical result oracle, or
proof rule whose arbitrary interpretation controls the returned value.

### Gates and decision

| Gate | Result |
|---|---|
| Fresh verification | PASS: clean builds; every positive target closes with exit 0 and `#Top`. |
| Real-program soundness/non-vacuity on integer lists | PASS: exact body executes; constructor and ground witnesses close; body and false-result mutations fail meaningfully; no false candidate rule witness was found on this domain. |
| Intent adequacy | **FAIL**: the source contract has no integer-only precondition, but the theorem excludes standard terminating float and boolean lists. |
| Trust/evidence auditability | LIMITED: the `intVals` representation bridge is mathematically direct and finitely supported, but lacks a bridge-free universal K connection theorem. |

Thus the reconstructed artifact is a sound but limited integer-list proof, not
a legitimate proof of the full generated source contract. The benchmark prompt
explicitly requires this material HumanEval-domain narrowing to be reported as
`FAIL / NOT_LEGIT`, rather than `CONCERNS / LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
