# Independent adversarial audit: 101-words-string

This audit used the rendered `SUPPLIED_SEMANTICS` boundary. I treated every
candidate artifact and prior output as untrusted, copied only source artifacts
to `/tmp/audit-work`, and rebuilt from source with K 7.1.337. The candidate's
proof reconstructs successfully and is result-sensitive. I found no
execution-bypassing or mathematically false proof-local rule. There are,
however, non-fatal audit limitations: the candidate entry claim begins at an
exact literal closure rather than including the top-level module-load step in
the same theorem, and the supplied string model recognizes fewer whitespace
characters than Python `str.split()`. Four requested generation-provenance
files are also absent. A separate reviewer-authored, bridge-free fixed-semantics
claim independently proves the exact module-to-closure connection.

## 1. Input and provenance integrity

### Semantics-mode boundary

`/reference/reference-semantics` is present, as required for
`SUPPLIED_SEMANTICS`. The mount therefore does not contradict the rendered
mode, and this is not an infrastructure breach.

I compared the candidate and trusted semantics recursively by relative path,
entry type, and SHA-256. The trees have 25 typed entries (one subdirectory and
24 K files), with:

- no missing candidate entry;
- no additional candidate entry;
- no type mismatch;
- no content mismatch; and
- no symlink.

The complete typed comparison is in
`/audit-output/evidence/integrity_check.py` and
`/audit-output/evidence/01_integrity.log`. The initial filesystem and tool
inventory is in `/audit-output/evidence/00_environment.log`.

The candidate `prompt.py` and `py2mpy.py` are regular files and are byte
identical to the trusted versions:

- `prompt.py` SHA-256:
  `96a270267ea64b34c5d4364f00c969284296ae45017b988c20a1c1c306dfc486`
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The candidate tree contains no symlink anywhere. `solution.py`,
`solution.mpy`, `spec.k`, and `verification.k` are regular files.

### Missing and untrusted provenance

The following specifically requested candidate provenance files are absent
(reported as nonexistent/mistyped rather than silently ignored):

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present. The candidate does contain
`prove.sh`, `kprove.out`, `concrete_tests.py`, and `concrete_tests.mpy`; I read
them only as untrusted claims. I did not reuse `kprove.out`, its test harness,
or any compiled result. `/candidate/__pycache__` was ignored. The missing
provenance weakens auditability but does not prevent independent proof
reconstruction.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical behavior

The trusted prompt asks for a function that takes a string containing words
separated by commas or spaces and returns the words as an array. Its examples
are:

- `"Hi, my name is John"` to
  `["Hi", "my", "name", "is", "John"]`; and
- `"One, two, three, four, five, six"` to
  `["One", "two", "three", "four", "five", "six"]`.

The trusted canonical implementation returns `[]` on the empty string,
replaces each comma with an ASCII space by iterating through the input, joins
the characters, and applies Python's no-argument `split()`.

The submitted implementation is:

```python
def words_string(s):
    return s.replace(",", " ").split()
```

On the intended domain of Python strings, its comma replacement is
extensionally the same as the canonical character loop, after which both use
the same Python `split()`. Non-string inputs are outside the prompt's domain;
the two implementations need not agree there.

### Trusted translation identity

