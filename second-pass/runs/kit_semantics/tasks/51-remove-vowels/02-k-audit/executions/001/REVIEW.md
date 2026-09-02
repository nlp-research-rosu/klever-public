# Independent adversarial review: 51-remove-vowels

This audit used the mandated `using-kit` then `validating-proof` workflow. I
treated every candidate report, cache, compiled definition, test, and trace as
untrusted. All execution used source copied to
`/tmp/audit-work/reconstruction`; reviewer artifacts and bounded logs are under
`/audit-output/evidence`.

## 1. Input and provenance integrity

### Layout and required records

`/audit-input.json` declares:

- problem `51-remove-vowels`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- the launcher container paths used by this audit.

The supplied-semantics boundary is internally consistent:
`/reference/reference-semantics` exists and is a directory. The required
pipeline-v3 records all exist, are readable, and have the expected regular-file
or directory type:

`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`,
`/generation-evidence/metrics.json`,
`/generation-evidence/runtime-metrics.json`,
`/generation-evidence/usage.json`,
`/generation-evidence/codex-last.txt`,
`/generation-evidence/codex-output.log`,
`/generation-evidence/prompt.txt`, and
`/generation-evidence/codex-trace/`.

The trace consists of one JSONL file containing 302 valid JSON records. Its
file SHA-256 is
`7975f5ebe95fd3bc0baa2844b388e5706dab3cc06a3f5927a74799e28b52be9f`,
which is the value recorded in both `invocation.json` and
`generation-result.json`. The logs contain the generator's proof claims, but I
did not use those claims as proof results.

Evidence:

- `evidence/01-audit-input-lock.log`
- `evidence/01-mounted-inventory.log`
- `evidence/01-generation-records.log`
- `evidence/01-generation-log-inspection.log`

### Campaign and hashes

The parsed `audit_campaign` object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`. The mounted lock's SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
equal to the recorded lock hash.

Independent `sha256sum` checks matched the launcher-recorded hashes for the
lock, canonical solution, trusted prompt, trusted translator, run/task/result
records, invocation, metrics, runtime metrics, usage, generator prompt, last
message, and output log. A sorted full-candidate per-file hash manifest contains
773 files and is preserved separately; source-only hashes are in the command
log. No candidate symlink exists.

Evidence:

- `evidence/01-integrity-checks.log`
- `evidence/01-candidate-file-hashes.txt`
- `evidence/01-candidate-hash-command.log`

### Candidate/trusted comparisons

- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- `diff -qr --no-dereference` reports no difference between
  `/candidate/reference-semantics` and
  `/reference/reference-semantics`.
- A separate entry-type/path comparison is empty.
- Per-file semantics hashes are identical.
- Neither semantics tree contains a symlink.
- Required proof artifacts `solution.py`, `solution.mpy`, `verification.k`,
  `spec.k`, `prove.sh`, and `PROOF.md` are regular files; `prove.sh` is
  executable.

Thus there is no infrastructure breach and no candidate semantics-integrity
failure. Candidate-provided `runtime-kompiled/` and
`verification-kompiled/` were ignored.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt says `remove_vowels(text)` takes a string and returns the
string without vowels. The trusted canonical implementation preserves order and
removes a character exactly when `character.lower()` is one of
`a`, `e`, `i`, `o`, `u`. The examples cover empty input, mixed newlines,
all-vowel input, uppercase vowels, and no-vowel input.

The candidate implementation initializes an empty result, iterates left to
right, appends a character exactly when it is not one of the ten literal ASCII
characters `aeiouAEIOU`, and returns the accumulator. On Python strings this is
equivalent to the canonical filter. As additional evidence for the only subtle
case, the reviewer differential checked every one of Python's 1,114,112
singleton code-point strings and found no canonical/candidate disagreement.

### Trusted regeneration

I ran:

```text
python3 /reference/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/solution.regenerated.mpy
cmp /tmp/audit-work/reconstruction/solution.mpy \
    /tmp/audit-work/reconstruction/solution.regenerated.mpy
