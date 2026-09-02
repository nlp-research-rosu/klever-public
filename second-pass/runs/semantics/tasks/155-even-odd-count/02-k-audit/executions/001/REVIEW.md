# Independent adversarial audit: 155-even-odd-count

The candidate is not a legitimate proof under the fixed supplied semantics.
Both submitted positive claims rebuild and print `#Top`, and the entry claim is
non-vacuous, but its proof depends on a priority-40 operational summary whose
match domain is strictly broader than the theorem offered to justify it. A
fully grounded counterexample shows the fixed semantics and the summary produce
opposite observable counts for the same decimal digit. The extended definition
therefore proves a concrete false reachability conclusion.

Audit mode: `SUPPLIED_SEMANTICS`. There was no infrastructure-mode
contradiction, so a candidate verdict is appropriate.

## 1. Input and provenance integrity

### Mode boundary and source integrity

`/reference/reference-semantics` is present, as required in supplied-semantics
mode. The recursive type, path, and byte comparison found that
`/candidate/reference-semantics` has no missing, additional, changed, mistyped,
or symlinked entry. The candidate `prompt.py` and `py2mpy.py` are byte-identical
to `/reference/prompt.py` and `/reference/py2mpy.py`. No candidate symlink was
found. See [01-integrity.log](evidence/01-integrity.log).

The candidate contains a Python bytecode cache
`/candidate/__pycache__/solution.cpython-310.pyc`. It was treated as an
untrusted build artifact and was not copied or used. All source inputs were
copied explicitly to `/tmp/audit-work/candidate-src`, all trusted inputs to
`/tmp/audit-work/trusted`, and hashes were recorded in
[02-scratch-copy.log](evidence/02-scratch-copy.log). No candidate K definition
or cache was reused.

### Missing provenance records

The following required records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace was present. Consequently, there were no such
records to read even as untrusted claims. This is a provenance and auditability
failure, though it is not the basis of the substantive proof-unsoundness
finding. The candidate also supplied no `PROOF.md` or candidate
`spec-vacuity.k`; neither was trusted or needed.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For every integer `num`, ignore the minus sign, inspect the decimal digits of
`abs(num)`, and return a two-element tuple: first the number of even digits,
then the number of odd digits. Thus `-12` maps to `(1, 1)`, `123` maps to
`(1, 2)`, and `0` maps to `(1, 0)`. There is no legal integer whose decimal
representation is empty; zero is the minimal one-character boundary case.

The candidate uses `ord(digit) % 2` instead of `int(digit) % 2`. For decimal
ASCII codes 48 through 57, code parity equals represented-digit parity because
48 is even. The sign is excluded by `abs`.

### Translation identity

