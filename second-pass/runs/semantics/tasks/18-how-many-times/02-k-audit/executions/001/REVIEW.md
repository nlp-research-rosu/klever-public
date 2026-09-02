# Independent adversarial audit: 18-how-many-times

The candidate does not contain a legitimate partial-correctness proof of the
submitted program. Its reconstructed claims do close and its postcondition is
non-vacuous, but the decisive entry rule in `verification.k` replaces the
program-defined closure call with a task-specific counting machine before the
supplied semantics performs binding, frame setup, body execution, recursive
lookup, slicing, calls, or returns. There is no bridge-free connection theorem.
Worse, the rule omits all machine-state cells and is false on its complete match
domain. A fresh witness proves `1` with the bridge while fixed supplied
semantics gets stuck at the deliberately wrong recursive binding
`#applyK(toCall(0), ...)`.

All candidate material, including its old `#Top` log, was treated as untrusted.
All executable work used fresh copies under `/tmp/audit-work`; candidate
compiled artifacts were not used. Reviewer scripts, K mutations, and bounded
logs are under `/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so there is no infrastructure
mode contradiction and a candidate verdict is appropriate.

The recursive, non-dereferencing comparison found:

- `/candidate/reference-semantics` and
  `/reference/reference-semantics` have identical entry sets, entry types, and
  bytes. There are no symlinks in either relevant tree.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  SHA-256 is
  `6fc9c00aa6b110ecf79f34e36f14b6b4c9a27128463ef6733b948e32a35c2bfc`.
- `/candidate/py2mpy.py` is byte-identical to
  `/reference/py2mpy.py`; SHA-256 is
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- All candidate entries are ordinary files or directories. The submitted
  `__pycache__/solution.cpython-310.pyc` is an irrelevant generated artifact and
  was neither trusted nor copied into scratch.

The requested provenance files `/candidate/run-input.json`,
`metrics.json`, `codex-last.txt`, and `codex-output.log` are all missing. No
structured generation trace is present. This is a provenance defect. The
present `proof-output.log` and `prove.sh` were read only as claims; the former
asserted an old `#Top`, which was not reused.

Evidence: `evidence/stage1-provenance.sh` and
`evidence/stage1-provenance.log`. The logged integrity command is:

```text
diff -ruN --no-dereference /reference/reference-semantics /candidate/reference-semantics
SEMANTICS_DIFF_EXIT=0
cmp -s /reference/prompt.py /candidate/prompt.py
PROMPT_CMP_EXIT=0
cmp -s /reference/py2mpy.py /candidate/py2mpy.py
TRANSLATOR_CMP_EXIT=0
```

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two strings `string` and `substring`, return the number of starting
positions at which `substring` occurs in `string`, counting overlapping
occurrences. The trusted canonical implementation iterates positions
`0 .. len(string)-len(substring)` and compares the corresponding slice. It
therefore also defines the empty substring to occur at all `len(string)+1`
boundaries.

The submitted implementation expresses the same recurrence:

- empty `substring` returns `len(string)+1`;
- otherwise, empty `string` returns `0`;
- otherwise it adds the indicator for
  `string.startswith(substring)` to the recursive result for `string[1:]`.

This is a different but mathematically appropriate algorithm. It is not total
as a CPython implementation for arbitrarily long strings because recursion can
raise `RecursionError`; that is a termination/intent limitation, not a
different returned value on terminating executions. The requested proof notion
is partial correctness.

### Trusted translation identity

The trusted translator regenerated `solution.mpy` from the submitted
`solution.py`. `cmp` returned zero and both files have SHA-256
`834583ae32fd1dd0b9cf76e7b3aa3fc0e9e1878fce4cda8acbddc80193bb0ae7`.
Thus the K AST is pinned byte-for-byte to the submitted Python source.

### Independent differential test

`evidence/differential.py` independently imports the trusted canonical and
candidate entry points. It tests:

- all three documented examples;
- both empty arguments and each guard boundary;
- exact match, no match, pattern longer than text, prefix/suffix/interior
  matches, and overlapping matches;
- all strings over `{a,b}` of length at most 7 against all patterns of length at
  most 4;
- Unicode examples;
- 1,000 deterministic generated pairs over `abc🙂`, with text lengths below 40
  and pattern lengths below 9.

The complete scope was 8,922 cases with zero mismatches and exit zero:

```text
python=3.10.12
cases=8922
mismatches=0
DIFFERENTIAL_EXIT=0
```

This is finite evidence for the Python rewrite, not a proof or a justification
for the K bridge. Evidence and exact commands:
`evidence/stage2-fidelity.sh`, `evidence/stage2-fidelity.log`, and
`evidence/differential.py`.

## 3. Clean proof reconstruction

Fresh source copies were made in `/tmp/audit-work/rebuild-final`. The semantics
copy came from the trusted `/reference/reference-semantics`, which stage 1
showed byte-identical to the candidate submission. No candidate kompiled
definition or cache was used.

Toolchain:

```text
K version: v7.1.337
Build date: Thu Jun 18 07:59:56 CDT 2026
```

The exact commands are in `evidence/stage3-reconstruct.sh` and the complete
bounded output is in `evidence/stage3-reconstruct.log`. The central commands
were:

```text
kompile .../reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition .../runtime-kompiled
krun .../concrete-tests.mpy --definition .../runtime-kompiled
kompile .../verification.k --backend haskell \
  --main-module HOW-MANY-TIMES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition .../verification-kompiled
kprove .../spec.k --definition .../verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC
```

Results:

| Reconstruction target | Exit | Relevant result |
|---|---:|---|
| LLVM semantics build | 0 | Built from trusted source |
| Concrete translated assertion program | 0 | Final `.K`, `NoExc`, exit code 0 |
| Haskell proof-definition build | 0 | Built from trusted source plus candidate `verification.k` |
| Original two-claim spec | 0 | `#Top` |
| Labeled helper claim alone | 0 | `#Top` |
| Labeled entry claim, using the separately proved helper as a trusted lemma | 0 | `#Top` |

`evidence/spec-labeled.k` differs from the candidate spec only by labels. The
helper was first proved independently. For the dependent entry run, both labels
were selected and only the already proved helper was marked trusted; this
isolates the entry obligation without pretending it is independent of its
invariant. `evidence/stage3-entry-dependent.log` records a second successful
instance of that dependent run.

The compiler emitted supplied-semantics exhaustiveness warnings for unrelated
generic functions such as `mapStrVS`, float conversions, and `valSeqAt`. They
did not prevent either build or any target run and are not an audit
infrastructure failure.

Fresh reconstruction therefore confirms the candidate's limited claim that
`kprove` closes under the extended theory. It does not validate that theory.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

The helper claim has no explicit precondition. For arbitrary finite code
sequence `S`, nonempty pattern `iCons(PC,PS)`, integer accumulator `A`, and
continuation `CONT`, it says the proof-machine term
`#overlapAcc(S, pattern, A)` becomes
`A + overlapCount(S, pattern)` before the same continuation.

The entry claim ranges over arbitrary finite code sequences `S` and `P`. It
assumes:

- the active computation is a direct call to a closure whose parameter names,
  captured scope `0`, and body macro have the submitted shape;
- scope `0` binds `how_many_times` to that closure, has parent `-1`, and may
  contain a disjoint `MODULE` remainder;
- scope `-1` is `builtinsScope`;
- remaining scopes are represented by a disjoint `REST`;
- `NEXT` is fresh in the complete scope map;
- `ret=noRet`, `exc=NoExc`, and exit code is zero;
- caller environment, heap, heap counter, stack, and continuation are otherwise
  arbitrary values of the indicated sorts.

