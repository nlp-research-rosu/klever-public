# Independent adversarial audit: 93-encode

The candidate does not contain a legitimate partial-correctness proof of the
full generated program contract. Fresh reconstruction does reproduce every
submitted `#Top`, and the submitted Python is faithful on the English-letter
domain. However, the only universal claim is a loop-only theorem that closes
through a task-specific fused semantics rule. That rule writes the same
otherwise-unconstrained `encodedChar` oracle used by the postcondition instead
of executing the loop body. A fresh opposite-interpretation test gives a false
conclusion witness. The entry-point claims are only three fixed strings; there
is no universal end-to-end claim for arbitrary-length messages.

All candidate artifacts were treated as untrusted. Builds and mutations used
fresh copies under `/tmp/audit-work/93-encode-audit`; candidate compiled
definitions, `kore-exec.tar.gz`, `__pycache__`, prose, logs, and prior `#Top`
claims were not reused.

## 1. Input and provenance integrity

The declared layout is `legacy-selected-stage1`, the condition is `bare`, and
the rendered semantics mode is `GENERATED_SEMANTICS`.

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`,
  `/generation-result.json`, and every required generation record are readable,
  regular, non-symlinked mounts. `usage.json` is present and was inspected.
  Historical `runtime-metrics.json` is absent but is not required for this
  legacy-selected layout.
- The campaign object in `/audit-input.json` is exactly equal to
  `/audit-campaign-lock.json`; the lock's SHA-256 is the recorded
  `ad5dfc...d745`.
- Every launcher-recorded file hash checked in
  `evidence/01_integrity_check.log` matches, including the run/task/result
  manifests, invocation, prompt, metrics, usage, Codex log/last message,
  canonical source, candidate/trusted prompts, and candidate/trusted
  translators. The embedded task manifest matches `/task.json` after the
  launcher-added `config` overlay.
- The generation result and invocation hashes for every evidence file also
  match. The sole JSONL trace is a regular file with 390 parseable records and
  no parse errors. The complete record summary is in
  `evidence/01_generation_records.log`; these success markers were not used as
  proof evidence.
- Candidate `prompt.py` is byte-identical to `/reference/prompt.py`, and
  candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- The independently computed pipeline tree digest of `/candidate` is
  `c56937...e9c`, exactly the invocation's retained workspace digest. The trace
  tree digest is `87162b...31e0`, exactly `usage.json`'s source-trace digest.
  The separate `candidate_tree_sha256` and `generation_codex_trace_sha256`
  fields in `/audit-input.json` use an unspecified, different tree encoding;
  they are not reproduced by the pipeline digest. Because the mounted
  candidate and trace independently bind exactly to their generation records
  and all per-file hashes match, this is an auditability observation, not a
  missing, unreadable, or contradictory provenance mount.
- `/reference/reference-semantics` does not exist, as required in
  `GENERATED_SEMANTICS`; the candidate also has no `reference-semantics`
  directory. No hidden or inferred reference semantics was used.

Evidence:

- `evidence/01_integrity_check.py` and `.log`
- `evidence/01_generation_records.py` and `.log`

There is no infrastructure breach requiring `AUDIT_ERROR`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` asks for `encode(message)`: swap the case of all English
letters and replace each vowel with the letter two positions ahead in the
English alphabet. Although it says “Assume only letters,” its second documented
example includes spaces, so the material domain is arbitrary-length messages
over English letters with the demonstrated preservation of spaces.

`/reference/canonical.py` constructs the ten-vowel `+2` mapping, swaps case on
the complete message, and applies the mapping to vowels in the swapped string.
The candidate instead advances an original vowel and then swaps that
character's case. These orders are equivalent for English upper/lowercase
letters.

### Translator identity

Fresh translation used the trusted `/reference/py2mpy.py`:

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`041d179bebc6e816f36536b78fe1bdee2f727614fef76283398c99a5d3c86666`;
`cmp` exited 0. See `evidence/02_regeneration.log`.

### Independent differential test

`evidence/02_differential.py` imports the trusted canonical and submitted entry
points independently. It exercised:

- 29 examples and boundary cases, including empty input, each vowel in each
  case, consonants, spaces, all ASCII English letters, repeated length-128
  inputs, and the documented examples;
- all 16,105 strings of lengths 0 through 4 over
  `"aAeEuUbBzZ "`; and
- 2,000 seeded random strings of lengths 0 through 256 over ASCII letters and
  space.

