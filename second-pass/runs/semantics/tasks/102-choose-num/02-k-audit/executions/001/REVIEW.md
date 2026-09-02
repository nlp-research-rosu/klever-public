# Independent adversarial audit: 102-choose-num

## Audit outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof for positive integer inputs under the supplied MPY semantics. Fresh
reconstruction proved every submitted claim, the proof wrapper contains the
exact submitted translated function body, and both a false-result mutation and
an independent body mutation were rejected at the expected result equality.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, because four
requested provenance artifacts are missing, the source-file-to-embedded-K link
is an audited current-artifact equality rather than a build-time dependency,
and the interpretation of the closed formula as “the biggest even integer” is
an elementary but informal intent bridge. None of these limitations enables a
false program result to be proved.

The complete evidence index is
[`evidence/README.md`](evidence/README.md). All builds and mutations were made
under `/tmp/audit-work/102-choose-num`; no candidate-built definition or cache
was copied or reused.

## 1. Input and provenance integrity

### Infrastructure and semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and the trusted
`/reference/reference-semantics` mount is present. There is therefore no
mode/mount contradiction and no infrastructure breach.

The candidate semantics tree has 24 ordinary files in two ordinary
directories. It has no symlinks. A recursive, no-dereference comparison against
the trusted tree exited 0 with no output:

```text
diff --no-dereference -r /candidate/reference-semantics /reference/reference-semantics
[exit 0]
```

Thus there are no missing, additional, changed, mistyped, or symlinked entries
inside the candidate's required `reference-semantics/` tree. This integrity
result does not bless the candidate's separate proof rules in
`verification.k`. Exact commands, entry types, and hashes are in
[`evidence/01_provenance.log`](evidence/01_provenance.log).

### Prompt and translator

The candidate prompt and translator are byte-identical to their trusted
versions:

```text
prompt.py:
3b2e226ef819e4547fbd11a4ee933844a256dcd27e6d79fc1da3d380ff755d18

py2mpy.py:
406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16
```

Both `cmp -s` commands exited 0.

### Missing and extra provenance material

The following requested candidate artifacts are absent; each `stat` probe
exited 1 with `No such file or directory`:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`

No file whose name suggests a structured generation trace (`*trace*`,
`*generation*.json`, or `*.jsonl`) is present. A structured trace is optional
when none exists, but the four named provenance artifacts are a real evidence
gap. The candidate also contains `concrete_tests.py`,
`concrete_tests.mpy`, `prove.sh`, and a `__pycache__` directory. These are
ordinary untrusted support/derived artifacts, not additions to the protected
semantics tree, and none was relied upon.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

On the intended positive-integer domain, the trusted prompt and canonical
implementation require:

> Given positive integers `x` and `y`, return the greatest even integer `z`
> satisfying `x <= z <= y`; return `-1` if no such integer exists.

The documented examples are `choose_num(12, 15) == 14` and
`choose_num(13, 12) == -1`.

The generated implementation has four effective cases:

1. `y` even and `y >= x`: return `y`;
2. `y` even and `y < x`: return `-1`;
3. `y` odd and `y - 1 >= x`: return `y - 1`;
4. otherwise: return `-1`.

These cases agree with the canonical implementation over positive integers.
For an odd upper bound, `y - 1` is its greatest even predecessor; for an even
upper bound, `y` itself is maximal.

### Trusted translation

The submitted `solution.py` was regenerated using the trusted translator:

```text
cd /tmp/audit-work/102-choose-num &&
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
[exit 0]

cmp -s regenerated-solution.mpy solution.mpy
[exit 0]
```

Both files have SHA-256
`e7231ffdf1d33721d51d14b7c16622606d9fadb9168a7ec34c4fbd8e838af226`.
The byte-identity evidence is in
[`evidence/02_program_fidelity.log`](evidence/02_program_fidelity.log).

### Independent differential testing

[`evidence/differential_test.py`](evidence/differential_test.py) independently
imports the trusted canonical entry point and the generated entry point. It
also uses the mathematical greatest-even formula, with direct enumeration as
an additional oracle on bounded intervals. Its scope was:

- 13 documented and branch-boundary cases, including the minimum positive
  endpoint, singleton ranges, reversed/empty ranges, and both sides of every
  comparison boundary;
- every `(x, y)` in `[1, 200] x [1, 200]`;
- 5,000 deterministic random pairs in `[1, 10^12]`, seed 102;
- 20,109 bounded cases additionally checked by explicit enumeration.

The command exited 0 after 45,013 total cases with `mismatch_count=0`.
This is finite adequacy evidence, not a replacement for the K proof.

## 3. Clean proof reconstruction

### Fresh concrete definition

K v7.1.337 was available independently. A fresh LLVM definition was built from
the scratch-copied, integrity-checked supplied semantics:

```text
kompile /tmp/audit-work/102-choose-num/reference-semantics/semantics.k \
  --backend llvm --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/102-choose-num/runtime-kompiled
