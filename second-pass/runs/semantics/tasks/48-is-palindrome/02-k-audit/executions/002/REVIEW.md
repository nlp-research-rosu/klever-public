# Independent adversarial review: 48-is-palindrome

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed the definitions from source, obtained a fresh
`#Top`, mechanically matched the program term in the claim to the trusted
regeneration, audited the proof-local equation and the supplied semantics, and
made both a body mutation and a distinct false-postcondition mutation fail for
the expected semantic reason. No candidate-provided build product, log, trace,
or prose assertion was used as proof.

## 1. Input and provenance integrity

The launcher declares `record_layout = legacy-selected-stage1` and
`semantics_mode = SUPPLIED_SEMANTICS`. This agrees with the mounts:
`/reference/reference-semantics` is present, is a real directory, and contains
the supplied semantics.

I read `/audit-input.json` first, then independently checked:

- `/audit-campaign-lock.json` is a regular file. Its parsed object exactly
  equals the `audit_campaign` object in `/audit-input.json`, and its SHA-256 is
  the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All records required for `legacy-selected-stage1` are regular, readable,
  non-symlinked files: `/run.json`, `/task.json`,
  `/generation-result.json`, `invocation.json`, `metrics.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`. The optional
  `usage.json` is present and was also read. Historical
  `runtime-metrics.json` is absent, but this layout does not require it.
- The recorded direct hashes of the run/task/result/invocation records,
  generation metrics, usage, prompt, last message, raw output, canonical,
  trusted prompt, and translator all match freshly computed SHA-256 values.
- The one JSONL trace file has SHA-256
  `681b51851d0ba9461e8b8db444ab2311553f32987d8448af185a7dea97dea68c`,
  exactly as recorded in `/generation-result.json`. All 164 JSONL events
  parsed. The full 5,526-line raw output log was also scanned; it contains
  failed construction attempts before the generator's eventual success. Those
  attempts and its final `#Top` claim were treated only as untrusted history.
- An independent implementation of the provenance tree-hash algorithm gives
  the candidate workspace digest
  `398be8e4b6757bc5419caf3e9a5165ef2aa21611ba9606ea35bec98080198f7b`,
  matching both the stage result and invocation. It gives supplied-semantics
  digest
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the recorded semantics manifest hash, and trace digest
  `42ba5e4bb5645b6c258806f22fe85bb514133bfa13a18f67a21204f8183ff37c`,
  matching `usage.json`.
- Recursive, no-dereference comparison of
  `/candidate/reference-semantics` against
  `/reference/reference-semantics` found identical directory and file sets,
  types, sizes, and contents. Neither tree contains a symlink. There are no
  missing, additional, changed, mistyped, or linked entries.
- `/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.

The complete check and all values are in
`/audit-output/evidence/stage1-provenance-verification.log`. Supporting
records are in `stage1-audit-input.log`, `stage1-required-json.log`,
`stage1-generation-trace-extract.log`, and
`stage1-generation-output-scan.log`. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

From `/reference/prompt.py`, the entry point is
`is_palindrome(text: str)`. It must return true exactly when the given string
is a palindrome. The documented cases are the empty string, two odd-length
palindromes, and a non-palindrome.

The trusted canonical implementation in `/reference/canonical.py:19` compares
each code point with the code point at the mirrored index and returns false at
the first mismatch; otherwise it returns true. The candidate in
`/candidate/solution.py` instead computes:

```python
return text == text[::-1]
```

For Python strings, equality with the full negative-step slice is exactly the
same palindrome predicate. The different algorithm does not narrow the
annotated string domain.

### Trusted translation

In the clean scratch copy I ran:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.mpy solution.regenerated.mpy
```

Both submitted and regenerated files have SHA-256
`8278b02d667e625ef15bdd083acb6461d92384f78a36828c230508569475e863`;
`cmp` exited 0. The exact command and status are in
`/audit-output/evidence/stage2-translation-identity.log`.

### Independent differential test

`/audit-output/evidence/differential_test.py` independently imports the trusted
canonical and candidate entry points and also uses a two-pointer oracle. It
preserves its complete generated input set in
`/audit-output/evidence/stage2-differential-inputs.json` (SHA-256
`3f3c4dff4c197a9ef4b44de4ea4ed68db8c7cb43dc31d3fcff0d1245db9b046e`).
The cases comprise:

- all four prompt examples;
- 12 explicit boundary cases covering length 0/1, even/odd length, successful
  completion, first and inner mismatches, NUL, combining characters, emoji,
  and a newline;
