# Independent adversarial audit: 32-find-zero

## Outcome

The candidate contains a legitimate, freshly reconstructible partial-correctness
proof of the submitted MPY program's execution result over an unbounded symbolic
domain of finite `Int`/`Float` coefficient lists satisfying the prompt's
structural conditions. The proof is result-constraining, executes program-defined
code under the supplied semantics, and is sensitive both to a program-body
change and to a false final result.

The qualification is material enough to prevent `PASS`, but not to make the
proof illegitimate: K proves that the program returns the recursively defined
`solveFrom`/`bisectFrom` execution summary. It does not prove a postcondition
such as `poly(xs, result) = 0`, a residual bound, or the real-analysis facts
which make that summary a root approximation. That bridge is standard and is
supported by independent differential evidence, but remains informal and
conditional on the supplied opaque arithmetic primitives. This is the
benchmark's stated `CONCERNS / LEGIT` case for an informal intent bridge which
does not enable a false conclusion.

All candidate-built definitions and prior logs were ignored during
reconstruction. Reviewer evidence is indexed by
`/audit-output/evidence/EVIDENCE.sha256`.

## 1. Input and provenance integrity

### Declared layout and required records

`/audit-input.json` declares:

- problem `32-find-zero`;
- condition `kit-semantics`;
- `record_layout` `pipeline-v3`;
- `semantics_mode` `SUPPLIED_SEMANTICS`; and
- the mounted paths used in this audit.

The required trusted supplied-semantics tree exists at
`/reference/reference-semantics`, so the mount agrees with the rendered
semantics mode. Every required pipeline-v3 record was present, readable, a
regular file, and not a symlink:

- `/run.json`;
- `/task.json`;
- `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/runtime-metrics.json`;
- `/generation-evidence/usage.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`; and
- the JSONL trace beneath `/generation-evidence/codex-trace/`.

The structured trace contained 983 parseable JSON records, one session ID, 213
recorded tool calls, and no malformed record. The full tool-call summary is in
`/audit-output/evidence/stage1/trace-summary.log`; the generation narrative and
its prior `VALIDATED`/`#Top` claims were treated only as untrusted historical
claims.

### Campaign, hashes, and trusted mounts

The JSON value of `/audit-campaign-lock.json` exactly equals the
`audit_campaign` block in `/audit-input.json`, and its actual SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The mounted run, task, result, invocation, metrics, runtime metrics, usage,
prompt, output, last-message, and trace-file hashes all equal their launcher
records. The task fields agree with the corresponding launcher manifest
fields; `/audit-input.json` additionally decorates that block with the run
configuration.

The candidate prompt and translator are byte-identical to their trusted mounts:

- prompt SHA-256:
  `17c137edab480f3be30b47bb48eea2748f23b120a73b2bb80c7901112e1b223f`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

`diff -r --no-dereference /reference/reference-semantics
/candidate/reference-semantics` exited 0. A separate type/path manifest and
per-file SHA-256 inventory found no missing, additional, mistyped, changed, or
symlinked entry and found zero symlinks in either tree. Thus the candidate did
not alter the fixed semantics. This integrity result does not bless rules in
`/candidate/verification.k`.

The complete commands, actual/expected hashes, recursive manifests, and exit
statuses are in `/audit-output/evidence/stage1/integrity.log`. Two earlier logs
in the same directory preserve reviewer-harness mistakes: the first assumed
`jq` was installed, and the second over-required exact equality between the
launcher-decorated manifest and `/task.json`. Neither was an input or candidate
failure; the corrected script exited 0 with `integrity_failures=0`.

