# Independent adversarial review: 18-how-many-times

The candidate cleanly reconstructs and its sole K claim is non-vacuous under
the candidate's generated semantics. It is nevertheless not a legitimate proof
of the real unrestricted Python program. The submitted implementation recurses
once per source-string position, actual CPython raises `RecursionError` on
satisfying inputs around the recorded limit of 1000, and the generated K
semantics instead has an unbounded call stack and returns the claimed integer.
That is a material source-contract/domain gap, not merely thin testing.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `18-how-many-times`, condition `bare`;
- `record_layout: legacy-selected-stage1`;
- `semantics_mode: GENERATED_SEMANTICS`;
- complete input provenance and no mounted reference semantics.

The rendered mode and mounts agree: neither
`/reference/reference-semantics` nor `/candidate/reference-semantics` exists.
No required entry in the candidate, trusted-reference, or generation-trace
trees is a symlink. All required candidate proof artifacts are real regular
files, and `prove.sh` is executable.

I read and parsed `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and all 193 JSONL records in
the structured trace. I also inspected the present legacy import records.
Historical runtime metrics are not required for this layout and were not
invented. The generation trace contains untrusted reports of intermediate
compiler errors, a backend crash, later `#Top`, and `KPROVE_PASSED`; none was
used as proof evidence.

The JSON object in `/audit-campaign-lock.json` is exactly equal to the
`audit_campaign` block, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every launcher-recorded per-file hash checked in the audit input and generation
result matches the mounted bytes. An independent canonical tree digest of
`/candidate` is
`f9caf4fcf4c18a75e2b69c8e0b72c0479a148f477b92430b3957c4e4fc1455d2`,
equal to both the generation result and retained-workspace record; the
structured trace tree digest likewise equals the usage record. Candidate
`prompt.py` and `py2mpy.py` are byte-identical to their trusted mounts.

Evidence:

- `evidence/00-generation-records.log`
- `evidence/01-integrity.log`
- `evidence/integrity_check.py`
- `evidence/generation_record_summary.py`

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks `how_many_times(string, substring)` to return the
number of starting positions at which `substring` equals the corresponding
slice of `string`, including overlapping positions. The canonical loop tests
exactly the indices in
`range(len(string) - len(substring) + 1)`. Consequently an empty pattern occurs
`len(string)+1` times.

The candidate implements the same recurrence in ordinary Python:

1. empty pattern: `len(string)+1`;
2. source shorter than a nonempty pattern: `0`;
3. otherwise count the current prefix if equal and recurse on `string[1:]`.

Trusted regeneration produced SHA-256
`f0a019c02b875920d0a9f35a504e27897d27548f3d0586189b0d64513b361fb5`
for both the regenerated and submitted `solution.mpy`; `cmp` exited 0
(`evidence/02-regenerate-mpy.log`).

The independent differential script used the trusted canonical as oracle and
tested:

- all three documented examples;
- empty source/pattern, equal-length match/nonmatch, shorter-source, overlap,
  nonmatch, NUL, and Unicode boundaries;
- every source over `{a,b}` through length 6 against every pattern through
  length 4;
- 2,000 seeded ASCII/Unicode generated pairs;
- five recursion-stress inputs through source length 1200.

There were zero ordinary-value mismatches before the recursion boundary, but
four material mismatches among 5,938 unique pairs:

| Input | Trusted canonical | Submitted Python |
|---|---:|---|
| `"a"*1000, "b"` | `0` | `RecursionError` |
| `"a"*1100, "b"` | `0` | `RecursionError` |
| `"a"*1100, "a"` | `1100` | `RecursionError` |
| `"ab"*600, "ab"` | `600` | `RecursionError` |

The recorded Python recursion limit was 1000. The prompt and type annotation
contain no input-length restriction. Thus this is a divergence on the intended
unrestricted `str × str` domain. The exact script, generated-input method,
outcomes, and nonzero mismatch exit are in
`evidence/differential_test.py` and `evidence/03-differential-python.log`.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work`, used no candidate-built
definition or cache, and used K 7.1.293:

- fresh LLVM build of `semantic.k`: exit 0;
- fresh Haskell build of `verification.k`: exit 0;
- the sole positive target claim selected by
  `--claims SPEC.how-many-times-correct`: exit 0 and exact output `#Top`.

Evidence:

- `evidence/04-tool-versions.log`
- `evidence/05-kompile-semantic-llvm.log`
- `evidence/09-kompile-verification-haskell.log`
- `evidence/10-kprove-positive.log`

Fresh concrete execution covered all material submitted constructors and both
sides of every branch. Eight normal/boundary programs all exited 0 with the
same integers as Python (`evidence/06-concrete-semantics.log`). A raw K
non-BMP-string test returned `2` for three emoji against two emoji
(`evidence/08-unicode-k-string.log`). The trusted translator separately emits
UTF-16 surrogate escapes for such a Python literal, which the K scanner rejects
(`evidence/07-unicode-translator-gap.log`); the submitted module itself contains
no non-BMP literal, so this is an additional bridge limitation rather than the
main failure.

Most importantly, fresh K execution of the trusted translation of
`how_many_times("a"*1000, "b")` exited 0 with `intVal(0)`
(`evidence/17-long-input-k-semantics.log`), exactly where the real submitted
Python raises. Clean reconstruction therefore confirms both the candidate's
reported `#Top` and the semantic substitution that makes it possible.

## 4. Adequacy and real-program pinning

The sole entry claim has no `requires`. In plain language its precondition is:

- arbitrary K strings `S` and `T`;
- an arbitrary continuation `CONT`;
- an arbitrary caller environment `_ENV`;
- a singleton functions map binding `"how_many_times"` to the constructor body
  shown in the claim.

Its postcondition is:

- the invocation is replaced by `intVal(overlapCount(S,T))`;
- the identical continuation follows;
- the functions map and caller environment are unchanged.

This is result-constraining: `overlapCount` is a defined function, not a fresh
right-hand variable or oracle. A satisfying state is obtained with
`S="aaaa"`, `T="aa"`, `CONT=.K`, `_ENV=.Map`, and the displayed binding.
Ground substitution gives:

- `overlapCount("aaaa","aa") = 3`;
- `overlapCount("","") = 1`;
- `overlapCount("abc","z") = 0`.

The K frontend reduces all three ground claim results, while an independent
direct slice-count, the canonical Python, and candidate Python all give the
same values on these witnesses (`evidence/15-witness-python.log` and
`evidence/16-overlap-witness-kprove.log`).

Real constructor-body pinning is strong. A reviewer script extracted the
function term actually bound in `spec.k`, normalized only the three explicit
`.Stmts` list units to concrete empty-list syntax, parsed both it and submitted
`solution.mpy` with the fresh definition, and compared complete KAST JSON. Both
constructor hashes are
`08eee53f3b885ab0e637fd92d051f3f8fbfeebfe27fd77555cfad15739c8989e`
and the ASTs are equal (`evidence/11-constructor-pinning.log`).

A body-sensitivity mutation changed the empty-pattern constant in the executed
claim body from `1` to `2`, leaving the result specification unchanged. It
parsed successfully and failed with `WarnStuckClaimState` on the expected
obligation
`lengthString(S)+1 = lengthString(S)+2` under `T=""`
(`evidence/13-body-sensitivity.log`).

The fatal pinning gap is below the constructor level: the K `invoke` is not a
faithful execution model of the real recursive Python call on the full claimed
domain. The formal precondition permits the length-1000 witness, but the K
configuration has no recursion-depth/exception component and produces a normal
integer where CPython terminates exceptionally. It therefore pins the submitted
body only in an idealized unbounded-stack language, not the real generated
program required by the benchmark.

## 5. Rule-by-rule static soundness review

The exhaustive declaration and rule inventory is
`evidence/RULE-INVENTORY.md`; the numbered source extraction is
`evidence/12-lexical-inventory.log`.

Inventory totals:

- all local syntax productions for `Module`, the statement/expression
  constructors, generated list sorts, values, functions, return markers, and
  15 control frames;
- one configuration with `<k>`, `<functions>`, and `<env>`;
- 35 ordinary semantic rules;
- one proof-local `[function]`, `overlapCount`, with four equations;
- one entry reachability claim;
- no local `[total]`, `[functional]`, `[simplification]`, `[concrete]`, opaque,
  priority, or auxiliary-claim extension.

