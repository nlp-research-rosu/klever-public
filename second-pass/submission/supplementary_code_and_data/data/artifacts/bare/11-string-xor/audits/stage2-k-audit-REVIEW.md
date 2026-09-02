# Independent adversarial review: 11-string-xor

The candidate reconstructs and closes a non-vacuous reachability proof under
its generated K semantics, and its proof-local accelerations are sound relative
to that idealized semantics. It is nevertheless not a legitimate proof of the
real generated Python program over the unrestricted HumanEval contract. The
generated semantics models recursive calls as unbounded and has no
`RecursionError` control effect. A valid length-998 input is a concrete false
conclusion witness: canonical Python returns normally, candidate Python raises,
and the exact translated K program returns normally. This materially narrows
the source-contract domain.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout =
legacy-selected-stage1`, `condition = bare`, problem `11-string-xor`, and
`semantics_mode = GENERATED_SEMANTICS`.

I inspected all records required for that layout:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the complete 414-record structured JSONL trace below
  `/generation-evidence/codex-trace/`.

All are regular, readable, non-symlink files. There are no symlinks in the
candidate, reference, or generation-evidence trees. Historical
`runtime-metrics.json` is absent, which the prompt explicitly allows for this
legacy-selected layout. The generation records were treated only as untrusted
claims; the full trace was parsed and inventoried in
[01-trace-inventory.log](evidence/01-trace-inventory.log).

The campaign block embedded in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, whose independently computed SHA-256 is the
recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
Every recorded per-file digest checked by the audit matches. The independently
computed pipeline tree digest of the mounted candidate is
`4305163a5da340cdf88e7d6f8207e7dc5500750b35d525b2f97e412424a2c19d`,
matching both the invocation and stage-one result workspace records. The trace
tree digest is
`c36712df6cc5e8be5601c154e9a6af14b8f6e60d1b3d2f5fbb137c18e5e47f8f`,
matching `usage.json`; its single JSONL file also matches the stage-one
per-file digest.

Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
mounted versions. `/reference/reference-semantics` is absent, as required for
`GENERATED_SEMANTICS`; there is no mode/mount contradiction. Commands, hashes,
and exit 0 are preserved in
[01-provenance.log](evidence/01-provenance.log) and the reviewer script
[01_provenance.sh](evidence/01_provenance.sh).

Stage result: provenance integrity passes; there is no audit-infrastructure
breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt requires `string_xor(a, b)` to accept binary strings and
return their bitwise XOR as a string. The trusted canonical implementation uses
`zip(a,b)`, so its observable behavior on unequal lengths truncates at the
shorter input.

The candidate implements the same value algorithm by recursively:

1. returning empty when either input is empty;
2. returning `"0"` plus the recursive tail result when the heads agree; and
3. returning `"1"` plus the recursive tail result otherwise.

Trusted regeneration with `/reference/py2mpy.py` is byte-identical to submitted
`solution.mpy`. See
[02-fidelity.log](evidence/02-fidelity.log).

The independent differential test covers the documented example, empty inputs,
all one-bit branch outcomes, unequal lengths, a 900-character recursion case,
all 65,025 pairs of binary strings with independent lengths 0 through 7, and
2,000 deterministic random pairs up to length 120. It found zero value
mismatches over 67,038 pairs:
[02_differential.py](evidence/02_differential.py).

That finite range stops just below the material runtime boundary. A separate
boundary test records the actual CPython recursion limit as 1000:

| Input lengths | Trusted canonical | Candidate |
|---:|---|---|
| 997, 997 | returns length 997 | returns length 997 |
| 998, 998 | returns length 998 | raises `RecursionError` |
| 1000, 1000 | returns length 1000 | raises `RecursionError` |
| 1100, 1100 | returns length 1100 | raises `RecursionError` |

The exact inputs are valid binary strings (`"0" * length`) and the prompt has
no length precondition. Commands and outcomes are in
[02-recursion-boundary.log](evidence/02-recursion-boundary.log), produced by
[02_recursion_boundary.py](evidence/02_recursion_boundary.py).

Stage result: trusted translation fidelity passes, but real implementation
fidelity fails on the unrestricted source-contract domain. This is a material
result/exception divergence, not a finite-test uncertainty.

## 3. Clean proof reconstruction

I copied only candidate source artifacts to
`/tmp/audit-work/11-string-xor/source`. No candidate-built definition or cache
was copied or reused. With K v7.1.293, I freshly built:

- LLVM `semantic.k`, main module `XOR`, syntax `MPY-SYNTAX`; and
- Haskell `verification.k`, main module `XOR-VERIFICATION`, syntax
  `MPY-SYNTAX`.

The original combined command

```text
kprove spec.k --spec-module XOR-SPEC \
  --definition /tmp/audit-work/11-string-xor/build/verification-kompiled \
  --output pretty
