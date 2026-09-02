# Independent adversarial review: 138-is-equal-to-sum-even

The candidate contains a legitimate partial-correctness proof of the submitted
program for the HumanEval integer domain. I did not rely on the candidate's
`#Top`, compiled definitions, `PROOF.md`, logs, mutations, or generation report.
The positive claim was rebuilt and proved from fresh source copies, the exact
program term was mechanically pinned, all local K declarations and rules were
inventoried, and a fresh false-result claim was rejected for the intended
reason.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, problem
`138-is-equal-to-sum-even`, and condition `kit-semantics`. The required
`/reference/reference-semantics` mount is present, so the rendered mode and
trusted mounts agree.

I read `/audit-input.json` and `/audit-campaign-lock.json`; the lock is exactly
equal to the embedded `audit_campaign` object and its SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
matching the launcher record.

All required pipeline-v3 records are regular, readable, non-symlinked files:
`/run.json`, `/task.json`, `/generation-result.json`,
`invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
`codex-last.txt`, `codex-output.log`, and `prompt.txt`. Their direct SHA-256
values match the recorded values. The generation result, invocation, metrics,
runtime metrics, usage, task, and run records are internally consistent. I
parsed all 251 JSON objects in the structured trace; its single JSONL file
matches the result/invocation file hash. These records assert generation
success but were not used as proof evidence.

Independent pipeline-v3 tree hashing of the mounted candidate produces
`427cd189b301a7c544bd2c697be0618d76a1f82a23782e2ca4d1ae43f3ea82c3`,
matching both the generation result and invocation `workspace_sha256`.
Independent pipeline hashing of the trace produces
`f148abea7c0c37189ae42b1376f4be60168261e0159b29a4be45bd7d67cb8517`,
matching `usage.json`. The audit manifest also carries launcher-specific
aggregate hash fields whose construction is not declared; I therefore did not
treat those as a substitute for mounted-content inspection.

The candidate and trusted prompt are byte-identical, as are the candidate and
trusted translators. The candidate `reference-semantics/` and trusted
`/reference/reference-semantics/` trees contain the same 25 entries with
identical entry types, modes, relative paths, and file hashes. Neither tree
contains a symlink, and recursive `diff --no-dereference` exits 0. The trusted
pipeline semantics-tree digest is
`4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
matching the task and audit manifests. All six required proof deliverables are
regular files. There is no infrastructure breach.

Evidence: [provenance_check.py](/audit-output/evidence/provenance_check.py),
[01-provenance.log](/audit-output/evidence/01-provenance.log).

## 2. Program fidelity and canonical comparison

The trusted prompt asks whether `n` is representable as the sum of exactly four
positive even integers. On the intended integer domain this is equivalent to:

```text
n >= 8 and n is even
```

Necessity follows because four positive even integers are each at least 2 and
their sum is even. Sufficiency is constructive: for even `n >= 8`,
`n = 2 + 2 + 2 + (n - 6)`, and `n - 6` is a positive even integer.

The trusted canonical function returns `n % 2 == 0 and n >= 8`. The submitted
function returns `n >= 8 and n % 2 == 0`. For integer inputs the predicates are
pure and total, so reversing the conjunction does not change the result. The
prompt examples 4, 6, and 8 return false, false, and true respectively.

Using the trusted translator from the scratch copy:

```bash
python3 /tmp/audit-work/138-audit/reference/py2mpy.py \
  /tmp/audit-work/138-audit/candidate/solution.py \
  > /tmp/audit-work/138-audit/candidate/regenerated-solution.mpy
cmp /tmp/audit-work/138-audit/candidate/solution.mpy \
    /tmp/audit-work/138-audit/candidate/regenerated-solution.mpy
```

both commands exit 0. Both translated files have SHA-256
`4be6b3778909ca1c91506046bb2f1925cb4f689dad0162b5f8faa007e84eee8d`;
the submitted translation is byte-identical to trusted regeneration.

