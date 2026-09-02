# Independent adversarial audit: 67-fruit-distribution

## Decision

The candidate is **FAIL / NOT_LEGIT**. Fresh reconstruction does confirm that
all five positive claims close and that the claims are non-vacuous. Those facts
do not establish the requested theorem about the real generated program:

1. The only universal claim does not quantify over a Python string. It binds
   `s` to the invented value `VFruits(A,O)` and relies on a task-specific rule
   that fabricates the two numeric words. There is no reachability claim or
   refinement theorem connecting all real valid `VStr` inputs to this
   abstraction.
2. The independently exercised `VStr` semantics is materially inaccurate.
   Both Python implementations return `8` on `"5   apples and   6 oranges"` and
   on `"   5 apples and 6 oranges   "`, while the freshly built Haskell K
   semantics returns `#Bottom` on both. On the ordinary input
   `"7 apples and 5 oranges"`, the LLVM build aborts because `nextSpace`
   computes an invalid substring boundary.

Thus the successful symbolic claim is a theorem about a substituted input
model, and the four real-string claims prove only the four fixed examples.

All reviewer-authored scripts and bounded logs are under
`/audit-output/evidence/`. The evidence manifest is
`evidence/07_evidence_manifest.log`.

## 1. Input and provenance integrity

The rendered mode is `GENERATED_SEMANTICS`. The trusted path
`/reference/reference-semantics` is absent, as required. There is no semantics
mode/mount contradiction, so this is a candidate audit rather than
`AUDIT_ERROR`.

The following required candidate artifacts are regular files: `run-input.json`,
`metrics.json`, `codex-last.txt`, `codex-output.log`, `prompt.py`, `py2mpy.py`,
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. The trusted `canonical.py`, `prompt.py`, and `py2mpy.py` are also
regular files. No symlink exists anywhere under `/candidate`; no required
artifact is missing or mistyped.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, and
`/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`. Their
SHA-256 values are respectively
`287ace00706dbc14460387cbd37396f40de3816fb26bd13182cec8a85fd6dddb`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The candidate additionally contains two compiled-definition directories,
`semantic-kompiled/` and `verification-kompiled/`, a `__pycache__/`, four
concrete example inputs, an abstract example, and a solution alias. These are
not missing trusted source and are not integrity violations in generated mode,
but all compiled/cache artifacts were ignored. No candidate helper K file or
candidate vacuity spec is present.

The untrusted provenance claims say generation exited 0 and `prove.sh` ended in
`#Top`. One structured JSONL trace is present and parses as 222 records. These
claims were not used as proof evidence. Exact artifact types, comparisons,
hashes, untrusted metadata excerpts, trace validation, and output-log command
summary are in:

- `evidence/01_provenance.sh`
- `evidence/01_trace_check.py`
- `evidence/01_provenance.log`

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks for the number of mangoes in a basket whose total fruit
count is `n`, given a string containing the apple and orange counts. For a
valid description with apple count `A` and orange count `O`, the result is
`n - A - O`. The examples and the fruit-count interpretation support
nonnegative counts and a basket total at least `A + O`.

The trusted canonical implementation splits on literal spaces, collects every
token for which `isdigit()` is true, converts those tokens to integers, and
subtracts their sum from `n`. The candidate uses Python's whitespace-collapsing
`split()`, then computes:

```text
n - int(words[0]) - int(words[3])
```

This is equivalent for the documented form `A apples and O oranges`, including
leading, trailing, and repeated spaces, but is intentionally less general than
the canonical implementation on malformed descriptions or strings containing
additional digit tokens.

### Translation identity

Running the trusted translator on the scratch copy of `solution.py` produced a
340-byte file byte-identical to the submitted `solution.mpy`; both have SHA-256
`a1215c2919dc54784dd3505ec12199891cb1307512e572cbc32bfd72b0ee34f2`.

### Independent differential testing

The reviewer script imports `/reference/canonical.py` and the scratch candidate
under distinct module names. It covers:

