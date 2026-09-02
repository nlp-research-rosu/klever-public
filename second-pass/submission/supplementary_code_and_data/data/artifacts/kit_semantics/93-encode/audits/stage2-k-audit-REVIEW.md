# Independent adversarial audit: HumanEval 93 `encode`

The candidate contains a legitimate partial-correctness proof of the submitted
program under the supplied MPY semantics. I rebuilt both definitions from
source, independently proved the only target claim, mechanically pinned the
claim's executed term to regenerated `solution.mpy`, inventoried every supplied
and proof-local K declaration/rule, and rejected fresh body and result
mutations. Candidate-provided compiled definitions, logs, `PROOF.md`, and
generation conclusions were not used as proof evidence.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3` and
`semantics_mode: SUPPLIED_SEMANTICS`. The rendered condition and trusted mounts
are consistent: `/reference/reference-semantics` exists.

The independent checker and complete bounded output are
`evidence/provenance_check.py` and
`evidence/01b-provenance-and-generation-records.log`.

- The `audit_campaign` object equals `/audit-campaign-lock.json` exactly, and
  the lock's SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- Every required `pipeline-v3` record is a readable regular file:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the structured trace.
- All recorded file and trace-member hashes reproduced. The one trace JSONL
  file has the recorded SHA-256
  `6bb4e83258684064480a8c77f21b64a24d50fd3bafebd00a1fc30ab52edd6e38`;
  all 214 lines parse as JSON. The generation records claim success, three
  logged `#Top` markers, and a final `KPROVE_PASSED`, but those remain
  untrusted historical claims.
- Candidate and trusted `prompt.py` are byte-identical at SHA-256
  `856a164439599802d5210e2969c1c5673c84b83b4bdca5db34384d7b10d3d741`.
  Candidate and trusted `py2mpy.py` are byte-identical at SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- The candidate and trusted reference-semantics trees have exactly the same
  directory plus 24 regular K files, with the same per-file SHA-256 values and
  no missing, additional, mistyped, changed, or symlinked entries. There are
  no symlinks anywhere under `/candidate`, `/reference`, or
  `/generation-evidence`.

For directory inputs I used an explicit entry-by-entry manifest and a
reviewer-defined canonical manifest digest rather than trusting the launcher's
opaque aggregate tree hash. This directly checks the source entries relevant
to the audit. There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt asks `encode(message)` to swap the case of English letters,
then replace each vowel with the English-alphabet letter two places later.
Although it says “Assume only letters,” its second required example includes
spaces, which therefore must pass through unchanged. The trusted canonical
implementation performs `message.swapcase()` and then maps the ten ASCII vowel
codes.

`/candidate/solution.py` performs the same operation as a method chain:
`swapcase`, followed by replacements
`a/e/i/o/u -> c/g/k/q/w` and
`A/E/I/O/U -> C/G/K/Q/W`. Replacement outputs are consonants, so later
replacements cannot transform them again.

Fresh trusted translation was run in `/tmp/audit-work/93-encode`:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated terms are byte-identical at
SHA-256
`fc50d53a7c774d8a12149ad71f3ab5988849f3623c8c83d72d4ed772e3c8f630`;
see `evidence/02-translation-identity.log`.

The independent differential script
`evidence/independent_differential.py` imports the trusted canonical and
candidate entry points directly. It checked both documented examples, the
empty string, every ASCII code-point and alphabetic branch boundary, exhaustive
English-letter/space strings through length two, and deterministic generated
ASCII/Unicode strings. Result:

```text
TOTAL checked=3256 mismatches=0
EXIT_STATUS: 0
```

The two required outputs were independently confirmed as `TGST` and
`tHKS KS C MGSSCGG`. See
`evidence/03-independent-differential.log`. This testing supports program
fidelity; it is not substituted for the K proof.

## 3. Clean proof reconstruction

