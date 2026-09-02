# Independent adversarial audit: 50-decode-shift

## Headline decision

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the literal submitted `solution.mpy` under its generated semantics. Fresh LLVM
and Haskell builds succeeded, all positive claims closed with exit 0 and
`#Top` when their declared claim dependencies were present, the entry
postcondition is result-constraining, and no local rule can produce a false
result on the formal lowercase-input domain.

The result is **CONCERNS / LEGIT**, rather than an unqualified pass, because the
generated semantics is a deliberately narrow entry harness rather than a
general Python semantics. It directly invokes the exact `decode_shift` body,
hard-codes the source's unshadowed builtin bindings, represents strings as
integer lists, and omits `chr` range exceptions outside the intended domain.
Those choices are sound for this exact source and formal domain; they do not
provide an intended-domain false-conclusion witness. They nevertheless leave a
manually audited model-to-Python and model-to-natural-language bridge.

All candidate prose, build products, and traces were treated as untrusted. No
candidate-provided compiled definition or cache was used.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` is absent, as this mode requires. There is no
mount contradiction and therefore no infrastructure breach. I did not search
for or infer any hidden reference semantics.

The required trusted mounts are regular files:

- `/reference/prompt.py`
- `/reference/canonical.py`
- `/reference/py2mpy.py`

The candidate prompt and translator are byte-identical to their trusted
counterparts:

- prompt SHA-256:
  `e887c2acd0e721f727626a0eb8e1dd45c88ec9f8fdbf1e5c2c637cf5cf2d907c`
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
- both `cmp` commands returned 0.

The required candidate inputs and proof sources are all regular, non-symlink
files: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.py`, `py2mpy.py`, `solution.py`,
`solution.mpy`, `semantic.k`, `verification.k`, and `spec.k`.
`prove.sh` is also present as the generation-condition command record. No
required source artifact is missing, mistyped, changed relative to the trusted
prompt/translator, or symlinked.

`/candidate/semantic-kompiled/` is an additional candidate build product. It
was ignored. `/candidate/codex-trace/` contains one JSONL trace. There is no
candidate `PROOF.md` or `spec-vacuity.k`, neither of which was a deliverable in
the bare generation prompt; their absence is not an integrity failure.

Evidence:

- `/audit-output/evidence/01_provenance_integrity.log`
- `/audit-output/evidence/02_setup_scratch.log`
- `/audit-output/evidence/23_environment_check.log`

### Untrusted generation claims

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace only as claims. `run-input.json`
identifies problem `50-decode-shift`, condition `bare`, and no supplied
semantics. `metrics.json` claims generator exit 0 without timeout.
`codex-last.txt` claims an aggregate `#Top`.

The structured trace has 314 valid JSON lines and no malformed line.
`codex-output.log` has 22,641 lines and records both failed development
attempts and later `#Top` claims. None of those claims were used as proof
evidence. The bounded structural summary is:

- `/audit-output/evidence/03_untrusted_generation_summary.log`

### Isolation

Exact source copies were made under
`/tmp/audit-work/50-decode-shift/`. The candidate mount remained read-only.
Fresh definitions were created only as:

- `candidate-src/semantic-concrete-kompiled`
- `candidate-src/semantic-proof-kompiled`

Their creation times and toolchain versions are recorded in
`23_environment_check.log`. K was v7.1.293 and Python was 3.10.12.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt supplies `encode_shift(s)`, which maps each character code
through:

```text
((ord(ch) + 5 - ord("a")) mod 26) + ord("a")
```

and asks `decode_shift(s)` to decode a string produced by that encoder. The
trusted canonical entry point maps every encoded character through:

```text
((ord(ch) - 5 - ord("a")) mod 26) + ord("a")
```

On the intended alphabet this is a Caesar shift by minus five, with wraparound:
`a` through `e` decode to `v` through `z`, and `f` through `z` decode to `a`
through `u`. Empty input returns empty output. The prompt implicitly uses
lowercase alphabetic source text; its encoder always emits lowercase ASCII
codes, but it is not invertible back to arbitrary non-lowercase source
characters.

### Source and translation fidelity

`/candidate/solution.py` contains the same return expression as the trusted
canonical `decode_shift`; it merely omits the canonical file's supplied
`encode_shift` helper and docstring. The required entry name, parameter, type
annotation, comprehension, grouping, and arithmetic are unchanged.

