# Independent adversarial review: 74-total-match

The candidate’s positive claims can be reconstructed and are
result-constraining, and the Python implementation is correct on the tested
domain. The submission is nevertheless not a legitimate proof of the real
generated program. Two independent defects are decisive:

1. the entry claims execute a new `runTotalMatch` wrapper containing a
   hand-copied closure, not the submitted `solution.mpy`; a deliberately false
   replacement `solution.mpy` still yields a fresh `#Top`; and
2. the proof-local priority-40 `For` rule is an unsound operational bridge. A
   ground one-string witness produces `"a"` under fixed supplied semantics but
   `"z"` under the bridge-enabled theory.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is no
mode/mount contradiction, so this is a candidate audit rather than
`AUDIT_ERROR`.

The recursive type-and-byte comparison found 25 entries in each semantics
tree, zero missing entries, zero additions, zero type changes, zero byte
changes, and no symlinked entries. Candidate `prompt.py` and `py2mpy.py` are
regular files byte-identical to their trusted versions:

- `prompt.py` SHA-256:
  `9662ed6743a83d0c34963151a98c5cdc9d33053cf3b26212adb7ff8abf9e3617`
- `py2mpy.py` SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

The definitive check and exact command are in
[01-integrity-rerun.log](evidence/01-integrity-rerun.log). The earlier
`01-integrity.log` records a reviewer-script `Path.lexists` mistake; the
corrected rerun exited 0 and is the result used here.

`solution.py`, `solution.mpy`, `spec.k`, `verification.k`, and
`reference-semantics/` are present with the expected regular-file/directory
types. The following requested provenance artifacts are missing:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No structured generation trace is present. These omissions weaken provenance
auditability but are not the basis for converting otherwise executable
candidate behavior into an infrastructure error. I inspected the untrusted
`prove.sh`, concrete test files, and source claims; their contents are recorded
in [02-source-inspection.log](evidence/02-source-inspection.log). Candidate
bytecode/cache material was not copied or used.

All source needed for execution was copied to `/tmp/audit-work`; no
candidate-provided compiled definition or cache was reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two finite lists of strings, sum Python `len` over every string in each
list. Return the first list when its total is less than or equal to the second
total; otherwise return the second list. Ties must select the first list.

The trusted canonical implementation uses two loops and the `<=` branch. The
candidate implementation performs the same computation with different local
names and a fall-through second return. On the intended domain, it also returns
the selected original list object rather than a copy.

### Translator identity

The trusted `/reference/py2mpy.py` regenerated the candidate MPY into scratch.
`cmp` reported byte identity, and both files have SHA-256
`470747b31c31d122130a383ca0b9634c28b09b5d709f3e679033c05f80100d8e`.
See [03-translation-identity.log](evidence/03-translation-identity.log) and the
preserved [regenerated-solution.mpy](evidence/regenerated-solution.mpy).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports the
trusted canonical entry point and candidate entry point and also checks the
direct natural-language sum/selection oracle. It checks result equality and
which input list object is returned.

The run covered 2,979 pairs:

- all five documented examples;
- 13 manual empty, tie, strict-less, strict-greater, empty-string, newline, and
  Unicode boundary cases;
- all 961 pairs of lists of length 0 through 2 over five representative string
  values; and
- 2,000 deterministically seeded generated pairs with list lengths 0 through 6.

It exercised the first branch 1,662 times and the second 1,317 times and found
zero mismatches. Exact generated inputs are preserved in
[differential-inputs.json](evidence/differential-inputs.json), whose recorded
SHA-256 is
`20c341067bbf4452e136fe7b797a32a0e9b8c3d95e3b5cdc1f9443434a898ff0`.
The command and exit 0 are in
[04-differential.log](evidence/04-differential.log).

This establishes strong finite source-level fidelity. It does not substitute
for a K reachability proof or connect the submitted file to a proof wrapper.

## 3. Clean proof reconstruction

