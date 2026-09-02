# Independent adversarial audit: 134-check-if-last-char-is-a-letter

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted program under the supplied MPY semantics. Clean
reconstruction closes every target claim, the claims mechanically pin the
regenerated program body, the proof-local rules are sound, and a fresh false
result is rejected for the expected reason.

The result is `CONCERNS / LEGIT`, rather than `PASS / LEGIT`, because the
supplied read-only semantics models alphabetic characters as ASCII only while
the submitted Python correctly uses CPython's Unicode-aware `str.isalpha()`.
This is the documented supplied-model behavior/representation gap covered by
campaign amendment v2 exception 1. It is not candidate-created narrowing.

## 1. Input and provenance integrity

`/audit-input.json` declares `record_layout: pipeline-v3`,
`semantics_mode: SUPPLIED_SEMANTICS`, and the expected problem and condition.
The trusted `/reference/reference-semantics` mount is present, as required.

I independently inspected and hashed all required records:

- `/audit-input.json` and `/audit-campaign-lock.json` are readable regular
  files. The lock SHA-256 is
  `053ed73cba6d14969a1268433f910c65d5a2c1f365fd324fb469fa1e51dadd01`,
  exactly the recorded value, and its parsed JSON exactly equals the
  `audit_campaign` block.
- `/run.json`, `/task.json`, `/generation-result.json`,
  `/generation-evidence/invocation.json`, `metrics.json`,
  `runtime-metrics.json`, `usage.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt` are all present as regular files and
  match their recorded file hashes.
- The structured trace contains one regular JSONL file. Its recorded file
  hash matches, all 345 events parse, and there are zero parse errors.
  Generation claims and prior `#Top` outputs were treated only as untrusted
  history.
- Pipeline tree digests independently match the generation workspace
  (`5c8d4075...`), supplied-semantics manifest (`4495a50f...`), and usage
  source trace (`6f007d83...`) records.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to their trusted
  mounts.
- Recursive type/path/content inventory of candidate and trusted
  `reference-semantics/` found 25 entries in each, zero differences, and no
  linked or unsupported entries. There are no missing, extra, changed, or
  mistyped supplied-semantics files.

The full independent check is
[stage1_integrity.log](/audit-output/evidence/stage1_integrity.log), and the
generation-trace index is
[stage1_generation_trace_summary.log](/audit-output/evidence/stage1_generation_trace_summary.log).
There is no audit-infrastructure breach.

I copied only candidate source artifacts plus the trusted semantics and trusted
Python references into `/tmp/audit-work/134-check-last-char`. Candidate-built
definitions, bytecode, and caches were neither copied nor used.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

The docstring requires `True` exactly when the last character is alphabetic
and is not part of a longer word, where words are groups separated by a literal
space. Equivalently, the final literal-space-delimited group must contain
exactly one alphabetic character. It explicitly requires:

- `"apple pie"` → `False`;
- `"apple pi e"` → `True`;
- `"apple pi e "` → `False`;
- `""` → `False`.

The submitted implementation rejects empty text, then requires
`txt[-1].isalpha()` and either a one-character input or a literal-space
predecessor. For strings, that is exactly the contract reading above. It
preserves the signature and does not narrow the documented input type.

The trusted canonical uses `txt.split(" ")[-1]`, length one, and an ASCII
`ord(lower(...))` range. It is a useful witness for ordinary ASCII inputs, but
campaign amendment v3 makes the docstring—not canonical identity—the contract.

### Translation identity

Fresh execution of:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

exited 0. Submitted and regenerated `solution.mpy` are byte-identical, both
with SHA-256
`d0a42ece2155635b68c0773c720a18ece548ce1a5dc07275f6350a8a3431717a`.
See [stage2_translation.log](/audit-output/evidence/stage2_translation.log).

### Independent differential

The reviewer-authored oracle independently takes the final
`txt.split(" ")[-1]` group, requires length one, and applies CPython
`isalpha()`. It does not import any K summary equation.

The differential covers 9,354 distinct strings:

- all four examples;
- explicit empty, singleton, last/non-last alphabetic, predecessor-space,
  predecessor-nonspace, trailing-space, repeated-space, tab, and newline
  boundaries;
- every string of lengths 0 through 5 over
  `(" ", "a", "Z", "1", "!", "\t")`;
- 14 Unicode/exotic cases.

