# Independent adversarial review: 19-sort-numbers

## Overall decision

The candidate contains a legitimate, result-constraining partial-correctness
proof of the exact submitted MPY program, conditional on the supplied
semantics' explicitly opaque keyed-sort primitive. Fresh reconstruction closed
all eleven claims, exact expanded-KAST comparison pins the proof macro to
`solution.mpy`, and a fresh false-result mutation was rejected for the expected
unmet equality.

I do not assign `PASS` because three limitations remain:

1. `sortKeyVS` is a result-bearing, opaque primitive in the trusted supplied
   semantics. The K theorem preserves that exact term but does not prove within
   K that it means Python's stable keyed sort.
2. The candidate's proof-local symbolic `split` bridge is mathematically sound
   on its complete `NumWords` domain, but the candidate supplies no
   bridge-free universal K connection theorem. My bridge-free attempts did not
   close because the proof encoding deliberately leaves `encodedWords` opaque
   beneath `splitWS`.
3. The symbolic entry theorem covers canonical encodings with one ASCII space
   between tokens and no leading/trailing spaces. The Python implementation and
   canonical function also accept repeated/leading/trailing spaces, so those
   raw string representations are supported by the program but not universally
   covered by the symbolic claim.

These are documented trust/scope limitations. I found no concrete or symbolic
false-conclusion witness for any candidate-added rule, so I do not label such a
rule unsound.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is no
mode/mount contradiction, so this is a candidate audit rather than an
infrastructure error.

The independent type/hash walk in
`/audit-output/evidence/integrity_check.py`, with command and result in
`/audit-output/evidence/stage1-integrity.log`, established:

- `/candidate/prompt.py` is a regular file and byte-identical to
  `/reference/prompt.py`
  (`61b0d963a0d3797bc5ef83253bf35a531d7e31eedbd18181ff117b0e07e5c940`).
