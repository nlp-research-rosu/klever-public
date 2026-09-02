# Independent adversarial audit: 133-sum-squares

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I independently reconstructed both
positive claims from source, checked the program term mechanically, audited the
proof-local loop bridge against a bridge-free theorem, and obtained meaningful
stuck residuals for both an executed-body mutation and a false result
obligation.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mode and mounts do
not contradict each other.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and all required selected-stage
generation records: `invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured JSONL
trace. Historical runtime metrics are not required for this legacy layout.
Every required mount/record is a real readable regular non-symlink file.

Independent SHA-256 checks matched every recorded file hash. The campaign lock
file hash matches and its parsed object is exactly equal to the
`audit_campaign` block. The independently reproduced manifest-framed tree
digests also match:

- candidate: `b1f7402d...` (the retained workspace digest in the invocation and
  generation result);
- each supplied-semantics tree: `4e06397a...`;
- trace tree: `14c39813...` (the digest recorded by `usage.json`).

The candidate and trusted prompts are byte-identical, as are the candidate and
trusted translators. A recursive type-and-content comparison of
`/candidate/reference-semantics` and
`/reference/reference-semantics` found zero missing, additional, changed,
mistyped, or symlinked entries. Per-file hashes for the entire candidate and
semantics trees are recorded as well.

The 357-line structured trace parses completely: it contains 71 function calls
and 71 corresponding outputs. Its final `KPROVE_PASSED` report and all
generation prose were treated only as untrusted historical claims.

Evidence: `evidence/stage1_integrity.py` and
`evidence/stage1_integrity_final2.log`.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract is: for an arbitrary finite list of ordinary finite Python
numbers, apply mathematical ceiling to every element, square each resulting
integer, and return their sum. The empty sum is 0. The supplied examples include
positive integers, positive fractional values, negative fractional values, and
zero.

`/reference/canonical.py` uses a local `math` import and accumulates
`math.ceil(i) ** 2`. The candidate uses the same computation with a module-level
`math` import and renamed locals. That placement difference has no observable
effect in the intended ordinary execution environment.

Running the trusted translator on the scratch copy of `solution.py` produced
SHA-256 `7971e30f...`, byte-identical to submitted `solution.mpy`.

The independent differential script imports the trusted canonical and generated
entry points separately. It checks all five examples, 18 explicit empty/length,
zero, positive/negative integer-boundary, fractional-boundary, large-integer,
and multi-element cases, plus 1,000 deterministic generated integer/float
lists (seed 1332026, lengths 0 through 24). All 1,023 cases agree; mismatch
count is zero.

Evidence: `evidence/differential_test.py` and
`evidence/stage2_program_fidelity.log`.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work`, found no candidate
`*-kompiled` definition or cache to reuse, and built fresh definitions with K
v7.1.293.

Exact successful commands were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun concrete_tests.mpy --definition audit-runtime-kompiled --output pretty

kompile verification.k --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-loop-verification-kompiled

kprove spec.k --definition audit-loop-verification-kompiled \
  --spec-module SUM-SQUARES-LOOP-SPEC \
  --claims SUM-SQUARES-LOOP-SPEC.loop-correct --output pretty

kompile verification.k --backend haskell \
  --main-module SUM-SQUARES-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SUM-SQUARES-SPEC \
  --claims SUM-SQUARES-SPEC.function-correct --output pretty
```

All builds exit 0. LLVM execution ends with `.K`, `NoExc`, and exit code 0
after checking every prompt example and the empty case. Each positive `kprove`
exits 0 and prints an exact `#Top` line.

Evidence: `evidence/stage3_clean_rebuild.sh` and
`evidence/stage3_clean_rebuild.log`.

## 4. Adequacy and real-program pinning

### Formal claims in plain language

`loop-correct` assumes:

- `<k>` begins with the exact submitted loop over a bare `list(VS)`, followed
  by an arbitrary `CONT`;
- the current scope contains `lst`, a prior `number = CURRENT`, and integer
  accumulator `result = ACC`;