The installed tools were independently located at `/usr/bin/kompile`,
`/usr/bin/krun`, and `/usr/bin/kprove`; both reported K
`v7.1.337` ([05-k-toolchain.log](evidence/05-k-toolchain.log)).

### Fresh concrete definition

From the scratch source copy, I ran:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/build/runtime-kompiled
```

It exited 0. The complete bounded output, including baseline exhaustiveness
warnings, is in
[06-runtime-kompile.log](evidence/06-runtime-kompile.log). The candidate’s five
translated examples then ran under `krun` with exit 0
([07-concrete-examples-krun.log](evidence/07-concrete-examples-krun.log)).

I additionally translated and ran seven reviewer-authored normal/boundary
assertions under both Python and the fresh LLVM definition. Translation,
Python, and K all exited 0:
[24-concrete-witness-translate.log](evidence/24-concrete-witness-translate.log),
[25-concrete-witness-python.log](evidence/25-concrete-witness-python.log), and
[26-concrete-witness-krun.log](evidence/26-concrete-witness-krun.log).
The sources are
[audit-concrete-witnesses.py](evidence/audit-concrete-witnesses.py) and
[audit-concrete-witnesses.mpy](evidence/audit-concrete-witnesses.mpy).

### Fresh proof definition and every positive claim

I ran:

```text
kompile verification.k --backend haskell \
  --main-module TOTAL-MATCH-VERIFICATION \
  --syntax-module TOTAL-MATCH-VERIFICATION \
  --output-definition /tmp/audit-work/build/verification-kompiled
```

It exited 0
([08-verification-kompile.log](evidence/08-verification-kompile.log)). I then
independently ran every positive claim:

- the loop module: exit 0 and `#Top`
  ([09-loop-proof.log](evidence/09-loop-proof.log));
- the original two-claim entry module: exit 0 and `#Top`
  ([10-entry-proofs.log](evidence/10-entry-proofs.log));
- the `<=` entry claim isolated in a reviewer module: exit 0 and `#Top`
  ([11-entry-first-proof.log](evidence/11-entry-first-proof.log)); and
- the `>` entry claim isolated in a reviewer module: exit 0 and `#Top`
  ([12-entry-second-proof.log](evidence/12-entry-second-proof.log)).

The split artifact is
[audit-entry-split.k](evidence/audit-entry-split.k). Thus the candidate
mechanically closes under its submitted proof theory. The later stages show
that this theory is not an honest theory of the submitted program.

## 4. Adequacy and real-program pinning

### Claims in plain language

The loop claim in `/candidate/spec.k:10-37` starts at the supplied semantics’
internal `#loop` with:

- an arbitrary algebraic string sequence `ITEMS`;
- current environment 1;
- integer accumulator `acc = I`;
- arbitrary old `item = OLD`; and
- otherwise empty heap, stack, and return/exception state.

It executes the exact `acc += len(item)` loop body followed by the proof-only
`readAccAndDrop("acc", "item")`. Its postcondition returns
`I + totalChars(ITEMS)`, stores that sum in `acc`, and removes `item`.

The first entry claim (`spec.k:42-57`) says that for arbitrary `StrSeq` values
`A` and `B`, if `totalChars(A) <= totalChars(B)`, `runTotalMatch(A,B)` reaches
`list(strVals(A))`.

The second (`spec.k:59-74`) says that if
`totalChars(A) > totalChars(B)`, the same wrapper reaches
`list(strVals(B))`. The preconditions are disjoint and cover every pair of
finite `StrSeq` totals; equality is correctly assigned to the first branch.
The returned values are explicit, not free variables, tautologies, or
one-way implications.

### Satisfying witnesses

[claim_witnesses.py](evidence/claim_witnesses.py) and
[22-claim-witnesses.log](evidence/22-claim-witnesses.log) record:

- `A=["a"]`, `B=["bb"]`: totals 1 and 2 satisfy the first precondition; both
  Python implementations return `A`;
