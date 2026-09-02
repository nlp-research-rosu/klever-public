# Independent adversarial audit — 148-bf

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I reconstructed the definitions from
source, proved the only target claim independently, mechanically pinned the
claim's macro-expanded module to regenerated `solution.mpy`, reviewed the full
K rule inventory, and rejected fresh body and postcondition mutations for the
expected result mismatch.

Candidate prose, compiled definitions, caches, traces, and prior `#Top` outputs
were not used as authority.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `148-bf`, and condition
`kit-semantics`. The supplied-semantics mount required by that mode exists at
`/reference/reference-semantics`.

The independent checker in
[`evidence/check_integrity.py`](evidence/check_integrity.py) establishes:

- `/audit-campaign-lock.json` is a regular readable file, its SHA-256 is
  `ad5dfc...8d745`, and its parsed JSON is exactly equal to the
  `audit_campaign` block in `/audit-input.json`.
- The recorded SHA-256 values for `/run.json`, `/task.json`,
  `/generation-result.json`, every required `pipeline-v3` generation record,
  the trusted canonical/prompt/translator, and the candidate prompt/translator
  all match the mounted bytes.
- The six required candidate proof artifacts are regular readable files.
- The structured trace contains one JSONL file with the exact per-file hash
  recorded by `generation-result.json`. All 398 JSONL records parse; there are
  zero parse errors.
- The candidate and trusted supplied-semantics trees each contain the same 25
  entries. Every relative entry has the same type and every file the same
  SHA-256; there are no missing, additional, changed, mistyped, or symlinked
  entries. Under the reviewer's documented manifest encoding, both trees have
  digest `3e4892...64ef5`.
- The candidate prompt and translator are byte-identical to their trusted
  mounts. No symlink occurs anywhere in the candidate, reference, or
  generation-evidence trees.

The launcher's directory hashes use an encoding not declared in
`audit-input.json`; I did not assume that encoding. I instead hashed every
regular file and constructed a type/path/file-hash manifest. This is stronger
for the required supplied-semantics comparison because it identifies additions,
omissions, type changes, symlinks, and changed bytes directly.

I read the required `pipeline-v3` records: `/run.json`, `/task.json`,
`/generation-result.json`, `invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the complete structured trace. The generation records claim
success, but those claims played no role in the verdict. The complete
record/hash check is in [`01-integrity.log`](evidence/01-integrity.log); the
trace/tool-call inventory is in
[`16-generation-record-inspection.log`](evidence/16-generation-record-inspection.log).
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract in `/reference/prompt.py:2` asks `bf(planet1, planet2)` to
accept two planet-name strings and return, in Sun-proximity order, the tuple of
planets strictly between them. Either invalid name yields `()`. The trusted
canonical at `/reference/canonical.py:7` also explicitly returns `()` for equal
valid endpoints.

The candidate implementation at `/candidate/solution.py:1` stores the eight
names in the specified order, rejects either invalid input, obtains both
indices, and slices strictly between the smaller and larger index. It omits the
canonical's explicit equal-name check, but this is semantically inert:
`planets[index + 1:index]` is empty. Forward, reverse, adjacent, equal, and
invalid branches therefore agree with the source contract.

Using only the trusted `/reference/py2mpy.py`, I regenerated the MPY text. The
regenerated and submitted files are byte-identical, both with SHA-256
`001874...feb2`; see
[`03-regenerate-mpy.log`](evidence/03-regenerate-mpy.log) and the preserved
[`solution.regenerated.mpy`](evidence/solution.regenerated.mpy).

The independent differential tester
[`evidence/differential_test.py`](evidence/differential_test.py) imports the
trusted canonical and generated entry points separately. Its oracle uses an
independent position map plus filtered enumeration, not either
implementation's slicing. With fixed seed 148 it checked:

- all three documented examples;
- all 64 valid-name pairs, including equal, adjacent, both orders, and maximum
  separation;
- 3,176 corpus-first, 3,176 corpus-second, and 397 same-string records drawn
  from the valid names plus empty, case/space/NUL/Unicode boundaries,
  planet-name mutations, and an exhaustive short-string corpus;
- 4,987 additional seeded generated pairs.

All 11,803 labeled records (11,648 unique input pairs) agreed in value and
tuple type. The command exited 0 with `mismatches=0`; see
[`04-differential.log`](evidence/04-differential.log). This is finite fidelity
evidence, not a substitute for the K proof.

## 3. Clean proof reconstruction

I copied only candidate source artifacts plus trusted inputs to
`/tmp/audit-work/fresh`. I did not copy or use any candidate `*-kompiled`
directory, binary, cache, output log, or compiled definition. The scratch-copy
command is recorded in [`02-copy-sources.log`](evidence/02-copy-sources.log).

Fresh Haskell build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
```

