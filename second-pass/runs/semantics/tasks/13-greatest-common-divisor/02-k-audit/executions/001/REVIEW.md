# Independent adversarial audit: 13-greatest-common-divisor

## Executive decision

The submitted Python program is faithfully translated, is pinned by the K
claims, and agrees with the ordinary nonnegative mathematical gcd on extensive
finite testing. Fresh LLVM and Haskell definitions build, all four submitted
claims separately return `#Top`, and an independently authored false
off-by-one postcondition fails for the expected unmet equality.

Those successes do **not** constitute a legitimate proof of the real loop.
`verification.k:51-58` adds a priority operational rule that removes the whole
`#while` computation and directly writes the desired `gcdSpec(A,B)` into `a`.
The final universal postcondition uses the same opaque symbolic term. There is
no bridge-free reachability theorem proving that the supplied semantics
executes the loop to that state; `euclid-step` proves only one tuple-assignment
step. Thus the main result is an assumption installed as an executable proof
rule, not a consequence established about the program.

This is a candidate legitimacy failure, not an audit-infrastructure failure.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`. The required trusted tree
`/reference/reference-semantics` exists and is an ordinary directory. An
independent `lstat`/SHA-256 traversal found 25 entries in each tree and zero
differences:

- no missing or additional candidate entries;
- no type mismatches;
- no symlinks;
- no byte differences.

The candidate prompt and translator are regular files and are byte-identical to
the trusted versions:

- `prompt.py`:
  `a7946546bc3a483bb5f2249ced878d510d6765d3c987a3e56dd878fe5bb60c19`
- `py2mpy.py`:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The complete command, status, and output are in
[`evidence/stage1_integrity.log`](evidence/stage1_integrity.log); the independent
checker is [`evidence/integrity_check.py`](evidence/integrity_check.py).

### Missing generation records

The following requested untrusted provenance artifacts are absent from
`/candidate`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- any filename suggesting a structured generation trace

This is a provenance/auditability gap. It is not an infrastructure breach
because all trusted inputs, supplied semantics, candidate source, program,
specification, and proof module needed for independent execution are present.
The existing `prove.log`, `prove.sh`, concrete tests, and prose comments were
read only as untrusted claims. No candidate-compiled definition or cache was
copied or reused.

The live toolchain was independently found at `/usr/bin`; `kompile`, `kprove`,
and `krun` all report K `v7.1.337`.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and implementations

`/reference/prompt.py` asks for
`greatest_common_divisor(a: int, b: int) -> int`, “a greatest common divisor of
two integers,” with examples `(3,5) -> 1` and `(25,15) -> 5`. It states no sign
or magnitude restriction.

`/reference/canonical.py` implements Euclid's loop directly:

```python
while b:
    a, b = b, a % b
return a
```

`/candidate/solution.py` first applies `abs` to both arguments, then iterates
while `b != 0`. It therefore returns the conventional nonnegative gcd for
arbitrary Python integers, including signed zero-boundary cases.

### Translation fidelity

From the scratch copy, the trusted command was:

```text
python3 /tmp/audit-work/source/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/solution.regenerated.mpy
```

It exited 0. `cmp -s` against the submitted `solution.mpy` exited 0, and both
files have SHA-256
`5d14d8f54a5051b7d84fb8c61fe12eb2330f21f81e7e2ddb8ad78170a7677197`.
Commands and statuses are in
[`evidence/stage2_fidelity.log`](evidence/stage2_fidelity.log).

### Independent differential execution

[`evidence/differential_gcd.py`](evidence/differential_gcd.py) imports the
trusted canonical entry point and submitted entry point independently. It
exercises:

- both documented examples;
- `(0,0)`, either argument zero, signs around zero, and `b == 0`/`b != 0`;
- equality, unit, exact-divisibility, one-step, and coprime cases;
- every ordered pair in `[-64,64]^2`;
- 2,000 deterministic random pairs in `[-10^18,10^18]^2`;
- structured arbitrary-precision values through 256 bits.

The run completed with exit 0 over 18,725 unique pairs and no exceptions. The
submitted implementation had zero mismatches with independent `math.gcd`.
There were 9,355 trusted-canonical/submitted mismatches, all reflecting the
canonical implementation's negative-sign result when its terminal `a` is
negative. Examples include canonical `(0,-9) -> -9` versus submitted and
`math.gcd` value `9`.

The divergence is real and fully preserved in
[`evidence/stage2_results.tsv`](evidence/stage2_results.tsv). It does not make
the submitted program incorrect for the natural-language contract: a
“greatest” common divisor is conventionally nonnegative, and the submitted
implementation matches that interpretation. It does mean the finite
canonical comparison cannot itself serve as the intent oracle for signed
inputs. Full inputs, hashes, and the bounded summary are in
[`evidence/stage2_inputs.tsv`](evidence/stage2_inputs.tsv) and
[`evidence/stage2_summary.json`](evidence/stage2_summary.json).

These tests are finite adequacy evidence only, not a proof.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/source`; no
candidate-built definition, `__pycache__`, or cache was reused.

