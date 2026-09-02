# Independent adversarial audit: 124-valid-date

The reconstructed K proof is legitimate for the submitted generated program,
but it does not establish equivalence to the mounted canonical implementation.
The generated program and theorem match the literal `mm-dd-yyyy` contract; the
trusted canonical implementation has materially different behavior because of
operator precedence and permissive parsing. That contradiction is the reason
for `CONCERNS` rather than `PASS`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is no infrastructure-mode
contradiction, so the candidate audit may proceed.

I recursively compared `/candidate/reference-semantics` with the trusted tree
using `diff --no-dereference -qr`. The command exited 0 with no differences.
The candidate tree has exactly the same directories and 24 regular `.k` files
as the trusted tree; it has no missing, additional, changed, mistyped, or
symlinked entries. The complete type listing and comparison are in
`evidence/logs/01-integrity.log`.

The other provenance checks were also clean:

- `/candidate/prompt.py` and `/reference/prompt.py` are byte-identical, SHA-256
  `71bb688daf8e872a52f7dfb4d4a09c07db640afd5fc1f8845baa1470a2930b78`.
- `/candidate/py2mpy.py` and `/reference/py2mpy.py` are byte-identical, SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
- `run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`, and the
  structured JSONL generation trace are present as regular files. Required
  proof sources `solution.py`, `solution.mpy`, `verification.k`, and `spec.k`
  are also present as regular files. No required artifact is missing or
  symlinked.

`run-input.json` claims the expected problem and hashes; `metrics.json` claims
generation exit 0; the prose/log/trace claim `VALIDATED`, a prior `#Top`, 30,923
differential cases, and two failed negative probes. I treated all of those as
untrusted claims. Their sizes and relevant claimed results are recorded in
`evidence/logs/02-provenance-claims.log`; none was used as proof evidence.

The candidate also contains `runtime-kompiled`, `verification-kompiled`,
`verification-llvm-kompiled`, bytecode caches, and candidate test artifacts.
Those are not extra entries inside the integrity-constrained semantics tree,
but they were excluded from reconstruction. Only source artifacts were copied
to `/tmp/audit-work/124-valid-date`.

Stage 1 result: PASS. No provenance or supplied-semantics integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract

From `/reference/prompt.py`, `valid_date` should accept a date string exactly
when it has the `mm-dd-yyyy` form, a month from 1 through 12, a day of at least
1, and an upper day bound of 29 for February, 30 for April/June/September/
November, and 31 for the other months. The prompt imposes no leap-year rule or
numeric year bound. The nonempty rule is implied by the exact format.

The submitted `solution.py` implements that literal reading by requiring
length 10, separators at offsets 2 and 5, ASCII digit codes in all other
positions, month 1..12, day at least 1, and the stated per-month upper bound.
All branches return a Boolean. For string inputs, a non-ten-length value exits
before indexing; a ten-character value makes every fixed index and `ord` call
safe.

The trusted translator was run afresh:

```text
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
```

Both files have SHA-256
`6f464d72932f2adf0eb5e829f4d2f47a1c489fbbe57898ccc21c403c983b1c78`;
the comparison exited 0. See `evidence/logs/03-translation-identity.log`.

### Canonical contradiction

The mounted `/reference/canonical.py` is not behaviorally equivalent to that
contract. It strips whitespace, splits on `-`, and uses `int`, so it accepts
some non-fixed-width, signed, whitespace-padded, underscore-containing, and
Unicode-digit forms. More importantly, Python gives `and` higher precedence
than `or` in these canonical conditions. The final condition is effectively:

```text
(month == 2 and day < 1) or day > 29
```

Consequently, after the month check the canonical implementation rejects every
day above 29 in every month. For example, it returns `False` for
`03-31-2000`, even though the prompt and submitted program return `True`.