This exited 0. Its only diagnostics were four unused-variable warnings in the
trusted `semantics/str.k`; see
[`05-kompile-proof.log`](evidence/05-kompile-proof.log).

`/candidate/spec.k` contains exactly one positive target claim,
`SPEC.bf-correct`. I independently ran:

```text
kprove spec.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC \
  --claims SPEC.bf-correct
```

It printed literal `#Top` and exited 0. The complete bounded output and status
are in [`06-kprove-positive.log`](evidence/06-kprove-positive.log).

I also built the concrete definition from the trusted source with LLVM and the
required `MPY-KRUN`/`MPY-SYNTAX` modules. It exited 0. The warnings concern
fixed-semantics total functions outside the exercised domain and are addressed
in stage 5; see
[`10-kompile-concrete.log`](evidence/10-kompile-concrete.log).

The preserved [`concrete_audit.py`](evidence/concrete_audit.py) has a
mechanically identical `bf` AST and adds 12 normal/boundary assertions. Its
trusted translation is
[`concrete_audit.mpy`](evidence/concrete_audit.mpy). `krun` terminated with
`.K`, `NoExc`, exit code cell 0, empty heap/stack, and process exit 0; see
[`09-concrete-source-and-translate.log`](evidence/09-concrete-source-and-translate.log)
and [`11-krun-concrete.log`](evidence/11-krun-concrete.log).

Finally, six reviewer-authored ground reachability claims—forward, reverse,
equal, invalid, and a non-ASCII code sequence—jointly printed `#Top` and exited
0. The claims and log are
[`spec-ground.k`](evidence/spec-ground.k) and
[`12-kprove-ground.log`](evidence/12-kprove-ground.log).

## 4. Adequacy and real-program pinning

The entry claim at `/candidate/spec.k:6` has no `requires` clause. In plain
language, its precondition is:

- `P1` and `P2` are arbitrary MPY string code sequences (`IntSeq`);
- execution starts in the standard module environment, with the builtins
  parent, empty heap and stack, fresh scope/heap allocators, no pending return
  or exception, and exit code 0.

Its postcondition is that loading and calling the submitted `bf` terminates
with:

```text
tuple(betweenPlanets(P1, P2))
```

and with the module's actual `bf` closure installed, environment restored,
scope allocator restored to 1, heap and stack empty, heap allocator 0,
`noRet`, `NoExc`, and exit code 0. The return is therefore not a free variable,
tautology, existential, or one-way implication.

The precondition is satisfiable. For example,
`P1 = strToCodes("Mercury")` and `P2 = strToCodes("Earth")` in the displayed
initial cells is a ground witness. Both trusted and candidate Python return
`("Venus",)`, the claim's summary reduces to that tuple, and the corresponding
ground K claim closes. Other explicit substitutions are recorded in stage 3.

Program pinning is mechanical:

1. Trusted regeneration proves submitted `solution.mpy` is the translation of
   submitted `solution.py`.
2. `kast --expand-macros --module VERIFICATION` parsed both the full
   `solution.mpy` module and the claim's `bfModule`. Their KORE is byte-identical
   with SHA-256 `f59cef...bb4d`; see
   [`08b-constructor-identity.log`](evidence/08b-constructor-identity.log).
   The initial diagnostic attempt using the definition's default syntax module
   could not see proof-local macros and is preserved in
   `08a-constructor-identity-default-module-failed.log`; it is not treated as
   evidence.
3. `bfCall(P1,P2)` expands only to the ordinary
   `Call(Name("bf"), str(P1), str(P2))`.

Thus `#loadAll` binds the real translated function body; normal fixed rules
perform lookup, left-to-right argument evaluation, parameter binding, every
assignment/branch/membership/index/slice, return, and frame pop.

The fresh body-sensitivity probe changes the module term actually loaded and
bound to an unconditional `return ()`. The mutant definition compiled
successfully, but its original `("Mercury","Earth") -> ("Venus",)` obligation
failed with a stuck `tuple(.ValSeq)` result and exit 1. See
[`verification-body-mutant-audit.k`](evidence/verification-body-mutant-audit.k),
[`spec-body-mutant-audit.k`](evidence/spec-body-mutant-audit.k),
[`13-kompile-body-mutant.log`](evidence/13-kompile-body-mutant.log), and
[`14-body-mutant-rejected.log`](evidence/14-body-mutant-rejected.log).

