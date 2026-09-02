# Independent adversarial review: 67-fruit-distribution

## Overall assessment

The candidate contains a freshly reconstructible, result-constraining partial-correctness proof of the submitted translated program on the formal exact-sentence domain. I rebuilt both K definitions from source, proved all five positive claims separately, confirmed that the embedded `solutionModule` is the same MPY term as the trusted translation, and obtained the expected failure from a fresh off-by-one postcondition.

The proof is not an unqualified `PASS` because its general claim uses two fresh opaque sequence constructors, `fruitSentenceCodes` and `decimalCodes`. The proof-local split and integer-decoding rules give those constructors their intended observations, but no bridge-free universal K theorem equates them with concrete ASCII code sequences. The rules are deterministic, guarded, mathematically correct for the exact input grammar, preserve the real control/state path, and do not encode the final subtraction. I found no false conclusion witness for either candidate rule. The missing machine-checked representation bridge is therefore an explicit evidence/intent limitation rather than a demonstrated unsoundness.

There is a second scope limitation: the formal theorem covers exactly `"<A> apples and <B> oranges"` with nonnegative counts and `A+B<=N`. The trusted canonical implementation accepts some malformed or extended strings on which the submitted implementation differs. Those probes are outside the stated formal grammar, but the natural-language prompt does not spell the grammar out as sharply as the K claim.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and `/reference/reference-semantics` is present as required. There is no infrastructure contradiction.

The recursive, no-symlink comparison found 26 tree entries on each side (the root, one directory, and 24 K files), with no missing, additional, mistyped, changed, or symlinked candidate entry. The prompt and translator are byte-identical to their trusted versions:

- `prompt.py`: SHA-256 `287ace00706dbc14460387cbd37396f40de3816fb26bd13182cec8a85fd6dddb`
- `py2mpy.py`: SHA-256 `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The complete independent check and hashes are in [01-provenance.log](evidence/01-provenance.log), produced by [check_provenance.py](evidence/check_provenance.py). No candidate symlink exists anywhere under `/candidate`.

### Missing generation records

The following requested untrusted generation records are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured trace (`*trace*` or `*.jsonl`)

Their absence reduces provenance/audit context but does not remove a proof source or a target claim. The candidate-provided `prove.sh`, `kprove.out`, concrete output, and test sources were read only as claims. Their hashes and bounded excerpts are in [25-untrusted-candidate-claims.log](evidence/25-untrusted-candidate-claims.log). In particular, the candidate's `kprove.out` merely says `#Top`; it was not reused.

### Isolation

The source artifacts needed for execution were copied to `/tmp/audit-work/reconstruction`; candidate caches and `__pycache__` were not copied or used. The exact copy command and source manifest are in [02-scratch-copy.log](evidence/02-scratch-copy.log). All compiled definitions in the audit were newly generated below that scratch directory.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt asks for the number of mangoes in a basket whose total fruit count is `n` and whose string supplies the apple and orange counts. On the example-shaped domain,

```text
s = "<A> apples and <B> oranges"
A >= 0, B >= 0, A + B <= N
```

the intended result is `N-A-B`.

The trusted canonical implementation splits on literal spaces, collects every token for which `isdigit()` is true, converts those tokens to integers, and returns `n-sum(tokens)`. The submitted implementation uses whitespace splitting and reads positions 0 and 3:

```python
fruits = s.split()
return n - int(fruits[0]) - int(fruits[3])
```

These algorithms agree on the formal five-token grammar. The submitted one is narrower on malformed or extended inputs.

### Translation identity

Running the trusted `/reference/py2mpy.py` against the scratch `solution.py` produced SHA-256
`eec464d352d469426d30b7f9287c03b7b1bf9a8d47132ec6f451b5008976cf63`, identical to the submitted `solution.mpy`. The authoritative rerun records translator exit 0 and `cmp` exit 0 in [03b-translation-byte-identity-rerun.log](evidence/03b-translation-byte-identity-rerun.log).

[03-translation-byte-identity.log](evidence/03-translation-byte-identity.log) is a retained initial logging-wrapper false start: its inner output reported `CMP_STATUS: 0`, but the wrapper recorded exit 1. I did not rely on it and reran the check with the translator and comparison statuses made explicit.

### Independent differential testing

[differential_test.py](evidence/differential_test.py) independently imports `/reference/canonical.py` and the scratch copy of `solution.py`. Its deterministic scope was:

- all four documented examples;
- zero, one-sided-zero, exact-total, and large-decimal boundaries;
- every `A,B` in `[0,8]` and every mango count in `[0,3]`;
- 2,000 generated triples from seed `670067`, with each component in `[0,10^9]`;
- empty, whitespace-only, missing-number, extra-number, negative-count, tab-delimited, and repeated-space robustness probes.

The exact command, deterministic input-manifest hash, results, and exit status are in [04-differential.log](evidence/04-differential.log):

```text
intended_domain_cases=2333
intended_domain_mismatches=0
outside_domain_probes=7
outside_domain_mismatches=6
EXIT_STATUS: 0
```

The empty string, whitespace-only string, missing-number string, extra-number string, negative-count string, and tab-delimited string diverged. They do not satisfy the formal exact grammar. The repeated-space probe agreed. This finite test supports implementation-to-intent alignment only on the tested scope; it is not the K proof.

## 3. Clean proof reconstruction

### Toolchain and concrete definition

The independently installed tools are K `v7.1.337` (build date 2026-06-18); see [05-toolchain.log](evidence/05-toolchain.log).

I generated a reviewer harness from the scratch `solution.py`, translated it with the trusted translator, and ran it in Python. It covers a documented case, zero boundaries, both one-sided-zero boundaries, an exact-total boundary, and a three-digit case. Generation, the complete MPY harness, and Python exit 0 are in [06-concrete-harness-generation.log](evidence/06-concrete-harness-generation.log), with generator source in [make_concrete_harness.py](evidence/make_concrete_harness.py).

The clean concrete build command was:

```bash
/usr/bin/kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0; warnings about non-exhaustive functions concern unused portions of the supplied baseline. See [07-kompile-concrete.log](evidence/07-kompile-concrete.log). Running

```bash
/usr/bin/krun concrete-harness.mpy \
  --definition runtime-kompiled \
  --output pretty
```

also exited 0 with `.K`, `NoExc`, and exit code 0. The complete bounded configuration is in [08-krun-concrete.log](evidence/08-krun-concrete.log).

### Proof definition and positive claims

The proof build command was:

```bash
/usr/bin/kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0 ([09-kompile-proof.log](evidence/09-kompile-proof.log)). The original complete target then produced `#Top` and exit 0:

```bash
/usr/bin/kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

See [10-kprove-all.log](evidence/10-kprove-all.log).

I also split the five source claims without changing their configurations or obligations; the reviewer artifact is [spec-individual.k](evidence/spec-individual.k). Every claim independently printed `#Top` and exited 0:

| Claim | Evidence |
|---|---|
| symbolic general claim | [11-kprove-general.log](evidence/11-kprove-general.log) |
| `"5 apples and 6 oranges", 19` | [12-kprove-example1.log](evidence/12-kprove-example1.log) |
| `"0 apples and 1 oranges", 3` | [13-kprove-example2.log](evidence/13-kprove-example2.log) |
| `"2 apples and 3 oranges", 100` | [14-kprove-example3.log](evidence/14-kprove-example3.log) |
| `"100 apples and 1 oranges", 120` | [15-kprove-example4.log](evidence/15-kprove-example4.log) |

No candidate-compiled definition, cache, `#Top`, or trace contributed to these runs.

## 4. Adequacy and real-program pinning

### Plain-language meaning of each entry claim

The general claim starts from the supplied MPY initial configuration, loads the exact fruit-distribution module, and calls it with the symbolic exact-sentence representation and total `N`. Its precondition says:

- `A` and `B` are nonnegative integers;
- `A+B<=N`, which also implies `N>=0`.

Its postcondition requires the final `<k>` result to be exactly `N-A-B`. It also requires:

- the temporary function scope and stack to be cleaned up;
- `ret` to be `noRet`;
- no exception and exit code 0;
- exactly one heap allocation (`heapLoc: 0 => 1`) for the split list.

Only the final scope map and heap contents are existentially framed. The returned value is not existential, free, tautological, or stated through a one-way implication.

The other four claims have no extra precondition and assert the four documented ground results. They use ordinary `Str` literals. Therefore the proof-local symbolic split and decimal rules do not match them; they exercise the supplied `strToCodes`, `splitWS`, and `intDigAcc` path.

### Exact submitted program

`solutionModule` is a name for a `Module(FuncDef(...))` term, after which ordinary supplied rules execute every statement and expression. It is not an operational shortcut for the function call.

[check_program_pinning.py](evidence/check_program_pinning.py) independently extracts the `solutionModule` RHS and compares it with the submitted `solution.mpy`, normalizing only the MPY list printer's two spellings of empty/tail `.Exprs`. The authoritative result in [21b-program-pinning-rerun.log](evidence/21b-program-pinning-rerun.log) is:

```text
submitted_normalized_sha256=9557778ad1fcf465cf8554ae2d5fbbe88dc7fe312b773f9965b8e52b62a38cc7
embedded_normalized_sha256=9557778ad1fcf465cf8554ae2d5fbbe88dc7fe312b773f9965b8e52b62a38cc7
normalized_module_terms_identical=True
EXIT_STATUS: 0
```

[21-program-pinning.log](evidence/21-program-pinning.log) is a retained reviewer-script iteration that did not yet normalize trailing empty-list commas; the corrected script and rerun above are the evidence used.

There are no helper or loop claims and no replacement implementation. The real control flow is:

```text
load Module -> bind FuncDef -> call closure -> bind s,n
-> evaluate s.split() -> allocate list -> assign fruits
-> evaluate n - int(fruits[0]) - int(fruits[3])
-> Return -> pop frame
```

### Satisfying states and concrete substitution

The state `A=5, B=6, N=19` satisfies every general precondition and gives result 8. [spec-ground-general.k](evidence/spec-ground-general.k) instantiates the symbolic representation at those values and independently closes with `#Top` and exit 0 in [22-kprove-ground-general.log](evidence/22-kprove-ground-general.log).

The ground claims themselves exhibit satisfying initial states for the four no-precondition entries. Substitution agrees with both Python implementations:

| `A,B,N` | Claimed result | Canonical | Submitted |
|---|---:|---:|---:|
| `5,6,19` | 8 | 8 | 8 |
| `0,1,3` | 2 | 2 | 2 |
| `2,3,100` | 95 | 95 | 95 |
| `100,1,120` | 19 | 19 | 19 |

These are also covered by the differential log and by fixed-semantics literal claims.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[inventory_k.py](evidence/inventory_k.py) inventories every statement in all 24 supplied K files and `verification.k`. The corrected exhaustive report is [16b-rule-inventory-rerun.md](evidence/16b-rule-inventory-rerun.md). It contains a source location, complete compact statement, path classification, and decision for each of:

```text
configuration: 1
syntax declarations: 229
contexts: 5
rules: 698
total inventoried statements: 933
```

Attribute-bearing entry counts are 147 `function`, 108 `total`, 0 `functional`, 25 `symbol`, 22 `no-evaluators`, 47 priority rules, 26 `owise`, 35 `concrete`, 0 simplification, two strict declarations, one sequentially strict declaration, and four macro-bearing declarations.

[16-rule-inventory.md](evidence/16-rule-inventory.md) is a retained first inventory pass whose parser treated indented rule guards beginning with `requires` as statement boundaries. The corrected `16b` report includes those guards and their priority attributes and is the report relied upon.

Because the mode is supplied semantics and the candidate tree is byte-identical to the trusted tree, unchanged baseline rules are accepted at the selected semantics level. The inventory separately marks every baseline entry reached by this program and every unused entry. I reviewed the reached path for evaluation order, cells, calls, allocation, and rule overlap. No generated helper K file or candidate semantic replacement exists.

### Mapping from submitted syntax to rules

| Submitted construct | Declaration and controlling rules |
|---|---|
| `Module`, statement list | `syntax.k:56-61`; `core.k:124-127` loads and sequences statements |
| `FuncDef`, `Params` | `syntax.k:53-60`; `functions.k:14-16` installs the closure |
| function call | `syntax.k:28`; `call.k:20-24,69-74`; `core.k:185-191` evaluates arguments left-to-right |
| parameter binding/return | `functions.k:63-66,78-90` |
| `Name` lookup | `syntax.k:12`; `core.k:130-181`, including the real builtins scope |
| `Assign` | `syntax.k:41` is RHS-strict; `controls.k:9-11` updates the current function scope |
| `Attribute` | `syntax.k:29` is receiver-strict; `call.k:16` creates the bound method |
| zero-argument `split` | fixed concrete rule `methods.k:72-86`; proof-local symbolic bridge `verification.k:15-29` |
| `Return` | `syntax.k:50` is strict; `functions.k:78-90` records the value and restores the caller |
| `BinOp("-")` | `syntax.k:15` is left-to-right `seqstrict`; `operators.k:12`; `int.k:13` |
| `Subscript` at 0 and 3 | `syntax.k:22,38`; `subscript.k:27-41`, including heap dereference, normalization, and `valSeqAt` |
| `Int` literals | `syntax.k:9`; `core.k:194` |
| `int(...)` | builtins binding `core.k:157-181`; call dispatch `call.k:32`; fixed rules `builtins.k:140,152-160`; symbolic bridge `verification.k:34-36` |

