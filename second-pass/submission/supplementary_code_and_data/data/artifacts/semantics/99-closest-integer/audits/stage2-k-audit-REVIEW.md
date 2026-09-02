# Independent adversarial audit: 99-closest-integer

The candidate is **not a legitimate partial-correctness proof of the HumanEval
contract**. A clean reconstruction does produce `#Top`, the submitted
constructor body is genuinely executed, and a fresh false postcondition is
rejected. However, the theorem's postcondition merely gives a name to the
program's `float ± 0.5`/truncate computation. That computation is not a
closest-integer function over the prompt's unrestricted numeric-string domain.
In addition, the used supplied-semantics parser for `float(str)` is observably
different from Python on valid numeric strings such as `"1e1"`.

Two concrete witnesses determine the verdict:

- `solution.closest_integer("9007199254740991")` returns
  `9007199254740992`. The trusted canonical implementation returns
  `9007199254740991`, which is also plainly the closest integer to this already
  integral value. Binary64 rounds `9007199254740991.0 + 0.5` to the even
  neighbor `9007199254740992.0`.
- The K semantics makes `decStrToF(codes("1e1"))` parse as `631.0`, so the K
  execution returns `631`. Both Python implementations return `10`. The
  exponent form is a valid string representation of a number and the prompt
  imposes no spelling restriction.

## 1. Input and provenance integrity

The declared record layout is `legacy-selected-stage1` and the rendered
semantics mode is `SUPPLIED_SEMANTICS`. The required trusted
`/reference/reference-semantics` mount is present, so the mounts do not
contradict the rendered mode.

I read and independently hashed:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the complete
  156-record structured JSONL trace;
- the trusted prompt, canonical implementation, and translator; and
- every candidate file and every supplied-semantics entry.

The exact check and output are
[`evidence/01_provenance_check.py`](evidence/01_provenance_check.py) and
[`evidence/01_provenance_check.log`](evidence/01_provenance_check.log). It
exited 0. Findings:

- `/audit-campaign-lock.json` is JSON-identical to the `audit_campaign` block
  and its SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every launcher-required record is a readable regular file. No candidate,
  trusted-input, generation-record, or semantics entry is a symlink or special
  file.
- All individually recorded launcher hashes match, including the run/task/
  generation-result manifests, generation prompt/log/trace records, canonical,
  prompt, and translator.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  versions.
- The candidate and trusted `reference-semantics/` manifests contain the same
  25 entries (one subdirectory and 24 files), with identical per-file hashes
  and no additions, omissions, type changes, or symlinks. The reviewer
  manifest digest of both trees is
  `c9d5d164df7f4f2318a280b9b9faab7e52c8e8ae500adcb11adce70b24190d20`.
- All five required candidate proof deliverables are present and regular.

The retained `usage.json` internally claims source-trace SHA-256
`cf91eaf4...`, while the retained JSONL file hashes to `afe21af0...`.
The latter is the hash declared by both `invocation.json` and
`generation-result.json`, and those retained records match their
launcher-recorded hashes. I treat the `usage.json` field as an inconsistent
untrusted legacy claim, not as an absent/unreadable mount or infrastructure
breach. Historical runtime metrics are absent, as permitted for this record
layout.

The generation report's `KPROVE_PASSED` and prior trace were not used as proof
evidence. No audit infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every string representing a number, return its closest integer. At an exact
halfway point, choose the integer farther from zero. The prompt provides no
bound on magnitude, precision, or accepted numeric spelling.

The trusted canonical first parses with Python `float`, recognizes lexical
decimal half cases, and otherwise uses Python `round`. The submitted
implementation instead always parses with `float`, then returns:

```text
int(number + 0.5) if number > 0.0 else int(number - 0.5)
```

That formula is a familiar real-arithmetic shortcut, but executing its addition
in binary64 makes it invalid at large representable integers.

### Translation identity

From the scratch copy, I ran:

```text
python3 /tmp/audit-work/candidate-src/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
cmp /tmp/audit-work/candidate-src/solution.regenerated.mpy \
  /tmp/audit-work/candidate-src/solution.mpy
```

