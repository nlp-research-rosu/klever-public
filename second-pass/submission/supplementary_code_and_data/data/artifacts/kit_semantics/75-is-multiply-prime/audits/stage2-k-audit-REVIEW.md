# Independent adversarial review: 75-is-multiply-prime

This review independently reconstructs the candidate under
`SUPPLIED_SEMANTICS`. Candidate prose, logs, traces, compiled definitions, and
the prior `#Top` were not treated as authority. All executable work used a
scratch copy at `/tmp/audit-work/75-audit-vYfTjU`; no candidate cache or
compiled definition was copied or reused.

## 1. Input and provenance integrity

Result: **PASS; no infrastructure breach**.

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem
`75-is-multiply-prime`, and condition `kit-semantics`. The launcher-declared
container paths exist and are readable. The required pipeline-v3 records were
all present as regular, non-symlinked files:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- generation `invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured JSONL trace below `codex-trace/`.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All 16 independently checked launcher hashes match: campaign lock, canonical,
trusted/candidate prompt and translator, run/task/result/invocation manifests,
all metrics and usage records, generation last/output/prompt, and the trace.
The trace is valid JSONL with 208 records and SHA-256
`f9f5bc50cf461f7e52c2965d00a2d69562910d23df8dd8192cc13278aa1af73f`.
The generation records were inspected only as historical claims.

The trusted `/reference/reference-semantics` tree required by this mode is
present. Recursive comparison against
`/candidate/reference-semantics` found the same 24 regular files and one
directory, with no missing, additional, changed, mistyped, or symlinked entry.
A reviewer-defined path/type/content digest is
`7747bea6461b1dd77450f771c2dbe99fdba12d588c66360180e25983ad67ccf2`
for both trees. Candidate `prompt.py` and `py2mpy.py` are byte-identical to
their trusted mounts. The required candidate proof artifacts are regular,
readable files. Candidate-provided `runtime-kompiled` and
`verification-kompiled` were deliberately ignored.

Evidence: `evidence/provenance_check.py`,
`evidence/provenance-integrity.log`, and `evidence/COMMANDS.md`.

## 2. Program fidelity and candidate-versus-canonical checks

Result: **PASS**.

The trusted prompt asks for `is_multiply_prime(a)` to return true exactly when
integer `a`, known to be less than 100, is a product of three prime numbers.
The trusted canonical implementation allows repeated primes, so, for example,
`8 = 2 * 2 * 2` qualifies. Products of primes are positive; nonpositive and
negative integers therefore return false.

`solution.py` preserves the entry signature and implements a loop-free
22-value disjunction:

```text
8, 12, 18, 20, 27, 28, 30, 42, 44, 45, 50,
52, 63, 66, 68, 70, 75, 76, 78, 92, 98, 99
```

Fresh translation with the trusted translator:

```bash
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

returned `0` for both commands. Both files have SHA-256
`2ed20f37c9f9cc534ea932248a2599788f3e6de80cc7303669d627aef0439709`.

The reviewer-authored differential test imports the trusted canonical and
candidate entry points independently. It checked:

- the documented example `30`;
- every nonnegative input `0..99`, which includes every true branch and both
  adjacent boundaries where they remain below 100;
- explicit negative boundaries and large-magnitude negatives;
- 24 deterministic randomly generated negative integers.

All 134 inputs agreed in both Boolean value and type; mismatch count was zero.
This is finite evidence rather than a substitute for the K proof.

Evidence: `evidence/differential_test.py`,
`evidence/differential-test.log`, and
`evidence/translation-fidelity.log`.

## 3. Clean proof reconstruction

Result: **PASS**.

Only candidate source artifacts and trusted mounted inputs were copied into
scratch. Fresh definitions were built with K `v7.1.293`.

The concrete definition was rebuilt:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited `0`. Fresh `krun` of `solution.mpy` exited `0` with final `.K`,
`NoExc`, and exit code `0`. A reviewer-authored driver called the exact
function on `30, 8, 99, 7, 9, 97, 0, -1000000`; all assertions passed and it
also ended with `.K`, `NoExc`, and exit code `0`.

The proof definition was rebuilt:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited `0`. Static enumeration finds exactly one positive target claim. Its
independent proof command was:

```bash
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.is-multiply-prime
```

It printed `#Top` and exited `0`.

The compiler warnings concern unused variables in supplied `str.k` and
non-exhaustive total functions in LLVM-only/off-path domains such as float,
method, builtin, and subscript support. None is reachable from this program,
and the same warnings do not prevent either clean build.

Evidence: `evidence/fresh-llvm-build.log`,
`evidence/fresh-krun-solution.log`,
`evidence/fresh-krun-driver.log`,
`evidence/concrete_driver.py`,
`evidence/fresh-haskell-build.log`, and
`evidence/fresh-positive-proof.log`.

## 4. Adequacy and real-program pinning