- all four documented examples;
- seven valid boundaries, including zero counts, zero mangoes, a large count,
  leading/trailing whitespace, and repeated spaces;
- a deterministic grid of all `A,O` from 0 through 25 with four total-count
  slack values, for 2,704 generated valid descriptions; and
- five explicitly classified malformed/out-of-domain robustness probes.

There were zero mismatches among 2,715 documented/boundary/generated valid
cases. All five malformed probes diverged and remain visible in the log:
empty/no-number strings, a missing `"and"`, a negative textual count, and an
extra digit token. Those probes are not used to claim an intended-domain
implementation failure.

Evidence:

- `evidence/02_differential.py`
- `evidence/02_fidelity.sh`
- `evidence/02_fidelity.log`

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/fresh`; candidate compiled
definitions and caches were not copied or consulted. The installed tools report
K `v7.1.293` and Python `3.10.12`.

### Fresh builds and positive claims

The following were freshly built from source:

- `semantic.k` with LLVM into `audit-semantic-kompiled`;
- a reviewer-only concrete driver importing `semantic.k`, with LLVM and
  Haskell into separate definitions; and
- `verification.k` with Haskell into `audit-verification-kompiled`.

The reviewer driver adds only
`auditRun(P,S,N) => P ~> invokeString(S,N)`. It contains no result equation and
therefore cannot make an incorrect return value appear.

The unmodified `spec.k` proved as a whole with exit 0 and `#Top`. A separate
reviewer spec added labels without changing any claim, and each of the five
claims independently exited 0 and printed `#Top`:

```text
SPEC-AUDIT.general
SPEC-AUDIT.example-1
SPEC-AUDIT.example-2
SPEC-AUDIT.example-3
SPEC-AUDIT.example-4
```

Parsing the submitted `solution.mpy` and the `solutionProgram` macro at depth
zero produced byte-identical 687-byte KAST files with SHA-256
`8a5bde8c642f5c081d240a211ec09b547ad4f78f068cd5910427df80e4aac463`.
This confirms exact syntactic pinning of the proof macro to the submitted
translated AST.

Exact build/proof commands, statuses, and bounded output are in
`evidence/03_build_and_prove.sh` and
`evidence/03_build_and_prove.log`.

### Generated-semantics concrete execution

Fresh Haskell execution through the reviewer-only driver produced:

| Input | Candidate Python | Canonical Python | Haskell K |
|---|---:|---:|---:|
| `"7 apples and 5 oranges"`, `19` | 7 | 7 | `VInt(7)` |
| `"0 apples and 0 oranges"`, `0` | 0 | 0 | `VInt(0)` |
| `"7 apples and 5 oranges"`, `12` | 0 | 0 | `VInt(0)` |

The same results were obtained through the fresh verification definition.
These normal and boundary executions satisfy the generated-semantics dynamic
check on the Haskell backend.

The LLVM build itself succeeded, but all three concrete calls aborted with an
invalid slice, for example:

```text
Invalid string slice: Requested start index 24 is greater than requested end index 23.
```

This is not treated as a generic container failure. It is a reproducible
backend disagreement caused by the source rule at `semantic.k:100`, which adds
`START` to `findString(...)`. The installed K string contract describes
`findString` as locating an occurrence in the haystack starting at an index;
the normal absolute-index behavior is also what the LLVM hook implements.
Haskell happens to return a relative offset in this installed version, which
makes the candidate rule pass on single-spaced strings. The source definition
therefore depends on a backend-specific hook discrepancy.

Haskell commands and results are in `evidence/03_backend_check.log`; LLVM
commands and failures are retained in `evidence/03_build_and_prove.log`.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **General claim.** Starting with empty function and environment maps, load
   the exact candidate AST and invoke `fruit_distribution` with `s` bound to
   `VFruits(A,O)` and `n` bound to `VInt(N)`. If `A >= 0`, `O >= 0`, and
   `N >= A + O`, execution reaches exactly `VInt(N-A-O)` with both maps empty.
2. **Example 1.** The exact AST invoked with the literal string
   `"5 apples and 6 oranges"` and `19` reaches exactly `VInt(8)`.
