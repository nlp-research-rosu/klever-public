# Independent adversarial review: HumanEval 14 `all_prefixes`

The candidate's two K claims do reconstruct to `#Top`, and the proof is
non-vacuous and body-sensitive. It is nevertheless not a legitimate proof of
the real Python program over its stated `str` domain. The individually
generated semantics interprets K strings bytewise: for the valid Python input
`"🙂"`, it proves/executes four byte prefixes instead of the single Python
prefix `"🙂"`. This is a material source-domain/model mismatch, for which the
benchmark's decision rule requires `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `14-all-prefixes`, condition `bare`;
- semantics mode `GENERATED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance; and
- no mounted reference semantics.

I read the launcher-owned input, campaign lock, `/run.json`, `/task.json`,
`/generation-result.json`, and every record required for this layout:
`invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, the complete 280-record structured trace, and the present
`usage.json`. Historical `runtime-metrics.json` is absent, which is explicitly
permitted for this legacy-selected layout.

The campaign-lock JSON is exactly equal to the `audit_campaign` block, and its
SHA-256 is the value recorded in `/audit-input.json`. Independently computed
digests match for all mounted regular files named by the audit input. The trace
file digest matches both the invocation and stage result. Using the pipeline's
tree-digest implementation, the mounted trace matches the digest recorded by
`usage.json`, and the candidate tree matches the workspace digest recorded by
both `invocation.json` and `/generation-result.json`. The two launcher
audit-packaging tree digests in `/audit-input.json` use a distinct tree scheme;
the content-level and pipeline-level provenance links above independently bind
the actual mounted inputs. All required records and candidate proof artifacts
are real regular files, and the candidate tree has no symlink or special entry.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. As required for
`GENERATED_SEMANTICS`, `/reference/reference-semantics` does not exist. There is
no infrastructure contradiction or missing launcher record.

Generation prose, logs, and the prior `KPROVE_PASSED` marker were treated only
as untrusted claims. A complete structural pass found no malformed trace
record. Evidence:

- `evidence/00-toolchain.log`
- `evidence/01-provenance.log` and `evidence/provenance_check.py`
- `evidence/01b-generation-record-summary.log` and
  `evidence/generation_record_summary.py`

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract is: for an input Python string, return a list containing
every nonempty prefix, ordered from length one through the full string. Thus
`"abc"` maps to `["a", "ab", "abc"]`, and the empty string maps to `[]`.
Neither the prompt nor type annotation restricts strings to ASCII.

The trusted canonical implementation iterates `i = 0 .. len(string)-1` and
appends `string[:i+1]`. The candidate uses the equivalent loop `i = 1` while
`i <= len(string)`, appending `string[:i]`, then incrementing `i`. This is
correct over Python's full `str` domain.

Fresh translation with the trusted `/reference/py2mpy.py` produced a file
byte-identical to submitted `solution.mpy`:

```text
c0ecfda3a494d3a984bae3c41e23a58eb8d3eae4517868f08341afbe4419a5f6
```

The independent differential script imports the trusted canonical and
candidate entry points and also compares an independently constructed prefix
list. It exercised 80 documented, empty, one-iteration, multi-iteration,
long, escaped, NUL, combining-character, non-ASCII, emoji, and deterministic
generated inputs. There were zero Python-level mismatches. The complete inputs,
seeded generator, command, digest, result, and exit status are in:

- `evidence/differential.py`
- `evidence/02-regeneration.log`
- `evidence/03-differential.log`

These finite tests support source-implementation fidelity; they do not validate
the generated K semantics.

## 3. Clean proof reconstruction

I copied source artifacts only to `/tmp/audit-work/rebuild`, ignored the
candidate `__pycache__`, archive, and any prior build claim, and created all
definitions under new `*-fresh-kompiled` paths.

Fresh commands and outcomes:

| Purpose | Evidence | Outcome |
|---|---|---|
| Compile generated semantics (Haskell) | `evidence/04-kompile-semantic.log` | exit 0 |
| Concrete empty input | `evidence/05-krun-empty.log` | `[]`, exit 0 |
| Concrete one-character ASCII | `evidence/06-krun-a.log` | `["a"]`, exit 0 |
| Concrete documented example | `evidence/07-krun-abc.log` | `["a","ab","abc"]`, exit 0 |
| Compile proof definition | `evidence/10-kompile-verification.log` | exit 0 |
| Prove the only loop claim | `evidence/11-kprove-loop.log` | `#Top`, exit 0 |
| Compile definition with proved lemma | `evidence/12-kompile-verified-lemma.log` | exit 0 |
| Prove the only entry claim | `evidence/13-kprove-entry.log` | `#Top`, exit 0 |

