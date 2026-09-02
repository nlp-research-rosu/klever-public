# Independent adversarial audit — HumanEval 159 `eat`

The candidate contains a legitimate partial-correctness proof of the submitted
program over the complete source-contract domain. This conclusion comes from a
fresh build and proof, not from the candidate's compiled directories,
`PROOF.md`, trace, or reported `#Top`.

## 1. Input and provenance integrity

The launcher declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `159-eat`, and condition
`kit-semantics`. The trusted `/reference/reference-semantics` mount is present,
so the mount boundary agrees with the rendered semantics mode.

I read `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
`/task.json`, `/generation-result.json`, every required pipeline-v3 record in
`/generation-evidence`, the 13,779-line `codex-output.log`, and the one
structured JSONL trace. The generation records were treated only as untrusted
history. In particular, their `VALIDATED` and `#Top` assertions played no role
in the result below.

The independent checker and complete output are
[`integrity_check.py`](/audit-output/evidence/integrity_check.py) and
[`01-integrity.log`](/audit-output/evidence/01-integrity.log). Its findings:

- The campaign-lock SHA-256 is
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
  exactly the recorded value, and the parsed lock object exactly equals the
  `audit_campaign` object in `/audit-input.json`.
- All required pipeline-v3 files are regular, readable, non-symlink files.
  Every launcher-recorded per-file hash checked by the script matches its
  mounted bytes. This includes the run/task/result manifests, invocation,
  metrics, runtime metrics, usage, prompt, last response, and complete output
  log.
- The structured trace has one regular JSONL file, SHA-256
  `64f6295a6fd8b4101be49a9d0b191c8a126ebc180a3ace4d23fc2999d073906a`,
  with 163 parseable records and zero parse errors. It contains 23 function-call
  records and a normal task-complete record.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts. Their hashes are respectively
  `4987cbdc1f933a0ea2354c67044dcc9cc479c47c6c0375f63498f5c11b7daa85`
  and
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- Recursive type/path/content comparison found exactly 25 entries in each
  supplied-semantics tree, no symlink or special entry, no missing or extra
  entry, and no byte difference. This satisfies the condition-specific
  semantics-integrity gate.
- The six required candidate proof artifacts are regular, non-symlink files.
  The independently hashed full candidate tree has 777 entries and no
  non-regular entries.

There is no provenance or mount breach. I copied only candidate proof/program
sources plus trusted prompt, canonical, translator, and semantics sources into
`/tmp/audit-work/159-eat`. Candidate `runtime-kompiled`,
`verification-kompiled`, Python caches, logs, and prose were not used to build
or prove anything.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract says that `number`, `need`, and `remaining` are integers
in the inclusive range 0 through 1000. The result is a two-element list:

- if `need <= remaining`, eat exactly `need` and return
  `[number + need, remaining - need]`;
- otherwise eat all stock and return `[number + remaining, 0]`.

The trusted canonical implements exactly that split. Candidate `solution.py`
uses the same expressions and differs only by omitting the canonical's explicit
`else` after an unconditional return.

The fidelity driver
[`02-fidelity.sh`](/audit-output/evidence/02-fidelity.sh) regenerated the MPY
program with `/reference/py2mpy.py`. The command exited 0, `cmp` exited 0, and
both submitted and regenerated files have SHA-256
`49f9697d0fa8809c3144fc5b812d49e68db0cdbb56b74617e8c089e0a8c6e78a`.
The exact record is
[`02-fidelity.log`](/audit-output/evidence/02-fidelity.log).

The independent differential script
[`differential_test.py`](/audit-output/evidence/differential_test.py) imports
the trusted canonical entry point and the scratch generated entry point by
separate file paths. It checks the four examples, all 64 selected domain
corners, 12,004 cases at `need == remaining` and its valid neighbors, every
triple in `[0,20]^3`, and 20,000 deterministic generated triples. This includes
the all-zero analogue of an empty boundary and both branches at 0 and 1000.
The exact 41,333 inputs are preserved in
[`differential-inputs.json`](/audit-output/evidence/differential-inputs.json),
SHA-256
`bea2d89aefa1d0d43c617045738b5aedb08776cc8152302624121decb9390a02`.
Both implementations and an independently written piecewise formula agreed on
every case: zero result, shape, or formula mismatches.

## 3. Clean proof reconstruction

The exact fresh commands are preserved in
[`03-reconstruction.sh`](/audit-output/evidence/03-reconstruction.sh), with
bounded output and individual statuses in
[`03-reconstruction.log`](/audit-output/evidence/03-reconstruction.log).
They used the trusted semantics copied from `/reference`, and wrote new
`fresh-runtime-kompiled` and `fresh-verification-kompiled` directories.

The concrete build was:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

It exited 0. The reviewer program
[`03-concrete-tests.py`](/audit-output/evidence/03-concrete-tests.py) was
translated by the trusted translator and executed with:

```bash
krun fresh-concrete-tests.mpy --definition fresh-runtime-kompiled
```

