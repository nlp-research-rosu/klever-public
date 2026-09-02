# Independent adversarial audit: 28-concatenate

The candidate's files were treated only as untrusted evidence. All executable
artifacts were copied or independently authored in
`/tmp/audit-work/28-concatenate`; both K definitions were rebuilt from source.
No candidate-provided cache or compiled definition was used.

The reconstructed claims do close, and the claims that are present are
non-vacuous. The candidate nevertheless does not contain a proof of the
requested universal function contract. It proves one universal *internal loop*
claim and only two concrete end-to-end calls. There is no symbolic entry claim
connecting arbitrary `List[str]` input through module loading, allocation,
binding, initialization, the loop, return, and frame cleanup to the
concatenated result. That missing theorem is a material adequacy failure and
determines the verdict.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` directory is present, so the trusted mounts do
not contradict the rendered mode.

The recursive candidate semantics check passed:

- `diff -r --no-dereference` exited 0.
- A separate recursive entry-type and SHA-256 inventory comparison exited 0.
- There are no candidate symlinks in the semantics tree, and it has no missing,
  additional, mistyped, or changed entry relative to the trusted tree.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted counterparts. Their SHA-256 values are respectively
`9481906207fb44fe66ec3a6b2bc82cf92b42739848b577fa9561de14375f807b`
and
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The required provenance files `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log` are missing. No structured generation
trace is present under any of the checked conventional names. Consequently
there were no provenance claims to credit or cross-check. The absence is an
auditability defect, not an infrastructure breach and not the basis of the
candidate verdict. Candidate auxiliary files (`prove.sh`, `smoke.py`,
`smoke.mpy`, and `__pycache__`) were not trusted.

Evidence:

- [integrity checker](/audit-output/evidence/stage1/check_integrity.sh)
- [integrity log, commands and exits](/audit-output/evidence/stage1/check_integrity.log)

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt specifies `concatenate(strings: List[str]) -> str`: return
the concatenation of the list elements in their original order. The documented
examples require `[]` to produce `""` and `["a","b","c"]` to produce `"abc"`.
The trusted canonical implementation is `return ''.join(strings)`. The intended
domain is every finite Python list whose elements are strings.

The candidate implementation initializes an empty accumulator, iterates once
per element in order, performs `result += string`, and returns the accumulator.
It is a different but extensionally appropriate algorithm on the intended
domain.

Using the trusted translator:

```text
python3 /reference/py2mpy.py /tmp/audit-work/28-concatenate/solution.py
```

produced a file byte-identical to submitted `solution.mpy`; both have SHA-256
`76f72a295e084927590a18af5a031a11a16dad65c5673d5fd10d1d29ce127456`.

The independent differential script imports the trusted canonical and copied
candidate entry points under distinct module names. It tests the two documented
examples, zero/one/many loop iterations, empty elements, embedded NUL and
newline, Unicode, long elements, all lists of length 0 through 4 over seven
representative string atoms, and 2,000 seeded broader cases. It also checks
that the input list is not mutated and that the result is a `str`.

Result: 4,812 cases, 0 mismatches. This is finite implementation-to-intent
evidence; it is not a K proof.

Evidence:

- [differential test](/audit-output/evidence/stage2/differential_test.py)
- [translation and differential log](/audit-output/evidence/stage2/check_fidelity.log)

## 3. Clean proof reconstruction

K was independently available as version `v7.1.337` (build date
2026-06-18). The scratch tree contains candidate `solution.py`,
`solution.mpy`, `spec.k`, and `verification.k`, the trusted prompt/canonical
translator inputs, and a fresh copy of the trusted supplied semantics. It
contains no copied candidate definitions or caches.

The concrete definition was rebuilt with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit 0. Fresh ASCII concrete execution covered empty, one-element,
three-element, empty-element, and embedded-newline inputs and ended with
`.K`, `NoExc`, empty stack, and exit code 0. An attempted BMP non-ASCII literal
failed in the LLVM interpreter at `strToCodes`; an astral literal failed even
earlier because the translator's surrogate-pair escape is rejected by the K
scanner. These are reproducible boundaries of the supplied semantics, whose
`str.k` explicitly labels literals ASCII-only. The normal and branch-boundary
reconstruction itself succeeded.

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell \
  --main-module CONCATENATE-VERIFICATION \
  --syntax-module CONCATENATE-VERIFICATION \
  --output-definition verification-kompiled
```

Exit 0. The original three-claim spec exited 0 and printed `#Top`. Each claim
was also copied exactly into a distinct reviewer module and proved separately:

| Claim | Exit | Required output |
|---|---:|---|
| universal internal loop | 0 | `#Top` |
| concrete empty call | 0 | `#Top` |
| concrete `["a","b","c"]` call | 0 | `#Top` |

Thus clean reconstruction passes for every positive claim that the candidate
actually submitted. It does not enlarge the scope of those claims.

Evidence:

- [tool versions](/audit-output/evidence/stage3/tool_versions.log)
- [LLVM build](/audit-output/evidence/stage3/kompile_runtime.log)
- [successful ASCII concrete run](/audit-output/evidence/stage3/concrete_runtime_ascii.log)
- [BMP non-ASCII boundary](/audit-output/evidence/stage3/concrete_runtime_supported.log)
- [astral-literal boundary](/audit-output/evidence/stage3/concrete_runtime.log)
- [Haskell proof build](/audit-output/evidence/stage3/kompile_verification.log)
- [original combined proof](/audit-output/evidence/stage3/kprove_all_original.log)
- [loop-only proof](/audit-output/evidence/stage3/kprove_loop.log)
- [empty-only proof](/audit-output/evidence/stage3/kprove_empty.log)
- [abc-only proof](/audit-output/evidence/stage3/kprove_abc.log)
- [separate claim artifacts](/audit-output/evidence/stage3)

## 4. Adequacy and real-program pinning

### Plain-language claims

1. **Internal loop claim (`spec.k:7`).** If `VS` is a K `ValSeq` consisting
   only of `str(IntSeq)` values, the current scope contains accumulator
   `str(A)`, an old loop-target value, and an unchanged `strings` argument,
   then executing
   `#loop(list(VS), Name("string"), concatenateLoopBody)` before any
   continuation leaves the continuation in place, changes `result` to the
   left-to-right concatenation fold starting from `A`, and leaves `string` as
   its old value for an empty sequence or as the final element otherwise.

2. **Empty entry claim (`spec.k:36`).** From the exact initial module
   configuration, load the translated module and call `concatenate([])`. The
   returned K value is exactly `str(.IntSeq)`. The claim preserves normal
   return/exception/exit cells and permits the expected existential final
   scope and heap state.

3. **ABC entry claim (`spec.k:58`).** From the same initial configuration,
   load the translated module and call `concatenate(["a","b","c"])`. The
   returned K value is exactly code sequence `[97,98,99]`, i.e. `"abc"`.

Each precondition is satisfiable. For the loop claim, one witness uses
`A=.IntSeq`,
`VS=vCons(str(iCons(120,.IntSeq)),.ValSeq)`, an empty old loop target,
environment location 1, and a scope at location 1 containing `result`,
`string`, and `strings`; `allStringValues(VS)` reduces to true and the claimed
result is `"x"`. For both entry claims, their written initial cells are the
semantics' concrete initial configuration. Fresh concrete execution witnesses
that configuration.

Ground substitutions for the empty entry, ABC entry, one-iteration loop,
empty-element loop, and a general three-element loop all agree with both Python
implementations. See
[concrete substitutions](/audit-output/evidence/stage4/concrete_substitutions.log).

### Program identity and control-flow match

The proof-local `concatenateLoopBody`, `concatenateBody`, and
`concatenateModule` are zero-argument definitional aliases. Their expansions
are exactly the constructor terms in the regenerated/submitted
`solution.mpy`: import, function definition, both initial assignments, the
`For`, its `AugAssign`, and the `Return`. They do not replace execution with an
answer. The two entry claims therefore execute the actual translated program,
not a substituted body.

The internal loop claim also matches real control flow after the list argument
has been allocated, bound to `strings`, looked up and dereferenced, and both
local initializers have run. It preserves the arbitrary continuation and
describes the exact loop body.

All three submitted claims constrain a result-bearing state: the loop fixes
the accumulator and final target; both entries fix the returned string. None is
a tautology or free-result claim.

### Material missing theorem

No claim begins at a symbolic function entry for an arbitrary all-string list.
The universal loop claim begins *after* module load, callee lookup, argument
evaluation/allocation, call-frame creation, parameter binding, both
initializations, and iterable lookup/dereference. The two entry claims test
that plumbing only for two concrete lists. Reachability claims are not
automatically composed merely because a helper claim and examples coexist in
the same file.

Accordingly, the formal proof does not establish:

```text
for every finite List[str] input xs,
if concatenate(xs) terminates, its returned value equals ''.join(xs)
```

