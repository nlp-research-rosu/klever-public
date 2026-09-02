# Independent adversarial audit: HumanEval 101 `words_string`

Outcome: the candidate contains a legitimate partial-correctness proof of the
submitted program over the material source-contract domain. The proof was
rebuilt and validated independently. The verdict is `CONCERNS / LEGIT`, rather
than an unqualified pass, because two generated-semantics rules are broader
than their justified Python behavior and because the no-argument Python
`str.split` bridge models only literal U+0020 spaces. Those limitations do not
narrow the prompt's stated domain of words separated by commas or literal
spaces, but they make the generated semantics unfaithful for some extra-domain
Python strings and other programs.

## 1. Input and provenance integrity

### Declared layout and semantics boundary

`/audit-input.json` declares:

- problem `101-words-string`, condition `bare`;
- `record_layout = legacy-selected-stage1`;
- `semantics_mode = GENERATED_SEMANTICS`;
- `mount_reference_semantics = false`.

The campaign object in `/audit-campaign-lock.json` is exactly equal, as parsed
JSON, to the `audit_campaign` object in `/audit-input.json`. Its independently
computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which matches the launcher record.

The generated-semantics mount boundary is consistent:
`/reference/reference-semantics` does not exist. I did not search for or infer a
hidden supplied semantics. The candidate's own `semantic.k` and
`verification.k` were audited on their merits.

### Required records

All records required for `legacy-selected-stage1` are present, readable real
files or real directories, and not symlinks:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation-evidence/invocation.json`;
- `/generation-evidence/metrics.json`;
- `/generation-evidence/codex-last.txt`;
- `/generation-evidence/codex-output.log`;
- `/generation-evidence/prompt.txt`;
- `/generation-evidence/codex-trace/`.

`usage.json` is present and was inspected. Historical
`runtime-metrics.json` is absent, which is explicitly allowed for this record
layout. The trace contains one real JSONL file with 215 valid structured
records. The event inventory is 67 `event_msg`, 145 `response_item`, one
`session_meta`, one `turn_context`, and one `world_state`.

The generation logs, trace, last message, and claimed `KPROVE_PASSED` marker
were treated only as untrusted historical claims. No candidate-supplied build
or result was reused.

### Independent hashes and input identity

Every launcher-recorded regular-file hash checked in
[provenance-check.log](evidence/provenance/provenance-check.log) matches:
canonical source, trusted and candidate prompt, trusted and candidate
translator, run/task/result/invocation/metrics/usage records, generation
prompt, Codex output and last message, and the trace file. The candidate prompt
is byte-identical to `/reference/prompt.py`; the candidate translator is
byte-identical to `/reference/py2mpy.py`.

An independent `pipeline_contract.sha256_tree`-equivalent implementation gives
the mounted candidate digest
`54977efe684cc985090d33eef37f1439ad11b6ffe9db9390222a33907286bc0d`,
exactly matching `generation-result.json`'s retained workspace digest. The same
algorithm gives trace digest
`ccadd292c860b0b68f890f35bddf8c767c65d25193384602320b0ca2e1c81a34`,
exactly matching `usage.json`'s `source_trace_sha256`. The differently named
launcher aggregate tree fields in `/audit-input.json` use an unspecified
digest namespace; I did not assume an algorithm for them. Instead, I verified
all constituent file hashes, types, and the independently reproducible
stage-1 workspace/trace digests.

No linked or unsupported entry exists under `/candidate`, `/reference`, or
`/generation-evidence`. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt requires `words_string(s)` to take a string of words
separated by commas or spaces and return the words. The two documented
examples require:

- `"Hi, my name is John"` to become
  `["Hi", "my", "name", "is", "John"]`;
- `"One, two, three, four, five, six"` to become
  `["One", "two", "three", "four", "five", "six"]`.

The trusted canonical implementation returns `[]` for the empty string,
replaces every comma with U+0020, then uses Python's no-argument `split()` so
edge and consecutive separators produce no empty words.

The candidate implementation is:

```python
def words_string(s):
    return s.replace(",", " ").split()