3. **Example 2.** The exact AST invoked with
   `"0 apples and 1 oranges"` and `3` reaches exactly `VInt(2)`.
4. **Example 3.** The exact AST invoked with
   `"2 apples and 3 oranges"` and `100` reaches exactly `VInt(95)`.
5. **Example 4.** The exact AST invoked with
   `"100 apples and 1 oranges"` and `120` reaches exactly `VInt(19)`.

The postconditions are exact values, not free variables, tautologies, or
one-way implications. The source body executes: `solutionProgram` loads the
function, `invokeFruit`/`invokeString` selects that stored body, the assignment
and return expression execute, and `finishCall` clears the isolated maps.
There are no loop/helper claims. The `runFruit` and `runString` wrapper rules
are not used by the five spec claims themselves.

Satisfying witnesses exist. In particular `A=5`, `O=6`, `N=19` satisfies the
general precondition and gives 8 in the claimed arithmetic, candidate Python,
canonical Python, abstract K execution, and fixed-string K execution. The four
literal claims likewise agree with both Python implementations. The complete
witness table is in `evidence/04_adequacy.log`.

### Material pinning failure

Syntactic program identity is established, but semantic input identity is not.
`VFruits` is not a Python value and cannot be supplied to `solution.py`.
The general proof reaches its result because the task-specific rule

```text
Call(VSplit(VFruits(A,O)), )
  => VWords(VNum(A), ..., VNum(O), ...)
```

places `A` and `O` directly in the two positions subsequently read by the
program. No auxiliary claim proves that executing `s.split()` on every real
valid string yields exactly this representation. No formal relation between
`VStr(S)` and `VFruits(A,O)` appears in any precondition, rule guard, or
connection theorem.

This is a result-bearing program-derived abstraction. The same `A,O` values
flow from the fabricated split result into the postcondition, so its use is
circular as a proof of parsing. Ground agreement on the four examples and the
differential grid is finite bridge evidence, not the required universal
connection theorem.

A concrete containment/value witness exposes the gap. For
`S = "5   apples and   6 oranges"`, `A=5`, `O=6`, `N=19`:

- `invokeFruit(5,6,19)` reaches `VInt(8)`;
- candidate Python and canonical Python both terminate with 8; but
- real-string `invokeString(S,19)` in the Haskell K semantics gives `#Bottom`.

The abstract execution therefore does not preserve the corresponding real
source execution even on this valid fruit-description input. The universal
claim does not pin the real string-input program.

## 5. Rule-by-rule static soundness review

The line-numbered sources, declaration scan, attribute scan, installed string
hook excerpt, and concrete counterexamples are preserved in
`evidence/05_static_and_counterexamples.log`.

### Complete local syntax and attribute inventory

| ID | Declaration | Attributes / role |
|---|---|---|
| S1 | `Program ::= Module(Stmts)` | `symbol(Module)` |
| S2 | `Stmts ::= Stmt \| Stmt Stmts` | singleton or ordered sequence |
| S3 | `Stmt ::= FuncDef \| Assign \| Return` | three used statement constructors, each symbolized |
| S4 | `Params ::= Params(String,String)` | exactly the target's two parameters |
| S5 | `Expr ::= Int \| Name \| Attribute \| Call0 \| Call1 \| Subscript \| BinOp` | `Attribute` and `Call0` are `strict(1)`; `Call1`, `Subscript`, and `BinOp` are left-to-right `seqstrict` on their expression arguments |
| S6 | `PyValue ::= VInt \| VStr \| VNum \| VFruits \| VWords \| VSplit \| VBuiltinInt` | symbolized runtime and abstract constructors |
| S7 | `Expr ::= PyValue` | runtime-value injection |
| S8 | `KResult ::= PyValue` | makes all `PyValue`s evaluation results |
| S9 | `Function ::= function(String,String,Stmts)` | stored target body |
| S10 | `KItem ::= exec \| setVar \| finishCall \| invokeFruit \| invokeString` | control/entry markers |
| S11 | `Int ::= spaceAt(String,Int) \| nextSpace(String,Int)` | both `[function]`; neither is `[total]` |
| S12 | `Program ::= solutionProgram` | proof-local `[macro]` |
| S13 | `KItem ::= runFruit \| runString` | verification input wrappers |

