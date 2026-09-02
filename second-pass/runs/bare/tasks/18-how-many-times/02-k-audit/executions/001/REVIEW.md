# Independent adversarial audit: 18-how-many-times

The reconstructed reachability proof is legitimate under the candidate's
generated, idealized MPY semantics. It executes the exact submitted function
body, constrains the result to a fully defined recurrence for overlapping
occurrences, closes freshly with `#Top`, and rejects a meaningful off-by-one
postcondition. The audit nevertheless assigns `CONCERNS` because the generated
semantics has unbounded calls while the submitted recursive Python function
hits CPython's recursion limit on a valid long-string input. That is an
observable bridge limitation between the proved MPY model and actual Python,
although it does not create a wrong *returned integer* and the theorem is only
partial correctness.

All candidate artifacts were treated as untrusted. No candidate-built
definition or cache was used. Executed sources were copied to
`/tmp/audit-work/how-many-times`; reviewer artifacts and bounded logs are under
`/audit-output/evidence`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` is absent, including as a symlink, while the
three trusted inputs are ordinary regular files:

- `/reference/canonical.py` (683 bytes)
- `/reference/prompt.py` (295 bytes)
- `/reference/py2mpy.py` (17,189 bytes)

There is no contradictory trusted semantics mount, so this is not an
infrastructure error. The exact check, types, candidate tree, and symlink scan
are in `evidence/03-boundary-and-artifact-inventory.log`.

### Required artifacts and provenance claims

The candidate has ordinary, non-symlinked source files for `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.
The required metadata files `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log` are present, and one structured JSONL
trace is present. No required source artifact is missing, mistyped, or
symlinked.

The candidate also contains `semantic-kompiled/`,
`verification-kompiled/`, `__pycache__/`, `run-example.mpy`, and generated
logs/traces. The compiled trees and bytecode are extra untrusted build products;
they were neither copied nor used. `run-example.mpy` is an optional concrete
driver. There is no candidate `PROOF.md` or `spec-vacuity.k`, but neither was a
required deliverable in the bare generation prompt.

The candidate prompt and translator are byte-identical to the trusted mounts:

| Artifact | SHA-256 | `cmp` |
|---|---|---:|
| candidate and trusted `prompt.py` | `6fc9c00aa6b110ecf79f34e36f14b6b4c9a27128463ef6733b948e32a35c2bfc` | 0 |
| candidate and trusted `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | 0 |

See `evidence/04-provenance-comparison.log`.

The untrusted metadata claims a bare/no-supplied-semantics generation, a
634-second successful run, and a final `KPROVE_PASSED` report. The 193-line
structured trace is valid JSONL and contains 37 tool calls; its final untrusted
messages make the same `#Top` claim. These claims were not relied upon.
Bounded summaries and hashes are in
`evidence/23-untrusted-trace-summary.log` and
`evidence/24-untrusted-log-summary.log`; the initial bounded content read is in
`evidence/05-untrusted-claims.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

For two Python strings `string` and `substring`, the result is the number of
start indices at which `substring` equals the corresponding slice of `string`.
Starts may overlap. Thus:

- `("", "a")` gives `0`;
- `("aaa", "a")` gives `3`;
- `("aaaa", "aa")` gives `3`;
- an empty substring occurs at every boundary, so `(S, "")` gives
  `len(S) + 1`.

This is the behavior of trusted `/reference/canonical.py`: it checks every
start in `range(len(string) - len(substring) + 1)` and counts equal slices.

The submitted `solution.py` uses an equivalent recurrence: handle the empty
needle, return zero when the remaining haystack is too short, count a matching
prefix, then recurse on the one-character tail. The algorithm counts overlaps
because it advances by one after a match.

### Translator identity

The submitted MPY is genuinely generated from the submitted Python. Running

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.mpy solution.regenerated.mpy
```

with the trusted translator exited zero. Both files have SHA-256
`f0a019c02b875920d0a9f35a504e27897d27548f3d0586189b0d64513b361fb5`.
See `evidence/06-regenerate-solution-mpy.log`.

### Independent differential test

`evidence/differential_test.py` imports the entry point directly from trusted
`/reference/canonical.py` and independently imports the scratch copy of the
submitted `solution.py`. Its scope is:

- the three documented examples and 12 additional empty/branch/Unicode cases;
- all 3,937 pairs over alphabet `{a,b}` with haystack lengths 0 through 6 and
  needle lengths 0 through 4;
- 1,000 deterministic generated pairs (seed 180018), with haystacks through
  length 64 and needles through length 16;
- one 1,100-character recursion-depth stress case.

