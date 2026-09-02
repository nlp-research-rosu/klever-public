# Independent adversarial review: 150-x-or-y

Generation condition: `semantics`  
Rendered semantics mode: `SUPPLIED_SEMANTICS`

## Executive decision

The candidate contains a legitimate, reconstructed partial-correctness proof of
the submitted function body. The loop claim closes using only the fixed supplied
semantics; the top-level claim closes using an exact-context copy of that proved
loop claim; the result is fixed by disjoint, terminating trial-division
equations; and a fresh false-result mutation is rejected with the concrete
residual `34`, not the false target `12`.

The verdict is `CONCERNS`, rather than `PASS`, for three auditability/bridge
limitations:

1. all four requested provenance records are missing;
2. the formal entry macro directly invokes an exact closure body instead of
   executing the submitted `Module(FuncDef(...))` and looking up `x_or_y`;
   this omits the otherwise irrelevant module-scope `x_or_y` binding from the
   symbolic entry state; and
3. the trusted canonical differs from both the generated implementation and the
   ordinary mathematical contract on `n <= 0`.

None of those limitations supplies an unsound rule or permits a false result.
The direct closure contains the exact regenerated body, has the same defining
scope, and the omitted module binding is not read by this body. Fresh concrete
execution of the full module and static name-use review support that bridge.

## 1. Input and provenance integrity

### Semantics-mode boundary

The trusted mount is consistent with `SUPPLIED_SEMANTICS`:
`/reference/reference-semantics` exists. Therefore this is not an
infrastructure breach and a candidate verdict is appropriate.

The reviewer recursively compared `/candidate/reference-semantics` against the
trusted tree by `lstat` entry type and SHA-256 file content. Both trees contain
26 entries. There are no missing, additional, changed, mistyped, or symlinked
entries. See:

- `evidence/check_integrity.py`
- `evidence/stage1-semantics-integrity.log`
- `evidence/stage1-mounts-inventory.log`

The candidate prompt and translator are byte-identical to their trusted
versions:

- `prompt.py`: SHA-256
  `d3c5a3ef8fbe608f4c6ddb2b0209fe20ac537b827fb3252e805681c6c92c3a14`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The commands and zero `cmp` statuses are in
`evidence/stage1-prompt-translator-integrity.log`.

### Missing required provenance

