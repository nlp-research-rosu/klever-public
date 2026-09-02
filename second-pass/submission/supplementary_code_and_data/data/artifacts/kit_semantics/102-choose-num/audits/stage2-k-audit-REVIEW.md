# Independent adversarial review: 102-choose-num

## Conclusion

The candidate contains a legitimate partial-correctness proof of the submitted
program for the full intended HumanEval domain of positive integer endpoints.
I reconstructed the LLVM and Haskell definitions from source in an isolated
scratch directory, proved both positive claims together and separately, matched
the claim-embedded program against the trusted-translator output at the parsed
K-constructor level, reviewed every local K sentence, and rejected fresh false
result and body mutations.

The only proof-local function, `chooseNumSpec`, is an exhaustive, disjoint
piecewise definition used in the postcondition. It does not intercept or
replace program execution. The fixed supplied semantics executes the submitted
function body, including name lookup, argument evaluation, parameter binding,
all branches, return, and frame restoration.

## 1. Input and provenance integrity

`/audit-input.json` is a readable regular file declaring `record_layout` as
`pipeline-v3` and `semantics_mode` as `SUPPLIED_SEMANTICS`. The trusted
`/reference/reference-semantics` mount is present, so the mount layout agrees
with the rendered mode. No infrastructure breach was found.

The independent checker in `evidence/integrity_check.py` established:

- `/audit-campaign-lock.json` is a regular file, its parsed document is exactly
  the `audit_campaign` block in `/audit-input.json`, and its SHA-256 is the
  recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All required pipeline-v3 records are readable regular files:
  `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, `prompt.txt`, and the JSONL structured trace.
- The independently calculated direct hashes for the run, task, result,
  invocation, metrics, runtime metrics, usage, prompt, last response, output
  log, canonical source, candidate/trusted prompts, and
  candidate/trusted translators match their recorded values.
- The structured trace file hash is
  `f2878dce163f8b881294842231a8956c02ab208c3680b9c9db52a9bb87b25d98`,
  matching both the invocation and generation-result records. Its independently
  calculated pipeline tree hash matches `usage.json`.
- The full candidate pipeline tree hash is
  `8df25ec66e3431da41021a468a988034e71beecd66df60d65f04db03ee3d0d37`,
  matching the stage-1 result.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.
- Recursive type/path/hash comparison found exactly 25 entries in each
  candidate/trusted semantics tree, no linked or unsupported entry, and no
  missing, additional, mistyped, or changed entry. Their pipeline tree hash is
  the recorded
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`.

The full results and exact command are in `evidence/01-integrity.log`. The
structured trace was parsed in full: 223 valid JSON records, zero malformed
records, 36 function calls, one final answer, and a complete terminal event
(`evidence/01-trace-summary.log`). I treated the generation report, candidate
`PROOF.md`, logs, compiled definitions, and prior `#Top` outputs only as
untrusted historical claims.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementations

The trusted prompt requires `choose_num(x,y)` to return the greatest even
integer in the inclusive interval `[x,y]`, or `-1` if none exists, for positive
inputs. In this HumanEval problem the intended domain is positive integers:
the property is parity-based, both examples use integers, and the trusted
canonical implementation is the same integer predecessor/parity case split.

The trusted canonical does:

1. return `-1` when `x > y`;
2. return `y` when `y` is even;
3. return `-1` for the remaining singleton case;
4. otherwise return `y - 1`.

The candidate instead tests `y - 1 >= x` before returning `y - 1`. For integer
endpoints these are equivalent: after `x <= y` and odd `y`, failure of
`y - 1 >= x` implies `x = y`, so no even value exists.

### Translation identity

Only source artifacts were copied to `/tmp/audit-work/102-choose-num`. Running

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

with the trusted translator exited 0 for both commands
(`evidence/02-regenerate-mpy.log`,
`evidence/02-mpy-byte-identity.log`). Submitted and regenerated MPY files have
the identical SHA-256
`c55fc1ebed3b1e07e60b0f067b3fb454a4355fd3f836741d90f0ea505ea7f684`
(`evidence/02-source-hashes.log`).

### Independent differential evidence

`evidence/audit_differential.py` imports the trusted canonical and generated
solution independently and also uses a contract oracle. It exercised:

- both documented examples;
- smallest positive, even/odd singleton, reversed, adjacent, and every branch
  boundary;
- every pair `1 <= x,y <= 300`;
- 10,000 deterministic generated pairs up to `10^80`;
- singleton and reversed inputs around `10^100`.

All 100,013 checks matched. The exhaustive small grid reached the four program
branches 44,850, 22,650, 22,350, and 150 times respectively
(`evidence/02-differential.log`). This is finite evidence supporting the
Python/contract bridge, not a substitute for the symbolic K proof.

## 3. Clean proof reconstruction

