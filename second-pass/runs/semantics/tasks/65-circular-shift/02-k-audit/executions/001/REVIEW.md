# Independent adversarial audit: 65-circular-shift

## Executive decision

The candidate contains a legitimate, freshly reconstructible partial-correctness
proof for every K integer `x` and every **nonnegative** K integer `shift`. Both
entry claims independently close with `#Top`; the claim executes the submitted
function body under the supplied semantics, constrains the returned string, is
body-sensitive, and rejects a fresh false-result mutation.

I assign `CONCERNS`, not `PASS`, for two limitations:

1. The prompt never explicitly restricts `shift` to nonnegative values. The
   generated Python differs from the trusted canonical implementation for four
   of five negative-shift probes, and the K claims exclude all such inputs.
2. Claim closure depends on the proof-local, result-bearing abstraction
   `strToCodes(Int2String(X)) => intCodes(X)`. It is an exact-pattern,
   conservative name for a pure fixed-semantics term, and I found no false
   conclusion witness. However, the candidate supplies no bridge-free
   machine-checked theorem for its totality/definedness; this bridge remains an
   explicit informal trust boundary.

Neither limitation makes a false K conclusion provable on the stated formal
domain, so the proof remains legitimate rather than `NOT_LEGIT`.

The complete command ledger is `evidence/COMMANDS.md`. Logs named below contain
the exact commands, exit statuses, and bounded output.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. The trusted mount therefore agrees
with the rendered mode; there is no infrastructure breach and no reason to
return `AUDIT_ERROR`.

`evidence/01_provenance.sh` performed type, symlink, byte, tree, manifest, and
digest checks. Its complete output is `evidence/01_provenance.log` (wrapper exit
0).

### Trusted/candidate comparisons

- `/candidate/prompt.py` is a regular file and byte-identical to
  `/reference/prompt.py` (`cmp` exit 0; SHA-256
  `2751ca433b3ea9f4f348dd18f65c357482e140739e26ec98b1e056e55b491dc0`).