The following requested artifacts are absent everywhere under `/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured trace (`*trace*` or `*.jsonl`) is present. This is an input
integrity and auditability concern, recorded in
`evidence/stage1-required-metadata.log`. It does not prevent independent
reconstruction from source.

### Excluded untrusted material

The candidate contains an untrusted Python bytecode cache and
`kore-exec.tar.gz`. The archive contains candidate-provided KORE and logs
(`spec.kore`, `vdefinition.kore`, `kore-exec.log`, and related files). Neither
artifact was copied into the reconstruction or used as proof evidence. Their
hashes and archive listing are in
`evidence/stage1-excluded-candidate-binaries.log`.

All executable source inputs were copied explicitly to
`/tmp/audit-work/reconstruction`; the semantics copy came from `/reference`,
not a candidate-built definition. The scratch inventory is in
`evidence/stage1-scratch-preparation.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` says that `x_or_y(n, x, y)` returns `x` when `n` is
prime and `y` otherwise. Its examples are:

- `x_or_y(7, 34, 12) == 34`
- `x_or_y(15, 8, 5) == 5`

`/reference/canonical.py` implements trial division: it special-cases `n == 1`,
tests every divisor in `range(2, n)`, returns `y` on the first divisor, and
otherwise returns `x`.

The generated `solution.py` implements the same trial division, with the
mathematically natural stronger boundary check `n < 2`. For positive integers
the two implementations agree. For zero and negative integers the canonical
returns `x`, while the generated implementation returns `y`; zero and negative
integers are not prime, so the generated behavior matches the prompt's ordinary
mathematical reading.

### Translation identity

The reviewer regenerated `solution.mpy` with the trusted translator:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

The regenerated and submitted terms are byte-identical, both with SHA-256
`9e433dad65c9d0b01eb8a7ca08fbff0520c2c931235b4ba7561fc7878f8f81c0`.
See `evidence/stage2-translation-identity.log`.

### Independent differential evidence

`evidence/differential_test.py` independently loads the trusted canonical and
generated entry points. It checks:

- both documented examples;
- negative, zero, one, and `n=2` empty-range boundaries;
- a one-iteration prime;
- first-divisor and later-divisor branches;
- square composite and larger-prime cases; and
- every integer `n` from -20 through 300, using distinct `x` and `y` objects.

Results in `evidence/stage2-differential.log`:

- positive-domain canonical/generated mismatches, `n=1..300`: **0**
- generated/mathematical-oracle mismatches, `n=-20..300`: **0**
- broad canonical/generated mismatches: **21**, exactly `n=-20..0`

The test exits 0 because the generated implementation matches the mathematical
oracle everywhere tested and matches the canonical throughout the positive
domain. The finite run supports, but does not prove, the intent bridge.

## 3. Clean proof reconstruction

### Toolchain and fresh definitions

No `kup` executable is installed, but an independent K toolchain is available:
`kompile`, `kprove`, and `krun` are K version `v7.1.337`. See
`evidence/stage3-toolchain.log`.

No candidate-built definition or cache was copied. The reviewer freshly built:

1. LLVM `runtime-kompiled` from the trusted
   `reference-semantics/semantics.k`;
2. Haskell `verification-kompiled` with main module
   `X-OR-Y-VERIFICATION`; and
3. Haskell `summary-kompiled` with main module `X-OR-Y-SUMMARY`.

Exact commands, statuses, and bounded output:

- `evidence/stage3-concrete-build.log`: exit 0
- `evidence/stage3-loop-proof-build.log`: exit 0
- `evidence/stage3-main-proof-build.log`: exit 0

Compiler warnings concern unused variables and known non-exhaustive fixed
semantics functions; none is a candidate-local parse/build error.

### Fresh dynamic reconstruction

The reviewer-authored `evidence/concrete_harness.py` embeds the submitted
function body and asserts the documented examples plus negative, zero, one,
empty-range, prime, first/later-divisor, square-composite, and larger-prime
cases. It was translated with the trusted translator and executed through the
fresh LLVM semantics.

`krun` exits 0 with final `.K`, environment 0, empty stack, `noRet`, `NoExc`,
and exit code 0. See `evidence/stage3-concrete-execution.log`.

### Every positive target claim

The loop claim was run independently against the definition that does **not**
import the summary rule:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module X-OR-Y-LOOP-SPEC --claims loop_correct
```

It exits 0 and prints `#Top`
(`evidence/stage3-loop-proof.log`).

The main claim was then run against the freshly compiled summary definition:

```text
kprove spec.k --definition summary-kompiled \
  --spec-module X-OR-Y-MAIN-SPEC --claims main_correct
```

It exits 0 and prints `#Top`
(`evidence/stage3-main-proof.log`).

Thus both submitted positive proof targets pass clean reconstruction.

## 4. Adequacy and real-program pinning

### Plain-language claims

`loop_correct` precondition:

- `N >= 2` and next divisor `D >= 2`;
- execution is exactly at the remaining `rangeObj(D,N,1)` loop, followed by
  the real trailing `return x` and `#endcall`;
- the active function frame contains `n=N`, `x=X`, `y=Y`, and old local
  `divisor=OLD`;
- module and heap are empty, the call stack has the exact one frame, and there
  is no return, exception, or nonzero exit yet.

Its postcondition says the loop and trailing return reach `#pop`, the returned
value is exactly `primeSelect(N,D,X,Y)`, and the final local divisor is exactly
`scanLast(N,D,OLD)`. Other listed state is preserved.

`main_correct` has no explicit arithmetic precondition. It starts from the
fixed semantics' clean initial state and directly calls an exact closure with
integer `N` and arbitrary K values `X,Y`. It says the returned K value is
exactly `primeSelect(N,2,X,Y)` and all other initial cells are restored.