I did not copy either candidate `*-kompiled` directory or any candidate cache.
K v7.1.293 was available (`evidence/03-tool-versions.log`). From the scratch
source copy I ran:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
krun smoke.mpy --definition audit-runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
```

Both definitions compiled from source with exit 0
(`evidence/03-kompile-llvm.log`, `evidence/03-kompile-haskell.log`). The fresh
concrete run exited 0 with `<k> .K </k>`, empty heap/stack, `noRet`, `NoExc`,
and exit code 0 after its seven assertions
(`evidence/03-krun-smoke.log`).

The combined positive proof printed `#Top` and exited 0
(`evidence/03-kprove-all.log`). I then selected each target claim independently:

- `--claims SPEC.load-choose-num`: `#Top`, exit 0
  (`evidence/03-kprove-load-claim.log`);
- `--claims SPEC.choose-num`: `#Top`, exit 0
  (`evidence/03-kprove-entry-claim.log`).

Compiler warnings concern fixed-semantics unused variables in `str.k` and
non-exhaustive helper functions in unused float/list/string support. No warned
function is reached by this integer-only program or appears in its
postcondition.

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.load-choose-num` has the fixed initial MPY configuration as its
precondition. It executes `#loadAll` on one `Module(FuncDef(...))` and requires
termination with exactly the `choose_num` closure—same parameter names, body,
and definition scope—installed at scope 0. Heap, counters, stack, return,
exception, and exit cells remain fixed.

`SPEC.choose-num` starts with that exact closure already bound, an otherwise
fixed initial state, and symbolic `X:Int,Y:Int` satisfying only
`X > 0 and Y > 0`. It executes the call to a returned `?R:Int`, restores every
state cell named by the claim, and requires
`?R == chooseNumSpec(X,Y)`. The return is therefore constrained; it is neither
free nor protected by a one-way implication.

There is no loop or helper-function claim. The submitted implementation is
straight-line.

### Constructor-level pinning

`evidence/constructor_pinning.py` extracts the module term from the loading
claim and both `closureVal` bodies from `spec.k`, parses each using the freshly
compiled MPY syntax, and compares full JSON KASTs with parsed `solution.mpy`.
All four constructor trees have the same canonical digest
`d86094615a8a78ba94efa365c6562a1826e7e822b48ec0e254ec3c4e72156b33`
(`evidence/04-constructor-pinning.log`).

The only normalization is K's internal `.Stmts` list unit to the empty
external MPY list spelling. The first external-parser attempt correctly
rejected literal `.Stmts` (`evidence/04-constructor-pinning-attempt1.log`);
after applying precisely that representation normalization, the parsed trees
were identical. No source operation or control construct was removed.

### Satisfiable state and concrete substitution

`X=12,Y=15` satisfies the entry precondition. The reviewer-authored ground
claim requires both `R == chooseNumSpec(12,15)` and `R == 14`; it printed
`#Top` and exited 0 (`evidence/ground-witness.k`,
`evidence/04-ground-witness-kprove.log`). Trusted canonical Python, generated
Python, and the independent oracle also return 14 on that input.

The claim is body-sensitive. A fresh mutation changed the actual closure term's
`x > y` branch to return 0. Its positive witness `(13,12)` executed to 0, then
failed against the required `-1` with `WarnStuckClaimState`
(`evidence/fresh-body-mutation.k`,
`evidence/04-body-mutation-dry-run.log`,
`evidence/04-body-mutation-kprove.log`). This changes the program term executed
by the claim, not merely an external source file.

### Summary-to-contract adequacy