### Fresh concrete definition

The following fresh build exited 0:

```text
kompile /tmp/audit-work/source/reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/source/runtime-kompiled --warnings none
```

An independently authored concrete MPY probe checked both prompt examples,
zero cases, all sign quadrants, and a coprime case. Translation exited 0;
`krun ... --definition runtime-kompiled` exited 0 and ended with `.K`,
`NoExc`, and exit code 0. Source and outputs:

- [`evidence/stage3_concrete_probe.py`](evidence/stage3_concrete_probe.py)
- [`evidence/stage3_concrete_probe.log`](evidence/stage3_concrete_probe.log)

### Fresh proof definition and every positive claim

The fresh Haskell build exited 0:

```text
kompile /tmp/audit-work/source/verification.k --backend haskell --main-module GCD-VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/source/verification-kompiled --warnings none
```

Every submitted target was then run separately:

| Claim | Exit | Output |
|---|---:|---|
| `euclid-step` | 0 | `#Top` |
| `program-correct` | 0 | `#Top` |
| `example-3-5` | 0 | `#Top` |
| `example-25-15` | 0 | `#Top` |

Exact commands and outputs are in the four
`evidence/stage3_claim_*.log` files and the bounded aggregate
[`evidence/stage3_rebuild_master.log`](evidence/stage3_rebuild_master.log).

This stage establishes verification closure under `MPY` **plus all rules in
`GCD-VERIFICATION`**. It does not independently establish that those added
rules follow from the supplied semantics.

## 4. Adequacy and real-program pinning

### Claims in plain language and satisfiable preconditions

1. `euclid-step` starts with a local environment location `L` whose exact local
   map contains integer `a=A` and `b=B`, an empty heap, `A >= 0`, and `B > 0`.
   It claims that executing the exact submitted tuple assignment terminates
   with `a=B` and `b=pyMod(A,B)`, preserving the surrounding scope map and
   parent. A satisfying state is `L=1`, `A=25`, `B=15`, parent 0, empty heap;
   its post-state is `a=15`, `b=10`.

2. `program-correct` has no explicit arithmetic restriction beyond
   `A0:Int,B0:Int`. Starting from the standard empty module scope and builtins
   scope, it loads the submitted function and calls it. It claims the returned
   K value is exactly `gcdSpec(absInt(A0),absInt(B0))`, while the module scope
   gains exactly the function closure. The initial configuration is
   satisfiable for every integer pair. At `(25,15)`, the right-hand side,
   trusted canonical implementation, and submitted implementation are all 5.

3. `example-3-5` has the same concrete initial configuration and claims the
   exact return value 1. Both Python implementations return 1.

4. `example-25-15` similarly claims 5. Both Python implementations return 5.

The executable witness record is
[`evidence/stage4_witnesses.log`](evidence/stage4_witnesses.log).

### Actual-program identity

