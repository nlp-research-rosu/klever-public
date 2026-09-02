# Independent adversarial audit: 156-int-to-mini-roman

The submitted Python implementation is correct on the stated finite domain, its
translation is faithful, and every submitted positive K claim reconstructs to
`#Top`. The proof is nevertheless not legitimate. Four priority-40 rules in
`/candidate/verification.k:191`, `:209`, `:230`, and `:251` replace real helper
calls without checking which helper binding was selected and without a
connection theorem covering their accepted context. Fresh machine-checked
witnesses show that each rule proves a false numeral result when the selected
helper is a real closure returning `"z"`. Fixed supplied semantics returns
`"z"` and rejects those false conclusions.

All candidate and launcher mounts remained read-only. Candidate-built
definitions and caches were not used. Source-only builds and mutations were
made below `/tmp/audit-work`; reviewer artifacts and bounded logs are under
`/audit-output/evidence`. Exact commands and statuses are collected in
`/audit-output/evidence/COMMANDS.md`.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem
`156-int-to-mini-roman`, and condition `semantics`. The required trusted
`/reference/reference-semantics` tree is present, so the mount agrees with the
rendered mode.

I read and checked:

- `/audit-campaign-lock.json`, `/run.json`, `/task.json`, and
  `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured JSONL trace under `/generation-evidence/codex-trace/`.

Every launcher-required record is a readable regular file and matches its
recorded SHA-256. The campaign-lock JSON exactly equals the `audit_campaign`
block in `/audit-input.json`, and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The structured trace contains one regular JSONL file; all 739 records parse.
The trace and generation prose were treated only as untrusted construction
claims. Their bounded structural summary is
`evidence/stage1-generation-inspection.log`.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A recursive entry-by-entry
comparison of the candidate and trusted supplied-semantics trees found exactly
24 files and one subdirectory on each side, with identical per-file digests,
types, and paths and no symlinks. There are no missing, additional, changed, or
mistyped semantics entries. All five required candidate proof artifacts are
present as regular files. See `evidence/integrity_check.py` and
`evidence/stage1-integrity.log` (`failure_count=0`).

There is no infrastructure breach. Candidate-provided compiled directories
exist, but they were ignored.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py:2` requires
`int_to_mini_roman(number)` to return the lowercase Roman-numeral representation
of an integer with `1 <= number <= 1000`. The documented results are
`19 -> "xix"`, `152 -> "clii"`, and `426 -> "cdxxvi"`.
`/reference/canonical.py:17` implements the standard descending-value algorithm
with subtractive symbols.

`/candidate/solution.py` uses a different but valid decimal-place-table
algorithm. Its four tables cover thousands digits 0–1 and hundreds, tens, and
ones digits 0–9. On the contract domain, every subscript is in bounds and all
output is already lowercase.

The trusted translator regenerated `/candidate/solution.mpy` byte-for-byte:
both submitted and regenerated files have SHA-256
`cd9c3c57f287e6b88bcab11024b63b51c22c2857d1b78f4418365ff56a69bbd7`
(`evidence/stage2-translation.log`).

The independent differential test imports the trusted canonical and scratch
copy of the generated candidate. It checks the three examples, numeral branch
landmarks around 4/5, 9/10, 40/50/90, 100/400/500/900, both contract
boundaries, and exhaustively every integer 1 through 1000. It also checks zero
as the natural empty-result edge immediately outside the positive domain; the
integer contract has no container-like empty input. There were zero mismatches
over all 1,000 in-domain inputs. The complete result-table digest is
`cd2c90e0b5e4b37f04abaead85ff5ca3e6f97ca72eee551e58d9b6f8528bcd2d`.
See `evidence/differential_test.py` and
`evidence/stage2-differential.log`.

Thus there is no candidate-versus-canonical implementation divergence.

## 3. Clean proof reconstruction

Only these sources were copied into scratch: the five candidate deliverables,
the trusted translator/canonical/prompt, and a fresh copy of the trusted
supplied semantics. No candidate definition or cache was copied or referenced.
The live toolchain is K v7.1.293.

Fresh builds all exited zero:

| Definition | Source and mode | Log |
|---|---|---|
| `fresh-runtime-kompiled` | supplied semantics, LLVM, `MPY-KRUN` | `evidence/stage3-kompile-runtime.log` |
| `fresh-lemma-kompiled` | `verification.k`, Haskell, `ROMAN-BASE` | `evidence/stage3-kompile-lemma.log` |
| `fresh-verification-kompiled` | `verification.k`, Haskell, `ROMAN-VERIFICATION` | `evidence/stage3-kompile-verification.log` |

The fresh LLVM definition executed eight normal, subtractive, mixed-place, and
boundary assertions with exit zero (`evidence/k_semantics_smoke.py`; the
`--output none` run has an intentionally empty
`evidence/stage3-krun-smoke.log`).

The submitted aggregate proof commands independently reconstructed:

- `ROMAN-LEMMA-SPEC`: exit 0 and `#Top`;
- `ROMAN-SPEC`: exit 0 and `#Top`.

I then selected and ran each positive claim separately. The four helper claims,
four index-range claims, and `romanCorrect` all independently exited zero and
printed `#Top`. Exact commands/statuses are in
`evidence/stage3-individual-claims-summary.log`; complete per-claim outputs are
`evidence/stage3-claim-*.log`.

This stage establishes genuine closure under the submitted theory. It does not
establish that every rule in that theory is sound.

## 4. Adequacy and real-program pinning

### Claim meanings

The four helper claims in `/candidate/spec.k:6-92` say that, for legal decimal
digits, executing the corresponding real helper closure returns the appropriate
code-sequence table entry. The helper domains are 0–1 for thousands and 0–9
for the other places.

The four range claims in `/candidate/spec.k:94-108` say that each arithmetic
index expression lies in its helper table's legal digit range whenever
`1 <= N <= 1000`.

The entry claim at `/candidate/spec.k:114-142` says that, for every integer
`N` in exactly the source-contract domain, calling
`int_to_mini_roman(N)` from the stated closure environment terminates at
`str(romanSpec(N))`. `romanSpec` is the concatenation of the four lowercase
digit encodings. The returned value is exact; it is neither a free variable,
tautology, nor one-way implication.

### Mechanical program identity

The entry claim does not replay module loading, but it binds all five function
names to closure parameters and bodies. This is acceptable only if those
constructor bodies are exactly the submitted translated program. The
reviewer script parses balanced constructor terms from `solution.mpy`, extracts
the five proof-local body definitions, tokenizes both sides, and checks the
claim's exact name/parameter/body/parent bindings. All five comparisons are
identical, there are no extra or missing translated functions, and the entry
claim contains exactly one symbolic call to the required entry point. See
`evidence/program_term_compare.py` and
`evidence/stage4-program-term-comparison.log`.

A satisfying entry state exists; for example, `N=1` satisfies the precondition
in the fully specified configuration. The K digit equations were parsed and
grounded for all 1,000 satisfying inputs. Their postcondition agrees with both
Python implementations in every case. Representative substitutions include
`1 -> "i"`, `19 -> "xix"`, `152 -> "clii"`,
`426 -> "cdxxvi"`, `944 -> "cmxliv"`, and
`1000 -> "m"` (`evidence/claim_witnesses.py` and
`evidence/stage4-ground-witnesses.log`).

