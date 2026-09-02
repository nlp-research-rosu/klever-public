# Independent adversarial audit: 78-hex-key

The reconstructed proof is legitimate and result-constraining. It executes the
exact trusted-translator output for the submitted `solution.py`, and both
positive claims close from clean source builds. The only verdict-level concern
is incomplete candidate provenance: four required generation artifacts are
absent. That defect limits auditability but does not invalidate the independently
reconstructed theorem.

Audit environment: K v7.1.337, recorded in
`evidence/00-environment.log`. All candidate material was treated as untrusted
and read-only. Fresh sources and builds were kept under
`/tmp/audit-work/78-hex-key`; reviewer evidence is under
`/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted mount is consistent with
that mode: `/reference/reference-semantics` exists and is a normal directory.
There is therefore no infrastructure breach.

`evidence/integrity_check.py` recursively compared entry names, entry types, and
SHA-256 hashes. The candidate and trusted supplied-semantics trees each contain
25 non-root entries and have zero mismatches. There are no missing, additional,
changed, mistyped, or symlinked entries in the candidate
`reference-semantics/` tree. The candidate prompt and translator are normal
files and byte-identical to the trusted mounts:

- `prompt.py`: SHA-256
  `0f302c2314267fba8ddb3d9fa69d4dbb49dee3249d64a84f1048661f1ad2ae6e`.
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

Four explicitly required candidate provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present; the audit instruction only requires
reading it when present. The extra top-level candidate artifacts
`concrete_tests.py`, `concrete_tests.mpy`, `prove.sh`, `kprove.out`, `krun.out`,
and `__pycache__/` are not trusted inputs. I read the two bounded output files
only as claims: they allege `#Top` and a normal final concrete configuration.
Neither output nor the bytecode/cache was reused. The exact integrity command
and result are in `evidence/01-integrity.log`.

Stage 1 decision: integrity of all theorem source inputs passes, while required
generation provenance is incomplete. This is the reason for `CONCERNS` rather
than `PASS`.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for the number of characters in a valid uppercase
hexadecimal string that are one of `2`, `3`, `5`, `7`, `B`, or `D`; empty input
is valid and produces zero. The trusted canonical implementation iterates by
index and increments once when the character is in the six-element tuple.

The candidate `solution.py` iterates directly over the string and increments
once when the character is in `"2357BD"`. On the intended domain these are the
same computation. Initializing `digit` to `""` is semantically inert except
that it gives the loop variable a defined value on empty input.

The trusted translator was run afresh:

```text
python3 /tmp/audit-work/78-hex-key/py2mpy.py \
  /tmp/audit-work/78-hex-key/solution.py \
  > /tmp/audit-work/78-hex-key/regenerated-solution.mpy
```

It exited 0. `cmp` against the submitted `solution.mpy` exited 0, and both files
have SHA-256
`38b240e2fa272c61074e88862eb2e90f8c2f8721ebd883d3976c5b466d3e6d7a`.
See `evidence/02-translation.log`.

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch copy of the generated solution. Its
input corpus includes:

- all five documented examples;
- empty input, every one-character hexadecimal branch boundary, all-prime and
  no-prime strings, forward/reversed alphabets, and length-1000 cases;
- every uppercase hexadecimal string of lengths 0 through 4 (69,905 strings);
- 2,000 deterministic generated strings of lengths 0 through 256.

After de-duplication, 71,878 exact inputs and both results are preserved in
`evidence/differential-inputs.jsonl` (SHA-256
`064558dba70f8b092def3e0f64783c2f40a2d5385c6874b8b1ce41255873629d`).
The run exited 0 with zero mismatches; see `evidence/03-differential.log`.
This is finite intent-bridge evidence, not a substitute for the K proof.

Stage 2 decision: pass.

## 3. Clean proof reconstruction

No candidate-built definition or cache was copied. The trusted supplied
semantics and the candidate source proof files were copied into scratch. The
following were built from source:

- LLVM concrete definition: `evidence/04-concrete-build.log`, exit 0.
- Haskell proof definition: `evidence/06-proof-build.log`, exit 0.

