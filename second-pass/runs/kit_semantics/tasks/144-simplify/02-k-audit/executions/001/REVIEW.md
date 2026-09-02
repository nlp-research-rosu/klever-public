# Independent adversarial review: 144-simplify

The candidate contains a legitimate partial-correctness proof of the submitted
program over the material HumanEval domain. I rebuilt every definition from
source, independently reproved the mutually recursive loop invariant family and
the entry claim, checked constructor-level program identity, audited every
proof-local rule, and rejected fresh body/result mutations.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected problem/condition
`144-simplify` / `kit-semantics`.

I read and checked all required pipeline-v3 records:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`; and
- all 762 JSONL records in the structured trace. The bounded trace/log index is
  `/audit-output/evidence/stage1-generation-record-index.log`. These generation
  records were used only as untrusted claims.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, and the lock SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
the value recorded by the launcher.

All launcher-declared direct file hashes match independently computed hashes,
including the canonical, prompt, translator, manifests, metrics, prompt,
Codex log, and last message. Every evidence-file hash listed in
`/generation-result.json`, including the structured trace file, also matches.
See `/audit-output/evidence/stage1-integrity.log` and the reviewer script
`/audit-output/evidence/check_manifest.py`.

All launcher provenance mounts and all pipeline-v3 required records are
present, readable, of the expected regular-file/directory type, and not
symlinks. The six required proof artifacts in `/candidate` are regular files.
An independent type/path/content digest read the complete candidate and trace
trees; it found 788 candidate files and no symlink or special entry. See
`/audit-output/evidence/stage1-independent-tree-hashes.log`.

The supplied-semantics boundary is intact:

- `/reference/reference-semantics` is present as required by the rendered mode;
- recursive, no-dereference comparison of the candidate and trusted semantics
  trees reports no missing, additional, changed, mistyped, or symlinked entry;
- both trees contain one directory and 24 regular files, have the same
  reviewer-defined tree digest
  `406d05d92bf35ae18f11c2e062b1f99f760ed1c85830c50aff7b2d21d6c47352`;
  and
- candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.

There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

The source contract says that `x` and `n` each represent a positive fraction
as `<numerator>/<denominator>`. `simplify(x, n)` must return `True` exactly
when

```text
(numerator(x) * numerator(n)) /
(denominator(x) * denominator(n))
```

is a whole number. On positive denominators this is equivalent to divisibility
of the numerator product by the denominator product.

The submitted `solution.py` performs a single Horner scan over
`x + "/" + n`, parses the four positive decimal fields into `a,b,c,d`, and
returns `(a*c) % (b*d) == 0`. It is a different algorithm from the canonical
but directly implements the stated exact-arithmetic property.

Trusted regeneration used:

```bash
python3 py2mpy.py solution.py
cmp -s regenerated-solution.mpy solution.mpy
```

Both commands exited 0. Submitted and regenerated constructor programs are
byte-identical with SHA-256
`fbfd1a3ce78959e88eb3e7b636324161981547eb8dd9e79dcf304aac56a3f359`.
The regenerated artifact and command record are
`/audit-output/evidence/regenerated-solution.mpy` and
`/audit-output/evidence/stage2-program-fidelity.log`.

The independent differential script
`/audit-output/evidence/independent_differential.py` imports both the trusted
canonical and generated entry points. It covers the three prompt examples,
one-digit and leading-zero boundaries, every parser phase, true/false return
branches, a binary64 precision boundary, very large integers, a Cartesian
sample, 5,000 seeded 50-digit cases, and malformed/empty diagnostics.

Results over 9,106 valid cases:

```text
generated_contract_mismatches=0
canonical_contract_mismatches=3
generated_canonical_divergences=3
```

The three divergences are attributable to the canonical's use of binary-float
division, not to the generated program:

1. `9007199254740993/9007199254740992 * 1/1` is non-integral. The canonical
   rounds the quotient to `1.0` and returns `True`; the generated program and
   exact contract return `False`.
2. Two 401-digit valid cases raise `OverflowError` in the canonical's `/`
   conversion; the generated exact-integer program returns the mathematically
   specified Boolean.

The prompt gives no magnitude bound. I therefore judge the generated program,
which agrees with the natural-language contract, as correct on these intended
inputs; the divergences expose limitations of the canonical implementation,
not a substituted program. Invalid-input differences are outside the prompt's
precondition and are recorded without being used as proof evidence.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/144-simplify`. No
candidate-supplied kompiled directory or cache was copied or used. The live K
toolchain reports K v7.1.293.

