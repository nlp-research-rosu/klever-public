# Independent adversarial audit — HumanEval 55-fib

The candidate contains a legitimate partial-correctness proof of the submitted
program over the intended natural-number input domain. I reconstructed the
semantics and proof from source, did not use either candidate-provided kompiled
directory, and independently checked provenance, program identity, claim
adequacy, every local K rule, body sensitivity, and non-vacuity.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `55-fib`, and condition
`kit-semantics`. The trusted `/reference/reference-semantics` tree is present,
so the mounts do not contradict the rendered mode.

All pipeline-v3 records required by the prompt are real regular files:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- the sole structured trace JSONL below
  `/generation-evidence/codex-trace/`.

The trace tree contains only real directories and a real regular file. The
candidate's required proof artifacts (`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, `prove.sh`, and `PROOF.md`) are likewise regular
files. No candidate supplied-semantics entry is a symlink or unsupported node.

Independent checks established:

- The JSON object in `/audit-campaign-lock.json` exactly equals the
  `audit_campaign` object in `/audit-input.json`.
- The campaign lock's SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- Every directly recorded file hash for the canonical, prompt, translator,
  run/task/result manifests, invocation, metrics, usage, generation prompt,
  last message, and output log matches the mounted bytes.
- The canonical pipeline tree hash of `/candidate` is
  `04012b97dddd6c04f537af64d5312d57b1e23f50ac1afd195919e80bee60d347`,
  matching both `generation-result.json` and `invocation.json`.
- The candidate and trusted semantics trees each have canonical pipeline tree
  hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching `task.json`.
- The generation trace tree hash is
  `190fee60368c6819e9c9bc8b7cd0ad198a64dc3164b01a81a76f4f0d0ba9b0a5`,
  matching `usage.json`.
- The candidate prompt and translator are byte-identical to the trusted
  mounts.
- A recursive relative-path, node-type, and per-file SHA-256 comparison found
  all 25 candidate supplied-semantics entries identical to the trusted tree,
  with no missing, additional, mistyped, changed, or linked entry.

The structured trace was parsed in full: 291 records, including all 26
generation shell calls and the construction's failed and successful proof
runs. The generation narrative and its earlier `#Top` are treated only as
untrusted history and are not used as audit proof evidence.

Evidence:

- `evidence/stage1_integrity.py`
- `evidence/stage1_integrity.log` (exit 0)
- `evidence/inspect_generation_trace.py`
- `evidence/generation_trace_summary.log` (exit 0)

There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt asks `fib(n: int)` to return the n-th Fibonacci number and
gives `fib(1) = 1`, `fib(8) = 21`, and `fib(10) = 55`. “n-th Fibonacci
number” makes `n` a natural-number index; the trusted recursive canonical has
the standard `0`, `1`, and `fib(n-1)+fib(n-2)` cases. Thus the intended
result-bearing domain is integer `n >= 0`.

There is no collection “empty” case. The relevant empty/boundary analogue is
the zero index, followed by the loop-guard boundary at `0/1` and the first
two-step value at `2`.

The submitted implementation is an iterative algorithm:

```python
a, b = 0, 1
while n > 0:
    b = a + b
    a = b - a
    n = n - 1
return a
```

Because assignments are sequential, the state transition is
`(a,b,n) -> (b,a+b,n-1)`.

### Regeneration and differential execution

In the clean scratch copy, the exact command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

produced SHA-256
`103d64645a70ab756fc825df0d3e25608bb10510fe88b6dbc17012ea54cd9efb`,
identical to the submitted `solution.mpy`; `cmp` exited 0.

The independent differential script imports the trusted mounted canonical
copy and the submitted solution copy using separate module loaders. It checks
the three documented examples, boundaries `0,1,2`, all values `0..30`, and a
seed-55 generated sample extending through `32` and `34`. All 33 unique
intended-domain cases agreed, with zero mismatches. This is finite fidelity
evidence, not the universal K proof.

Negative integers were recorded separately as an excluded-domain probe: the
trusted recursive canonical reaches `RecursionError`, while the iterative
candidate returns `0`. That is not a material intended-domain divergence; it
also explains why the formal precondition must not be read as covering
negative indices.

Evidence:

- `evidence/differential_test.py`
- `evidence/stage2_fidelity.log` (exit 0, complete inputs and rows)

## 3. Clean proof reconstruction

Only candidate source artifacts and the trusted semantics were copied into
`/tmp/audit-work/fib-audit`. Candidate `runtime-kompiled`,
`verification-kompiled`, caches, bytecode, logs, and traces were not copied or
used.

