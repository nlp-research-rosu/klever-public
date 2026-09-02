# Independent adversarial audit: 14-all-prefixes

## Conclusion

The candidate contains a legitimate partial-correctness proof of the submitted generated program. I rebuilt both definitions from source, proved the two-claim specification from the clean build, mechanically matched the constructor term used by the entry claim to the trusted regeneration of `solution.mpy`, reviewed every local K sentence, and obtained the expected failures from both an executable-body mutation and an independently written false-result mutation.

The proof is unbounded in string length. It does not reduce the contract to examples, fixed sizes, bounded unrolling, ASCII inputs, or a finite test domain. Its symbolic input is an arbitrary finite `IntSeq`, which is at least as broad as the code-point-sequence representation needed for Python strings.

No audit infrastructure breach was found.

## 1. Input and provenance integrity

The launcher declares:

- problem `14-all-prefixes`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

I used the `container_paths` mounts, not the host-only provenance paths. `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`, `/task.json`, `/generation-result.json`, all records required for this legacy layout, the candidate mount, and the trusted mounts are real and readable. `runtime-metrics.json` is absent, but this layout explicitly does not require historical runtime metrics. `usage.json` is present and was inspected.

The `audit_campaign` object equals `/audit-campaign-lock.json` structurally, and the independently computed lock hash is the declared `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

The independent provenance checker recomputed every declared regular-file hash used by this layout, including:

| Mounted artifact | SHA-256 result |
|---|---|
| trusted canonical | `6cfaba155817dc12117193c2a62dfbb8ae109db90d967ed45314a6c5c7abb211`, match |
| trusted/candidate prompt | `f4eca2c1c9ceb5ca5b0b0885dfd75fb4f768967fd2e53640176e413a499cc165`, match |
| trusted/candidate translator | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`, match |
| run manifest | `321818dc4f5c9795e25ea800ab12c1b1e5cf0bcc70b308443b9f08339a122db0`, match |
| task manifest | `beb7890541eb45df6a01405d4bb650583d45e198a5d0a9424667a07c69db7200`, match |
| stage-1 result | `4f6357b3fa28f4e5457945322918dacf3df056c773deb7e241d37ca0e8101223`, match |
| invocation | `97295097d982edf9675746f81f47acf6e19c8ce069a32adb3072ac8a163c7aeb`, match |
| generation metrics | `746f32adb99c93c5ed9d6fd830eabbb2397380d08e27250946b6f484f965a4d1`, match |
| generation usage | `95165766d7f31a0750b1b28e9c26fb97d7b91934c7301fb8c6e402d9b26bb3dc`, match |
| generation output | `a16cce433ec88f11d25d67af0dac11748bf21c69dd169781e997df270f512783`, match |
| structured trace file | `fea710acf0162ac55b15ded71072a0d7d01ef4e682c9526b9ac814441ebde67c`, match |

I independently reimplemented the pipeline tree-hash format. The mounted candidate hashes to `52c454781d34ae87a19ce4d39c210d317c2aa90cd6bb19432ca76f3f562e354c`, exactly the retained workspace digest in `/generation-result.json`. The trusted supplied-semantics tree hashes to `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`, exactly the recorded manifest digest. The trace tree hashes to `c84fb2c29cfee3117956a568078a5a0a610b012b09eed6dd595b2df7eaacd0c0`, exactly `usage.json`'s source-trace digest.

The candidate and trusted `reference-semantics/` inventories each contain the same 25 directories/files. Their types and per-file SHA-256 values are identical. Neither tree contains a symlink; the candidate has no missing, additional, mistyped, or changed semantics entry. Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted mounts.

The required structured trace consists of one JSONL file and all 317 lines parse. The generation output has 15,249 lines. It contains both failed intermediate proof attempts and eventual `#Top` reports. Those records were treated only as untrusted history; no generation-time success was used as proof evidence.

Evidence:

- [provenance checker](evidence/stage1/provenance_check.py)
- [provenance log](evidence/stage1/provenance-check.log)
- [generation-record inspector](evidence/stage1/generation_record_inspect.py)
- [generation-record log](evidence/stage1/generation-record-inspection.log)

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says that `all_prefixes(string: str)` returns every nonempty prefix of `string`, ordered from shortest to longest. Thus `""` maps to `[]`, a one-character string maps to a one-element list, and `"abc"` maps to `["a", "ab", "abc"]`.

The canonical implementation iterates `i` over `range(len(string))` and appends `string[:i+1]`. The candidate iterates `end` over `range(1, len(string) + 1)` and appends `string[:end]`. These are extensionally the same on every Python `str`.

Trusted regeneration was:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
```

It exited 0. `cmp -s regenerated-solution.mpy solution.mpy` exited 0. Both files have SHA-256 `98271db4e02d617f8a444f10b620c44eefe9021daa13c685cfe7db4ddc7418ca`.

The independent differential test imports the trusted canonical and candidate entry points separately and also checks an independently written slicing formula. It covered:

- the documented `"abc"` example;
- empty, one-iteration, and repeated-iteration boundaries;
- control characters, repeated characters, combining characters, non-ASCII text, emoji, and a length-256 string;
- every string of length 0 through 5 over a four-symbol alphabet;
- 2,000 deterministic generated strings of length 0 through 96 over an alphabet containing ASCII, controls, Unicode, and emoji.

After deduplication, 3,333 inputs were tested, with zero mismatches. The complete input list is preserved; its ordered digest is `e9a3dd255d65bdbd4ec51c669386bb58d86919515dd5371f9f710e49cfb26e1c`.

Evidence:

- [translation log](evidence/stage2/translation-identity.log)
- [differential script](evidence/stage2/differential_test.py)
- [differential inputs](evidence/stage2/differential-inputs.json)
- [differential log](evidence/stage2/differential-test.log)

Stage 2 result: PASS.

## 3. Clean proof reconstruction

All source needed for execution was copied to `/tmp/audit-work/run-002`. The semantics copy came from `/reference/reference-semantics`, not from a candidate cache. No candidate-built definition existed or was reused. The live toolchain is K `v7.1.293`.

The clean concrete build command was:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-rebuild-kompiled
```

It exited 0. `krun smoke.mpy --definition audit-runtime-rebuild-kompiled` exited 0 and ended with `.K`, `NoExc`, exit code 0, and the expected empty, one-prefix, and three-prefix heap lists.

The clean proof build command was:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-rebuild-kompiled
```

It exited 0. The two positive claims in `spec.k` are the loop invariant and the end-to-end entry theorem. I ran the loop claim alone:

```text
kprove spec-loop.k \
  --definition audit-verification-rebuild-kompiled \
  --spec-module SPEC-LOOP
```

It exited 0 and printed `#Top`.

I then ran the complete target spec, retaining the loop claim as the entry theorem's coinductive circularity:

```text
kprove spec.k \
  --definition audit-verification-rebuild-kompiled \
  --spec-module SPEC
```

It exited 0 and printed `#Top`. This independently executes every positive target claim. Deleting the loop claim from the entry theorem's proof context is not a valid isolation test because it removes the declared loop invariant dependency.

The compiler's LLVM-only non-exhaustiveness warnings concern `mapStrVS`, float conversions, `joinCodes`, and out-of-bounds `valSeqAt`; none is on the submitted program's path. The Haskell build/proof warnings are unused-variable warnings in supplied `strLt` rules and the intentionally existential final loop variable. There was no build or proof error.

Evidence:

- [tool version](evidence/stage3/tool-versions.log)
- [LLVM build](evidence/stage3/kompile-llvm.log)
- [concrete execution](evidence/stage3/krun-smoke.log)
- [Haskell build](evidence/stage3/kompile-haskell.log)
- [loop proof](evidence/stage3/kprove-loop.log)
- [complete proof](evidence/stage3/kprove-all.log)

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim requires:

- `END <= STOP`;
- current environment location `L`;
- a current scope binding `end` to an integer, `prefixes` to heap reference `H`, and `string` to `str(S)`;
- heap location `H` containing `list(ACC)`;
- the exact source loop body and arbitrary continuation `CONT`.

