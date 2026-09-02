# Independent adversarial audit: 66-digitsum

This is a completed audit of the immutable candidate under
`SUPPLIED_SEMANTICS`. The proof reconstructs successfully and is
result-constraining, but it proves the candidate's ASCII-only computation, not
the real HumanEval contract implemented by the trusted canonical function. The
concrete source-domain witness `"É"` must return `201`; the candidate and its K
postcondition return `0`. Under the benchmark's explicit mapping, this material
source-contract mismatch is `FAIL / NOT_LEGIT`, even though the narrower theorem
is internally sound.

## 1. Input and provenance integrity

### Launcher records

`/audit-input.json` declares:

- problem `66-digitsum`;
- condition `semantics`;
- record layout `legacy-selected-stage1`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- a mounted trusted semantics at `/reference/reference-semantics`.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, and the layout-required records
`invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the complete structured trace. `usage.json` is present and was
also inspected. The single trace file has 605 JSON lines and no parse errors.
Historical runtime metrics are absent, which is permitted for
`legacy-selected-stage1` and was not reconstructed.

The audit campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. The lock's independently calculated SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the launcher record. All launcher-recorded file hashes checked by the
reviewer match. The generation trace's actual SHA-256 is
`e0f30356b76aa6d9364ca94487f846bedbf964c36fb0fd65b9dbcd67d9c3ec3c`,
also equal to its manifest entries.

The candidate prompt and translator are byte-identical to their trusted
versions:

- prompt:
  `26e089859958a11b71b028884c146d360f5e2c079a59aeb4275b43b1f5f3e9ae`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

### Supplied-semantics integrity

The trusted semantics is present, as required for this mode. I compared the
candidate and trusted trees recursively by relative path, entry type, and file
content. There are no missing, additional, changed, mistyped, or symlinked
entries. There are no symlinks anywhere in the candidate. The independent
reviewer manifest digest for the matched semantics entries is
`9ab9aa657f6c8f60c1c225623047dc978d56547f60ebc6949d4d920a988262e3`.
That digest uses a reviewer-defined manifest format; the dispositive check is
the zero-problem entry/type/content comparison, not trust in a candidate tree
hash.

The old generation transcript claims `KPROVE_PASSED`; it was treated only as an
untrusted claim. Its complete structure, tool calls, successes, and earlier
stuck attempts were inspected but were not reused for reconstruction.

Evidence:

- [provenance checker](/audit-output/evidence/provenance_check.py)
  and [result log](/audit-output/evidence/stage1-provenance.log);
- [all mounted-input file hashes](/audit-output/evidence/stage1-mounted-input-hashes.log);
- [generation-record summary](/audit-output/evidence/stage1-generation-record-summary.log).

Stage 1 result: **PASS**. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

`/reference/prompt.py` asks for `digitSum(s)` on a string and says to sum the
codes of uppercase characters. The trusted `/reference/canonical.py` makes the
operative source behavior precise:

```python
return sum(ord(char) if char.isupper() else 0 for char in s)
```

Thus, for every Python `str` in the stated domain, the required value is
`sum(ord(c) for c in s if c.isupper())`. The empty string returns zero. The
contract does not restrict inputs to ASCII strings.

The candidate instead tests:

```python
if code >= 65 and code <= 90:
    result += code
```

That is equivalent only for ASCII uppercase letters. Initializing `char` and
`code` before the loop is result-inert, but replacing `str.isupper()` with the
65–90 interval is not.

### Trusted regeneration

In a clean scratch copy I ran:

```text
cd /tmp/audit-work/66-digitsum-audit
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited zero. The submitted and regenerated MPY files have the
same SHA-256,
`9f036b3d3f83e4e73cc0c82025b9d667307b1fe024f8cc2cb13c1a8aa6801c7b`.
See [the translation log](/audit-output/evidence/stage2-translation.log).

### Independent differential test

The reviewer test imports `/reference/canonical.py::digitSum` and the scratch
copy of the candidate entry point. It checks:

- all six documented examples;
- the empty string;
- code-point branch boundaries 64, 65, 66, 89, 90, and 91;
- representative ASCII and Unicode strings;
- 500 seeded generated ASCII strings;
- 500 seeded generated strings drawn from U+0000–U+07FF; and
- every single-character string from U+0000 through U+07FF.

