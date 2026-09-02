# Independent adversarial review: 79-decimal-to-binary

The candidate contains a legitimate unbounded partial-correctness proof for
the material HumanEval contract: every nonnegative integer input that
terminates returns its ordinary base-2 digits between the two literal `db`
wrappers. I rebuilt both definitions from source, proved the loop circularity
and the complete two-claim target from a clean scratch tree, mechanically
matched the inline closure to the submitted translated program, reviewed the
complete local K rule inventory, and rejected a fresh reachable false result.

## 1. Input and provenance integrity

The launcher record declares `record_layout = pipeline-v3`,
`semantics_mode = SUPPLIED_SEMANTICS`, problem
`79-decimal-to-binary`, and condition `kit-semantics`. The trusted
`/reference/reference-semantics` mount is present, as required for this mode.
There is no rendered-mode/mount contradiction.

I used the launcher-provided `container_paths`, not the host provenance paths.
All required pipeline-v3 records are real readable regular files:

- `/run.json`, `/task.json`, and `/generation-result.json`;
- `invocation.json`, `metrics.json`, `runtime-metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`;
- the one structured trace JSONL file below `codex-trace/`.

Every recorded evidence-file hash, run/task/result hash, canonical hash,
prompt hash, translator hash, and campaign-lock hash matched the independently
read mounted bytes. The audit-campaign lock JSON is exactly equal to the
`audit_campaign` object in `/audit-input.json`. All 636 structured trace
records parsed as JSON, and the trace tree hash matched `usage.json`.
Generation claims were not used as proof evidence.

Using the pipeline-v3 tree algorithm, the mounted candidate hashes to
`178c3afda295cbdf3074cb0a38f0283e8eac8423d58546005baf8c7168b3742a`,
exactly the `outputs.workspace_sha256` in `/generation-result.json`. The
separate launcher packaging digest recorded as `candidate_tree_sha256`
(`94610b...`) is a different recorded digest scheme and was not conflated
with the pipeline-v3 tree hash.

The supplied-semantics integrity boundary passed:

- candidate and trusted trees have the same 25 entries;
- corresponding entry types and bytes are identical;
- neither tree contains a symlink or unsupported entry;
- both have the pipeline tree hash
  `4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f`,
  matching the task manifest;
- candidate `prompt.py` and `py2mpy.py` are byte-identical to the trusted
  mounts.

Evidence:
[`01-integrity.log`](evidence/01-integrity.log),
[`check_integrity.py`](evidence/check_integrity.py),
[`01-generation-records.log`](evidence/01-generation-records.log), and
[`inspect_generation.py`](evidence/inspect_generation.py).

Stage 1 result: PASS. There is no audit-infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The trusted prompt asks for the ordinary binary representation of a decimal
number, with every middle character equal to `0` or `1`, and literal `db`
prefix and suffix. The trusted canonical implements
`"db" + bin(decimal)[2:] + "db"`.

The coherent material domain is the nonnegative integers, including zero.
For a negative Python integer, the canonical's `[2:]` expression itself
produces a non-binary middle character and conflicts with the prompt's explicit
digit-only postcondition. Negative integers therefore are not silently removed
from a valid stated behavior; they are outside the natural-number contract
expressed jointly by the prose and canonical algorithm. Non-integers are also
outside Python `bin`'s input contract.

The submitted implementation initializes a trailing `db`, handles zero
explicitly, repeatedly prepends `chr(48 + n % 2)`, replaces `n` by `n // 2`,
and finally prepends the leading `db`. It is a different but faithful
algorithm on that entire unbounded domain.

The trusted translator regenerated `solution.mpy` byte-for-byte. Both files
have SHA-256
`894932ade6d0d81345caabdb1fc621bb668b7816d2d7aef5a0b3df54e4118e65`.

The independent differential test imported the trusted canonical and submitted
entry points under separate module names. It checked:

- the documented examples `15` and `32`;
- zero and both branch/loop boundaries (`0`, `1`, `2`, and nearby values);
- every integer from `0` through `4096`;
- `2**k - 1`, `2**k`, and `2**k + 1` for `k = 0..1024`;
- 2,000 deterministic generated nonnegative integers up to 1,024 bits.