The reviewer-authored concrete program `evidence/concrete_audit.py` contains the
exact submitted implementation followed by assertions for empty input, every
prompt example, every one-character hexadecimal branch, an all-prime string,
and a no-prime string. It was translated with the trusted translator. `krun`
exited 0 with `.K`, `NoExc`, and exit code 0; see
`evidence/05-concrete-run.log`.

Every positive claim was checked without relying on candidate output:

| Target | Fresh command evidence | Result |
|---|---|---|
| `loop-lemma` alone | `evidence/07-proof-loop-lemma.log` | exit 0, `#Top` |
| both original claims | `evidence/09-proof-all-claims.log` | exit 0, `#Top` |
| original `entry-point` after the independently closed loop lemma is marked trusted | `evidence/19-proof-entry-original-after-loop.log` | exit 0, `#Top` |

The last command uses the original `spec.k`; it does not alter the entry claim.
Trusting the loop label there is proof composition only after the exact loop
claim independently closed. An entry-only diagnostic that filtered the helper
claim out was interrupted after 120 seconds of symbolic loop unrolling
(`evidence/08-proof-entry-point-only.log`, status 130). That diagnostic is not
used as positive or negative proof evidence. The original two-claim proof and
the composed per-claim checks all close.

The concrete LLVM build emitted non-exhaustive-totality warnings for operations
such as float conversion, keyed mapping, joining, and out-of-bounds sequence
access. None is reachable from this program. They belong to the trusted
supplied semantics rather than a candidate proof extension. The Haskell proof
build only emitted unused-variable warnings in unrelated string-order rules.

Stage 3 decision: pass.

## 4. Adequacy and real-program pinning

### Claims in plain language

The `loop-lemma` starts at the real supplied-semantics loop head with:

- an arbitrary finite code sequence `CS` as the remaining string;
- a current local frame containing integer accumulator `ACC`, prior loop value
  `DIGIT`, and preserved `NUM`;
- no return or exception in progress, exit code 0, and arbitrary framed
  continuation/caller state.

If the loop terminates, it resumes the exact continuation, adds
`hexCount(CS)` to `count`, leaves `digit` unchanged for empty `CS` or equal to
the final one-character string otherwise, preserves `num`, and preserves every
other explicit cell.

The `entry-point` starts from the supplied MPY initial configuration, loads a
single `hex_key` function with `hexKeyBody`, and calls that function on
`str(CS)` for arbitrary `CS:IntSeq`. If execution terminates, the `<k>` result
is exactly `hexCount(CS)`. The module closure is retained, the local call frame
is removed, and environment, allocation, heap, stack, return, exception, and
exit cells have the stated final values. The RHS is not a fresh variable,
tautology, implication, or existential result.

### Exact real-program identity

The trusted-translator output and the entry claim’s
`Module(FuncDef(..., hexKeyBody))` were independently parsed by `kast` with
macro expansion. Their KAST files are byte-identical with SHA-256
`5d9eed7cbddc042f542f7e9dacef07b946472636097ed3effc2aceed87497142`.
Commands and the expanded term are in `evidence/13-ast-pinning.log`. Thus the
claim executes the submitted `solution.mpy` AST rather than a substitute.

The helper claim starts exactly where the actual `For` rule reaches
`#loop(str(CS), Name("digit"), hexKeyLoopBody)`. Each supplied-semantics step
binds the head one-character string, executes the real `If`/membership body,
updates `count` only on membership, and recurs on the string suffix. Its
`finalDigit` component matches the actual loop-target side effect.

### Satisfiable witnesses

`evidence/spec-ground-witnesses.k` instantiates the complete entry
configuration for empty input and for `"AB"` (code sequence 65, 66), with
postconditions 0 and 1. The ground claims exited 0 with `#Top`; both Python
implementations also returned 0 and 1. See
`evidence/14-ground-witness-proofs.log`. These are concrete states satisfying
the entry precondition. The loop precondition is also realized during the
`"AB"` execution: after initialization and call binding, `ACC=0`,
`DIGIT=str(.IntSeq)`, `NUM=str([65,66])`, and the remaining loop input is
`[65,66]`.

