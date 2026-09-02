# Independent adversarial audit: 101-words-string

## Executive decision

The candidate contains a legitimate, result-constraining partial-correctness proof of the submitted translated program on the task's stated domain: strings whose word separators are commas and literal spaces. I independently rebuilt both K definitions, ran each positive claim separately, checked the submitted `.mpy` against the trusted translator, compared the Python implementations on 26,208 inputs, exercised the rebuilt generated semantics on every local branch class, reviewed every local declaration and rule, and obtained the expected stuck obligation from a fresh false-result mutation.

The concern is a language-model scope gap, not a proof bypass. The formal universal claim has no domain predicate and ranges over every K `String`, but the generated rule for Python `str.split()` recognizes only the literal ASCII space. CPython and the trusted canonical implementation also split tabs, line breaks, carriage returns, and other Unicode whitespace. Concrete witnesses outside the prompt's comma/literal-space separator domain are recorded in [13-semantic-scope-probe.log](evidence/13-semantic-scope-probe.log). No false-rule witness was found on the intended domain, so this is not classified as an unsoundness or a `FAIL`.

## 1. Input and provenance integrity

The rendered mode and trusted mounts are consistent. `/reference/reference-semantics` does not exist, as required for `GENERATED_SEMANTICS`; therefore no hidden or inferred semantics baseline was used. The mode check and complete top-level candidate inventory are in [01-provenance.log](evidence/01-provenance.log).

Required candidate sources are present as ordinary files:

- `solution.py`, `solution.mpy`
- `semantic.k`, `verification.k`, `spec.k`
- `prove.sh`
- `prompt.py`, `py2mpy.py`
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`
- the structured JSONL generation trace

There are no symlinks anywhere under `/candidate`. No required source artifact is missing or mistyped. The candidate also contains an extra prebuilt `semantic-kompiled/` directory. It is untrusted generated output, not a source integrity failure, and it was neither copied nor used.

`/candidate/prompt.py` is byte-identical to `/reference/prompt.py`, with SHA-256 `96a270267ea64b34c5d4364f00c969284296ae45017b988c20a1c1c306dfc486`. `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`, with SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The run metadata, final report, generation log, and all 215 structured trace events were read only as untrusted claims. They claim a successful combined `kprove` run. The complete bounded trace extraction is in [02b-structured-trace-summary.log](evidence/02b-structured-trace-summary.log); no candidate-reported success was relied on.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

From `/reference/prompt.py`, the entry point accepts a string of words separated by commas or spaces and returns the words as a list. From `/reference/canonical.py`, empty input returns `[]`; commas are converted to literal spaces; runs and edge occurrences of separators contribute no empty words.

The candidate implementation is:

```python
def words_string(s):
    return s.replace(",", " ").split()
```

For the intended string domain this is the same algorithmic result as the canonical implementation: replace each comma with a literal space, then split into maximal non-separator words while discarding empty fields. It preserves the required signature and has no hidden imports, state, nondeterminism, or exceptional path for string inputs.

### Trusted translation identity

Only source artifacts were copied to `/tmp/audit-work/reconstruction`. The trusted `/reference/py2mpy.py` regenerated `solution.mpy`; `cmp` reported byte identity. Both submitted and regenerated files have SHA-256 `041a394199807703db4f10d119803ffbf9b1791d7ea1428ed5526a0a41bc81f0`. See [03-copy-and-translate.log](evidence/03-copy-and-translate.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports the trusted canonical function and the scratch candidate function. It also uses a separately written character scanner as a literal comma/space contract oracle. Its input scope includes:

- both documented examples;
- empty, singleton, only-separator, leading/trailing separator, repeated separator, comma/space mixture, no-separator, punctuation, digit, and Unicode-word cases;
- every string of length 0 through 7 over the alphabet `a`, `b`, comma, and literal space;
- 5,000 deterministic generated attempts using seed 101 and varied word/separator lengths.

After deduplication, all three implementations agreed on all 26,208 inputs, with zero mismatches. The exact command, summary, and exit 0 are in [04-differential-results.log](evidence/04-differential-results.log); every generated input is preserved in [differential-inputs.jsonl](evidence/differential-inputs.jsonl).

This is finite fidelity evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

The K toolchain was independently available as version v7.1.293. Candidate-provided definitions and caches were not copied. Separate definitions were built from the scratch source:

| Purpose | Exact build evidence | Result |
|---|---|---|
| Concrete LLVM semantics | [05-build-concrete.log](evidence/05-build-concrete.log) | exit 0 |
| Haskell proof semantics | [06-build-proof.log](evidence/06-build-proof.log) | exit 0 |

The rebuilt LLVM semantics was compared with both Python implementations on 18 concrete inputs covering every `splitSpaces` rule class: empty, nonempty without a space, leading space, first space after a word, repeated spaces, comma replacement, edge commas, both prompt examples, punctuation, and non-ASCII word characters. Every `krun` exited 0 and all 18 results agreed. Commands, inputs, decoded K results, and Python results are in [07b-concrete-comparison.log](evidence/07b-concrete-comparison.log) and [concrete-inputs.jsonl](evidence/concrete-inputs.jsonl).

The earlier [07-concrete-comparison.log](evidence/07-concrete-comparison.log) records a reviewer-harness failure to decode K's `\xHH` token notation. It occurred after successful K execution, was fixed by using Python string-literal decoding, and is superseded by the complete exit-0 rerun.

Every positive target claim was then selected and run independently against the fresh Haskell definition:

| Claim | Evidence | Exit/output |
|---|---|---|
| `SPEC.words-string-general` | [08-proof-general.log](evidence/08-proof-general.log) | exit 0, `#Top` |
| `SPEC.prompt-example-hi` | [09-proof-example-hi.log](evidence/09-proof-example-hi.log) | exit 0, `#Top` |
| `SPEC.prompt-example-numbers` | [10-proof-example-numbers.log](evidence/10-proof-example-numbers.log) | exit 0, `#Top` |