[exit 0]
```

The reviewer-authored
[`evidence/concrete_audit.py`](evidence/concrete_audit.py) was translated with
the trusted translator. It asserts ten normal and boundary results. `krun`
consumed every assertion, ended with `.K`, `NoExc`, and exit code 0, and the
process exited 0. The complete bounded transcript is
[`evidence/03_concrete_rebuild.log`](evidence/03_concrete_rebuild.log).

The LLVM compiler warned about globally non-exhaustive total functions such as
`mapStrVS`, `floorFI`, and `valSeqAt`. None of those symbols is reachable from
this integer-only function. The warnings are accounted for in Stages 5 and 7;
they did not cause or conceal a concrete failure.

### Fresh proof definition and every positive claim

Before compilation, `test ! -e verification-kompiled` exited 0. The Haskell
definition was then built solely from scratch source:

```text
kompile /tmp/audit-work/102-choose-num/verification.k \
  --backend haskell --main-module CHOOSE-NUM-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/102-choose-num/verification-kompiled
[exit 0]
```

Every submitted target claim was run independently:

| Claim selector | Output | Exit |
|---|---:|---:|
| `CHOOSE-NUM-SPEC.all-positive-inputs` | `#Top` | 0 |
| `CHOOSE-NUM-SPEC.even-upper-in-range` | `#Top` | 0 |
| `CHOOSE-NUM-SPEC.even-upper-before-range` | `#Top` | 0 |
| `CHOOSE-NUM-SPEC.odd-upper-predecessor-in-range` | `#Top` | 0 |
| `CHOOSE-NUM-SPEC.odd-upper-no-even-in-range` | `#Top` | 0 |

Each exact command has the form:

```text
kprove /tmp/audit-work/102-choose-num/spec.k \
  --definition /tmp/audit-work/102-choose-num/verification-kompiled \
  --spec-module CHOOSE-NUM-SPEC \
  --claims CHOOSE-NUM-SPEC.<label>
```

The complete command/output record is
[`evidence/04_proof_rebuild.log`](evidence/04_proof_rebuild.log). The only
Haskell warnings concern unused variables in the fixed supplied `str.k`; there
was no stuck claim, timeout, backend failure, or reused candidate cache.

## 4. Adequacy and real-program pinning

### Plain-language claim meanings

All five claims require the same exact clean initial state: environment 0; an
empty module scope whose parent is the builtins scope; next scope location 1;
empty heap and stack; `noRet`; `NoExc`; and exit code 0.

| Claim | Additional precondition | Required returned K value |
|---|---|---|
| `all-positive-inputs` | `X > 0`, `Y > 0` | `largestEvenInRange(X,Y)` |
| `even-upper-in-range` | positive; `Y mod 2 = 0`; `X <= Y` | `Y` |
| `even-upper-before-range` | positive; `Y mod 2 = 0`; `X > Y` | `-1` |
| `odd-upper-predecessor-in-range` | positive; `Y mod 2 = 1`; `X < Y` | `Y - 1` |
| `odd-upper-no-even-in-range` | positive; `Y mod 2 = 1`; `X >= Y` | `-1` |

For positive integers, `pyMod(Y,2)` is either 0 or 1. The two even subcases and
two odd subcases are disjoint and exhaustive.

### Satisfiable states and ground substitutions

The shared initial cell state above is concrete and realizable. The reviewer
exhibited at least one ground witness for every precondition:

| Claim | `(X,Y)` | Claimed value | Canonical | Generated |
|---|---:|---:|---:|---:|
| all positive | `(12,15)` | 14 | 14 | 14 |
| even/in range | `(12,14)` | 14 | 14 | 14 |
| even/before range | `(15,14)` | -1 | -1 | -1 |
| odd/predecessor in range | `(14,15)` | 14 | 14 | 14 |
| odd/no even | `(15,15)` | -1 | -1 | -1 |