The formal domain is all two-string MPY inputs, including invalid code
sequences. It does not narrow the HumanEval string domain to examples, fixed
sizes, or valid planet names. Non-string Python objects are excluded exactly as
the prompt's typed contract permits.

## 5. Rule-by-rule static soundness review

The exhaustive normalized inventory is
[`07-rule-inventory.log`](evidence/07-rule-inventory.log), generated by the
preserved [`inventory_k.py`](evidence/inventory_k.py). It covers all 24 supplied
K source files, `verification.k`, and `spec.k`:

```text
953 records
  234 syntax declarations
  712 rules
    238 operational
    405 ordinary equational
     32 concrete-only
     20 owise
     14 proof-local definitional-summary
      3 proof-local macro equations
    (the categories above classify semantic role; owise/concrete are attributes)
    5 evaluation contexts
    1 configuration
    1 reachability claim
```

Every inventory row includes source line, declaration/rule kind, attributes,
normalized full statement, and review disposition. The disposition partition
is: one active configuration, 246 active or potentially overlapping fixed
records, 265 same-module constructor/sort-disjoint fixed records, 416 unused
constructor-disjoint fixed records, 24 proof-local records, and the target
claim. “Unused” means the rule head cannot occur in this theorem; it is not a
claim that finite testing validated the rule.

Attribute inventory found 149 function declarations, 111 `total`
declarations, 32 `concrete` equations, 26 `owise` attributes, 29 priority
attributes, seven macro/macro-rec declarations, no `functional` declaration,
and no simplification rule. There are 25 fixed-semantics symbolic declarations;
22 are explicitly `no-evaluators`, while `floorFI`, `toF`, and `ceilF` have
only concrete equations in Haskell. All are supplied, float/sort/hash
constructor-disjoint, and unreachable here. The focused proof-local and opaque
list is in [`15-inventory-focus.log`](evidence/15-inventory-focus.log).

### Proof-local records

The 24 proof-local records are exactly seven declarations and 17 equations:

- `bfBody`, `bfModule`, `bfCall`: three macro declarations/equations. Macro
  expansion is constructor-identical to the actual program, so these are
  semantically inert syntax abbreviations, not operational bridges.
- `planetValues`: one total nullary definition of the exact eight prompt names
  in prompt order.
- `planetIndex`: eight singleton equality cases returning 0 through 7 and one
  final guard that is the conjunction of all eight negations. The eight ASCII
  code sequences are pairwise distinct; the guards are disjoint and exhaustive.
- `betweenPlanets`: one direct call to `betweenIndices` on the two indices.
- `betweenIndices`: three disjoint and exhaustive integer cases. A negative
  index yields empty; two nonnegative ordered indices build positions strictly
  between them; the reverse/equal case reverses only the endpoints, not the
  result order. Equal and adjacent indices reduce to empty.

The proof-local attribute set is only four `[function,total]` declarations and
three `[macro]` declarations. There is no local priority, `owise`, concrete,
simplification, opaque/no-evaluator symbol, ordinary operational rule, or
auxiliary claim. Consequently there is no local rule that intercepts
membership, `tuple.index`, comparison, slicing, call, or return, and no
result-bearing oracle or smuggled answer.

`betweenIndices` is syntactically defined for arbitrary integers, but every
value reaching it from `betweenPlanets` is `-1` or 0 through 7. Its out-of-range
extension is a definition of the summary symbol, not a rewrite of program
execution and not an assumption about Python. All theorem-dependent calls to
`buildVS` are in-bounds.

### Fixed-semantics execution path

The material source constructs map to the following fixed declarations and
rules, all inventoried individually:

- module/function/sequence: `#loadAll`, `FuncDef`, statement sequencing;
- binding/call/control: `Name/#look`, `Call/#callee/#evalArgs/#applyK`,
  `closureVal`, `#bindP`, frame push, `Return`, `#pop`;
- values: `Str/strToCodes`, `TupleExpr/toTuple`, `Int`;
- guards: `BoolOp("or")`, tuple `in`/`not in`, `#memberAcc`, structural string
  equality, integer `<`;
- methods/slices: `Attribute`, tuple `index/idxOfVS`, `Subscript/Slice`,
  bound evaluation, clamping, and `buildVS`;
- state: module scope update, callee scope allocation/deallocation, and the
  unchanged heap, stack, return, exception, and exit-code cells.

