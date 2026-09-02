# Adversarial review: 16-count-distinct-characters

The candidate has a reproducible, non-vacuous K reachability proof of a
result-constraining statement under its submitted theory. It also pins the
submitted translated body. It is nevertheless not a legitimate proof of the
real generated Python program: the generated semantics implements only ASCII
`A`-`Z` lowercasing, while the unrestricted Python `str` contract and trusted
canonical implementation use Unicode-aware `str.lower()`. On the satisfying
input `"Ää"`, the rebuilt K semantics returns and proves `2`; both the trusted
canonical and submitted Python return `1`.

The complete reviewer command ledger is
[evidence/COMMANDS.md](/audit-output/evidence/COMMANDS.md). All mutations,
scripts, and logs are reviewer-authored and reside below
`/audit-output/evidence`; all builds reside below `/tmp/audit-work`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `16-count-distinct-characters`;
- condition `bare`;
- `record_layout: legacy-selected-stage1`;
- `semantics_mode: GENERATED_SEMANTICS`;
- no mounted reference semantics.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, and the lock's SHA-256 is the recorded
`ad5dfc...745`. The required launcher records for this layout are present,
readable regular files: `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace.
The optional `usage.json` is also present and was inspected. Historical
runtime metrics are absent and were not reconstructed, as required for this
legacy-selected layout.

There are no symlinks or unsupported entries in the candidate, reference, or
generation-evidence trees. `/reference/reference-semantics` is absent, which
is exactly the required generated-semantics boundary. The candidate's
`prompt.py` and `py2mpy.py` are byte-identical to the trusted mounted versions.
The independently calculated file hashes match the hashes in
`/audit-input.json`. The independently implemented stage-1 content-tree hash
of `/candidate` is
`6e5af0c42054365d33dfc2d5bf0126312f76d701a1d913e060a355b66684a044`,
matching both the retained-workspace hash in `invocation.json` and the
workspace hash in `generation-result.json`. The trace file hash matches the
generation result, and its content-tree hash matches `usage.json`. The
audit-wrapper's separately recorded directory digests are preserved verbatim
in the log; no unspecified host provenance path was followed.

Evidence:

- [provenance_check.py](/audit-output/evidence/provenance_check.py) and
  [01-provenance.log](/audit-output/evidence/01-provenance.log), exit 0;
- [generation_record_summary.py](/audit-output/evidence/generation_record_summary.py)
  and
  [01-generation-record-summary.log](/audit-output/evidence/01-generation-record-summary.log),
  which parse all 122 JSONL trace records and the 6,433-line text log;
- [00-toolchain.log](/audit-output/evidence/00-toolchain.log): K 7.1.293 and
  Python 3.10.12.

The generation records claim prior successful construction and `#Top`. They
were treated only as untrusted historical claims and did not supply any proof
result used below. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks for the number of distinct characters in a Python
string regardless of case. The trusted canonical operationalizes that contract
as:

```python
return len(set(string.lower()))
```

The submitted `solution.py` has exactly the same function signature and
expression (it merely omits the docstring). The source domain is Python
`str`; neither the prompt nor canonical restricts characters to ASCII.
Because the canonical uses `lower`, the authoritative behavior is Python
`str.lower`, not a stronger `casefold` interpretation.

Regeneration with the trusted translator:

```text
python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/source/solution.py |
  cmp - /tmp/audit-work/source/solution.mpy
```

exited 0, establishing byte identity. See
[02-translator-byte-identity.log](/audit-output/evidence/02-translator-byte-identity.log).

The independent differential script imports the canonical and submitted entry
points separately. It checks the two documented examples, empty and singleton
boundaries, mixed case, digits, whitespace, NUL, combining characters,
extended Latin, Greek, Turkish-I, sharp-S, and emoji cases, then 2,000
deterministically generated strings of lengths 0 through 32. It found zero
mismatches across 2,018 cases. This is finite implementation-fidelity
evidence, not a K proof. See
[differential_test.py](/audit-output/evidence/differential_test.py) and
[02-python-differential.log](/audit-output/evidence/02-python-differential.log).

## 3. Clean proof reconstruction

Only the eight submitted source artifacts were copied explicitly to
`/tmp/audit-work/source`; candidate `__pycache__`, compiled definitions, and
caches were not copied or reused. Fresh definitions were built into
`/tmp/audit-work/build`:

- LLVM `semantic.k`, main module `SEMANTIC`, syntax module `MPY-SYNTAX`:
  exit 0 in
  [03-kompile-concrete.log](/audit-output/evidence/03-kompile-concrete.log).
- Haskell `verification.k`, main module `VERIFICATION`, syntax module
  `MPY-SYNTAX`: exit 0 in
  [03-kompile-proof.log](/audit-output/evidence/03-kompile-proof.log).

`spec.k` contains four positive claims, at source lines 7, 25, 40, and 55;
the inventory is
[03-positive-claims-list.log](/audit-output/evidence/03-positive-claims-list.log).
One fresh `kprove` command over the original `SPEC` module independently ran
all four. It exited 0 and printed `#Top`; see
[03-kprove-positive.log](/audit-output/evidence/03-kprove-positive.log).

