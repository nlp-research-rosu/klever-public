# Independent adversarial review: 116-sort-array

The reconstructed K proof is legitimate relative to the supplied semantics, but
it has a material, non-fatal trust-boundary limitation. The whole-program claim
executes the exact submitted MPY term and constrains the result and state, but
the mathematical meaning of both sorting steps is carried by the supplied
opaque symbols `sortVS` and `sortKeyVS`. The proof therefore establishes correct
composition with those fixed primitives; it does not itself prove that the
primitive results are ordered permutations. The supplied runtime has a
concrete insertion-sort implementation and the independent tests agree with
CPython, but there is no machine-checked connection theorem in the mounted
artifacts between that runtime implementation and the opaque proof symbols.

This warrants `CONCERNS / LEGIT`, not failure: the symbols model Python
built-ins intentionally outside the program-defined code, the theorem remains
interpretation-parametric, the candidate states the ordering conclusion
conditionally, and no proof-local rule can manufacture a false result.

## 1. Input and provenance integrity

`/audit-input.json` declares `pipeline-v3`, problem `116-sort-array`, condition
`kit-semantics`, and `SUPPLIED_SEMANTICS`. The required trusted semantics mount
`/reference/reference-semantics` is present, so the mount agrees with the
rendered mode.

I treated all generation records as untrusted provenance and inspected every
record required for pipeline-v3:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the single JSONL trace below `/generation-evidence/codex-trace/`.

The trace contains 265 valid JSON records and no malformed line. Its one file
hash agrees independently with both `invocation.json` and
`generation-result.json`. The generation log and all directly recorded
pipeline files match their launcher-recorded SHA-256 values. See
`evidence/stage1-integrity.log`,
`evidence/stage1-trace-summary.log`, and
`evidence/stage1-generation-log-scan.log`.

`/audit-campaign-lock.json` is a regular readable file, its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
and its parsed object is exactly the `audit_campaign` block in
`/audit-input.json`. There is no campaign-lock breach.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. The candidate's
`reference-semantics/` has 24 regular files and one subdirectory, exactly like
the trusted tree. A recursive name/type/content comparison found zero missing,
additional, mistyped, changed, or symlinked entries. No candidate source
artifact is a symlink. An independent per-file SHA-256 manifest covers all 771
candidate files, including but not relying on the candidate-provided compiled
definitions (`evidence/stage1-candidate-file-sha256.txt`). The compiled
definitions were not copied into scratch or used.