Constructor identity therefore passes. Semantic body sensitivity does not.
`evidence/entry_body_sensitivity.k` changes the actual `_roman_ones` closure
body bound in the entry configuration to `return "z"` and tests `N=1`.
With the bridge-enabled definition, the original `"i"` postcondition still
proves `#Top` (exit 0). With bridge-free `ROMAN-BASE`, the same claim exits 1
with `WarnStuckClaimState` and a final `str(iCons(122, .IntSeq))`, namely
`"z"`. The bridge-enabled entry proof is therefore insensitive to a material
program-body change it is supposed to execute.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule-inventory.tsv` inventories every local sentence in the 24
supplied-semantics files, `verification.k`, and `spec.k`, including normalized
full text, source line, module, attributes, classification, and static
disposition. Its SHA-256 is
`dcf40e4ed611d991b792291eb42496bdc3ad9c7188a6f6087b8ac5e5775823dd`.
The inventory contains:

- 1 configuration, 233 syntax declarations, 5 contexts, 755 rules, and 9
  claims: 1,003 records total;
- 148 function declarations, 107 `total` declarations, 25 `symbol`
  declarations, 22 `no-evaluators` declarations, 49 priority attributes, 67
  concrete equations, and 26 `owise` rules;
- no local `functional` declaration and no simplification rule.

The unchanged supplied semantics contributes 928 records and is the selected
semantics baseline. I checked its used path in detail; unused constructs and
their opaque primitives do not contribute to these claims. The candidate adds
six proof-local syntax declarations, 60 rules, and nine claims. Inventory
generation, cross-count checks, and disposition totals are in
`evidence/build_rule_inventory.py` and
`evidence/stage5-rule-inventory-summary.log`.

### Used-construct coverage

Every material constructor in `solution.mpy` has a declaration and an execution
route:

| Program construct | Selected semantics route |
|---|---|
| `Module`, `FuncDef`, `Params`, statement sequence | `syntax.k:53-61`, `core.k:124-127`, `functions.k:14-16` |
| `Call`, `Name`, closure dispatch | `syntax.k:12,28`, `core.k:130-154`, `call.k:18-21,69-75` |
| `Return` and frame restoration | `syntax.k:50`, `functions.k:78-90` |
| `Int`, `BinOp`, `%`, `//` | `syntax.k:9,15`, `core.k:194`, `operators.k:12`, `int.k:15-20` |
| `TupleExpr`, `Subscript` | `syntax.k:21-22`, `tuple.k:14-16`, `subscript.k:11-41` |
| `Str` and string `+` | `syntax.k:13`, `str.k:13-24` |

`BinOp` is `seqstrict(2,3)` and argument lists use the shared left-to-right
`#evalArgs` loop, so the fixed semantics defines evaluation order. Calls push a
frame, bind parameters, execute the body, return, pop the frame, and restore
environment/stack/scope state. Tuple creation and indexing are concrete on the
finite helper cases. Python and K integers agree on 1–1000; all strings are
ASCII, inside the selected string model.

The supplied semantics contains named symbolic trust boundaries for floats,
sorting, MD5, and total-but-underspecified out-of-bounds `valSeqAt`. None lies
on the target proof path: there are no floats, sorting, or hashes, and helper
case-splitting makes every tuple index ground and in bounds.

### Proof-local rules other than the bridges

The five body functions at `/candidate/verification.k:15-70` are exact
constructor definitions of the translated bodies. The 32 digit equations at
`:79-113` are pairwise disjoint, truthful codepoint encodings and cover every
digit used by the claims. The four index equations at `:120-130` implement
decimal-place extraction, and `romanSpec` at `:135-142` truthfully concatenates
the four encodings.

The ten `#helperCase` rules at `:148-157` are disjoint constructor cases for a
proof-driver symbol. The four `#check*` rules at `:166-180` rewrite to `true`
only under the stated range guard. Their accompanying claims prove those
guards from the entry domain. None of these functions has an overlapping
false equation or unconstrained result on a claim-reachable use.

### Rejected operational bridges and false witnesses

The four rules at `/candidate/verification.k:191-267` match a source-level
helper call inside any scope containing `"number" |-> N`, then directly
replace it by the table result computed from `N`. Each is an operational
bridge, not a derived lemma:

- it does not look up the helper name or require the exact submitted closure
  binding/body;
- `_M:Map` admits a local binding of the helper name, and the parent is
  unconstrained;
- `...` admits an arbitrary continuation and omitted stack, heap, return,
  exception, and allocation state;
- it skips callee and argument evaluation, parameter binding, frame
  allocation, body execution, return, and pop;
- `[priority(40)]` makes it preempt the supplied generic `Call` route.

The separately proved helper claims do not justify this match domain. They
start from exact top-level configurations with `env=0`, an exact helper
binding, empty stack/heap, and their own continuation. They do not prove
equivalence for arbitrary bindings, caller frames, continuations, or omitted
cells. No bridge-free universal connection theorem covers every state the
four rules accept.

`evidence/bridge_rule_witnesses.k` supplies a false conclusion for every
rejected rule:

| Bridge | Satisfying `number` | Bridge-fabricated result | Fixed selected binding/result |
|---|---:|---|---|
| thousands, `:191` | 1000 | `"m"` | closure `return "z"` gives `"z"` |
| hundreds, `:209` | 100 | `"c"` | closure `return "z"` gives `"z"` |
| tens, `:230` | 10 | `"x"` | closure `return "z"` gives `"z"` |
| ones, `:251` | 1 | `"i"` | closure `return "z"` gives `"z"` |