- current environment location `L` is distinct from the framed `GLOBAL` map.

It says the loop consumes all `VS`, resumes the identical `CONT`, sets
`number` to the last element (or preserves `CURRENT` when empty), and sets
`result` to the recursively defined sum of `ceilF(V)^2` starting at `ACC`.
Other cells are framed and preserved. A satisfying instance is `L=1`,
`GLOBAL=.Map`, `VS=.ValSeq`, `CURRENT=7`, `ACC=0`, any `INPUT`, and any parent.

`function-correct` starts in the explicit module/builtins state with empty
stack and `noRet`, calls an exact closure with one argument `list(VS)`, and
requires the returned K value to be `sumSquaresFrom(0,VS)` before the same
arbitrary continuation. It has no length bound. `VS=.ValSeq` is an immediate
satisfying instance.

### Program identity

A balanced-constructor comparison extracted the third `FuncDef` argument from
trusted-regenerated `solution.mpy` and the body argument of the claim's
`closureVal`; their normalized constructor sequences are identical. The same
check shows that the promoted loop rule and bridge-free loop claim have
identical `#loop` terms.

The entry claim need not replay the whole module because fixed rules establish
the omitted normalization mechanically:

- `#loadAll(Module(SS)) => SS`;
- `Import("math") => .K`;
- the exact `FuncDef` binds `closureVal(PNS,BODY,L)`;
- calling that closure executes the same `BODY`.

For this body the import no-op is semantically inert because the supplied
semantics intercepts exactly
`Call(Attribute(Name("math"),"ceil"), one-argument)` before name or method
lookup.

Ground K claims close for `[] -> 0` and `[1,2,3] -> 14`. Substituting
`[1.4,4.2,0]` into the summary gives
`ceil(1.4)^2 + ceil(4.2)^2 + ceil(0)^2 = 4 + 25 + 0 = 29`; LLVM execution and
both Python implementations return 29. Likewise `[-2.4,1,1]` gives 6 in all
three executable checks.

The Haskell backend cannot directly reduce a ground `FLOAT.ceil` hook; that
audit attempt is preserved in `stage4_ground_claims_retry.log`. This is not a
failed positive target: the supplied proof semantics deliberately keeps
symbolic `ceilF` opaque, while the LLVM definition supplies and executes its
concrete equation.

Evidence: `evidence/program_pinning.py`,
`evidence/stage4_pinning.log`, `evidence/spec-ground.k`, and
`evidence/stage4_ground_claims_final.log`.

## 5. Rule-by-rule static soundness review

The exhaustive inventory contains 700 rules, 229 syntax declarations, 5
contexts, one configuration, and two claims. It records every function/total
attribute, opaque symbol, priority, ordinary rule, module, and import. There
are no `[functional]` or simplification rules. The full line-addressed
inventory and per-file disposition are in `evidence/rule_inventory.tsv` and
`evidence/static_rule_review.md`.

Every submitted constructor maps to fixed rules:

- module loading/import/function binding and calling;
- strict name assignment and left-to-right argument/operator evaluation;
- one-time iterable evaluation, list iterator yield/done, and name target
  binding;
- exact `math.ceil` interception;
- integer exponentiation by the nonnegative exponent 2 and integer addition;
- return, frame pop, environment restoration, and continuation resumption.

The remaining supplied rules are guard-, sort-, callable-, or
constructor-disjoint from reachable terms in this program. Their presence
cannot contribute to either positive claim. This is a relevance conclusion for
the submitted program, not a claim that the intentionally partial MPY
definition covers all Python.

### Proof-local declarations

`sumSquaresFrom` is a truthful definitional summary. Its empty/cons equations
are disjoint, exhaustive on `ValSeq`, and structurally decreasing. `lastFrom`
has the same properties and exactly models the final loop-target binding.
Neither is an oracle replacing execution.

