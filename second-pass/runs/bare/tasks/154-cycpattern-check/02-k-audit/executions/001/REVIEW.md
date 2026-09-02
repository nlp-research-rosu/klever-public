# Independent adversarial audit: 154-cycpattern-check

## Executive decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the actual submitted `solution.mpy` under its generated semantics. The proof
definition and all 12 positive claims rebuild cleanly, the whole-program claim
executes the byte-identical generated program, the loop claim matches its real
loop head and continuation, and a false result mutation is rejected.

The result is `CONCERNS / LEGIT`, not `PASS`, because the submitted program and
its formal reference function return `False` whenever `b == ""`, whereas the
trusted canonical implementation returns `True`. This is a real
implementation-to-intent limitation: the contract says that `b` itself or a
rotation must be a substring, and Python considers the empty string a
substring. The word “word” could be read as excluding empty inputs, but neither
the signature nor an explicit precondition says so. Independent testing found
this exact divergence on every sampled empty-`b` case and no divergence on
4,446 nonempty-`b` cases.

There is also an out-of-scope semantics overreach: the syntax admits explicit
slice steps, but the rules ignore them. The submitted program uses only
`NoBound` steps, so this defect cannot affect any reachable state of this
program or its proof. It is recorded as a reuse limitation rather than a
material Gate A failure.

## 1. Input and provenance integrity

### Semantics boundary

The rendered mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics`
does not exist, as required. The boundary check exited 0. There is therefore no
trusted or hidden semantics baseline to infer or compare against.

Evidence: [stage1-mount-and-tree.log](/audit-output/evidence/stage1-mount-and-tree.log).

### Required artifacts and types

The candidate contains regular, non-symlinked files for:

- `prompt.py`, `py2mpy.py`, `solution.py`, and `solution.mpy`;
- `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`;
- helper sources `solution-program.k` and `build_solution_k.py`;
- `run-input.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and a 393-record structured JSONL trace.

No required source artifact is missing, mistyped, or symlinked. There are no
additional K source files that could silently contribute rules. Candidate
extras are generated or evidentiary products: `semantic-kompiled/`,
`verification-kompiled/`, `__pycache__/`, logs, metrics, and the trace. All
candidate-compiled definitions and caches were ignored.

`PROOF.md` and `spec-vacuity.k` are absent, but neither was a required
generation deliverable and the audit did not treat their absence as a defect.