- all 9,841 strings of lengths 0 through 8 over the alphabet `a`, `b`, `☃`;
- 2,000 deterministic generated strings, lengths 0 through 64, from a
  Unicode-heavy alphabet with seed 480048.

All three implementations returned actual `bool` values and agreed on all
11,857 inputs. The command exited 0 with `mismatches=0`; see
`/audit-output/evidence/stage2-differential.log`. This is finite fidelity
evidence, not a replacement for the K theorem.

## 3. Clean proof reconstruction

I created `/tmp/audit-work/reconstruction-001` and copied only candidate source
artifacts plus the trusted prompt, canonical, translator, and trusted supplied
semantics. I did not copy or use a candidate `*-kompiled` directory or cache.
The scratch-copy inventory is in
`/audit-output/evidence/stage2-scratch-copy.log`.

The installed live toolchain is K v7.1.293. `kup` is not installed, but
`kompile`, `krun`, and `kprove` are independently available and report the
expected version. Source inventory found exactly one positive target claim,
`/candidate/spec.k:6`.

The fresh commands were:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

Both builds exited 0. The sole positive `kprove` command exited 0 and printed
`#Top`. Its complete bounded log is
`/audit-output/evidence/stage3-positive-kprove.log`; build logs are
`stage3-kompile-llvm.log` and `stage3-kompile-haskell.log`.

I also ran the submitted concrete assertions on the fresh LLVM definition.
`krun concrete-tests.mpy --definition audit-runtime-kompiled` exited 0 with an
empty `<k>` cell, no exception, and exit code 0; see
`stage3-concrete-krun.log`.

The compiler emitted non-exhaustiveness warnings for general-purpose helpers
such as `mapStrVS`, several float conversions, `joinCodes`, and `valSeqAt`, and
unused-variable warnings in `strLt`. None is on this proof's execution path:
the target uses `IntSeq` string slicing and `intSeqAt`, not those helpers.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim in `/candidate/spec.k` has no `requires` clause. Its precondition is
the exact default MPY configuration:

- arbitrary `IS:IntSeq` supplied as the string value `str(IS)`;
- module environment 0 with an empty map and parent builtins frame -1;
- empty heap and call stack, location counters 1 and 0;
- no pending return or exception, and exit code 0.

It loads one module-level function binding with the submitted name, parameter,
and body, then calls that binding on `str(IS)`.

The postcondition requires the `<k>` result to be exactly `palindrome(IS)`.
It also requires the module scope to contain the exact resulting closure and
pins every other state cell: environment, scope and heap counters, heap,
stack, return state, exception, and exit code. This is an exact result
equality, not an implication or a free result variable.

`palindrome` is defined in `/candidate/verification.k:8-10` as:

```text
IS ==K buildIS(IS, isLen(IS) -Int 1, -1, -1)
```

The fixed slice rules start at `length - 1`, stop just before `-1`, and step
by `-1`; `buildIS` therefore selects indices `length-1, ..., 0` and then
terminates. Thus this term is structural equality of the input with its
reverse, the ordinary definition of a palindrome.

### Mechanical program identity

`/audit-output/evidence/check_program_pinning.py` extracted the balanced
`Module(...)` argument of `#loadAll` and compared it with the trusted
regeneration. The only normalization was whitespace/comments and the explicit
`.Stmts` list identity permitted in claim syntax. The normalized
constructor terms were identical.

I then parsed both terms with the fresh K definition using `kast --sort
Module --output kore`. Their KORE files are byte-identical and both have
SHA-256
`1a6e51afdf6a6e48c0d05fe7effe029d22751c3b56b1f85ddb2d10f8931e4a4a`.
See `stage4-program-pinning.log`,
`stage4-kast-constructor-comparison.log`, and the retained
`solution.regenerated.kore` and `spec-executed-program.kore`.

The expected final closure repeats the same body. There are no helper or loop
claims and no substituted function.

### Satisfiable instances

Every `IntSeq` instantiates the claim, so the precondition is plainly
satisfiable. For the concrete witness `IS = .IntSeq`, the start index and stop
are both `-1`, `buildIS` returns `.IntSeq`, and the result is `true`.

For four ground strings, the trusted Python canonical, candidate Python, and
fresh LLVM execution agreed:

| Input | Canonical | Candidate | Fresh K |
|---|---:|---:|---:|
| `""` | true | true | true |
| `"aba"` | true | true | true |
| `"abba"` | true | true | true |
| `"zbcd"` | false | false | false |

The exact K final scope is retained in
`/audit-output/evidence/stage4-concrete-satisfying-inputs.log`.

### Body sensitivity

The separate retained
`/audit-output/evidence/spec-body-mutation.k` changes the program term actually
loaded and called to `Return(Bool(false))`. It also changes the expected
closure body, so it cannot fail merely because source and final scope differ.
It leaves the original result obligation `palindrome(IS)` intact.

`kprove` parsed and executed the mutated body, reached `<k> false`, and then
exited 1 with `WarnStuckClaimState` because the result implication does not
hold. The empty sequence is a ground false witness: the mutated program
returns false while `palindrome(.IntSeq)` is true. See
`stage4-body-sensitivity-kprove.log`.

The formal domain is all finite K `IntSeq` values, which contains the
code-point sequence of every Python string and is broader because K does not
restrict each integer to a valid Unicode scalar. This is harmless
over-coverage, not source-contract narrowing.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/stage5-rule-inventory.tsv` contains every declaration
from all 24 supplied K files, `verification.k`, and `spec.k`, with source file,
line, complete collapsed declaration, attributes, target relevance, and audit
decision. Direct `rg` counts exactly match the generated inventory:

| Kind | Count |
|---|---:|
| syntax declarations | 228 |
| of which `[function]` | 147 |
| configurations | 1 |
| contexts | 5 |
| ordinary rules | 670 |
| `[owise]` rules | 26 |
| target claims | 1 |
| total inventoried declarations | 931 |

Attribute counts are: 107 `total`, 32 `concrete`, 29 priority, 25 symbol, three
macro, and one macro-rec. There are no `functional` declarations and no
`simplification` rules. Completeness evidence is in
`stage5-inventory-completeness.log`; the detailed special-attribute list is in
`stage5-special-attributes.log`.

The supplied tree is the fixed trusted semantics selected by the benchmark.
I nevertheless inspected every source rule. The TSV records declarations and
rules on the target path as `ACCEPT_FIXED_FAITHFUL_ON_TARGET_PATH`, unused
fixed rules as `ACCEPT_FIXED_UNUSED_BY_TARGET`, and the proof-local equation
separately. Grouping those per-entry decisions:

- `syntax.k` and `core.k`: constructor sorts match the trusted translator.
  The configuration is fully pinned. `#loadAll` exposes the real module
  statements, statement sequencing is ordered, and name lookup walks the
  selected scope and builtins parent without fabricating a binding.
- `functions.k` and `call.k`: `FuncDef` installs the actual closure body;
  calls evaluate the callee and arguments left-to-right, allocate a fresh
  frame, bind `"text"` to `str(IS)`, execute the body, and return through
  `#pop`. The saved continuation and environment are restored and the call
  frame is removed. The target's closure-call rule has no competing
  problem-local interception.
- `operators.k`, `int.k`, `str.k`, and `subscript.k`: contexts enforce operand
  and bound evaluation. Unary integer minus maps `1` to `-1`. The three slice
  bounds are evaluated in order; the string slice uses the guarded
  `slStart`/`slStop`/`slStep` and `buildIS` equations. String equality is
  exactly structural `IntSeq` equality. The positive/negative slice guards are
  disjoint, and the recursive index remains in bounds for this fixed
  full-reversal slice.
- `verification.k`: the only candidate extension is the fully covered,
  non-recursive definitional summary `palindrome`. Its sole equation is true
  for every `IntSeq` by definition, has no overlap, priority, `total`,
  `simplification`, or opaque attribute, and does not match or replace a
  program term. It influences only the destination's mathematical
  presentation. It is not an operational bridge or an oracle.
- `assert.k`, `bool.k`, `iter.k`, `range.k`, `list.k`, `tuple.k`, `set.k`,
  `comprehension.k`, `controls.k`, `dict.k`, `methods.k`, `builtins.k`,
  `float.k`, and `sort.k` are imported fixed modules but their task-irrelevant
  operations never become redexes in this claim. `concrete.k` is included only
  by `MPY-KRUN`; the Haskell proof module imports `MPY`, not `MPY-CONCRETE`.

The exact target mapping is:

| Submitted construct | Declaration/behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | `syntax.k:50-61`, `core.k:124-127`, `functions.k:14-16,78-90` |
| `Call(Name("is_palindrome"), ...)` | `call.k:20-21,69-75`, `core.k:130-154,186-191` |
| `Compare(..., CmpOp("==", ...))` | `operators.k:14-17`, `str.k:25` |
| `UnaryOp("-", Int(1))` | `operators.k:10`, `core.k:194`, `int.k:7` |
| `Subscript(..., Slice(NoBound, NoBound, -1))` | `subscript.k:43-121`, `core.k:227-229` |

### Opaque and total symbols

The fixed tree declares 25 symbolic trust-boundary functions:

- sorting/digest: `sortVS`, `sortKeyVS`, `md5hexCodes`;
- float/conversion: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
  `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`,
  `roundFN`, and `sqrtF`.

None appears in the target program, target postcondition, residual, or
proof-local rule. Therefore no opaque value affects a branch, return, state
cell, exception, or theorem conclusion here. The compiler's non-exhaustive
`total` warnings likewise concern unused domains. Relevant functions
`isLen`, slice normalization, and `buildIS` have truthful, guarded,
structurally descending equations on this fixed step.

No rule that can enable a false target conclusion was found, so this review
makes no unsound-rule allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`, so there was no candidate negative
test to trust.

I created the distinct
`/audit-output/evidence/spec-vacuity-audit.k`. It leaves the exact submitted
program term and all state obligations unchanged but changes the destination
from `palindrome(IS)` to `notBool palindrome(IS)`.

First:

```text
kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run --output none
```

exited 0, establishing successful parsing and proof-artifact construction.
Then the same command without `--dry-run` exited 1 and produced
`WarnStuckClaimState`. The residual explicitly contains the actual equality
result and its negation in the failed implication; this is not a parser error,
timeout, unrelated crash, or unreachable mutation.

For the satisfying witness `IS = .IntSeq`, actual execution and
`palindrome(.IntSeq)` are true while the mutated destination is false. Logs are
`/audit-output/evidence/stage6-vacuity-dry-run.log` and
`stage6-vacuity-kprove.log`.

## 7. Proven versus assumed accounting

### What the proof establishes

Under the supplied MPY semantics, for every finite `IS:IntSeq`, starting in the
fully specified default state, loading the exact trusted translation of
`solution.py`, resolving and calling its `is_palindrome` binding on `str(IS)`,
and terminating returns:

```text
IS ==K buildIS(IS, isLen(IS) -Int 1, -1, -1)
```

It also establishes the pinned final module binding and preservation/restoration
of the environment, heap, allocation counters, call stack, return state,
exception state, and exit code. Since the `buildIS` term is the input sequence
in reverse order, this is exactly the requested palindrome result. The theorem
is universal over the modeled string values, not bounded to examples or fixed
lengths.

### Trust ledger

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser/compiler, Haskell backend, and K built-ins for integer/Boolean/map/list/equality reasoning | All formal execution and `#Top` | Standard unavoidable checker trust; acceptable |
| Trusted `/reference/py2mpy.py` | Source-to-constructor bridge | Byte-checked against candidate copy; regeneration is identical; acceptable |
| Trusted supplied semantics | Python-subset execution | Exact recursive integrity check passed; all target-path rules were audited; acceptable |
| Python string to `str(IntSeq)` representation | Relates HumanEval strings to the formal input | Every Python string has a finite code-point sequence; target operations depend only on order and equality; formal domain is broader, not narrower; acceptable |
| `buildIS` full reverse equals mathematical reversal | Relates operational summary to “palindrome” | Follows directly from the disjoint guarded slice equations and descending indices; no opaque symbol is involved; acceptable |
| Trusted canonical and independent differential run | Finite program-fidelity support | 11,857 zero-mismatch cases; empirical only and not used to close the theorem |
| 25 fixed opaque symbols listed above | Other imported language features | None is reachable from or appears in this proof; no dependency; acceptable |

Concrete MPY string-literal conversion is ASCII-only, so the retained LLVM
smoke programs use ASCII. This does not narrow the formal theorem: the entry
claim accepts `str(IS)` directly for arbitrary integer sequences, and slicing
and equality are code-point-parametric. The Unicode-heavy Python differential
run supports the source implementation bridge but is not presented as a
universal K proof.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(auditability and trust accounting) all pass. The proof is result-constraining,
non-vacuous, sensitive to the loaded body, universal over the material source
domain, and contains no task-answer oracle or execution-bypassing rule.

VERDICT: PASS
LEGITIMACY: LEGIT
