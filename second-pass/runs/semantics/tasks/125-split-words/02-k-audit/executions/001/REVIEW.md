# Independent adversarial review: 125-split-words

This review was performed from source in `/tmp/audit-work`, using K
v7.1.337. Candidate caches, archives, logs, and prebuilt artifacts were not
used. The rendered mode is `SUPPLIED_SEMANTICS`; the trusted supplied semantics
mount is present, so there is no mode/mount infrastructure contradiction.
Reviewer artifacts and bounded logs are hashed in
`evidence/MANIFEST.sha256`.

The candidate's three target claims do freshly produce `#Top`, and a false
off-by-one postcondition is rejected. Those facts are not sufficient for
legitimacy. Five priority rules in `verification.k` replace the fixed branch
semantics while ignoring the branch Boolean. Ground counterexamples show that
each rule proves the opposite of the fixed semantics on an ordinary string
state. In addition, the formal entry calls a proof-local copy of the function
body rather than consuming `solution.mpy`, and the implementation/postcondition
materially disagree with the trusted canonical implementation. The result is
therefore `FAIL / NOT_LEGIT`.

## 1. Input and provenance integrity

### Mode boundary

- Rendered mode: `SUPPLIED_SEMANTICS`.
- `/reference/reference-semantics` exists as a real directory.
- The candidate `reference-semantics/` tree and the trusted tree have identical
  entry names, entry types, and bytes. `diff --recursive --no-dereference`
  returned 0. There are no symlinks in either tree.
- The candidate prompt and translator are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- This consistency means the audit is not an `AUDIT_ERROR`. The trusted
  supplied tree does not bless the candidate's rules in `verification.k`.

Evidence: `evidence/stage1_integrity.sh` and
`evidence/stage1-integrity.log`.

### Missing and extra provenance artifacts

The following expressly requested artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured generation trace is present under the checked conventional names
(`generation-trace.json`, `generation-trace.jsonl`,
`structured-generation-trace.json`, or `trace.json`).

The proof sources (`solution.py`, `solution.mpy`, `spec.k`,
`verification.k`), candidate prompt/translator, and supplied-semantics entries
are regular files. Candidate-only untrusted extras include
`__pycache__/`, `kore-exec.tar.gz`, `concrete_tests.py`,
`concrete_tests.mpy`, `prove.sh`, and `prove-output.log`. They were inspected
only as claims and then ignored during reconstruction. In particular, neither
the archive nor any candidate-built cache was extracted or reused.

The missing records are provenance failures, but they do not prevent an
independent source reconstruction.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The prompt says:

1. if whitespace exists, split into words on whitespace;
2. otherwise, if a comma exists, split on commas;
3. otherwise, return the count of lowercase letters at odd zero-based alphabet
   positions (`b`, `d`, ..., `z` for ASCII).

The trusted canonical implementation makes this operationally precise:

1. it enters the whitespace branch only when literal ASCII space `" "` occurs,
   then calls `txt.split()`;
2. otherwise, if `","` occurs, it evaluates
   `txt.replace(",", " ").split()`, which drops leading, trailing, and repeated
   empty fields;
3. otherwise, it counts every character for which `islower()` is true and
   `ord(character) % 2 == 0`.

The candidate instead:

1. enters the first branch for any occurrence of space, tab, newline, or
   carriage return;
2. calls `txt.split(",")`, preserving empty comma fields;
3. counts only the thirteen literal ASCII characters `bdfhjlnprtvxz`.

### Trusted translation

Running the trusted translator afresh over `solution.py` produced a file
byte-identical to the submitted `solution.mpy`. Both SHA-256 hashes are:

`0893ed55c993d253598f623b2cda9937139d072dfdab2dcd58fb4eeb791fb218`

Evidence: `evidence/stage2-translation.log`.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry and the generated entry. Its complete input set is preserved in
`evidence/differential-inputs.json`; every result is preserved in
`evidence/differential-results.json`.

The 2,039 deduplicated inputs comprise:

- all three documented examples;
- empty input and explicit delimiter boundaries;
- leading, trailing, adjacent, and repeated delimiters;
- every string of length 0 through 4 over
  `{a, b, comma, space, tab, vertical-tab}`;
- 500 deterministic generated strings (seed 125, lengths 0 through 24) over
  letters, digits, punctuation, several whitespace characters, and selected
  Unicode lowercase characters.