Only source files and the trusted reference semantics were copied into
`/tmp/audit-work/93-encode`. Neither `/candidate/runtime-kompiled` nor
`/candidate/verification-kompiled` was copied or used.

Fresh concrete build:

```text
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition concrete-kompiled-audit
```

This exited 0 (`evidence/04-concrete-build.log`). A reviewer probe whose
function AST was mechanically checked equal to `solution.py` was translated
with the trusted translator and run with:

```text
krun concrete-probe.mpy --definition concrete-kompiled-audit
```

It checked the empty input, both examples, every vowel in both cases,
consonants, spaces, and mixed-case vowels. `krun` exited 0 at `.K`, with empty
heap/stack, `noRet`, `NoExc`, and exit code 0
(`evidence/concrete_probe.py`, `evidence/05-concrete-execution.log`).

Fresh proof build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled-audit
```

This exited 0 (`evidence/06-proof-build.log`). Static enumeration found exactly
one positive target claim, `SPEC.encode`. Its independent proof command was:

```text
kprove spec.k --definition verification-kompiled-audit --spec-module SPEC
```

It printed exactly one `#Top` and exited 0
(`evidence/07-positive-proof.log`). Thus every positive target claim closes in
the fresh source-only reconstruction.

LLVM reported non-exhaustive-totality warnings for unrelated map/float/join/
subscript functions; the Haskell build and proof reported only unused variables
in `strLt`. None of those symbols is on the target execution path, as checked
in Stage 5.

## 4. Adequacy and real-program pinning

### Formal entry claim

`SPEC.encode` has no `requires` clause. Its source configuration says:

- load the exact `Module(FuncDef("encode", ...))`;
- call the resulting module binding on arbitrary `str(CS:IntSeq)`;
- start at environment 0, fresh module/builtins scopes, scope location 1,
  empty heap and stack, `noRet`, `NoExc`, and exit code 0.

This precondition is satisfiable. Examples include `CS = .IntSeq` and
`CS = iCons(117, .IntSeq)`, the modeled string `"u"`.

The destination constrains the return to:

```text
str(replaceC(... replaceC(mapSwap(CS), 97, 99) ..., 85, 87))
```

with all ten exact replacements. It also constrains the installed function
binding and every configuration cell: restored environment/scope location,
empty heap and stack, `noRet`, `NoExc`, and exit code 0. The result is neither
free nor implication-only. There are no loops or helper claims.

### Mechanical program identity

`evidence/extract_spec_program.py` extracts the balanced `Module(...)` argument
from `#loadAll`. The claim writes the variadic expression-list unit explicitly
as `.Exprs`, while `.mpy` program syntax represents the same unit by a trailing
comma and omission. After only that unit normalization, both the submitted
`solution.mpy` and extracted claim program were parsed by the same fresh K
syntax into canonical JSON KAST. Their KAST SHA-256 values are identical:

```text
f9f9d443d1a48fcfdf1cc010abe08eb619e0679b615b88efd836a177523ad95e
constructor_level_cmp_status=0
```

See `evidence/08c-program-term-pinning-normalized.log`. Two earlier diagnostic
attempts (`08-...` and `08b-...`) are preserved; they failed to parse the raw
or initially mis-normalized unit and are not used as evidence.

Trusted regeneration therefore pins `solution.py` to `solution.mpy`, and
canonical KAST equality pins `solution.mpy` to the function body actually
executed by the claim.

### Satisfying ground substitutions and body sensitivity

`evidence/claim_ground_witnesses.py` evaluates the formal postcondition
independently and compares it with both Python functions. Empty, vowel,
consonant, example, and all-vowel witnesses agree; see
`evidence/09b-claim-ground-witnesses.log`.

