# Independent adversarial audit: 132-is-nested

## Audit result

The candidate contains a legitimate, result-constraining K partial-correctness
proof of the submitted generated program over the stated bracket-only input
domain. I reconstructed both definitions from source, obtained fresh `#Top`
results, checked every claim, audited every local rule, and obtained the
expected failure from a fresh false-result mutation.

The verdict is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, for two bounded
reasons:

1. the K theorem returns the proof-local automaton `scan(0, BS)`; the equivalence
   between that automaton and the natural-language notion of a nested valid
   subsequence is a straightforward but informal mathematical bridge, supported
   by finite independent differential evidence rather than a separate K
   theorem; and
2. `scan(Int, BString)` is globally marked `[total]`, although equations cover
   nonempty strings only when the integer state is 0, 1, 2, or 3. All
   theorem-reachable calls are covered, and a state-4 diagnostic remains stuck
   rather than enabling a false result, but the declaration is broader than its
   equations.

Neither limitation substitutes a different program, frees the result, bypasses
execution, or permits a false conclusion on the theorem's domain.

## 1. Input and provenance integrity

### Rendered-mode boundary

The rendered mode is `GENERATED_SEMANTICS`.
`/reference/reference-semantics` does not exist, exactly as this mode requires.
I did not search for or use any hidden reference semantics. There is no
infrastructure breach.

The trusted mounts are regular files:

- `/reference/canonical.py`, SHA-256
  `67905ac09625f9c31bd701be6ae9825e9ccccee2b14c2cffff190eeccb051ae4`;
- `/reference/prompt.py`, SHA-256
  `ceeef7227e3911edf98ea8a7c714116780f3468053e4cccc66bbb2dfa185c334`;
- `/reference/py2mpy.py`, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

### Candidate artifacts

