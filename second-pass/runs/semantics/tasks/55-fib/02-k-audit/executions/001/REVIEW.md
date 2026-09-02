# Independent adversarial audit: 55-fib

The candidate contains a legitimate partial-correctness proof for the submitted
program on non-negative integer inputs. The proof was rebuilt from source,
executes the byte-pinned translated program, constrains its result to a defined
Fibonacci fold, is sensitive to the loop body, and rejects a false result.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
prompt does not explicitly say `n >= 0` even though that is the conventional
domain and the formal theorem imposes it; the final identification of the
tail-recursive fold with the natural-language “n-th Fibonacci number” is an
ordinary mathematical/informal bridge supported, but not universally proved,
by differential testing; and four requested generation/provenance records are
missing. None of these limitations makes a false target result provable.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted mount is consistent
with it: `/reference/reference-semantics` exists. There is no infrastructure
mode breach.

The recursive integrity check found:

- All required proof sources (`solution.py`, `solution.mpy`, `spec.k`,
  `verification.k`, `prompt.py`, and `py2mpy.py`) are regular files.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
  trusted `/reference` versions.
- The candidate and trusted semantics trees have the same 24 K files, paths,
  directory/file types, and bytes.
- Neither semantics tree contains a symlink. There are no missing, additional,
  mistyped, changed, or symlinked entries inside candidate
  `reference-semantics/`.
- `/candidate/run-input.json`, `/candidate/metrics.json`,
  `/candidate/codex-last.txt`, and `/candidate/codex-output.log` are missing.
  No structured trace is present. These absences limit provenance evidence but
  were not used as a substitute for reconstruction.
- Candidate `__pycache__`, concrete-test files, and `prove.sh` were treated only
  as untrusted supporting artifacts. No candidate cache or compiled definition
  was copied into a build.