There are no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`,
priority, or `owise` declarations/rules. No symbol is declared with an opaque
attribute. `VFruits` and `VNum` are nevertheless fresh, uninterpreted data
constructors whose values are result-bearing in the general proof; their only
meaning comes from the task-specific rules inventoried below.

The configuration is exactly `<py>` containing `<k>`, `<functions>`, and
`<env>`. A heap, allocation identity, exception state, I/O, and call stack are
not modeled. This is sufficient for the fixed target only if split/int behavior
is correct: the created word list is read at two positions and never mutated or
observed by identity, the return is the final statement, and the isolated entry
has no caller frame.

### Complete `semantic.k` rule inventory

| ID / line | Rule and decision |
|---|---|
| R1 / 58 | `Module(SS) => exec(SS)`: faithful module-body entry for the one top-level definition. |
| R2 / 60 | `exec(S SS) => exec(S) ~> exec(SS)`: faithful left-to-right statement sequencing. |
| R3 / 61 | `exec(S) => S`: faithful singleton execution. R2/R3 are structurally disjoint. |
| R4 / 63 | `FuncDef` stores `function(P1,P2,BODY)`: faithful for the target's two-argument top-level definition. |
| R5 / 66 | Assignment schedules the RHS before `setVar`: faithful for the used name target. |
| R6 / 67 | `V ~> setVar(X)` updates the environment: faithful target state change. |
| R7 / 70 | `Return(E) => E`: faithful only because return is the target's final statement and there is no caller frame. It is not reusable semantics for early return, but no intended-input false conclusion follows in this program. |
| R8 / 72 | `invokeFruit` selects the stored real body but binds `s` to synthetic `VFruits(A,O)`: operational body execution is preserved, yet the input substitution is illegitimate for a universal theorem about Python strings. Its dependents are the general claim and abstract example. |
| R9 / 76 | `invokeString` selects the stored body and binds real `VStr(S)`/`VInt(N)`: faithful isolated entry rule. |
| R10 / 80 | `finishCall` returns the value and clears both maps: correct for the empty, isolated spec entries. The unguarded erasure would be too broad with pre-existing state or a caller continuation; that is a narrower reuse gap, not an intended-entry unsoundness claim. |
| R11 / 84 | Environment name lookup: faithful for `s`, `n`, and `words`. |
| R12 / 86 | `Name("int") => VBuiltinInt`: faithful for this environment. It can overlap R11 if an environment binds `"int"`; the fixed program never does, so this is a non-material language-reuse gap. |
| R13 / 87 | Integer AST literal to `VInt`: faithful for indices 0 and 3. |
| R14 / 89 | Any `PyValue` gets a `"split"` attribute: over-broad (for example, Python integers have no `split`), but real target calls use `VStr`; `VFruits` is separately rejected as synthetic. |
| R15 / 91 | Splitting `VFruits(A,O)` fabricates a five-word value containing `VNum(A)` and `VNum(O)`: task-specific result-bearing operational bridge with no Python counterpart or universal connection theorem. The repeated-space witness above shows abstract `VInt(8)` while the corresponding real-string K execution is `#Bottom`. |
| R16 / 96 | `spaceAt(S,0) => findString(S," ",0)`: gives the first literal-space position. It combines with R19 to make a leading-space substring `[0,0)`, which is outside the installed `substrString` contract and yields `#Bottom` on a real intended input. |
| R17 / 97 | Positive-index `spaceAt` recurrence decreases `I`, so it terminates for all uses. Its intended correctness depends on R18. Negative inputs are uncovered but the helper is not declared total and the target never supplies them. |
| R18 / 100 | `nextSpace(S,START) => START + findString(S," ",START)`: materially false under the normal absolute-index `findString` contract. Witness: in `"7 apples and 5 oranges"`, searching from index 2 locates the next space at absolute index 8; this rule computes `2+8=10`. The fresh LLVM execution consequently reaches invalid boundaries `24 > 23` and aborts on that ordinary intended input. Haskell success relies on its backend-specific relative-offset behavior. |
| R19 / 102 | String split constructs only five words and locates tokens through R16-R18. It does not implement Python `split()` whitespace collapsing. Witnesses: repeated-space and leading-space descriptions both return 8 in candidate/canonical Python but reduce to `#Bottom` in fresh Haskell K. This is a concrete false execution conclusion on the intended domain. |
| R20 / 110 | Index 0 projection from `VWords`: faithful and disjoint from R21. |
| R21 / 111 | Index 3 projection from `VWords`: faithful and disjoint from R20. |
| R22 / 113 | `int(VInt(I)) => VInt(I)`: mathematically faithful. |
| R23 / 114 | `int(VNum(I)) => VInt(I)`: internally consistent but only supports the rejected synthetic `VFruits` bridge; the general claim depends on it. |
| R24 / 115 | `int(VStr(S)) => VInt(String2Int(S))`: faithful for intended nonnegative decimal count tokens. It is not a complete Python `int` model, but wider cases are unused. |
| R25 / 117 | Integer subtraction: faithful using K's unbounded integers, aligned with Python integers for this operation. |