I regenerated MiniPython with:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/generated/solution.mpy
cmp /tmp/audit-work/generated/solution.mpy /tmp/audit-work/candidate-src/solution.mpy
```

Both commands succeeded. The generated and submitted files are byte
identical, with SHA-256
`041a394199807703db4f10d119803ffbf9b1791d7ea1428ed5526a0a41bc81f0`.
See `/audit-output/evidence/02_translate.log`.

### Independent differential testing

`/audit-output/evidence/differential_test.py` imports the trusted canonical
entry point and the scratch copy of the submitted entry point under distinct
module names. It does not reuse proof equations.

The corpus contains:

- both documented examples;
- empty, one-character, prefix/suffix, adjacent-separator, and
  separator-only boundaries;
- tabs, newlines, form feed, Unicode whitespace, Unicode non-whitespace, and
  an embedded NUL;
- every string of lengths 0 through 5 over
  `("a", "Z", ",", " ", "\t")`; and
- 2,000 seeded generated strings of lengths 0 through 80.

After deduplication, all 5,875 inputs and both results are preserved in
`/audit-output/evidence/differential_cases.jsonl` (SHA-256
`9121f7fd0a0f410c8be5467fd4ea5bad13570cfa45cc1c140ab67f9d13ac324b`).
The command exited 0 with zero mismatches. See
`/audit-output/evidence/03_differential.log`.

This is strong finite evidence for candidate-versus-canonical program
fidelity; it is not a universal K/Python connection theorem.

## 3. Clean proof reconstruction

All work in this stage used `/tmp/audit-work/candidate-src`, copied source,
and fresh output directories. No candidate-built K definition or cache was
present or reused.

### Concrete definition and independent execution

I built the concrete definition from the copied, integrity-checked submitted
semantics:

```text
kompile candidate-src/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled
```

The command exited 0. The compiler emitted totality warnings for several
unrelated helpers, which are discussed in Stage 5. See
`/audit-output/evidence/05_kompile_llvm.log`.

The reviewer-authored harness
`/audit-output/evidence/concrete_reconstruction.py` begins with an exact copy
of `solution.py` and asserts the examples, empty input, comma-only input,
adjacent commas, mixed whitespace, and boundary commas. It was translated
with the trusted translator. Running the resulting MPY program under the fresh
LLVM definition exited 0:

```text
krun generated/concrete_reconstruction.mpy \
  --definition concrete-kompiled --output none
```

See `/audit-output/evidence/04_concrete_translate.log` and
`/audit-output/evidence/06_krun_concrete.log`.

I also ran the submitted `solution.mpy` itself under that definition. It
terminated at `.K` and placed a `words_string` binding in scope 0 whose
`closureVal` has the exact submitted parameter, return body, and captured
environment 0. The complete final configuration is in
`/audit-output/evidence/15_krun_solution_module.log`.

### Proof definition and all positive target claims

I built the proof definition from the copied source:

```text
kompile candidate-src/verification.k \
  --backend haskell \
  --main-module WORDS-STRING-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0; see `/audit-output/evidence/07_kompile_haskell.log`.

There is exactly one positive claim and no auxiliary or loop claim. I ran it
independently:

```text
kprove candidate-src/spec.k \
  --definition verification-kompiled \
  --spec-module WORDS-STRING-SPEC
```

It exited 0 and printed `#Top`. See
`/audit-output/evidence/08_kprove_positive.log`. The only warnings concern
unused pattern variables in the trusted `strLt` rules, which this program does
not reach.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim has no `requires` clause. Its inferred input domain is every
`CS:IntSeq`. Its initial state is the default empty module environment:

- current environment 0;
- scope 0 empty with builtins scope -1 as parent;
- fresh scope location 1;
- empty heap with fresh heap location 0;
- empty stack;
- no pending return or exception; and
- exit code 0.

The initial computation calls `wordsStringFunction` with the modeled string
`str(CS)`.

The postcondition requires the call to be consumed and return exactly
`ref(0)`. It requires heap location 0 to contain exactly
`list(wordsStringExpected(CS))`, increments the fresh heap location to 1, and
restores the remaining control and state cells. The result is neither a free
variable nor an implication-only or tautological obligation.

There are no loops and therefore no helper loop claims to match against
control flow.

### Pin to the submitted body

`wordsStringFunction` reduces to a literal `closureVal` with parameter `s`,
captured environment 0, and the same single `Return` AST as the trusted
translation of `solution.py`. The mechanical comparison in
`/audit-output/evidence/pinning_check.py` normalizes only the equivalent
concrete-versus-explicit `.Exprs` list spelling. It reports:

```text
return_body_byte_normalized_equal=True
solution_is_single_expected_funcdef=True
verification_contains_expected_closure=True
```

Both normalized return bodies have SHA-256
`fceddb0566c15a5ed4f8f4a33538ca23d55bc0c676f3c00c814279259353e626`.
See `/audit-output/evidence/14_pinning.log`.

The fixed top-level `FuncDef` rule would capture the current environment, and
the submitted module concretely produces this same closure in environment 0
(Stage 3). The proof claim then executes the body through ordinary fixed
callee, argument, method, allocation, return, and frame-pop rules.

I also created `/audit-output/evidence/spec-module-connection.k`, which puts
the exact submitted `Module(FuncDef(...))` under `#loadAll` and requires the
exact closure used by the entry claim. I built a separate Haskell definition
whose main module is the fixed `MPY` semantics alone; it does not import
`verification.k` or either proof-local function. The connection proof exited
0 with `#Top`. See
`/audit-output/evidence/18_module_connection_build.log` and
`/audit-output/evidence/19_module_connection_proof.log`. This supplies a
machine-checked, bridge-free connection from the real submitted module to the
literal closure.

