# Independent adversarial audit — HumanEval 58 `common`

## Executive finding

The candidate contains a freshly reproducible, non-vacuous K reachability proof for a **strictly narrower theorem**: for every pair of finite lists of mathematical integers, the exact submitted constructor program evaluates under the candidate's generated semantics to the sorted, duplicate-free integer intersection.

That is not a legitimate proof of the full source contract. The trusted prompt says only “two lists” and gives no integer element restriction. The trusted canonical program has defined behavior on non-integer lists such as string and tuple lists. The K configuration and claim accept only `list(Ints)`, and a string-list source witness that both Python programs evaluate successfully cannot even be parsed as a K input. This is a material source-domain narrowing. The benchmark's decision rule maps that Kit `SOUND-BUT-LIMITED` result to `FAIL / NOT_LEGIT`.

There are also real candidate-versus-canonical discrepancies on broader list inputs: type-sensitive `bool`/`int` collisions return different representatives, and unhashable elements in a list whose other input is empty produce `[]` in the canonical implementation but `TypeError` in the candidate rewrite. These reinforce, but are not needed for, the verdict.

All work was performed from source copies in `/tmp/audit-work/58-common-audit`; no candidate compiled definition or cache was used. Reviewer scripts, mutations, and bounded logs are in `/audit-output/evidence/`.

## 1. Input and provenance integrity

Status: **PASS; no infrastructure breach.**

`/audit-input.json` declares:

- problem `58-common`, condition `bare`;
- `record_layout` = `legacy-selected-stage1`;
- `semantics_mode` = `GENERATED_SEMANTICS`;
- candidate, trusted prompt, trusted translator, canonical, generation records, trace, manifests, and campaign lock through its `container_paths` map.

I read the launcher-owned audit input, `/audit-campaign-lock.json`, `/run.json`, `/task.json`, `/generation-result.json`, the generation invocation and metrics, `usage.json`, `codex-last.txt`, `codex-output.log`, `prompt.txt`, the legacy records that were also present, and the structured 83-record JSONL trace. The generation records claim a successful `#Top`, but that claim was not used as proof evidence until independently reconstructed in Stage 3.

The campaign-lock object is exactly equal to `audit_input["audit_campaign"]`, and the lock file's SHA-256 is the recorded `ad5dfc...d745`. Every required regular-file SHA-256 checked in [01-integrity.log](evidence/01-integrity.log) matches its recorded field, including the run/task/result/invocation manifests, generation metrics, usage, generation prompt/output/last, canonical, trusted prompt, and translator. The independently computed pipeline tree digest of `/candidate` is `4fa1b9...17`, matching `generation-result.json`; the trace digest is `6811bc...fbb`, matching `usage.json`. The additional launcher aggregate fields in `/audit-input.json` were read; because that file does not specify their aggregate serialization, integrity was grounded in the matching per-file hashes and the record-owned pipeline tree hashes.

All required entries are regular files or real directories. No candidate or trace symlink/unsupported node was found. The candidate has all required proof artifacts: `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and `prove.sh`.

The candidate `prompt.py` and `py2mpy.py` are byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`. In accordance with `GENERATED_SEMANTICS`, `/reference/reference-semantics` is absent. `runtime-metrics.json` is absent, but it is not required for `legacy-selected-stage1` and was not reconstructed or treated as a defect.

Evidence:

- [integrity_check.py](evidence/integrity_check.py)
- [run_integrity.sh](evidence/run_integrity.sh)
- [01-integrity.log](evidence/01-integrity.log)

## 2. Program fidelity and candidate-versus-canonical checks

Status: **FAIL on the unrestricted source-contract domain; PASS on ordinary integer lists.**

### Contract and implementations

The trusted prompt requires `common(l1, l2)` to return the sorted unique common elements of two lists. It places no type parameter or integer-only restriction on the list elements.

The trusted canonical implementation:

1. iterates over both lists;
2. compares each `e1` with each `e2`;
3. adds the matching `e1` value to a Python set;
4. returns the sorted list of that set.

The submitted implementation is:

```python
def common(l1: list, l2: list):
    return sorted(set(l1) & set(l2))
```

