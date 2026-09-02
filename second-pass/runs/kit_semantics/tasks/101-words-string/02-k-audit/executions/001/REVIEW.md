# Independent adversarial review: HumanEval/101 `words_string`

The candidate contains a legitimate partial-correctness proof for the material
comma/space domain of the HumanEval contract. I reconstructed the supplied
semantics and proof from source, obtained a fresh `#Top`, mechanically pinned
the claim's executed module to the trusted translation, audited the complete K
source inventory, and rejected independent false-result and body mutations.
Candidate reports, caches, and prior traces were not used as proof authority.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. This is internally consistent:
`/reference/reference-semantics` exists as required.

The independent checker
[`evidence/verify_provenance.py`](evidence/verify_provenance.py) read
`/audit-input.json` and `/audit-campaign-lock.json`, then checked the mounted
paths rather than the host provenance strings. Its complete output is
[`evidence/stage1-provenance.log`](evidence/stage1-provenance.log). In
particular:

- The campaign block equals the lock JSON, and the lock's SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required pipeline-v3 record is a readable regular file:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the one structured
  trace JSONL. No required record is a symlink.
- Every declared file hash and every invocation/result evidence hash matches.
  The independently implemented pipeline tree hash is
  `7e0f09407da5f40d38ce6df37846752e23bcfee75a317147764427f27e4a52c9`
  for `/candidate`, matching both generation records. The trace tree hash is
  `f8e9f96652c6c664381244855c30fdf4698559c466b7457e0fc6324b9a82457c`,
  matching `usage.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounted versions.
- Candidate and trusted `reference-semantics/` have exactly the same directory
  and file entries, entry types, and bytes. There are no missing, additional,
  changed, mistyped, unsupported, or symlinked entries. Both have pipeline
  tree hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.
- The complete candidate tree has no symlink entries.

I also read all launcher-required generation records and parsed all 221 JSONL
trace events. The bounded inspection, including every recorded tool call and
output status, is
[`evidence/stage1-generation-record-inspection.log`](evidence/stage1-generation-record-inspection.log);
the parser is
[`evidence/inspect_generation_records.py`](evidence/inspect_generation_records.py).
Those records show generation-time parser failures followed by correction,
fresh builds, `#Top`, and negative probes, but they remain untrusted historical
claims and do not contribute to the verdict.

There is no infrastructure breach, so candidate verdict markers are
appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

`/reference/prompt.py` requires `words_string(s)` to accept a string whose words
are separated by commas or spaces, split it into words, and return the words as
a list. The examples require:

```text
"Hi, my name is John" -> ["Hi", "my", "name", "is", "John"]
"One, two, three, four, five, six" ->
  ["One", "two", "three", "four", "five", "six"]
```

The trusted canonical implementation returns `[]` for the empty string,
replaces each comma with an ordinary space by a character loop, joins the
characters, then calls no-argument `split()`.

Candidate `/candidate/solution.py` is:

```python
def words_string(s):
    return s.replace(",", " ").split()
```

This is a different but extensionally equivalent implementation on Python
strings. It preserves the signature and exercises both relevant string
operations directly.

### Trusted translation identity

The exact command

```bash
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
```

exited 0. `cmp -s` against the submitted `solution.mpy` exited 0. Both files
have SHA-256
`041a394199807703db4f10d119803ffbf9b1791d7ea1428ed5526a0a41bc81f0`.
Commands and statuses are in
[`evidence/stage2-program-fidelity.log`](evidence/stage2-program-fidelity.log).

### Independent differential test