Its postcondition is exact, not a one-way implication: the closure call must
become the integer `overlapCount(S,P)` before the same continuation, with
unrewritten cells framed. There is no free result variable or tautology.

### Satisfiable precondition and concrete substitution

`evidence/spec-ground-entry.k` exhibits a fully ground state:

- `S` is the code sequence for `"aaaa"` and `P` for `"aa"`;
- `CONT=.K`, caller environment `0`, `MODULE=.Map`, and `REST=.Map`;
- scopes have only keys `0` and `-1`;
- `NEXT=1`, heap and stack are empty, and all normal-control cells have the
  required values.

The freshness requirement is true because key `1` is absent. The ground K claim
closed with `#Top`; independent overlap counting, the trusted canonical, and
the submitted Python implementation all returned `3`:

```text
formal_overlapCount=3
canonical=3
candidate=3
GROUND_KPROVE_EXIT=0
```

Evidence: `evidence/ground-comparison.py`,
`evidence/stage4-ground.sh`, and `evidence/stage4-ground.log`.

### Failure to execute the submitted body

The `<k>` term contains the exact closure body only syntactically. Candidate
rule `/candidate/verification.k:106` has priority 30 and rewrites

```text
#applyK(toCall(closureVal(..., howManyTimesBody, 0)), (str(S), str(P), .Vals))
=> #overlapEval(S,P)
```

before the fixed closure-call rule in supplied `call.k:69` can create a frame,
bind parameters, or begin the body. Consequently, the proof does not exercise
the submitted `If`, `Compare`, `len`, `startswith`, slice, recursive lookup,
recursive call, `Return`, stack, or frame-pop behavior. The helper claim matches
only the invented `#overlapAcc` control flow; that symbol never occurs in
`solution.mpy` or the supplied semantics.

The body macro is byte-faithful, and the formal result is the intended result,
but syntactic matching is not an execution connection theorem. This is a
material real-program-pinning failure.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5-inventory.sh` and the 3,997-line
`evidence/stage5-inventory.log` are the exhaustive inventory. For every
supplied semantics file, `verification.k`, and `spec.k`, the log contains:

- counts of syntax declarations, rules, contexts, configurations, and claims;
- every declaration/rule start and every relevant attribute;
- the complete numbered source, so multiline declarations and all alternatives
  are unabridged.

The supplied tree contains 227 top-level syntax declarations, 695 rules, five
contexts, and one configuration. Candidate `verification.k` adds three syntax
declarations and ten rules; `spec.k` has two claims. Counts by file are:

| File | Syntax | Rules | Contexts/config/claims | Audit classification |
|---|---:|---:|---|---|
| `semantics.k` | 0 | 0 | 0 | Assembly/import boundary |
| `assert.k` | 0 | 3 | 0 | Fixed supplied semantics, unused by proof |
| `bool.k` | 0 | 13 | 1 context | Fixed; only generated strictness machinery is incidental |
| `builtins.k` | 38 | 137 | 0 | Fixed; `len` path is used only by bridge-free body execution |
| `call.k` | 3 | 21 | 0 | Fixed; call/frame rules are displaced by candidate bridge |
| `comprehension.k` | 3 | 7 | 0 | Fixed, unused |
| `concrete.k` | 5 | 16 | 0 | Fixed concrete-only runtime leg, not imported in proof module |
| `controls.k` | 3 | 34 | 0 | Fixed; `If`/`IfExp` are displaced |
| `core.k` | 37 | 46 | 1 configuration | Fixed configuration, lookup, evaluation, lengths |
| `dict.k` | 12 | 28 | 0 | Fixed, unused |
| `float.k` | 34 | 121 | 0 | Fixed, unused |
| `functions.k` | 4 | 15 | 0 | Fixed; return/pop rules are displaced |
| `int.k` | 1 | 16 | 0 | Fixed integer addition used by summary and body |
| `iter.k` | 1 | 0 | 0 | Fixed declarations, unused |
| `list.k` | 5 | 27 | 0 | Fixed, unused |
| `methods.k` | 27 | 75 | 0 | Fixed `startswith`; displaced by bridge |
| `operators.k` | 0 | 10 | 2 contexts | Fixed comparisons/addition dispatch; displaced |
| `range.k` | 2 | 6 | 0 | Fixed, unused |
| `set.k` | 6 | 12 | 0 | Fixed, unused |
| `sort.k` | 6 | 19 | 0 | Fixed, unused |
| `str.k` | 5 | 28 | 0 | Fixed string equality/helpers |
| `subscript.k` | 15 | 40 | 2 contexts | Fixed `string[1:]`; displaced |
| `syntax.k` | 16 | 0 | 0 | Fixed AST syntax |
| `tuple.k` | 4 | 21 | 0 | Fixed, unused |
| `verification.k` | 3 | 10 | 0 | Candidate extensions, analyzed individually below |
| `spec.k` | 0 | 0 | 2 claims | Candidate proof obligations |

For purposes of the theorem, all 695 rules in the byte-verified reference tree
are the selected fixed supplied semantics, not candidate proof extensions.
Every one is enumerated in the inventory. The complete tree was inspected for
interactions with the candidate additions. No supplied rule was labeled
unsound: no concrete or symbolic false-conclusion witness was found for a fixed
rule on the used fragment. Rules in unused modules do not contribute to claim
closure. The fixed-semantics trust boundary is accounted for in stage 7.

There are no `[simplification]` rules and no `[functional]` declarations in the
inventoried files. The inventory enumerates every priority rule. The only
candidate priority is the decisive priority-30 bridge. Candidate extensions add
no opaque symbol. Supplied opaque/symbolic declarations are:

- `sortVS`, `sortKeyVS`, and `md5hexCodes`;
- float-family symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`.