There were 9,110 unique cases and zero mismatches. An “empty” input is not
defined for this scalar-integer API.

Evidence:
[`02-fidelity.log`](evidence/02-fidelity.log),
[`differential.py`](evidence/differential.py), and
[`run_fidelity.sh`](evidence/run_fidelity.sh).

Stage 2 result: PASS.

## 3. Clean proof reconstruction

I copied only the candidate proof/program source files and the trusted
translator, prompt, canonical, and supplied-semantics tree to
`/tmp/audit-work/79-audit/source`. No candidate `*-kompiled` directory,
cache, or generated backend artifact entered scratch.

The active tools report K version `7.1.293`. From source, I built:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition fresh-runtime-kompiled

kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition fresh-verification-kompiled
```

Both builds exited 0. A reviewer-authored six-case concrete program, whose
function AST was mechanically checked equal to `solution.py`, executed under
the fresh LLVM definition with final `.K`, `NoExc`, exit code 0, and `krun`
exit 0.

The loop circularity was independently selected:

```text
kprove spec.k --definition fresh-verification-kompiled \
  --spec-module SPEC --claims SPEC.binary-loop
```

It exited 0 and printed `#Top`.

The submitted positive target is the two-claim dependency set: the entry claim
uses `SPEC.binary-loop` as its circularity. Its clean invocation was:

```text
kprove spec.k --definition fresh-verification-kompiled --spec-module SPEC
```

It exited 0 and printed `#Top`, establishing closure of both claims. As an
additional diagnostic, selecting only `SPEC.decimal-to-binary` deliberately
removed its helper circularity and did not finish before the reviewer
interrupted it; that is not the submitted proof dependency graph and is not
counted as a failed positive claim.

Evidence:
[`03-prepare-scratch.log`](evidence/03-prepare-scratch.log),
[`03-fresh-build.log`](evidence/03-fresh-build.log),
[`03-concrete-witness.log`](evidence/03-concrete-witness.log),
[`03-prove-binary-loop.log`](evidence/03-prove-binary-loop.log), and
[`03-prove-all.log`](evidence/03-prove-all.log). The bounded selector
diagnostic is documented in
[`03-prove-target.log`](evidence/03-prove-target.log).

Stage 3 result: PASS.

## 4. Adequacy and real-program pinning

### `SPEC.binary-loop`

Plain-language precondition: the control is at the exact submitted `#while`
term; environment 1 is a plain local scope containing string accumulator
`ACC` and integer `N`; the module and builtins scopes, allocators, empty heap,
return state, exception state, and exit code have the shown values; the stack
and continuation are preserved; and `N >= 0`.

Postcondition: the loop continuation is reached with `decimal = 0` and
`binary = str(OUT)`, where `binRel(N, ACC, OUT)` holds. The relation performs
the same remainder/prepend/floor-divide recurrence as one loop iteration.

A satisfying ground state is:
`N = 5`, `ACC = [65]`, empty heap, environment 1, scope location 2,
empty stack, `noRet`, `NoExc`, and exit code 0. The unique related output is
the code sequence `[49, 48, 49, 65]`.

### `SPEC.decimal-to-binary`

Plain-language precondition: call `decimal_to_binary(N)` in the exact module
scope shown in the claim; the binding is the submitted closure with parameter
`decimal` and the complete submitted body; builtins are the fixed supplied
builtins; all other state cells are their clean initial values; and `N >= 0`.

Postcondition: the call has returned `str(CODES)`, all caller state is restored,
and `decimalResultRel(N, CODES)` holds. This relation requires the leading code
pair `[100,98]` (`db`), the exact repeated-division digit sequence (with a
separate `0` case), and the trailing `[100,98]`.

A satisfying ground state is the displayed initial state with `N = 0`.
The postcondition uniquely gives codes `[100,98,48,100,98]`, or `db0db`.

