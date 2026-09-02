# Independent adversarial review: 50-decode-shift

The candidate is **not a legitimate proof**. Fresh reconstruction does produce
`#Top` for all three submitted claims, the theorem is non-vacuous, and the
executed closure is mechanically identical to the regenerated target function.
However, the top-level proof depends on an operational loop bridge whose match
domain is strictly broader than its separately proved connection claim. The
bridge accepts an arbitrary builtin scope and can prove a concrete false
execution result. That is a material proof-rule unsoundness, so the successful
top-level `#Top` cannot establish the real-program theorem.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `50-decode-shift`;
- condition `semantics`;
- `semantics_mode = SUPPLIED_SEMANTICS`;
- `record_layout = legacy-selected-stage1`.

The trusted `/reference/reference-semantics` tree is present, as required for
this mode. There is no mode/mount contradiction.

I independently checked the launcher records with
`evidence/stage1/provenance_audit.py`; its bounded output is
`evidence/stage1/provenance.log`.

- `/audit-campaign-lock.json` is a real regular file, its SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  and its parsed object exactly equals the `audit_campaign` block.
- All launcher-required files and directories for
  `legacy-selected-stage1` are present, readable, correctly typed, and not
  symlinks.
- The 15 launcher-recorded regular-file hashes checked by the script match.
  The seven evidence-output hashes declared by `/generation-result.json`,
  including the structured trace file, also match.
- All eight JSON records found at the layout locations parsed successfully.
  The one structured trace file was consumed as 363 valid JSONL records. The
  817,669-byte `codex-output.log` and 404-byte `codex-last.txt` were consumed
  in full. Their contents were treated only as untrusted generation claims.
- `usage.json` is present and was inspected. Historical
  `runtime-metrics.json` is absent, but the prompt explicitly says it was never
  required for this legacy-selected layout.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`;
  `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Recursive type/path/content comparison of
  `/candidate/reference-semantics` and
  `/reference/reference-semantics` succeeds for all 25 directory/file
  entries. There are no missing, additional, changed, mistyped, special, or
  symlinked entries. The independent manifest digest is
  `c9d5d164df7f4f2318a280b9b9faab7e52c8e8ae500adcb11adce70b24190d20`.

The observed toolchain is K 7.1.293 and Python 3.10.12
(`evidence/stage1/toolchain.log`). No infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt defines `encode_shift(s)` as shifting each character by
five modulo the 26-letter alphabet. It asks `decode_shift(s)` to decode a
string produced by that encoder. Therefore the material argument domain is
finite strings of lowercase ASCII codes 97 through 122, including the empty
string. Every encoder output is in this domain.

The trusted canonical implementation returns, for each input character `ch`,

```text
chr(((ord(ch) - 5 - ord("a")) % 26) + ord("a"))
```

and concatenates these characters left to right.

`/candidate/solution.py` implements exactly that operation with an explicit
accumulator and `for` loop. The choice of loop instead of comprehension does
not change the result.

### Translation identity

I regenerated the program with the trusted translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/solution.regenerated.mpy
cmp -s /tmp/audit-work/fresh/solution.regenerated.mpy \
  /tmp/audit-work/fresh/solution.mpy
```

Both commands jointly exit 0; the regenerated file is byte-identical to the
submission (`evidence/stage2/regeneration.log`).

### Independent differential testing

`evidence/stage2/differential.py` independently imports the trusted canonical
entry point and generated entry point. It checks:

- empty input;
- all 26 one-character values;
- the wrap boundaries below, at, and above input `f`;
- whole-alphabet and wraparound patterns;
- long repetitive boundary patterns;
- every lowercase string through length three;
- fixed-seed generated strings at lengths 4 through 1024;
- representative `decode_shift(encode_shift(x)) = x` lowercase cases.

The run covered 18,563 decoder cases and five inverse cases. It exits 0 with
zero mismatches and zero inverse failures
(`evidence/stage2/differential.log`). This is finite evidence, not a
replacement for the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/fresh`, using the trusted
semantics tree. I did not copy or use the candidate's `kore-exec.tar.gz`,
`__pycache__`, compiled definitions, or caches.