The canonical function agreed with the independent contract oracle on all 3,070
cases. The candidate disagreed with the canonical function on 860 cases. The
smallest material witness used in the review is:

```text
input:       "É" (U+00C9)
isupper():   True
canonical:   201
candidate:   0
```

All documented examples and ASCII branch boundaries pass. That finite success
does not repair the Unicode-domain divergence.

Evidence:

- [differential script](/audit-output/evidence/differential_test.py);
- [complete bounded result log](/audit-output/evidence/stage2-differential.log).

Stage 2 result: **FAIL for real-program fidelity to the trusted contract**. This
is a material result divergence on the intended `str` domain.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied into
`/tmp/audit-work/66-digitsum-audit`. No candidate-built definition, cache,
`spec.json`, archive, or old trace was used. K is version 7.1.293; see
[the toolchain log](/audit-output/evidence/stage3-toolchain.log).

### Concrete definition

The following fresh LLVM build exited zero:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

An independently authored ASCII probe containing empty, example, boundary,
all-lowercase, and all-uppercase assertions ran to a final configuration with
`.K`, `NoExc`, and exit code 0. The submitted closure body visible in that final
configuration is the expected translated body.

A separate Unicode-literal probe intentionally failed with exit 113 at
`strToCodes("\xc3\x89")`. This is not a positive proof failure: the supplied
semantics explicitly guards literal decoding to codes below 128, while the
symbolic claims accept input directly as `str(S:IntSeq)`. It is retained as an
important language-model boundary.

Evidence:

- [runtime build](/audit-output/evidence/stage3-kompile-runtime.log);
- [ASCII probe source](/audit-output/evidence/k_runtime_ascii_probe.py)
  and [successful run](/audit-output/evidence/stage3-krun-ascii-probe.log);
- [Unicode probe source](/audit-output/evidence/k_runtime_probe.py)
  and [observed semantics limitation](/audit-output/evidence/stage3-krun-runtime-probe.log).

### Proof definitions and positive claims

The bridge-free Haskell definition was rebuilt from `verification.k` with main
module `DIGIT-SUM-VERIFICATION`. Both foundational claims then closed:

| Positive target | Definition | Result |
|---|---|---|
| `DIGIT-SUM-INITIALIZATION-SPEC` | `verification-kompiled` | `#Top`, exit 0 |
| `DIGIT-SUM-LOOP-SPEC` | `verification-kompiled` | `#Top`, exit 0 |

Next, `verification.k` was rebuilt with main module
`DIGIT-SUM-VERIFICATION-WITH-LOOP-LEMMA`, and the composed public claim closed:

| Positive target | Definition | Result |
|---|---|---|
| `DIGIT-SUM-ENTRY-SPEC` | `verification-with-lemma-kompiled` | `#Top`, exit 0 |

The exact commands and bounded outputs are preserved in:

- [base proof build](/audit-output/evidence/stage3-kompile-verification.log);
- [initialization proof](/audit-output/evidence/stage3-kprove-initialization.log);
- [loop proof](/audit-output/evidence/stage3-kprove-loop.log);
- [lemma definition build](/audit-output/evidence/stage3-kompile-with-lemmas.log);
- [entry proof](/audit-output/evidence/stage3-kprove-entry.log).

Stage 3 result: **PASS**. Every declared positive claim closes in a clean
reconstruction.

## 4. Adequacy and real-program pinning

### Claims in plain language

1. **Initialization claim.** Starting from a call of the exact one-parameter
   closure on symbolic `str(S)`, in the fixed empty module/builtins state, the
   semantics evaluates the call setup and three initial assignments. It reaches
   the actual `for` loop head with `result = 0`, `char = ""`, `code = 0`, the
   callee scope installed, and the caller frame saved.

2. **Loop claim.** Starting at the actual string-loop head on an arbitrary
   remaining sequence `S`, with integer accumulator `A`, exact return
   continuation, exact saved frame, empty heap, and arbitrary old `s`, `char`,
   and `code` local values, execution returns
   `A + digitSumSpec(S)` and restores the caller state.

