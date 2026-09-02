# Independent adversarial review: 38-decode-cyclic

## Executive conclusion

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted `decode_cyclic` implementation under the supplied MPY
semantics. A clean source rebuild succeeds, the submitted two-claim proof
closes with `#Top`, the claim body is mechanically identical to the
trusted-regenerated target body, and independent body/result mutations are
rejected for the expected semantic reasons.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because two
proof-local slice simplifications are asserted as derived mathematical lemmas
rather than separately discharged by a bridge-free K proof. They are true on
their complete guards, and no false conclusion witness exists, but attempts to
make the fixed-semantics backend establish the symbolic sequence-length
induction did not close. The finite Python/K evidence and the manual derivation
support legitimacy but do not turn that derivation into an additional
machine-checked theorem.

Tool versions are recorded in `evidence/tool-versions.log`: Python 3.10.12 and
K 7.1.293.

## 1. Input and provenance integrity

### Record layout and required records

`/audit-input.json` declares:

- problem `38-decode-cyclic`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

Every record required for that layout is present, readable, and a regular
non-symlinked file:

- `/run.json`
- `/task.json`
- `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/usage.json` (present and inspected)
- the structured trace below `/generation-evidence/codex-trace/`

Historical `runtime-metrics.json` is absent. This is expressly permitted for
`legacy-selected-stage1`; it is not a reconstructed record and is not treated
as a defect.

The generation records claim that the original run passed. That claim was not
relied on. The trace was parsed as 326 valid JSONL records; the retained trace
file hash is
`f00c21468f86a1a241a4eca64d815998e7880cd46c1ea7d5e826a75766abd408`.
The generation records and their relevant proof/build assertions were
inspected only to establish provenance.

### Independent hash and campaign checks

`evidence/stage1_integrity.py` independently hashes the mounted paths, compares
the embedded campaign object to `/audit-campaign-lock.json`, checks record
types/readability, parses every structured-trace line, and recursively compares
the semantics trees. Its exact command/output are in
`evidence/stage1_integrity.log`; it exits 0 with `errors=0`.

Notable matches:

- campaign lock:
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- canonical:
  `b5e4551db239ad5ca7da867428c197cc08511d0fb144c6c351c9dc16b4bb423a`;
- trusted and candidate prompt:
  `76b76b6f211ef2f4243678ddb1df6013ceac62da09fefe7bc38ba55e404a1ef8`;
- trusted and candidate translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- generation output, prompt, metrics, usage, manifests, result, and invocation
  all match their launcher-recorded SHA-256 values.

The campaign lock JSON is exactly equal to the `audit_campaign` block in
`/audit-input.json`, and its independent hash matches
`hashes.audit_campaign_lock_sha256`.

### Supplied-semantics boundary

The trusted `/reference/reference-semantics` tree is present as required.
Candidate and trusted trees each contain 25 descendants. A recursive
type/path/byte comparison found no missing, additional, changed, mistyped, or
symlinked entry. A reviewer-local path/type/content tree digest is identical on
both sides:

`e7e97b99fb2596d45b95c28ee873b7d18ed57e631865ac0a9128b07a4fa1e308`.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounts. There is no infrastructure breach, so a candidate verdict is
appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` supplies `encode_cyclic`, which partitions a string into
blocks of three and left-rotates each complete block by one; a final block of
length one or two is unchanged. The required `decode_cyclic(s: str)` takes an
encoded string and returns the decoded string. The prompt contains no explicit
example assertions.

`/reference/canonical.py` implements decoding by applying `encode_cyclic`
twice. On a complete triple, two left rotations equal one right rotation; an
incomplete final block is unchanged. Since the block transformation is a
bijection, every finite string is a possible encoded input; there is no
material hidden size bound.

The submitted `/candidate/solution.py` uses the equivalent recursive
algorithm:

- if `len(s) < 3`, return `s`;
- otherwise return `s[2] + s[:2] + decode_cyclic(s[3:])`.

It preserves the required signature. This is a different but contract-correct
algorithm.

### Trusted regeneration

In scratch, the trusted translator command was:

```text
python3 /tmp/audit-work/38-decode-cyclic/py2mpy.py /tmp/audit-work/38-decode-cyclic/solution.py > /tmp/audit-work/38-decode-cyclic/solution.regenerated.mpy
```

It exited 0. `cmp` against the submitted `solution.mpy` exited 0; both files
have SHA-256
`33e04dde6676394955f4f478f5d0734059c07ff5e143dcc8c8a055af49958d1f`.
See `evidence/stage2_fidelity.log`.

### Independent differential evidence

`evidence/differential_test.py` independently loads the trusted canonical and
submitted implementation. Its third oracle directly right-rotates each
complete three-character block and does not reuse either implementation. The
test set contains:

- empty and lengths 1 through 36, covering the `< 3` branch boundary and every
  residue class modulo three;
- the candidate examples, spaces, controls, NULs, non-ASCII code points, and
  surrogate code points;
- 5,000 deterministically generated strings of lengths 0 through 300;
- both raw decode comparison and encode/decode round-trip comparison.

Exact command and result are in `evidence/stage2_fidelity.log`: 5,058 total
cases, zero decode mismatches, zero encode-round-trip mismatches, exit 0.
This is finite evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to
`/tmp/audit-work/38-decode-cyclic`. The scratch `reference-semantics` came from
the trusted tree. No candidate-built kompiled definition or cache was copied
or used; `/candidate/__pycache__` was ignored.

### Concrete definition

The clean LLVM build command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. Fresh `krun` execution of the trusted-regenerated
`solution.mpy` exited 0. A reviewer test module made by appending assertions to
the exact submitted source also exited 0 with `NoExc` and exit code 0. It
covers the base boundary, every group-size residue around the first three
blocks, recursive cases, controls/spaces, and an encode/decode round trip.
Commands and bounded output are in `evidence/stage3_rebuild.log`; the generator
is `evidence/make_k_concrete_tests.py`.

### Proof definition and positive target

The clean Haskell build was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. The submitted positive target was then run exactly:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`; see
`evidence/stage3_original_spec.log`. This run proves both submitted claims in
their submitted mutual proof environment.

For dependency diagnosis, the helper claim alone also exits 0 with `#Top`.
An intentionally altered entry-only spec with the helper removed gets stuck at
the recursive call. That nonzero result, retained in
`evidence/stage3_rebuild.log`, is not a failed submitted target: it demonstrates
that the entry theorem genuinely uses the co-proved induction helper instead of
closing without it.

Clean reconstruction therefore passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

`spec.k:8-28` is the induction/helper claim. Its precondition says:

- execution is at the exact `decode_cyclic` body followed by `#endcall`;
- local scope `L` binds `s` to `str(CS)` and has the real module scope as
  parent;
- module scope 0 binds `decode_cyclic` to the exact target closure;
- the builtin scope is at -1;
- `L` is distinct from 0/-1 and below the next fresh scope location;
- all entries in the symbolic remainder `SC` are below `NEXT`;
- there is no active return or exception.

Its postcondition says that normal execution reaches the real `#pop` control
point with the return register exactly
`retV(str(decodeCodes(CS)))`. Heap, heap location, stack, exception, and exit
code are preserved by the claim pattern.

`spec.k:30-47` is the entry claim. Starting from the exact initial state and a
module-scope binding of `decode_cyclic` to the target closure, a call on any
`str(CS)` returns exactly `str(decodeCodes(CS))`. Scope location, heap, stack,
return state, exception state, and exit code are all fixed, not omitted.

The result is neither free nor tautological. `decodeCodes` is independently
defined by exhaustive equations; it is not a fresh oracle shared between an
execution shortcut and the postcondition.

### Satisfiable preconditions

The entry precondition is exhibited by any `CS`, including `.IntSeq`, in the
literal state written in the claim.

One concrete helper witness is:

```text
CS = iCons(98, iCons(99, iCons(97, .IntSeq)))  // "bca"
L = 1
NEXT = 2
SC = .Map
HEAP = .Map
HNEXT = 0
STACK = .List
CODE = 0
```

All freshness inequalities and `keysBelow(.Map, 2)` hold, and the three
explicit scope keys are distinct. Thus neither claim is vacuous.

### Mechanical body and binding identity

