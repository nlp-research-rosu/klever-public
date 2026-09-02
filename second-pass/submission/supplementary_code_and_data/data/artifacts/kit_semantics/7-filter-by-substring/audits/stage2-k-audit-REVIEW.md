# Independent adversarial review: 7-filter-by-substring

## Executive decision

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I rebuilt both definitions without
candidate caches, proved the helper circularity independently, proved the full
two-claim specification with the circularity retained, checked that the entry
claim embeds the parsed submitted program, reviewed every K declaration/rule,
and rejected a fresh false result postcondition on a satisfying input.

The proof-local theory has no operational bridge and no opaque result oracle.
Its only result summary, `filterAcc`, is a terminating mathematical definition
whose two guarded cases exactly mirror the fixed string-containment branch.
The loop claim connects that summary to actual execution of the loop and
`append`.

## 1. Input and provenance integrity

### Launcher record and layout

`/audit-input.json` declares:

- problem `7-filter-by-substring`;
- condition `kit-semantics`;
- record layout `pipeline-v3`;
- semantics mode `SUPPLIED_SEMANTICS`; and
- mounted inputs through its `container_paths` map.

The supplied-semantics mode agrees with the mounts:
`/reference/reference-semantics` exists and is a directory. There is no
mode/mount contradiction and therefore no audit-infrastructure breach.

All required pipeline-v3 records were present, readable, correctly typed, and
not symlinks:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `/generation/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- `/generation/codex-trace`, containing one regular JSONL trace.

The exact type checks and the independent SHA-256 of `/audit-input.json` are in
`evidence/31-record-layout-types.log`.

### Independent hashes and semantic-tree comparison

`evidence/01-provenance-check.log` independently recomputes every
launcher-recorded regular-file hash. All hashes match, including the trusted
canonical, prompt, translator, run/task/result manifests, all generation
records, the plain output log, and the raw structured-trace file.

The candidate prompt is byte-identical to `/reference/prompt.py`, and the
candidate translator is byte-identical to `/reference/py2mpy.py`.

The supplied semantics comparison is entry-by-entry, not a trust in the
launcher boolean:

- 25 entries exist in each tree;
- every relative name and entry type matches;
- every regular-file SHA-256 matches;
- neither tree contains a symlink, extra entry, missing entry, or special
  entry; and
- the reviewer-defined canonical manifest digest is identical for both trees:
  `be33a565bce2ab7be5268671512997fc361449f7c45dcfbc2b2195987ee59bf8`.

The launcher’s tree-hash serialization is not specified, so I did not pretend
that a differently serialized reviewer manifest should equal its tree digest.
Instead, the evidence records the complete per-entry comparison.

The six required candidate proof artifacts are regular files and no candidate
entry is a symlink (`evidence/23-candidate-source-inventory.log`). A second
reviewer-defined digest covers all 779 candidate entries, including the
candidate-built caches that were later ignored
(`evidence/27-candidate-tree-digest.log`).

### Generation records treated as claims only

I read all small JSON/text records directly. The structured trace was parsed
in full: 639/639 records parsed, with no malformed record
(`evidence/02-trace-inventory.log`). The 57,610-line plain output log was also
decoded and scanned in full (`evidence/22-generation-log-inventory.log`).
Their statements about `#Top`, differential tests, and `VALIDATED` were not
used as proof evidence.

Stage 1 result: **integrity gate passed**.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

The trusted prompt requires:

```python
filter_by_substring(strings: List[str], substring: str) -> List[str]
```

It must return, in original order and with duplicates preserved, exactly those
input strings containing `substring`. The examples require `[]` for an empty
input and `['abc', 'bacd', 'array']` when filtering
`['abc', 'bacd', 'cde', 'array']` by `'a'`.

The trusted canonical implementation is the direct list comprehension
`[x for x in strings if substring in x]`.

### Submitted implementation

`solution.py` uses an explicit loop. It allocates an empty result, iterates
over `strings`, appends `string` exactly when `substring in string`, and
returns the result. The extra initialization `string = ""` affects only the
loop variable on an empty input, not the returned value.

### Translation identity

In scratch, I ran the trusted mounted translator against the copied
`solution.py`. The regenerated file and submitted `solution.mpy` are
byte-identical:

```text
7e30ddefc3173507c5c5596732a66540c397b4e19f31fc16875b537954f934c7
```

Command, comparison status, and hashes are in
`evidence/04-translation-identity.log`.

### Independent differential testing

`evidence/differential_test.py` independently imports the trusted canonical
copy and generated implementation. It does not import candidate test code or
reuse K summary equations.

Its 6,570 cases cover:

- both documented examples;
- empty lists, empty strings, and the empty substring;
- exact, longer-than-string, prefix, suffix, middle, and absent substrings;
- repeats and duplicate list elements;
- combining characters, non-ASCII characters, emoji, NUL, and newline;
- exhaustive small products; and
- 5,000 deterministic generated cases.

The run exited 0 with zero mismatches. The exact scope and input-set digest are
in `evidence/05-differential-test.log`.

Stage 2 result: **program fidelity passed**.

## 3. Clean proof reconstruction

### Scratch isolation and toolchain

`evidence/setup_scratch.sh` created
`/tmp/audit-work/reconstruction` only if it did not already exist. It copied:

- candidate source/spec artifacts, but no `*-kompiled` directory, cache,
  parsed definition, or generated backend file;
- the trusted canonical, prompt, and translator; and
- the trusted `/reference/reference-semantics` tree, not a candidate-built
  definition.

The initial scratch listing is preserved in
`evidence/03-scratch-setup.log`.

`kup` is unavailable, but an independent system K installation is functional:
`kompile`, `krun`, and `kprove` are K v7.1.293
(`evidence/06-toolchain.log`). This follows the live-tooling route required by
the Kit skills.

### Fresh concrete definition

The LLVM definition was freshly built from the trusted source semantics as
`reviewer-runtime-kompiled`. Build exit status was 0
(`evidence/07-llvm-build.log`).

The compiler reported existing supplied-semantics exhaustiveness and
unused-variable warnings. None is a failed build, and none concerns a
proof-local rule.

The concrete smoke program contains the exact submitted function plus both
prompt assertions. `krun` exited 0 in a terminal configuration with:

- `<k> .K </k>`;
- `<exc> NoExc </exc>`;
- exit code `0`; and
- heap results for both the empty and documented-example calls.

The complete bounded terminal configuration is in
`evidence/08-concrete-smoke.log`.

### Fresh proof definition and positive claims

The Haskell definition was freshly built as
`reviewer-verification-kompiled`; build exit status was 0
(`evidence/09-haskell-build.log`).

`SPEC.filter-loop` was selected with its correct qualified label. It printed
`#Top` and exited 0 (`evidence/12-kprove-filter-loop.log`).

An initial diagnostic selected only `SPEC.filter-by-substring`. K’s
`--claims` option removes all unselected claims, so that command removed the
`SPEC.filter-loop` circularity required by the entry proof and began
unbounded symbolic loop execution. I interrupted it and recorded it as a
diagnostic, not a proof result, in
`evidence/12-kprove-filter-by-substring.log`. Earlier unqualified selectors
were also preserved as selector errors; they are not treated as claim
failures.

The correct complete target command retained both claims:

```bash
kprove spec.k \
  --definition reviewer-verification-kompiled \
  --spec-module SPEC
```

It printed literal `#Top` and exited 0
(`evidence/15-kprove-spec-all.log`). Thus both positive target claims close in
the same theory, with the entry claim able to use the independently closing
loop circularity.

The three candidate positive ground value claims also printed `#Top` and
exited 0 (`evidence/16-kprove-value-checks.log`). Reviewer-authored ground
domain/result witnesses did the same
(`evidence/17-kprove-ground-witnesses.log`).

Stage 3 result: **clean reconstruction passed**.

## 4. Adequacy and real-program pinning

### Plain-language meaning of the claims

`SPEC.filter-loop` says:

> If the active computation is the exact submitted `for` loop over a remaining
> semantic list `VS`, every remaining element is a semantic string, the local
> result variable points to heap list `ACC`, and the local substring is
> `str(P)`, then the loop consumes its computation and changes that heap list
> to `filterAcc(ACC, P, VS)`. The loop variable may finish at an existential
> value; all framed state is preserved.

Its precondition is `allStrVS(VS)`. The accumulator may contain arbitrary
values, which is sound because the loop only appends selected suffix elements.
The broader arbitrary accumulator/outer-map/continuation domain does not
assert a false result.