The exact commands and statuses are indexed in
`evidence/command-index.txt`. The complete bounded logs are under
`evidence/stage3/`.

### Concrete definition

The trusted semantics compiled from source with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

Exit status was 0. The trusted translator also reproduced
`concrete_tests.mpy` byte-for-byte. Fresh `krun` execution exited 0 with
`.K`, `NoExc`, and `<exit-code> 0 </exit-code>`
(`evidence/stage3/01-kompile-runtime.log` through
`03-krun-concrete.log`).

### Proof definitions and every positive target

The base proof definition compiled from source with exit 0:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-base-kompiled
```

Individually:

- `SPEC.decode-loop`: exit 0 and `#Top`;
- `SPEC.char-inverse`: exit 0 and `#Top`.

The extended definition also compiled from source with exit 0:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-WITH-LOOP --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

`SPEC.decode-shift` then exited 0 and printed `#Top`.

The logs are
`evidence/stage3/04-kompile-base.log` through
`08-kprove-decode-shift.log`. Thus the candidate's dynamic reconstruction
claim is reproducible. This stage establishes closure under the submitted
theory only; Stage 5 shows that theory is unsound.

## 4. Adequacy and real-program pinning

### Plain-language claim meanings

1. **`decode-loop`** (`spec.k:8`): from an exact function-frame state, if
   `CS` is a lowercase code sequence, executing the real `#loop` over `CS`
   consumes it, preserves the arbitrary continuation `KONT`, changes
   `result` from `ACC` to `decodeAcc(ACC, CS)`, and leaves `ch` equal to its
   prior value for empty `CS` or the final one-character string otherwise.
   The module scope, standard builtins, locations, empty heap, stack frame,
   return state, exception, and exit code are pinned.

2. **`decode-shift`** (`spec.k:44`): from the ordinary module environment
   containing the submitted `decode_shift` closure and standard builtins,
   calling it on any lowercase code sequence returns exactly
   `str(decodeCodes(CS))`, with the ordinary empty caller stack/heap and no
   exception.

3. **`char-inverse`** (`spec.k:61`): for every lowercase code
   `97 <= C <= 122`, applying the candidate's mathematical encoder character
   transform and then decoder transform returns `C`.

Each precondition is satisfiable. `evidence/stage4/formal_witnesses.py`
exhibits entry inputs `""`, `"a"`, `"f"`, `"z"`, `"mjqqt"`, and the wrapped
alphabet, a loop state with `ACC="q"` and `CS="az"`, and character witnesses
97, 102, and 122. All formal results equal both Python implementations
(`evidence/stage4/formal-witnesses.log`).

### Mechanical program pinning

The top claim does not load the whole submitted module, but it pins the target
binding to `decodeClosure`. This is adequate here because:

- trusted regeneration gives byte identity with `solution.mpy`;
- `evidence/stage4/pinning_check.py` extracts the `decode_shift` parameter
  and body constructors from that regenerated module;
- K's own parser expands both the extracted expected closure and
  `decodeClosure`;
- the two expanded KORE terms are byte-identical, 4,519 bytes, with SHA-256
  `0ec266909a1a5e65ccd5d168e7e1f9c9460974ee29012b4bcc4c431f323ce92e`.

The source term, expanded terms, and log are preserved under
`evidence/stage4/`.

The loop helper also matches the actual `For(Name("ch"), Name("s"),
decodeStep)` control flow. The postcondition contains
`decodeCodes(CS)` rather than a free result variable or one-way implication.

### Body sensitivity

I changed the actual executed `decodeStep` constructor from subtracting 5 to
subtracting 4, rebuilt a fresh base definition, and reran the loop connection
claim. The mutation compiles, but the claim exits 1 with
`WarnStuckClaimState`; its residual compares the correct `C - 5` summary
(`C + -102`) with the mutated `C - 4` execution (`C + -101`).

The mutant sources and logs are
`evidence/stage4/verification-body-mutant.k`,
`spec-body-mutant.k`, `body-mutant-kompile-base.log`, and
`body-mutant-loop-proof.log`. This is a genuine program-term mutation, not a
change to an unused external source file.

