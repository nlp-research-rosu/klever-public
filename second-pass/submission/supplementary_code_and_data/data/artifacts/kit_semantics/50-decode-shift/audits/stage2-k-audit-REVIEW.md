# Independent adversarial review: 50-decode-shift

This review treats every candidate artifact and generation record as untrusted
evidence. All executions used fresh source copies under
`/tmp/audit-work/50-decode-shift`; neither candidate kompiled directory nor any
candidate cache was copied or used.

## 1. Input and provenance integrity

Status: **PASS**.

`/audit-input.json` declares `record_layout = pipeline-v3`,
`condition = kit-semantics`, and `semantics_mode = SUPPLIED_SEMANTICS`. The
trusted `/reference/reference-semantics` tree is present, so the mounted inputs
agree with the rendered mode.

I checked every required pipeline-v3 record:

- `/run.json`, `/task.json`, `/generation-result.json`
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, and `usage.json`
- `/generation-evidence/codex-last.txt`, `codex-output.log`, and `prompt.txt`
- the sole 295-line JSONL trace under
  `/generation-evidence/codex-trace/2026/07/25/`

All required files are real regular readable files, all required trees are real
directories, every structured record parses, and there are no symlinks in the
candidate supplied-semantics tree, trusted semantics tree, or generation
evidence. The generation output is valid UTF-8 (715,412 bytes, 18,832 lines,
no NUL bytes). These records claim a successful proof, but no such claim was
used as proof evidence.

The audit campaign object is structurally identical to
`/audit-campaign-lock.json`, whose SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded file hash checked by the audit matches its mounted bytes.
Independent pipeline-tree hashes also bind the mounted trees to their source
manifests:

- candidate tree:
  `2a5edf00bdcb8c91d225bf4344e53ceee8640586ed80955d92d9164ce19c2830`,
  equal to the invocation output workspace hash;
- trusted and candidate semantics trees:
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  equal to the task input semantics hash;
- trace tree:
  `066b16468d489608fb91f533e473a3b52eb059da029e20162ed11c8866ebce60`,
  equal to the usage record's source-trace hash.

The candidate and trusted `prompt.py` files are byte-identical; so are their
`py2mpy.py` files. A recursive path/type/byte comparison of
`/candidate/reference-semantics` against
`/reference/reference-semantics` found no missing, additional, mistyped,
changed, or linked entry. Thus the supplied-semantics integrity boundary is
intact. The check is reproducible in
`evidence/integrity_check.py` and `evidence/01-integrity.log`.

## 2. Program fidelity and candidate-versus-canonical checks

Status: **PASS**.

### Contract and implementation

The trusted prompt supplies `encode_shift`, which maps each character to the
lowercase alphabet by shifting its code forward by five modulo 26. The required
`decode_shift(s)` takes a string produced by that encoder and returns the
original string. The range of `encode_shift` is exactly the finite lowercase
ASCII strings: every output character is in `a` through `z`, and each such
string has a lowercase preimage.

The trusted canonical decoder maps every input code `C` to

```text
((C - 5 - 97) mod 26) + 97.
```

`/candidate/solution.py` implements the same formula in an accumulator-based
`for` loop. It has the requested signature and preserves order and length. Its
only control-flow boundary is the empty/nonempty loop case; its arithmetic
wraps for input codes `a` through `e` and does not wrap for `f` through `z`.

### Trusted regeneration

In scratch I ran:

```text
python3 py2mpy.py solution.py > solution.mpy
cmp -s solution.mpy solution.submitted.mpy
```

Both commands exited 0. The regenerated and submitted files have the same
SHA-256,
`7147a83014f826f194d82fd44e5255f53c81602bc63c525837363ab8229ace81`.
See `evidence/02-translation-identity.log`.

### Independent differential

`evidence/differential_test.py` imports the trusted canonical and prompt
modules and the generated solution from explicit scratch paths. It tests the
empty input; codes `a`, `e`, `f`, and `z`; wrap-transition pairs; every
one-character input; every lowercase string of lengths zero through three;
full and reversed alphabets; long uniform strings; and 2,100 deterministic
generated strings of lengths 4 through 127. The prompt contains no explicit
example assertions to replay.

There were zero mismatches over 20,419 direct generated-versus-canonical cases
and zero mismatches over 20,419 `decode_shift(encode_shift(x)) = x` cases.
Command and result are in `evidence/03-python-differential.log`. This is finite
fidelity evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

Status: **PASS**.

