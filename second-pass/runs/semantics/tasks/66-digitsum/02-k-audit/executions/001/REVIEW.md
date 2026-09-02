# Independent adversarial review: 66-digitsum

Decision: **FAIL / NOT_LEGIT**.

The K claims reconstruct successfully and are non-vacuous for a hand-copied
closure body, and I found no false candidate-local proof rule. The submission
nevertheless fails the required real-program-pinning gate: no claim loads or
calls the submitted `solution.mpy`. Replacing the scratch copy of both
`solution.py` and `solution.mpy` with `return 999`, rebuilding the proof
definition, and rerunning the entry proof still produces `#Top`. The formal
theorem therefore proves a substituted K macro rather than the submitted
program artifact. Independently, the submitted implementation disagrees with
the trusted canonical function on non-ASCII uppercase characters, for which
the prompt supplies no exclusion.

Audit scratch directory:
`/tmp/audit-work/66-digitsum.dlRQYF`. No candidate-provided compiled
definition, cache, `kore-exec.tar.gz`, or Python bytecode was used.

## 1. Input and provenance integrity

### Mode boundary

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` is present. There is therefore no
infrastructure-mode contradiction and a candidate verdict is appropriate.

The recursive, no-dereference comparison of the candidate
`reference-semantics/` against the trusted tree exited 0 with no output:
[semantics tree comparison](evidence/01_semantics_tree_diff.log). The prompt
and translator also compare byte-for-byte:

- `prompt.py` SHA-256 in both locations:
  `26e089859958a11b71b028884c146d360f5e2c079a59aeb4275b43b1f5f3e9ae`;
- `py2mpy.py` SHA-256 in both locations:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

See [trusted-file comparison](evidence/01_trusted_file_compare.log),
[candidate manifest](evidence/01_candidate_manifest.log), and
[reference manifest](evidence/01_reference_manifest.log). All candidate and
trusted reference entries are ordinary files/directories; neither tree
contains a symlink ([type check](evidence/01_file_types.log)). Thus there are
no missing, additional, changed, mistyped, or symlinked entries inside the
candidate supplied-semantics tree.

### Missing and extra provenance artifacts

The following specifically requested candidate records are absent:

- `run-input.json`;
- `metrics.json`;
- `codex-last.txt`;
- `codex-output.log`.

This is recorded in
[required-provenance check](evidence/01_required_provenance.log). No named
structured generation trace is present. `spec.json` is instead a KAST v3
serialization whose stale main module is `DIGIT-SUM-SPEC` and which contains
two `KClaim` sentences; it is not the current three-module `spec.k` and was
not used ([shape](evidence/01_spec_json_shape.log), [complete untrusted
content](evidence/01_spec_json_untrusted.log)). Other extra generated/cache
artifacts—`kore-exec.tar.gz`, `__pycache__/solution.cpython-310.pyc`, and
`spec.json`—were treated only as untrusted evidence and ignored for all
builds.

The missing provenance records reduce auditability but are not an
infrastructure failure; all source artifacts needed for an independent audit
were available.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

`/reference/prompt.py` asks for `digitSum(s)` on a string: return the sum of
the character codes of uppercase characters, with examples including the
empty string. `/reference/canonical.py` makes the intended predicate precise:
for every character, add `ord(char)` when `char.isupper()` is true, otherwise
add zero. The prompt does not restrict inputs to ASCII-only strings.

The submitted `solution.py` instead adds a code only when
`65 <= ord(char) <= 90`. This is equivalent on ASCII inputs, including all six
documented examples, but not on the stated Python-string domain. Source and
contract are preserved in
[contract and programs](evidence/02_contract_and_programs.log).

### Translation identity

I regenerated the MPY source from the submitted Python source with the trusted
translator:

```text
python3 /tmp/audit-work/66-digitsum.dlRQYF/trusted/py2mpy.py \
  /tmp/audit-work/66-digitsum.dlRQYF/candidate/solution.py