Result: 1,159 matches and **880 mismatches**; the script exited 1 as intended
when mismatches were found. Representative material divergences are:

| Input | Trusted canonical | Candidate |
|---|---|---|
| `"a\tb"` | integer `1` | list `["a", "b"]` |
| `"a\nb"` | integer `1` | list `["a", "b"]` |
| `","` | list `[]` | list `["", ""]` |
| `"a,,b"` | list `["a", "b"]` | list `["a", "", "b"]` |
| `"ê"` | integer `1` | integer `0` |

All documented examples and empty input agree. The divergences are nevertheless
part of the intended Python string domain and are not cosmetic.

Evidence: `evidence/stage2-differential.log`,
`evidence/differential-inputs.json`, and
`evidence/differential-results.json`.

Stage 2 result: **FAIL** for implementation-to-canonical fidelity.

## 3. Clean proof reconstruction

Only the following were copied into `/tmp/audit-work/candidate-src`:

- trusted `/reference/reference-semantics`;
- candidate source files `solution.py`, `solution.mpy`, `spec.k`, and
  `verification.k`;
- trusted `py2mpy.py`, `prompt.py`, and `canonical.py`.

No candidate kompiled directory, cache, archive, or executable was copied.

### Concrete definition

Fresh LLVM compilation used:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. `krun solution.mpy` exited 0 with `.K`, `NoExc`, and exit code 0.
An independent probe, `evidence/concrete_probe.py`, contains an AST-identical
copy of the submitted function plus normal and boundary assertions for all
three branches. The trusted translator generated the probe's `.mpy`; both
ordinary Python and fresh `krun` executions exited 0.

Evidence:

- `evidence/stage3-probe-translation.log`
- `evidence/stage3-kompile-llvm.log`
- `evidence/stage3-krun-solution.log`
- `evidence/stage3-python-probe.log`
- `evidence/stage3-krun-probe.log`

### Proof definition and positive claims

Fresh Haskell compilation used:

```text
kompile verification.k --backend haskell \
  --main-module SPLIT-WORDS-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0. Every target claim was then selected and run independently:

| Claim | Exit | Required output |
|---|---:|---|
| `SPEC.whitespace` | 0 | `#Top` |
| `SPEC.comma` | 0 | `#Top` |
| `SPEC.odd-lowercase-count` | 0 | `#Top` |

Evidence:

- `evidence/stage3-kompile-haskell.log`
- `evidence/stage3-kprove-whitespace.log`
- `evidence/stage3-kprove-comma.log`
- `evidence/stage3-kprove-count.log`

The compiler also reported non-exhaustive `[total]` matches for `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. None of those functions
is reached by this submitted function or its entry claims. This is a narrower
unused-semantics coverage gap, not an unsoundness finding for this theorem;
there is no false conclusion witness from those warnings on the submitted
path.

Stage 3 result: **PASS for mechanical reconstruction**, but `#Top` is under
the candidate-extended theory and is subject to Stages 4 and 5.

## 4. Adequacy and real-program pinning

### Plain-language claims

All formal inputs are internal `str(CS:IntSeq)` values.

- `whitespace`: if the sum of occurrences of codes 32, 9, 10, and 13 is
  positive, calling the proof-local closure returns `ref(0)`, allocates at heap
  location 0 the list produced by `splitWS`, and advances `heapLoc` from 0 to 1.
- `comma`: if the modeled whitespace sum is non-positive and the comma
  occurrence count is positive, the call returns `ref(0)`, allocates the
  `splitSep` result at heap location 0, and advances `heapLoc` to 1.
- `odd-lowercase-count`: if the modeled whitespace and comma counts are
  non-positive, the call returns the sum of occurrences of the thirteen ASCII
  codes for `b,d,...,z`, with no heap allocation.

Because `cntSub` is mathematically nonnegative on finite sequences, the
non-positive premises intend zero counts.

The destinations are not tautologies. List results constrain the returned
reference, exact heap value, and next heap location. The integer claim
constrains `<k>` to `oddAlphabetCount(CS)`. The remaining modeled state is
preserved, and there is no result-bearing right-only free variable.

### Satisfiable ground states and substitution

`evidence/claim_witnesses.py` constructs satisfying inputs, evaluates the
formal summary, and compares it with both Python implementations. Every entry
precondition has multiple concrete witnesses:

| Claim/input | Formal result | Candidate Python | Canonical Python |
|---|---|---|---|
| whitespace / `"a b"` | `["a","b"]` | same | same |
| whitespace / `"a\tb"` | `["a","b"]` | same | integer `1` |
| comma / `"a,b"` | `["a","b"]` | same | same |
| comma / `","` | `["",""]` | same | `[]` |
| count / `"abcdef"` | `3` | `3` | `3` |
| count / `"ê"` | `0` | `0` | `1` |

The initial cells in each spec are realizable: module environment 0, the
builtins parent at -1, empty stack/heap, `scopeLoc = 1`, `heapLoc = 0`,
`noRet`, and `NoExc`. The call rule allocates callee scope 1, binds `txt`,
executes the body, and pops the frame.

Evidence: `evidence/claim_witnesses.py`,
`evidence/claim-witnesses.json`, and
`evidence/stage4-claim-witnesses.log`.

### Program pinning

The `<k>` cell does **not** load or invoke the submitted `solution.mpy` module.
It calls:

```text
Call(solutionClosure, str(CS))
```

`verification.k` independently defines `solutionClosure` as a closure over
`solutionBody`, and independently restates the body as a K term. Neither
`spec.k` nor `verification.k` references `solution.mpy`.

For the submitted candidate, the copied K body is textually faithful to
`solution.mpy`, and the trusted-translation byte check supports that manual
bridge. It is nevertheless not a machine-checked artifact pin. A sensitivity
experiment replaced the scratch `solution.mpy` with the valid translation of:

```python
def split_words(txt):
    return 999
```

The mutant hash differs from the submitted hash, but a fresh proof-definition
build and all target claims still returned `#Top`, because the proof never
reads that file. This does not allege that the original body copy differs; it
demonstrates the material pinning gap required by the audit instructions.

Evidence:

- `evidence/pinning-mutant.py`
- `evidence/pinning-mutant.mpy`
- `evidence/stage4-pinning-prep.log`
- `evidence/stage4-pinning-kompile.log`
- `evidence/stage4-pinning-kprove.log`

Stage 4 result: **FAIL** under the explicit real-artifact pinning requirement,
despite a faithful manual body copy and genuinely constrained destinations.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/inventory_k.py` extracted and classified every declaration from the
trusted `semantics.k` tree, candidate `verification.k`, and `spec.k`.
`evidence/rule-inventory.tsv` contains the exact source path, line, kind,
attributes, normalized statement, decision, and rationale for all **946**
items:

- 232 syntax declarations
- 705 rules
- 5 contexts
- 1 configuration
- 3 reachability claims

Attribute coverage includes 151 function-bearing rows, 109 `total` rows,
36 `concrete` rows, 50 priority-bearing rows, 25 `symbol(...)` rows, 29
`owise` rows, and 24 `no-evaluators` rows. There are no `functional` or
`simplification` declarations/rules. Exact commands and counts are in
`evidence/stage5-rule-inventory.log`,
`evidence/stage5-attribute-counts.log`, and
`evidence/stage5-special-attributes.log`.

The inventory dispositions are:

- 202 fixed rules used/reviewed on the submitted path;
- 334 fixed rules for constructs not reached by this program;
- 140 unused opaque float/sort rules or declarations;
- 16 concrete-only rules excluded from the proof main module;
- 3 unused assertion-oracle rules;
- 233 fixed syntax/configuration/context declarations;
- 5 candidate declarations;
- 4 candidate truthful definitional equations/summaries;
- 5 candidate unsound operational bridges;
- 1 accurate but unpinned body-copy equation;
- 3 result-constraining entry claims.

Unused fixed opaque boundaries include float symbols, `sortVS`,
`sortKeyVS`, and `md5hexCodes`. They cannot influence this program's control,
state, or result. `MPY-CONCRETE` is imported by `MPY-KRUN` but not by the
Haskell proof main module. `Assert` is absent from the submitted program and
positive claims.

### Used-construct mapping

Every construct in `solution.mpy` has a fixed declaration and execution path:

| Submitted construct | Fixed semantics |
|---|---|
| `Module`, statement sequence | `syntax.k`; `core.k` `#loadAll`/sequence rules |
| `FuncDef`, closure, params, return | `functions.k`, `call.k` |
| `Name`, scope lookup | `core.k` |
| `Assign`, `If`, `#branch` | `controls.k` |
| `Call`, `Attribute`, argument order | `call.k`, `core.k` |
| `Int`, `Str` literals | `core.k`, `str.k` |
| `BinOp`, `Compare`, `CmpOp` | `operators.k`, `int.k` |
| string `count` and `split` | `methods.k` |
| list allocation/reference | `core.k` `#alloc`; `methods.k` split rules |