[`evidence/claim_witnesses.py`](evidence/claim_witnesses.py) checked the
preconditions, `pyMod`, formula, and both Python implementations; it exited 0
with `witness_failures=0`. See
[`evidence/05_claim_witnesses.log`](evidence/05_claim_witnesses.log).

### Pinning to the submitted translated program

The claim starts with the proof-local entry item `#chooseNum(X,Y)`. Its sole
rule rewrites that item to a fixed-semantics `Call` of a `closureVal`. The
closure's parameters are exactly `("x","y")`, its parent scope is 0, its
arguments are exactly `(X,Y)`, and its body is the submitted function body.

[`evidence/program_pinning.py`](evidence/program_pinning.py) mechanically
removed only the outer `Module(FuncDef(...))` constructors from the submitted
`solution.mpy`, normalized the K list unit's equivalent omitted and explicit
spellings, and required exact identity with the closure body in
`verification.k`. It found one and only one `#chooseNum` operational rule and
reported:

```text
exact_submitted_body_in_wrapper=True
submitted_function_body_sha256=20486f357cab9c14fbfbb406401f87b5f2f7ae30895a4d04e05599a8118d0e88
[exit 0]
```

The fixed `FuncDef` rule in `semantics/functions.k` would bind exactly the same
closure at module load. The submitted module contains no executable statement
other than that function definition, so calling the exact closure directly
does not skip a module side effect relevant to `choose_num`.

The actual body is executed through fixed rules for call dispatch, parameter
binding, lookup, arithmetic, comparison, branching, return, and frame pop. It
is not replaced with `largestEvenInRange`. There are no helper or loop claims.
Every observable cell is present in the entry claims and returns to its stated
value. The right-hand K value is fixed, not existential, free, tautological, or
guarded by a one-way implication.

The limitation is auditability rather than soundness: `verification.k` embeds a
manually maintained exact copy instead of making the build depend directly on
`solution.mpy`. Current-artifact identity is established, but a future source
edit would require this pinning check to be repeated.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[`evidence/rule_inventory.md`](evidence/rule_inventory.md) enumerates every
local `requires`, module/import, configuration, syntax declaration, context,
ordinary rule, claim, and end-module statement in `semantics.k`, all 23 helper
K files, `verification.k`, and `spec.k`. Multi-line rules include their guards
and attributes. The inventory contains:

- 1,104 entries;
- 229 syntax declarations;
- 697 ordinary rules;
- 5 contexts;
- 1 configuration;
- 5 claims.

It identifies `function`, `total`, `functional`, `simplification`, `concrete`,
`owise`, `macro`, strictness, priority, symbol, and `no-evaluators` attributes
where present. There are no proof-local priority, simplification, functional,
concrete, or opaque declarations. The generator, exact command, exit 0, output
hash, and counts are preserved in
[`evidence/07_static_inventory.log`](evidence/07_static_inventory.log).

Each rule receives a theorem-relative decision:

- `FIXED-SUPPLIED/PATH`: fixed rule checked against the actual integer
  execution path;
- `FIXED-SUPPLIED/UNREACHABLE`: fixed baseline rule whose left-hand side cannot
  match a reachable term/value of this program;
- `PROOF-LOCAL/PATH`: candidate extension reviewed individually below;
- `ENTRY-CLAIM`: obligation checked for adequacy and non-vacuity.

This is not a claim that the supplied subset models every Python program.
For unreachable fixed rules, the narrower conclusion is that they cannot
enable any conclusion in this theorem. There is no intended-domain false
conclusion witness for them, so they are not mislabeled as unsound.

### Construct-to-rule map and execution fidelity

| Submitted construct | Declaration/evaluation | Operational effect |
|---|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `syntax.k`; `core.k` load/sequencing; `functions.k` function binding | Concrete load installs the exact closure in scope 0 |
| `Call`/closure | `call.k` lines 20-21 and 69-75 | Evaluate callee/arguments left-to-right, allocate frame, save continuation |
| `Name("x")`, `Name("y")` | `core.k` lines 131-154 | Resolve parameters from the new call frame |
| `Int` | `core.k` line 194 | Produce mathematical K integers |
| `UnaryOp("-")` | strict syntax; `operators.k` line 10; `int.k` line 7 | Evaluate operand, compute `0 -Int I` |
| `BinOp("%")`, `BinOp("-")` | sequentially strict syntax; `operators.k` line 12; `int.k` lines 13, 15, 19-20 | Preserve left-to-right evaluation; Python-style mod by positive 2 and integer subtraction |
| `Compare`, `CmpOp("==",...)`, `CmpOp(">=",...)` | comparison contexts and dispatch in `operators.k`; integer equations in `int.k` | Evaluate left then right and produce the intended Boolean |
| `If` | strict condition syntax; `controls.k` lines 51-54; `truthy(Bool)` in `core.k` | Execute exactly one selected statement list |
| `Return` | strict syntax; `functions.k` lines 78-90 | Record value, discard only the remaining callee body, restore caller continuation/environment, deallocate call scope |