The independent differential script imports the trusted canonical and
candidate entry points. It covers the documented examples, every threshold and
parity boundary around 8, all integers from -200 through 200, four
hundred-digit boundaries, and 256 deterministic generated integers in
`[-10^30,10^30]`: 661 distinct integer cases in total. It finds zero
canonical/candidate mismatches and zero mismatches against an independently
stated contract oracle. A scalar integer function has no in-domain “empty”
case; `None` was nevertheless checked diagnostically, and both functions raise
`TypeError`. Diagnostic bool/float cases also agree but are not used to enlarge
the K theorem.

Evidence: [02-translation-fidelity.log](/audit-output/evidence/02-translation-fidelity.log),
[differential_test.py](/audit-output/evidence/differential_test.py),
[03-differential.log](/audit-output/evidence/03-differential.log).

## 3. Clean proof reconstruction

I copied only source artifacts into
`/tmp/audit-work/138-audit/candidate`. The candidate's
`runtime-kompiled/`, `verification-kompiled/`, caches, and logs were neither
copied nor referenced. K reports version 7.1.293.

The fresh Haskell proof definition was built with:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

It exits 0. `spec.k` contains exactly one positive target claim. The independent
proof command:

```bash
kprove spec.k \
  --definition fresh-verification-kompiled \
  --spec-module SPEC
```

exits 0 and prints `#Top`. This is the only positive target and therefore every
positive target closes. The only Haskell build/proof warnings are unused
variables in dormant string comparison equations.

I also freshly built the LLVM definition:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled
```

It exits 0. `krun solution.mpy` executes the real submitted module to `.K`,
installs the expected exact closure, leaves the heap and stack empty, restores
environment 0, reports `NoExc`, and has exit code 0. A reviewer-authored
translated harness checks -1,000,000, -2, 0, 4, 6, 7, 8, 9, 10, 1,000,000,
and 1,000,001; it also ends in `.K` with `NoExc` and exit code 0. LLVM's
non-exhaustiveness warnings concern only unused supplied helpers.

Evidence: [04-haskell-build.log](/audit-output/evidence/04-haskell-build.log),
[05-positive-kprove.log](/audit-output/evidence/05-positive-kprove.log),
[06-llvm-build.log](/audit-output/evidence/06-llvm-build.log),
[concrete_harness.py](/audit-output/evidence/concrete_harness.py),
[07-concrete-execution.log](/audit-output/evidence/07-concrete-execution.log).

## 4. Adequacy and real-program pinning

The sole entry claim has no `requires` or `ensures` clause. Its effective
precondition is:

- `N` is a K `Int`;
- execution begins in the complete standard initial configuration: environment
  0; empty module scope 0 whose parent is the builtins scope at -1; scope
  location 1; empty heap, call stack, and return state; `NoExc`; exit code 0.

Its postcondition is direct, not existential or implicational. It requires the
returned K Boolean to be:

```text
N >=Int 8 andBool pyMod(N, 2) ==Int 0
```

It also fixes the complete final state: the exact function closure is installed
in scope 0, the temporary call scope is gone, environment and scope allocation
are restored, heap and heap location are unchanged, stack is empty, return
state is `noRet`, exception is `NoExc`, and exit code is 0.

Mechanical constructor tokenization finds the entire submitted `solution.mpy`
as one exact contiguous subtree of the entry computation, immediately under
`#loadAll`, followed by
`Call(Name("is_equal_to_sum_even"), Int(N))`. The submitted translation has 66
constructor tokens and occurs exactly once at the expected claim offset. This
is not a source filename indirection: the claim executes the actual module,
definition, body, lookup, argument, and call.