This is not thin testing or a minor intent bridge. It is the absence of the
requested universal entry theorem and is independently sufficient for
`FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The line-addressed inventory covers every K file in the supplied tree plus
`verification.k` and `spec.k`. It contains:

- 708 rules;
- 235 syntax declarations;
- 154 records carrying `function`, 116 carrying `total`;
- 45 priority records, 27 `owise` records, and 37 `concrete` records;
- 25 `symbol` and 22 `no-evaluators` records;
- 5 contexts, 1 configuration, and 3 claims;
- no local `functional`, `simplification`, or `simplifier` declaration.

The full text and attributes of every record are in
[rule_inventory.txt](/audit-output/evidence/stage5/rule_inventory.txt).
Every record has an explicit disposition in
[construct_assessment.csv](/audit-output/evidence/stage5/construct_assessment.csv).
The latter marks 42 supplied rules traversed by these claims, 233 supplied
declarations, and 787 supplied records that are not reachable on this
program's typed paths. The supplied records are the unmodified selected
semantics, not candidate-authored proof extensions. `MPY-CONCRETE` is used by
the LLVM runtime module but is not imported by the Haskell proof module.

### Mapping of submitted syntax to semantics

| Submitted construct | Declaration and execution rules |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| `ImportFrom("typing","List")` | `syntax.k:43`; non-math no-op at `controls.k:35-44` |
| `FuncDef`, `Params` | `syntax.k:53,57`; closure binding at `functions.k:14-16` |
| `Call`, `Name` | `syntax.k:12,28`; lookup `core.k:130-154`; callee/arguments `call.k:18-21` |
| `ListExpr` | `syntax.k:17`; left-to-right evaluation and allocation `list.k:12-15` |
| call frame/binding/return | `call.k:69-74`; `functions.k:62-66,77-90` |
| `Assign(Name,Str)` | strict RHS in `syntax.k:41`; literal `str.k:13-17`; store `controls.k:9-18` |
| `For` over the list ref | `syntax.k:45`; one-time dereference `controls.k:104-108`; loop protocol `controls.k:65-74`; list iterator `list.k:8-10` |
| loop target `Name` | `tuple.k:30-41` |
| `AugAssign` | strict RHS in `syntax.k:44`; scope update `controls.k:20-31`; string addition `str.k:20-24` plus the reviewed symbolic generalization |
| `Return` | `syntax.k:50`; abrupt return and frame pop `functions.k:77-90` |

This route preserves left-to-right argument evaluation, creates one heap list
for the input expression, creates and later deletes the call scope, leaves the
heap allocation monotonic, iterates in list order, performs inline string-code
concatenation, restores the caller environment, and returns through an empty
stack with `noRet` and `NoExc`. The proof-local rules introduce no priority
rule, exception rule, allocation shortcut, call shortcut, or abrupt-control
bridge.

### Proof-local declarations and rules

The 8 declarations and 13 rules in `verification.k` were reviewed as follows:

- `isStringValue` and `allStringValues` are truthful structural predicates;
  their cases are disjoint/complete and recursion descends.
- `stringCodes(str(S)) => S` is the correct projection on every used value.
  Its `[total]` declaration is over-broad because no equation covers non-string
  `Val`. Every actual use is guarded by the all-string predicate, so there is
  no witnessed false result on the intended domain. This is recorded as a
  coverage gap, not labeled unsound.
- `concatenateValues` is the left-to-right code-sequence fold. Under
  `allStringValues`, its recursive calls to `stringCodes` are within the
  covered string case.
- `finalLoopValue` is a complete structural fold and correctly describes
  Python's final loop-target behavior.
- The three body/module aliases expand exactly to the submitted MPY terms and
  do not bypass execution.

The added rule

```text
applyBin("+", str(A), V)
  => str(seqConcat(A, stringCodes(V)))
requires isStringValue(V)
```

is the only proof-local rule that contributes directly to operational
evaluation. Its overlap with the fixed supplied rule at `V=str(B)` has the same
right-hand side after `isStringValue` and `stringCodes` reduce. A fresh
bridge-free theorem for the explicit structural domain `V=str(B)` exited 0
with `#Top`.

However, the required bridge-free theorem over the candidate rule's complete
Boolean-guard domain did not close. It exited 1 with a stuck implication
containing `true == auditIsStringValue(V)` and an unreduced
`applyBin("+",str(A),V)`. Thus the candidate provides no machine-checked
universal connection from that guard to fixed execution. The artifacts are:

- [bridge-free baseline](/audit-output/evidence/stage5/bridge-baseline.k)
- [complete-guard theorem](/audit-output/evidence/stage5/bridge-connection-spec.k)
- [complete-guard failure log](/audit-output/evidence/stage5/kprove_bridge_connection.log)
- [structural theorem](/audit-output/evidence/stage5/bridge-structured-spec.k)
- [structural theorem success log](/audit-output/evidence/stage5/kprove_bridge_structured.log)

There is no concrete or symbolic witness showing that the generalized rule can
produce a false string-addition result on the intended all-string domain.
Therefore this review does **not** label the rule unsound; it records the
narrower connection-evidence gap required by the audit instructions.

The supplied semantics' opaque `no-evaluators` symbols are `sortVS`,
`sortKeyVS`, `md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
`absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`. None can
occur on this program's string/list path or influence its branches, result,
state, exception, or postcondition.

No inventoried rule is rejected as unsound in this review, so there is no
unsupported unsoundness allegation requiring a false-conclusion witness. The
candidate fails because the target universal claim is missing, not because an
invented false rule has been demonstrated.

## 6. Fresh non-vacuity test

A reviewer-authored spec changed the concrete ABC result's last code point from
99 (`"abc"`) to 100 (`"abd"`). The input is the same satisfiable exact initial
state and call as the positive ABC claim.

The mutation dry-run exited 0, proving it parsed and built successfully. The
actual proof exited 1 with `WarnStuckClaimState`. Its residual is a normal final
configuration whose `<k>` cell contains exactly
`str(iCons(97,iCons(98,iCons(99,.IntSeq))))`; that term does not unify with the
mutated destination ending in 100. The failure is therefore the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash.

Evidence:

- [fresh mutation](/audit-output/evidence/stage6/spec-vacuity-fresh.k)
- [successful dry-run/build](/audit-output/evidence/stage6/kprove_mutation_dry_run.log)
- [expected stuck proof](/audit-output/evidence/stage6/kprove_mutation.log)

The submitted concrete entry claims are non-vacuous and result-constraining.
This does not supply their missing universal generalization.

## 7. Proven versus assumed accounting

### Formally established by the reconstructed K proofs

- The exact internal loop transforms a string accumulator according to
  `concatenateValues` for every K `ValSeq` satisfying `allStringValues`, while
  preserving its continuation and updating the loop target as specified.
- The exact translated program returns `""` on `[]`.
- The exact translated program returns `"abc"` on `["a","b","c"]`.
- The fresh false `"abd"` result is rejected.

### Trusted or conditional boundaries

- The entire byte-identical supplied semantics and its imported K
  `INT`/`BOOL`/`STRING`/`MAP`/`LIST`/`K-EQUAL` operations are the fixed language
  model. Relevant trusted primitives include map lookup/update/membership,
  list/frame operations, integer allocation arithmetic, K equality, and the
  `lengthString`/`substrString`/`ordChar` hooks used for source literals.
- The K parser, kompiler, Haskell prover/backend, and LLVM runtime are trusted
  to implement their published logic and hooks.
- The trusted `py2mpy.py` is the source-to-MPY bridge. Byte identity proves the
  submitted MPY is its output for `solution.py`; it does not itself prove Python
  semantic equivalence.
- The proof-local symbolic string-addition generalization is structurally
  consistent with the fixed string rule, but its complete-guard bridge-free
  connection theorem is absent and the reviewer attempt did not close.
- The mapping from arbitrary Python strings to the K `IntSeq` model is not
  universally validated. Concrete K literals are explicitly ASCII-only and
  failed on tested non-ASCII inputs, although Python differential tests passed
  Unicode cases.
- The 22 imported opaque supplied symbols listed in Stage 5 are trusted
  semantics boundaries but unreachable and non-dependent for these claims.

### Empirical and informal evidence only

- The 4,812-case Python differential run strongly supports that the submitted
  Python implementation matches `''.join` on the tested valid inputs.
- Fresh ASCII K execution supports the concrete operational bridge for the
  tested normal/boundary inputs.
- The natural-language meaning of `concatenate` is taken from the trusted
  prompt and canonical implementation. Neither differential evidence nor that
  informal bridge replaces a universal reachability claim.

### Decision

Clean `#Top` reconstruction and non-vacuity both pass. Real-program pinning is
sound for the exact helper and two exact calls. Nevertheless, the proof set
omits the universal entry claim required by the problem, and the only
proof-local execution generalization also lacks the validation workflow's
complete-guard machine connection. Under the stated decision boundary, a
missing target proof is `FAIL / NOT_LEGIT`, even when the implementation is
empirically correct and narrower claims are honest.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
