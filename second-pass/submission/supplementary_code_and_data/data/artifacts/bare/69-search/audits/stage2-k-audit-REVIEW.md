# Independent adversarial review: 69-search

This review treats every candidate artifact and generation record as untrusted
evidence. All executable work used source-only copies under
`/tmp/audit-work`; no candidate kompiled definition, cache, traceback archive,
or prior `#Top` was reused.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, condition `bare`, and
`semantics_mode = GENERATED_SEMANTICS`. The declared container paths resolve to
the mounted inputs. The required files and directories are real regular files
or real directories, not symlinks, and the mounts are read-only
([mount log](/audit-output/evidence/logs/39-readonly-mounts.log)).

The audit campaign lock has SHA-256
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching `/audit-input.json`, and its parsed JSON object is exactly equal to
the `audit_campaign` block. The independently checked hashes of
`/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, the trusted files, and every evidence file
listed by `generation-result.json` all match their records. The complete
structured trace has one regular JSONL file, 332 valid JSON lines, and no
malformed event. Counts and every digest are preserved in the
[provenance log](/audit-output/evidence/logs/01-provenance.log).

The independently reimplemented length-delimited safe-tree digest of
`/candidate` is
`19fbe222eac441c9cc3d6beafe115b45a9d14ab9eed79e11c92d1e4bdd704966`.
That exactly matches the retained workspace hash in both the selected
invocation and generation result. The corresponding trace-tree digest is
`c8f97ec9345a3757743ff34d5c119d154f162a6a71a357b5be8cd30ba7bedeb3`,
matching `usage.json`; the only trace file also matches its separately recorded
file digest. `/audit-input.json` additionally records opaque launcher package
digests for those two trees (`91a2...` and `d0ede...`) without declaring their
framing algorithm. I did not compare those opaque package values to a
different tree-hash algorithm; instead, I checked every constituent and the
layout-defined safe-tree/file hashes above. There is no missing, changed,
mistyped, linked, or unreadable provenance input.

For the generated-semantics boundary:

- `/reference/reference-semantics` is absent, as required.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`.
- Candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The generation output and trace claim successful construction and proof
  runs, but no such claim was accepted as proof evidence.

The candidate contains all required proof sources. `kore-exec.tar.gz` and
`__pycache__` are irrelevant generated/debug artifacts and were not copied
into the build.

Stage 1 result: integrity gate passed; no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for a nonempty list of positive integers, return the
greatest positive integer whose frequency in the list is at least that integer;
return `-1` if none exists. The trusted canonical implementation constructs a
frequency table and scans positive indices. The candidate instead initializes
`answer = -1`, scans each list value, and promotes it when
`lst.count(value) >= value` and it exceeds the current answer. Because every
in-domain value is positive, this different algorithm implements the same
contract.

Trusted regeneration used:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/candidate-src/solution.regenerated.mpy
cmp -s solution.mpy solution.regenerated.mpy
```

Both commands exited 0; the submitted and regenerated `.mpy` files are byte
identical ([regeneration](/audit-output/evidence/logs/02-regenerate-mpy.log),
[comparison](/audit-output/evidence/logs/03-mpy-byte-identity.log)).

The independent [differential script](/audit-output/evidence/differential_test.py)
loads the trusted canonical and candidate modules by separate paths. It checks:

- all three documented examples;
- singleton, just-below/equal/above frequency, outer-false and inner-false
  boundaries, competing qualifiers, all-ones, and a large absent value;
- every list of lengths 1–6 over values 1–5 (19,530 inputs);
- 2,000 deterministic random lists of lengths 1–80 over values 1–1000.

There were zero intended-domain mismatches
([full log](/audit-output/evidence/logs/04-differential.log)). The requested
empty case is outside the stated domain: the canonical raises `ValueError`,
whereas the candidate returns `-1`. This is documented but is not a narrowing
of, or divergence on, the source-contract domain.

Stage 2 result: program fidelity passed.

## 3. Clean proof reconstruction

The observed toolchain is K `v7.1.293` and Python `3.10.12`
([tool log](/audit-output/evidence/logs/05-toolchain.log)). Fresh output
definitions were placed only below `/tmp/audit-work/build`.

The generated semantics compiled from source with:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/semantic-llvm-kompiled
```