3. **Entry claim.** Starting from the exact submitted closure applied to any
   `str(S)` in the fixed clean state, the returned value is exactly
   `digitSumSpec(S)`, with the fixed state restored.

There are no explicit `requires` clauses. Satisfying states plainly exist:

- entry/initialization: `S = .IntSeq` with the exact fixed maps and empty heap
  and stack shown in the claim;
- loop: `S = .IntSeq`, `A = 0`, `INPUT = str(.IntSeq)`,
  `OLDCHAR = str(.IntSeq)`, and `OLDCODE = 0`, with the exact saved frame.

### Mechanical pinning

The entry theorem directly constructs a closure rather than first executing the
entire `Module(FuncDef(...))`. This is permitted only if the binding and body
are mechanically the same. I parsed both the trusted-regenerated
`solution.mpy` and a `Module(FuncDef(..., digitSumBody))` reconstruction using
the fresh K definition with `--expand-macros --output json`. The resulting JSON
KAST files are byte-identical, both with SHA-256
`a472a340093fbda907f7cc84c12d76938dff3389c9a5e73dd49ea660d6f25120`.
This comparison also normalizes the one-argument `Call` and sequence syntax.

Evidence:

- [claim program term](/audit-output/evidence/claim_program.mpy);
- [solution parse](/audit-output/evidence/stage4-kast-solution.log);
- [claim-term parse](/audit-output/evidence/stage4-kast-claim-program.log);
- [constructor comparison](/audit-output/evidence/stage4-constructor-comparison.log).

The loop claim uses the same macro-expanded `digitSumLoopBody`, so its loop head
matches real control flow. This is a genuine body-sensitive theorem, not a
source-file-only association.

### Result constraint and concrete substitutions

`digitSumSpec` is exhaustive and terminating:

```text
digitSumSpec(.IntSeq) = 0
digitSumSpec(iCons(C, R)) =
  (if 65 <= C <= 90 then C else 0) + digitSumSpec(R)
```

The entry result contains no free result variable and is not an implication or
tautology. Ground configuration claims machine-check the formal values; the
reviewer then compares them with both Python implementations:

| Input | Formal `digitSumSpec` | Candidate Python | Trusted canonical |
|---|---:|---:|---:|
| `""` | 0 | 0 | 0 |
| `"abAB"` | 131 | 131 | 131 |
| `"É"` / `[201]` | 0 | 0 | 201 |

The ground claims print `#Top` and exit 0. The backend reports them as trivial
after frontend simplification, which is expected for these ground total
function terms. An earlier bare-functional-claim form was rejected because this
backend does not support functional claims; that unrelated failed form is
preserved and was not counted as evidence.

Evidence:

- [ground configuration claims](/audit-output/evidence/ground-spec.k);
- [ground proof](/audit-output/evidence/stage4-kprove-ground-values.log);
- [Python comparison](/audit-output/evidence/stage4-ground-compare.log);
- [unsupported discarded form](/audit-output/evidence/stage4-kprove-ground-functional-unsupported.log).

Stage 4 result: **program pinning and result constraint PASS; source-contract
adequacy FAIL**. The theorem exactly pins the submitted candidate but proves the
wrong human-facing property on non-ASCII uppercase inputs.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer inventory contains every local `configuration`, syntax sentence,
function/total/opaque declaration, context, rule, priority rule, and claim from
the supplied K tree, `verification.k`, and `spec.k`. It has 942 source
sentences:

- 928 supplied-semantics sentences;
- 11 proof-local declarations/rules in `verification.k`; and
- 3 reachability claims in `spec.k`.

The classified totals include 86 total-function declarations, 38 other
function declarations, 22 opaque/no-evaluator declarations, 430 ordinary
function or macro equations, 32 concrete equations, 209 ordinary operational
rules, 31 priority operational rules, 5 evaluation contexts, and 3 claims.
There are no local `[simplification]` rules. Each row records task relevance
and an audit decision. The 22 opaque declarations are fixed float, sort, or MD5
boundaries and are syntactically unreachable from this program and its claims.

