# Independent adversarial audit: 94-skjkasdkd

## Executive finding

The candidate contains a legitimate, result-constraining partial-correctness
proof under its generated semantics. I rebuilt both definitions from source,
ran the original complete target spec, obtained `#Top` with exit status 0,
mechanically matched the proof's program macro to the trusted regeneration of
`solution.mpy`, reviewed every local declaration and rule, changed the executed
program body and observed proof failure, and separately changed the
postcondition and observed the expected unmet obligation.

The result is not an unqualified `PASS`. The generated semantics is an
idealized unbounded-stack subset of Python, while the concrete recursive
`solution.py` can raise `RecursionError` on an unrestricted integer input; the
fresh witness `[1000003]` does so. The local `and` rules also evaluate the right
operand after a false left operand, unlike Python short-circuiting, although
the only submitted right operand is a pure, total integer comparison and no
wrong result, state, control, or exception witness exists on the intended
integer-list domain. Finally, the trusted canonical treats `1` as prime when
there is no genuine prime, whereas the candidate follows the natural-language
prime contract. These are visible trust/intent limitations, not proof
shortcuts or domain narrowing. They justify `CONCERNS / LEGIT`.

## 1. Input and provenance integrity

### Declared layout and semantics boundary

`/audit-input.json` declares:

- problem `94-skjkasdkd`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- `mount_reference_semantics: false`.

The trusted `/reference/reference-semantics` tree is absent, as this mode
requires. The candidate also has no `reference-semantics` tree. I did not
search for or use any hidden fixed semantics.

The launcher-declared candidate, canonical, prompt, translator, manifests,
generation files, and trace mounts all exist and are readable. None of the
required records or candidate source artifacts is a symlink. The candidate
tree has nine regular files: the eight source/deliverable files and one Python
bytecode cache. No candidate-built K definition was used.

Evidence:

- full mount/type inventory:
  `/audit-output/evidence/stage1/mount_inventory.log`;
- required-record inventory:
  `/audit-output/evidence/stage1/required_record_inventory.log`;
- candidate leaf hashes:
  `/audit-output/evidence/stage1/candidate_file_hashes.log`.

### Campaign lock and byte hashes

The parsed `/audit-campaign-lock.json` is exactly equal to the
`audit_campaign` object in `/audit-input.json`. Its observed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the recorded hash.

All independently computed launcher-declared file hashes matched:

| Artifact | Observed and recorded SHA-256 |
|---|---|
| trusted canonical | `d1dd5909bcdd2600d7171948865387fc85a1592dbb57baae6e7dd90e93b22daa` |
| trusted and candidate prompt | `1c6ca165f1b5548225ce755ffb9fe188813105f3eac8cfb3f515326db7f25812` |
| trusted and candidate translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| run manifest | `16ab5496e5b7251ecd747d4b58693a614cb2f6d680317214f597d0437ab39c24` |
| task manifest | `2299bc0a6f67153b68f57a5de998da571902d639603b8be1e10eb631444229c9` |
| stage-1 result | `5d3265c374decff4a0f4d2e5baad3c3b2133bff1645ad4963e5344fbf863e56f` |
| invocation | `b9282ca0102111741bc6609e9859d838dadab11badaad175c27f36895e776ec2` |
| metrics | `89518140f6f9d126ed8e89ccf3f9af3cdbd578bc8be0b6ecb96d9d7363e6815e` |
| usage | `019c1fdc057eee6b64833bff8c3eceeeb7710ba6638b9c65d70a00280c80bef1` |
| generation prompt | `4fbd8d83152646045c82c9b1c86a3c0c9bf686de949fcbf8c3eff6755a261d9e` |
| Codex last message | `5b9d939857f9e872275243bfb53eb053f04a456ccdfc6123064f86111dee4dfb` |
| Codex output log | `734ee4d8c4ec1107b9b55333272c779a9d1840b9eaa2e28bdc0d09dd8c179d0b` |

`prompt.py` and `py2mpy.py` are also byte-identical between candidate and
trusted mounts, not merely hash-equal.