Thus clean proof reconstruction passes.

## 4. Adequacy and real-program pinning

### Plain-language claims

`words-string-general` has no explicit `requires`. Its implicit precondition is a K `String` `S`, the exact submitted program followed by `invoke("words_string", S)` in `<k>`, and an empty `<functions>` map. Its postcondition requires `<k>` to contain exactly `ListVal(wordsContract(S))` and requires `<functions>` to contain exactly the installed submitted function body.

`prompt-example-hi` and `prompt-example-numbers` have the same entry state with their respective ground strings. Each postcondition fixes the exact expected ground list and the exact installed function map.

There is no free result variable, existential result, implication-only postcondition, omitted result cell, or wildcard final function state. All three claims consume the program and invocation and constrain the returned `ListVal`.

### Real source program

The program term embedded in each claim is the submitted translated AST. The only surface difference is that `solution.mpy` represents the empty `Exprs` list as the translator's concrete `Call(..., )`, whereas a K claim names the same generated list unit as `.Exprs`. After normalizing only that list-unit spelling and parsing through the rebuilt syntax, all three claim terms have byte-identical KAST JSON to `solution.mpy`. See [11b-real-program-pinning-kast.log](evidence/11b-real-program-pinning-kast.log).

The earlier raw-text diagnostic [11-real-program-pinning.log](evidence/11-real-program-pinning.log) intentionally exposes the surface spelling mismatch (`cmp=1`); it is not a parsed-term mismatch.

### Satisfiability and concrete substitution

Every entry precondition is realizable. For example, `S = ""` with the exact module/invocation computation and empty functions map is a concrete initial configuration; fresh LLVM execution reaches `ListVal(.List)`. The two ground examples are also direct satisfying states.

For the additional satisfying input `S = "a,,b"`, the claimed result reduces by the local equations to `["a", "b"]`. Both `/reference/canonical.py` and the scratch `solution.py` return `["a", "b"]`; this substitution is recorded in [11-real-program-pinning.log](evidence/11-real-program-pinning.log), and the corresponding K execution appears in [07b-concrete-comparison.log](evidence/07b-concrete-comparison.log).

There are no loops or helper reachability claims. The real control path is module loading, function lookup/invocation, return-expression evaluation, nested `replace`, then `split`; all of those steps execute under ordinary semantic rules.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

There are exactly three local K source files: `semantic.k`, `verification.k`, and `spec.k`. The source and grep inventory is preserved in [12-static-rule-inventory.log](evidence/12-static-rule-inventory.log).

Local syntax declarations are:

| File/lines | Declaration | Role and decision |
|---|---|---|
| `semantic.k:7` | `Program ::= Module(Stmts)` | Exact translator root; sound for this program. |
| `semantic.k:9` | `Stmts ::= List{Stmt,""}` | Statement sequence; the submitted body/module each use one statement. |
| `semantic.k:10-11` | `Stmt ::= FuncDef(...) \| Return(...)` | Exactly the used statement constructs. |
| `semantic.k:13-15` | `Ids`, `Params`, `Exprs` list syntax | Exactly represents one parameter and two/zero call arguments. |
| `semantic.k:16-19` | `Expr ::= Name \| Str \| Attribute \| Call` | Exactly the four expression forms in `solution.mpy`. |
| `semantic.k:27` | `Function ::= function(String,Stmts)` | Stored capture-free one-parameter function. |
| `semantic.k:28` | `PyVal ::= StrVal(String) \| ListVal(List)` | Complete value kinds needed by this program. |
| `semantic.k:30-31` | `KItem ::= invoke \| execute` | Internal function-entry and statement-execution controls. |
| `semantic.k:33` | `eval(Expr,Map) [function]` | Partial evaluator; all actually used forms are covered. No `[total]` claim. |
| `semantic.k:34` | `asString(PyVal) [function]` | Partial projection; used only on `StrVal`. No `[total]` claim. |
| `verification.k:9` | `splitSpaces(String) [function]` | Recursive literal-space splitter; equations audited below. |
| `verification.k:26` | `wordsContract(String) [function,total]` | One unguarded equation covers every K `String`, so totality is justified. |

The configuration has only `<k>` and `<functions>` cells. That is sufficient: the used string operations are pure; the program has no heap, I/O, exception handling, mutation, closure, loop, or allocation behavior.

There are no local `[functional]`, `[simplification]`, `[concrete]`, priority/`priorities`, or opaque declarations or rules. Comments containing English words such as “concrete” and “functional-correctness” are not attributes.

### Complete local rule inventory

| Rule | Classification | Static decision |
|---|---|---|
| `semantic.k:41-42`, module load | Ordinary semantic rule | Matches the exact singleton module, removes it from `<k>`, and installs the same name, parameter, and body into an initially empty map. Continuation is preserved. Sound for the submitted module. |
| `semantic.k:45-46`, invoke | Ordinary semantic rule | Selects the actual map binding, passes the input string as the sole local `StrVal`, and preserves the continuation. There is no name-only shortcut or fabricated result. |
| `semantic.k:48`, execute return | Ordinary semantic rule | Replaces the sole `Return(E)` body with `eval(E,ENV)` and preserves the continuation. Sound because this body has no following statements or cleanup effects. |
| `semantic.k:50`, name lookup | Function equation | The actual local environment is the singleton `s |-> StrVal(S)`, exactly the equation's domain. It returns the bound value. |
| `semantic.k:51`, string literal | Function equation | A source `Str(S)` denotes `StrVal(S)` independently of the environment. |
| `semantic.k:54-55`, `replace` call | Function equation / semantic primitive bridge | Recursively evaluates the pure receiver and applies K's standard `replaceAll` to the two literal string arguments. For the actual nonempty old value `","`, this matches Python's no-count `str.replace`. Argument evaluation cannot expose a missed state/control effect because both arguments are literals. |
| `semantic.k:58-59`, no-argument `split` | Function equation / semantic primitive bridge | Recursively evaluates the pure receiver and returns `ListVal(splitSpaces(...))`. This is sound for comma/literal-space task inputs after replacement. It has the documented other-whitespace scope limitation below. |
| `semantic.k:61`, `asString` | Function equation | Exact projection from `StrVal`; every use receives that constructor. |
| `verification.k:11`, empty split | Definitional equation | Empty input has no words, so returns `.List`. |
| `verification.k:12-14`, leading space | Definitional recursive equation | For nonempty strings whose first character is a literal space, discards exactly that separator. The recursive string is one character shorter. |
| `verification.k:15-17`, no space | Definitional equation | A nonempty string with no literal space is exactly one word. |
| `verification.k:18-22`, interior space | Definitional recursive equation | When the first literal space occurs after index zero, emits the nonempty prefix and recurses strictly after the separator. |
| `verification.k:27`, `wordsContract` | Definitional summary | Replaces commas with literal spaces, then invokes the audited splitter. It names the mathematical contract and does not rewrite or bypass the program computation. |

For every ground K `String`, the four `splitSpaces` guards are disjoint and exhaustive: empty; nonempty with first space at index 0; nonempty with no space; or nonempty with first space at a positive index. Recursive rules strictly shorten the string. Their right-hand sides agree with literal-space tokenization, and there are no overlapping inconsistent equations.

All translated constructs map to both a syntax declaration and a behavior rule: `Module`, `FuncDef`, `Params`, `Return`, nested `Call`, `Attribute`, `Name`, `Str`, and the empty `Exprs` list. Function state is created once and read by exact key. Nested evaluation is inside K functions rather than small-step syntax, but all nested expressions are pure and non-throwing on the declared string domain, so evaluation order and omitted intermediate cells cannot alter an observable result.

### Scope witness and narrower evidence gap