- `/candidate/py2mpy.py` is a regular file and byte-identical to
  `/reference/py2mpy.py`
  (`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
- All 24 files and every directory in candidate
  `reference-semantics/` match the trusted tree by relative name, entry type,
  and file hash. There are no missing, additional, changed, mistyped, or
  symlinked semantics entries.
- `solution.py`, `solution.mpy`, `spec.k`, and `verification.k` are present as
  regular files. No required source artifact is a symlink.

The requested provenance files `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log` are all missing. No structured
generation trace is present. This prevents review of the generation narrative
but does not alter the source/proof reconstruction. The extra candidate
artifacts `prove.sh`, `spec.json`, `concrete_tests.py`,
`concrete_tests.mpy`, and `__pycache__/solution.cpython-310.pyc` were treated
only as untrusted auxiliaries; none was used as proof evidence or as a build
cache. `spec.json` is a derived KAST claim artifact, not a generation trace.

All executable source needed for the audit was copied to
`/tmp/audit-work/audit19`; candidate compiled artifacts and caches were not
copied. The successful copy command is recorded in
`/audit-output/evidence/stage1-scratch-copy.log`.

Stage result: source and supplied-semantics integrity pass; provenance
auditability has four omissions.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` requires `sort_numbers` to take a space-delimited string
whose tokens are the English numerals `zero` through `nine` and return those
tokens in ascending numeric order. The documented example maps
`"three one five"` to `"one three five"`.

`/reference/canonical.py` filters empty fields produced by splitting on the
ASCII space, maps each valid word to 0 through 9, performs Python's stable
ascending sort by that key, and rejoins with one space. Thus duplicates are
preserved; the empty string returns the empty string; leading, trailing, and
repeated ASCII spaces are tolerated. Invalid numeral words are outside the
stated domain and cause the canonical mapping to fail.

The submitted `solution.py` defines the same ten key values by an if-chain
(`nine` reaches the final return) and computes:

```text
" ".join(sorted(numbers.split(), key=number_value))
```

On the intended valid-token domain this is extensionally equivalent to the
canonical algorithm. Its default key 9 for invalid words and its acceptance of
non-space whitespace are outside the stated domain.

### Translator fidelity

Using the trusted copied translator, I ran:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

Both submitted and regenerated files have SHA-256
`6472ec4252c9ab7657e7b53f05c8a30b86a74fc05d9560c4de4134e6414818d9`,
and `cmp` exited 0. Exact commands and statuses are in
`stage2-regenerate.log` and `stage2-byte-identity.log`.

### Independent differential test

`/audit-output/evidence/differential_test.py` independently imports the trusted
canonical module and scratch copy of the submitted module. It covers:

- the documented example, empty input, ascending/descending order,
  duplicates, leading/trailing spaces, and repeated spaces;
- every singleton, exercising all ten `number_value` outcomes;
- every sequence of lengths 0 through 4 over the ten valid words (11,111
  cases);
- 2,000 deterministic generated cases of lengths 0 through 30, with one
  through four ASCII spaces as separators and optional edge spaces
  (seed 190019).

All 13,130 comparisons matched, and all ten helper outcomes matched 0 through
9. The case-record digest is
`2b1677ba5546b1717a2d316fa7e1f3ad43e21bcbb5ac90e6667a155234db2200`.
The exact run exited 0; see `stage2-differential.log`.

Stage result: pass.

## 3. Clean proof reconstruction

The installed live toolchain is K v7.1.337. All builds used source in
`/tmp/audit-work/audit19` and fresh output directories.

### Concrete definition

The LLVM definition was freshly built with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

It exited 0 (`stage3-kompile-concrete.log`). The compiler reported fixed
baseline non-exhaustive-match warnings for `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt`. The submitted program does not use the
first four or `valSeqAt`; `joinCodes` is used only on the string sequence
promised by the keyed-sort trust contract. These warnings are coverage gaps in
trusted total symbols, not false candidate rules.

`/audit-output/evidence/concrete_harness.py` contains the exact submitted
function bodies plus auditor-authored assertions for the example, empty input,
zero/nine boundaries, duplicates, and reverse order. It was translated with
the trusted translator and run under the fresh LLVM definition. `krun` exited
0 with `<k> .K </k>`, `<exc> NoExc </exc>`, and exit code 0; see
`stage3-concrete-translate.log` and `stage3-krun-concrete.log`.

### Proof definition and positive claims

The Haskell proof definition was freshly built with:

```text
kompile verification.k --backend haskell \
  --main-module SORT-NUMBERS-VERIFICATION \
  --syntax-module SORT-NUMBERS-VERIFICATION \
  --output-definition verification-kompiled
```

It exited 0 (`stage3-kompile-proof.log`). I then ran each target claim in an
independent `kprove` invocation using its exact label:

- `number-value-zero`
- `number-value-one`
- `number-value-two`
- `number-value-three`
- `number-value-four`
- `number-value-five`
- `number-value-six`
- `number-value-seven`
- `number-value-eight`
- `number-value-nine`
- `sort-numbers-symbolic`

Every invocation exited 0 and printed exactly one `#Top`. Commands and complete
bounded outputs are in the eleven `stage3-kprove-*.log` files; the driver and
aggregate status are in `run_positive_claims.sh` and
`stage3-positive-claims-summary.log` (`POSITIVE_CLAIM_FAILURES: 0`).

Stage result: pass.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable states

Each of the ten helper claims has implicit precondition `true`, starts from the
standard MPY initial configuration, loads the two submitted definitions, and
calls `number_value` on one concrete valid word. Its postcondition requires the
corresponding concrete integer 0 through 9 in `<k>`. The other mutable cells
may take existential final values, but exception and exit-code cells remain
`NoExc` and 0.

The main claim also has implicit precondition `true`. Its sort annotation
`WORDS:NumWords` restricts `WORDS` to finite sequences made solely from the ten
`NumWord` constructors. It calls `sort_numbers` on
`str(encodedWords(WORDS))`, where `encodedWords` denotes the empty string for
the empty sequence and exactly one ASCII space between nonempty words. It
requires the returned `<k>` value to equal the same-input term
`numericOutput(WORDS)`, not a fresh variable:

```text
str(joinCodes(" ", sortKeyVS(wordsVS(WORDS), numberKey)))
```

The default configuration in `core.k` (empty module scope and heap, builtin
parent scope, environment 0, empty stack, `noRet`, `NoExc`, exit code 0)
exhibits a satisfying entry state for all claims. `.NumWords`,
`nw(zeroW,.NumWords)`, and
`nw(threeW,nw(oneW,nw(fiveW,.NumWords)))` are explicit satisfying main inputs.
`claim_substitutions.py` and `stage4-claim-substitutions.log` record all ten
helper substitutions and six main substitutions. Under the named
`sortKeyVS` contract, every claimed result agrees with both Python
implementations, with zero mismatches.

### Exact submitted program

The proof does not read `solution.mpy` dynamically; it uses the
`solutionModule` macro. I therefore parsed and macro-expanded both the actual
submitted `solution.mpy` and the expression `solutionModule` under the fresh
proof definition:

```text
kast solution.mpy ... --sort Module --expand-macros --output json
kast --expression solutionModule ... --sort Module --expand-macros --output json
```

The JSON outputs are byte-identical, both with SHA-256
`8940a98446767dd88ade1e1b76d67f54a3649d3b3b8ef979b88c734fab446a43`.
See `stage4-kast-submitted.log`, `stage4-kast-macro.log`,
`stage4-kast-identity.log`, `submitted-module.json`, and
`macro-module.json`. This independently pins both function bodies, definition
order, parameter lists, call nesting, keyword argument, and return expression
to the regenerated real program.

`numberKey` is the exact module-scope closure
`closureVal("word", numberBody, 0)`. Normal lookup after `#loadAll` selects
that binding. The fixed call semantics evaluates the callee and arguments
left-to-right, pushes a function frame, binds parameters, executes the actual
if-chain, and pops the frame on return.

The main postcondition is result-constraining but conditional in meaning:
`sortKeyVS` remains opaque in the proof backend. The theorem proves the program
returns the exact supplied-semantics sort term; translating that term to
"ascending numeric words" uses the supplied primitive's contract.

The formal raw string domain is narrower than all behavior supported by the
Python functions: the theorem does not quantify over repeated, leading, or
trailing spaces. This is an adequacy limitation, not a substituted-program
failure.

Stage result: exact-program and result pinning pass; raw-input coverage and
opaque-sort interpretation are concerns.

## 5. Rule-by-rule static soundness review

`/audit-output/evidence/rule-inventory.md`, generated by
`k_inventory.py`, inventories 981 local K sentences by file and line:
configurations, syntax declarations, contexts, functions, total/functional and
opaque attributes, priority/concrete/owise/macro/simplification attributes,
ordinary rules, and claims. It covers the assembly `semantics.k`, all 23
supplied helper K files, `verification.k`, and `spec.k`. The assembly file has
no local semantic sentences; it only requires/imports the helper modules. The
inventory contains a disposition for every row. No local simplification rule
or candidate-local opaque symbol exists.

All supplied files are the selected fixed baseline and byte-identical to the
trusted mount. The only result-bearing fixed opaque symbol used here is
`sortKeyVS(ValSeq,Val)` (`sort.k:49`), declared
`[function,total,symbol,no-evaluators]`. Fixed call routing (`call.k`) resolves
`sorted`, dereferences the allocated list, retains the `key` closure, and
rewrites to a newly allocated `list(sortKeyVS(VS,KV))`. String `join`
(`methods.k:26-31`) then folds the resulting string sequence. The LLVM-only
concrete leg (`concrete.k:20-59`) independently computes every key through
real closure calls and stable insertion. The proof leg intentionally does not
import it.

### Used-construct map

| Submitted construct | Declaration/behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k:53-61`; `core.k:123-127`; `functions.k:13-16` |
| `If`, `Compare`, `Name`, `Str`, `Int`, `Return` | `syntax.k:9-15,30,49-50`; `core.k:129-153,193-205`; `operators.k:14-20`; `str.k:12-26`; `controls.k:50-54`; `functions.k:62-90` |
| Function calls and keyword argument | `syntax.k:25,28-29`; `core.k:94-102,183-191`; `call.k:15-32,69-75` |
| `numbers.split()` | fixed `methods.k:70-86`, plus the audited proof-local bridge |
| `sorted(..., key=number_value)` | builtin binding `core.k:156-181`; fixed opaque proof rule `sort.k:44-64`; LLVM concrete leg `concrete.k:20-59` |
| `" ".join(...)` | method routing `call.k:24,61-67`; `methods.k:23-31` |
| allocation/state | `core.k:62-121`; sorted and split both use the same `#alloc` mechanism |

Evaluation order, binding, frame/return control, and allocation are therefore
not replaced by a task-local result rule.

### Candidate-local inventory

`verification.k` contributes 42 inventoried sentences: 11 syntax
declarations and 31 rules.

- `numberBody`, `sortBody`, `solutionModule`, and `numberKey` are macros whose
  expanded module is byte-identical to `solution.mpy`.
- `NumWord` has exactly ten disjoint constructors; `NumWords` has empty and
  cons constructors.
- `wordVal` and `wordCodes` each have ten disjoint, exhaustive equations.
  `wordsVS` has exhaustive empty/cons equations. All recursive calls descend.
- `encodedWords` has three disjoint, exhaustive structural equations: empty,
  singleton, and length at least two. They encode only ASCII letters and code
  32 between tokens.
- `numericOutput` has one unguarded equation. It is a definitional summary of
  the same fixed `joinCodes(sortKeyVS(...))` expression produced by the real
  function; it neither computes a task-specific sort nor introduces an oracle.

The one operational bridge is `verification.k:95-99`:

```text
<k> #applyK(toCall(boundMethodV(str(encodedWords(WORDS)), "split")), .Vals)
 => #alloc(list(wordsVS(WORDS))) ... </k> [priority(30)]
```

Its complete match domain is a no-argument call on the exact bound method of
the encoded valid-word string, with an arbitrary continuation suffix. The
fixed rule at `methods.k:72-74` has the same receiver, argument shape,
continuation framing, and omitted-cell footprint, and rewrites to
`#alloc(list(splitWS(CS,.IntSeq,.ValSeq)))`. Both preserve every cell and the
continuation, and both defer the identical heap write/freshness check to
`#alloc`. The bridge introduces no return, exception, frame pop, or other
abrupt control.

The value equality follows by structural induction on `WORDS`:

- empty encoding is empty, and fixed `splitWS` flushes no token;
- each singleton is a nonempty ASCII-letter token and flushes to its matching
  `wordVal`;
- in the multiword case, code 32 flushes exactly the head and fixed `splitWS`
  recurses on the tail; none of the word encodings contains a whitespace code.

The three `encodedWords` shape rules and the ten finite word equations make
that induction exhaustive and overlap-free. I found no counterexample on the
intended domain.

There is nevertheless no candidate-supplied, bridge-free universal K theorem.
I removed the bridge in `verification-nobridge.k`, freshly compiled
`nobridge-kompiled`, and attempted the universal claim in
`split-connection-spec.k`. The run exited 1 with a stuck implication because
`encodedWords(WORDS)` is deliberately opaque beneath `splitWS`; ground terms
of that nested form similarly remain opaque. See
`stage5-kompile-nobridge.log`, `stage5-split-connection-proof.log`, and
`stage5-split-ground-proof.log`. These failures are not false-rule witnesses:
they show the missing machine connection and motivate the concern.

The bridge is value-sensitive. In `verification-bad-split.k` I changed only
its result to an empty list. That mutated definition built successfully, but
the main symbolic claim exited 1 with `WarnStuckClaimState` on
`sortKeyVS(.ValSeq,numberKey)` versus
`sortKeyVS(wordsVS(WORDS),numberKey)`. See
`stage5-kompile-bad-split.log`, `spec-bad-split.k`, and
`stage5-bad-split-proof.log`.

The fixed semantics' non-exhaustive total-symbol warnings and its other opaque
float/MD5/plain-sort symbols are fully listed in the inventory. They are not
reached by this submitted program. No priority overlap among used rules yields
different right-hand sides on the intended domain. I claim no candidate rule
is unsound and therefore provide no purported false-conclusion witness for an
original rule.

Stage result: static soundness passes, with a missing universal machine
connection for the otherwise mathematically justified split bridge.

## 6. Fresh non-vacuity test

I authored `/audit-output/evidence/spec-vacuity.k`, which keeps the exact
entry state and real call but changes the main result obligation from
`numericOutput(WORDS)` to `numericOutput(nw(zeroW,WORDS))`. This claims that
every result has an additional zero. The precondition is satisfiable; for
`WORDS=.NumWords`, the actual result is `""` while the mutation denotes
`"zero"` under the supplied sort contract.

The mutation was first compiled with `kprove --dry-run`. It exited 0 and
produced the backend command, so the negative result is not a parser/import
failure (`stage6-vacuity-build.log`). The actual proof then exited 1 with
`WarnStuckClaimState`. Its residual shows execution reached the returned
`joinCodes(sortKeyVS(wordsVS(WORDS),numberKey))` term and failed the implication
against the added-zero
`joinCodes(sortKeyVS(vCons("zero",wordsVS(WORDS)),numberKey))` term. See
`stage6-vacuity-proof.log`.

This is a reachable, result-bearing failure for a demonstrably false
satisfying input. It is not a timeout, crash, or unrelated residual.

Stage result: pass.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the supplied MPY definition plus the audited split bridge, the proof
establishes partial correctness of the exact expanded submitted module:

- each concrete valid word call to `number_value` returns its integer 0 through
  9 with no exception and exit code 0;
- for every finite `WORDS:NumWords`, if the real `sort_numbers` call on its
  canonical single-space encoding terminates, it returns exactly
  `str(joinCodes(space,sortKeyVS(wordsVS(WORDS),numberKey)))`, where
  `numberKey` is the actual submitted helper closure;
- the claimed return is not free or tautological, and changing either its
  input sequence or the split result invalidates the proof.

This is not, by itself, a K theorem defining the ordering behavior of
`sortKeyVS`.

### Trust ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.337 compiler, Haskell prover, LLVM executor, and builtin Int/String/Map/List hooks | all proof/build results | ordinary toolchain trust; fresh source builds avoid candidate caches |
| All 24 trusted supplied-semantics files | language execution, cells, lookup, calls, allocation, strings, sorting | exact candidate copy verified; this is the mode-selected fixed semantics |
| `sortKeyVS(VS,KV)` | directly determines the returned word order | externally supplied, result-bearing opaque primitive; K theorem is parametric in the term. Its stable-keyed-sort meaning is a named trust assumption |
| LLVM `MPY-CONCRETE` keyed-sort leg | concrete validation only | independently calls the real key closure and stable-inserts; supports but does not universally prove the opaque proof symbol's interpretation |
| Candidate split bridge | converts the symbolic encoded string to the symbolic token list | mathematically justified over the complete `NumWords` domain and value-sensitive; missing successful bridge-free universal K theorem |
| `encodedWords`/`wordsVS`/`wordVal`/`wordCodes`/`numericOutput` | input and postcondition representation | exhaustive, disjoint, terminating definitions; no fresh unconstrained value |
| Trusted translator | source-to-MPY identity | trusted input; fresh output is byte-identical to submitted `solution.mpy` |
| Differential and concrete tests | intent/primitive bridge on tested inputs | finite evidence only: 13,130 Python cases plus bounded K assertions; not substituted for the reachability proof |
| ASCII string model | all ten numeral spellings and separator | adequate here because every intended token and separator is ASCII |
| Invalid tokens, non-space whitespace, and noncanonical spacing in the symbolic theorem | excluded or incompletely covered behavior | invalid tokens are outside the prompt; the raw-spacing restriction is the documented theorem-scope concern |

The candidate's prose, absent generation logs, `spec.json`, and any prior
reported result are not in the trust ledger. They were not used to establish
closure or soundness.

### Gate summary

- Dynamic reconstruction: pass (11/11 fresh `#Top` results).
- Real-program soundness: pass, with the split connection machine-evidence
  limitation noted above.
- Intent adequacy: concern because the main theorem's raw-string encoding is
  narrower than the implementations' accepted space formatting and because
  numeric ordering is conditional on an opaque supplied primitive.
- Evidence auditability: concern because four requested provenance artifacts
  are absent; reconstruction, mutation, and differential evidence is otherwise
  reproducible below `/audit-output/evidence/`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
