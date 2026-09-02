# Independent adversarial review: 82-prime-length

The candidate is not a legitimate partial-correctness proof of the full
generated program. Fresh reconstruction confirms that all three submitted
claims close, and the Python implementation itself is faithful. The fatal
problem is instead the theorem and proof-extension boundary: the only
large-input entry claim does not constrain the returned Boolean. It ends at an
invented marker produced by proof-local priority rules that preempt the real
`While`, discard its continuation, and fabricate cleaned control/state cells.
A fresh intended-domain witness proves that this marker is unreachable under
the fixed supplied semantics.

All candidate artifacts, compiled outputs, prose, and generation records were
treated as untrusted. All execution used fresh source copies and newly built
definitions below `/tmp/audit-work/prime-length-audit`.
Reviewer-authored executable/K artifacts used by the audit are also preserved
under `/audit-output/evidence/artifacts/`.

## 1. Input and provenance integrity

Status: pass; no audit-infrastructure breach.

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, `semantics_mode = SUPPLIED_SEMANTICS`, problem
`82-prime-length`, and condition `semantics`. I read the launcher record,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, the invocation and metrics records, the optional
`usage.json`, both Codex text records, the generation prompt, and the complete
973-line structured JSONL trace. Historical `runtime-metrics.json` is absent,
which is permitted for this declared legacy layout.

The independent provenance checker is
`/audit-output/evidence/stage1_provenance.py`; its exact run and output are in
`/audit-output/evidence/stage1_provenance.log`. It established:

- Every required record is a readable regular file or, for the trace root, a
  readable directory.
- The campaign-lock object is structurally equal to the `audit_campaign` block.
  Its actual and recorded SHA-256 are both
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every recorded single-file hash checked by the launcher record matches,
  including the run/task/result/invocation/metrics/usage records, prompt,
  canonical, translator, Codex records, and trace file.
- The structured trace has 973 valid JSON objects and zero parse errors. The
  full 2,300,139-character, 77,984-line Codex output was read by the checker;
  its old `#Top` and stuck-claim occurrences were counted only as untrusted
  historical claims.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted counterparts.
- The candidate and trusted `reference-semantics/` manifests each contain the
  same 25 entries with identical types and content hashes. Recursive `diff`
  also returned zero. There are no symlinks in the candidate, reference, or
  generation-evidence mounts.
- The trusted `/reference/reference-semantics` exists, as required by
  `SUPPLIED_SEMANTICS`.

The candidate contains all required proof artifacts. Candidate caches,
`current-spec.json`, `spec.json`, `kore-exec.tar.gz`, bytecode, and historical
logs were not used as definitions or proof results.

## 2. Program fidelity and candidate-versus-canonical checks

Status: pass.

The trusted prompt requires `prime_length(string)` to return `True` exactly
when the Python string's length is prime. The trusted canonical implementation
computes the length, rejects lengths 0 and 1, tries every divisor from 2 through
`length - 1`, rejects on a zero remainder, and otherwise returns `True`
(`/reference/prompt.py:2`, `/reference/canonical.py:6`).

The candidate implements the same algorithm with a `while` loop:

- `n = len(string)`;
- return `False` for `n < 2`;
- test divisors starting at 2 while `divisor < n`;
- return `False` when `n % divisor == 0`;
- otherwise increment by 1 and ultimately return `True`
  (`/candidate/solution.py:1`).

The trusted translator regenerated the submitted term byte-for-byte. Both
`solution.mpy` and the fresh `solution.regenerated.mpy` have SHA-256
`a83f11f40bee4fd66c4575c4fad03318b4fa3438a3d731c323b46e13487670ed`,
and `cmp` exited 0. The exact commands are in
`/audit-output/evidence/stage2_fidelity.sh` and their successful log is
`/audit-output/evidence/stage2_fidelity.log`.

The reviewer-authored differential test
`/audit-output/evidence/stage2_differential.py` imports the trusted canonical
and candidate modules independently. It covered:

- all four documented examples;
- explicit empty, branch-boundary, prime, and composite lengths;
- Unicode, combining-character, and embedded-NUL strings;
- five content patterns for every length from 0 through 300;
- 500 deterministic random strings with lengths through 500.

All 2,030 cases returned a Boolean and matched the canonical result; mismatch
count was zero. This is finite fidelity evidence, not a proof.

## 3. Clean proof reconstruction

Status: the submitted positive claims reconstruct and close; this is
verification evidence only.

Only source artifacts were copied into scratch. Neither candidate-built
definitions nor caches were copied. K 7.1.293 freshly built:

1. `audit-runtime-kompiled` from the trusted
   `reference-semantics/semantics.k` using LLVM, `MPY-KRUN`, and `MPY-SYNTAX`;
2. `audit-verification-kompiled` from the submitted `verification.k` and the
   scratch trusted semantics using Haskell, `VERIFICATION`, and `MPY-SYNTAX`.

The reviewer concrete program contains the exact submitted function and
assertions at lengths 0 through 12 plus the documented examples. Its trusted
translation executed to `.K` with exit code 0 under the fresh LLVM definition.

Each positive target was then selected and run independently:

| Command target | Output | Exit |
|---|---:|---:|
| `SPEC.prime-length-small` | `#Top` | 0 |
| `SPEC.prime-length-setup` | `#Top` | 0 |
| `LOOP-SPEC.divisor-loop` | `#Top` | 0 |

The exact compile, concrete, and proof commands, statuses, and bounded outputs
are preserved in `/audit-output/evidence/stage3_reconstruct.sh` and
`/audit-output/evidence/stage3_reconstruct.log`. This independently confirms
closure under the submitted extended theory. It does not establish that the
extended theory is sound or that these claims amount to the requested entry
theorem.

## 4. Adequacy and real-program pinning

Status: fail for the full source contract.

### Plain-language claims

`prime-length-small` (`/candidate/spec.k:51`) starts an exact call to
`primeLengthClosure` on an arbitrary `str(CS)`. Its precondition is
`0 <= isLen(CS) < 2`; its postcondition is the returned value `false`, with the
initial module/builtins state restored. This is a sound, result-constraining
entry theorem for lengths 0 and 1.

`prime-length-setup` (`/candidate/spec.k:77`) has precondition
`isLen(CS) >= 2`. It starts the same exact call but its destination is
`#primeLoopEntry(isLen(CS), 2)`, with scopes and control state erased. This is
not a returned value or a state of the supplied Python semantics. It does not
state that the function returns `noDivisorsFrom(isLen(CS), 2)`, still less that
it returns the required Boolean characterization of primality.

`divisor-loop` (`/candidate/spec.k:9`) begins at the supplied semantics'
internal `#while` control point with live local values `n = N` and
`divisor = D`, an exact loop body, exact `Return(True)` suffix, call frame, and
otherwise fixed cells. Its only arithmetic precondition is `D >= 2`. Its
postcondition is the returned Boolean `noDivisorsFrom(N,D)`. The claim is
sound even when `D >= N`, and its broader domain is harmless.

### Program identity

The entry claims use an explicit closure rather than loading the complete
module. That representation is acceptable in principle here:

- trusted regeneration makes `solution.py` and `solution.mpy` mechanically
  connected;
- `primeLengthClosure`, `primeBody`, and `primeLoopBody` expand to the same
  function name, parameter, defining environment, and constructor body;
- the reviewer claim in
  `/tmp/audit-work/prime-length-audit/body-identity.k` compares the expanded
  proof term to the normalized constructor term from `solution.mpy`;
  `BODY-IDENTITY.submitted-body` printed `#Top` and exited 0. The initial
  parser-normalization attempt and successful corrected run are both retained
  in `/audit-output/evidence/stage4_identity.log` and
  `/audit-output/evidence/stage4_identity_success.log`.
  A preserved copy is
  `/audit-output/evidence/artifacts/body-identity.k`.

Thus the immutable aliases themselves do not substitute a different body.
The adequacy failure is that no sound fixed-semantics entry theorem executes
that body through its large-input return.

### Satisfying states and concrete substitutions

The independent witness record is
`/audit-output/evidence/stage4_ground_witnesses.log`.

- `CS = .IntSeq` satisfies `prime-length-small`; both Python
  implementations return `False`.
- `CS = iCons(97,iCons(98,.IntSeq))` (the string `"ab"`) satisfies
  `prime-length-setup`; both Python implementations return `True`, while the
  claim's destination is only the proof marker.
- `N=2,D=2` satisfies `divisor-loop`; `noDivisorsFrom(2,2)`, the candidate,
  and the canonical are all `True`.
- `N=4,D=2` yields `False`; `N=5,D=2` and `N=11,D=2` yield `True`; these agree
  with both Python implementations.

The setup prose says that the setup and loop claims yield the desired result,
but the formal artifacts do not compose them. The setup destination omits the
exact loop condition, body, continuation, frame, and cells needed to match the
loop theorem. More importantly, that destination is obtained only by the
unsound operational bridge analyzed in Stage 5. `PROOF.md`, prose, and static
inspection cannot replace a missing sound entry reachability claim.

## 5. Rule-by-rule static soundness review

Status: fail.

### Exhaustive inventory and used-construct mapping