The observed independent toolchain is K v7.1.293 for `kompile`, `krun`, and
`kprove`. `kup` is absent, but the independently installed toolchain runs, so
the mandated `using-kit` live path applies.

### Concrete definition

The fresh LLVM build command was:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-audit-kompiled
```

It exited 0. The warnings concern unused variables and non-exhaustiveness in
supplied functions that are not used by this integer program.

`krun solution.mpy` exited 0 and displayed the loaded module state. In
particular, module scope `0` binds `"fib"` to `closureVal("n",
.ParamNames, BODY, 0)`, where `BODY` is exactly the submitted assignment,
while, and return sequence. All other final cells match the entry claim's
caller state.

A reviewer-authored fixture contains the exact same `fib` AST and assertions
for `-1,0,1,2,8,10,15`. AST identity was checked mechanically before
translation. Python and the fresh LLVM semantics both executed the fixture
with exit 0.

Evidence:

- `evidence/concrete_audit.py`
- `evidence/check_fixture_identity.py`
- `evidence/stage3_llvm_build.log` (exit 0)
- `evidence/stage3_concrete_execution.log` (exit 0 and loaded closure)

### Proof definition and positive targets

The fresh Haskell build command was:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

It exited 0. The two positive audit runs were:

```text
kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.loop-inv

kprove spec.k --definition verification-audit-kompiled \
  --spec-module SPEC
```

Each exited 0 and printed `#Top`. The first independently closes the helper
circularity. The complete run closes both `loop-inv` and the dependent
`fib-call` entry claim; the entry claim properly needs the loop claim
available as its circularity, so the complete run is the relevant independent
execution of that target.

Evidence:

- `evidence/stage3_haskell_build.log` (exit 0)
- `evidence/stage3_kprove_loop_inv.log` (`#Top`, exit 0)
- `evidence/stage3_kprove_all.log` (`#Top`, exit 0)

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-inv` says: from the exact internal loop head, with local
`n=N`, `a=A`, and `b=B` and `N >= 0`, the supplied semantics finishes the
loop with `n=0` and
`a=fibFrom(A,B,N)`. The final local `b` is existential because the entry
function returns only `a`. The outer scope map, arbitrary continuation, and
all omitted cells are framed and preserved.

`SPEC.fib-call` says: with `"fib"` bound to the exact one-parameter submitted
closure, calling it on any K integer `N >= 0` returns
`fibFrom(0,1,N)` and restores the shown caller environment, module/builtins
scopes, allocator, heap, stack, return, exception, and exit-code state.

The helper is fully defined:

- `fibFrom(A,B,N) = A` when `N <= 0`;
- `fibFrom(A,B,N) = fibFrom(B,A+B,N-1)` when `N > 0`.

For `N >= 0`, this is exactly the first component after `N` standard
Fibonacci transitions. It is result-constraining, not a free variable,
oracle, implication-only summary, or tautology.

### Mechanical pinning

The claim does not start by loading the whole module, which is permitted only
if the binding/body identity is mechanically established. I established that
identity in three independent ways:

1. trusted translation regenerates the submitted `solution.mpy` byte for byte;
2. the fresh LLVM module-load state displays the exact claimed parameter,
   body, parent scope `0`, module parent `-1`, and surrounding cells; and
3. `extract_claim_program.py` extracts the exact closure term from
   `SPEC.fib-call`, removes only the explicit `.Stmts` list-unit spelling,
   reconstructs a module, and parses both terms with `kast --sort Module
   --expand-macros --output json`.

The two constructor JSON files are byte-identical and share SHA-256
`e38d1862293c2531d6743d4dc7140697b4f9b6b640b31983a3036b27f6f3111d`.
Thus the claim executes the submitted function binding and body, not a
substituted program.

The real entry execution reaches the helper claim with environment `1`, local
scope `1`, the exact three local values, the exact `#while` condition/body,
and the actual trailing `Return(Name("a"))`. The loop claim's framed
continuation therefore contains the real return and frame-pop behavior rather
than bypassing it.

Evidence:

- `evidence/extract_claim_program.py`
- `evidence/stage4_constructor_identity.log` (exit 0)
- `evidence/used_construct_map.md`

Two earlier reviewer-only constructor comparison attempts are preserved as
`stage4_constructor_identity_attempt1.log` and
`stage4_constructor_identity_attempt2.log`: they used the wrong parser start
sort and then an internal list-unit spelling. They are test-scaffolding
errors, not candidate proof failures; the corrected constructor comparison
above is the relied-on result.

### Satisfying witnesses and substitutions