- `A=["x"]`, `B=["y"]`: totals 1 and 1 exercise the tie and both return `A`;
- `A=["ab"]`, `B=["x"]`: totals 2 and 1 satisfy the second precondition; both
  return `B`; and
- loop witness `I=7`, old item `"z"`, items `["ab",""]`: the claimed
  accumulator is `7 + 2 + 0 = 9`.

### Fatal real-program pinning failure

The claims’ `<k>` cell does not load or execute the submitted
`solution.mpy`. It starts from the proof-local term `runTotalMatch(A,B)`.
`verification.k:113-138` rewrites that term directly to `Call(closureVal(...))`
whose function body is manually copied into `verification.k`. Neither
`verification.k` nor `spec.k` requires or mentions `solution.mpy`, `Module`, or
`FuncDef`; the exact scan is in
[27-program-pinning-dependency-scan.log](evidence/27-program-pinning-dependency-scan.log).

The copied body currently matches the translated source by inspection, but
that is not a mechanized execution or dependency. The body-sensitivity
experiment makes the gap concrete:

1. I replaced scratch `solution.py` with `return lst2` and regenerated
   `solution.mpy`. Its SHA-256
   `d1be7e8e183d57c40b0d2472344a7170e26ca091f96b259819260bda60a49f44`
   differs from the submitted MPY hash
   ([17-pinning-mutation-translate.log](evidence/17-pinning-mutation-translate.log)).
2. I freshly rebuilt `verification.k`; compilation exited 0
   ([18-pinning-mutation-kompile.log](evidence/18-pinning-mutation-kompile.log)).
3. Both entry claims still exited 0 with `#Top`
   ([19-pinning-mutation-proof.log](evidence/19-pinning-mutation-proof.log)).

The mutated sources are
[pinning-mutated-solution.py](evidence/pinning-mutated-solution.py) and
[pinning-mutated-solution.mpy](evidence/pinning-mutated-solution.mpy). A proof
that is unchanged by replacing the purported program with an implementation
that violates one branch proves the hand-written wrapper, not the real
generated program. This independently meets the `FAIL / NOT_LEGIT` boundary
for a substituted program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[static_inventory.py](evidence/static_inventory.py) generated the exhaustive
[rule-inventory.tsv](evidence/rule-inventory.tsv) from all 25 supplied
semantics files, `verification.k`, and `spec.k`. The definitive counts are in
[rule-inventory-summary.json](evidence/rule-inventory-summary.json) and the
command is in
[23b-static-inventory-final.log](evidence/23b-static-inventory-final.log):

- 1,093 inventoried sentences;
- 706 rules: 695 supplied baseline and 11 proof-local;
- 233 syntax declarations: 227 supplied and six proof-local;
- 146 `function`, 108 `total`, 47 priority, and 35 `concrete`
  declarations/rules;
- no `simplification` rule and no `functional` declaration; and
- three claims.

[opaque-symbol-inventory.tsv](evidence/opaque-symbol-inventory.tsv) identifies
the only locally unequated functions as supplied `md5hexCodes` and
`sortKeyVS`; both are explicit `no-evaluators` boundaries and neither is
reachable from this program. There is no proof-local opaque result or oracle.

The candidate semantics tree exactly equals the trusted supplied baseline.
Every baseline rule is therefore classified in the inventory as part of the
selected fixed semantics; every used construct was additionally traced through
syntax, evaluation order, scopes, calls, iteration, binding, arithmetic,
comparison, return, and configuration cells. The full construct map and
per-extension analysis are in
[static-review.md](evidence/static-review.md).

The fixed path is coherent for the submitted constructs: `Module` loads
statements; `FuncDef` binds a closure; calls allocate and restore a function
scope; `For` repeatedly calls the list iterator and writes the target binding;
`len(str(IntSeq))` uses structural `isLen`; `AugAssign` uses integer addition;
`<=` uses integer comparison; and `Return` unwinds the frame. The proof wrapper
bypasses the first two of those real-program steps.

### Accepted proof-local definitions