I wrote `evidence/scripts/differential_audit.py`, which independently imports
the mounted canonical entry point and the scratch copy of the generated entry
point. Its deterministic 36,302-case input set is preserved in
`evidence/differential-inputs.json` and covers:

- all five documented examples;
- empty, malformed, whitespace, Unicode, and length boundaries;
- month fields 00..99 and day fields 00..99 for years 0000, 2000, and 9999;
- every printable-ASCII single-position mutation of `03-11-2000`;
- 5,000 seeded generated ASCII strings and 1,000 seeded generated Unicode
  strings.

The exact command and exit 1 are in `evidence/logs/04-differential.log`; all 74
mismatch records are in `evidence/differential-results.json`. They divide as
follows (`evidence/logs/19-differential-classification.log`):

- 54 cases where canonical was `False`, generated was `True`, and the literal
  prompt oracle was `True`. These are precisely prompt-valid day-30/day-31
  cases across the three exhaustive years.
- 20 cases where canonical was `True`, generated was `False`, and the literal
  prompt oracle was `False`. These arise from the canonical parser's permissive
  whitespace/width/sign/underscore/Unicode handling.
- The generated implementation had zero disagreements with the literal prompt
  oracle on the finite sample.

The nonzero differential status is intentional and material. A different
algorithm is allowed, and static inspection shows the generated algorithm
matches the stated 29/30/31 contract. Nevertheless, it is not a rewrite of the
trusted canonical behavior. The prompt-versus-canonical contradiction is an
intent bridge limitation, not a false K theorem about the submitted program.

Stage 2 result: CONCERN. Translation fidelity passes; canonical equivalence
fails materially, while literal prompt alignment passes.

## 3. Clean proof reconstruction

No candidate-built definition or cache was copied or referenced. K v7.1.293
was available at `/usr/bin`. I built fresh definitions from the scratch source.

Concrete supplied-semantics build:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled
```

This exited 0 (`evidence/logs/05-kompile-concrete.log`). The compiler warned
about several supplied total functions that are incomplete on irrelevant
value constructors and about unused variables in `strLt`; none is reached by
this program. These warnings are addressed again in Stage 5.

Proof build:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0 (`evidence/logs/06-kompile-proof.log`). The only messages were
unused-variable warnings in the unchanged supplied `strLt` rules.

I then ran every positive target claim independently rather than trusting a
combined prior run:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.invalid-length
# #Top; exit 0

kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC --claims SPEC.length-ten
# #Top; exit 0
```

The complete bounded outputs and statuses are in
`evidence/logs/07-kprove-invalid-length.log` and
`evidence/logs/08-kprove-length-ten.log`. Each contains `#Top` and
`EXIT_STATUS: 0`.

Stage 3 result: PASS. All positive targets close under a clean source build.

## 4. Adequacy and real-program pinning

### Entry claims in plain language

`SPEC.invalid-length` starts from the standard module configuration, loads the
submitted `valid_date` definition, and calls it on an arbitrary formal string
`str(CS)`. Its precondition is exactly `isLen(CS) != 10`. Its postcondition is
the concrete result `false`. It additionally requires the call to restore
environment 0, scope allocator 1, empty heap, heap allocator 0, empty stack,
`noRet`, `NoExc`, and exit code 0, while retaining the loaded function binding.

`SPEC.length-ten` has no value restriction beyond the explicit ten-constructor
shape `iCons(C0,...iCons(C9,.IntSeq))`. It loads and calls the same function and
requires the exact result `validDate10(C0,...,C9)`, with the same final-state
constraints. The ten integers are otherwise arbitrary, so non-ASCII and even
non-Unicode mathematical code values remain in the formal domain and are
rejected by the digit predicate as appropriate.

The two preconditions are satisfiable and exhaustive over the finite
`IntSeq` algebra: a sequence either has exactly ten constructors or its
recursively computed `isLen` differs from ten.

### Pin to the submitted program

The `<k>` cell does not call an unconstrained oracle. It executes:

```text
#loadAll(validDateProgram) ~> Call(Name("valid_date"), ...)
```

`validDateProgram` reduces to a `Module(FuncDef(..., validDateBody))`, and
`validDateBody` is the complete translated statement sequence. The supplied
rules then perform module loading, install a closure, resolve the name, bind
the argument, execute every statement, process `Return`, and pop the frame.
No proof-local rule matches `Call`, `#loadAll`, an operation in the body, or a
returned value.

As an independent structural check, I compiled `verification.k` afresh with
LLVM and ran submitted `solution.mpy` under the clean runtime definition and
the one-term `validDateProgram` alias under the clean verification definition.
The final configurations are byte-identical: both are 4,947 bytes with SHA-256
`f7c081ef516d4ca0f158d87629decf685d5a703d005f6d291af89e0f830aabf4`.
They include the same complete closure body. Sources and evidence are
`evidence/program-alias.mpy`, `evidence/submitted-final-config.txt`,
`evidence/alias-final-config.txt`, and
`evidence/logs/09-kompile-verification-llvm.log` through
`evidence/logs/14-alias-identity.log`.

I also created a concrete K witness program whose `valid_date` function AST is
asserted equal to `solution.py` before translation. It exercises empty input,
the normal valid case, the final 31-day branch, February overflow, and 30-day
month overflow. `krun` ended with `.K`, `NoExc`, exit code 0
(`evidence/logs/10-concrete-witnesses.log`).

A separate concrete substitution record is in
`evidence/logs/13-witness-python.log`:

| Input | Satisfied entry | Formal result | Generated Python | Canonical Python |
|---|---|---:|---:|---:|
| `""` | invalid length | false | false | false |
| `03-11-2000` | length ten | true | true | true |
| `03-31-2000` | length ten | true | true | false |
| `02-30-2000` | length ten | false | false | false |
| `04-31-2000` | length ten | false | false | false |

There are no helper or loop claims; the source is loop-free. Each target
postcondition fixes the returned Boolean rather than leaving a result variable,
using a tautology, or proving only one direction of a desired equivalence.
`validDate10` is total and fully defined in `verification.k`.

Finally, changing `validDateProgram` to load `return False` compiled cleanly
but made the original `SPEC.length-ten` proof fail with a residual `false`
result and changed closure body. This independent body-sensitivity evidence is
in `evidence/mutations/verification-program-mutant.k` and
`evidence/logs/20-body-mutant-kompile.log` through
`evidence/logs/21-body-mutant-proof.log`.

Stage 4 result: PASS for real-program pinning and result adequacy. The canonical
disagreement remains the Stage 2 intent limitation.

## 5. Rule-by-rule static soundness review

### Inventory scope

There is no candidate-generated `semantic.k` or generated-semantics helper in
this `SUPPLIED_SEMANTICS` submission. The candidate's
`reference-semantics/semantics.k` and all 23 imported helper files are exact
copies of the trusted baseline. I nevertheless inventoried every `syntax`,
configuration, context, rule, claim, and relevant attribute line across all 24
supplied K files plus `verification.k` and `spec.k`. The reviewer script and
94,241-byte line-addressed output are
`evidence/scripts/k_source_inventory.py` and
`evidence/logs/18-k-source-inventory.log`.

The exhaustive candidate-local proof extension inventory is seven syntax
constructors, seven equations, and two target claims. There are no local
`[functional]`, `[simplification]`, `[concrete]`, priority, `owise`, opaque,
`symbol`, or `no-evaluators` declarations, and no local operational `<k>` rule.

