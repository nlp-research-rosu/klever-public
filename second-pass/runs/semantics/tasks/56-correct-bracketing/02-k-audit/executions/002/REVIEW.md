# Independent adversarial review: 56-correct-bracketing

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program over the full source-contract domain. The
verdict is `CONCERNS / LEGIT`, rather than `PASS`, because three low-level
proof-only normalization bridges (two return routes and scope-map deletion)
do not have successful bridge-free universal `kprove` connection claims: the
unextended Haskell backend stops at its generated strictness freezer or an
unreduced built-in map update. Their source-level derivations, state
footprints, fixed-LLVM behavior, and bridge-enabled behavior agree, and no
false-conclusion witness exists. This is a non-fatal auditability limitation,
not evidence of unsoundness.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, `semantics_mode = SUPPLIED_SEMANTICS`, and complete
input provenance. I read its record layout, container-path map, hashes, and
integrity fields before using any candidate evidence. I also read
`/audit-campaign-lock.json`; its JSON object exactly equals the
`audit_campaign` block, and its SHA-256 is the declared
`ad5dfcc0...1a78d745`.

For the declared legacy-selected layout, I inspected `/run.json`,
`/task.json`, `/generation-result.json`, `invocation.json`, `metrics.json`,
`usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, and all 672
JSONL records in the structured trace. The trace parses without error. Their
launcher-recorded file hashes all match. The historical run did not record
`runtime-metrics.json`; that record is expressly non-required for this layout
and is not treated as a defect. The prior `KPROVE_PASSED` report was treated
only as an untrusted claim.

Independent mounted-tree checks found:

- all required provenance records and proof deliverables are regular and
  readable;
- the mounted candidate tree has pipeline digest
  `23d82f7a...b117709`, exactly the stage-1 retained-workspace digest;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions;
- candidate and trusted `reference-semantics/` trees have exactly the same
  entry names, entry types, and bytes, with no missing, extra, changed, or
  symlinked entries;
- both supplied-semantics trees have pipeline tree digest
  `4e06397a...e3789f`, the declared trusted manifest digest.

No semantics-mode contradiction or infrastructure breach exists.
[The reproducible integrity log](evidence/stage1_integrity.log) and
[full-trace parser summary](evidence/stage1_trace_parse.log) record commands,
hashes, and statuses.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says `brackets` is a string consisting of `<` and `>`.
The result is true exactly when the string is correctly balanced: no prefix
has more closings than openings, and the final opening/closing counts are
equal. The trusted canonical implementation maintains an integer depth,
rejects immediately when it becomes negative, and accepts exactly when the
final depth is zero.

The candidate implements that same algorithm. Its extra initialization
`bracket = ""` is overwritten before every nonempty-loop use and is inert for
the empty case. The `else` treats every non-`<` character as closing; on the
stated domain that character is exactly `>`, so there is no domain narrowing
or divergence.

Regenerating with `/reference/py2mpy.py` exits 0. The regenerated and submitted
`solution.mpy` files are byte-identical, both SHA-256
`a4f95cf1...bf74132`; see
[translation identity](evidence/stage2_translation_identity.log).

The independent differential test imports the trusted canonical and copied
submitted entry points and also uses an independently written balance oracle.
It covers the four documented examples, empty and one-character cases, every
branch boundary, deep balanced/unbalanced cases, every binary bracket string
of lengths 0 through 12, and 2,000 seeded strings of lengths 0 through 256.
All 10,205 cases agree, with zero mismatches. This finite test supports
fidelity; it is not substituted for the K proof. The script and exact run are
[differential_test.py](evidence/differential_test.py) and
[stage2_differential.log](evidence/stage2_differential.log).

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`, taking the
semantics and translator from the trusted mount. Before building, no
`*-kompiled` directory existed in scratch. Candidate caches and compiled
definitions were neither copied nor used.

Using K 7.1.293, the following fresh operations all succeeded:

- LLVM compilation of trusted `reference-semantics/semantics.k`, with
  `MPY-KRUN` / `MPY-SYNTAX`, exits 0;
- concrete execution of a reviewer-authored assertion harness exits 0 with
  `.K`, `NoExc`, and exit code 0;
- Haskell compilation of copied `verification.k`, with `VERIFICATION` /
  `MPY-SYNTAX`, exits 0;
- the mutually inductive `loop-zero,loop-positive` proof prints `#Top` and
  exits 0;
- the complete
  `loop-zero,loop-positive,correct-bracketing` proof prints `#Top` and exits
  0.

