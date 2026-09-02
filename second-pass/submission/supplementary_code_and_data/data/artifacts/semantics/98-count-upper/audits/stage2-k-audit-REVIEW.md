# Independent adversarial review: 98-count-upper

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed the definitions and proof without candidate caches,
mechanically pinned the entry claim to the trusted-regenerated program, audited
the only proof-local definition, exercised concrete witnesses, and obtained the
expected failure from independent body and postcondition mutations.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`condition: semantics`, and `semantics_mode: SUPPLIED_SEMANTICS`. The required
trusted tree `/reference/reference-semantics` is present, so the mounts do not
contradict the rendered semantics mode.

The independent checks are in
[`evidence/provenance_check.py`](evidence/provenance_check.py) with the complete
bounded transcript in
[`evidence/01-provenance-check.log`](evidence/01-provenance-check.log).
They establish:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and all three trusted source inputs are regular, readable files,
  not symlinks. The trace root is a real readable directory.
- The campaign object in `/audit-input.json` equals
  `/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value.
- Every recorded file hash checked in the log matches: run manifest, task
  manifest, stage-1 result, invocation, metrics, runtime metrics, usage,
  generation prompt, generation last/output, canonical, trusted prompt, and
  translator.
- The mounted candidate tree has the pipeline-v3 digest
  `cd7c02ec1081ac6ac0464582e35aebd7c46a3cf5c5f9e1cdcbcdfc70adbcbce6`,
  matching the stage-1 output workspace digest. The trace tree has digest
  `bc8a7ada1b291f08224d957d17147d3ae28187ed84d9c8cd7a476ca046e9f842`,
  matching `usage.json`; its sole JSONL file has the separately recorded hash
  `f362b1dd0b5f76736a5ad3e495d9eeb52f4c60ef7cae389f18aa5d61dca02beb`.
- All 180 structured-trace lines parse as JSON. The large text records were
  read completely and hashed, not accepted from their summaries. A bounded
  extraction of every recorded call/output and agent message is in
  [`evidence/02-generation-trace-summary.log`](evidence/02-generation-trace-summary.log).
  The records merely claim that generation eventually obtained `#Top`; no
  later audit conclusion relies on that claim.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts. Candidate and trusted `reference-semantics/` have exactly the same 26
  entries, types, lengths, and file hashes. Their pipeline-v3 tree hash is
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  which matches `/task.json`. Neither tree contains a symlink, extra entry,
  missing entry, changed entry, or unsupported type.
- All required candidate proof artifacts (`solution.py`, `solution.mpy`,
  `verification.k`, and `spec.k`) are regular and readable. Candidate-provided
  `runtime-kompiled/`, `verification-kompiled/`, bytecode, logs, and prose were
  excluded from reconstruction.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a Python string `s`, return the number of
characters at zero-based even indices whose value is one of the five uppercase
ASCII vowels `A`, `E`, `I`, `O`, or `U`. The trusted canonical implementation
iterates indices `0, 2, 4, ...` and tests `s[i] in "AEIOU"`.

The submitted implementation scans every character while toggling `even`,
starting from `True`. It increments an integer by the Boolean expression
`even and ch in "AEIOU"`. Thus the tested iterations are exactly indices
`0, 2, 4, ...`; Python's `int += bool` gives the intended integer increment.
This is a different but domain-equivalent algorithm for every Python string.

Using the trusted translator on the scratch copy generated SHA-256
`ba22e092394c5accab36c88258414fa97e71b496a1cfa48ee229d6f5f318d514`
for both regenerated and submitted `solution.mpy`; `cmp` exited 0. The exact
command and status are in
[`evidence/03-translation-identity.log`](evidence/03-translation-identity.log).

The independent differential driver
[`evidence/differential_test.py`](evidence/differential_test.py) separately
imports `/reference/canonical.py` and the scratch `solution.py`. It covers the
three documented examples; empty, one-character, parity, membership, embedded
NUL, and Unicode boundaries; all strings of lengths 0 through 5 over a
seven-symbol branch-covering alphabet; and 5,000 deterministic longer generated
strings. It checked 24,571 distinct strings, required both results to have
exact type `int`, and found zero mismatches. See
[`evidence/04-differential-test.log`](evidence/04-differential-test.log).
This is finite fidelity evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