None is reachable from this solution or its proof summary.

### Construct-to-semantics map

The complete used path, if the bridge is removed, is:

| Submitted construct | Declaration | Fixed execution rules |
|---|---|---|
| `Module`, statement list | `syntax.k:56,61` | `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` |
| `Name` | `syntax.k:12` | `core.k:130-154` |
| `Str("")` and strings | `syntax.k:13`; `core.k:13,15` | `str.k:13-17` |
| `Int` | `syntax.k:9` | `core.k:194` |
| `If` | `syntax.k:49` | strictness plus `controls.k:51-54` |
| `IfExp` | `syntax.k:23` | strict condition plus `controls.k:57-60` |
| `Compare`, `CmpOp("==",...)` | `syntax.k:30,32` | `operators.k:15-20`; string equality `str.k:25` |
| `BinOp("+",...)` | `syntax.k:15` | sequential strictness, `operators.k:12`, integer `int.k:9` |
| `Call` and argument lists | `syntax.k:28,37` | `call.k:20-32`; left-to-right argument loop `core.k:183-191` |
| user closure call | `core.k:31,185-188` | `call.k:69-74`, parameter binding `functions.k:62-75` |
| `len(string)` | builtins binding `core.k:157-181` | `builtins.k:17-26` |
| `Attribute(...,"startswith")` | `syntax.k:29` | `call.k:16,24`; `methods.k:61,166-169` |
| `Subscript`, `Slice`, `NoBound` | `syntax.k:22,38,39` | `subscript.k:27-69,72-121` |
| recursive name and call | same `Name`/`Call` rules | captured parent scope lookup then the closure-call rules |
| `Return` | `syntax.k:50` | `functions.k:77-90` |

The fixed syntax enforces the relevant evaluation order: `BinOp` is
left-to-right `seqstrict`; conditions and returns are strict; `Call` evaluates
the callee then arguments left-to-right; `IfExp` evaluates only its selected
branch. Strings are immutable values, so the body should not mutate the heap.
Calls temporarily update environment, scopes, scope allocation, stack, and
return state, then `#pop` restores/deallocates the frame. The bridge skips all
of these transitions and simply frames every omitted cell.