Fresh Haskell definitions were built with:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION-BASE \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-base-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Both exited 0. Logs:

- `/audit-output/evidence/stage3-kompile-base.log`
- `/audit-output/evidence/stage3-kompile-full.log`

The seven loop claims form one mutually recursive circularity family: digit
claims transition to slash claims and vice versa. Selecting a single label
removes sibling circularities and causes symbolic tail unrolling; I terminated
that diagnostic. The correct independent command includes and proves every
claim in `LOOP-SPEC` together:

```bash
kprove loop-spec.k \
  --definition audit-verification-base-kompiled \
  --spec-module LOOP-SPEC
```

It printed `#Top` and exited 0. This definition imports
`VERIFICATION-BASE`, which contains no operational bridge. Log:
`/audit-output/evidence/stage3-kprove-loop-all.log`.

The positive entry proof was independently run with:

```bash
kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0. Log:
`/audit-output/evidence/stage3-kprove-target.log`.

I also rebuilt the concrete definition from the trusted semantics:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
krun reviewer-concrete.mpy --definition audit-runtime-kompiled
```

The build exited 0. The execution completed at `.K` with `NoExc` and exit code
0 for six assertions covering the prompt examples, boundaries, leading zeroes,
and the binary64 rounding case. See
`/audit-output/evidence/stage3-kompile-concrete.log`,
`/audit-output/evidence/reviewer_concrete.py`, and
`/audit-output/evidence/stage3-krun-concrete.log`.

Thus both clean dynamic gates close; no candidate cache or prior `#Top` is
needed.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

The claim invokes a closure with parameters exactly `("x","n")`, body
`simplifyBody`, and defining scope 0. Its arguments are two nonempty symbolic
strings. The initial module/builtin scopes, environment, allocation counters,
heap, stack, return state, and exception state match a direct call from module
scope.

The precondition says:

- the first code of `x` is an ASCII digit; and
- scanning the rest of `x`, an inserted slash, and all of `n` accepts exactly
  three slash transitions, accepts only ASCII digits otherwise, and finishes
  with four strictly positive Horner accumulators.

This includes every finite source-contract fraction pair, without a length or
numeric bound and with leading zeroes. It also admits some out-of-contract
splits whose *combined* stream has the same four-field grammar; that is a
sound superset and does not exclude any intended input.

The postcondition is the deterministic `scanResult` fold of the exact combined
input codes. On an accepted stream it accumulates `A,B,C,D` and reduces to:

```k
pyMod(A *Int C, B *Int D) ==Int 0
```

Because accepted `B` and `D` are positive, this is exactly the requested
whole-number property. The returned Boolean is therefore constrained; it is
neither free nor a tautological implication.

### Mechanical program identity

The reviewer script `/audit-output/evidence/check_program_pinning.py` uses the
trusted translator, independently extracts and expands the three proof aliases,
and compares constructor tokens while normalizing only explicit associative
`.Stmts`/`.Exprs` units. It reports:

```text
stored_module_byte_identity=True
proof_body_constructor_identity=True
entry_claim_exact_params_body_scope=True
```

The submitted module contains one `simplify(x,n)` binding, and the claim's
direct closure has exactly that parameter list, body, and defining scope.
Direct closure construction is semantically the function binding/body allowed
by the benchmark's constructor-level pinning rule; it does not substitute a
summary for the body.

### Satisfying states and concrete substitutions

For `x="1/5"` and `n="5/1"`, choose:

```text
XHEAD=49, XTAIL=[47,53], NHEAD=53, NTAIL=[47,49].
```