The syntax uses strict/sequence-strict attributes for assignment RHS,
conditions, returns, attributes, and integer binary operands. Calls use the
explicit left-to-right `#evalArgs` loop. Closure calls allocate a callee scope,
bind `txt`, push a continuation frame, and restore/deallocate the scope on
return while preserving escaping heap allocation. On the submitted path,
`cntSub`, `dropIS`, `splitWS`, `flushTok`, `isWSC`, `splitSep`, integer
addition/comparison, lookup, allocation, and return equations have disjoint
guards or agreeing cases, structurally descending recursion, and sufficient
coverage. The ASCII-only `strToCodes` rule covers every literal appearing in
this program; formal input `CS` is already an internal code sequence.

### Candidate definitional rules

- `solutionBody` is an accurate, terminating name for the copied K body, but
  is not a binding to `solution.mpy`.
- `solutionClosure` truthfully constructs a closure over that copied body.
- `whitespaceCount`, `commaCount`, and `oddAlphabetCount` are unconditional,
  nonrecursive definitional sums of the fixed `cntSub` function. Their
  equations do not overlap and are mathematically true for the modeled code
  points.

These equations do not themselves smuggle a wrong branch or result.

### Five unsound operational bridges

The five rules at `verification.k` lines 13, 22, 31, 41, and 50 all match a
cooled `#branch(_B, THEN, .Stmts)` while deliberately discarding `_B`. They
read only a `$proofPath` value from scope 0, accept arbitrary additional map
bindings and parent, omit every other cell, and frame an arbitrary continuation
through `<k> ... </k>`. Priority 35 preempts the fixed rules:

```text
#branch(true, T, E)  => T
#branch(false, T, E) => E
```

The entry preconditions are not guards on the bridge rules. There is no
bridge-free universal connection theorem over the rules' complete match
domains, no proof that the arbitrary continuation is harmless, and no binding
rule that makes `$proofPath` semantically determine the actual Boolean.

The reviewer-authored witnesses give each state an ordinary string binding and
the indicated Boolean:

| Candidate rule | Ground string/Boolean | False conclusion enabled |
|---|---|---|
| path 1, first branch | `"abc"`, `false` | selects whitespace `then` arm |
| path 2, first branch | `"a b"`, `true` | discards whitespace `then` arm |
| path 3, first branch | `"a b"`, `true` | discards whitespace `then` arm |
| path 2, second branch | `"abc"`, `false` | selects comma `then` arm |
| path 3, second branch | `"a,b"`, `true` | discards comma `then` arm |

`evidence/branch-witness-extended.k` states exactly these five false
one-step conclusions. With the candidate proof definition, all five close
together with `#Top` and exit 0. The otherwise identical claims in
`evidence/branch-witness-fixed.k` were each selected independently against a
fresh fixed-semantics Haskell definition. Every one exited 1 with
`WarnStuckClaimState`, because fixed semantics takes the opposite arm.

Evidence:

- `evidence/stage5-branch-extended.log`
- `evidence/stage5-fixed-kompile.log`
- `evidence/stage5-fixed-path1.log`
- `evidence/stage5-fixed-path2-first.log`
- `evidence/stage5-fixed-path3-first.log`
- `evidence/stage5-fixed-path2-second.log`
- `evidence/stage5-fixed-path3-second.log`

These are concrete false-conclusion witnesses, not merely missing
justifications. Although the target claims arrange `$proofPath` consistently
with their premises, the rules are globally false on ordinary in-domain string
states and are not narrowed to those premises. Priority changes control flow;
it does not prove the missing equivalence.

Finally, removing only those five rules and rebuilding exposes dependence on
the extension:

- `SPEC.whitespace` still proves `#Top`;
- `SPEC.comma` fails with a residual symbolic first `#branch`;
- `SPEC.odd-lowercase-count` fails with the same genuine residual.