```

Both commands exited 0. Both files have SHA-256
`b3cf89a61dce62002983fda7137a9b82d2a85a369ed4d4a56d14ae3d2cad2534`.
The submitted `solution.mpy` is therefore byte-identical to trusted
regeneration.

### Independent differential execution

`evidence/reviewer_differential.py` imports the trusted canonical entry point
from `/reference/canonical.py` and the scratch candidate entry point directly.
It does not import candidate tests or use proof equations. It covers:

- all six documented examples;
- 52 empty, singleton, branch-neighbor, mixed, control-character, and Unicode
  boundary cases;
- all 8,421 strings of lengths zero through three over a branch-focused
  alphabet;
- 2,000 deterministic generated strings of lengths zero through 128; and
- all 1,114,112 possible Python singleton code-point strings, including
  in-memory surrogate values.

Result:

```text
total=10479 mismatches=0
unicode_singletons=1114112 unicode_singleton_mismatches=0
EXIT: 0
```

Evidence:

- `evidence/02-candidate-source-inspection.log`
- `evidence/02-regeneration-differential.log`
- `evidence/reviewer_differential.py`

## 3. Clean proof reconstruction

### Source isolation and builds

The scratch tree contains candidate `solution.py`, regenerated/submitted
`solution.mpy`, `verification.k`, and specs, but uses a fresh copy of the
trusted `/reference/reference-semantics`. It contains none of the candidate's
compiled definitions or caches.

The live tools report K v7.1.293. Fresh commands and results:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
EXIT: 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
EXIT: 0
```

The LLVM compiler reported fixed-semantics exhaustiveness warnings for several
unused helpers. The Haskell build reported only unused variables in the
off-path `strLt` rules. No warning concerns a proof-local declaration or a
construct used by this program.

Evidence:

- `evidence/03-build-llvm.log`
- `evidence/03-build-haskell.log`

### Positive claims

The auxiliary claim was independently selected:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC --claims SPEC.loop-invariant
#Top
EXIT: 0
```

The entry theorem depends on that loop claim as a circularity. A diagnostic run
that selected only `SPEC.remove-vowels` filtered out its required circularity
and remained in active symbolic execution; I interrupted that non-target
diagnostic with status 130. This is not a failed candidate claim. The actual
target command retains both claims:

```text
kprove spec.k --definition reviewer-verification-kompiled \
  --spec-module SPEC
#Top
EXIT: 0
```

This independently proves every positive claim in the candidate's target spec
under the fresh definition.

Evidence:

- `evidence/03-proof-loop-invariant.log`
- `evidence/03-proof-remove-vowels.log`
- `evidence/03-proof-complete-spec.log`

### Concrete reconstruction

The trusted translator generated `reviewer-concrete.mpy` from
`evidence/reviewer_concrete.py`. Under the fresh LLVM definition, the ASCII
boundary suite (empty, vowel, consonant, all ten vowels, mixed case, and the
newline example) exited 0 with no failed assertion.

Two deliberately broader attempts are also retained. A non-BMP source literal
failed at the K scanner because the translator emitted surrogate escapes; a BMP
non-ASCII literal executed but hit the supplied semantics' ASCII-only `Str`
literal limitation and exited 113. These are not hidden successes. They do not
affect this generated program: its only source literal is ASCII, and the formal
entry input is an arbitrary already-constructed `str(TEXT:IntSeq)`. Python-side
Unicode adequacy was checked independently in Stage 2.

Evidence:

- `evidence/reviewer_concrete.py`
- `evidence/03-concrete-witnesses.log`

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.loop-invariant` has no explicit `requires`. Its starting pattern says:
at a real `#loop` head, `REST` is the remaining string, the current local frame
contains exactly `text`, `result = ACC`, and `char = OLD`, while the continuation,
other scopes, parent, and omitted cells are framed. Its destination consumes
the loop, changes `result` to `removeVowelsFrom(REST, ACC)`, and permits the
final unobservable `char` value to be existential. It preserves `text`, other
scopes, continuation, and omitted state.

A concrete satisfying loop state is obtained with
`REST = ACC = TEXT = OLD = .IntSeq`, `L = 1`,
`P = parent(0)`, an empty trailing continuation, that exact three-entry local
scope, and the standard empty heap/stack and no-exception cells. Hence the loop
claim is not vacuous.