The audit manifest's aggregate tree hashes use a launcher-side aggregation
scheme not exposed as a command in this legacy image. As an independent
cross-check, the installed pipeline tree hasher produces
`ad566e366862220de8386f859ae9da6d2eceb2ac23c2b52bfee9d1eed2b1d550`
for `/candidate`, exactly matching all three stage-1 records
`invocation.inputs.workspace_sha256`,
`invocation.outputs.workspace_sha256`, and
`generation-result.outputs.workspace_sha256`. It produces
`02e0a4a622ab2a5497e0270b185898909dfcab87aa3bb4bdf7706470d5dd489b`
for the trace tree, exactly matching `usage.json`'s
`source_trace_sha256`. The sole trace file itself hashes to
`d0de0db352c89abf6468dba6a76216e46518150f1a263f78b48b6f02e1567f6f`,
matching the invocation and generation result. Thus the independently mounted
leaf content and two independent provenance aggregates agree; there is no
mount-integrity breach. The exploratory comparison with the different
installed aggregate is preserved in
`/audit-output/evidence/stage1/tree_hash_check.log` so it cannot be mistaken
for a leaf hash comparison.

The complete hash checks are in
`/audit-output/evidence/stage1/integrity_check.log` and
`generation_declared_hashes.log`.

### Required legacy-selected generation records

I read `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the structured trace. Runtime metrics are
not a required historical record for this layout and were not reconstructed.

The trace has 294 valid JSON lines and zero malformed lines: one session
record, 86 event messages, 205 response items, one world state, and one turn
context. It contains 51 tool calls and their outputs and ends in the claimed
successful generation result. The 28,246-line Codex output log and structured
trace were treated only as untrusted records of what the generator claimed to
do. I did not rely on their earlier `#Top`.

Evidence:

- `/audit-output/evidence/stage1/required_records.log`;
- `/audit-output/evidence/stage1/trace_summary.log`;
- `/audit-output/evidence/stage1/generation_log_summary.log`.

No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt says: given a list of integers, find the largest prime value
and return the sum of its decimal digits. It gives six examples. It does not
state what to do if there is no prime.

The trusted canonical scans the list from `maxx = 0`, uses trial division, and
digit-sums `maxx`. Its helper omits the usual `n < 2` check, so `isPrime(1)`
returns true. Consequently, on a no-genuine-prime list containing `1`, the
canonical returns `1`. That behavior conflicts with the natural-language use
of “prime”; it is not evidence that `1` is mathematically prime.

The candidate implements:

1. exact recursive trial division from divisor 2;
2. a structural list fold selecting the greatest genuine prime, with base 0;
3. recursive decimal digit sum;
4. their composition at `skjkasdkd`.

This is a different but contract-faithful algorithm for lists on which a
largest genuine prime exists, and it defines the no-prime case as 0.

### Trusted regeneration

I ran:

```text
cd /tmp/audit-work/candidate-clean
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

The command exited 0. Both files have SHA-256
`a537d17594c25efbe49fe5a6a69f79faa6e23d4445c269e483dafb5ec4eb678e`.
Evidence: `/audit-output/evidence/stage2/regenerate_translation.log`.

### Independent differential

`/audit-output/evidence/stage2/differential_test.py` independently imports the
trusted canonical and the scratch candidate. Its third oracle is an iterative
implementation using `math.isqrt`; it shares neither the candidate recursion
nor the K reference equations.

The exact scope was:

- all six prompt examples;
- 17 curated empty, negative, no-prime, prime/composite-boundary, duplicate,
  multi-digit, and recursion-boundary cases;
- all 4,369 lists of lengths 0 through 3 over
  `[-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12]`;
- 1,000 deterministic random lists, seed `940026`, lengths 0 through 30,
  values -100 through 1000.

Results over 5,392 executions:

- all six examples passed in candidate and canonical;
- candidate versus the independent contract oracle: one mismatch;
- canonical versus the contract oracle: 357 mismatches;
- candidate versus canonical: 358 mismatches.

The 357 canonical/contract mismatches are exactly the `1` issue on lists with
no genuine prime. The candidate's sole contract-oracle mismatch is
`[1000003]`: the candidate raises Python `RecursionError`, while the iterative
oracle and canonical return 4. This is termination/resource evidence, not a
wrong value returned by a normally terminating candidate call. Partial
correctness does not prove termination, but the generated semantics' failure
to model the observable exception remains a trust limitation.

Evidence and complete first-mismatch records:
`/audit-output/evidence/stage2/differential_test.log`.

Judgment: there is no result divergence where the candidate returns normally
and the natural-language largest-genuine-prime result is defined. The
canonical's behavior on `1` exposes an underspecified/buggy no-prime boundary,
so it contributes to `CONCERNS`; it does not show that the proof substitutes a
different body or narrows the proof to finitely many cases.

## 3. Clean proof reconstruction

I copied only these sources into `/tmp/audit-work/candidate-clean`:
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. I copied no K kompiled directory
and used no candidate cache.

The observed tools were K `v7.1.293` for `kompile`, `krun`, and `kprove`, and
Python 3.10.12. Evidence:
`/audit-output/evidence/stage3/tool_versions.log`.

### Fresh builds and target proof

The fresh concrete definition command was:

```text
kompile semantic.k --backend haskell \
  --syntax-module MPY-SYNTAX --main-module SEMANTIC \
  --output-definition audit-semantic-kompiled
