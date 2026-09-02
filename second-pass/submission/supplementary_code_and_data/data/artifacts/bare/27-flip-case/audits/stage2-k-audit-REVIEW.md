# Independent adversarial review: 27-flip-case

## Executive assessment

The candidate contains a legitimate partial-correctness proof for the exact
submitted constructor program under the freshly compiled Haskell K definition.
The universal claim has no input restriction beyond `S:String`; all three
positive claims independently rebuild and close with `#Top`; the submitted
Python body is executable-AST-equivalent to the trusted canonical body; the
trusted translator reproduces `solution.mpy` byte-for-byte; and a mechanical
KORE constructor comparison pins the claim to that translated body.

I assign concerns rather than an unqualified pass for two non-fatal
limitations:

1. `flipSpec(S)` is definitionally the same `pySwapCase(S)` symbol used by the
   operational rule for the external `str.swapcase` primitive. The reachability
   proof therefore proves dispatch to that primitive, while the bridge from
   `pySwapCase` to the natural-language case-flipping contract remains in the
   generated semantics/trust boundary. That bridge has unusually strong
   evidence—an exhaustive equation audit and a concrete Haskell execution over
   every non-identity Unicode mapping—but it is not a separate bridge-free K
   connection theorem about CPython.
2. A fresh LLVM build of the same K sources is not Unicode-faithful. For
   example, it executes `"ß"` to `"ß"` instead of Python's `"SS"`. The selected
   proof and the candidate's own proof script use the Haskell backend, whose
   concrete execution agrees with Python, so this does not enable a false
   conclusion in the reconstructed proof. It is nevertheless a real
   backend-portability limitation in the generated semantics.

No material domain narrowing, substituted program, vacuity, proof-local
oracle, false Haskell semantic equation, or execution-bypassing rule was found.

## 1. Input and provenance integrity

The declared layout is `legacy-selected-stage1`, the condition is `bare`, and
the mode is `GENERATED_SEMANTICS`. I read `/audit-input.json` first and used its
`container_paths`; host provenance paths were not treated as container paths.

All required records are present, readable regular files:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `usage.json`,
  `codex-last.txt`, `codex-output.log`, and `prompt.txt`; and
- the single 229-record JSONL trace below
  `/generation-evidence/codex-trace/`.

The campaign object in `/audit-input.json` is structurally identical to
`/audit-campaign-lock.json`. All recorded regular-file hashes independently
recomputed in
`/audit-output/evidence/01-provenance/check_provenance.log` match. The trace
file SHA-256 matches both `generation-result.json` and `invocation.json`.
Using an independent reimplementation of the pipeline tree hash, the mounted
candidate is
`f2b6d0dfd1ff9115f278a29e49d913f9705b0ba8d2d80772c5c33debacb4905e`,
exactly the retained stage-one workspace hash; the trace tree is
`a35841d7c47e33d495a710c86baeda505fbe6087e7206557c4ecb2d2cd05afa9`,
exactly `usage.json`'s source-trace hash. This also provides independently
specified tree hashes rather than relying on the launcher integrity booleans.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`. There are no symlinks in
the candidate, reference, or generation-evidence trees. As required for
generated semantics, `/reference/reference-semantics` is absent; no hidden
reference semantics was sought or used.

The structured trace was parsed line-by-line with no parse errors, and all 43
recorded tool calls were inventoried in
`/audit-output/evidence/01-provenance/generation_trace_summary.log`. The full
13,938-line flat Codex output was likewise scanned in
`/audit-output/evidence/01-provenance/codex_output_summary.log`. These records
were treated only as untrusted generation history. Historical
`runtime-metrics.json` is absent, which the declared legacy layout explicitly
allows; `usage.json` is present and was inspected. There is no infrastructure
breach.

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt's contract is: for an input Python string, change lowercase
characters to uppercase and uppercase characters to lowercase, with
`flip_case("Hello") == "hELLO"`. The intended annotated domain is all Python
`str` values. The trusted canonical implementation is:

```python
return string.swapcase()
```

The candidate implementation has the identical executable statement. Its
omission of the canonical docstring and type annotations does not change the
function body. The AST comparison is recorded in
`/audit-output/evidence/02-fidelity/translator_and_ast.log`.

Fresh translation used the trusted translator:

```text
python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

It exited 0, and `cmp` exited 0 against the submitted `solution.mpy`; both
files have SHA-256
`f34d90ab871c6106c87ea64aa17e5ae4da5bfd5e86ca7ce805959554f8ae8620`.

