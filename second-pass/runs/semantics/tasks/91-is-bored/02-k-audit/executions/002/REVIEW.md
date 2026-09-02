# Independent adversarial review: 91-is-bored

## Outcome

The candidate's five written claims can be rebuilt and proved, and the
proof-local equations used by those claims are not unsound shortcuts. The
submission nevertheless does **not** contain the required partial-correctness
proof over the HumanEval source-contract domain:

1. The only claims that execute a complete `is_bored` call are the two fixed
   prompt examples. The three universal claims start at a hand-constructed
   internal `#loop` state. There is no universal reachability claim connecting
   an arbitrary call of the submitted function to the state-0 loop theorem.
2. The submitted implementation is not extensionally equal to the trusted
   canonical function on Python's unrestricted `str` domain. Deterministic
   witnesses include leading ASCII whitespace and Unicode whitespace after a
   delimiter.

Thus the written theorems are sound but materially narrower than the requested
theorem. Under the benchmark-specific decision boundary, that is
`FAIL / NOT_LEGIT`, not a nonfatal concern.

## 1. Input and provenance integrity

I first read `/audit-input.json`. It declares:

- problem `91-is-bored`;
- condition `semantics`;
- record layout `legacy-selected-stage1`;
- semantics mode `SUPPLIED_SEMANTICS`;
- a mounted reference-semantics baseline.

The campaign object in `/audit-campaign-lock.json` is structurally identical to
the `audit_campaign` object in `/audit-input.json`, and the lock file's SHA-256
is the declared
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All required records for this legacy-selected-stage1 layout are real readable
files or real directories. `usage.json` is optional for this layout but is
present and was inspected. Historical `runtime-metrics.json` is absent, which
is allowed for this declared legacy layout.

The required generation records were read as untrusted evidence:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, `prompt.txt`, and the JSONL trace. The
complete 3,375,164-byte textual log was read, and all 1,162 trace lines parse as
JSON. The generation record claims success, but that claim was not used as
proof evidence.

Every directly declared file hash matches. The independently reimplemented
pipeline tree hash additionally gives:

| Tree | Observed hash | Independent comparison |
|---|---|---|
| trusted reference semantics | `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f` | matches launcher manifest hash |
| candidate reference semantics | same | recursively identical to trusted tree |
| mounted candidate | `706713753b2dcc729a26757cdead6a8e7c7c8568c003ba0e842f3b81be7a7c23` | matches invocation retained-workspace hash |
| generation trace | `0e45c8aa19718bf5053c0cfb1bcca132dbea37d5c3bbb7df610eebed1d3d49e2` | matches `usage.json` source-trace hash |

`/candidate/prompt.py` and `/candidate/py2mpy.py` are byte-identical to their
trusted mounts. A recursive type-and-content inventory of
`/candidate/reference-semantics` and `/reference/reference-semantics` found no
missing, additional, modified, mistyped, unsupported, or symlinked entries.
The supplied-semantics boundary is therefore intact. There is no audit
infrastructure breach.

Evidence:

- [integrity checker](evidence/integrity_check.py)
- [integrity command and results](evidence/01-integrity.log)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt says to count sentences that start with the word `I`, with
sentences delimited by `.`, `?`, or `!`. The trusted canonical implementation
makes this precise by:

1. applying `re.split(r'[.?!]\s*', S)`;
2. counting split pieces for which `sentence[0:2] == 'I '`.

Consequently, whitespace consumed after a delimiter is Python regex `\s`, while
whitespace at the start of the entire input is not discarded by the canonical
function. The prompt places no finite length, ASCII, or whitespace restriction
on `S`; the intended HumanEval input domain is Python `str`.

The candidate instead uses a three-state character scanner. Its state 0 exists
at function entry and after each delimiter, and it skips only code 32 or codes
9 through 13 in that state. This creates two material differences:

- it discards leading ASCII whitespace at the beginning of the whole input,
  which the canonical function does not;