### Complete `verification.k` rule inventory

| ID / line | Rule and decision |
|---|---|
| V1 / 9 | `solutionProgram` macro expands to the full submitted AST. The independent KAST comparison proves exact syntactic equality; it does not repair the input abstraction. |
| V2 / 25 | `runFruit(P,A,O,N) => P ~> invokeFruit(A,O,N)`: a transparent wrapper, used only by concrete reviewer/candidate input artifacts, not by `spec.k`. It inherits R8/R15's synthetic-input limitation. |
| V3 / 28 | `runString(P,S,N) => P ~> invokeString(S,N)`: a transparent wrapper preserving program load then invocation. |

There are no generated helper K source files. The five `spec.k` claims are the
complete claim inventory and were restated in Stage 4.

### Used-construct coverage and control/state review

| Submitted `.mpy` construct | Declaration and execution rules |
|---|---|
| `Module` | S1; R1 |
| statement sequence | S2; R2-R3 |
| `FuncDef`, `Params` | S3-S4; R4 |
| `Assign(Name(...),...)` | S3/S5; R5-R6 |
| `Return` | S3; R7 |
| `Name("s"/"n"/"words")` | S5; R11 |
| `Name("int")` | S5; R12 |
| `Attribute(...,"split")` | S5 `strict(1)`; R14 |
| zero-argument `Call` | S5 `strict(1)`; R15 or R19 |
| one-argument `Call` | S5 `seqstrict(1,2)`; R22-R24 |
| `Subscript(...,Int(0/3))` | S5 `seqstrict(1,2)`; R13 and R20/R21 |
| `BinOp("-",...)` | S5 `seqstrict(2,3)`; R25 |

Heating/cooling generated from `strict`/`seqstrict` evaluates receivers,
function/argument pairs, subscript operands, and subtraction operands
left-to-right, matching the used Python expressions. Function registration,
parameter binding, assignment, and terminal cleanup account for every state
change in the modeled cells. There is no loop, recursion in the program,
allocation-sensitive observation, exception branch, or output.

The model's missing general call stack and abrupt-return machinery do not harm
this last-statement target. The value-bearing `VFruits` bridge and inaccurate
real-string split are material and do.

## 6. Fresh non-vacuity test

The reviewer created `spec-vacuity-audit.k` only in scratch. It changes the
general destination from `VInt(N-A-O)` to the false
`VInt(N-A-O+1)`. The satisfying witness `A=5`, `O=6`, `N=19` has actual result
8 and mutated expected result 9.

`kprove --dry-run` exited 0, confirming the mutation parsed and built. The real
proof command exited 1 with `WarnStuckClaimState` and the expected failed
implication:

```text
N -Int A -Int O #Equals N -Int A -Int O +Int 1
```

This is a semantic unmet obligation, not a parser error, missing import,
timeout, or unrelated crash. It establishes that the general claim constrains
the result and is non-vacuous. It does not establish that `VFruits` is a valid
model of real strings.

Mutation source, exact commands, exit statuses, and residual:

- `/tmp/audit-work/fresh/spec-vacuity-audit.k`
- `evidence/06_nonvacuity.sh`
- `evidence/06_nonvacuity.log`

## 7. Proven versus assumed accounting

### Precisely proven under the candidate theory

Fresh `kprove` establishes that, under the Haskell interpretation of the
candidate K definition:

- loading the exact submitted AST and invoking it with synthetic
  `VFruits(A,O)`, nonnegative `A,O`, and `N >= A+O` reaches exactly
  `VInt(N-A-O)` in the isolated configuration; and
- loading the exact AST with each of the four literal example strings reaches
  the stated literal result.

The proof is discriminating with respect to the result. This is partial
correctness under the supplied theory; it is not a proof that the theory
faithfully models all intended Python inputs.

### Trust and assumption ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K reachability engine and Haskell backend | all `#Top` results and mutation rejection | Necessary low-level trust boundary. Fresh commands give reproducibility, but the observed string-hook backend disagreement is concerning. |
| Standard K `Int`, `Bool`, `String`, `Map`, K sequencing, map operations, arithmetic/comparison/Boolean hooks | all execution and claims | Acceptable standard primitives in principle. `findString` is misused by R18 and behaves differently across the installed Haskell/LLVM hooks; that use is not accepted. |
| Trusted `py2mpy.py` | source-to-`.mpy` identity | Acceptable trusted input. Byte identity and independent KAST macro identity are established. |
| Trusted prompt and canonical implementation | natural-language interpretation and differential oracle | Acceptable task inputs. Their relationship is supplied by the audit problem, not proved by K. |
| `VFruits(A,O)` and `VNum(I)` constructors | general claim through R8, R15, R23 | Illegitimate result-bearing program-derived abstraction. No real Python value, representation invariant, exact execution claim, or universal connection theorem fixes the bridge. |
| `spaceAt`/`nextSpace` and fabricated `VWords` split semantics | four concrete claims and every potential real-string theorem | Materially concerning/incorrect. Concrete intended-input witnesses yield `#Bottom`; LLVM exposes invalid absolute positions even on ordinary single spacing. |
| Candidate-versus-canonical differential run | implementation-to-intent bridge on tested cases | Finite empirical evidence only: 2,715 intended-format cases with zero mismatches. It cannot replace a universal K connection theorem. |
| Informal exact-format argument | claim that fixed positions 0 and 3 denote apple/orange counts | Reasonable for documented single-format strings, but absent from the formal general claim and insufficient to validate the generated string semantics. |
| Partial-correctness termination scope | theorem interpretation | K reachability proves the stated terminating paths. The Python target is straight-line on valid inputs, but malformed-input exceptions and broader Python behavior are excluded. |

There are no proof-local lemmas, simplification rules, priority rules, or
machine-checked connection claims beyond the five entry claims. Candidate
prose, traces, differential evidence, and prior `#Top` were not substituted for
the reconstructed K proof.

### Gate accounting

- **Real-program soundness / pinning: FAIL.** The universal result relies on
  the unconnected `VFruits` abstraction, and real-string semantics has concrete
  intended-input counterexamples.
- **Intent adequacy: FAIL.** Only four literal real strings are proved; the
  universal theorem does not range over the natural-language string domain.
- **Evidence auditability: PASS.** Fresh commands, statuses, scripts,
  counterexamples, claim witnesses, mutation, and a manifest are preserved.

Successful reconstruction and non-vacuity therefore cannot rescue legitimacy.
The candidate contains useful example proofs and strong empirical evidence for
the Python rewrite, but not a legitimate partial-correctness proof of the real
generated program over its intended domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