The generated semantics comments describe Python `str.split()` generally, but `splitSpaces` recognizes only `" "`. The concrete witness `S = "a\tb"` yields `["a\tb"]` in K while both actual Python implementations yield `["a", "b"]`. Newline, carriage-return, and non-breaking-space probes also diverge. Exact commands and results are in [13-semantic-scope-probe.log](evidence/13-semantic-scope-probe.log).

Those witnesses do not satisfy the prompt's stated comma-or-space separator condition if “space” is read as the literal separator demonstrated by the examples. Consequently I do not label the rule unsound on the intended domain. The missing formal predicate and the broader behavior of CPython/canonical `split()` remain an adequacy concern. A stronger artifact would either model all Python whitespace or explicitly restrict the universal claim to the literal comma/space alphabet.

No task-answer oracle, unconstrained result symbol, false simplification, operational shortcut, hidden priority, or proof-local result fabrication was found.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`, so none was trusted. I created [spec-vacuity.k](evidence/spec-vacuity.k) in scratch. It leaves the exact entry program and state unchanged but changes the result-bearing obligation to:

```k
ListVal(ListItem("__AUDIT_FALSE__") wordsContract(S))
```

This is demonstrably false for the satisfying input `S = ""`, where both Python functions and fresh K execution return `[]`.

The mutation first passed `kprove --dry-run` with exit 0, proving that it parsed and built against the fresh definition; see [14-vacuity-build-dry-run.log](evidence/14-vacuity-build-dry-run.log). The real proof then exited 1 with `WarnStuckClaimState`. Its residual explicitly contains the unmet disequality between `splitSpaces(...)` and `ListItem("__AUDIT_FALSE__") splitSpaces(...)`, followed by the prover's “cannot be rewritten further” error. See [15-vacuity-proof-failure.log](evidence/15-vacuity-proof-failure.log).

This is a reachable result-obligation failure, not a parser error, missing import, timeout, or unrelated crash. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the submitted generated semantics, for every K `String` `S`, execution from:

1. the exact translated `solution.mpy` program,
2. the scheduled invocation `words_string(S)`, and
3. an empty function map

reaches:

```text
ListVal(splitSpaces(replaceAll(S, ",", " ")))
```

with the exact submitted function installed in the function map. It separately establishes the two prompt examples as ground reachability claims. The result is fixed, body-sensitive through the inlined AST and ordinary execution rules, and discriminates against a false added-word postcondition.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 compiler, LLVM runtime, Haskell backend, and prover | Parsing, execution, and proof closure | Standard unavoidable toolchain trust; rebuilt from source inputs and cross-checked across backends. |
| K built-ins `replaceAll`, `lengthString`, `substrString`, `findString`, integer comparisons, lists, and maps | All computed words and recursive control | Fixed external language primitives, not task-specific or opaque candidate symbols. Accepted low-level boundary; intended cases are supported by concrete and differential evidence. |
| Trusted `/reference/py2mpy.py` | Source-to-`.mpy` bridge | Designated trusted input. Byte identity pins its output; its general correctness is outside the K theorem. |
| Generated syntax and ordinary interpreter rules | Source-language execution | Audited rule by rule above. No rule skips the submitted body or supplies its final result. |
| `splitSpaces` equations | Result-bearing model of no-argument `split()` | Fully defined and mathematically sound for literal-space tokenization. The equality to complete CPython whitespace behavior is not proved and is false outside that scope. |
| `wordsContract` equation | Human-contract meaning of the final list | Transparent definition, not an oracle. Its alignment with the English phrase “commas or spaces” is an informal intent bridge supported by the canonical implementation and finite tests. |
| Differential and concrete tests | Python/canonical/semantics fidelity on sampled inputs | Reproducible finite evidence only; not substituted for `kprove` or a universal connection theorem. |

The proof does not establish correctness for non-string inputs, Python exception behavior, arbitrary methods/AST constructs, or exact CPython `split()` behavior on whitespace other than the literal space. Partial correctness and the local generated language subset are the intended theorem boundary.

### Gate summary

- Real-program soundness: pass on the intended comma/literal-space separator domain. The exact body executes; no result-bearing oracle or bridge bypass exists; the false mutation fails meaningfully.
- Intent adequacy: legitimate but limited. The literal delimiter contract is covered, while the formal universal string claim omits the domain restriction and the generated `split()` model is narrower than CPython.
- Trust/evidence auditability: pass. Source, commands, statuses, inputs, outputs, mutation, and reviewer scripts are preserved under `evidence/`.

The scope limitation warrants `CONCERNS`, but it does not invalidate the requested partial-correctness theorem on the intended domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