**Stage 1 result: PASS. No infrastructure breach.**

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py:12` defines `find_zero(xs)`. Its material contract is:

1. `xs` is a finite list of polynomial coefficients;
2. it has an even number of coefficients;
3. its highest coefficient is nonzero, which also makes the list nonempty and
   therefore at least length two; and
4. the result is one zero point, illustrated after rounding by `-0.5` for
   `[1, 2]` and `1.0` for `[-6, 11, -6, 1]`.

`/reference/canonical.py:28` starts at `[-1.0,1.0]`, doubles the symmetric
endpoints until their polynomial values have non-positive product, bisects to
width at most `1e-10`, and returns the lower endpoint. It therefore implements
a floating approximation, rather than generally returning an exactly
representable algebraic zero.

`/candidate/solution.py:1` evaluates the same polynomial by an iterative
power fold rather than `math.pow`. `/candidate/solution.py:11` uses the same
bracketing and bisection algorithm. Its `len(xs)/-len(xs)` and
`len(xs)/len(xs)` expressions equal `-1.0` and `1.0` on every contract-valid
input.

### Trusted regeneration

In fresh scratch, the exact command

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

exited 0, and `cmp -s regenerated-solution.mpy solution.mpy` exited 0. Both
files have SHA-256
`e4d2220c63e04122186eba4a4a7b010bc6cffaeb093f863dddabae6cdcb62710`.
See `/audit-output/evidence/stage2/translator-identity.log` and the preserved
`/audit-output/evidence/stage2/regenerated-solution.mpy`.

### Independent differential test

`/audit-output/evidence/stage2/differential_test.py` independently imports the
trusted canonical module and the candidate module. It exercised:

- both prompt examples;
- minimal length two;
- roots at zero and at each initial endpoint;
- an input requiring endpoint expansion;
- inputs exercising both bisection updates;
- mixed integer/float inputs;
- a small but nonzero highest coefficient;
- lengths 2, 4, 6, 8, 10, and 12; and
- 200 deterministic generated valid inputs.

The command and result are in
`/audit-output/evidence/stage2/differential.log`. It exited 0 with:

```text
intended_domain_cases=210
mismatches=0
expand_true=164
expand_false_exit=210
bisect_begin_branch=3857
bisect_end_branch=3657
```

The explicitly tested empty-list boundary is outside the source precondition:
there is no nonzero highest coefficient. The canonical implementation returns
`-1.0` for it, while the candidate raises `ZeroDivisionError`. This is a real
implementation divergence but not a narrowing of the intended contract
domain. Inputs with a zero highest coefficient or odd length likewise fall
outside the guarantee and may not terminate, so they were not misreported as
positive differential cases.

Finite differential testing supports source/intent alignment; it is not used
as a universal proof.

**Stage 2 result: PASS on the intended domain, with the excluded empty-input
behavior recorded.**

## 3. Clean proof reconstruction

Only source files and the trusted supplied semantics were copied to
`/tmp/audit-work/32-find-zero`. No candidate `runtime-kompiled`,
`verification-kompiled`, `verification-base-kompiled`, cache, Python bytecode,
or prior proof output was copied or reused.

The available tools were K `v7.1.293` and Python `3.10.12`; see
`/audit-output/evidence/tool-versions.log`.

### Fresh Haskell definition

The exact command

```text
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION-BASE \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-base-kompiled
```

exited 0. The warnings were unused-variable warnings in the unchanged supplied
semantics. See `/audit-output/evidence/stage3/kompile-haskell.log`.

### Every declared positive proof target

The five invocations declared positive by `/candidate/prove.sh:42` were rerun
against that fresh definition. Every invocation exited 0 and printed a literal
line `#Top`:

| Invocation | Selected claims | Exit | Result |
|---|---|---:|---|
| 1 | `SPEC.find-load`, `SPEC.find-init` | 0 | `#Top` |
| 2 | three `poly-loop-*` claims | 0 | `#Top` |
| 3 | three `poly-loop-*` plus `expand-loop` | 0 | `#Top` |
| 4 | `bisect-head` | 0 | `#Top` |
| 5 | three `poly-loop-*` plus `bisect-loop` | 0 | `#Top` |

The exact runner is
`/audit-output/evidence/stage3/run_positive_proofs.sh`; the summary and
individual bounded logs are in `/audit-output/evidence/stage3/`.

### Fresh LLVM definition and concrete execution

The supplied semantics was also freshly compiled with:

```text
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0; see `/audit-output/evidence/stage3/kompile-llvm.log`.
The independent source
`/audit-output/evidence/stage3/runtime_probe.py` was translated with the trusted
translator and executed under this definition. It checks both prompt examples
and an expansion-required cubic. `krun` reached `.K`, `NoExc`, exit code 0 and
itself exited 0. The source, MPY term, exact command, and full bounded final
configuration are preserved in `/audit-output/evidence/stage3/`.

**Stage 3 result: PASS. The prior candidate definitions and prior `#Top`
reports were unnecessary.**