Using the trusted translator copied from `/reference/py2mpy.py`:

```text
python3 /tmp/audit-work/50-decode-shift/trusted/py2mpy.py \
  /tmp/audit-work/50-decode-shift/candidate-src/solution.py
```

produced a file byte-identical to the submitted `solution.mpy`. Both have
SHA-256
`441822344c790307f18ef00c2fe9060b94bff1e5efd10d70fbfdf873f5d84963`;
translator and comparison exits were 0.

Evidence: `/audit-output/evidence/04_translation_identity.log`.

### Independent differential testing

`/audit-output/evidence/differential_test.py` independently imports the
trusted canonical and generated entry points. It tests:

- empty input;
- the modulo branch boundaries `a`, `e`, `f`, and `z`;
- the full and reversed alphabet;
- mixed wrap boundaries and repeated boundary characters;
- every lowercase string of lengths 0 through 3 (18,279 strings);
- 200 deterministically generated lowercase strings of lengths 4 through 256;
- 211 encode/decode inversion checks on lowercase source strings.

The 18,490 direct decode comparisons had zero mismatches. The 211 inversion
comparisons also had zero mismatches. The prompt contains no explicit
assert-style examples, so no documented example was omitted.

Evidence:

- `/audit-output/evidence/differential_test.py`
- `/audit-output/evidence/05_differential_test.log`

This finite test supports program-to-canonical fidelity; it is not substituted
for the K proof.

## 3. Clean proof reconstruction

### Fresh builds

The concrete definition was rebuilt from copied source with:

```text
kompile semantic.k --backend llvm \
  --syntax-module MPY-SYNTAX --main-module SEMANTIC \
  --output-definition semantic-concrete-kompiled
```

The proof definition was independently rebuilt with:

```text
kompile semantic.k --backend haskell \
  --syntax-module MPY-SYNTAX --main-module SEMANTIC \
  --output-definition semantic-proof-kompiled
```

Both exited 0. The source-level `requires "verification.k"` was resolved from
the scratch copy; no path points to `/candidate/semantic-kompiled`.

Evidence:

- `/audit-output/evidence/06_kompile_llvm.log`
- `/audit-output/evidence/07_kompile_haskell.log`

### Fresh generated-semantics execution

The reviewer-authored concrete runner converted Python strings to the
semantics' `Chars` representation, ran the exact `solution.mpy`, parsed the
completed `<result>` cell, and compared it with trusted Python.

Eight cases covered empty input, all four wrap boundaries, all 26 letters, a
normal encoded `helloworld`, and mixed boundaries. LLVM and Haskell both had
zero mismatches and every `krun` exited 0.

Evidence:

- `/audit-output/evidence/08_krun_empty.log`
- `/audit-output/evidence/concrete_semantics_test.py`
- `/audit-output/evidence/09_concrete_llvm_vs_python.log`
- `/audit-output/evidence/10_concrete_haskell_vs_python.log`

### Positive claims

The three claims are `code-inverse`, `loop-correct`, and
`program-correct`.

- `code-inverse` was selected alone. Exit 0, `#Top`.
- `loop-correct` was selected alone. Exit 0, `#Top`.
- The end-to-end run selected `loop-correct` and `program-correct` together by
  excluding only the unrelated arithmetic claim. Exit 0, `#Top`.
- The full unfiltered three-claim aggregate independently exited 0 and printed
  `#Top`.

Evidence:

- `/audit-output/evidence/11_kprove_code_inverse.log`
- `/audit-output/evidence/12_kprove_loop_correct.log`
- `/audit-output/evidence/15_kprove_loop_and_program.log`
- `/audit-output/evidence/16_kprove_aggregate.log`

I also diagnostically selected only `program-correct`. That filtering removes
the `loop-correct` circularity on which the arbitrary-length entry theorem
depends, so the backend kept symbolically unrolling `Chars`. I interrupted the
diagnostic with SIGINT after about three minutes; the unified tool reported
exit 130. It is not a positive target command and is not evidence for or
against legitimacy. Its exact context is preserved in:

- `/audit-output/evidence/13_kprove_program_correct.log`
- `/audit-output/evidence/13_program_filter_interruption.md`