Limitation: the candidate's own entry claim still does not compose module
loading, the `words_string` name lookup, and the call in one reachability
claim. It begins at the exact closure after the now independently checked
module-load transition. This is a presentation/composition limitation, not a
substituted-body or result-oracle gap.

### Satisfying witness and concrete substitution

`/audit-output/evidence/spec-ground.k` instantiates the claim with
`CS = [97, 44, 44, 98]`, the modeled string `"a,,b"`, and requires the exact
modeled result `["a", "b"]`. It uses the same realizable initial state as the
entry claim. The ground proof exited 0 with `#Top`; see
`/audit-output/evidence/09_kprove_ground.log`.

`/audit-output/evidence/ground_witness.py` independently evaluates the
formal helper model, trusted canonical Python, and candidate Python:

```text
input "a,,b":
formal claim result = ["a", "b"]
canonical result    = ["a", "b"]
candidate result    = ["a", "b"]
```

See `/audit-output/evidence/10_ground_witness.log`.

### Intent/model boundary witness

The same evidence exposes a real but non-fatal bridge limitation:

```text
input "\fa":
formal claim result = ["\fa"]
canonical result    = ["a"]
candidate result    = ["a"]

input "a\u2003b":
formal claim result = ["a\u2003b"]
canonical result    = ["a", "b"]
candidate result    = ["a", "b"]
```

The supplied semantics' `isWSC` recognizes only code points 32, 9, 10, and
13. Python's no-argument `split()` also recognizes form feed, vertical tab,
and Unicode whitespace. This does not make the candidate's K rule false under
the supplied semantics, and the prompt explicitly speaks of comma and space
separators. It does mean the formal result cannot be advertised as a complete
model of Python `split()` over all Python strings.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/build_rule_inventory.py` inventories every K source
item in the supplied semantics, `verification.k`, and `spec.k`, preserving the
complete source block, path, line span, attributes, relevance classification,
and a per-item judgment. The exhaustive JSONL record is
`/audit-output/evidence/rule_inventory.jsonl`; its command and summary are in
`/audit-output/evidence/13_rule_inventory.log` and
`/audit-output/evidence/rule_inventory_summary.txt`.

The inventory covers 26 files and 933 source items:

| Kind | Count |
|---|---:|
| local syntax declarations | 229 |
| configuration declarations | 1 |
| contexts | 5 |
| ordinary semantic/proof-local rules | 697 |
| reachability claims | 1 |

Attribute inventory:

| Attribute/class | Count |
|---|---:|
| `function` | 147 |
| `total` | 108 |
| `functional` | 0 |
| `simplification` rules | 0 |
| `concrete` | 35 |
| priority rules | 41 |
| `owise` | 26 |
| `symbol` | 25 |
| `no-evaluators` opaque declarations | 22 |

Every record is classified either as a reviewed proof-local definition, a
relevant fixed-semantics rule, a concrete-only rule, or a fixed supplied rule
outside the reachable slice. A fixed rule is outside the slice when its head
cannot be generated by this AST and no reachable rule calls its helper. Such a
rule cannot affect this claim; it remains part of the trusted supplied
baseline rather than a candidate proof extension.

The 22 explicitly opaque/no-evaluator symbols are `md5hexCodes`; the float
helpers `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`,
`truncF`, `roundF`, `roundFN`, and `sqrtF`; and `sortVS` and `sortKeyVS`.
None occurs in the submitted program, entry claim, proof-local definitions,
or reachable rule slice. No opaque value can influence this proof's branch,
return, heap, exception, or postcondition.

`MPY-CONCRETE` is imported only by the LLVM module `MPY-KRUN`; it is not
imported by the proof module `MPY`. Its concrete sorting/deep-equality rules
therefore cannot help close the proof.

### Program construct map

Every syntactic construct in `solution.mpy` is declared and accounted for:

| Construct | Declaration | Operational treatment |
|---|---|---|
| `Module` | `semantics/syntax.k:61` | `#loadAll` and statement sequencing in `core.k:124-127`; checked concretely and by the auxiliary connection theorem, but omitted from the candidate entry claim |
| `FuncDef` | `syntax.k:53` | closure creation/binding in `functions.k:14-16`; auxiliary theorem proves it creates the exact literal closure used at claim entry |
| `Params` | `syntax.k:57` | parameter names become the closure's `ParamNames` and are bound by `#bindP` |
| `Return` | `syntax.k:50` (`strict`) | value evaluation, return state, and frame pop in `functions.k:78-90` |
| `Call` | `syntax.k:28` | callee-first then left-to-right argument evaluation in `call.k:20-24` and `core.k:183-191` |
| `Attribute` | `syntax.k:29` (`strict(1)`) | receiver evaluation then `boundMethodV` in `call.k:16` |
| `Name` | `syntax.k:12` | lexical scope-chain lookup in `core.k:130-154` |
| `Str` | `syntax.k:13` | ASCII literal conversion in `str.k:13-17`; this body uses only comma and space literals |