## 4. Adequacy and real-program pinning

### Plain-language meaning of the eight claims

The claims in `/candidate/spec.k` have the following exact roles:

- `poly-loop-empty`: an exhausted list loop terminates without changing the
  accumulator or power, and leaves the last coefficient unchanged.
- `poly-loop-int`: one integer-headed iteration updates value and power with
  the source operations, records that head as the current coefficient, then
  summarizes the remaining sequence.
- `poly-loop-float`: the analogous float-headed iteration.
- `expand-loop`: from the actual first while-loop head and exact following
  bisection/return continuation, execute the bracketing loop and leave
  `begin`/`end` equal to `bracketBegin`/`bracketEnd`; every other observed cell
  is preserved.
- `bisect-head`: expose the supplied semantics' `#while` staging for the second
  while statement without adding a summary.
- `bisect-loop`: execute the actual bisection loop and return suffix, producing
  `bisectFrom(NS,B,E)`, popping the function frame, restoring environment 0,
  and preserving heap, heap counter, exception state, and exit code.
- `find-load`: execute the exact module load, function binding, `find_zero`
  lookup, and argument evaluation to the actual closure application.
- `find-init`: execute closure application, parameter binding, and the three
  initial assignments to the first expansion-loop head.

All `poly-loop-*` preconditions are satisfiable, for example with `L=1` and a
base map whose only key is 0. `validCoeffs` claims are satisfiable with
`NS = nInt(1,nInt(2,.NumSeq))`; `bisect-head` has no `requires` condition.
Ground witnesses for every claim family are recorded in
`/audit-output/evidence/stage4-5/precondition-witnesses.log`.

### Mechanical program identity

`/candidate/verification-program.mpy` is the proof constructor
`solutionModule`. Fresh Haskell execution of both the submitted
`solution.mpy` and this constructor under the proof definition produced
byte-identical closure configurations:

```text
krun solution.mpy --definition verification-base-kompiled
krun verification-program.mpy --definition verification-base-kompiled
diff -u krun-solution.out krun-verification-program.out
```

All three commands exited 0. The two outputs have the same SHA-256,
`b7ebd4a78d14bf99e9603226c0f8e61e361c3e76a88c93af42226e32aedd77dc`.
See `/audit-output/evidence/stage4-5/program-term-identity.log`.
This constructor-level test confirms the parameters, bindings, and bodies
used in the claims, rather than merely comparing an external source filename.

The modular boundaries also compose exactly:

```text
find-load RHS = find-init LHS
find-init RHS = expand-loop LHS
expand-loop RHS = bisect-head LHS
bisect-head RHS = bisect-loop LHS
```

There is no single packaged end-to-end claim, but no weakened implication or
free value is introduced at these boundaries. Their exact syntactic equality
is sufficient for reachability transitivity; the lack of one wrapper claim is
an artifact-maintenance observation, not a proof failure.

### Proof-local body sensitivity

The audit changed the `polyStep` term actually executed by the claims from

```text
power = power * x
```

to

```text
power = power + x
```

while leaving `polyAcc`/`polyPower` obligations unchanged. The mutated
definition compiled successfully. Its `poly-loop-*` proof exited 1 with
`WarnStuckClaimState`; the residual contained
`"power" |-> addF(P,X)` rather than the required multiplicative summary.
This is the body-sensitivity test required by Gate A1. See
`/audit-output/evidence/stage4-5/verification-body-mutation.k`,
`body-mutation-kompile.log`, and `body-mutation-proof.log`.

### Concrete substitution into the claimed result

For three satisfying inputs, the audit independently evaluated the recursively
defined claimed result after substituting the concrete initial endpoints
`B0=-1.0`, `E0=1.0`:

| Coefficients | `claimed_solveFrom` | Candidate Python | Canonical Python |
|---|---:|---:|---:|
| `[1,2]` | `-0.5000000000582077` | same | same |
| `[-6,11,-6,1]` | `0.9999999999417923` | same | same |
| `[10,0,0,1]` | `-2.1544346900773235` | same | same |

The script and complete output are
`/audit-output/evidence/stage4-5/precondition_witnesses.py` and
`precondition-witnesses.log`.