It exited 0 at `.K`, `NoExc`, exit code 0. Its seven heap results were
`[11,4]`, `[11,0]`, `[7,0]`, `[0,0]`, `[1000,1000]`, `[1000,0]`, and
`[2000,0]`, covering normal, equal-stock, insufficient, zero, and maximum
boundaries.

The proof build was:

```bash
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

It exited 0. I then ran all positive claims together and each labeled target
separately:

```bash
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC \
  --claims SPEC.eat-enough
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC \
  --claims SPEC.eat-insufficient
```

Each command printed `#Top` and exited 0. Thus no combined invocation can hide
an unproved target.

The fresh compilers emitted warnings about unused tail variables in generic
string-order rules. The LLVM build additionally reported incomplete `[total]`
coverage for generic helpers such as `mapStrVS`, float conversions,
`joinCodes`, and `valSeqAt`. None of these declarations or constructors is in
the target dependency slice. They neither matched nor supplied a logical
premise to these proofs; they are documented fixed-semantics scope limitations,
not candidate proof rules or failed target obligations.

## 4. Adequacy and real-program pinning

`SPEC.eat-enough` assumes all three symbolic integers are in `[0,1000]` and
`NEED <= REMAINING`. It proves that the call returns `ref(0)`, whose fresh heap
entry is exactly
`[NUMBER + NEED, REMAINING - NEED]`.

`SPEC.eat-insufficient` has the same full numeric domain and assumes
`NEED > REMAINING`. It proves a fresh heap entry exactly
`[NUMBER + REMAINING, 0]`.

Together the guards are disjoint and exhaustive over the prompt domain. Both
claims also constrain environment 0, the exact `eat` binding, the two scopes,
`scopeLoc`, empty initial/final stack, empty-to-singleton heap allocation,
`heapLoc`, return state, exception state, and exit code. The result is not a
free variable, implication-only summary, or tautology.

The claims manually embed a closure rather than loading the whole MPY module.
That is adequate here because
[`pinning_check.py`](/audit-output/evidence/pinning_check.py) mechanically
extracts both closure bodies, normalizes only the parser's two spellings of the
empty `Stmts` list, parses each as a complete MPY function with the fresh K
definition, and compares complete JSON KAST objects with `solution.mpy`.
All three hashes are
`8cea70eb3d2559d98baaa44fe9d977cbd33cc391aa40da898afde7e7067a3963`;
both constructor comparisons are `True`. See
[`04-pinning.log`](/audit-output/evidence/04-pinning.log).

There are no helper or loop claims and no loop. Every material operation in
the real body executes under fixed semantics. A separate reviewer body
mutation, [`04-body-mutation.k`](/audit-output/evidence/04-body-mutation.k),
changes the actually installed enough-branch body to add one extra carrot.
`kprove` reaches heap `[12,4]` for `(5,6,10)`, becomes stuck against expected
`[11,4]`, and exits 1. This is body sensitivity of the executed claim term, not
merely a changed external source file.

Both preconditions are satisfiable. The independent witness output in
[`04-claim-witnesses.log`](/audit-output/evidence/04-claim-witnesses.log)
shows:

- `(5,6,10)` satisfies the enough claim and gives claimed, canonical, and
  generated result `[11,4]`;
- `(2,11,5)` satisfies the insufficient claim and gives `[7,0]` in all three.

The manual body duplication is an artifact-maintenance risk for future edits,
but trusted regeneration plus the constructor comparison resolves identity for
this immutable candidate.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[`rule-inventory.md`](/audit-output/evidence/rule-inventory.md), generated by
[`rule_inventory.py`](/audit-output/evidence/rule_inventory.py). It contains
one row with location, complete guarded source, attributes, dependency
decision, and rationale for every local block:

- 695 ordinary or attributed rules;
- 227 syntax declarations;
- five evaluation contexts;
- one configuration;
- two target claims;
- 146 function-bearing declarations, 107 with `total`;
- 45 priority-bearing blocks, 26 `owise` blocks, and 35 concrete blocks;
- 25 symbol-bearing declarations, 22 with `no-evaluators`;
- zero `functional` declarations and zero simplification rules.

`verification.k` contributes zero blocks: it only imports `MPY`. `spec.k`
contributes only the two target claims. There is therefore no proof-local
function, lemma, equation, priority rule, simplifier, operational bridge,
oracle, auxiliary claim, or answer-encoding rule to audit. A search of the
trusted semantics found no `eat`, carrot, problem-159, or task-variable hook.

The complete target rule map is
[`critical-slice.md`](/audit-output/evidence/critical-slice.md). In summary:

- the call layer evaluates the bound callee, then the three arguments
  left-to-right;
- lookup selects the explicitly pinned closure and then the three exactly
  bound parameters;
- the call rule creates one fresh callee scope, preserves the continuation,
  and pushes one frame;
- `Compare` evaluates left then right and `<=` dispatches to ordinary
  unbounded integer comparison;
- `If` uses the resulting Boolean and selects exactly one branch;
- generated `seqstrict` rules and integer dispatch implement the three
  branch-result additions/subtractions in left-to-right order;
- `ListExpr` evaluates exactly two elements, preserves order, and `#alloc`
  writes the only fresh heap entry;
