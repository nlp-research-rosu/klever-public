# Independent adversarial review: 89-encrypt

## Audit conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program. I reconstructed the definitions from trusted/source-only copies, ran
the complete positive specification to `#Top`, mechanically pinned the entry
claim to the regenerated program body, inventoried all 1,030 source-level K
declarations/rules/claims, and rejected fresh false-result and body mutations.
No candidate-introduced operational bridge, opaque result, oracle, domain
restriction, or answer-encoding rule is present.

The audit used the required `using-kit` and `validating-proof` workflows. The
candidate's `PROOF.md`, compiled directories, traces, logs, and reported
`VALIDATED` status were treated only as untrusted claims.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem `89-encrypt`, and the expected
container paths. The supplied reference semantics is present at
`/reference/reference-semantics`, so the trusted mounts agree with the rendered
mode.

All required pipeline-v3 records were present, regular/readable files:
`/run.json`, `/task.json`, `/generation-result.json`, invocation, metrics,
runtime metrics, usage, last message, output log, prompt, and the structured
trace. I parsed every one of the 289 trace JSONL records and read the entire
24,967-line generation output. Their prior `#Top`, mutation, and validation
statements were not reused as proof evidence. See
[01-generation-records.log](evidence/01-generation-records.log).

Independent integrity results are in
[01-provenance.log](evidence/01-provenance.log):

- `/audit-campaign-lock.json` is exactly equal as a JSON object to the campaign
  block in `/audit-input.json`; its SHA-256 is the recorded
  `e71e1d695e6ff...de40d0e`.
- The canonical, trusted prompt, trusted translator, candidate prompt,
  candidate translator, run/task/result records, and every required generation
  record have their recorded file hashes.
- The sole trace JSONL file has its recorded
  `3e6c0f2d...637273` hash. The independent path/kind/size/content trace-tree
  digest is `614d5e51...45b65`, equal to `usage.json`'s source-trace digest.
- The mounted candidate tree's independent pipeline manifest digest is
  `c8c910a3...e65788`, equal to both invocation and generation-result workspace
  digests.
- Candidate and trusted semantics have the same path/kind/size/content digest,
  `4495a50f...29ad1`. A second recursive per-entry comparison found identical
  directory/file sets and identical bytes. Neither tree contains a symlink or
  unsupported/mistyped entry.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.

The launcher also records its own mount/package digests (for example
`3c68b0c9...abf4` for both semantics trees and `5dd4496f...a0e` for the trace).
I did not rely on those launcher assertions: the independent regular-file,
per-file, recursive-entry, and pipeline-manifest checks above establish the
mounted content directly. There is no provenance or infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `encrypt(s)` to rotate each lowercase English
letter by `2*2 = 4` positions, wrapping within `a` through `z`. The trusted
canonical implementation uses the lowercase alphabet as a lookup table and
passes every non-lowercase character through unchanged.

The submitted `solution.py` uses an equivalent algorithm: for each character,
it checks `97 <= ord(c) <= 122`, computes
`chr(((ord(c)-97+4) % 26)+97)` in that branch, and otherwise appends `c`.
The signature is preserved.

Trusted regeneration produced a byte-identical `solution.mpy`; both submitted
and regenerated files hash to
`f8bb5c3f4be259c845fcc121f8563b6b6934d16553f3f507571cde1a2ba8e422`.
The exact command and result are in
[02-translator-identity.log](evidence/02-translator-identity.log).

The reviewer-authored differential
[differential_test.py](evidence/differential_test.py) imports the trusted
canonical and generated candidate from distinct file paths. It tested:

- all four documented examples;
- empty input, guard boundaries 96/97/122/123, every ROT4 wrap boundary, ASCII
  controls, punctuation, upper case, non-ASCII Unicode, and lone surrogates;
- every one of the 1,114,112 possible one-code-point Python strings;
- 2,500 seed-8904 composite strings and four long/broad strings.

All 1,116,641 comparisons matched. The complete bounded result is in
[02-differential.log](evidence/02-differential.log). There is no
canonical/docstring contradiction and no candidate/canonical divergence over
the intended Python-string domain.

## 3. Clean proof reconstruction

I copied only source proof artifacts plus the trusted prompt/canonical/
translator and trusted reference-semantics sources into
`/tmp/audit-work/reconstruction`. Candidate `runtime-kompiled`,
`verification-kompiled`, bytecode, and caches were neither copied nor used.
The live tools are K `v7.1.293`; see
[03-toolchain.log](evidence/03-toolchain.log).

