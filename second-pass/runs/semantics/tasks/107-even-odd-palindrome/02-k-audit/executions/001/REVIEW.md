# Independent adversarial audit — 107-even-odd-palindrome

The reconstructed reachability proof is legitimate and result-constraining. It
executes a K term that is parser-identical to the trusted translation of the
submitted `solution.py`, and all four entry claims close independently in a
fresh Haskell definition. I assign **CONCERNS / LEGIT**, rather than PASS,
because the final bridge from the arithmetic postcondition to the
natural-language notion of palindrome is an independently checked
combinatorial/finite-domain argument, not another K theorem, and the candidate
omits its requested generation metadata. Neither limitation permits a false
program result to be proved.

Audit tools were Python 3.10.12 and K v7.1.337
(`evidence/toolchain.log`). Candidate files were treated as untrusted and
copied without caches to `/tmp/audit-work/reconstruction`; all definitions used
below were built there from source. Exact commands and status-file conventions
are in `evidence/COMMANDS.md`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present as a real directory. There is
therefore no semantics-mode/mount contradiction and no infrastructure breach.

`evidence/integrity_check.py` recursively compared type, relative path, and
SHA-256 for the candidate and trusted semantics trees. Every directory and all
24 K files were present, non-symlinked, and byte-identical; there were no
missing, additional, changed, mistyped, or symlinked semantics entries.
Candidate `prompt.py` and `py2mpy.py` are also regular files and byte-identical
to `/reference/prompt.py` and `/reference/py2mpy.py`. Full hashes and the
per-entry result are in `evidence/stage1-integrity.log` (command exit 0).

The proof sources `solution.py`, `solution.mpy`, `spec.k`, and
`verification.k` are present as regular files. The following requested
provenance artifacts are absent:

- `run-input.json`
- `metrics.json`
- `codex-last.txt`
- `codex-output.log`
- a structured generation trace

No `PROOF.md` is present. Candidate-only extras are `concrete-tests.py`,
`concrete-tests.mpy`, `prove.sh`, and
`__pycache__/solution.cpython-310.pyc`. They are not semantics-integrity
violations, are not imported by the proof, and were not reused for the fresh
reconstruction. The absent untrusted metadata limits provenance auditability
but does not prevent independent source reconstruction.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted contract asks, for an integer `n` with `1 <= n <= 1000`, for the
pair `(even_count, odd_count)` of decimal integer palindromes in the inclusive
range `1..n`. The canonical implementation tests
`str(i) == str(i)[::-1]` for every integer in that range and increments the
count selected by parity.

The submitted implementation is a different constant-time algorithm:

- for `1..9`, it splits the one-digit values by parity;
- for `10..99`, it adds the repeated-digit palindromes `11,22,...`;
- for `100..999`, it counts completed leading-digit blocks and the current
  `H?H` block;
- for `1000`, it returns the same count as at 999 because 1000 is not a
  palindrome.

The intended-domain branches are exhaustive and have boundaries at 10, 100,
and the special value 1000.

Running the trusted translator on the scratch `solution.py` produced
`evidence/regenerated-solution.mpy`. It is byte-identical to submitted
`solution.mpy`; both have SHA-256
`cc7a50bf0a19c016af4c35d9a2d1c63d6fc0d8dc3c87a35594df3e0096516c67`.
See `evidence/stage2-regenerate.log` (translator exit 0, `cmp` exit 0).

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the scratch submitted entry point. It ran:

- documented examples `n=3` and `n=12`;
- `n=0` as an out-of-contract empty-iteration case (there is no empty
  collection input for this integer-valued API);
- explicit boundaries around every program branch and representative hundred
  blocks;
- 80 deterministic generated values with seed 107; and
- every intended input `n=1..1000`.

There were zero mismatches over all 1,000 intended inputs. The examples yielded
`(1,2)` and `(4,6)`, and the out-of-contract zero case yielded `(0,0)` in both
implementations. Inputs and complete results are preserved in
`evidence/stage2-differential.log` (exit 0). This is exhaustive finite evidence
on the stated domain, not a substitute for the K proof.

## 3. Clean proof reconstruction

No candidate-compiled definition or cache was copied. From the scratch source
tree I freshly built:

- LLVM `runtime-audit-kompiled` from
  `reference-semantics/semantics.k`, main module `MPY-KRUN`, syntax module
  `MPY-SYNTAX`; and
- Haskell `verification-audit-kompiled` from `verification.k`, main module
  `VERIFICATION`, syntax module `MPY-SYNTAX`.

Both `kompile` commands exited 0
(`evidence/stage3-kompile-llvm.log`,
`evidence/stage3-kompile-haskell.log`). The LLVM build reports
non-exhaustive-match warnings in supplied, unused collection/float/method/
subscript helpers; the Haskell build reports only unused-variable warnings in
supplied string comparison rules. None is in the submitted program's
dependency slice, and no intended-domain false conclusion witness follows
from these warnings. I therefore record the narrow coverage warning rather
than call those trusted baseline rules unsound.