```

It exited 0. Evidence:
`/audit-output/evidence/stage3/kompile_semantic.log`.

The fresh proof definition command was:

```text
kompile verification.k --backend haskell \
  --syntax-module MPY-SYNTAX --main-module VERIFICATION \
  --output-definition audit-verification-kompiled
```

It exited 0. Evidence:
`/audit-output/evidence/stage3/kompile_verification.log`.

The candidate's complete positive target was then run independently:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

Actual bounded output:

```text
#Top
EXIT_STATUS: 0
```

Evidence: `/audit-output/evidence/stage3/kprove_all_claims.log`.

The spec contains six claims and the command proves the complete mutually
supporting claim set. I also made a semantically identical labeled copy.
The recursive `prime-from` claim independently prints `#Top` when selected
alone. A diagnostic that selected the dependent `prime` claim while filtering
out its supporting claim no longer represented the complete target theory and
did not complete promptly; I interrupted that diagnostic. It is not counted
as a target failure. The preserved records are
`kprove_labeled_prime_from.log` and `kprove_each_claim.log`.

### Fresh concrete generated-semantics execution

The corrected reviewer script ran nine cases through both scratch
`solution.py` and scratch-built `krun`:

| Input class | Input | Python / K result |
|---|---|---|
| empty | `[]` | 0 / 0 |
| one is not prime | `[1]` | 0 / 0 |
| smallest prime | `[2]` | 2 / 2 |
| composites only | `[4,6,8,9]` | 0 / 0 |
| negative plus prime | `[-3,11]` | 2 / 2 |
| repeated prime | `[7,7]` | 7 / 7 |
| prompt boundary | `[0,8,1,2,1,7]` | 7 / 7 |
| multi-digit choice | `[181,32,109]` | 10 / 10 |
| larger prime | `[104729]` | 23 / 23 |

Every `krun` ended with `.K`, the exact expected `result(intVal(...))`, and
exit status 0. Evidence:
`/audit-output/evidence/stage3/concrete_semantics_compare_corrected.log`.

The first reviewer attempt wrote the empty variadic list as `listVal(.Vals)`,
which is not concrete input syntax; that parser error is preserved in
`concrete_semantics_compare.log`. It was corrected to `listVal()`. It is not
proof or non-vacuity evidence.

## 4. Adequacy and real-program pinning

### Plain-language claims

The six entry claims state:

1. For `N >= 2` and `D >= 2`, invoking the real
   `is_prime_from(N,D)` body returns the Boolean described by testing divisors
   from `D` upward.
2. For every K integer `N`, invoking the real `is_prime(N)` body returns false
   below 2 and otherwise the divisor-search result from 2.
3. For all K integers `N` and `BEST`, invoking the real
   `choose_prime(N,BEST)` body returns `N` exactly when `N` is prime and
   greater than `BEST`; otherwise it returns `BEST`.
4. For every K value list `VS`, invoking the real
   `largest_prime(listVal(VS))` body returns its structural reference fold.
   On the source-contract subtype, every element is `intVal`.
5. For every K integer `N`, invoking the real `digit_sum(N)` body returns the
   recursive reference digit sum.
6. For every `VS`, executing
   `init(solutionProgram,listVal(VS))` consumes `<k>` to `.K` and changes
   `<result>` from `noResult` to exactly
   `result(intVal(refAnswer(VS)))`.

The first five claims intentionally frame and preserve `_R:Result`; helper
execution does not run `finish`. The sixth claim does not leave the observable
result free: it requires one exact value. The configuration contains no heap,
I/O, allocation, global-state, or exception cell that could be silently
omitted.

### Mechanical program identity

I used the freshly compiled definition and K's parser/macro expander:

```text
kast solution.mpy --definition audit-verification-kompiled \
  --module VERIFICATION --sort Pgm --output json --expand-macros
kast --expression solutionProgram \
  --definition audit-verification-kompiled \
  --module VERIFICATION --sort Pgm --output json --expand-macros
cmp ...
```

The two expanded JSON terms are byte-identical, each SHA-256
`b2bfadf33abe5c012085bee2638a6201dd2feff6d6c473349c45fb46ea5f90e0`.
Evidence:

- `/audit-output/evidence/stage4/program_term_identity.log`;
- `/audit-output/evidence/stage4/parsed-solution.json`;
- `/audit-output/evidence/stage4/expanded-macro.json`.

`solutionDefs` reduces to `programDefs(solutionProgram)`, and `programDefs`
reduces to `collectDefs` of the exact module statements. Calls therefore look
up and execute the actual six function bindings and bodies. No rule rewrites a
program call to `refAnswer` or another result oracle.

The manually duplicated macro is an artifact-maintenance risk for future
edits, but trusted regeneration plus the constructor-level comparison pins
this immutable candidate exactly.

### Satisfiable states and concrete substitutions

Every precondition is satisfiable. The preserved witnesses are:

| Claim | Witness | Candidate helper / reference |
|---|---|---|
| `is_prime_from` | `N=2,D=2` | `true / true` |
| `is_prime` | `N=1` | `false / false` |
| `choose_prime` | `N=7,BEST=5` | `7 / 7` |
| `largest_prime` | `[4,7]` | `7 / 7` |
| `digit_sum` | `181` | `10 / 10` |
| entry | `[0,8,1,2,1,7]` | reference/candidate/canonical `7/7/7` |

An additional entry substitution `[181,32,109]` gives
reference/candidate/canonical `10/10/10`.

Evidence:
`/audit-output/evidence/stage4/ground_witnesses.py` and
`ground_witnesses.log`.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
`/audit-output/evidence/stage5/rule_review.md`. It enumerates every local syntax
production and attribute, all 12 semantic helper equations, all 36 operational
rules, all 15 verification equations/macros, and all six claims, with an
individual decision and source line for each. A raw declaration/rule index is
in `local_declaration_inventory.log`.

### Inventory summary

- Local syntax covers exactly `Module`, `FuncDef`, `Return`, `If`,
  parameters/statements, integer/Boolean/name expressions, the four used
  binary operators, three comparisons, Boolean `and`, named calls, index 0,
  and slice `1:`.
- Runtime values are integers, Booleans, and lists. Internal continuation
  frames make left-to-right evaluation and calls explicit.
- The configuration is only `<k>` plus `<result>`, which is sufficient for
  this pure program.
- Verification adds two exact program macros and six transparent mathematical
  functions.
- There are no local simplification rules, priority rules, `[concrete]` rules,
  `[functional]` declarations, fresh values, opaque symbols, or
  uninterpreted result-bearing abstractions.
- The only `[total]` declarations are `refPrimeFrom` and `refPrime`.

Every constructor actually present in `solution.mpy` is mapped in the
inventory's construct-to-rule table. There is no default rule that fabricates
a value for an unmodeled used construct.

### Calls, state, control, and equations

The call path is:

```text
init
  -> invokeProgram
  -> collect exact definitions / invoke "skjkasdkd"
  -> lookup exact def / bind exact parameters
  -> execute exact statements
  -> evaluate exact return expression and nested calls
  -> finish / write exact result
```

The semantics uses `<k>` continuations as the call stack. Caller environments
and pending operations are stored in explicit frames. `Return` discards the
remaining statements of that function while preserving the caller
continuation. `If` evaluates its Boolean first and selects exactly one branch.
Arguments and binary/comparison operands are evaluated left to right. All
function names are present and unique; `len` is handled by a disjoint builtin
rule. All arities match. Subscript and slice rules are guarded by the preceding
length branch. There is no allocation or state change beyond the final result.

The reference equations are transparent and guarded:

- `refPrimeFrom` increases the divisor until a factor or square-root boundary;
- `refPrime` starts at 2;
- `refChoose` has disjoint complementary guards;
- `refLargest` decreases list length;
- `refDigitSum` decreases a nonnegative decimal quotient;
- `refAnswer` composes the last two.

For integer lists, these equations define 0 when there is no prime, otherwise
the maximum prime, followed by its decimal digit sum. That natural-language
interpretation follows by ordinary induction on divisor, list length, and
decimal quotient. The reachability proof formally connects program execution
to the equations; the final “these equations mean prime maximum and digit sum”
sentence is a transparent mathematical interpretation, not a second hidden K
theorem.