```

The regenerated and submitted files are byte-identical, both with SHA-256
`9f036b3d3f83e4e73cc0c82025b9d667307b1fe024f8cc2cb13c1a8aa6801c7b`.
See [translation identity](evidence/02_translation_identity.log).

### Independent differential test

[differential_test.py](evidence/differential_test.py) independently imports
the trusted canonical and submitted functions. It covers:

- all six documented examples and the empty string;
- singleton code points on both sides of each candidate branch boundary,
  including 64/65 and 90/91;
- exhaustive strings of length 0 through 4 over an eight-character alphabet;
- explicit non-ASCII uppercase and titlecase controls; and
- 5,000 deterministic generated strings of length 0 through 32.

The complete 9,357 inputs are in
[differential-inputs.json](evidence/differential-inputs.json), and complete
results are in
[differential-results.json](evidence/differential-results.json). The command
exited 1 because it found 6,179 mismatches
([bounded log](evidence/02_differential.log)). Representative material
witnesses are:

| Input | Trusted canonical | Candidate |
|---|---:|---:|
| `"É"` (`U+00C9`) | 201 | 0 |
| `"Ω"` (`U+03A9`) | 937 | 0 |
| `"Ａ"` (`U+FF21`) | 65313 | 0 |
| `"aΩZ"` | 1027 | 90 |

The documented and ASCII-boundary cases agree. The divergence is nevertheless
material because neither the prompt nor canonical entry point imposes an
ASCII-input precondition.

## 3. Clean proof reconstruction

K version `v7.1.337` and Python `3.10.12` were used
([versions](evidence/03_tool_versions.log)). All source was copied to fresh
scratch; no candidate cache or compiled definition was copied.

### Concrete definition

The supplied MPY definition was freshly compiled with LLVM:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0
([build log](evidence/03_build_runtime.log)). The candidate's concrete
assertion suite then terminated with `.K`, clean cells, and exit status 0
([krun log](evidence/03_concrete_assertions.log)). Compiler warnings concerned
unrelated supplied total functions and did not stop the build.

### Proof definitions and every positive claim

The base Haskell proof definition was freshly compiled from `verification.k`
with main module `DIGIT-SUM-VERIFICATION`
([build log](evidence/03_build_proof_base.log)). Both auxiliary claims were
then independently run against that definition, which does not import the
candidate's operational lemma module:

| Claim/module | Exit | Result | Evidence |
|---|---:|---|---|
| initialization / `DIGIT-SUM-INITIALIZATION-SPEC` | 0 | `#Top` | [log](evidence/03_prove_initialization.log) |
| loop invariant / `DIGIT-SUM-LOOP-SPEC` | 0 | `#Top` | [log](evidence/03_prove_loop.log) |

A second Haskell definition was freshly built with main module
`DIGIT-SUM-VERIFICATION-WITH-LOOP-LEMMA`
([build log](evidence/03_build_proof_with_lemmas.log)). The composed entry
claim also closed:

| Claim/module | Exit | Result | Evidence |
|---|---:|---|---|
| entry / `DIGIT-SUM-ENTRY-SPEC` | 0 | `#Top` | [log](evidence/03_prove_entry.log) |

Thus reconstruction itself passes: every positive target claim exits zero and
prints `#Top`.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable preconditions

There are no explicit `requires` clauses; each claim is universally quantified
over its sorted variables while fixing all visible cells.

- **Initialization.** In a pristine module/builtin configuration, directly
  call a closure whose body is `digitSumBody` on `str(S)`. The claim executes
  the three assignments and call-frame creation and reaches the exact string
  loop head with `result=0`, `char=""`, and `code=0`.
- **Loop invariant.** From the exact loop/return/endcall continuation, exact
  one-frame stack, accumulator `A`, and remaining string `str(S)`, execution
  returns `A + digitSumSpec(S)`, removes scope 1, pops the frame, and restores
  environment 0.
- **Entry.** In the same pristine configuration, directly call that copied
  closure on `str(S)` and return exactly `digitSumSpec(S)`.

[claim_witnesses.py](evidence/claim_witnesses.py) and its
[output](evidence/04_claim_witnesses.log) exhibit concrete states. For example,
entry and initialization use `S=[65,90,97]`; the loop witness uses
`S=[65,122,90]`, `A=7`, concrete old locals, and predicts 162. These sorted
terms and exact maps/lists satisfy the respective preconditions.

The result is not free or tautological: the same `S` supplied to the closure
occurs in the recursively defined destination. Ground substitution gives:

| Input | `digitSumSpec` | Candidate Python | Canonical Python |
|---|---:|---:|---:|
| `""` | 0 | 0 | 0 |
| `"@AZ["` | 155 | 155 | 155 |
| `"AZa"` | 155 | 155 | 155 |
| `"É"` | 0 | 0 | 201 |
| `"aΩZ"` | 90 | 90 | 1027 |

### Pinning failure

The `<k>` cell does **not** execute `Module(FuncDef(...))` from
`solution.mpy`, does not install the `digitSum` closure in module scope, and
does not look up or call the submitted `digitSum` binding. It directly
constructs and calls:

```text
closureVal(("s", .ParamNames), digitSumBody, 0)
```

