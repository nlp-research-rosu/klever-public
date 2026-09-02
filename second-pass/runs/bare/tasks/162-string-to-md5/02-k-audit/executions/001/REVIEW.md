# Independent adversarial audit: 162-string-to-md5

The candidate contains a legitimate, non-vacuous partial-correctness proof of
the submitted generated program under its generated semantics. I reconstructed
all definitions from source, independently closed every positive claim, matched
the proof macros to the trusted regeneration constructor-for-constructor, and
made both a body mutation and a false-result mutation fail for the expected
reason.

I assign `CONCERNS / LEGIT`, not `PASS`, because two bridges are not themselves
proved by the reachability claim:

1. the trusted canonical explicitly uses ASCII while the candidate uses default
   UTF-8, producing four return-versus-exception divergences on valid non-ASCII
   examples; and
2. the theorem's `expectedMd5` is defined using the same generated MD5
   semantics that models `hashlib`, so its RFC/CPython meaning rests on the
   separately audited semantics, imported K hooks, ordinary mathematics, and
   finite differential evidence.

Neither issue substitutes another program, makes the claim vacuous, bounds the
input length, or narrows the material normal-return ASCII domain. The formal
claim ranges over symbolic K strings and the generated UTF-8/RFC equations
soundly cover Unicode scalar strings as well. These are therefore documented
trust/intent limitations rather than a `NOT_LEGIT` defect.

## 1. Input and provenance integrity

I read `/audit-input.json` first. It declares `record_layout: pipeline-v3`,
problem `162-string-to-md5`, condition `bare`, and
`GENERATED_SEMANTICS`. I used only its `container_paths`; the host provenance
paths were not followed.

The independent checker
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py) records its
full run in
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log). It found:

- `/audit-campaign-lock.json` is a real regular file, its SHA-256 is
  `ad5dfcc0…d745`, and its parsed object exactly equals the campaign block in
  `/audit-input.json`.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, `prompt.txt`, and the structured trace
  are present, readable, and nonsymlinked. Every recorded per-file hash
  matches.
- All 350 structured JSONL trace records parse. The generation trace, final
  report, and prose were inspected only as untrusted generation claims.
- The independently computed pipeline-v3 content digest of `/candidate` is
  `ef203d91…134e`, exactly matching both the invocation and generation-result
  workspace digests. The trace content digest is `76e41dad…c1a`, matching
  `usage.json`; its sole trace-file hash also matches the result manifest.
- Candidate `prompt.py` and `py2mpy.py` byte-match the trusted mounted prompt
  and translator. Their hashes are respectively `58845cc4…e38` and
  `406485ea…b16`.
- As required for generated-semantics mode,
  `/reference/reference-semantics` is absent. I did not search for or infer a
  hidden reference semantics.
- The task manifest's common fields match the launcher copy. The launcher adds
  the derived `config` field recorded separately as `manifest_config`; the
  original task-record hash still matches.

There is no infrastructure breach. Source-only candidate artifacts and trusted
references were copied to `/tmp/audit-work/reconstruction`; no candidate
compiled definition, cache, tarball, log, or trace was reused. The copy record
is [scratch-copy.log](/audit-output/evidence/scratch-copy.log).

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt says: given a string `text`, return its MD5 hash-equivalent
string, except return `None` for the empty string. Its example requires
`string_to_md5("Hello world") ==
"3e25960a79dbc69b674cd4ec67a72c62"`.

The trusted canonical implements:

```python
return hashlib.md5(text.encode('ascii')).hexdigest() if text else None
```

Thus it returns `None` for `""`, returns the standard lowercase 32-hex MD5 for
nonempty ASCII strings, and raises `UnicodeEncodeError` for non-ASCII strings.

The candidate implements:

```python
return None if text == "" else hashlib.md5(text.encode()).hexdigest()
```

For `str` inputs, the empty test agrees with truthiness. Default `encode()` is
UTF-8, so all ASCII normal returns agree; ordinary non-ASCII Unicode scalar
strings return a UTF-8 MD5 instead of raising. A lone surrogate still raises
under Python's strict default encoder.

### Trusted regeneration

I regenerated the submitted program using the trusted translator:

```text
python3 trusted_py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both `.mpy` files have SHA-256
`246747f3…af73`; `cmp` exits 0. See
[translation-identity.log](/audit-output/evidence/translation-identity.log).

### Independent differential

[differential.py](/audit-output/evidence/differential.py) imports the trusted
canonical and candidate entry points independently. It exercises the documented
cases; empty/nonempty branch boundary; NUL, whitespace, and ASCII-control
characters; MD5 padding boundaries 55/56/57; block boundaries 63/64/65 and
127/128/129; and 100 deterministic generated ASCII inputs.

Result: 118/123 outcomes match. The five mismatches are the four valid
non-ASCII probes `é`, `π`, `😀`, and `Aπ😀z`, where the canonical raises and
the candidate returns UTF-8 MD5, plus a lone-surrogate probe where both raise
`UnicodeEncodeError` but report different codecs/messages. The command
deliberately exits 1 when any differential mismatch exists; the complete inputs
and outputs are in
[differential.log](/audit-output/evidence/differential.log).

This is a real implementation-versus-canonical distinction. I do not treat it
as material source-domain narrowing: every input on which the canonical
normally returns is covered, the prompt never says ASCII, and the candidate
extends ordinary Unicode-scalar behavior. It remains an intent/encoding concern
because the trusted canonical is the only supplied executable oracle.

## 3. Clean proof reconstruction

The audited toolchain is K `v7.1.293`; exact version output is in
[toolchain.log](/audit-output/evidence/toolchain.log).

### Fresh builds

I built three fresh definitions from copied source:

```text
kompile --backend llvm semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-audit-kompiled

kompile --backend haskell semantic.k --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-haskell-audit-kompiled

kompile --backend haskell verification.k --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

All three builds exit 0; see
[build-concrete.log](/audit-output/evidence/build-concrete.log),
[build-concrete-haskell.log](/audit-output/evidence/build-concrete-haskell.log),
and [build-proof.log](/audit-output/evidence/build-proof.log).

LLVM execution returns 113 for nonempty MD5 computations despite compiling;
that bounded backend evidence is preserved in
[krun-differential-llvm-failure.log](/audit-output/evidence/krun-differential-llvm-failure.log).
This is not used as a candidate verdict: fresh Haskell semantic execution and
direct `kore-exec` provide a functioning concrete path.

### Independent positive claims

The exact CLI label form emitted by this K version is
`SPEC.label(<name>)`. Each target was run independently:

| Claim | Exit | Output evidence |
|---|---:|---|
| `empty` | 0 | `#Top` in [kprove-empty.log](/audit-output/evidence/kprove-empty.log) |
| `nonempty-symbolic` | 0 | `#Top` in [kprove-nonempty-symbolic.log](/audit-output/evidence/kprove-nonempty-symbolic.log) |
| `prompt-example` | 0 | `#Top` in [kprove-prompt-example.log](/audit-output/evidence/kprove-prompt-example.log) |
| `unicode-utf8` | 0 | `#Top` in [kprove-unicode-utf8.log](/audit-output/evidence/kprove-unicode-utf8.log) |
| `multiblock-padding` | 0 | `#Top` in [kprove-multiblock-padding.log](/audit-output/evidence/kprove-multiblock-padding.log) |

The first attempted short label was rejected as an unused label rather than
misreported as a proof; that diagnostic is retained in
[kprove-filter-label-diagnostic.log](/audit-output/evidence/kprove-filter-label-diagnostic.log).

### Concrete generated-semantics execution

Fresh Haskell `krun` agrees with candidate Python for empty, the prompt example,
55/56 padding, 64/65 block boundaries, and the submitted 80-character case.
The full record is
[krun-differential.log](/audit-output/evidence/krun-differential.log).

K's `krun -cTEXT` configuration parser converts code points above U+00FF to
UTF-8 byte-valued K strings before the candidate's explicit UTF-8 semantics
runs, causing double encoding. I isolated that front-end issue by constructing
full KORE configurations containing genuine `\u03c0`, `\u20ac`, and
`\U0001f600` string domain values and invoking the rebuilt Haskell
`kore-exec` directly. The K results exactly match Python:

- `π` → `31bf0b12546409e15021243132fc7574`
- `€` → `bca53fde466a76b7bee3e18997e94a7a`
- `😀` → `2a02eac39d716a70ecf37579185927b6`

Commands, inputs, and outputs are in
[kore-exec-pi-direct.log](/audit-output/evidence/kore-exec-pi-direct.log),
[kore-exec-unicode-boundaries.log](/audit-output/evidence/kore-exec-unicode-boundaries.log),
and the three `*-full-config.kore` evidence files. This establishes that the
generated semantic rules, rather than the `krun` config parser, have the
intended Unicode-scalar behavior.

## 4. Adequacy and real-program pinning

### Plain-language claim meanings

| Claim | Initial domain | Required normal result |
|---|---|---|
| `empty` | exactly `text = ""` | `None` |
| `nonempty-symbolic` | every K string `S` with `S != ""` | `expectedMd5(S)`, defined as `pyString(md5String(S))` |
| `prompt-example` | exactly `"Hello world"` | prompt's 32-hex digest |
| `unicode-utf8` | exactly internal Unicode string `"π"` | MD5 of its UTF-8 bytes |
| `multiblock-padding` | exactly 80 ASCII `a` characters | `b15af9c…0f98` |

Every precondition is satisfiable. Witnesses are respectively `""`, `"a"`,
`"Hello world"`, `"π"`, and `"a"*80`. Substitution gives:

- `""`: candidate and canonical return `None`, and fresh K execution gives
  `pyNone`.
- `"Hello world"`: both Python functions and K give `3e25960a…2c62`.
- `"π"`: candidate Python and direct KORE execution give `31bf0b12…7574`;
  canonical raises because of its explicit ASCII choice.
- `"a"*80`: both Python functions and K give `b15af9cd…0f98`.

### Program identity

The claims execute `#load(solutionProgram)`, not an oracle or a substituted
summary invocation. `solutionProgram` expands to the exact import/function
binding, and `solutionBody` expands to the actual returned conditional and
nested encode/MD5/hexdigest calls.

[program_term_check.py](/audit-output/evidence/program_term_check.py)
extracts both function-rule right-hand sides, expands `solutionBody`, removes
only the explicit list unit `.Stmts`, and compares constructor tokens with the
trusted-regenerated `solution.mpy`. Both terms contain 78 constructor tokens
and are identical; see
[program-term-check.log](/audit-output/evidence/program-term-check.log).

The operational semantics then executes every material constructor:
module/import/function loading, invocation/binding, return, conditional,
string comparison, names, attributes, zero/one-argument calls, UTF-8 encoding,
MD5, and hex formatting.

### Body sensitivity

I changed the program term actually executed by a separate claim:
`solutionBodyMutant => Return(NoneVal) .Stmts`. The mutant definition builds
successfully, but the original prompt postcondition gets stuck with
`<result> pyNone </result>` and exits 1. Sources and logs:

- [verification-body-mutant.k](/audit-output/evidence/verification-body-mutant.k)
- [spec-body-mutant.k](/audit-output/evidence/spec-body-mutant.k)
- [build-body-mutant.log](/audit-output/evidence/build-body-mutant.log)
- [kprove-body-mutant.log](/audit-output/evidence/kprove-body-mutant.log)

This demonstrates real body dependence rather than dependence on an unchanged
external source file.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[RULE-INVENTORY.md](/audit-output/evidence/RULE-INVENTORY.md); raw declaration
locations are in
[declaration-lines.log](/audit-output/evidence/declaration-lines.log).
It accounts for all 154 `semantic.k` rules, all three `verification.k` rules,
all local syntax/function declarations and attributes, the configuration, and
all five claims.

There are no local `[total]`, `[functional]`, opaque, `owise`, priority, or
trusted declarations. The only simplifications are the empty/recursive UTF-8
equations and concrete MD5 evaluation. All guarded rule families are disjoint
on their reached domains:

- empty/nonempty string recursion;
- four UTF-8 numeric ranges;
- block stop/step;
- round base/step;
- 16 nibble constants;
- four Boolean/index round ranges;
- 16 shift range/residue cases; and
- 64 ground MD5 constants.