The following are disjoint, terminating, and truthful over their use domains:

- algebraic `StrSeq`;
- structural conversion `strVals`;
- total structural `totalChars`;
- the `nextStrings` symbolic-list iterator adapter; and
- the guarded proof-only `readAccAndDrop` observer.

`readAccAndDrop` defines a new operation rather than summarizing an existing
program operation. Its special semantics is acceptable for observing the loop
claim, but that special observer cannot establish equivalence for a different
continuation.

### Rejected proof-local `For` bridge, with false conclusion witness

`/candidate/verification.k:86-108` adds this priority-40 operational bridge:
it matches the exact shape `For(Name(ITEM), list(strVals(ITEMS)),
ACC += len(ITEM))`, replaces the whole loop with `.K`, and updates only `ACC`
to its old value plus `totalChars(ITEMS)`. Its match admits:

- arbitrary accumulator and item names;
- an arbitrary continuation after the `For`;
- any current map containing an integer accumulator; and
- arbitrary framed heap, stack, return, exception, and other cells.

Fixed semantics also writes `ITEM` on every nonempty iteration. The bridge
instead preserves an old `ITEM` binding or leaves it absent. The candidate loop
claim is not a bridge-free universal connection theorem for this match domain:
it uses literal names `"acc"` and `"item"`, requires the exact
`readAccAndDrop` continuation, and deliberately deletes the item binding. It
does not justify arbitrary continuations, arbitrary names, or the state the
bridge actually preserves.

The required false-conclusion witness is machine checked and uses the intended
list-of-strings input domain:

- initial state: `acc=0`, `item="z"`;
- loop input: `["a"]`;
- loop body: the exact `acc += len(item)` shape;
- immediate continuation: read `item`.

Using fixed supplied semantics plus only the truthful symbolic iterator
adapter, K proves final `acc=1`, final `item="a"`, result `"a"`
([audit-fixed.k](evidence/audit-fixed.k),
[audit-fixed-witness.k](evidence/audit-fixed-witness.k), and
[14-fixed-witness-proof.log](evidence/14-fixed-witness-proof.log)). Fixed
semantics rejects the conclusion `"z"` with exit 1 and a
`WarnStuckClaimState` residual explicitly containing result/item `"a"`
([audit-fixed-false-witness.k](evidence/audit-fixed-false-witness.k) and
[16-fixed-false-witness-rejected.log](evidence/16-fixed-false-witness-rejected.log)).

The bridge-enabled candidate theory proves the false result `"z"` with exit 0
and `#Top`
([audit-bridge-false-witness.k](evidence/audit-bridge-false-witness.k) and
[15-bridge-false-witness-proof.log](evidence/15-bridge-false-witness-proof.log)).
Thus this is a concrete false conclusion, not merely a missing explanation or
an untested edge case. The bridge contributes directly to the entry proof by
replacing both program loops.

### Other adequacy limits

The formal `StrSeq` represents each string by an arbitrary `IntSeq` and proves
length as constructor count. Relating this representation to all Python
Unicode strings is an informal bridge; finite Unicode differential tests
support but do not prove it. The wrapper also passes unboxed list values and
therefore states structural return-value behavior, not Python list-object
identity. Those points would warrant concerns if the proof were otherwise
sound and pinned. They are not needed for the failure decision, and I do not
label any additional rule unsound on their basis.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. I created
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), changing the first entry
claim’s result from `list(strVals(A))` to `list(strVals(B))` while retaining
the satisfiable precondition `totalChars(A) <= totalChars(B)`.
`A=["a"]`, `B=["bb"]` is a concrete satisfying witness for which both Python
implementations return `A`, so the mutation is genuinely false.

The mutated specification compiled successfully with `kprove --dry-run`, exit
0 ([20-vacuity-mutation-build.log](evidence/20-vacuity-mutation-build.log)).
The actual proof exited 1 with `WarnStuckClaimState`; the residual says the
reached `list(strVals(A))` cannot imply `list(strVals(B))` when `A != B`
([21-vacuity-mutation-rejected.log](evidence/21-vacuity-mutation-rejected.log)).
This is the expected unmet result obligation, not a parser error, missing
import, timeout, or unrelated crash.