That is a good rewrite for normal hashable, mutually orderable values, especially ordinary integers, but it is not behaviorally identical to the canonical nested loops over every list input on which the canonical terminates normally.

### Translator identity

The trusted translator was run in scratch:

```text
python3 /tmp/audit-work/58-common-audit/trusted/py2mpy.py \
  /tmp/audit-work/58-common-audit/candidate/solution.py \
  > /tmp/audit-work/58-common-audit/regenerated.mpy
cmp regenerated.mpy candidate/solution.mpy
```

Both commands exited 0. Both files have SHA-256 `eebc62...2722`, establishing byte identity. See [02-fidelity.log](evidence/02-fidelity.log).

### Independent differential evidence

[differential_test.py](evidence/differential_test.py) independently imports the trusted canonical and candidate modules. It covers:

- both prompt examples;
- both empty, one empty, singleton hit and miss;
- duplicates, negative values, opposite order, and arbitrary-precision integers;
- a type-sensitive `bool`/`int` equality case;
- string and tuple values;
- unhashable elements with an empty opposite input;
- every pair among all lists of lengths 0 through 3 over `{-2,-1,0,1,2}`: 24,336 pairs;
- 2,000 fixed-seed random integer-list pairs.

There were zero generated-integer mismatches. Three broad-domain fixed cases differed:

1. `l1=[False, True, 2]`, `l2=[0, 1, 3]`: canonical returns the `bool` representatives `[False, True]`, while the candidate returns integer representatives `[0, 1]`. Python list equality happens to regard these lists as equal, but their values have different types and representations.
2. `l1=[[1]]`, `l2=[]`: canonical returns `[]`; candidate raises `TypeError: unhashable type: 'list'`.
3. `l1=[]`, `l2=[[1]]`: canonical returns `[]`; candidate raises the same `TypeError`.

String and tuple examples matched both Python programs, which is important for proof scope: they are clean, normally terminating source inputs excluded only by the K model.

The differential command therefore exits 1 to expose these discrepancies; this is candidate evidence, not an audit failure. Full inputs and outcomes are in [02-fidelity.log](evidence/02-fidelity.log).

## 3. Clean proof reconstruction

Status: **PASS for the submitted positive claim.**

The candidate sources and trusted inputs were copied to `/tmp/audit-work/58-common-audit`. No `*-kompiled` tree or candidate cache was copied. K reported version 7.1.293.

### Fresh concrete definition

The generated semantics was rebuilt with LLVM:

```text
kompile --backend llvm candidate/semantic.k \
  --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition semantic-kompiled-audit
```

Exit: 0.

[concrete_compare.py](evidence/concrete_compare.py) then executed the real `solution.mpy` with the rebuilt definition on ten normal/boundary integer cases. It parsed the final `<k>` value and compared it with both Python implementations. Prompt examples, both/one empty, hit/miss, duplicate/negative, both insertion-sort branches, and arbitrary-precision values all matched; all `krun` processes exited 0.

### Fresh proof definition and positive target

The proof definition was rebuilt with Haskell:

```text
kompile --backend haskell candidate/verification.k \
  --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition verification-kompiled-audit
```

Exit: 0.

`spec.k` has exactly one positive target claim. It was run independently:

```text
kprove candidate/spec.k \
  --definition verification-kompiled-audit \
  --spec-module SPEC
```

Output: `#Top`. Exit: 0.

Exact commands, statuses, and bounded concrete/proof output are in [run_reconstruction.sh](evidence/run_reconstruction.sh) and [03-reconstruction.log](evidence/03-reconstruction.log).

## 4. Adequacy and real-program pinning

Status: **real-program pinning and result constraint pass for integer lists; source-contract adequacy fails.**

### Entry claim in plain language

There is no explicit `requires` condition. Sort typing supplies the formal precondition:

- `IS1` and `IS2` are arbitrary finite K `Ints` sequences;
- `<l1>` is exactly `list(IS1)`;
- `<l2>` is exactly `list(IS2)`;
- `<k>` begins with the exact constructor module/function/body shown in the submitted `solution.mpy`.

The postcondition requires:

- `<k>` becomes exactly `list(commonSpec(IS1 ; IS2))`;
- `<l1>` and `<l2>` remain unchanged;
- `commonSpec(IS1 ; IS2)` rewrites to
  `sortInts(intersectInts(uniqueInts(IS1) ; uniqueInts(IS2)))`.