### Scoped limitations, not unsound shortcuts

1. **Python short-circuit control.** Operational rule O24 evaluates the right
   operand of `and` even after a false left operand. A reachable example is
   `choose_prime(4,0)`: Python skips `4 > 0`, while K evaluates it. The right
   operand in the submitted program is always that pure, total integer
   comparison; both executions return `0`, touch no state, and cannot throw on
   the source-contract type. Because there is no concrete or symbolic false
   result/state/control conclusion on the intended domain, I do not label the
   rule materially unsound. It is a narrower semantic-fidelity gap and one
   reason for `CONCERNS`.

2. **Division and modulo scope.** K `/Int` is not a full Python-floor-division
   model for arbitrary negative operands. The only reachable division is a
   nonnegative digit sum divided by positive 10; prime modulo has positive
   `N` and divisor. Thus the equations are sound on every submitted use.

3. **Over-broad total annotation.** `refPrimeFrom` is declared total over all
   `Int,Int`, but its equations do not usefully cover `D=0` with nonnegative
   `N` because modulo zero is undefined. Every claim use has `D>=2`, or starts
   at 2 through `refPrime`; coverage and descent are complete there. The
   over-declaration neither replaces execution nor enables a wrong result on
   an integer-list entry state. It is an unused global-theory cleanliness
   limitation.

4. **Resource exceptions.** The K model has mathematical recursion and no
   CPython recursion-limit cell. The `[1000003]` differential witness is a
   real boundary where abstract K/Python mathematics yields 4 but CPython
   `solution.py` raises `RecursionError`. This is an explicit trust boundary of
   the generated language model. It does not narrow the formal claim to a
   finite size; it prevents interpreting the theorem as total correctness or
   exact resource-bounded CPython behavior.

The corrected `--warnings all` compilation exited 0. Its only warning was that
the `<mpy>` symbol appeared unused while compiling the definition without a
spec. The earlier `-W all` invocation used the wrong CLI option and is
preserved separately; it is not a definition error. Evidence:
`kompile_lint_all.log` and `kompile_lint_all_corrected.log`.

### Body sensitivity

I made a distinct operational mutation: in the exact program macro, the
submitted entry body

```text
return digit_sum(largest_prime(lst))
```

was changed to `return 0`. The mutated program term has SHA-256
`cb457ad13370f93bec5e2ecf23d8016f24a3ac46e21cc1ed3bd503edd49f8486`,
different from the real term's
`b2bfadf33abe5c012085bee2638a6201dd2feff6d6c473349c45fb46ea5f90e0`.
The mutated definition compiled successfully. Its proof failed with
`WarnStuckClaimState`, final result `0`, and unmet equality
`0 == refDigitSum(refLargest(VS))`.

This mutation changes the term actually executed by the claim, rather than
only changing external `solution.py`. It demonstrates body sensitivity and
that no reference function bypasses entry-body execution.

Evidence:

- `/audit-output/evidence/stage5/verification-body-mut.k`;
- `/audit-output/evidence/stage5/spec-body-mut.k`;
- `/audit-output/evidence/stage5/body_mutation_term_difference.log`;
- `/audit-output/evidence/stage5/kprove_body_mutation_expected_failure.log`.

No materially unsound local rule was identified. Accordingly, there is no
unsupported “unsound” label lacking the false-conclusion witness required by
the audit prompt.

## 6. Fresh non-vacuity test

I did not rely on a candidate mutation file; none was submitted. The fresh
reviewer mutation preserved the exact program and helper claims and changed
only the entry result obligation from:

```text
result(intVal(refAnswer(VS)))
```

to:

```text
result(intVal(refAnswer(VS) +Int 1))
```

The mutation is preserved at
`/audit-output/evidence/stage6/spec-vacuity-fresh.k`.

A `kprove --dry-run` parsed and built the mutation successfully with exit
status 0:

```text
kprove spec-vacuity-fresh.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Evidence: `mutation_dry_run.log`.

The state `VS = intVal(2)` satisfies the entry precondition (there is no
`requires`). The real program and original reference result are 2; the
mutation demands 3. Evidence: `mutation_witness.log`.

The actual proof command was:

```text
kprove spec-vacuity-fresh.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`. The residual final configuration has
the real exact result:

```text
result ( intVal ( refDigitSum ( refLargest ( VS ) ) ) )
```

and the failed implication contains:

```text
refDigitSum(refLargest(VS)) +Int 1
  == refDigitSum(refLargest(VS))