The fresh LLVM semantics concretely executed the exact `solution.mpy` on
normal and boundary inputs. It returned 3 for `"xyzXYZ"`, 4 for `"Jerry"`, 0
for empty, and 3 for `"AaBb!"`, agreeing with both Python implementations. It
returned 2 for `"Ää"` (and 3 for `"Αα"`), disagreeing with Python. The full
bounded configurations and exit 0 are in
[03-krun-concrete.log](/audit-output/evidence/03-krun-concrete.log); the
corresponding Python values are in the differential and Unicode-oracle logs.

Thus clean K reconstruction succeeds, but dynamic reconstruction already
exposes a semantics-fidelity failure.

## 4. Adequacy and real-program pinning

### Claims in plain language

The universal claim has no explicit `requires`. Its initial configuration
contains:

- the concrete `Module(FuncDef(...))` constructor tree for
  `count_distinct_characters`;
- an empty environment;
- any `S:String` in `<input>`;
- `noResult`.

Its destination consumes `<k>`, binds `string` to `StrVal(S)`, preserves the
input, and requires the exact result
`IntVal(expectedDistinctCharacters(S))`. The three ground claims use the same
program/configuration with `"xyzXYZ"`, `"Jerry"`, and `""`, requiring results
3, 4, and 0 respectively. Each precondition is plainly satisfiable by the
fresh initial configuration for its input; the universal one is satisfied,
for example, by `S=""`, `S="xyzXYZ"`, and `S="Ää"`.

The claim term is not a substituted program. The reviewer mechanically
extracted the first entry claim, normalized only `.Exprs` (K's empty-list
unit) to the corresponding empty concrete list position, parsed both terms
with the fresh definition, and compared their KAST JSON. Both hashes are
`0b0efd...fa88`, and `cmp` exits 0. See
[extract_claim_program.py](/audit-output/evidence/extract_claim_program.py)
and
[04-program-term-identity-v2.log](/audit-output/evidence/04-program-term-identity-v2.log).
The earlier `04-program-term-identity.log` is a retained diagnostic in which
`.Exprs` was incorrectly fed directly to the concrete `.mpy` parser; it is not
relied upon.

There are no loops or helper claims. Every material operation in the actual
body is dispatched: parameter binding, `string` lookup, `lower`, `set`, `len`,
return, and result write. A material body-sensitivity mutation removed the
`lower()` call from the term actually executed by its claim. On `"Aa"` the
mutated execution reached `IntVal(2)`, could not establish the original target
1, produced `WarnStuckClaimState`, and exited 1. See
[spec-body-mutation.k](/audit-output/evidence/spec-body-mutation.k) and
[04-body-sensitivity.log](/audit-output/evidence/04-body-sensitivity.log).

Concrete substitution distinguishes theorem adequacy:

| Satisfying input | Formal/K result | Canonical Python | Submitted Python |
|---|---:|---:|---:|
| `""` | 0 | 0 | 0 |
| `"xyzXYZ"` | 3 | 3 | 3 |
| `"Ää"` | 2 | 1 | 1 |

The claim pins the real translated body, but its semantics/postcondition does
not pin the real meaning of Python `lower` over the source domain.

## 5. Rule-by-rule static soundness review

The exhaustive local inventory is
[rule-inventory.md](/audit-output/evidence/rule-inventory.md). It covers every
submitted K declaration:

- D01-D07: `Program`, `Stmts`, `Stmt` (`FuncDef`, `Return`), `Params`,
  `Strings`, `Expr` (`Name`, `Attribute`, `Call`), and `Exprs`;
- D08-D12: `Value`, `Result`, `KResult`, the four continuation items, and the
  four-cell configuration;
- D13-D16: functions `lowerString`, `lowerChar`, `charsSet`, and
  `expectedDistinctCharacters`;
- R01-R10: all ordinary configuration/operational rules;
- R11-R16: every semantic function equation;
- R17: the verification summary equation;
- C01-C04: all reachability claims.

There are no local `[total]`, `[functional]`, `[simplification]`,
`[concrete]`, explicit-priority, or opaque declarations. `lowerChar` has one
`[owise]` equation, which receives the generated lower priority. The only
imports are K's `STRING-SYNTAX`, `INT`, `BOOL`, `STRING`, `SET`, and `MAP`.

Construct coverage is complete for the submitted AST. R01 loads the exact
single function and binds its one parameter. R02 evaluates the sole return
expression. R08, R06, and R04 enforce the actual outside-in control sequence
for `len(set(string.lower()))`; their argument/receiver continuations then
produce inside-out value evaluation. R03 reads the parameter. R05, R07, and
R09 apply lower/set/length. R10 writes the only observable result. `<env>` is
written once and read once; `<input>` is read and preserved; `<result>` is
written once. No used construct needs heap, allocation, I/O, exceptions, or a
call stack.