This is an equality-bearing destination term, not a free existential, tautology, or one-way implication. A satisfying state is `IS1=.Ints`, `IS2=.Ints`; a nonempty witness is the first prompt example. Concrete substitution for both was checked against the K execution and both Python implementations in Stage 3.

### Mechanical program identity

[pinning_check.py](evidence/pinning_check.py) balanced-parses the first `Module(...)` constructor in `solution.mpy` and in the claim, tokenizes them, and compares the constructor sequences. Both contain 56 tokens and are identical. This is in addition to trusted translator byte identity. The claim therefore pins the immutable submitted function binding and body despite embedding it rather than importing the `.mpy` file dynamically.

The semantics combines module loading with the external entry-point invocation: it binds the two exact parameter names to `<l1>`/`<l2>` and executes the exact `Return` body. Because the submitted module contains only that definition and the body is pure, omitting creation of a persistent Python function object has no material observable effect on this entry-point theorem.

### Body sensitivity

The fresh [audit-body-mutation.k](evidence/audit-body-mutation.k) changes the **executed claim term** from `set(l1) & set(l2)` to `set(l1) & set(l1)` while retaining the original postcondition. A witness is `IS1=1,.Ints`, `IS2=.Ints`: the mutant returns `[1]`, while the contract result is `[]`.

The mutation parsed, reached the final equality, emitted `WarnStuckClaimState`, and exited 1. Thus the successful claim depends on the submitted body. See [04-negative-tests.log](evidence/04-negative-tests.log).

### Material adequacy failure

The claim's formal domain is only finite integer sequences because:

- `Ints ::= List{Int, ","}`;
- both input cells must contain `PyValue`;
- the only list value production is `list(Ints)`.

The trusted source contract does not impose this restriction. The clean witness

```python
l1 = ["beta", "alpha"]
l2 = ["alpha"]
```

returns `["alpha"]` in both the canonical and candidate Python implementations. The rebuilt K definition rejects `list("beta","alpha")` while parsing the input cell, exiting 113. Exact evidence is in [run_domain_probe.sh](evidence/run_domain_probe.sh) and [06-domain-probe.log](evidence/06-domain-probe.log).

This is not merely missing semantics for an unused construct. It excludes a material class of actual entry-point inputs admitted by the source signature/contract and correctly handled by the real generated program. Under the benchmark decision boundary, this adequacy failure is terminal `FAIL / NOT_LEGIT`.

## 5. Rule-by-rule static soundness review

Status: **the local rules are sound and deterministic on the integer fragment reached by the submitted program; the value-domain model is materially incomplete for the source contract.**

The complete source scan is preserved in [05-static-scan.log](evidence/05-static-scan.log). There are no generated helper K files beyond `semantic.k` and `verification.k`.

### Complete declaration inventory

`semantic.k` declares:

- AST syntax: `Module(PyStmt)`, `FuncDef(String,Params,PyStmt)`, `Return(PyExpr)`, two-string `Params`, `Name(String)`, unary-argument `Call`, and `BinOp(String,PyExpr,PyExpr)`;
- value syntax: `Ints ::= List{Int,","}`, `list(Ints)`, and `set(Ints)`;
- configuration `<py>` containing `<k>`, `<l1>`, and `<l2>`;
- ten local function-attribute symbols across the two files:
  `containsInt`, `uniqueInts`, `intersectInts`, `insertInt`, `sortInts`,
  `makeSet`, `setAnd`, `sortedValue`, `eval`, and `commonSpec`;
- one non-function control item, `execute`.

There are **no** local `[total]`, explicit `[functional]`, opaque, priority, `[owise]`, `[anywhere]`, `[concrete]`, macro, or simplification declarations/rules. No proof-local lemma or auxiliary claim exists. `spec.k` contains only the single target reachability claim.

### Exhaustive rule inventory and decisions

All 25 local rules are accounted for:

| Lines | Rule(s) | Review |
|---|---|---|
| `semantic.k:36` | `containsInt` on `.Ints` gives `false` | Sound base case. |
| `semantic.k:37` | head equality OR recursive suffix membership | Sound structural membership recursion. |
| `semantic.k:40` | `uniqueInts(.Ints)` | Sound base case. |
| `semantic.k:41-42` | discard a head found in the suffix | Sound; retains one last occurrence. |
| `semantic.k:43-44` | retain a head absent from the suffix | Sound; complementary guard. |
| `semantic.k:47` | empty left intersection | Sound base case. |
| `semantic.k:48-49` | retain a left head present in the right | Sound. |
| `semantic.k:50-51` | discard a left head absent from the right | Sound; complementary guard. |
| `semantic.k:54` | insert into empty list | Sound base case. |
| `semantic.k:55-56` | insert before `J` when `I <= J` | Sound for a sorted suffix. |
| `semantic.k:57-58` | retain `J` and recurse when `I > J` | Sound; complementary integer guard and structural descent. |
| `semantic.k:61` | sort empty list | Sound base case. |
| `semantic.k:62` | insertion-sort recursion | Sound; descends on the input suffix. |
| `semantic.k:67` | list-to-set as `uniqueInts` | Sound mathematical finite-integer set representation. Which duplicate occurrence is retained is unobservable for equal integers. |
| `semantic.k:68` | set intersection as `intersectInts` | Sound when its inputs are duplicate-free set representations, as they are in the real execution. |
| `semantic.k:69` | sorted set becomes a sorted list | Sound for integer sets. |
| `semantic.k:70` | sorted list becomes a sorted list | Sound on integer lists; unused by the submitted body but independently truthful. |
| `semantic.k:77` | lookup of the first parameter name | Sound. |
| `semantic.k:78-79` | lookup of distinct second parameter name | Sound, disjoint from the first lookup for actual `"l1"`/`"l2"`. |
| `semantic.k:80-81` | evaluate built-in `set(E)` | Sound for this exact module: `set` is not shadowed and `E` is a pure parameter lookup. |
| `semantic.k:82-83` | evaluate built-in `sorted(E)` | Sound for this exact module: `sorted` is not shadowed. |
| `semantic.k:84-86` | evaluate `E1 & E2` through `setAnd` | Sound for the actual pure set operands. Evaluation order is unobservable on integer inputs. |
| `semantic.k:94-97` | exact `common` module entry binds its two parameters to input cells and starts `BODY` | Sound entry-harness abstraction for the exact submitted one-definition module. It reads but does not alter `<l1>/<l2>`. |
| `semantic.k:98-99` | executing `Return(E)` yields `eval(E,...)` | Sound for the exact pure return body; no continuation or state effect is discarded. |
| `verification.k:9-10` | expand `commonSpec` to unique/intersect/sort | Sound transparent definitional summary; it neither bypasses the executed body nor introduces an oracle. |

### Coverage, guards, overlap, and state

Every submitted constructor maps to a declaration and a reached rule: module, function definition, parameters, return, calls, names, and `&`. Every material operation—both argument lookups, both set conversions, intersection, sorting, and return—executes through transparent equations.

For `uniqueInts` and `intersectInts`, the base/nonempty shapes are disjoint, while `containsInt` versus `notBool containsInt` guards are complementary. For `insertInt`, `<=Int` and `>Int` are disjoint and exhaustive for K integers. The two name-lookup rules are disjoint when the actual parameter strings differ. The call rules have distinct literal callee names, and the binary rule has the literal `"&"`. Recursions strictly descend on finite sequences. Although some evaluator symbols are intentionally partial outside the exact fragment, no unmodeled term is reached by this submitted program.

Only `<k>` changes. `<l1>` and `<l2>` are read and preserved. No heap, mutation, allocation, exception, I/O, loop, call stack, or abrupt control effect occurs in the submitted body, so no such cell is needed for the proved integer execution.

The syntax/rules are broader than the fixed program in limited ways (for example, the specialized `set`/`sorted` rules do not model shadowing for hypothetical different programs). No false conclusion witness from that over-breadth exists for the immutable submitted program and intended entry binding, so I do **not** classify those rules as unsound. The demonstrated defect is instead the narrower `Int` value grammar: a source-valid string input is rejected before execution.

No task-answer oracle, unconstrained fresh result, inconsistent totalization, answer-encoding simplification, or operational shortcut was found.