The positive proof reconstruction therefore succeeds.

Generated-semantics reconstruction fails the required Python comparison on
ordinary valid Unicode strings:

- Python `all_prefixes("🙂")` is `["🙂"]` because Python indexes Unicode code
  points.
- Fresh K execution returns four elements:
  `"\xf0"`, `"\xf0\x9f"`, `"\xf0\x9f\x99"`, and
  `"\xf0\x9f\x99\x82"`.
- For `"a🙂b"`, Python returns three prefixes, while K returns six byte
  prefixes.

The full configurations are in `evidence/19-krun-emoji.log` and
`evidence/08-krun-unicode.log`. The explicit cross-runtime comparison is
`evidence/14-semantic-python-compare.log` with its source in
`evidence/semantic_python_compare.py`; it records two mismatches and exits 1.
The reviewer-created inputs are preserved as `evidence/run-emoji.mpy` and
`evidence/run-unicode.mpy`.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim says: given the exact submitted loop and exact suffix
`return result; restore caller`, an environment containing input `S`, an
abstract list of the first `N` K prefixes, and `i=N+1`, where
`0 <= N <= lengthString(S)`, running the remainder restores the old environment
and yields all K prefixes of `S`.

Its precondition is satisfiable; for example:

```text
S = "abc", N = 0, I = 1, OLD = emptyEnv
```

The entry claim says: from empty variable and function environments, execute
the embedded submitted module, call `all_prefixes(S)`, restore the empty
variable environment, and return exactly
`listVal(allPrefixes(S))`. Its only condition,
`0 <= lengthString(S)`, is satisfiable and effectively universal. `S=""`,
`S="abc"`, and `S="🙂"` are concrete satisfying inputs.

### Program identity

The `<k>` term begins with `Run(solutionProgram, Call(...))`.
`solutionProgram` expands to the complete submitted function binding and body.
Fresh trusted translation plus the simple embedding generator reproduced
submitted `solution-program.k` byte-for-byte, with digest:

```text
3eaf083860f0ff3d0517ace61d36dd3ed5095d465320dca7a8fc859b9a5cd19a
```

See `evidence/09-program-embedding.log`. The typing-only import is the only
discarded source effect, and that is semantically inert here. Every material
assignment, loop guard, append, slice, increment, and return appears in the
executed term.

The prioritized loop rule is not an unconstrained oracle. It is the
`N=0,I=1` specialization of the independently proved `loop-spec.k` theorem,
which was proved in a definition that did not contain the later bridge. Its
continuation, environment, restored state, and arbitrary preserved function
environment agree with the bridge's complete match.

The result is constrained, not free: the false mutation
`all_prefixes("a") => []` stops at `listVal(pacc("a",1))`. In addition, changing
the actual embedded initializer from `i=1` to `i=2` made the theorem fail on
`"a"` at `listVal(vnil)`. The changed body term, build, claim, and residual are
preserved in `evidence/body-mutation-verification.k`,
`evidence/body-mutation-spec.k`, and logs 15-16.

Ground substitution exposes the adequacy boundary:

| `S` | Claimed/K result | Both Python implementations |
|---|---|---|
| `""` | empty list | empty list |
| `"abc"` | `"a","ab","abc"` | `"a","ab","abc"` |
| `"🙂"` | four UTF-8 byte prefixes | one prefix, `"🙂"` |

Thus the claim pins the submitted constructor body, but not that body's real
Python Unicode behavior.

## 5. Rule-by-rule static soundness review

The exhaustive declaration/rule inventory is
`evidence/rule-inventory.md`, supported by the literal scan in
`evidence/20-static-declaration-scan.log`. It enumerates:

- every syntax production;
- all value, environment, function, and control declarations;
- all 39 rules in `semantic.k`;
- all proof-local functions, ordinary rules, simplification rules, claims,
  opaque terms, and the sole priority rule; and
- a constructor-to-rule map for every construct in `solution.mpy`.

There are no local `[total]` or `[functional]` declarations. Partial helpers
stop visibly outside their modeled types/shapes. The used environment lookup,
updates, sequencing, integer operations, loop control, function installation,
argument binding, restoration, and final return are faithful for this
alias-free program. Modeling `append` as replacement of the sole list variable
is adequate because the list is freshly allocated, never aliased, and append's
return value is discarded. Unused syntax lacks rules in places, which is
acceptable in generated-semantics mode.