Concrete definition:

```text
kompile /tmp/audit-work/reconstruction/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/concrete-kompiled
```

A reviewer-generated harness begins with the exact 279 submitted
`solution.py` bytes and adds boundary assertions. Fresh translation, LLVM
compilation, and `krun` exited 0 with final `.K`, `NoExc`, and exit code 0.
See [03-concrete-build-run.log](evidence/03-concrete-build-run.log).

Proof definition:

```text
kompile --backend haskell \
  /tmp/audit-work/reconstruction/verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/reconstruction/verification-kompiled
```

That clean build exited 0
([03-proof-build.log](evidence/03-proof-build.log)). The loop helper claim
independently printed `#Top` and exited 0
([03-kprove-encrypt-loop.log](evidence/03-kprove-encrypt-loop.log)). The actual
positive target command, which proves the complete `SPEC` module with both
claims available, was:

```text
kprove /tmp/audit-work/reconstruction/spec.k \
  --definition /tmp/audit-work/reconstruction/verification-kompiled \
  --spec-module SPEC
```

It printed literal `#Top` and exited 0 in 6.4 seconds; see
[03-kprove-all-claims.log](evidence/03-kprove-all-claims.log).

For completeness, I diagnostically selected `SPEC.encrypt-entry` alone. That
selection removes the separately named `encrypt-loop` circularity, so the
backend kept unrolling the symbolic loop; I interrupted it with exit 130. It
is not the candidate's target command and says nothing adverse about the
complete proof. The command and interpretation are preserved in
[03-claim-selection-diagnostic.md](evidence/03-claim-selection-diagnostic.md).

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.encrypt-loop` has no `requires` clause. For arbitrary remaining
`S:IntSeq`, accumulator `A:IntSeq`, prior loop-target value `C0`, original
input, closure value, and preserved continuation, it starts at the supplied
semantics' real:

```text
#loop(str(S), Name("c"), exact-submitted-If-body)
```

in function scope 1. It reaches the continuation with `out` changed from
`str(A)` to `str(encryptFold(A,S))` and `c` changed from `C0` to
`finalLoopChar(S,C0)`. It is a derived circularity, not an operational rule in
the compiled definition. The empty case terminates under fixed semantics; the
cons case executes one actual iterator yield, target bind, branch, builtin
calls, arithmetic/concatenation, and scope update before recursive reuse.

`SPEC.encrypt-entry` also has no `requires` clause. For arbitrary
`S:IntSeq`, it starts from the standard module configuration, loads the exact
submitted function binding plus the audit-only statement:

```text
result = encrypt(str(S))
```

and reaches `.K` with the exact closure still bound and `result` equal to
`str(encryptResult(S))`. It additionally constrains scope allocation, heap,
heap allocation, stack, return state, and exception state to normal final
values. The omitted exit-code cell is framed and the program has no exit
operation.

### Mechanical pinning

The reviewer checker
[program_pinning.py](evidence/program_pinning.py) removes whitespace only
outside K String tokens and extracts balanced constructor terms. It established:

- trusted regeneration equals submitted `solution.mpy`;
- the sole submitted `FuncDef` constructor has digest
  `07935c5c...91bf2`;
- the first constructor inside the entry claim's loaded `Module` is byte-for-
  byte the same normalized constructor with the same digest;
- the only remaining loaded constructor is exactly
  `Assign(Name("result"),Call(Name("encrypt"),str(S:IntSeq)))`;
- the target closure contains the exact same body once, at definition scope 0;
- the postcondition contains exactly one
  `"result" |-> str(encryptResult(S))` binding and no entry precondition.

Thus the claim runs a harness around the submitted function; it does not prove
a substituted implementation or a free summary. See
[04-program-pinning.log](evidence/04-program-pinning.log).

Every Python `str` is representable as a finite `IntSeq` of code points. The
model admits additional integer sequences too, so this is a superset rather
than a narrowing. Although supplied `Str(String)` source literals and `chr`
are ASCII-limited, every program literal is ASCII and the guarded arithmetic
can call `chr` only with 97 through 122. Arbitrary input code points are carried
symbolically and take the pass-through branch. Therefore there is no supplied-
model representation gap on the source-contract domain.

Concrete satisfying substitutions are recorded in
[04-witness-substitution.log](evidence/04-witness-substitution.log). In
particular:

- entry witness: `S=.IntSeq`, empty module/heap/stack, env 0, `noRet`, `NoExc`;
  formal summary, canonical, and candidate all return `""`;
- loop witness: `S` is the four-character string backtick–`a`–`z`–`{`,
  accumulator `"PREFIX:"`, `c=""`, env 1; the post-substitution appends the
  corresponding backtick–`e`–`d`–`{` ciphertext and leaves `c="{"`;
- additional boundary, Unicode, and surrogate witnesses agree among the formal
  equations and both Python implementations.

The independent body-sensitivity claim changes the executed constructor from
ROT4 to ROT5. It parses successfully, but for `"w"` fixed execution yields
code 98 (`"b"`) and cannot meet the unchanged ROT4 code-97 (`"a"`) result.
`kprove` reports `WarnStuckClaimState` and exit 1. See
[04-body-sensitivity-dry-run.log](evidence/04-body-sensitivity-dry-run.log) and
[04-body-sensitivity-proof.log](evidence/04-body-sensitivity-proof.log).

## 5. Rule-by-rule static soundness review

The exhaustive source-level inventory is
[05-rule-inventory.md](evidence/05-rule-inventory.md), generated by
[k_rule_inventory.py](evidence/k_rule_inventory.py) from the clean sources.
It lists every item with full normalized text, attributes, target relation,
and assessment:

| Kind | Count |
|---|---:|
| Configuration | 1 |
| Syntax declarations | 249 |
| Contexts | 5 |
| Rules | 773 |
| Claims | 2 |
| Total | 1,030 |

The import/reachability classification is: 107 used fixed-semantics items, 845
target-inert fixed items, 32 `MPY-CONCRETE` items excluded from the proof import
graph, 30 opaque target-inert items, 14 proof-local items, one loop claim, and
one target entry claim. The compact used-path mapping, including declarations,
evaluation order, state footprints, calls/returns, guards, and priorities, is
[05-used-rule-map.md](evidence/05-used-rule-map.md).

### Submitted syntax and fixed operational path

Every submitted constructor is declared: `Module`, `FuncDef`, `Params`,
statement sequencing, `Expr/Str`, `Assign`, `For`, `If`, `BoolOp`, `Compare`,
`CmpOp`, `Call`, `Name`, `Int`, `AugAssign`, `BinOp`, and `Return`. The actual
path uses:

- standard module loading and left-to-right statement sequencing;
- module/function/builtins scope lookup and ordinary closure call frames;
- one-time iterable evaluation and structural string iteration;
- target binding to the current scope;
- short-circuit Boolean evaluation and integer comparisons;
- `ord`, guarded integer arithmetic/`pyMod`, ASCII-safe `chr`;
- string `seqConcat`, return, frame pop, and caller result assignment.

Strict/seqstrict declarations plus the explicit call argument loop preserve
the program's evaluation order. The body allocates no heap objects and has no
output, exceptions, mutation outside its local scope, or abrupt loop control.
The entry postcondition checks normal control/state, not only a value.

Fixed priorities for heap refs, cells, math/hashlib interceptions, collection
operations, and sorting have nonmatching constructor heads/guards. The generic
call rule is `[owise]`, but no higher-priority interception matches
`encrypt`, `ord`, or `chr`; ordinary lookup and call dispatch therefore applies.

### Proof-local inventory

`verification.k` contains exactly five `[function,total]` declarations and nine
equations:

| Extension | Classification and audit |
|---|---|
| `rot4Code` | Definitional summary. Its sole unguarded equation is exactly `pyMod(C-97+4,26)+97`; no operational term or cell is matched. |
| `encryptedChar` | Definitional summary. The guards `C<97`, `97<=C<=122`, and `C>122` are pairwise disjoint and exhaustive; each result is the source branch's singleton code sequence. |
| `encryptFold` | Definitional summary. Empty/cons cases are disjoint and exhaustive, and recursion strictly descends on the second `IntSeq`. It names the repeated `out += ...` transition proved by the loop claim. |
| `encryptResult` | Direct wrapper equation initializing the accumulator to `.IntSeq`. |
| `finalLoopChar` | Definitional bookkeeping. Empty/cons cases are exhaustive and structurally descending; it affects only final local-scope matching, not ciphertext. |

There are no proof-local `<k>` rules, priorities, simplifications, `[concrete]`
rules, `[owise]` equations, opaque/no-evaluator symbols, fresh values, or
unconstrained oracles. No extension bypasses lookup, calls, the loop, builtins,
return, or state effects. Automated guard/range/descent checks are in
[05-proof-local-checks.log](evidence/05-proof-local-checks.log).

The supplied semantics contains opaque float, sorting, and MD5 symbols for
other tasks. None occurs in the program term, either claim, any proof-local RHS,
or a target residual. Likewise, compiler warnings concern target-inert supplied
functions. The supplied model is partial for many unused Python operations;
an unmodeled unused construct is not a false conclusion for this theorem.

I found no rule that enables a false conclusion on an intended input. Hence
there is no unsoundness claim requiring a counterexample witness.

## 6. Fresh non-vacuity test

I did not reuse candidate `spec-vacuity.k`. The reviewer-authored
[audit-spec-vacuity.k](evidence/audit-spec-vacuity.k) executes the exact
submitted closure on satisfying input `"z"` but changes the result obligation
from the true `"d"` (code 100) to false `"e"` (code 101).

The dry run parsed/compiled the mutation and exited 0:
[06-vacuity-dry-run.log](evidence/06-vacuity-dry-run.log). The real proof then
exited 1 with `WarnStuckClaimState`. Its terminal residual contains:

```text
<k> str(iCons(100, .IntSeq)) ~> .K </k>
```

which is the expected unmet result rather than a parser, import, timeout, or
unrelated backend failure. See
[06-vacuity-proof.log](evidence/06-vacuity-proof.log). The proof is
result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Formally established

Conditional on the fixed supplied semantics and K implementation, the
successful reachability proof establishes this partial-correctness statement:
for every finite `S:IntSeq`, executing the exact regenerated/submitted
`encrypt` binding in the entry harness reaches normal completion with
`result = str(encryptResult(S))`, where each code `C` becomes
`((C-97+4) mod 26)+97` exactly when `97<=C<=122`, and is unchanged otherwise.
The theorem is unbounded in string length. It also establishes the claimed
scope, heap, allocator, stack, return, and exception state. It is not merely a
finite test and does not assert a separate total-correctness/liveness theorem.

### Trust ledger

| Boundary | Effect and dependents | Assessment/evidence |
|---|---|---|
| Supplied `MPY` semantics on the used path | Determines value, evaluation order, loop/call/return control, scopes, heap, and exceptions for both claims. | Acceptable fixed benchmark boundary. Candidate tree is recursively identical to trusted semantics. Used rules were statically mapped and concrete boundary cases executed. |
| K parser/compiler, Haskell backend, solver, and reachability/circularity implementation | Establishes clean `#Top` and rejects false claims. | Standard machine-checking trust boundary; live K 7.1.293, clean builds, positive and negative runs recorded. |
| K builtin integer/Boolean/String/Map/List mathematics | Supports comparisons, `pyMod`, sequence structure, and state maps. | Ordinary mathematical/toolchain primitives; the target uses only simple integer and algebraic-sequence cases. |
| Trusted `py2mpy.py` transliteration | Connects `solution.py` AST to `solution.mpy`. | Byte-identical trusted/candidate translator; trusted regeneration is byte-identical; constructor-level claim pinning and body mutation give independent support. |
| Python source/canonical intent bridge | Connects the formal per-code summary to the HumanEval contract. | Direct algebraic correspondence plus 1,116,641 zero-mismatch differential cases. Testing supports this bridge but is not substituted for K proof. |
| `IntSeq` as Python-string representation | Relates modeled codes to CPython characters. | Every CPython string is representable; the theorem covers all such sequences and more. ASCII-only source-literal/`chr` limitations are not reached outside ASCII literals/results, so no contract-domain gap exists. |

There is no proof-local trusted primitive, result-bearing opaque symbol,
empirical operational bridge, or informal assumption that fixes the answer.
Differential and concrete testing support only the source/model/translator
bridges stated above; they are not presented as universal proof.

### Gate and benchmark decision

- Gate A (real-program soundness): pass. Exact body execution, complete state
  footprint, sound total summaries, satisfying witnesses, body sensitivity,
  and fresh false-result rejection all hold.
- Gate B (intent adequacy): pass. The theorem covers every finite modeled
  string and every Python string, with no candidate narrowing, fixed sizes, or
  bounded unrolling; its postcondition is exactly canonical ROT4.
- Gate C (trust/evidence auditability): pass. All boundaries and dependents are
  explicit, and commands, scripts, positive/negative outputs, and the complete
  rule inventory are preserved.

There is no material adequacy gap and no non-fatal model/evidence limitation
requiring the campaign amendment's `CONCERNS` mapping.

VERDICT: PASS
LEGITIMACY: LEGIT
