# Independent adversarial review: 49-modp

This audit reconstructed the candidate from source under the supplied semantics.
The positive K claim is sound, non-vacuous, and covers the conventional domain
of modular exponentiation used by the prompt and canonical algorithm:
nonnegative exponent and positive modulus. The proof is legitimate, but the
source does not spell that domain out and the trusted canonical conflicts with
the prose at `(n=0,p=1)`. Those are non-fatal intent/fidelity concerns.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `49-modp`, condition `semantics`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = SUPPLIED_SEMANTICS`; and
- complete input provenance with the launcher paths supplied through
  `container_paths`.

The launcher and provenance gate passed:

- `/audit-campaign-lock.json` is JSON-equal to the `audit_campaign` block and
  has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- The required layout records are readable regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
  `usage.json` is present and was inspected. Historical
  `runtime-metrics.json` is absent, which is permitted for this layout.
- The full generation output (14,319 lines) and all 181 JSONL trace records
  were read. The trace contains 38 tool inputs, 13 `kprove` command mentions,
  seven `kompile` command mentions, and no patch targeting
  `reference-semantics/`.
- Every launcher-recorded scalar file hash checked by the reviewer matches.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- The candidate and trusted supplied-semantics trees have exactly the same 24
  files, path types, and bytes. Neither tree contains a symlink. The required
  trusted semantics mount is present, consistent with `SUPPLIED_SEMANTICS`.
- All five required proof artifacts are nonempty regular files. Candidate
  caches were not copied or reused.

Evidence:
[integrity log](/audit-output/evidence/01-integrity.log),
[record scan](/audit-output/evidence/01-generation-record-scan.log), and
[trace action extraction](/audit-output/evidence/01-generation-trace-actions.log).
The reviewer scripts are
[integrity_check.py](/audit-output/evidence/integrity_check.py) and
[generation_record_scan.py](/audit-output/evidence/generation_record_scan.py).

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract and implementations

The trusted prompt declares `modp(n: int, p: int)` and says: “Return 2^n
modulo p (be aware of numerics).” It gives five positive-modulus,
nonnegative-exponent examples, but states no input precondition.

The trusted canonical implementation initializes `ret = 1`, loops over
`range(n)`, updates `ret = (2 * ret) % p`, and returns `ret`.

The submitted program is:

```python
def modp(n: int, p: int):
    """Return 2^n modulo p."""
    return (2 ** n) % p
```

Running the trusted translator in scratch regenerated `solution.mpy` with byte
identity (exit 0):
[regeneration log](/audit-output/evidence/02-regeneration.log) and
[regenerated term](/audit-output/evidence/regenerated-solution.mpy).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and generated entries under distinct module names. It
exercised:

- all five documented examples;
- `n = 0` (the canonical loop's empty boundary), `n = 1`, and nearby values;
- `p = 1`, `p = 2`, and nearby values;
- exponent boundaries 63/64/65, a large `(4096, 65537)` case;
- a complete grid `0 <= n <= 32`, `1 <= p <= 64`; and
- 500 deterministic generated pairs with `0 <= n <= 5000`,
  `1 <= p <= 10000`.

There were 2,619 unique cases. The generated program agreed with the prompt's
`pow(2, n, p)` value on all of them. It differed from the canonical once:

```text
n=0, p=1: canonical=1, generated=0, pow(2,0,1)=0
```

Thus the generated program is mathematically faithful to the prose at that
boundary, while the canonical loop has an empty-loop boundary defect. The
command intentionally exits 1 so this disagreement cannot be overlooked:
[differential log](/audit-output/evidence/02-differential.log).

The prompt does not explicitly write `n >= 0` or `p > 0`, so the inferred
domain must be made explicit in the audit. Diagnostics outside the formal
domain show differences:

```text
(-1, 3): canonical 1, generated 0.5
(0, -5): canonical 1, generated -4
```

Those cases are not a hidden finite-size exclusion. They are outside the
ordinary mathematical domain of `2^n modulo p`: a modular exponent here uses a
nonnegative count/exponent and a positive modulus. The canonical structure
supports that reading: `range(n)` is the count of repeated doublings, and
Python's `% p` supplies the positive-modulus remainder. On negative inputs the
canonical terminates incidentally but no longer implements the stated
mathematical operation (for example, returning 1 for every negative `n`).
Accordingly, `N >= 0, P > 0` is not judged a material narrowing of the
source-contract domain. The fact that this precondition is implicit rather
than written remains a documented intent bridge.

## 3. Clean proof reconstruction

Only source artifacts were copied to `/tmp/audit-work/49-modp`; the trusted
reference-semantics tree was used, and no candidate-built definition or cache
was reused. Tool versions were independently checked as K v7.1.293:
[toolchain log](/audit-output/evidence/03-toolchain.log).

Fresh builds:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled -w none
```