[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and candidate entry points directly from their fixed paths.
It does not reuse the candidate's test oracle. It covers:

- both documented examples;
- the empty string and one-character boundaries;
- comma/non-comma canonical loop branches;
- leading, trailing, adjacent, and mixed separators;
- every string of length 0 through 6 over `('a','B','0',',',' ')`;
- explicit ASCII and Unicode whitespace, non-ASCII text, emoji, and NUL; and
- 5,000 deterministic generated strings of length 0 through 80.

The command exited 0 with `UNIQUE_TOTAL_CASES=24431`,
`MISMATCHES=0`, and `DIFFERENTIAL_OK`. This is finite program-fidelity
evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/reconstruction`. Candidate
`runtime-kompiled/`, `verification-kompiled/`, Python bytecode, and other
caches were neither copied nor used.

The full command record is
[`evidence/stage3-clean-reconstruction.log`](evidence/stage3-clean-reconstruction.log);
the reproducible runner is
[`evidence/run_stage3.sh`](evidence/run_stage3.sh). The independent results
were:

| Operation | Result |
|---|---|
| Regenerate `smoke.mpy` with the trusted translator | exit 0; byte-identical |
| `kompile ... --backend llvm --main-module MPY-KRUN ... --output-definition runtime-fresh-kompiled` | exit 0 |
| `krun regenerated-smoke.mpy --definition runtime-fresh-kompiled` | exit 0; final `.K`, `NoExc`, exit code 0 |
| `kompile --backend haskell verification.k --main-module VERIFICATION ... --output-definition verification-fresh-kompiled` | exit 0 |
| `kprove spec.k --definition verification-fresh-kompiled --spec-module SPEC` | exit 0; `#Top` |

`spec.k` contains exactly one positive target claim,
`SPEC.words-string`; the full-module `kprove` command therefore exercised every
positive target claim.

The LLVM compiler reported supplied-semantics non-exhaustiveness warnings for
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. The Haskell
build/proof reported only unused variables in the supplied `strLt` rules.
None of these symbols is reachable from this target. Their static status is
accounted for in Stages 5 and 7; the warnings did not cause a build or backend
failure.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no `requires` clause or length bound. Its pre-state says:

- `CS` is an arbitrary finite `IntSeq`, passed as the modeled string
  `str(CS)`;
- the computation first loads a module containing one `words_string` binding,
  then looks up and calls that binding;
- the loaded body is
  `return s.replace(",", " ").split()`;
- the module and builtins scopes, empty heap, allocation counters, empty stack,
  return state, exception state, and exit code are all pinned.

Its post-state says:

- execution returns `ref(0)`;
- heap location 0 contains exactly
  `list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))`;
- exactly one heap object has been allocated (`heapLoc` changes 0 to 1);
- the real module binding remains, the temporary call scope/frame is gone, and
  environment, scope counter, stack, return state, exception state, and exit
  code are all constrained.

The result is therefore neither free nor tautological. It is the exact
recursively defined comma replacement and whitespace-token list, stored in the
returned heap object.

### Mechanical program identity

[`evidence/extract_claim_program.py`](evidence/extract_claim_program.py)
mechanically extracts the argument of `#loadAll` from candidate `spec.k`. Its
only normalization changes the rule parser's spelling `.Exprs` to the program
parser's spelling of the same empty list. Both the submitted `solution.mpy` and
the extracted term were parsed with `kast --sort Module --output json` through
the fresh definition. `cmp -s` on the resulting constructor JSON exited 0:
`MECHANICALLY_EXTRACTED_CONSTRUCTOR_AST_IDENTITY: YES`. See
[`evidence/stage4-pinning.log`](evidence/stage4-pinning.log). The log retains an
earlier harmless reviewer parser-syntax probe, followed by the successful
mechanical extraction.

Thus the claim executes the same function name, parameter binding, and body as
the trusted regenerated `solution.mpy`; it does not prove a substituted
program.

### Real control flow and state

The actual fixed-semantics path is:

```text
#loadAll -> statement sequencing -> FuncDef binding -> Name lookup
-> closure call/frame push -> parameter binding
-> receiver/argument evaluation -> replaceC
-> bound split dispatch -> splitWS/flushTok -> one list allocation
-> Return -> frame pop -> ref(0)
```

`Call` evaluates the callee before arguments; `#evalArgs` evaluates arguments
left-to-right. `Attribute` and `Return` strictness, lookup through the selected
closure binding, the active continuation, heap allocation, return state, and
frame cleanup are all executed by fixed rules. There is no candidate bridge
that can bypass any step.

The precondition is satisfiable; for example `CS = .IntSeq` with the explicitly
shown empty initial heap/scopes state is a concrete witness. Independent ground
substitution in
[`evidence/ground_result_check.py`](evidence/ground_result_check.py) checked
seven witnesses. Empty input yields `[]`; `"a,b"` yields `["a","b"]`; both
prompt examples yield their required lists. In every case the instantiated
formal result, trusted canonical result, and candidate Python result agree.

A separate body-sensitivity mutation changed the program term actually loaded
and executed to `s.replace(",", ",").split()`, retained the original
`"a,b" -> ["a","b"]` obligation, built successfully, and failed with the
actual heap `["a,b"]`. This is valid sensitivity evidence for the body, not an
external-source-only mutation.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`evidence/rule-inventory.md`](evidence/rule-inventory.md), generated by
[`evidence/build_rule_inventory.py`](evidence/build_rule_inventory.py). It
contains every source-level `requires`, module/import, configuration, syntax
declaration, context, function declaration, ordinary rule, and claim from the
verified supplied tree, `verification.k`, and positive `spec.k`. Multiline
declarations are retained in full. Strictness-generated rules are accounted
for at their source syntax declaration.