Only source files were copied to `/tmp/audit-work/98-count-upper`; neither
candidate kompiled directory was copied or referenced. K version 7.1.293 was
available independently.

The concrete definition was built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

It exited 0; see
[`evidence/05-clean-runtime-kompile.log`](evidence/05-clean-runtime-kompile.log).
The warnings concern incomplete totalization in supplied, unused operations
such as float conversion, list helpers, and positional access. None is on this
program's material path. A reviewer-authored MPython test module containing 11
normal and boundary assertions then reached `.K` with empty exception state
and exit code 0. The source and transcript are
[`evidence/audit_concrete_tests.py`](evidence/audit_concrete_tests.py) and
[`evidence/08-clean-concrete-krun.log`](evidence/08-clean-concrete-krun.log).

The proof definition was built with:

```text
kompile verification.k --backend haskell \
  --main-module COUNT-UPPER-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

It exited 0; see
[`evidence/06-clean-verification-kompile.log`](evidence/06-clean-verification-kompile.log).
I then ran the sole positive target command:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module COUNT-UPPER-SPEC
```

It independently checked both claims in the module, printed exactly `#Top`,
and exited 0. See
[`evidence/07-clean-positive-kprove.log`](evidence/07-clean-positive-kprove.log).
The warning diagnostics are unused-variable lint, not stuck states or failed
obligations.

## 4. Adequacy and real-program pinning

### Claim scope

The first claim is a loop invariant. In plain language: from a loop head with
remaining semantic string codes `S`, integer accumulator `ACC`, and parity
flag `EVEN`, executing the exact submitted loop body consumes all of `S` and
changes `count` to `ACC + countUpperFrom(S, EVEN)`. It preserves the framed
scope store and leaves final `even`/`ch` existential because only the count is
needed. There is no explicit `requires` restriction; its displayed exact local
bindings and K sorts are its precondition.

The second claim starts from the ordinary empty module configuration, loads a
literal `Module(FuncDef(...))`, looks up `count_upper`, calls it on an arbitrary
semantic string `str(S:IntSeq)`, and returns `countUpperFrom(S, true)`. It also
requires the heap, stack, return, exception, and exit-code cells to start in
their displayed normal states, and asserts that they are restored after the
call while the exact closure remains in the module scope. Again there is no
extra `requires`. The formal domain is all finite `IntSeq` values, which is
broader than, and therefore contains rather than narrows, the intended domain
of Python strings encoded by their character codes.

### Mechanical pinning and witnesses

[`evidence/pinning_check.py`](evidence/pinning_check.py) extracts the `Module`
inside the entry claim's actual `#loadAll` redex, removes only three explicit
`.Stmts` right-unit spellings that the program parser omits, parses both it and
trusted-regenerated `solution.mpy` through `kast`, and compares the complete
KAST. The terms are equal. See
[`evidence/09-program-pinning.log`](evidence/09-program-pinning.log). This is a
constructor-level comparison of the program actually executed by the claim,
not a comparison to a separate source filename.

Both preconditions are satisfiable. The fresh ground spec
[`evidence/ground-witnesses.k`](evidence/ground-witnesses.k) uses:

- a loop state with `S = "aBCdEf"`, environment location 1, `count = 7`,
  `even = true`, and `ch = ""`; it reaches `count = 8`, `even = true`, and
  `ch = "f"`;
- the exact entry configuration with the same string; it reaches result `1`
  and the stated final cells.

The ground proof printed `#Top` and exited 0
([`evidence/10-ground-witnesses-kprove.log`](evidence/10-ground-witnesses-kprove.log)).
Both trusted canonical Python and submitted Python return `1` for this input,
as independently recorded in the differential run. Thus the concrete
substitution agrees among the claim, program, and oracle.