All 18,134 intended-domain comparisons matched; exit status was 0. The script
also reports Unicode diagnostics separately because the prompt names the
English alphabet. In particular, `"İı"` exposes a candidate/canonical
difference outside that reading (`"i̇I"` versus `"k̇K"`); it is not used as the
primary verdict basis.

Conclusion: program and translator fidelity pass for the material English
source-contract domain.

## 3. Clean proof reconstruction

The observed toolchain was K v7.1.293 and Python 3.10.12. Both definitions were
freshly built from copied source:

| Definition | Command log | Exit |
|---|---|---:|
| Abstract proof definition | `evidence/03_build_verification.log` | 0 |
| Concrete proof/execution definition | `evidence/03_build_concrete_verification.log` | 0 |

Every submitted positive claim was then run separately:

| Claim | Definition | Result | Evidence |
|---|---|---|---|
| `SPEC.encode-loop-correct` | abstract | `#Top`, exit 0 | `03_prove_encode_loop.log` |
| `CONCRETE-SPEC.example-test` | concrete | `#Top`, exit 0 | `03_prove_example_test.log` |
| `CONCRETE-SPEC.example-message` | concrete | `#Top`, exit 0 | `03_prove_example_message.log` |
| `CONCRETE-SPEC.ascii-domain` | concrete | `#Top`, exit 0 | `03_prove_ascii_domain.log` |

The universal loop run repeatedly warns that `encodedChar` and
`advancedVowel` have no evaluators in the abstract definition. This is
substantive, not cosmetic; stage 5 demonstrates that the proof relies on their
opacity.

Fresh `krun` executions under the concrete generated semantics produced:

| Input | K result | Canonical Python | Candidate Python |
|---|---|---|---|
| `""` | `""` | `""` | `""` |
| `"aA bB"` | `"Cc Bb"` | `"Cc Bb"` | `"Cc Bb"` |
| `"This is a message"` | `"tHKS KS C MGSSCGG"` | same | same |

Commands and complete bounded configurations are in
`evidence/03_concrete_krun.log` and
`evidence/03_concrete_python.log`.

Dynamic reconstruction therefore passes as a reproduction of the submitted
claims. It does not establish their adequacy or theory soundness.

## 4. Adequacy and real-program pinning

### Plain-language claims

`SPEC.encode-loop-correct` has no side-condition restricting `S`. Its
precondition is:

- `<k>` contains `loopString("char", S, encodeLoopBody())`;
- the environment contains exactly `char = C`, `message = M`, and
  `result = R`, all strings; and
- arbitrary unchanged `functions` and `result` cells.

Its postcondition says the loop terminates with empty `<k>`, preserves the
message and the two other cells, allows any final `char`, and sets the
accumulator to `R + encodeSpec(S)`.

The three `CONCRETE-SPEC` claims start from empty environment/functions and
`noResult`, execute `encodeProgram() ~> invoke("encode", fixedString)`, and
constrain the returned value to the listed concrete string. They have no input
variable:

- `"test"` returns `"TGST"`;
- `"This is a message"` returns `"tHKS KS C MGSSCGG"`;
- the single 53-character string containing every ASCII English letter once
  plus one space returns one fixed 53-character output.

The label `ascii-domain` overstates the third theorem. A single string is not a
theorem over every string, every length, or every ordering drawn from that
alphabet.

### Program pinning

The claims do not read `solution.mpy` directly; they use `encodeProgram()`.
This is acceptable only if the constructor term is identical. After trusted
regeneration, `evidence/04_pinning_spec.k` mechanically checks that
`encodeProgram()` expands to the exact regenerated `Module(FuncDef(...))`
constructor tree. `kprove` returned `#Top`, exit 0
(`evidence/04_constructor_pinning.log`). Thus the fixed concrete claims do pin
the submitted program term.

### Satisfying states and substitutions

- A satisfying loop state is
  `S="a", C="x", M="a", R="", FS=.Map, RES=noResult`. Its concrete expected
  post-state has `char="c"` and `result="C"`. The ground reachability witness
  in `evidence/04_ground_witness_spec.k` proves exactly that (`#Top`, exit 0);
  both Python implementations also return `"C"` for `"a"`.
- The three entry preconditions are concretely satisfiable by their empty
  initial cells. Their expected outputs agree with both Python implementations,
  as shown by stages 2 and 3.

A body-sensitivity mutation changed the actual constructor executed by the
loop claim from `ord(char) + 2` to `ord(char) + 3`, leaving the fused `+2`
pattern unchanged. It built successfully and the formerly positive loop claim
failed with `WarnStuckClaimState`; see
`evidence/04_body_mutation.diff` and `04_body_sensitivity.log`.

