# Independent adversarial review: 101-words-string

The candidate’s sole reachability claim does reconstruct to `#Top`, is
non-vacuous, constrains the returned heap object, and mechanically pins the
submitted function body. The submitted Python program also agrees with the
trusted canonical implementation in extensive differential testing.

It is nevertheless not a legitimate proof of the real Python program over the
source-contract string domain. The proof’s material no-argument `str.split()`
bridge recognizes only four whitespace code points. For the satisfying input
`"a\u000bb"`, both real Python implementations return `["a", "b"]`, while
clean K execution and the claimed postcondition return `["a\u000bb"]`. This is
a concrete false-result witness for a used semantics rule, not merely thin
evidence or an unused language feature. The theorem therefore proves the
program only under a materially narrower/incorrect string model.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `101-words-string`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

I read the launcher-owned audit input first and used only its `container_paths`
to locate mounted artifacts. `/audit-campaign-lock.json` is present, readable,
and its object matches `audit_input.audit_campaign` field-for-field. Its
independent SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the launcher-recorded lock hash.

All records required by `legacy-selected-stage1` are present, readable regular
files/directories, and were inspected:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, present `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the JSONL structured trace below `/generation-evidence/codex-trace/`.

The generation trace’s per-file SHA-256 is
`78f997f5f232959da7dc4ad717834ee9cf6d4759fc38fdb075d6751bf3328305`,
matching both `invocation.json` and `generation-result.json`. The other
launcher-recorded file hashes independently match as well. The generation
records show an earlier reported `#Top`, but I treated that only as an
untrusted historical claim. Legacy runtime metrics were never recorded and are
not required for this layout.

The supplied-semantics boundary is internally consistent:

- `/reference/reference-semantics` exists as required;
- `diff -r --no-dereference /reference/reference-semantics
  /candidate/reference-semantics` exits 0;
- neither tree contains a symlink or additional/mistyped entry;
- every corresponding file has the same independent per-file SHA-256.

The candidate prompt and translator are byte-identical to their trusted mounts:

- prompt:
  `96a270267ea64b34c5d4364f00c969284296ae45017b988c20a1c1c306dfc486`;
- translator:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The candidate contains all required proof artifacts: `solution.py`,
`solution.mpy`, `verification.k`, `spec.k`, and `prove.sh`. No
infrastructure breach was found. Detailed commands, record inspection, event
counts, and hashes are in
[`evidence/provenance_integrity.log`](evidence/provenance_integrity.log) and
[`evidence/mounted_file_hashes.txt`](evidence/mounted_file_hashes.txt).

## 2. Program fidelity and candidate-versus-canonical checks

The natural-language contract says that `words_string(s)` receives a string of
words separated by commas or spaces and returns the words as an array. The
trusted canonical implementation:

1. returns `[]` immediately for the empty string;
2. replaces each comma with an ASCII space by a character loop;
3. joins the characters and calls Python `str.split()` with no explicit
   separator.

The submitted implementation is:

```python
def words_string(s):
    return s.replace(",", " ").split()
```

This is extensionally equivalent to the canonical algorithm for Python strings,
including the empty input and all branch boundaries of the canonical loop.

Trusted regeneration was checked without accepting the candidate script:

```text
cmp solution.mpy <(python3 /reference/py2mpy.py solution.py)
exit 0
```

Thus the submitted `solution.mpy` is byte-identical to fresh output from the
trusted translator.

The independent differential test imports `/reference/canonical.py` and the
scratch copy of the generated entry point under distinct module names. It
covers:

- both documented examples;
- empty, singleton, comma-only, space-only, repeated, leading, and trailing
  separators;
- tab/newline/control and Unicode whitespace boundaries;
- Unicode words and embedded NUL;
- every string of lengths 0 through 5 over a seven-character boundary alphabet;
- 2,000 seeded strings of lengths 0 through 100.

It checked 21,631 inputs with zero mismatches. This is finite evidence for the
Python-to-Python implementation bridge, not a replacement for the K proof.
Artifacts:
[`evidence/differential_test.py`](evidence/differential_test.py) and
[`evidence/program_fidelity.log`](evidence/program_fidelity.log).

## 3. Clean proof reconstruction

I created `/tmp/audit-work/101-words-string-independent-audit` from only the
candidate source artifacts and fresh trusted mounts. I copied no
candidate-built definition or cache.

The installed tools report K version `v7.1.293`. Fresh builds and proof runs:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
exit 0

kompile verification.k --backend haskell \
  --main-module WORDS-STRING-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
exit 0

kprove spec.k --definition verification-kompiled \
  --spec-module WORDS-STRING-SPEC
