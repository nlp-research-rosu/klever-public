# Independent adversarial audit: 125-split-words

The candidate is **not a legitimate proof**. Fresh reconstruction does make the
three submitted claims print `#Top`, and the claims are result-constraining and
mechanically pinned to the submitted translated function body. However,
`verification.k` adds five priority-35 operational rules that ignore the
evaluated branch Boolean and instead use a proof-only `$proofPath` scope
binding to choose control flow. Those rules are false axioms over their match
domains. The candidate theory proves five exact opposite-Boolean conclusions
that the fixed supplied semantics rejects, and it proves three false results
for concrete executions of the submitted closure. In addition, `solution.py`
materially disagrees with the trusted canonical implementation on the
unrestricted source-contract domain.

## 1. Input and provenance integrity

### Launcher and campaign records

`/audit-input.json` is readable and declares:

- `record_layout = legacy-selected-stage1`
- `condition = semantics`
- `semantics_mode = SUPPLIED_SEMANTICS`
- `problem_id = 125-split-words`
- a complete provenance status

The trusted `/reference/reference-semantics` mount is present, so the mount
agrees with the rendered semantics mode. `/audit-campaign-lock.json` is
structurally identical to the `audit_campaign` block in `/audit-input.json`.
Its recomputed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
exactly the value recorded by the launcher.

All records required for `legacy-selected-stage1` are present, regular,
readable files: `/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the JSONL trace. Historical
`runtime-metrics.json` is absent, which is explicitly permitted for this
layout. The legacy records say the original generation succeeded, but I used
that only as an untrusted claim.

I independently recomputed the single-file hashes. They match the launcher
values, including:

- canonical: `6f758b9346cb3be14b584c0436117e484b6e7b6c41bda7ee2713740fffd6b30f`
- prompt: `c9ac5a400f5388b93fcc2acc0fa2adf0237e9f1802cebec7f375644658bd9aa0`
- translator: `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`
- run: `321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0`
- task: `d56f55951227a18ebb0149f47ceab60b52e603b96004c6fd2f5bb318c4200911`
- generation result: `fe0a6849692d737448752f0d9b2c85499e3432ea93176a767d2a9693b105dbd8`
- invocation: `5d83160f5a915b8a5a3da856d87a3b72d546bb82c5bea4de60b25227f1d22a68`
- generation metrics: `518e1a2c0e2227ab50340a49ae0cc06d405294e33e938d8a1a3f0ba11728a398`
- usage: `5bd89df3854e461153f420fddb8855be03adde6718cf84a4f1ad5dd2979fa292`
- trace file: `d0e4f49ed654ef89b0271ffcfe0141eb1a3abaef6b7a8c8ff32effdb940f714e`

The 383-line structured trace parses completely. It contains 81 tool calls and
records the evolution from fixed-semantics residuals to the `$proofPath`
rules. The 27,525-line output log and all other generation records were read
and hashed; their prior `#Top` and final report were not treated as proof.

Evidence:

- [integrity commands and hashes](evidence/01_integrity.sh) and
  [bounded log](evidence/01_integrity.log)
- [generation-record parser](evidence/01_generation_records.py) and
  [parsed summary](evidence/01_generation_records.log)

### Candidate/trusted-input comparison

`cmp` gives exit 0 for candidate versus trusted `prompt.py` and `py2mpy.py`.
`diff -qr --no-dereference` gives exit 0 for
`/candidate/reference-semantics` versus
`/reference/reference-semantics`. Neither tree contains a symlink, and the
file/type inventory finds no missing, extra, or mistyped semantics entry. An
independent sorted per-file candidate hash manifest has SHA-256
`1a7fe1a5332288e9c64b8e2ed28deb9cab7e3f81bf3b91697ee582983d402544`.

The required proof artifacts—`solution.py`, `solution.mpy`, `verification.k`,
`spec.k`, and `prove.sh`—are present as regular files. Candidate compiled
artifacts, logs, Python bytecode, and `kore-exec.tar.gz` were ignored.

There is no infrastructure breach, so a candidate verdict is appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The prompt asks for `split_words(txt)` on strings. Reading the trusted
canonical implementation makes the operational contract precise for the
unrestricted Python `str` domain:

1. If the literal space `" "` occurs, return `txt.split()`.
2. Otherwise, if `","` occurs, return
   `txt.replace(",", " ").split()`, which drops leading/trailing empty fields
   and collapses repeated commas as whitespace.
