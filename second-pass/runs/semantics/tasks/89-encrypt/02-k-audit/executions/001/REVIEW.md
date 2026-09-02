# Adversarial proof audit: 89-encrypt

The candidate is not a legitimate proof package. Fresh reconstruction does
reproduce `#Top` for both submitted claims, and a fresh false-result mutation
is correctly rejected. Those positive facts do not survive the static
soundness and program-pinning gates:

1. `verification.k:66-88` installs a priority-40 operational loop bridge over
   a broader binding/context domain than the bridge-free loop theorem proves.
   A ground intended-input witness shows that fixed semantics rejects the
   claimed result while the bridge makes the same false claim prove as `#Top`.
2. The entry claim begins with a manually preinstalled duplicate closure. Its
   `<k>` cell never loads or executes the submitted `solution.mpy` `Module` or
   `FuncDef`.
3. Independently, `solution.py` conflicts with the trusted canonical behavior
   for non-lowercase characters in the prompt's general string domain.

There was no infrastructure breach: the trusted supplied-semantics mount is
present as required, the candidate semantics tree matches it exactly, and the
K tools ran normally.

## 1. Input and provenance integrity

### Trusted/candidate comparisons

- Rendered mode is `SUPPLIED_SEMANTICS`.
  `/reference/reference-semantics/` exists, so the trusted mounts do not
  contradict the rendered mode.
- Recursive, no-symlink-dereference comparison of
  `/candidate/reference-semantics/` against the trusted tree exited 0 with no
  differences. The candidate tree has no missing, additional, changed,
  mistyped, or symlinked entry.
- `/candidate/prompt.py` is byte-identical to `/reference/prompt.py`.
- `/candidate/py2mpy.py` is byte-identical to `/reference/py2mpy.py`.
- Candidate proof/program inputs used here are regular files. The unrelated
  `/candidate/__pycache__/solution.cpython-310.pyc` cache was ignored and was
  not copied into the reconstruction.

Exact commands, file types, and statuses are in
[01_integrity.sh](evidence/01_integrity.sh) and
[01_integrity.log](evidence/01_integrity.log).

### Missing provenance artifacts

The following requested untrusted-generation artifacts are absent:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`
- any structured generation trace discoverable by the requested names or
  `.json`/`.jsonl` search

There is also no candidate `PROOF.md` or candidate `spec-vacuity.k`. These
omissions reduce provenance/auditability but did not prevent independent source
reconstruction.

### Toolchain

The independent system toolchain reported K v7.1.337 (build date 2026-06-18)
for both `kompile` and `kprove`. No candidate-built definition or cache was
used.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language and canonical contract

The trusted prompt asks `encrypt(s)` to rotate alphabet letters by
`2 * 2 = 4` positions. The trusted canonical implementation makes the domain
boundary explicit: a character in
`"abcdefghijklmnopqrstuvwxyz"` is rotated four positions modulo 26; every other
character is copied unchanged.

The candidate instead applies

```text
chr((ord(char) - 97 + 4) % 26 + 97)
```

to every character. It is correct for lowercase ASCII letters, including
wraparound, but maps uppercase, punctuation, digits, whitespace, and Unicode
characters into lowercase ASCII instead of preserving them.

### Translation fidelity

Fresh translation used the trusted command:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy
```

It exited 0, and `cmp -s` plus `diff -u` both confirmed byte identity with the
submitted `solution.mpy` (exit 0). Thus the `.mpy` file faithfully represents
the candidate Python; the error is in the candidate algorithm, not
translation.

### Independent differential evidence

[differential.py](evidence/differential.py) independently imports the trusted
canonical and generated entry points. It covers the four documented examples,
empty/boundary cases on both sides of the lowercase branch, every lowercase
string of length at most two, and 2,000 deterministic representative longer
inputs (seed 890089; 1,000 lowercase and 1,000 mixed ASCII/Unicode).

Results:

| Group | Cases | Mismatches |
|---|---:|---:|
| Documented examples | 4 | 0 |
| Empty/branch boundaries | 22 | 14 |
| All lowercase strings, length at most 2 | 703 | 0 |
| Deterministic generated inputs | 2,000 | 935 |
| Total | 2,729 | 949 |