| Local equation | Class and complete domain | State footprint | Soundness decision |
|---|---|---|---|
| `validDateProgram => Module(FuncDef(..., validDateBody))` | Definitional summary; one nullary case | None | Sound. It names the submitted module and does not replace loading or calling it. |
| `validDateBody => <complete Stmts>` | Definitional summary; one nullary case | None | Sound. The RHS is the complete regenerated body; execution remains in supplied rules. |
| `validDateClosure => closureVal(("date",.ParamNames),validDateBody,0)` | Definitional summary; one nullary case | None | Sound. This is exactly the closure installed by the supplied `FuncDef` rule in module environment 0. |
| `dateDigit(C) => C -Int 48` | Mathematical definition for every `C:Int` | None | Sound integer equation; immediate termination. |
| `dateTwoDigits(A,B) => dateDigit(A)*Int 10 +Int dateDigit(B)` | Mathematical definition for every integer pair | None | Sound decimal decoding; reduces to `dateDigit` and integer arithmetic. |
| `badDateDigit(C) => dateDigit(C)<Int 0 orBool dateDigit(C)>Int 9` | Mathematical definition for every integer | None | Sound characterization of codes outside ASCII `0`..`9`. |
| `validDate10(C0,...,C9) => <nested #if>` | Mathematical definition for every integer ten-tuple | None | Sound spelling of separators, eight digit tests, month range, positive day, and the 29/30/31 branch table. It is used only as the result postcondition. |

Every local `[function,total]` symbol has one unconditional equation, so
coverage is complete and there are no pairwise overlaps. Dependencies are
acyclic: `validDate10` calls `badDateDigit`/`dateTwoDigits`, those call
`dateDigit`, and all reduce to built-in integer/Boolean operations. The task's
answer is encoded only in the postcondition definition; no rule rewrites a
program call or computed result to that answer. Thus it is a property to be
proved, not a smuggled execution shortcut.

The two `spec.k` claims listed in Stage 4 are the only claims. They contain no
auxiliary circularity, invariant, or helper theorem.

### Used-syntax and supplied-rule mapping

Every constructor in `solution.mpy` is declared and has a reachable supplied
semantic route:

| Submitted construct | Declaration and rules used |
|---|---|
| `Module`, `FuncDef`, `Params`, `Stmts` | `syntax.k:53-61`; `core.k:124-127` loads/sequences statements; `functions.k:14-16` installs the exact closure. |
| `Name`, `Call`, `Exprs` | `syntax.k:12,28,37`; `core.k:130-154` performs lexical/builtin lookup; `call.k:19-32` evaluates the callee then arguments; `core.k:183-191` evaluates arguments left-to-right; `call.k:69-75` enters the user frame. |
| `Int`, `Bool`, `Str` | `syntax.k:9-13`; `core.k:193-196` evaluates integer/Boolean literals; `str.k:13-17` turns the ASCII `"-"` literal into code 45. |
| `Assign`, `If`, `Return` | `syntax.k:41,49-50`; `controls.k:7-19` writes the current local scope; `controls.k:49-52` evaluates truth and selects one branch; `functions.k:77-90` records the return value, restores the caller, removes the callee frame, and restores `scopeLoc`. |
| `BoolOp("or",...)` | `syntax.k:16`; `bool.k:12-24` evaluates only the head and short-circuits left-to-right, matching Python for these Boolean comparison operands. |
| `BinOp` | `syntax.k:15` is `seqstrict(2,3)`; `operators.k:12` dispatches cooled operands; `int.k:9-17` supplies the used `+`, `-`, and `*` cases. |
| `Compare`, `CmpOp` | `syntax.k:30-32`; `operators.k:14-17` evaluates left then wrapped right operands; `int.k:22-27` supplies all used integer comparisons; `str.k:25-26` supplies separator equality/inequality. |
| `Subscript` | `syntax.k:22,38`; `subscript.k:25-41` evaluates object then index, normalizes the fixed nonnegative index, and returns a one-code string through `intSeqAt`. |
| `len`, `ord` | `core.k:156-181` provides their builtin bindings; `builtins.k:17-26` maps string `len` to `isLen`; `builtins.k:142-144` maps `ord` of a one-code string to that code. |

