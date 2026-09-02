# Independent adversarial audit: 17-parse-music

This audit reconstructed the proof from candidate source using K 7.1.293 and
the trusted supplied semantics. Both submitted positive claims reproduce
`#Top`, the result obligation is non-vacuous, and the claim's macro-expanded
program is the submitted translated program. Nevertheless, this is not a
legitimate proof of the HumanEval program on real input strings. The entry
claim ranges over a fresh, unconnected `musicCodes(Music)` constructor, and a
candidate-local rule replaces the supplied `str.split()` transition with a
ghost iterator. That rule returns a different kind of value and suppresses the
split-list heap allocation. Executable fixed-versus-extended witnesses expose
both differences.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `17-parse-music`;
- condition `semantics`;
- semantics mode `SUPPLIED_SEMANTICS`;
- record layout `legacy-selected-stage1`; and
- complete input provenance.

There is no infrastructure breach.

The independent checker in `evidence/provenance_check.py` read the launcher
record and mounted inputs rather than the host-only provenance paths. Its full
output is `evidence/01-provenance.log` (exit 0). In particular:

- `/audit-campaign-lock.json` is structurally equal to the
  `audit_campaign` object and has the recorded SHA-256
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the sole structured trace file all
  exist as readable regular files and match their recorded hashes.
- The required trace file's direct SHA-256 is
  `dc5340ae8a0e32412fc66004385c7e6e08ed39f266282b296667f3d7347eb87b`.
  All 345 JSONL records parsed successfully.
- The full 20,572-line `codex-output.log` and all structured events were read
  by `evidence/summarize_generation_records.py`; the bounded extraction is
  `evidence/25-generation-record-summary.log`. Those records were treated
  solely as untrusted construction history.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts and match the launcher hashes.
- The candidate and trusted `reference-semantics/` trees have exactly the
  same 26 entries, types, modes, and file bytes. Neither tree contains a
  symlink. Their independently defined path/type/mode/content manifest
  digests are both
  `636f164370ef6350ce86439a334f9eb9c1e4294ceda02337840db006b8085b92`.
- No candidate entry is a symlink. All required proof artifacts are present
  as regular files.

The trusted `/reference/reference-semantics` mount is present, as required by
the rendered supplied-semantics mode. The candidate copy is exact. This
integrity result fixes the selected baseline; it does not validate the
proof-specific rules in `/candidate/verification.k`.

All execution sources were copied to `/tmp/audit-work/reconstruction`.
Crucially, its `reference-semantics/` came from the trusted reference mount,
not from a candidate cache. No candidate-built definition was copied. The
source-copy manifest is `evidence/02-scratch-copy.log`.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt describes a string of musical-note tokens:

- `o` means four beats;
- `o|` means two beats; and
- `.|` means one beat.

The result is the corresponding list of integers. The trusted canonical
implementation builds that mapping and processes nonempty fields from
`music_string.split(' ')`.

The candidate uses `music_string.split()`, tests `o` and `o|`, and maps its
remaining branch to 1. It is extensionally equal to the canonical function on
valid space-delimited strings made only from the three documented notes. It is
more permissive outside that language: invalid tokens are treated as quarter
notes and tab/newline separators are accepted, whereas the canonical function
raises `KeyError` for the tested cases. The proof fails for a more fundamental
reason even on valid note strings, so the diagnostic out-of-domain differences
do not determine the verdict.

### Trusted regeneration

Command:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/reconstruction/solution.py \
  > /tmp/audit-work/reconstruction/regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Both files have SHA-256
`fd131af8a2ebf3749359fb81b36453db2da86229334451021cb9b4bbfb0a92f8`.
See `evidence/03-translation.log`.

### Independent differential test

`evidence/differential_test.py` imports the trusted canonical and candidate
entry points independently. It covers the documented example, empty input,
each of the three branch outcomes, transitions between branches, leading,
trailing, and repeated ASCII spaces, the proof witness `o o| .|`, and every
sequence of the three notes through length six.

Command:

```text
python3 /audit-output/evidence/differential_test.py
```

Result (`evidence/04-differential.log`, exit 0):