- `/candidate/py2mpy.py` is a regular file and byte-identical to
  `/reference/py2mpy.py` (`cmp` exit 0; SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- Recursive `diff -r --no-dereference` between the candidate and trusted
  `reference-semantics/` trees exits 0. Both manifests contain exactly the same
  two directories and 25 regular `.k` files, with no missing, additional,
  changed, mistyped, or symlinked entry.
- There are no symlinks anywhere below `/candidate`.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are regular
  files. Their candidate SHA-256 values are recorded in
  `evidence/01_provenance.log`.

The trusted semantics identity selects the fixed language semantics; it does
not bless the four proof-local rules in `verification.k`, which are audited
separately in stage 5.

### Missing and extra provenance material

The following requested candidate metadata is absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace (`*trace*`, `*.json`, or `*.jsonl`)

No `PROOF.md` or candidate vacuity artifact is present. Consequently there was
no generation report to trust or rebut; this is missing provenance evidence,
not an execution-infrastructure failure.

Additional untrusted artifacts are `concrete-tests.py`,
`concrete-tests.mpy`, `prove.sh`, and `__pycache__/`. No candidate cache or
compiled definition was copied or reused. I inspected the source tests and
script only as claims.

The live toolchain was independently available:

```text
K version: v7.1.337
Build date: Thu Jun 18 07:59:56 CDT 2026
```

See `evidence/07_final_checks.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

From the trusted prompt and canonical source, the function converts integer
`x` to its decimal Python string `s`. If `shift > len(s)`, it returns `s`
reversed. Otherwise it returns the suffix of length `shift` followed by the
remaining prefix, i.e. a right circular shift. The documented examples are
`circular_shift(12, 1) == "21"` and
`circular_shift(12, 2) == "12"`.

For negative `x`, both the canonical implementation and generated program treat
the leading minus sign as part of `s`. There is no empty integer-string case;
`x = 0`, whose string has length one, is the minimum-length boundary.

The generated program uses Python negative slice indices:

```python
return s[-shift:] + s[:-shift]
```

For `0 <= shift <= len(s)`, this equals the canonical
`s[len(s)-shift:] + s[:len(s)-shift]`, including `shift == 0` and
`shift == len(s)`. For `shift > len(s)`, both take the reversal branch.

### Translation fidelity

In scratch, the trusted copied translator regenerated `solution.mpy` from the
copied `solution.py`. `cmp -s` exits 0, and both files have SHA-256
`ea135d25f2f2f0824e0fe9055892c5a7024291d5df41e5b27007257cae091901`.
See `evidence/02_fidelity.log`.

### Independent differential

`evidence/02_differential.py` imports independently copied trusted canonical and
generated entry points. It exercises:

- both documented examples;
- zero shift;
- one-character inputs (`x = 0` and `x = 7`);
- `len-1`, exact-length, first-oversize, and large-oversize boundaries;
- positive and negative `x`;
- 1,200 deterministic generated inputs, biased toward every branch boundary.

On the formal nonnegative-shift domain, 18 explicit boundary cases plus 1,200
generated cases produced zero mismatches (seed `650065`). The script exits 0.
Complete inputs/results and the exact command are in
`evidence/02_fidelity.log`.

The prompt does not state `shift >= 0`, so the script separately probed five
negative shifts. Four differ:

```text
x=12,    shift=-1: canonical "12",    generated "21"
x=12345, shift=-1: canonical "12345", generated "23451"
x=12345, shift=-2: canonical "12345", generated "34512"
x=-123,  shift=-1: canonical "-123",  generated "123-"
```

This is a real candidate-versus-canonical divergence if negative shifts are in
the intended domain. The K proof makes no false claim about those inputs because
both entry preconditions require `SHIFT >=Int 0`; the unannounced restriction is
an adequacy concern.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/case`; trusted
inputs were copied separately to `/tmp/audit-work/trusted`. Candidate compiled
definitions, caches, and bytecode were not copied. Final `cmp`/`diff` checks
confirm that the primary scratch source still equals the candidate source
(`evidence/07_final_checks.log`).

### Fresh concrete definition and execution

The exact LLVM build is in `evidence/03_build_runtime.sh`:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled --warnings none
```

It exits 0 (`evidence/03_build_runtime.log`). The reviewer-authored
`evidence/03_reviewer_concrete.py` was translated with the trusted translator
and run with:

```text
krun reviewer-concrete.mpy --definition runtime-kompiled --output pretty
```

The run exits 0 after assertions over normal, exact-length, zero-shift,
oversize, one-character, and negative-`x` cases. The final configuration has
`.K`, `NoExc`, and exit code `0`; see `evidence/03_run_concrete.log`.

### Fresh proof definition

The exact Haskell build is in `evidence/03_build_proof.sh`:

```text
kompile verification.k --backend haskell \
  --main-module CIRCULAR-SHIFT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled --warnings none
```

It exits 0 (`evidence/03_build_proof.log`).

Every positive target was then run independently:

| Claim | Selection | Result |
|---|---|---|
| normal shift | `--claims CIRCULAR-SHIFT-SPEC.normal-shift` | exit 0, `#Top` |
| oversize shift | `--claims CIRCULAR-SHIFT-SPEC.oversize-shift` | exit 0, `#Top` |

Both commands use `--depth 300`, `--warnings none`, the fresh
`verification-kompiled`, and spec module `CIRCULAR-SHIFT-SPEC`. Complete command
lines and output are in `evidence/03_prove_normal.log` and
`evidence/03_prove_oversize.log`.

There was no timeout, backend uncertainty, reused `#Top`, or candidate-provided
compiled evidence.

## 4. Adequacy and real-program pinning

### Claims in plain language

Both claims begin with the complete initial call state:

- `<k>` contains `Call(Name("circular_shift"), (X, SHIFT))`;
- environment location is 0;
- scope 0 binds only `circular_shift` to the submitted closure and has the
  builtins scope at parent -1;
- heap and stack are empty;
- allocation counters are at their initial values;
- return state is `noRet`, exception state is `NoExc`, and exit code is 0.

The **normal claim** requires:

```text
LEN = length(decimal-string-codes(X))
SHIFT >= 0
SHIFT <= LEN
```

At termination, the `<k>` value must be
`circularShiftSpec(X, SHIFT, LEN)`, whose applicable equation is suffix
`[-SHIFT:]` plus prefix `[:-SHIFT]`.

The **oversize claim** requires:

```text
LEN = length(decimal-string-codes(X))
SHIFT >= 0
SHIFT > LEN
```

Its required terminal value is the full step-`-1` slice, i.e. reversal.

The two preconditions are disjoint and partition every nonnegative shift.
`X` is unrestricted over mathematical K integers. The destination is not a
fresh variable, tautology, implication, or unconstrained existential: it is an
exact `Val`. All displayed non-`k` cells are unrewritten and therefore must be
restored exactly.

### Real-program identity

The claim does not load `solution.mpy` as a module at proof time. Instead it
starts from the function-call state with `circularShiftClosure` installed.
That constant expands to a closure containing assignment, comparison,
reversal branch, normal slicing/concatenation, return, parameters
`("x","shift")`, and parent scope 0.

This is manual embedding, so I checked the pin rather than trusting its comment:

1. trusted translation is byte-identical to the submitted MPY;
2. `evidence/04_adequacy.py` parses balanced K terms, normalizes only the
   translator's empty-`.Stmts` sugar, and requires exact equality between the
   submitted function body and embedded closure body;
3. the check exits 0 and reports
   `submitted_body_equals_embedded_closure_body: true`.

Thus the claim executes a semantic term identical to the submitted function,
not a substituted algorithm. There are no loops and no helper reachability
claims. Function call, binding, assignment, condition evaluation, slices,
concatenation, return, frame pop, and state restoration all execute through the
fixed supplied rules.

As a separate sensitivity check, I swapped suffix and prefix only in the
embedded program body, rebuilt successfully, and reran the unchanged normal
claim. The proof exits 1 with `WarnStuckClaimState` and the unmet ordering
equality (`evidence/05_verification_program_body_mutation.k`,
`evidence/05_program_body_sensitivity.log`). This shows the proof is sensitive
to real body behavior.

### Satisfying states and ground substitution

`evidence/04_adequacy.py` exhibits and checks:

| Claim | `X` | `SHIFT` | `LEN` | Formal/canonical/generated result |
|---|---:|---:|---:|---|
| normal | 12 | 1 | 2 | `"21"` |
| normal boundary | 12 | 2 | 2 | `"12"` |
| oversize | 12 | 3 | 2 | `"21"` |
| oversize, negative `x` | -123 | 5 | 4 | `"321-"` |

Every precondition evaluates true, and all three results agree.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_static_inventory.py` independently extracts every K entry from
the supplied semantics, `verification.k`, and `spec.k`.
`evidence/05_static_inventory.tsv` has 1,104 data rows:

| Kind | Count |
|---|---:|
| ordinary rules | 698 |
| simplification rules | 1 |
| reachability claims | 2 |
| syntax declarations (all attribute variants) | 230 |
| contexts | 5 |
| configuration | 1 |
| imports | 88 |
| top-level `requires` | 25 |
| modules / endmodules | 27 / 27 |

There are no `[functional]` declarations. The inventory records every
`[function]`, `[total]`, `[macro]`, `[strict]`, `[seqstrict]`, `[symbol]`,
`[no-evaluators]`, priority, and `owise` occurrence and includes each complete
multiline rule/guard. `evidence/05_special_declarations.txt` and
`evidence/05_opaque_symbols.txt` provide focused extracts.

`evidence/05_rule_assessment.tsv` attaches a disposition to every inventory
row. Supplied-semantics rows are marked as fixed selected semantics and as
coming from either a reached or unreachable module. This use of the trusted
baseline does not extend to proof-local rows.

### Fixed supplied semantics

The entire tree is authoritative at the selected semantics level because it is
byte-identical to the trusted `SUPPLIED_SEMANTICS` mount. I nevertheless traced
every construct on the submitted execution path. The exact declaration/rule
map is `evidence/05_construct_map.md`.

The reached behavior is:

- generated strictness heats/cools assignment RHS, unary operand, binary
  operands left-to-right, condition, and return expression in order;
- name lookup walks the callee scope then the builtins parent;
- calls evaluate the callee and arguments, allocate one frame, bind `x` and
  `shift`, and execute the stored body;
- `str(Int)` yields `str(strToCodes(Int2String(Int)))`;
- `len(str(IS))` is `isLen(IS)`;
- integer `>`, unary minus, Boolean branch selection, string slicing, and
  string concatenation follow their fixed domain rules;
- `Return(V)` records `V`, discards only the rest of that function body, pops
  exactly the saved frame, restores environment/scope allocation, and exposes
  `V` to the original continuation.

The slice step is always default `1` or explicit `-1`, never zero. Normal-branch
starts/stops are within the CPython-style clamped range; reversal starts at
`LEN-1` and stops before `-1`. The recursive `buildIS` calls therefore access
only in-range string positions. There is no allocation or mutation on this
program path, and no exception-producing used operation.

The 25 fixed opaque `[symbol]` declarations are confined to sort, float, and
MD5 facilities. None is reachable from this integer/string program. Fixed
priority rules concern ref dereference, mutating collections, special calls,
or other unreachable behavior; no relevant priority preempts the ordinary
function, slice, or return path.

### Proof-local inventory

`verification.k` contributes exactly:

1. `syntax IntSeq ::= intCodes(Int)`: a fresh opaque constructor;
2. one simplification rule,
   `strToCodes(Int2String(X)) => intCodes(X)`;
3. macro syntax for `circularShiftClosure`;
4. one exact expansion of that closure;
5. function syntax `circularShiftSpec(Int, Int, Int)`;
6. an oversize equation guarded by `SHIFT > LEN`;
7. a normal equation guarded by `SHIFT <= LEN`.

There are no proof-local `[total]` or `[functional]` declarations, priorities,
configuration rewrites, call interceptions, abrupt-control rewrites, or
state-cell rules.

The two `circularShiftSpec` guards are disjoint and exhaustive over integer
`SHIFT` and `LEN`. Their right sides are precisely the postcondition: reversal
for oversize and suffix-plus-prefix otherwise. They do not match `Call` or
replace program execution. Encoding the desired mathematical result in the
postcondition is legitimate; the actual body must and does execute to reach it.

The closure rule is a definitional macro for the exact submitted semantic body,
as established in stage 4. It neither changes evaluation order nor omits cells.

### `intCodes` boundary

The only delicate extension is:

```k
rule strToCodes(Int2String(X:Int)) => intCodes(X) [simplification]
```

Its complete match domain is exactly integer-to-decimal-string conversion
followed by ASCII-code conversion. It has no continuation, binding, state,
control, or priority effect. It influences the string value, its length, the
branch, both slices, the returned value, and the postcondition.

For every integer, `Int2String` produces a nonempty decimal string containing
only ASCII digits and possibly `-`; the fixed recursive `strToCodes` is defined
on all such strings. The fresh `intCodes(X)` can conservatively name that exact
sequence. The rule asserts no particular digit, length, slice, branch, or task
answer. For example, at `X = 12` the fixed expression produces codes
`[49, 50]`; the rule names that same result `intCodes(12)` rather than asserting
that it is empty or has different codes.

This is why I do **not** label the rule unsound: I found no concrete or symbolic
false conclusion witness, and an opposite content interpretation is not
licensed by the defining equation. The proof also establishes the rotation
identity parametrically in whatever exact code sequence the conversion yields.

It is nonetheless a material evidence gap. The rule preempts reduction of a
pure fixed-semantics computation, is used on both execution and postcondition
sides, and the candidate provides no independent bridge-free universal
connection theorem. Removing only the declaration/rule builds successfully but
leaves the normal proof stuck before branch selection with
`#Ceil(strToCodes(Int2String(X)))` and two unexplored branches
(`evidence/07_verification_without_intcodes.k`,
`evidence/07_without_intcodes.log`, build exit 0, proof exit 1). Closure thus
depends on the abstraction's totality/definedness fact.

This is a narrower trust/validation concern, not a witnessed false semantic
rule. Finite concrete and differential evidence supports the bridge on tested
inputs but does not prove it universally.

### Static conclusion

No proof-local rule encodes a substituted program, bypasses a used construct,
fabricates a result, introduces an unconstrained oracle, or enables a witnessed
false conclusion on the formal input domain. There is no overlap, guard,
priority, totality, allocation, control, or state-restoration defect on the
reached path.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k`; no candidate mutation evidence was
trusted.

I created `evidence/06_spec-vacuity.k`, a distinct spec module that keeps the
program and initial state unchanged but deliberately demands
**prefix plus suffix** in the normal branch instead of **suffix plus prefix**.
This changes the result-constraining obligation. The state
`X = 12345`, `SHIFT = 2`, `LEN = 5` satisfies the precondition and witnesses
falsity:

```text
correct result: "45123"
mutated result: "12345"
```

The exact sequence in `evidence/06_nonvacuity.sh` is:

1. `kprove ... --dry-run`: exit 0, proving the mutation parses and builds;
2. ordinary `kprove` against the fresh positive definition: exit 1;
3. backend output: `WarnStuckClaimState`, followed by the failed equality
   between the two opposite `seqConcat(buildIS(...), buildIS(...))` orders.

The wrapper exits 0 only after observing the expected nonzero proof result.
`evidence/06_nonvacuity.log` preserves the command, statuses, and residual.
This is a meaningful unmet postcondition, not a parser error, missing import,
timeout, unrelated crash, or unreachable mutation.

The separate program-body mutation in stage 4 provides independent execution
sensitivity. An earlier exploratory result mutation named
`05_body_sensitivity*` is superseded by the clean stage-6 artifact and is not
relied upon.

## 7. Proven versus assumed accounting

### Precisely proven

Under the fresh Haskell definition consisting of the trusted supplied semantics
plus the audited proof-local equations:

- for every mathematical integer `X`;
- for every mathematical integer `SHIFT >= 0`;
- with `LEN` equal to the code-sequence length of `str(X)`;
- from the exact initial call configuration containing the submitted closure;

every terminating execution covered by the normal or oversize claim returns
exactly `circularShiftSpec(X, SHIFT, LEN)` and restores the displayed
environment, scopes, counters, heap, stack, return state, exception state, and
exit code. For `SHIFT <= LEN` this result is the last `SHIFT` characters followed
by the preceding characters; for `SHIFT > LEN` it is the reversed string.

This is partial correctness. The report does not promote concrete termination
tests into a general termination theorem.

### Trust ledger

| Boundary | Dependents | Classification |
|---|---|---|
| K v7.1.337 compiler, Haskell/LLVM backends, SMT/KORE execution | all machine results | Necessary toolchain trust; fresh builds and independent success/failure behavior make it auditable. |
| Byte-identical supplied MPY semantics and imported K `INT`, `BOOL`, `STRING`, `MAP`, `LIST` primitives | all execution, slicing, arithmetic, strings, cells | Acceptable selected-semantics boundary mandated by `SUPPLIED_SEMANTICS`. |
| Trusted translator `py2mpy.py` | Python-to-MPY identity | Acceptable trusted input; byte identity was independently checked. |
| Manual closure embedding | real-program pin | Acceptable with concern-level manual bridge; exact structural equality and body-sensitivity were independently checked. |
| `intCodes` simplification / universal totality of decimal ASCII conversion | branch definedness, length, slices, result, both claims | Sound-looking conservative abstraction with no false witness, but no independent K connection theorem; concerning informal bridge. |
| Ordinary mathematical equivalence of negative-index slices and `len-shift` slices for `0 <= shift <= len` | natural-language/canonical adequacy | Direct arithmetic/slice argument plus finite differential support; not a substitute for the K proof. |
| 1,218-case differential and reviewer concrete execution | empirical Python/K bridge on sampled inputs | Reproducible finite evidence only. It cannot establish universal equivalence. |
| Assumption that a shift count is nonnegative | theorem-to-prompt domain | Concerning: formalized explicitly by K, but absent from prompt; negative canonical divergences are recorded. |

No candidate prose, trace, prior `#Top`, or test result is counted as a proof.
The differential supports only implementation/canonical agreement over tested
inputs. The successful reachability claims, static rule audit, body sensitivity,
and non-vacuity test are the proof evidence.

### Verdict rationale

The proof reconstructs, constrains the result, runs the real submitted body, and
contains no witnessed unsound shortcut. It is therefore `LEGIT`. It does not
earn `PASS` because the negative-shift scope is not stated by the prompt and the
result-bearing `intCodes` totality bridge is not independently proved inside K.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