Only these source artifacts were copied into scratch: the candidate's
`solution.py`, submitted `solution.mpy`, `verification.k`, and `spec.k`; the
trusted prompt, canonical, translator, and supplied semantics. Fresh
definitions were written to `reviewer-runtime-kompiled` and
`reviewer-verification-kompiled`.

The installed `kompile`, `kprove`, and `krun` are all K v7.1.293; pyk is
7.1.293; and the K source commit is
`ff15baac9e66426612ec45ff912af7f14965b64a`, matching the launcher records.
See `evidence/04b-k-toolchain-binding.log`. The broader frozen-toolchain helper
recorded in `evidence/04-toolchain.log` could not find Lean on this subprocess's
PATH. Lean is not an input, backend, or proof artifact for this K-only task;
the K-specific binding and all required K executions succeeded, so this does
not create uncertainty about the reconstructed candidate proof.

### Concrete definition

The trusted supplied semantics compiled from source with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition reviewer-runtime-kompiled
```

It exited 0. Its warnings concern imported but unused total functions and
unused variables. A trusted-translation concrete harness containing the exact
candidate function tested empty input, both sides of the modulo boundary,
the endpoint letters, a simple sequence, and the full alphabet. `krun` exited
0 with `.K`, `NoExc`, and exit code 0. See
`evidence/05-fresh-llvm-build.log`,
`evidence/06-fresh-concrete-execution.log`, and
`evidence/concrete-audit.py`.

### Proof definition and positive claims

The Haskell proof definition compiled from source:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition reviewer-verification-kompiled
```

It exited 0 (`evidence/07-fresh-haskell-build.log`). The complete positive
command

```text
kprove spec.k --definition reviewer-verification-kompiled --spec-module SPEC
```

exited 0 and printed `#Top`
(`evidence/08-positive-proof-all.log`). I also isolated the claims:

- `SPEC.character-inverse`: exit 0, `#Top`;
- `SPEC.loop-invariant`: exit 0, `#Top`;
- `SPEC.loop-invariant,SPEC.decode-shift`: exit 0, `#Top`.

The entry claim properly depends on the loop circularity, so it was selected
with that dependency rather than deleting the lemma from the proof set. Exact
commands, outputs, and statuses are in
`evidence/09-positive-proof-per-claim.log`. The arithmetic inverse emits
`WarnTrivialClaim` because function simplification and integer reasoning
discharge it without operational rewriting; its satisfiable precondition
prevents that from being vacuity.

## 4. Adequacy and real-program pinning

Status: **PASS**.

### Claims in plain language

1. `character-inverse` says that for every integer code `C` from 97 through
   122, applying the declared forward shift and then the declared backward
   shift equals `C`.
2. `loop-invariant` says that, in the exact plain local frame and exact module
   and builtins scopes, executing the submitted loop over remaining lowercase
   code sequence `CS` changes `result` from `str(ACC)` to
   `str(decodeAcc(CS,ACC))`. It preserves the continuation and all framed cells;
   only the final loop-variable value is existential.
3. `decode-shift` says that, for every finite code sequence satisfying
   `lowerCodes`, calling the exact `decode_shift` closure returns
   `str(decodeAcc(CS,.IntSeq))` and restores environment, scopes, allocation
   state, heap, stack, return state, exception state, and exit code.

These are result equalities, not implications to a free output variable.

### Mechanical constructor comparison

`evidence/program_pinning_check.py` parses balanced constructor applications
from regenerated `solution.mpy` and `spec.k`, tokenizes their constructor terms,
and removes only explicit `.Stmts` units that the translator's list macro may
omit. It found exactly two closure bodies in `spec.k`, and both are identical
to the regenerated `FuncDef` body: 145 normalized tokens with digest
`fa041561232c8ccd39515e9a2958412ab7a0ba0b9e6447fd618a08ca9b92f5a1`.
The `#loop` body is also identical to the actual translated `For` body: 94
tokens with digest
`8d36b91716e8b7f73b4fd358bb86dae57e3ff61121ea43c7922cc6b26ec09bb1`.

The comparison also checks function name `decode_shift`, sole parameter `s`,
definition environment 0, and both entry and invariant closures. Thus the claim
executes the same function binding and body as the byte-identical submitted
program, with only the demonstrated list-unit macro normalization. It does not
prove a substituted helper or summarized call.

### Satisfying states and ground results

Concrete witnesses exist for every precondition:

- `character-inverse`: `C = 97`;
- `loop-invariant`: `CS = ACC = INPUT = .IntSeq` and
  `CH = str(.IntSeq)` in the displayed exact frame;
- `decode-shift`: `CS = iCons(102,.IntSeq)` (the input `"f"`).

For `""`, `"a"`, `"e"`, `"f"`, `"z"`, `"fghij"`, and the full alphabet, the
ground `decodeAcc` result equals both Python implementations. Representative
results include `"a" -> "v"`, `"e" -> "z"`, `"f" -> "a"`, and
`"z" -> "u"`. Full evidence is in `evidence/10-program-pinning.log`.

A separate body-sensitivity mutation changed all shift literals in the
executed loop and closure terms from 5 to 4 while leaving the summary
unchanged. It parsed, ran, and exited 1 with `WarnStuckClaimState`; the residual
contrasts the original `C - 102` result with the mutated `C - 101` result.
See `evidence/spec-body-sensitivity-audit.k` and
`evidence/12-body-sensitivity.log`.

## 5. Rule-by-rule static soundness review

Status: **PASS**.

`evidence/rule-inventory.tsv` is an exhaustive inventory of every source-level
syntax declaration, configuration, context, rule, and claim in
`reference-semantics/semantics.k`, every required helper K file,
`verification.k`, and `spec.k`. Its 941 rows exactly equal an independent
source statement-start count:

- 231 syntax declarations;
- one configuration;
- five evaluation contexts;
- 701 rules (456 function equations, seven macro equations, and 238
  operational rules);
- three reachability claims.

It records every `function`, `total`, `functional`, `no-evaluators`, priority,
`owise`, concrete, and simplification attribute. There are 149 function
declarations, 111 total declarations, no `functional` declarations, 22
`no-evaluators` declarations, 29 priority rules, and no simplification rules.
Completeness and raw attribute evidence are in
`evidence/11-k-inventory.log` and
`evidence/14-static-completeness-scan.log`.

### Proof-local extensions

`verification.k` contains exactly four declarations and six equations:

| Extension | Classification and decision |
|---|---|
| `decodeCode(C)` | Total definitional summary, one unconditional equation: `pyMod(C-102,26)+97`. It names the actual source arithmetic and does not rewrite operational state. |
| `encodeCode(C)` | Total definitional summary, one unconditional equation: `pyMod(C-92,26)+97`, algebraically the trusted prompt's `C+5-97` formula. |
| `decodeAcc(CS,ACC)` | Total structural definition. Empty input returns `ACC`; the constructor case appends `decodeCode(head)` and recurs on the strict tail. Cases are disjoint and exhaustive. |
| `lowerCodes(CS)` | Total structural predicate. Empty is true; the constructor case checks 97–122 and recurs on the strict tail. Cases are disjoint and exhaustive. |

There are no proof-local priority rules, simplifications, concrete rules,
opaque/no-evaluator symbols, or operational rewrites. The definitions do not
replace any program-defined call. The universally quantified fixed-semantics
loop claim is the connection theorem from real execution to `decodeAcc`; the
entry then uses that proved circularity.

### Material fixed-semantics path

Every submitted construct is mapped to its syntax and semantics in
`evidence/static-review-summary.md`. On the pinned state the operational order
is:

```text
exact closure lookup
-> callee evaluation
-> left-to-right argument evaluation
-> fresh plain call frame and parameter binding
-> ASCII docstring evaluation/discard
-> result/ch initialization
-> one-time string iterable evaluation
-> finite string iterator steps
-> loop target binding
-> result lookup
-> ord lookup/call
-> left-to-right integer -, %, + evaluation
-> chr lookup/call
-> string concatenation
-> result assignment
-> return and frame restoration
```

The exact scope chain fixes `ord` and `chr` to the builtins frame; no shadow
binding is possible. `ord` receives a one-character string. For every
precondition-satisfying input, modulo 26 yields 0–25 and `chr` receives
97–122, inside the supplied ASCII guard. The loop rules preserve the suffix and
do not introduce return, exception, allocation, or other abrupt effects.
String values are immutable code sequences, so the assignment is the only
material state change inside the loop. Return restores all entry cells.

The priorities in the supplied definition apply to cells, heap references,
special calls, collections, or unrelated control constructs. Their guards and
sorts do not match this exact plain string/integer execution. No material rule
is opaque or concrete-only.