- 1,104 intended valid cases;
- zero intended-domain mismatches;
- four explicit diagnostic out-of-domain cases; and
- four diagnostic mismatches, all reported rather than hidden.

This is finite evidence for implementation/canonical agreement on the tested
valid strings. It is not a universal theorem and does not connect the proof's
ghost input to source strings.

## 3. Clean proof reconstruction

The available toolchain is K 7.1.293. `kup` is absent, but independently
installed `kompile`, `krun`, and `kprove` all run at `/usr/bin`; see
`evidence/05-toolchain.log`.

The following commands were run in the clean scratch copy:

| Command | Result | Evidence |
|---|---:|---|
| `kompile reference-semantics/semantics.k --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX --output-definition runtime-kompiled` | exit 0 | `06-kompile-llvm.log` |
| `krun concrete-test.mpy --definition runtime-kompiled` | exit 0, final `.K`, `NoExc`, exit-code 0 | `07-krun-concrete.log` |
| `kompile verification.k --backend haskell --main-module PARSE-MUSIC-BASE --syntax-module MPY-SYNTAX --output-definition verification-base-kompiled` | exit 0 | `08-kompile-base.log` |
| `kprove spec.k --definition verification-base-kompiled --spec-module PARSE-MUSIC-LOOP-SPEC` | exit 0, `#Top` | `09-kprove-loop.log` |
| `kompile verification.k --backend haskell --main-module PARSE-MUSIC-VERIFICATION --syntax-module MPY-SYNTAX --output-definition verification-kompiled` | exit 0 | `10-kompile-entry.log` |
| `kprove spec.k --definition verification-kompiled --spec-module PARSE-MUSIC-ENTRY-SPEC --branching-allowed 100` | exit 0, `#Top` | `11-kprove-entry.log` |

Thus the candidate's positive verification claim is reproducible. This proves
closure under the supplied semantics plus the candidate's extensions; it does
not establish that those extensions preserve fixed-semantics execution.

The LLVM build warned that several supplied `[total]` functions are not
syntactically exhaustive on exotic `cellsMark` values or empty indexing.
Those functions are outside this program's dependency cone and are discussed
in stage 5. The warnings do not cause either positive claim to close and do
not explain the candidate-local defect.

## 4. Adequacy and real-program pinning

### Plain-language claims

The loop claim says: from a loop head over `musicIter(M)`, with target `note`,
an existing output list `A`, and a current `note` value `N`, execution consumes
the entire ghost note sequence; it appends 4/2/1 according to the constructors
of `M` and leaves `note` equal to the last ghost token (or `N` for an empty
sequence).

The entry claim says: from the initial module configuration, load the submitted
function and call it on the internal value
`str(musicCodes(M))`. It must terminate with `ref(0)`, with the heap exactly
`0 |-> list(musicAcc(.ValSeq,M))`, `heapLoc` exactly 1, clean stack/return/
exception cells, and exit code 0.

Neither claim has an explicit `requires`. Their constructor patterns are their
preconditions.

### Satisfiable preconditions and ground result

The loop precondition is satisfiable, for example with
`M = whole(.Music)`, `L = 1`, `B = 0`, `A = .ValSeq`, `N` the empty string,
and exact maps containing the displayed scope and heap entry. The base proof
quantifies over that state and closes.

The entry precondition is syntactically satisfiable with
`M = whole(half(quarter(.Music)))` in the displayed initial configuration.
`evidence/artifacts/spec-witness.k` substitutes that ground value and the
explicit expected list `[4,2,1]`; the proof prints `#Top` and exits 0
(`evidence/13-kprove-abstract-witness.log`). Both Python implementations return
`[4,2,1]` for the intended concrete text `o o| .|`
(`evidence/04-differential.log`).

That comparison does not supply the missing premise
`musicCodes(whole(half(quarter(.Music))) = codes("o o| .|")`. No such equation
exists.

### Program-term identity

The entry claim does execute the submitted function binding and body, subject
to its proof extensions. Using the independently compiled definition:

```text
kast --definition verification-kompiled \
  --module PARSE-MUSIC-VERIFICATION --sort Module \
  --expand-macros --output json solution.mpy

kast --definition verification-kompiled \
  --module PARSE-MUSIC-VERIFICATION --sort Module \
  --expand-macros --output json claim-program.mpy
```

Both expanded JSON terms are byte-identical, with SHA-256
`ccc96cd905d382aecea6d56d36855bc3317119abf858654edeed842622b01442`.
See `evidence/12-program-pinning.log` and the preserved JSON under
`evidence/artifacts/`.

The body is also proof-sensitive. The auditor changed the whole-note branch in
the macro from `append(4)` to `append(5)`, thereby changing the term actually
executed by the claim. Its expanded JSON digest changed to
`afd5fe5849b3f1338a790af8edd93d512e0cab2c72e8e211c5b13862a163187d`
(`evidence/20-body-mutant-pinning.log`). The isolated loop proof then failed
with the expected unmet equality between an accumulator extended by 4 and one
extended by 5 (`evidence/21-kprove-body-mutant.log`,
`KPROVE_EXIT_STATUS=1`).

### Failure to pin real inputs and fixed execution

The formal entry input is not a concrete source string. `musicCodes(Music)` is
a fresh constructor of sort `IntSeq` with no equations. A constructor-level
comparison between `str(musicCodes(whole(.Music)))` and the concrete string
value `str(iCons(111,.IntSeq))` produces different KAST JSON hashes:

```text
ghost:    5f4f9bb5c7dd0674da3b71b8cd784ab71137e817d1c80fef1a54422650846937
concrete: e99a3dbee8d9950ba493fff4ef03b9d0ad9dc9a24a5322c08795988b5c1358d8
```

See `evidence/31-input-domain-constructor-comparison.log`. Consequently, no
ordinary ground string made from `.IntSeq`/`iCons` is an instance of the entry
claim's argument pattern.

Removing only the candidate's `split` bridge leaves fixed supplied semantics
in control. The variant builds, but the universal entry proof fails at
`splitWS(musicCodes(M),.IntSeq,.ValSeq)` because the opaque code sequence has no
constructor equation (`evidence/17-kompile-no-bridge.log` and
`evidence/18-kprove-no-bridge.log`, proof exit 1). This is the genuine
unproved connection obligation.

Finally, the ground concrete text `o o| .|` was executed symbolically under the
same submitted program and fixed supplied split rules. Requiring the
candidate's destination footprint fails: the actual state contains the
allocated split-token list at heap location 1 and ends with `heapLoc = 2`
(`evidence/14-kprove-concrete-witness.log`, exit 1). The corrected destination,
which includes that list and `heapLoc = 2`, closes with `#Top`
(`evidence/15-kprove-concrete-actual-state.log`, exit 0). The returned list is
still `[4,2,1]`; the material disagreement is the execution and allocation
footprint that the candidate bridge skipped.

