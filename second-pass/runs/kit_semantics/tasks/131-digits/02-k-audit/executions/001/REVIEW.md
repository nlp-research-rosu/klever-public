# Independent adversarial review: HumanEval 131 `digits`

This audit followed the mandated `using-kit` then `validating-proof` workflow.
Candidate prose, compiled definitions, logs, traces, and prior `#Top` results
were treated only as untrusted claims. All executable artifacts were copied to
`/tmp/audit-work`, and both definitions were rebuilt from source.

## 1. Input and provenance integrity

Outcome: pass; no infrastructure breach.

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and a mounted trusted semantics. Every
required pipeline-v3 record was present, readable, regular (or a directory
where required), and not a symlink:

- `/run.json`, `/task.json`, `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one-file structured trace tree under
  `/generation-evidence/codex-trace/`;
- the trusted prompt, canonical implementation, translator, and semantics;
- the candidate mount and all six required proof deliverables.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`, whose file hash is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
All launcher-recorded direct file hashes independently matched, including both
manifests, all generation records, prompt, canonical, translator, and campaign
lock. The trace contains 458 valid JSONL records; its raw file hash
`31dcd9e53468a9111fe8875ae4cdeb9c9b3b8e147ac08ff7b139cba273897746`
matches both `invocation.json` and `generation-result.json`.

The historical records say generation succeeded and claimed validation. Those
claims were not used below. The historical run's Kit revision differs from the
later audit-campaign Kit revision; these are separately identified generation
and audit environments, and the required audit campaign block/lock itself
matches.

The candidate prompt and translator are byte-identical to their trusted mounts.
Most importantly for `SUPPLIED_SEMANTICS`, an independent recursive inventory
found exactly 25 entries in each semantics tree and equal path, file type, and
file content for every entry. There are no missing, additional, mistyped, or
symlinked entries. Evidence and the exact checks are in
[`provenance_check.log`](evidence/provenance_check.log) and
[`provenance_check.py`](evidence/provenance_check.py).

## 2. Program fidelity and candidate-versus-canonical checks

Outcome: pass.

The trusted prompt's contract is: for a positive integer `n`, return the product
of its odd decimal digits, or zero if it has no odd decimal digit. The examples
are `digits(1)=1`, `digits(4)=0`, and `digits(235)=15`. The trusted canonical
implementation converts `n` to decimal text, multiplies odd characters, and
tracks whether any were found.

The candidate uses repeated quotient/remainder instead. At each iteration it
tests `n % 2`, multiplies by `n % 10` on the odd branch, then executes
`n // 10`. This is equivalent for positive integers because an integer and its
last base-10 digit have the same parity.

Running the trusted `/reference/py2mpy.py` on the scratch copy of `solution.py`
produced a byte-identical `solution.mpy`; both files hash to
`fa4e9b547ee6a1a238a203ec3c101b8ac51b6ee014c73f182c0dd5442f726571`.

The auditor-authored differential test imports the trusted canonical entry
point and the scratch candidate entry point. It preserved and checked 30,162
positive integers: all values 1 through 25,000; every prompt example; branch
and decimal-length boundaries; powers of ten plus/minus one through 120 decimal
places; all-even and mixed-digit cases; and 5,000 deterministic generated
values. Both final-digit branches and both contract-result classes were
exercised. There were zero intended-domain mismatches.

`n=0` also agreed at zero. For `n=-1`, the canonical raises `ValueError` while
the candidate returns zero; negative inputs are expressly outside the
positive-integer source contract and are not a domain narrowing. Exact commands,
statuses, scope, and preserved inputs are in
[`fidelity_checks.log`](evidence/fidelity_checks.log),
[`differential_test.py`](evidence/differential_test.py), and
[`differential_inputs.txt`](evidence/differential_inputs.txt).

## 3. Clean proof reconstruction

Outcome: pass.

