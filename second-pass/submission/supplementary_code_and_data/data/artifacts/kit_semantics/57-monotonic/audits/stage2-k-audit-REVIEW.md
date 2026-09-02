# Independent adversarial review: 57-monotonic

Assessment: the candidate contains a legitimate, non-vacuous partial-correctness
proof of the submitted program under the supplied semantics. The proof is not
an unqualified validation of Python's `sorted`: its human-facing monotonicity
interpretation remains conditional on the supplied opaque `sortVS` primitive
having the standard ascending-sort meaning, plus an elementary but informal
mathematical bridge. That is a non-fatal trust-boundary limitation.

## 1. Input and provenance integrity

The launcher declares:

- problem `57-monotonic`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `pipeline-v3`.

All pipeline-v3 records required by the audit prompt are present, readable,
regular files: `/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`, and
`prompt.txt`. The structured trace is one regular JSONL file with 417 parseable
records; there are no malformed rows. The trace and prose claim prior success,
but I did not use that claim as proof evidence. Full structural results are in
[`00-generation-record-inspection.log`](evidence/00-generation-record-inspection.log).

`/audit-campaign-lock.json` is a regular file. Its parsed JSON object exactly
equals the `audit_campaign` block in `/audit-input.json`, and its SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded regular-file digest independently checked by the reviewer
matches: the run/task/result/invocation records, all generation evidence files,
canonical program, prompt, and translator.

The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. A type-and-content manifest
comparison of the two semantics trees is exact: the candidate has no missing,
additional, changed, mistyped, or symlinked entry. Independent pipeline tree
digests are:

- candidate workspace:
  `239596a216f0ee81741f9c1a6dedcc3d3d9e4ca783a713b3692b34b6df366942`,
  matching both the invocation and generation result;
- candidate and trusted semantics, each:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`;
- structured trace:
  `fd952fbb8df5429dd81bd1b669c90344969321c31751610785845f6d9d2a17e5`,
  matching `usage.json`; its sole file hash also matches the invocation/result
  manifest.

The independent hashing and recursive manifest code and output are
[`integrity_check.py`](evidence/integrity_check.py) and
[`01-integrity.log`](evidence/01-integrity.log). There is no infrastructure
breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt asks whether a list is monotonically increasing or
decreasing. On the intended, mutually orderable input elements, this means that
every adjacent pair is nondecreasing or every adjacent pair is nonincreasing.
Empty, singleton, and all-equal lists satisfy the contract.

The canonical implementation returns true exactly when:

```text
l == sorted(l) or l == sorted(l, reverse=True)
```

The generated `solution.py` returns that same Boolean expression directly.
This is behaviorally equivalent to the canonical `if`/`return` form, including
short-circuit evaluation and exceptions raised by `sorted`.

### Trusted regeneration

From the scratch copy I ran:

```bash
python3 /reference/py2mpy.py solution.py | cmp - solution.mpy
```

It exited 0, proving byte identity with the submitted `solution.mpy`; see
[`02-translation-byte-identity.log`](evidence/02-translation-byte-identity.log).

### Independent differential

[`differential_test.py`](evidence/differential_test.py) imports the trusted
canonical and candidate entry points from their separate absolute paths. It
does not reuse a proof equation. It checked:

- all three prompt examples;
- empty, singleton, both two-element orders, equality/duplicate cases;
- the first and late branch-transition boundaries;
- very large integers and representative floats, strings, and tuples;
- a mixed incomparable case, comparing exception type and message;
- all 3,906 lists of lengths 0 through 5 over `[-2,2]`;
- 2,000 deterministic random integer lists of lengths 0 through 25.

The exact result was `checked=5925 mismatches=0`, exit 0. See
[`03-python-differential.log`](evidence/03-python-differential.log). This finite
test supports program fidelity; it is not used as a universal K proof.

## 3. Clean proof reconstruction

I copied source artifacts to `/tmp/audit-work/reconstruction` and copied the
semantics from the trusted `/reference/reference-semantics`, not from a
candidate-built definition. Candidate `runtime-kompiled/`,
`verification-kompiled/`, caches, and bytecode were not copied or used. Fresh
outputs were named `audit-runtime-kompiled` and
`audit-verification-kompiled`.

The available `kompile`, `krun`, and `kprove` are all K v7.1.293; see
[`04-tool-versions.log`](evidence/04-tool-versions.log).

### Fresh concrete definition

Command:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0. Its warnings concern total functions on constructors absent from
this program (`mapStrVS`, float conversions, `joinCodes`, and `valSeqAt`).
See [`05-kompile-llvm.log`](evidence/05-kompile-llvm.log).

The reviewer-authored source and trusted translation are
[`audit_k_concrete.py`](evidence/audit_k_concrete.py) and
[`audit_k_concrete.mpy`](evidence/audit_k_concrete.mpy). Twelve assertions cover
empty/singleton, both two-element orders, all-equal, both prompt-positive
branches, the prompt-negative case, both direction-change boundaries, and
duplicates. Translation exited 0
([`06-translate-audit-k-concrete.log`](evidence/06-translate-audit-k-concrete.log)).
Fresh `krun` exited 0 with `.K`, empty stack, `noRet`, `NoExc`, and exit code 0
([`07-krun-audit-k-concrete.log`](evidence/07-krun-audit-k-concrete.log)).

### Fresh proof definition and positive claim

Commands:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

Both exited 0, and `kprove` printed `#Top`. The only positive target claim is
`SPEC.monotonic`, so every positive target was run. The exact logs are
[`08-kompile-haskell.log`](evidence/08-kompile-haskell.log) and
[`09-kprove-positive.log`](evidence/09-kprove-positive.log).