`evidence/extract_decode_body.py` extracts the target function's `Stmts`
argument from the trusted-regenerated constructor module using balanced
constructor/string parsing. `kast --expand-macros` was run separately on that
term and on `decodeBody` in the fresh proof definition. The KORE files compare
byte-identically and both hash to:

`471d71efe3614c4329bc9768c93b59ff8be0916181975189607e48ec5753b08b`.

Commands are in `evidence/stage4_pinning.log`. `decodeClosure` expands to the
same parameter `"s"`, same body, and defining environment 0 as the
trusted-regenerated unannotated `FuncDef`.

The complete module also binds the prompt-supplied `encode_cyclic` helper.
Omitting that unused binding from the entry claim is semantically inert:
the mechanically checked target body resolves only local `s`, builtin `len`,
and global `decode_cyclic`. Loading either function has no effect other than
installing its closure. Fresh concrete execution of the complete regenerated
module confirms the two real bindings.

### Concrete substitutions

`spec-ground.k` substitutes:

- `CS = .IntSeq`, expected `""`;
- codes 97,98, expected `"ab"`;
- codes for `"bcaefd"`, expected `"abcdef"`.

The fixed program execution claims close together with `#Top`, exit 0
(`evidence/stage4_pinning.log`). These agree with both Python implementations
and the independent block oracle.

### Body sensitivity

`evidence/make_body_mutant.py` changes the term actually executed by the claim,
not merely an external source file:

```text
Subscript(Name("s"), Int(2))
  -> Subscript(Name("s"), Int(1))
```

The mutated definition builds successfully. Its proof exits 1 with
`WarnStuckClaimState`; the residual exposes the required but false equality
between indices 1 and 2. The ground witness `"bca"` returns `"cbc"` under the
mutant instead of the claimed/correct `"abc"`. See
`evidence/stage4_body_sensitivity.log`.

Real-program pinning and adequacy pass.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k-rule-inventory.md`, generated by
`evidence/k_rule_inventory.py`, enumerates every top-level syntax declaration,
configuration, context, rule/equation, simplification, priority rule,
concrete-only equation, opaque symbol declaration, and claim in:

- the assembly `reference-semantics/semantics.k`;
- all supplied helper K files below `reference-semantics/semantics/`;
- `verification.k`;
- `spec.k`.

There are 946 entries:

- 231 syntax declarations;
- 707 rules/equations;
- five contexts;
- one configuration;
- two claims.

Classification finds 22 opaque symbol declarations, 52 priority rules, 50
concrete-only equations, six simplification rules, and 599 other ordinary
rules/equations. Each row is tagged as fixed/used theorem slice,
fixed/outside theorem slice, or proof-local/claim. The inventory log exits 0.

All 751 fixed/outside-slice rows were checked for reachability from the target
constructor/control slice. Their left-hand symbols never arise on this target
path; the 22 supplied opaque symbols (float operations, sort/digest-style
boundaries, and similar facilities) are in this category and cannot influence
the branch, result, cells, or claims.

The 177 fixed/used-slice rows were checked as a group by constructor and
semantic role. `evidence/construct-rule-map.md` maps every constructor in the
complete `solution.mpy` to its declaration/rules and distinguishes the
unexecuted `encode_cyclic` helper from the target path.

### Fixed target slice

The target uses the supplied semantics as follows:

- `Call` evaluates the callee, then arguments left-to-right, resolves the real
  lexical binding, allocates a fresh scope, pushes the exact continuation, and
  binds `s`.
- `len` dispatches through the builtin binding to `isLen`.
- `Compare` evaluates both operands and integer `<` decides the branch.
- `If` evaluates only the selected body.
- string indexing and slicing use `normIdx`, `slStart/slStop`, `clampHi`, and
  `buildIS`; under the `len >= 3` branch all target indices are in bounds.
- both string additions use the truthful recursive `seqConcat`.
- recursive calls use the same closure/body and a strictly shorter `s[3:]`.
- `Return` sets the return register; `#pop` restores the caller environment,
  deletes the callee scope, restores `scopeLoc`, and resumes the saved
  continuation.

No target operation mutates heap data, performs output, allocates a list, or
raises a modeled exception. Fixed priority rules preserve dereferencing and
call dispatch; no proof-local priority rule preempts fixed execution.
Evaluation order, control stack, scope state, and result are all represented.

