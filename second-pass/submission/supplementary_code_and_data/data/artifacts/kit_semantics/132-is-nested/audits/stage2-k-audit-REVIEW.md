# Independent adversarial review: 132-is-nested

The candidate contains a legitimate partial-correctness proof of the submitted
program for the full source-contract domain. I reconstructed the proof from
source under the trusted supplied semantics, audited the proof-local theory,
mechanically pinned the entry claim to regenerated `solution.mpy`, and rejected
a fresh false result obligation for a satisfying input.

## 1. Input and provenance integrity

The launcher record `/audit-input.json` declares:

- `record_layout = pipeline-v3`
- `problem_id = 132-is-nested`
- `condition = kit-semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`
- the mounted paths used in this review, distinct from its host-only provenance
  paths.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` is present. No infrastructure breach was
found.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required JSON/text/log record
under `/generation-evidence`, and all 313 JSONL events in the structured trace.
The generation records were treated only as untrusted claims. The trace
inventory records 44 tool calls and the candidate's ultimate `VALIDATED`
assertion; none was used as proof of correctness.

Independent integrity results:

- The campaign-lock JSON is exactly equal to the `audit_campaign` block. Its
  SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the launcher-recorded value.
- The direct SHA-256 values of `/run.json`, `/task.json`,
  `/generation-result.json`, invocation, metrics, runtime metrics, usage,
  generation prompt, generation last/output, trusted prompt, translator, and
  canonical implementation all match their recorded values.
- The sole trace file hashes to the value recorded by the invocation:
  `ec2c8dc404fd9f276b58c3bb4251e84de45c7181a873578689a78eb9c2784f93`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- A recursive type/path/content comparison between candidate and trusted
  `reference-semantics/` found zero missing, additional, changed, mistyped, or
  symlinked entries. Both trees contain the same 24 regular files.
- No symlink occurs anywhere in the candidate, trusted reference, or generation
  evidence trees. All required candidate proof artifacts are readable regular
  files.
- An independent per-file snapshot hashes all 771 candidate files and all 24
  trusted semantics files. This supplements, rather than assumes, the
  launcher's aggregate-tree hashes.

Evidence:
[stage1_integrity.log](evidence/stage1_integrity.log),
[trace_inventory.py](evidence/trace_inventory.py),
[mounted_tree_hashes.log](evidence/mounted_tree_hashes.log),
[candidate_file_sha256.txt](evidence/candidate_file_sha256.txt), and
[trusted_semantics_file_sha256.txt](evidence/trusted_semantics_file_sha256.txt).

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For a string containing only `[` and `]`, `is_nested` must return `True` iff
there is a valid bracket subsequence with nesting. Under the canonical
implementation and examples, this is exactly the existence of four positions
in increasing order containing `[`, `[`, `]`, `]`. The selected characters
form `[[]]`; conversely, any valid bracket subsequence with a nested pair
contains an outer open, inner open, inner close, and outer close in that order.

The trusted canonical implementation collects opening positions and reversed
closing positions and returns whether at least two can be paired in order. The
candidate implements the equivalent four-state subsequence recognizer:

- states 0 and 1 consume opening brackets;
- states 2 and 3 consume closing brackets;
- state 4 is accepting and absorbing.

This is a different but contract-equivalent algorithm.

### Translation identity

In the isolated scratch tree I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`1436315c5fd2725fed7f0263fc7712c265e8be7c89dc237ff79afe0126448ed6`.
Thus the submitted `.mpy` is exactly the trusted translator's output for the
submitted Python.

### Independent differential execution

`evidence/differential_test.py` imports the trusted canonical entry point and
the candidate entry point independently. It also uses a separately implemented
four-index definition oracle. It checks:

- all six documented examples;
- empty and explicit recognizer branch-boundary cases;
- every one of the 8,191 bracket strings of lengths 0 through 12;
- 104 deterministic generated inputs of lengths 13 through 128.

There were 8,295 unique inputs, corpus SHA-256
`7f7bb8172575a3d4a2a73a3aa8dc3ad55cc95394a17a9655bc3380bee7a75ed4`,
and zero canonical/candidate/definition discrepancies. This is finite
fidelity evidence, not a substitute for the symbolic K proof.

Evidence:
[stage2_fidelity.log](evidence/stage2_fidelity.log) and
[differential_test.py](evidence/differential_test.py).

## 3. Clean proof reconstruction

I copied only source artifacts to
`/tmp/audit-work/132-is-nested-review`. Candidate `runtime-kompiled`,
`verification-kompiled`, caches, and bytecode were not copied or used. The
supplied semantics in scratch came from the trusted `/reference` tree.

Fresh commands and results:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-fresh
```

Exit 0. The warnings are supplied-semantics non-exhaustiveness or unused-variable
warnings and do not involve the target path.

```text
krun auditor_concrete_tests.mpy --definition runtime-kompiled-fresh
```