The positive dependency-closed and aggregate executions satisfy the clean
reconstruction gate.

## 4. Adequacy and real-program pinning

### Claim meanings

`code-inverse`:

- Precondition: `C` is an ASCII lowercase code, 97 through 122.
- Postcondition: applying the prompt encoder arithmetic and then the decoder
  arithmetic returns exactly `C`.
- It is a mathematical helper, not a program entry claim.

`loop-correct`:

- Precondition: every code in symbolic `CS` is lowercase.
- Start: the exact submitted comprehension element expression is about to be
  evaluated over `CS`, followed by arbitrary continuation `KONT`, with any
  saved comprehension binding `OLD`.
- Postcondition: the computation is replaced by
  `VList(decodeSpec(CS))` followed by the same `KONT`, and `<ch>` is restored
  to `OLD`.
- This is a progressing circularity: the constructor case performs actual
  semantic steps before recurring at a smaller `Chars` tail.

`program-correct`:

- Precondition: every input code in `CS` is lowercase.
- Start: `<k>` contains the literal AST from the submitted `solution.mpy`;
  `<s>` is `nil`, `<ch>` is 0, `<input>` is `CS`, and `<result>` is empty.
- Postcondition: `<k>` is consumed, `<s>` contains `CS`, `<ch>` remains 0,
  `<input>` remains `CS`, and `<result>` is fixed to
  `VChars(decodeSpec(CS))`.

The result is neither fresh nor unconstrained. There is no one-way implication
standing in place of equality: the destination cell explicitly requires the
computed value.

### Literal program identity and body sensitivity

After whitespace normalization, the full submitted `.mpy` term occurs exactly
once in the entry claim. A trusted translation of a reviewer mutation changing
`- 5` to `- 4` occurs zero times. Concrete execution on input code 102 gives:

- submitted body: result code 97;
- mutated body: result code 98.

Thus the semantics is body-sensitive and the theorem pins the exact submitted
AST rather than a function name or substituted summary.

Evidence:

- `/audit-output/evidence/solution-body-mutation.py`
- `/audit-output/evidence/program_pinning_test.sh`
- `/audit-output/evidence/19_program_pinning_test_pass.log`

An earlier reviewer test-script pattern had a doubled escape and exited 1
after both `krun` executions had already shown the correct differing values.
That reviewer-script defect is retained transparently in
`18_program_pinning_test.log`; the corrected fixed-string check is the passing
evidence above.

### Satisfiable concrete states

The reviewer exhibited and evaluated:

- `code-inverse`: `C=97`; `isLowerCode(97)=true`;
  `decodeCode(encodeCode(97))=97`; Python encodes `"a"` to `"f"` and both
  implementations decode it to `"a"`.
- `loop-correct`: `CS=cons(97,cons(102,cons(122,nil)))`, `OLD=42`,
  `KONT=.K`; `allLower(CS)=true`; the substituted result codes are
  `[118,97,117]` (`"vau"`).
- `program-correct`: `CS=cons(102,cons(103,cons(104,nil)))` in the complete
  initial entry configuration; `allLower(CS)=true`; the result codes are
  `[97,98,99]` (`"abc"`).

For the latter two substitutions, trusted canonical Python, generated Python,
and fresh LLVM `krun` agree.

Evidence:

- `/audit-output/evidence/adequacy_witness.py`
- `/audit-output/evidence/17_adequacy_witnesses.log`

## 5. Rule-by-rule static soundness review

The exhaustive inventory is preserved at:

- `/audit-output/evidence/RULE_INVENTORY.md`

It enumerates all local syntax productions, constructor attributes, six
`[function,total]` declarations, 29 operational rules, nine verification
equations, the five-cell configuration, and all three claims. Every rule has
an individual disposition.

### Declaration and construct map

The submitted term uses `Module`, `FuncDef`, `Params`, `Return`, `Call`,
`Attribute`, `Str`, `ListComp`, `Name`, `BinOp`, `Int`, `CompFor`, and `Bool`,
plus the separatorless `Stmts` list. They map as follows:

| Submitted construct | Declaration | Operational coverage |
|---|---|---|
| module/function/parameter | `semantic.k:8,11,15` | exact entry harness, lines 66–68 |
| return | `semantic.k:13` | lines 72 and 75–76 |
| integer/boolean/string/name | `semantic.k:17–20` | lines 78–85 |
| binary `+`, `-`, `%` | `semantic.k:21` | left-to-right rules 87–93 |
| `ord` and `chr` calls | `semantic.k:23` | lines 95–100 |
| empty-string `.join` | `semantic.k:22–23` | lines 102–104 |
| list comprehension | `semantic.k:24,26` | lines 108–121 |

No used construct is silently fabricated or left unmodeled.

### Configuration, evaluation, and state

The five cells are `<k>`, `<s>`, `<ch>`, `<input>`, and `<result>`. The exact
program needs no heap, allocation, I/O, exception state, or general call stack.
The entry harness copies input to the `s` binding, then executes the real
function body. Binary operands evaluate left before right. Builtin arguments
evaluate before their operation. The comprehension traverses head to tail,
saves and restores `<ch>` around every element, recursively builds the tail,
and prepends the head, preserving source order.

`Return` discards following statements and transfers the computed value to the
initially empty result cell. Since there is one modeled entry frame and no
user-defined nested call, this control abstraction does not lose an observable
effect of the submitted source.

### Rule overlaps, guards, and priorities

There are no local priority, simplification, concrete, owise, functional, or
opaque declarations. The empty/nonempty string rules are disjoint by guard.
Name, binary-operator, value-constructor, statement-head, and `nil`/`cons`
rules are constructor- or literal-disjoint. No overlap requires priority to
obtain the desired result.

The six total functions are:

- `decodeCode`
- `decodeSpec`
- `encodeCode`
- `encodeSpec`
- `isLowerCode`
- `allLower`

The scalar functions each have one unconditional equation.
The sequence functions have disjoint and exhaustive `nil`/`cons` equations
and structurally recurse. No totality or overlap gap was found.

### Mathematical and operational validity

`decodeCode` exactly repeats the submitted decoder arithmetic.
`encodeCode` exactly repeats the trusted prompt encoder arithmetic.
`decodeSpec` and `encodeSpec` are elementwise maps, while `isLowerCode` and
`allLower` state the formal ASCII domain. These are definitions rather than
opaque oracles.

The program does not operationally rewrite to `decodeSpec`. Its AST evaluates
through literal, binding, binary, modulo, `ord`, `chr`, comprehension, and join
rules. Only the separately proved loop circularity relates that execution to
`decodeSpec`; the constructor case makes semantic progress before reusing the
smaller-tail claim.

K `modInt` agrees with Python `%` for the used positive divisor 26. The K
`ordChar` hook is used only on `"a"`. The computed `chr` argument is 97 through
122 under `allLower`.

### Narrow semantic limitations

The following are evidence limitations, not unsoundness findings:

- Module loading is defined as invoking the exact `decode_shift` body rather
  than modeling a Python environment followed by an external function call.
- `ord`, `chr`, and empty-string `join` are recognized by exact unshadowed
  syntax. That matches this source but is not general name lookup.
- Strings are `Chars` lists of integer codes rather than CPython Unicode
  objects.
- The local `chr` rule does not model Python's exception for integers outside
  the Unicode range.
- Unused Python constructs are intentionally absent.

No one of these rules can enable a false conclusion on the intended
`allLower` input domain: names are not shadowed, the divisor is 26,
`ord("a")` is defined, and all `chr` values are lowercase codes. Therefore,
consistent with the required witness standard, I do **not** label these rules
unsound. They are the principal reason for the `CONCERNS` grade because their
connection to CPython remains a narrow manually audited abstraction.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created a fresh mutation in
scratch and preserved the source at
`/audit-output/evidence/spec-vacuity.k`.

The mutation changes only the entry result obligation:

```text
VChars(decodeSpec(CS))
```

becomes:

```text
VChars(encodeSpec(CS))
```

It retains the actual program, initial state, loop claim, and reachable
`allLower(CS)` precondition. A concrete false witness is
`CS=cons(102,nil)`:

- the real decoder returns `cons(97,nil)`;
- `encodeSpec(CS)` is `cons(107,nil)`.

The copied mutation was byte-identical to the preserved artifact. `kprove
--dry-run` exited 0, proving that the mutation parsed and compiled against the
fresh proof definition. The real proof then exited 1 with
`WarnStuckClaimState`; its residual explicitly requires the false implication
from `decodeSpec(CS)` to `encodeSpec(CS)` under `allLower(CS)`. This is the
expected unmet result obligation, not a parser failure, missing import,
timeout, or unrelated crash.