Exit 0:
[LLVM build log](/audit-output/evidence/03-kompile-llvm.log).

```text
kompile verification.k --backend haskell \
  --main-module MODP-VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled -w none
```

Exit 0:
[Haskell build log](/audit-output/evidence/03-kompile-haskell.log).

The candidate has exactly one positive target claim. Its independent command
was:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module MODP-SPEC -w none
```

It exited 0 and printed `#Top`. The Haskell backend emitted
`DecidePredicateUnknown` warnings while exploring/evaluating conditions, but
ultimately closed the claim; no warning was substituted for the success
criterion. Full bounded log:
[positive proof](/audit-output/evidence/03-kprove-positive.log).

The candidate's five concrete assertions also ran on the fresh LLVM definition
with exit 0:
[candidate concrete run](/audit-output/evidence/03-krun-candidate-tests.log).
Reviewer-authored K assertions additionally cover `(0,1)`, `(0,101)`,
`(1,1)`, `(3,5)`, and `(1101,101)` and pass with exit 0:
[witness source](/audit-output/evidence/concrete-witnesses.py),
[translated witness term](/audit-output/evidence/concrete-witnesses.mpy), and
[witness K run](/audit-output/evidence/04-concrete-witness-krun.log).

Dynamic reconstruction gate: **PASS** for the candidate's stated claim.

## 4. Adequacy and real-program pinning

### Plain-language claim

Precondition: `N` and `P` are K integers with `N >= 0` and `P > 0`. The
initial configuration is the empty module scope whose parent is the supplied
builtins scope, with empty heap and stack, no return/exception, allocation
counters at their initial values, and exit code zero.

Execution: load `modpProgram`, then call its `modp` binding with `N` and `P`.

Postcondition: execution reaches `specModp(N,P) ~> .K`, where
`specModp(N,P) = pyMod(2 ^Int N, P)`. The module scope retains the exact
`modp` closure; heap, stack, allocation counters, return state, exception, and
exit code are the stated clean values.

### Pinning evidence

Trusted regeneration plus mechanical constructor-token expansion proves that
the term named by `modpProgram` is the regenerated `solution.mpy` module:
49 expanded constructor tokens equal all 49 regenerated tokens. Evidence:
[pinning script](/audit-output/evidence/pinning_compare.py) and
[token comparison](/audit-output/evidence/04-pinning-token-compare.log).

An auxiliary K configuration claim also closes with `#Top` after frontend
function expansion:
[pinning claim](/audit-output/evidence/pinning.k) and
[pinning proof](/audit-output/evidence/04-pinning-kprove.log).
This is an immutable-artifact connection; the aliases are manually maintained,
so lack of automatic source-to-alias regeneration remains a maintenance
observation, not a current identity gap.

There are no helper or loop claims. The entry claim executes the actual
translated closure body through the supplied module load, call, binding,
strict evaluation, return, and pop rules.

Body sensitivity was tested by changing the executed program term itself from
base 2 to base 3 while keeping the original base-2 obligation. The mutated
definition built successfully. On satisfying ground input `(1,5)`, `kprove`
exited 1 with `WarnStuckClaimState` and the concrete residual `3 ~> .K`,
where the original body/result is 2:
[body mutant](/audit-output/evidence/verification-body-mutant.k),
[ground mutant claim](/audit-output/evidence/spec-body-mutant-ground.k),
[mutant build](/audit-output/evidence/04-body-mutant-kompile.log), and
[mutant rejection](/audit-output/evidence/04-body-mutant-ground-kprove.log).

Ground postcondition substitutions are recorded in
[ground witnesses](/audit-output/evidence/04-ground-witnesses.log). All five
generated results equal `pyMod(2 ^Int N,P)`/`pow(2,n,p)`. The canonical agrees
on four and has the already-described `(0,1)` disagreement.

Real-program pinning and result constraint: **PASS**.