All required proof deliverables are present as regular source artifacts. There
is no infrastructure uncertainty, malformed mount, or missing launcher record
that would require `AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

The natural-language contract says to sort a finite array of non-negative
integers by increasing number of `1` bits, breaking ties by decimal integer
value. A negative example makes it prudent to include negative integers too.
The trusted canonical implementation performs a numeric stable sort followed
by a stable sort on `bin(x)[2:].count("1")`.

All three displayed expected outputs in `/reference/prompt.py` contradict that
prose and the trusted canonical:

| Input | Displayed output | Canonical output |
|---|---|---|
| `[1,5,2,3,4]` | `[1,2,3,4,5]` | `[1,2,4,3,5]` |
| `[-2,-3,-4,-5,-6]` | `[-6,-5,-4,-3,-2]` | `[-4,-2,-6,-5,-3]` |
| `[1,0,2,3,4]` | `[0,1,2,3,4]` | `[0,1,2,4,3]` |

The trusted canonical plus the unambiguous prose selects the popcount contract;
the inconsistent displayed results cannot all be required simultaneously.

`/candidate/solution.py` uses:

```python
sorted(sorted(arr), key=lambda value: bin(value).count("1"))
```

This agrees with the canonical on every Python integer: the only text removed
by canonical's `[2:]` is part of `0b` or `-0b`, which contains no character
`"1"`. Numeric sorting first and stable key sorting second is equivalent to one
lexicographic sort by `(popcount(abs(x)), x)`.

I regenerated the MPY using the trusted translator in a clean scratch
directory:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

The regenerated and submitted files are byte-identical, both with SHA-256
`6ff0e5b4cbff22ebde8c9732a03e7ed7fbda366019cb017286e35f27dc65a6ee`
(`evidence/stage2-regeneration.log`).

The independent script `evidence/stage2_differential.py` imports the trusted
canonical and candidate from distinct paths and also uses a direct
lexicographic mathematical oracle. It tested:

- 15 explicit/documented/boundary cases;
- all 19,608 lists of lengths zero through five over
  `{-3,-2,-1,0,1,2,3}`; and
- 5,000 deterministic generated lists of lengths zero through 30, including
  powers and boundaries through 1024-bit integers.

All 24,623 cases matched, neither implementation mutated its input, and each
returned a new list. The complete input/result JSONL is
`evidence/stage2-differential-inputs.jsonl`, SHA-256
`e16848bd21ebb3e7d425434e29e9da768257efb3fdb35f796c26f63aa4251e6f`.
Finite testing supports fidelity; it is not substituted for the K proof.

## 3. Clean proof reconstruction

Only candidate source files needed for the theorem were copied to
`/tmp/audit-work/116-sort-array`; the translator, canonical, prompt, and
semantics came from `/reference`. No candidate `*-kompiled` directory or cache
was copied. K reports version 7.1.293.

The concrete definition was rebuilt from trusted source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited 0. Ten independently authored K smoke cases covering empty, zero,
positive, negative, mixed-sign, duplicate, power-of-two, and large-integer
inputs all terminated with `.K`, `NoExc`, and exit code 0
(`evidence/stage3-kompile-llvm.log` and
`evidence/stage3-krun-smoke.log`). The LLVM compiler's non-exhaustiveness
warnings concern unused partial-language functions such as float conversions
and out-of-bounds subscript helpers; none is reached by this program.

The proof definition was rebuilt:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0. Every positive target claim was then run independently:

| Claim command suffix | Output | Exit |
|---|---:|---:|
| `--claims SPEC.key-nonnegative` | `#Top` | 0 |
| `--claims SPEC.key-negative` | `#Top` | 0 |
| `--claims SPEC.sort-array` | `#Top` | 0 |
| no selector (all claims) | `#Top` | 0 |

Exact commands and bounded output are in
`evidence/stage3-kprove-key-nonnegative.log`,
`evidence/stage3-kprove-key-negative.log`,
`evidence/stage3-kprove-sort-array.log`, and
`evidence/stage3-kprove-all.log`. The only Haskell warnings are unused tail
variables in two `strLt` base cases; they do not affect rule meaning.

Thus the candidate's positive verification claim is reproducible. This
successful `#Top` is only closure under the audited theory, not by itself the
soundness or adequacy judgment.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`SPEC.key-nonnegative` says that, for any K integer `I >= 0`, calling the exact
submitted lambda in the stated empty initial state returns
`popcountAbs(I)` and restores all stated cells.

`SPEC.key-negative` states the same for every `I < 0`. The two guards are
disjoint and exhaustive over K integers.

`SPEC.sort-array` says that, for any finite `ValSeq VS` whose every member is a
K `Int`, loading the exact module and calling `sort_array(ref(0))` reaches
`ref(2)`. Heap location 0 still contains `VS`; location 1 contains
`sortVS(VS)`; location 2 contains
`sortKeyVS(sortVS(VS), exact-key-closure)`; `heapLoc` is 3; the call frame is
gone; the stack is empty; and no exception or nonzero exit occurred.

The result is not a fresh logical variable, tautology, or implication-only
postcondition. It fixes the returned reference, both allocated values, the
input value, allocation counter, closure binding, scope state, control stack,
return state, exception state, and exit code.

### Mechanical program identity