- it does not discard other Unicode characters matched by Python regex `\s`
  after delimiters.

### Translator fidelity

Fresh translation used the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both files have SHA-256
`c67074e139048d0e105db65f2c5b19123923087e625626990091a610233ea841`;
the command exited 0. Thus the K input faithfully translates the submitted
Python, and the discrepancies below are not translator drift.

Evidence: [regeneration log](evidence/02-regeneration.log).

### Independent differential test

The reviewer-authored differential imports the trusted canonical entry point
and candidate entry point under separate module names. It tests:

- both documented examples;
- empty and minimal strings;
- each delimiter;
- every candidate state-transition boundary;
- ASCII and Unicode whitespace boundaries;
- multiple-sentence cases;
- 1,000 deterministic generated inputs from a documented alphabet and seed.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py
```

The run covered 44 explicit and 1,000 generated cases. It exited 1 after
reporting 14 mismatches. Representative false-result witnesses are:

| Input | Trusted canonical | Candidate |
|---|---:|---:|
| `" I am bored"` | 0 | 1 |
| `"\tI am bored"` | 0 | 1 |
| `".\u00a0I am bored"` | 1 | 0 |
| `".\u2003I am bored"` | 1 | 0 |
| `"  I start here!\tI tab-leading.\n\nI newline-leading"` | 2 | 3 |

The last case is also embedded in the candidate's own concrete test module,
where the noncanonical expected result is 3. These witnesses are ordinary
finite Python strings in the source-contract domain. This is a material
implementation/specification disagreement.

Evidence:

- [differential source and complete input generator](evidence/differential_test.py)
- [differential results](evidence/03-differential.log)

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/fresh`. The semantics copy came from the trusted reference
mount after recursive candidate-versus-reference identity was established.
No candidate-provided compiled definition, archive, cache, or prior log was
copied or used.

The live tools are K `v7.1.293`; `kompile`, `krun`, and `kprove` are installed
independently at `/usr/bin`. Evidence:
[toolchain log](evidence/04-toolchain.log).

### Concrete definition

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This fresh build exited 0. The submitted concrete test source was translated
again, required to be byte-identical to `concrete-tests.mpy`, and executed:

```text
krun regenerated-concrete-tests.mpy --definition runtime-kompiled
```

That exited 0 with final `<k> .K </k>` and exit-code 0. This confirms execution
of the candidate's asserted examples, not agreement with the trusted
canonical.

Evidence:

- [LLVM build log](evidence/05-kompile-concrete.log)
- [fresh concrete execution log](evidence/06-krun-candidate-tests.log)

### Proof definition and every positive claim

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

The fresh Haskell build exited 0. The three loop claims are mutual
circularities: delimiter transitions intentionally move between them, so they
must be enabled as one dependency group. Every written positive claim was
nevertheless run independently at the smallest valid dependency granularity:

| Command | Output | Exit |
|---|---|---:|
| `kprove spec.k --definition verification-kompiled --spec-module SPEC --claims loop-state-0,loop-state-1,loop-state-2` | `#Top` | 0 |
| same, `--claims prompt-example-0` | `#Top` | 0 |
| same, `--claims prompt-example-1` | `#Top` | 0 |
| same, with no `--claims` filter | `#Top` | 0 |

Evidence:

- [Haskell build log](evidence/07-kompile-proof.log)
- [mutual loop proof](evidence/08-kprove-loop-group.log)
- [first entry example](evidence/09-kprove-example-0.log)
- [second entry example](evidence/10-kprove-example-1.log)
- [all submitted claims](evidence/11-kprove-all.log)

The positive reconstruction gate passes. This establishes closure of the five
written claims under the supplied K theory; it does not establish that the
right HumanEval theorem was written.

## 4. Adequacy and real-program pinning

### Plain-language claim inventory

The three helper claims share a well-formed function-frame configuration. The
local count is arbitrary `N`, the remaining iterable is arbitrary `CS`, the
heap is empty, the frame is set to return and unwind, and the global map must
not shadow the builtin `ord`.