## 6. Fresh non-vacuity test

Status: **PASS.**

I did not rely on the candidate's `mutation-spec.k`. The fresh [audit-false-post.k](evidence/audit-false-post.k) leaves the exact executed program unchanged and changes only the result obligation:

```k
=> list(0, commonSpec(IS1 ; IS2))
```

The realizable witness `IS1=.Ints`, `IS2=.Ints` should return `list(.Ints)`, not `list(0,.Ints)`.

Command:

```text
kprove audit-false-post.k \
  --definition verification-kompiled-audit \
  --spec-module AUDIT-FALSE-POST
```

The spec built and symbolically executed to the result. `kprove` exited 1 with `WarnStuckClaimState`; the residual explicitly contains the unmet equality between `0, sortInts(...)` and `sortInts(...)`. This is the expected result-bearing failure, not a parser error, timeout, missing import, or unrelated crash. The full bounded residual and status are in [04-negative-tests.log](evidence/04-negative-tests.log).

The separate body-sensitivity mutation described in Stage 4 also reached its mismatched result and failed, but it is not being substituted for this false-postcondition test.

## 7. Proven versus assumed accounting

### Precisely established by the successful reachability proof

Conditional on the candidate definition and K toolchain, for every finite K integer sequence `IS1` and `IS2`, starting with:

```text
<k> exact submitted Module(FuncDef(...)) </k>
<l1> list(IS1) </l1>
<l2> list(IS2) </l2>
```

the computation reaches:

```text
<k> list(sortInts(intersectInts(uniqueInts(IS1);
                                uniqueInts(IS2)))) </k>
```

with both input cells unchanged. The theorem is partial correctness, though all local helper recursions also structurally terminate on finite K lists.

### Trust and assumption ledger

| Boundary | Effect | Assessment |
|---|---|---|
| K 7.1.293 parser, kompilers, backends, prover, and generated axioms | All parsing, execution, and proof closure | Standard unavoidable machine-checking trust boundary. |
| Imported K `INT`, `BOOL`, `STRING`, and list infrastructure | Integer equality/order, Boolean logic, strings used as AST names, finite sequence representation | Acceptable low-level primitives. |
| Trusted `py2mpy.py` transliteration | Links `solution.py` AST to submitted constructor term | Strongly supported here by trusted regeneration and byte identity. |
| Entry-harness rule from module definition plus `<l1>/<l2>` to body execution | Connects the translated definition to the intended entry-point invocation | Informal but exact for this one-definition, pure program; constructor pinning and body mutation support it. |
| Generated set/intersection/sort equations as models of Python built-ins on integers | Gives the result's mathematical meaning | Transparent, guarded, structurally recursive equations; manually justified rule by rule and supported by ten K/Python concrete comparisons plus 26,336 generated integer differential pairs. The tests are finite evidence, not a universal theorem. |
| `commonSpec` | Names the unique/intersect/sort term used in the postcondition | Acceptable definitional summary; no opaque value and no circular operational bridge. |
| Restriction from Python `list` values to K `list(Ints)` | Removes strings, tuples, booleans-as-distinct-values, and all other element domains | **Illegitimate for the unrestricted trusted source contract.** It is the terminal adequacy failure. |

There are no opaque symbols, fresh result variables, empirical oracles inside the proof, proof-local simplification rules, lemmas, priorities, or assumed loop invariants. The generation log and its prior `#Top` are not part of this accounting; only the fresh reconstruction is.

### Gate and verdict accounting

- Fresh positive verification: **PASS** (`#Top`, exit 0).
- Real-body identity, result constraint, body sensitivity, and non-vacuity on finite integer lists: **PASS**.
- Static soundness of local equations on the reached integer fragment: **PASS**.
- Source-contract/input-domain adequacy: **FAIL** because the theorem excludes normally terminating non-integer list inputs, with string lists as a concrete witness.
- Candidate-versus-canonical fidelity on the broad list domain: **FAIL** on the three recorded type/unhashable witnesses.
- Evidence reproducibility: **PASS** for the claims made in this review.

The reconstructed result would be honestly described in generic Kit terminology as sound but materially limited. The benchmark explicitly requires that a material narrowing of the HumanEval source-contract domain be mapped to `FAIL / NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