See the [inventory generator](/audit-output/evidence/k_inventory.py) and
[complete inventory](/audit-output/evidence/k-rule-inventory.tsv).

### Used construct mapping

The material execution path consists of:

- exact closure call and parameter binding;
- left-to-right assignment and name lookup;
- empty string and integer literals;
- one-time evaluation of the `for` iterable;
- `IntSeq` string iteration and target binding;
- builtin `ord` on the yielded one-character string;
- integer `>=` and `<=`;
- short-circuit `and`;
- `if`;
- integer `AugAssign("+")`; and
- return, frame pop, and state restoration.

For every used construct, the declarations, dispatch rules, cell effects, and
audit result are enumerated in
[the used-construct map](/audit-output/evidence/used-construct-map.tsv).
Evaluation order and bindings are pinned by the exact scopes. The loop preserves
input order; `ord(str(iCons(C, .IntSeq)))` returns `C`; the two integer
comparisons implement precisely the candidate's 65–90 guard; and accumulator
addition is ordinary integer addition. No allocation, output, exception, or
mutable heap behavior is abstracted on this path.

The supplied semantics has an ASCII-only `strToCodes` rule. The only source
literal used by the submitted body is `""`, so that limitation does not
falsify the K theorem. It does, however, prevent treating concrete MPY
execution as a universal CPython-string bridge. The entry theorem introduces
symbolic input as `str(S)` directly.

### Proof-local declarations and equations

- `digitSumBuiltins` is a macro for the fixed builtins scope; only `ord`
  contributes to this proof.
- `digitSumLoopBody` and `digitSumBody` are exact constructor macros. The full
  body comparison in Stage 4 rules out a substituted program.
- `digitSumSpec` has disjoint base/cons equations, exhaustively covers
  `IntSeq`, and descends structurally. It truthfully summarizes the candidate's
  ASCII-threshold computation. It is not a truthful statement of the trusted
  canonical contract.
- There are no proof-local opaque symbols, fresh result oracles, or
  simplification axioms.

### Priority-20 operational bridges

The initialization and loop rules in
`DIGIT-SUM-VERIFICATION-WITH-LOOP-LEMMA` are operational bridges, so their
priority does not by itself justify them. Their justification is stronger:

1. each bridge's complete body is textually identical to its corresponding
   reachability claim, apart from `claim`/`rule`, label, and
   `[priority(20)]`;
2. each corresponding claim was independently proved using the base
   `DIGIT-SUM-VERIFICATION` definition, which does not import either bridge;
3. the bridge domains have the same exact continuation and all cells as those
   claims.

The initialization bridge is restricted to the exact empty caller
continuation, clean heap, fixed maps, and call body. The loop bridge is
restricted to
`#loop(...) ~> Return(...) ~> #endcall`, the exact saved
`frame(.K, 0, 1)`, clean heap, and fixed state. It does not accept an arbitrary
suffix, stack, heap, exception state, or output effect. Therefore its match
domain is not broader than its bridge-free theorem.

The hashes of normalized bridge/claim bodies match independently for both
bridges; see [the comparison script](/audit-output/evidence/bridge_compare.py)
and [log](/audit-output/evidence/stage5-bridge-comparison.log).

### Operational body sensitivity

I changed the actually executed `digitSumLoopBody` update from
`result += code` to `result += 1`, leaving `digitSumSpec` unchanged. The mutated
definition compiled successfully. Its loop theorem then exited 1 with
`WarnStuckClaimState` and the expected unmet obligation:

```text
A + 1 + digitSumSpec(R) = A + C + digitSumSpec(R)
where 65 <= C <= 90
```

For example, `C = 65`, `A = 0`, `R = .IntSeq` is a satisfying false witness.
This demonstrates sensitivity to the program term actually executed by the
claim.

Evidence:

- [mutated verification](/audit-output/evidence/verification-body-mutation.k);
- [mutated spec](/audit-output/evidence/spec-body-mutation.k);
- [successful mutation build](/audit-output/evidence/stage5-kompile-body-mutation.log);
- [expected failed connection proof](/audit-output/evidence/stage5-kprove-body-mutation.log).