The formal `validScan` precondition reduces to `true`; `scanResult` reduces to
`true`; both Python implementations return `True`.

For `x="1/6"` and `n="2/1"`, the accepted accumulators are
`A=1,B=6,C=2,D=1`; `scanResult` reduces to `false`; both Python
implementations return `False`.

Ground K claims for the true precondition and both result values print `#Top`
in `/audit-output/evidence/stage4-ground-k-results.log`. The frontend labels
these ground function reductions trivial; the separate dynamic entry proof and
stage-6 false mutation establish that this is not theorem vacuity.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`/audit-output/evidence/build_rule_inventory.py` reads every K source file and
emits source location, module, kind, attributes, normalized text, and a block
hash for every declaration, configuration, context, rule, and positive claim.
The exhaustive result is
`/audit-output/evidence/static-rule-inventory.txt`.

Inventory totals:

| Provenance | Inventory |
|---|---:|
| Trusted supplied semantics | 695 rules, 227 syntax declarations, 5 contexts, 1 configuration |
| Proof-local | 19 equational rules, 2 priority operational rules, 4 function-declaration blocks, 8 positive claims |
| Total | 961 records |

The 695 supplied rules are the fixed semantics selected by
`SUPPLIED_SEMANTICS`; recursive integrity comparison establishes that the
candidate neither altered nor supplemented that baseline. They are marked
`trusted-fixed` individually in the inventory. The 22 fixed
`no-evaluators` symbols are:

```text
md5hexCodes, intFloatDiv, divII, floatMod, floatLt, absF, subF,
divF, addF, mulF, powF, gtF, eqF, decStrToF, divFloatIntV,
intToF, truncF, roundF, roundFN, sqrtF, sortVS, sortKeyVS
```

None is reachable from this integer/string/loop program or its proof.

The used constructor-to-semantics map is:

| Program construct | Declaration and material fixed rules |
|---|---|
| `Module`, `FuncDef`, `Params` | `syntax.k`; `core.k` `#loadAll`; `functions.k` closure binding |
| direct closure call | `core.k` argument evaluation; `call.k` closure frame creation; `functions.k` parameter binding/pop |
| `Assign`, `Name`, `Int`, `Str` | `syntax.k`; `controls.k` assignment; `core.k` lookup/literals; `str.k` literal codes |
| `For` over concatenated strings | `controls.k` `For/#loop/#loopStep`; `str.k` `seqConcat` and string iterator |
| nested `If` | strict syntax and `controls.k` `#branch` rules |
| `BinOp` `+,-,*,%` | evaluation order in `syntax.k`/`operators.k`; integer equations in `int.k`; string `+` in `str.k` |
| comparisons `==` | `operators.k`; string equation in `str.k`; integer equation in `int.k` |
| `ord(ch)` | name/builtin call routing in `core.k`/`call.k`; one-character rule in `builtins.k` |
| `Return` | strict evaluation and exact frame unwind in `functions.k` |

This covers every constructor in `solution.mpy`; there is no unmodeled used
operation and no used opaque result.

### Every proof-local declaration and rule

The following accounts for all 21 proof-local rules:

| Rules | Count | Decision |
|---|---:|---|
| `simplifyLoopBody`, `simplifyReturn`, `simplifyBody` | 3 | Exact constructor aliases. Mechanical expansion equals the trusted translation. They name terms and do not bypass execution. |
| `simplifyScope` | 1 | One exhaustive equation for its declared argument sorts; the eight bindings and parent scope exactly match fixed call/assignment execution. |
| `validScan(.IntSeq, phase)` for phases 0,1,2 | 3 | Correctly reject incomplete streams. Guards/patterns are disjoint. |
| `validScan(.IntSeq,3,A,B,C,D)` | 1 | Correctly accepts iff all four source-contract values are positive. |
| `validScan(iCons(...),phase)` for phases 0,1,2,3 | 4 | Slash and digit cases use disjoint codes; digit updates are the exact Horner steps; recursion strictly shortens `IntSeq`. |
| `validScan` `owise` | 1 | Makes the declared function total by rejecting all remaining phase/shape cases; it cannot overlap an applicable specific rule. |
| `scanResult` positive phase-3 base | 1 | Denominator product is nonzero under its positive guard; `pyMod(A*C,B*D)==0` is the exact result. |
| `scanResult` slash transition | 1 | Guard restricts phase to 0,1,2 and advances exactly one field. |
| `scanResult` digit transitions for phases 0,1,2,3 | 4 | Pairwise phase-disjoint, slash-disjoint through `isDigitC`, and strictly decreasing. They cover every `validScan`-true nonempty state. |
| `loop-digit-bridge` | 1 | Sound operational bridge; exact connection and state analysis below. |
| `loop-slash-bridge` | 1 | Sound operational bridge; exact connection and state analysis below. |