Inventory totals are:

- 1,073 records;
- 457 equational and 238 operational rules;
- 145 function and 82 other syntax declarations;
- 107 `total`, 45 priority, 36 `concrete`, 26 `owise`, 4 macro, and 25
  `symbol(...)` occurrences;
- zero `functional` declarations and zero simplification rules.

Each inventory record has one decision:

- `TARGET_PATH_ACCEPT`: used by this execution and individually reviewed;
- `FIXED_ASSEMBLY_ACCEPT`: fixed assembly/configuration;
- `FIXED_OUT_OF_PATH` or `FIXED_UNUSED_DECLARATION`: constructor/callee
  disjoint from the target and unable to establish its result;
- `UNUSED_OPAQUE_BOUNDARY`: a supplied opaque/symbolic primitive with no target
  dependency;
- `PROOF_LOCAL_NO_EXTENSION`: the three declarations in `verification.k`;
- target-claim/scaffolding decisions for `spec.k`.

### Used construct-to-rule map

| Submitted construct | Declaration and relevant fixed behavior |
|---|---|
| `Module`, `Stmts` | `syntax.k`; `core.k` `#loadAll` and statement sequencing |
| `FuncDef`, `Params` | `syntax.k`; `functions.k` binds the exact closure body |
| `Name("words_string")`, `Name("s")` | `core.k` scope-chain lookup |
| `Call` | `call.k` callee-first routing and `core.k` left-to-right `#evalArgs` |
| `Attribute` | strict declaration in `syntax.k`; `call.k` creates the bound method |
| `Str(",")`, `Str(" ")` | `str.k` `strToCodes`, concretely producing codes 44 and 32 |
| `replace` | `methods.k` `applyMethod` and `replaceC` |
| no-argument `split` | priority-40 `methods.k` rule, then `splitWS`, `flushTok`, `isWSC` |
| result list | `core.k` `#alloc`; `list.k` `valSeqConcat` |
| `Return` | strict declaration; `functions.k` return state and exact frame pop |

### Relevant rule validity

- `replaceC` is exhaustive on empty/cons `IntSeq`; its equality and negated
  equality guards are disjoint; every recursive call consumes one constructor.
- `splitWS` is exhaustive on empty/cons sequences. `isWSC(C)` and its negation
  are disjoint, and each recursive call consumes one input constructor.
  `flushTok` is exhaustive on empty/cons current tokens.
- `seqConcat` and `valSeqConcat` are exhaustive structural recursions.
- `isWSC` is total and identifies codes 32, 9, 10, and 13. In particular it
  implements ordinary-space splitting required by the prompt.
- The priority-40 no-argument split rule exactly preempts generic method
  dispatch for the same bound receiver and empty argument list. It allocates
  the list that the real call returns; it does not discard a continuation,
  fabricate an unrelated result, or alter another cell.
- Lookup, argument evaluation, closure binding, frame push/pop, return, and
  allocation preserve the complete target state footprint. Freshness guards
  are satisfied by the pinned counters and empty initial heap.
- There are no proof-local equations, totality assertions, priorities,
  ordinary rewrites, opaque symbols, lemmas, helper claims, or operational
  bridges. `verification.k` only imports the byte-verified `MPY` module.

The 25 supplied symbolic primitives are for floats, sorting, and MD5; the
warning-bearing total functions are likewise in unused domains. No target term
or reachable continuation contains their constructors or selects their
callees. Because K rewriting requires a matching redex and the inventory has no
global simplification rule, these unused declarations cannot affect closure of
this claim. I make no claim that the supplied semantics is a complete global
CPython model; only its target path is needed here.