R01/R02 and primitive-name dispatch are deliberately narrow, not reusable
Python semantics. R02 also admits a framed K continuation rather than modeling
general Python call/return unwinding. No such caller state is reachable from
this submitted top-level program, so these are coverage/reuse limitations,
not witnessed false conclusions on the intended execution. Direct dispatch of
`set` and `len` is binding-correct here because the real module defines no
shadowing binding. Missing behavior for unused Python constructs is permitted
in generated-semantics mode.

The function equations have disjoint guards at their uses:

- `lowerString` and `charsSet` split empty from nonempty strings, cover those
  cases, and recurse on a strictly shorter suffix;
- `lowerChar` splits ASCII uppercase from its `owise` complement;
- `expectedDistinctCharacters` is unconditional;
- the operational call patterns for lower, set, and len do not overlap on the
  used term.

The material failure is R14, `lowerChar(C) => C [owise]`, combined with R05.
It treats every non-ASCII-uppercase character as unchanged. This does not
model Python `str.lower`. The required concrete false-conclusion witness is:

1. `"Ää"` is a Python `str` and satisfies the universal entry precondition.
2. For `C="Ä"`, the ASCII guard `65 <= ordChar(C) <= 90` is false, so R14
   leaves `Ä` unchanged.
3. The generated semantics therefore obtains two distinct characters and
   returns `IntVal(2)`.
4. The reviewer-added concrete reachability claim requiring 2 builds, exits
   0, and prints `#Top`; see
   [spec-unicode-witness.k](/audit-output/evidence/spec-unicode-witness.k) and
   [05-unicode-false-conclusion-kprove-v2.log](/audit-output/evidence/05-unicode-false-conclusion-kprove-v2.log).
5. Python evaluates `"Ä".lower()` to `"ä"`, so both independent Python
   implementations return 1; see
   [05-unicode-python-oracles.log](/audit-output/evidence/05-unicode-python-oracles.log).

The first Unicode witness run used an unresolved relative `requires` and
exited 113; that parser diagnostic is retained in the non-authoritative
`05-unicode-false-conclusion-kprove.log`. The corrected `-v2` run is the
successful false-conclusion witness.

R17 is a truthful definition *of the generated model*:
`size(charsSet(lowerString(S)))`. But it reuses the same result-bearing
helpers used by execution and has no bridge theorem establishing that
`lowerString` equals Python `str.lower`. Consequently `#Top` mainly proves
constructor dispatch to the model's own summary; it does not repair the false
source-language semantics.

This is a material real-program soundness and source-domain adequacy failure,
not merely thin empirical support. It has the required satisfying false
witness.

## 6. Fresh non-vacuity test

The reviewer created a distinct `SPEC-VACUITY` module using the unchanged
submitted program and satisfying prompt-example input `"xyzXYZ"`, but changed
the result obligation from the true 3 to the false 4. The spec built
successfully during `kprove`; execution reached `.K` with `IntVal(3)`, the
claim produced `WarnStuckClaimState`, and `kprove` exited 1 for the expected
unmet result obligation.

Evidence:

- [spec-vacuity.k](/audit-output/evidence/spec-vacuity.k);
- [06-false-postcondition.log](/audit-output/evidence/06-false-postcondition.log).

This is a meaningful proof failure rather than a parser error, timeout,
missing import, or unreachable mutation. The original proof is therefore
result-constraining and non-vacuous. Non-vacuity does not cure the wrong
semantics.

## 7. Proven versus assumed accounting and decision

Precisely stated, the successful reachability proof establishes partial
correctness of the exact submitted constructor term under the candidate's K
model: for any modeled K string `S`, a terminating run reaches the result
`size(charsSet(lowerString(S)))`, with the modeled environment/input state
described above. It also establishes the three ASCII ground examples.

It does **not** establish the HumanEval theorem over Python strings. The
unproved—and false—bridge is that candidate `lowerString` implements Python
`str.lower` for every source-domain input.

The full trust accounting is
[trust-ledger.md](/audit-output/evidence/trust-ledger.md). In summary:

- trusted low-level boundaries are K 7.1.293 and its parser/backends, plus K
  STRING, SET, and MAP primitives;
- the translator link is byte-checked, and the claim/program link is
  constructor-checked;
- there are no opaque proof symbols, proof-local simplifications, axioms,
  totality declarations, or auxiliary claims;
- `lowerString`, `charsSet`, and `expectedDistinctCharacters` are explicit
  equations, but the first is not a faithful Python primitive;
- Python differential testing supports candidate-versus-canonical fidelity
  only on its tested cases and is not substituted for the K proof;
- the K/Python Unicode disagreement is a direct counterexample to the required
  semantics bridge.

Kit Gate A (real-program soundness) fails on the witnessed lower operation.
Gate B (intent/domain adequacy) also fails because the unrestricted `str`
domain is materially reduced to behavior that is correct only for
ASCII-case interactions. Gate C evidence is reproducible, but cannot rescue
the failed theorem. Under the benchmark's explicit mapping, even a
sound-but-limited theorem that materially narrows the HumanEval source
contract is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