A direct standalone Haskell evaluation of the ground `solveFrom` term could
not run because the Haskell backend intentionally lacks `FLOAT.int2float`;
the expected missing-hook diagnostic is preserved in
`claimed-result-linear-haskell-unsupported.log`. A separately compiled LLVM
definition containing the proof summaries aborted when asked to run the
standalone `--term` summary; that diagnostic is in
`claimed-result-linear-llvm.log`. These exploratory backend limitations are
not treated as candidate failures: the required Haskell proofs succeeded, the
actual MPY program executed under LLVM, and the substituted recursive result
was independently checked against both Python implementations.

**Stage 4 result: PASS for program pinning and result constraint. The
summary-to-root meaning remains the Stage 7 concern.**

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/stage4-5/k_inventory.py` generated the line-addressed
inventory `/audit-output/evidence/stage4-5/rule-inventory.tsv`. It contains
1,166 records across the exact supplied semantics, `verification.k`, and
`spec.k`, including:

- 737 rules;
- 237 syntax declarations;
- 8 claims;
- 1 configuration;
- 5 contexts;
- every module, import, and require declaration; and
- every occurrence of `function`, `total`, `simplification`, `concrete`,
  `owise`, `priority`, `macro`, `symbol`, `no-evaluators`, and `hook`.

The 737-rule count includes 695 fixed supplied-semantics rules and all 42
candidate-local rules. There are no generated helper K files beyond the fixed
supplied tree and `verification.k`; compiled KORE and candidate caches were
not sources and were not inventoried as proof rules.

The unchanged supplied tree is the selected fixed semantics. Every fixed rule
is listed in the inventory and classified there by file, line, declaration
kind, and attributes. Unused fixed-language features cannot contribute to
these claims. The used fixed-semantics paths were additionally reviewed as
follows:

| Used construct | Declaration and execution rules | Review |
|---|---|---|
| module and statement sequencing | `syntax.k:53-61`, `core.k:49-60,124-127`, `functions.k:14-16` | Exact load order and closure binding; observed in `find-load` |
| names/scopes | `core.k:129-181` | Lexical lookup reaches module then builtins; claims pin both maps |
| calls/arguments | `syntax.k:28`, `core.k:183-191`, `call.k:18-32,69-75` | Callee first, arguments left-to-right, exact closure body and frame |
| assignment | `syntax.k:41`, `controls.k:8-18` | RHS strict; current frame updated; no cell-variable branch is reachable in these plain frames |
| list iteration/for | `controls.k:62-74`, `list.k:8-10` | Iterable evaluated once; head binding and tail continuation match each `poly-loop-*` claim |
| while/if | `controls.k:50-54,76-82` | Source guards and their Boolean negations are exhaustive and disjoint |
| return/pop | `functions.k:77-90` | Return value, frame pop, environment restoration, and scope deletion match `bisect-loop` |
| operators/order | `syntax.k:14-15,41,45,49-50`, `operators.k:10-17` | Strict/seqstrict evaluation and dispatch preserve source order |
| `len` | `builtins.k:17-26`, `core.k:221-229` | `len(list(numVals(NS)))` is the structural `vsLen`; valid inputs avoid zero division |
| integers/floats | `int.k:7-27`, `float.k:19-56,97-151,189-206` | Sort-disjoint dispatch; proof-side float results are intentionally opaque terms with concrete LLVM twins |

Relevant duplicate mixed `Int`/`Float` dispatch rules in `float.k:132-151` and
`float.k:197-206` have identical right-hand sides, so their overlap cannot
derive conflicting results. No candidate priority rule preempts this fixed
execution.

### Every local declaration and rule

`/candidate/verification.k:9-44` declares:

1. the disjoint finite sequence constructors `.NumSeq`, `nInt`, and `nFloat`;
2. structural input functions `numVals`, `numLen`, `lastNonZero`, and
   `validCoeffs`;
3. eight nullary AST abbreviations covering the exact translated function
   bodies and loop components; and
4. the result-bearing functions `polyAcc`, `polyValue`, `polyPower`,
   `polyLast`, `bracketBegin`, `bracketEnd`, `bisectFrom`, and `solveFrom`.

All are functions; the result summaries are `total`, symbolic,
`no-evaluators` functions. There is no local `functional` declaration, opaque
constant without equations, priority rule, `owise` rule, ordinary operational
`<k>` rewrite, or candidate macro.

Every one of the 42 rules is covered below:

| Local rule lines | Rules covered | Judgment |
|---|---|---|
| 51, 52, 53 | three `numVals` equations | Sound structural embedding of empty, integer-head, and float-head sequences |
| 57, 60, 63, 67 | four equality simplifications | Sound no-confusion/injectivity consequences of disjoint `NumSeq`, `ValSeq`, `Int`, and `Float` constructors |
| 72, 73, 74 | three `numLen` equations | Sound structural length with strict descent |
| 76, 77, 78, 79, 81 | five `lastNonZero` equations | Sound last-element test; recursive and singleton guards are disjoint because recursion requires a nonempty tail |
| 84 | `validCoeffs` | Exactly length at least two, even length, and nonzero final coefficient |
| 89, 96, 103, 110, 114, 119, 132, 148 | eight AST abbreviation equations | Byte/constructor identity established mechanically against regenerated `solution.mpy` |
| 155, 156, 161 | three `polyAcc` equations | Exact source accumulator and power updates, structurally descending on `NumSeq` |
| 166 | `polyValue` | Definitional initial accumulator `0.0` and power `1.0` |
| 168, 169, 172 | three `polyPower` equations | Exact final power fold, structurally descending |
| 175, 176, 179 | three `polyLast` equations | Exact initial/current/final `coeff` state, structurally descending |
| 185, 189 | two `bracketBegin` equations | Exact source expansion update or exit, split on `G` versus `notBool G` |
| 192, 196 | two `bracketEnd` equations | Same exact split and transition for the right endpoint |
| 202, 210, 218 | three `bisectFrom` equations | Exact while exit, begin-update, and end-update; while and if guards partition the cases |
| 223 | `solveFrom` | Pure composition of the already connected expansion and bisection summaries |

The structural functions terminate by a smaller `NumSeq`. The loop summaries
need not normalize when the corresponding program loop does not terminate;
their recursive equations take exactly the program transition, and the theorem
is partial correctness. The complementary Boolean guards prevent conflicting
terminal equations. Declaring these symbols total does not assert a root
property and does not fabricate a terminal value for an executing program
path.

### Extension classification and state footprint

- The input functions and AST names are definitional summaries.
- `polyAcc`, `polyPower`, and `polyLast` are program-derived result summaries
  connected universally by the three constructor-split `poly-loop-*` claims.
- `bracketBegin` and `bracketEnd` are program-derived endpoint summaries
  connected by `expand-loop` over the exact closure, active continuation,
  function frame, scopes, heap, return, exception, and exit-code cells.
- `bisectFrom` is a program-derived returned-value summary connected by
  `bisect-loop` over the exact return suffix and frame pop.
- `solveFrom` only composes connected summaries.

None is an operational bridge: no candidate rule rewrites `Call`, `#applyK`,
`For`, `#loop`, `While`, `#while`, `Return`, or a `poly` invocation in `<k>`.
Program-defined operations execute under the fixed semantics. The same
summary symbols occur in claim postconditions, but their value is not a
circular oracle because independent, bridge-free fixed-execution claims
connect each source loop to its equations.