Body sensitivity was tested separately from postcondition non-vacuity.
[`evidence/spec-body-mutation.k`](evidence/spec-body-mutation.k) changes
`even`'s initialization to `false` in both the module executed by `#loadAll`
and the closure asserted in the post-state, while leaving the original
`countUpperFrom(S, true)` result obligation. `kprove` parsed and executed this
claim but exited 1 with a failed implication on the reachable one-character
branch; for `S = iCons(65, .IntSeq)` (Python string `"A"`), the changed body
returns 0 while the claimed original summary is 1. The residual and exit
status are in
[`evidence/11-body-sensitivity-kprove.log`](evidence/11-body-sensitivity-kprove.log).
The test therefore changes the body actually executed by the theorem.

The entry claim is result-constraining, controls the actual selected binding,
executes every assignment, iteration, membership test, parity update, and
return, and restores all material cells. It is neither a tautology nor an
implication with a free returned value.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`evidence/rule-inventory.tsv`](evidence/rule-inventory.tsv), generated by
[`evidence/rule_inventory.py`](evidence/rule_inventory.py); summary and
coverage check are in
[`evidence/12-rule-inventory-summary.log`](evidence/12-rule-inventory-summary.log).
It inventories every locally declared syntax/function, configuration, context,
rule, and claim across the supplied top-level semantics, all 23 supplied helper
files, `verification.k`, and `spec.k`. Its 933 rows comprise:

- 228 syntax declarations, including 147 declarations with `function`, 108
  with `total`, 25 opaque `symbol` declarations, 22 `no-evaluators`
  declarations, and four macro-bearing declarations; there are no
  `[functional]` declarations;
- one configuration and five evaluation contexts;
- 697 rules, including 45 priority rules, 35 concrete-only rules, 26 `owise`
  rules, and zero simplification rules;
- the two reachability claims, inventoried as obligations rather than assumed
  rewrites.

The lexical declaration count independently equals the inventory count. Every
supplied-semantics row is marked as part of the condition-selected fixed
semantics, not as a candidate justification. The exact candidate/trusted tree
comparison in stage 1 prevents the candidate from changing or adding any such
rule. Opaque float/sort and other supplied symbols appear in the ledger, but
none is reached by this program or its summary.

The material constructor-to-rule mapping is
[`evidence/used-construct-map.md`](evidence/used-construct-map.md). It checks
configuration and cells; statement sequencing; actual function binding; call
frame creation, parameter binding, return, and frame restoration; assignment
strictness; string iteration and loop control; short-circuit evaluation;
membership; integer-plus-Boolean behavior; and parity negation. Evaluation is
left-to-right where it matters, no used operation allocates heap objects, and
the exact entry maps exclude an alternate `count_upper` binding.

The complete proof-local extension inventory is small:

| Extension | Class and domain | State/control footprint | Soundness decision |
|---|---|---|---|
| `countUpperFrom(IntSeq, Bool)` declaration | Definitional summary; all constructor-form `IntSeq` and both Booleans | None; its value affects the invariant and final result only | Sound. It is total over its declared algebraic domain and is not opaque. |
| `countUpperFrom(.IntSeq, _) => 0` | Base equation | None | Sound: an empty suffix contributes zero. |
| `countUpperFrom(iCons(C,REST),EVEN) => indicator + countUpperFrom(REST,notBool EVEN)` | Constructor equation | None | Sound: `strContains(iCons(C,.IntSeq),strToCodes("AEIOU"))` is exactly one-character membership in the five fixed uppercase vowels; recursion strictly descends on `REST` and toggles parity. |

The two equation patterns are disjoint and exhaustive. Their recursive descent
is structural. They do not overlap inconsistently with any supplied equation.
`verification.k` has no rule matching `<k>`, `Module`, `FuncDef`, `Call`,
`For`, `#loop`, return control, a state cell, or another operational term; it
has no priority, simplification, concrete, `owise`, fresh, or opaque rule.
Accordingly `countUpperFrom` names a mathematical value after and alongside
real execution; it does not replace execution and is not an operational bridge
or program-derived oracle. No bridge-free connection theorem is needed for an
operation that is not bridged—the loop and entry reachability proofs themselves
establish the connection through fixed execution.