No candidate-provided compiled directory or cache was reused. K 7.1.293 built
the following fresh definitions solely from the scratch source and trusted-
identical supplied semantics:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/rebuilt-runtime-kompiled
```

This exited zero. The auditor-generated concrete program then ran with `krun`
and terminated with `.K`, `NoExc`, exit code zero, an empty heap/stack, and
results `1, 0, 1, 15, 0, 945, 15` for `1`, `4`, `10`, `235`, `2468`, `97531`,
and a 40-digit boundary case. See
[`kompile_llvm.log`](evidence/kompile_llvm.log) and
[`krun_concrete.log`](evidence/krun_concrete.log).

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition /tmp/audit-work/rebuilt-verification-kompiled
```

This also exited zero. The loop claim selected independently printed `#Top` and
exited zero. The submitted positive proof unit is the complete `SPEC` module:

```text
kprove spec.k \
  --definition /tmp/audit-work/rebuilt-verification-kompiled \
  --spec-module SPEC
```

It selects both `digits-loop` and `digits-entry`, printed `#Top`, and exited
zero. Exact outputs are in
[`kompile_haskell.log`](evidence/kompile_haskell.log),
[`kprove_digits_loop.log`](evidence/kprove_digits_loop.log), and
[`kprove_all_fresh.log`](evidence/kprove_all_fresh.log).

As a diagnostic, selecting only `SPEC.digits-entry` omitted the auxiliary loop
circularity and remained compute-bound until interrupted; it is not the
candidate's target command and is not counted as success or failure. K proves
the entry and its loop invariant together in the successful all-claims unit.
The diagnostic is recorded in
[`kprove_entry_only_diagnostic.md`](evidence/kprove_entry_only_diagnostic.md).
Compiler warnings concerned non-exhaustive helpers in unused supplied modules
and unused variables; no warning concerned a constructor on this program path.

## 4. Adequacy and real-program pinning

Outcome: pass.

### Formal claims in plain language

`digits-loop` assumes `N >= 0`, arbitrary integer accumulated product `P`, and
a presence bit `F` equal to zero or one. From the exact real `#while` head and
body, it states that:

- local `n` becomes zero;
- local `product` becomes `P * oddDigitsProduct(N)`;
- local `found` becomes the Boolean union
  `F + oddDigitSeen(N) - F*oddDigitSeen(N)`;
- the active continuation, unrelated scopes, and unrelated cells are framed.

This precondition is satisfiable, for example with
`N=0, P=7, F=0, L=1` and a local scope containing
`n=0, product=7, found=0`.

`digits-entry` assumes an arbitrary mathematical integer `N > 0` and the
complete normal initial module configuration: environment zero, builtins scope,
fresh scope counter one, empty heap/stack, `noRet`, `NoExc`, and exit code zero.
It loads a `digits` binding, calls it normally, and constrains the returned
`<k>` value to
`oddDigitsProduct(N) * oddDigitSeen(N)`. The final normal-state cells are also
constrained; only the post-load global map is existential because it contains
the installed function. `N=1` with the displayed initial cells is a concrete
satisfying state.

### Exact submitted-program identity

Trusted regeneration first established source-to-`solution.mpy` identity. An
independent balanced-constructor extractor then compared the regenerated
`Module(...)` against the `Module(...)` inside the entry claim. After removing
only four explicit `.Stmts` associative-list units—which the translator omits
as syntax identities—both sides contain the same 173 constructor tokens and
the same normalized hash
`885987b46113cd575903eba1b9be8ea79f4398b7a3f72ae561c1ac3570815712`.
Thus the claim executes the submitted function binding and exact body, not a
substituted implementation. See
[`program_pinning_check.log`](evidence/program_pinning_check.log) and its
[`script`](evidence/program_pinning_check.py).

The entry computation includes `#loadAll`, name lookup, argument evaluation,
closure dispatch, parameter binding, all assignments and loop iterations,
return, and frame pop. There is no operational bridge over any of them.

Concrete substitutions `N=1,4,10,235,2468,97531` and a 40-digit positive
integer gave equal values from the formal summary, trusted canonical, and
candidate implementation. The fresh body-sensitivity probe in stage 6 changes
the constructor term actually executed, not an external source file.