`evidence/concrete_harness.py` begins with a byte-identical 22-line copy of
`solution.py`, verified by `cmp`, followed by reviewer-authored assertions at
normal and branch-boundary inputs. The trusted translator generated
`evidence/concrete_harness.mpy`. Fresh LLVM `krun` exited 0 with final `.K`,
`NoExc`, and exit code 0 (`evidence/stage3-krun-harness.log`).

`evidence/split_positive_specs.py` split the four submitted claim blocks
without editing their bodies, placing each in a distinct module. The four
independent commands all exited 0 and printed `#Top`:

| Submitted claim | Domain | Evidence |
|---|---|---|
| 1 | `1 <= N < 10` | `evidence/stage3-kprove-claim-1.log` |
| 2 | `10 <= N < 100` | `evidence/stage3-kprove-claim-2.log` |
| 3 | `100 <= N < 1000` | `evidence/stage3-kprove-claim-3.log` |
| 4 | `N = 1000` | `evidence/stage3-kprove-claim-4.log` |

The exact unsplit submitted `spec.k` also exited 0 and printed `#Top`
(`evidence/stage3-kprove-full-spec.log`). Status files alongside each log
record the exit codes.

## 4. Adequacy and real-program pinning

All claims start from the supplied initial configuration: module environment
0, empty module map with builtins parent `-1`, builtins scope installed, empty
heap and stack, allocation counters at their initial values, `noRet`, `NoExc`,
and exit code 0.

In plain language, the four claims say:

1. for any integer `N` from 1 through 9, execute the submitted entry point and
   return exactly the two arithmetic summary counts;
2. the same for 10 through 99;
3. the same for 100 through 999; and
4. for the ground input 1000, return exactly `(48,60)`.

The destination `<k>` cell is an exact two-element tuple. Its elements are
`evenPalindromes(N)` and `oddPalindromes(N)`; they are neither free variables
nor implications. The post-state also requires the expected loaded closure,
restored environment, empty heap/stack, no return/exception state, and exit
code 0.

`#runEvenOdd` expands to `#loadAll(solutionModule)` followed by a real
`Call(Name("even_odd_palindrome"), N)`. `solutionModule` installs
`solutionBody`; it does not replace the call or body with a summary. The proof
therefore performs lookup, argument evaluation/binding, all real branches and
assignments, tuple construction, return, and frame pop under the supplied
semantics.

Because `verification.k` duplicates the translated AST rather than reading
`solution.mpy` at proof time, I performed a parser-level pin. The reviewer
extractor expanded `solutionModule`/`solutionBody`, rendered internal empty
statement lists in program syntax, and parsed both that term and the trusted
regenerated `.mpy` to KORE. The two KORE files are byte-identical with SHA-256
`6769acba55c58bacf72b53cb6d7f7b1f024cef4f01c061256593fc7bff5bb102`
(`evidence/regenerated-solution.kore`,
`evidence/verification-expanded.kore`,
`evidence/stage4-extract-program.log`). A preliminary attempt to embed
internal `.Stmts` notation directly in a program-surface claim failed to parse
(exit 113, `evidence/stage4-program-pin.log`); it is retained transparently and
is not used as evidence.

Every entry precondition is satisfiable. Ground witnesses are `N=3`, `12`,
`222`, and `1000`; their formal destinations equal both Python
implementations:

- `3 -> (1,2)`
- `12 -> (4,6)`
- `222 -> (11,20)`
- `1000 -> (48,60)`

`evidence/ground_claim_check.py` also evaluated the formal piecewise summary
against both Python implementations for every `N=1..1000` and found zero
mismatches (`evidence/stage4-ground-claims.log`, exit 0).

## 5. Rule-by-rule static soundness review

`evidence/inventory_k_rules.py` generated the exhaustive inventory in
`evidence/rule-inventory.md`. Its scope is the supplied root semantics, all 23
helper K files, and `verification.k`. It contains 1,115 top-level
declarations:

- 708 ordinary rules;
- 234 syntax declarations;
- one configuration and five contexts;
- 28 includes, 87 imports, and all module framing;
- 152 declarations bearing `function`, 109 bearing `total`, and none bearing
  `functional`;
- 45 priority-bearing, 26 `owise`, and 36 concrete-bearing declarations;
- 22 `no-evaluators` opaque declarations and 25 symbol-bearing declarations;
  and
- no simplification declarations.

Every inventory row records source line, full normalized declaration,
attributes, and an audit decision. The supplied entries are byte-identical
fixed semantics selected by the task, not candidate extensions. The static
dependency slice used here was nevertheless reviewed against the real program;
the exact construct/rule mapping is in
`evidence/used-construct-map.md`.

The used path has the following properties:

- statement and tuple elements evaluate left-to-right;
- integer `<`, `==`, `+`, `-`, `*`, `%`, and `//` dispatch to supplied integer
  rules;
- every divisor is a positive constant (`2`, `10`, `11`, or `100`), and
  supplied `pyMod` implements Python floor division;
- `If` selects one branch from a Boolean integer comparison;
- assignments update only the active callee scope;
- the call allocates one frame, binds `n`, executes the body, returns the exact
  tuple, then restores/deallocates the frame;
- the heap, exception, and exit-code cells are not fabricated or abstracted;
  and