### Trusted-file comparisons

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`:
SHA-256
`66607b421ed8b5eb91de52ca96f1b071ecc536edf716451650816ae4e7701f64`.

`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`:
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Evidence:
[stage1-integrity-and-provenance.log](/audit-output/evidence/stage1-integrity-and-provenance.log).

The candidate’s prior `#Top`, reported 961 tests, final message, metrics, and
trace were read only as untrusted claims. None is used as proof evidence in
this decision. All executable source was copied to
`/tmp/audit-work/154-cycpattern-check`; no compiled candidate artifact was
copied. Evidence:
[stage1-scratch-copy.log](/audit-output/evidence/stage1-scratch-copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and algorithms

The prompt asks `cycpattern_check(a, b)` to return `True` iff `b` itself or one
of its cyclic rotations occurs as a contiguous substring of `a`.

The trusted canonical implementation sets `pat = b + b`, considers
length-`len(b)` windows of `a`, and compares them with length-`len(b)` windows
of `pat`. For `b == ""`, its nested ranges execute and `a[i:i] == ""`, so it
returns `True`.

The submitted implementation enumerates indices `0 <= i < len(b)` and checks
`b[i:] + b[:i] in a`. It is an equivalent rotation enumeration when `b` is
nonempty. When `b` is empty the loop executes zero times and returns `False`.

The complete trusted and submitted source listing is preserved in
[stage2-source-inspection.log](/audit-output/evidence/stage2-source-inspection.log).

### Translation and wrapper identity

Running the trusted translator from the scratch copy reproduced the submitted
`solution.mpy` byte-for-byte. Independently regenerating `solution-program.k`
from that `.mpy` also reproduced the submitted helper byte-for-byte. Both
comparisons exited 0.

Evidence:
[stage2-translation-and-wrapper.log](/audit-output/evidence/stage2-translation-and-wrapper.log).

### Independent differential test

The reviewer-authored test imports the trusted canonical entry point and the
submitted entry point independently. It covers:

- all six documented examples;
- empty strings, one-character strings, longer patterns, repeated characters,
  unrotated matches, first/middle/last-rotation matches, and all-false paths;
- Unicode cases;
- the Cartesian product of all `a`/`b` words over `{a,b}` through length 5;
- 600 deterministic generated pairs over `abcxyz`.

The test set contains 4,568 unique pairs. The complete run found 122
mismatches, all with `b == ""`; canonical returned `True` and submitted code
returned `False`. Restricting to nonempty `b` executed 4,446 unique pairs with
zero mismatches.

Artifacts and evidence:

- [differential_check.py](/audit-output/evidence/differential_check.py)
- [differential-inputs.json](/audit-output/evidence/differential-inputs.json)
- [stage2-differential-full-domain.log](/audit-output/evidence/stage2-differential-full-domain.log)
- [stage2-differential-nonempty-b.log](/audit-output/evidence/stage2-differential-nonempty-b.log)

This testing supports only the tested Python behavior. It is not substituted
for the K proof.

## 3. Clean proof reconstruction

### Fresh builds

K v7.1.293 was independently installed at `/usr/bin/{kompile,krun,kprove}`.
`kup` was absent, but the independently installed live toolchain ran normally.
Evidence: [stage3-toolchain.log](/audit-output/evidence/stage3-toolchain.log).

The clean reconstruction directory initially contained source files only and
no `*-kompiled` directory:
[stage3-clean-source-preparation.log](/audit-output/evidence/stage3-clean-source-preparation.log).

The generated language semantics was rebuilt for concrete execution:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-fresh-kompiled
```

Exit 0:
[stage3-kompile-generated-semantics-llvm.log](/audit-output/evidence/stage3-kompile-generated-semantics-llvm.log).

The proof definition was independently rebuilt:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-fresh-kompiled
```

Exit 0:
[stage3-kompile-proof-haskell.log](/audit-output/evidence/stage3-kompile-proof-haskell.log).

### Concrete reconstruction

Fresh `krun` executions agreed with independent Python execution on:

| `(a, b)` | Purpose | K/Python result |
|---|---|---|
| `("hello","ell")` | documented true, match at index 0 | `True` |
| `("abcd","abd")` | documented false | `False` |
| `("ba","ab")` | match on last loop iteration | `True` |
| `("cab","abc")` | match on last loop iteration | `True` |
| `("ab","abc")` | longer pattern/all branches false | `False` |
| `("anything","")` | zero loop iterations | `False` |
| `("","a")` | empty haystack | `False` |
| `("","")` | both empty | `False` |
| `("aaaa","aa")` | repeated characters | `True` |
| `("🙂ab","ab🙂")` | Unicode rotation | `True` |

Evidence:
[stage3-krun-generated-normal.log](/audit-output/evidence/stage3-krun-generated-normal.log),
[stage3-krun-generated-boundaries.log](/audit-output/evidence/stage3-krun-generated-boundaries.log),
and [stage3-krun-unicode.log](/audit-output/evidence/stage3-krun-unicode.log).

### Positive claims

The original positive target command was rerun from fresh source:

```text
kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`. The only diagnostics were unused existential
final-environment warnings:
[stage3-kprove-all-positive-claims.log](/audit-output/evidence/stage3-kprove-all-positive-claims.log).

The spec has 12 claims. A reviewer-authored, otherwise equivalent labeled copy
was used to invoke each target separately. Claims that depend on the loop
invariant were selected together with that invariant. Every invocation exited
0 and printed `#Top`.

Evidence:
[run_each_positive_claim.sh](/audit-output/evidence/run_each_positive_claim.sh),
[spec-labeled.k](/audit-output/evidence/artifacts/spec-labeled.k), and
[stage3-kprove-each-positive-claim.log](/audit-output/evidence/stage3-kprove-each-positive-claim.log).

The fresh dynamic reconstruction gate passes.

## 4. Adequacy and real-program pinning

### Claims in plain language

The first nine entry claims have implicit precondition `true` over their exact
ground `a,b` arguments (six prompt examples and three boundaries). Starting
with empty environment and `NoResult`, each executes `solutionProgram() ~>
start`, consumes the computation, and requires the output to be
`pyBool(cyclicContains(a,b))`.

The tenth entry claim is symbolic in `A` with `b == ""`; it requires the same
whole-program execution and result `cyclicContains(A,"")`, which reduces to
`False`.

The loop claim starts at the exact submitted `while` statement followed by the
real trailing `return False`, with exact bindings for `a`, `b`, and `i`. Its
precondition is `0 <= I <= lengthString(B)`. It requires the final result to be
`cyclicContainsFrom(A,B,I)`.

The final whole-program claim ranges over arbitrary K strings `A,B`, starts
from the exact submitted program with empty environment and `NoResult`, and
requires the exact result `cyclicContains(A,B)`.

### Pinning and result constraint

`solutionProgram()` is a macro whose expansion was regenerated
byte-identically from `solution.mpy`; it contains the complete submitted
`Module(FuncDef(...))` body. It is not a substitute implementation or an
operational summary.

`solutionLoop()` is also a macro, expanding to the exact `While(...)` term in
that body. After the initial `i = 0` assignment, normal statement sequencing
reaches:

```text
solutionLoop() ~> exec(Return(Bool(false)))
```

Thus the loop circularity matches real control flow and the actual trailing
return. The macros do not bypass expression evaluation or state changes.

Every claim rewrites `<k>` to `.K` and constrains `<out>` to a concrete
`Result(pyBool(...))`. `?RHO` existentially permits the genuine final
environment, but it does not occur in or weaken the result. The claims are
neither tautologies nor one-way implications with a free result.

All entry preconditions are satisfiable. Representative satisfying states are:

- `A="hello", B="ell"` for a true ground entry;
- `A="abcd", B="abd"` for a false ground entry;
- arbitrary `A="abc", B=""` for the symbolic empty claim;
- `A="cab", B="abc", I=2` for the loop claim, satisfying
  `0 <= 2 <= length("abc")`;
- `A="cab", B="abc"` for the symbolic whole-program claim.

All 12 reviewer substitutions agree between the K reference function and the
submitted/remaining-loop computation. The empty witnesses deliberately expose
the separate canonical mismatch. Evidence:
[claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and
[stage4-claim-witnesses.log](/audit-output/evidence/stage4-claim-witnesses.log).

The theorem is a partial-correctness theorem. This review does not relabel it
as a total-correctness theorem.

## 5. Rule-by-rule static soundness review

The complete source and machine-extracted declaration/rule locations are in
[stage2-source-inspection.log](/audit-output/evidence/stage2-source-inspection.log)
and
[stage5-static-inventory-source.log](/audit-output/evidence/stage5-static-inventory-source.log).

### Exhaustive declaration inventory

`MPY-SYNTAX` declares:

- `Program ::= Module(Stmts)`;
- statement lists and `FuncDef`, `Assign`, `While`, `If`, `Return`;
- `Params` and comma-separated parameter strings;
- `Name`, `Int`, `Bool`, `Call`, `BinOp`, `Compare`, and `Subscript`
  expressions, expression lists, `CmpOp`, `Slice`, and `Bound`;
- runtime `pyInt`, `pyBool`, `pyStr`, value lists, `NoResult`, and `Result`;
- control items `exec`, `assignTo`, `whileGuard`, `ifGuard`, `ReturnValue`,
  `binLeft`, `binRight`, `compareLeft`, `compareRight`, `sliceBase`,
  `sliceLower`, `sliceUpper`, `sliceStep`, and `LenCall`;
- `Value` as the local `KResult` sort.

`MPY` adds `start` and `indexOf(String,String,Int) [function,total]`.

`SOLUTION-PROGRAM` adds `solutionProgram() [macro]`.

`VERIFICATION` adds `solutionLoop() [macro]`,
`cyclicContains(String,String) [function,total]`, and
`cyclicContainsFrom(String,String,Int) [function,total]`.

There are no explicit `[functional]` declarations, priorities,
`[simplification]` rules, `[owise]` rules, proof-local opaque result
constructors, or other helper K files. `indexOf` is opaque only on symbolic
arguments and is discussed below.

The configuration has exactly the state needed by this program:
`<k>`, two string arguments in `<args>`, a map `<env>`, and `<out>`.
There is no heap, allocation, I/O, exception, or call-stack behavior for the
program to preserve.

### `semantic.k` rules

Each local rule is accounted for:

1. Lines 78–79, `indexOf => findString [concrete]`: faithful for concrete K
   strings and treated as the external string-search primitive. On symbolic
   strings it remains a total Int-valued function; the theorem is parametric
   in that value. This is a named trust boundary, not a program-body summary.
2. Lines 84–87, module entry: matches the exact function name, parameter
   names, two string arguments, and empty environment; it binds `a,b` and
   begins the actual body. Sound for the submitted entry.
3. Lines 90 and 91, empty/nonempty statement sequencing: consumes the list
   unit or executes its head before its tail. Sound and ordered.
4. Lines 93 and 94–95, assignment: evaluates the RHS before updating the
   named map binding. Sound; the actual targets are `i`.
5. Lines 97, 98–99, and 100–101, `if`: evaluates the condition first and
   chooses exactly one branch using disjoint Boolean guards. Sound.
6. Lines 103, 104–106, and 107–108, `while`: evaluates the condition, executes
   the body then recurs on `true`, and exits on `false`. Guards are disjoint
   and exhaustive for `pyBool`.
7. Lines 110 and 111–112, `return`: evaluates the expression, records its
   value, and discards the remaining computation. In this single-frame
   semantics that is the required function-return effect. All actual returns
   have a continuation produced by statement sequencing.
8. Lines 115, 116, and 117–118, literals and names: inject integers/Booleans
   and perform map lookup. Every submitted lookup is bound on every reachable
   path.
9. Lines 121 and 122, `len`: evaluates its string argument then uses
   `lengthString`. Direct syntactic binding to builtin `len` is valid for this
   isolated module, which neither defines nor shadows `len`.
10. Lines 125, 126, 127, and 128, binary expressions: enforce left-to-right
    evaluation and implement exactly the used integer/string `+` cases.
11. Lines 131 and 132, comparison setup: enforce left-to-right evaluation.
12. Lines 133–135 and 136–138, integer `<`: the guards are disjoint and
    exhaustive.
13. Lines 139–141 and 142–144, string `in`: use `indexOf >= 0` versus
    `indexOf < 0`; these guards are disjoint and exhaustive for an Int result,
    with the saved left operand as needle and evaluated right operand as
    haystack.
14. Lines 148–149, subscript setup: evaluates the base first.
15. Lines 150–151 and 152–153, lower-bound setup: defaults `NoBound` to zero or
    evaluates the explicit bound.
16. Lines 154–155 and 156–157, lower-bound continuation: carries default zero
    or the evaluated integer lower bound.
17. Lines 158–159, 160–161, and 162–163, upper bound: defaults `NoBound` to
    string length or evaluates the explicit integer, then calls
    `substrString` with start/end indices.

For the submitted program, every slice has `STEP = NoBound`, and the only
bounds are `0 <= i < length(b)` or `NoBound`. Thus all used `substrString`
calls have Python-equivalent, in-range start/end indices.

The narrower gap is that rule 16 discards `_STEP` without requiring
`NoBound`. A constructed unused program evaluating `"abcd"[::2]` returns
`"abcd"` under this semantics while Python returns `"ac"`. This is a concrete
false-behavior witness for reuse of the declared but unused explicit-step
syntax:
[unused-explicit-step.mpy](/audit-output/evidence/artifacts/unused-explicit-step.mpy)
and
[stage5-unused-explicit-slice-step.log](/audit-output/evidence/stage5-unused-explicit-slice-step.log).
It is not a false conclusion witness for the submitted program: its
byte-identified syntax contains only `NoBound` steps, so the bad case is
unreachable for every intended `a,b` input.

### Helper and verification rules

`solution-program.k` has one macro rule. Its RHS is the exact regenerated
`solution.mpy` term, so it is a truthful syntactic name and not an operational
bridge.

`verification.k` has five rules:

1. `solutionLoop()` expands to the exact submitted while term. This is a
   truthful syntactic name used by the invariant.
2. `cyclicContains(A,B) => cyclicContainsFrom(A,B,0)` states the reference
   starting index.
3. `cyclicContainsFrom(_,B,I) => false` for
   `I >= lengthString(B)` states that no rotations remain.
4. It returns `true` when `I < length(B)` and the current rotation has
   `indexOf >= 0`.
5. It recurs at `I+1` when `I < length(B)` and the current rotation has
   `indexOf < 0`.

The three `cyclicContainsFrom` guards are pairwise disjoint and exhaustive on
the proved domain. Recursion increases `I` toward `length(B)`. The entry
function starts at zero and the loop claim requires `I >= 0`, so all substring
bounds used by the proof are valid. The `[total]` annotation is broader than
the audited negative-index behavior of K’s substring builtin; no claim or
reachable program state uses a negative index. With no false witness on the
intended claim domain, this is recorded as an out-of-domain coverage gap, not
as an unsound proof rule.

The spec itself contains 12 reachability claims and no local rules.

### Used-construct coverage

Every constructor in `solution.mpy` maps to the reviewed declarations and
rules:

- `Module`, `FuncDef`, `Params` → exact entry rule;
- `Assign`, `Name`, `Int`, integer `BinOp("+")` → sequencing, lookup,
  literal, evaluation, and map-update rules;
- `While`, `Compare("<")`, `Call(Name("len"),...)` → while, comparison, and
  length rules;
- `If`, `Compare("in")`, string `BinOp("+")`, `Subscript`, `Slice`,
  `NoBound` → branch, string-search, concatenation, and slice rules;
- `Return`, `Bool` → literal and function-return rules.

Normal and boundary runs collectively exercised every rule branch used by the
submitted program, including zero/multiple loop iterations, true/false `if`,
true/false `<`, found/not-found `in`, default/explicit slice bounds, integer
and string addition, and true/false returns.

### Body sensitivity

As a separate operational-sensitivity check, the actual wrapped program body
was changed only from `return True` to `return False` in the match branch.
The mutated proof definition compiled successfully, but the positive proof
exited 1 with `WarnStuckClaimState`; for `("hello","ell")` the observed output
was `Result(pyBool(false))` instead of the required true result.

Artifacts and evidence:

- [body-sensitivity-solution-program.k](/audit-output/evidence/artifacts/body-sensitivity-solution-program.k)
- [stage5-body-sensitivity-diff.log](/audit-output/evidence/stage5-body-sensitivity-diff.log)
- [stage5-body-sensitivity-kompile.log](/audit-output/evidence/stage5-body-sensitivity-kompile.log)
- [stage5-body-sensitivity-kprove.log](/audit-output/evidence/stage5-body-sensitivity-kprove.log)

This demonstrates that the proof is sensitive to the real program body and
does not close through a hardcoded operational substitute.

## 6. Fresh non-vacuity test

The candidate had no `spec-vacuity.k` to trust or reuse. The reviewer created a
new claim for the satisfiable input `("hello","ell")` and deliberately required
`Result(pyBool(false))`. Both Python implementations, the unmutated K
reference function, and fresh concrete K execution return `True`.

The distinct mutation passed `kprove --dry-run` with exit 0, establishing that
it parsed and built:
[stage6-vacuity-dry-run.log](/audit-output/evidence/stage6-vacuity-dry-run.log).

The actual proof command exited 1 with `WarnStuckClaimState`. Its residual
final configuration contained:

```text
<out> Result ( pyBool ( true ) ) </out>
```

so failure was specifically the unmet false result obligation, not a parser
error, missing import, timeout, unreachable claim, or unrelated crash.

Mutation and proof evidence:
[spec-vacuity-audit.k](/audit-output/evidence/artifacts/spec-vacuity-audit.k)
and
[stage6-vacuity-kprove.log](/audit-output/evidence/stage6-vacuity-kprove.log).

The non-vacuity gate passes.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the generated `MPY` semantics, for arbitrary K strings `A,B`, if the
exact submitted `solution.mpy` entry execution terminates from its specified
initial cells, it consumes `<k>` and returns:

```text
Result(pyBool(cyclicContains(A,B)))
```

The proved loop invariant states the analogous fact from any real loop head
with `0 <= I <= lengthString(B)`, using
`cyclicContainsFrom(A,B,I)`. The six example and four boundary claims are
ground/specialized confirmations; the loop and whole-program claims carry the
symbolic result.

For nonempty `B`, the reference function checks exactly each cyclic rotation
at indices `0 .. length(B)-1`. For empty `B`, it defines the result as `False`.

### Trust and assumption ledger

| Boundary | Dependents | Classification |
|---|---|---|
| Trusted `py2mpy.py` translates the submitted Python AST to the constructor term | Real-program pinning | Trusted input; output identity was checked byte-for-byte. Translator correctness itself is outside the K theorem. |
| K builtins for unbounded Int, Bool, String, Map, `lengthString`, `substrString`, `+String`, and `findString` | All semantic execution | Ordinary K runtime trust boundary. Used-path behavior was reviewed and concretely exercised, including Unicode. |
| `indexOf` is total and equals K `findString` on concrete strings; symbolic occurrences remain opaque | `in`, `cyclicContainsFrom`, loop and whole theorem | Acceptable external primitive, not program-derived. The symbolic theorem is interpretation-parametric because execution and postcondition use the same primitive. Concrete true/false witnesses agree with Python, but no machine-checked universal CPython connection theorem is claimed. |
| The generated subset semantics represents the relevant Python behavior | Bridge from K theorem to `solution.py` | Audited rule-by-rule for every used construct and supported by concrete execution. It excludes general Python globals, shadowing, exceptions, non-string arguments, heap, and I/O. |
| Rotation enumeration expresses the natural-language property for nonempty `b` | Intent bridge | Mathematically direct and supported by 4,446 zero-mismatch differential cases, but not a separate K theorem against `canonical.py`. |
| Empty strings are in scope | Intent/domain interpretation | Concerning: no formal precondition excludes them, and the trusted canonical differs from the candidate on every tested empty-`b` case. |
| Explicit-step and negative-index slice behavior | No submitted-program claim | Outside the used construct/state domain. Explicit steps are known inaccurate; negative-index totality is not validated. Neither can be reached by this program for any string inputs. |

The K proof, not the differential tests or candidate prose, establishes the
formal execution theorem. Differential testing supports only the Python/K and
intent bridges over the enumerated inputs.

### Gate accounting

- Real-program soundness (Gate A): **PASS**. Fresh `#Top`, exact source
  pinning, ordinary body execution, sound rules on all reachable submitted
  states, body sensitivity, satisfiable preconditions, and rejected false
  postcondition.
- Intent adequacy (Gate B): **LIMITED**. The theorem faithfully describes the
  submitted program but disagrees with the trusted canonical and the natural
  substring reading at `b == ""`.
- Trust/evidence auditability (Gate C): **PASS WITH RECORDED BOUNDARIES**.
  Commands, statuses, source mutations, concrete cases, and finite-test scope
  are preserved. No finite evidence is presented as a universal theorem.

The empty-input discrepancy prevents `PASS`, but it does not make the proof of
the actual generated program unsound, vacuous, or substituted. The appropriate
decision is therefore `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