I do not label any proof-local rule unsound: there is no false-conclusion
witness for those rules on their match domain. The decisive `"É"` witness is
instead an adequacy witness: it shows that a sound theorem about the candidate's
ASCII computation is not the requested theorem about the trusted source
contract.

Stage 5 result: **PASS for proof-theory soundness; FAIL remains for theorem
adequacy**.

## 6. Fresh non-vacuity test

The reviewer-authored `spec-vacuity.k` changes the public result obligation to
the universally false off-by-one result:

```text
digitSumSpec(S) +Int 1
```

The entry precondition is satisfiable; `S = .IntSeq` is a concrete witness, for
which the correct formal result is zero and the mutation requires one.

`kprove --dry-run` exited zero and emitted the `kore-exec` proof command, so the
mutation built and parsed successfully. The actual proof exited 1 with
`WarnStuckClaimState` on precisely:

```text
digitSumSpec(S) +Int 1 = digitSumSpec(S)
```

This is an reached, result-bearing residual, not a parser error, missing import,
timeout, or unrelated backend crash.

Evidence:

- [fresh mutation](/audit-output/evidence/spec-vacuity.k);
- [successful dry run](/audit-output/evidence/stage6-vacuity-dry-run.log);
- [expected proof failure](/audit-output/evidence/stage6-vacuity-proof.log).

Stage 6 result: **PASS**. The reconstructed theorem is non-vacuous and
discriminates false result obligations.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied MPY semantics, for every finite algebraic `IntSeq S`, if the
exact submitted one-argument closure is called in the claim's fixed clean state,
the execution characterized by the reachability proof returns:

```text
sum(C for C in S if 65 <= C <= 90)
```

and restores the fixed caller state. The loop theorem proves the analogous
suffix property for arbitrary integer accumulator `A`. This is a genuine,
unbounded symbolic theorem over `IntSeq`, not finite unrolling or example
checking. In Kit terminology it is a sound but intent-limited partial-correctness
result.

It does **not** establish:

```text
sum(ord(c) for c in Python_string if c.isupper())
```

for all Python strings. It also does not independently prove the full supplied
language semantics equivalent to CPython.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 prover and builtin Int/Bool/Map/List/String theories | all machine-checked claims | Necessary ordinary toolchain trust; version and fresh results recorded |
| Fixed supplied MPY semantics | program execution | Integrity verified; used rules are adequate for this candidate term, but the semantics is a documented subset and its literal decoder is ASCII-only |
| Trusted `py2mpy.py` translation | source-to-MPY identity | Candidate translator is byte-identical to trusted; fresh output is byte-identical to submission |
| Closure/body normalization instead of executing the whole module first | entry pinning | Acceptable: expanded constructor KAST is exactly identical |
| Initialization and loop operational bridges | composed entry proof | Acceptable: exact bridge-free universal claims close, match contexts exactly, and body sensitivity is demonstrated |
| `digitSumSpec` mathematical definition | final result | Formally defined and exact for the candidate; not an assumption, but materially mismatched to canonical Unicode uppercase behavior |
| Fixed opaque float/sort/MD5 symbols | none | All 22 are unreachable and cannot influence control, state, or result here |
| CPython `str.isupper` versus the 65–90 K/candidate guard | requested HumanEval result | **Illegitimate bridge**: it is false, with `"É"` as a concrete witness |
| Differential tests | source-contract comparison only | Finite evidence, not a proof; here it decisively refutes equivalence rather than being used to assert it |

### Gate and benchmark decision

- Real-program proof soundness (Kit Gate A): **PASS** for the exact submitted
  candidate.
- Intent adequacy (Kit Gate B): **FAIL** because the candidate and postcondition
  materially omit non-ASCII uppercase characters from the unrestricted Python
  `str` contract.
- Evidence auditability (Kit Gate C): **PASS**; commands, sources, positive
  proofs, body mutation, false-result mutation, and differential witnesses are
  preserved.

Kit would describe the reconstructed narrower theorem as
`SOUND-BUT-LIMITED`. The benchmark prompt expressly maps that status to
`FAIL / NOT_LEGIT` when the limitation materially narrows the HumanEval
source-contract domain. The `"É"` witness makes that mapping mandatory.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