A fresh body mutation changed `.replace("O", "Q")` to
`.replace("O", "R")` in both the executed module term and the retained final
function binding, while preserving the original postcondition. It therefore
changes the actual program rather than an external source file. `kprove`
exited 1 with `WarnStuckClaimState`, exposing the computed
`replaceC(...,79,82)` versus required `replaceC(...,79,81)` equality
(`evidence/spec-body-audit.k`, `evidence/12-body-sensitivity-proof.log`).

## 5. Rule-by-rule static soundness review

`evidence/k_rule_inventory.py` read every K source file in the supplied tree,
plus `verification.k` and `spec.k`. The complete file/line/source inventory is
`evidence/10b-exhaustive-rule-inventory.log`:

- 227 syntax declarations;
- 695 rules: 402 ordinary equations, 35 concrete equations, 20 owise
  equations, 187 ordinary operational rules, 6 owise operational rules, and
  45 priority operational rules;
- 145 function declarations, 107 `total` declarations, 22
  `no-evaluators` opaque declarations, 5 contexts, and one configuration;
- zero `functional` and zero `simplification` declarations;
- one target claim.

`verification.k` has no local syntax, function, totality declaration, opaque
symbol, priority, equation, semantic rewrite, simplification, bridge, or helper
claim. It only imports the supplied `MPY` module. Thus there is no
candidate-added rule capable of encoding the task answer or bypassing program
execution.

### Used syntax and reachable rule families

The program's complete constructor set is:

```text
Attribute, Call, FuncDef, Module, Name, Params, Return, Str
```

The mechanical map is in `evidence/15b-used-construct-rule-map.log`. The
material rules are:

- AST declarations and strictness in `semantics/syntax.k`: `Attribute`
  evaluates its receiver; `Return` evaluates its expression.
- Module load and sequencing: `core.k:124-127`.
- Module-level function binding: `functions.k:14-16`.
- Current-scope name lookup: `core.k:130-154`.
- Callee-first call evaluation and left-to-right argument accumulation:
  `call.k:18-24` and `core.k:183-191`.
- Closure frame creation, parameter binding, return, and exact frame pop:
  `call.k:69-75` and `functions.k:62-90`.
- ASCII literal construction: `str.k:12-17`.
- Bound-method construction and dispatch: `call.k:15-24`.
- `swapcase`, `mapSwap`, and `swapC`: `methods.k:18-21` and
  `methods.k:112-164`.
- Single-character `replace` and `replaceC`: `methods.k:104-109`.

The control/state footprint is complete. A call allocates scope 1, pushes a
frame, binds `message`, executes the nested method calls, sets/clears `ret`,
deletes scope 1, restores environment 0 and scope location 1, and leaves
heap/heap location, exception, and exit code unchanged. The claim constrains
all those cells.

`swapC`'s uppercase and lowercase guards are disjoint, its owise case is their
complement, and its arithmetic is the exact ASCII case offset. `mapSwap`
structurally descends one `iCons` at a time. `replaceC` has disjoint and
exhaustive equality/inequality branches and likewise structurally descends.
The ten replacement literals are all single-character ASCII strings, so the
method rule's domain is exactly met. No guard overlap gives different
right-hand sides; no totalization is used as an unconstrained result.

### Remaining inventoried rules

Every inventory row not in the reachable families above is a fixed supplied
rule whose constructor, callable, operator, receiver type, or method tag does
not occur on this target path. This is the disposition for those rows: fixed
baseline but unreachable and therefore unable to contribute to this claim.
In particular:

- all 22 opaque symbols are float, sort, or MD5 facilities; the mechanical
  search found none in `solution.mpy` or `spec.k`;
- none of the 45 source priority rules can match this execution (cell,
  reference, math/hash, split/sort, assertion, and collection-specific guards
  are absent);
- concrete-only equations and `MPY-CONCRETE` are not part of the Haskell target
  proof path;
- the compiler's non-exhaustive-totality warnings concern unreachable
  constructors and cannot fabricate this string result.