There were 4,953 executions. The returned values matched in all ordinary,
exhaustive, generated, and Unicode cases. The sole mismatch was:

```text
string = "a" repeated 1100 times
substring = "z"
canonical = return 0
candidate = RecursionError("maximum recursion depth exceeded in comparison")
```

The script correctly exited 1 so the discrepancy remains visible. Exact output
is in `evidence/07-differential.log`. This is an implementation-to-intent
limitation for large valid strings, not evidence of an incorrect integer on a
normal return.

## 3. Clean proof reconstruction

### Fresh builds

The available independently installed toolchain is K
`v7.1.293` (build date 2025-10-03); see `evidence/08-toolchain.log`.
Only source files copied to scratch were used.

The concrete definition was rebuilt with:

```text
kompile semantic.k --main-module SEMANTIC --syntax-module MPY-SYNTAX \
  --backend llvm --output-definition semantic-fresh-kompiled
```

It exited 0 (`evidence/09-build-concrete.log`).

The proof definition was independently rebuilt with:

```text
kompile verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --backend haskell \
  --output-definition verification-fresh-kompiled
```

It exited 0 (`evidence/13-build-proof.log`).

### Positive target claim

`spec.k` contains exactly one positive claim,
`SPEC.how-many-times-correct`. The independent command was:

```text
kprove spec.k --definition verification-fresh-kompiled \
  --spec-module SPEC
```

It exited 0 and printed exactly `#Top`; see
`evidence/14-positive-proof.log`. Thus every positive target claim closes in a
clean reconstruction.

### Fresh concrete generated-semantics execution

`evidence/generate_concrete_programs.py` generated eight MPY programs in
scratch by retaining the submitted translated module and appending a concrete
entry call. The generated inputs are preserved under
`evidence/concrete-programs/`; generation and copy commands are in
`evidence/10-generate-concrete-programs.log` and
`evidence/11-preserve-concrete-programs.log`.

Fresh LLVM `krun` results matched both Python implementations for:

| Case | K | canonical Python | submitted Python |
|---|---:|---:|---:|
| `("aaaa", "aa")` | 3 | 3 | 3 |
| `("", "a")` | 0 | 0 | 0 |
| `("", "")` | 1 | 1 | 1 |
| `("abc", "")` | 4 | 4 | 4 |
| `("ab", "abc")` | 0 | 0 | 0 |
| `("baba", "ab")` | 1 | 1 | 1 |
| `("🙂🙂🙂", "🙂🙂")` | 2 | 2 | 2 |

For the 1,100-character stress witness, K and the canonical returned 0 while
submitted Python raised `RecursionError`. The complete bounded comparison is in
`evidence/12-concrete-semantics-compare.log`. This confirms both the normal-case
semantic bridge and the recursion-resource limitation.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The sole entry claim has no explicit side condition. Its sort and cell patterns
are its precondition:

- `S` and `T` range over all K `String` values;
- `<k>` begins with
  `invoke(strVal(S), strVal(T)) ~> CONT`, for arbitrary continuation `CONT`;
- `<functions>` contains the `how_many_times` binding whose parameters and
  complete body are written out in the claim;
- `<env>` is an arbitrary map `_ENV`.

The postcondition says modeled execution leaves
`intVal(overlapCount(S,T)) ~> CONT` in `<k>`, with the same exact function
binding and the same environment map. The result is not free, existential,
tautological, or guarded by a one-way implication.

### Pinning the submitted program

The claim starts at the semantic entry token `invoke`, rather than literally
starting from the outer `Module(...)` term in `solution.mpy`. This is a manual
entry-state pin, so it merits scrutiny. It is nevertheless pinned to this
submission:

1. `solution.mpy` is byte-identified with trusted translation of
   `solution.py`.
2. The function body in the claim is constructor-for-constructor the body in
   that `solution.mpy`.
3. Freshly executing the actual `solution.mpy` installs exactly that body in
   `<functions>` and reaches `.K`; the complete parser/installation result is
   in `evidence/15-install-program-state.log`.
4. The `invoke` rule reads the body from that exact map binding and executes it;
   there is no rule that replaces the body with `overlapCount` or another
   oracle.

Accordingly, this is not a substituted-program proof. The pin is static and
auditor-checked rather than a separate reachability claim from the outer
`Module` term; that is an auditability limitation, not a result-bearing
soundness hole.

The single claim is also the circularity for actual recursive control flow.
Every recursive source call evaluates `string[1:]` and `substring`, reaches the
same `invoke` token with the same function map, and carries the pending
addition/return/environment frames in the universally quantified `CONT`.
There are no synthetic helper or loop claims.

### Satisfying state and ground substitution

A concrete satisfying entry state is:

```text
S = "aaaa"
T = "aa"
CONT = .K
_ENV = .Map
<functions> = the exact installed submitted binding shown in the claim
```

This state is realizable after the actual submitted module is installed and
the entry call is made. Fresh K execution reaches `intVal(3)` with the function
map preserved and environment restored
(`evidence/16-ground-concrete-entry.log`). Both Python implementations return
3 (`evidence/17-ground-python-entry.log`).

The claimed recurrence reduces as:

```text
overlapCount("aaaa","aa")
= 1 + overlapCount("aaa","aa")
= 2 + overlapCount("aa","aa")
= 3 + overlapCount("a","aa")
= 3
```

Thus the concrete claimed result agrees with K, submitted Python, and trusted
canonical Python.

## 5. Rule-by-rule static soundness review

The source hashes, numbered declarations, all rules and the claim are preserved
in `evidence/21-local-rule-declaration-inventory.log` and
`evidence/22-source-listings.log`.

### Complete local declaration inventory

`MPY-SYNTAX` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: an empty-separated list of `Stmt`;
- `Stmt`: `FuncDef`, `If`, `Return`, and `Expr`;
- list/support sorts `Strings`, `Params`, `Exprs`, and `CmpOps`;
- `Expr`: `Int`, `Str`, `Name`, `BinOp`, `Compare`, `Call`, and `Subscript`;
- `CmpOp`, `Slice`, and `Bound` (`Expr` or `NoBound`).

`SEMANTIC` declares:

- `Value`: `intVal`, `strVal`, `boolVal`;
- `Function`: `function(Params,Stmts)`;
- `Returned`: `returned(Value)`;
- the K control items `eval`, `addLeft`, `addRight`, `cmpLeft`, `cmpRight`,
  `ifFrame`, `lenFrame`, `callArgOne`, `callArgTwo`, `invoke`, `prefixBase`,
  `prefixEnd`, `tailFrame`, `makeReturn`, and `returnFrame`.

Its configuration is exactly `<py>` containing `<k>`, `<functions>`, and
`<env>`. No heap, allocation, I/O, exception, or explicit resource/stack cell
exists.

`VERIFICATION` adds one symbol,
`overlapCount(String,String):Int [function]`. There are no local
`[total]`, `[functional]`, `[simplification]`, priority, `owise`, macro,
alias, or opaque declarations. `spec.k` adds one reachability claim.

### Mapping every submitted construct

| Construct used in `solution.mpy` | Declaration and behavior |
|---|---|
| `Module`, statement lists | `Program`/`Stmts`; semantic rules 59–62 |
| `FuncDef`, `Params`, string parameter lists | syntax lines 9, 14–15; install rule 64 |
| `If` and empty/nonempty branch lists | `Stmt`; rules 89–91 plus list rules |
| `Return` | `Stmt`; rules 124–130 |
| `Int`, `Str`, `Name` | `Expr`; rules 70–73 |
| `BinOp("+",...)` | `Expr`; rules 75–77 |
| `Compare` and `CmpOp("=="/"<",...)` | `Expr`/`CmpOp`; rules 79–86 |
| `Call(Name("len"),...)` | `Call`; rules 94–95 |
| recursive two-argument `Call` | `Call`; rules 109–122 |
| prefix `Subscript`/`Slice` with `NoBound` and `len` | slice syntax; rules 97–102 |
| tail `Subscript`/`Slice(Int(1),NoBound,NoBound)` | slice syntax; rules 104–107 |

Every constructor in the submitted MPY is declared and has a rule path. The
unused grammar alternatives do not need full Python coverage in generated,
minimal semantics.

### All 35 semantic rules

The following list is exhaustive. “Target-sound” means the rule agrees with
the submitted well-typed program's operation under the idealized MPY model.