No local rule was found unsound, so this review makes no unsound-rule claim
requiring a false-conclusion witness. The narrower evidence limitation is the
absence of a formal root/residual theorem, addressed in Stage 7.

**Stage 5 result: PASS for rule soundness.**

## 6. Fresh non-vacuity test

The audit did not rely on `/candidate/spec-mutation.k`. It created the fresh
`/audit-output/evidence/stage6/spec-vacuity.k`, changing the final bisection
obligation from

```text
bisectFrom(NS,B,E)
```

to

```text
addF(bisectFrom(NS,B,E),1.0)
```

This is false for the satisfying witness `NS=nInt(1,nInt(2,.NumSeq))`,
`B=-1.0`, `E=1.0`: ordinary concrete arithmetic gives approximately `-0.5`
versus `0.5`.

The dry-run command compiled the mutation successfully and exited 0:

```text
kprove spec-vacuity.k \
  --definition verification-base-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --claims SPEC-AUDIT-VACUITY.wrong-bisect-result \
  --dry-run
```

The same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. Its terminal residual explicitly failed the implication
`B #Equals addF(B,1.0)`; it was not a parser error, missing import, timeout,
or unrelated backend crash. Exact commands and output are in
`/audit-output/evidence/stage6/vacuity-dry-run.log` and
`vacuity-proof.log`.