### Construct coverage and control/state review

| Submitted construct | Declarations/rules |
|---|---|
| module, import, function definition | `semantic.k:5–12`, `64–69` |
| function invocation/parameter binding | `40–44`, `72–77` |
| return/control completion | `79–83` |
| `None`, string, names | `14–16`, `87–91` |
| string `==` | `17`, `23`, `93–98` |
| conditional expression | `18`, `100–103` |
| attribute selection | `19`, `105–112` |
| zero/one-argument calls | `20–21`, `114–127` |
| default UTF-8 encode | `117–118`, `157–181` |
| `hashlib.md5(...).hexdigest()` | `107–120`, `182–365` |

Evaluation order is receiver/function first, then argument; comparison is left
then right; the conditional evaluates only its selected branch. Invocation
looks up the exact stored function and binds `text`; return consumes the
function continuation and writes only `<result>`. No allocation, heap, output,
or mutable MD5 object is observable in this submitted program, so representing
the one-use MD5 object by its byte payload preserves the exact state footprint.

Special-casing `Name("hashlib")` could overlap generic lookup if a local
`hashlib` binding existed, and representing raw bytes and the modeled MD5
object with the same `pyBytes` tag would accept other invalid Python programs.
Neither false behavior can be enabled by this submitted constructor tree for
any text input: invocation resets the only local binding to `text`, and the
outer `hexdigest` receiver is always the result of the intervening `md5` call.
Under the generated-semantics rule that minimal exact-program coverage is
acceptable, these are reuse limitations, not witnessed unsoundness on the
intended domain.

### UTF-8 and MD5 mathematics

[utf8_formula_check.py](/audit-output/evidence/utf8_formula_check.py)
exhaustively checks all 1,112,064 Unicode scalar values against Python UTF-8;
there are zero mismatches. The rule's numeric guard also assigns three bytes to
the 2,048 surrogate code points, while Python strict UTF-8 raises. The Haskell
backend itself rejects a surrogate K string literal, as
[kprove-surrogate-witness.log](/audit-output/evidence/kprove-surrogate-witness.log)
shows. Thus the formal K-string domain is Unicode scalar text and omits
Python's representable lone-surrogate strings. This is a narrow
language-model/domain caveat, not a false reachable conclusion for a valid K
string; it does not materially narrow the prompt/canonical normal-return domain.

[md5_table_check.py](/audit-output/evidence/md5_table_check.py) independently:

- recomputes every one of the 64 constants as
  `floor(2^32 * abs(sin(i+1)))`;
- derives all 64 shift entries from the 16 guarded rules; and
- implements the RFC rounds independently and compares them with `hashlib` on
  empty, prompt, padding/block boundaries, all byte values, and a 1,024-byte
  generated vector.

Every comparison matches; see
[md5-table-check.log](/audit-output/evidence/md5-table-check.log). Static
inspection additionally confirms padding to 56 modulo 64, low-64-bit
little-endian length encoding (K's fixed-width `Int2Bytes` truncates excess
high bits), little-endian word loads/output, modulo-2^32 addition, round state
permutation, feed-forward, and lowercase hexadecimal formatting.

### Proof-local extensions

- `solutionBody` and `solutionProgram` are definitional macros, not operational
  shortcuts; their constructor identity is mechanically checked.
- `expectedMd5(S) => pyString(md5String(S))` is a definitional postcondition
  summary. It does not skip the body: the body executes through `#eval`.
- The semantics' encode/hashlib rules are models of fixed external primitives.
  The same `md5Bytes` value influences execution and the final summary, so the
  reachability proof alone does not establish that this name has RFC/CPython
  meaning. It is not an unconstrained oracle, however: every ground bytes value
  reduces through the complete padding/block/round/hex equations audited above.

No inventoried local rule supplies an arbitrary result, assumes the task
answer, erases a material state effect, or admits a witnessed false conclusion
on the material input domain.

## 6. Fresh non-vacuity test

The candidate supplied no relied-upon vacuity test. I created
[spec-vacuity-audit.k](/audit-output/evidence/spec-vacuity-audit.k), changing
only the last prompt-example digest digit from the true `…c62` to false
`…c63`.

