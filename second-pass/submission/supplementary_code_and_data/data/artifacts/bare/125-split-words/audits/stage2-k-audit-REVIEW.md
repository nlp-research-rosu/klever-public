# Independent adversarial audit: 125-split-words

The reconstructed K theorem is sound under the candidate's generated semantics,
is non-vacuous, and mechanically pins the submitted `solution.mpy`. It is not,
however, a proof of the required HumanEval implementation: `solution.py`
materially disagrees with the trusted canonical function on ordinary comma
boundaries and on the unrestricted Python `str` domain. The successful `#Top`
therefore proves the behavior of a substituted/wrong implementation, not the
source contract.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1`,
`condition = bare`, and `semantics_mode = GENERATED_SEMANTICS`. The mounted
`/reference/reference-semantics` is absent, as required for this mode; I did not
infer or use any hidden reference semantics.

I independently checked the launcher-owned records before using candidate
content:

- `/audit-campaign-lock.json` is a regular file, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object exactly equals the `audit_campaign` block in
  `/audit-input.json`.
- `/run.json`, `/task.json`, `/generation-result.json`, the invocation,
  metrics, usage, prompt, final message, full output log, and structured trace
  are present, regular, readable, and match the recorded direct hashes.
  `runtime-metrics.json` is not required for this legacy layout.
- The full structured trace contains 208 valid JSONL records. The retained
  candidate tree has the pipeline digest
  `37cf88d86cb9b4482f82fa4d59931df0cd9f082cf2ae244cc3e96548b7d79a12`,
  matching both the invocation and selected stage result. The structured-trace
  pipeline digest is
  `0e7c0db772a6d8255faa687ef460249309ba35967e8a40b91122cef79872195b`,
  matching `usage.json`. The launcher also records its own tree-digest fields;
  these use a different launcher scheme and were not conflated with the public
  pipeline digest.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts, with SHA-256 values
  `c9ac5a400f5388b93fcc2acc0fa2adf0237e9f1802cebec7f375644658bd9aa0`
  and
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
  The trusted canonical hash is
  `6f758b9346cb3be14b584c0436117e484b6e7b6c41bda7ee2713740fffd6b30f`.
- No symlink or unsupported entry occurs in the candidate, reference, or
  generation-evidence trees. Every proof source artifact required by the
  generation prompt is present.

The generation records say that the generator obtained `#Top`; they were
treated only as untrusted historical claims. Reproducible checks are in
[`stage1-integrity.log`](evidence/stage1-integrity.log),
[`stage1-generation-record-inventory.log`](evidence/stage1-generation-record-inventory.log),
and [`stage1-trace-inventory.log`](evidence/stage1-trace-inventory.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Trusted contract

Reading `/reference/prompt.py` together with `/reference/canonical.py`, the
trusted function accepts an unrestricted Python string and:

1. if the string contains a literal ASCII space, returns `txt.split()`;
2. otherwise, if it contains a comma, replaces commas by spaces and then uses
   `split()`, which collapses separator runs and drops empty fields;
3. otherwise, counts characters for which `islower()` is true and whose Unicode
   code point is even. On ASCII letters this counts `b,d,...,z`.

The candidate instead tests whether no-argument `split()` followed by empty
join changes the string, so any CPython whitespace selects its first branch. It
uses `txt.split(",")`, preserving leading, trailing, and repeated-comma empty
fields. Its last branch counts only the thirteen ASCII characters
`b,d,...,z`, not all lowercase Unicode characters accepted by the canonical
predicate.

### Translation identity

The exact command

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy
```

exited 0. `cmp` exited 0, and both regenerated and submitted files have SHA-256
`df19e38bff0c6bbb1f301ab129ef175ef193e54f38b70a28dbf152a2b6d02ec0`.
Thus `solution.mpy` faithfully represents the submitted Python, but the Python
itself is wrong. See
[`stage2-translator-identity.log`](evidence/stage2-translator-identity.log).

### Independent differential test

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and candidate entry points independently. Its 6,501 unique inputs
include all documented examples, explicit empty/branch/boundary cases, every
string of length 0 through 4 over an eight-symbol ASCII/Unicode alphabet, and
2,000 seeded strings of length 0 through 20. It exited 1 after finding 3,519
mismatches. Concrete false-behavior witnesses include:

| Input | Trusted canonical | Candidate |
|---|---|---|
| `","` | `[]` | `["", ""]` |
| `"a,,b,"` | `["a", "b"]` | `["a", "", "b", ""]` |
| `"left\tright"` (tab escape) | `6` | `["left", "right"]` |
| `"ê"` | `1` | `0` |

The complete bounded output is
[`stage2-differential.log`](evidence/stage2-differential.log). These are
material result divergences within the documented Python `str` domain, not
algorithmic style differences.

## 3. Clean proof reconstruction

All candidate-provided compiled definitions and caches were ignored. Source
artifacts were copied to `/tmp/audit-work/candidate`, and I created fresh,
distinct output definitions.

These builds both exited 0 under K v7.1.293:

```text
kompile verification.k --backend llvm --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition concrete-kompiled
kompile verification.k --backend haskell --main-module MPY-VERIFICATION --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

The exact log is
[`stage3-clean-rebuild.log`](evidence/stage3-clean-rebuild.log).

Fresh LLVM execution was compared with both Python functions on 14 normal and
boundary inputs. K had zero mismatches with candidate Python, including empty
input, whitespace-only input, all three branches, repeated commas, Unicode
whitespace, and Unicode lowercase input. The same output visibly preserves the
canonical divergences. The controlling successful run is
[`stage3-concrete-semantics-final.log`](evidence/stage3-concrete-semantics-final.log).
Two earlier diagnostic logs are preserved: the first exposed a reviewer output
parser limitation, and the second exposed escaped command-line input rather
than a semantics defect; both were corrected before the controlling run.

The candidate's exact aggregate command

```text
kprove spec.k --definition proof-kompiled --spec-module SPLIT-WORDS-SPEC
```

exited 0 and printed `#Top`. I also placed each of the eight positive claims in
an isolated spec module and ran eight independent `kprove` commands. Every one
exited 0 and printed `#Top`. K emitted `WarnTrivialClaim` for every claim,
meaning definitional simplification made source and destination identical
without reachability rewriting; the adequacy, static, body-sensitivity, and
non-vacuity checks below establish what that simplification means. Logs:
[`stage3-original-positive-command.log`](evidence/stage3-original-positive-command.log)
and [`stage3-positive-claims.log`](evidence/stage3-positive-claims.log).

## 4. Adequacy and real-program pinning

The universal claim has no `requires` clause: every K `String` is admitted. In
plain language, it says the return is:

- the modeled no-argument whitespace split if empty-joining that split differs
  from the input;
- otherwise the modeled comma split if a comma is found;
- otherwise the sum of occurrences of the thirteen ASCII letters
  `b,d,...,z`.

The other seven claims are unconditional ground instances for the three prompt
examples, empty input, whitespace precedence, Unicode whitespace, and repeated
commas. There are no helper, loop, invariant, or lemma claims.

The `<k>` cell starts with `runProgram(solutionAST,S)`. `runProgram` selects the
real `split_words` binding, `invoke` binds `txt`, and `exec`/`eval`/`call`
traverse the actual statements and expressions. I extracted the `solutionAST`
rule RHS, normalized only K's explicit `.Exprs`/`.Stmts` empty-list units to
their empty program-syntax rendering, parsed both terms with `kast --output
json`, and obtained byte-identical KAST hashes
`aace024997c71444ee927f8003323dff817288002dba4c4e9e427ba540d07d2e`.
See
[`stage4-program-term-identity-rerun.log`](evidence/stage4-program-term-identity-rerun.log).

Every precondition is satisfiable. For example, substituting `S = "abcdef"`
produces `VInt(3)`, matching both Python functions. Substituting `S = ","`
produces `VList("", "")`, matching candidate Python but contradicting canonical
`[]`. Thus the RHS constrains the result and accurately exposes, rather than
repairs, the wrong implementation.

For body sensitivity, I changed the final executed `txt.count("z")` constructor
inside the `solutionAST` rule to `txt.count("a")`, rebuilt a separate Haskell
definition, and reran the original spec. The proof exited 1 with
`WarnStuckClaimState`; its residual compared the mutated `a` summary against
the required `z` summary. The mutation and exact log are
[`body-sensitivity.patch`](evidence/body-sensitivity.patch) and
[`stage4-body-sensitivity.log`](evidence/stage4-body-sensitivity.log).

The claim therefore pins the real submitted program and is body-sensitive. Its
fatal adequacy defect is that this real submitted program does not implement
the trusted task.

## 5. Rule-by-rule static soundness review

[`rule-inventory.md`](evidence/rule-inventory.md) inventories all 35 logical
local syntax/symbol declarations, the configuration, all 48 local rules, and
all eight claims. The mechanical extraction is preserved in
[`stage5-rule-inventory-extract-rerun.log`](evidence/stage5-rule-inventory-extract-rerun.log).

Construct coverage is complete for `solution.mpy`: module/function, one
parameter, assignment, `if`, return, name/string/attribute/call/comparison/
addition expressions, empty and singleton call lists, and singleton comparison
lists all have declarations and applicable rules. The unused integer-literal
production is harmless. The only state is a local binding map and return
outcome; this pure program requires no heap, I/O, exception, or allocation
cell.

The exhaustive review found:

- Name binding, assignment, function selection/invocation, statement
  sequencing, return propagation, branch selection, and the observable result
  are preserved. Expression order is adequate because every used expression is
  pure and has at most one call argument.
- The whitespace scan's guards are disjoint and exhaustive on reachable
  indices, and its index strictly increases. Its 29 declared characters
  exactly equal CPython 3.10.12's exhaustive `isspace()` character set; see
  [`stage5-whitespace-set.log`](evidence/stage5-whitespace-set.log).
- Join recurses structurally. Separator splitting has disjoint found/not-found
  guards and strictly shortens the string for the only used nonempty separator,
  comma. Empty separator is intentionally outside the submitted program path
  and is not silently assigned a fabricated result.
- Function lookup's equal/unequal cases are disjoint. `iteValue`'s Boolean
  cases are disjoint and exhaustive. There are no local priority, `owise`,
  `anywhere`, explicit simplification, macro, or proof-only operational rules.
- `oddLetterCount` and `containsWhitespace` are truthful definitional summaries
  of the candidate expression and guard. They do not replace program
  execution: `solutionAST` still reduces through `exec`/`eval`/`call`. No fresh
  or opaque result-bearing oracle occurs.

I make no claim that a local K rule is semantically false, so no unsupported
“unsound rule” allegation is being used for the verdict. The concrete false
conclusions in Stage 2 are caused by the submitted Python algorithm itself and
are faithfully reproduced by these semantics.

## 6. Fresh non-vacuity test

I created a distinct reviewer spec whose unconditional ground claim changes the
result for `"abcdef"` from the actual `VInt(3)` to the demonstrably false
`VInt(4)`. The mutation is
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k).