I found no unsound target-relevant rule. Consequently there is no unsoundness
allegation requiring a false-conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`.
[`evidence/audit-spec-vacuity.k`](evidence/audit-spec-vacuity.k) keeps the exact
program, uses the satisfying input `"a,b"`, and changes the result obligation
from the true two-token list `["a","b"]` to the false single-token list
`["ab"]`.

Using the fresh Haskell definition:

```bash
kprove /audit-output/evidence/audit-spec-vacuity.k \
  --definition /tmp/audit-work/reconstruction/verification-fresh-kompiled \
  --spec-module AUDIT-SPEC-VACUITY --dry-run
# exit 0

kprove /audit-output/evidence/audit-spec-vacuity.k \
  --definition /tmp/audit-work/reconstruction/verification-fresh-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
# exit 1, WarnStuckClaimState
```

The residual reaches `ref(0)` and visibly contains the actual heap list
`["a","b"]`; failure is the intended result mismatch, not a parser error,
timeout, missing import, or unreachable mutation.

The separate
[`evidence/audit-spec-body-sensitivity.k`](evidence/audit-spec-body-sensitivity.k)
also dry-runs with exit 0 and proves with exit 1, showing the actual mutated
result `["a,b"]`. Exact commands and bounded residuals are in
[`evidence/stage6-mutations.log`](evidence/stage6-mutations.log). An exploratory
mutation that used an unsupported empty replacement string is retained in
`evidence/stage6-mutations-development.log` for transparency and is not relied
upon.

The fresh false-result mutation is meaningful and rejected for the expected
unmet obligation. The proof is non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What is formally proven

Under the supplied `MPY` reachability semantics, for every finite
`CS:IntSeq`, if the exact submitted module is loaded in the claim's initial
state and `words_string(str(CS))` terminates, execution reaches the fully
constrained final state. The returned value is `ref(0)`, and location 0 contains
exactly:

```k
list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))
```

The function binding, environment, allocation count, stack, return state,
exception state, and exit code are also as claimed. This is universal symbolic
partial correctness, not bounded testing or unrolling.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser/compiler/Haskell backend and reachability logic | Machine-checked closure | Standard accepted proof-tool trust boundary; rebuilt independently |
| Byte-verified supplied `MPY` semantics and K builtin Int/Bool/String/Map/List hooks | All operational steps and helper equations | Accepted fixed low-level boundary; every target-relevant source rule was audited |
| Trusted `py2mpy.py` translation | Python-source-to-constructor bridge | Accepted benchmark input; submitted translation regenerated byte-identically |
| `IntSeq` as modeled Python text | Input and returned string tokens | Formal claim is broader over arbitrary integers; valid Python strings form a satisfying subset |
| Recursive helper meaning (`replaceC`, `splitWS`, `flushTok`) | Natural-language “replace commas, return words” interpretation | Equations are exhaustive, disjoint, descending, and inspectably express the property; ground and differential evidence corroborate the bridge |
| Partial-correctness interpretation | Termination | Termination is not claimed; no false total-correctness statement is made |
| Finite Python and LLVM tests | Program/canonical and model sanity | Supporting evidence only; not used in place of the universal K proof |

The supplied fixed definition also declares these unused symbolic/opaque
boundaries:

```text
intFloatDiv, divII, floatMod, floatLt, absF, floorFI, toF, ceilF,
subF, divF, addF, mulF, powF, gtF, eqF, decStrToF,
divFloatIntV, intToF, truncF, roundF, roundFN, sqrtF,
sortVS, sortKeyVS, md5hexCodes
```

None influences a branch, value, state cell, exception, or postcondition on
this execution. No candidate-added trusted primitive or empirical oracle is
present.

The supplied model recognizes codes 32, 9, 10, and 13 as whitespace, while
real CPython no-argument `str.split()` recognizes additional Unicode
whitespace. This does not narrow the prompt's material domain of words
separated by commas or ordinary spaces, and the generated Python implementation
itself matches the canonical implementation on the broader tested cases. The K
theorem should not be cited as an exact CPython theorem for additional Unicode
whitespace code points; that is an explicit, non-material supplied-model
boundary.

### Decision

The positive claim closes from a clean build, constrains the actual result and
complete relevant state, executes the mechanically identical submitted program,
has no proof-local extension, covers arbitrary finite modeled strings rather
than fixed sizes, and rejects both a fresh false result and a supported body
mutation. There is no material source-contract or soundness gap.

VERDICT: PASS
LEGITIMACY: LEGIT
