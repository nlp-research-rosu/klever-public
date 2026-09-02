# Independent adversarial audit — HumanEval 48 `is_palindrome`

## Executive finding

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPython semantics.

The decisive facts are:

- trusted regeneration is byte-identical to `solution.mpy`;
- the target claim mechanically contains the same `FuncDef` and body, followed
  only by an observation assignment;
- `verification.k` adds no rule, equation, helper, lemma, priority, opaque
  symbol, or operational bridge;
- a clean Haskell definition rebuilt from source proves the sole target claim
  with `#Top` and exit 0;
- the claim ranges over every semantic `IntSeq`, not examples or bounded
  lengths;
- fresh result and body mutations both fail with the expected result-specific
  terminal states.

The concrete string-literal front end of the supplied semantics is ASCII-only.
That limitation does not narrow this theorem: the submitted function contains
no string literal, and its claim supplies the argument directly as
`str(S:IntSeq)`. A ground proof using the integer code point `128578` confirms
that the formal theorem is not ASCII-bounded. The mapping from Python strings
to code-point sequences remains part of the ordinary model-adequacy trust
boundary, not a proof-local assumption.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- `record_layout`: `pipeline-v3`;
- `condition`: `kit-semantics`;
- `semantics_mode`: `SUPPLIED_SEMANTICS`;
- `mount_reference_semantics`: `true`.

The rendered mode and trusted mounts agree, so no infrastructure-stop condition
was triggered.

I read the launcher manifest and all records required for `pipeline-v3`:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the 225-line structured JSONL trace. These generation records
were treated only as untrusted historical claims.

The independent checker in `evidence/provenance_check.py` established:

- every required record is a real regular file or directory;
- every recorded per-file SHA-256 matches the mounted object;
- the structured trace file hash matches `generation-result.json`, and every
  one of its 225 lines parses as JSON;
- `/audit-campaign-lock.json` has the recorded hash and is exactly equal as
  structured JSON to the `audit_campaign` block in `/audit-input.json`;
- the complete candidate mount has 779 entries, no symlinks or unsupported
  nodes, and an independently computed reviewer tree hash;
- the required candidate deliverables are real regular files;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts;
- the 25-entry candidate `reference-semantics/` tree is exactly equal to the
  trusted tree by relative path, entry type, and file content, with no missing,
  extra, mistyped, changed, or symlinked entry.

Exact results and exit status are in `evidence/01-provenance.log`. Stage 1
passes.

## 2. Program fidelity and canonical comparison

### Source contract

`/reference/prompt.py` defines `is_palindrome(text: str)` and says to determine
whether the given string is a palindrome. Its examples require:

- `""`, `"aba"`, and `"aaaaa"` to return `True`;
- `"zbcd"` to return `False`.

`/reference/canonical.py` checks every symmetric pair and returns `False` on
the first mismatch, otherwise `True`. Thus the intended domain is all Python
`str` values, with no length or alphabet bound, and the result is true exactly
when the code-point sequence equals its reversal.

The submitted implementation is:

```python
def is_palindrome(text: str):
    return text == text[::-1]
```

This is an equivalent algorithm on the intended string domain.

### Trusted regeneration

In the clean scratch copy I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy /candidate/solution.mpy
```

Both exited 0. Both files have SHA-256
`8278b02d667e625ef15bdd083acb6461d92384f78a36828c230508569475e863`.
See `evidence/02-regeneration.log`.

### Independent differential test

`evidence/differential_audit.py` imports the trusted canonical and submitted
entry points by absolute path. It also uses an independent quantified
symmetric-index definition as a third oracle. Its cases include:

- all documented examples;
- empty, one-character, two-character equal/unequal, odd/even palindrome,
  first and late mismatch boundaries;
- NUL, newline, combining characters, BMP Unicode, supplementary-plane emoji,
  and the maximum Unicode code point;
- every string of length 0 through 6 over four symbols;
- 2,000 deterministic generated strings of lengths 0 through 64.

Command and result:

```text
python3 /audit-output/evidence/differential_audit.py
TOTAL_CASES=7476
MISMATCHES=0
EXIT_STATUS=0
```

See `evidence/03-differential.log`. Differential testing is finite adequacy
evidence, not a substitute for the K theorem. Stage 2 passes.

## 3. Clean proof reconstruction

Only source artifacts were copied to
`/tmp/audit-work/48-is-palindrome-audit`. Candidate
`runtime-kompiled/`, `verification-kompiled/`, caches, binaries, logs, and
traces were not copied or used.

The successful clean reconstruction used new, previously absent output
directories and the following commands:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-review4-kompiled

python3 py2mpy.py runtime-audit.py > runtime-audit.mpy
krun runtime-audit.mpy --definition runtime-review4-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-review4-kompiled

kprove spec.k --definition verification-review4-kompiled \
  --spec-module SPEC --claims SPEC.is-palindrome
```