The entry precondition is satisfiable, for example by the exact displayed
caller state with `N=0`; the concrete run exhibits that loaded state. The same
construction works for every ground nonnegative integer.

For `N = 0,1,2,8,10`, the ground helper results are respectively
`0,1,1,21,55`. A k-cell ground spec printed `#Top`, and an independent script
confirmed every value against both Python implementations. The initial
reviewer attempt used unsupported bare functional claims; its diagnostic is
preserved as `stage4_ground_substitutions_attempt1.log`. The corrected
configuration claims and comparisons are in:

- `evidence/spec-summary-ground.k`
- `evidence/substitute_claim_results.py`
- `evidence/stage4_ground_substitutions.log` (`#Top`, exit 0)

### Body sensitivity

A fresh operational-sensitivity mutation changes the actual closure body to
compute `b = a + b + 1`, while retaining the original claimed result for
input `1`. The mutation parsed successfully, then `kprove` exited 1 with
`WarnStuckClaimState` and a terminal actual result `2`. This changes the term
executed by the claim itself; it is not merely an edit to an external source
file.

Evidence:

- `evidence/spec-body-sensitivity-audit.k`
- `evidence/stage4_body_sensitivity.log`

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.md` inventories every declaration block from the
assembled supplied `reference-semantics/semantics.k`, every required helper K
file, `verification.k`, and `spec.k`, with full text and source line. The
inventory contains:

- 26 source files, 28 modules, 29 file requirements, and 92 imports;
- 228 syntax blocks, one configuration, and five contexts;
- 698 rules (695 supplied-semantics rules plus three proof-local rules);
- two reachability claims;
- 146 blocks with `function`, 108 with `total`, no `functional`
  declaration, 25 named `symbol` declarations, and 22 explicit
  `no-evaluators` opaque blocks;
- 45 priority-bearing rule blocks, 26 `owise` rule blocks, 35
  concrete-bearing rule blocks, and one simplification rule.

`evidence/rule_review.tsv` gives each of the 698 rules a separate
file/line/category/relevance/disposition row. Of these, 31 are on the symbolic
fib path, two additional rules perform module loading/binding for the pinning
check, 16 are in the LLVM-only `MPY-CONCRETE` module, and 649 are excluded by
constructor, literal operator tag, sort, guard/shape, or import reachability.
No supplied rule contains `fib` or `Fibonacci`.

### Used syntax and fixed-semantics execution

`evidence/used_construct_map.md` maps every constructor in `solution.mpy` to
its declaration and execution rules. The material chain is:

```text
Call/name lookup -> left-to-right argument evaluation -> exact closure frame
-> parameter bind -> sequential assignments -> while guard and body
-> return evaluation -> frame pop and caller restoration
```

The relevant guards and overlaps are sound:

- plain-scope assignment/lookup rules apply; their higher-priority cell
  alternatives require a `"$cells"` marker absent from this frame;
- the generic call route is `owise`, but none of the supplied syntactic
  math/hash interceptors matches `Call(Name("fib"), ...)`;
- integer `+`, `-`, and `>` cases are sort- and operator-tag-specific;
- the while true/false guards are complementary after the integer comparison
  yields Bool;
- the closure rule allocates fresh scope `1`, saves the exact continuation,
  caller environment, and allocator, and the pop rule restores/deallocates
  precisely those components; and
- K-generated strict/seqstrict heating gives the required evaluation order.

The loop circularity matches the real `#while` term and actual continuation.
It does not introduce return, pop, exception, cleanup, allocation, or another
abrupt operational bridge. Fixed rules execute those effects.

### Proof-local extensions

There are exactly three:

1. `fibFrom(A,_B,N) => A` for `N <= 0`;
2. `fibFrom(A,B,N) => fibFrom(B,A+B,N-1)` for `N > 0`; and
3. `(A +Int B) -Int A => B [simplification]`.

The first two are a definitional summary, not operational rules: they match
only `fibFrom` terms, read/write no cells, have disjoint and exhaustive
integer guards, and recurse only while positive `N` strictly decreases. The
successful loop claim is the bridge-free fixed-semantics connection theorem
from the actual loop to that summary.

The third is a derived mathematical lemma over K's unbounded mathematical
integers. It is the universal additive-group identity `(A+B)-A=B`, decreases
term size, and has no conflicting proof-local equation. It simplifies the
state produced after the real sequential assignments; it does not replace a
program term or state transition.

There are no proof-local priority rules, ordinary operational rewrites,
unconstrained result symbols, call interceptions, or task-answer encodings.
Consequently no operational-bridge connection theorem or opposite oracle
interpretation is missing.