`SPEC.remove-vowels` also has no explicit `requires`. It starts from the
complete standard MPY configuration, loads one exact `remove_vowels` binding,
and calls it on any `str(TEXT)`. It requires the returned K value to equal
`str(removeVowelsFrom(TEXT, .IntSeq))`; it also constrains the final module
binding, environment, scope allocator, heap, heap allocator, stack, return
state, exception state, and exit code.

An entry precondition witness is the standard initial configuration with
`TEXT = .IntSeq`. This is exactly the empty-string call.

### Mechanical program pinning

`evidence/constructor_compare.py` extracts the balanced `Module(...)` term from
trusted-regenerated `solution.mpy` and from the entry claim's `#loadAll`.
After removing only explicit `.Stmts` empty-list tails and whitespace, which are
concrete-syntax normalizations for the same list constructors:

```text
solution_normalized_bytes=261
claim_normalized_bytes=261
module_constructor_equal=True
result_is_constrained=True
observable_closure_body_equal=True
EXIT: 0
```

The claim therefore executes the submitted function binding and body, not a
substituted implementation or external source summary. `verification.k`
contains no `<k>` rule, `Call` interception, priority rule, or operational
bridge.

### Concrete substitutions and body sensitivity

Ground summary substitutions for `""`, `"a"`, `"b"`, and `"bA-z"` close with
`#Top` in `REVIEWER-SUMMARY-GROUND`; the corresponding trusted canonical and
candidate Python outputs are respectively `""`, `""`, `"b"`, and `"b-z"`.
The first functional-form test was rejected by the backend as an unsupported
functional claim; the revised configuration claims built and closed. This
diagnostic is preserved rather than misreported as proof evidence.

The independently rerun body-sensitivity artifact changes the actually loaded
`FuncDef` body to `Return(Str(""))` and asks for the original consonant result
on `"b"`. It dry-runs successfully, then exits 1 with
`WarnStuckClaimState`, showing the changed body returned `str(.IntSeq)`. Thus
the theorem genuinely depends on the executed body.

Evidence:

- `evidence/04-constructor-pinning.log`
- `evidence/reviewer-summary-ground.k`
- `evidence/04-ground-substitutions.log`
- `evidence/04-body-sensitivity.log`

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule-inventory.tsv` is a one-row-per-declaration inventory generated
from every K source file in the supplied semantics plus `verification.k` and
`spec.k`. It contains:

- 698 ordinary rules;
- 228 syntax declarations;
- 5 contexts;
- 1 configuration; and
- 2 claims.

It records the full declaration text, attributes, line, disposition, and
reason. Separate inventories enumerate every occurrence of `function`, `total`,
`functional`, `simplification`, priority, `concrete`, `owise`, `symbol`, and
`no-evaluators`. There is no `[functional]` declaration and the only
`[simplification]` rules are the two proof-local constructor cases.

Every inventory row received one of these dispositions:

- 113 fixed, material declarations: inspected on the execution dependency path;
- 787 fixed, off-path declarations: exact trusted supplied semantics with no
  reachability from this program;
- 28 declarations in fixed opaque/off-path groups;
- 4 proof-local declarations: individually justified below; and
- 2 audited reachability claims.

There are 22 actual `[no-evaluators]` syntax symbols: float arithmetic and
conversion symbols, `sortVS`, `sortKeyVS`, and `md5hexCodes`. None is reachable
from the submitted term or from `removeVowelsFrom`.

Evidence:

- `evidence/05-exhaustive-declaration-inventory.log`
- `evidence/05-inventory-summary.log`
- `evidence/05-function-total-inventory.log`
- `evidence/05-actual-opaque-symbols.log`
- `evidence/build_rule_inventory.py`
- `evidence/rule-inventory.tsv`

### Used-construct map and fixed-rule review

The submitted constructors and their material semantics are:

| Program construct | Declaration/rule path | Static finding |
|---|---|---|
| `Module`, `FuncDef`, statement lists | `syntax.k`; `core.k` `#loadAll`/sequencing; `functions.k` function binding | Exact body is stored as a closure in module scope; no summary replaces it. |
| `Call`, `Name`, `Params` | `call.k` generic `Call` route; `core.k` lookup/left-to-right arguments; `call.k` closure frame; `functions.k` parameter binding | Callee binding is resolved normally, the argument is evaluated before binding, and a fresh local frame is pushed. No higher-priority local interception exists. |
| `Assign` | strict RHS plus `controls.k` local-map update | Initializes `result` and `char` in the current frame only. |
| `For` over `str(TEXT)` | `controls.k` `For/#loop`; `str.k` `#iterNext`; `tuple.k` `#bindTgt` | Each step yields exactly one singleton code string, binds `char`, executes the body, then reconstructs the next real loop head. Empty input consumes the loop. |
| `Compare(..., "not in", Str("aeiouAEIOU"))` | comparison contexts and dispatch in `operators.k`; ASCII literal and `strContains` in `str.k` | Operands evaluate in order. Singleton substring membership is exactly code membership in the ten-code literal; `notBool` selects the complement. |
| `If` | strict condition plus `controls.k` `#branch` rules | Exactly one branch executes based on the Boolean comparison. |
| `AugAssign(result, "+", char)` | `controls.k` local update; `str.k` `applyBin("+")`; `seqConcat` | Appends the singleton to the accumulator, preserving order. No heap/ref rule is applicable. |
| `Return`, call pop | strict return; `functions.k` `Return/#pop` | Sets the return value, restores environment and continuation, removes the local frame, and restores `scopeLoc`; heap, exception, and exit cells remain unchanged. |

