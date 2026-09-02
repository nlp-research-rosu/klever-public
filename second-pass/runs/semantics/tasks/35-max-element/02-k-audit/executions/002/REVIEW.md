# Independent adversarial audit: 35-max-element

The candidate reconstructs successfully and its claims are non-vacuous, but it
does **not** contain a legitimate proof of the full HumanEval contract. The
universal claim quantifies over a proof-only `intVals(IntSeq)` tail that is
constructor-distinct from the supplied semantics' real `.ValSeq`/`vCons`
representation. No bridge-free connection theorem relates those
representations. Consequently, the only claims that execute ordinary list
tails are the two fixed prompt examples. The formal universal domain is also
restricted to non-empty integer sequences even though the prompt says `list`
and the canonical implementation works for other non-empty comparable lists.

## 1. Input and provenance integrity

Status: **PASS (audit infrastructure intact).**

I first read `/audit-input.json`. It declares:

- problem `35-max-element`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance;
- the mounted paths under `container_paths`.

The trusted `/reference/reference-semantics` tree is present, as required for
this mode. This is therefore not a `GENERATED_SEMANTICS` audit, and I did not
invoke the `writing-semantics` workflow.

The campaign block in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

All records required for `legacy-selected-stage1` are present, readable, and
regular files/directories of the expected kind:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the structured trace at
  `/generation-evidence/codex-trace/2026/07/22/rollout-2026-07-22T23-03-06-019f8d24-2cbe-7ac0-a0ea-9ae7e6694037.jsonl`.

`runtime-metrics.json` is absent, which is expressly permitted for this legacy
layout. No required launcher provenance mount is absent. The structured trace
contains 265 valid JSON records; I parsed every record and inventoried its event
types, tool calls, outputs, messages, and completion records. The historical
generation report claims one `#Top`, but I did not rely on that claim.

Independently computed hashes match the launcher's directly recorded hashes,
including:

| Artifact | SHA-256 |
|---|---|
| trusted canonical | `cd753991163bad434b268f6c65c18168e77f964d20917b628643e8d96740756e` |
| trusted/candidate prompt | `75ceb54ce0c4ea472f0613ef75a8b6bc8d5b530e6749df89eff0779faa70a96b` |
| trusted/candidate translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| run manifest | `321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0` |
| task manifest | `2a6af94deacc6f3972b251cf77cc018db9ca74fdcc44eed3a3e71dfa26536578` |
| generation result | `0e1a36f17b69064a6dda6c1ef0f2f7cf4294b3a5875eb808ec6adcb63021537f` |
| generation invocation | `10194c3f40cd38477be71b7b81b38df783c29e131499d2c2fbfb616a8d87ee0a` |
| generation metrics | `1889b95de3d2ad3fbeebfd53928a09c23fb7a2edb35828eb9231e33420c34c79` |
| generation usage | `2215536a69e405486146d3f2748b6bc09b877cd0c049a8effaf6c9f84a4170e8` |
| generation prompt | `3ccfe05a1e1620ec7e34cf354de6eeb973da0fe27a12a04f4ac62b0a78eeec09` |
| generation last response | `197905ee7c657cf2efb5619addc8e3d7f9c188d468d52dece29f136292463bed` |
| generation output log | `d2498b0d454b995e1f7791bcc905e3fc1e0c51bf08bdccce6c510a7f3a787a4d` |
| structured trace file | `d404819013ed44cf79f8798d82777196d9306093979afa7c732b874572e38b1f` |

`cmp` establishes byte identity between candidate and trusted `prompt.py` and
between candidate and trusted `py2mpy.py`. Recursive
`diff -r --no-dereference` establishes exact entry and byte identity between
`/candidate/reference-semantics` and the trusted supplied tree. Both trees
contain only regular directories/files, with no missing, additional,
mistyped, changed, or symlinked entry. A separate search found no symlinks in
the candidate, reference, or generation-evidence trees.

The required candidate proof artifacts (`solution.py`, `solution.mpy`,
`verification.k`, `spec.k`, and `prove.sh`) are all present as regular files.

Evidence:

- `evidence/provenance_check.sh`
- `evidence/provenance.log`
- `evidence/inspect_trace.py`
- `evidence/trace-inspection.log`

## 2. Program fidelity and candidate-versus-canonical checks

Status: **implementation fidelity passes; proof-domain fidelity does not.**