`/audit-output/evidence/stage5_inventory.py` inventories every local
`syntax`, `rule`, `context`, `configuration`, and `claim` declaration in the
trusted supplied semantics, `verification.k`, and `spec.k`. The corrected
attribute-aware output is
`/audit-output/evidence/stage5_rule_inventory_v2.log`.

The inventory contains 945 entries:

- 232 syntax declarations;
- 704 rules;
- 5 contexts;
- 1 configuration;
- 3 claims.

It separately lists all 149 function-bearing entries, 107 total declarations,
25 symbol declarations, 22 `no-evaluators` declarations, 32 concrete-rule
entries, 32 priority entries, 26 `owise` entries, and every opaque/symbolic
declaration. There are no local `functional` or `simplification` declarations.
The earlier uncorrected attribute scan is retained as
`stage5_rule_inventory.log`; it over-counted attributes mentioned in comments
and is not used for the totals above.

The same inventory maps every constructor used by `solution.mpy` to its
declaration and execution rules: `Module`, `FuncDef`, parameters and statement
lists, `Assign`, name lookup, `Call`, `len`, `If`, `Compare`/`CmpOp`,
`Int`/`Bool`, `Return`, `While`, `%`, `AugAssign(+)`, and argument lists.

On the reached path, the supplied rules preserve left-to-right call/argument
evaluation, create and pop the call frame, bind and update the current local
scope, compute string length structurally, dispatch integer comparisons and
positive-divisor modulo, execute `while` through `#while/#whileCond`, and
propagate `Return` by discarding the function suffix and popping the exact
frame. Heap, exception, and exit cells remain unchanged. None of the supplied
semantics' float, sort, MD5, or other opaque symbols occurs in the submitted
program or claims. Unused fixed-semantics entries therefore cannot influence
claim closure. The fixed supplied tree is also exactly the trusted tree
selected by the benchmark condition.

### Proof-local rule decisions

The five syntax declarations and nine rules in
`/candidate/verification.k` have these dispositions:

| Extension | Class and decision |
|---|---|
| `primeLoopBody` and its equation, lines 8–17 | Truthful definitional abbreviation; accepted. |
| `primeBody` and its equation, lines 19–31 | Truthful definitional abbreviation; accepted. |
| `primeLengthClosure` and its equation, lines 33–35 | Truthful exact closure abbreviation; accepted. |
| `#primeLoopEntry`, `#capturePrimeLoopN`, `#capturePrimeLoopD`, lines 40–42 | Fresh proof-only observation/control symbols; their use is result-relevant to the large-input setup claim. |
| `While(_C,_B)` interception, lines 43–49 | Rejected operational bridge. It ignores condition and body, admits every continuation and framed cell through `...`, and priority 1 preempts the supplied `While => #while` rule. |
| capture-N rule, lines 51–56 | Rejected as part of the bridge. It retains a real lookup of `"divisor"` but carries arbitrary `REST`. |
| capture-D/cleanup rule, lines 58–69 | Rejected operational/control bridge. It explicitly discards `_REST`, rewrites arbitrary `env`, `scopes`, `scopeLoc`, `stack`, and `ret` cells, and fabricates `#primeLoopEntry`. |
| `noDivisorsFrom` base-true rule, lines 73–75 | Valid when `D >= N`. |
| zero-remainder rule, lines 76–77 | Valid for `D < N`, and disjoint from the other cases. |
| recursive nonzero rule, lines 78–79 | Valid for the loop uses: `D >= 2` makes modulo defined, the guard is complementary to zero remainder, and `D+1` descends toward the base case. |

The `noDivisorsFrom` guards are exhaustive and pairwise disjoint over the
helper claim's domain. The three abbreviation functions have single
equations. There are no proof-local opaque values, totality assertions, or
simplification rules. The defect is confined to, but material in, the three
capture/cleanup rules.

### Required false-conclusion witness

The complete bridge context and state footprint are tested by:

- `/tmp/audit-work/prime-length-audit/verification-fixed.k`, which contains
  the same exact body aliases and marker syntax but no capture bridge;
- `/tmp/audit-work/prime-length-audit/bridge-witness-extended.k`;
- `/tmp/audit-work/prime-length-audit/bridge-witness-fixed.k`;
- `/audit-output/evidence/stage5_bridge_witness.sh` and its exact log
  `/audit-output/evidence/stage5_bridge_witness.log`.

Preserved copies of the three K sources are under
`/audit-output/evidence/artifacts/`.

The witness is the real generated-function call on the intended input `"ab"`
(length 2), from the normal initial configuration.

1. Under the candidate's extended definition, the false relative-to-fixed
   claim that this call reaches `#primeLoopEntry(2,2)` printed `#Top` and
   exited 0.