Adequacy and pinning therefore pass. They do not cure the unsound promotion
rule below.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/stage5/rule_inventory.py` consumed every line of:

- `reference-semantics/semantics.k`;
- all 23 supplied helper `.k` files;
- `verification.k`;
- `spec.k`.

`evidence/stage5/rule-inventory.log` preserves the complete multiline block
for every declaration and rule with source line, exact source hash, and
attributes. It inventories:

- 708 rules;
- 235 syntax declarations;
- 5 contexts;
- 1 configuration;
- 3 claims;
- 116 `total` declarations;
- 25 opaque `symbol` declarations;
- all ordinary, `owise`, concrete, macro, strictness, and priority entries.

There are no `functional` or `simplification` declarations in the audited
sources. `evidence/stage5/attributes-and-priorities.txt` is a focused index of
all totality, opacity, and priority sites. The per-source and
candidate-rule assessment is in
`evidence/stage5/rule-assessment.md`.

`evidence/stage5/used_construct_map.py` also maps all 17 constructors in the
submitted `solution.mpy` to their syntax groups and semantic rules; no
constructor is undeclared.

### Fixed-semantics dependency review

The material target path uses module lookup and closure call, left-to-right
argument evaluation, parameter binding, the ASCII docstring expression,
ordinary assignment, string iteration, target binding, `AugAssign`, nested
integer binary operations, `ord`, `chr`, string concatenation, return, and
frame pop.

On `lowerCodes(CS)`:

- string iteration yields one-character strings in order;
- `ord` is exact on those strings;
- integer subtraction and `pyMod(_,26)` are ordinary unbounded-integer
  mathematics with nonzero divisor;
- the computed `chr` argument is always 97 through 122, inside the supplied
  semantics' ASCII rule;
- string `+` is exact sequence concatenation;
- call/return and the exact cells preserve evaluation order and control.

The used fixed-semantics rules have disjoint applicable cases or agreeing
overlaps and do not fabricate values. The supplied semantics is intentionally
partial outside this path. Its Unicode, exception, invalid-index, escaping
closure, import, float, sort, md5, and other unsupported/opaque behavior is
unreachable here. In particular, none of the 25 supplied opaque symbols occurs
in the target term, summary, branch, or postcondition.

The candidate-local total functions `decodeChar`, `decodeAcc`,
`decodeCodes`, `loopLast`, `encodeChar`, and `lowerCodes` are truthful,
constructor-complete, non-overlapping, and structurally descending where
recursive. The three macros are exact constructor aliases, as Stage 4 checks.

### Materially unsound operational bridge

The remaining candidate extension is
`verification.k:69-102`, rule `decode-loop-lemma`.

Its complete match context is:

- `#loop(str(CS), Name("ch"), decodeStep) ~> KONT`;
- environment 1;
- function scope 1 with `s`, `result`, and `ch`;
- module scope 0 with the exact `decodeClosure`;
- **arbitrary** `BUILTINS:Scope` at location -1;
- scope location 2, empty heap, heap location 0;
- exact caller frame, `noRet`, `NoExc`, and exit code 0;
- guard `lowerCodes(CS)`.

It removes the loop immediately, keeps `KONT`, and writes the mathematical
`decodeAcc` and `loopLast` summaries. It therefore replaces all loop
iteration, target binding, name lookup, `ord`/`chr` calls, arithmetic,
concatenation, and control execution.

The bridge-free connection theorem is the independently closed
`decode-loop` claim. That theorem covers arbitrary `KONT` and the other exact
cells, but it fixes location -1 to `builtinsScope`. It does **not** quantify
over arbitrary `BUILTINS:Scope`. The operational bridge's match domain is
strictly larger than its justification domain.

This is not merely a missing argument. A concrete false-conclusion witness is
preserved as `evidence/stage5/spec-bad-builtins.k`:

- `CS = [97]`, the intended-domain input `"a"`;
- `ACC = ""`, `CH = ""`, and the otherwise exact loop state;
- location -1 is `scope(.Map, root)`, so neither `chr` nor `ord` is bound.

Under the extended candidate theory, `kprove` exits 0 with `#Top`, asserting
that this loop returns `"v"` and final `ch = "a"`
(`evidence/stage5/bad-bridge-extended.log`).