### Candidate extension decisions

All ten candidate rules are accounted for:

1. **`howManyTimesBody` macro rule (`verification.k:8-27`) — acceptable
   syntax summary.** Its expansion matches the submitted translated function
   body. It does not itself prove behavior.
2. **Three `overlapCount` equations (`:31-41`) — truthful definitional
   summary.** The cases pattern-empty, text-empty/pattern-nonempty, and
   both-nonempty are disjoint and exhaustive over `IntSeq`. Recursive calls
   decrease the text sequence. The equations express an overlapping
   position-by-position count.
3. **Three `#overlapEval` rules (`:46-76`) — truthful rules for the invented
   proof machine.** Their empty-pattern, empty-text/nonempty-pattern, and
   nonempty/nonempty cases are disjoint and exhaustive. They do not describe
   Python control flow.
4. **Two `#overlapAcc` rules (`:78-101`) — truthful accumulator-machine
   rules on their matched cases.** The recursive case requires a nonempty
   pattern and decreases the text; the base text case returns the accumulator.
   The unhandled nonempty-text/empty-pattern state is not used and the symbol is
   not declared total. The helper invariant follows from these equations and
   `overlapCount`.
5. **Priority-30 closure bridge (`:106-118`) — materially unsound and
   illegitimate.** It is an operational bridge, not a harmless definition. Its
   matched context includes an arbitrary continuation and omits environment,
   scopes, freshness, heap, stack, return, exception, and exit cells. Its only
   guard is the syntactic closure/argument shape. Its justification scope is
   empty: there is no bridge-free universal connection claim anywhere in the
   candidate. It preempts the fixed closure call and injects exactly the
   task-answer recurrence.

The bridge is not merely unsupported; it has a concrete false-conclusion
witness on its actual complete match domain. The reviewer used ordinary intended
input strings `string="a"` and `substring="a"`, directly supplied the exact
closure, but set captured scope `0` to
`"how_many_times" |-> 0`. This is permitted by the bridge because it mentions no
scope cell.

- With the candidate bridge, the ground claim that the call returns `1` exits
  zero and prints `#Top`.
- A fresh Haskell definition containing the same exact body macro but no bridge
  executes the fixed supplied semantics. It reaches the genuine recursive
  call:

```text
#applyK(toCall(0), str(.IntSeq), str(iCons(97,.IntSeq)), .Vals)
```

  and exits 1 with `WarnStuckClaimState`. Thus fixed execution does not return
  `1`, whereas the candidate rule proves that it does.

This witness compares binding, control, frame state, and continuation, not just
the mathematical value. Exact artifacts and commands are
`evidence/fixed-wrapper.k`,
`evidence/spec-bridge-wrong-binding.k`,
`evidence/spec-fixed-wrong-binding.k`,
`evidence/stage5-bridge-witness.sh`, and
`evidence/stage5-bridge-witness.log`. The recorded status triple is:

```text
FIXED_BUILD_EXIT=0
BRIDGE_WRONG_BINDING_KPROVE_EXIT=0
FIXED_WRONG_BINDING_KPROVE_EXIT=1
```

This supplies the required false conclusion witness. Independently, even on the
entry claim's stronger good-scope precondition, there is still no universal
bridge-free theorem connecting the submitted body to `overlapCount`; finite
differential tests cannot fill that proof obligation.

## 6. Fresh non-vacuity test

The candidate did not provide `spec-vacuity.k`. The reviewer created
`evidence/spec-vacuity-audit.k`, retaining the helper but changing the universal
entry result from `overlapCount(S,P)` to
`overlapCount(S,P) +Int 1`.

This is demonstrably false for the satisfying stage-4 input:
the actual/formal result for `("aaaa","aa")` is `3`, while the mutation demands
`4`. It also fails generally, including the empty-pattern branch.