Both commands exited 0. Both `.mpy` files have SHA-256
`03b8b5404453ce9bc22c44f48cde9d11866c6cbe1cd4ce147f6a40c0781579e3`.
See [`evidence/02_translation_identity.log`](evidence/02_translation_identity.log).

### Independent differential execution

[`evidence/02_differential.py`](evidence/02_differential.py) independently
imports `/reference/canonical.py` and the scratch `solution.py`. It runs all
documented examples; empty/invalid spellings; zero; positive and nonpositive
branches; both sides of half boundaries; trailing-zero and exponent forms;
binary64 precision boundaries; 75 generated near-half strings; and 100
deterministically generated decimal strings. It also uses `Decimal` with
half-away rounding as a separate direct interpretation of the natural-language
contract.

Exact command:

```text
python3 /audit-output/evidence/02_differential.py
```

It intentionally exited 1 after reporting mismatches. All 223 inputs and their
input-set digest are in
[`evidence/02_differential.log`](evidence/02_differential.log). The documented
examples pass, but there are 31 generated-versus-canonical mismatches and 32
generated-versus-direct-contract mismatches.

The decisive implementation witness does not depend on a subtle lexical
interpretation:

```text
input:       "9007199254740991"
generated:   9007199254740992
canonical:   9007199254740991
closest:     9007199254740991
```

This is a material result divergence on the prompt's intended domain.

## 3. Clean proof reconstruction

I copied only candidate source artifacts plus the trusted prompt, translator,
canonical, and trusted supplied semantics to
`/tmp/audit-work/candidate-src`. Candidate caches and compiled definitions were
not copied or reused. The toolchain is K `v7.1.293`; see
[`evidence/03_toolchain.log`](evidence/03_toolchain.log).

### Concrete definition

Exact command:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0. The build log is
[`evidence/03_runtime_build.log`](evidence/03_runtime_build.log). The compiler
reported several non-exhaustive-totality warnings in supplied helpers; none
prevented the build.

The candidate smoke program ran with:

```text
krun smoke.mpy --definition audit-runtime-kompiled
```

It exited 0 with final `.K`; see
[`evidence/03_krun_candidate_smoke.log`](evidence/03_krun_candidate_smoke.log).

I added an independent concrete K program containing normal and adversarial
assertions. Its preserved source is
[`evidence/03_audit_boundary.py`](evidence/03_audit_boundary.py). After trusted
translation, this command exited 0:

```text
krun audit-boundary.mpy --definition audit-runtime-kompiled
```

The assertions establish that the supplied semantics returns the same
incorrect large-number results as the generated program, and that it returns
`631` for `"1e1"`. The same log records Python returning `10` for `"1e1"`:
[`evidence/04_semantics_divergence_witness.log`](evidence/04_semantics_divergence_witness.log).

### Proof definition and all positive claims

Exact build:

```text
kompile verification.k \
  --backend haskell \
  --main-module CLOSEST-INTEGER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0; see
[`evidence/03_proof_build.log`](evidence/03_proof_build.log).

There is exactly one target claim. I ran:

```text
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module CLOSEST-INTEGER-SPEC
```

It exited 0 and printed `#Top`; see
[`evidence/03_positive_claim.log`](evidence/03_positive_claim.log).

Thus clean verification succeeds under the submitted theory. That success is
not the verdict: the following stages show that the theory's postcondition and
used language model do not establish the requested property of the real
program.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

Precondition: there is no `requires` clause. `CS` is any `IntSeq`; `<k>` starts
with `runClosest(str(CS))`; and all other cells are fixed to the initial module
configuration (environment 0, empty module scope with the builtins parent,
fresh scope location 1, empty heap/stack, no pending return or exception, and
exit code 0).

Postcondition: execution finishes with the same non-`k` cells and the `<k>`
result

```text
nearestAway(decStrToF(CS))
```

where `nearestAway(F)` is definitionally

```text
if gtF(F, 0.0)
then truncF(addF(F, 0.5))
else truncF(subF(F, 0.5))
```

The result is therefore constrained; it is not a free variable, tautology, or
one-way implication. But it is exactly the program expression with a new name.
There is no theorem that this binary64 expression is the mathematically closest
integer, and the large-number witness shows such a theorem would be false.

### Body identity and entry normalization