**Stage 6 result: PASS.**

## 7. Proven versus assumed accounting

### What the successful K proof establishes

For every finite symbolic `NumSeq` consisting of arbitrary K `Int` and `Float`
coefficients such that:

```text
numLen(NS) >= 2
and numLen(NS) is even
and the final coefficient is nonzero
```

the fixed MPY execution of the exact submitted module, called as
`find_zero(list(numVals(NS)))`, has the following partial-correctness property:
if execution reaches the relevant loop exits and function return, its result is
exactly

```text
solveFrom(
  NS,
  divII(numLen(NS), -numLen(NS)),
  divII(numLen(NS),  numLen(NS)))
```

where the equations of `solveFrom`, `bracketBegin`/`bracketEnd`, `bisectFrom`,
and `polyValue` reproduce each program update and guard. At the return
boundary, the proof also establishes the exact scope/frame cleanup, restored
environment, unchanged heap and heap counter, `noRet`, `NoExc`, and exit code
0 specified by `bisect-loop`.

The domain is symbolic and unbounded in list length and coefficient magnitude;
it is not a finite enumeration or bounded unrolling. As a partial-correctness
proof it does not establish loop termination.

### Trust and evidence ledger

| Boundary | Influence | Status and evidence |
|---|---|---|
| Supplied MPY semantics | All binding, evaluation, control, state, and numeric dispatch | Trusted by the rendered `SUPPLIED_SEMANTICS` condition; candidate copy is recursively identical |
| Trusted translator | Constructor identity of `solution.mpy` | Trusted mount; candidate copy and regenerated output are byte-identical |
| `divII`, `intToF`, `addF`, `subF`, `mulF`, `divF`, `gtF`, `eqF` | Initial endpoints, polynomial values, branches, returned result | Fixed-semantics primitives; opaque/total in Haskell and concrete via LLVM rules. The execution theorem is parametric in their terms and does not assume a hidden value equation |
| Program-derived summaries | Loop state and final result | Not trusted oracles: universally connected to fixed execution by the successful loop claims; body mutation breaks the connection |
| Modular composition | End-to-end theorem packaging | Exact adjacent configurations were inspected mechanically; no single wrapper claim was supplied |
| Candidate-versus-canonical numerical equivalence | Alignment of iterative powers with canonical `math.pow` under floating rounding | Source-level mathematical equivalence plus 210 zero-mismatch finite differential cases; not a universal floating-point theorem |
| Odd-degree/bracketing/bisection argument | Interprets `solveFrom` as a root approximation and supplies ordinary-real termination | Informal standard mathematics, not a K claim; this is the principal concern |
| Full CPython numeric behavior | NaN, infinity, overflow/conversion exceptions, custom numeric objects | Not modeled completely by the supplied MPY semantics; the material ordinary finite `Int`/`Float` HumanEval domain is covered |

### Adequacy judgment

The formal result is not free, tautological, or a one-way implication: the
returned value is fixed by an exact recursive execution summary, body
sensitivity is demonstrated, and a plus-one result mutation is rejected. The
source-contract domain is not materially narrowed: every finite mixed
`Int`/`Float` sequence satisfying the prompt's even-length/nonzero-leading
condition is represented symbolically.

However, neither `spec.k` nor another checked theorem states or proves the
human-facing root property. The argument that an odd-degree polynomial is
eventually bracketed and that bisection returns an adequate approximation is
informal; the exact residual/tolerance expected by HumanEval is also not a K
postcondition. Because that bridge is standard, explicitly bounded, supported
by concrete and differential evidence, and not encoded as a false proof rule,
it is a non-fatal legitimacy concern rather than `FAIL / NOT_LEGIT`.

**Stage 7 result: sound execution theorem with a documented informal
summary-to-intent boundary.**

VERDICT: CONCERNS
LEGITIMACY: LEGIT