It concludes that the loop reaches `CONT`, preserves the surrounding scope and bindings except for an unconstrained final integer value of `end`, and replaces the heap list with `prefixesAcc(S, END, STOP, ACC)`. Other configuration cells are framed. This is appropriate because the loop body does not allocate, call user code, raise an exception on the modeled path, or change control stacks.

The entry claim has no additional `requires` clause. For arbitrary `S:IntSeq`, it starts in the exact clean semantics configuration, loads `solutionModule()`, and calls `all_prefixes(str(S))`. It concludes:

- returned value `ref(0)`;
- heap location 0 contains `list(allPrefixes(S))`;
- heap allocation advances from 0 to 1;
- the exact function closure remains in module scope;
- stack is empty, return state is `noRet`, exception is `NoExc`, and exit code is 0.

The postcondition is an equality-bearing state description, not a free result variable, tautology, or one-way implication.

### Satisfiable witnesses

A loop witness is `END = STOP = 1`, `S = .IntSeq`, `ACC = .ValSeq`, `CONT = .K`, a scope containing the three required bindings, and a heap mapping `H` to the empty list. The zero-iteration rule immediately satisfies the postcondition.

An entry witness is the stated clean initial configuration with `S = .IntSeq`. The explicit ground theorem proves return `ref(0)` and heap list `[]`. A second explicit ground theorem substitutes `S = iCons(97, iCons(98, iCons(99, .IntSeq)))` and proves the heap list `["a", "ab", "abc"]` without using `allPrefixes` in the postcondition. Both ground claims close together with `#Top`; both Python implementations produce the same explicit values.

### Mechanical program identity

The trusted translator regeneration is byte-identical to submitted `solution.mpy`. A reviewer script independently extracts the four zero-argument constructor-helper equations from `verification.k`, recursively expands `solutionModule()`, parses both the expansion and `solution.mpy` with `kast`, and compares their KAST trees. Both contain 142 nodes and are identical.

Consequently the entry claim executes the same `Module`, `ImportFrom`, `FuncDef`, docstring `Expr`, `Assign`, `For`, `Call`, `BinOp`, `Attribute`, `Subscript`, `Slice`, and `Return` constructor term as the trusted translation. The typing-only import is modeled as an inert import by supplied semantics and its binding is never read. The docstring constant is evaluated and discarded; this is also inert for the function result.

### Body sensitivity

I changed the constructor term actually executed by the claim: the `range` start inside `allPrefixesBody()` was changed from `Int(1)` to `Int(2)`, while the theorem and mathematical summary remained unchanged. The mutated verification definition compiled successfully. Its proof exited 1 with `WarnStuckClaimState`; the residual showed the executed body containing `Int(2)` and the unmet heap equality. The concrete false witness is `"a"`, for which the mutated body returns `[]` while the theorem requires `["a"]`.

Evidence:

- [constructor comparison script](evidence/stage4/program_term_check.py)
- [constructor comparison log](evidence/stage4/program-term-check.log)
- [ground K claims](evidence/stage4/spec-ground-entry.k)
- [ground K proof](evidence/stage4/kprove-ground-witnesses.log)
- [ground Python comparison](evidence/stage4/ground-python-witness.log)
- [body-mutated verification](evidence/stage4/verification-body-mut.k)
- [body-mutated spec](evidence/stage4/spec-body-mut.k)
- [body-mutation build](evidence/stage4/body-mutation-build.log)
- [body-mutation proof failure](evidence/stage4/body-mutation-proof.log)

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source inventory covers `reference-semantics/semantics.k`, all 23 supplied helper files, `verification.k`, and `spec.k`: 26 files and 1,110 top-level K sentences.

| Kind | Count |
|---|---:|
| syntax declarations | 233 |
| rules | 702 |
| contexts | 5 |
| configurations | 1 |
| claims | 2 |
| imports/requires/module boundaries | 167 |

The 702 rules comprise 238 operational rules, 429 equations or macro rules, and 35 concrete-only rules. The inventory records every sentence's source span, full text, attributes, normalized hash, classification, disposition, and rationale. Attribute-bearing sentence counts include 151 `function`, 111 `total`, 45 `priority`, 35 `concrete`, 26 `owise`, 22 `no-evaluators`, four `macro`, one `macro-rec`, two strictness declarations, and one sequential-strictness declaration. There is no explicit `[simplification]` rule and no `[functional]` declaration.