```

printed `#Top` and exited 0. A labeled audit copy proved the recursive claim
alone with `#Top`, and proved the intended two-claim set with `#Top`. The entry
claim depends on the recursive circularity, so filtering the helper out is not
an independent form of the intended target. Exact commands, all successful
outputs, and the final script status 0 are in
[03-rebuild.log](evidence/03-rebuild.log).

Fresh LLVM execution of the real `solution.mpy` matches Python values for:

- both empty-input branches;
- every single-bit equal/different branch;
- the prompt example;
- both unequal-length directions; and
- both concrete `cons` strings and proof-side `segment/seed` strings.

Each logged result is mechanically checked against its expected K term in
[03-concrete.log](evidence/03-concrete.log).

The decisive semantics discrepancy also reconstructs dynamically. On
`Args(str(segment(998,seed(0))), str(segment(998,seed(0))))`, `krun` exits 0
and returns a `str` containing exactly 998 false-bit `cons` constructors. On
the corresponding real inputs, candidate Python raises `RecursionError`.
[02-recursion-boundary.log](evidence/02-recursion-boundary.log) records both
sides.

Stage result: proof reconstruction succeeds under the submitted theory, but
generated-semantics execution is not faithful to the real recursive program on
the full intended domain.

## 4. Adequacy and real-program pinning

The recursive claim says:

> For any nonnegative `N` and `M`, executing the exact submitted function body
> in an environment holding `segment(N,S1)` and `segment(M,S2)` returns
> `xorText(N,M,S1,S2)`, preserving an arbitrary caller continuation and
> arbitrary `<args>`.

The entry claim says:

> Starting from the exact translated one-function module and two
> nonnegative-length segments, execution returns the same `xorText` result.

These are result-constraining reachability claims, not implications to a free
result. The entry precondition is satisfiable. For example,
`N=M=3`, `S1=seed(2)`, `S2=seed(3)` represents `"010"` and `"110"` and the
claimed result is `"100"`. Both Python implementations and both ground K
claims agree. See
[04-spec-ground-witness.k](evidence/04-spec-ground-witness.k) and
[04-pinning.log](evidence/04-pinning.log).

Real-program constructor pinning passes. After macro expansion, the KORE for
trusted-regenerated `solution.mpy` and `solutionProgram` is byte-identical:

```text
45ce3e937fc565ea64b7138cc3cb9ab8d24c2d5b4b162d0d28d9790dac8341ad
```

A body-sensitivity mutation changes the executed unequal-head literal from
`"1"` to `"0"` while leaving the original result obligation `"1"`. It builds,
executes to `returned("0")`, and is rejected with a stuck claim. Thus changing
only the actual program term invalidates the theorem; the bridge does not hide
that mutation. Evidence:
[04-spec-body-sensitivity.k](evidence/04-spec-body-sensitivity.k).

At the value-representation level, every finite binary string
`c[0:n]` is represented by
`segment(n,seed(sum(bit(c[i]) * 2^i)))`; the separate length preserves leading
zeroes. `xorText` consumes until either length is zero, matching canonical
`zip`.

The adequacy failure is operational, not syntactic or algebraic. The formal
precondition accepts `N=998`; its K execution returns normally, whereas the
actual candidate raises. The generated definition omits a material control
effect exercised by the submitted recursive body. Therefore the claim does not
pin real-program behavior on the unrestricted contract even though it pins the
constructor body.

Stage result: constructor pinning and result adequacy pass inside the idealized
model; real-execution/domain adequacy fails.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[05-static-rule-review.md](evidence/05-static-rule-review.md), backed by the
line-indexed source record
[05-inventory.log](evidence/05-inventory.log). It enumerates every local syntax
declaration and all 35 rules in `semantic.k`, all 9 rules in `verification.k`,
all attributes, both claims, and the absence of local simplification rules,
functional declarations, or proof-local lemmas.

### Construct and state coverage

Every constructor used by `solution.mpy` is declared and executed:
`Module`, `FuncDef`, `Params`, statement lists, `If`, `Return`, `Name`, `Str`,
`Int`, `Compare`/`CmpOp`, `BinOp`, `Subscript`, `Slice`/`NoBound`, and `Call`.
Only `<k>` and read-only `<args>` cells are modeled. No used construct requires
heap, output, allocation, or mutation.

The non-`seqstrict` operand order is broader than CPython's left-to-right order,
but all submitted operands are pure and there is no observable state or
modeled exception on the covered short executions. Equality, indexing, slicing,
concatenation, if selection, return propagation, and statement continuation
rules are disjoint or agree on overlaps. The three `xorText` equations have
disjoint guards exhaustive for nonnegative claim inputs and descend on each
recursive step.

`head` is total and functional. Every ground `Stream` term normalizes through
`next(seed(I))`; `head(seed(I))` fixes its parity bit. For symbolic streams the
theorem is parametric in the same abstract selector on both execution and
summary, so it is not a result oracle.