The satisfying witness is `"Hello world"`. A `--dry-run` compiles the mutation
successfully and exits 0
([kprove-vacuity-dry-run.log](/audit-output/evidence/kprove-vacuity-dry-run.log)).
The real proof exits 1 with `WarnStuckClaimState`; its residual is fully
executed `.K` and the actual `…c62` result, which fails to unify with the
mutated destination. See
[kprove-vacuity.log](/audit-output/evidence/kprove-vacuity.log).

This is the expected unmet result obligation, not a parser error, missing
import, timeout, unrelated crash, or unreachable mutation. Non-vacuity passes.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the reconstructed generated semantics and imported K hooks:

- loading and invoking the exact submitted module with `text = ""` consumes
  the computation and returns `pyNone`;
- for every nonempty K string `S`, loading and invoking the exact submitted
  module consumes the computation and returns
  `pyString(md5String(S))`;
- the three ground refinements produce the prompt, Unicode-π, and 80-byte
  results stated in `spec.k`.

This is partial correctness. It does not prove termination of arbitrary large
inputs, but every proved terminating outcome is result-constrained.

### Trust and limitation ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| K `v7.1.293` compiler, Haskell prover/runtime, and reachability logic | all claims | Trusted toolchain. Fresh builds/runs avoid candidate caches. |
| Built-in `String`, `Bytes`, `Int`, `Bool`, and `Map` hooks | all operational and MD5 equations | Low-level semantic trust boundary. Relevant byte-width behavior is documented by the installed K definition; representative executions pass. |
| Trusted `py2mpy.py` transliteration | program identity | Byte regeneration plus constructor comparison establish this immutable artifact link. |
| Generated rules for module loading, binding, evaluation order, return, and attributes/calls | program execution | Statically audited against every used constructor; body mutation confirms sensitivity. |
| `str.encode()` as UTF-8 over K Unicode scalar strings | every nonempty result | Equations exhaustively match Python scalars. Lone-surrogate Python strings are outside executable K-string/backend scope. |
| `hashlib.md5` / RFC 1321 meaning of `md5Bytes` | every nonempty result and `expectedMd5` | External primitive/model boundary. Equations are complete on ground bytes and statically audited; constants/shifts and finite independent differentials pass. There is no separate machine-checked universal connection theorem to CPython. |
| ASCII canonical versus candidate default UTF-8 | implementation-to-oracle intent | All canonical normal-return ASCII cases agree; valid non-ASCII behavior differs. Prompt does not select an encoding, so this remains explicit rather than silently resolved. |
| `krun -cTEXT` Unicode configuration parsing | concrete test harness only | It double-encodes code points above U+00FF. Direct proper-KORE `kore-exec` tests isolate and pass the semantic behavior, so the faulty front end is not used to validate those cases. |
| Imported module availability and absence of resource/implementation failures | exceptions and termination | Standard `hashlib` availability is assumed. Exceptional resource behavior and termination are outside partial correctness. |

Differential testing, table checks, and traces are supporting evidence only.
They are not substitutes for the five reconstructed K proofs. Conversely, the
K proof establishes equality to its semantic MD5 model; the external RFC/CPython
interpretation is precisely the audited boundary above.

### Gate and decision summary

- Real-program soundness: **PASS**. Exact program term, body execution,
  preserved control/state on the reached path, satisfiable claims, and two
  discriminating mutations.
- Intent adequacy: **PASS with concern**. Full empty/nonempty symbolic K-string
  domain and unbounded lengths are covered; no finite-size restriction exists.
  Canonical ASCII versus candidate UTF-8 is an encoding-intent discrepancy, not
  a narrowed normal-return domain.
- Trust/evidence auditability: **PASS with concern**. Every artifact, command,
  exit status, bounded output, test scope, and oracle is preserved, but the
  generated MD5-to-CPython bridge is audited rather than machine-proved as a
  separate connection theorem.

All reviewer-authored evidence is content-hashed in
[SHA256SUMS](/audit-output/evidence/SHA256SUMS).

VERDICT: CONCERNS
LEGITIMACY: LEGIT