Running the trusted translator on the copied `solution.py` produced a file
byte-identical to submitted `solution.mpy`; both SHA-256 hashes are
`4eb2b3f6755b8446a0c9559d07c8c85a6e525b69fe8126b31b411763bb0ecc3c`.
The command and exit 0 are in
[04-translation-identity.log](evidence/04-translation-identity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports
the trusted canonical entry point and copied candidate entry point. Its exact
input list is preserved as
[differential_inputs.json](evidence/differential_inputs.json). It covered:

- both documented examples;
- zero, both signs, one-digit and decimal-length boundaries;
- all decimal digits 0 through 9, hence both parity branches;
- every integer in `[-10000, 10000]`;
- 2,000 deterministic seed-155 integers with widths from 0 through 512 bits;
- crafted all-even, all-odd, mixed, and large decimal values.

There were 21,942 distinct inputs and zero mismatches, with tuple type also
checked. See [05-differential.log](evidence/05-differential.log). This is strong
finite evidence for implementation-to-canonical agreement, not a universal
K proof.

## 3. Clean proof reconstruction

The installed K toolchain is version `v7.1.337`; see
[00-toolchain.log](evidence/00-toolchain.log).

The following were independently rebuilt from the scratch source copy:

| Target | Result | Evidence |
|---|---:|---|
| LLVM `MPY-KRUN` definition from supplied source | exit 0 | [06-build-runtime.log](evidence/06-build-runtime.log) |
| Trusted regeneration and K execution of `concrete_tests.mpy` | exit 0, final `.K`, no exception, exit code 0 | [19-concrete-regeneration.log](evidence/19-concrete-regeneration.log) |
| Haskell base definition, main module `EVEN-ODD-VERIFICATION` | exit 0 | [08-build-proof-base.log](evidence/08-build-proof-base.log) |
| Positive loop claim, module `EVEN-ODD-LOOP-SPEC` | exit 0 and `#Top` | [09-prove-loop.log](evidence/09-prove-loop.log) |
| Haskell summary definition, main module `EVEN-ODD-VERIFICATION-SUMMARY` | exit 0 | [10-build-proof-summary.log](evidence/10-build-proof-summary.log) |
| Positive entry claim, module `EVEN-ODD-SPEC` | exit 0 and `#Top` | [11-prove-entry.log](evidence/11-prove-entry.log) |

The runtime build emitted non-exhaustiveness warnings for several unused
supplied-baseline helper functions. The proof builds emitted only unused
variable warnings in `strLt`. None is an infrastructure failure, and none
explains the candidate's positive `#Top` results.

Thus clean reconstruction succeeds. The later soundness failure is not a
missing tool, timeout, malformed mount, stale cache, or failed positive claim.

## 4. Adequacy and real-program pinning

### Loop claim

The `EVEN-ODD-LOOP-SPEC` precondition says:

- the next computation is the actual digit loop over arbitrary `CS:IntSeq`,
  with exactly the submitted loop body, followed by arbitrary continuation
  `CONT`;
- `env` is local scope 1;
- the scope map is exactly the trusted builtins at `-1`, the submitted module
  scope at `0`, and one local scope at `1`;
- local `num`, `even_count`, and `odd_count` are integers and `digit` is a
  value.

Its postcondition resumes `CONT`, adds the parity counts of all codes in `CS`
to the two counters, and makes `digit` the last one-character string (or leaves
the old value for an empty sequence). Other generated configuration cells are
framed. The body has no return, exception, allocation, break, or continue on
the supported digit path.

The loop claim matches the real `For` control flow: `#iterNext` yields one
character, `#bindTgt` updates `digit`, the real `ord`/modulo/compare/if path
updates exactly one counter, and the circularity applies at the next loop head.

### Entry claim

The `EVEN-ODD-SPEC` precondition says:

- execute `even_odd_count(Int(N))` for any mathematical K integer `N`;
- start in module environment 0 with exactly the submitted function closure
  and trusted builtins;
- start with scope location 1, empty heap and stack, no pending return or
  exception, and exit code 0.

The postcondition is an exact tuple, not a free value or implication:
`evenDigits(strToCodes(Int2String(absInt(N))))` and the corresponding
`oddDigits`. All cells are pinned.

The entry claim begins after module loading; it does not literally parse a
filesystem path in its `<k>` cell. However, the hand-written macros are
structurally exact copies of submitted `solution.mpy`. To check that coupling
independently, [program-pin-witness.k](evidence/program-pin-witness.k) loads the
exact submitted AST under the fixed base semantics and reaches precisely
`#evenOddModuleScope`; it closes with exit 0 and `#Top` in
[15-program-pin.log](evidence/15-program-pin.log). Together with trusted
translator byte identity, this rules out a substituted function body. The
coupling is manual and fragile, but it is exact in this submission.

### Satisfying ground states

The entry precondition is satisfiable. For example, choose `N = 0`, `env = 0`,
the exact two loaded scopes, scope location 1, empty heap/stack, `noRet`,
`NoExc`, and exit code 0. The formal result is `(1, 0)`. The same construction
works for every K integer.

[claim_witness.py](evidence/claim_witness.py) substitutes `0`, `-12`, `123`,
`-24680`, `102030405`, and `10**50`. The formal postcondition model, trusted
canonical Python, and candidate Python agree on every witness; see
[16-claim-ground-witnesses.log](evidence/16-claim-ground-witnesses.log).

Adequacy and result pinning therefore pass in isolation. They do not make the
proof-local operational bridge sound.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[K-INVENTORY.md](evidence/K-INVENTORY.md), generated by the preserved
[k_inventory.py](evidence/k_inventory.py), contains one row for every
configuration, syntax declaration, context, rule, and claim in the complete
supplied semantics plus `verification.k` and `spec.k`. It inventories 945
entries: 705 rules, 232 syntax declarations, five contexts, one configuration,
and two claims. Each row records attributes including `function`, `total`,
`symbol`, `no-evaluators`, `macro`, `concrete`, `owise`, and `priority`.
There are no local `simplification` or `functional` declarations.

All 928 supplied-semantics entries are byte-identical to the selected trusted
baseline. I reviewed their configuration, overlaps, evaluation order, calls,
returns, control flow, state changes, allocations, priorities, totality
annotations, and opaque declarations. Their rules not reached by this program
cannot contribute to either target claim. On the reached path:

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequencing | `syntax.k`, `core.k`, `functions.k` load the exact closure and execute statements in order |
| `Name`, nested `Call`, argument evaluation | `core.k` and `call.k` perform lexical lookup, evaluate callee then arguments left-to-right, and dispatch by the resolved value |
| `abs`, `str`, `ord` | `builtins.k` implements integer absolute value, decimal `Int2String` conversion through `strToCodes`, and one-character code extraction |
| `For`, target binding, `If`, `Assign`, `AugAssign` | `controls.k`, `iter.k`, and `tuple.k` implement one-shot iterable evaluation, loop stepping, branch truthiness, and local writes |
| `%`, `==`, `+` | `operators.k` and `int.k` route to `pyMod`, integer equality, and integer addition |
| `Str`, `TupleExpr`, `Return`, frame pop | `str.k`, `tuple.k`, `functions.k`, and `core.k` evaluate the docstring, construct the result tuple, and restore/deallocate the call frame |

The candidate adds 14 sound definition/macro entries, two target claims, and
one unsound operational bridge:

- `evenDigits` and `oddDigits` have disjoint, exhaustive algebraic equations
  for empty and cons `IntSeq` values. Recursion strictly descends and the
  parity equations are ordinary integer mathematics.
- `lastSeen` has disjoint empty/cons equations, strictly descends, and exactly
  models the final loop-target value.
- `#digitLoopBody`, `#evenOddFunctionBody`, and `#evenOddModuleScope` are macros,
  not oracles. Their expansions exactly reproduce the submitted AST and loaded
  closure.
- No proof-local value is opaque, no task answer is installed as an
  unconstrained function, and no candidate simplification rule exists.

### Unsound priority-40 operational bridge

`verification.k:62-86` replaces

```text
#loop(str(CS), Name("digit"), #digitLoopBody) ~> CONT
```

with `CONT` and directly writes the summarized local scope. It is an
operational bridge: it preempts all fixed loop execution. Its complete match
domain fixes `env = 1` and the four bindings in local scope 1, but the
ellipses in `<scopes>` admit arbitrary scopes 0 and -1 and arbitrary additional
scope entries. It also frames every other configuration cell.

The only claimed connection theorem, `EVEN-ODD-LOOP-SPEC`, is materially
narrower. It requires scope 0 to be exactly `#evenOddModuleScope`, scope -1 to
be exactly `builtinsScope`, and the complete map to contain exactly scopes
`-1`, `0`, and `1`. That theorem does not establish the bridge over a module
scope that shadows `ord`. Rule priority cannot supply the missing
context-containment proof.

This is not merely an evidence gap; there is a concrete false conclusion
witness in [bridge-context-witness.k](evidence/bridge-context-witness.k):

1. Use intended integer input `1`, hence loop sequence `iCons(49, .IntSeq)`.
2. Ground every cell and bind module-scope `ord` to a real closure that returns
   integer `0`.
3. Under fixed semantics, lexical lookup calls that closure. `0 % 2 == 0`, so
   the loop reaches `even_count = 1`, `odd_count = 0`. The base reachability
   claim closes with exit 0 and `#Top`; see
   [12-bridge-base-witness.log](evidence/12-bridge-base-witness.log).
4. Under the summary definition, the priority bridge skips lookup and the body
   and uses code parity of 49. It proves the opposite state,
   `even_count = 0`, `odd_count = 1`, also with exit 0 and `#Top`; see
   [13-bridge-false-summary.log](evidence/13-bridge-false-summary.log).

Thus the proof extension can establish a result observably false under the
fixed semantics. The number `1` is in the intended input domain, and the
counterexample is in the bridge's express match domain. Although the submitted
entry precondition happens to supply the unshadowed module scope, a globally
false proof rule cannot be justified by calling its bad cases unreachable; the
rule must have been narrowed to the connection theorem's domain. This is a
Gate-A real-program soundness failure and a material proof-rule unsoundness.

## 6. Fresh non-vacuity test

The fresh mutation [spec-vacuity.k](evidence/spec-vacuity.k) adds one to the
even-count component of the entry postcondition. It is demonstrably false at
the satisfying input `N = 0`: the actual and original formal result is `(1, 0)`
while the mutation requires `(2, 0)`.

The mutated spec parses and builds successfully under `--dry-run` with exit 0;
see [17-vacuity-dry-run.log](evidence/17-vacuity-dry-run.log). Actual proof
execution exits 1 with `WarnStuckClaimState`. Its residual explicitly requires

```text
evenDigits(...) +Int 1 #Equals evenDigits(...)
```

and fails the implication check; see
[18-vacuity-proof.log](evidence/18-vacuity-proof.log). This is the expected
unmet result obligation, not a parser/import error, unrelated crash, or
timeout.

The entry theorem is therefore result-constraining and non-vacuous. This test
does not validate the operational bridge that was used to obtain the original
result.

## 7. Proven-versus-assumed accounting

### What the successful K runs establish

The base `#Top` establishes, under the supplied fixed semantics, partial
correctness of the loop summary only in the exact builtins/module/local-scope
configuration stated by `EVEN-ODD-LOOP-SPEC`.

The entry `#Top` establishes closure of the entry claim only under the extended
theory containing the priority bridge. In that theory the call reaches the
tuple of code-parity counts. Because the extended theory contains the
machine-demonstrated false rule above, this closure cannot be promoted to a
sound theorem about execution under the fixed semantics.

Neither reachability result proves termination. The intended execution is a
finite digit loop, but the audited theorem is reported only as partial
correctness.

### Trust ledger

1. **K implementation and mathematical hooks.** `kprove`, the Haskell backend,
   K integer/map/list/string theories, `absInt`, `Int2String`, `ordChar`,
   `substrString`, and integer operations are trusted primitives. They affect
   control and final values. This is the normal low-level trust boundary.
2. **Supplied semantics.** The entire reference semantics is the mode-selected
   trusted language model. The candidate copy is byte-identical. The actual
   program path uses ordinary lookup, call, loop, integer, string, and tuple
   rules; none is proof-local.
3. **Imported but unreachable opaque symbols.** The supplied definition
   declares `md5hexCodes`; float-domain `intFloatDiv`, `divII`, `floatMod`,
   `floatLt`, `absF`, `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`,
   `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
   `truncF`, `roundF`, `roundFN`, and `sqrtF`; and sorting-domain `sortVS` and
   `sortKeyVS` as symbolic/opaque boundaries. The exact declarations appear in
   [K-INVENTORY.md](evidence/K-INVENTORY.md). No submitted construct can reach
   them, so they influence neither target claim nor the counterexample.
4. **Proof-local mathematical functions.** `evenDigits`, `oddDigits`, and
   `lastSeen` are not assumed or opaque; their exhaustive recursive equations
   fix their values.
5. **Program artifact bridge.** Trusted translation gives byte identity between
   `solution.py` and `solution.mpy`. The exact-AST module-load witness gives a
   fixed-semantics connection to the manually encoded entry scope. This is
   machine-supported but remains an auditor reconstruction absent from the
   candidate's provenance records.
6. **Intent bridge.** The formal theorem counts parity of decimal character
   codes. The statement that this equals decimal digit parity relies on
   `Int2String(absInt(N))` yielding ASCII digit codes 48 through 57 and on 48
   being even. This is ordinary mathematics plus the trusted string hook, and
   is independently supported—but not universally proved—by the differential
   test.
7. **Canonical equivalence.** Agreement with `/reference/canonical.py` is
   empirical over 21,942 preserved inputs. It supports the Python-to-intent
   bridge only; it is not a replacement for the K reachability proof.
8. **Candidate operational summary.** The priority-40 loop rule is neither a
   trusted external primitive nor a sound derived theorem over its match
   domain. It directly affects branch results and the final tuple. The exact
   counterexample makes this boundary illegitimate.

### Decision

Clean reconstruction, program fidelity, claim adequacy, and non-vacuity all
pass. Provenance is incomplete. Most importantly, the entry proof relies on a
materially unsound proof-local operational rule that can prove a concrete
false result under the fixed semantics. Per the decision boundary, this is not
a legitimate partial-correctness proof.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