The formal `IntSeq` domain is broader than valid uppercase hexadecimal text.
That is not a strengthening or vacuity: it includes the complete intended
domain, and the same singleton-code membership computation remains sound on
the extra sequences.

Stage 4 decision: pass.

## 5. Rule-by-rule static soundness review

`evidence/static-rule-inventory.md`, generated by
`evidence/static_inventory.py`, is the exhaustive source inventory. It lists
every source line beginning with `syntax`, `configuration`, `context`, `rule`,
or `claim`, including the complete stanza, attributes, classification, and
used-path status. Across `semantics.k`, all 23 helper files,
`verification.k`, and `spec.k`, it contains:

- 233 syntax declarations;
- 1 configuration;
- 5 explicit evaluation contexts;
- 703 rules;
- 2 claims;
- 944 total inventoried entries, of which 102 are on this program/proof path.

Of these, 227 syntax declarations, the configuration, all five contexts, and
695 rules are the exact selected supplied-semantics baseline. They are not
candidate-local proof extensions. `MPY-CONCRETE` is inventoried because it is
used for the fresh concrete definition but is not imported by the Haskell
proof module. Entries marked “not used by solution” have no path from the exact
submitted AST or candidate helper equations. The manual mapping and decisions
for the complete used path are in `evidence/used-path-review.md`.

The used execution route is:

| Phase | Selected-semantics sources |
|---|---|
| AST declarations and strict/seqstrict evaluation | `semantics/syntax.k:9-61` |
| initial configuration, module load, sequencing, names, literals | `semantics/core.k:49-215` |
| function definition, argument binding, return, frame removal | `semantics/functions.k:8-90`, `semantics/call.k:19-74` |
| `For` control and string iterator | `semantics/controls.k:65-85`, `semantics/iter.k:8`, `semantics/str.k:8-10` |
| loop-target binding | `semantics/tuple.k:31-41` |
| `If` and string membership | `semantics/operators.k:15-17`, `semantics/str.k:13-41`, `semantics/controls.k:51-54` |
| integer accumulator update | `semantics/controls.k:20-31`, `semantics/int.k:9` |

This route evaluates the actual callee and argument, allocates and restores the
call frame, preserves the heap (the program performs no allocation), evaluates
the iterable once, preserves iteration order, and returns the actual local
`count`. Priority alternatives for refs/cells cannot match the exact plain
local frame. No used construct is unmodeled or fabricated.

The six candidate syntax/rule groups in `verification.k` were reviewed over
their complete domains:

1. `hexKeyLoopBody` is a syntax macro expanding to the exact translated `If`
   and `AugAssign` body.
2. `hexKeyBody` is a syntax macro expanding to the exact translated function
   statement sequence.
3. `isPrimeHexCode(C)` has one unguarded, total equation. Singleton `[C]`
   occurs in `[50,51,53,55,66,68]` exactly when `C` is a code for one of
   `2357BD`.
4. `primeHexBit(C)` has one unguarded, total equation returning exactly 1 or 0
   from that Boolean.
5. `hexCount` has disjoint, exhaustive empty/cons equations and strictly
   descends on the tail.
6. `finalDigit` has disjoint, exhaustive empty/cons equations and strictly
   descends on the tail. It affects the loop-local `digit`, not the entry
   result.

There are no candidate-local `priority`, `owise`, `simplification`, `concrete`,
`trusted`, or operational rewrite rules, and no candidate-local opaque symbol.
The scan is preserved in `evidence/20-extension-and-opaque-scan.log`. The
mathematical helpers summarize the postcondition and invariant; none rewrites a
program call, loop, membership expression, return, continuation, or state cell.
Therefore there is no operational bridge needing a bridge-free connection
theorem and no result-bearing oracle.