Under the freshly built bridge-free definition, the same claim exits 1 with
`WarnStuckClaimState` at `#look("chr", -1)`
(`evidence/stage5/bad-bridge-base.log`). Fixed execution cannot produce the
asserted result. Thus the rule enables a demonstrably false execution
conclusion for an intended-domain string.

The rule has priority 40 and is the extension used to close the top-level
claim. Narrowing its final scope entry to `builtinsScope` would fit the
connection theorem, but the immutable candidate did not do so. Per the
benchmark boundary, an over-broad rule belongs in `CONCERNS` only when it
cannot prove a false conclusion. This one can, so it is a material soundness
failure.

## 6. Fresh non-vacuity test

I created a new mutation in `evidence/stage6/spec-vacuity.k`. It changes the
top-level result obligation to append code 97 (`"a"`) to every correct result:

```text
str(seqConcat(decodeCodes(CS), iCons(97, .IntSeq)))
```

The state is satisfiable; for `CS = .IntSeq`, it falsely requires `"" = "a"`.

First, `kprove --dry-run` exits 0 and emits the backend command, proving that
the mutation parses and builds
(`evidence/stage6/01-vacuity-dry-run.log`). The actual proof exits 1 with
`WarnStuckClaimState`. Its residual is precisely:

```text
decodeAcc(.IntSeq, CS)
  = seqConcat(decodeAcc(.IntSeq, CS), iCons(97, .IntSeq))
```

See `evidence/stage6/02-vacuity-proof.log`. This is the expected unmet result
obligation, not a parser error, timeout, or unrelated failure. The original
entry claim is discriminating and non-vacuous.

## 7. Proven-versus-assumed accounting and decision

### What the successful runs establish

The bridge-free `decode-loop` proof establishes the exact loop summary for
lowercase sequences in the standard builtin environment. The bridge-free
`char-inverse` proof establishes the stated per-character inverse arithmetic.

The top-level `decode-shift` run establishes closure only in the **extended
submitted theory**, which assumes `decode-loop-lemma` over arbitrary builtin
scopes. Because that theory proves the false witness above, its `#Top` is not a
sound partial-correctness proof of the real generated program.

### Trust ledger

- **K toolchain and logical hooks:** K 7.1.293, integer/Boolean/string/map/list
  hooks, parsing, compilation, and proof backend are the ordinary low-level
  trust boundary.
- **Supplied MPY semantics:** fixed by the trusted mount. Its material
  lowercase-ASCII call/loop/string/integer fragment is exercised in the
  bridge-free connection claim and fresh concrete execution. Its documented
  unused partial-language limitations do not affect this theorem.
- **Translator bridge:** the trusted translator regenerates the submitted MPY
  byte-for-byte; KORE macro comparison pins the exact target closure. This is
  mechanical evidence, not an assumed source rewrite.
- **Mathematical summaries:** `decodeChar`, `decodeAcc`, `decodeCodes`,
  `loopLast`, `encodeChar`, and `lowerCodes` are defined by exhaustive
  equations. They introduce no opaque or fresh result-bearing values.
- **Supplied opaque primitives:** the 22 float symbols, two sort symbols, and
  one md5 symbol are imported but absent from every reachable target term and
  postcondition. No result depends on them.
- **Candidate loop bridge:** this is a program-derived, control- and
  result-bearing operational abstraction. Its bridge-free theorem is narrower
  than its rule. The false `"a"`/empty-builtins witness makes this boundary
  illegitimate.
- **Python differential evidence:** 18,563 finite cases support
  implementation/canonical agreement and the source-contract bridge. They
  cannot repair or replace the failed universal K soundness obligation.
- **Natural-language adequacy:** interpreting `lowerCodes` as encoder outputs
  and `decodeCodes` as shift-minus-five is ordinary arithmetic and matches the
  trusted canonical program. There is no material HumanEval domain
  restriction.

Gate B (intent/domain adequacy) and the non-vacuity evidence are satisfactory.
Gate A (real-program soundness) fails because a proof-local operational rule
can establish a false conclusion and contributes to top-level closure.
Therefore the benchmark's required mapping is `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