The concrete run ended with `.K`, `NoExc`, and exit code 0. Static enumeration
found exactly one positive target claim. Its independent proof printed exactly
`#Top` and exited 0. The full bounded build/proof record is
`evidence/04d-clean-rebuild-and-positive-proof.log`; the reviewer driver is
`evidence/rebuild_and_prove.sh`.

Earlier reviewer smoke attempts are preserved in `evidence/04-*.log` through
`04c-*.log`. Two deliberately included non-ASCII literals exposed the supplied
semantics' documented ASCII-only literal path: supplementary emoji was rejected
by the K scanner, and `"é"` stopped at `strToCodes`. A later attempt completed
both builds but stopped before proof because of a reviewer inventory-regex bug.
None used a candidate cache, and none is a candidate proof failure. The final
ASCII concrete fixture and symbolic all-`IntSeq` proof completed cleanly.

Stage 3 passes.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

`SPEC.is-palindrome` has no `requires` clause. Its formal input is every finite
`S:IntSeq`. It starts from the exact initial MPython configuration, loads a
module containing the submitted function, calls that function with `str(S)`,
and stores the return in module variable `__result`.

The destination requires:

- `<k>` to be empty;
- the module scope to contain the exact function closure and
  `__result |-> (S ==K buildIS(S, isLen(S)-1, -1, -1))`;
- the caller environment and scope allocator to be restored;
- empty heap, unchanged heap allocator, empty call stack, `noRet`, `NoExc`, and
  exit code 0.

The result is neither free nor existential. It is fixed to equality between
the input sequence and the sequence read from its last index down to zero.

### Mechanical identity

`evidence/pinning_check.py` performs balanced-constructor extraction rather
than a substring search. It established:

- regenerated MPython is byte-identical to submitted MPython;
- the first `FuncDef` in the claim is constructor-identical, modulo whitespace,
  to the regenerated program's `FuncDef`;
- the destination closure body is constructor-identical to the regenerated
  body;
- the only added executable suffix is
  `Assign(Name("__result"), Call(Name("is_palindrome"), str(S)))`.

All checks passed with exit 0 in `evidence/05-pinning.log`. This is a normal
observation harness around the same function binding and body, not a
substituted implementation.

### Satisfying states and concrete substitutions

Because there is no `requires` clause, the explicit initial configuration is
satisfiable for every constructor `IntSeq`; the empty sequence is the simplest
witness.

`evidence/ground_substitution.py` substitutes empty, one-character,
palindrome, non-palindrome, and Unicode code-point sequences into the claimed
reversal expression and compares it with both Python implementations. Every
result agrees (`evidence/06-ground-substitution.log`).

Reviewer-generated ground K claims then replaced the symbolic input and result
with:

- empty sequence → `true`;
- codes for `"aba"` → `true`;
- codes for `"ab"` → `false`;
- codes `(128578, 233, 128578)` → `true`.

Each independently printed `#Top` and exited 0. The generator, commands, and
outputs are in `evidence/instantiate_ground_specs.py`,
`evidence/run_ground_specs.sh`, and `evidence/09-ground-kprove.log`.

Finally, `evidence/spec-reviewer-body-mutation.k` changes both program-body
constructor occurrences to `Return(Bool(false))` while retaining the required
empty-string result `true`. It builds, then fails with a terminal
`__result |-> false` state (`evidence/11-body-sensitivity.log`). The theorem is
sensitive to the body actually executed.