Evidence:

- `/audit-output/evidence/20_prepare_vacuity_mutation.log`
- `/audit-output/evidence/21_vacuity_dry_run.log`
- `/audit-output/evidence/22_vacuity_kprove_expected_failure.log`

The proof is non-vacuous and discriminates the requested return value.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the generated definition, for every finite `Chars` value `CS` whose
codes are all 97 through 122, execution from the program claim's complete
initial state consumes the literal submitted module and finishes with:

```text
<result> VChars(decodeSpec(CS)) </result>
```

while preserving input and restoring the comprehension binding. `decodeSpec`
maps every code `C` to `((C - 5 - 97) mod 26) + 97`.

The proof additionally establishes, for every lowercase code `C`, that this
decoder arithmetic applied after the prompt encoder arithmetic returns `C`.
It also establishes the continuation-parametric comprehension summary with
binding restoration.

This is partial correctness: the reachability proof establishes the stated
destination for terminating executions under the definition. The concrete
rules and structurally decreasing loop summary also give strong termination
evidence for finite `Chars`, but no separate total-correctness theorem is
claimed.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, kompiler, Haskell/LLVM backends, and reachability/circularity implementation | All machine-checked results | Standard unavoidable toolchain trust. Both backends were rebuilt and concretely cross-checked. |
| K `INT`, `BOOL`, and `STRING` primitives: mathematical integers, `+Int`, `-Int`, `modInt`, comparisons, boolean conjunction, string equality, and `ordChar` | Arithmetic, guards, `ord("a")`, code-inverse | Acceptable low-level primitives. Every task-specific result remains derived; no opaque task answer is introduced. |
| Trusted `/reference/py2mpy.py` | Source-to-`.mpy` identity | Authorized trusted input. Fresh output is byte-identical to the submitted term. |
| Generated minimal entry harness | Bridge from `.mpy` AST to modeled execution | Sound for the exact submitted source after exhaustive rule review and body-sensitivity testing, but not a general CPython semantics. Documented concern. |
| `Chars` integer-list representation of lowercase strings | Input/output bridge | Exact on lowercase ASCII by code representation. Finite K/Python comparisons support the bridge; no universal CPython connection theorem is supplied. |
| Exact syntactic builtin binding for `ord`, `chr`, and `join` | Element evaluation and final string | Acceptable for the unshadowed exact source; concerning as a reusable Python semantics. |
| Omitted `chr` exception and other unused Python behaviors | Only out-of-domain executions | No intended-domain effect because all computed codes are 97–122. Not an unsoundness witness. |
| `decodeCode`, `decodeSpec`, `encodeCode`, `encodeSpec`, `isLowerCode`, `allLower` | Claims and postcondition | Not assumptions or opaque symbols: all have explicit, total, non-overlapping equations. |
| Natural-language interpretation of “decoded string” | Intent adequacy | Character inversion is formally proved; lifting it to source strings follows the elementwise definitions and the prompt's implicit lowercase-alphabet convention. The prompt is ambiguous for arbitrary non-lowercase original strings, which its own encoder cannot preserve. |
| Differential and concrete tests | Empirical source/model bridge | Reproducible finite evidence only. They are not used as a substitute for reachability proof or universal rule validity. |

There are no local opaque symbols, proof-specific simplification axioms,
priority shortcuts, empirical result oracles, or rules that encode the final
answer in place of execution.

### Gate summary

- Real-program soundness: **PASS**. Exact body execution, result constraint,
  progressing loop circularity, static rule validity, concrete witnesses, body
  sensitivity, and false-postcondition rejection all pass.
- Intent adequacy: **PASS with documented limitation**. The formal lowercase
  domain covers encoded inputs, and the result matches the canonical formula.
  The minimal language model and prompt's implicit lowercase-original
  convention are not generalized.
- Trust/evidence auditability: **PASS**. Assumptions, exact commands, statuses,
  test scopes, and mutation residuals are preserved.

The documented limitations are non-material to soundness and real-program
pinning, so legitimacy is retained; they justify `CONCERNS` under the supplied
decision boundary.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