The supplied baseline has a broader unused trust surface: 19 opaque float
symbols, opaque symbolic sort and keyed-sort symbols, opaque MD5 codes,
concrete-only equations, and partial valid-program helpers. Compiler
non-exhaustiveness warnings likewise concern unused `mapStrVS`, float,
`joinCodes`, and `valSeqAt` cases. None can be constructed on this program's
path, appears in a proof-local definition, or influences a branch/result/cell
in these claims. They are recorded as unused fixed-semantics boundaries, not
smuggled correctness conclusions. No inventoried rule enables a false
conclusion for a lowercase input, so there is no unsound-rule claim requiring a
false-conclusion witness.

## 6. Fresh non-vacuity test

Status: **PASS**.

I did not reuse the candidate's `spec-vacuity.k`. The fresh mutation
`evidence/spec-false-result-audit.k` changes only the target of the entry claim:

```text
str(decodeAcc(CS,.IntSeq))
```

becomes

```text
str(seqConcat(decodeAcc(CS,.IntSeq),iCons(120,.IntSeq))).
```

For the satisfying witness `CS = .IntSeq`, the real and formally summarized
result is `""`, whereas the mutated target is `"x"`.

The mutated spec's `kprove --dry-run` exited 0, showing that it imports and
builds successfully. The actual proof then exited 1 with
`WarnStuckClaimState`. Its residual is the expected unmet equality:

```text
decodeAcc(CS,.IntSeq)
= seqConcat(decodeAcc(CS,.IntSeq),iCons(120,.IntSeq)).
```

This is a reachable result obligation, not a parser error, missing import,
timeout, or unrelated backend failure. Exact mutation, commands, statuses, and
bounded output are in `evidence/13-fresh-nonvacuity.log`.

## 7. Proven versus assumed accounting

Status: **PASS**.

### Formally proven

Under the supplied `MPY` semantics, for every finite `IntSeq CS` whose elements
are all 97 through 122, if the exact submitted `decode_shift` call terminates,
it returns the string obtained by shifting every code backward by five modulo
26 in the same order, with the listed initial machine state restored. The
fixed-semantics loop claim proves this for arbitrary remaining `CS` and
arbitrary accumulator `ACC`. Separately, the arithmetic claim proves that this
backward code transformation is the inverse of the prompt's forward
transformation for every lowercase code.

This is unrestricted over the finite lowercase-string domain; it is not a
finite-size theorem or bounded unrolling. It is partial correctness, not a
separate termination/resource theorem.

### Assumptions and trust boundaries

| Boundary | Dependents | Decision |
|---|---|---|
| Supplied `MPY` definition models the relevant Python subset | All operational claims | Acceptable by the rendered mode. The material rules were statically reviewed and concretely exercised; ASCII strings, unbounded K integers, plain calls/loops, and the used builtins agree with the intended execution. Unicode and unsupported exceptions are outside the theorem. |
| Trusted `py2mpy.py` transliterates the candidate AST | Program identity | Acceptable. Regeneration is byte-identical, constructor comparison pins the exact closure/loop, and a material constructor-body mutation breaks the proof. |
| K frontend, Haskell/LLVM backends, SMT reasoning, and host execution are correct | Machine checking | Ordinary low-level proof-tool trust. Versions and source commit are recorded and fresh reconstruction succeeds. |
| Natural-language “encoded with `encode_shift`” means a finite lowercase encoded string | Intent/domain alignment | Acceptable and non-narrowing. The encoder's range is exactly finite lowercase ASCII strings; the arithmetic inverse is universally proved and the Python bridge has broad independent finite tests. |
| 22 opaque supplied symbols and other unused imported facilities | None of these claims | Acceptable unused baseline surface. No such term can arise or influence the result; no conclusion is conditional on its interpretation. |
| Differential and concrete tests | Fidelity/bridge evidence only | Properly limited. They support translation/model adequacy but are not treated as universal proof or as a substitute for `kprove`. |

Gate A passes: real code executes, all state/control effects are accounted for,
the proof-local equations are sound, preconditions are satisfiable, body
sensitivity holds, and a false result is rejected. Gate B passes: the formal
domain equals the source contract's encoded-string domain and the postcondition
is the requested inverse. Gate C passes: all commands, scopes, assumptions, and
finite evidence are reproducible and separately identified.

The reconstructed proof is result-constraining, non-vacuous, universally scoped
over the material source domain, and mechanically pinned to the real generated
program. No material adequacy or soundness gap remains.

VERDICT: PASS
LEGITIMACY: LEGIT