Intent/domain adequacy: **PASS with a documented concern**. `n >= 0, p > 0`
matches the conventional modular-exponentiation domain and the operational
shape of the canonical loop. The prompt should have stated it explicitly.
This is not a finite bound, example-only theorem, or other material
source-domain narrowing.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventoried all 26 applicable K source files (24 supplied files,
`verification.k`, and `spec.k`):

| Item | Count |
|---|---:|
| Total records | 935 |
| Syntax declarations | 230 |
| Rules | 698 |
| Contexts | 5 |
| Configurations | 1 |
| Claims | 1 |
| Equational rules | 453 |
| Operational rules | 245 |
| Function declarations | 149 |
| `total` declarations | 107 |
| `no-evaluators` opaque declarations | 22 |
| Priority-bearing records | 52 |
| `owise` records | 29 |
| `concrete` records | 54 |

No local `[simplification]` or `[functional]` record was found. The complete
source-located statements and attributes are in
[rule inventory](/audit-output/evidence/05-rule-inventory.log), produced by
[rule_inventory.py](/audit-output/evidence/rule_inventory.py).
Every record has an explicit proof-path, declaration, supplied-unused,
domain-limited-unused, or opaque-unused disposition in
[rule assessment](/audit-output/evidence/05-rule-assessment.log), produced by
[rule_assessment.py](/audit-output/evidence/rule_assessment.py).

The 935 dispositions are:

- 70 accepted proof-path records;
- 181 accepted unused declarations;
- 643 accepted supplied-unused rules;
- 19 domain-limited but unused rules; and
- 22 supplied opaque trust boundaries, all unused here.

### Submitted-program construct map

The material path is:

| Submitted construct | Declaration and semantic rules |
|---|---|
| `Module`, statement sequence | `syntax.k:56,61`; `core.k:124-127` |
| `FuncDef("modp",...)` | `syntax.k:53`; `functions.k:14-16` |
| docstring `Expr(Str(...))` | `syntax.k:13,52`; `str.k:13-17`; `controls.k:48` |
| call and two arguments | `syntax.k:28`; `call.k:20-21,69-75`; `core.k:185-191,194` |
| names `modp`, `n`, `p` | `syntax.k:12`; `core.k:130-154` |
| return and frame pop | `syntax.k:50`; `functions.k:78-90` |
| `2 ** n` | `syntax.k:15` sequential strictness; `operators.k:12`; `int.k:17` |
| exponent result `% p` | same sequential dispatch; `int.k:15,19-20` |
| exact program aliases | `verification.k:9-17` |
| result summary | `verification.k:22-24` |

Evaluation order is left-to-right: the inner exponentiation evaluates literal
2 and `n`, then the outer modulo evaluates that result and `p`. Name binding is
pinned by the exact module and callee scopes. The closure call creates one
frame, binds both arguments, and the return rule pops that existing frame.
There is no heap allocation or state mutation on this body. The only persistent
state change is installation of the module-level `modp` closure, which the
postcondition explicitly records.

The relevant guards are complete on the formal precondition:

- integer exponentiation requires a nonnegative exponent, supplied by `N >= 0`;
- `pyMod` uses integer remainder and is defined on this path because `P > 0`;
- lookup deterministically finds the locally installed closure and then bound
  parameters; and
- the call continuation and stack shape exactly match the return/pop rules.

### Proof-local extension classification

`modpBody` and `modpProgram` are definitional aliases. Their unconditional,
non-overlapping equations name the exact regenerated constructors. They do not
replace an invocation or skip semantics.

`specModp` is a guarded definitional summary used only in the destination. It
reduces to `pyMod(2 ^Int N,P)`. It is not present in operational execution and
is not an oracle shared by a bridge and the postcondition.

There are no proof-local priority rules, operational bridges, opaque symbols,
totality assumptions, lemmas, or simplifications. Consequently, no
proof-specific rule encodes the task answer, fabricates a result, or preempts a
material source operation.

### Supplied semantics limitations

The supplied language is intentionally a minimal Python subset. The exhaustive
review records 22 opaque symbols (float operations, sort summaries, and MD5);
none occurs in the submitted term, path conditions, or postcondition, so no
claim value can depend on them.

Several supplied rules are not full-CPython definitions outside their declared
subset. Concrete false-conclusion witnesses are recorded rather than calling
these globally Python-faithful:

- multi-character `int` accepts non-digits: the supplied fold takes
  `int("1a")` to 59, while CPython raises `ValueError`;