Stage 4 passes.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/build_rule_inventory.py` inventories every source-level declaration
block in the 24 supplied K files, `verification.k`, and the target spec. The
complete, line-addressed inventory is `evidence/rule-inventory.tsv`; its summary
is `evidence/07-rule-inventory-summary.log`.

It contains 1,096 items:

- 695 ordinary source rules;
- 227 syntax declarations;
- 5 contexts;
- 1 configuration;
- 25 file requirements, 88 imports, 27 modules, 27 endmodules;
- 1 target claim.

Attributes inventoried from declaration brackets include 145 `function`, 107
`total`, 35 `concrete`, 45 `priority`, 26 `owise`, 25 `symbol`, 22
`no-evaluators`, 4 `macro`, 2 `strict`, and 1 `seqstrict` items. There are no
`functional`, `simplification`, or `anywhere` items. Every inventory row has a
target-relevance classification and a static decision. Rules outside the
target slice are explicitly marked fixed-baseline and not relied upon; no
target-domain false conclusion witness was found for any such rule, so they
are not mislabeled as unsound.

Most importantly, the proof-local rows are only:

```text
requires "reference-semantics/semantics.k"
module VERIFICATION
  imports MPY
endmodule
```

There is no candidate-added function, totalization, rule, simplification,
priority, claim, opaque symbol, or operational bridge in the proof definition.
The target claim is compiled as a spec and is not imported as a semantic rule
into `VERIFICATION`.

### Used construct map and active rules

| Submitted construct | Declaration and semantics |
|---|---|
| `Module`, `FuncDef`, statement list | `syntax.k`; `core.k` module/statement sequencing; `functions.k` closure binding |
| `Assign`, `Call`, `Name` | strict RHS in `syntax.k`; `controls.k` assignment; `call.k` callee/argument route; `core.k` lookup |
| `Return`, `Compare` | strict return; `functions.k` return/pop; comparison contexts and dispatch in `operators.k` |
| `Subscript`, `Slice`, `NoBound` | subscript contexts and bound-evaluation chain in `subscript.k` |
| `UnaryOp("-", Int(1))` | strict unary operand, integer literal, `applyUn("-", I)` |
| string equality | `str.k` maps `str(A) == str(B)` to structural `A ==K B` |
| reverse slice | `slStep=-1`, `slStart=len-1`, `slStop=-1`, and `buildIS` in `subscript.k` |

The exact active source rows are extracted in
`evidence/08-attribute-summary.log`. Their behavior is:

1. Module load preserves statement order. `FuncDef` binds the exact body in
   module scope 0.
2. `Call` evaluates the function name, then the single argument left-to-right.
   The resulting closure creates fresh frame 1 with parent 0, binds `text` to
   `str(S)`, and saves the caller continuation.
3. `Return` evaluates its expression before control transfer. `Name("text")`
   resolves from the callee frame.
4. Subscript contexts evaluate the object and then the slice bounds in order.
   The two missing bounds become `noB`; `Int(1)` becomes 1 and unary minus
   uniquely becomes `-1`.
5. For negative step, the guards selecting `slStart=len-1` and `slStop=-1` are
   disjoint from their positive-step alternatives.
6. For a finite sequence of length `n`, `buildIS` starts at `n-1`. Its recursive
   guard and base guard are logical complements. The index decreases by one;
   every `intSeqAt` call is in bounds; recursion stops at `-1`. The result is
   exactly the reverse sequence. Empty input immediately selects the base rule.
7. String equality therefore returns exactly the postcondition expression.
   Return/pop restores the caller, removes the callee frame, and restores the
   allocator; module assignment records the Boolean. No allocation, exception,
   output, or other observable state is skipped.

The applicable equations are covered, pairwise guard-disjoint or agreeing, and
descending on this fixed `-1` slice path. No target-active priority rule
preempts a conflicting behavior. The `owise` generic call/compare routes are
the ordinary dispatch routes because no more specific target rule overlaps
them.

### Opaque and incomplete fixed-semantics boundaries

`evidence/opaque-ledger.md` enumerates all 22 explicit
`[no-evaluators]` symbols, plus constructor-equational functions that can stay
abstract or have compiler-reported uncovered cases. Float, sorting, MD5,
`strLt`, `valSeqAt`, `mapStrVS`, and `joinCodes` are not reached. The target
uses no result-bearing opaque symbol.

LLVM compilation reports non-exhaustiveness for several of those unrelated
fixed functions. The target does use `intSeqAt`, which is intentionally partial
outside nonnegative in-bounds indices; the reverse builder establishes exactly
that safe domain. It does not use total-but-under-specified `valSeqAt`.

The supplied `Str(String)` literal rule is ASCII-only. Concrete witnesses
`"é"` and `"🙂"` expose that coverage gap, as recorded in the early smoke logs.
This is not a false rule, and it is unreachable from the submitted body and
symbolic entry claim. The formal domain remains all `IntSeq`, including the
ground supplementary-plane witness proved above.

No rule that encodes the palindrome answer, fabricates a used result, replaces
the function call, or permits a false target conclusion was found. Stage 5
passes.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`.
`evidence/spec-reviewer-false.k` is a fresh reviewer-authored mutation. It
executes the exact submitted function on `str(.IntSeq)` from the explicit
satisfiable initial state but changes the result obligation to
`__result |-> false`.