The loop invariants must be selected together because they are mutual
circularities. A diagnostic selecting only `loop-zero` entered prolonged proof
search and was interrupted; it is not a target proof result. The actual mutual
proof and complete target set close independently from scratch.

Exact commands, bounded output, and statuses are in
[LLVM build](evidence/stage3_kompile_llvm.log),
[concrete run](evidence/stage3_krun_concrete.log),
[Haskell build](evidence/stage3_kompile_haskell.log),
[mutual-loop proof](evidence/stage3_kprove_mutual_loops.log), and
[complete proof](evidence/stage3_kprove_all.log).

## 4. Adequacy and real-program pinning

### Claims in plain language

- `loop-zero`: from the actual submitted loop head, with arbitrary remaining
  string suffix `S`, local depth 0, the exact final-return continuation, a
  real caller frame, and a fresh callee scope location, execution returns
  `bracketResult(S,0)` to the caller and removes the callee frame.
- `loop-positive`: the same actual loop and continuation at any integer
  `D > 0` returns `bracketResult(S,D)` and performs the same exact cleanup.
- `correct-bracketing`: from the standard empty module configuration, load the
  exact submitted module, call the installed `correct_bracketing` binding on
  arbitrary semantic string `str(S)`, and return
  `bracketResult(S,0)`. The post-state contains the exact installed closure,
  with heap, stack, exception, exit code, and allocators as specified.

Every precondition is satisfiable. Examples include the entry state with
`S=.IntSeq`; the reachable empty-input loop head at `L=1`, depth 0, empty
suffix; and the reachable `"<>"` loop head after processing `<`, with depth 1
and suffix `">"`. The freshness guards hold when the rest of the scope map
contains only module and built-in frames.

Ground K obligations for `""`, `"<"`, `"<>"`, and `"><"` jointly print
`#Top`; their formal values are respectively true, false, true, false and
agree with both Python implementations. The satisfying states and values are
recorded in [stage4_ground_results.log](evidence/stage4_ground_results.log).

### Mechanical pinning

The entry claim's `Module(...)` term and the trustedly regenerated
`solution.mpy` differ textually only because the translator prints an omitted
empty `Stmts` list while the claim spells its constructor unit `.Stmts`.
After expanding that single list-unit surface form, K's rule parser produces
byte-identical KORE for both terms (same SHA-256
`8f5f9609...a251ea`). The claim then calls the just-installed
`correct_bracketing` binding on `str(S)`. This is constructor-level pinning,
not a source-name assertion; see [stage4_pinning.log](evidence/stage4_pinning.log).

A body-sensitivity mutation changes both copies of the actually embedded
function body so that the `else` branch increments rather than decrements.
The closure post-state is changed consistently, avoiding a trivial binding
mismatch. The proof builds but fails with a reachable stuck state; `"<>"` is
a concrete witness because the mutated program returns false while the
claimed summary and both Python implementations return true. See
[spec-body-mutation.k](evidence/spec-body-mutation.k) and
[stage4_body_sensitivity.log](evidence/stage4_body_sensitivity.log).

The formal input `S:IntSeq` is unbounded and includes all finite strings over
codes 60 (`<`) and 62 (`>`). The theorem therefore covers the entire stated
HumanEval domain; it is not an examples-only, fixed-size, or bounded-unrolling
result. It is actually stronger in accepting arbitrary code sequences, on
which both program and summary consistently treat non-60 codes as closing.

## 5. Rule-by-rule static soundness review

The exhaustive inventory contains all 949 local configuration, syntax,
context, rule, function/total/opaque/priority/simplification, and claim
declarations from the 24 supplied K files plus `verification.k` and `spec.k`.
It is preserved as
[stage5_rule_inventory.tsv](evidence/stage5_rule_inventory.tsv). The detailed
per-rule classification, used-construct mapping, overlaps, guards, control
effects, and state footprints are in
[stage5_static_review.md](evidence/stage5_static_review.md).

The key conclusions are:

- every material constructor in `solution.mpy` maps to fixed rules for module
  load, definition/binding, left-to-right evaluation, string iteration,
  assignment, calls/returns, comparisons, branches, arithmetic, and frame
  lifecycle;
- `bracketResult` is fully defined, total, guard-disjoint, terminating on the
  suffix, and contains no opaque or fresh result;
- its eight equations exactly express prefix-valid bracketing at the current
  depth; no equation encodes a fixed example or bypasses the function body;