The independent differential test
`/audit-output/evidence/02-fidelity/differential_test.py` imported the trusted
canonical and candidate entry points separately. It tested the documented
example; empty input; ASCII upper/lower/non-case boundaries; controls and
escaping; one-, two-, three-, and four-byte Unicode; titlecase and combining
characters; multi-character expansions; the maximum scalar; lone surrogates;
and deterministic generated strings from each encoding-width pool. The 1,579
inputs have deterministic input SHA-256
`62d6990c53ee1a20315b1f56f52921e38c5bce1c9131af4428e32156bc6ff742`.
There were zero mismatches
(`/audit-output/evidence/02-fidelity/differential_test.log`).

## 3. Clean proof reconstruction

All candidate source artifacts were copied into `/tmp/audit-work/candidate`.
No candidate-compiled definition or cache existed or was reused. The submitted
Unicode helper was preserved separately, regenerated with
`gen_unicode_case.py`, and compared byte-for-byte. Regeneration exited 0,
`cmp` exited 0, and both helper files have SHA-256
`c09aed4113b37b80c83100360298de60c66f669ffce8001f0ef56b91c76325d5`
(`/audit-output/evidence/03-reconstruction/regenerate_unicode_helper.log`).

Two fresh definitions were built:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

Both exited 0. Logs are
`/audit-output/evidence/03-reconstruction/kompile_concrete.log` and
`kompile_proof.log`.

The behaviorally relevant Haskell reconstruction was concretely executed on 13
normal and boundary strings, including empty, controls, Unicode expansions,
all UTF-8 widths, supplementary case mappings, the maximum scalar, and
surrogate-pass encodings. It had zero Python mismatches
(`/audit-output/evidence/03-reconstruction/semantics_differential_haskell.log`).
The separate LLVM execution had six non-ASCII mismatches, preserved in
`/audit-output/evidence/03-reconstruction/semantics_differential.log`. This is
the backend concern stated above, not concealed as a passing smoke test.

The three unlabeled candidate claims were copied unchanged into separate
reviewer modules solely to run each target independently. Each command exited
0 and printed `#Top`:

```text
kprove spec-claim1.k --definition proof-kompiled \
  --spec-module SPEC-CLAIM1
kprove spec-claim2.k --definition proof-kompiled \
  --spec-module SPEC-CLAIM2
kprove spec-claim3.k --definition proof-kompiled \
  --spec-module SPEC-CLAIM3
```

The per-claim logs are
`/audit-output/evidence/03-reconstruction/kprove_claim1.log`,
`kprove_claim2.log`, and `kprove_claim3.log`. The original combined command
also exited 0 and printed `#Top`
(`/audit-output/evidence/03-reconstruction/kprove_all_original.log`).

## 4. Adequacy and real-program pinning

The claims have no textual `requires` clause. Their entry preconditions and
postconditions are:

| Claim | Entry state in plain language | Required final result |
|---|---|---|
| Universal | Exact submitted `Module(FuncDef(...swapcase...))` in `<k>`; arbitrary `S:String` in `<arg>`; empty function map and environment | `strVal(flipSpec(S))`, exact function binding installed, empty environment |
| Prompt example | Same exact module; argument `"Hello"`; empty maps | `strVal("hELLO")` and the installed exact binding |
| Unicode example | Same exact module; argument UTF-8 bytes for `"Straße Δelta"`; empty maps | UTF-8 bytes for `strVal("sTRASSE δELTA")` and the installed exact binding |

Every precondition is satisfiable. Concrete witnesses and agreement with both
Python implementations are recorded in
`/audit-output/evidence/04-adequacy/satisfying_instances.log`: the universal
claim was instantiated at `""`, `"Hello"`, and `"ß"`; the two concrete claims
were instantiated at their stated inputs. All claimed, canonical, and
candidate values agree.

Trusted regeneration establishes source-to-`solution.mpy` identity. For the
remaining constructor-level link, I parsed the submitted `solution.mpy` and a
copy of the exact claim program (using the concrete empty-list spelling)
through `kast --sort Module --output kore`. `cmp` exited 0, and both KORE terms
have SHA-256
`bad042c8228fb4c1ceb3cb6049f9cb78b760cecc61b9cffc249ea9e8f435e241`
(`/audit-output/evidence/04-adequacy/program_pinning.log`). Thus `.Exprs` in
the claim is the empty list from the submitted trailing-comma constructor, not
a substituted call shape.

The claim executes module loading, exact binding installation, argument
binding, name lookup, receiver-first attribute evaluation, zero-argument call
dispatch, and exact return control. It does not replace the submitted body
with a summary. The only result-bearing primitive is the modeled external
string method.