`evidence/stage4_extract_claim_program.py` extracts the `#loadAll` argument
directly from `SPEC.sort-array`. The spec uses explicit right-unit constructors
such as `.Exprs`, `.ParamNames`, and `.Stmts`, while translated MPY uses the
surface list abbreviations. After deleting only those explicit empty
right-units, `kast` produced byte-identical 2,104-byte constructor trees for
the claim program and trusted regeneration, both SHA-256
`8718d8b31e0bb2f19b9f3d66d0b01f662e11efc0bd14dd1a8bec0e2b95237fb2`.
See `evidence/stage4-program-pinning.log` and the raw extracted term
`evidence/stage4-claimed-program.mpy`.

The two earlier logs named `stage4-program-pinning-*-attempt.log` record
program-parser rejections of explicit internal empty-list tokens. They are
diagnostic parser attempts, not proof or identity failures; the successful
comparison uses the documented surface normalization and compares parsed KAST,
not whitespace.

### Satisfiable preconditions and ground substitution

Concrete witnesses are:

- `I = 5` for `I >= 0`, with key result 2;
- `I = -5` for `I < 0`, with key result 2; and
- `VS = [3,4,-2,0]` for `allIntVS(VS)`.

For the list witness, the abstract postcondition instantiates to numeric
intermediate `[-2,0,3,4]` and keyed result `[0,-2,4,3]`; both trusted canonical
and candidate Python return `[0,-2,4,3]`. A ground K substitution claim also
prints `#Top`. See `evidence/stage4-witnesses.log` and
`evidence/stage4-ground-kclaim.log`.

### Adequacy limitation

`SPEC.sort-array` closes when selected alone. Therefore neither key claim is
needed to prove it. Symbolic execution never invokes the key: the fixed
proof-level `sorted(..., key=KV)` rule allocates
`sortKeyVS(VS, KV)` as an opaque value. The exact key closure is pinned as data,
but its popcount theorem is not composed with the whole-program theorem.

This is not substitution of another program and does not narrow the domain:
the theorem ranges over arbitrary finite integer sequences, including negative
integers. It is, however, a real summary-to-property limitation. The ordering
meaning of the postcondition depends on the external contracts assigned to
`sortVS` and `sortKeyVS`.

## 5. Rule-by-rule static soundness review

`evidence/stage5-rule-inventory.md` is the exhaustive source inventory for
`semantics.k`, all 23 helper K files, `verification.k`, and `spec.k`. It
contains 937 entries:

- 229 syntax declarations;
- 699 rules;
- five contexts;
- one configuration; and
- three claims.

It separately counts 147 function-bearing entries, 109 totality-bearing
entries, 22 `no-evaluators` entries, 35 concrete entries, 45 priority entries,
26 `owise` entries, five macro/macro-rec entries, the strictness declarations,
and every opaque symbol. There are no local simplification or `anywhere` rules.

Each entry is classified in the inventory. The 698
`FIXED_SOURCE_DISJOINT_UNUSED` entries have outer constructors or labels that
cannot occur in this submitted program's constructor trajectory. They cannot
be premises of the target claim. This classification does not purport to
certify the supplied minimal Python semantics for programs using those unused
constructs; it establishes their irrelevance to this theorem. The remaining
fixed and proof-local entries were reviewed as follows.

### Construct-to-rule map