Evidence:

- [inventory generator](evidence/stage5/build_rule_inventory.py)
- [complete JSON ledger](evidence/stage5/rule-inventory.json)
- [complete readable ledger](evidence/stage5/rule-inventory.md)
- [inventory build log](evidence/stage5/rule-inventory-build.log)

### Submitted-construct coverage

Every material submitted construct maps to fixed supplied semantics:

| Submitted construct | Declaration/semantics |
|---|---|
| `Module`, `ImportFrom`, `FuncDef`, statements and expressions | `syntax.k`; load/sequencing in `core.k`; import handling in `controls.k`; closure creation in `functions.k` |
| parameter binding, call, return, frame restoration | left-to-right argument evaluation in `core.k`; routing/frame creation in `call.k`; binding/return/pop in `functions.k` |
| names and builtins | chained scope lookup and `builtinsScope` in `core.k` |
| integer literal and `+` | literal rule in `core.k`; dispatch in `operators.k`; integer addition in `int.k` |
| list construction and allocation | `ListExpr`, `#evalArgs`, `#alloc`, and `list(ValSeq)` in `list.k`/`core.k` |
| `len(string)` | `applyBuiltin("len", ...)`, `seqLen`, and `isLen` in `builtins.k`/`core.k` |
| `range(1, len+1)` | builtin construction in `builtins.k`; `inRange` and iterator transitions in `range.k` |
| `for` and target binding | exact `#loop/#loopStep` control flow in `controls.k`; `#bindTgt` in `tuple.k` |
| string prefix slice | evaluation order and `doSlice` in `subscript.k`; `slStart`, `slStop`, `slStep`, and `buildIS` |
| `prefixes.append(...)` | bound-method routing in `call.k`; priority-40 in-place heap update in `list.k` |
| docstring expression | ASCII literal conversion in `str.k`; value discard in `controls.k` |

The active order is Python-like for the submitted term: RHS before assignment, iterable once before the loop, call callee before arguments, arguments left to right, and slice bounds left to right. The function call creates and later removes its local scope, preserves the returned heap list, restores the caller environment, and leaves an empty stack/no exception.

### Candidate proof extensions

`verification.k` contains six syntax declarations and seven equations:

1. `prefixesAcc` has two guarded equations. `END < STOP` and `END >= STOP` are disjoint and exhaustive over integers. The recursive equation advances `END` by one and appends exactly `S[:END]`; recursion therefore descends toward `STOP` under all uses. The base returns the existing accumulator. This is a definitional mathematical summary, not an operational bridge.
2. `allPrefixes(S)` is the exact specialization `prefixesAcc(S, 1, isLen(S)+1, .ValSeq)`.
3. `allPrefixesLoopBody`, `allPrefixesBody`, `allPrefixesDef`, and `solutionModule` are ground, total constructor abbreviations, each with exactly one equation. Their complete expansion was mechanically compared to the submitted program term.

There is no proof-local operational rewrite, priority rule, opaque symbol, unconstrained oracle, concrete-only rule, or explicit simplification lemma. No rule intercepts the program's function call or bypasses its body. `prefixesAcc` influences the postcondition but never replaces execution, so there is no circular execution/oracle dependency.

The loop claim is a derived reachability circularity, not a semantics rewrite. Its `#loop` term, body, binding, environment, heap reference, and arbitrary continuation are all explicit. Symbolic execution performs a real iterator step, binds `end`, executes the real slice/append body, and returns to a smaller matching loop state before circularity can apply. The arbitrary continuation is preserved rather than discarded.

### Supplied trust boundaries and unused rules

The supplied proof definition contains 22 opaque `[no-evaluators]` symbols: `md5hexCodes`; the float functions `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`; and sort functions `sortVS` and `sortKeyVS`. None is reachable from the submitted constructor term, appears in either claim, or contributes to closure. `MPY-CONCRETE` is imported only into the LLVM runtime module and is absent from the Haskell proof definition.