The result is not a free variable, tautology, or one-way implication.
`primeSelect` reduces to `X` or `Y` under mutually exclusive guards.

### Body identity and control flow

The submitted `solution.mpy` uses:

`Module`, `FuncDef`, `Params`, `If`, `Compare`, `Name`, `CmpOp`, `Int`,
`Return`, `For`, `Call`, and `BinOp`.

The candidate's macros reproduce the translated body exactly:

- `solution.mpy:3-5` corresponds to `verification.k:18-20`;
- `solution.mpy:6-11` corresponds to `verification.k:21-22` plus
  `verification.k:10-14`; and
- `solution.mpy:12` corresponds to `verification.k:23`.

`#xOrY` constructs `closureVal(("n","x","y"), xOrYBody, 0)` and invokes it
through the fixed `Call` semantics. Macros expand syntax; they do not replace
any body computation with a result oracle. The early comparison, range call,
iterator, divisor assignment, modulo, equality, branch, early return, and
trailing return all execute under the fixed supplied semantics.

### Pinning limitation

The formal entry does not start with the literal submitted
`Module(FuncDef(...))` and `Call(Name("x_or_y"),...)`. It directly supplies the
closure value. Therefore module loading, the `x_or_y` binding, and entry-name
lookup are outside `main_correct`.

This is not a substituted algorithm: the closure body, parameters, defining
scope, call, and return are exact. Static review shows that the only names read
by the body are local `n`, `x`, `y`, `divisor`, and builtin `range`; the
omitted module binding named `x_or_y` cannot affect those lookups.

The reviewer nevertheless tested the distinction:

- `evidence/real-program-pin.k` starts from the literal submitted module. Its
  first symbolic attempt reaches the correct value but fails because the claim
  initially forgot to record the module-scope binding; the residual and exit 1
  are preserved in `evidence/stage4-real-program-pin.log`.
- After recording that state change, the universal `N<2` literal-program
  branch closes with `#Top` in
  `evidence/stage4-real-program-pin-small-v4.log`.
- The universal `N>=2` exploratory bridge was manually interrupted and is not
  used as failure or verdict evidence. The reason the submitted summary cannot
  apply is static and exact: its module scope is pinned to `.Map`, whereas a
  normally executed `FuncDef` leaves an `x_or_y` binding. See
  `evidence/stage4-real-program-pin-scan.log`.
- The fresh LLVM harness executes the full module on all relevant branch
  classes and succeeds.

This body-and-call pin is adequate for the requested function theorem, but the
missing formal module-load/name-lookup bridge is a documented concern.

### Satisfying witnesses and substitutions

A main precondition witness is the clean initial configuration with
`N=7, X=34, Y=12`. A loop precondition witness is the exact loop configuration
with `N=9, D=2, OLD=99, X=91, Y=92`.

`evidence/ground-witnesses.k` checks:

- main inputs `(1,7,9) -> 9`
- `(2,11,13) -> 11`
- `(7,34,12) -> 34`
- `(15,8,5) -> 5`
- the concrete loop witness reaches `retV(92)` and final `divisor=3`

The main witnesses close with `#Top` in
`evidence/stage4-ground-main-witnesses.log`; the loop witness closes with
`#Top` using the bridge-free definition in
`evidence/stage4-ground-loop-witness.log`. Both Python implementations agree on
all four positive main inputs, as recorded by the differential test.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The full inventory is `evidence/k-source-inventory.md`, generated by
`evidence/inventory_k.py`. It covers all 26 K source files used by the proof:
the supplied semantics tree, `verification.k`, and `spec.k`.

It contains 1,119 anchored entries:

- 706 rule sentences
- 232 syntax declarations
- 5 contexts
- 1 configuration
- 2 claims
- 29 modules, 29 endmodules, 90 imports, and 25 top-level requires