The trusted prompt asks `max_element(l: list)` to return the maximum element of
the list. A maximum is defined for a non-empty list of mutually comparable
elements. The trusted canonical implementation seeds `m` with `l[0]`, visits
every element, updates `m` when `e > m`, and returns `m`.

The candidate implementation is:

```python
def max_element(l: list):
    return max(l)
```

This is a different but extensionally suitable algorithm for non-empty
comparable Python lists. With the trusted translator, regeneration exits zero
and produces a file byte-identical to the submitted `solution.mpy`, SHA-256
`b040afa3d90d99cfcc4af2a4d930d009cfbf495e7de3998c1d24d2899e6b8791`.

The independent differential test imports the trusted canonical and generated
entry points separately. It covers both prompt examples; singleton, duplicate,
ascending/descending, update/no-update, negative, huge-integer, and other branch
boundaries; every list of length 1 through 5 over `[-2,2]`; and 1,000 seeded
random integer lists of lengths 1 through 30. It also checks booleans, mixed
integers/floats, strings, and infinities. All 4,919 non-empty cases agree in
both value and result type.

On `[]`, the canonical raises `IndexError` while the candidate raises
`ValueError`. Because the requested maximum does not exist on an empty list,
this is recorded as an exceptional-boundary difference rather than the main
failure.

The broader test cases expose a proof-scope issue: for example, both Python
implementations return `"z"` for `["aa", "z", "ab"]` and `2.5` for
`[1, 2.5, -3, 2.25]`, but the universal K claim accepts only `Int`/`IntSeq`.
The prompt contains no integer-only annotation or precondition.

Evidence:

- `evidence/program_fidelity.sh`
- `evidence/differential_test.py`
- `evidence/program-fidelity.log`

## 3. Clean proof reconstruction

Status: **PASS as verification under the submitted extended theory.**

I copied only source artifacts to `/tmp/audit-work/work`, using the trusted
translator and trusted supplied-semantics tree. No candidate-built definition
or cache was copied or reused. Before building, both `runtime-kompiled` and
`verification-kompiled` were absent.

The independently observed tool version was K `v7.1.293`.

Fresh concrete build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

This exited 0. A trustedly translated independent five-case concrete program
then ran with `krun`, exited 0, and ended at `.K`, `NoExc`, empty stack, and
exit code 0.

Fresh proof build:

```text
kompile verification.k --backend haskell \
  --main-module MAX-ELEMENT-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

This exited 0. Running the original submitted `spec.k` against that definition
exited 0 and printed `#Top`.

I also made a mechanically labeled copy of the four exact claims and selected
them independently:

| Positive target | Exact selection | Exit/output |
|---|---|---|
| abstract `#maxAcc` fold | `MAX-ELEMENT-SPEC-LABELED.fold` | 0, `#Top` |
| first prompt example | `MAX-ELEMENT-SPEC-LABELED.example-one` | 0, `#Top` |
| second prompt example | `MAX-ELEMENT-SPEC-LABELED.example-two` | 0, `#Top` |
| universal entry with required fold circularity | `fold,universal` fully qualified | 0, `#Top` |

An initial reviewer-authored label-filter attempt used the wrong declaration
spelling and received only `Unused filtering labels`; it occurred after the
original spec had already returned `#Top`. It is preserved in
`clean-rebuild.log` and was corrected in `individual-claims.log`. This is an
auditor command error, not a candidate proof failure.

The compiler's warnings about unused variables and non-exhaustive total
functions originate in the supplied fixed semantics. The warned functions are
not on this target's proof path.

Evidence:

- `evidence/clean_rebuild.sh`
- `evidence/clean-rebuild.log`
- `evidence/individual_claims.sh`
- `evidence/individual-claims.log`
- `evidence/artifacts/audit-concrete.py`
- `evidence/artifacts/audit-concrete.mpy`
- `evidence/artifacts/spec-labeled.k`

## 4. Adequacy and real-program pinning

Status: **FAIL.**

### Plain-language claims

The first claim has no `requires` clause. For arbitrary `REST:IntSeq`,
`ACC:Int`, and continuation `CONT:K`, it says that folding the supplied
semantics' maximum accumulator over the proof-only list
`list(intVals(REST))` produces `maxOf(ACC, REST)` and preserves `CONT`.

The universal entry claim also has no textual `requires`, but its variable
sorts and starting term impose its precondition:

- the input is non-empty;
- its first element is an `Int`;
- its remaining elements are represented by `intVals(REST:IntSeq)`;
- the environment, heap, locations, stack, return, and exception cells have
  the exact initial values shown in the claim.

It says the loaded `max_element` call returns exactly
`maxOf(FIRST, REST)`. The result is not existential, free, tautological, or
guarded by a one-way implication. Only the final scopes map is existential,
which appropriately abstracts the temporary/module bindings and does not
weaken the result.

The last two claims execute the same wrapper on the two ordinary concrete list
values from the prompt and require exact results `3` and `123`.

### Program identity and sensitivity

A mechanical whitespace-insensitive constructor comparison extracts the
right-hand side of `maxElementProgram` and proves it identical to the complete
submitted `solution.mpy`:

```text
Module(FuncDef("max_element",Params("l"),
  Return(Call(Name("max"),Name("l")))))
```

Thus the claim executes the actual submitted function binding and body.

The state with `FIRST=1` and
`REST=iCons(2,iCons(3,.IntSeq))`, together with the exact cells in the entry
claim, is a satisfiable formal precondition. Its ground claim returns `3` with
`#Top`; both Python implementations return `3` for the corresponding ordinary
list `[1,2,3]`.

A body-sensitivity mutation changed the constructor term actually used by the
claim to `Return(Int(0))`. The mutated definition compiled successfully, but
the example proof exited 1 with a `WarnStuckClaimState` whose final `<k>` value
was `0` rather than required `3`. This confirms dependence on the real body.

### Decisive representation gap

The universal starting list is not an ordinary list value in the supplied
semantics. Real finite list tails use only:

```text
.ValSeq
vCons(Val, ValSeq)
```

The candidate adds the distinct constructor:

```text
intVals(IntSeq)
```

For `[1,2,3]`, an actual semantics value is:

```text
list(vCons(1, vCons(2, vCons(3, .ValSeq))))
```

The universal claim instead uses:

```text
list(vCons(1, intVals(iCons(2, iCons(3, .IntSeq)))))
```

No substitution for `REST` makes these constructor terms identical. The two
candidate iterator rules give the latter term a plausible observer behavior,
but there is no bridge-free universal connection theorem from real
`.ValSeq`/`vCons` execution to this abstraction. Fresh, well-formed connection
claims for the expected base and step equations both compile and then fail
with stuck states:

```text
intVals(.IntSeq)  => .ValSeq
intVals(iCons(I,R)) => vCons(I,intVals(R))
```

This does **not** show that the iterator equations derive a false result; it
shows the narrower required evidence gap. The abstract constructor is not a
reachable real list representation, and the actual fixed semantics cannot
establish even its base/step representation connection. The two concrete
example claims cover only two fixed sizes and cannot replace a universal
real-list theorem.

This is a real-program pinning failure for the universal input domain. It is
not merely a source-to-proof maintenance observation.

### Material source-domain restriction

Independently, `FIRST:Int` and `REST:IntSeq` restrict the theorem to integers.
The source annotation is `list`, not `list[int]`, and both the canonical and
candidate correctly return maxima for other non-empty comparable lists.
Strings and floats are concrete witnesses of valid source behavior excluded by
the formal claim. Under the benchmark's decision rule, this material narrowing
is `FAIL / NOT_LEGIT`, not a non-fatal concern.

Evidence:

- `evidence/pinning_check.py`
- `evidence/adequacy_pinning.sh`
- `evidence/adequacy-pinning.log`
- `evidence/artifacts/ground-witness.k`
- `evidence/artifacts/verification-body-mutated.k`
- `evidence/artifacts/spec-body-mutated.k`
- `evidence/artifacts/representation-gap.k`
- `evidence/extension-sensitivity.log`

## 5. Rule-by-rule static soundness review

Status: **the used rules are locally coherent, but the connection/adequacy gap
from Stage 4 remains fatal.**

### Exhaustive inventory

`evidence/rule-inventory.md` is generated from every `syntax`, `rule`,
`configuration`, `context`, and `claim` declaration in:

- the assembled trusted `semantics.k`;
- every trusted helper file under `semantics/`;
- candidate `verification.k`;
- candidate `spec.k`.

It contains 940 individually located entries:

- 230 syntax declarations;
- 700 rules;
- 1 configuration;
- 5 contexts;
- 4 reachability claims;
- 0 simplification rules;
- 25 declarations with `no-evaluators`.

Every entry records attributes, whether it is on the target path, and a review
disposition. The 25 opaque `no-evaluators` symbols belong to supplied float,
sort, and MD5 support and cannot affect this integer-maximum path.

### Candidate-local inventory

| Extension | Class and review |
|---|---|
| `maxElementProgram : Module [function,total]` | Nullary definitional program constant. Its one equation is complete and exactly matches `solution.mpy`. |
| `intVals(IntSeq) : ValSeq` | Fresh proof-only representation constructor. It has no constructor equality to real list tails. |
| `maxOf(Int,IntSeq) : Int [function,total]` | Mathematical fold. Base and recursive equations cover the two `IntSeq` constructors, do not overlap, and recurse structurally. |
| `#iterNext(list(intVals(.IntSeq)))` | Operational representation bridge/definition. It yields `#iterDone`, frames the arbitrary continuation, and changes no state cell. |
| `#iterNext(list(intVals(iCons(I,R))))` | Operational representation bridge/definition. It yields exactly `I`, carries `intVals(R)`, frames the arbitrary continuation, and changes no state cell. |
| priority 40 on both iterator rules | No overlap with each other or the fixed `.ValSeq`/`vCons` list rules because the constructors are disjoint. Priority does not supply the missing representation theorem. |

There are no candidate-local simplification rules, `[concrete]` rules, opaque
symbols, or `functional` declarations.

The iterator equations are exhaustive over `IntSeq` and locally truthful if
`intVals` is *defined* to mean an abstract integer sequence. I therefore do
not label them globally false or unsound. Their problem is that they supply
semantics to an artificial input representation and then the universal claim
uses that representation without proving its relation to real list values.

The iterator value is proof-relevant: it reaches `#maxAcc`, determines
`maxInt`, and determines the final postcondition. A separate mutation changed
the step rule from yielding `I` to yielding `I+1`. That definition compiled,
and the ground proof correctly failed at computed `3` versus required `2`.
Thus the proof cannot accept an opposite iterator interpretation.

### Used fixed-semantics path

Every material constructor in `solution.mpy` maps to the supplied syntax:
`Module`, `FuncDef`, `Params`, `Return`, `Call`, and `Name`. The claim directly
supplies a `list(ValSeq)` value.

The executed rule sequence is:

1. `#loadAll(Module(SS))` exposes the function definition.
2. `FuncDef` binds an exact `closureVal` in module scope.
3. `Call` evaluates the callee before arguments; `Name("max_element")`
   resolves through the actual environment.
4. The closure call allocates a temporary scope, pushes the exact continuation
   frame, and binds `l` to the supplied argument.
5. The function body evaluates `Name("max")` by normal scope/builtins lookup,
   so the binding is pinned to `builtinV("max")`, not selected by text alone.
6. The call dispatcher evaluates the argument left-to-right and routes the
   one-iterable builtin call to `#maxAcc0`.
7. The first real `vCons(FIRST,...)` is consumed by the fixed list iterator and
   seeds the integer maximum accumulator.
8. Remaining abstract elements are consumed by the two candidate iterator
   rules; fixed `#maxAcc` updates with mathematical `maxInt`.
9. `Return` sets `retV`, and `#pop` restores the caller environment,
   continuation, scope location, and stack.

For the claimed non-empty integer path, binding, evaluation order, calls,
returns, guards, and state footprints are coherent. The bare unboxed list is
read-only, so bypassing caller-side allocation does not hide a mutation or
alias effect in this function. The heap remains empty. The final scope is
appropriately abstracted, while stack, return, exception, and result remain
constrained.

The fixed semantics deliberately has no empty-`max` error transition from
`#iterDone ~> #maxCont0`; empty input is not part of the formal claim. The
supplied semantics also contains narrower models and opaque boundaries for
other Python constructs, but none occurs on this target path.

No inventoried candidate rule is declared unsound, so no unsupported
false-conclusion accusation is made. The fatal finding is the absence of the
required connection theorem and the resulting theorem-domain mismatch.

Evidence:

- `evidence/inventory_k.py`
- `evidence/inventory-generation.log`
- `evidence/rule-inventory.md`
- `evidence/extension_sensitivity.sh`
- `evidence/extension-sensitivity.log`
- `evidence/artifacts/verification-bridge-mutated.k`
- `evidence/artifacts/spec-bridge-mutated.k`