`digitSumBody` and `digitSumLoopBody` are manually written macros in
`verification.k`. They currently match the submitted function body after
macro/list-sugar expansion, but neither `spec.k` nor `verification.k`
references `solution.py`, `solution.mpy`, or a `FuncDef("digitSum", ...)`.
The omitted fixed-semantics path is mapped in
[used-construct-map.md](evidence/used-construct-map.md).

I performed the required body-sensitivity check in a separate scratch copy:

1. changed `solution.py` to `def digitSum(s): return 999`;
2. regenerated and byte-checked the mutated `solution.mpy`;
3. left the K proof files unchanged;
4. rebuilt the Haskell proof definition from source; and
5. reran the entry proof.

The setup and distinct hashes are in
[body-sensitivity setup](evidence/04_body_sensitivity_setup.log), the rebuild
exited 0 ([build](evidence/04_body_sensitivity_build.log)), and the entry proof
still exited 0 with `#Top`
([proof](evidence/04_body_sensitivity_proof.log)). This is not merely a
post-compilation dependency observation: the definition was rebuilt after the
source and MPY mutation. It demonstrates that the theorem is insensitive to
the real program artifact.

This violates the explicit requirement that the `<k>` cell execute the actual
submitted `solution.mpy` and falls under the decision boundary for a
substituted program.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

[k_rule_inventory.py](evidence/k_rule_inventory.py) inventories every
`configuration`, `syntax`, `rule`, `claim`, `context`, and alias declaration
in the supplied root/helper K files and `verification.k`. The complete
reviewer-authored inventory is
[k-rule-inventory.json](evidence/k-rule-inventory.json); each of its 939
entries includes file, line, complete declaration text, attributes,
classification, source group, opacity flag, and review decision.

The recorded totals are
([summary](evidence/05_inventory_summary.log)):

- 1 configuration and 77 ordinary syntax declarations;
- 147 function/functional-form declarations, of which 108 carry `total`;
- 7 macro syntax declarations;
- 594 ordinary rules, 26 `owise` rules, 47 priority rules, and 35
  concrete-only rules;
- 5 contexts;
- 25 explicit `symbol` declarations, including 22 `no-evaluators` opaque
  boundaries;
- no `functional`-keyword declaration and no simplification/simplifier rule.

All 928 supplied-semantics declarations are byte-identical to the trusted
selected semantics. Their inventory decision is
`ACCEPTED_AT_SELECTED_SEMANTICS_LEVEL`: they define the fixed semantics and
are not candidate proof extensions. This trusted baseline does not bless the
11 declarations in `verification.k`, which were separately audited. The 22
opaque supplied symbols are all float, sort, or MD5 facilities and are
enumerated in
[special inventory](evidence/05_special_inventory_python.log); none is
reachable from this submitted AST or appears in a claim/result. An earlier
optional renderer attempt using unavailable `jq` exited 127
(`05_special_inventory.log`); the successful Python renderer produced the
cited evidence and the missing convenience binary had no audit impact.

### Used fixed semantics

The submitted AST uses `Module`, `FuncDef`, `Params`, statement sequencing,
`Assign`, `Name`, `Int`, `Str`, `For`, `Call`, `Compare`, `CmpOp`,
`BoolOp`, `If`, `AugAssign`, and `Return`. Every construct is mapped to its
declaration and operational rules in
[used-construct-map.md](evidence/used-construct-map.md). Complete numbered
source reads are preserved for
[core/string semantics](evidence/05_used_semantics_core.log),
[control/call semantics](evidence/05_used_semantics_control.log), and
[builtin/operator/value semantics](evidence/05_used_semantics_values.log).

For the copied body, the rules enforce:

- left-to-right string iteration and singleton-character binding;
- callee evaluation followed by left-to-right argument evaluation;
- lexical lookup of the real `ord` builtin;
- integer comparisons at inclusive boundaries 65 and 90;
- short-circuit `and` and strict `If` condition evaluation;
- current-frame updates of `char`, `code`, and `result`; and
- exact return, frame pop, scope deletion, and caller-environment restoration.

The heap remains empty; no allocation, exception, output, or opaque primitive
affects the result.

### Candidate-local declarations

The exact 11 declarations and their full extension records are in
[proof-extension-audit.md](evidence/proof-extension-audit.md):

- `digitSumBuiltins` is a compile-time scope macro with the same bindings as
  trusted `builtinsScope`;
- `digitSumLoopBody` and `digitSumBody` are compile-time syntactic copies, not
  execution shortcuts;
- `digitSumSpec` has disjoint/exhaustive `.IntSeq` and `iCons` equations,
  structurally descends, and truthfully computes the inclusive-65..90 sum;