The active control/state path is complete. Loading writes only the function
binding in module scope 0. Calling allocates scope 1 and pushes one frame;
parameter binding and all assignments affect that local scope. `Return/#pop`
deletes scope 1, restores environment 0 and allocator 1, clears the return
state and frame stack, and leaves the module binding. This program allocates no
heap object, changes no exit code, and raises no modeled exception on the claim
domains. All configuration cells in the supplied semantics are present in the
claim and constrained in the destination.

Relevant priorities/overlaps are benign: the generic `Call` rule is `owise`
but no problem-local call interception exists; cell-aware binding/assignment
priorities require a `$cells` frame and cannot match this plain closure; heap
reference priorities require `ref` operands and cannot match the formal string
input. Integer and string operator cases are sort-disjoint. Fixed indices are
in bounds in the length-ten claim, and the invalid-length branch returns before
any index, so the partial `intSeqAt` rules cover every reached use.

Fresh LLVM compilation warned that unrelated supplied helpers (`mapStrVS`,
`floorFI`, `toF`, `ceilF`, `joinCodes`, and the list helper `valSeqAt`) are not
exhaustive on all imported value constructors. None occurs in the submitted
program or proof path; unmatched total terms remain abstract rather than
asserting a false result. The only Haskell-proof warnings concern unused tail
variables in supplied `strLt`, which is also unreachable because the program
does no string ordering.

I found no unsound local or used supplied rule, so there is no claimed
unsoundness requiring a false-conclusion witness. The narrower remaining gap is
that the supplied semantics itself is a mode-mandated foundation rather than a
proved model of all CPython behavior; that is accounted for in Stage 7.

Stage 5 result: PASS. The proof theory used by these claims is sound for the
formal and intended string domain, with no execution bypass.

## 6. Fresh non-vacuity test

I did not rely on candidate `spec-vacuity.k`. The fresh reviewer mutation is
`evidence/mutations/audit-false-result.k`, with its scratch copy at
`/tmp/audit-work/124-valid-date/audit-false-result.k`. It preserves the real
module load and call but changes the result obligation for the satisfying
length-ten input `12-31-9999` from its actual `true` value to `false`.

The witness was checked independently against the scratch generated Python:

```text
input='12-31-9999' length=10 generated=True
```

See `evidence/logs/15-mutation-witness.log`.

The mutation first built successfully:

```text
kprove audit-false-result.k --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT --dry-run
# exit 0
```

See `evidence/logs/16-mutation-dry-run.log`. The actual proof command then
exited 1 with `WarnStuckClaimState`; its reached configuration contains
`<k> true ~> .K </k>` while the destination demands `false`. This is the exact
unmet result obligation, not a parser error, import failure, timeout, or
unreachable mutation. Full output is in
`evidence/logs/17-mutation-proof.log`.

The additional program-body mutation described in Stage 4 also built and made
the original positive claim fail, but the fresh false-result probe alone
satisfies the required non-vacuity test.

Stage 6 result: PASS. The proof is result-discriminating and body-sensitive.

## 7. Proven versus assumed accounting

### Precisely proven

Relative to the supplied `MPY` semantics and the proof-local mathematical
definitions, the successful reachability claims establish this partial-
correctness result for the actual submitted `solution.mpy`:

- For every formal string `str(CS)` with `isLen(CS) != 10`, any terminating
  execution of the loaded `valid_date` call reaches the Boolean `false` and the
  fully constrained final configuration.
- For every formal string containing exactly ten arbitrary integer codes, any
  terminating execution reaches exactly `validDate10` of those ten codes and
  the same fully constrained final configuration.
- `validDate10` is exactly the candidate program's ASCII separator/digit,
  month, and 29/30/31 day predicate.

This is not a termination theorem, a theorem about non-string Python objects,
a proof that the supplied subset semantics equals CPython in general, or a
proof that the generated program equals `/reference/canonical.py`.