### Proof-local accelerations

The three priority-40 `exec` rules are operational bridges over the exact body:

- `N=0` models the first empty return;
- `N>0,M=0` models the second empty return; and
- positive lengths prepend Boolean head XOR and recurse on the exact tails.

Their guards are disjoint. No concrete or symbolic false conclusion exists for
these bridges relative to the candidate's idealized semantics. I independently
validated them by compiling a reviewer-authored definition containing the
exact program/body macros and identical recursive summary but no `priority`,
`prependResult`, or `exec` shortcut. Expanded KORE again matches
`solution.mpy`, and both universal claims close with `#Top`:
[05-bridge-free-identity.log](evidence/05-bridge-free-identity.log) and
[05-bridge-free.log](evidence/05-bridge-free.log). Thus the bridges do not
smuggle the XOR result relative to fixed submitted semantics.

### Unsound used rule and concrete false conclusion witness

`semantic.k:109` rewrites every recursive call directly to a fresh `exec` of
the same body. The configuration has no call-stack depth and no exception
state, so this rule permits unbounded recursion. That is materially unsound as
a semantics of the actual submitted CPython program on its unrestricted valid
inputs.

Concrete witness:

```text
a = "0" * 998
b = "0" * 998
sys.getrecursionlimit() = 1000
```

- trusted canonical: normal return, 998 zeroes;
- candidate Python: raises `RecursionError`;
- generated semantics executing the real `solution.mpy`: normal return, 998
  false bits, exit 0.

The rule therefore enables the false conclusion that the real function
normally returns its XOR at length 998. This is not inferred from a timeout or
missing feature; all three outcomes were executed and recorded in
[02-recursion-boundary.log](evidence/02-recursion-boundary.log).

Stage result: the local proof theory is consistent and its accelerations are
connected to the ideal semantics, but the used recursive-call semantics is
materially unsound relative to real CPython behavior on the intended domain.

## 6. Fresh non-vacuity test

The reviewer mutation keeps the exact `solutionProgram` and a satisfiable input
`a="0", b="1"` unchanged, but changes the required result from true `"1"` to
false `"0"`:
[06-spec-vacuity-audit.k](evidence/06-spec-vacuity-audit.k).

`kprove --dry-run` succeeds, establishing that the mutation parses and builds.
The actual proof exits 1 with `WarnStuckClaimState`; the residual is the
reachable

```text
returned ( str ( cons ( true , empty ) ) )
```

against the false destination. The wrapper verifies both the nonzero status and
the expected residual, then exits 0:
[06-nonvacuity.log](evidence/06-nonvacuity.log).

Stage result: the proof is non-vacuous and discriminates its result. This does
not repair the source-semantics/domain mismatch.

## 7. Proven versus assumed accounting

What the successful reachability proof actually establishes is:

> Under the submitted idealized K semantics, with mathematical unbounded
> recursion, executing the exact translated function on arbitrary
> nonnegative-length bit segments returns the recursive `xorText` pairwise-XOR
> summary.

That statement is machine-checked twice: with the candidate's accelerations and
with a fresh acceleration-free definition.

Trust and assumption ledger:

| Boundary | Effect | Assessment |
|---|---|---|
| K v7.1.293 compiler, LLVM/Haskell backends, SMT/K builtins | Proof/execution engine | Ordinary unavoidable toolchain trust. |
| Imported `BOOL`, `INT`, `STRING` operations | Bit parity, division, comparison, XOR, strings | Acceptable low-level primitives; used equations have ordinary mathematical meaning. |
| Trusted `py2mpy.py` | Python AST to constructor identity | Byte regeneration and KORE macro comparison independently checked. |
| `segment/seed/head/next` representation | Connects bit strings to proof values | Algebraically adequate for every finite binary string; concrete normal/boundary executions support it. |
| `xorText` to canonical `zip` XOR | Human-facing result meaning | Follows by induction on the shorter nonnegative length; broad finite differential evidence has zero value mismatches below the runtime boundary. |
| Priority-40 operational bridges | Skip fixed interpreter steps | Acceptable relative to submitted semantics because a bridge-free universal K proof closes. |
| Unbounded recursive-call rule with no stack/exception | Changes normal return versus `RecursionError` | Illegitimate and decisive. It affects control, termination mode, and the claimed final result on valid source inputs. |

The proof is not merely missing evidence about the last boundary: the
length-998 witness demonstrates the opposite behavior. The source contract has
no length restriction, and the trusted canonical handles the witness. Treating
the mathematical K execution as the real Python execution materially narrows
the HumanEval domain. Under the benchmark's explicit mapping, that is
`FAIL / NOT_LEGIT`, even though the idealized theorem is machine-checked,
result-constraining, body-sensitive, and non-vacuous.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