The exact run is in `evidence/stage6-nonvacuity.sh` and
`evidence/stage6-nonvacuity.log`:

```text
kprove .../spec-vacuity-audit.k --definition .../verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT --dry-run
MUTATION_DRY_RUN_EXIT=0

kprove .../spec-vacuity-audit.k --definition .../verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-VACUITY-AUDIT
MUTATION_KPROVE_EXIT=1
```

The failure is the expected unmet result obligation, not a parser error,
timeout, missing import, or unrelated crash. `WarnStuckClaimState` reports that
the source and destination terms unify but the implication fails, with the
residual excluding:

```text
isLen(S) +Int 1 #Equals isLen(S) +Int 2
```

Therefore the candidate proof is non-vacuous and discriminates a false result.
This favorable result does not establish real-program soundness.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the supplied semantics **extended with all candidate rules**, it
machine-checks that:

1. the invented `#overlapAcc` machine computes accumulator plus
   `overlapCount`; and
2. an exact-shaped closure call rewrites to `overlapCount(S,P)` in entry states
   satisfying the stated scope/freshness/control precondition.

Because item 2 takes the candidate priority bridge immediately, this is a proof
about the bridge-extended theory. It is not a proof that fixed supplied
semantics executes `solution.mpy` to that result. It also does not prove module
loading, the Python recursion's termination, or universal equivalence with the
trusted canonical implementation.

### Trust and assumption ledger

| Boundary or assumption | Influence | Assessment |
|---|---|---|
| Supplied reference semantics, byte-verified against candidate | Defines configuration and all fixed execution | Required and acceptable trust boundary for `SUPPLIED_SEMANTICS` mode |
| K v7.1.337 frontend, LLVM/Haskell backends, and builtin integer/Boolean/map/list theories | Builds, concrete execution, symbolic closure | Ordinary toolchain trust; fresh builds and exact logs make it auditable |
| Supplied opaque sort, digest, and float symbols listed in stage 5 | None on this program or proof path | Acceptable but irrelevant |
| `overlapCount` equations and `startsWith`/length arithmetic | Defines the intended mathematical answer | Transparent, terminating equations; acceptable ordinary mathematics |
| Helper reachability claim | Connects `#overlapAcc` to `overlapCount` | Machine-checked, but only about candidate proof machinery |
| Body macro equals submitted AST | Syntactic identity only | Established by inspection and trusted translation; insufficient for behavior |
| Candidate priority bridge equals fixed closure execution | Controls every entry proof result and skips all body/control/state behavior | Illegitimate. No connection theorem; concrete wrong-binding witness refutes its full domain |
| Python differential, 8,922 cases | Supports rewrite-versus-canonical result agreement for tested terminating inputs | Useful finite empirical bridge only; cannot justify the K operational rule |
| Ground K/Python comparison | Shows result constraint and one satisfying entry state | Useful adequacy/non-vacuity evidence only |
| Natural-language interpretation of arbitrary `IntSeq` as Python strings | Intent bridge | Reasonable for equality/prefix/slice operations; not the source of the failure |
| CPython recursion behavior | Termination of submitted rewrite for very long text | Excluded by partial correctness; natural-function totality remains unproved |

### Gate decisions

- Fresh verification: **pass** under the submitted extended theory.
- Gate A / real-program soundness: **fail**. The program-defined body does not
  execute, the operational bridge has no universal connection theorem, and a
  concrete false-conclusion witness refutes its complete domain.
- Result constraint/non-vacuity: **pass**.
- Intent evidence: the Python rewrite has strong finite support, but this cannot
  rescue Gate A.
- Provenance completeness: defective because the four requested generation
  records and structured trace are absent.

The decision boundary requires `FAIL / NOT_LEGIT` for a proof that relies on a
materially unsound execution-bypassing rule or fails to pin the real submitted
program. Both conditions hold here.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