### Adequacy failure

There is no submitted claim of the required shape

```text
encodeProgram() ~> invoke("encode", pyStr(S))
  => returned(pyStr(encodeSpec(S)))
```

for symbolic `S`. The universal loop claim omits module loading, function
lookup/binding, initialization, `For` entry, return, and the final result cell.
The only entry claims are finitely many examples. Consequently the candidate
materially narrows an arbitrary-length HumanEval contract to three fixed
messages. Under the benchmark decision rule, this alone is
`FAIL / NOT_LEGIT`, not a non-fatal concern.

## 5. Rule-by-rule static soundness review

The exhaustive local inventory is
`evidence/05_rule_inventory.md`. It enumerates all 20 local syntax sentence
heads (17 in `semantic.k` and 3 in `verification.k`) and their alternatives,
all local function/total declarations, all 41 rules in
`semantic.k`, all 3 rules in `concrete.k`, all 7 rules in `verification.k`,
the sole priority rule, both `[owise]` rules, all 4 simplification rules, and
all 4 claims.

### Construct coverage

| Submitted constructor | Declaration/rules |
|---|---|
| `Module`, `FuncDef` | `semantic.k:7,25,76,81-86` |
| `Assign`, `AugAssign` | `semantic.k:26-27,88-92` |
| `For` over a string | `semantic.k:28,110-155` |
| Exact vowel-membership `If` | `semantic.k:29,94-108` |
| `Return` | `semantic.k:30,157-159` |
| `Name`, `Str`, `Int`, `BinOp` | `semantic.k:17-20,168-173,181-182` |
| `Compare(...,"in",...)` | `semantic.k:21,174-175,183-184` |
| `ord`, `chr`, `.swapcase()` calls | `semantic.k:22-23,176-187` |

The four-cell configuration is sufficient for this exact one-function,
stateful path. No heap, allocation, I/O, exception, or nested call stack is
used. Head-before-tail statement scheduling is correct; expression operations
are pure, so their functional evaluation creates no observable evaluation
order difference here. Closure capture, return unwinding, and exception
behavior are incomplete for general Python but are not exercised by this body:
the function has no globals or nested calls and `Return` is last.

The vowel cases and their `[owise]` alternative are disjoint. Empty/nonempty
loop guards are disjoint. The generic loop step binds the first character,
executes the real body, and recurs. Map lookup-after-update, string identity,
and string associativity simplifications are valid. `encodeSpec` has disjoint,
covering length guards and decreases string length. The local base rules are
otherwise adequate for the used English-letter path.

### Unsound operational bridge

`semantic.k:120-146` is not an ordinary language rule. It is a
`[priority(40)]` operational bridge matching the exact submitted loop body.
For each nonempty iteration it skips:

- vowel guard execution;
- assignment to `char`;
- `ord`, integer addition, and `chr`;
- `.swapcase()`; and
- accumulator `AugAssign`.

It directly writes:

```text
result := result + encodedChar(first)
char   := advancedVowel(first)
```

In the abstract definition used to prove `SPEC.encode-loop-correct`,
`encodedChar`, `advancedVowel`, and `swapCaseChar` are declared total functions
but have no equations. `encodedChar` is result-bearing, and the postcondition's
`encodeSpec` is defined with that same symbol. There is no bridge-free
connection theorem showing that the displaced body produces
`encodedChar(first)`. Sharing the symbol between execution and postcondition is
circular.

The required false-conclusion witness is concrete and reproducible:

```text
encodedChar(_)  = "!"
advancedVowel(C) = C
swapCaseChar(C)  = C
input             = "a"
```

This is a legal interpretation of the otherwise equation-free total functions
in the abstract proof theory. Under the bridge, the submitted full constructor
program returns `"!"` (`evidence/05_bridge_opposite_fused.log`). With only the
fused rule removed, under the same interpretation, the fixed generic rules
execute the real body:

```text
"a" is a vowel
chr(ord("a") + 2) = "c"
swapCaseChar("c") = "c"
```

and return `"c"` (`evidence/05_bridge_opposite_bridgefree.log`). Thus the
bridge enables the false conclusion `"!"` on the intended input `"a"`.
Reviewer sources are preserved as `evidence/05_opposite.k`,
`05_opposite-verification.k`, and `05_remove_fused_bridge.diff`.