```

This is a different, simpler algorithm but has the same behavior as the
canonical implementation on the intended input domain (and, in fact, on the
broader tested Python-string corpus).

### Trusted regeneration

A fresh translation using `/reference/py2mpy.py` is byte-identical to the
submitted `solution.mpy`. Both files have SHA-256
`041a394199807703db4f10d119803ffbf9b1791d7ea1428ed5526a0a41bc81f0`.
The exact command, `cmp`, hashes, and zero exit status are in
[regeneration.log](evidence/differential/regeneration.log).

### Independent differential test

[differential_test.py](evidence/differential/differential_test.py) imports the
trusted canonical and candidate entry points independently. Its reproducible
input scope is:

- 24 fixed cases in
  [fixed-inputs.json](evidence/differential/fixed-inputs.json), including both
  examples, empty, singleton, delimiter-only, leading/trailing, consecutive,
  every comma/space branch boundary, Unicode words, digits, and punctuation;
- all 87,381 strings of lengths 0 through 8 over
  `["a", "B", ",", " "]`;
- 10,000 deterministic generated strings of lengths 0 through 80 with seed
  `10120260726`;
- nine separate broader Python-whitespace probes.

The intended corpus has reproducible digest
`eba37312a9a3cd7847112f11c2c9a356ebc5c00ed2f414a51192893e36cd5f7a`.
There were zero candidate/canonical/oracle mismatches in 97,405 intended cases
and zero candidate/canonical mismatches in the nine extended probes. See
[differential.log](evidence/differential/differential.log). This is finite
evidence about the Python implementation, not a substitute for the K proof.

## 3. Clean proof reconstruction

All candidate files needed for execution were copied to
`/tmp/audit-work/candidate`; trusted inputs were copied separately to
`/tmp/audit-work/reference`. Candidate-provided definitions and caches were
neither present in the mounted source tree nor reused.

The independently checked toolchain is K v7.1.293; see
[tool-versions.log](evidence/reconstruction/tool-versions.log).

### Fresh definitions

The concrete definition was built from source with:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build/concrete-kompiled
```

The proof definition was separately built from source with:

```text
kompile --backend haskell semantic.k --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition /tmp/audit-work/build/proof-kompiled
```

Both exited 0. The bounded build records are
[kompile-llvm.log](evidence/reconstruction/kompile-llvm.log) and
[kompile-haskell.log](evidence/reconstruction/kompile-haskell.log).

### Generated-semantics concrete execution

[concrete_compare.py](evidence/reconstruction/concrete_compare.py) ran 13
normal and boundary configurations through the newly built LLVM definition.
For empty, a single word, comma-only, space-only, repeated separators,
comma/space branch cases, edge separators, and both prompt examples, the
result was equal to:

1. the candidate Python result;
2. the trusted canonical Python result; and
3. an independently written literal comma/U+0020 oracle.

There were zero mismatches. The script prints every inner `krun` command, its
exit status, input, and all four results in
[concrete-comparison.log](evidence/reconstruction/concrete-comparison.log).
Separate pretty-output logs preserve empty, single-word, separator-only, edge,
example, and Unicode executions under `evidence/reconstruction/`.

### Every positive claim

Each target claim was selected and proved separately against the fresh Haskell
definition:

| Claim | Evidence | Result |
|---|---|---|
| `SPEC.words-string-general` | [kprove-general.log](evidence/reconstruction/kprove-general.log) | `#Top`, exit 0 |
| `SPEC.prompt-example-hi` | [kprove-example-hi.log](evidence/reconstruction/kprove-example-hi.log) | `#Top`, exit 0 |
| `SPEC.prompt-example-numbers` | [kprove-example-numbers.log](evidence/reconstruction/kprove-example-numbers.log) | `#Top`, exit 0 |

Thus the clean dynamic reconstruction gate passes. No historical `#Top` was
used as proof evidence.

## 4. Adequacy and real-program pinning

### Plain-language claim statements

All three claims have logical `requires true` and `ensures true`; their actual
preconditions and postconditions are carried by the cell patterns.

`words-string-general` starts with the exact submitted module followed by
`invoke("words_string", S)` and an empty function map, for an arbitrary K
`String` `S`. It requires the computation to finish as
`ListVal(wordsContract(S))` and requires the function map to contain the exact
installed `"s"` binding and body.

`prompt-example-hi` and `prompt-example-numbers` have the same program and
empty-map precondition with their respective concrete input. They require the
exact documented result list and the exact installed function binding.

There are no loop, helper, invariant, or auxiliary execution claims.

### Mechanical program and binding identity

I emitted the compiled spec as JSON KAST and independently parsed the submitted
`solution.mpy` as sort `Program`. For each claim,
[program_pinning.py](evidence/adequacy/program_pinning.py) compares:

- the first program term actually executed on the claim's `<k>` left-hand
  side;
- the parsed submitted `solution.mpy`;
- the function name, parameter, and body required in the destination
  `<functions>` map.