| No. / source | Rule and decision |
|---|---|
| S1 / 59 | `Module(SS) => SS`: exposes the translated module statements; target-sound. |
| S2 / 60 | `.Stmts => .K`: terminates an empty block; target-sound. |
| S3 / 61 | `(S SS) => S ~> SS`: left-to-right statement sequencing; target-sound. |
| S4 / 62 | `Value ~> .Stmts => Value`: returns the final top-level expression value. It would discard later top-level statements in a broader language, but the only audit drivers place one entry expression last and the submitted module has none. This is a scope limitation, not an intended-domain false witness. |
| S5 / 64–65 | `FuncDef` updates `<functions>` and preserves other cells; it installs the exact submitted body. |
| S6 / 67 | `Expr(E) => eval(E)`: evaluates an expression statement; target-sound. |
| S7 / 70 | integer literal to `intVal`; target-sound. |
| S8 / 71 | string literal to `strVal`; target-sound. |
| S9 / 72–73 | name lookup from `<env>`; target names are present in each invocation. |
| S10 / 75 | addition begins by evaluating the left operand; correct Python order. |
| S11 / 76 | after the left value, evaluate the right operand; correct order. |
| S12 / 77 | add two integer values with K unbounded integer addition; correct for the target. |
| S13 / 79–80 | comparison begins with its left expression; correct order. |
| S14 / 81–82 | comparison then evaluates the right expression while retaining the left; correct order. |
| S15 / 83–84 | string `==` returns K string equality. Operand naming is reversed in the frame but equality is symmetric; target-sound. |
| S16 / 85–86 | integer `<` compares retained left with evaluated right; target-sound. |
| S17 / 89 | `If` evaluates its condition before either block; correct control order. |
| S18 / 90 | true Boolean selects the then block. |
| S19 / 91 | false Boolean selects the else block. S18 and S19 have disjoint guards and complete Boolean coverage. |
| S20 / 94 | target `len` evaluates its sole argument first; target-sound. |
| S21 / 95 | string length uses `lengthString`; target-sound on tested ASCII, combining-codepoint, and non-BMP witnesses. |
| S22 / 97–98 | prefix slicing first evaluates the base string; correct target order. |
| S23 / 99–100 | it then evaluates `len(H)` for the upper bound; correct target order. |
| S24 / 101–102 | it applies `substrString(S,0,I)`. The program reaches this only after proving `len(S) >= len(T)`, so the used bounds are valid. |
| S25 / 104–105 | tail slicing first evaluates its base; correct target order. |
| S26 / 106–107 | it returns `substrString(S,1,len(S))`. In the submitted control flow this is reached only when nonempty `T` and `len(S) >= len(T)`, hence `S` is nonempty and bounds are valid. |
| S27 / 109–110 | recursive-call argument one is evaluated first. The callee expression is hardwired, but the exact program has a fixed global binding and no callee-expression effects. |
| S28 / 111–112 | recursive-call argument two is evaluated after argument one; correct Python argument order. |
| S29 / 113 | the two evaluated values become `invoke(V1,V2)`; target-sound. |
| S30 / 116–122 | `invoke` checks the exact function binding, saves the caller map, creates the two-parameter local environment, executes the stored body, and pushes a return frame. This is the real body, not an operational summary. It idealizes away CPython recursion/resource errors; the concrete 1,100-character witness is the documented model boundary. |
| S31 / 124 | `Return(E)` evaluates its expression first; target-sound. |
| S32 / 125 | a returned expression value becomes `returned(V)`; target-sound. |
| S33 / 128 | `returned(V)` discards a following `Stmt`; on the exact body this is only unexecuted remainder after a return. |
| S34 / 129 | `returned(V)` discards a following `Stmts` block; on the exact body this discards exactly the remaining current function block. S33/S34 may overlap on list injections, but their right sides agree. Broader arbitrary MPY contexts are not justified; none is reachable in the submitted program. |
| S35 / 130–131 | reaching the matching `returnFrame` exposes the value and restores exactly the saved caller environment. Pending `CONT` is preserved, including an addition frame. |

There is no operational rule that mentions `overlapCount`, rewrites a call to
the desired answer, introduces a fresh result, skips the submitted body, or
discards the active continuation across a return frame. Thus there is no
result-bearing oracle or smuggled correctness conclusion.

The only concrete semantic-to-Python false-behavior witness is the resource
boundary already recorded: S30's idealized unbounded call model returns 0 for
`("a"*1100,"z")`, while this CPython execution raises `RecursionError`. This is
not claimed as a false equation inside the selected K semantics; it is the
specific language-model adequacy gap supporting the `CONCERNS` verdict.

### All four verification rules

`overlapCount` is a definitional mathematical summary; it does not replace
operational execution.

| No. / source | Guard and decision |
|---|---|
| V1 / 9–10 | If `T == ""`, return `length(S)+1`, exactly the number of string boundaries. |
| V2 / 12–14 | If `T` is nonempty and `S` is shorter than `T`, return 0; no start can match. |
| V3 / 16–21 | If `T` is nonempty, `S` is long enough, and the prefix equals `T`, return one plus the count in `S[1:]`; this preserves overlapping starts. |
| V4 / 23–27 | Under the same nonempty/long-enough conditions with a nonmatching prefix, count only `S[1:]`. |

The guards are pairwise disjoint and exhaustive for every pair of K strings.
V3 and V4 terminate as equations: nonempty `T` plus `len(S) >= len(T)` implies
`S` is nonempty, and the recursive first argument loses one code point. The
rules agree with the ordinary bijection between starts after position zero and
starts in the one-character tail. No overlap, priority, totalization, or
unconstrained case was found.