Result: **PASS**.

The sole entry claim has the following plain-language meaning:

- **Precondition:** `A` is a K integer and `A < 100`, in the ordinary initial
  module configuration with empty module scope/heap/stack, normal
  return/exception state, and exit code zero.
- **Execution:** load a module defining `is_multiply_prime(a)` with the
  submitted body, resolve that binding, and call it on symbolic `A`.
- **Postcondition:** the returned value in `<k>` is exactly the explicit
  22-way Boolean disjunction above. The module function binding is retained;
  the callee frame is gone; environment, allocators, empty heap/stack,
  return/exception state, and exit code are all constrained.

The claim is not keyed only by a function name. A mechanical balanced-term
comparison found that the first `Module(...)` under the claim's `#loadAll` is
constructor-for-constructor identical to the freshly regenerated
`solution.mpy`, ignoring whitespace. The subsequent term is exactly
`Call(Name("is_multiply_prime"), (A:Int, .Exprs))`. Thus ordinary definition
binding, lookup, parameter binding, all 22 comparisons, short-circuit control,
return, and frame cleanup execute under the supplied semantics. There are no
helper or loop claims.

The precondition is satisfiable. Substitution checks give:

| `A` | Formal result | Canonical | Candidate |
|---:|---:|---:|---:|
| 30 | true | true | true |
| 16 | false | false | false |
| 99 | true | true | true |
| -1 | false | false | false |
| `-10^30` | false | false | false |

All witnesses satisfy `A < 100`. The returned value is not a free variable,
tautology, or implication-only condition.

An independent prime predicate and triple enumeration produces exactly the
same 22 products below 100, with no extra or missing claim value. Because all
primes are at least two, factors in any product below 100 are themselves below
100; the enumeration is exhaustive. Negative integers cannot be products of
positive primes. This connects the finite formal result to the source
contract without narrowing its domain.

Evidence: `evidence/claim_pinning_check.py`,
`evidence/claim-pinning.log`,
`evidence/contract_set_check.py`, and
`evidence/contract-set-check.log`.

## 5. Rule-by-rule static soundness review

Result: **PASS**.

The complete line-addressed inventory covers `semantics.k`, every supplied
helper K file, `verification.k`, and `spec.k`: 227 syntax declarations, one
configuration, five contexts, 695 rules, and one claim, for 929 items. It
enumerates 145 function, 107 total, 45 priority, 26 owise, 35 concrete, 25
symbol, 22 no-evaluator, four macro, one macro-rec, two strict, and one
seqstrict attributes. There are no local `functional`, `simplification`, or
`anywhere` items.

Every item has an explicit disposition in
`evidence/classified-k-inventory.tsv`:

- 60 on-path items are individually classified `ON_PATH_SOUND`;
- the one claim is `TARGET_CLAIM_RESULT_CONSTRAINING`;
- 25 supplied opaque/symbol declarations are
  `OPAQUE_UNUSED_NO_DEPENDENCY`;
- 56 concrete-only items are absent from the Haskell proof;
- the remaining 787 fixed-semantics items are reviewed off-path declarations
  or guarded rules with no left-hand-side term constructible by this program.

`verification.k` contributes no local syntax, function, totality assertion,
opaque symbol, priority, equation, ordinary semantic rule, simplification,
operational bridge, lemma, or auxiliary claim. It only imports the
byte-identical supplied `MPY`. In particular, no proof rule contains any of
the 22 answer constants. Those constants occur in the submitted source body
and the result specification, not in semantics.

The exact material path is:

1. `#loadAll` and statement sequencing execute the actual `FuncDef`, which
   installs its closure at module scope `0`.
2. Generic call routing evaluates the callee, performs direct in-scope
   lookup, evaluates the already-valued argument left-to-right, allocates
   callee scope `1`, pushes the caller frame, and binds `a`.
3. Generated `Return` strictness, the Boolean head context, comparison
   contexts, direct lookup of `a`, integer-literal evaluation, and integer
   equality evaluate the submitted disjunction left-to-right.
4. Boolean `or` guards are complementary: a truthy head returns and a false
   head advances. No branch result is fabricated.
5. `Return` records the computed Boolean; `#pop` restores the caller,
   deletes the callee frame, resets `scopeLoc`, and empties stack/return state.
   No heap, exception, output, or exit-code effect occurs.

Relevant overlaps are benign or disjoint. Cell-aware lookup/binding priority
rules require a `"$cells"` marker absent from both plain frames. Ref-specific
operator/Boolean priority rules cannot match integer/Boolean operands. Generic
call is `[owise]` and no interception matches a plain call through the loaded
name. Integer equality has one applicable result. Structural recursion in the
on-path `appendVal` helper descends and covers both list constructors.
No reachable total function is unconstrained.