## 5. Rule-by-rule static soundness review

Outcome: pass.

The exhaustive source inventory contains 942 items: 695 fixed-semantics rules,
ten proof-local rules, 229 syntax declarations, five contexts, one
configuration, and two claims. Each item is enumerated by file/line with its
attributes, complete normalized statement, and review decision in
[`k_rule_inventory.txt`](evidence/k_rule_inventory.txt). The grouping rationale
is in [`static_rule_review.md`](evidence/static_rule_review.md), and every used
constructor is mechanically mapped to declarations and rules in
[`used_construct_map.md`](evidence/used_construct_map.md).

### Used supplied-semantics path

The relevant rules are in `syntax.k`, `core.k`, `operators.k`, `int.k`,
`controls.k`, `functions.k`, and `call.k`:

- syntax strictness and contexts enforce RHS-first assignment, left-to-right
  binary operands and call arguments, and condition-first `If`/`While`;
- `#loadAll` and statement sequencing install and execute the real module;
- scope lookup selects the installed closure and local integers;
- the call rules push a frame, bind `n`, execute the body, and restore state;
- integer literals, comparisons, multiplication, Python remainder, and floor
  division implement every material operation;
- while rules preserve the body/continuation cycle and false-condition exit;
- return sets the returned integer and pops the frame normally.

The program mutates only its three local bindings plus temporary call-control
cells. It neither allocates nor dereferences heap objects. Divisors are the
fixed nonzero constants two and ten.

There are 45 priority-bearing fixed rules. Ref/cell priorities cannot match
because the program carries integers and its unannotated frame lacks the
`"$cells"` marker. Specialized call priorities for math/hashlib/sort/collections
do not match `Call(Name("digits"), ...)`. The static check also confirms
`MPY-CONCRETE` is absent from the proof definition while present in the fresh
LLVM definition; see [`static_checks.log`](evidence/static_checks.log).

The fixed semantics has 22 explicit `no-evaluators` symbols:
`md5hexCodes`, `sortVS`, `sortKeyVS`, and the float symbols
`intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
`addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
`intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`. The concrete-only
`floorFI`, `toF`, and `ceilF` are likewise symbolic on proof inputs. None occurs
in the program, claims, or proof-local rules; none influences a branch, cell,
or result. There are no local `functional` declarations.

Unused supplied-subset rules were checked for overlapping extensible heads and
priorities. Operand/callee constructors and guards keep them off this integer
program path. No rule can enable a concrete false conclusion for this program
on a positive input, so there is no unsound-rule witness to report.

### Proof-local inventory

`verification.k` contains no `<k>` rule, priority, `owise`, concrete rule,
opaque symbol, or operational bridge. It adds only:

1. `oddDigitsProduct`, with disjoint rules for `N<=0`, positive odd parity, and
   positive even parity;
2. `oddDigitSeen`, with the same exhaustive partition;
3. four simplifications: `1*X=X`, `X*1=X`, `(X+1)-X=1`, and multiplication
   associativity.

For positive `N`, Python remainder modulo two is exactly zero or one, so each
summary's guards are exhaustive and non-overlapping. Let
`r = pyMod(N,10)` and `q=(N-r)/10`. Then `N=10q+r`,
`0<=r<10`, and `q<N`; recursion therefore descends to zero. Because `10q` is
even, `N` and final digit `r` have the same parity. The product function
multiplies exactly odd `r` values; the presence function is one exactly when an
odd digit occurs. This also supplies the universal summary-to-contract bridge,
not merely finite testing. All four simplifications are true over mathematical
integers, and overlapping applications agree.

`digits-loop` is an auxiliary reachability circularity over the exact loop, not
an ordinary rewrite injected into execution. It makes semantic progress before
reuse. `digits-entry` depends on it, but no bridge or shared oracle makes that
dependency circular at the value level.

## 6. Fresh non-vacuity test

Outcome: pass.