By induction on `S`, the summary counts exactly those offsets whose current
parity is true and whose code is in `{65,69,73,79,85}`. Starting with `true`
therefore counts precisely zero-based even indices. This is ordinary
mathematics, and it is consistent with all independent differential and ground
evidence. No task-answer rule, fabricated result, unconstrained abstraction, or
used unmodeled construct was found. I therefore make no unsound-rule allegation
requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not reuse a candidate mutation. The fresh mutation
[`evidence/spec-false-postcondition.k`](evidence/spec-false-postcondition.k)
keeps the exact original executed module and state but changes the result to
`countUpperFrom(S, true) +Int 1`. The standard entry state with the empty string
is a satisfying counterexample: both Python implementations and the true K
summary return 0, while the mutation demands 1.

The command was:

```text
kprove spec-false-postcondition.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-POSTCONDITION
```

It built/parses successfully, reached the relevant final state, and failed for
the expected unmet obligation with `S = .IntSeq`; `kprove` exited 1 and emitted
`WarnStuckClaimState`, not a parser error, timeout, missing import, or unrelated
crash. See
[`evidence/13-false-postcondition-kprove.log`](evidence/13-false-postcondition-kprove.log).
The positive proof is therefore discriminating and non-vacuous.

## 7. Proven versus assumed accounting

What is formally established is partial correctness under the supplied
semantics: for every finite semantic character-code sequence `S`, if execution
of the exact trusted-regenerated `count_upper` module from the stated normal
configuration terminates, its returned value is `countUpperFrom(S, true)`, with
the asserted module binding and control/state cells. The generic loop claim
establishes the corresponding accumulator relation for every suffix, starting
integer, and parity Boolean.

The ordinary structural induction above identifies that recursive result with
the source contract's number of uppercase ASCII vowels at even indices. There
is no finite-size restriction, bounded unrolling, examples-only precondition,
or exception that removes part of the intended Python-string domain.

The trust ledger is:

- **K implementation and backends.** `kompile`, LLVM execution, Haskell
  symbolic execution, `kprove`, SMT/builtin arithmetic, maps, Booleans, and
  strings are the normal low-level trusted computing base. They affect all
  claims and are acceptable for a K proof.
- **Supplied semantics.** The launcher-selected reference semantics is a fixed
  trust boundary for this condition. Its entire candidate copy is
  byte-identical to the trusted mount. The audit nevertheless checked the
  complete local inventory and every rule on the material path. Supplied
  opaque symbols and compiler totality warnings are outside the path and have
  no dependent claim here.
- **Translator/program identity.** `/reference/py2mpy.py` is trusted by the
  benchmark. Byte-identical regeneration and KAST equality connect
  `solution.py`, submitted `solution.mpy`, and the term executed by the entry
  claim. This bridge is mechanical rather than empirical.
- **String representation.** The theorem uses `str(IntSeq)` as the supplied
  semantic representation of Python strings. Mapping Python characters to
  sequence entries is the intended fixed-semantics representation; the formal
  theorem is actually broader because it allows arbitrary integer entries.
  The program only compares against fixed ASCII vowel codes, so non-ASCII
  entries correctly contribute zero. Unicode, combining, NUL, and longer cases
  were also checked differentially. The tests support this bridge finitely;
  the rule-level argument supplies the general justification.
- **Mathematical summary.** `countUpperFrom` is fully defined by truthful,
  exhaustive, descending equations. It is neither assumed nor opaque. The
  informal induction connecting it to the English phrase “even indices” is
  direct and does not narrow the theorem.
- **Termination.** The requested and Kit status is partial correctness; the
  proof does not claim a separate total-correctness theorem. This is not an
  adequacy defect. On the intended finite-string domain, the fixed loop and the
  summary both structurally consume one character per iteration.
- **Empirical evidence.** Concrete K execution, 24,571 differential inputs,
  ground claims, and both mutations validate fidelity and sensitivity only.
  None is used as a substitute for the positive reachability proof.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C (trust and
evidence auditability) all pass. The proof is sound, result-constraining, pins
the real translated program, and covers the full material source-contract
domain without a material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