The specification does not read `solution.mpy` at proof time; it uses
`Module(GcdDef)`, so the duplicate macro tree required an independent pinning
check. Both the trusted regenerated `solution.mpy` and `Module(GcdDef)` were
parsed in `GCD-VERIFICATION` with `--expand-macros --output kore`. The expanded
KORE files are byte-identical and share SHA-256
`acb7fe33d7d4d7006e9a640292ffe92dfa94eb464d1046df1966ace090d4b9c7`.
The final successful commands and statuses are in
[`evidence/stage4_pinning.log`](evidence/stage4_pinning.log). A first preserved
attempt used an explicit program-parser `.Stmts` terminator and failed to parse;
[`evidence/stage4_pinning_attempt1.log`](evidence/stage4_pinning_attempt1.log)
is not used as positive evidence.

Thus the claim is pinned to the real submitted constructor program, not a
substitute.

### Adequacy failure inside the pinned execution

The program reaches the exact `#while(GcdCondition,GcdLoopBody)` term, but
`verification.k:51-58` then preempts the supplied while semantics. Instead of
evaluating the condition, executing the body, and returning to the loop head,
the added rule deletes the loop and changes the local bindings from
`a=A,b=B` to `a=gcdSpec(A,B),b=0`.

The postcondition is therefore result-constraining but circular: it asks for
the exact opaque term that the operational bridge itself inserted. Real-program
pinning does not repair this missing execution-to-summary connection.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/stage5_rule_inventory.md`](evidence/stage5_rule_inventory.md)
line-addresses and normalizes every declaration and rule in all 24 supplied K
files, `verification.k`, and `spec.k`. Its 946 items comprise:

- 703 rules: 594 ordinary, 46 priority, 37 concrete, and 26 `owise`;
- 233 syntax declarations, including 123 function-syntax entries, nine macro
  entries, and 23 `no-evaluators` opaque-symbol entries;
- five contexts, one configuration, and four claims;
- 115 occurrences of `total` across 107 declarations;
- no `functional` declaration and no simplification rule.

The inventory generator, summary, exact command, and status are:

- [`evidence/build_rule_inventory.py`](evidence/build_rule_inventory.py)
- [`evidence/stage5_rule_inventory_summary.json`](evidence/stage5_rule_inventory_summary.json)
- [`evidence/stage5_inventory.log`](evidence/stage5_inventory.log)

An earlier inventory pass over-counted attributes appearing inside comments or
map brackets; it is preserved as
[`evidence/stage5_inventory_attempt1.log`](evidence/stage5_inventory_attempt1.log)
and is not used for the counts above.

### Supplied-semantics rules

Items 1-928 are exactly the trusted supplied-semantics tree. Under the rendered
mode they are the selected fixed operational semantics, and the recursive
integrity check proves that the candidate neither changed nor supplemented
them. I reviewed the inventory for declarations, guards, overlaps, priorities,
totality, and opaque values. Nothing in the fixed tree is candidate-local
answer encoding.

Of the 22 fixed `no-evaluators` symbols (float operations, sort summaries, and
MD5), none is reachable from this integer GCD program or its claims. They
cannot affect its control, state, result, or proof. The fixed `MPY-CONCRETE`
module is present only in the LLVM build; the Haskell proof imports `MPY` and
does not receive those concrete-only operational rules.

The constructs actually used by `solution.mpy` map as follows:

| Program construct | Declaration and operative supplied rules |
|---|---|
| `Module`, statement sequence | `syntax.k:56,61`; `core.k:124-127` loads and sequences statements left-to-right |
| `FuncDef` | `syntax.k:53`; `functions.k:14-16` creates a closure in the current scope |
| `Call`, `Name`, arguments | `syntax.k:12,28`; `core.k:130-152,157-191`; `call.k:20-21,69-74` perform lexical lookup, left-to-right argument evaluation, parameter binding, frame creation, and call dispatch |
| `abs` | `core.k:157-180` binds the builtin; `call.k:31`; `builtins.k:44` returns trusted K `absInt` |
| name assignment | `syntax.k:41` makes the RHS strict; `controls.k:9-18` updates the current local scope |
| `While` and `b != 0` | `syntax.k:9,30,46`; `controls.k:77-82`; `operators.k:15-17`; `int.k:27`; `core.k:199-205` evaluate the integer guard and either run the body or fall through |
| tuple RHS and `%` | `syntax.k:15,21`; `tuple.k:14-16`; `operators.k:12`; `int.k:15,19-20` evaluate both tuple elements before binding and implement Python-style modulo |
| tuple target assignment | `tuple.k:31-57` unpacks the already evaluated tuple left-to-right into the local names |
| `Return` | `syntax.k:50`; `functions.k:78-90` stores the value, discards the remaining function body, pops the frame, and restores the caller |

For the reachable integer states, the supplied evaluation order and state
footprints match the Python program: both arguments are bound before the body,
both `abs` calls precede the loop, the tuple RHS is fully evaluated before
either target changes, `%` is never evaluated with zero divisor, and return
restores the caller without heap allocation or observable output.

### Candidate-local items 929-942

1. **`GcdDef`, `GcdBody`, `GcdCondition`, `GcdLoopBody`, and `GcdClosure`
   declarations/rules (`verification.k:9-35`)** are definitional macros. Their
   equations are non-overlapping and terminating. The expanded-KORE identity
   check establishes that the program macros exactly denote the submitted
   program. `GcdClosure` also matches the closure shape made by fixed
   `functions.k`.

2. **`gcdSpec` (`verification.k:39-46`)** is a program-derived,
   result-bearing opaque function. The `B=0` and `B>0` concrete equations are
   disjoint. On nonnegative ground arguments they cover the uses, and the
   Euclidean remainder gives descent for `B>0`. On negative or symbolic
   arguments they deliberately remain opaque. The equations are ordinary
   mathematical Euclidean recurrence, but there is no separate formal theorem
   in the submission that this symbol denotes “greatest common divisor.” More
   importantly, the same opaque symbol is used both in the operational bridge
   and in the final postcondition.

3. **Full-loop priority bridge (`verification.k:51-58`)** matches the exact
   submitted `#while`, any trailing continuation, environment location `L`,
   and a local scope whose integer `a=A,b=B` are nonnegative. It reads and
   writes the local scope, frames the heap, stack, return, exception, allocation
   and exit cells, preserves the arbitrary continuation, sets `b=0`, and places
   `gcdSpec(A,B)` in `a`. Priority 40 intentionally preempts
   `controls.k:78`, the fixed rule that would evaluate the condition.

   For this exact side-effect-free body, the asserted Euclidean summary is
   mathematically plausible and finite ground execution supports it. I do
   **not** label the equation extensionally false, so no false-conclusion
   witness is claimed for it. The narrower, material defect is that it is an
   unsupported operational bridge and encodes the task answer. The mandatory
   bridge-free universal connection theorem over its complete match domain
   does not exist. `euclid-step` begins with `GcdLoopBody`, not with
   `#while`; it proves one assignment only and does not establish iteration,
   the zero branch, repeated preservation, or connection to `gcdSpec`.

   A fresh definition with this single operational bridge removed compiled
   successfully. Running the universal claim with `--depth 80` exited 1 with
   `WarnStuckClaimState`; the residual already exposes the unproved symbolic
   base connection
   `absInt(A0) == gcdSpec(absInt(A0),0)`, with an unexplored loop branch.
   Exact source, commands, and output:

   - [`evidence/verification-no-bridge.k`](evidence/verification-no-bridge.k)
   - [`evidence/spec-no-bridge.k`](evidence/spec-no-bridge.k)
   - [`evidence/stage5_no_bridge_proof.log`](evidence/stage5_no_bridge_proof.log)

   This diagnostic is not presented as a proof that the mathematical summary
   is false. It shows that the submitted `#Top` depends on the answer-bearing
   axiom and that the required fixed-semantics connection proof was not supplied.