The entry claims are therefore non-vacuous and result-constraining. This
positive finding does not repair the substituted-program and unsound-bridge
failures.

## 7. Proven versus assumed accounting

### What the successful reachability runs establish

Conditional on the candidate’s extended K theory, the successful entry proofs
establish partial correctness of the custom `runTotalMatch` term:

- for all finite algebraic `StrSeq` values `A,B`, if
  `totalChars(A) <= totalChars(B)`, that term reaches the structural list `A`;
- if `totalChars(A) > totalChars(B)`, it reaches the structural list `B`; and
- the special observed internal loop reaches the starting accumulator plus
  `totalChars` and then deletes its loop-variable binding.

They do not establish those statements for the loaded submitted
`solution.mpy`, because that artifact is absent from the proof dependency
graph. They also do not establish ordinary fixed-semantics loop behavior,
because the end-to-end run uses a bridge shown to prove a false observable
state.

As reachability claims, these are partial-correctness results; they are not
separate termination proofs.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| Trusted supplied MPY semantics, identical to `/reference/reference-semantics` | Concrete runs, all claims | Acceptable selected semantics boundary. Used paths were statically traced. |
| K v7.1.337 parser/compiler/Haskell and LLVM backends and K builtins for integers, maps, lists, strings | All machine results | Necessary toolchain trust; independently rebuilt, never candidate-compiled. |
| Trusted `/reference/py2mpy.py` | Source-to-MPY identity | Acceptable trusted translator; byte identity proved for the submitted source. |
| `StrSeq`/`IntSeq` as the Python list-of-strings model | Entry theorem’s human-language interpretation | Informal representation bridge, supported only finitely by differential and concrete tests. |
| `strVals`, `totalChars`, `nextStrings` | Loop and entry symbolic execution | Acceptable local structural definitions/adapters; exhaustive equations and fixed-iterator correspondence. |
| `readAccAndDrop` | Loop auxiliary claim only | Acceptable definition of a proof-only observer, but its result cannot justify other continuations. |
| supplied `md5hexCodes`, `sortKeyVS` opaque functions | None for this program | Explicit fixed-semantics primitives, irrelevant and unreachable here. |
| priority-40 proof-local `For` summary | Both end-to-end entry claims | Illegitimate. It replaces program execution, lacks a universal connection theorem, and admits the recorded false conclusion. |
| hand-copied `runTotalMatch` closure | Both end-to-end entry claims | Illegitimate program-identity bridge. It is independent of `solution.mpy`; the body mutation proves lack of pinning. |
| 2,979-case Python differential and seven concrete K witnesses | Source fidelity and finite representation evidence | Empirical only; cannot replace either K proof or universal bridge justification. |

### Gate outcomes and decision

- Stage 1 integrity: supplied semantics, prompt, and translator pass; four
  provenance artifacts and the structured trace are absent.
- Stage 2 source fidelity: pass on byte regeneration and 2,979 differential
  pairs.
- Stage 3 reconstruction: all positive claims freshly compile and print
  `#Top`.
- Stage 4 adequacy/pinning: fail; the proof is insensitive to a materially
  false replacement of `solution.mpy`.
- Stage 5 static soundness: fail; the `For` bridge proves the recorded false
  result/state on a satisfiable intended-domain input.
- Stage 6 non-vacuity: pass; a meaningful wrong-result mutation builds and is
  rejected for the expected obligation.
- Stage 7 accounting: the actual successful theorem is only about an unpinned
  wrapper under an unsound extended theory.

The correctness of the Python source, fresh `#Top` outputs, and successful
non-vacuity mutation do not cure either decisive defect. Under the requested
decision boundary, this is a substituted-program proof relying on a materially
unsound proof rule.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