`evidence/k-source-review.tsv`, generated by
`evidence/annotate_k_inventory.py`, attaches a disposition and rationale to
every one of those entries. Its SHA-256 and disposition counts are recorded in
`evidence/stage5-annotated-inventory.log`.

The supplied semantics entries are type-and-byte-identical to the selected
trusted semantics level. Seventy-seven entries form the reachable construct
slice and were checked in detail. The other 1,010 fixed entries are not
reachable from this submitted AST and contribute no candidate-local proof
power. Fourteen remaining structural entries and every candidate-local entry
are individually classified in the TSV.

### Used-construct mapping

| Submitted construct | Declaration and operational path |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| `FuncDef`, closure | `syntax.k:53`; `functions.k:14-16` |
| `Call`, parameters, return | `syntax.k:28,50,57,60`; `call.k:20-21,69-75`; `functions.k:63-66,78-90` |
| `Name` | `syntax.k:12`; `core.k:130-154` |
| integer literal | `syntax.k:9`; `core.k:194` |
| `If` | `syntax.k:49`; `controls.k:51-54` |
| `Compare`, `<`, `==` | `syntax.k:30,32`; `operators.k:15-17`; `int.k:22,26` |
| `BinOp("%",...)` | `syntax.k:15`; `operators.k:12`; `int.k:15,19-20` |
| `range(2,n)` | builtin lookup in `core.k:157-181`; call routing in `call.k`; `builtins.k:178`; `range.k` |
| `For` and loop target | `syntax.k:45`; `controls.k:65-74`; `tuple.k:31-34`; `range.k:20-24` |

Evaluation order is correct for the used slice: `BinOp` is sequentially strict,
`If` and `For` evaluate their condition/iterable, comparison contexts evaluate
left then right, calls evaluate callee then arguments left-to-right, and the
range iterable is evaluated once. `D>=2` prevents modulo by zero.

State is also exact for the used slice. Function call allocates scope 1, binds
the three arguments, the loop assigns `divisor` before each body execution,
early `Return` discards the function continuation, and `#pop` restores
environment/scope location and clears the return state. No used operation
allocates heap objects, mutates the heap, performs I/O, or raises an in-model
exception.

### Candidate-local inventory

The complete candidate-local proof extensions are:

1. three syntax macros: `xOrYLoopBody`, `xOrYBody`, and `#xOrY`;
2. function `primeSelect` with four guarded equations;
3. function `scanLast` with three guarded equations; and
4. the priority-40 loop summary rule.

There are no candidate-local `total`, `functional`, simplification,
`[owise]`, `[concrete]`, `symbol`, `no-evaluators`, or opaque declarations.

The `primeSelect` guards are pairwise disjoint and exhaustive on every use
(`D>=2`): `N<2`; `N>=2,D>=N`; and
`N>=2,D<N` split by `pyMod(N,D)==0` versus nonzero. The recursive equation
strictly increases `D` toward `N`.

The `scanLast` guards are likewise disjoint and exhaustive on its use domain
`N>=2,D>=2`. Its recursion strictly increases `D`, carrying the last assigned
divisor.

The loop summary is an operational bridge, but it has the required bridge-free
universal connection theorem: `loop_correct` imports only
`X-OR-Y-VERIFICATION`, not `X-OR-Y-SUMMARY`, and closes independently. The
summary's matched term, continuation, stack, bindings, guards, and every listed
cell are identical to the claim. Normalized lines compare with zero diff in
`evidence/stage5-loop-claim-summary-equivalence.log`. The only difference
outside the compared body is proof label versus rule priority.

The summary accepts no arbitrary continuation: its complete K cell is exactly
the remaining loop, trailing `Return(x)`, and `#endcall`. It reads the range,
local bindings, and fixed control state; it writes only the local `divisor`, K
control, and return cell as the proved claim states. `priority(40)` cannot
broaden its match.

### Soundness decision

No candidate-local rule is unsound. Consequently there is no unsoundness label
requiring a false-conclusion witness. The narrower evidence gap is the
direct-closure versus literal-module bridge described in Stage 4; no tested or
symbolic state shows a false returned value from it.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate mutation was trusted.
The reviewer created `evidence/spec-vacuity-fresh.k`.