The theorem therefore executes the right syntax but not every material
operation of that syntax, and its precondition materially replaces the real
source-contract domain with synthetic values. This is a real-program adequacy
failure, not merely an artifact-maintenance observation.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` inventories every source-level
`configuration`, `syntax`, `context`, `rule`, and `claim` in the trusted
semantics tree, candidate verification file, and spec. Its 957 normalized
records, source lines, attributes, and per-record decisions are preserved in
`evidence/16-k-rule-inventory.log`:

- 928 supplied-semantics records;
- 27 candidate `verification.k` records; and
- two specification claims.

There are no candidate-local simplification rules, `[functional]`
declarations, or separately generated helper K files. The exact mapping from
every submitted constructor to fixed declarations/rules is
`evidence/used-construct-map.md`.

Because this is supplied-semantics mode, all 928 fixed records are the exact
selected trusted baseline. The rules in the target dependency cone were
manually checked for sequencing, strictness, lookup, binding, frame
creation/pop, allocation, list mutation, split, iteration, comparison, and
return. The remaining fixed records have leading constructors absent from both
the program and that closure and cannot match a target proof state; each is
classified in the inventory as fixed baseline outside the target dependency
cone. The non-exhaustive fixed `[total]` warnings concern `mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`; none is reachable here.

### Candidate-local record decisions

| Inventory records | Decision |
|---|---|
| K0929 `Music` | Accept as a disjoint, unbounded, finite ghost note algebra. |
| K0930 `musicCodes(Music)` | Not a truthful encoding definition: it has no equations and no connection to concrete strings. This is an unconnected result-bearing input abstraction and materially narrows the theorem domain. |
| K0931 `musicIter(Music)` | Accept only as a ghost iterable declaration. |
| K0932-K0935 ghost iterator equations | Internally disjoint, exhaustive, decreasing, and correct for the ghost constructors; conditional on the unproved input abstraction. |
| K0936 split rule | Reject. It is an operational bridge with no bridge-free universal theorem. It changes returned value kind, heap, `heapLoc`, and arbitrary continuation observations. |
| K0937-K0941 `musicAcc` | Accept. Base/whole/half/quarter cases are disjoint and exhaustive, recurse on a strict `Music` subterm, and append the documented 4/2/1 values. `[total]` is supported. |
| K0942-K0946 `musicLast` | Accept. Cases are disjoint/exhaustive and structurally decreasing; returned final token is correct. `[total]` is supported. |
| K0947-K0954 four macros and equations | Accept as non-overlapping syntax macros. Mechanical KAST comparison establishes the submitted program/body/closure term. |
| K0955 loop summary rule | Its state summary is supported by the separately proved K0956 claim against `PARSE-MUSIC-BASE`, and the body mutation is rejected. The installed rule frames an arbitrary continuation while the auxiliary claim proves an empty continuation. No universal context theorem is supplied. This straight-line loop has no abrupt effects, and no false continuation witness was found, so the broadening is recorded as a narrower evidence gap rather than independently labeled unsound. Its domain nevertheless begins at the unconnected ghost iterator. |
| K0956 loop claim | Sound, result-constraining partial-correctness statement over the ghost iterator. It is not itself a theorem about `str.split`. |
| K0957 entry claim | Result-constraining and syntactically pinned, but inadequate for real inputs and dependent on the rejected split bridge. |

### Required false-conclusion witnesses for the rejected bridge

The complete bridge match is:

```text
<k>
  #applyK(
    toCall(boundMethodV(str(musicCodes(M)), "split")),
    .Vals)
  ~> KREST
</k>
```

It has no guards on `M`, `KREST`, heap, heap location, stack, scopes, return,
exception, or exit cells. Priority 35 preempts the supplied no-argument split
rule at `methods.k:72-74`. Fixed semantics produces
`#alloc(list(splitWS(...)))`, returns a fresh `ref`, writes `<heap>`, and
increments `<heapLoc>`. The bridge instead produces `musicIter(M)` while
framing every state cell.

The ground, immediate-continuation observer in
`evidence/artifacts/bridge-observer.k` asks whether the split result is a
reference:

- With the bridge, the proof closes with result `false`, unchanged empty heap,
  and `heapLoc = 0` (`evidence/27-kprove-bridge-context.log`, `#Top`, exit 0).
- With only fixed supplied semantics, the identical ground redex and
  continuation close with result `true`, a new heap entry containing
  `splitWS(...)`, and `heapLoc = 1`
  (`evidence/29-kprove-no-bridge-context.log`, `#Top`, exit 0).

This is an executable false-conclusion witness over the bridge's own ground
match domain: the candidate extension and fixed semantics make opposite
observable conclusions from the same state and continuation.

The intended-domain witness is the concrete valid string `o o| .|` from stage
4. Fixed semantics produces the extra token-list allocation and `heapLoc = 2`,
whereas the submitted entry conclusion says there is no such allocation and
`heapLoc = 1`. The failing and corrected ground claims give both sides of that
witness.

There is also a value-level interpretation witness for the unconnected
abstraction. Since nothing fixes `musicCodes(whole(.Music))`, interpreting it
as the codes for `o|` would still make the bridge yield token `o` and result
`[4]`, while the real program on `o|` returns `[2]`. The theory does not admit a
concrete equality substitution because `musicCodes` is a distinct free
constructor; that is exactly the domain-pinning failure rather than evidence
for the intended encoding.