- the initialization and loop `priority(20)` rules have exactly the cell,
  continuation, binding, and state footprints of the independently proved
  auxiliary claims. They accept no extra continuation or omitted cell. The
  priority changes selection only on the exact established domain.

The auxiliary claims were proved with main module
`DIGIT-SUM-VERIFICATION`, before either operational rule was imported. They
therefore serve as bridge-free universal connection theorems for the exact
rule domains rather than circular assumptions.

I found no candidate-local rule that enables a false conclusion on its
declared domain, no overlap inconsistency, no totality hole in
`digitSumSpec`, no simplification shortcut, and no unconstrained
program-derived oracle. Accordingly, I do **not** label any rule unsound and
do not manufacture a false-rule witness. The material failure is narrower and
separately witnessed: the honest theorem term is not pinned to the submitted
program artifact.

## 6. Fresh non-vacuity test

I created
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k), changing the entry
destination from `digitSumSpec(S)` to `digitSumSpec(S) +Int 1`. This is
demonstrably false for the satisfying input `S=.IntSeq`: the copied body
returns 0 while the mutation requires 1.

`kprove --dry-run` parsed and built the mutation successfully with exit 0
([dry-run log](evidence/06_mutation_dry_run.log)). The actual proof then exited
1 with `WarnStuckClaimState`, specifically exposing the unmet implication:

```text
digitSumSpec(S) +Int 1 #Equals digitSumSpec(S)
```

It ended with the expected “configuration cannot be rewritten further”
prover error, not a parser, import, timeout, or unrelated backend failure
([proof log](evidence/06_mutation_proof.log)). Thus the copied-body theorem is
meaningfully result-constraining and non-vacuous. This does not cure its
artifact-pinning failure.

## 7. Proven versus assumed accounting

### What the successful K proof establishes

Conditional on the supplied MPY semantics and K toolchain, the successful
reachability proof establishes partial correctness of this exact *constructed
K closure*: for every finite `IntSeq S`, from the pristine cells in the entry
claim, execution of the hand-written `digitSumBody` closure has final integer
`digitSumSpec(S)`, the sum of codes in inclusive range 65..90. The auxiliary
loop theorem establishes the corresponding accumulator invariant and complete
frame cleanup. The false mutation confirms that this integer equality matters
to closure.

It does not establish:

- execution or binding of the `FuncDef` in submitted `solution.mpy`;
- sensitivity to any change in `solution.py` or `solution.mpy`;
- equivalence to `str.isupper()` on all Python strings;
- Python exception behavior outside the singleton-string `ord` calls reached
  by this loop; or
- termination beyond the partial-correctness interpretation.

### Trust ledger

| Boundary | Dependents and status |
|---|---|
| Byte-identical supplied MPY semantics | Defines all K execution. Acceptable and required by `SUPPLIED_SEMANTICS`; candidate did not alter it. |
| K 7.1.337, Haskell/LLVM backends, SMT and K integer/collection hooks | Ordinary machine-checking trusted computing base. Builds and positive/negative runs behaved consistently. |
| Trusted `py2mpy.py` | Establishes byte identity of Python-to-MPY translation. Acceptable for source fidelity, but the proof never imports the resulting MPY. |
| Manual equality of `digitSumBody`/`digitSumLoopBody` to the current MPY body | Static inspection shows equality now. Concerning and ultimately illegitimate as program pinning because no machine-checked dependency exists; the `return 999` rebuild is the counterexample. |
| `digitSumSpec` equations | Not assumed or opaque: fully defined, total over `IntSeq`, and connected to copied-body execution by the loop claim. |
| Two operational lemmas | Not assumed: independently proved against fixed semantics over their exact complete contexts. |
| 22 supplied opaque float/sort/MD5 symbols | Acceptable but irrelevant: none influences control, state, or result here. |
| Python/canonical intent bridge | Only finitely tested and in fact refuted for Unicode uppercase inputs. It cannot support the requested natural-language property. |
| Missing provenance logs | Evidentiary limitation. They are not used as proof evidence and do not create infrastructure uncertainty. |

### Final decision

The positive `#Top` results are genuine for the theory and copied closure, and
the local proof rules are sound on their exact domains. However, a legitimate
submission under the stated decision boundary must pin the actual generated
program. This one does not: a materially different submitted program survives
a clean rebuild with the same successful entry proof. That is a substituted
program, requiring `FAIL / NOT_LEGIT`. The canonical Unicode divergence is an
additional material intent failure rather than the basis for an unsound-rule
claim.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