| Claim | Precondition in plain language | Postcondition |
|---|---|---|
| `loop-state-0` | execution begins at the candidate loop with scanner state 0 | the returned value is exactly `bored0(CS,N)` |
| `loop-state-1` | same, with scanner state 1 | the returned value is exactly `bored1(CS,N)` |
| `loop-state-2` | same, with scanner state 2 | the returned value is exactly `bored2(CS,N)` |
| `prompt-example-0` | a ground call of the candidate closure on `"Hello world"` | exact integer 0 |
| `prompt-example-1` | a ground call on the prompt's second example | exact integer 1 |

All preconditions are satisfiable. For example, take `GLOBAL=.Map`,
`INPUT=.IntSeq`, `N=0`, `CH=str(.IntSeq)`, and `CODE=0`; the `ord` guard is
true. Concrete helper witnesses respectively use:

- state 0 and remaining `"I am"`, yielding 1;
- state 1 and remaining `" "`, yielding 1;
- state 2 and remaining `".I "`, yielding 1.

The corresponding whole Python strings `"I am"`, `"I "`, and `"x.I "` return
1 from both Python implementations. Both ground example claims also agree with
both implementations. Evidence:
[claim witnesses](evidence/claim_witnesses.py) and
[results](evidence/16-claim-witnesses.log).

### Constructor-level program identity

The verifier does not literally paste `solution.mpy` into `spec.k`; it uses
`boredLoopBody` and `boredFunctionBody`. I parsed both terms using the fresh K
definition, expanded the loop abbreviation mechanically, parsed the freshly
regenerated `solution.mpy`, and compared KAST constructor trees.

Both the loop-body comparison and full function-body comparison are `True`.
The two normalized function bodies share SHA-256
`f8e924f3941d0973b93c162d52fd57bb0ff7b8b09b1baf447d20cb65a50309bb`.
Therefore the two ground entry claims execute exactly the submitted function
body, and the helper claims execute exactly its loop body.

Evidence:

- [pinning checker](evidence/pinning_check.py)
- [pinning results](evidence/12-pinning.log)

### Fatal missing entry theorem

Constructor identity does not supply a missing reachability claim. The only
body-pinned **entry** claims use the two fixed literal inputs. No claim has the
shape:

```text
Call(Name("is_bored"), str(CS)) => bored0(CS, 0)
```

or an equivalent arbitrary-input call-to-result property. The universal helper
claims assume that initialization, argument binding, call entry, and the
transition to `#loop` have already occurred. They cannot be mechanically
composed into a full-program theorem because the required universal
call-to-loop connection is absent from `spec.k`.

This is not merely an artifact-maintenance observation: the missing claim is
the only theorem that would quantify over actual calls of the generated
program. Two ground examples do not prove an unrestricted HumanEval domain.

### Result and body sensitivity

Each written claim constrains its returned value; none has a free RHS result or
tautological implication. A separate mutation changed the program term
actually used by the entry claim—`boredFunctionBody` initialized `count` to 1
instead of 0. The mutated definition built successfully. The
`prompt-example-0` proof then exited 1 with `WarnStuckClaimState` and a residual
`<k> 1 ~> .K </k>` against target 0.

Evidence:

- [mutated body](evidence/body-mutated-verification.k)
- [mutated build](evidence/14-body-mutation-kompile.log)
- [body-sensitivity failure](evidence/15-body-mutation-proof.log)

The ground theorem is body-sensitive, but the candidate still lacks an
arbitrary-input entry theorem and computes the wrong source-contract results
on the Stage 2 witnesses.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

A reviewer-authored scanner inventoried every local `syntax`, `configuration`,
`context`, `rule`, and `claim` block in all 24 supplied K files,
`verification.k`, and `spec.k`. It records the complete block text, source
line, attributes, reachability classification, assessment, and rationale.