| Used construct/operation | Declarations and rules | Finding |
|---|---|---|
| `Module`, `FuncDef`, `Params`, `Return`, `Call`, `Name`, `KwArg`, annotated `Lambda`, `Attribute`, `Str` | `syntax.k`; `core.k`; `functions.k`; `call.k` | Exact parser tree; left-to-right callee/argument evaluation; ordinary frame creation/binding/return/pop. |
| Configuration, lookup, built-ins binding, heap allocation | `core.k:49-60`, `117-191` | Claim cells match configuration. `#look` resolves local/module scopes before fixed built-ins; `#alloc` preserves heap and increments the fresh counter. |
| `bin(value)` | `call.k`, `builtins.k:108-121`, `int.k:19-20` | Sign guards are exhaustive/disjoint. `binCodes`/`binAcc` structurally generate magnitude bits, with positive descent. |
| `"1"` and `.count("1")` | `str.k:13-17`, `call.k:16-24`, `methods.k:34-44` | ASCII code 49 is constructed; `Attribute` binds the receiver; `cntSub` and `dropIS` count non-overlapping occurrences. For a one-character pattern this is the bit count. |
| Inner `sorted(arr)` | `call.k:38-46`, `sort.k:18-37` | The input reference is dereferenced after argument evaluation, and a new heap list containing `sortVS(VS)` is allocated. |
| Outer `sorted(..., key=lambda ...)` | keyword tagging in `core.k:95-102`; `sort.k:49,61-62` | The key expression is evaluated to the exact closure and tagged. The fixed rule then allocates an opaque `sortKeyVS` result. |
| Concrete keyed runtime | `concrete.k:25-59` | Runtime-only rules call the key through normal `#callee`, stable-insert pairs using strict `<`, and unpair the result. Equal keys are inserted after existing equals, preserving stability. |
| Proof domain and key summary | all six entries in `verification.k` | Truthful structural definitions only; no operational interception. |

### Evaluation, state, control, overlap, and totality

The normal `Call` rule is `owise`; exact higher-priority dereference and
runtime keyed-sort rules preempt it only on their stated shapes. Callees are
evaluated before arguments, arguments left-to-right, keyword values are tagged
only after evaluation, and the resolved `"sorted"`/`"bin"` bindings come from
the fixed built-ins scope. The two `sorted` calls each allocate one fresh list.
The function frame is created, parameter `arr` is bound to the caller's
reference, and `Return`/`#pop` restores the caller environment and scope counter
while intentionally preserving escaped heap allocations. No used rule discards
an admitted continuation or fabricates exception/control state.

The relevant guarded equations have no false overlap:

- `allIntVS` separates empty and `vCons` sequences and strictly descends.
- `popcountAbs` separates `I >= 0` and `I < 0`, covering every K integer.
- `bin` uses the same sign split; `binCodes` separates zero and positive, and
  `binAcc` descends on a positive magnitude.
- `cntSub` separates empty from nonempty inputs; its nonempty guards are
  complementary, and each recursive call drops at least one code for the
  nonempty `"1"` pattern.
- integer insertion uses complementary `<=Int` and `>Int` guards.
- concrete keyed insertion uses `kLt` versus `notBool kLt`; ties take the
  recursive branch, which is the stable choice.

The `[total]` declarations on `allIntVS` and `popcountAbs` are supported by
exhaustive, terminating equations. The supplied `[total, no-evaluators]`
declarations on `sortVS` and `sortKeyVS` instead mark an explicit external
primitive boundary.

### Opaque sort boundary

`sortVS` and `sortKeyVS` are fixed supplied-semantic symbols, not candidate
extensions. Their proof-level operational rules read the already-evaluated list
and key, allocate exactly one list, and preserve the framed continuation. For
the exact pure, integer-total lambda, this state/control summary agrees with all
fresh concrete executions.

Their values remain opaque, however. The Haskell definition has no universal
equations establishing permutation, ordering, stability, or equivalence to
`MPY-CONCRETE.#ksort`; the semantics comments refer to external Lean/notes
evidence that is not mounted. Because the program-defined code does not
implement sorting—it deliberately calls Python's built-in—these can be treated
as externally trusted library primitives. The formal theorem is
interpretation-parametric and the human ordering conclusion must remain
conditional on their contracts.

I do not label either rule unsound: no false K equality follows from it on the
int-list domain, and the postcondition retains the same opaque symbol rather
than equating it to an incorrect concrete sequence. The narrower finding is an
unproved summary-to-property bridge. The concrete runtime and differential
evidence support that bridge finitely but do not prove it universally.