- `Return` discards the unreachable fallback in the enough branch, then
  `#pop` restores the caller environment, removes the callee scope, restores
  `scopeLoc`, and returns the allocated reference;
- no rule on the path changes exception or exit-code cells.

Every relevant equation has disjoint constructor or Boolean guards, recursive
helpers (`appendVal` and `vals2valSeq`) structurally descend, and the reachable
total functions cover their complete reachable algebraic domains. The relevant
priorities do not preempt real work; no result-bearing abstraction occurs.

Rows marked `FIXED-UNREACHED` are generic parts of the exact trusted
supplied-semantics tree. Their left-hand AST constructor or internal
continuation cannot be produced from either claim's closure body. This includes
all dictionaries, floats, strings, methods, iteration, sorting, MD5, slicing,
comprehensions, assertions, and concrete-only keyed-sort rules. They cannot
rewrite a target state or enable a false target conclusion. The fixed semantics
is intentionally a partial Python subset, so rules outside their documented
supported inputs are not silently imported as claims about this program.

The 25 opaque symbols are `sortVS`, `sortKeyVS`, `md5hexCodes`, and the float
symbols `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `floorFI`,
`toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
`decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and
`sqrtF`. None occurs in `solution.mpy`, either claim, or any reachable internal
term. Consequently no claim branch, result, state cell, exception, or
postcondition depends on an arbitrary interpretation of one.

No rule used by the target encodes the desired answer, fabricates an
unmodeled used result, skips a program-defined computation, or broadens a
justification context. No false-conclusion witness exists for a relevant rule;
the direct Python/K concrete comparisons instead agree on both branch and
boundary witnesses.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The fresh mutation is
[`06-nonvacuity.k`](/audit-output/evidence/06-nonvacuity.k). It retains the
symbolic enough-stock precondition and actual closure body but changes the
first heap result from `NUMBER + NEED` to `NUMBER + NEED + 1`.
`(5,6,10)` is a satisfying witness: the mutation demands 12 while execution
returns 11.

The exact driver is
[`06-nonvacuity.sh`](/audit-output/evidence/06-nonvacuity.sh). First:

```bash
kprove audit-nonvacuity.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-NONVACUITY \
  --dry-run --output none
```

exited 0, proving the mutation parsed and compiled to KORE. The real proof
command then exited 1 with `WarnStuckClaimState`. Its residual says the terms
unify but the implication fails and displays the unmet equality:

```text
NUMBER +Int NEED +Int 1 #Equals NUMBER +Int NEED
```

The wrapper verifies both expected diagnostics and exits 0. The bounded and raw
records are
[`06-nonvacuity.log`](/audit-output/evidence/06-nonvacuity.log) and
[`06-nonvacuity-raw.log`](/audit-output/evidence/06-nonvacuity-raw.log).
This is a reachable result failure, not a parser error, timeout, missing import,
or unrelated backend crash.

## 7. Proven versus assumed accounting

What is machine proved: relative to the exact supplied `MPY` definition, for
every K integer triple in the prompt's inclusive bounds, if the call terminates,
the fresh returned list and all explicitly mentioned state cells have exactly
the branch-specific values stated in Section 4. Both branch claims close
individually. This is partial correctness; no separate liveness theorem is
claimed.

Trust and evidence ledger:

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied `MPY` rules for call, lookup, integer comparison/arithmetic, branch, list allocation, return, and cleanup | Both K claims | Acceptable fixed-semantics boundary. The candidate copy is byte-identical to the trusted mount, the complete relevant slice was reviewed, and concrete LLVM observations agree. |
| K built-in unbounded integers, Booleans, maps/lists, generated strictness, Haskell backend, SMT integration, and `kprove` | Formal closure and arithmetic side conditions | Conventional toolchain trust. Fresh K v7.1.293 builds and three positive proof invocations were used. |
| Trusted `py2mpy.py` as source-to-constructor translation | Real-program identity | Not formally proved correct. Mitigated by byte-identical trusted regeneration, direct source inspection, exact KAST equality for both closure bodies, body mutation, and differential evidence. |
| Human reading of the list heap as the prompt's two-element returned array | Intent bridge | Direct in this semantics: ordered `vCons` pairs are the modeled list payload, and `ref(0)` points to that exact fresh heap entry. |
| Trusted canonical Python and reviewer piecewise formula | Implementation-to-intent evidence | Finite evidence only: 41,333 exact recorded cases with zero mismatches. It supplements but does not replace the universal K claims. |
| The 25 generic opaque supplied symbols listed in Section 5 | None | Acceptable because they are absent from the entire reachable proof slice and have no dependent target fact. |
| Termination | None in the partial-correctness theorem | Not assumed to derive the postcondition. The straight-line concrete executions terminate, but no total-correctness claim is made. |

There are no proof-local assumptions, trusted claims, lemmas, simplifications,
or empirical result oracles. The only informal maintenance bridge—source to the
manually embedded closure body—was discharged mechanically for the immutable
artifacts. The formal domain is not narrowed, both material branches are
covered, the postcondition is exact and discriminating, and the relevant
semantics executes every operation.

VERDICT: PASS
LEGITIMACY: LEGIT