The claim does not load the complete `Module(FuncDef(...))`. `runClosest`
directly calls a one-argument `closureVal` whose body is `closestBody()` and
whose defining environment is 0. This omits module definition/name lookup, but
the immutable constructor body and binding are pinned:

- trusted regeneration is byte-identical to submitted `solution.mpy`;
- [`evidence/04_body_identity.py`](evidence/04_body_identity.py) mechanically
  tokenizes the translated `FuncDef` body and `closestBody` RHS at constructor
  level, normalizing only the explicit/implicit empty `.Stmts`;
- both terms contain 92 constructor tokens and hash to
  `d071cc32ae53941789b46ba60e01b0158283a492781e511d80948d44fb76d418`;
  see [`evidence/04_body_identity.log`](evidence/04_body_identity.log).

The direct closure uses the same parameter `"value"`, exact body, and module
scope 0 that executing the real `FuncDef` would produce. For this immutable
single-definition module, the omitted definition step is a semantically inert
entry normalization, not a substituted body.

As an operational-sensitivity test, I changed the `Float(0.5)` in the *executed
positive branch of `closestBody`* to `Float(1.5)` while leaving the
postcondition unchanged. The modified definition built successfully, then
`kprove` exited 1 with `WarnStuckClaimState` and the residual

```text
truncF(addF(decStrToF(CS), 0.5))
  = truncF(addF(decStrToF(CS), 1.5))
```

See
[`evidence/04_verification_body_mutation.k`](evidence/04_verification_body_mutation.k),
[`evidence/04_body_mutation_build.log`](evidence/04_body_mutation_build.log),
and
[`evidence/04_body_mutation_proof.log`](evidence/04_body_mutation_proof.log).
The claim is genuinely body-sensitive.

### Satisfiable states and ground substitutions

The precondition is satisfiable, for example with
`CS = iCons(49, iCons(48, .IntSeq))`, the character codes for `"10"`, and the
exact initial cells printed in the claim. No guard must be solved.

Concrete substitutions give:

| Input | Claimed RHS under concrete K | Generated Python | Canonical Python | Contract |
|---|---:|---:|---:|---:|
| `"10"` | 10 | 10 | 10 | 10 |
| `"14.5"` | 15 | 15 | 15 | 15 |
| `"-14.5"` | -15 | -15 | -15 | -15 |
| `"9007199254740991"` | 9007199254740992 | 9007199254740992 | 9007199254740991 | 9007199254740991 |
| `"1e1"` | 631 | 10 | 10 | 10 |