The call creates scope 1, binds `x` and `y`, and pushes a frame. All body values
are integers or booleans. There is no heap allocation, mutation, output, or
exceptional operation. Return restores environment 0, scope location 1, empty
stack, `noRet`, and leaves the heap and exception cells unchanged. The literal
divisor is 2, so the partial zero-divisor case of integer modulo is unreachable.

Relevant rule patterns are sort-disjoint or guard-disjoint. Strictness and
contexts establish the expected evaluation order. Fixed priority rules for
heap references/cells cannot apply because the reachable operands are direct
integers and booleans. The generic `[owise]` call rule is the applicable route;
none of the fixed special `Call` patterns matches the closure call.

### Proof-local extension inventory

1. `#chooseNum(Int,Int)` is a fresh entry syntax item.
   Its sole rule is an entry adapter, closest to an operational bridge in the
   Kit taxonomy. It does not replace any fixed-semantics operation because the
   left side is fresh harness syntax. The right side begins the exact closure
   call and executes the entire body under fixed semantics. Its arbitrary
   continuation is preserved; it introduces no return, exception, frame pop,
   or state update itself. It reads/writes no non-`k` cell. Exact body,
   parameters, parent scope, and arguments are established by the pinning
   evidence in Stage 4.

2. `largestEvenInRange(Int,Int) [function,total]` is a definitional mathematical
   summary, not an operational replacement. It has one unconditional equation:

   ```text
   let r = pyMod(Y,2), z = Y-r;
   return z if X <= z, else -1.
   ```

   Coverage is total, there is no overlapping equation, and evaluation
   terminates. For positive `Y`, `r` is 0 or 1; therefore `z` is even and is the
   greatest even integer at or below `Y`. If `X <= z`, `z` is the interval
   maximum. If `X > z`, no even integer can lie between `X` and `Y`. The symbol
   is fully defined and is not an oracle.

There is no circularity in which the same opaque value drives execution and
the postcondition: program execution never uses `largestEvenInRange`.

### Priorities, opaque symbols, totality, and unused surface

The supplied baseline contains priority rules and opaque/total primitives for
other language features. The inventory records each one. The named opaque or
effectively opaque symbols are:

`md5hexCodes`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`floorFI`, `toF`, `ceilF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, `sortVS`, and `sortKeyVS`.

None appears in the submitted AST, proof-local rules, reachable values, guards,
or postconditions. Similarly, the compiler's non-exhaustive-totality warnings
are confined to unused string/list/float paths. They supply no branch, result,
state, or equality in this proof. This is an acceptable low-level fixed
semantics boundary, not a smuggled task answer.

### Independent operational sensitivity

As a check distinct from the false-postcondition test, the reviewer changed
only the even/in-range body return from `y` to `y + 2`, rebuilt a separate
Haskell definition, and asked it to prove the original result:

```text
kompile verification-body-mutation.k ... --output-definition body-mutation-kompiled
[exit 0]

kprove spec-body-mutation.k ... --dry-run
[exit 0]

kprove spec-body-mutation.k ... \
  --claims CHOOSE-NUM-SPEC-BODY-MUTATION.mutated-body-must-not-prove-original-result
[exit 1]
```

The residual explicitly contains the impossible equality
`Y #Equals Y +Int 2` on the reachable even/in-range branch and reports
`WarnStuckClaimState`. The mutation and complete transcript are
[`evidence/verification-body-mutation.k`](evidence/verification-body-mutation.k),
[`evidence/spec-body-mutation.k`](evidence/spec-body-mutation.k), and
[`evidence/08_body_sensitivity.log`](evidence/08_body_sensitivity.log).
This shows that closure depends on the body computation; the adapter does not
bypass it.

No inventoried rule supplies an intended-domain false conclusion witness.
Accordingly, no rule is labeled unsound.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. The reviewer created a distinct
fresh mutation,
[`evidence/spec-vacuity.k`](evidence/spec-vacuity.k), which requires the real
result to equal `largestEvenInRange(X,Y) + 2` for all positive inputs. This is
demonstrably false at the satisfying input `(X,Y)=(12,14)`: both Python
implementations and the correct formula return 14, while the mutated
postcondition requires 16.