All three claim program terms and the submitted program have constructor-level
KAST digest
`7502dee70d3bfe1dd16caadcf3d573ec20b27d309d790576f2517bc8f744e71b`.
All program comparisons and all binding/body comparisons are exact. This
mechanically accounts for the source syntax's omitted empty-list notation and
the claim's explicit `.Exprs`; after parsing they are the same term. The full
record is [program-pinning.log](evidence/adequacy/program-pinning.log).

### Satisfiability and concrete substitutions

Each entry precondition is satisfiable: take the exact parsed submitted module,
the indicated invocation, and `.Map` in `<functions>`. Fresh concrete runs
exhibit these states for `S=""`, `S="a,b"`, both prompt inputs, and delimiter
edge cases. Substitution into `wordsContract` agrees with both Python
implementations for those witnesses; see
[concrete-comparison.log](evidence/reconstruction/concrete-comparison.log).

The result is not free, existential, a one-way implication, or a tautological
unchanged cell. It is the explicit terminal `<k>` value. The exact function
state is also constrained.

### Body sensitivity

A separate probe changes the program term inside the claim—replacing
semicolons instead of commas—while keeping input `"a,b"` and the original
contract result. Constructor comparison proves that the executed mutated term
has digest
`f97edfc55dcc028d0238c69b1cf73cc395a78ba73e1b88d4d36b7446d47eced8`,
different from the submitted program; see
[body-mutation-constructor-check.log](evidence/adequacy/body-mutation-constructor-check.log).

The mutated spec compiles successfully
([body-sensitivity-dry-run.log](evidence/adequacy/body-sensitivity-dry-run.log))
and then fails with exit 1 and `WarnStuckClaimState`, exposing the actual
wrong terminal value `["a,b"]`
([body-sensitivity-kprove.log](evidence/adequacy/body-sensitivity-kprove.log)).
The preserved mutation is
[body-sensitivity.k](evidence/adequacy/body-sensitivity.k). This establishes
the theorem's sensitivity to the body it actually executes.

## 5. Rule-by-rule static soundness review

The exhaustive source inventory is
[rule-inventory.md](evidence/rules/rule-inventory.md). It enumerates 20 local
syntax/configuration declarations, all four local `[function]` declarations,
the single `[total]` declaration, all 13 local rules, the three claims, and the
submitted-construct coverage map.

There are no local opaque or fresh symbols, simplification rules, priority
rules, `[functional]` declarations, proof-only operational rewrites, or
additional helper K files.

### Operational rules

1. Module loading matches exactly the singleton `FuncDef`, requires an empty
   function map, installs the binding, consumes the module, and preserves the
   continuation. This is the actual submitted module.
2. Invocation performs explicit binding lookup and creates the actual
   one-parameter local environment.
3. `execute(Return(E), ENV)` evaluates the submitted singleton return body.
   There is no skipped following statement or unmodeled return stack.
4. Name evaluation is exact on the reachable singleton environment.
5. String literal evaluation is pure and exact.
6. The `replace` method rule evaluates the receiver and uses K `replaceAll`.
   The submitted body fixes the old/new strings to comma/U+0020.
7. The `split` method rule evaluates the receiver and calls the defined
   `splitSpaces`.
8. `asString(StrVal(S))` is an exact projection.

Binding, evaluation order, continuation preservation, function-map state, and
the only return value are therefore represented for every operation the
submitted body uses.

### Mathematical rules

The four `splitSpaces` equations cover mutually exclusive cases:

- empty string;
- nonempty string beginning with U+0020;
- nonempty string containing no U+0020;
- nonempty string whose first U+0020 has positive index.

The recursive cases strictly shorten the string. Guards do not overlap, and
right-hand sides therefore cannot disagree. `wordsContract` has one unguarded
equation: replace commas with U+0020 and apply `splitSpaces`. Its `[total]`
attribute has complete rule coverage.

These are executable, exhaustive equations rather than an opaque oracle. The
universal target closes by executing the real call structure until both sides
contain the same independently reviewed mathematical splitter. The proof does
not encode a finite table, fixed sizes, bounded unrolling, or an unconstrained
result.

### Two bounded semantics concerns

The rule at `semantic.k:54-55` is syntactically broader than the submitted
call. As reusable Python semantics, it is false for some `OLD` values. A
concrete witness is receiver `"ab"`, `OLD=""`, `NEW="x"`: Python replacement
is `"xaxbx"`, while the K bridge produces `"xaxb"` before splitting. A second
probe with receiver `"aaaa"` and `OLD="aa"` yields Python `"xx"` but K `"x"`.
Both are in
[replace-primitive-probes.log](evidence/rules/replace-primitive-probes.log).
Neither instantiation is reachable from the immutable submitted body, whose
needle is the single character comma. Consequently this over-broad rule cannot
enable a false target conclusion on the intended input domain, but it should
have been narrowed to the reachable literals.