It exited 0
([log](/audit-output/evidence/logs/06-kompile-semantic-llvm.log)). Ten fresh
`krun` executions cover empty-loop, branch, frequency, and normal examples.
Every K result equals independent candidate Python; every nonempty result also
equals trusted canonical Python. Exact generated commands and outputs are in
the [concrete comparison log](/audit-output/evidence/logs/08-concrete-semantics.log).
An earlier reviewer regex failed to parse an otherwise correct `VInt(-1)`
output; that reviewer-script failure is retained in
`07-concrete-semantics.log` and was corrected before any conclusion.

The Haskell proof definitions and every positive target were independently
rebuilt/run:

| Target | Evidence | Result |
|---|---|---|
| compile raw `VERIFICATION-CORE` | [09 log](/audit-output/evidence/logs/09-kompile-verification-core.log) | exit 0 |
| raw loop connection claim | [10 log](/audit-output/evidence/logs/10-kprove-loop-lemma.log) | `#Top`, exit 0 |
| compile bridge-enabled `VERIFICATION` | [11 log](/audit-output/evidence/logs/11-kompile-verification.log) | exit 0 |
| example one | [12 log](/audit-output/evidence/logs/12-kprove-example-one.log) | `#Top`, exit 0 |
| example two | [13 log](/audit-output/evidence/logs/13-kprove-example-two.log) | `#Top`, exit 0 |
| example three | [14 log](/audit-output/evidence/logs/14-kprove-example-three.log) | `#Top`, exit 0 |
| universal functional claim | [15 log](/audit-output/evidence/logs/15-kprove-functional.log) | `#Top`, exit 0 |
| all entry claims together | [16 log](/audit-output/evidence/logs/16-kprove-all.log) | `#Top`, exit 0 |

Stage 3 result: clean reconstruction passed.

## 4. Adequacy and real-program pinning

The claims mean:

- `loop-invariant`: from an exact `loop("value", IS, searchLoopBody)` followed
  by the exact `return answer` continuation, with list `L`, accumulator `A`,
  and the three-entry environment, raw semantics reaches a cleared environment
  and result `scan(L, IS, A)`. It is universal in `L`, `IS`, `A`, and the
  overwritten previous loop value.
- `example-one`, `example-two`, and `example-three`: the literal documented
  input starts from `boot` and returns respectively `2`, `3`, and `-1`.
- `functional-correctness`: for arbitrary integer `H` and arbitrary finite
  `IntSeq T`, the exact program on nonempty `cons(H,T)` consumes computation,
  clears the environment, and returns
  `searchSpec(cons(H,T))`. There is no positivity precondition, so the theorem
  covers a strict superdomain of the required nonempty positive lists; it does
  not narrow the HumanEval domain.

The submitted `.mpy` program and the `searchProgram` term used by every claim
were separately parsed with the fresh core definition, macros expanded, and
emitted as KORE. `cmp -s` exited 0, and both files have SHA-256
`0c92a6a3345675feeec794a71198440fe9c957609a9bd3d987ae45dbbe8b170d`
([commands](/audit-output/evidence/logs/17-kast-solution-term.log),
[macro parse](/audit-output/evidence/logs/18-kast-claim-program-term.log),
[identity](/audit-output/evidence/logs/19-constructor-term-identity.log)).
This is constructor-level identity, not a similarity judgment.

All preconditions are satisfiable. The literal examples witness their claims.
For the universal entry, `H=1, T=.Ints` is a satisfying state and returns `1`.
For the loop claim, `L=IS=cons(1,.Ints), A=-1` and any previous integer
satisfy the start. Ground substitutions for seven distinct outcomes compare
the claimed `searchSpec`, a declarative frequency/max oracle, candidate Python,
and canonical Python; all agree
([script](/audit-output/evidence/claimed_result_ground.py),
[log](/audit-output/evidence/logs/36-ground-postcondition.log)).