A concrete satisfying state is the listed initial configuration with `N = 8`.
Substitution gives `true`; both Python implementations return `True`. Ground
substitutions at -2, 7, 8, 9, and 10 all agree among the formal expression,
canonical function, and submitted function. The separately authored body
sensitivity probe changes the body inside the actually executed `FuncDef` to
`return False`; at input 8 it reaches residual `false` and cannot prove a
`true` destination. Thus the theorem is sensitive to the body it executes.

The integer domain is the material HumanEval domain: parity and “positive even
integer summands” define an integer property, and every prompt example and the
canonical implementation use that domain. The theorem does not claim behavior
for arbitrary Python objects or floating-point values; this is not a material
narrowing of the source contract.

Evidence: [adequacy_pinning.py](/audit-output/evidence/adequacy_pinning.py),
[08-adequacy-pinning.log](/audit-output/evidence/08-adequacy-pinning.log),
[reviewer-body-sensitivity.k](/audit-output/evidence/reviewer-body-sensitivity.k),
[11-body-sensitivity.log](/audit-output/evidence/11-body-sensitivity.log).

## 5. Rule-by-rule static soundness review

I inventoried the supplied root semantics, every imported helper K file,
`verification.k`, and `spec.k`. The exhaustive inventory contains 929 items:
227 syntax declarations, 695 rules, five contexts, one configuration, and the
one target claim. It enumerates all function and total declarations, all 29
priority rules, all 28 `owise` rules, all 33 concrete-only rules, and every
opaque symbol. There are no simplification rules and no `[functional]`
declarations.

`verification.k` merely imports `MPY`; it declares no syntax, function,
totality assertion, opaque symbol, priority rule, semantic rule,
simplification, bridge, lemma, or auxiliary claim. `spec.k` contributes only
the proof goal. Consequently there is no candidate-local theory extension
capable of smuggling the task answer.

The 77 target-reachable supplied items implement this path:

```text
#loadAll(Module(FuncDef(...)))
  -> bind exact closure in scope 0
  -> look up and call it
  -> evaluate Int(N), allocate temporary scope 1, bind n
  -> evaluate n >= 8
  -> short-circuit or evaluate pyMod(n,2) == 0
  -> Return / #pop
  -> exact Boolean and restored complete state
```

Grammar and contexts preserve left-to-right evaluation. Target-reachable
overlaps are constructor- or guard-disjoint: cell-aware priority rules cannot
apply because the ordinary frame has no `"$cells"` marker; annotated and plain
closures are different constructors; Boolean `and` guards are complementary;
integer operator equations are operator-disjoint. The modulo divisor is the
fixed nonzero positive integer 2, so
`pyMod(N,2) = ((N %Int 2) +Int 2) %Int 2` is defined and agrees with Python
modulo for every integer. It is a fully defined supplied function, not a fresh
or opaque result-bearing oracle. No used operation allocates, outputs, raises,
loops, or invokes an unmodeled construct.

The other 851 items are unreachable from the submitted module for every
`N:Int`: 177 are dormant declarations, 619 are dormant operational rules, 33
are LLVM-only concrete rules, and 22 are named opaque boundaries. The opaque
symbols are float operations, `sortVS`, `sortKeyVS`, and `md5hexCodes`; none
occurs in the program, claim, path condition, or postcondition.

The supplied partial language has broader limitations, recorded rather than
hidden: `valSeqAt` is underspecified out of bounds; broad string `encode` and
multi-character `int(str)` rules omit some CPython error behavior; bool is not
modeled as an `int` subclass by `isIntV`; and symbolic float, sort, and MD5
operations are opaque. Concrete witnesses such as `"A".encode("utf-16")` and
`int("aa")` demonstrate the limits of those dormant rules. They are not
false-conclusion witnesses for this theorem because no intended input can make
the real submitted body construct or reach them. No task answer, skipped
property-bearing computation, or unconstrained result is present in the
target-reachable rules.