### Supplied but unused boundaries

The supplied semantics deliberately contains symbolic opaque primitives for
other HumanEval tasks. The complete named-symbol list is:

`sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`,
`floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
`mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, and `sqrtF`.

They are result-bearing trust boundaries for programs that use sorting,
hashing, or floats, but none of their constructors, dispatch routes, or
dependents is reachable from this integer-only submitted program or either
claim. Other supplied subset limitations—ASCII-oriented strings,
underspecified invalid indexing, and omitted Python exception behavior—are
also absent from the submitted path. I found no rule that can enable a false
fib conclusion on `N >= 0`; accordingly I make no unsupported “unsound rule”
allegation and no false-witness obligation arises.

Evidence:

- `evidence/inventory_k_rules.py`
- `evidence/rule_inventory.md`
- `evidence/review_all_rules.py`
- `evidence/rule_review.tsv`
- `evidence/rule_inventory_generation.log`
- `evidence/rule_review_generation.log`
- `evidence/stage5_static_checks.log`

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation
`evidence/spec-vacuity-audit.k` keeps the exact submitted closure, chooses
the satisfying and loop-exercising input `8`, and changes only the required
result from the true `21` to the false `22`.

First,

```text
kprove spec-vacuity-audit.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --dry-run --output none
```

completed successfully, establishing that the mutation builds and parses.
The actual proof command then exited 1, emitted `WarnStuckClaimState`, and
showed terminal `<k> 21 ~> .K </k>` failing to unify with the destination
`22`. This is the expected unmet result obligation, not a parser error,
missing import, timeout, or unrelated crash.

Evidence:

- `evidence/spec-vacuity-audit.k`
- `evidence/stage6_fresh_nonvacuity.log`

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` definition and the audited proof-local equations, for
every mathematical K integer `N >= 0`, execution of the exact submitted
`fib` closure from the stated caller state is partially correct: if it
terminates normally, the returned value is `fibFrom(0,1,N)`, and the listed
caller state is restored. The loop theorem establishes the corresponding
summary from arbitrary integer accumulators `A,B` and nonnegative remaining
count `N`.

The proof is universal over `N >= 0`; it is not a finite unrolling, an example
set, or a fixed-size theorem.

### Trusted or informal boundaries

1. **Supplied MPY semantics.** Its configuration, integer/control/call rules,
   and K-generated heating/cooling are the language-model trust base. This is
   acceptable because the condition explicitly supplies that semantics, its
   tree is byte-identical to the trusted mount, every local rule was
   inventoried, and all material operations execute under its fixed rules.
2. **K toolchain and logic.** K v7.1.293, the Haskell and LLVM backends, SMT
   implication checking, K's mathematical `Int`/`Bool`/`Map`/`List`
   primitives, and host hooks are trusted. This is the normal proof-checker
   boundary.
3. **Trusted translator.** `py2mpy.py` is outside the K theorem. Its exact
   mounted bytes match provenance; regeneration is byte-identical; and KAST
   constructor comparison pins the resulting function body. This boundary is
   acceptable.
4. **Fibonacci intent bridge.** Identifying the first component of repeated
   `(A,B)->(B,A+B)` transitions from `(0,1)` with the zero-indexed Fibonacci
   sequence is ordinary mathematics and matches the trusted recursive
   canonical. It does not introduce an oracle.
5. **Source-domain interpretation.** `n` is a natural-number index, hence
   `N >= 0`. This is supported by the phrase “n-th Fibonacci number,” the
   examples, and the trusted canonical's only normal base cases. Negative
   integers are explicitly excluded rather than silently claimed.
6. **Finite empirical evidence.** Python differential tests and LLVM
   assertions support only the source/constructor/semantics bridges on their
   recorded inputs. They do not substitute for the universal K proof.
7. **Unused supplied opaque symbols.** The 25 names listed in Stage 5 are
   assumptions only for programs whose execution reaches them. Neither fib
   claim depends on one.

Termination as a separate liveness theorem, behavior for negative or
non-integer inputs, CPython correctness, and the correctness of K itself are
not claimed.

### Gate and benchmark decision

- Gate A (real-program soundness): PASS.
- Gate B (intent adequacy): PASS; `N >= 0` covers the material source-contract
  domain.
- Gate C (trust/evidence auditability): PASS; all relied-on artifacts,
  commands, scopes, and assumptions are explicit and reproducible.

The successful proof is sound, result-constraining, non-vacuous, and
mechanically pinned to the regenerated submitted program. There is no
material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