I found no false conclusion witness enabled on the intended input domain, so I
do not label any used rule unsound. Global Python fidelity of unused,
deliberately minimal supplied-semantics facilities is outside this theorem;
that is a narrower evidence boundary, not an unsoundness finding about this
proof.

## 6. Fresh non-vacuity test

The candidate's `spec-vacuity.k` was not used. The reviewer-generated
`evidence/spec-false-audit.k` changes only the final result constraint from:

```text
replaceC(..., 85, 87)
```

to:

```text
replaceC(..., 85, 88)
```

It leaves the executed program, function binding, precondition, and all state
cells unchanged. The mutation is demonstrably false at the satisfying input
`CS = iCons(117, .IntSeq)` (`"u"`): the correct result is `"W"`, while the
mutant requires `"X"` (`evidence/09b-claim-ground-witnesses.log`).

The mutation first built successfully:

```text
kprove spec-false-audit.k --definition verification-kompiled-audit \
  --spec-module SPEC-FALSE-AUDIT --dry-run
EXIT_STATUS: 0
```

See `evidence/13-false-mutation-build.log`. The actual proof then exited 1 with
`WarnStuckClaimState`; its residual is exactly the unmet
`replaceC(...,85,87) #Equals replaceC(...,85,88)` obligation, followed by
“configuration cannot be rewritten further”
(`evidence/14-false-mutation-proof.log`). This is meaningful non-vacuity, not a
parser, import, timeout, or unrelated backend failure.

## 7. Proven-versus-assumed accounting

The successful K reachability claim establishes, for arbitrary modeled
`str(CS)`, that executing the exact submitted function body through ordinary
load, lookup, binding, method-call, return, and frame rules reaches the exact
nested `mapSwap`/ten-`replaceC` result and the stated normal final
configuration. In Kit terminology this is partial correctness; no independent
total-correctness theorem is claimed.

Trust and evidence ledger:

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler and Haskell prover | Checks all symbolic execution and implication steps | Standard proof-checker trust boundary; fresh `#Top`/exit 0 recorded |
| Supplied MPY reference semantics and K builtins | Defines value, binding, control, state, ASCII case, and replacement behavior | Required fixed-semantics boundary; candidate copy is exact and the reachable rules were statically audited |
| 22 supplied opaque float/sort/MD5 symbols | Potentially result-bearing only for unrelated programs | Acceptable here because none is syntactically or dynamically reachable and no claim depends on one |
| Trusted `py2mpy.py`, CPython AST parsing, and source/term bridge | Identifies `solution.py` with the K program | Outside the K theorem; supported by byte-identical regeneration and canonical KAST program comparison |
| English-ASCII intent bridge | Interprets `mapSwap` and the ten `replaceC` folds as the prompt operation | Direct consequence of the exhaustive guarded equations: vowels map two codes forward after case swap, consonants/spaces are not replacement targets, and replacement outputs are consonants |
| Trusted canonical Python plus CPython differential execution | Supports implementation/intent agreement on tested inputs | Finite empirical evidence only; 3,256 independent cases, zero mismatches |

The formal domain is all `IntSeq` string values, so it does not narrow the
prompt's English-letter/space domain. For non-ASCII codes the supplied semantics
does not model CPython Unicode case conversion; that behavior is outside the
prompt's English-alphabet contract. Non-string arguments, external state,
I/O, and concurrency are also outside the formal claim.

Gate A passes: the real body executes without proof-local extensions, all state
is preserved/constrained, the actual-body mutation is rejected, and the false
result is rejected. Gate B passes: the domain covers the source contract and
the postcondition's fixed equations directly implement its transformation.
Gate C passes: all assumptions and finite evidence are named and reproducible.
There is no material adequacy gap or source-domain narrowing.

`evidence/16-evidence-consistency.log` performs a final consistency check over
the positive proof, mutations, differential result, program pinning, and
inventory evidence.

VERDICT: PASS
LEGITIMACY: LEGIT