```

This is the expected reachable unmet result obligation, not a parser error,
timeout, or unrelated crash. Evidence:
`/audit-output/evidence/stage6/kprove_false_post_expected_failure.log`.

The proof is non-vacuous and discriminates a false result.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the freshly built `VERIFICATION` definition, the six
partial-correctness reachability claims close. In particular, for every finite
K `VS:Vals`, every covered execution of the exact constructor term parsed from
the trusted regeneration of `solution.mpy` that terminates normally at
`finish` has `.K` and:

```text
result(intVal(refAnswer(VS)))
```

The helper claims establish the exact results of the five real helper bodies
in the contexts stated in `spec.k`. For source-contract integer lists,
`refAnswer` transparently denotes the digit sum of the greatest integer at
least 2 with no divisor from 2 through its square root, or 0 when none exists.
There is no fixed-length bound or example-only precondition.

This is a partial-correctness result under the selected generated semantics.
It is not a total-correctness theorem, a CPython stack/resource theorem, or a
theorem that the trusted canonical's `1` behavior is mathematically correct.

### Trust ledger

| Boundary | Effect and dependents | Judgment |
|---|---|---|
| K compiler, Haskell backend, `kprove`, and proof kernel implementation | All machine-checked closure depends on the toolchain behaving correctly. | Ordinary unavoidable trusted computing base; version and clean commands recorded. |
| Standard `domains.md` `INT`, `BOOL`, `STRING`, and `MAP` definitions | Supplies unbounded arithmetic, Booleans, strings, finite maps, and their hooks. | Acceptable low-level standard-library boundary; no task answer is encoded there. |
| Trusted `py2mpy.py` | Connects Python AST to `solution.mpy`. | Byte identity was independently regenerated; acceptable. |
| Manual `solutionProgram` macro | Connects spec text to the submitted constructor program. | Mechanically expanded and byte-compared; exact for this immutable candidate. Future maintenance is informal, current pinning is not. |
| Locally generated Python-subset semantics | Defines calls, returns, expressions, lists, and results used by the theorem. | Exhaustively audited and concretely checked. It has no answer oracle. The short-circuit and resource idealizations are explicit concerns. |
| Transparent `ref*` equations | State the mathematical result used in helper and final postconditions. | Equations are inspected, guarded, descending on proof uses, and independently differentially supported. No opaque value remains. |
| Mathematical interpretation of `ref*` as prime maximum/digit sum | Human-facing meaning of the equations. | Ordinary inductive reasoning; not replaced by differential testing. |
| Differential testing | Supports implementation/semantics/intent bridges on 5,392 Python cases and nine K cases. | Finite evidence only; it is not used as the universal K proof. |
| CPython recursion/resource behavior | Affects termination/exception behavior, witnessed by `[1000003]`. | Excluded from the abstract theorem; nonfatal for partial correctness but material enough to prevent an unqualified pass. |
| Trusted canonical no-prime behavior | Canonical returns 1 on no-genuine-prime lists containing 1. | Conflicts with the natural-language definition of prime and exposes an underspecified boundary. Reported as a concern, not silently assumed. |

### Gate decisions and final mapping

- **Dynamic reconstruction:** PASS. Both definitions were rebuilt; the complete
  positive spec printed `#Top` and exited 0.
- **Gate A, real-program soundness:** PASS. The exact body executes, reference
  functions are transparent, the result is constrained, body sensitivity
  holds, and the fresh false postcondition fails for the right reason.
- **Gate B, intent adequacy:** PASS with a documented boundary concern. The
  theorem covers arbitrary finite integer lists under the abstract semantics,
  not finite examples or fixed sizes, and implements genuine mathematical
  primality. The no-prime/canonical `1` behavior is underspecified and the
  resource model is idealized.
- **Gate C, trust/evidence:** PASS with documented limitations. All audit
  artifacts and exact commands exist; finite evidence is kept separate from
  universal proof.

The benchmark's `FAIL / NOT_LEGIT` conditions do not apply: the proof is not
missing, bounded, vacuous, result-free, source-substituted, or dependent on a
materially false task-answer rule. The nonfatal generated-semantics and
canonical-boundary limitations rule out an unqualified `PASS`, yielding the
valid pairing below.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