The result is not free, existential, tautological, or constrained only by an
implication: the result cell changes from `noResult` to a specific `VInt` term,
and the false-result test in Stage 6 is rejected.

Stage 4 result: real-program pinning and result adequacy passed.

## 5. Rule-by-rule static soundness review

The exhaustive reviewer-authored
[inventory](/audit-output/evidence/rule-inventory.md) enumerates every local
syntax declaration, configuration cell, partial function, total function,
macro, ordinary rule, priority rule, and claim in `semantic.k`,
`verification-core.k`, `verification.k`, `loop-lemma-spec.k`, and `spec.k`.
There are:

- 14 syntax groups plus one configuration in `semantic.k`;
- four intentionally partial evaluator/projection functions and one total
  `count` function;
- 23 semantic rules;
- three exact program macros and seven macro/function equations in
  `verification-core.k`;
- four total mathematical functions (`promote`, `scan`, `searchSpec`,
  `positive`);
- one priority rule, the loop bridge;
- no local opaque/fresh symbols, `functional` declarations, simplification
  rules, or proof-only mathematical axioms.

Construct coverage is complete:

| Submitted constructor | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params` | syntax SD01/SD03/SD05; exact entry rule SR13 |
| statement lists | SD02; SR14–SR15 |
| `Assign` | SD05; SR16 |
| `For` | SD05; SR20–SR22 |
| `If` | SD05; SR17–SR19 |
| `Return` | SD05; SR23 |
| `Int`, `Name`, unary `-` | SD06; SR01–SR03 and SR07–SR08 |
| `Attribute`/`Call` for `list.count` | SD06–SD07; SR04, SR09, SR10–SR12 |
| `Compare >=` and `Compare >` | SD06, SD08–SD09; SR05–SR06 |

The semantics is deliberately a minimal integer-list subset. Missing behavior
for unused Python constructs is therefore not a defect. On the used,
well-typed constructs: expressions are pure; RHS lookup uses the pre-update
environment; statement and loop order are left-to-right; the input list is not
mutated; Python and K integers are both unbounded here; and the return rule's
abrupt continuation discard is correct for the modeled top-level function.
All five configuration cells are accounted for.

`count` is total because its equal and unequal head cases are disjoint and
exhaustive and recursion strictly shortens the list. `promote` uses a condition
and its Boolean negation, so its two rules are disjoint/exhaustive. `scan` and
`positive` split empty/nonempty constructors and structurally descend.
`searchSpec` is an unguarded definitional wrapper. No overlap permits
inconsistent results.

The only operational bridge is `BR01` in `verification.k`. Its full matched
context includes:

- the exact loop body and exact trailing `return answer`, with no `...` suffix;
- the complete `program`, `input`, exact three-binding `env`, and `result`;
- the only five cells in the configuration.

The bridge writes `.K`, clears the environment, and stores `scan`, exactly as
the fixed loop plus return is claimed to do. Its bridge-free universal
connection theorem imports `VERIFICATION-CORE`, not `VERIFICATION`. A
reviewer script removes only the `claim`/`rule` wrapper and priority attribute;
the complete remaining token streams are identical with the same SHA-256
([identity log](/audit-output/evidence/logs/35-bridge-claim-identity.log)).

Two ground full-program witnesses with distinct results (`[1] -> 1`,
`[2] -> -1`) were run under the raw core and bridge-enabled definitions. The
final KORE configurations are byte-identical in each pair
([qualifying comparison](/audit-output/evidence/logs/28-bridge-witness-qualifies-compare.log),
[rejecting comparison](/audit-output/evidence/logs/31-bridge-witness-rejects-compare.log)).

For operational/body sensitivity, I changed the executed loop comparison from
`>=` to `>` while leaving the `scan` summary unchanged. The mutated definition
compiled successfully, but the bridge-free connection proof exited 1 with
`WarnStuckClaimState` and the expected unmet `scan/promote` equality
([mutation](/audit-output/evidence/mutations/body-sensitivity/verification-core.k),
[build](/audit-output/evidence/logs/33-body-mutation-kompile.log),
[failed theorem](/audit-output/evidence/logs/34-body-mutation-kprove.log)).
Thus the connection theorem depends on the material body, not merely its name
or an external source file.

No inventoried local rule is unsound, so there is no asserted unsoundness for
which a false-conclusion witness is owed. In particular, `scan` is fully
equational rather than opaque, and BR01 is not an unconstrained result oracle.

Stage 5 result: static soundness gate passed.

## 6. Fresh non-vacuity test

No candidate mutation evidence was trusted. The fresh
[mutation](/audit-output/evidence/mutations/spec-vacuity-audit.k) changes the
documented first example's required result from true value `2` to false value
`3`. Its start state is plainly satisfiable.

The exact dry-run command successfully built the proof input and exited 0
([log](/audit-output/evidence/logs/37-vacuity-dry-run.log)). The actual proof
command then exited 1 with `WarnStuckClaimState`; its residual is a fully
terminated real program configuration containing `<result> VInt(2) </result>`,
which cannot meet the mutated `VInt(3)` destination
([log](/audit-output/evidence/logs/38-vacuity-false-proof.log)). This is the
expected unmet result obligation, not a parser error, timeout, missing import,
or unrelated crash.

Stage 6 result: non-vacuity passed.

## 7. Proven versus assumed accounting

What is machine-checked: under the candidate's generated K semantics, the exact
trusted-regenerated constructor program, on every nonempty finite K integer
list, partially-correctly returns the recursively defined
`searchSpec` result. The raw-semantics loop theorem establishes the exact
program-derived `scan` summary before that summary is admitted as a priority
rule. The three documented concrete results are also proved.

Trust and evidence ledger:

| Boundary | Influence | Accounting |
|---|---|---|
| K `v7.1.293`, Haskell/LLVM backends, reachability/circularity mechanism | proof execution and induction | Standard proof-engine trust boundary; freshly rebuilt and version-recorded. |
| Built-in K `INT`, `BOOL`, `MAP`, casts, and generated list syntax | arithmetic, guards, environment, parsing | Standard low-level semantics/math boundary; no task answer is encoded in it. |
| Trusted `py2mpy.py` | Python AST-to-constructor identity | Byte-verified and rerun; output is byte-identical, then constructor-identical to the claim term. |
| Generated `semantic.k` as a model of the used Python subset | value, control, environment, final result | Exhaustively reviewed for every used construct and concretely compared on boundaries/examples. This is not a universal machine-checked refinement theorem against CPython. |
| BR01 loop summary | control, environment, result | Not assumed: supported by a bridge-free universal K claim with exact context, plus ground and body-sensitivity checks. |
| Meaning of `searchSpec` as “greatest positive value with frequency at least itself” on positive lists | intent adequacy | Independent ordinary argument: every nonzero-frequency candidate occurs in the list; `scan` visits every occurrence; `promote` starts at `-1` and retains exactly the greatest qualifying visited positive value. Ground and differential evidence support but do not replace that argument. No separate K theorem states this declarative max characterization. |
| Trusted canonical differential oracle | empirical implementation bridge | Finite evidence only: 21,530 intended-domain cases with zero mismatch. It is not used to close any K claim. |

There are no local opaque values, fresh result symbols, unconstrained
interpretations, or assumed program-defined helpers. `positive` is unused, so
it has no dependents. Termination beyond what is inherent in finite `IntSeq`
execution is not claimed; the requested theorem is partial correctness.

Gate A (real-program soundness), Gate B (source-domain/intent adequacy), and
Gate C (trust/evidence auditability) all pass. I select the benchmark's
non-fatal-concern status rather than an unqualified pass because two bridges
remain outside the machine-checked theorem: the individually generated
Mini-Python-to-CPython refinement and the declarative “greatest qualifying
integer” characterization of the recursive `searchSpec` fold. Both are
transparent, narrowly scoped, independently reviewed, and strongly tested;
neither can make a false K conclusion provable or narrow the HumanEval domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