Examples include canonical ``"`"`` versus generated `"d"`, canonical `"A"`
versus generated `"y"`, and canonical `"é"` versus generated `"k"`.
The differential command intentionally exits 1 when mismatches exist.
Commands, status, and bounded mismatch output are in
[02_fidelity.log](evidence/02_fidelity.log).

This is a material implementation/specification divergence on the intended
general-string domain. The differential run is finite evidence, not a proof;
the source-level missing `else` branch independently explains it.

## 3. Clean proof reconstruction

All candidate source inputs needed for execution were copied into
`/tmp/audit-work`. The proof reconstruction used a fresh copy of the trusted
`/reference/reference-semantics/` tree, not a candidate build output.

The concrete definition was built from source:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0. Freshly translated `concrete-tests.py` was byte-identical to the
submitted `concrete-tests.mpy`; `krun concrete-tests.fresh.mpy --definition
runtime-kompiled` exited 0 with `.K` and exit code 0.

The bridge-free proof definition and loop proof were then rebuilt/run:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module VERIFICATION \
  --output-definition verification-kompiled
kprove --definition verification-kompiled spec.k --spec-module LOOP-SPEC
```

Both commands exited 0, and `kprove` printed `#Top`.

The bridge-enabled function definition and function proof were independently
rebuilt/run:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION-WITH-LOOP \
  --syntax-module VERIFICATION-WITH-LOOP \
  --output-definition function-verification-kompiled
kprove --definition function-verification-kompiled spec.k \
  --spec-module FUNCTION-SPEC
```

Both commands exited 0, and `kprove` printed `#Top`.

The concrete compile emitted supplied-baseline warnings about several unused
non-exhaustive total functions; all builds completed. The proof builds emitted
only unused-variable warnings in fixed `strLt` rules. Full bounded outputs and
every exit status are in [03_reconstruct.log](evidence/03_reconstruct.log).

Fresh reconstruction therefore passes the dynamic-closure gate. It does not
establish that the theory used by the second proof is sound.

## 4. Adequacy and real-program pinning

### `LOOP-SPEC`

There is no explicit `requires`; the K sorts are its precondition. In plain
language, it starts:

- with `#loop(str(CS), Name("char"), encryptLoopBody)` as the entire
  computation;
- in environment location 1;
- with exact module/builtins scopes at locations 0 and -1;
- with location 1 containing only `result = str(A)`, `char = OLD`, and
  `s = str(INPUT)`, parented to location 0;
- with an empty heap.

It requires the loop computation to be consumed. The post-state keeps `s`
unchanged, sets `result` to `encryptAcc(A, CS)`, and sets `char` to the last
one-character string in `CS` (or preserves `OLD` for empty `CS`). Omitted
configuration cells are framed by K cell completion.

A concrete satisfying state is
`A = CS = INPUT = .IntSeq` and `OLD = str(.IntSeq)` with the stated maps/cells.
The post-state is identical in that empty-loop case.

### `FUNCTION-SPEC`

Again there is no explicit `requires`. It starts with
`Call(Name("encrypt"), str(CS))`, environment 0, a module scope containing a
manually preinstalled `encryptClosure`, the trusted builtins scope, fresh
scope/heap locations, empty heap/stack, `noRet`, and `NoExc`.

It requires the call to finish as exactly `str(encryptCodes(CS))`; the return is
not a free variable, tautology, implication, or unconstrained existential. A
satisfying state is obtained with `CS = .IntSeq` and the exact displayed
cells/maps.

[ground-spec.k](evidence/ground-spec.k) substitutes empty string, `"hi"`, and
`"A"` into the formal entry state. It dry-runs successfully and proves all
three ground claims as `#Top` (exit 0). The corresponding formula/generated/
canonical comparison is:

| Input | Formal | Generated Python | Canonical Python |
|---|---|---|---|
| `""` | `""` | `""` | `""` |
| `"hi"` | `"lm"` | `"lm"` | `"lm"` |
| `"A"` | `"y"` | `"y"` | `"A"` |