The candidate had zero docstring-oracle mismatches and zero example failures.
The canonical had eight observed Unicode divergences, including returning
`False` for `"é"` and raising `TypeError` for `"İ"`. Those observations do not
show a candidate defect: Unicode edge behavior is not pinned by an example,
and Unicode-aware `isalpha()` is a defensible, plain-language reading of
“alphabetical character.”

The script, complete generated corpus, and results are
[stage2_differential.py](/audit-output/evidence/stage2_differential.py),
[stage2_inputs.json](/audit-output/evidence/stage2_inputs.json), and
[stage2_differential.log](/audit-output/evidence/stage2_differential.log).

## 3. Clean proof reconstruction

The live toolchain is K v7.1.293. Both definitions were rebuilt from source in
scratch:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

Both exited 0. LLVM emitted fixed-semantics non-exhaustive-function warnings
for unrelated subset operations; Haskell emitted only unused-variable warnings
in `strLt`. None match a term used by this program.

A reviewer-authored concrete program containing the exact submitted function
plus all examples and additional branch assertions was translated with the
trusted translator and executed under the fresh LLVM definition. `krun` exited
0 with `.K`, `NoExc`, and exit code 0. Evidence:
[stage3_smoke.py](/audit-output/evidence/stage3_smoke.py),
[stage3_kompile_llvm.log](/audit-output/evidence/stage3_kompile_llvm.log), and
[stage3_krun_smoke.log](/audit-output/evidence/stage3_krun_smoke.log).

The following fresh positive proof commands all exited 0 and printed `#Top`:

```text
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC \
  --claims SPEC.target-empty
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC \
  --claims SPEC.target-nonalpha
kprove spec.k --definition audit-verification-kompiled --spec-module SPEC \
  --claims SPEC.target-alpha
kprove spec-model-boundary.k --definition audit-verification-kompiled \
  --spec-module SPEC-MODEL-BOUNDARY
```

The combined and per-claim logs are
[stage3_kprove_all_targets.log](/audit-output/evidence/stage3_kprove_all_targets.log),
[stage3_kprove_target_empty.log](/audit-output/evidence/stage3_kprove_target_empty.log),
[stage3_kprove_target_nonalpha.log](/audit-output/evidence/stage3_kprove_target_nonalpha.log),
[stage3_kprove_target_alpha.log](/audit-output/evidence/stage3_kprove_target_alpha.log),
and
[stage3_kprove_model_boundary.log](/audit-output/evidence/stage3_kprove_model_boundary.log).
The complete exact command record is
[COMMANDS.md](/audit-output/evidence/COMMANDS.md).

## 4. Adequacy and real-program pinning

The three entry claims say:

- `target-empty`: for a modeled string of length zero, execute the target
  closure and return `standaloneLastLetter(IS)`, which reduces to `false`.
- `target-nonalpha`: for positive length with a non-ASCII-alphabetic last
  modeled code, execute the target closure and return `false`.
- `target-alpha`: for positive length with an ASCII-alphabetic last modeled
  code, execute the target closure and return `true` at length one, otherwise
  return whether the penultimate code is 32.

These preconditions are disjoint and exhaustive over all finite `IntSeq`
strings: structural length is either zero or positive, and on positive length
`isAlphaC(last)` is Boolean.

Each claim starts with a call through the exact global
`"check_if_last_char_is_a_letter"` binding. The closure contains the actual
parameter, complete translated body, and defining environment. The claims
also pin environment 0, builtins parent, scope/heap locations, empty heap and
stack, `noRet`, `NoExc`, and exit code 0. The right-hand side is the required
Boolean summary itself—not an unconstrained variable or implication.

Mechanical constructor comparison found:

- submitted `solution.mpy` equals trusted regeneration;
- all three claim closures have parameter `"txt"`, no cell variables,
  defining environment 0, and the same 131 normalized constructor tokens as
  the regenerated body;
- normalization removes only explicit/implicit `.Exprs` and `.Stmts` list
  terminators, which is parser-level syntax normalization.

See [stage4_pinning.py](/audit-output/evidence/stage4_pinning.py) and
[stage4_pinning.log](/audit-output/evidence/stage4_pinning.log).

Concrete satisfying witnesses also agree with the formal result and both
Python implementations:

| Claim case | Input | Formal result |
|---|---:|---:|
| empty | `""` | `False` |
| nonalpha | `"1"` | `False` |
| alpha singleton | `"a"` | `True` |
| alpha, space predecessor | `" a"` | `True` |
| alpha, nonspace predecessor | `"ba"` | `False` |

Finally, a reviewer-authored body-sensitivity claim changed the executed
closure body itself to `return True` while retaining the empty-input summary.
It parsed and executed, then `kprove` exited 1 with `WarnStuckClaimState` and
reachable residual `<k> true ~> .K </k>`. This is genuine body sensitivity,
not a mutation of an external unused source file. See
[stage4_body_sensitivity.k](/audit-output/evidence/stage4_body_sensitivity.k)
and
[stage4_body_sensitivity.log](/audit-output/evidence/stage4_body_sensitivity.log).

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The source inventory includes every `syntax`, `rule`, `context`,
`configuration`, `claim`, and `alias` entry in all trusted supplied-semantics
K files and candidate `verification.k`: 1,021 entries total (245 syntax
declarations, 770 rules, five contexts, and one configuration). It records
function/total/opaque/symbol/priority/simplification/concrete/owise/macro and
strictness attributes for every entry and assigns a review decision to every
one.

The full table is
[stage5_rule_inventory.md](/audit-output/evidence/stage5_rule_inventory.md);
the raw attribute index is
[stage5_attribute_index.txt](/audit-output/evidence/stage5_attribute_index.txt).
Each unused declaration/rule is explicitly accepted at the selected fixed-model
semantics level, not asserted to be a universal CPython model. Unused
fixed-subset and opaque declarations were checked for overlap with the used
term vocabulary. They have no matching path into these claims; in
particular, unrelated float, sort, MD5, collection, loop, and comprehension
boundaries cannot contribute to closure.

### Used syntax and operational rules

The executed constructor-to-rule mapping is:

| Program construct | Trusted declaration/rules |
|---|---|
| `FuncDef`, closure binding, name lookup | `syntax.k`, `core.k`, `functions.k` |
| `Call`, callee then left-to-right argument evaluation, closure frame | `call.k`, `core.k`, `functions.k` |
| `If`, truthiness and selected branch | `controls.k`, `core.k` |
| `Return`, frame pop and state restoration | `functions.k` |
| `len(str)` | `builtins.k` via structural `isLen` in `core.k` |
| unary negative indices and integer comparisons | `operators.k`, `int.k` |
| string subscript and negative-index normalization | `subscript.k` |
| bound `isalpha` method | `call.k`, `methods.k` |
| short-circuit `and`/`or` | `bool.k` |
| string literal and singleton equality | `str.k` plus the proof-local constructor lemma |

Evaluation order is faithful on the used path: callee lookup precedes arguments;
arguments are evaluated left-to-right; `If` evaluates only its chosen branch;
`and` and `or` short-circuit; and `Return` discards the remaining callee body
before `#pop` restores the caller. Empty input never indexes. For nonempty
input, `-1` normalizes in bounds. The `-2` access occurs only after the
alphabetic test and the length-one `or` case fail, so its length is at least
two and it is also in bounds.

The heap is empty and the argument is a bare `str`, so fixed priority rules for
heap refs and cell variables do not match. The exact scope binding fixes lookup
to the submitted closure. No candidate priority rule preempts fixed semantics.
Call/return leaves every explicitly pinned non-result cell unchanged.

### Candidate proof extensions

`verification.k` has exactly these extensions:

1. `standaloneLastLetter(IntSeq) [function, total]` with four equations.
   Their guards are pairwise disjoint and exhaustive: length zero;
   positive/nonalpha; length one/alpha; and length greater than one/alpha.
   Indexes are in bounds wherever used. The equations are nonrecursive,
   mathematical definitions of the intended modeled result. The symbol never
   matches `<k>` and replaces no program execution. The three reachability
   claims are the execution-to-summary connection theorems.
2. `iCons(C, REST) ==K .IntSeq => false [simplification]`. This is
   disjointness of the nonempty and empty free constructors.
3. `iCons(C, .IntSeq) ==K iCons(D, .IntSeq) => C ==Int D
   [simplification]`. This is singleton-constructor injectivity.

All three are true on their complete domains. They have no state footprint,
opaque value, continuation frame, binding shortcut, or control effect. There
are no proof-local operational bridges, oracles, trusted primitives, concrete
rules, priority rules, auxiliary claims, or circularities. No candidate-owned
unsound rule was found, so there is no false-conclusion witness to report for
one.