The first four K observations are covered by the original and reviewer K smoke
programs. The last is isolated in
`evidence/04_semantics_divergence_witness.log`. These substitutions show both
failure modes: the theorem faithfully describes a flawed program result on the
large integer, and it describes a substituted `float(str)` behavior on the
exponent spelling.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/05_rule_inventory.py`](evidence/05_rule_inventory.py) reads every K
source file in the trusted/candidate-identical supplied tree, plus
`verification.k` and `spec.k`, and writes the full sentence-level inventory to
[`evidence/05_rule_inventory.tsv`](evidence/05_rule_inventory.tsv). The script
exited 0; see
[`evidence/05_rule_inventory.log`](evidence/05_rule_inventory.log).

The inventory covers 26 K files and 1,102 entries:

- 698 rules, one reachability claim, one configuration, and five contexts;
- 230 syntax declarations;
- every module/import/require boundary;
- 147 `[function]`, 109 `[total]`, 22 `[no-evaluators]`, 45 priority-bearing,
  26 `[owise]`, and all concrete declarations/rules found by the inventory;
- zero `[simplification]` and zero `[functional]` declarations.

Every TSV row has an audit class and assessment. Fixed supplied rules that
cannot occur on this program's execution path are retained as
`fixed-supplied-unreached`; they are not silently omitted. I found no concrete
false-conclusion witness for those rows and do not label them unsound. Reached
fixed rules are assessed against the selected semantics and real Python below.

### Candidate-local extensions

The candidate adds exactly three syntax/rule pairs:

| Extension | Class | Assessment |
|---|---|---|
| `closestBody() : Stmts [function,total]` | Definitional summary | Its sole equation is constructor-identical to regenerated `solution.mpy`. No overlap. |
| `runClosest(Str) : KItem` | Fresh entry wrapper | It creates the exact closure and invokes ordinary fixed call semantics. It does not preempt an existing program operation. |
| `nearestAway(Float) : Int [function,total]` | Definitional summary | Its equation truthfully defines the name as the `gtF`/`addF`/`subF`/`truncF` expression, but does not prove that expression has the advertised closest-integer meaning. |

There are no candidate-local priority rules, simplifications, claims used as
lemmas, or opaque symbols. The rules are left-linear, have one equation each,
and have no pairwise guard overlap.

`nearestAway` is not itself an inconsistent rewrite: it is a definition. The
unsound step is treating that definition as the requested mathematical
postcondition. A concrete false meaning-witness is
`F = 9007199254740991.0`: the RHS evaluates to
`9007199254740992`, while the closest integer is
`9007199254740991`.

### Used-construction map and control/state review

| Submitted constructor/operation | Declaration and material fixed rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; module sequencing in `core.k`; closure creation in `functions.k`. The entry wrapper skips only the already-pinned definition step. |
| `Call`, parameter `"value"` | `call.k` evaluates callee then arguments through `#evalArgs`, allocates a scope/frame, and `#bindP` binds the parameter. |
| `Name` lookup | `core.k` walks the local/module/builtins scope chain; `"float"` and `"int"` resolve to `typeV` entries in `builtinsScope`. |
| `Assign` | Strict RHS evaluation from `syntax.k`; `controls.k` writes `number` in the current call scope. |
| `Float` literal and `float(value)` | `float.k` evaluates the literal and maps `float(str(CS))` to result-bearing opaque `decStrToF(CS)`. |
| `Compare(..., ">")`, `If` | `operators.k` preserves operand evaluation; `float.k` maps `>` to opaque `gtF`; `controls.k` branches on the resulting Boolean. |
| `BinOp("+"/"-")` | `operators.k` dispatches; `float.k` maps to opaque `addF`/`subF`. |
| `int(float)` | `float.k` maps to opaque `truncF`. |
| `Return` | Strict result evaluation, `retV`, frame pop, caller environment restoration, scope removal, and continuation restoration in `functions.k`. |

The fixed semantics therefore preserves left-to-right call/argument evaluation,
local assignment, branch control, return control, stack state, and all visible
cells for this body. The claim's initial configuration matches the fixed
configuration (apart from the known source spelling of the exit-cell attribute,
which compiles to the same cell). The function scope is allocated at 1 and
removed on return; environment, stack, heap, return state, exception state, and
exit code are restored as claimed.

The used float symbols `decStrToF`, `gtF`, `addF`, `subF`, and `truncF` are
fixed supplied `[function,total,symbol,no-evaluators]` primitives in the
Haskell proof. Their concrete equations use K's binary64 hooks. This permits a
structural symbolic proof but leaves their value meanings at the trust
boundary.

Overlaps on the used path are benign at the K-theory level: duplicate
mixed-float and float-conversion equations in `float.k` have identical
right-hand sides; integer/float dispatch cases are sort-disjoint; and the
negative/general `decStrToF` equations are separated by the leading-minus
guard. No candidate rule changes priority or skips stateful execution.

### Concrete false-conclusion witness for a used semantic rule

The general concrete rule at `reference-semantics/semantics/float.k:162`
matches every nonempty `IntSeq` not beginning with `'-'`:

```text
decStrToF(CS)
  => intToF(intPart(CS))
     +Float intToF(fracPart(CS)) /Float intToF(fracScale(CS))
```

It does not require digit codes (apart from treating code 46 as a dot).
For `CS = codes("1e1") = [49,101,49]`, `intPart` applies
`C - 48` to the letter `e`, producing:

```text
intPart(codes("1e1")) = 631
decStrToF(codes("1e1")) = 631.0
```

The reviewer K assertion that the result is 631 passes. Python
`float("1e1")` is `10.0`, and both Python implementations return 10. This is
the required concrete false-conclusion witness over the intended domain. It
shows a material used-construct language-model gap, not merely missing
semantics for an unused construct.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created
[`evidence/06_spec_vacuity_audit.k`](evidence/06_spec_vacuity_audit.k), changing
the target result to:

```text
nearestAway(decStrToF(CS)) +Int 1
```

This is demonstrably false for the satisfying input `CS = codes("10")`, where
the program and original claimed expression produce 10, not 11.

The mutation first built/parsed successfully:

```text
kprove --dry-run spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module CLOSEST-INTEGER-SPEC-VACUITY-AUDIT
```

Exit 0; see
[`evidence/06_vacuity_build.log`](evidence/06_vacuity_build.log).

Then:

```text
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module CLOSEST-INTEGER-SPEC-VACUITY-AUDIT
```

exited 1 with `WarnStuckClaimState`. The residual explicitly contains the
unmet equality

```text
truncF(addF(decStrToF(CS), 0.5)) +Int 1
  = truncF(addF(decStrToF(CS), 0.5))
```

See [`evidence/06_vacuity_proof.log`](evidence/06_vacuity_proof.log). This is a
meaningful reached obligation, not a parse error, timeout, or unrelated crash.
The proof is non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting and decision

### What the successful K proof actually establishes

Under the supplied K theory, from the exact initial cells and for any symbolic
`CS:IntSeq`, the direct exact-body closure call reduces to:

```text
#if gtF(decStrToF(CS), 0.0)
#then truncF(addF(decStrToF(CS), 0.5))
#else truncF(subF(decStrToF(CS), 0.5))
#fi
```

with call-frame state restored. This is a universal, body-sensitive,
non-vacuous symbolic execution characterization. Because the Haskell backend
keeps the five float operations opaque, it principally proves that the program
builds the same opaque expression that `nearestAway` expands to.

It does **not** establish that this expression denotes the closest integer, nor
that `decStrToF` agrees with Python `float` over all numeric strings.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Trusted translator and constructor comparison | Connects `solution.py`, `solution.mpy`, and `closestBody`; all target execution depends on it. | Acceptable: trusted regeneration is byte-identical and mechanical body comparison passes. |
| Direct closure entry wrapper | Omits module definition/name lookup but fixes the exact body, parameter, and defining environment. | Acceptable for this immutable single-definition program; body mutation is detected. |
| Supplied call/control/state semantics | Determines evaluation order, bindings, frame/return effects, and cells. | Acceptable as the selected fixed semantics on the exercised body path; rebuilt independently. |
| `decStrToF` | Determines parsed value, branch, arithmetic, and final result. | Illegitimate for the full contract: concrete `"1e1"` witness gives 631 rather than Python 10. |
| `gtF` | Determines the branch. | Conditional fixed primitive; concrete `>Float` bridge is reasonable for finite binary64 values used in ordinary cases. |
| `addF` / `subF` | Determines the shifted float and final result. | Accurate for Python binary64 execution on the large-number witness, but exactly why the submitted algorithm violates the closest-integer contract. |
| `truncF` | Determines the returned integer. | Conditional fixed primitive for finite values; concrete equation models truncation toward zero. |
| “`nearestAway` means closest integer” | The requested human-facing postcondition depends entirely on this bridge. | False, not proved: `9007199254740991.0` is a counterexample. |
| Differential and concrete tests | Support finite program/semantics bridges only. | Reproducible finite evidence, never substituted for the K proof. |

### Gate accounting

- **Fresh verification:** PASS. The sole positive claim prints `#Top` and exits
  0.
- **Real-program/body pinning:** body identity and sensitivity PASS, but overall
  real-program semantic pinning FAILS on valid exponent-form numeric strings.
- **Result constraint/non-vacuity:** PASS.
- **Intent/domain adequacy:** FAIL. The unrestricted prompt includes the
  exhibited large integer and gives no spelling restriction. Restricting to
  small, plain decimal spellings would materially narrow the HumanEval
  source-contract domain and, under the benchmark's explicit mapping, would
  still be `FAIL / NOT_LEGIT`.
- **Trust/evidence auditability:** the audit evidence is reproducible, but the
  two result-bearing bridges needed for the advertised theorem are false.

The clean `#Top` is thus an honest proof of a limited internal expression
identity, not a partial-correctness proof of the requested closest-integer
contract for the real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