exit 0
output: #Top
```

`spec.k` contains exactly one positive claim, so this independently runs every
target claim. Compiler warnings concern unrelated non-exhaustive/opaque
functions and unused `strLt` tail variables; the exact bounded outputs are in
[`evidence/clean_reconstruction.log`](evidence/clean_reconstruction.log).

A fresh ASCII K harness, generated byte-identically by the trusted translator,
passes examples, empty input, repeated commas, and mixed ASCII whitespace.
A Unicode-NBSP harness exposes the supplied runtime’s ASCII literal boundary
and exits 113 at `strToCodes`, which is a language-model limitation rather than
a failed target command.

## 4. Adequacy and real-program pinning

### Claim in plain language

The entry precondition is a complete initial call configuration:

- `<k>` calls a closure value on `str(CS)`;
- environment 0 and an empty module scope whose parent is the builtins scope;
- scope allocator 1;
- empty heap with heap allocator 0;
- empty call stack, no pending return, no exception, and exit code 0.

There is no `requires` clause: `CS` ranges over every `IntSeq`.

The postcondition requires normal completion with returned reference `ref(0)`.
Heap location 0 must contain exactly:

```text
list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))
```

and `heapLoc` must become 1. The result is therefore fully constrained; it is
not a free variable, tautology, or one-way implication.

### Satisfying witnesses

The precondition is realizable. Two reviewer-authored ground claims instantiate
the exact entry cells:

- `CS = .IntSeq`, formal/Python result `[]`;
- `CS = [97,44,98]` (`"a,b"`), formal/Python result `["a","b"]`.

Both ground K claims close with `#Top`, and both trusted canonical and generated
Python implementations equal the ground formal results. See
[`evidence/spec-ground-witnesses.k`](evidence/spec-ground-witnesses.k),
[`evidence/ground_python_witnesses.py`](evidence/ground_python_witnesses.py),
and [`evidence/ground_witnesses.log`](evidence/ground_witnesses.log).

### Program pinning

The claim does not load the complete module; it calls
`wordsStringFunction`, which reduces to a closure. That normalization is
mechanically justified:

- clean `krun solution.mpy` binds `words_string` in scope 0 to the same
  parameter sequence, body, and defining scope;
- a reviewer script asks the fresh K parser for constructor-level JSON for
  both submitted `solution.mpy` and the theorem closure reconstructed as the
  corresponding `FuncDef`;
- after only explicit empty list-tail surface normalization (`.Exprs` and
  `.Stmts`), the constructor trees are exactly equal.

The check exits 0 with `constructor_trees_equal=true`. See
[`evidence/constructor_pinning.py`](evidence/constructor_pinning.py) and
[`evidence/constructor_pinning.log`](evidence/constructor_pinning.log).
Omitting the persistent module binding is inert for this nonrecursive body,
which reads only local `s`.

A separate body-sensitivity mutation changes the closure’s actual replacement
operation from comma→space to comma→`x`, while retaining the original
postcondition. It builds successfully and `kprove` exits 1 with a
`WarnStuckClaimState` residual comparing
`splitWS(replaceC(CS,44,120),...)` to
`splitWS(replaceC(CS,44,32),...)`. Input `","` is a concrete distinguishing
witness. See [`evidence/body_sensitivity.log`](evidence/body_sensitivity.log).

The theorem therefore pins and executes the submitted body under the supplied
K semantics. Its defect is the semantics-to-real-Python bridge, not program
substitution or result vacuity.

## 5. Rule-by-rule static soundness review

I generated and reviewed an exhaustive inventory of:

- all 697 local rules;
- all 229 syntax declarations, including 148 function-bearing and 108 `total`
  declarations;
- all 32 `[concrete]`, 29 priority, 26 `[owise]`, and five context
  declarations;
- all opaque symbols, the configuration, proof-local definitions, and the
  sole claim.

The complete source-line inventory is
[`evidence/rule_inventory.md`](evidence/rule_inventory.md), generated by
[`evidence/rule_inventory.py`](evidence/rule_inventory.py). The per-module
disposition, used constructor mapping, overlap/coverage checks, and
proof-extension records are in
[`evidence/static_review.md`](evidence/static_review.md).

The material execution slice is:

1. the exact closure constant;
2. generic callee and left-to-right argument evaluation;
3. plain closure frame allocation and parameter binding;
4. local `s` lookup;
5. strict receiver evaluation and bound-method formation;
6. ASCII comma/space literal conversion;
7. the one-character `replace` equations;
8. the no-argument `split` priority rule and its helper equations;
9. fresh result-list allocation;
10. `Return` and frame pop.

The proof-local rules are not opaque or circular:

- `wordsStringFunction` is the constructor-checked exact closure;
- `wordsStringExpected(CS)` is an unconditional definitional summary using the
  fixed `replaceC` and `splitWS` functions.

Within the K theory, both are terminating/covered for their uses, and the body
executes independently to the same fixed helper term. No helper/loop claim,
semantic shortcut over source control flow, or unconstrained program-derived
oracle exists.

### False used rule and required witness

The fixed no-argument split bridge is
`reference-semantics/semantics/methods.k:72-86`. It matches an evaluated
`str(CS).split()` call and allocates `list(splitWS(CS,...))`. Its control and
heap footprint are appropriate, but its result predicate is:

```text
isWSC(C) =
  C == 32 or C == 9 or C == 10 or C == 13
```

Python `str.split()` also treats vertical tab U+000B as whitespace. The
reviewer witness is fully executable:

```text
input: "a\u000bb"
trusted canonical: ["a", "b"]
generated Python:  ["a", "b"]
clean K result:    ["a\u000bb"]
```

The reviewer `.mpy` is byte-identical to trusted translator output. Its Python
assertion exits 0. Clean `krun` exits 1 and visibly leaves the one-word K result
and two-word assertion value in separate heap objects with
`AssertionError`. Exact evidence is in
[`evidence/concrete_semantics_gap.py`](evidence/concrete_semantics_gap.py),
[`evidence/concrete_semantics_gap.mpy`](evidence/concrete_semantics_gap.mpy),
and [`evidence/semantics_gap.log`](evidence/semantics_gap.log).

The same conclusion follows symbolically at the entry claim’s satisfying
`CS=[97,11,98]`: both program execution and `wordsStringExpected` use the
incorrect one-word helper result. Unicode whitespace supplies further
witnesses, while concrete literals beyond ASCII can become stuck.

This is a material false conclusion for the real Python string function. The
trusted mount establishes integrity of the supplied tree; it does not transform
this narrower character model into Python behavior.

All unrelated semantics modules are constructor-disjoint from this execution
slice and cannot contribute to closure. Their opaque float, sort, MD5, and
underspecified OOB-list symbols are recorded as inert trust boundaries rather
than silently treated as evidence for this theorem.

## 6. Fresh non-vacuity test

I did not rely on a candidate vacuity artifact. The fresh mutation leaves the
program and precondition unchanged and changes only the result obligation:
it prepends an extra word `"x"` to the required result list. For satisfying
input `""`, the program returns `[]` while the mutation requires `["x"]`.

The mutation dry-run parses and builds successfully:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module WORDS-STRING-SPEC-VACUITY-AUDIT --dry-run
exit 0
```

The actual proof then exits 1 with `WarnStuckClaimState`. Its residual is the
expected false equality:

```text
splitWS(replaceC(CS,44,32),...)
=
vCons(str([120]), splitWS(replaceC(CS,44,32),...))
```

This is a reachable unmet postcondition after normal execution, not a parser
error, timeout, or unrelated crash. Artifacts:
[`evidence/spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k) and
[`evidence/non_vacuity.log`](evidence/non_vacuity.log).

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the exact supplied `MPY` theory, for every algebraic `IntSeq CS`, starting
from the claim’s complete initial cells, executing the constructor-identical
closure:

```python
return s.replace(",", " ").split()
```

reaches normal completion, allocates heap object 0, returns `ref(0)`, and stores
exactly:

```text
list(splitWS(replaceC(CS,44,32), .IntSeq, .ValSeq))
```

The result is body-sensitive and the false result mutation is rejected.

### Trust and assumption ledger

- **K toolchain and builtin theories:** trusted for parsing, rewriting, maps,
  lists, integers, strings, Booleans, equality, and reachability. Both clean
  builds and all proof probes are reproducible.
- **Trusted translator:** byte integrity is established, and fresh translation
  equals `solution.mpy`.
- **Source-to-claim body bridge:** mechanically established by K constructor
  equality and clean module execution; no ongoing generation mechanism is
  assumed.
- **Function-call/frame/allocation semantics:** fixed supplied rules. Their
  complete cells and control effects were checked on the used path.
- **`replaceC`:** fixed, fully defined structural equations; faithful for the
  submitted one-character arguments.
- **`splitWS` as Python no-argument `str.split()`:** materially invalid. It
  affects the returned value and final postcondition, and the executable
  U+000B witness refutes the bridge.
- **Human-facing “array of words” interpretation:** conditional on the split
  bridge. It holds for the commonly tested comma/ASCII-space fragment but is
  not proved for the full real Python string behavior.
- **Opaque float, sorting, MD5, and total OOB symbols:** imported but
  constructor-disjoint and inert for this claim; no conclusion here depends on
  them.
- **Differential tests:** finite empirical support only for equivalence of the
  two Python implementations. They do not connect the faulty K split model to
  Python.

### Gate accounting and decision

- Clean verification gate: **passes** (`#Top`, exit 0).
- Program constructor pinning and body sensitivity: **pass**.
- Result constraint/non-vacuity: **pass**.
- Real-program semantics soundness: **fails** on a used result-bearing bridge
  with a concrete satisfying false-result witness.
- Full source-contract intent adequacy: **fails** because the K theorem proves
  only the narrower supplied whitespace model.
- Evidence reproducibility: **passes**; commands, inputs, outputs, statuses,
  mutations, and inventories are preserved below `/audit-output/evidence/`.

Because a material used semantics rule makes a false result provable for the
real generated program, the successful K reachability proof is not legitimate
for the requested HumanEval contract.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