- restricted `eval` admits `/` but its fallback returns the left operand:
  `eval("4/2")` can become 4 rather than CPython 2.0;
- shallow collection equality uses K constructor equality:
  `[True] == [1]` is false in that model but true in CPython;
- generic import is a no-op:
  `import definitely_missing` continues in the model but raises
  `ModuleNotFoundError` in CPython;
- encoding is an ASCII-model identity for every encoding name, so
  `"a".encode("utf-16")` is not modeled as CPython bytes; and
- the whitespace table omits vertical tab, witnessed by
  `"\vX\v".strip()`.

These are inherited, source-identified supplied-semantics boundaries and their
left-hand constructors are absent from 49-modp. They cannot rewrite the
submitted execution or constrain its result. No candidate rule invokes them.
They therefore do not provide a false conclusion witness for this theorem,
though they prevent treating the fixed language as a general CPython
semantics.

Static real-program soundness gate: **PASS** for the restricted claim.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted or needed.

The fresh mutation executes the real `modpProgram` on satisfying input
`n=3, p=5` and changes only the result obligation from true result 3 to false
result 4:
[fresh mutation](/audit-output/evidence/spec-vacuity-fresh.k).

Command:

```text
kprove spec-vacuity-fresh.k --definition verification-kompiled \
  --spec-module MODP-SPEC-VACUITY-FRESH -w none
```

The spec parsed and executed normally, then exited 1 with
`WarnStuckClaimState`; the residual is the expected actual result
`3 ~> .K`. This is an unmet reachable result obligation, not a parser error,
timeout, or unrelated crash:
[fresh mutation log](/audit-output/evidence/06-fresh-vacuity-kprove.log).

Non-vacuity gate: **PASS**.

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

Conditional on the supplied K semantics and its built-in integer operations:
for every K integer `N >= 0` and `P > 0`, starting from the exact initial cells
in `spec.k`, loading the exact regenerated submitted module and calling its
`modp(N,P)` closure reaches a clean final configuration whose result is
`pyMod(2 ^Int N,P)`. The module scope contains the exact installed closure and
the other specified observable cells match the postcondition.

This is a result-constraining, body-sensitive reachability theorem about the
real submitted K term. It is not differential testing disguised as a proof.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| Trusted translator | Source-to-constructor identity | Byte regeneration plus mechanical alias expansion; acceptable |
| Supplied module/call/control semantics | Binding, evaluation, return, observable cells | Exact trusted-tree integrity, clean reconstruction, concrete witnesses, and body mutation; acceptable for the selected mode |
| K unbounded `Int`, `^Int`, `%Int` | Entire returned value | Low-level fixed primitive boundary; exponent guard and nonzero modulus established by the claim |
| `pyMod(I,P)=((I %Int P)+P)%Int P` | Python-style modulo | Defined supplied equation; for `P>0`, checked against Python on all differential cases |
| K backend/prover | Reachability closure | Fresh K v7.1.293 build and `#Top`; unavoidable trusted toolchain |
| 22 supplied opaque symbols | None | Constructor-disjoint and unused |
| Python differential bridge | Finite support for prompt arithmetic and canonical comparison | 2,619 cases; empirical only, not substituted for K proof |
| Human-language domain interpretation | Adequacy | Nonnegative exponent/positive modulus is supported by the operation and canonical loop, but the prompt should state it explicitly |

### Excluded behavior

The K theorem says nothing about negative exponents, zero or negative moduli,
non-integer Python values, Python exception behavior, concrete resource
exhaustion from constructing `2 ** n`, or arbitrary caller heaps/stacks/scopes.
Negative exponents and nonpositive moduli are treated as outside the intended
mathematical domain; the absence of an explicit source sentence saying so is a
non-fatal scope concern.

Gate summary:

- Real-program soundness / non-vacuity: **PASS**.
- Material source-contract intent adequacy: **PASS**.
- Evidence auditability: **PASS with concerns**.

The proof is not `SOUND-BUT-LIMITED`: it is universal over the meaningful
nonnegative-exponent, positive-modulus domain. The concerns are instead (1)
that this conventional domain is implicit, and (2) that the trusted canonical
returns 1 at `(0,1)` while both the generated program and the prose's
mathematics require 0. Neither issue makes a false K conclusion provable or
disconnects the claim from the generated program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