The mutation parsed and built against the fresh definition:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module CHOOSE-NUM-SPEC-VACUITY --dry-run
[exit 0]
```

The actual mutation proof then exited 1:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module CHOOSE-NUM-SPEC-VACUITY \
  --claims CHOOSE-NUM-SPEC-VACUITY.false-off-by-two
[exit 1]
```

It produced `WarnStuckClaimState`, `WarnUnexploredBranches`, and a residual
whose even/in-range path has actual K value `Y` but requires the correct
conditional result plus 2. This is the expected unmet result obligation, not a
parser error, missing import, timeout, unrelated crash, or unreachable
mutation. The exact transcript is
[`evidence/06_nonvacuity.log`](evidence/06_nonvacuity.log).

## 7. Proven versus assumed accounting

### Precisely established by the reachability proof

Conditional on the fixed supplied MPY semantics and K toolchain, for every K
integer `X > 0` and `Y > 0`, starting in the exact clean state written in the
claim, execution of the exact submitted `choose_num` closure body satisfies:

```text
result =
  Y - pyMod(Y,2), if X <= Y - pyMod(Y,2);
  -1,             otherwise.
```

All five independently selected claims close. The four specialized claims also
establish the corresponding even/odd and in-range/out-of-range returns.
Execution consumes the function computation and restores the claimed
environment, scopes, allocation counters, heap, stack, return state, exception
state, and exit code. In the Kit's terms this is a partial-correctness theorem:
the postcondition holds on terminating executions. The body is straight-line
and all symbolic paths closed, but the report does not broaden the theorem
beyond the supplied semantics.

### Trust ledger and limitations

| Boundary or assumption | Influence | Assessment |
|---|---|---|
| Trusted prompt, canonical implementation, and translator mounts | Natural-language intent and source-to-MPY bridge | Authorized trusted inputs; candidate copies and one generated output were byte-checked |
| Supplied MPY semantics | All operational behavior | Authorized fixed semantics; candidate tree recursively identical and rebuilt fresh |
| K v7.1.337, Haskell/LLVM backends, SMT and K integer/map/list primitives | Compilation, symbolic arithmetic, proof closure, concrete execution | Ordinary formal-tool trust boundary; versions and actual outputs recorded |
| Unbounded K `Int`, `+Int`, `-Int`, comparisons, `%Int`, Boolean connectives | Every result-bearing arithmetic step | Matches Python's unbounded integers on the positive-integer domain; `pyMod(_,2)` is explicitly defined |
| Current `solution.mpy` body equals the closure embedded in `verification.k` | Pinning theorem to the submitted program | Mechanically checked and body-sensitive, but not a build-time file dependency; documented concern |
| Formula means greatest even integer in the interval | Bridge from formal result to prose | Elementary ordinary mathematics, explained above; not separately encoded as quantified maximality/evenness predicates |
| Intended inputs are positive integers | Theorem scope | Consistent with canonical parity logic and examples; the prompt says “positive numbers” without an explicit type annotation, so floats/bools are not covered |
| Differential run over 45,013 inputs | Python rewrite/canonical adequacy | Strong finite evidence only; not used as a universal proof |
| Fixed opaque float/sort/digest and other unused primitives | None on this AST or postcondition | Imported baseline surface but unreachable and harmless for this theorem |
| Missing generation/provenance logs | Audit trail only | Prevents full reconstruction of how the candidate was produced; does not affect fresh proof reconstruction |

### Excluded behavior

The theorem does not cover zero or negative inputs, floats, booleans as Python
integers, wrong arity/types, alternative Python implementations, or behavior
outside the supplied MPY subset. It proves the current translated function
under the stated clean initial state. Differential testing and the canonical
file support the intent bridge but are not substituted for the K proof.

### Decision

Gate A (real-program soundness) passes: the exact body executes, both
result- and body-sensitivity tests reject false alternatives, and no
result-bearing oracle or unsound proof extension is present. Gate B (intent
adequacy) passes for positive integers, with the documented type-wording and
formula-to-prose limitations. Gate C is adequate for legitimacy but has the
missing-provenance and manual-pinning auditability concerns described above.
Those concerns warrant `CONCERNS`, not `FAIL`: the proof remains sound,
result-constraining, and pinned to the current real generated program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