No proof-local rule encodes the task answer, replaces program execution with an
oracle, rewrites a call or return, or enables a false conclusion. No claimed
unsound rule therefore requires a false-conclusion witness.

## 6. Fresh non-vacuity test

I inspected but did not rely on the candidate's mutation files. The fresh audit
mutation is preserved as `evidence/stage6-false-result.k`. It uses the exact
program and the satisfying input `[3,4]`, keeps the correct final heap
obligations, but falsely requires the function to return caller-owned `ref(0)`
instead of newly allocated `ref(2)`.

The parser/backend dry run exited 0:

```text
kprove stage6-false-result.k \
  --definition verification-audit-kompiled \
  --spec-module STAGE6-FALSE-RESULT \
  --claims STAGE6-FALSE-RESULT.wrongly-returns-input --dry-run
```

The real proof command then exited 1 with `WarnStuckClaimState`. Its residual is
a fully terminated state with `<k> ref(2) ~> .K </k>`, while the destination
requires `ref(0)`. The error is the intended unmet result obligation, not a
parse error, missing import, timeout, or unrelated crash. Exact outputs are in
`evidence/stage6-dry-run.log` and
`evidence/stage6-kprove-false-result.log`.

This proves that the positive theorem discriminates at least this meaningful
false returned-reference obligation.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the rebuilt Haskell definition:

1. The exact submitted function body is loaded and bound.
2. For every finite `ValSeq` of K integers, its exact call reaches `ref(2)` with
   the complete state described in Stage 4.
3. The caller's input list is preserved, two new list values are allocated,
   call/control state is restored, and no modeled exception occurs.
4. In the two isolated exact-call claims, the submitted key lambda returns
   `popcountAbs(I)` for every K integer, with `popcountAbs` defined from the
   supplied `binCodes` and `cntSub` equations.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K toolchain and built-in Int/Bool/String/Map/List theories | Parsing, rewriting, arithmetic, maps, and all claims | Ordinary machine-checking trust base. |
| Trusted `py2mpy.py` | Source-to-MPY bridge | Mitigated by byte-identical regeneration and parsed constructor comparison. |
| Supplied MPY syntax, configuration, lookup, call, allocation, and return rules | Whole program and key claims | Fixed semantics; relevant slice statically reviewed and concretely exercised. |
| `binCodes`, `pyMod`, `strToCodes`, `cntSub`, `dropIS` | Meaning of the isolated key result | Defined by terminating equations and symbolically executed; correspondence to Python is also finitely differential-tested. |
| Opaque `sortVS` | Numeric first pass and location 1 | Externally trusted Python-library primitive; concrete insertion rules support it, but no mounted universal connection theorem. |
| Opaque `sortKeyVS` | Final value at location 2 and returned result | Externally trusted stable-key-sort primitive; the proof rule does not call the key and the runtime implementation is not universally connected to the proof symbol. This is the principal concern. |
| Stable two-pass sorting implies ordering by `(popcount, value)` | Human-facing postcondition | Ordinary mathematical argument, conditional on the two sort contracts. |
| CPython canonical and 24,623-case differential run; ten concrete K cases | Candidate/canonical/runtime bridge | Reproducible finite evidence only, not a universal theorem. |
| Prompt examples | Intended output | Internally inconsistent; not used as proof premises. Trusted canonical and prose agree on the selected contract. |

The full finite integer-list source domain is covered; there is no fixed-size,
bounded-unrolling, or example-only restriction. The exclusion of non-integer
list elements agrees with the stated integer-array contract. Negative integers
are included despite the prose's narrower “non-negative” phrase.

The result is therefore a sound and non-vacuous reachability proof of the exact
program relative to the supplied library contracts. It is legitimate, but the
candidate's headline `VALIDATED` overstates how much of the sorting property is
machine-checked: the returned opaque term is exact, while its ordering and
permutation meaning is assumed at the fixed primitive boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