- the nine proof-local operational rules have exact, narrow state patterns.
  They preserve or update every fixed cell correctly and have no result oracle;
- the six branch/arithmetic bridges each have a fresh, bridge-free universal
  connection claim under the fixed semantics that prints `#Top`;
- the two return connections reach the expected evaluated Boolean but the
  unextended Haskell backend leaves it in `#freezerReturn`; the `#pop`
  connection reaches exactly `(L |-> frame SC)[L <- undef]` but does not prove
  that built-in map term equal to `SC`. These failed probes are expected
  normalization residuals, not alternate results or control effects;
- fixed LLVM and bridge-enabled Haskell execution of the same reviewer harness
  end in byte-equivalent normalized final configurations
  ([comparison log](evidence/stage5_final_config_comparison.log)).

The return bridges are the direct composition of fixed literal/lookup/
comparison rules with fixed abrupt return. They discard exactly the suffix
that fixed `Return` discards. The pop bridge is ordinary map deletion under
the explicit freshness guard and exactly restores result, caller, stack tail,
and allocator. I found no satisfiable state in any rule's match domain where
it enables a false result, state, or control conclusion.

The supplied fixed semantics does import opaque float, sort, and MD5 symbols,
plus some intentionally totalized unused helpers. None is reachable from this
program, summary, or proof. There is no task-answer oracle in the reachable
theory.

## 6. Fresh non-vacuity test

The reviewer mutation changes only the entry result obligation from
`bracketResult(S,0)` to `notBool bracketResult(S,0)`. The empty string is a
satisfying witness: actual and formal results are true, while the mutated
target is false.

The mutated spec dry-run builds successfully and exits 0. Its actual proof
exits 1 with `WarnStuckClaimState`; the residual is precisely
`bracketResult(S,0) = notBool bracketResult(S,0)`. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash. Artifacts:
[spec-vacuity.k](evidence/spec-vacuity.k),
[build log](evidence/stage6_vacuity_build.log), and
[proof log](evidence/stage6_vacuity_proof.log).

## 7. Proven versus assumed accounting

### What the successful proof establishes

Relative to the supplied MPY semantics and proof-local rules reviewed above,
for every finite `IntSeq S`, if the loaded submitted call terminates from the
specified standard state, its returned Boolean is exactly
`bracketResult(S,0)`. The mutually inductive claims establish the loop for
zero and every positive integer depth, including immediate rejection of a
negative prefix and exact function-frame cleanup. On strings over `<` and
`>`, the fully defined summary is exactly the canonical balanced-bracket
predicate. This is partial correctness; the report does not replace it with a
claim about unrestricted CPython objects or characters outside the stated
contract.

### Trust ledger

- **Trusted mounted inputs:** original prompt, canonical implementation,
  translator, and supplied semantics. Integrity was independently checked.
- **K trust:** K 7.1.293 parser/compiler, Haskell reachability engine,
  circularity mechanism, SMT reasoning, and built-in Int/Bool/String/Map/List
  mathematics.
- **Translation bridge:** trusted CPython-AST translator; its regenerated
  constructor file is byte-identical to the submitted file.
- **Intent bridge:** the ordinary mathematical fact that the depth/prefix
  algorithm and `bracketResult` characterize balanced brackets. It is
  supported by exhaustive small-domain and broad differential tests but is
  also visible directly in the exhaustive equations.
- **Proof-local operational bridges:** six have machine-checked bridge-free
  universal connections. The two return bridges and one pop-normalization
  bridge rely on direct inspection of fixed rules plus Boolean-sort and Map
  mathematics because the unextended Haskell backend cannot normalize the
  corresponding universal claims. They affect control and the final result,
  so this limitation is material enough to prevent `PASS`, but their exact
  patterns, concrete fixed/extended agreement, and absence of a false witness
  make the proof legitimate.
- **Empirical evidence:** 10,205 Python differential cases and 11 concrete K
  assertions. These support fidelity and the low-level bridge audit only;
  they are not treated as universal proof.
- **Unreachable opaque primitives:** fixed float, sorting, MD5, and
  out-of-bounds helper abstractions listed in the static review. No target
  claim depends on them.

Gate B (intent/domain adequacy) passes: no material source-domain restriction
exists. The proof is result-constraining and non-vacuous. The only adverse
finding is the missing successful universal connection proof for three
low-level normalization bridges, which is reported as a legitimate-proof
concern rather than hidden or mislabeled as unsound.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