The inventory contains 946 blocks:

- 230 syntax declarations;
- 705 rules;
- 5 contexts;
- 1 configuration;
- 5 claims.

It identifies 148 function declarations, 110 total declarations, no
`functional` declaration, 45 priority rules, 26 `owise` rules, 35 concrete
rules, 6 simplification rules, 25 supplied symbol declarations, and the one
proof-local `no-evaluators` declaration containing `bored0/1/2`.

Evidence:

- [inventory generator](evidence/k_inventory.py)
- [complete per-block inventory](evidence/rule-inventory.tsv)
- [inventory summary](evidence/rule-inventory-summary.md)
- [inventory command log](evidence/13-rule-inventory.log)

Every block has one of these decisions:

- `SUPPLIED_FIXED_USED_REVIEWED`: reached by this program and checked against
  the relevant modeled operation;
- `SUPPLIED_FIXED_UNUSED`: cannot be reached from this program and therefore
  cannot contribute to these claims; no global Python-equivalence assertion is
  made for it;
- `SUPPLIED_FIXED_OPAQUE_UNUSED`: an explicit supplied abstraction that is
  unreachable here;
- a proof-local exact-definition/summary classification;
- `CLAIM_REVIEWED`.

This treatment does not assume that the trusted baseline blesses
proof-specific rules. All `verification.k` rules were assessed separately.

### Used-construct map and execution fidelity

| Submitted construct | Declaration and material fixed rules |
|---|---|
| module/function binding | `Module`, `FuncDef`, `Params`; module sequencing; `closureVal` creation |
| function call and argument | `Call`, `Name`, `#look`, builtin/global lookup, left-to-right `#evalArgs`, closure application, `#bindP` |
| locals | `Assign(Name,Val)` and the integer `AugAssign` rule update the active scope |
| loop | `For` evaluates its iterable once, then `#loop/#iterNext/#iterYield/#bindTgt/#loopLbl` consumes one string element at a time |
| `ord(ch)` | ordinary name lookup selects `builtinV("ord")`; the builtin rule returns the sole code from a one-character `str` |
| comparisons | `Compare` evaluates left then right and dispatches to the integer `applyCmp` equations |
| boolean guards | `BoolOp` contexts implement left-to-right, value-returning `and`/`or`; `If` dispatches through `truthy` |
| return | `Return`, `#pop`, and the saved frame restore the caller and expose the exact integer |

The cells and allocation rules are framed consistently: this function uses no
heap object or closure cell, the claims start with an empty heap, and all
priority cell/ref rules are guard-inapplicable. The call rule binds the one
argument before the body, the loop obtains `ord` through the normal environment
rather than name-based interception, and return unwinds the one supplied frame.
No used material operation is fabricated or skipped.

The fixed string-literal converter is explicitly ASCII-only. Both ground entry
claims use ASCII literals, so this restriction does not make those claims
false. It does, however, underscore why those two literals cannot stand in for
the unrestricted Python `str` contract. The internal loop claims accept
abstract `IntSeq` values, but, again, no universal entry claim supplies one to
the actual function call.

### Proof-local rules

`verification.k` adds three declarations and ten rules:

1. `boredLoopBody` and `boredFunctionBody` are total nullary constructor
   abbreviations. Mechanical comparison proves exact identity with the
   submitted body. They replace no execution.
2. `isBoredDelimiter(C)` is exactly
   `C == 46 or C == 63 or C == 33`.
3. `isBoredWhitespace(C)` is exactly
   `C == 32 or 9 <= C <= 13`.
4. `bored0`, `bored1`, and `bored2` have an empty-sequence base case and one
   cons case each. The constructor guards are disjoint, every recursive call
   strictly consumes the tail, and the equations reproduce the candidate's
   state transitions and count update.

The summary functions are result-bearing, but they are not unconstrained
oracles. The three loop reachability claims execute the fixed loop semantics
and connect each internal state to the corresponding summary. The
`no-evaluators` attribute prevents speculative narrowing of an abstract
sequence; it does not provide a free equation, and all constructor cases used
by execution are covered.