The supplied semantics is intentionally a Python subset and does not model every exception or unsupported program. The submitted program uses none of those gaps: its range step is one, every prefix slice index is in the modeled range, the only source literal is ASCII, and it never performs float, sort, MD5, dict, set, comprehension, assertion, or out-of-bounds indexing operations. I found no rule that enables a false conclusion for any satisfying intended `str` input. Therefore there is no unsound-rule allegation requiring a false-conclusion witness.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

The reviewer-authored mutation keeps the valid loop circularity and changes the entry result from `ref(0)` to `ref(1)`. It changes a result-constraining obligation and is false in the clean initial configuration for every input; `S = .IntSeq` is a concrete satisfying witness.

First:

```text
kprove spec-vacuity.k \
  --definition audit-verification-rebuild-kompiled \
  --spec-module SPEC-VACUITY --dry-run --output none
```

exited 0, proving that the mutation parses and builds.

Then the same command without `--dry-run` exited 1 with `WarnStuckClaimState`. The residual terminal configuration contains `<k> ref(0) ~> .K </k>` and cannot unify with the mutated destination `ref(1)`. This is the expected unmet result obligation, not a parser error, import failure, timeout, crash, or unreachable mutation.

Evidence:

- [fresh mutation](evidence/stage6/spec-vacuity.k)
- [successful mutation dry run](evidence/stage6/vacuity-dry-run.log)
- [expected stuck proof](evidence/stage6/vacuity-proof.log)

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### Formally proven

Under the supplied MPY semantics and the proof-local mathematical definitions, for every finite `S:IntSeq`, starting from the clean module configuration:

1. the exact trusted-translated module loads;
2. its `all_prefixes` closure is called with `str(S)`;
3. if execution terminates, it returns `ref(0)`;
4. heap location 0 contains, in order, the slices `S[:1]` through `S[:isLen(S)]`;
5. the allocation counter becomes 1, the stack and return state are restored, no modeled exception remains, and the exit code is 0.

The auxiliary theorem proves the corresponding accumulator invariant for every `END <= STOP`, arbitrary existing accumulator, and arbitrary continuation. This is an unrestricted symbolic reachability proof, not a finite-size theorem.

### Assumed or empirically bridged

| Boundary | Influence | Assessment/evidence |
|---|---|---|
| K implementation, Haskell backend, SMT/integer/map/list hooks | proof checking and low-level mathematics | Normal foundational trust boundary; version and exact commands recorded |
| supplied MPY rules for module load, calls, scopes, lists, range, slicing, and strings | execution meaning of the submitted term | Acceptable selected-semantics boundary; candidate copy is exactly the trusted tree, and all used rules were statically audited |
| trusted `py2mpy.py` | Python AST to constructor representation | Trusted benchmark input; regeneration is byte-identical |
| `str(S:IntSeq)` as the Python-string value model | source/semantics intent bridge | Structural for len/slice and empirically supported on controls/Unicode by 3,333 differential cases; theorem is over the broader arbitrary-`IntSeq` model |
| typing-only import as a no-op and docstring as an inert expression | module namespace metadata, not return value | Acceptable and non-material; neither affects control, heap result, or function binding |
| trusted canonical implementation | differential oracle only | Finite supporting evidence, never substituted for the K proof |
| 22 supplied opaque float/MD5/sort symbols | none | Unreachable and dependency-free for both claims |

There is no externally trusted result-bearing primitive on the actual proof path, no empirical oracle inside the K theorem, and no informal summary-to-result jump. The summary-to-property bridge is established by truthful prefix-fold equations plus real loop execution.

Validation gates:

- Gate A, real-program soundness: PASS.
- Gate B, intent adequacy: PASS. The theorem covers arbitrary string length and all prefix-loop boundaries.
- Gate C, trust/evidence auditability: PASS. Commands, scripts, inputs, positive results, and negative mutations are preserved under `evidence/`.

The evidence recapture workflow itself is preserved as [rerun_and_capture.sh](evidence/rerun_and_capture.sh).

Stage 7 result: PASS.

VERDICT: PASS
LEGITIMACY: LEGIT