The fixed `valSeqAt` is marked total, but no underspecified out-of-bounds value is used: the split result has five explicit elements, so indices 0 and 3 reduce by ordinary constructor equations.

### Proof-local inventory and decisions

1. `syntax IntSeq ::= decimalCodes(Int) | fruitSentenceCodes(Int,Int)` (`verification.k:9-10`) introduces two fresh constructors. They do not overlap the concrete `.IntSeq`/`iCons` constructors. They are opaque: no equation relates either to a concrete code sequence. This is the source of the documented bridge concern.

2. The split rule (`verification.k:15-29`) is a result-bearing operational bridge. It matches only:

   - the fresh exact-sentence constructor;
   - the no-argument `"split"` method;
   - nonnegative `A,B`.

   Its priority 30 preempts the fixed priority-40 concrete split rule only on that fresh constructor. It preserves the complete continuation: the redex becomes the same `#alloc(...)` mechanism used by fixed semantics, so allocation still reads/writes `heap` and `heapLoc` with the usual freshness guard. It does not touch scopes, environment, stack, return, exception, or exit cells. Arbitrary continuations remain after `#alloc`; it introduces no return or abrupt control.

   For an exact ASCII sentence, the five emitted elements are the mathematically correct whitespace split. The rule does not state the final result and does not skip the function body, subscripts, integer calls, or subtraction.

3. The integer rule (`verification.k:34-36`) is a pure result-bearing bridge from the fresh decimal constructor to its nonnegative integer parameter. Its guard covers exactly the formal nonnegative use. It is disjoint from concrete `iCons` numeral terms and preempts the fixed generic decoder only for `decimalCodes(I)`. Its equation is the intended inverse of nonnegative decimal notation.

4. `solutionModule` (`verification.k:41-59`) is a total nullary definitional function with one equation. Its RHS is the exact translated source term, as independently checked above. It names the program; it does not replace execution.

No local rule is a simplification, lemma, loop circularity, unconstrained fresh value, or answer-bearing oracle.

### Overlap, totality, opacity, and false-witness discipline

The two bridge guards do not overlap each other. Their overlaps with fixed library routing are deliberately resolved by priority and limited to the fresh constructors. Each recursive fixed function reached by the real program descends over a concrete sequence or list. The program uses unbounded mathematical integers, consistent with Python integers for this computation.

The supplied baseline contains 22 `no-evaluators` opaque symbols, principally float operations, sorting, and MD5. None is reachable from this program. The other baseline total functions that can remain abstract on malformed inputs are likewise not reached abstractly on the formal domain.

I do **not** label either candidate bridge unsound: I found no concrete or symbolic state in the intended exact-sentence domain on which its stated conclusion is false. Instead, the narrower evidence gap is that there is no bridge-free universal theorem connecting:

```text
fruitSentenceCodes(A,B)
```

to the concrete ASCII sequence for `"<A> apples and <B> oranges"`, or `decimalCodes(I)` to concrete decimal digits.

This dependence is visible in the bridge-free control. [verification-no-bridges.k](evidence/verification-no-bridges.k) and [spec-no-bridges.k](evidence/spec-no-bridges.k) compile successfully ([17-kompile-no-bridges.log](evidence/17-kompile-no-bridges.log)), but proof fails with exit 1 and a meaningful residual at `splitWS(fruitSentenceCodes(A,B),...)`, downstream `valSeqAt`, and `int` in [18-kprove-no-bridges-expected-failure.log](evidence/18-kprove-no-bridges-expected-failure.log).

The result is also sensitive to the bridge value. [verification-wrong-int.k](evidence/verification-wrong-int.k) deliberately interprets each decimal token as `I+1`. It builds successfully ([23-kompile-wrong-int.log](evidence/23-kompile-wrong-int.log)), while the original result claim fails with:

```text
N -Int (A +Int 1) -Int (B +Int 1)
  #Equals
N -Int A -Int B
```

See [24-kprove-wrong-int-expected-failure.log](evidence/24-kprove-wrong-int-expected-failure.log). This rejects the opposite interpretation and shows that the postcondition is not closing merely because the same parameter names occur in the bridges and the spec.

## 6. Fresh non-vacuity test

The reviewer-authored [spec-vacuity.k](evidence/spec-vacuity.k) changes the general result obligation from:

```text
N -Int A -Int B
```

to:

```text
N -Int A -Int B +Int 1
```