Evidence: [provenance integrity log](evidence/01_provenance_integrity.log) and
[scratch-copy log](evidence/00_scratch_copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for `fib(n)`, the n-th Fibonacci number, with examples
`fib(10)=55`, `fib(1)=1`, and `fib(8)=21`. The trusted canonical implementation
defines `F(0)=0`, `F(1)=1`, and `F(n)=F(n-1)+F(n-2)`. The conventional and
audited input domain is non-negative integers. The prompt's annotation is
`int`, but it does not expressly state non-negativity.

The candidate uses the standard iterative pair update:

```text
(a,b) := (0,1)
repeat n times: (a,b) := (b,a+b)
return a
```

The trusted translator regenerated `solution.mpy` byte-for-byte. Both submitted
and regenerated files have SHA-256
`bcc0a953f1ebd6a40b63e057203b8d3958c3d07765e249e25372bbbdccde3ffd`.
See [translator identity](evidence/02_translator_identity.log).

The independent differential script imports the trusted canonical and
submitted entry points separately. It exercised the three documented examples,
the zero-iteration/branch boundaries `0,1,2,3`, and 64 seeded generated draws
from `0..25` (23 unique combined inputs). It found zero mismatches. The script
also recorded, outside the audited domain, that `fib(-1)` raises
`RecursionError` in the canonical implementation while the submitted iterative
implementation returns 0. This confirms why the theorem's `N >= 0` restriction
matters.

Evidence: [differential script](evidence/differential_test.py) and
[differential results](evidence/03_python_differential.log).

## 3. Clean proof reconstruction

All source needed for execution was copied into
`/tmp/audit-work/55-fib-audit`. The builds used K
`v7.1.337` from `/usr/bin`; scratch output directories were required not to
exist before compilation.

### Concrete definition

The LLVM definition was built from the scratch copy of
`reference-semantics/semantics.k` with main module `MPY-KRUN` and syntax module
`MPY-SYNTAX`. The reviewer concrete program's first 15 lines were byte-identical
to submitted `solution.py`, then added assertions for
`n=0,1,2,8,10,20`. Python and K executions both exited 0. `krun` ended with
`.K`, exit code 0, an empty heap/stack, and the exact submitted closure loaded
in module scope.

Evidence:

- [toolchain and concrete-source identity](evidence/04_toolchain_and_concrete_source.log)
- [fresh LLVM build](evidence/05_llvm_build.log)
- [fresh concrete execution](evidence/06_krun_concrete.log)
- [reviewer concrete source](evidence/concrete_audit.py)

The LLVM compiler reported non-exhaustive `total` declarations for unrelated
helpers (`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`).
Stage 5 accounts for these; none can occur in this program.

### Proof definition and claims

The Haskell definition was freshly compiled from `verification.k`, main module
`FIB-VERIFICATION`, syntax module `MPY-SYNTAX`. It exited 0. See
[fresh Haskell build](evidence/07_haskell_build.log).

Every positive claim was reconstructed:

- `FIB-SPEC.fib-loop` alone: exit 0 and `#Top`
  ([loop proof](evidence/08_kprove_fib_loop.log)).
- The unfiltered original spec: exit 0 and `#Top`
  ([full proof](evidence/10_kprove_full_spec.log)).
- Both labels explicitly selected, so the entry and its declared loop
  dependency were unquestionably loaded: exit 0 and `#Top`
  ([explicit two-claim proof](evidence/11_kprove_both_explicit.log)).

Selecting only `fib-all-natural` filtered away its circularity and remained
compute-bound without output. The reviewer interrupted that diagnostic after
approximately 33m34s; it is recorded as status 130 and is not treated as a
proof failure. Loading the dependency explicitly closed in seconds. See
[entry-only filtering diagnostic](evidence/09_kprove_fib_entry.log).

Thus the decisive clean reconstruction signal is present: the original proof
and the explicit set of all positive claims both exit zero and print `#Top`.

## 4. Adequacy and real-program pinning

### Claims in plain language

`fib-loop` says: from a loop head over `rangeObj(I,N,1)`, with current locals
`n=N`, `a=A`, and `b=B`, execution consumes the loop and preserves its
continuation and all framed cells. At the destination, `a` equals
`fibRun(A,B,I,N)`. Final `b` and `_` are existential because the entry
continuation does not observe them.

`fib-all-natural` says: for every K integer `N >= 0`, begin from the exact
language initial configuration, load the submitted Fibonacci module, and call
`fib(N)`. The call returns `fibSpec(N)`, leaves the exact submitted closure in
module scope, removes the callee scope, and restores environment, allocation
counters, heap, stack, return state, exception state, and exit code.

### Exact program identity and control flow

Expanding the nullary definitions `fibProgram` and `fibBody` produces the
submitted `solution.mpy` term exactly, including the docstring and all
statements. The machine comparison is in
[program pinning and witnesses](evidence/12_program_pinning_and_witnesses.log);
the reviewer script is
[program_pinning_check.py](evidence/program_pinning_check.py).

The `<k>` path does not call an oracle. It:

1. expands `fibProgram` to the exact `Module(FuncDef(...))`;
2. executes module loading and fixed-semantics function definition;
3. looks up the resulting closure and evaluates argument `N`;
4. allocates a normal call scope and binds `n`;
5. executes the docstring expression and the three assignments;
6. looks up the real `range` builtin and creates `rangeObj(0,N,1)`;
7. reaches the exact `#loop` term in `fib-loop`;
8. executes tuple evaluation/unpacking and integer addition through fixed
   semantics; and
9. executes the real `Return`, pops the frame, and yields the constrained
   integer result.

No helper claim substitutes a different program or bypasses a call.

### Satisfiable preconditions and concrete substitution

An entry witness is `N=0` with the exact initial cells shown in the claim:
`env=0`, module/builtins scopes, `scopeLoc=1`, empty heap/stack, counters zero,
`noRet`, `NoExc`, and exit code 0. Its postcondition is
`fibSpec(0)=fibRun(0,1,0,0)=0`.

A loop witness is:

```text
I=0, N=3, A=0, B=1, OLD_INDEX=0, L=1
active scope = {"n":3,"a":0,"b":1,"_":0}, parent(0)
REST = module scope containing fibClosure plus builtins scope
CONT = remaining Return(Name("a")) / end-call computation
scopeLoc=2, heap empty, heapLoc=0
stack contains the caller frame, ret=noRet, exc=NoExc, exit=0
```

It satisfies the helper start pattern and reaches `a=2`.

For `N=0,1,2,3,10`, concrete substitution produced respectively
`0,1,1,2,55` from `fibSpec`, the canonical Python implementation, and the
submitted Python implementation. All three agreed.

The return is therefore neither free nor tautological. The destination is an
exact result term, not a one-way implication.

## 5. Rule-by-rule static soundness review

The exhaustive inventory covers all 26 audited K sources:

```text
232 syntax declarations
1 configuration
5 contexts
701 rules
2 claims
```

It records every source hash, declaration/rule line, attributes, priorities,
functions, total declarations, opaque symbols, and both claims. Among the
inventoried declaration blocks, 150 carry `function`, 111 carry `total`, 45
carry priority, 29 carry `owise`, 36 carry `concrete`, and 25 carry
`symbol(...)`. There are no proof-local or supplied `simplification` or
`functional` declarations.

Evidence:

- [complete rule inventory](evidence/rule_inventory.txt)
- [inventory generation/counts](evidence/13_rule_inventory_generation.log)
- [per-file counts and opaque-symbol list](evidence/18_static_attribute_audit.log)
- [per-source disposition and used-construct closure](evidence/static_rule_review.md)

### Candidate-local inventory

| Extension | Class and decision |
|---|---|
| `fibBody` | Definitional constant; exactly the submitted body. Sound. |
| `fibClosure` | Definitional constant; exactly the closure fixed semantics creates. Sound. |
| `fibProgram` | Definitional constant; exactly the submitted module term. Sound. |
| `fibRun` base/step | Mathematical fold, not an operational bridge. Guards `I>=N` and `I<N` are disjoint/exhaustive; recursive measure `N-I` decreases. Sound. |
| `fibSpec` | Unconditional definition `fibRun(0,1,0,N)`. Sound. |
| `fib-loop` | Machine-checked auxiliary execution theorem/circularity. It executes the exact loop syntax and preserves all framed state. Sound. |
| `fib-all-natural` | Entry execution theorem using the proved loop claim. Sound and result-constraining. |

There are no candidate-local priorities, opaque symbols, simplifications,
concrete rules, or operational bridges.

### Relevant fixed-semantics path

Every submitted constructor was mapped to declarations and operational rules:
module/function loading, statement sequencing, `Int`, `Str`, `Name`, ordinary
assignment, `Call`, one-argument `range`, `For`, range iteration, `TupleExpr`,
pair unpacking, `BinOp("+")`, and `Return`. The exact source lines are tabulated
in [the static review ledger](evidence/static_rule_review.md).

Evaluation order is correct on this path. `BinOp` evaluates left then right;
tuple elements are evaluated left-to-right before unpacking; tuple assignment
therefore computes `(b,a+b)` before writing either variable. `For` evaluates
its iterable once. Ordinary scopes contain no `"$cells"` marker, so
higher-priority cell rules are disjoint. No math, MD5, method, ref, or special
call interception overlaps the two calls in this program.

The loop proof follows fixed semantics:

- if `I>=N`, `inRange(I,N,1)` is false and the loop ends with `a=A`;
- if `I<N`, range yields `I`, `_` is bound, the body computes
  `(B,A+B)`, and the next loop head is `(B,A+B,I+1,N)`;
- these are exactly the two `fibRun` equations.

### Opaque symbols, priorities, totality, and broader semantics

The 25 supplied opaque symbols comprise 22 float/conversion symbols, two sort
symbols, and `md5hexCodes`. None occurs in the program, a branch condition, the
loop summary, or the final postcondition. They have no result/control/state
influence on this proof.

Fresh compilation exposed several broader `total`-coverage warnings. The
supplied semantics also documents a deliberately limited Python subset
(ASCII-only string literals, restricted imports/exceptions and closure escape,
opaque float/sort/MD5 behavior, and total-but-opaque out-of-bounds indexing).
Rules for those unused constructs were inventoried and classified as inert
subset/evidence limitations. Because no such term is reachable from the exact
program on `N>=0`, there is no target-domain false-conclusion witness; they are
not mislabeled as target unsoundness and do not contribute to claim closure.

### Body sensitivity

The reviewer changed both exact loop-body occurrences from `a+b` to `a-b`,
while deliberately leaving `fibRun` unchanged. The mutated semantics/proof
definition compiled. Its loop proof exited 1 with `WarnStuckClaimState` and the
expected unmet equality:

```text
fibRun(B,A-B,I+1,N) = fibRun(B,A+B,I+1,N), with I<N
```

This demonstrates sensitivity to the real property-bearing computation.

Evidence:

- [body mutation diff](evidence/15_body_mutation_diff.log)
- [mutated build](evidence/16_body_mutation_build.log)
- [expected body-mutation failure](evidence/17_body_mutation_proof.log)
- [mutated verification](evidence/body-mutation-verification.k)
- [mutated helper spec](evidence/body-mutation-spec.k)

No target-reachable rule was found materially unsound.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so no candidate mutation was
trusted. The reviewer copied the original spec in scratch, renamed the module,
and changed only the entry result obligation from:

```text
fibSpec(N)
```

to:

```text
fibSpec(N) +Int 1
```

The helper dependency name was updated solely for the renamed module. At the
satisfying witness `N=0`, the real result is 0 and the mutation requires 1.

The mutated spec successfully parsed and compiled with `kprove --dry-run`
(exit 0). The live proof then exited 1 with `WarnStuckClaimState`, after real
execution reached the correct final configuration. Its residual is precisely:

```text
fibRun(0,1,0,N) +Int 1 = fibRun(0,1,0,N), with N>=0
```

This is a meaningful unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

Evidence:

- [preserved false spec](evidence/spec-vacuity.k)
- [mutation diff](evidence/20_vacuity_mutation_diff.log)
- [successful dry run](evidence/21_vacuity_dry_run.log)
- [expected proof failure](evidence/22_vacuity_proof.log)

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics and candidate-local definitional equations,
for every K integer `N>=0`, if execution of the exact submitted translated
module/call terminates, its return value is:

```text
fibSpec(N) = fibRun(0,1,0,N)
```

where `fibRun` repeatedly transforms `(A,B,I)` to `(B,A+B,I+1)` until `I>=N`.
The proof additionally establishes the exact post-call module scope and
restoration of the other modeled state cells. This is a partial-correctness
statement, not a resource-bound or CPython-implementation theorem.

The ordinary mathematical bridge to Fibonacci is:

```text
F0=0, F1=1
invariant at iteration i: (a,b)=(Fi,F(i+1))
step: (Fi,F(i+1)) -> (F(i+1),Fi+F(i+1))=(F(i+1),F(i+2))
```

Thus after `N` iterations `a=F_N`. This bridge is transparent and supported by
the differential evidence, but it is an informal mathematical argument rather
than a separate K theorem equating `fibSpec` with the trusted recursive
canonical function.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K compiler, parser, Haskell/LLVM backends, and reachability implementation | All machine results | Necessary toolchain trust; fresh builds and exit/output signals recorded. |
| K builtin integer, Boolean, string, map, list, equality, and arithmetic hooks | Relevant fixed semantics and `fibRun` | Ordinary low-level trust boundary. Python and K both use unbounded mathematical integers for this target path. |
| Trusted mounted translator | Python-to-`solution.mpy` bridge | Translator itself is assumed; byte regeneration proves the submitted term is its actual output. |
| Supplied reference semantics | Program execution model | Integrity is exact. Relevant constructs were concretely exercised and statically reviewed; the semantics is not a formal proof of CPython. |
| `fibRun` to natural-language Fibonacci | Intent bridge | Informal induction plus finite independent differential testing. This is the principal reason for `CONCERNS`. |
| 25 opaque supplied-semantics symbols | Unrelated float/sort/MD5 programs | Inert: no target claim or reachable state depends on them. |
| Broader subset/totality gaps | Unused constructs | Inert for this theorem; explicitly excluded from the target conclusion. |
| Missing generation records | Provenance only | Concerning evidence absence, but no proof step relies on their claims. |

### Excluded behavior

- Negative integers and non-integer Python values are outside the formal
  precondition. The recorded `n=-1` divergence confirms this exclusion is
  observable.
- The theorem does not assert behavior for Python exceptions, resource
  exhaustion, machine limits, or constructs not used by the submitted program.
- Differential tests are finite bridge evidence only; they are not substituted
  for the K proof.
- Candidate prose, scripts, caches, and any prior claims of `#Top` were not
  trusted.

The clean `#Top`, exact program pinning, body sensitivity, and false-result
rejection establish legitimacy. The stated domain/intent/provenance limitations
warrant concerns without invalidating the proof.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