3. Otherwise, count characters for which `islower()` is true and the Unicode
   code point is even. For ASCII `a` through `z`, these are
   `b,d,f,h,j,l,n,p,r,t,v,x,z`.

The candidate instead:

1. selects the first branch when any of space, tab, newline, or carriage return
   occurs;
2. uses `txt.split(",")`, preserving empty comma fields; and
3. counts only the 13 hard-coded ASCII letters.

These are material differences, not merely a different algorithm.

### Trusted regeneration

Running the trusted copied translator on copied `solution.py` produced
`regenerated-solution.mpy`. `cmp` returned 0 and both files have SHA-256
`0893ed55c993d253598f623b2cda9937139d072dfdab2dcd58fb4eeb791fb218`.
Thus the submitted `solution.mpy` faithfully translates the submitted Python.

### Independent differential test

The independent test imports copied trusted canonical and candidate modules
under distinct module names. It covers all three examples, empty inputs,
leading/trailing/repeated delimiters, every candidate branch boundary,
Unicode lowercase boundaries, every string of length 0 through 4 over
`a,b,c,SPACE,COMMA,TAB,LF,CR,VT,FF`, and 4,000 deterministic generated
strings. Among 14,967 unique inputs it found 8,156 mismatches.

Representative divergences:

| Input | Trusted canonical | Candidate |
|---|---|---|
| `","` | `[]` | `["", ""]` |
| `"a,,b"` | `["a", "b"]` | `["a", "", "b"]` |
| `"a\tb"` | `1` | `["a", "b"]` |
| `"à"` (U+00E0) | `1` | `0` |
| `"β"` (U+03B2) | `1` | `0` |

This is an independent implementation/specification failure on the intended
domain. Evidence: [differential source](evidence/02_differential.py),
[fidelity commands](evidence/02_program_fidelity.sh), and
[results](evidence/02_program_fidelity.log).

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/125-split-words`; no
candidate definition or cache was copied. The available tools are K
v7.1.293. Fresh commands and results were:

| Command | Result |
|---|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition audit-runtime-kompiled` | exit 0 |
| `krun solution.mpy --definition audit-runtime-kompiled` | exit 0, `.K`, `NoExc` |
| reviewer ground assertion program under that definition | exit 0, `NoExc` |
| `kompile verification.k --backend haskell --main-module SPLIT-WORDS-VERIFICATION --syntax-module MPY-SYNTAX --output-definition audit-verification-kompiled` | exit 0 |
| all three claims together | `#Top`, exit 0 |
| `--claims SPEC.whitespace` | `#Top`, exit 0 |
| `--claims SPEC.comma` | `#Top`, exit 0 |
| `--claims SPEC.odd-lowercase-count` | `#Top`, exit 0 |

The first reconstruction log also contains three exploratory filtering calls
using bare labels; K rejected those labels with exit 113. They are command-line
selection errors, not proof attempts. The corrected fully-qualified calls
above are recorded separately and all close.

Evidence:

- [clean build/proof commands](evidence/03_clean_rebuild.sh) and
  [log](evidence/03_clean_rebuild.log)
- [correct individual-claim commands](evidence/03_individual_claims.sh) and
  [log](evidence/03_individual_claims.log)
- [ground execution commands](evidence/09_ground_and_semantic_boundary.sh) and
  [log](evidence/09_ground_and_semantic_boundary.log)

This stage establishes only closure under the candidate’s extended theory.
Stage 5 shows why that theory is not sound.

## 4. Adequacy and real-program pinning

### Plain-language reading of the claims

All claims call `solutionClosure` on `str(CS)` from a clean module environment
plus a proof-only `$proofPath` binding. They require an empty call stack,
`noRet`, and `NoExc`.

- `whitespace`: when the sum of occurrences of code points 32, 9, 10, and 13
  is positive, return heap reference 0; allocate at 0 a list equal to
  `splitWS(CS, .IntSeq, .ValSeq)`; advance `heapLoc` to 1.
- `comma`: when that whitespace count is zero and comma count is positive,
  return heap reference 0; allocate `splitSep(CS, 44, .IntSeq)` at 0; advance
  `heapLoc` to 1. This deliberately preserves empty fields.
- `odd-lowercase-count`: when both delimiter counts are zero, return the sum
  of occurrence counts of the 13 hard-coded ASCII letters.

The result and heap are constrained; these are not tautological claims.

### Satisfiable entry states and ground substitution