The claim executes a real `Call(Name("decimal_to_binary"), ...)`; it does not
start after the program's work. A mechanical constructor-level comparison
removed comments/whitespace and normalized only the translator's omitted empty
`If` else to explicit `.Stmts`. The parameter name matched and all 167
normalized body tokens were identical between `solution.mpy` and the closure
inside `spec.k`. Thus the claim pins the submitted function body, not a
substitute.

Concrete substitutions `0`, `1`, `2`, `15`, `32`, and `2**256 + 1` produced
the same unique relation value in the trusted canonical and submitted Python
implementations. There is no free result variable: `?CODES` is existential on
the right but is constrained by a total, deterministic structural relation.

The inline claim term is maintained manually rather than regenerated
automatically. Under the immutable candidate this is an artifact-maintenance
observation, not an adequacy failure, because trusted regeneration plus the
mechanical constructor comparison establishes identity.

Evidence:
[`04-adequacy-pinning.log`](evidence/04-adequacy-pinning.log) and
[`adequacy_and_pinning.py`](evidence/adequacy_and_pinning.py).

Stage 4 result: PASS.

## 5. Rule-by-rule static soundness review

The exhaustive inventory contains 941 entries:

- 703 rules: 695 supplied operational/equational rules and 8 proof-local
  equations;
- 230 syntax declarations: 227 supplied and 3 proof-local;
- 5 contexts, 1 configuration, and the 2 positive claims.

Every inventory row records file, line, complete normalized declaration,
attributes, target-path relevance, decision, and rationale. The complete
rule-by-rule artifact is
[`05-rule-inventory.tsv`](evidence/05-rule-inventory.tsv). The supporting
target-path and overlap analysis is
[`05-static-review.log`](evidence/05-static-review.log).

### Proof-local inventory

`verification.k` adds no syntax for program expressions/statements or K
control, no `<k>` rewrite, operational bridge, priority, simplification,
`anywhere` rule, opaque symbol, or no-evaluator symbol. It adds only:

1. `binRel(Int, IntSeq, IntSeq) [function,total]`:
   - `N = 0` requires structural equality of accumulator and output;
   - `N > 0` recurs with quotient `(N - pyMod(N,2))/2` and prepends
     `48 + pyMod(N,2)`;
   - `N < 0` is false.
2. `decimalTailRel(Int, IntSeq) [function,total]`:
   - zero fixes `0db`;
   - positive inputs invoke `binRel` from trailing `db`;
   - negative inputs are false.
3. `decimalResultRel(Int, IntSeq) [function,total]`:
   - a leading `db` exposes the tail relation;
   - the `[owise]` complement is false.

The sign guards are pairwise disjoint and exhaustive. The
prefix/`owise` cases are complementary. For every positive `N`,
`pyMod(N,2)` is 0 or 1 and the recursive quotient is a nonnegative integer
strictly below `N`; the equations terminate and are consistent. These are
truthful definitional summaries. They do not replace program execution.

### Used supplied-semantics path

Every constructor used by `solution.mpy` is declared and has a real execution
path:

| Program construct | Material supplied rules |
|---|---|
| module/statements/names/literals | `syntax.k`; `core.k` loading, sequencing, lookup, literals |
| assignment, `if`, `while` | `controls.k` plain assignment, branching, repeated guard evaluation, loop label |
| call/arguments/frame/return | `call.k` callee-then-left-to-right-arguments routing and closure frame; `functions.k` binding, return, pop |
| integer `+`, `%`, `//`, `==`, `!=` | `operators.k` dispatch; `int.k` Python remainder and floor quotient |
| strings and concatenation | `str.k` ASCII literal conversion and structural concatenation |
| `chr` | builtins lookup plus `builtins.k` guarded singleton-string result |

The exact scopes in both claims are plain scopes without `$cells`, so
cell-reference priority rules cannot overlap. The values on this path are
integers and strings, not heap references, excluding heap-dereference
priorities. The only direct special `Call` rules are for `math.*` and
`hashlib.md5`; neither overlaps either `Call(Name("decimal_to_binary"),...)`
or `Call(Name("chr"),...)`. The generic call rule therefore performs actual
lookup and evaluation. The `chr` argument is always 48 or 49, so its supplied
ASCII guard is always satisfied. The divisor is the fixed nonzero integer 2.
No allocation, output, exception, or other state effect is skipped.