The candidate's mutation files were not reused. The auditor authored
[`audit-spec-vacuity.k`](evidence/audit-spec-vacuity.k), which executes the exact
submitted body on satisfying input `235` but changes the required result from
15 to 16.

- `kprove ... --dry-run` exited zero, establishing successful parsing/build.
- The actual proof exited one with `WarnStuckClaimState`.
- The residual normal configuration contains `<k> 15 ~> .K </k>`, directly
  exposing the unmet false result 16.

The exact logs are
[`audit_vacuity_dry_run.log`](evidence/audit_vacuity_dry_run.log) and
[`audit_vacuity_failure.log`](evidence/audit_vacuity_failure.log).

An additional independent body-sensitivity mutation changes the executed
product update from `*` to `+`. On input 3 it retains the original expected
result 3. It also built successfully and then failed with
`WarnStuckClaimState`, leaving actual `<k> 4 ~> .K </k>`. This demonstrates
that changing the body term changes the theorem's execution rather than being
bypassed. See
[`audit-spec-body-sensitivity.k`](evidence/audit-spec-body-sensitivity.k),
[`audit_body_dry_run.log`](evidence/audit_body_dry_run.log), and
[`audit_body_failure.log`](evidence/audit_body_failure.log).

## 7. Proven versus assumed accounting

Outcome: Gates A, B, and C pass.

### What is formally proven

Under the supplied `MPY` semantics and proof-local mathematical equations, the
two-claim reachability proof establishes partial correctness for every
mathematical integer `N>0`: if execution reaches a terminating result, loading
and calling the exact submitted `digits` body returns
`oddDigitsProduct(N)*oddDigitSeen(N)` normally, with the specified control and
state cells restored. The exhaustive equations and base-10 argument above show
that this value is precisely the product of all odd decimal digits, or zero
when there are none. There is no size, digit-count, example-only, or unrolling
bound.

The theorem is partial correctness. It does not separately assert a termination
theorem, although concrete positive executions terminate by repeated division
by ten.

### Trust ledger

| Boundary | Dependents and assessment |
|---|---|
| Trusted supplied `reference-semantics` | Defines value, binding, control, and state behavior for both claims. Its candidate copy is recursively identical to the trusted mount. The exact used subset was statically reviewed and concretely reconstructed; acceptable for `SUPPLIED_SEMANTICS`. |
| K 7.1.293 parser/compiler, Haskell backend, reachability/circularity implementation, SMT support, and integer builtins | Required for the machine-checked `#Top` and arithmetic discharge. This is the ordinary proof-tool trust boundary; acceptable. |
| LLVM backend | Used only for independent concrete reconstruction, not for symbolic proof validity; acceptable corroboration. |
| Trusted `py2mpy.py` and CPython AST parsing | Connect `solution.py` to the constructor program. Byte identity and constructor-level claim comparison make this bridge auditable; acceptable. |
| `oddDigitsProduct`, `oddDigitSeen`, and four simplifications | Not assumed or opaque: exhaustive equations and ordinary integer equalities fix their values. Both claims depend on them; statically valid. |
| Base-10 interpretation | The quotient/remainder/parity induction is an explicit ordinary-mathematics bridge from summaries to the natural-language contract. It is universal, not inferred from testing; acceptable. |
| Opaque float/sort/md5 and concrete-only symbols | No dependent claim and no reachable occurrence. They do not affect this theorem. |
| Trusted canonical Python | Used only as an independent finite differential oracle and concrete substitution check. It is not a premise of the K proof and does not substitute for it. |

Finite differential testing supports implementation-to-intent alignment and
the source/semantics bridge on its recorded inputs only. The successful K proof,
static summary argument, and negative probes supply the universal theorem,
rule validity, and discrimination evidence.

The proof is sound, result-constraining, non-vacuous, pins the real generated
program, and covers the full stated positive-integer HumanEval domain. No
material adequacy or trust-boundary limitation remains.

VERDICT: PASS
LEGITIMACY: LEGIT