### The entry claim

C1 (`spec.k` 8–37) is the only claim. It is an exact execution circularity over
the submitted function binding. Its arbitrary `CONT` is necessary to cover
recursive calls under addition and return frames; S35 preserves that
continuation. Because multiple semantic steps occur before every recursive
re-entry, use as a reachability circularity is guarded. The postcondition fixes
the returned integer and restores the original environment.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. The reviewer-created
`evidence/spec-vacuity.k` changes the sole result obligation to:

```text
intVal(overlapCount(S,T) +Int 1)
```

It retains the exact body and precondition. The satisfying witness
`S="aaaa"`, `T="aa"`, `CONT=.K`, `_ENV=.Map` makes the mutation false:
actual/claimed-correct result 3 versus mutated result 4.

The mutation dry-run command parsed and built successfully with exit 0:

```text
kprove spec-vacuity.k --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

See `evidence/19-vacuity-build.log`.

The actual mutation proof command was:

```text
kprove spec-vacuity.k --definition verification-fresh-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`, and the residual explicitly contained
the unmet obligation
`lengthString(S) +Int 1 #Equals lengthString(S) +Int 2`. This is an expected
semantic proof failure, not a parser error, missing import, timeout, or
unreachable mutation. See `evidence/20-vacuity-proof.log`.

## 7. Proven versus assumed accounting

### What is machine-proved

Under the freshly compiled `SEMANTIC` and `VERIFICATION` theory, for every K
string pair `S,T`, arbitrary continuation `CONT`, and arbitrary initial
environment map, executing `invoke(strVal(S),strVal(T))` with the exact
submitted function binding satisfies partial correctness: every terminating
modeled execution reaches `intVal(overlapCount(S,T)) ~> CONT`, preserves the
function binding, and restores the initial environment.

This does not prove termination. It does not prove absence of CPython
exceptions or resource exhaustion. It does not prove behavior on non-string
arguments or arbitrary MPY programs.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K parser, Haskell reachability backend, circularity rule, and LLVM runtime | All formal closure and concrete K results | Standard checker/toolchain trust boundary; independently rebuilt with version recorded. |
| `DOMAINS`, K `Int`/`Bool`/`String`, `lengthString`, `substrString`, equality, integer arithmetic/order | Every branch and final integer | Fixed low-level K primitives, not task-specific or result oracles. Boundary and Unicode tests give finite support, not a proof of implementation correctness. |
| K `Map`, generated list syntax, cells, and K sequencing | Binding, statement order, call/return state | Fixed library semantics. Local rules explicitly preserve or update each relevant cell. |
| Trusted `/reference/py2mpy.py` | Python-to-MPY program identity | Trusted problem input; regenerated output is byte-identical. |
| Manual entry-state pin from parsed `Module` to the exact `<functions>` binding | Whether the theorem concerns this submitted body | Exact source comparison plus fresh concrete installation. It is not a separate machine-checked installation claim, so it is an auditability concern, but no mismatch exists. |
| Informal recurrence-to-English/counting argument | Natural-language meaning of `overlapCount` | Ordinary induction/bijection over start positions, supported by the independent canonical differential. It is not a second K theorem. |
| Idealized unbounded call stack and omission of `RecursionError` | Exceptional behavior and whether a large input returns normally | Genuine limitation. The concrete 1,100-character witness demonstrates it. It does not permit a wrong integer on a modeled normal return, but prevents an unqualified PASS for actual CPython behavior. |

There are no local opaque symbols, empirical oracles, assumed task-answer
rules, operational shortcuts, or unproved fresh values influencing the result.
Differential and concrete testing support only the program/intent and
model/Python bridges; they are not substitutes for the `#Top` proof.

### Gate summary and decision

- Real-program soundness under the selected generated MPY semantics: **PASS**.
  The exact body executes; the result summary is fully equated; environment and
  continuation effects are preserved; the false mutation is rejected.
- Intent/language-model adequacy: **LIMITED**. Returned values align strongly
  with the canonical and ordinary overlap-count mathematics, but the actual
  submitted recursive Python raises at a valid large input that the unbounded
  MPY semantics evaluates normally.
- Trust/evidence auditability: **PASS WITH DOCUMENTED BOUNDARIES**. All commands,
  inputs, statuses, sources, and bounded relevant outputs are preserved.

The proof is therefore legitimate partial correctness for the actual
translated algorithm in its generated source-level semantics, but the
CPython-resource bridge is not strong enough for `PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