Evidence: `evidence/remove_branch_bridges.py`,
`evidence/stage5-no-bridges-prep.log`,
`evidence/stage5-no-bridges-kompile.log`,
`evidence/stage5-no-bridges-whitespace.log`,
`evidence/stage5-no-bridges-comma.log`, and
`evidence/stage5-no-bridges-count.log`.

Stage 5 result: **FAIL**. The candidate relies on materially unsound
proof-local control-flow rules.

## 6. Fresh non-vacuity test

The reviewer-created `evidence/spec-vacuity.k` changes the count destination
from:

```text
oddAlphabetCount(CS)
```

to the deliberately false:

```text
oddAlphabetCount(CS) +Int 1
```

The witness `"abcdef"` satisfies the claim premise and has actual/formal result
3, not 4.

`kprove --dry-run` exited 0, proving that the mutation parses and builds against
the fresh definition. The real proof then exited 1 with
`WarnStuckClaimState`. Its residual says that the term unifies with the
destination but the implication fails, and explicitly contains the impossible
equality between the occurrence sum and that sum plus 1. This is the expected
unmet result obligation, not a parser error, missing import, timeout, or
unreachable mutation.

Evidence:

- `evidence/spec-vacuity.k`
- `evidence/stage6-vacuity-dry-run.log`
- `evidence/stage6-vacuity-proof.log`

Stage 6 result: **PASS** for non-vacuity. This does not cure the unsound theory
or adequacy failures.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

Under the candidate-extended K theory, the successful runs establish that the
proof-local copied closure reaches:

- `splitWS(CS, .IntSeq, .ValSeq)` when the modeled four-code whitespace sum is
  positive;
- `splitSep(CS, 44, .IntSeq)` when that sum is non-positive and the comma count
  is positive;
- the sum of thirteen ASCII occurrence counts otherwise.

This statement is result-constraining and non-vacuous. It is a theorem of the
altered theory, not a valid proof under the fixed supplied semantics: the comma
and count targets cease to close when the false branch bridges are removed.
It also characterizes the candidate implementation rather than the trusted
canonical behavior on the material counterexamples in Stage 2.

### Trust and assumption ledger

| Boundary | Influence | Assessment |
|---|---|---|
| K v7.1.337, Haskell backend, SMT, builtin Int/Bool/String/Map/List hooks | All symbolic execution and ordinary mathematics | Necessary low-level tool trust; acceptable |
| Byte-identical supplied semantics | Language execution | Mandated fixed semantics; used path reviewed; acceptable with documented subset limits |
| Trusted `py2mpy.py` | Python-to-MPY bridge | Byte identity established; acceptable for the submitted translation |
| Fixed `cntSub`, `splitWS`, `splitSep`, allocation and call/return rules | Branch conditions and all results | Inspectable equations on the used path; acceptable |
| ASCII-only `strToCodes` and four-code `isWSC` model | Concrete language/intent bridge | Sound for submitted ASCII literals, but narrower than general Python whitespace/Unicode behavior |
| Opaque float, sort, keyed-sort, and MD5 symbols | None in this program | Unused; no dependency |
| `MPY-CONCRETE` deep equality/key-sort rules and `Assert` oracle | Concrete probes only or unreachable | Excluded from the proof or absent from program; no proof dependency |
| `solutionBody`/`solutionClosure` | Entire claimed program execution | Body copy is accurate, but the proof is insensitive to `solution.mpy`; unacceptable under the explicit pinning requirement |
| `$proofPath` branch rules | Control, returned value, allocation, final postcondition | Illegitimate operational oracle; five machine-checked false witnesses |
| Differential testing | Canonical adequacy on 2,039 inputs | Finite evidence only; establishes observed mismatches, not a universal theorem |
| Ground claim witnesses | Satisfiability and example substitution | Finite support only; not a replacement for reachability proof |

### Final gate accounting

- Fresh positive proof reconstruction: pass.
- Result constraint/non-vacuity: pass.
- Real-program soundness: fail because five operational bridges are false over
  their match domains and are required by two target claims.
- Real-artifact pinning: fail because the proof consumes a proof-local body
  copy and remains unchanged when `solution.mpy` is replaced.
- Natural-language/canonical adequacy: fail because of material tab/newline,
  comma-empty-field, and Unicode-lowercase divergences.
- Provenance/auditability: limited by the missing generation records, although
  reviewer evidence is reproducible.

The clean `#Top` outputs therefore do not constitute a legitimate
partial-correctness proof of the required real generated program.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