Commands and outputs are in [04c_adequacy.log](evidence/04c_adequacy.log).

### Failure to execute the submitted program artifact

The candidate proof never places `Module(...)`, `#loadAll(...)`, or
`FuncDef(...)` from `solution.mpy` in an entry claim. The only source occurrence
of `solution.mpy` is its regeneration at `prove.sh:4`; neither `kprove` command
consumes it. `FUNCTION-SPEC` assumes that an `encryptClosure` has already been
installed.

The macros in `verification.k:27-56` duplicate the submitted AST's body and
closure shape, so the substituted body itself is textually faithful. That
reduces but does not eliminate the gap: module loading, real `FuncDef`
execution, and the resulting binding are assumed rather than proved. This
violates the required real-program `<k>` pinning check.

The auxiliary loop claim matches the actual duplicated loop body and exact
intended local/module/builtins state. The operational rule later installed
from it does not retain those exact binding constraints, as Stage 5 shows.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[05_rule_inventory.md](evidence/05_rule_inventory.md), reproducibly generated
by [rule_inventory.py](evidence/rule_inventory.py), inventories every local
declaration in the supplied semantics, `verification.k`, and `spec.k`:

- 946 declarations total;
- 705 rules;
- 233 syntax declarations;
- five contexts;
- two reachability claims;
- one configuration.

Every row records source/line, declaration kind, attributes, classification,
and audit disposition. There are no local `[simplification]` rules and no
`[functional]` declarations. The fixed supplied baseline contains 22
`no-evaluators` opaque symbols (float operations, sorting, and MD5); none is
reachable from this program AST or influences either claim. The complete
opaque list, used-construct mapping, configuration/cell review, control and
evaluation order, calls/returns, state changes, total-function coverage, and
proof-local rule decisions are in
[05_used_constructs.md](evidence/05_used_constructs.md).

Relevant fixed rules faithfully implement module sequencing, lexical lookup,
left-to-right callee/argument evaluation, closure frames, parameter binding,
string iteration, target binding, assignment/augmented assignment, integer
arithmetic/Python modulo, `ord`/`chr`, string concatenation, and return/frame
teardown. The candidate's `encryptCode`, `encryptCodes`/`encryptAcc`, and
`lastChar` functions have exhaustive disjoint constructor cases and structural
descent. The three source macros have one expansion each and match the
submitted AST.

### Unsound operational bridge: `verification.k:66-88`

The priority-40 rule replaces the real loop whenever it sees:

- the exact location-1 local map and `env = 1`;
- an empty heap;
- but **arbitrary other scope entries** and **an arbitrary continuation**.

The displaced loop body performs binding-sensitive lookups for `ord` and
`chr` through parent scope 0 and builtins scope -1. The bridge neither matches
nor preserves those bindings. `LOOP-SPEC` proves only the narrower state with
the exact correct module/builtins scopes and no continuation.

A reviewer-authored bridge-free connection claim copies the bridge's complete
ellipsis-bearing match domain. It builds (`--dry-run` exit 0) but fails under
`VERIFICATION` (exit 1). Its residual includes paths where parent scope 0 or
`chr` is absent. See
[bridge-connection.k](evidence/bridge-connection.k) and
[04_bridge_check.log](evidence/04_bridge_check.log).

More decisively, [bridge-witness.k](evidence/bridge-witness.k) provides a ground
false-conclusion witness:

- intended input is lowercase `"a"` (code 97);
- env 1, local variables, parent relation, trusted builtins scope, and empty
  heap satisfy the rule's match;
- module scope 0 validly shadows `chr` with `builtinV("ord")`.

Under bridge-free fixed semantics, the body honors that binding, computes 101,
and reaches `applyBuiltin("ord", 101, .Vals)`. The asserted output `"e"` is
not obtained; `kprove` exits 1 with `WarnStuckClaimState` and an unmet equality.

Under `VERIFICATION-WITH-LOOP`, the candidate rule matches the identical
configuration, skips binding/call/body execution, sets the result to `"e"`,
and proves the false claim as `#Top` with exit 0. The paired exact commands and
outputs are in [04b_bridge_witness.log](evidence/04b_bridge_witness.log).