There is no proof-local `Call` interception, operational priority rule, abrupt
return bridge, exception bridge, heap abstraction, or uninterpreted value that
can choose the postcondition. Pairwise overlaps either have disjoint
constructors or identical mathematical meaning. I therefore make no claim that
a proof-local rule is logically unsound, and no false-rule witness is
applicable. The fatal findings are theorem adequacy and source-contract
alignment, not a smuggled rewrite.

The supplied but unused opaque/symbol boundaries are:

`md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`; and `sortVS`, `sortKeyVS`.

None appears in the submitted program, proof-local summaries, control flow, or
postconditions, so none affects claim closure.

## 6. Fresh non-vacuity test

The candidate supplied no trusted non-vacuity evidence. I created a distinct
reviewer spec module with the same satisfiable ground entry state as
`prompt-example-0`, but changed the required result from the true 0 to the false
1.

The mutation first built successfully:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

Exit status: 0.

The actual proof command was:

```text
kprove spec-vacuity-audit.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT
```

It exited 1 with `WarnStuckClaimState`. The residual contains
`<k> 0 ~> .K </k>`, exactly the true program result that fails to unify with
the mutated target 1. This is a meaningful unmet result obligation, not a
parser error, missing import, timeout, or unrelated crash.

Evidence:

- [false mutation](evidence/spec-vacuity-audit.k)
- [successful mutation build](evidence/17-vacuity-dry-run.log)
- [expected proof rejection](evidence/18-vacuity-proof.log)

The ground claim is therefore non-vacuous. This does not manufacture the
missing universal entry theorem.

## 7. Proven versus assumed accounting

### What is machine-checked

Conditional on the supplied semantics and K backend:

- the candidate loop, when entered in state 0, 1, or 2 with the exact framed
  continuation from `spec.k`, returns the recursively defined candidate
  summary over every finite `IntSeq`;
- the exact submitted function body returns 0 on `"Hello world"`;
- the exact submitted function body returns 1 on the second prompt example.

These are partial-correctness reachability results. They are not a theorem
about all calls of `is_bored`.

### Trusted or informal boundaries

| Boundary | Dependents | Audit status |
|---|---|---|
| supplied operational semantics and K builtins | every claim | accepted as the selected fixed semantics; used path statically reviewed |
| trusted `py2mpy.py` | source-to-K identity | accepted; fresh output is byte-identical |
| KAST abbreviation expansion | ground entry and loop-body pinning | mechanically checked |
| proof-local `bored0/1/2` mathematics | loop postconditions | acceptable for the candidate scanner; exhaustive descending equations plus fixed-semantics loop claims |
| supplied float/sort/MD5 opaque symbols | none | inert and irrelevant |
| universal call-to-loop initialization | required HumanEval theorem | **missing**, not an assumption that can be accepted |
| candidate-summary-to-canonical contract | required HumanEval result | **false** on recorded satisfying inputs |
| candidate concrete/random tests | finite behavior only | empirical; cannot replace either missing theorem |

The Kit-style soundness gate passes for the five theorems that were actually
written: their local theory is sound on the reached domain, their
preconditions are satisfiable, their results are constrained, and false
mutations are rejected. Intent adequacy fails because the only full-program
claims are two examples and because the program disagrees with the trusted
canonical function. Ordinarily this is a `SOUND-BUT-LIMITED` description of
the written theorem set. The benchmark prompt explicitly maps a materially
narrow HumanEval source-contract theorem to `FAIL / NOT_LEGIT`.

## Decision

Fresh `#Top` results are genuine but establish only three internal loop
summaries and two ground calls. They do not establish partial correctness of
the real generated program for arbitrary source-contract inputs, and the
generated program itself has material result divergences from the trusted
canonical implementation. These are candidate defects, not infrastructure
uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