## 4. Adequacy and real-program pinning

### Claim in plain language

The entry claim has no explicit `requires`. For every K `VS:ValSeq`, it starts
from a realizable empty module configuration with:

- current environment 0;
- empty module scope 0 whose parent is the supplied builtins scope at -1;
- empty heap at allocation counter 0;
- empty call stack, `noRet`, `NoExc`, and exit code 0.

Its `<k>` cell loads a module containing the submitted `monotonic` definition,
then assigns:

```text
result = monotonic(list(VS))
```

The destination requires normal completion (`.K`), empty stack, `noRet`,
`NoExc`, exit code 0, and a Boolean `result`. Its postcondition is the
equivalence:

```text
result ==Bool
  ((VS ==K sortVS(VS))
   orBool
   (VS ==K revVS(sortVS(VS))))
```

The temporary heap and allocation counter are existential because the two
`sorted` calls allocate temporary lists. They do not determine the returned
Boolean. `?R` is also existential syntax, but it is the actual destination
binding produced by execution and is constrained by `==Bool`; it is not a free
oracle or a one-way implication. The fresh false mutation in stage 6 confirms
that distinction operationally.

### Mechanical program identity

[`program_term_compare.py`](evidence/program_term_compare.py) parses the
constructor trees rather than comparing prose or source filenames. The
`FuncDef` extracted from `solution.mpy` and the one executed by `spec.k` have
the same normalized SHA-256,
`669656c5dc651d03199248596d6f06dcfe48018d3db9dd7ef8ae3d4f8fbcf66b`.
It also verifies the following constructor is exactly the expected assignment
and call on `list(VS)`. Both checks returned true; see
[`10-program-term-compare.log`](evidence/10-program-term-compare.log).

There are no loop or helper claims to substitute for execution. Module loading,
function definition, name lookup, argument evaluation, frame creation,
parameter binding, both `sorted` calls as reached, list comparisons,
short-circuit control, return, frame pop, and assignment all run through the
fixed semantics.

### Satisfiability and ground substitutions

The displayed initial cells with any concrete finite `VS` satisfy the claim's
precondition. Ground substitutions for `[]`, ascending, descending,
nonmonotonic, and all-equal lists produce respectively
`true, true, true, false, true`, agreeing with both Python implementations.
See [`claim_substitution.py`](evidence/claim_substitution.py) and
[`11-claim-substitution.log`](evidence/11-claim-substitution.log). The fresh
LLVM execution in stage 3 independently covers the same states.

The candidate body-sensitivity file was treated as untrusted input but rerun
against the fresh definition. It changes the constructor actually executed by
the claim to `Return(Bool(false))`; it does not merely edit `solution.py`.
`kprove` exited 1 with `WarnStuckClaimState` and a terminal
`"result" |-> false`, contradicting the demanded true result. See
[`16-candidate-body-sensitivity.log`](evidence/16-candidate-body-sensitivity.log).

There is no finite-size or example-only precondition. The symbolic theorem
quantifies over an unrestricted finite `ValSeq`. The human-facing ordering
interpretation presupposes mutually orderable elements, as does the canonical
normal-return behavior. Mixed incomparable Python elements raise rather than
return a Boolean; the candidate Python implementation matches that behavior,
while the supplied K sort abstraction does not model that exception. This is a
model limitation, not a hidden size/domain restriction in the claim.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`rule-inventory.csv`](evidence/rule-inventory.csv) inventories every source
statement in the assembled supplied semantics, all 24 helper K files, and
`verification.k`, with file/line span, normalized declaration, attributes,
reachability disposition, and review basis. It has 1,093 rows, including:

- 697 semantic/equational/simplification rules;
- 227 syntax/function/macro declarations;
- 5 evaluation contexts and 1 configuration;
- all module, import, and requires declarations.

Attribute coverage includes 146 function declarations, 107 `total`
declarations, 25 `symbol` declarations, 22 `no-evaluators` declarations, 45
priority rules, 36 concrete attributes, 26 `owise` rules, the generated
`strict`/`seqstrict` declarations, and both simplification rules. There are no
local `functional` declarations or auxiliary claims. Counts and dispositions
are summarized in
[`rule-inventory-summary.md`](evidence/rule-inventory-summary.md); the
reproducible generator and log are
[`build_rule_inventory.py`](evidence/build_rule_inventory.py) and
[`12-rule-inventory.log`](evidence/12-rule-inventory.log).

The 865 fixed-semantics statements marked off-path and 24 off-path opaque
primitives have top constructors or sorts absent from every reachable target
term. They cannot influence the target's value, cells, control, or proof
closure. This includes floats, ranges, sets, tuples, subscripts,
comprehensions, string methods, dicts, keyed sorting, and MD5. Their
noninterference is recorded row by row rather than silently treating the whole
semantics tree as relevant.

### Used-constructor map

| Submitted/claim construct | Declaration and operational rules |
|---|---|
| `Module`, statement sequence | `syntax.k:56,61`; `core.k:124-127` |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14-16` |
| `Name` | `syntax.k:12`; `core.k:129-181` |
| `Call`, argument list | `syntax.k:28,37`; `call.k:18-21`; `core.k:183-191` |
| closure call and parameter binding | `call.k:69-75`; `functions.k:62-75` |
| `KwArg("reverse", ...)` | `syntax.k:25`; `core.k:94-102` |
| `Bool(true)` | `syntax.k:11`; `core.k:193-196` |
| `Compare` / `CmpOp("==", ...)` | `syntax.k:30,32`; `operators.k:14-17,33-42`; `list.k:27-28` |
| `BoolOp("or", ...)` | `syntax.k:16`; `bool.k:13-25` |
| `sorted` binding and call | `core.k:156-181`; `sort.k:14-37,61-66` |
| reverse result | `sort.k:51-59` |
| allocation | `core.k:117-121` |
| `Return` and frame pop | `syntax.k:50`; `functions.k:77-91` |
| `Assign(Name("result"), ...)` | `syntax.k:41`; `controls.k:8-18` |

The strict/sequence-strict declarations and explicit contexts evaluate the
callee before arguments, arguments left to right, comparison operands left to
right, and assignment RHS before the write. `BoolOp` evaluates only its head
and then short-circuits. The first comparison can therefore suppress the
second `sorted`, exactly as Python does.

The builtins scope fixes the `"sorted"` binding to `builtinV("sorted")`.
Specialized `#applyK` sort rules preempt the generic `[owise]` builtin route.
They allocate `list(sortVS(VS))`; the reverse keyword applies
`condRev`, whose Boolean guards are disjoint and complete. `revVS` and
`revVSAcc` structurally descend and preserve all elements in reverse order.

The generic comparison rule is `[owise]`; priority dereference rules unwrap the
fresh sorted-list reference before `list.k` applies sequence equality. Calls
push a frame, bind the actual list to `l`, and store the caller continuation;
`Return` records the value and `#pop` restores the caller before assignment.
The cell-aware priority alternatives are inapplicable because these ordinary
frames contain no `"$cells"` marker. Allocation is monotone and starts from an
empty heap, so the two potential sorted results have fresh locations.

### Proof-local extensions

`verification.k` adds exactly two rules:

```text
A ==Bool (A orBool B) => true  requires A
B ==Bool (A orBool B) => true  requires notBool A
```

They are derived Boolean identities. They read or write no configuration cell,
replace no program operation, introduce no abrupt control, and create no fresh
or opaque value. Their only role is to normalize the postcondition after the
fixed semantics has selected the short-circuit branch. The guards are
disjoint on their possible syntactic overlap, and the RHS is true throughout
each guard. The complete four-case truth table is
[`13-proof-local-truth-table.log`](evidence/13-proof-local-truth-table.log),
generated by
[`proof_local_truth_table.py`](evidence/proof_local_truth_table.py).
Thus they are sound derived lemmas, not operational bridges.

### Result-bearing abstraction

`sortVS` is the only on-path opaque result-bearing symbol. It is in the fixed
supplied semantics, not in `verification.k`, and represents the external Python
builtin `sorted`, not program-defined code. The operational rule still
performs binding, argument evaluation, allocation, comparison, short-circuit
control, and return; only the sorted sequence value is abstracted. Ground
integer and string rules implement insertion sort for concrete execution.