- proof module `VERIFICATION` imports `MPY`, not the concrete-only
  `MPY-CONCRETE`.

The proof-local inventory is small and exhaustive:

- `solutionBody` plus one unconditional function equation: a definitional AST
  macro, parser-pinned above;
- `solutionModule` plus one unconditional equation: the exact function name,
  parameter, and body wrapper;
- `#runEvenOdd` plus one rule: a fresh load-and-call wrapper that preempts no
  supplied behavior;
- total `leadingDigit` and `currentBlock`, each with an unconditional equation
  and constant nonzero divisor; and
- partial `evenPalindromes`/`oddPalindromes`, each with four disjoint equations
  that jointly cover exactly `1..1000`.

The last two functions occur only in postconditions. They never replace
program execution, influence control, or act as a program-derived oracle.
Their equations agree on no overlapping symbolic guard, because the first
three ranges are disjoint and the fourth equation is only ground 1000.
`currentBlock` is valid on the three-digit range because, with leading digit
`H` and last two digits `R`, `(R-H+10)/10` is the number of values `t` for
which `H t H <= N`.

The 22 supplied opaque/no-evaluator symbols are:
`sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
`subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
`divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`, and
`md5hexCodes`. None occurs in the submitted AST, entry wrapper, destination,
or transitive used rule slice. Thus none bears the result of this theorem.

I found no proof-local unsound rule and therefore claim no false-conclusion
witness. The LLVM exhaustiveness warnings concern supplied symbols unreachable
here; without a reachable intended-domain witness they are recorded as a
coverage gap, not mislabeled as unsoundness.

## 6. Fresh non-vacuity test

The reviewer-authored `evidence/spec-vacuity-audit.k` changes the first claim's
even component from `evenPalindromes(N)` to
`evenPalindromes(N) +Int 1`, preserving the executable program, initial state,
other result component, and satisfiable precondition.

The mutation first passed `kprove --dry-run` (exit 0), establishing successful
parsing/spec compilation (`evidence/stage6-vacuity-dry-run.log`). The actual
proof then exited 1, not by timeout or parser/backend failure, with
`WarnStuckClaimState`; the residual reaches the exact returned tuple and fails
the final implication equating the real even result with the off-by-one
destination (`evidence/stage6-vacuity-proof.log`).

For the satisfying witness `N=3`, both Python implementations return `(1,2)`
while the mutation demands `(2,2)`
(`evidence/stage6-mutation-witness.log`, exit 0). This is meaningful
result-sensitivity evidence.

## 7. Proven versus assumed accounting

What the successful K proof establishes is partial correctness under the
supplied MPY semantics: for each of the four claim domains, if the parser-pinned
submitted program reaches normal return from the exact initial configuration,
the returned tuple and final observable cells are exactly those in the
piecewise arithmetic postcondition. It does not claim behavior outside
`1..1000`, non-integer inputs, or Python features outside the supplied subset,
and partial correctness alone is not a separate termination theorem.

Trust and evidence ledger:

| Boundary | Effect on this theorem | Assessment |
|---|---|---|
| K v7.1.337 parser, compiler, Haskell prover/backend, and built-in integer/Boolean/map/list theories | All parsing, symbolic execution, arithmetic, and reachability closure | Necessary low-level proof-tool trust; acceptable and version-recorded. |
| Trusted supplied semantics tree | Defines the MPY execution relation | Required by `SUPPLIED_SEMANTICS`, byte-identical in the candidate, freshly rebuilt; the used rule slice was statically reviewed. |
| Trusted `py2mpy.py` | Connects `solution.py` syntax to `solution.mpy` | Candidate translator is byte-identical; fresh output is byte-identical; proof AST is parser-identical KORE. No semantic decision is delegated to the translator. |
| The 22 supplied opaque symbols listed in stage 5 | None | Present in the global trusted language but unreachable and independent of every claim result here. |
| `leadingDigit`, `currentBlock`, `evenPalindromes`, `oddPalindromes` | Fix the exact destination value | Fully equational and result-constraining, not opaque and not operational bridges. Guard coverage/overlap and arithmetic were reviewed. |
| Combinatorial connection from the piecewise equations to “count decimal palindromes” | Connects the formal arithmetic result to natural-language intent | Informal: one-digit base counts are `(4,5)`; two-digit palindromes are `11d`; three-digit palindromes are `H?H` and have parity `H`; 1000 adds none. This is mathematically persuasive but not a K theorem, so it is the principal concern. |
| Python differential evidence against trusted canonical | Supports program/formula-to-intent alignment on the stated finite domain | Exhaustive over all 1,000 valid inputs with zero mismatches, plus examples/boundaries. It supports only this finite bridge and does not replace reachability closure. |
| Missing candidate metadata/trace | Generation provenance only | Auditability concern; it does not enter or weaken the reconstructed theorem. |

The proof contains no program-body substitution, operational shortcut,
unconstrained result, proof-local opaque value, task-answer rewrite on the
execution path, or vacuous precondition. The remaining limitations justify
CONCERNS rather than FAIL: the proof itself is sound and pins the real
generated program.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