The mutation uses the satisfying initial input `(N,X,Y)=(7,34,12)` and changes
the result-constraining target to the demonstrably false value `12`.

First, `kprove --dry-run` parses and builds the mutation successfully with exit
0 (`evidence/stage6-vacuity-build.log`). The actual proof then exits 1 with
`WarnStuckClaimState`. The residual K cell is:

```text
34 ~> .K
```

which cannot unify with the false destination `12`. This is the expected unmet
result obligation, not a parser error, missing import, timeout, unrelated
crash, or unreachable mutation. Exact command and bounded output are in
`evidence/stage6-vacuity-proof.log`.

The proof is therefore non-vacuous and discriminating.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the fixed supplied MPY semantics, the exact submitted `x_or_y` function
body, when directly invoked as the exact closure represented by `#xOrY`, has
this partial-correctness property for every K integer `N` and K values `X,Y`:

- if execution reaches a return, the returned value is
  `primeSelect(N,2,X,Y)`;
- `primeSelect` is `Y` for `N<2`;
- for `N>=2`, it is `Y` if trial division finds a divisor in `[2,N)`, and `X`
  otherwise.

The loop connection additionally proves the exact final `divisor` local and
return-control state for every `N>=2,D>=2`. The proof is partial correctness;
it does not separately establish termination in a different termination logic.

### Trust ledger

1. **K implementation and K builtins.** Integer arithmetic, Boolean logic,
   maps/lists, matching, reachability, and circularity implementation are part
   of the K toolchain trust base. All claims depend on this.

2. **Supplied MPY semantics.** The entire fixed semantics is a selected trusted
   input and was integrity-matched exactly. The used integer/control/call slice
   directly determines execution. This boundary is acceptable in
   `SUPPLIED_SEMANTICS` mode; candidate-local proof rules were not blessed by
   that match and were audited separately.

3. **Unused fixed opaque symbols.** The supplied semantics declares these 25
   symbol primitives: `sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`,
   `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`,
   `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
   `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`.
   None is reachable from `solution.mpy`, influences a branch or result, or is
   mentioned in either target claim. They are acceptable but irrelevant fixed
   trust boundaries.

4. **Translation and body identity.** Byte identity proves that the submitted
   `.mpy` is the trusted translator's output for `solution.py`. The translator's
   fidelity to CPython AST is an external trusted front-end boundary. Static
   constructor mapping and concrete full-module execution support this bridge.

5. **Direct-closure entry bridge.** It is an informal/static bridge that
   direct invocation of the exact closure is the target function call after
   module loading. It omits only the module binding and lookup. The exact body,
   defining scope, parameters, and fixed call semantics are present; the body
   never reads `x_or_y`. This is sound for this program but is the principal
   reason for `CONCERNS` instead of `PASS`.

6. **Modular proof import.** K does not turn the prior `#Top` log into a
   cryptographic theorem object. The main definition contains the loop claim as
   a rule. Independent bridge-free proof plus exact normalized body equality is
   the audit evidence that makes this modular step acceptable.

7. **Mathematical intent.** The fact that an integer `N>=2` is prime exactly
   when no integer in `[2,N)` divides it is ordinary mathematics. The K
   equations implement that definition. Differential tests are finite support,
   not a universal proof.

8. **Canonical domain.** Canonical/generated equivalence is empirically
   supported for positive integers 1 through 300 and follows structurally for
   that domain. It is false for `n<=0`; the generated implementation instead
   matches the prompt's mathematical prime/non-prime wording there. The prompt
   gives no explicit positivity precondition, so this limitation remains
   visible.

9. **Provenance records.** The missing generation metadata and trace cannot
   support any claim. The verdict relies only on independently reconstructed
   source, proof runs, static review, and reviewer-authored tests.

Differential tests, concrete execution, and this report do not substitute for
the K proof. They support only translation/body identity, the direct-closure
bridge, and natural-language adequacy.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