The symbolic K theorem is interpretation-parametric in `sortVS`: it proves
that the exact program returns the equality-to-sort formula for whatever
sequence this fixed primitive denotes. It does **not** prove a universal
connection theorem saying that `sortVS` is an ascending permutation. The same
symbol's appearance in execution and the postcondition would be circular if
`sortVS` summarized program-defined computation. Here it is an expressly
external primitive, so this is an acceptable conditional boundary, but it
prevents an unqualified claim that K itself proved sorting or monotonicity.

No rule was judged materially unsound on the intended orderable, flat-list
domain, so there is no claimed unsound rule requiring a false-conclusion
witness. The narrower evidence gap is the unproved external `sortVS` contract
and the supplied model's omission of Python exception behavior for
incomparable elements.

## 6. Fresh non-vacuity test

I did not reuse the candidate `spec-vacuity.k`. The reviewer-authored
[`fresh-false-mutation.k`](evidence/fresh-false-mutation.k) executes the exact
submitted body on `[1,20,4,10]`, a realizable input which is neither
nondecreasing nor nonincreasing, but demands `result == true`.

First, the following dry run parsed and compiled the mutation successfully
(exit 0):

```bash
kprove fresh-false-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-MUTATION \
  --dry-run
```

See [`14-false-mutation-dry-run.log`](evidence/14-false-mutation-dry-run.log).

The actual proof command:

```bash
kprove fresh-false-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-MUTATION
```

exited 1 with `WarnStuckClaimState`. Its fully executed terminal configuration
contains `"result" |-> false`, two correctly sorted heap values, `.K`,
`NoExc`, and exit code 0. The failure is therefore the expected unmet result
obligation, not a parser error, missing import, timeout, unreachable mutation,
or unrelated crash. Exact output is in
[`15-false-mutation-proof.log`](evidence/15-false-mutation-proof.log).

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY theory and the two sound Boolean simplifications, the
fresh successful reachability proof establishes partial correctness for the
exact submitted constructor body, for an unrestricted symbolic finite
`ValSeq`: normal completion binds `result` to

```text
(VS ==K sortVS(VS))
orBool
(VS ==K revVS(sortVS(VS)))
```

It also establishes the modeled normal control state: consumed computation,
empty stack, restored module environment, `noRet`, `NoExc`, and exit code 0.
It is result-constraining and body-sensitive.

### Trusted or informal boundaries

| Boundary | Influence | Assessment |
|---|---|---|
| Supplied MPY semantics and K v7.1.293 toolchain | All execution and proof steps | Required fixed theorem base; rebuilt from source, not candidate caches |
| Trusted `py2mpy.py` | Source-to-constructor identity | Candidate translation is byte-identical; translator correctness itself is trusted |
| `sortVS` external primitive | Both comparisons and returned Boolean; temporary heap contents | Acceptable low-level library boundary, but its universal ascending-sort contract is not proved in this K claim |
| `revVS` and Boolean/list/K primitives | Reverse result, equality, and branching | Defined by exhaustive, descending equations or K builtins on the used domain |
| “equal to ascending sort or its reverse iff nondecreasing or nonincreasing” | Human-facing interpretation | Elementary mathematics over a finite total order, but informal rather than a separate K theorem |
| Python/K representation bridge | Relates `list(VS)` to ordinary input lists | Strong for the intended flat, orderable values; exceptions, NaN/custom comparison, and nested mutable aliasing are not modeled |

The Python differential and LLVM assertions support only their tested bridge
and concrete inputs. They do not replace the symbolic reachability proof or
prove the universal `sortVS` contract.

### Excluded claims

The candidate does not establish:

- a standalone theorem that `sortVS` is a stable ascending permutation;
- CPython exception behavior for mixed incomparable elements;
- NaN ordering, user-defined comparison side effects, or concurrent mutation;
- complete Python deep-equality/aliasing behavior for arbitrary nested lists;
- a separate termination, complexity, or resource theorem.

### Decision

The proof is legitimate: it reconstructs cleanly, executes and pins the real
translated body, has no unsound proof-local extension, constrains the actual
result, covers the unbounded material input domain, and rejects a meaningful
fresh false result. It is not a substituted, bounded, or vacuous theorem.

The appropriate benchmark outcome is nevertheless the middle category because
the intended monotonicity reading depends on the named opaque `sortVS` library
contract and an informal summary-to-property bridge, and because the supplied
subset omits exceptional/unorderable Python behavior. Those limitations do not
make a false target conclusion provable on the intended orderable-list domain
and do not materially narrow that domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