There are no proof-local opaque, `[simplification]`, `[functional]`, or
unconstrained total symbols. `scanResult` is intentionally not declared total;
all of its uses are guarded by `validScan`.

### Operational bridges

Both bridge rules are result-bearing and preempt fixed loop execution at
priority 40, so they require the strongest check. They pass it:

- **Complete context.** Each rule matches the entire `<k>` continuation:
  the exact `#loop`, exact remaining `simplifyReturn .Stmts`, and exact
  `#endcall`, with nothing after it. It matches environment 1, exactly the
  module/callee/builtin scope map, scope location 2, empty heap, heap location
  0, exactly one `frame(.K,0,1)`, `noRet`, and `NoExc`. The only omitted
  configuration cell is `exit-code`, which is framed and unchanged.
- **Binding and body.** Equality guards fix the loop body, return statement,
  all eight local bindings, parent scope, and builtin scope. `XARG`, `NARG`,
  and the old `ch` may be arbitrary because fixed execution no longer reads
  them after this loop head; the connection claims quantify over the same
  values.
- **Domain partition.** The digit bridge requires phase 0..3, a digit head,
  and `validScan`; the slash bridge requires phase 0..2, code 47, and
  `validScan`. Code 47 is not a digit. Expanding the relevant `validScan`
  equation yields exactly the corresponding one-step precondition in one of
  the four digit or three slash connection claims.
- **State/control footprint.** The bridge and connection claims agree on the
  Boolean result, callee-scope removal, environment restore, scope-location
  restore, frame pop, stack, heap, heap counter, return state, exception state,
  module/builtin scopes, and continuation.
- **Universal connection.** `LOOP-SPEC` imports `VERIFICATION-BASE`, not
  `VERIFICATION`. Its seven mutually recursive claims therefore execute only
  fixed semantics and the truthful helper equations. Their fresh aggregate
  proof is `#Top`.

No opposite interpretation of `scanResult` is admitted: its exhaustive
valid-domain equations fix every result, and the bridge-free connection claims
reach that same term.

### Operational body sensitivity

I copied `verification.k` to
`/audit-output/evidence/verification-body-mutated.k` and changed the `For`
body actually used by `simplifyBody` from `simplifyLoopBody` to `.Stmts`.
The mutated definition compiled successfully. A ground call on the satisfying
input `"1/5","5/1"` then failed with `WarnStuckClaimState` at:

```text
applyBin("%", 0, 0)
```

and `kprove` exit 1. Thus changing the executed body changes/invalidates the
claimed computation; merely editing an external unused file was not the test.
Artifacts and logs:

- `/audit-output/evidence/body-sensitivity-spec.k`
- `/audit-output/evidence/stage5-body-sensitivity-kompile.log`
- `/audit-output/evidence/stage5-body-sensitivity-kprove.log`

I found no unsound proof-local rule, so there is no false-conclusion witness to
report against one. The positive and mutation witnesses instead support the
sound decisions above.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation is
`/audit-output/evidence/fresh-false-result-spec.k`.

Its input `"1/6","2/1"` satisfies the source and entry preconditions and
returns `False` in both Python implementations. The mutation changes the
result obligation to `true`.

Build/parse check:

```bash
kprove fresh-false-result-spec.k \
  --definition audit-verification-kompiled \
  --spec-module FRESH-FALSE-RESULT-SPEC \
  --dry-run
```