Exit 0 with `.K`, `NoExc`, and exit code 0. Before translation, an AST check
established that the function in the reviewer-authored concrete test is
identical to candidate `solution.py`.

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-fresh
```

Exit 0.

```text
kprove spec.k --definition verification-kompiled-fresh \
  --spec-module SPEC --claims SPEC.loop
```

Output `#Top`; exit 0.

```text
kprove spec.k --definition verification-kompiled-fresh \
  --spec-module SPEC
```

Output `#Top`; exit 0. The complete-module command proves both positive claims
and makes `SPEC.loop` available as the circularity required by `SPEC.program`.
Thus each positive target was independently exercised from fresh sources.

Evidence:
[stage3_reconstruction.log](evidence/stage3_reconstruction.log),
[run_stage3.sh](evidence/run_stage3.sh), and
[auditor_concrete_tests.py](evidence/auditor_concrete_tests.py).

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop` says: in the exact plain function frame, for any bracket-only
remaining string `CS` and any recognizer state `S` between 0 and 4, executing
the actual translated loop changes local `state` to `nestedScan(CS,S)`.
`bracket` may become the last iterated character, while `string`, the
continuation, outer scopes, and all omitted cells are framed. The submitted
body has no return, exception, break, continue, heap, allocation, or output
inside the loop, so its arbitrary continuation framing introduces no control
shortcut.

`SPEC.program` says: for every finite `IntSeq CS` whose elements are exactly
91 or 93, start from the fresh module configuration, load the submitted
function binding and body, call it with `str(CS)`, and reach a Boolean
`RESULT` satisfying:

```text
RESULT ==Bool nestedResult(CS)
```

This is an equality, not a one-way implication or a free destination. The
returned Boolean is result-constraining.

### Mechanical program identity

I extracted the `Module(...)` argument actually executed under
`SPEC.program` and removed exactly six explicit `.Stmts` sequence-identity
tokens. K's standalone program parser does not accept those identity tokens,
although claim syntax does; removing list identities is semantically inert.
K `kast` then produced byte-identical JSON ASTs for:

- trusted-regenerated `solution.mpy`;
- the module executed by the claim.

Both KAST files hash to
`26ad1a8c23648eeb63362bb21ee06c03e0463df8230f82816fa9b2f8be24d454`.
The claim therefore pins the exact function name, parameter, binding, and body.
The first standalone parse attempt and the corrected identity-normalized
comparison are both preserved; the former is a parser-surface observation, not
proof evidence.

### Satisfiable states and ground substitutions

The loop precondition is satisfiable, for example with
`CS = .IntSeq`, `S = 0`, the displayed plain local frame, and any permitted
framed cells. The entry precondition is satisfiable with the empty string and
with `[[]]`; `bracketInput` accepts both.

Seven ground substitutions include every accepting-state boundary and both
prompt outcomes. For example:

- empty: `bracketInput = true`, `nestedResult = false`, canonical `false`,
  candidate `false`;
- `[[]]` (codes 91, 91, 93, 93): `bracketInput = true`,
  `nestedResult = true`, canonical `true`, candidate `true`;
- the long negative example:
  `nestedResult = canonical = candidate = false`.

All seven substitutions agree.

Evidence:
[stage4_pinning.log](evidence/stage4_pinning.log),
[stage4_pinning_attempt1.log](evidence/stage4_pinning_attempt1.log),
[extract_spec_program.py](evidence/extract_spec_program.py), and
[concrete_claim_substitution.py](evidence/concrete_claim_substitution.py).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.md` records every top-level declaration, context,
configuration, rule, and claim in:

- trusted `reference-semantics/semantics.k` and all 23 helper K files;
- candidate `verification.k`;
- candidate `spec.k`.

It contains source hashes and 1,113 inventory records, including 705 rules,
231 syntax declarations, five contexts, one configuration, and two claims. It
individually tags every source occurrence of `[function]`, `[total]`,
`[concrete]`, priority, `[owise]`, macro, strictness, and
`[no-evaluators]`. There is no source `[simplification]` or `[functional]`
attribute.

Each supplied rule is marked either `SUPPLIED_FIXED_REACHED`,
`SUPPLIED_FIXED_UNREACHED`, or `SUPPLIED_CONCRETE_ONLY`. An unreached rule's
LHS constructor/value cannot be produced by this submitted program, and it
does not overlap any reached target rule. This is not a claim that the small
supplied semantics models all of Python; it is a per-rule noncontribution
decision for this theorem. The 22 opaque/no-evaluator declarations are all on
unreachable floating-point, sorting, or digest operations and cannot affect
the target value, control, state, exception, or postcondition.

The constructor-level map in `evidence/used_construct_map.md` traces every
submitted constructor through declarations and rules for:

- module load and sequential statements;
- plain lexical lookup and binding;
- callee-before-argument and left-to-right evaluation;
- plain function entry, parameter binding, return, and frame restoration;
- string literal encoding and left-to-right iteration;
- loop-target binding, body execution, and loop continuation;
- assignments and state updates;
- integer and string comparisons;
- branch truthiness and control.