The initial/final claim contains all active configuration cells. Call setup
allocates a fresh callee scope, binds `s`, and saves the continuation. Return
restores the caller environment and stack and removes the callee scope. List
allocation writes heap location 0 and increments `heapLoc`. No rule in the
reachable slice changes output, external state, or an omitted exception cell.

### Proof-local definitions

There are exactly two proof-local function definitions.

1. `wordsStringFunction`

   This is a nullary definitional function with one unguarded equation. It
   produces a literal closure; it does not rewrite a `Call`, replace method
   execution, pop a frame, or fabricate a result. The body and captured
   environment match the submitted function as discussed in Stage 4. There is
   no overlapping equation. Although it is not marked `total`, its sole
   nullary case is covered.

2. `wordsStringExpected(CS)`

   This is marked `[function, total]` and has one unguarded equation over the
   complete `IntSeq` domain:

   ```text
   splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq)
   ```

   It does not intercept or replace program execution. It is a definitional
   name for a composition of two fixed-semantics helpers. There is no overlap
   and no proof-local recursion. The actual function body still executes
   through fixed semantics and independently reaches that composition. Thus,
   using the fixed helpers in the postcondition is not an unconstrained
   proof-local oracle.

### Reachable fixed rules, overlap, priority, and totality

- `replaceC` has an empty-sequence base case and two nonempty cases guarded by
  `C == A` and its Boolean negation. They are disjoint, exhaustive, and recurse
  on the tail.
- `splitWS` has an empty-sequence case and two nonempty cases guarded by
  `isWSC(C)` and its negation. They are disjoint, exhaustive, and recurse on
  the remaining input.
- `flushTok` splits structurally on an empty versus nonempty current token.
  `seqConcat` and `valSeqConcat` likewise split structurally and descend.
- `isWSC` is total for all model integers and returns exactly membership in
  `{32, 9, 10, 13}`. The narrower-than-Python set is an intent adequacy
  limitation, not a false conclusion relative to the selected supplied
  semantics.
- The `replace` method rule applies only to one-code-point old and new strings,
  exactly the arguments used here.
- The no-argument `split` rule has priority 40 over generic bound-method
  dispatch. Its matched context preserves the trailing computation and
  allocates the result; it does not introduce abrupt control or omit a state
  effect. The priority selects the more specific fixed behavior and does not
  supply a proof shortcut.
- `Call` evaluates the callee before arguments; `#evalArgs` evaluates
  arguments left-to-right; the closure call allocates and later removes the
  callee scope; `Return` and `#pop` preserve the value and restore control.
- The comma and space `Str` literals satisfy the semantics' ASCII guard.

The LLVM compiler warned that unrelated declared-total helpers such as
`mapStrVS`, several float converters, `joinCodes`, and `valSeqAt` have
non-exhaustive patterns. None is generated or referenced in this proof slice,
so those warnings cannot make this conclusion close. They are nevertheless
preserved in `/audit-output/evidence/05_kompile_llvm.log` rather than hidden.

I found no candidate rule for which the selected semantics plus ordinary
mathematics yields a false conclusion on the intended comma/space input
domain. Accordingly, I do not label any candidate rule unsound. The form-feed
and Unicode-space examples are explicit witnesses against an over-broad
Python-semantics interpretation, not witnesses that a K rule is false in the
supplied model.

### Operational/body sensitivity

As a separate check from postcondition non-vacuity, I changed the embedded
body to replace commas with `"X"` while keeping the expected summary's
space replacement. The mutated definition compiled successfully
(`/audit-output/evidence/11_body_mutation_build.log`). Its proof exited 1 with
`WarnStuckClaimState`, leaving the expected unmet equality between:

```text
splitWS(replaceC(CS, 44, 88), ...)
```

and:

```text
splitWS(replaceC(CS, 44, 32), ...)
```

See `/audit-output/evidence/verification-body-mutation.k`,
`/audit-output/evidence/spec-body-mutation.k`, and
`/audit-output/evidence/12_body_mutation_proof.log`. The positive proof is
therefore sensitive to the body computation it purports to verify.

## 6. Fresh non-vacuity test

The candidate provides no `spec-vacuity.k`. I created
`/audit-output/evidence/spec-vacuity.k` from scratch. It preserves the
original precondition and execution but changes the result-bearing heap
obligation by prepending an extra `"X"` token:

```text
vCons(str(iCons(88, .IntSeq)), wordsStringExpected(CS))
```

For the satisfying input `CS = .IntSeq` (the empty Python string), ordinary
execution and both Python implementations return `[]`; the mutation requires
`["X"]`.

The mutated spec completed `kprove --dry-run` with exit 0, establishing that it
parses and builds against the fresh proof definition. See
`/audit-output/evidence/16_vacuity_dry_run.log`.

The actual proof exited 1 with `WarnStuckClaimState`, not a parser error,
timeout, missing import, or unrelated crash. Its residual is the unmet
result equality:

```text
splitWS(replaceC(CS, 44, 32), ...)
  ==
vCons(str(iCons(88, .IntSeq)),
      splitWS(replaceC(CS, 44, 32), ...))
```

See `/audit-output/evidence/17_vacuity_proof.log`. This is meaningful fresh
non-vacuity evidence.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Under the unmodified supplied K semantics, for every modeled `IntSeq` `CS`,
if execution begins in the exact initial configuration in `spec.k` and the
literal closure corresponding to the submitted function is called with
`str(CS)`, partial correctness establishes that a terminating execution:

- returns exactly `ref(0)`;
- stores exactly
  `list(splitWS(replaceC(CS, 44, 32), .IntSeq, .ValSeq))` at heap location 0;
- advances `heapLoc` from 0 to 1; and
- restores the remaining framed control state with no exception.

This is a result-constraining reachability theorem about the real submitted
function body under the selected semantics. It is not merely a test report,
and the candidate's prior `#Top` played no role in accepting it.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K 7.1.337 compiler and Haskell/LLVM backends | Parsing, rewriting, and proof checking | Standard machine-checking trust boundary; rebuilt independently |
| Trusted mounted supplied semantics | All language execution and modeled string behavior | Required fixed boundary; candidate copy is byte/type identical |
| Trusted `py2mpy.py` | Source-to-MPY identity | Byte-identity check pins submitted MPY to submitted Python |
| `wordsStringFunction` literal closure | Selects body, parameters, and environment | Audited exact and body-sensitive; a bridge-free fixed-semantics auxiliary claim proves exact module loading creates the closure, although the candidate entry claim does not compose the name lookup |
| `wordsStringExpected` | Final heap value | Audited truthful fixed-helper composition, not opaque and not execution-bypassing |
| K `IntSeq` as Python string codes | Bridge from model values to Python strings | Acceptable for comma/ASCII-space intent, limited for full Unicode/Python whitespace behavior |
| Candidate-versus-canonical differential corpus | Implementation-to-reference bridge on 5,875 inputs | Strong finite evidence only; not a universal proof |
| 22 supplied opaque symbols | Potential external primitives in the overall language | None is reachable or result-bearing for this claim |
| Missing generation provenance | Historical reconstruction | Auditability concern; independent source reconstruction still succeeds |
| Termination | Outside partial correctness | Not claimed by this verdict |

There is no fresh, unconstrained, or opaque value on the result path. No
empirical result is substituted for the K reachability proof. The two
documented limitations do not enable a false formal postcondition under the
selected semantics, and they do not substitute a different function body.
They do prevent an unqualified claim that the theorem models every behavior of
Python's Unicode `str.split()` or that the candidate's single target claim
itself includes the top-level module-load and name-lookup steps.

### Decision

The clean `#Top`, exact body pin, fixed-semantics execution, satisfying ground
witness, body-sensitivity failure, and fresh false-result failure establish a
legitimate non-vacuous partial-correctness proof. The candidate's
direct-closure presentation (despite the successful independent connection
theorem), narrower supplied whitespace model, finite intent bridge, and
missing generation provenance warrant `CONCERNS` rather than an unqualified
`PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