| Claim | Satisfying `CS` | Candidate result | Canonical result |
|---|---|---|---|
| whitespace | `"Hello world!"` (whitespace count 1) | `["Hello", "world!"]` | same |
| comma | `","` (whitespace 0, comma 1) | `["", ""]` | `[]` |
| odd count | `""` (both counts 0) | `0` | `0` |

The ground witness program executes successfully under fresh LLVM semantics.
The comma witness also directly exhibits the formal theorem’s disagreement
with the trusted source contract. Evidence:
[witness evaluator](evidence/09_claim_witnesses.py) and
[ground log](evidence/09_ground_and_semantic_boundary.log).

### Mechanical pinning

The entry claims do not load the whole `Module(...)`; they call a direct
closure. That is acceptable only if the closure is mechanically the submitted
function. I generated a K spec by extracting the sole `split_words` body from
the regenerated `solution.mpy`, normalizing only the translator’s printed
empty collection slots to the parser-equivalent `.Exprs` and `.Stmts`.
`kprove` then proved both:

- `solutionBody` is exactly the extracted constructor body; and
- `solutionClosure` is exactly `closureVal("txt", extractedBody, 0)`.

The pinning spec printed `#Top`, exit 0. A separate mutation changed the
executed body’s final `txt.count("z")` to `txt.count("a")`; the original
odd-count obligation then built successfully but became a genuine stuck claim
and exited 1. This changes the K term actually executed by the claim, so it is
a valid body-sensitivity test.

Evidence:

- [pinning generator](evidence/04_generate_pinning.py),
  [commands](evidence/04_pinning.sh), and [log](evidence/04_pinning.log)
- [body-mutation generator](evidence/07_generate_body_mutation.py),
  [commands](evidence/07_body_sensitivity.sh), and
  [stuck residual](evidence/07_body_sensitivity.log)

There is no automatic source-to-proof regeneration in the candidate; that is
an artifact-maintenance limitation, not the decisive failure for this
immutable submission.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The reviewer-generated inventory enumerates the full text and line range of
every `requires`, module/import, configuration, syntax declaration, context,
rule, and claim in the supplied `semantics.k`, all 23 component K files,
`verification.k`, and `spec.k`. Across the imported source it records:

- 27 modules and one configuration;
- 232 syntax declarations;
- 705 rules and 3 claims;
- 150 function declarations, including 107 marked `total` and 43 unmarked
  partial/opaque declarations;
- 50 priority-bearing rules, 26 `owise` rules, and 5 contexts;
- no `[functional]` declarations and no simplification rules.

The complete inventory is
[08_rule_inventory.txt](evidence/08_rule_inventory.txt), generated by
[08_inventory.py](evidence/08_inventory.py). It is the exhaustive record;
the discussion below isolates the rules reachable from this program and every
candidate-local extension.

### Used-construct map

| Submitted construct | Fixed declaration and rule path | Assessment |
|---|---|---|
| `FuncDef`, direct closure call, parameter binding, `Return` | `syntax.k`; `call.k` frame allocation; `functions.k` bind/return/pop | Correctly preserves environment, stack, returned value, and callee-frame deallocation for this one-parameter function |
| `Assign(Name(...), ...)`, `Name(...)` | strict RHS plus `controls.k` assignment and `core.k` lookup | Correct current-scope write and lookup on this path |
| `BinOp("+",...)` | sequential strictness, `operators.k`, `int.k` | Left-to-right evaluation and integer addition are represented |
| `Compare(..., ">", 0)`, `If` | contexts/strictness, integer comparison, `controls.k` `truthy` and fixed `#branch` rules | Fixed rules are Boolean-sensitive; candidate priority rules unsoundly preempt them |
| `Attribute`, `Call`, `str.count` | `call.k` callee/argument evaluation and `methods.k` `applyMethod`/`cntSub` | Fixed, recursively defined occurrence count; symbolically opaque because not marked total, but ground equations are value-defining |
| no-argument `split` | `methods.k` `#applyK`, allocation, `splitWS`, `flushTok`, `isWSC` | Faithful to the supplied four-code whitespace model, but not full CPython whitespace |
| comma `split` | `methods.k` `splitSep` and allocation | Faithful to candidate `str.split(",")`; intentionally keeps empty fields, hence not canonical |
| string/int literals and list result | `str.k`, `core.k`, heap allocation | All submitted literals are ASCII and all material allocations are represented |

All other supplied component modules and their rules are imported but
unreachable from the submitted constructor body. Their declarations remain
enumerated in the exhaustive inventory. No candidate file changes the trusted
semantics tree.

### Candidate-local definitional rules

`verification.k` has five local function symbols and ten rules:

1. `solutionBody` and its one defining equation
   (`/candidate/verification.k:63-124`).
2. `solutionClosure` and its one defining equation (lines 126-127).
3. `whitespaceCount` and its one equation (lines 131-136).
4. `commaCount` and its one equation (lines 138-139).
5. `oddAlphabetCount` and its one equation (lines 143-157).
6. Five operational `#branch` rules (lines 13-58).

The five function equations are definitional summaries, not execution
shortcuts. Their domains are covered by their single equations, their
right-hand sides truthfully mirror the submitted body and supplied
`cntSub`, and they have no pairwise overlaps. They introduce no fresh or
unconstrained result.

### The five operational bridges are unsound

Each bridge has priority 35, lower numerically and therefore preemptive over
the fixed default-priority Boolean rules. Each reads a chosen `$proofPath`
value from scope 0, ignores `_B:Bool`, and rewrites the `<k>` cell while
framing every other cell. They are operational bridges because they replace
the fixed `#branch(true,...) => then` /
`#branch(false,...) => else` behavior.

| Candidate rule | False conclusion witness |
|---|---|
| lines 13-21, path 1 forces no-arg split arm | With `B=false`, it proves `#branch(false, Return(split()), .Stmts) => Return(split())`; fixed semantics produces `.K` |
| lines 22-30, path 2 discards no-arg split arm | With `B=true`, it proves that same branch redex reaches `.K`; fixed semantics selects `Return(split())` |
| lines 31-39, path 3 discards no-arg split arm | Same opposite-Boolean witness with path 3 |
| lines 41-49, path 2 forces comma split arm | With `B=false`, it proves `#branch(false, Return(split(",")), .Stmts) => Return(split(","))`; fixed semantics produces `.K` |
| lines 50-58, path 3 discards comma split arm | With `B=true`, it proves that comma redex reaches `.K`; fixed semantics selects `Return(split(","))` |

All five witness claims close together as `#Top` under the candidate
definition. Each one separately produces `WarnStuckClaimState` and exit 1
under a fresh fixed-semantics definition. Thus every unsoundness finding has
an exact false conclusion witness; it is not an inference from a timeout or
missing proof.

Evidence:

- [five candidate-theory witnesses](evidence/05_bridge_false_witnesses.k)
- [same destinations under fixed semantics](evidence/05_fixed_false_witnesses.k)
- [build/comparison log](evidence/05_bridge_soundness.log)
- [five individual fixed failures](evidence/05_fixed_witnesses_individual.log)

The problem is not merely an over-broad unused rule. Whole-program claims on
the exact `solutionClosure` demonstrate observable false results:

| Concrete input and proof path | Candidate theory proves | Actual bridge-free program |
|---|---|---|
| `""`, path 1 | allocated empty list | integer `0` |
| `" "`, path 2 | list `[" "]` | empty list |
| `","`, path 3 | integer `0` | list `["", ""]` |

All three false whole-program claims print `#Top` under the candidate
extensions; all three stick and exit 1 after the five bridges are removed.
Evidence:
[false whole-program claims](evidence/11_false_program_claims.k),
[bridge-free copies](evidence/11_false_program_claims_no_bridges.k), and
[comparison log](evidence/11_false_program_claims.log).

The bridges also accept an arbitrary continuation via `...`. In the wrong
Boolean case they change abrupt-return behavior: forcing `Return` can pop a
frame and discard the suffix, while deleting a true return can preserve and
execute it. They therefore fail value, continuation, and control-state
fidelity. The scope binding is not a justification theorem, and the claim
preconditions are not guards on the global rules. No bridge-free universal
connection theorem is supplied for any accepted context. The match domains
strictly exceed any domain on which the intended path selection is valid.

As a dependency check, a fresh definition with all five bridges deleted still
proves the whitespace claim, but the comma and odd-count claims both produce
real stuck residuals and exit 1. This confirms that the submitted successful
proof materially relies on the invalid extension:
[bridge-removal generator](evidence/06_generate_no_bridges.py),
[commands](evidence/06_no_bridges.sh), and
[residuals](evidence/06_no_bridges.log).

### Supplied-model boundary

The supplied `isWSC` recognizes only code points 32, 9, 10, and 13. CPython
`str.split()` also treats other Unicode whitespace as separators. On
`"a b\u00a0c"` both Python implementations return `["a", "b", "c"]`, while
the supplied `splitWS` model yields `["a", "b\u00a0c"]`. A ground model claim
for the latter prints `#Top`; the CPython result claim sticks and exits 1.
This is not a candidate modification of supplied semantics, but it is a
material language-model/intent boundary for an unrestricted Python `str`
contract. Evidence:
[semantic-boundary claims](evidence/09_semantic_boundary.k) and
[log](evidence/09_ground_and_semantic_boundary.log).