`SPEC.filter-by-substring` says:

> Starting from the standard MPY module configuration, load the exact submitted
> module and call its `filter_by_substring` closure on `list(VS)` and `str(P)`.
> If every element of `VS` is a semantic string, execution returns `ref(0)`;
> heap location 0 contains `list(filterAcc(.ValSeq, P, VS))`; module binding,
> allocation counter, stack, return state, exception state, and exit code have
> the stated final values.

The result is not a free variable or implication-only condition. It is fixed
at a concrete heap location and constrained by a recursively defined ordered
filter.

### Parsed program identity

I extracted the `Module(...)` term inside the entry claim’s `#loadAll`,
normalized only explicit internal empty-list units to surface syntax, and
parsed both it and submitted `solution.mpy` with `kast` under the fresh
definition. Their canonical KORE hashes are identical:

```text
be8f02aa9f0bbd39833300501563318aba7965452ff8c92e1ccd7655d9c0b595
```

See `evidence/program_pinning.py` and
`evidence/30-program-pinning-normalized.log`. This establishes syntactic
pinning independently of visual similarity.

The separately rerun body mutation changes `in` to `not in` while retaining
the original expected result for `["a"], "a"`. It exits 1 with
`WarnStuckClaimState` and a residual empty result list
(`evidence/20-body-mutation-proof.log`). The proof is therefore sensitive to
the material body computation.

### Satisfiable preconditions and concrete substitution

`VS = .ValSeq` satisfies both claims’ `allStrVS(VS)` precondition. The
documented four-string semantic sequence is a nonempty satisfying witness.
Both are machine-checked in `evidence/spec-ground-witness.k`; the witness
module printed `#Top`.

For the empty witness and pattern `"a"`, `filterAcc` reduces to `.ValSeq`,
matching both Python implementations. For the documented nonempty witness and
pattern `"a"`, it reduces to the code-sequence representation of
`["abc", "bacd", "array"]`, also matching both Python implementations.
The K reductions are in `evidence/17-kprove-ground-witnesses.log`; the Python
results are in `evidence/05-differential-test.log`.

The loop claim’s existential final `string` binding is harmless: that local
value is not the returned result, and the whole-program claim pops the function
frame.

Stage 4 result: **adequacy and real-program pinning passed**.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k-rule-inventory.tsv` inventories every top-level declaration in all
25 supplied-semantics entries, `verification.k`, and `spec.k`, with file,
line, kind, attributes, and full logical block. It contains:

- 230 syntax declarations;
- 703 rules;
- 5 contexts;
- 1 configuration;
- 2 reachability claims; and
- all module/import/require declarations.

The attribute pass found 158 function declarations, 117 `total`
declarations, 22 `no-evaluators` declarations, 25 symbols, 45 priority rules,
35 concrete rules, 27 `owise` rules, and 3 simplification rules. No
`functional` declaration is present.

`evidence/k-rule-decisions.tsv` adds a decision and rationale to every one of
the 1,227 inventoried rows. It distinguishes fixed active rules, fixed
inactive rules, concrete-only rules, inactive opaque primitives,
proof-local definitions, the proof-local derived lemma, structural
declarations, and the two claims. Generation hashes and class counts are in
`evidence/24-k-inventory-v2.log` and
`evidence/26-k-rule-decisions-v2.log`.

### Configuration, syntax, and reachable-rule mapping

The configuration has the expected computation, current environment, scope
store, scope allocator, heap, heap allocator, call stack, return state,
exception state, and exit code. The entry claim fixes every observable
program-final cell; the helper claim frames cells it does not change.

| Submitted construct | Declaration and fixed behavior | Review |
|---|---|---|
| `Module`, `ImportFrom` | `syntax.k`; `core.k` load/sequencing; `controls.k` unsupported-import no-op | `typing.List` is unused at runtime, so the no-op is adequate here. |
| `FuncDef`, call, return | `functions.k` closure/bind/return/pop; `call.k` callee/argument/frame rules | Binding, left-to-right arguments, frame creation, return, cleanup, and continuation are executed, not summarized by a local bridge. |
| `Assign`, `Name`, `Str("")` | `controls.k`, `core.k`, `str.k` | Local bindings and empty ASCII literal are modeled directly. |
| `ListExpr` | `list.k` evaluation and `#alloc` | The result is a fresh heap object at location 0 in the entry claim. |
| `For` | `controls.k` `#loop`; `list.k` iterator; `tuple.k` name target binding | Iteration consumes one head at a time, updates `string`, executes the body, and returns to the exact loop head used by the circularity. |
| `substring in string` | `operators.k`; `str.k` `applyCmp`, `strPrefix`, `strContains` | Operands evaluate in order and contiguous substring membership controls the branch. |
| `result.append(string)` | `call.k` attribute/callee routing; priority-40 `list.k` append | The mutating rule preempts generic bound-method evaluation and updates exactly the referenced heap list. |
| `If` and expression statement | `controls.k` branch and value-discard rules | True/false control is complete; append’s `noneV` is discarded. |

