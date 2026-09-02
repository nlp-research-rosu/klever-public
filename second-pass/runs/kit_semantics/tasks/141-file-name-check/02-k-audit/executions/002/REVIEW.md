# Independent adversarial review: 141-file-name-check

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program. I reconstructed it from source and
did not rely on candidate-provided compiled output or reported `#Top` results.
The final status is `CONCERNS / LEGIT`, rather than `PASS`, because the
universal connection between CPython strings and the semantics' algebraic
`IntSeq` representation remains an informal representation bridge. This does
not narrow the K claims: they quantify over every finite `IntSeq`, including
sequences containing non-ASCII code points.

## 1. Input and provenance integrity

I read `/audit-input.json` first. It declares `record_layout` `pipeline-v3`,
problem `141-file-name-check`, generation condition `kit-semantics`, and
`SUPPLIED_SEMANTICS`. The required trusted
`/reference/reference-semantics` mount is present, so the rendered mode and
trusted mounts are consistent.

The independent integrity checker is
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py), with its
complete result in
[01-independent-integrity-check.log](/audit-output/evidence/01-independent-integrity-check.log).
It found:

- the campaign block in `/audit-input.json` exactly equals
  `/audit-campaign-lock.json`, and both independently hash to the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`;
- all required `pipeline-v3` records are present, regular, readable files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured
  trace;
- every launcher-recorded direct file hash matches its mounted file;
- the independently recomputed trusted-semantics and candidate-semantics tree
  digests both equal
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- recursive entry-by-entry comparison finds no missing, additional, changed,
  mistyped, or symlinked entry in the candidate `reference-semantics/` tree;
- the candidate prompt and translator are byte-identical to the trusted
  prompt and translator;
- the one trace file contains 998 valid JSONL records, and both its individual
  file hash and the trace-tree digest match the launcher record; and
- the candidate workspace digest also matches, with no unsupported candidate
  entries.

The checker ended `ERROR_COUNT=0`, exit 0. Supporting bounded records are
[01-semantics-diff.log](/audit-output/evidence/01-semantics-diff.log),
[01-required-records-hashes.log](/audit-output/evidence/01-required-records-hashes.log),
[01-trace-integrity.log](/audit-output/evidence/01-trace-integrity.log),
[01-generation-json-records.log](/audit-output/evidence/01-generation-json-records.log),
and
[01-generation-text-records.log](/audit-output/evidence/01-generation-text-records.log).
I treated the generation reports and trace only as untrusted historical
claims. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt requires `"Yes"` exactly when:

1. there are at most three ASCII decimal digits `0` through `9`;
2. there is exactly one dot;
3. the substring before the dot is nonempty and its first character is an
   ASCII Latin letter;
4. the suffix after the dot is exactly `txt`, `exe`, or `dll`.

All other strings must return `"No"`. The submitted `solution.py` implements
that contract by counting the dot, checking the first character against an
explicit 52-character ASCII alphabet, comparing the last four characters
against `.txt`, `.exe`, and `.dll`, and summing the ten individual ASCII digit
counts.

Using the trusted translator, I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s solution.mpy regenerated-solution.mpy
```

The command exited 0. Both MPY files are byte-identical and have SHA-256
`d6a7d6f62016632bdec20a046b3c820c447d8d0c2d1098de7a05402d6e7c54ab`;
see
[02-regeneration.log](/audit-output/evidence/02-regeneration.log).

### Independent differential test

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py) imports
the scratch copies of the trusted canonical function and submitted generated
function and compares both to an independently written literal-contract
oracle. It exercised:

- 31 documented, empty, boundary, suffix, dot-count, digit-threshold, and
  Unicode cases;
- every string of lengths 0 through 5 over
  `aZ09.txedl?é²`; and
- 20,000 seeded generated strings of lengths 0 through 24.

This produced 420,635 unique cases. The generated program had zero
literal-contract mismatches. Full input-generation parameters and results are
in
[02-differential-results.log](/audit-output/evidence/02-differential-results.log);
the script exited 0.

The trusted canonical function differs from the literal prompt on six tested
Unicode cases because it uses Python `isalpha()` and `isdigit()`. For example,
it accepts `é.txt` and `中.exe` despite the prompt's Latin restriction and
rejects `a１２３４.txt` and `a²²²².txt` despite those strings containing no
ASCII digit from `0` through `9`. The submitted program follows the explicit
prompt on these cases. I therefore record the candidate-versus-canonical
differences, but do not treat the canonical function's broader Unicode
predicates as overriding the stated source contract.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/proof`. The source-only
copy manifest is
[02-scratch-source-copy.log](/audit-output/evidence/02-scratch-source-copy.log);
no candidate definition or cache was reused. The independently discovered
toolchain was `/usr/bin/kompile`, `/usr/bin/kprove`, and `/usr/bin/krun`,
all K version `v7.1.293`; `kup` was unavailable, so direct live tools were
used as permitted by the Kit workflow. See
[03-toolchain.log](/audit-output/evidence/03-toolchain.log).

From scratch I built:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled-fresh

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-fresh

kompile --backend haskell reference-semantics/semantics.k \
  --main-module MPY --syntax-module MPY-SYNTAX \
  --output-definition lemma-kompiled-fresh
```