## 6. Fresh non-vacuity test

The candidate contains no `spec-vacuity.k`; no candidate negative test was
trusted. I created a distinct `SPEC-VACUITY` claim that changes the odd-count
result to `oddAlphabetCount(CS) +Int 1`. `CS = .IntSeq` satisfies both
delimiter preconditions and the actual result is 0, so the mutated
postcondition is demonstrably false.

- Python ground witness: exit 0 and result 0.
- `kprove ... --dry-run`: exit 0, proving the mutation parses/builds.
- actual mutated proof: `WarnStuckClaimState`, unmet result obligation, exit 1.

This is meaningful non-vacuity evidence: the original result obligation is
discriminating. It does not validate the operational rules used to reach that
result.

Evidence:
[fresh mutation](evidence/10_spec_vacuity.k),
[commands](evidence/10_non_vacuity.sh), and
[residual](evidence/10_non_vacuity.log).

## 7. Proven versus assumed accounting

### What the reconstructed `#Top` actually establishes

Conditioned on the supplied MPY theory **plus the five false `$proofPath`
axioms**, K establishes partial-correctness reachability for the exact direct
closure body:

- for symbolic `IntSeq` inputs satisfying each of the three count
  preconditions;
- from an initial scope containing the corresponding path number;
- to the modeled `splitWS`, `splitSep`, or 13-letter count result and the
  stated heap/control cells.

It does not establish that the fixed semantics selects those paths, does not
establish the trusted canonical contract, and does not establish full CPython
string behavior.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, kompiler, Haskell/LLVM backends, SMT, and K builtin Int/Bool/String/Map/List operations | all builds and claims | Normal accepted verification trust boundary; version and fresh outputs recorded |
| Trusted `py2mpy.py` | source-to-`solution.mpy` bridge | Acceptable here: candidate copy is byte-identical and trusted regeneration is byte-identical |
| Supplied reference semantics tree | all program execution | Integrity passes exactly; its four-code whitespace abstraction is nevertheless an explicit model/CPython adequacy limitation |
| Fixed `cntSub` | both branch conditions and all count postconditions | Acceptable fixed-semantics operation: recursive ground equations define non-overlapping occurrence counting; symbolic terms remain opaque because the declaration is not `total` |
| Fixed `splitWS`, `flushTok`, `isWSC` | whitespace result | Defined by recursive equations; acceptable for the named supplied model, limited for full Python whitespace |
| Fixed `splitSep` | comma result | Defined by recursive equations and faithful to candidate `split(",")`; conflicts with the trusted canonical contract |
| `solutionBody`, `solutionClosure`, and three candidate count summaries | all entry claims | Definitional and mechanically/execution-sensitively checked |
| Five priority-35 `$proofPath` rules | target closure of at least comma and odd-count claims; all extended executions that match | **Illegitimate**. They affect control and results, ignore the Boolean, lack connection theorems, and admit machine-checked false conclusions |
| Differential and ground tests | finite source/model bridges only | Reproducible finite evidence, not a universal proof |

The imported supplied theory also declares opaque/no-evaluator primitives
`md5hexCodes`, `sortVS`, `sortKeyVS`, and the float family
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`, `toF`,
`ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. None is reachable from this submitted body or influences any target
claim. Partial dispatch functions for unused builtins, dicts, floats, lists,
ranges, sorting, subscripting, and tuples are likewise exhaustively listed in
the rule inventory and have no target dependency.

### Gate and decision summary

- Gate A, real-program soundness: **FAIL**. Five false operational axioms can
  prove false results for the exact submitted closure.
- Gate B, intent adequacy: **FAIL**. The generated implementation and formal
  comma/branch behavior materially diverge from the trusted canonical
  contract; the supplied whitespace model also excludes Python behavior on
  part of the unrestricted string domain.
- Gate C, evidence auditability: the audit evidence is reproducible and the
  finite evidence is labeled honestly, but it cannot rescue Gates A or B.
- Non-vacuity: **PASS** as a diagnostic only.

A theorem may be true even if a particular proof is invalid, but this
candidate’s successful `#Top` depends on a theory that demonstrably proves
false real-program executions. Under the benchmark decision boundary this is
`FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