The active priorities are fixed-semantics dispatch priorities. In particular,
the specialized append mutation correctly preempts the generic bound-method
route. `verification.k` adds no priority or ordinary operational rule.

### Proof-local extensions

#### `strCodes`

Class: definitional summary. It does not replace execution.

- `strCodes(str(S)) = S`.
- The `owise` equation returns `.IntSeq` on every disjoint non-string
  constructor.
- The `[total]` declaration is therefore covered.
- Its only result influence is through the input-domain predicate, the guarded
  equality normalization, and `filterAcc`.

The opposite concrete interpretation was rejected with residual
`iCons(97, .IntSeq)` (`evidence/21-opposite-projection-proof.log`).

#### `allStrVS`

Class: definitional summary. Its empty and `vCons` equations exhaust
`ValSeq`, recurse on a strict tail, and say that every head equals the string
reconstructed from `strCodes`. Constructor disjointness makes this true
exactly for semantic strings. It changes no state and appears only in
preconditions.

#### Guarded `applyCmp` simplification

Class: derived lemma, not an operational bridge.

It rewrites:

```k
applyCmp("in", str(P), V)
```

to the same fixed operation with right operand `str(strCodes(V))`, only under
the guard that `V` equals that operand. This is equality congruence. On overlap
with fixed `MPY-STR`, `V = str(S)` and `strCodes(str(S)) = S`, so both routes
agree. The rule reads/writes no cell, changes no continuation, chooses no
membership result, and leaves the fixed `strContains` computation in place.

#### `filterAcc`

Class: definitional summary. It never matches a program computation.

- The empty suffix returns the accumulator.
- On a string head, the contained and excluded guards are Boolean
  complements.
- The contained case appends exactly the original head.
- The excluded case preserves the accumulator.
- Both recurse on the strict tail.
- It is deliberately not marked `total` outside the string-head domain, while
  every theorem use is covered by `allStrVS`.

There is no overlap disagreement, non-descent, fabricated value, or task-answer
oracle.

#### `SPEC.filter-loop`

Class: derived reachability claim/circularity. It matches the exact loop
syntax, local bindings, heap result object, and any explicitly framed
continuation/state. Its justification domain is its complete match domain
because the claim itself is universally machine-checked under fixed semantics.
It reads the suffix/pattern/accumulator, updates the loop variable and result
heap list, consumes only the loop, and preserves framed state. It introduces
no abrupt return or exception.

### Fixed-semantics totality and opaque boundaries

The fresh builds warn that several supplied total functions are not
equationally exhaustive over their declared broad sorts, including
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. On missing
cases they remain total but uninterpreted; that is an under-specification, not
a false equation. None is reachable from this program or present in its
postcondition. I therefore record the narrower evidence limitation rather
than label any such rule unsound.

The 22 fixed `no-evaluators` declarations cover float operations, sorting, and
MD5. They likewise remain uninterpreted on the proof side. None influences
this theorem’s control, state, return, `filterAcc`, or precondition.

I found no inconsistent overlap among active rules, no priority that bypasses
the submitted body, and no local rule encoding the requested answer. Because
there is no operational bridge or program-derived opaque abstraction, the
validation skill’s bridge-free connection-theorem obligation is not
triggered.

Stage 5 result: **static soundness gate passed**.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The reviewer-authored
`evidence/spec-reviewer-vacuity.k` executes the exact submitted program on the
satisfying input:

```python
strings = ["abc"]
substring = "a"
```