For body sensitivity, the reviewer translated a material mutation
`return string` and changed the program term actually executed by the mutation
claim to `Return(Name("string"))`; the function-map destination was changed to
the same mutated body while the `"hELLO"` obligation was retained. `kprove`
exited 1 with a meaningful residual `strVal("Hello")`
(`/audit-output/evidence/04-adequacy/body_sensitivity_mutation.log`). This is
not the invalid experiment of changing only an unused external source file.

The universal precondition is not finitely bounded and does not strengthen the
source domain. `S:String` includes every UTF-8/surrogate-pass byte
representation used for Python strings in this semantics and even additional
malformed byte strings. There is therefore no material source-contract domain
narrowing.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

The machine-generated inventory at
`/audit-output/evidence/05-static/rule_inventory.tsv` contains every local
syntax declaration, configuration, rule, function equation, and claim, with
source lines, attributes, classification, text, and reviewer assessment. It
has 2,855 entries:

- `semantic.k`: 12 syntax/function declarations, one configuration, 11
  ordinary operational rules, and eight function equations (one `owise`);
- `unicode-case.k`: one total function declaration, 2,816 concrete equations,
  and one `owise` equation;
- `verification.k`: one function declaration and one equation; and
- `spec.k`: three reachability claims.

There are exactly two `total` declarations (`utf8CharLen` and `pySwapChar`),
no `functional` declarations, no simplification rules, no explicit priority
attributes, no opaque symbols, and two `owise` rules. The counts and the
exhaustive Unicode checks are in
`/audit-output/evidence/05-static/rule_inventory_summary.log`.

### Syntax, configuration, and used constructs

The grammar is a small constructor language for the actual translator output.
The configuration has only `<k>`, `<arg>`, `<functions>`, and `<env>`; each is
read or written. The exact mapping from every submitted constructor to its
declaration and rule path is in
`/audit-output/evidence/05-static/construct_coverage.md`. All material
constructs are modeled. The unused `Str` and multi-statement forms are extra
coverage, not fabricated behavior for a used construct.

### Operational rules

Each of the 11 rules was reviewed separately:

1. `Module(BODY)` preserves the continuation, executes `BODY`, and only then
   invokes the named entry point with the configured string argument.
2. Multi-statement sequencing is left-to-right and does not affect this
   singleton module.
3. `FuncDef` stores the exact parameters and untranslated body.
4. `#invoke` requires the selected map binding, installs that exact body, binds
   the sole parameter in an empty environment, and appends the exact
   `#endCall` marker.
5. `Return(E)` evaluates `E` before `#return`.
6. `Name(N)` performs exact environment lookup.
7. `Str(S)` returns the corresponding string value; it is unused here.
8. `Attribute(E,NAME)` evaluates the receiver before attribute selection.
9. Attribute selection preserves both receiver and method name in
   `boundStringMethod`.
10. The zero-argument call rule evaluates the callee before `#callNoArgs`;
    swapcase dispatch matches the exact `"swapcase"` name and preserved
    receiver.
11. The return rule applies only to
    `V ~> #return ~> #endCall`, returns that value, and clears the callee
    environment. It does not match or discard an arbitrary continuation.

Map update, lookup, argument evaluation, receiver evaluation, call selection,
and return control therefore agree with the submitted single-function program.
No operational proof bridge preempts these rules, and there are no loop/helper
claims.

### Result functions and equations

`pySwapCase` has a correct empty base and, for a nonempty Haskell-backend byte
string, consumes a width of 1–4 and recurses on a strictly shorter suffix.
`utf8CharLen`'s explicit guard intervals are pairwise disjoint; `owise`
covers all remaining inputs. On valid Python UTF-8 encodings the intervals
give exactly the proper width. C0/C1 and F5–F7 are assigned widths 2 and 4,
respectively, but those are malformed UTF-8 and outside the Python-string
encoding bridge; the universal K theorem is over-broad there rather than
narrower on the intended domain. Boundary helper claims, including empty,
guard endpoints, fallback bytes, mapped characters, and a multi-character
`pySwapChar` fallback, built and closed with `#Top`
(`/audit-output/evidence/05-static/helper_boundary_claims.log`).

The 2,816 concrete `pySwapChar` equations were parsed and checked against
`chr(codepoint).swapcase()` for all 1,114,112 Python code points. There are
exactly 2,816 expected non-identity entries, 76 expansions, one identity
`owise` fallback, and zero parse failures, duplicates, omissions, extras, or
wrong right-hand sides. Regeneration was byte-identical. A single Haskell
execution concatenating every non-identity code point returned 7,984 UTF-8
bytes with SHA-256
`1de2ac8e29e0690e1b3f97244e86a5434b3d5d30fcb2730b404ba65d67daa98c`,
exactly Python's output
(`/audit-output/evidence/05-static/all_mapped_k_test.log`).