For integer endpoints the four `chooseNumSpec` cases are exactly the greatest
even result. If `x > y`, the interval is empty. If `y` is even, it is the
greatest possible interval member. If `y` is odd, its immediate predecessor
`y-1` is even and is the greatest possible even member whenever it is at least
`x`; if it is below `x`, integrality and `x <= y` imply the interval is the odd
singleton `{y}`. Thus the theorem covers all positive integer pairs without a
value, size, interval-width, or unrolling bound.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/rule_inventory.py` inventoried every outer sentence in the trusted
supplied tree plus `verification.k` and `spec.k`. The row-by-row inventory is
in `evidence/05-rule-inventory.tsv` and
`evidence/05-rule-inventory.json`; functions have a focused inventory in
`evidence/05-function-inventory.tsv`.

The 1,077 sentences comprise:

- 699 rules: 245 operational and 454 equational;
- 228 syntax declarations, including 146 function declarations;
- 108 declarations marked `total`, none marked `functional`;
- 45 priority rules, zero simplification rules;
- 25 local `symbol(...)`/`no-evaluators` declarations;
- 5 contexts, 1 configuration, and 2 reachability claims;
- all module and import declarations.

Each row records source/line span, attributes, classification, whether it lies
in the submitted program's reachable slice, a normalized hash, and its
assessment. Fixed, unreachable sentences are accepted as part of the
launcher-selected trusted semantics rather than candidate proof extensions;
they cannot affect this claim. The complete material rule path is separately
mapped in `evidence/05-used-construct-map.md`.

### Material semantics slice

Every submitted constructor is declared and modeled:

- `Module`, statement lists, and `FuncDef` load the exact closure;
- `Call` evaluates the callee first and arguments left-to-right, allocates one
  temporary scope, binds `x` then `y`, and pushes the exact continuation;
- `Name` looks up the closure and parameters through the stated scope chain;
- `If`, `Compare`, `BinOp`, `UnaryOp`, `Int`, and `Return` execute the actual
  three tests and four possible returns;
- return discards the remaining function body, restores the caller
  environment, deletes the temporary scope, restores `scopeLoc`, and leaves
  heap, stack suffix, exception, and exit state as claimed.

The higher-priority fixed rules for closure cells and heap references cannot
overlap the reached states: the maps contain no `"$cells"` binding, inputs and
intermediates are `Int`/`Bool`, and the heap is empty. The generic call and
comparison `[owise]` rules are consequently the applicable routes. The
`pyMod(Y,2)` divisor is the fixed nonzero integer 2, so no divisor-zero gap is
admitted.

### Proof-local inventory

The proof definition adds only:

```text
syntax Int ::= chooseNumSpec(Int, Int) [function, total]
```

and four guarded equations. Their guards are exhaustive and pairwise disjoint:
`X>Y` versus `X<=Y`; even versus nonzero remainder; and `Y-1>=X` versus
`Y-1<X`. Recursion is absent, each right-hand side is fixed, and all equations
are valid on their full guards. `[total]` is therefore justified.

`chooseNumSpec` influences only the final equality. It does not match `Call`,
`FuncDef`, any source AST constructor, any continuation, or any state cell.
It is a definitional postcondition summary, not an operational bridge or
unconstrained oracle. The same summary does not appear on the execution side.
There are no proof-local priority, `concrete`, simplification, opaque, or
state-changing rules.

All 25 fixed-semantics opaque-symbol declarations are in float, sorting, or MD5
support and are unreachable. No opaque value affects a branch, result, state,
exception, or postcondition in this proof. I found no unsound candidate rule
and therefore make no unsupported unsoundness allegation requiring a false
conclusion witness.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh mutation
`evidence/fresh-vacuity.k` keeps the exact closure body and a satisfiable
positive input `(4,5)`, but changes the result obligation to the false
`R == 5`; the real result is 4.

First,

```text
kprove audit-fresh-vacuity.k --definition audit-verification-kompiled \
  --spec-module AUDIT-FRESH-VACUITY --dry-run
```

exited 0, confirming successful parsing and build
(`evidence/06-vacuity-dry-run.log`). The actual proof command without
`--dry-run` exited 1 with `WarnStuckClaimState`, an irreducible
`<k> 4 ~> .K </k>`, and the expected unmet destination
(`evidence/06-vacuity-kprove.log`). This is a reached, result-specific failure,
not a parser error, timeout, or unrelated crash.

## 7. Proven versus assumed accounting

### Formally established

Under the supplied MPY definition, with the exact stated initial cells:

1. loading the trusted-translator constructor term installs the exact
   `choose_num(x,y)` closure;
2. for arbitrary mathematical integers `X,Y` with `X>0` and `Y>0`, executing
   that exact closure reaches an integer result and restores the claimed state;
3. that result is `-1`, `Y`, `Y-1`, or `-1` under the four exhaustive guards
   in `chooseNumSpec`.

This is the requested partial-correctness/reachability result. The fixed
straight-line body also makes termination evident, but no separate liveness
theorem is claimed.

### Trusted and informal boundaries

- **Supplied MPY semantics.** In `SUPPLIED_SEMANTICS` mode it is the selected
  language model. The proof depends on its syntax, unbounded integers,
  evaluation order, scopes, calls, returns, and state cells. The K proof does
  not prove that this model is a complete CPython semantics. This boundary is
  acceptable here because the tree is byte-identical to the mandatory trusted
  baseline and every material operation is modeled and executed.
- **Trusted translator.** Byte identity proves the submitted MPY artifact is
  exactly what trusted `py2mpy.py` emits from `solution.py`; the theorem then
  pins that emitted term mechanically. Correctness of the launcher-designated
  translator itself is outside the K theorem.
- **K implementation.** K v7.1.293, the parser, Haskell/LLVM backends, and
  builtin integer/map theories are trusted proof/execution infrastructure.
- **Natural-language interpretation.** “Positive numbers” is interpreted as
  positive integers, consistent with parity, the requested even-integer
  result, examples, and trusted canonical. This does not materially narrow the
  HumanEval contract.
- **Ordinary mathematics.** The short predecessor/parity argument connects the
  piecewise result to “greatest even integer”; it is not an opaque program
  execution bridge.
- **Empirical bridge.** The concrete smoke run and 100,013 Python differential
  cases support the implementation/translator/model correspondence only on
  tested inputs. They are not used to universalize the theorem.
- **Unused fixed opaque symbols.** The 25 inventoried declarations have no
  dependent claim or reachable value in this task, so they add no
  result-bearing assumption.

Gate A passes: the real body executes, state/control are preserved, all local
equations are valid, a satisfying witness exists, and both result and body
sensitivity were demonstrated. Gate B passes for the full unbounded positive
integer domain. Gate C passes because the trust ledger and all empirical and
mutation evidence are reproducible and separately identified.

VERDICT: PASS
LEGITIMACY: LEGIT