## 6. Fresh non-vacuity test

The auditor-created `evidence/artifacts/spec-vacuity.k` uses the satisfiable
ground start `M = whole(.Music)` and changes the required returned list from
the true `[4]` to the false `[5]`.

Commands:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module PARSE-MUSIC-VACUITY-SPEC --dry-run --output none

kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module PARSE-MUSIC-VACUITY-SPEC
```

The dry run exits 0, demonstrating that the mutation builds
(`evidence/22-vacuity-dry-run.log`). The actual proof exits 1 with
`WarnStuckClaimState`; its final heap contains the actual
`list(vCons(4,.ValSeq))`, which cannot unify with required `[5]`
(`evidence/23-kprove-vacuity.log`).

This is meaningful non-vacuity evidence: the submitted result is constrained
within the ghost theorem. It does not repair the theorem's input-domain or
operational-bridge defects.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the supplied K semantics extended by the candidate rules, for every
finite ghost `Music` term, a call of the exact submitted translated function
on the synthetic value `str(musicCodes(M))` terminates along the modeled path
with a freshly allocated output list equal to `musicAcc(.ValSeq,M)`. The loop
body itself is checked inductively and maps ghost whole/half/quarter tokens to
4/2/1. This is a non-vacuous theorem about the extended ghost execution.

It does not establish that any concrete valid Python string is an instance of
the precondition, that supplied `splitWS` produces that ghost iterator, or that
the entry destination matches fixed-semantics execution.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K 7.1.293 parser, compiler, Haskell/LLVM backends, and reachability logic | All builds/proofs | Ordinary machine-checking trust boundary; acceptable. |
| Exact supplied semantics tree and K builtin Int/Bool/String/Map/List operations | All concrete and symbolic execution | Launcher-trusted selected semantics; target dependency cone audited. ASCII-only string modeling is adequate for `o`, `|`, `.`, and spaces. |
| Trusted `py2mpy.py` transliteration | Program identity | Acceptable; trusted regeneration is byte-identical. |
| Candidate macros for program/body/closure | Entry and loop claims | Acceptable; expanded KAST is identical to the submitted translation. |
| `musicAcc`, `musicLast` mathematics | Loop and entry destinations | Acceptable, exhaustive recursive equations. |
| Isolated loop reachability claim | Installed K0955 summary and entry proof | Machine-checked against the base definition and body-sensitive. Arbitrary-continuation generalization lacks a universal context artifact, a non-fatal evidence gap relative to the decisive failure. |
| `musicCodes(Music)` as an encoding of source strings | Entry precondition, split bridge, final result association | Illegitimate. No equations, concrete constructor equality, connection theorem, or ground source-string instantiation exists. |
| Candidate split operational bridge | Entry proof and its exact heap destination | Illegitimate and observably false relative to fixed semantics: value kind, heap allocation, heap location, and continuation observations differ. |
| Differential testing | Candidate/canonical behavior on tested valid strings | Finite empirical support only; it cannot prove the ghost-to-concrete bridge. |
| Informal assertion that the proof-only iterator is “equivalent” | Candidate construction narrative | Untrusted prose contradicted by executable state and continuation witnesses. |

### Gate and benchmark decision

- Clean positive reconstruction: **PASS** as a verification event.
- Gate A real-program soundness: **FAIL**. The required split connection
  theorem is absent, and the installed bridge has concrete state/value
  counterexamples.
- Gate B intent adequacy: **FAIL**. The entry domain contains synthetic
  `musicCodes` terms rather than concrete valid music strings. This materially
  narrows/replaces the HumanEval source-contract domain.
- Non-vacuity: **PASS** inside the synthetic theorem.
- Evidence auditability: the reviewer evidence is reproducible, but evidence
  quality cannot redeem Gates A and B.

Under the benchmark mapping, a proof that uses an execution-bypassing,
observably inequivalent bridge and does not quantify over real source inputs is
`FAIL / NOT_LEGIT`, even though its internal positive claims print `#Top`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