The proof-local `pacc` base and append-step define the loop accumulator.
`allPrefixes(S)` reduces to `pacc(S,lengthString(S))`. Positive `pacc` remains
an irreducible abstract result term, but its base/step equations constrain its
recursive meaning; it is not a free RHS variable. The step simplification's
guard is broader than the invariant domain, so reuse for negative or
out-of-range `N` would need a clearer definition or narrower guard. I do not
label those unspecified cases unsound without a false conclusion witness.

The exact operational bridge in `verified-lemma.k` preserves the only
observable cells and exact continuation, and its supporting proof is
bridge-free and at least as general. The body-sensitivity test confirms that it
does not silently summarize a materially changed program.

### Materially unsound Python-semantics rules and witnesses

Two used generated rules make false conclusions about the real Python
operations:

1. `semantic.k:102`:
   `lenVal(strVal(S)) => intVal(lengthString(S))`.

   False-Python witness on the intended domain: `S="🙂"`. CPython and the
   trusted canonical use length 1; K `lengthString` causes four loop
   iterations.

2. `semantic.k:104`:
   `prefixVal(strVal(S),intVal(I)) =>
   strVal(substrString(S,0,I))`.

   False-Python witness on the intended domain: `S="🙂", I=1`. Python slicing
   yields `"🙂"`; fresh K execution yields `"\xf0"`.

Rules 90 and 93-94 route the actual submitted `len` call and slice through
those primitives, so the defect is reachable, result-bearing, and not an
unused language gap. The whole-program false conclusion is the four-element K
result in `evidence/19-krun-emoji.log`. This is not merely a display encoding:
the K list has four `strVal` elements and the loop count differs from Python's
one.

## 6. Fresh non-vacuity test

I created a new ground mutation, separate from candidate artifacts:

```k
Run(solutionProgram, Call(Name("all_prefixes"), Str("a")))
  => listVal(vnil)
```

The initial environments are empty, so the precondition is realizable, and the
obligation is demonstrably false because both Python implementations return
`["a"]`.

`kprove --dry-run` parsed and built the mutation successfully (exit 0;
`evidence/17-vacuity-dry-run.log`). The actual proof exited 1 with
`WarnStuckClaimState`; its reachable residual is
`listVal(pacc("a",1))`, which does not unify with the false empty-list target
(`evidence/18-kprove-vacuity.log`). This is the expected unmet result
obligation, not a parser error, timeout, missing import, or unrelated crash.
The mutation is preserved in `evidence/spec-vacuity.k`.

Non-vacuity passes, but it only shows that the K theorem discriminates its own
postcondition. It does not repair the Unicode semantics mismatch.

## 7. Proven versus assumed accounting

### What the successful proof establishes

Conditional on K 7.1.293, its Haskell backend, the imported built-ins, and the
candidate's generated semantics, the reachability proof establishes partial
correctness of the exact embedded constructor program: for any K `String` `S`,
if execution terminates, it restores the caller variable environment and
returns the abstract K value
`listVal(pacc(S,lengthString(S)))`. The loop theorem establishes the recursive
accumulator step, and the exact proved specialization supplies the entry proof.

It does not establish that K `lengthString`/`substrString` implement Python
`len` and slicing for all Python strings. Fresh execution disproves that
necessary bridge.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted translator `/reference/py2mpy.py` | Program identity | Acceptable; regenerated output is byte-identical. |
| K parser, kompiler, KORE engine, Haskell backend | All proof closure | Standard low-level proof trust boundary. |
| Imported `INT`, `BOOL`, `K-EQUAL` primitives | Arithmetic and guards | Acceptable for used unbounded integer/Boolean behavior. |
| Imported `STRING` `lengthString`/`substrString` | Loop count, every prefix, final result | Acceptable as K byte-string primitives, but illegitimate as an unqualified Python-`str` bridge; concrete witnesses refute equivalence. |
| Candidate environment/control rules | Binding, state, call/return | Statically adequate for every path of this submitted body. |
| `pacc` and `allPrefixes` summaries | Final postcondition | Base/step constrained within the invariant; describe the K result, not independently the Python Unicode result. |
| Proved loop-to-result operational bridge | Replaces loop execution in entry proof | Acceptable within the candidate semantics: exact context, preserved cells, bridge-free general theorem, and body sensitivity. |
| Python differential tests | Candidate versus canonical source behavior | Finite empirical support only; 80 cases, zero mismatches. |
| K concrete tests | Generated semantics versus Python | Decisive counterevidence: ASCII agrees, Unicode does not. |

Under the Kit gates, the proof extensions and non-vacuity checks are sound
inside the candidate K model, but intent/language adequacy fails on an
unrestricted material part of the HumanEval `str` domain. This is
`SOUND-BUT-LIMITED` only in generic Kit terminology. The benchmark explicitly
maps material source-domain narrowing of this kind to `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