Commands:

```text
kprove spec-reviewer-false.k \
  --definition verification-review4-kompiled \
  --spec-module SPEC-REVIEWER-FALSE --dry-run

kprove spec-reviewer-false.k \
  --definition verification-review4-kompiled \
  --spec-module SPEC-REVIEWER-FALSE \
  --claims SPEC-REVIEWER-FALSE.empty-must-be-false
```

The dry run exited 0, proving that the mutation parses and builds. The proof
exited 1 with `WarnStuckClaimState`; its terminal residual had `.K`, `NoExc`,
exit code 0, and `__result |-> true`, while the destination required `false`.
This is the expected unmet result obligation, not a parser error, timeout,
unreachable mutation, or unrelated crash.

The exact output is `evidence/10-fresh-non-vacuity.log`, and the driver is
`evidence/run_fresh_mutation.sh`. Stage 6 passes.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied `MPY` definition and K's reachability logic, for every
finite `S:IntSeq`, executing the exact translated `is_palindrome` function on
`str(S)` from the stated initial configuration reaches the fully constrained
terminal configuration with:

```text
__result |-> (S ==K buildIS(S, isLen(S) -Int 1, -1, -1))
```

The other modeled cells have the exact normal-return state. By the inspected
fixed slice equations, `buildIS` in this invocation is the reversal of `S`.
Thus the formal returned Boolean is true exactly when the modeled string is a
palindrome. This is an unrestricted symbolic theorem, not a finite-size
unrolling.

### Trusted or informal boundary

| Boundary | Influence | Assessment and evidence |
|---|---|---|
| Trusted `py2mpy.py` | Selects the executed constructors and function body | Acceptable. It is launcher-trusted, candidate-identical, and fresh regeneration is byte-identical. Constructor-level claim comparison passes. |
| Supplied `MPY` semantics | Defines loading, binding, call/return, slice, equality, and state | Acceptable fixed foundation for `SUPPLIED_SEMANTICS`. The complete source was integrity-checked and inventoried; every target-active rule was reviewed. No proof-local extension exists. |
| K v7.1.293 compiler, Haskell/LLVM backends, Kore execution, builtin integer/list/equality theories | Establishes compilation, concrete execution, and reachability closure | Ordinary low-level trust boundary. Fresh positive, ground, negative, and body-sensitive outcomes are mutually discriminating. |
| Python `str` ↔ semantic `IntSeq` of code points | Transfers the formal sequence theorem to the HumanEval input type | Acceptable model-adequacy bridge for this property. Equality and reversal depend only on sequence order. Python differential coverage includes Unicode, and a K ground claim covers code point 128578. Concrete source literals remain ASCII-only, but the function body has no literal and the entry value is injected directly. |
| Mathematical reading of `buildIS(S,len(S)-1,-1,-1)` as reversal | Connects the operational expression to “palindrome” | Established by exhaustive inspection of the applicable guarded equations and their decreasing index; concrete substitutions and ground K claims support the interpretation. |

No trusted primitive or opaque symbol supplies the palindrome answer. No
empirical result is used in place of the K reachability proof.

### Not claimed

The artifact does not prove the translator, the supplied semantics, K, or
CPython themselves correct. It does not model arbitrary non-string inputs,
which are outside the annotated source contract. It does not establish
resource bounds or a complete Python exception/Unicode-literal parser. These
exclusions do not narrow the theorem's material `str` input domain or its
palindrome result.

All seven required stages pass. The proof is sound under the selected fixed
semantics, result-constraining, body-sensitive, and pinned to the real
regenerated program without a material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