This is demonstrably false at the satisfying state `A=5,B=6,N=19`: the mutation asks for 9, while both Python implementations, concrete K execution, the concrete example claim, and the original symbolic claim produce 8.

The mutated spec builds/parses successfully under `kprove --dry-run`, exit 0, in [19-vacuity-dry-run-build.log](evidence/19-vacuity-dry-run-build.log). The actual proof command was:

```bash
/usr/bin/kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exits 1 with `WarnStuckClaimState` after reaching the actual final value. The residual contains exactly:

```text
N -Int A -Int B
  #Equals
N -Int A -Int B +Int 1
```

See [20-vacuity-kprove-expected-failure.log](evidence/20-vacuity-kprove-expected-failure.log). This is a semantic failure of the intended false obligation, not a parser error, missing import, timeout, unreachable mutation, or unrelated crash.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the supplied MPY semantics plus the two stated proof-local symbolic-library rules, the successful reachability proof establishes:

> For all mathematical integers `A,B,N` satisfying `A>=0`, `B>=0`, and `A+B<=N`, execution of the exact submitted MPY `fruit_distribution` body from the specified initial configuration, on `str(fruitSentenceCodes(A,B))` and `N`, reaches result `N-A-B`, performs exactly one list allocation, restores the call frame, and terminates the modeled call with `NoExc` and exit code 0.

It also independently establishes the four literal prompt examples through the supplied concrete string/split/integer rules.

The proof executes the actual translated body. It proves the returned arithmetic result rather than a summary variable. The false-postcondition and wrong-bridge experiments show both result and bridge sensitivity.

### Trust and assumption ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Byte-identical supplied semantics (24 K files) | Defines the entire MPY execution model used by all claims | Authorized fixed semantics for this mode; relevant rules were statically mapped and freshly executed |
| K `v7.1.337`, Haskell prover, LLVM runner, K builtins for integer/boolean/string/map/list operations | Parsing, rewriting, SMT/arithmetic reasoning, concrete execution | Ordinary toolchain/trusted computing base |
| `fruitSentenceCodes(A,B)` informal representation contract | Connects the general K input term to the human sentence grammar; affects split, both decoded values, and the final result | Sound by ordinary exact-string reasoning and finitely supported, but not machine-connected to concrete codes; principal concern |
| `decimalCodes(I)` informal representation contract | Connects each symbolic token to nonnegative decimal notation; affects both `int` results and final subtraction | Deterministic and guarded, with wrong interpretation rejected; no universal concrete-code theorem |
| Symbolic split rule | Replaces fixed `splitWS` on the fresh opaque sentence constructor | Acceptable low-level symbolic-library boundary on the formal grammar; control/state preserving; bridge-free proof does not close |
| Symbolic `int` rule | Replaces fixed digit folding on the fresh opaque decimal constructor | Acceptable low-level symbolic-library boundary on nonnegative values; directly result-bearing and therefore explicitly disclosed |
| `solutionModule` textual/AST duplication | Selects what program is loaded | Independently normalized to the trusted-translated `solution.mpy`; acceptable definitional name |
| Fixed opaque `sortVS`, `sortKeyVS`, `md5hexCodes`, and float symbols (`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, plus fixed `floorFI`, `toF`, `ceilF`) | Potential value or control effects in other programs | Inventoried fixed-baseline opacity; none is reachable here |
| Differential testing | Supports source-to-canonical agreement on 2,333 formal-domain cases | Finite evidence only; not a substitute for K reachability or the missing representation theorem |
| Concrete K harness and four literal claims | Supports fixed `Str`/`splitWS`/`intDigAcc` behavior at selected cases | Finite bridge evidence only |

### Excluded behavior

The theorem does not cover:

- empty or whitespace-only strings;
- missing or additional numeric fields;
- negative apple/orange spellings;
- alternative word order;
- tab-delimited or other non-exact sentence forms;
- arbitrary strings accepted by the canonical token-scanning algorithm;
- Python exceptions outside the safe exact grammar;
- non-ASCII string semantics.

The six recorded out-of-domain differential mismatches make this exclusion observable rather than hypothetical.

### Decision

The proof is legitimate for the exact formal domain: it reconstructs, constrains the real result, loads the exact translated program, and rejects meaningful false mutations. The proof-local rules are low-level deterministic abstractions of `split` and `int`, not smuggled final-answer rules; no false conclusion witness was found for their guarded domains.

The general symbolic-to-concrete string correspondence is nevertheless informal rather than machine-checked, and the formal grammar is narrower than the canonical implementation's permissive behavior. Those limitations prevent an unqualified pass and are the basis for `CONCERNS / LEGIT`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