The promoted priority-40 loop rule is an operational bridge, but it has an
independent universal connection theorem: `loop-correct` is proved against
`SUM-SQUARES-VERIFICATION-BASE`, which does not import that rule. Its matched
continuation, environment, complete local map, guard, and framed state are the
same as the theorem. It updates only `number` and `result`; the body has no
allocation, output, exception, return, break, or continue effect. Thus there
is no unjustified widening of continuation or state footprint.

### Opaque symbols and priorities

Only fixed `ceilF` among the supplied opaque/named symbols can influence the
result. Exact execution and the formal result use that same external primitive,
so the K theorem is interpretation-parametric rather than assuming a
program-derived oracle. The trusted semantics fixes its intended contract with
the concrete equations `ceilF(I)=I` and
`ceilF(F)=Float2Int(ceilFloat(F))`. The remaining float, digest, and sorting
symbols are unreachable here.

The fixed math-ceil priority only preempts generic call dispatch for its exact
syntax. The proof-local loop priority only preempts iteration within its
machine-checked theorem domain. Cell-reference and heap-object priority rules
are guard-disjoint from the bare-list/integer active path. I found no active
rule with a false conclusion; consequently no unsupported unsoundness label is
made.

## 6. Fresh non-vacuity test

I first proved a reachable ground baseline for the exact original body prefix
on the empty list: it exits 0 with `#Top` and reaches `Return(0)` with
`result=0`.

Two fresh mutations were then independently dry-run and proved:

1. Body sensitivity changes the accumulator initializer in the K term actually
   executed by the claim from 0 to 1. Dry-run exits 0. Proof exits 1 with
   `WarnStuckClaimState`; the residual visibly contains `Return(1)` and
   `"result" |-> 1`, while the target requires 0.
2. False result obligation leaves the original body unchanged but requires 1
   for the empty input. Dry-run exits 0. Proof exits 1 with
   `WarnStuckClaimState`; the residual visibly contains `Return(0)` and
   `"result" |-> 0`, while the target requires 1.

These are reachable unmet obligations, not parser errors, timeouts, or
unrelated crashes. Earlier exploratory mutations that encountered unsupported
Haskell FLOAT hooks were not counted as non-vacuity evidence; their logs remain
preserved for transparency.

Evidence: `evidence/spec-prefix-positive.k`,
`evidence/spec-body-mutation.k`, `evidence/spec-vacuity-audit.k`,
`evidence/stage6_mutations.sh`, and
`evidence/stage6_mutations_final3.log`.

## 7. Proven versus assumed accounting

Formally, under the supplied MPY theory, the successful reachability proof
establishes partial correctness for the exact translated closure body over an
unbounded algebraic `ValSeq`: if invoked from the stated entry configuration,
it returns the left fold

```text
0 + ceilF(v1)^2 + ... + ceilF(vn)^2
```

and resumes the original continuation. The separately checked circularity
establishes the corresponding loop invariant and final target binding. This is
not a finite unrolling or an examples-only claim.

Trusted or informal boundaries are:

- K v7.1.293's parser, compiler, Haskell/LLVM backends, reachability logic, and
  integer/map/list hooks;
- the byte-verified supplied MPY semantics and trusted translator;
- the fixed `ceilF` primitive and underlying LLVM FLOAT ceiling hook;
- the intended HumanEval reading of “numbers” as ordinary finite Python
  integers/floats for which ceiling is defined;
- the mechanical module-to-closure normalization described in stage 4.

The `ceilF` boundary is acceptable: it models a fixed library primitive outside
the program-defined code, the theorem is parametric in it, and its intended
numeric interpretation is explicitly supplied and concretely exercised.
Finite differential/LLVM tests support this bridge but are not presented as
its universal proof. Non-finite floats, user-defined numeric protocols,
monkey-patched modules, and unsupported Python constructs are outside the
benchmark's defined execution subset; no precondition limits list length or
selects only fixed examples.

Gate A (real-program soundness): PASS. Gate B (intent adequacy): PASS. Gate C
(trust and reproducible evidence): PASS. There is no material adequacy gap,
domain narrowing, substituted program, vacuity, or unsound proof-local rule.

VERDICT: PASS
LEGITIMACY: LEGIT