All three commands exited 0. Their bounded logs are
[03-kompile-runtime.log](/audit-output/evidence/03-kompile-runtime.log),
[03-kompile-verification.log](/audit-output/evidence/03-kompile-verification.log),
and
[03-kompile-lemma.log](/audit-output/evidence/03-kompile-lemma.log).

The only proof-local simplification is
`N >Int 3 => false requires N <=Int 3`. I proved that guarded implication
against the fixed `MPY` definition, without importing `verification.k`:

```text
kprove lemma-spec.k --definition lemma-kompiled-fresh \
  --spec-module LEMMA-SPEC
```

It exited 0 and printed `#Top`. `WarnTrivialClaim` is expected here because the
claim is the direct SMT-valid integer implication; see
[03-kprove-lemma.log](/audit-output/evidence/03-kprove-lemma.log).

I then selected and ran every positive entry claim separately using:

```text
kprove spec.k --definition verification-kompiled-fresh \
  --spec-module SPEC --claims SPEC.<label>
```

| Claim | Exit | Result evidence |
|---|---:|---|
| `empty-name` | 0 | `#Top` |
| `bad-dot-count` | 0 | `#Top` |
| `bad-initial` | 0 | `#Top` |
| `bad-extension` | 0 | `#Top` |
| `too-many-digits-txt` | 0 | `#Top` |
| `too-many-digits-exe` | 0 | `#Top` |
| `too-many-digits-dll` | 0 | `#Top` |
| `valid-name-txt` | 0 | `#Top` |
| `valid-name-exe` | 0 | `#Top` |
| `valid-name-dll` | 0 | `#Top` |

The executable driver
[run_positive_claims.sh](/audit-output/evidence/run_positive_claims.sh)
records the exact command template and labels; every claim has a separate
bounded `03-kprove-<label>.log`. The consolidated exact command and status
ledger is
[commands-and-status.md](/audit-output/evidence/commands-and-status.md).

An independently translated ASCII concrete suite also ran to final `.K` with
`NoExc` and exit code 0 under the fresh LLVM definition:
[03-concrete-krun-ascii.log](/audit-output/evidence/03-concrete-krun-ascii.log).
A separate probe containing non-ASCII *source literals* stopped at
`strToCodes("\xc3\xa9.txt")`, exit 113:
[03-concrete-krun.log](/audit-output/evidence/03-concrete-krun.log). This is the
fixed semantics' explicit ASCII-only source-literal decoder, not an execution
rule that turns Unicode input into a false result. Entry claims supply input
directly as arbitrary `IntSeq`, so this concrete parser/decoder limitation
does not restrict their quantified input.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

Every claim starts from the same fully specified state: the `file_name_check`
name is bound to a one-parameter closure containing `fileNameCheckBody`;
the caller and builtins scopes, scope location, empty heap and stack,
`noRet`, `NoExc`, and exit code 0 are fixed. Every destination fixes the
returned string to literal `"Yes"` or `"No"` and fixes all those operational
cells, rather than leaving a result or state variable unconstrained.

The claims mean:

| Claim | Precondition | Required return |
|---|---|---|
| `empty-name` | input is empty | `No` |
| `bad-dot-count` | input is nonempty and dot count is not 1 | `No` |
| `bad-initial` | one dot and first code is not in the ASCII Latin alphabet | `No` |
| `bad-extension` | one dot, valid ASCII-Latin first code, and no allowed suffix | `No` |
| `too-many-digits-txt` | prior checks pass, suffix `.txt`, ASCII-digit count above 3 | `No` |
| `too-many-digits-exe` | prior checks pass, not `.txt`, suffix `.exe`, count above 3 | `No` |
| `too-many-digits-dll` | prior checks pass, neither prior suffix, suffix `.dll`, count above 3 | `No` |
| `valid-name-txt` | prior checks pass, suffix `.txt`, count at most 3 | `Yes` |
| `valid-name-exe` | prior checks pass, not `.txt`, suffix `.exe`, count at most 3 | `Yes` |
| `valid-name-dll` | prior checks pass, neither prior suffix, suffix `.dll`, count at most 3 | `Yes` |

These are an exhaustive partition of finite `IntSeq`: empty/nonempty;
dot count equal/not equal to one; initial singleton contained/not contained in
the 52-code alphabet; no allowed suffix or the ordered, mutually distinct
`.txt`/`.exe`/`.dll` alternatives; and digit sum above or at most three.