All witnesses use integers in the intended input domain. Under
`ROMAN-VERIFICATION`, the four false numeral claims collectively print `#Top`
and exit 0 (`evidence/stage5-bridge-false-closes.log`). Under bridge-free
`ROMAN-BASE`, the four correct `"z"` claims print `#Top`
(`evidence/stage5-base-correct-closes.log`), while each false numeral claim
independently exits 1 with `WarnStuckClaimState`. Every residual visibly ends
at codepoint 122 (`"z"`); see
`evidence/stage5-base-false-summary.log` and the four full
`stage5-base-false-*.log` files.

These are concrete false conclusions enabled by each rule, not merely missing
evidence. The rules also use the same digit functions that form the final
postcondition. Although the base helper claims connect the original helper
bodies to those digits in one exact context, they do not establish the
bridges' broader operational domain. The four bridges therefore smuggle the
task-specific result past real call execution and fail the mandatory
real-program soundness gate.

## 6. Fresh non-vacuity test

No candidate mutation was trusted. The fresh mutation in
`evidence/spec-vacuity.k` keeps the exact entry state and precondition but
requires the genuine Roman result followed by an extra lowercase `"x"`. It is
demonstrably false at the satisfying input `N=1`: the program returns `"i"`
and the mutation requires `"ix"`.

The `--dry-run` command exits 0, establishing that the mutation parses and
builds (`evidence/stage6-vacuity-build.log`). The actual proof exits 1 with
`WarnStuckClaimState`; its residual explicitly contains the failed equality
between `romanSpec(N)` and `seqConcat(romanSpec(N), iCons(120, .IntSeq))`
(`evidence/stage6-vacuity-proof.log`). This is an expected unmet result
obligation, not a parser error, timeout, unrelated crash, or unreachable
mutation.

The submitted entry claim is therefore result-constraining and non-vacuous
under its theory. Non-vacuity does not make the theory's false operational
bridges sound.

## 7. Proven versus assumed accounting

The successful reconstructed proof establishes the following conditional
statement: in `ROMAN-VERIFICATION`, which includes the four helper-call bridge
axioms, every initial entry configuration with `1 <= N <= 1000` reaches
`str(romanSpec(N))`. Separately, `ROMAN-BASE` proves each original table helper
from an exact top-level invocation context and proves the four arithmetic
index bounds.

It does not establish that fixed supplied semantics executes the real entry
program to that result, because the entry proof relies on four globally false
rules that bypass its helper calls.

Trust and evidence ledger:

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.293 frontend, Haskell/LLVM backends, KORE prover, and builtin integer/map/string theories | Parsing, execution, and proof closure | Ordinary low-level trusted computing base; acceptable |
| Unmodified supplied MPY semantics | Binding, evaluation order, calls/returns, state, and primitive operations | Selected semantics boundary; integrity verified and used path reviewed |
| Supplied symbolic float/sort/MD5 and underspecified out-of-bounds symbols | Potential abstract values in other programs | Explicit fixed-semantics trust boundary, but unused by this proof |
| Trusted `py2mpy.py` | Python-AST to constructor bridge | Acceptable here: trusted mount and byte-identical regeneration |
| Proof-local body and digit/index/spec equations | Program identity and intended result | Exact or truthful on the formal domain; grounded and independently checked |
| Four priority helper-call bridges | Final value, helper binding, evaluation, call control, and state footprint | Illegitimate: false-witness claims close |
| Exhaustive CPython differential test | Candidate-versus-canonical behavior for all 1,000 allowed integers | Strong finite-domain implementation evidence; not a replacement for K execution soundness |
| Constructor and ground-witness scripts | Source-to-claim identity and concrete postcondition checks | Reproducible audit evidence; not a universal bridge theorem |

The formal domain exactly matches the source contract and the stated
postcondition matches the requested lowercase Roman representation, so there is
no domain-narrowing defect. The candidate program itself is correct. The
failure is Gate A real-program soundness: the theory can and does prove false
results for helper calls and remains `#Top` after a material helper-body
mutation. Under the benchmark decision boundary, materially unsound
proof-specific rules require `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