The complete `solution.mpy` additionally uses comprehensions, lists, ranges,
`min`, `join`, and closure-cell machinery inside `encode_cyclic`. Those fixed
rules are covered by the fresh LLVM round-trip test but are not reached by the
proved target body. Their presence therefore cannot smuggle the target result.

### Proof-local entries 929-946

The 18 proof-local/claim rows in the inventory were decided individually:

1. `decodeBody` syntax and macro rule: a purely syntactic definitional
   expansion, mechanically identical to the regenerated target body. It does
   not replace any operation.
2. `decodeClosure` syntax and macro rule: the exact one-parameter closure at
   module environment 0. It does not summarize execution.
3. `decodeCodes` declaration and two equations: a definitional summary, not an
   operational bridge. For `n = isLen(CS)`, guards `n < 3` and `n >= 3` are
   disjoint and exhaustive because sequence length is a nonnegative integer.
   The recursive case emits element 2, then elements 0 and 1, then recurses on
   indices 3 through `n-1`. Its recursive length is `n-3`, so it terminates.
   It exactly right-rotates every complete block and preserves an incomplete
   suffix.
4. Slice-length simplification: for `n >= 3`,
   `clampHi(3,n,1)=3`. The fixed `buildIS(CS,3,n,1)` enumerates precisely
   `3,...,n-1`, so applying fixed `isLen` gives `n-3`. This is true for the
   complete rule guard.
5. `clampHi` simplification: if `n>3`, fixed `clampHi` returns its in-range
   index 3; if `n=3`, its positive-step high clamp returns `n=3`. These are all
   cases under `n>=3`.
6. `keysBelow` declaration/base/recursive equations: on a finite
   `Int |-> Scope` map, the function is exactly the conjunction that every key
   is less than `N`. Recursive descent removes one map entry; AC
   decompositions agree because conjunction is commutative.
7. `keysBelow(M,N+1) => true` when `keysBelow(M,N)`: every key below `N` is
   below `N+1`.
8. `N in_keys(M) => false` under `keysBelow(M,N)`: `N` cannot be a key.
9. Fresh update normalization: if every key of `M` is below `N`, then updating
   key `N` equals disjoint insertion `(N |-> S) M`.
10. Scope removal normalization: removing the explicitly inserted fresh key
    `N` returns `M`.
11. Helper claim: an exact active-frame execution theorem. Its circular use is
    after real semantic progress and on `s[3:]`, whose length drops by three.
    It introduces no abrupt effect beyond the real fixed `Return/#pop` path.
12. Entry claim: an exact real call from a fully pinned initial state; it
    depends on the helper rather than bypassing recursive execution.

The map simplifications have compatible guards and right-hand sides and do not
overlap inconsistently with fixed map behavior. `decodeCodes [total]` has
complete guards and strict recursive descent. `keysBelow` is not declared
total; it is used only under the explicit well-formed scope-map invariant.
There is no fresh result-bearing opaque symbol, unconstrained oracle, task
answer axiom, call interception, arbitrary-continuation bridge, or fabricated
state transition.

### Independent lemma evidence and limitation

`evidence/stage5_fixed_lemma_check.log` first records a fixed-only functional
claim attempt. The definition builds, but K 7.1.293 reports that functional
claims are unsupported and produces no claims (exit 113). The later
reachability encodings in
`evidence/stage5_fixed_lemma_retry.log`,
`evidence/stage5_fixed_lemma_inductive.log`, and
`evidence/stage5_fixed_lemma_split.log` build/parse but get stuck on the exact
symbolic sequence-length induction; they do not derive a contradictory result
or a false witness.

This failure to obtain a separate bridge-free `#Top` is not evidence that the
candidate lemma is false. The fixed equations above give a complete
mathematical derivation for every `IntSeq` and every state satisfying
`isLen(CS) >= 3`. It is nevertheless the non-fatal proof-extension evidence
limitation that determines `CONCERNS` rather than `PASS`.

No inventoried candidate rule was found unsound, so there is no false
conclusion witness to report.

## 6. Fresh non-vacuity test

The reviewer-generated `spec-vacuity.k` retains the candidate helper unchanged
and changes only the entry postcondition:

```text
str(decodeCodes(CS))
  -> str(seqConcat(decodeCodes(CS), iCons(33, .IntSeq)))
```

For the satisfying entry input `CS=.IntSeq` (Python input `""`), the real
result is `""` while the mutation requires `"!"`.

Evidence is in `evidence/stage6_nonvacuity.log`:

1. `evidence/make_vacuity_mutant.py` exits 0.
2. `kprove ... --dry-run` exits 0, demonstrating that the mutation parses and
   builds in the real proof environment.
3. Live `kprove` exits 1 with `WarnStuckClaimState`.
4. The residual is the expected unmet result equality:
   `decodeCodes(CS) == seqConcat(decodeCodes(CS), iCons(33,.IntSeq))`.

This is a reachable semantic failure, not a parser error, missing import,
timeout, or unrelated crash. The proof is result-discriminating and
non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under the supplied MPY semantics plus the audited proof-local definitions and
simplifications, the reconstructed K proof establishes this
partial-correctness property:

> For every finite `IntSeq CS`, from the exact initial configuration in the
> entry claim, calling the submitted `decode_cyclic` closure on `str(CS)`
> follows the real translated body and, if it reaches the claim's terminal
> state, returns exactly `str(decodeCodes(CS))`, with normal exception/exit
> state and restored call-frame state.

The helper establishes the corresponding active-frame body result and
supplies induction for recursive calls on a sequence shorter by three.
`decodeCodes` denotes per-block right rotation, which is the inverse of the
prompt's per-block left rotation. The formal domain is all `IntSeq` strings,
not finitely many examples or fixed sizes; it does not narrow the HumanEval
string domain.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell/LLVM backends, and reachability/circularity implementation | All machine results | Standard unavoidable proof-tool trust; acceptable. |
| Supplied MPY semantics as a model of the used Python subset | Meaning of calls, strings, slices, recursion, scopes, and return | Integrity-checked and used slice audited. It is not full CPython, but it models every material target operation. Acceptable for this supplied-semantics benchmark. |
| `IntSeq` as the string-code model | Universal entry domain and result | Python indexing/concatenation are code-point operations at this abstraction. Symbolic input avoids the supplied ASCII-only concrete literal converter. Unicode differential cases provide finite support. Non-fatal intent bridge. |
| Proof-local slice/clamp lemmas | Recursive helper closure | Universally true by the complete derivation in Stage 5; separate fixed-only automation did not close. Acceptable for legitimacy but a documented concern. |
| `keysBelow` scope invariant and map lemmas | Symbolic fresh recursive frame allocation/removal | Defined and mathematically sound for the scope maps admitted by the precondition; concrete witness and real proof exercise it. Acceptable. |
| Constructor-level extraction/KORE comparison | Identity of claimed body with submitted body | Mechanical and byte-identical after trusted regeneration. Acceptable. |
| Equivalence of right rotation to applying prompt `encode_cyclic` twice | Human-facing contract | Elementary per-block argument; independently checked on 5,058 cases. The tests are supporting evidence, not the universal proof. Acceptable. |
| CPython recursion/resource limits | Very long concrete Python calls | Excluded by the benchmark's partial-correctness semantics. The proof does not claim CPython resource-totality. |

No opaque supplied symbol affects target control or result. `decodeCodes` is
fully equation-defined; the same unconstrained symbol is not shared between an
execution bridge and the postcondition. Differential tests, traces, and the
candidate's original `#Top` are not used as substitutes for the reconstructed
K proof.

### Gate summary and decision

- Real-program soundness: pass. Fixed execution is retained; proof-local rules
  are truthful; exact body/control/state are pinned; body and result mutations
  are rejected.
- Intent adequacy: pass. The theorem covers every finite string-code sequence
  and proves the contract-equivalent block transformation; there is no fixed
  bound or example-only restriction.
- Evidence/trust auditability: legitimate with a non-fatal limitation. Exact
  scripts, commands, statuses, and bounded outputs are preserved, but the
  proof-local symbolic slice-length lemma has a manual universal derivation
  rather than a separate fixed-only K `#Top`.

That limitation does not allow a false conclusion on any intended input and
does not justify `FAIL / NOT_LEGIT`; it does justify the conservative
`CONCERNS / LEGIT` classification.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