`flipSpec(S) => pySwapCase(S)` is a truthful definitional alias and does not
replace an operational program region. It is also not independent evidence
that the primitive has the natural-language meaning; that distinction is why
the primitive appears in the trust ledger.

No Haskell rule was found that enables a false result on the intended domain.
The concrete false-behavior witness is limited to LLVM portability:
`S="ß"` yields `"ß"` in the fresh LLVM definition while Python and fresh
Haskell yield `"SS"`; the larger `"Straße Δelta"` witness similarly leaves
its non-ASCII characters unchanged under LLVM. These exact outputs are in the
two semantics differential logs. I do not label an individual K equation
globally false on that basis: the proof uses the Haskell definition, and the
failure arises from backend-dependent `STRING` hook representation. I do
label the generated semantics backend-specific.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was relied upon. The fresh reviewer mutation is
`/tmp/audit-work/candidate/spec-vacuity-audit.k`. It executes the exact
submitted program at the satisfiable input `"Hello"` but changes the
result-constraining postcondition from `"hELLO"` to the demonstrably false
`"hELLO!"`.

The dry run

```text
kprove spec-vacuity-audit.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
```

exited 0, proving the mutation parses and builds
(`/audit-output/evidence/06-nonvacuity/mutation_dry_run.log`). The actual proof
exited 1 with `WarnStuckClaimState`; the residual is the expected real result
`strVal("hELLO")`, not a parser error, crash, timeout, or unreachable mutation
(`/audit-output/evidence/06-nonvacuity/mutation_kprove.log`). The proof is
result-constraining and non-vacuous.

## 7. Proven versus assumed accounting

### Precisely proven

Under the freshly compiled Haskell K definition, for every K string `S`, the
exact submitted module from empty function/environment maps symbolically
executes through its actual body, installs its exact function binding, and
reaches `strVal(pySwapCase(S))` with an empty environment. The two concrete
end-to-end corollaries for `"Hello"` and `"Straße Δelta"` are also proved.
This is a partial-correctness statement; it does not claim general CPython
semantics for programs outside the modeled constructor subset.

### Trust ledger

| Boundary | Influence | Status and evidence |
|---|---|---|
| K 7.1.293 compiler, Haskell backend, reachability prover, and builtin `STRING`/`MAP`/`INT` hooks | All parsing, execution, and proof closure | Ordinary foundational trust. Tool versions were checked; definitions were rebuilt from source. |
| Trusted `/reference/py2mpy.py` | Source-to-constructor identity | Authorized trusted input; fresh output is byte-identical and the claim term is KORE-identical. |
| CPython 3.10.12 / Unicode 13 `str.swapcase` tables | Every Unicode result from `pySwapChar` | External library-primitive contract. Helper regeneration, exhaustive equation comparison, all-mapped Haskell execution, and Python differential testing support it; there is no independent K theorem about CPython internals. |
| UTF-8/surrogate-pass representation of Python `str` as Haskell-backend K `String` bytes | Character boundaries and recursive result | Informal representation bridge supported by boundary executions, surrogate cases, and all-mapped execution. LLVM's different behavior is the documented portability concern. |
| `flipSpec(S) = pySwapCase(S)` | Universal postcondition wording | Definitional summary, not an oracle and not independent evidence of the primitive's intent. |
| Termination of recursive `pySwapCase` on every finite valid encoding | Concrete realization of the symbolic result | Informal descent argument: each valid nonempty input consumes 1–4 bytes. Partial correctness itself does not require a total-termination theorem. |

There are no opaque result symbols, proof-local simplification lemmas,
operational summary bridges, priority shortcuts, or assumed loop invariants.
Generation prose, prior traces, differential tests, and the prior `#Top` were
not used as substitutes for the reconstructed K proof.

### Gate accounting and decision

- Gate A, real-program soundness: pass for the reconstructed Haskell
  definition. The body executes, constructor identity is mechanical, all
  positive claims close, body sensitivity holds, and the false result mutation
  is rejected.
- Gate B, intent adequacy: pass for the material source domain. The universal
  claim is not finitely bounded or restricted, and the modeled external
  primitive covers the pinned CPython/Unicode behavior.
- Gate C, trust/evidence auditability: pass with explicit limitations. Every
  trust boundary and dependent result is listed, and all claimed tests and
  commands have preserved artifacts.

The proof is legitimate, but the external-primitive intent bridge and concrete
LLVM divergence are sufficient non-fatal limitations to withhold an
unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