The exact frame has no `$cells`, references, heap objects, or mutating methods,
so fixed priority rules for closure cells and heap dereferences are
inapplicable. Fixed semantics executes every material operation; no rule skips
the function or loop.

### Proof-local theory

`verification.k` adds exactly four functions and ten equations:

- `nestedStep`: five guards form a complete, pairwise-disjoint partition of
  all integer states/codes. Every RHS is the corresponding Python branch.
- `nestedScan`: two disjoint constructor equations, with strict structural
  descent on the tail.
- `bracketInput`: two disjoint constructor equations, with strict structural
  descent and exact code restriction 91/93.
- `nestedResult`: one exhaustive equation equating acceptance with state 4.

All four `[total]` declarations are backed by exhaustive terminating
equations, so totalization does not introduce a result-bearing unconstrained
value. None matches or rewrites a Python program term. `SPEC.loop` is a
derived reachability circularity that executes the fixed semantics rather than
an operational bridge. Its state bounds are inductive because each permitted
step remains in 0 through 4.

I found no answer-encoding operational rule, unconstrained oracle,
execution bypass, false overlap, hidden control effect, or fabricated result.
Consequently there is no unsound-rule allegation requiring a false-conclusion
witness.

Evidence:
[k_rule_inventory.md](evidence/k_rule_inventory.md),
[used_construct_map.md](evidence/used_construct_map.md), and
[stage5_inventory.log](evidence/stage5_inventory.log).

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation
`evidence/auditor-false-spec.k` loads the exact submitted module, calls it on
the empty bracket string, and changes the result obligation from the correct
`false` to `true`. The input satisfies `bracketInput(.IntSeq)`.

```text
kprove auditor-false-spec.k --definition verification-kompiled-fresh \
  --spec-module AUDITOR-FALSE-SPEC --dry-run
```

Exit 0, establishing that the mutation parses and builds.

```text
kprove auditor-false-spec.k --definition verification-kompiled-fresh \
  --spec-module AUDITOR-FALSE-SPEC
```

Exit 1 with `WarnStuckClaimState`. The residual contains:

```text
<k>
  false ~> .K
</k>
```

This is the expected unmet result, not a parser error, missing import, timeout,
or unrelated crash. It establishes that the proof is discriminating and that
the exact program body determines the result.

Evidence:
[auditor-false-spec.k](evidence/auditor-false-spec.k),
[stage6_nonvacuity.log](evidence/stage6_nonvacuity.log), and
[stage6_false_proof_raw.log](evidence/stage6_false_proof_raw.log).

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY semantics, for every finite bracket-only `IntSeq`, the
exact submitted and trusted-regenerated program, loaded into the fresh module
configuration and called normally, is partially correct with returned Boolean
equal to the four-state `[[]]` subsequence recognizer. The symbolic domain is
unbounded in length; it is not a finite unrolling or fixed-size theorem.

The K proof also establishes the loop summary for every bracket-only suffix and
every state 0 through 4 in the exact reachable plain local frame. The proof
does not merely prove the mathematical summary independently: it connects that
summary to fixed execution of the real loop and whole function.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Supplied `reference-semantics/` | Defines syntax, evaluation, scopes, calls, loops, and values for both claims. | Acceptable fixed benchmark boundary. It is recursively identical to the trusted mount, and every material used rule was reviewed and concretely exercised. Unused language gaps are irrelevant to this program. |
| Trusted `py2mpy.py` | Bridges candidate Python AST to `solution.mpy`, then to the claim's executed constructor term. | Acceptable. Regeneration is byte-identical, and KAST comparison pins the claim module mechanically. |
| K v7.1.293, Haskell/LLVM backends, SMT and host runtime | Implements compilation, symbolic reachability, and concrete execution. | Standard unavoidable trusted computing base. Both definitions were rebuilt cleanly. |
| Human-language interpretation and trusted canonical Python | Identifies the requested property as `[[]]` in subsequence order. | Acceptable intent bridge: the equivalence has a direct two-way mathematical argument and agrees with the trusted canonical implementation. |
| Differential and ground tests | Support Python equivalence, boundary behavior, and the intent bridge on finite inputs. | Supporting evidence only; not used in place of the universal K reachability proof. |

There is no proof-local opaque symbol, empirical program summary, trusted
primitive, simplification lemma, or operational bridge on which the returned
value depends.

### Exclusions

- This is partial correctness, as required by the Kit workflow; a separate
  liveness theorem is not claimed.
- Inputs other than strings containing only `[` and `]` are outside the source
  contract and formal precondition. This is not a narrowing of that contract.
- Unused CPython features and unused portions of the supplied partial Python
  semantics are not claimed.

## Decision

The positive claims reconstruct with fresh `#Top` results, the formal domain
matches the unrestricted source-contract domain, the returned Boolean is
constrained, the claim executes the mechanically identical submitted program,
the proof-local equations are sound, and the fresh false result is rejected
for the expected reason. There is no material adequacy or trust-boundary gap.

VERDICT: PASS
LEGITIMACY: LEGIT