Exit: 0. Log:
`/audit-output/evidence/stage6-false-mutation-build.log`.

Proof attempt:

```bash
kprove fresh-false-result-spec.k \
  --definition audit-verification-kompiled \
  --spec-module FRESH-FALSE-RESULT-SPEC
```

Exit: 1, with `WarnStuckClaimState`. The residual is the expected unmet
obligation:

```text
<k> false ~> .K </k>
```

This is a reachable semantic failure, not a parse error, timeout, missing
import, or unrelated crash. Log:
`/audit-output/evidence/stage6-false-mutation-kprove.log`.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied semantics, for every finite pair of nonempty code sequences
satisfying the entry `validScan` precondition, invoking the exact submitted
`simplify(x,n)` closure reaches the Boolean obtained by parsing the four
positive decimal fields and testing:

```text
(A*C) mod (B*D) == 0
```

Per the Kit contract this is reported as partial correctness: when execution
terminates from a satisfying state, the returned result is the stated Boolean.
The formal domain is symbolic and unbounded; it is not a finite unrolling or
collection of examples.

### Trust ledger

| Boundary | Dependents and judgment |
|---|---|
| Exact supplied semantics tree | Defines Python-subset evaluation, cells, calls, iteration, control, strings, `ord`, integer arithmetic, and `pyMod`. It is the selected fixed trust boundary in supplied-semantics mode, independently integrity-checked. Acceptable. |
| K v7.1.293 parser/compiler, Haskell reachability backend, SMT reasoning | All machine-checked conclusions depend on these tools. Normal unavoidable proof-tool trust. Acceptable. |
| LLVM backend | Used only for concrete supporting execution, not for universal proof closure. Acceptable finite evidence. |
| Trusted `py2mpy.py` translator | Used to regenerate the constructor program. Byte identity and an independent proof-body token comparison reduce the bridge to exact syntactic transliteration. Acceptable. |
| K builtin mathematical domains | Relevant primitives are unbounded integers, Boolean connectives, maps/lists, strings/codes, equality, arithmetic, remainder, and comparisons. The positive denominator guard keeps remainder defined. Acceptable ordinary mathematical/tool trust. |
| Fixed opaque symbols | All 22 are listed in stage 5. None influences this program, control flow, state, bridge, or postcondition. Inert here. |
| Proof-local symbols | No opaque value. All are exhaustively equational on their use domains or connected to fixed execution by the bridge-free loop proof. Formally justified. |
| Natural-language grammar bridge | Interprets the documented fraction format as finite ASCII decimal digit strings with `/`, matching examples and the supplied semantics' string model. This covers the material HumanEval domain; Unicode numeral spellings and invalid fractions are excluded. Acceptable. |
| Divisibility interpretation | For positive `B,D`, `pyMod(A*C,B*D)==0` iff the product is a whole number. Ordinary exact arithmetic; no empirical oracle is substituted. Acceptable. |
| Reviewer differential and concrete tests | 9,106 Python cases and six LLVM assertions support implementation/model alignment only. They are not treated as universal proof or as a replacement for the connection theorem. |
| Trusted canonical | Used as required differential evidence. Its binary-float rounding/overflow behavior diverges from the unbounded natural contract in three exhibited cases; it is not assumed as an exact-arithmetic theorem oracle there. |

There is no program-derived oracle, unproved operational shortcut, free result,
or materially narrowed input-size domain.

### Gate decisions

- Gate A — real-program soundness: **PASS**.
- Gate B — intent adequacy: **PASS** for arbitrary finite valid positive ASCII
  fraction strings; no fixed length or value bound.
- Gate C — trust/evidence auditability: **PASS**. Commands, statuses, scripts,
  mutations, inventories, and bounded logs are preserved under
  `/audit-output/evidence/`.

The canonical float limitations are documented but do not make the candidate's
exact-arithmetic implementation or theorem illegitimate. The proof is
result-constraining, pins the real generated body, and has no material adequacy
gap.

VERDICT: PASS
LEGITIMACY: LEGIT