The supplied tree contains 25 opaque/symbol declarations for float, sorting,
and MD5 facilities. None is reachable from this program or its postcondition.
Fresh compilation reported six non-exhaustive-totality warnings involving
`mapStrVS`, `joinCodes`, `valSeqAt`, `floorFI`, `toF`, and `ceilF`; none is
reachable or mentioned by the theorem. All 45 supplied priority rules and all
six direct `Call` rules are inventoried. There are no supplied
`simplification` or `anywhere` rules. No supplied source contains the task
name, proof relation names, or task answer.

I found no rule that enables a false conclusion on the intended domain, so no
rule is labeled unsound and no false-conclusion witness is asserted.

Stage 5 result: PASS.

## 6. Fresh non-vacuity test

I did not rely on the candidate's `spec-vacuity.k`. The reviewer-authored
[`spec-fresh-vacuity.k`](evidence/spec-fresh-vacuity.k) executes the exact
submitted closure at the satisfying input `2` but changes the result obligation
from the real `db10db` to false `db11db`.

The mutation first passed `kprove --dry-run` with exit 0, establishing that it
parses and builds against the fresh definition. The actual mutated proof exited
1 with `WarnStuckClaimState`. Its residual shows the fully executed actual code
sequence:

```text
[100, 98, 49, 48, 100, 98]  // "db10db"
```

which does not unify with the requested `db11db`. This is the expected,
reachable unmet result obligation, not a parser error, timeout, missing import,
or unrelated crash.

Evidence:
[`06-fresh-vacuity.log`](evidence/06-fresh-vacuity.log) and
[`run_fresh_vacuity.sh`](evidence/run_fresh_vacuity.sh).

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics, for every symbolic mathematical integer
`N >= 0`, if the exact submitted call reaches its return state, its result is
the unique string-code sequence described by `decimalResultRel`: literal
leading and trailing `db`, `0` for zero, and for positive `N` the
most-significant-first sequence obtained by repeated remainder modulo 2 and
floor division by 2. The theorem is symbolic and unbounded; it is not a finite
set of examples or a bounded unrolling.

### Trust ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| Supplied MPY operational semantics for scopes, calls, evaluation order, integers, strings, loops, `chr`, and return | Both claims | Benchmark-mandated fixed semantics; integrity-checked byte-for-byte and every material operation executes |
| K 7.1.293 frontend, Haskell/LLVM backends, `kore-exec`, SMT/arithmetic hooks, and K built-in `Int`, `Bool`, `String`, `Map`, `List`, and structural equality | Meaning of both `#Top` results | Ordinary proof-tool trust boundary |
| Trusted `py2mpy.py` translation | Source-to-`solution.mpy` bridge | Regeneration was byte-identical; no candidate translator change |
| Mathematical reading of the remainder/floor recurrence as ordinary base-2 notation | Human-facing contract interpretation | Direct well-founded definition: remainder is 0/1, quotient decreases, and `N = 2Q + R`; no result oracle is assumed |
| Trusted canonical Python implementation | Differential oracle only | 9,110 finite checks support implementation alignment; they do not replace the K proof |
| Partial correctness | Termination | The requested theorem does not prove termination. Independently, for `N > 0`, `0 <= N//2 < N`, so the actual natural-number loop terminates; this ranking argument is not used to manufacture `#Top` |
| Supplied float/sort/MD5 opaque symbols and six unused totality-warning sites | None | Explicitly inventoried but unreachable and irrelevant to the theorem |

There is no empirical program-result bridge inside the proof, no
program-derived oracle, no operational summary that skips the body, and no
informal assumption on which claim closure depends. Differential and concrete
tests are kept in their proper role as finite bridge evidence.

Stage 7 result: PASS.

The clean proof is sound, result-constraining, pins the real regenerated
program, and covers the full material source-contract domain without a finite
bound or proof-local semantic shortcut.

VERDICT: PASS
LEGITIMACY: LEGIT