### Supplied-model divergence

The one material model limitation is explicit in trusted `methods.k`:
`isAlphaC` recognizes only codes 65–90 and 97–122. Trusted `str.k` also limits
literal decoding to ASCII. The fixed-model witness
`str(iCons(233, .IntSeq))` therefore returns `false` under MPY; the fresh
boundary claim proves `#Top`. CPython and the submitted program return `True`
for `"é"`.

This is a concrete model-vs-CPython behavior witness, not an unsound
candidate rule. The formal theorem still covers every `IntSeq` the supplied
model represents, including code 233, with no candidate-added guard or size
bound. Candidate `PROOF.md` explicitly records the gap and witness in both
Gate B and its trust ledger, and the submitted Python is faithful to CPython on
the gap. All four amendment-v2 exception-1 conditions are therefore met.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer mutation uses
the real closure body on the satisfiable modeled input `" a"`
(`iCons(32, iCons(97, .IntSeq))`) but requires the false result. Both Python
implementations and the formal summary return `True`.

The mutation built and executed far enough to reach the final Boolean. `kprove`
then exited 1 with `WarnStuckClaimState`, residual
`<k> true ~> .K </k>`, and destination `false`. This is the expected unmet
result obligation—not a parser failure, missing import, timeout, or unrelated
crash.

Artifacts:
[stage6_false_result.k](/audit-output/evidence/stage6_false_result.k) and
[stage6_false_result.log](/audit-output/evidence/stage6_false_result.log).
The proof is non-vacuous and discriminates an incorrect result.

## 7. Proven versus assumed accounting

### What is proved

Under the supplied MPY semantics, for every finite modeled string
`str(IS:IntSeq)`, starting from the exact pinned target binding and clean
call-state cells, if the target call terminates then it returns:

- `false` for empty input;
- `false` when the last modeled code is not ASCII alphabetic;
- `true` for a one-code ASCII alphabetic string;
- otherwise, for an ASCII-alphabetic final code, whether the preceding code is
  literal space 32.

The proof executes the submitted function body; it does not prove a substituted
helper or merely assume the summary.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| Supplied MPY semantics | Defines all used value, evaluation, call, control, state, and method behavior for every target claim | Required fixed trust boundary; used slice audited. |
| ASCII `strToCodes` / `isAlphaC` | Determines the model's alphabetic result | Documented nonfatal model gap with `"é"` witness; causes this `CONCERNS` verdict. |
| K v7.1.293, Haskell/LLVM backends, SMT/runtime | Compilation, concrete execution, and reachability checking | Standard proof-tool trust boundary. |
| Trusted `py2mpy.py` | Connects `solution.py` to `solution.mpy` | Byte-identical regeneration plus constructor-level claim comparison. |
| K builtin INT/BOOL/STRING/MAP/LIST theories | Structural length, arithmetic, equality, maps, and stack representation | Ordinary imported mathematical/runtime primitives on the used domain. |
| Summary-to-docstring reading | Interprets “alphabetical” and literal-space-separated word | Transparent informal intent bridge; examples and 9,354-case independent differential support it but do not replace the K proof. |
| CPython Unicode alphabet tables | Affect real `str.isalpha()` beyond ASCII | Outside the fixed MPY theorem; candidate behavior tested and faithful, gap explicitly reported. |
| Termination | K reachability result is partial correctness | Not separately proved; honestly excluded by theorem wording. |

Opaque float, sorting, MD5, and other unused supplied-model symbols have no
dependency path to any target result. Differential testing is finite evidence
only. Candidate `PROOF.md`, generation logs, and prior traces were not used as
substitutes for reconstruction or static soundness.

### Gate and benchmark decision

- Gate A (real-program soundness): PASS.
- Gate B (intent/domain adequacy): PASS for every input the fixed model
  represents, with the documented supplied-model Unicode behavior gap.
- Gate C (trust/evidence auditability): PASS.
- Campaign mapping: amendment v2 exception 1 requires the documented
  supplied-model representation/behavior gap to map to `CONCERNS / LEGIT`.

There is no candidate-caused narrowing, bounded unrolling, substituted body,
vacuity, failing positive claim, or unsound proof extension. The concern is
limited to what the immutable supplied semantics can say about non-ASCII
alphabetic characters.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