Strictness and explicit contexts enforce the used evaluation order.
Membership structurally scans the tuple; the short-circuit invalid branch
prevents `idxOfVS` from seeing a missing name. Tuple index therefore cannot
reach its intentionally unmodeled `ValueError` case. Both computed indices are
0 through 7 before slicing, so the active `valSeqAt` calls are in-bounds.
Forward, reverse, equal, and adjacent slice endpoints have the claimed
behavior. Return stores the value, pops the real frame, and restores every
cell constrained by the claim.

The LLVM compiler warned that several supplied `total` functions are not
syntactically exhaustive, including `valSeqAt` on empty/out-of-bounds
sequences. `mapStrVS`, float helpers, and `joinCodes` are unreachable.
`valSeqAt` is reached only with the in-bounds indices established above, where
its ordinary equations reduce. These fixed-source warnings therefore cannot
enable a false conclusion for any intended input.

The remaining supplied rules are headed by unused syntax, distinct callable
names, distinct value sorts, or continuations that never occur in this
program. They cannot rewrite the target execution or its summary. Priority
rules on those heads do not broaden their match into an active state.

I found no unsound rule contributing to the theorem. Accordingly, no false
conclusion witness for an unsound rule exists or is claimed.

## 6. Fresh non-vacuity test

I ignored the candidate's `spec-vacuity.k` as authority and wrote the fresh
[`spec-vacuity-audit.k`](evidence/spec-vacuity-audit.k). It uses the satisfiable
input `("Mercury","Earth")` but changes the result-bearing destination from
`("Venus",)` to `()`.

The exact mutation first passed `kprove --dry-run` with exit 0, demonstrating
successful parsing/building; see
[`17-vacuity-dry-run.log`](evidence/17-vacuity-dry-run.log). The real proof then
exited 1 with `WarnStuckClaimState`. Its irreducible `<k>` cell contains:

```text
tuple(vCons(str(iCons(86,iCons(101,iCons(110,iCons(117,iCons(115,.IntSeq)))))),
            .ValSeq))
```

Those codes spell `"Venus"`, the expected real result, which does not unify
with the false empty tuple. This is the intended unmet obligation, not a
parser error, timeout, missing import, or unrelated crash. See
[`18-vacuity-rejected.log`](evidence/18-vacuity-rejected.log).

## 7. Proven versus assumed accounting

### Precisely proven

Under the mounted supplied MPY semantics, for every pair of `IntSeq` values
`P1,P2`, starting from the claim's displayed standard configuration, execution
of the exact regenerated and submitted `bf` module and call is partially
correct: if it reaches the observed final configuration, its returned value is
exactly the tuple of the fixed eight planet values strictly between the two
valid endpoints in increasing index order, or empty when either endpoint is
invalid, when they are equal, or when they are adjacent. The displayed final
environment, scopes, allocators, heap, stack, return marker, exception, and exit
code are also constrained.

This is universal over the formal two-string domain, not a finite unrolling or
collection of examples.

### Assumptions and trust boundaries

- **Supplied MPY semantics:** mandated by `SUPPLIED_SEMANTICS` and byte-identical
  to the trusted mount. It supplies all execution rules. The relevant subset
  was statically audited and concretely exercised. Unused language facilities
  remain outside the theorem.
- **K v7.1.293 compiler and Haskell/LLVM backends:** trusted to implement
  parsing, macro expansion, rewriting, and reachability. This is the ordinary
  low-level proof-tool trust boundary.
- **K built-in Int/Bool/String/Map/List/equality operations:** trusted ordinary
  mathematics and data-structure primitives. They affect guards, structural
  equality, indices, and state maps.
- **Trusted translator:** trusted to map the accepted Python subset to MPY
  constructors. Byte-identical regeneration and macro-expanded KORE identity
  make the bridge auditable.
- **Prompt order:** Mercury through Neptune is supplied directly by the source
  contract and is encoded verbatim in `planetValues`.
- **CPython and the independent oracle:** used only for finite differential
  evidence about the Python-to-intent bridge. They are not premises used by
  `kprove` and do not replace the universal proof.
- **Opaque primitives:** the fixed semantics contains float/sort/hash opaque
  symbols, but none can influence this program's control, state, result, or
  postcondition. There is no proof-local opaque or fresh result-bearing symbol.

Non-string arguments are outside the typed HumanEval contract and formal
claim. The result is partial correctness; no separate liveness theorem is
claimed. These exclusions do not narrow the requested source-contract domain.

Gate A (real-program soundness), Gate B (intent adequacy), and Gate C
(auditability/trust accounting) all pass. There is no material adequacy gap or
candidate-local unsoundness.

VERDICT: PASS
LEGITIMACY: LEGIT