The supplied tree does expose opaque primitives for other language fragments:
19 float no-evaluator symbols plus `floorFI`, `toF`, and `ceilF`;
`md5hexCodes`; and `sortVS`/`sortKeyVS`. Total/underspecified out-of-bounds
sequence access and some deliberately partial valid-input models also belong
to the supplied trust boundary. The submitted AST contains no float, string,
list, dict, set, tuple, range, subscript, method, builtin, iterator, sort, MD5,
assignment, conditional, or loop term. None of these symbols/rules can affect
control, state, result, or postcondition here.

No inventoried rule was labeled unsound for this theorem, so there is no
unsound-rule finding requiring a false-conclusion witness. Full inventory and
per-module reasoning are in `evidence/k-rule-inventory.md`,
`evidence/classified-k-inventory.tsv`, and
`evidence/rule-assessment.md`; the generating scripts are preserved beside
them.

## 6. Fresh non-vacuity test

Result: **PASS**.

The audit-created mutation is preserved as
`evidence/spec-audit-vacuity.k`. It does not reuse the candidate mutation. It
renames the module/claim and changes only the final result disjunct from
`A ==Int 99` to `A ==Int 97`; the real loaded body remains unchanged.

First, the mutated specification built successfully:

```bash
kprove spec-audit-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  --claims SPEC-AUDIT-VACUITY.audit-false-postcondition \
  --dry-run
```

Exit: `0`.

The same command without `--dry-run` exited `1`, emitted
`WarnStuckClaimState`, and reported that the destination unifies but its
condition implication fails. The residual explicitly compares the mutated
22-way formula ending in `A ==Int 97` with the actual `A ==Int 99` branch.
This is the expected unmet result obligation, not a parse error, timeout,
missing import, or unrelated crash.

`A = 99` is a concrete witness: it satisfies `A < 100`, the actual program
returns true, and the mutated destination is false. The positive theorem is
therefore discriminating and non-vacuous.

Evidence: `evidence/spec-audit-vacuity.k`,
`evidence/fresh-vacuity-dry-run.log`, and
`evidence/fresh-vacuity-proof.log`.

## 7. Proven versus assumed accounting

Result: **PASS**.

### What the K proof establishes

Under the supplied `MPY` operational model, for every K integer `A < 100`,
from the pinned initial state, execution of the exact regenerated module and
entry call reaches a normal final state whose returned Boolean is true exactly
for the 22 listed integers. It also establishes the stated final module
binding and absence of leaked callee scope, heap mutation, stack frame, return
marker, exception, or nonzero exit code. Per the Kit contract, this is
reported as partial correctness.

Combined with the exhaustive elementary enumeration of products of three
primes below 100, this is the requested source-contract result for the full
integer domain `A < 100`; it is not a finite-example theorem or bounded
unrolling of a larger formal domain.

### Assumptions and trust boundaries

- **Supplied MPY semantics:** trusted as the selected operational model.
  Integrity is independently established. Only module loading, scopes,
  ordinary function call/return, integer equality, and Boolean short-circuit
  behavior are material; these rules were statically audited and concretely
  exercised.
- **K foundations/toolchain:** K parsing/elaboration, generated strictness
  rules, K `Int`/`Bool`/`Map`/`List` primitives, `kompile`, the Haskell/Kore
  prover, SMT reasoning, and the host runtime are trusted. This is the normal
  low-level proof-checker boundary.
- **Trusted translator:** equivalence from `solution.py` AST to
  `solution.mpy` is a trusted input boundary. Risk is reduced by fresh
  byte-identical regeneration and mechanical constructor equality between
  translated artifact and claim term. The translated subset used here is only
  definition, return, `or`, equality, names, and integer literals.
- **Contract bridge:** the meaning of “multiplication of 3 prime numbers” is
  connected to the explicit set by elementary mathematics and an independent
  exhaustive triple enumeration. This bridge is not itself a K primality
  theorem, but its bounded positive domain is fully enumerated, negative
  exclusion is immediate, and it agrees with the trusted canonical on the
  complete nonnegative domain. It is an acceptable intent bridge, not a
  material adequacy gap.
- **Opaque supplied symbols:** all 25 declared opaque/symbol boundaries are
  unused. No theorem conclusion depends on an interpretation of any of them.
- **Canonical/CPython differential:** supports implementation and contract
  fidelity on the recorded 134 inputs only. It is not used to close the K
  claim or replace universal symbolic execution.

Excluded behavior is exactly non-integer Python inputs and integers
`A >= 100`, neither of which belongs to the stated contract. There is no
proof-local oracle, empirical result bridge inside K, hidden source
substitution, narrowed HumanEval domain, or unproved program-defined helper.

The reconstructed proof is sound, result-constraining, non-vacuous, and pins
the real translated program over the complete source-contract domain. The
remaining trust boundaries are ordinary and do not create a material
adequacy or soundness gap.

Exact commands and statuses are consolidated in `evidence/COMMANDS.md`.

VERDICT: PASS
LEGITIMACY: LEGIT