### Candidate claims 943-946

The four `spec.k` items are reachability obligations, not semantic rules.
`euclid-step` is a valid exact body-execution lemma under its satisfiable guard.
The examples are true ground consequences of the extended theory and real
execution. `program-correct` is universally result-constraining, but its
closure depends on the unsupported full-loop bridge above.

Static Gate A therefore fails even though the dynamic claims close. The
supplied-semantics trust boundary does not bless rules in `verification.k`.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was relied upon. I created
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k), a distinct module that
changes the universal result to:

```text
gcdSpec(absInt(A0), absInt(B0)) +Int 1
```

The witness `(A0,B0)=(25,15)` satisfies the original entry state; real Python,
the submitted Python, and the ground recurrence return 5, while the mutation
demands 6.

The mutation first passed a parser/build-only run:

```text
kprove /tmp/audit-work/source/spec-vacuity.k --definition /tmp/audit-work/source/verification-kompiled --spec-module GCD-SPEC-VACUITY --claims false-off-by-one --dry-run --warnings none
```

Exit status: 0.

The actual proof command, without `--dry-run`, exited 1 and emitted
`WarnStuckClaimState`. Its residual contains the expected failed implication
between `gcdSpec(...)` and `gcdSpec(...) +Int 1`; there was no parser error,
missing import, timeout, or unrelated crash.