## 6. Fresh non-vacuity test

Status: **PASS.**

I created a fresh universal postcondition mutation:

```text
maxOf(FIRST, REST) +Int 1
```

The satisfying witness `FIRST=1`,
`REST=iCons(2,iCons(3,.IntSeq))` corresponds to `[1,2,3]`; both Python
implementations return `3`, while the mutated target is `4`.

`kprove --dry-run` on the mutation exited 0, establishing that it parsed and
built successfully. The actual proof then exited 1 with
`WarnStuckClaimState`. The residual explicitly reports the failed implication
`FIRST #Equals FIRST +Int 1` on the base branch. This is the expected unmet
result obligation, not a parser error, missing import, timeout, or unrelated
crash.

The positive proof is therefore result-constraining and non-vacuous. This does
not repair its domain/connection failure.

Evidence:

- `evidence/nonvacuity.sh`
- `evidence/nonvacuity.log`
- `evidence/artifacts/spec-vacuity-audit.k`

## 7. Proven versus assumed accounting

Status: **the exact abstract theorem is proved; the requested real-program
contract is not.**

### What the successful reachability proof establishes

Conditional on the supplied K definition plus candidate `verification.k`, it
establishes:

1. `#maxAcc` over `list(intVals(REST))` computes the structurally recursive
   integer fold `maxOf(ACC, REST)`.
2. The exact translated wrapper body, called with a first real integer followed
   by an `intVals` abstract tail, returns `maxOf(FIRST, REST)`.
3. The exact translated wrapper returns `3` and `123` on the two ordinary
   concrete prompt lists.

It does not establish a universal claim over ordinary `.ValSeq`/`vCons` list
terms, nor does it establish the source contract for non-integer comparable
lists.

### Trust ledger

| Boundary | Effect/dependents | Assessment |
|---|---|---|
| K compiler/prover/backend v7.1.293 | All machine-checking results | Necessary low-level trust boundary. Fresh builds and discriminating mutations reduce, but cannot eliminate, this trust. |
| Trusted supplied semantics | Defines the selected Python subset, configuration, calls, list iteration, and integer `max` | Acceptable benchmark boundary. Candidate copy is byte-identical. It is intentionally not full Python. |
| Trusted `py2mpy.py` | Connects `solution.py` AST to `solution.mpy` constructors | Acceptable mounted translator boundary; byte-identical regeneration and mechanical program-term comparison support it. |
| K `Int`/`maxInt` mathematics | Determines `maxOf` and `#maxAcc` values | Ordinary mathematical primitive; acceptable. |
| Candidate `maxOf` equations | Defines the requested integer fold | Fully covered, disjoint, decreasing, and acceptable. |
| Candidate `intVals` iterator behavior | Supplies every tail element used by the universal proof and therefore the result | Locally exhaustive and value-sensitive, but **not connected by a bridge-free theorem to real `ValSeq` execution**. Fatal for the target theorem. |
| Intended-domain assumption “non-empty integers only” | Excludes empty lists and all non-integer comparable lists | Non-empty is natural for a maximum; integer-only is not stated by the prompt and is materially narrowing. Fatal under the benchmark mapping. |
| Existential final scopes | Hides temporary/module scope cleanup | Acceptable because result, control, heap, stack, return, and exception are separately constrained. |
| Imported opaque float/sort/MD5 symbols | None on this target path | Harmless here; they do not occur in any reachable target term. |
| Differential testing | Supports Python implementation equivalence on 4,919 inputs | Finite empirical bridge only. It cannot replace the missing K representation theorem or broaden the formal claim. |

### Gate accounting and decision

- Fresh positive verification: **PASS** (`#Top`, exit 0).
- Program-body identity and body sensitivity: **PASS**.
- Result constraint/non-vacuity: **PASS**.
- Proof-local equation consistency on the represented abstract domain: **PASS**.
- Real ordinary-list universal connection: **FAIL**.
- Full source-contract domain alignment: **FAIL**.
- Reproducible audit evidence: **PASS**.

The two failed gates are material. In particular, two fixed real-list examples
plus a universal theorem over a disconnected proof-only list representation do
not prove unrestricted real list inputs, and the integer-only formal domain
materially narrows the stated HumanEval contract. The correct benchmark mapping
is therefore `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