The real and formally summarized result is `["abc"]`. The mutation instead
requires the final result heap object to be empty.

First, a `kprove --dry-run` parsed and built the mutation successfully, exiting
0 (`evidence/18-vacuity-dry-run.log`). The actual proof then exited 1 with
`WarnStuckClaimState` (`evidence/19-vacuity-proof.log`).

The residual is the expected unmet obligation, not an unrelated error:

- computation has terminated at `ref(0)`;
- stack is empty, return state is `noRet`, exception is `NoExc`, and exit code
  is 0; and
- heap location 0 contains the code-sequence representation of `["abc"]`,
  which cannot unify with the mutated empty result.

This is a reachable, result-constraining failure.

Stage 6 result: **fresh non-vacuity gate passed**.

## 7. Proven-versus-assumed accounting

### What the reachability proof establishes

Under the supplied MPY theory, for every finite semantic sequence `VS` whose
elements are all `str(...)` and every pattern code sequence `P`, execution of
the exact submitted translated module and function call on `list(VS), str(P)`
has the stated partial-correctness result:

- it returns `ref(0)`;
- heap location 0 is exactly
  `list(filterAcc(.ValSeq, P, VS))`;
- `filterAcc` preserves order and duplicates and includes exactly heads for
  which supplied `strContains(P, headCodes)` is true;
- the module closure is the exact submitted body;
- the function frame is removed;
- the heap allocator is 1;
- the stack is empty;
- the return state is reset;
- no modeled exception is present; and
- exit code is 0.

This is a reachability/partial-correctness result, not a separately stated
liveness theorem.

### Trust and assumption ledger

1. **K v7.1.293 frontend, Haskell backend, LLVM backend, builtin theories, and
   solver stack.** These are the machine-checking trust base. The independent
   audit rebuilds and polarity tests them but does not prove the tools.

2. **Trusted supplied MPY semantics.** Integrity is exact, and I statically
   reviewed every declaration/rule. The current theorem depends only on the
   active slice mapped in Stage 5. The semantics is intentionally a Python
   subset; behavior outside that subset is not claimed.

3. **Trusted `py2mpy.py`.** The task design declares this translator trusted.
   I checked byte identity of the submitted translation and parsed identity of
   the program embedded in the claim. Those checks do not prove the translator
   correct for all Python.

4. **External-input representation.** The theorem supplies the read-only
   input as an unboxed semantic `list(VS)` and strings as `str(IntSeq)`.
   Python normally represents a list object with identity. This program never
   mutates, aliases, compares identity of, or returns the input object, so the
   representation difference has no observable effect on the requested
   result. The theorem directly covers arbitrary `IntSeq` strings.

5. **String/int-sequence intent bridge.** Supplied `strContains` is a complete
   contiguous-sequence definition, which is the prompt property. The concrete
   literal loader is ASCII-only, but the only program literal is `""`; external
   symbolic inputs range over arbitrary code sequences. Python differential
   tests include non-ASCII inputs. This is adequate for this theorem, though
   it is not an exhaustive proof of CPython Unicode implementation details.

6. **Inactive fixed opaque symbols.** The proof definition contains supplied
   opaque/total primitives for `intFloatDiv`, `divII`, `floatMod`, `floatLt`,
   `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`,
   `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
   `sqrtF`, `sortVS`, `sortKeyVS`, and `md5hexCodes` (with related broad
   total symbols `floorFI`, `toF`, and `ceilF`). None is reachable or
   result-bearing here. No conclusion in this review is conditional on an
   interpretation of them.

7. **Empirical bridge only where stated.** The 6,570-case differential run and
   LLVM smoke execution support implementation-to-intent and concrete
   execution fidelity on tested inputs. They are not substitutes for the
   universal K reachability proof.

### Final rationale

The reconstructed target proof closes, constrains the actual returned heap
object, embeds the real submitted program, rejects both a material body change
and a fresh false result, and uses only sound proof-local definitions/lemmas.
The supplied semantics has documented inactive under-specification and opaque
primitives, but none can affect this theorem. The remaining trust boundaries
are ordinary for a supplied-semantics K proof and create no material adequacy
gap for the stated `List[str]`, `str` contract.

VERDICT: PASS
LEGITIMACY: LEGIT