Removing the bridge and rerunning the submitted universal proof produces a
genuine stuck implication whose residual requires
`encodedChar(first) == swapCaseChar(first)` on a nonvowel branch
(`evidence/05_bridgefree_positive_residual.log`). Even importing the concrete
equations does not supply a machine-checked universal connection proof;
`05_bridgefree_concrete_loop.log` remains stuck on the corresponding symbolic
equivalence.

`concrete.k` does define
`encodedChar(C) = swapCaseChar(advancedVowel(C))`, and ground
bridge-enabled/bridge-free execution agrees for `"aA bB"`. This supports the
finite concrete runs only. It does not retroactively justify the abstract
universal `#Top`, because `SPEC` is proved against `verification-kompiled`
without those evaluators.

The concrete `swapCaseChar` rule implements ASCII casing rather than Python's
full Unicode casing. `evidence/05_unicode_semantics_witness.log` supplies the
specific rule-level witness `"é"`: Python returns `"É"` while the generated K
semantics returns `"é"`. Given the prompt's explicit English-alphabet language,
this is recorded as an excluded-model limitation rather than relied upon for
the verdict. No other rule is labeled unsound without a witness.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; none was trusted or reused.

The fresh mutation in `evidence/06_spec_vacuity.k` preserves the satisfiable
entry precondition for `"test"` but changes the required return value from the
true `"TGST"` to the false `"TGSS"`. Both trusted canonical and submitted
Python return `"TGST"`.

Command:

```text
kprove spec-vacuity-audit.k \
  --definition concrete-verification-kompiled \
  --spec-module CONCRETE-SPEC-VACUITY-AUDIT \
  --claims CONCRETE-SPEC-VACUITY-AUDIT.false-example-test
```

The spec parsed and built, then `kprove` exited 1 with
`WarnStuckClaimState`. The residual final configuration contains
`result = "TGST"` and cannot unify with `"TGSS"`. Full bounded output and exit
status are in `evidence/06_vacuity_proof.log`.

This passes the result-constraint/non-vacuity check for the concrete entry
claim. It cannot repair the missing universal entry theorem or the circular
abstract bridge.

## 7. Proven versus assumed accounting

### What the successful K runs actually establish

Conditioned on the submitted theory:

1. For arbitrary K string `S`, the *fused abstract* `loopString` operation
   appends the recursively defined `encodeSpec(S)` to `R`, where both execution
   and specification use the same unconstrained `encodedChar`.
2. The exact submitted constructor program returns the asserted outputs on
   precisely three fixed messages under the concrete ASCII helper equations.

They do not establish partial correctness of `encode` for every
source-contract message.

### Trust ledger

| Boundary | Influence | Assessment |
|---|---|---|
| Trusted prompt, canonical, and translator mounts | Contract, oracle, program constructor identity | Acceptable; hashes and byte identity checked |
| K v7.1.293 builtin `String`, `Int`, `Bool`, `Map`, `lengthString`, `substrString`, `findString`, `ordChar`, `chrChar`, and arithmetic/string hooks | All parsing and execution | Ordinary low-level toolchain trust |
| `encodeProgram`/`encodeBody`/`encodeLoopBody` constructor functions | Which program/body claims execute | Mechanically pinned to trusted-regenerated `solution.mpy` |
| `swapCaseChar`, `advancedVowel`, `encodedChar` in the abstract definition | Branch-independent character state and final result | Illegitimate for the universal proof: opaque, result-bearing, and unconnected |
| Fused loop rule `semantic.k:120-146` | Skips all material operations in each loop iteration | Illegitimate operational bridge; false conclusion witness recorded |
| `concrete.k` character equations | Three ground proofs and `krun` | Correct for one-character English ASCII; finite evidence does not prove the universal bridge |
| Differential Python test | Candidate/canonical implementation bridge on 18,134 inputs | Strong finite evidence only, not a K theorem |
| Manual reading that the three fixed outputs are representative | Contract coverage | Unacceptable substitute for an unrestricted reachability claim |

### Gate accounting and decision

- Real-program soundness (Gate A): **FAIL**. The only universal result
  computation uses an unproved, falsifiable operational oracle bridge. The
  false-postcondition check passes, but A1-A4 do not.
- Intent adequacy (Gate B): **FAIL**. There is no symbolic entry-point theorem;
  three fixed strings materially narrow an arbitrary-length contract.
- Evidence auditability (Gate C): generation and reviewer evidence are
  reproducible, but they cannot validate the failed theory or missing theorem.

Fresh `#Top` results, constructor pinning, Python differential agreement, and a
successful non-vacuity probe are therefore insufficient. The benchmark mapping
requires a materially bounded HumanEval proof and a result-bearing unsound
semantics bridge to be classified `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