The dry-run command exited 0, establishing that the mutation parsed and built:

```text
kprove /audit-output/evidence/spec-vacuity-audit.k --definition /tmp/audit-work/candidate/proof-kompiled --spec-module AUDIT-SPEC-VACUITY --dry-run
```

The corresponding real proof exited 1 with `WarnStuckClaimState`, and the
residual was exactly `<k> VInt ( 3 ) ... </k>`. This is the expected unmet
result obligation, not a parser error, timeout, unrelated crash, or unreachable
mutation. See
[`stage6-nonvacuity.log`](evidence/stage6-nonvacuity.log).

## 7. Proven versus assumed accounting

### What is mechanically proven

Under the candidate's generated K semantics, for every K `String`, executing
the exact submitted constructor program reaches the candidate-specific nested
summary described in Stage 4. The seven ground claims are instances of that
behavior. The result is constrained, the entry domain is universal rather than
finitely bounded, the theorem is body-sensitive, and a false result is
rejected.

This does **not** prove that the summary equals the trusted canonical result.
In fact, the finite witnesses in Stage 2 refute that statement.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, LLVM/Haskell backends, and `kprove` reachability engine | All reconstructed execution and proof results | Ordinary low-level trusted computing base; exact commands and outputs are preserved. |
| K `DOMAINS` primitives for mathematical integers, Booleans, strings, maps, and lists (`findString`, `substrString`, `lengthString`, `countAllOccurrences`, arithmetic, lookup/update) | String methods, control guards, counts, environment | Acceptable fixed primitive boundary. No task answer is encoded in an opaque primitive. |
| Trusted mounted `py2mpy.py` | Python-to-constructor identity | Accepted launcher input; byte identity of its fresh output was independently checked. |
| Generated semantics' correspondence to the used CPython subset | Interpretation of the K theorem as behavior of `solution.py` | Statically reviewed rule by rule and concretely checked on normal/boundary inputs. The whitespace character bridge was exhaustively checked against CPython 3.10. This remains an informal language-model bridge, not a separate universal theorem about CPython. |
| `solutionAST` program constant | Every entry claim | Not assumed: constructor-level identity with submitted `solution.mpy` was mechanically checked, and a body mutation broke the proof. |
| `oddLetterCount` and `containsWhitespace` | Universal destination summary | Not opaque assumptions: both have complete defining equations and exactly name candidate computations. |
| Differential testing | Source-contract comparison and finite semantics evidence | Finite evidence only; it is not used as a substitute for the K proof. One mismatch is enough to refute candidate/canonical equivalence. |

Kit Gate A (real-program soundness and non-vacuity) passes under the generated
semantics. Gate B (intent adequacy) fails: the proven implementation materially
disagrees with the trusted HumanEval contract on its unrestricted `str` domain.
Gate C is auditable with the named low-level trust boundaries and preserved
evidence.

The benchmark decision rule is decisive: a sound theorem about a materially
narrowed or substituted HumanEval implementation is `FAIL / NOT_LEGIT`, not
`CONCERNS / LEGIT`. The candidate's historical `#Top`, and the independently
reconstructed `#Top`, cannot cure the implementation/specification
discrepancy.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