This witness uses an intended-domain input and demonstrates a concrete false
conclusion enabled by the rule. It is not merely an untested generalization.
Although the submitted entry state's particular module binding is unshadowed,
a globally false proof rule cannot be justified by calling its bad instances
off-path; its guard must be narrowed to the bridge-free theorem's domain. The
bridge is therefore materially unsound, and the function proof imports and
uses a theory containing it.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`. A fresh mutation was created in
scratch and preserved as [spec-vacuity.k](evidence/spec-vacuity.k). It uses the
same satisfiable empty-string entry state as `FUNCTION-SPEC` but changes the
required result from `str(.IntSeq)` (`""`) to
`str(iCons(120, .IntSeq))` (`"x"`).

The mutation:

1. builds/parses successfully with `--dry-run` (exit 0);
2. executes to the actual empty-string return;
3. fails the changed result obligation with `WarnStuckClaimState` (exit 1).

The residual contains `str(.IntSeq)` at the computation head, so this is the
expected reachable result mismatch, not a parser/import error, timeout, or
unrelated crash. Exact commands and output are in
[06_nonvacuity.log](evidence/06_nonvacuity.log).

The submitted entry theorem is result-constraining and non-vacuous. That does
not repair its unsound supporting theory or artifact-pinning gap.

## 7. Proven versus assumed accounting

### What the successful `#Top` establishes

Under the supplied semantics **plus the candidate's proof-local definitions
and operational bridge**, K establishes:

- the exact bridge-free loop claim for arbitrary finite `IntSeq` input and the
  exact correct module/builtins/local state in `LOOP-SPEC`; and
- a call on a manually preloaded duplicate `encryptClosure` returns the
  sequence obtained by applying `((C - 97 + 4) mod 26) + 97` to every input
  code, in `FUNCTION-SPEC`.

It does not establish that `solution.mpy` was loaded to create that closure. It
does not establish the trusted canonical behavior on general strings. Because
the second definition contains a demonstrably false operational rule, its
`#Top` is not usable as an honest proof result.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Trusted supplied MPY semantics | All concrete/proof execution | Accepted fixed semantics level; candidate tree is exactly identical. Used-path rules were statically mapped. |
| K v7.1.337 parser/compiler/backends | All dynamic results | Ordinary machine-checking trust boundary; independent fresh builds ran without infrastructure failure. |
| Trusted `/reference/py2mpy.py` | Python-to-MPY identity | Acceptable translator boundary for this audit; byte identity was re-established. |
| `encryptCode`, `encryptAcc`, `lastChar` equations | Claimed output/local summary | Acceptable defined mathematics; exhaustive, disjoint, descending, and no opaque result oracle. |
| Fixed `pyMod`, `ord`, `chr`, string/Int operations | Character computation | Acceptable selected-semantics primitives on this path; all result-affecting operations are defined, and `chr`'s guard follows from modulo 26. |
| 22 fixed opaque `no-evaluators` symbols | None | Unused; no influence on control, state, or result. |
| Macro duplicate of function/closure | `FUNCTION-SPEC` program identity | Concerning and insufficient for the required artifact pin: exact body duplication is an informal/source comparison, not execution of `solution.mpy`'s `Module`/`FuncDef`. |
| Priority-40 loop operational bridge | Closure of `FUNCTION-SPEC` | Illegitimate. It is broader than its connection claim and a ground fixed-vs-extended witness proves it can fabricate a false result/termination transition. |
| Differential comparison to canonical | Intent bridge only | Finite empirical evidence. It supports—and source inspection explains—the observed general-string divergence; it is not substituted for a K proof. |

### Decision

Fresh positive `#Top` results and a successful non-vacuity test are necessary
but not sufficient. The bridge rule makes a concrete false claim provable, and
the entry claim proves a manually substituted closure instead of executing the
submitted MPY module. Either defect blocks legitimacy; the canonical-domain
divergence is an additional material adequacy failure. This is a candidate
failure, not an audit-infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