The reviewer-authored
[claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) exhibits a
satisfying state for every precondition. Its witnesses are `""`, `"abc"`,
`"1.txt"`, `"a.pdf"`, `"a1234.txt"`, `"a1234.exe"`, `"a1234.dll"`,
`"a.txt"`, `"a.exe"`, and `"a.dll"`. Every precondition evaluated true, and
both Python implementations returned the claim's literal destination. See
[04-claim-witnesses.log](/audit-output/evidence/04-claim-witnesses.log).

### Mechanical program pinning

`fileNameCheckBody` is a syntax macro, not a runtime semantic shortcut. I
parsed both the regenerated `solution.mpy` module and an independently
constructed module containing the exact claim closure, expanded macros, and
rendered KORE under the fresh definition. Both files were 14,414 bytes,
byte-identical, and had SHA-256
`6f9e0d8d503f0cdcf9aeaeb372e5c9adc71c9bd8352537223dfc001861953331`.
The commands and hashes are in
[04-program-term-identity.log](/audit-output/evidence/04-program-term-identity.log).
Thus the `<k>` term calls the same function binding and body as the trusted
regeneration of the submitted source. The entry claims start from that binding
instead of replaying module loading; the reviewed `FuncDef` rule's only
material effect for this module is to install the same closure in scope 0, and
the submitted module has no import, initialization, or other top-level effect.

I also changed the macro body's final `Return(Str("Yes"))` to
`Return(Str("No"))`, rebuilt a fresh mutated proof definition successfully,
and reran `valid-name-txt`. The proof exited 1 with
`WarnStuckClaimState`; its residual returned `No` while the destination still
required `Yes`. This mutation changes the term actually executed by the
claim. Evidence:
[04-body-mutation-diff.log](/audit-output/evidence/04-body-mutation-diff.log),
[04-body-mutation-kompile.log](/audit-output/evidence/04-body-mutation-kompile.log),
and
[04-body-mutation-kprove.log](/audit-output/evidence/04-body-mutation-kprove.log).

## 5. Rule-by-rule static soundness review

The reviewer-authored
[static_inventory.py](/audit-output/evidence/static_inventory.py) lexically
inventories every top-level K sentence in all supplied semantic sources plus
`verification.k`, `spec.k`, and `lemma-spec.k`. The source-complete output
[05-static-inventory.log](/audit-output/evidence/05-static-inventory.log)
contains each sentence's file, line span, category, complete text, and
SHA-256. It contains 1,093 top-level sentences:

- 700 rules: 622 ordinary, 28 `owise`, 43 priority 40, 4 priority 45,
  1 priority 39, 1 combined priority-40/`owise`, and 1 simplification;
- 231 syntax sentences, including 37 function declarations, 85
  `function,total`, 25 `function,total,symbol`, 2 function/token, and 5
  macros;
- 5 contexts, 1 configuration, 28 modules, 89 imports, and 11 claims; and
- no `functional` declaration.

The exhaustive per-file disposition is
[static_rule_review.md](/audit-output/evidence/static_rule_review.md), and the
active constructor-to-rule map is
[used_construct_map.md](/audit-output/evidence/used_construct_map.md).
Every semantic file and every proof-local declaration is covered there,
including configuration/cells, strictness, evaluation order, calls, argument
binding, frames, returns, branch control, indexes, slices, counting, guards,
overlaps, priorities, totality, opaque declarations, and simplifications.

The active path is:

```text
module/statement loading
→ closure lookup and one-argument call
→ parameter frame
→ dot count
→ first-code index/membership
→ left-to-right short-circuit suffix comparisons and slicing
→ ten count calls and integer additions
→ guarded return and frame restoration
```

The first index is reached only after dot count is one, so the string is
nonempty. The `-4` step-1 slice rules correctly clamp short strings and adjust
negative bounds. `cntSub`'s singleton-prefix and non-prefix guards are
complementary and recursion consumes the input. Function return discards the
remaining function continuation and restores the caller frame. The claim
destinations constrain the result and all material state cells.

The proof-local extension contains:

- the syntactic `fileNameCheckBody` macro, mechanically pinned above;
- `decimalDigitCount`, a single exhaustive equation equal to the exact ten
  executed singleton counts;
- `fileExtensionIs`, a single equation for the exact `[-4:]` slice and
  equality;
- `allowedFileExtension`, a single equation for the three exact suffixes; and
- the one guarded, independently proved integer simplification.

The three summary functions occur only in preconditions; none intercepts or
replaces program execution. There is no proof-local priority, opaque symbol,
operational bridge, circularity, helper claim, or task-answer oracle.