Evidence: [rule_inventory.py](/audit-output/evidence/rule_inventory.py),
[rule-inventory.md](/audit-output/evidence/rule-inventory.md),
[09-rule-inventory-command.log](/audit-output/evidence/09-rule-inventory-command.log),
[static-review.md](/audit-output/evidence/static-review.md).

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The fresh
`REVIEWER-FALSE-SPEC.false-result-at-eight` claim executes the exact submitted
module and exact body at the satisfying input 8, but changes the
result-constraining destination from the correct `true` to `false`.

First:

```bash
kprove reviewer-false-spec.k \
  --definition fresh-verification-kompiled \
  --spec-module REVIEWER-FALSE-SPEC \
  --dry-run
```

exits 0, establishing that the mutation parses and builds. The actual proof
command without `--dry-run` exits 1 with `WarnStuckClaimState`. Its residual is
`<k> true ~> .K </k>` in the otherwise expected final state, while the
destination demands `false`. This is the expected unmet result obligation, not
a parse failure, missing import, timeout, crash, or unreachable mutation.

The independent body-sensitivity mutation likewise builds with dry-run exit 0
and fails with proof exit 1, residual `<k> false ~> .K </k>`, after executing
the changed body. Both wrapper checks exit 0 only because they explicitly
require the inner proof command to exit nonzero.

Evidence: [reviewer-false-spec.k](/audit-output/evidence/reviewer-false-spec.k),
[10-false-mutation.log](/audit-output/evidence/10-false-mutation.log),
[11-body-sensitivity.log](/audit-output/evidence/11-body-sensitivity.log).

## 7. Proven versus assumed accounting

What is machine proved: under the supplied `MPY` semantics, starting in the
claim's concrete initial state, loading the exact regenerated module and
calling its exact bound function with any K integer `N` reaches the complete
final state with returned Boolean
`N >=Int 8 andBool pyMod(N,2) ==Int 0`. The proof executes every
property-bearing source operation. This is a partial-correctness reachability
statement; no separate resource bound or general theorem about all Python
objects is claimed.

Trust and assumption ledger:

| Boundary | Effect on theorem | Assessment |
|---|---|---|
| K 7.1.293 parser, kompiler, Haskell backend, solver, and builtin Int/Bool/Map theories | Implements and checks all K rewriting and arithmetic | Standard unavoidable proof-tool trust; fresh rebuild, successful positive proof, and discriminating negative proofs support correct use |
| Supplied `MPY` semantics | Defines module load, scoping, calls, returns, Boolean control, comparison, and modulo | Exact trusted-tree integrity established; every target-reachable rule statically checked and dynamically exercised; unused partial-language limits explicitly excluded |
| Trusted `py2mpy.py` | Maps `solution.py` to the K constructor program | Submitted `solution.mpy` is byte-identical to trusted regeneration, and the claim's executed constructor subtree is mechanically identical |
| Trusted prompt and canonical implementation | State intent and the reference behavior | Candidate matches the canonical on the full formal integer formula; 661 finite cases are corroboration, not a proof substitute |
| Elementary integer argument connecting parity/lower bound to four positive even summands | Connects the formal Boolean to the natural-language property | Ordinary complete mathematical argument: necessity by parity/minimum; sufficiency by `2+2+2+(N-6)` |
| CPython and reviewer differential/concrete tests | Empirical cross-checks only | Finite evidence; not imported into K and not used instead of the universal reachability proof |

The 22 supplied opaque symbols and the compiler's dormant totality warnings
have no dependent target claim. There is no proof-local primitive, empirical
bridge, program summary, circular abstraction, or informal claim that the
source body executed when it did not. The source-to-property bridge is
supported both by exact canonical agreement and the elementary universal
integer argument.

Decision: the clean proof closes, is non-vacuous and result-constraining, pins
the real regenerated program, covers the unrestricted intended integer domain,
and uses no materially unsound target rule or proof extension. The appropriate
benchmark decision is `PASS / LEGIT`.

VERDICT: PASS
LEGITIMACY: LEGIT