### Trust ledger

| Boundary | Effect and dependents | Status |
|---|---|---|
| Supplied `MPY` semantics, including `#loadAll`, scope lookup, calls/frames, binding, sequencing, assignment, branching, returns, subscripting, `len`, `ord`, and integer/string/Boolean operations | Determines all value, control, state, and exception behavior in both claims | Acceptable: mandated fixed foundation, byte-identical to the trusted mount, and the entire reached rule slice was statically reviewed. It remains a conditional semantics-to-CPython boundary. |
| K v7.1.293 parser/compiler, LLVM backend, Haskell backend, kore-exec, SMT/matching machinery, and imported K `INT`/`BOOL`/`STRING`/`MAP`/`LIST` primitives | Implements every build, concrete run, and proof result | Acceptable standard toolchain trust boundary; supported by clean rebuilds and discriminating negative tests, not proved inside K. |
| Trusted `/reference/py2mpy.py` and CPython AST parsing | Connects `solution.py` to the proved `solution.mpy` term | Acceptable conditional boundary: byte regeneration passed, the concrete witness AST matched, and alias configurations matched. Universal translator correctness is assumed as instructed. |
| Proof-local aliases `validDateProgram`, `validDateBody`, `validDateClosure` | Connect the claim's loaded term to the submitted program | Acceptable and audited, not opaque: all have exact equations, execute through fixed semantics, match the regenerated closure, and fail under a body mutation. |
| Interpretation of `mm-dd-yyyy` as exactly ten positions with ASCII digits | Connects `validDate10` to human intent | Concerning but not illegitimate: it matches the literal prompt and examples, but the prompt does not spell out Unicode parsing and the trusted canonical intentionally or accidentally accepts broader forms. |
| Mounted canonical implementation | Intended executable reference used for the required differential | Concerning: authentic trusted input, but its precedence makes all day values above 29 invalid, contradicting the prompt. The K theorem does not assume or prove canonical equivalence. |
| Reviewer CPython differential and concrete tests | Empirical support for source behavior, prompt interpretation, and the K/Python bridge on tested cases | Acceptable finite evidence only. The 36,302 cases, concrete witnesses, and alias comparison do not replace the universal K proof or prove universal CPython equivalence. |

There is no proof-local trusted primitive or opaque symbol. The imported
supplied theory does contain opaque or symbolic helpers for unrelated language
features. The exhaustive inventory records all of them. The explicit
`no-evaluators` symbols are `sortVS`, `sortKeyVS`, `intFloatDiv`, `divII`,
`floatMod`, `floatLt`, `absF`, `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`,
`eqF`, `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
`sqrtF`, and `md5hexCodes`. The supplied float helpers `floorFI`, `toF`, and
`ceilF` are total symbolic declarations with concrete equations only on their
int/float cases; `strLt` and `valSeqAt` can likewise remain abstract on
nonconstructor/unsupported cases. None of these symbols, rules, or abstract
cases is reachable from either target claim, affects a guard, changes state,
or occurs in the result. Their presence is therefore an acceptable inactive
part of the fixed semantics, not an assumed correctness conclusion for this
proof.

### Decision

Gate A (real-program soundness) passes: the proof executes the exact submitted
body, preserves the complete active state, has true non-overlapping equations,
constrains the result, and rejects both a false result and a changed body.
The theorem matches the literal natural-language property, and its evidence is
reproducible. The material canonical/generated disagreement prevents an
unqualified `PASS`, but it does not make the K theorem false, vacuous, or about
a substituted program. The appropriate decision is therefore
`CONCERNS / LEGIT`.

All reviewer-authored scripts, mutations, preserved inputs/results, final
configurations, exact commands, bounded outputs, and exit statuses are under
`/audit-output/evidence/`; `evidence/logs/22-evidence-status-and-hashes.log`
summarizes their statuses and hashes.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