A material body mutation changed the real matching-branch update from
`count += 1` to `count += 2`. Its definition built successfully
(`evidence/17-body-mutation-build.log`) and the original invariant then failed
with exit 1 at the expected obligation
`ACC + 2 + hexCount(R) = ACC + (hexCount(R) + 1)`
(`evidence/18-body-mutation-proof.log`). This confirms body sensitivity.

No inventoried candidate rule is labeled unsound, so no false-conclusion
witness is required. The only narrower supplied-semantics evidence gap is the
compiler’s unused-operation totality warnings noted in Stage 3; those rules are
trusted baseline and unreachable here, so they cannot enable this theorem’s
conclusion.

Stage 5 decision: pass.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` exists. I created the independent
`evidence/spec-vacuity.k`, retaining the loop lemma and changing only the entry
result from `hexCount(CS)` to the false result `hexCount(CS) +Int 1`. Empty
input is a satisfying counterexample: the actual and original claimed result
is 0, while the mutation demands 1.

The mutation parsed and compiled successfully under `kprove --dry-run` with
exit 0 (`evidence/15-vacuity-dry-run.log`). The real proof run then exited 1
with `WarnStuckClaimState`; its residual explicitly reports the failed
implication between `hexCount(CS)` and `hexCount(CS) +Int 1`. See
`evidence/16-vacuity-proof.log`. This is an expected unmet result obligation,
not a parser error, missing import, timeout, or unrelated crash.

Stage 6 decision: pass.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics and the exact initial configuration in
`spec.k`, for every finite `CS:IntSeq`, every terminating execution of the
exact submitted `hex_key(str(CS))` returns:

```text
hexCount(CS)
```

where `hexCount` is the structural sum of 1 for codes
50, 51, 53, 55, 66, or 68 and 0 for every other code. This is a
partial-correctness theorem; it is not reported as an independent termination
proof. On the prompt’s valid uppercase hexadecimal domain, that value is
exactly the requested number of prime hexadecimal digits.

### Trust and assumptions

- **Selected supplied semantics.** The exact trusted
  `/reference/reference-semantics` tree defines execution, values,
  configuration, evaluation order, calls, loops, and returns. This is the
  mode-mandated trust boundary. The candidate copy is byte/type identical.
- **K implementation and hooked mathematics.** K v7.1.337, the Haskell/LLVM
  backends, and built-in integer, Boolean, string, map, list, equality, and
  code-point hooks are trusted. The used theorem relies on integer addition,
  equality, maps, sequences, and ASCII literal decoding.
- **Trusted translator.** `/reference/py2mpy.py` is outside the reachability
  theorem but is trusted to define the generated `.mpy` program. Fresh
  translation and macro-expanded KAST identity pin that generated program to
  the theorem.
- **Intent encoding.** The standard code-point facts
  `2=50`, `3=51`, `5=53`, `7=55`, `B=66`, and `D=68` connect the formal
  recurrence to the prompt. The supplied semantics evaluates the literal
  `"2357BD"` with those codes on the used path.
- **Finite empirical bridge.** The 71,878-case differential test and fresh K
  concrete assertions support generated-Python/canonical and concrete-semantics
  agreement only on their recorded inputs. They are not used as universal
  proof premises.

The proof definition imports supplied opaque symbols that are unreachable from
this program: `sortVS`, `sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`,
`floatMod`, `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, and `sqrtF`. None occurs in `solution.mpy`,
`verification.k`, `spec.k`, or the 102-entry used path, and none influences
control, observable state, the returned value, or a postcondition in this
proof. The supplied structural functions `strLt` and `valSeqAt` can also remain
abstract on symbolic/non-structural cases; they too are unreachable here.

There are no candidate-local trusted primitives, empirical execution
summaries, opaque values, or informal arguments standing in for program
execution. Candidate `kprove.out`, `krun.out`, absent generation records, and
differential tests are not treated as substitutes for the reconstructed
reachability proof.

Gate A (real-program soundness): pass. Gate B (intent adequacy): pass. Gate C
(reviewer evidence and trust accounting): pass, with the documented candidate
provenance limitation. The proof is legitimate; incomplete required provenance
warrants a concern but does not create a material soundness or adequacy gap.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