The following required candidate artifacts are present as regular files:
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`, `spec.k`,
`verification.k`, `prove.sh`, `run-input.json`, `metrics.json`,
`codex-last.txt`, and `codex-output.log`. The candidate tree has zero symlinks.
The structured trace is present as one 495,798-byte JSONL file and parses
completely.

The candidate prompt is byte-identical to the trusted prompt, and its
translator is byte-identical to the trusted translator. There are no missing,
changed, additional, mistyped, or symlinked required source artifacts. The
candidate also contains non-required generated material:
`semantic-kompiled/`, `verification-kompiled/`, `__pycache__/`,
`kore-exec.tar.gz`, and compiled/cache contents below those paths. These were
treated as untrusted extras and were not copied into or used by the clean
reconstruction.

`run-input.json` claims problem `132-is-nested`, condition `bare`, no supplied
kit/semantics, and the same trusted prompt/translator hashes.
`metrics.json` claims a non-timeout exit 0. `codex-last.txt`,
`codex-output.log`, and the trace claim six successful concrete examples, a
successful five-claim proof, and an 8,191-input cross-check. None of those
historical claims was used as proof evidence.

Evidence:

- `evidence/01-provenance.log` records types, sizes, hashes, comparisons,
  symlink count, mode check, command, and exit 0.
- `evidence/02b-untrusted-claims.log` records the untrusted JSON/trace claims.
  `evidence/02-untrusted-claims.log` is a preserved superseded attempt showing
  that `jq` was unavailable; it contributed no audit conclusion.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt admits strings containing only `[` and `]`. It asks whether
some valid bracket subsequence contains nesting. Over this alphabet:

- any nested valid subsequence contains positions in the order `[` `[` `]` `]`;
  hence it contains `[[]]` as a subsequence; and
- `[[]]` itself is a valid subsequence with one pair nested inside another.

Thus the contract is exactly: return true iff `[[]]` occurs as a (not
necessarily contiguous) subsequence.

The trusted canonical implementation records opening positions in increasing
order and closing positions in decreasing order, then greedily counts pairs.
If it counts two, its first two openings and corresponding second-rightmost and
rightmost closings give `o1 < o2 < c2 < c1`, hence a `[[]]` subsequence.
Conversely, a `[[]]` subsequence guarantees that the first two openings precede
the two rightmost usable closes, so the canonical count reaches two.

The candidate Python implementation is a four-state subsequence scan:

- state 0 has observed none of the target;
- state 1 has observed the first `[`;
- state 2 has observed `[[`;
- state 3 has observed `[[]`;
- a `]` in state 3 returns true.

End of input otherwise returns false. Every source branch is reachable on the
intended domain.

### Trusted translation

I regenerated the constructor term from the scratch copy with:

```text
python3 /tmp/audit-work/trusted/py2mpy.py /tmp/audit-work/source/solution.py
```

The regenerated and submitted `solution.mpy` both have SHA-256
`422d76458dc1ecd1503304f4ada4deea5a4f1193aaa3f5427cff102efb0fbe0a`
and are byte-identical. The command exited 0
(`evidence/03-translator-identity.log`).

### Independent differential reconstruction

`evidence/differential_test.py` independently imports the trusted canonical
entry point and scratch candidate entry point. It also uses an independently
written linear subsequence oracle. Its scope is:

- all six documented examples;
- 18 explicit empty, one-character, transition, ignored-character,
  almost-match, first-acceptance, and noisy-boundary cases;
- every one of the 32,767 bracket strings of lengths 0 through 14; and
- 2,250 seeded strings at lengths 15, 16, 31, 32, 63, 64, 127, 128, and 255.

The exact recorded command was:

```text
python3 /audit-output/evidence/differential_test.py
```

It performed 35,041 comparisons, found zero mismatches among the prompt
expectation, independent oracle, trusted canonical, and candidate, and exited
0 (`evidence/04-differential.log`). This finite run supports, but does not
replace, the K proof or the informal universal contract argument.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/source`; no candidate `*-kompiled` directory, cache, Python
bytecode, or KORE crash archive was copied. The initial scratch manifest and
tool versions are in `evidence/05-toolchain.log`. The independent toolchain was
K v7.1.293.

### Fresh generated-semantics builds and execution

The concrete definition was freshly built with:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module MPY-SYNTAX --output-definition semantic-kompiled
```

It exited 0 (`evidence/06-kompile-llvm.log`). A direct `[[]]` run exited 0 and
ended with empty computation/maps and `boolVal(true)`
(`evidence/08-krun-smoke.log`).

`evidence/concrete_semantics_compare.py` then ran the fresh LLVM semantics on 12
normal and boundary inputs, including empty input, both single characters,
partial matches, `[[]]`, the difficult documented negative example, and noisy
positive inputs. For every case it records the exact nested `krun` command and
exit status and compares K with both Python implementations. All 12 `krun`
commands exited 0 and all 12 results agreed; the driver exited 0
(`evidence/09-concrete-semantics-compare.log`).

### Fresh proof build and all positive claims

The proof definition was freshly built with:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition verification-kompiled
```

It exited 0 (`evidence/07-kompile-haskell.log`). The candidate's complete proof
was then reconstructed with:

```text
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

It printed `#Top` and exited 0 (`evidence/10-kprove-all-positive.log`). This run
has no trusted claims and proves the four mutually dependent loop claims and
entry claim together.

For target-by-target confirmation, `evidence/spec-labeled.k` is the same five
claims with labels added and no logical change. Each target was run separately,
with the other four explicitly marked trusted only for that individual run:

| Target | Result | Evidence |
|---|---|---|
| loop state 0 | `#Top`, exit 0 | `evidence/12-kprove-loop0.log` |
| loop state 1 | `#Top`, exit 0 | `evidence/12-kprove-loop1.log` |
| loop state 2 | `#Top`, exit 0 | `evidence/12-kprove-loop2.log` |
| loop state 3 | `#Top`, exit 0 | `evidence/12-kprove-loop3.log` |
| end-to-end entry | `#Top`, exit 0 | `evidence/12-kprove-entry.log` |

The trusted labels in these five diagnostic runs are not the basis for the
verdict; the prior combined run proves all five together without trust. A
preserved `--claims loop0` experiment (`evidence/11-kprove-loop0.log`) was
interrupted because filtering removed the other mutually recursive
circularities and caused unbounded unrolling. It has no success status and is
not counted as proof evidence.

## 4. Adequacy and real-program pinning

### Claims in plain language

The four loop claims have no explicit `requires`, so their precondition is the
displayed configuration:

- computation is the real loop continuation
  `iterate("bracket", BS, loopBody)` followed exactly by the submitted
  fall-through `Return(false)`;
- the loaded function is exactly `is_nested` with `solutionBody`;
- the environment contains arbitrary bracket strings for `string` and
  `bracket`, and state is respectively 0, 1, 2, or 3; and
- no result has yet been returned.

Each claim says that executing the remaining suffix consumes the computation,
clears the function/environment maps through the real return rule, and produces
exactly `boolVal(scan(state, BS))`.

The entry claim accepts every finite `BS:BString` with empty functions,
environment, and result. It says that executing `theSolution`, then calling
`start(BS)`, consumes the computation, returns the maps to empty, and yields
exactly `boolVal(scan(0, BS))`.

### Satisfiability and ground substitutions

An entry state with `BS = lbr lbr rbr rbr .BString`, empty maps, and
`noResult` satisfies the entry precondition. Its claimed result is true, and
fresh K execution, candidate Python, and trusted canonical Python all return
true. Empty input similarly gives false; the documented difficult negative
also gives false.

Ground loop witnesses are:

| State | Remaining suffix | Claimed/executed result |
|---:|---|---|
| 0 | `[[]]` | true |
| 1 | `[]]` | true |
| 2 | `]]` | true |
| 3 | `]` | true |

For each, arbitrary `ORIG = CUR = .BString` completes a satisfying displayed
state. `evidence/14-adequacy-witnesses.log` records the substitutions and
agreement with direct suffix execution.

### Pinning to the submitted program

The submitted `solution.mpy` freshly parses to the full constructor tree in
`evidence/13-kast-submitted-program.log`. The proof-local nullary equations
expand:

1. `theSolution` to `Module(FuncDef("is_nested", Params("string"),
   solutionBody))`;
2. `solutionBody` to the submitted state initialization, `For`, and final
   false return; and
3. `loopBody` to the exact nested `If`/assignment/early-true-return tree.

This is constructor-for-constructor the parsed submitted AST. The trusted
translator identity establishes the same link back to `solution.py`. Although
`spec.k` names this AST through `theSolution` instead of opening the
`solution.mpy` file at proof time, the static equality is exact; no substituted
operation or omitted statement was found.

All program-defined statements execute under the operational rules. There is
no rule that rewrites `is_nested`, its loop, or a program expression directly
to `scan`. The result cell is fixed to `boolVal(scan(...))`; there is no
right-only existential, free result, implication-only weakening, or unchanged
wildcard.

As a separate body-sensitivity check, I changed the real early
`Return(Bool(true))` AST node to `Return(Bool(false))` in a scratch verification
copy (`evidence/verification-body-mutation.k`). The mutated definition compiled
successfully (exit 0, `evidence/16-body-mutation-kompile.log`), but the original
proof failed with `WarnStuckClaimState` and exit 1 at the state-3 loop claim
(`evidence/17-body-mutation-kprove.log`). The proof is therefore sensitive to
the material body behavior it claims.

## 5. Rule-by-rule static soundness review

`evidence/RULE_INVENTORY.md` is the exhaustive inventory. It enumerates every
local syntax/configuration declaration, function and attribute, all 30
operational rules in `semantic.k`, all 12 proof-local equations in
`verification.k`, all five claims, and the used-construct coverage map.

### Construct and state coverage

The submitted parsed program uses `Module`, `FuncDef`, parameter/string lists,
statement lists, `Assign`, `Name`, integer/Boolean/string literals, `For`, `If`,
`Compare`/`CmpOp`, integer `BinOp("+")`, and `Return`. Every one maps to a
specific syntax declaration and operational rule. Input `BString` inductively
models exactly all finite bracket-only strings. Runtime state is limited to the
computation, function map, environment map, and result, all of which are read
or written.

The rules preserve:

- module/function loading before the call;
- lookup and old-environment expression evaluation;
- left-to-right statement and loop-body order;
- one-time iterable evaluation;
- loop-variable binding to each one-character bracket string;
- integer comparison/addition and exact bracket equality;
- branch selection; and
- early return, including discarding the remaining loop/statement
  continuation and setting the result.

There is no relevant allocation, heap, I/O, exception, or nested call in the
submitted subset. K integers have the same unbounded behavior needed by the
small nonnegative automaton state.

The `For` rule prebinds its target to an empty string before `iterate`. Python
would leave a prior target binding unchanged on an empty iterable. In this
specific program the target is never read after the loop and the final return
clears the environment, so the difference cannot affect control, result, or
any claimed final cell on any intended input. Likewise, clearing the entire
function/environment maps on return is a deliberately single-call semantics
and exactly matches every theorem destination. These are limitations for reuse
as a general Python semantics, not false conclusions about the submitted
program.

### Proof extensions

The only proof-local execution terms are `loopBody`, `solutionBody`, and
`theSolution`. They are nullary, completely defined, terminating
constructor abbreviations. They do not skip execution.

`scan` is a definitional result summary, not an operational bridge. Its nine
equations are constructor-disjoint, truthful for automaton states 0–3, and
recursive equations strictly shorten the suffix. It never appears in
`semantic.k` or on an operational rule's right-hand side. Therefore its shared
presence in claims is not a circular program oracle.

There are no opaque symbols, fresh result-bearing symbols, priority rules,
`owise` rules, simplification rules, operational bridges, or task-answer rules.
No extension preempts fixed execution.

The sole coverage issue is the over-broad `[total]` declaration on
`scan(Int,BString)`: `scan(4,lbr .BString)` has no equation. I do not label any
equation unsound, because no equation has a false right-hand side and no false
conclusion witness was found. A full-configuration ground diagnostic compiled
and failed with an unmet equality, leaving `scan(4,...)` visible
(`evidence/spec-scan-gap.k`,
`evidence/15b-scan-totality-gap.log`, exit 1). The earlier unsupported
bare-functional-claim attempt is preserved in
`evidence/15-scan-totality-gap.log` (backend exit 113) and is not treated as a
candidate failure. The actual theorem starts at state 0 and the equations close
over exactly `{0,1,2,3}`, so the uncovered term is unreachable in every claim.

No materially unsound semantic or proof rule was found on the intended
program/input domain.

## 6. Fresh non-vacuity test

I did not reuse any candidate vacuity artifact. The fresh mutation is
`evidence/spec-vacuity.k`. It fixes the satisfiable input to `[[]]` and changes
the entry result obligation from the true result to `boolVal(false)`.

The mutation was first compiled without proving:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

It exited 0 and emitted KORE
(`evidence/18-vacuity-dry-run.log`). The actual proof command was:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

It exited 1 with `WarnStuckClaimState`. The residual is a fully terminated,
empty-map configuration whose actual result is `boolVal(true)`, which cannot
unify with the mutated false destination
(`evidence/19-vacuity-kprove.log`). This is the expected unmet result
obligation, not a parse error, missing import, timeout, unrelated crash, or
unreached mutation.

## 7. Proven versus assumed accounting

### Precisely established

Under the submitted `semantic.k`, imported K domains, and the five
reachability claims, the fresh trust-free `#Top` establishes:

- for every finite bracket-only `BS`, if the exact submitted program execution
  terminates from the displayed empty entry configuration, it consumes the
  computation, leaves empty function/environment maps, and returns exactly
  `boolVal(scan(0, BS))`; and
- from each real loop head with state 0–3 and the exact fall-through
  continuation, execution of the remaining suffix returns exactly
  `boolVal(scan(state, BS))`.

This is partial correctness. The audit does not promote it to a separate formal
termination theorem, even though all concrete finite executions terminate and
the operational recursion consumes the finite suffix.

### Trust ledger

| Boundary | Effect | Assessment |
|---|---|---|
| K v7.1.293 compiler, parser, Haskell/LLVM backends, and reachability kernel | All builds, executions, and `#Top` | Necessary low-level proof-system trust; acceptable. Fresh rebuilds avoid candidate binaries. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, list, and `domains.md` operations | Literals, arithmetic, comparisons, maps, generated lists | Standard fixed K primitives; acceptable. No task conclusion is hidden in them. |
| Candidate-generated `semantic.k` as a model of the used Python subset | Connects the `.mpy` AST to Python behavior | Individually audited for every used construct and concretely compared on boundaries. Acceptable for `GENERATED_SEMANTICS`, but still a manually validated semantic bridge rather than a supplied reference semantics. |
| Trusted `py2mpy.py` plus byte comparison | Connects `solution.py` to `solution.mpy` | Trusted input and exact byte identity; acceptable. |
| `theSolution`/body constructor equations | Connect proof entry to the submitted AST | Exact definitions, parsed-term comparison, and body sensitivity; formally used and acceptable. |
| `scan` equations for states 0–3 | Defines the K postcondition | Formally present, exhaustive on all theorem-reachable calls, and no operational use. The global `[total]` annotation outside these states is a documented concern. |
| Equivalence “nested valid subsequence” iff `[[]]` subsequence; `scan` recognizes it | Connects formal postcondition to English intent | Informal mathematical argument. It is compelling and independently tested but not a separate K theorem; this is the main reason for `CONCERNS`. |
| Trusted canonical and Python runtime used by differential tests | Empirical source-to-intent support | 35,041 finite comparisons with zero mismatches. Support only; not universal proof. |

There are no opaque symbols, unconstrained external primitives, fresh
result-bearing abstractions, assumed program helpers, or empirical operational
bridges.

### Exclusions and decision

The theorem excludes strings containing characters other than square brackets,
general Python programs beyond the submitted AST, general multi-call/call-stack
behavior, and a formal total-correctness guarantee. These exclusions agree with
the prompt and requested partial-correctness scope.

Gate A (real-program soundness and non-vacuity) passes. The proof executes the
exact body, constrains the result, is body-sensitive, and rejects the false
mutation. The intent and evidence bridge is adequate but partly informal, and
the `scan` totality annotation is globally broader than its equations. Those
limitations warrant `CONCERNS` but do not undermine legitimacy on the stated
domain.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