The supplied semantics has 25 opaque symbols: 22 float functions, `sortVS`,
`sortKeyVS`, and `md5hexCodes`. None is dependency-reachable from the
expanded program or any claim constraint. Warnings about unused or incomplete
fixed-semantics functions concern constructor-disjoint operations such as
floats, lists, sorting, conversions, and builtins. Inactive rules were
inventoried, not silently omitted.

I found no active rule that enables a false program conclusion on the intended
domain. Accordingly, there is no unsoundness allegation requiring a
false-conclusion witness. The narrower evidence gap is the external
representation correspondence discussed in Stage 7.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh reviewer mutation
is
[reviewer-vacuity.k](/audit-output/evidence/reviewer-vacuity.k). It executes
the exact closure on the ground satisfying input `"a.txt"` but changes the
result-constraining destination from `"Yes"` to `"No"`.

The mutation first built successfully:

```text
kprove reviewer-vacuity.k --definition verification-kompiled-fresh \
  --spec-module REVIEWER-VACUITY --dry-run
```

This exited 0; see
[06-false-mutation-build.log](/audit-output/evidence/06-false-mutation-build.log).
The actual proof command exited 1 with `WarnStuckClaimState`. The residual
`str(iCons(89,iCons(101,iCons(115,.IntSeq))))` is `"Yes"`, while the mutated
destination is `"No"`:
[06-false-mutation-kprove.log](/audit-output/evidence/06-false-mutation-kprove.log).
Stage 4 independently confirms that `"a.txt"` satisfies the corresponding
entry condition and both Python functions return `"Yes"`. The failure is
therefore the expected reachable unmet obligation, not a parse error, timeout,
or unrelated crash.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the supplied MPY semantics, for every finite algebraic `IntSeq` supplied
as the sole argument in the exact initial state, execution of the exact
translated `file_name_check` closure has the following partial-correctness
property:

- it returns `"No"` for empty input, non-unit dot count, a non-ASCII-Latin
  first code, a disallowed suffix, or more than three occurrences of ASCII
  codes `0` through `9`; and
- it returns `"Yes"` when the dot count is one, the first code is in the
  explicit ASCII-Latin set, the suffix is `.txt`, `.exe`, or `.dll`, and the
  ASCII-digit count is at most three.

The partition is unrestricted by length or a finite example set. It includes
arbitrary integer code sequences, so it is at least as broad as the source
contract's string domain. This is partial correctness: the reachability claims
do not separately prove a termination theorem.

As an additional domain check, the reviewer-authored
[unicode-intseq-spec.k](/audit-output/evidence/unicode-intseq-spec.k)
directly supplies non-ASCII code points as `IntSeq`. The claim for U+00E9
followed by `.txt` proves `"No"` because the first code is not ASCII Latin;
the claim for `a` followed by four U+FF11–U+FF14 full-width digits and `.txt`
proves `"Yes"` because only ASCII digits count. Both ground claims closed
together with exit 0 and `#Top`:
[07-unicode-intseq-ground-checks.log](/audit-output/evidence/07-unicode-intseq-ground-checks.log).

### Trusted and informal boundaries

| Boundary | Role | Assessment |
|---|---|---|
| Supplied MPY semantics | Defines execution | Acceptable fixed trust boundary; integrity is exact and every dependency-reachable rule was reviewed. |
| Trusted `py2mpy.py` | Translates Python AST to the MPY term | Acceptable benchmark trust boundary; trusted regeneration is byte-identical and expanded-term identity pins the claim body. |
| K frontend, Haskell prover backend, and SMT solver | Parse, compile, rewrite, and discharge integer/Boolean obligations | Standard unavoidable proof-tool trust boundary. |
| Mathematical `Int`, `Bool`, maps/lists, equality hooks | Low-level data and configuration operations | Acceptable; active uses have ordinary meanings. |
| 25 supplied opaque symbols | Fixed float/sort/MD5 primitives | Inert for this theorem; none is reachable from the program or constraints. |
| CPython `str` ↔ algebraic `IntSeq` | Connects real source inputs to formal input sequences | Soundly motivated and tested, but not established by a universal machine-checked encoding theorem; this is the reason for `CONCERNS`. |
| Differential testing | Tests the source/contract and representation bridge on 420,635 cases | Empirical support only; not used as a substitute for the K proof. |
| Termination | Whether every call terminates | Not claimed by reachability partial correctness; the reviewed recursive operations descend, but no separate total-correctness theorem is asserted. |

The fixed `strToCodes` function decodes only ASCII source literals. All
literals in the submitted program and claims are ASCII, and the symbolic
input bypasses that decoder as an arbitrary `IntSeq`. Thus the formal theorem
does **not** materially narrow the HumanEval source-contract domain. However,
because the CPython-string-to-code-sequence correspondence is supported by
ordinary interpretation, differential evidence, and specific Unicode ground
claims rather than a universal formal encoding theorem, the appropriate
completed-audit classification is `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