The complete material source is preserved in
`evidence/05-material-rule-review.log`. Evaluation-order attributes are
appropriate: `Assign`, `For`, `If`, and `Return` are strict in the required
operand, `AugAssign` evaluates its RHS, comparison uses explicit contexts, and
call arguments use a left-to-right accumulator.

Configuration and state footprints are consistent with the claims. The module
definition changes only module scope. A call allocates one scope, pushes one
frame, binds the parameter and locals, iterates without allocation, returns,
pops the frame, and restores allocator and stack. The entry postcondition
observes all these cells. No exception-producing used construct is modeled on
this well-typed string path.

### Proof-local declarations

There is exactly one proof-local symbol:

```text
removeVowelsFrom(IntSeq, IntSeq) [function, total]
```

Its three rules are sound mathematical equations:

1. Empty remaining input returns the accumulator.
2. A constructor whose singleton occurs in the ten-code vowel sequence recurses
   on the strict tail without changing the accumulator.
3. Under the exact Boolean-complement guard, a non-vowel constructor recurses
   on the strict tail after `seqConcat` appends that singleton.

The empty and constructor shapes are disjoint. On constructor inputs the two
guards are exact complements because fixed `strContains` is a total Boolean
function. Recursion strictly decreases `REST`; coverage is exhaustive over the
free `IntSeq` constructors. The `[simplification]` attributes assert these same
true equations and do not widen their guards. The function matches no cell and
cannot bypass execution.

The loop claim is a derived circular execution lemma, not an ordinary rule in
the compiled definition. Its exact body contains no return, break, exception,
allocation, output, or stateful helper. Its arbitrary continuation is therefore
preserved rather than discarded. The entry claim executes the fixed call path
and uses the proved loop claim at the exact real loop head.

### Smuggling, overlaps, priorities, and warnings

A task-string scan finds `remove_vowels`, the vowel literal, and
`removeVowelsFrom` only in `spec.k` and `verification.k`, never in the supplied
semantics. There is no proof-local priority rule, opaque symbol, totality oracle,
call bridge, or `<k>` rewrite. Fixed priority rules for heap references, cell
variables, unrelated builtins, floats, sorting, dictionaries, and concrete-only
operations cannot match this execution.

LLVM exhaustiveness warnings concern fixed off-path helpers such as
`mapStrVS`, float conversions, `joinCodes`, and `valSeqAt`. I do not label
those rules unsound: no false conclusion witness on this program's intended
domain exists, and no warned symbol is in the dependency path. Their narrower
status is an unused supplied-semantics trust-boundary limitation.

Evidence:

- `evidence/05-used-semantics-extract.log`
- `evidence/05-material-rule-review.log`
- `evidence/05-smuggling-and-types.log`

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh
`evidence/reviewer-spec-false.k` retains the genuine loop circularity and changes
the result-constraining entry obligation for the satisfying input `"b"` from
the true result `"b"` to the false empty string.

Commands:

```text
kprove reviewer-spec-false.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-SPEC-FALSE --dry-run
DRY_RUN_EXIT: 0

kprove reviewer-spec-false.k \
  --definition reviewer-verification-kompiled \
  --spec-module REVIEWER-SPEC-FALSE
PROOF_EXIT: 1
```

The failure is the expected unmet obligation, not a parser or infrastructure
error. `WarnStuckClaimState` shows the terminal result
`str(iCons(98, .IntSeq))` and reports that it cannot unify with the false
`str(.IntSeq)` destination. The same `"b"` witness returns `"b"` in both Python
implementations and passes the fresh LLVM concrete suite.

Evidence:

- `evidence/reviewer-spec-false.k`
- `evidence/06-fresh-nonvacuity.log`

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every finite `TEXT:IntSeq`, if execution
of the trusted-regenerated submitted module and
`remove_vowels(str(TEXT))` terminates, it reaches exactly:

```text
str(removeVowelsFrom(TEXT, .IntSeq))
```

The summary is a universally defined stable left-to-right filter that removes
exactly codes 97, 101, 105, 111, 117, 65, 69, 73, 79, and 85. The reachability
proof also establishes the stated final module binding, empty call stack, no
pending return, no exception, unchanged heap/heap allocator, restored scope
allocator, environment 0, and exit code 0. This is a partial-correctness result,
not a separately proved liveness or resource-bound theorem.

The formal domain is all `str(IntSeq)` values, which contains the entire source
contract's string-code domain and is not finitely bounded. It is over-broad
because arbitrary K integers can occur as codes, but the extra cases are handled
soundly and do not narrow the HumanEval contract.

### Trust ledger

| Boundary | Influence | Evidence and classification |
|---|---|---|
| K v7.1.293 parser/compiler/Haskell prover and K builtins | All proof checking and mathematical hooks | Standard accepted proof-kernel/toolchain trust; fresh builds and runs recorded. |
| Exact supplied MPY semantics | Program evaluation, cells, calls, strings, loops | Mandated selected semantics; candidate tree is byte/type identical to trusted tree. Every declaration is inventoried and the complete material dependency path was statically reviewed. Acceptable. |
| Trusted `py2mpy.py` | Python-to-constructor translation | Candidate translator matches trusted bytes; trusted regeneration is byte-identical to submitted `solution.mpy`. The translator itself is not formally verified. Acceptable benchmark trust boundary. |
| K `String`, `Int`, `Map`, `List`, and Boolean hooks | Literal decoding, scopes, stacks, guards | Fixed low-level semantics primitives, not task-answer oracles. Acceptable. |
| Source-intent bridge from Python strings to `IntSeq` | Interpretation as character/code sequence | The generated program uses only ASCII source literals; formal input is arbitrary `str(TEXT)`. Independent differential execution covers all Python singleton code points and 10,479 multi-character cases. The compositional order-preserving filter argument remains ordinary informal mathematics, not a K theorem about CPython. Acceptable and non-material. |
| Twenty-two fixed opaque float/sort/digest symbols | None | Unreachable by constructor, sort, and call dependency analysis. They influence no branch, result, state, or claim here. Acceptable off-path boundary. |
| Termination and resources | Liveness only | Outside partial correctness. No result conclusion depends on assuming a fixed input bound. |

There is no proof-local trusted primitive, empirical bridge, fresh opaque value,
or operational rewrite. Differential execution supports implementation/intent
and Python/model adequacy only; it is not substituted for the K reachability
proof.

### Gate and benchmark decision

- Gate A — real-program soundness: PASS. Fresh `#Top`, exact body pinning,
  truthful exhaustive summary, body sensitivity, satisfiable preconditions,
  and fresh result mutation all succeed.
- Gate B — intent adequacy: PASS. The theorem covers unrestricted finite string
  inputs and establishes the requested stable vowel filter.
- Gate C — trust/evidence auditability: PASS. Trust boundaries are explicit and
  every material command, script, input scope, exit status, and residual is
  preserved.

The proof is sound, result-constraining, non-vacuous, and about the actual
trusted-regenerated program. The observed non-ASCII source-literal limitation
is off the submitted program path and does not narrow its symbolic input
theorem. No material adequacy gap or unsound rule remains.

VERDICT: PASS
LEGITIMACY: LEGIT