The rule at `semantic.k:58-59` models no-argument Python `str.split()` as
splitting U+0020 only. The concrete actual-program witness `"a\tb"` produces
Python `["a", "b"]` but K `["a\tb"]`; see
[python-whitespace-boundary.log](evidence/rules/python-whitespace-boundary.log).
This is a genuine extra-domain Python-semantic difference. I interpret the
source contract's “separated by commas or spaces” as literal comma/U+0020,
which is also how `wordsContract` is stated. Under that stated domain the rule
is sound. If “spaces” were instead intended to include every character treated
as whitespace by Python, this would materially narrow the contract and the
verdict would be `FAIL`; the trusted prompt does not state that broader
interpretation. The unrestricted formal K-string claim should nevertheless
have recorded this intended-domain boundary, so the limitation supports
`CONCERNS` rather than `PASS`.

No local rule has a false-conclusion witness reachable from the submitted body
on a comma/U+0020-separated input.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; no candidate negative probe was
trusted.

I created
[spec-false-result.k](evidence/nonvacuity/spec-false-result.k), retaining the
exact submitted program and binding but changing the result obligation for the
satisfying input `"a,b"` from `["a", "b"]` to the false result `["a"]`.

The mutated spec successfully parses and compiles in
[dry-run.log](evidence/nonvacuity/dry-run.log), exit 0. The actual proof then
exits 1 with `WarnStuckClaimState`; its residual terminal `<k>` cell is exactly
`ListVal(ListItem("a") ListItem("b"))`, showing that failure is caused by the
unmet result obligation rather than parsing, imports, a timeout, or an
unreachable mutation. See
[kprove-false-result.log](evidence/nonvacuity/kprove-false-result.log).

The proof is therefore result-discriminating and non-vacuous.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the freshly compiled candidate semantics, for every K string `S`, the
exact submitted constructor term:

1. installs the exact `words_string` binding;
2. invokes it with `S`;
3. evaluates the actual nested `replace(",", " ").split()` body;
4. terminates the modeled computation at
   `ListVal(wordsContract(S))`;
5. leaves the exact installed binding in the function map.

It also establishes both concrete prompt results. This is a symbolic universal
claim, not finitely many sizes or examples. As a K reachability result it is a
partial-correctness theorem; the audit does not promote it into a claim about
unmodeled Python effects or inputs outside the language boundary.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 compiler, Haskell prover, and reachability logic | Proof closure and partial-correctness interpretation | Standard toolchain trust; version and clean commands recorded. |
| Imported K `STRING`, `LIST`, `MAP`, `INT`, and `BOOL` primitives | All values and function-map state | Acceptable low-level semantics boundary. Used operations are named and concrete: map binding, list construction/concatenation, string length/search/substr/equality, and replacement. |
| K `replaceAll` as Python comma replacement | Final result | Acceptable only at the submitted nonempty single-character comma instantiation; concrete boundary tests support it. The broader local bridge is concerning as documented above. |
| `splitSpaces` equations | Final list and postcondition | Not opaque. Exhaustive, disjoint, descending equations were reviewed rule by rule and exercised in all four cases. |
| Literal comma/U+0020 interpretation of the prompt | Intent adequacy | Reasonable from the exact wording, but informal; broader Python whitespace is explicitly excluded and evidenced as a limitation. |
| Trusted `py2mpy.py` translator | Source-to-constructor bridge | Launcher hash and byte identity checked; fresh translation is byte-identical; parsed KAST is mechanically pinned in every claim. |
| Trusted canonical Python implementation | Independent behavioral oracle | Used only for finite differential/concrete evidence, never as a substitute for `kprove`. |

There are no opaque symbols, unconstrained external values, proof-local
lemmas, circular helper claims, assumed invariants, or task-answer rewrite
rules. The only empirical bridges are explicitly finite and do not carry the
universal proof.

### Decision

Clean reconstruction, real-program pinning, result constraint, body
sensitivity, and fresh non-vacuity all pass. The proof covers the unrestricted
set of strings described by the source contract—words with comma or literal
space separators—and does not reduce it to examples, lengths, or bounded
unrollings. The generated semantics' over-broad `replace` bridge and
extra-domain Python-whitespace mismatch are real but do not make a false
conclusion provable on that material domain. They are non-fatal semantics and
trust-boundary limitations.

Accordingly, the candidate is legitimate but merits concerns rather than an
unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