Every constructor used by `solution.mpy` maps to syntax and an exercised rule:
`Module`, `FuncDef`, `If`, `Return`, expression statement, `Int`, `Str`,
`Name`, integer `BinOp("+")`, string equality, integer less-than, `len`, the
two actual slice shapes, and the two-argument recursive call. The rules preserve
left-to-right operand/argument evaluation, use a fresh two-parameter call
environment, save and restore the caller map, and propagate return through the
remaining statement list before popping the call frame. The two Boolean branch
rules are complementary. The two return-discard rules can overlap on a
singleton list but have identical results. No local operational bridge rewrites
program execution to `overlapCount`.

The four `overlapCount` equations are truthful, disjoint, exhaustive on K
strings, and descending:

1. empty pattern gives `length(S)+1`;
2. a longer nonempty pattern gives zero;
3. an equal current prefix gives one plus the tail count;
4. a different current prefix gives the tail count.

In recursive equations 3/4, the guards imply
`length(S) >= length(T) >= 1`, so `S[1:]` is strictly shorter. This is a
definitional mathematical summary, not an unconstrained result-bearing
abstraction.

The semantic rules special-case the names `len` and `how_many_times` instead of
implementing general Python resolution. That is over-broad as a reusable
Python semantics but does not enable a false conclusion for this pinned body,
which cannot shadow either name. I therefore do not label those equations
unsound on the submitted path.

The call subsystem at `semantic.k:109-131`, together with the absence of a
stack/exception cell, is materially unsound as a model of the actual submitted
CPython execution over the claim's full domain. The required false-conclusion
witness is concrete:

```text
S = "a" repeated 1000 times
T = "b"
formal/K conclusion = intVal(0)
trusted canonical = 0
submitted Python = RecursionError
```

This is not speculation about an isolated rule: the same translated body and
input were executed under the fresh LLVM definition and under Python, with the
opposite observable outcomes recorded in stages 2 and 3. The generated
semantics silently fabricates a normal result for an actually used control
effect it does not model.

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created a fresh
`SPEC-VACUITY` in scratch with the identical executed body and changed only the
result obligation from:

```k
intVal(overlapCount(S,T))
```

to:

```k
intVal(overlapCount(S,T) +Int 1)
```

The mutation is false for the satisfying witness `S=""`, `T=""`: the real
result and `overlapCount` are `1`, while the mutation demands `2`. `kprove`
accepted and compiled the spec, reached the backend, exited 1, and emitted
`WarnStuckClaimState` with the expected failed implication
`lengthString(S)+1 = lengthString(S)+2` under `T=""`. This is a semantic proof
failure, not a parser error, timeout, or unrelated crash
(`evidence/14-false-postcondition.log`). The original formal claim is therefore
non-vacuous and result-sensitive.

## 7. Proven versus assumed accounting

What the successful K proof establishes precisely is conditional:

> Under the candidate's idealized `SEMANTIC` transition system, for every K
> String pair, arbitrary continuation, and arbitrary caller map, invoking the
> exact submitted constructor body reaches the integer defined by
> `overlapCount`, with the continuation, function binding, and caller map
> preserved.

Formally established within that system:

- normal execution of the exact constructor body, not a replacement body;
- the recursive reachability argument via the guarded target circularity;
- preservation of continuation and caller environment;
- equality of the returned K integer with the four-equation recurrence;
- non-vacuity and body sensitivity.

Trusted or informal boundaries:

- K 7.1.293's compiler, Haskell prover, LLVM interpreter, reachability logic,
  and generated parsers;
- imported K hooks for unbounded integers, Booleans, Strings
  (`lengthString`, `substrString`, equality), Maps, and K sequencing;
- the trusted translator and the independently checked constructor identity;
- the ordinary mathematical interpretation of the four-equation recurrence as
  overlapping occurrence count, supported by direct-count and differential
  evidence but not by a separate theorem against the canonical loop;
- Python/K Unicode correspondence, with a successful raw-K non-BMP example but
  a documented trusted-translator literal-encoding gap;
- critically, the candidate assumes an unbounded, exception-free call stack.
  That assumption affects control and the final result domain, is contradicted
  by the length-1000 witness, and is illegitimate for a theorem presented as
  covering the real unrestricted generated program.

Gate A fails at real-program semantic fidelity despite the internally sound
abstract proof and successful negative probes. Gate B also fails because the
HumanEval contract has no length bound while the submitted Python ceases to
return an integer at ordinary finite lengths. Gate C evidence is reproducible,
but it cannot repair those failures. Under the benchmark's explicit mapping, a
material narrowing of the unrestricted source-contract domain is
`FAIL / NOT_LEGIT`, even if described generically as sound-but-limited.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