Exact commands, status, and residual:

- [`evidence/stage6_dry_run.log`](evidence/stage6_dry_run.log)
- [`evidence/stage6_false_proof.log`](evidence/stage6_false_proof.log)
- [`evidence/stage6_nonvacuity_master.log`](evidence/stage6_nonvacuity_master.log)

Non-vacuity passes: the extended theory discriminates a false result. This does
not validate the theory's operational bridge.

## 7. Proven versus assumed accounting

### What the successful K runs actually establish

Under the fixed supplied `MPY` semantics **augmented by every rule in
`GCD-VERIFICATION`**, K establishes:

- the exact tuple-assignment body maps nonnegative `A,B>0` to
  `B,pyMod(A,B)`;
- the exact submitted program reaches the symbolic term
  `gcdSpec(absInt(A0),absInt(B0))`;
- the two prompt instances reach 1 and 5;
- the postcondition is not vacuous, because an off-by-one result does not close.

The universal reachability run does not establish the full loop summary from
the fixed semantics. That summary is an axiom in the augmented theory.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted supplied `MPY` tree | All parsing, control, scopes, calls, state, and return behavior | Acceptable by `SUPPLIED_SEMANTICS`; candidate tree is identical |
| K `v7.1.337` frontend/backends and builtin INT/BOOL/MAP/STRING hooks, including `absInt` | Arithmetic and proof execution | Ordinary toolchain/low-level trust boundary |
| Trusted CPython AST translator | Program constructor identity | Acceptable; byte identity independently checked |
| `gcdSpec` concrete equations | Ground recurrence and example results | Mathematically reasonable on nonnegative ground inputs; opaque symbol itself is not a proved intent theorem |
| `verification.k:51-58` full-loop rule | Entire universal returned value and loop state | **Illegitimate**: answer-bearing operational bridge with no bridge-free connection theorem |
| Informal Euclidean argument | Why the asserted bridge appears true | Not machine-checked in the candidate and cannot substitute for the missing reachability theorem |
| Differential tests against `math.gcd` | Finite implementation-to-intent bridge | Supportive over 18,725 cases only; not universal and not a K proof |
| Missing generation records | Provenance of how candidate was generated | Auditability concern; does not alter reconstructed source behavior |

### Final gate assessment

- Dynamic reconstruction: pass.
- Real-program identity and result constraint: pass.
- Fixed-semantics connection / proof-extension soundness: **fail**.
- Natural-language intent alignment: supported for conventional nonnegative
  gcd; the trusted canonical's signed-result behavior is separately documented.
- Non-vacuity: pass.
- Provenance completeness: concern.

The candidate program is likely correct, but the candidate does not contain a
legitimate partial-correctness proof of that fact. The main theorem was inserted
as an operational rewrite rather than derived through a loop invariant or an
exact bridge-free auxiliary reachability proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