2. Under a freshly compiled bridge-free supplied definition, the claim that
   the same call returns `true` printed `#Top` and exited 0.
3. Under that bridge-free definition, the marker claim exited 1 with
   `WarnStuckClaimState`. Its irreducible `<k>` cell contains `true ~> .K`,
   not the marker, and the genuine module/builtins scopes and scope location
   remain restored.

This is a concrete false conclusion enabled by the rejected rules on a
satisfying intended-domain input. It also exhibits the control mismatch: the
bridge discards the real `Return(True) ~> .Stmts ~> #endcall` continuation and
fabricates different scope/frame cleanup. There is no bridge-free universal
connection theorem over the bridge's complete match domain. The separately
proved `divisor-loop` starts at one exact `#while` state and cannot justify a
rule matching arbitrary raw `While` terms, arbitrary suffixes, and arbitrary
cells.

## 6. Fresh non-vacuity test

Status: pass for the small-input slice; it does not cure the large-input
adequacy and soundness failures.

No candidate vacuity artifact was trusted. I created
`/tmp/audit-work/prime-length-audit/spec-vacuity-audit.k`, changing the
result-constraining destination of `prime-length-small` from `false` to
`true`. This mutation is false for the explicit satisfying witness
`CS = .IntSeq` (and also for a one-character sequence).
A preserved copy is
`/audit-output/evidence/artifacts/spec-vacuity-audit.k`.

The exact script and output are
`/audit-output/evidence/stage6_nonvacuity.sh` and
`/audit-output/evidence/stage6_nonvacuity.log`:

- `kprove ... --dry-run` parsed and built the mutated specification, printed
  the backend command, and exited 0;
- the real proof exited 1 with `WarnStuckClaimState`;
- the residual has `false ~> .K` under the original satisfiable length
  constraints, exactly the unmet `false` versus mutated `true` obligation.

This is meaningful non-vacuity evidence for the submitted small-length claim.
There is no large-input returned-result claim to mutate.

## 7. Proven versus assumed accounting

Status: Gate A fails; the candidate is not legitimate.

What the three successful submitted proof runs establish, precisely and only
under the submitted extended theory, is:

1. for every modeled string sequence of length 0 or 1, the exact submitted
   closure returns `false`;
2. for every modeled string sequence of length at least 2, execution under the
   capture extension reaches the invented marker
   `#primeLoopEntry(length,2)`;
3. from the exact internal divisor-loop configuration with `D >= 2`, supplied
   execution returns the recursively defined `noDivisorsFrom(N,D)`.

They do not establish a sound fixed-semantics entry theorem saying that the
submitted generated function returns `noDivisorsFrom(length,2)` for every
length at least 2, or that it returns the source-contract result over the full
domain.

Trust and assumption ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied MPY configuration, call/frame, lookup, control, integer, modulo, and string-sequence rules | All three claims | Acceptable benchmark-selected fixed semantics; exact tree integrity verified and every reached rule mapped. |
| K's unbounded `Int` and structural `IntSeq` length | Length, divisors, loop summary | Acceptable here. Python integers are unbounded, and content is unobserved except through structural length. |
| K toolchain/backend correctness, version 7.1.293 | All machine checks | Ordinary explicit trust boundary. |
| `primeBody`, `primeLoopBody`, `primeLengthClosure` equations | Entry and loop claims | Acceptable definitions; trusted translator identity and fresh constructor identity check support exact pinning. |
| `noDivisorsFrom` equations | Loop result | Acceptable mathematical definition on `D >= 2`; equations are guarded, disjoint, exhaustive, and descending. |
| Elementary bridge from “no divisor in 2..N-1” to primality for `N >= 2` | Human-facing contract | Ordinary informal mathematics, acceptable if a sound entry theorem returned that value. |
| Differential comparison against canonical Python | Program-fidelity bridge only | Finite empirical support over 2,030 cases; not a substitute for the K theorem. |
| `While` capture and cleanup rules | The only length-at-least-2 entry claim and any proposed composition | Illegitimate. They replace execution, alter control/state, admit broader contexts than any helper theorem, and have the concrete false witness above. |
| Prose-level composition of setup marker with `divisor-loop` | Claimed full result | Illegitimate as a substitute for a fixed-semantics result-constraining entry claim. |

The Python implementation is correct and the loop helper is useful proof
progress. Nevertheless, the requested decision concerns a legitimate proof of
the unrestricted string contract, not whether some claims printed `#Top`.
Because the large-input entry result is missing and its replacement depends on
a materially unsound operational bridge, the required benchmark mapping is
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
