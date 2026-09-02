# Independent adversarial review: 154-cycpattern-check

## Determination

The candidate has a reproducible, non-vacuous K reachability proof of its
submitted `solution.mpy` under its generated semantics. It does **not** prove
the required HumanEval behavior on the full source-contract domain. The
candidate deliberately defines the empty second word to have no rotations and
returns `False`, while the trusted canonical program returns `True` for every
input with `b == ""`. The formal helper and two positive claims encode the
candidate's `False` behavior, so `#Top` proves the wrong contract at that
boundary.

Under the generic Kit vocabulary this is sound but materially limited. The
benchmark's explicit mapping makes such a material source-domain alteration
`FAIL / NOT_LEGIT`, not `CONCERNS / LEGIT`.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `154-cycpattern-check`;
- condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`; and
- no mounted reference semantics.

I read and independently checked `/audit-input.json`,
`/audit-campaign-lock.json`, `/run.json`, `/task.json`,
`/generation-result.json`, all layout-required generation records,
`usage.json` (present), the two legacy records (present), all 393 structured
trace records, all candidate artifacts, and all three trusted reference files.
The campaign-lock JSON exactly equals the campaign block in
`/audit-input.json`, and its SHA-256 is the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.

All launcher-declared container paths exist and are readable. Every recorded
per-file hash checked against the mounted bytes. In particular:

- candidate `prompt.py` is byte-identical to `/reference/prompt.py`;
- candidate `py2mpy.py` is byte-identical to `/reference/py2mpy.py`;
- the candidate pipeline tree digest is
  `80ce1749d28c71246a9ad5c6b8d5bbe910a73080ac5c8b552dee7aaefe15885c`,
  equal to both the invocation and result workspace hashes;
- the trace pipeline tree digest is
  `2dfd2471488725b8c380060b7221b2811ba4fb12f02624b81e773f0d0748ece1`,
  equal to `usage.json`'s source-trace hash;
- the sole trace file's hash is
  `3c9f52173ca1a42c815bfb0e14eff3980b20f77dd4ad1d7d7e701619f7f05084`,
  equal to the generation result's recorded file hash; and
- there are no symlinks below `/candidate`, `/reference`, or
  `/generation-evidence`.

`/reference/reference-semantics` is absent, as required for
`GENERATED_SEMANTICS`; `/candidate/reference-semantics` is also absent. No
mode/mount contradiction or infrastructure breach was found. Historical
`runtime-metrics.json` is absent, but it is not required for this
`legacy-selected-stage1` layout.

The generation records were treated only as untrusted history. They are
notably revealing: trace line 24 states that the empty-second-word behavior
would be `False`, and the claimed 961-pair differential test used this
handwritten oracle:

```python
def reference(a, b):
    return any(b[i:] + b[:i] in a for i in range(len(b)))
```

That oracle repeats the candidate's empty-range behavior rather than importing
the trusted canonical. Thus the historical “961 exhaustive pairs passed” claim
does not test the real source contract.

Evidence:

- [provenance_integrity.log](evidence/provenance_integrity.log)
- [verify_provenance.py](evidence/verify_provenance.py)
- [generation_record_inspection.log](evidence/generation_record_inspection.log)
- [inspect_generation_records.py](evidence/inspect_generation_records.py)

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

The trusted prompt says to return `True` iff the second word, or any rotation
of it, is a substring of the first word. The trusted canonical
(`/reference/canonical.py:16-22`) forms `pat = b + b` and checks:

```python
for i in range(len(a) - len(b) + 1):
    for j in range(len(b) + 1):
        if a[i:i+len(b)] == pat[j:j+len(b)]:
            return True
```

For `b == ""`, the outer range has `len(a) + 1` iterations and the inner range
has one. Both slices are `""`, so the canonical returns `True`, including when
`a == ""`.

The candidate (`/candidate/solution.py:1-7`) instead loops only while
`i < len(b)`. It performs no iteration when `b == ""` and returns `False`.
For nonempty string inputs its rotation search is a valid alternative
algorithm.

### Trusted regeneration

In scratch, this command regenerated the submitted constructor term:

```text
python3 py2mpy.py solution.py > solution.regenerated.mpy
```

`cmp -s solution.regenerated.mpy solution.mpy` exited 0. Both files have
SHA-256
`46ea97790d2a06dd56fda3e1f414bf3cd00a89a509e78f335520449e081bfaa2`.
Thus `solution.mpy` is a byte-faithful trusted translation of the submitted
`solution.py`.

### Independent differential

The reviewer test imports the trusted canonical and candidate entry points
directly. It covers all six prompt examples; loop-skipped, first-hit,
later-hit, all-miss, singleton, longer-pattern, empty, and Unicode boundaries;
and all `a,b` over alphabet `{a,b}` of lengths 0 through 4. There were 972
unique cases.

The test exited 1 with 32 mismatches. Every mismatch had `b == ""`:

```text
MISMATCH source=boundary a='' b='' canonical=True candidate=False
MISMATCH source=boundary a='anything' b='' canonical=True candidate=False
...
mismatch_count=32
EXIT_STATUS=1
```

All documented examples agreed. The 32 failures are the 31 generated first
strings plus the additional `"anything"` boundary.

Evidence:

- [translator_regeneration.log](evidence/translator_regeneration.log)
- [solution.regenerated.mpy](evidence/solution.regenerated.mpy)
- [differential_test.py](evidence/differential_test.py)
- [differential_test.log](evidence/differential_test.log)

Stage result: **FAIL for full-contract program fidelity**. This is a candidate
defect, not an infrastructure failure.

## 3. Clean proof reconstruction

All source artifacts needed for execution were copied to
`/tmp/audit-work/154-cycpattern-check`. No candidate-built definition or cache
was copied or used. The observed tools were K v7.1.293 and Python 3.10.12.

Fresh concrete definition:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-llvm-kompiled
EXIT_STATUS=0
```

Fresh proof definition:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module VERIFICATION-SYNTAX \
  --output-definition verification-haskell-kompiled
EXIT_STATUS=0
```

The original candidate proof command over all 12 claims printed `#Top` and
exited 0:

```text
kprove spec.k --definition verification-haskell-kompiled \
  --spec-module SPEC
#Top
EXIT_STATUS=0
```

The delivered `prove.sh` was also run from the clean scratch tree. It rebuilt
its own Haskell definition, executed its three concrete cases, printed `#Top`,
and exited 0.

For claim-by-claim reconstruction, I made a semantics-inert copy of `spec.k`
that only adds labels. Separate `kprove --claims` invocations closed the six
prompt examples, three ground boundaries, the symbolic-empty claim, and the
loop invariant. The whole-program claim was selected together with its
intended loop-invariant dependency. Every invocation printed `#Top` and exited
0.

Generated-semantics concrete testing ran 13 normal/boundary/Unicode inputs
through the freshly compiled LLVM definition. K agreed with candidate Python
on all 13 (`k_candidate_mismatch_count=0`). It disagreed with the trusted
canonical on the two tested empty-`b` inputs
(`k_canonical_mismatch_count=2`), faithfully exposing rather than masking the
candidate bug.

Evidence:

- [toolchain.log](evidence/toolchain.log)
- [kompile_semantic_llvm.log](evidence/kompile_semantic_llvm.log)
- [kompile_verification_haskell.log](evidence/kompile_verification_haskell.log)
- [kprove_all_positive.log](evidence/kprove_all_positive.log)
- [candidate_prove_sh_clean.log](evidence/candidate_prove_sh_clean.log)
- [spec-labeled.k](evidence/spec-labeled.k)
- [run_each_claim.sh](evidence/run_each_claim.sh)
- individual `evidence/kprove_claim_*.log` files
- [concrete_semantics_compare.py](evidence/concrete_semantics_compare.py)
- [concrete_semantics_compare.log](evidence/concrete_semantics_compare.log)

Stage result: the proof reconstructs successfully; reconstruction does not
cure the contract mismatch.

## 4. Adequacy and real-program pinning

### Plain-language claims and satisfiable preconditions

`spec.k` contains:

1. Six fixed-input claims for the prompt examples. Each starts with the exact
   generated program, the listed two string arguments, empty environment, and
   no result. Each requires termination with output
   `cyclicContains(a,b)`. These preconditions are immediately satisfiable by
   their displayed ground configurations.
2. Three fixed boundaries for `("abc","abc")`, `("x","x")`, and
   `("anything","")`, with the same result constraint. Their displayed
   configurations satisfy their preconditions.
3. A symbolic empty-pattern claim: for every K string `A`, execute the whole
   program with `(A,"")` and return `cyclicContains(A,"")`. A witness is
   `A = "anything"`.
4. A loop claim: for arbitrary strings `A,B` and
   `0 <= I <= lengthString(B)`, execute the actual loop followed by the real
   trailing `return False`, starting from the exact `a`, `b`, and `i`
   bindings, and return `cyclicContainsFrom(A,B,I)`. A witness is
   `A = "hello"`, `B = "ell"`, `I = 0`; the endpoint witness
   `A = ""`, `B = ""`, `I = 0` also satisfies the guard.
5. A whole-program claim: for all K strings `A,B`, execute the generated
   program from empty environment and no result, and return
   `cyclicContains(A,B)`. A witness is `A = "hello"`, `B = "ell"`.

The output is genuinely constrained. Only the final environment is
existential (`?RHO`); `<out>` must be exactly the stated Boolean, and `<k>`
must be consumed.

### Mechanical program identity

The pinning chain was independently reconstructed:

- trusted translation of `solution.py` is byte-identical to `solution.mpy`;
- `python3 build_solution_k.py` regenerates a byte-identical
  `solution-program.k`;
- parsing `solution.mpy` and macro-expanding `solutionProgram()` with the
  fresh definition yields byte-identical KAST JSON; and
- extracting the `While` constructor from the parsed function body yields
  exactly the macro-expanded `solutionLoop()` KAST.

The only builder normalization replaces a translator-rendered blank empty
statement list with `.Stmts`; the KAST identity check demonstrates that this
is semantically inert.

A body-sensitivity experiment changed the executed source-level
`return True` to `return False`, translated that changed source, embedded the
changed constructor term, and rebuilt a separate proof definition. The
mutant spec built successfully, then `kprove` exited 1 with
`WarnStuckClaimState`; its residual final state contained
`Result(pyBool(false))` where the original contract demanded true. This is a
mutation of the term actually executed by the claim, not an unused external
file.

### Concrete substitution

For `A = "hello", B = "ell"`, candidate Python, canonical Python, and K all
return `True`. For the decisive satisfying state
`A = "anything", B = ""`, the candidate and K return `False`, while the
trusted canonical returns `True`. Therefore the whole-program theorem is
adequate for the submitted implementation but inadequate for the intended
HumanEval result.

Evidence:

- [program_pinning_regeneration.log](evidence/program_pinning_regeneration.log)
- [constructor_pinning.log](evidence/constructor_pinning.log)
- [parsed-solution.json](evidence/parsed-solution.json)
- [expanded-solutionProgram.json](evidence/expanded-solutionProgram.json)
- [loop_constructor_pinning.log](evidence/loop_constructor_pinning.log)
- [expanded-solutionLoop.json](evidence/expanded-solutionLoop.json)
- [body_mutation_generation.log](evidence/body_mutation_generation.log)
- [body_mutation_kompile.log](evidence/body_mutation_kompile.log)
- [body_mutation_build.log](evidence/body_mutation_build.log)
- [body_mutation_proof_expected_failure.log](evidence/body_mutation_proof_expected_failure.log)

## 5. Rule-by-rule static soundness review

The source-line inventory is preserved in
[local_declaration_inventory.log](evidence/local_declaration_inventory.log);
the following is the exhaustive semantic review.

### Syntax, configuration, attributes, and opaque boundaries

`semantic.k:3-55` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: juxtaposed `Stmt` list;
- `Stmt`: `FuncDef`, `Assign`, `While`, `If`, and `Return`;
- `Params` and comma-separated `Strings`;
- `Expr`: `Name`, `Int`, `Bool`, `Call`, `BinOp`, `Compare`, and
  `Subscript`;
- comma-separated `Exprs`, `CmpOp`, `Slice`, and `Bound` (`Expr` or
  `NoBound`);
- runtime `Value` (`pyInt`, `pyBool`, `pyStr`), `Values`, and `Result`;
- continuation items `exec`, `assignTo`, `whileGuard`, `ifGuard`,
  `ReturnValue`, `binLeft`, `binRight`, `compareLeft`, `compareRight`,
  `sliceBase`, `sliceLower`, `sliceUpper`, `sliceStep`, and `LenCall`; and
- every `Value` as `KResult`.

`semantic.k:64-70` declares exactly four cells: `<k>`, input `<args>`,
variable `<env>`, and observable `<out>`. Every non-`k` cell is used. The
runtime module adds `start` and
`indexOf(String,String,Int) [function,total]`. Its sole defining rule is
`[concrete]`.

`solution-program.k` adds one macro, `solutionProgram()`, with one exact
constructor-expansion rule. `verification.k` adds one macro,
`solutionLoop()`, and two `[function,total]` symbols,
`cyclicContains` and `cyclicContainsFrom`.

There are no local `[functional]`, `[simplification]`, priority, `owise`,
`anywhere`, or trusted declarations. There are no proof-local opaque symbols
other than `indexOf` remaining uninterpreted on symbolic arguments because its
equation is concrete-only.

### All 37 rules in `semantic.k`

1. **`indexOf` (`semantic.k:78-79`)** rewrites ground calls to K's
   `findString`. For concrete K strings this matches Python string-membership's
   needed found/not-found test. On symbolic strings it intentionally remains
   an arbitrary total integer. The rule is not locally false, but there is no
   bridge-free universal theorem equating the symbolic wrapper to
   `findString`; the universal proof is interpretation-parametric in this
   external primitive.
2. **Entry (`84-87`)** matches the exact one-function module and exact
   `cycpattern_check(a,b)` binding, consumes the supplied two string arguments,
   installs exactly those bindings, and executes the matched `BODY`. This is a
   task-entry harness, not an answer rule: it accepts any body and executes it.
3. **Statement sequencing (`90-91`)** removes an empty list or schedules the
   first statement before the rest. It gives source order.
4. **Assignment (`93-95`)** evaluates the right side first and updates the
   named map entry. This is correct for the only used target, `Name("i")`.
5. **Conditionals (`97-101`)** evaluate the guard before either branch; the
   `BV` and `notBool BV` rules are disjoint and exhaustive over Boolean values.
6. **Loops (`103-108`)** evaluate the guard, schedule body then the same loop
   on true, and terminate the loop on false. The two Boolean guards are
   disjoint and preserve the continuation.
7. **Return (`110-112`)** evaluates its expression, writes the exact value to
   `<out>`, and discards the active remainder. In this semantics there is only
   one top-level function frame and no caller stack, so this models both early
   return and final return without omitting any modeled observable cell.
8. **Literals and lookup (`115-118`)** inject integer/Boolean values and read
   the exact map binding for a name.
9. **`len` (`121-122`)** evaluates its sole argument and applies
   `lengthString` to a string. The direct builtin binding is safe for this
   exact program because the entry environment contains only `a`, `b`, and
   later `i`; it cannot shadow `len`.
10. **Binary operations (`125-128`)** enforce left-to-right evaluation and
    correctly implement the only two used `+` cases: integer addition and
    string concatenation.
11. **Comparisons (`131-144`)** enforce left-to-right evaluation. Integer `<`
    splits into disjoint `<` and `>=` rules. String `in` splits on the
    integer result of `indexOf` into disjoint `>= 0` and `< 0` rules. All used
    value cases are covered.
12. **Slices (`148-163`)** evaluate base, then the used lower or upper
    expression, default missing lower to 0 and missing upper to string length,
    and call `substrString`. This is correct for `b[i:]` and `b[:i]` because
    the loop invariant guarantees `0 <= i < len(b)` whenever these slices are
    reached. The grammar admits an explicit step, but the operational rules
    ignore it; that construct is not present in `solution.mpy`, so this is a
    documented unused-language gap rather than a defect under generated
    minimal-semantics rules.

The rule count is exactly 37: 1 primitive bridge, 1 entry, 2 sequencing, 2
assignment, 3 conditional, 3 loop, 2 return, 3 literal/lookup, 2 `len`, 4
binary, 6 comparison, and 8 slicing rules.

### Generated helper and proof rules

- **`solutionProgram()` macro (`solution-program.k:5-20`)**: exact generated
  constructor term, mechanically validated above.
- **`solutionLoop()` macro (`verification.k:10-22`)**: exact `While`
  constructor from that term, mechanically validated above.
- **`cyclicContains(A,B)` (`verification.k:28`)**: definitionally starts at
  index 0.
- **`cyclicContainsFrom` stop (`29-30`)**: returns false when
  `I >= lengthString(B)`.
- **`cyclicContainsFrom` hit (`31-37`)**: returns true when `I` is in range
  and the rotation is found.
- **`cyclicContainsFrom` miss (`38-44`)**: advances to `I+1` when in range
  and not found.

The stop/hit/miss guards are pairwise disjoint and cover all integer
found/not-found outcomes for the claim's `0 <= I <= len(B)` domain. The miss
rule strictly increases `I` toward the stop guard. These are definitional
summary equations, not operational shortcuts. They encode the candidate's
choice that an empty `B` has no rotations; that equation is internally
consistent but fails the trusted source behavior.

`spec.k` has exactly 12 claims: six documented examples, three ground
boundaries, one symbolic empty-pattern theorem, one loop circularity, and one
whole-program theorem. No additional helper claim, simplification, priority,
or hidden trusted rule exists.

### Construct-to-rule coverage and overall judgement

Every constructor in `solution.mpy` maps to a declaration and rule group:

| Program construct | Declaration/rules |
|---|---|
| `Module`, `FuncDef`, `Params` | entry rule 84-87 |
| statement list | rules 90-91 |
| `Assign`, `Name`, `Int` | 93-95 and 115-118 |
| `While` and integer `<` | 103-108 and 131-138 |
| `Call(Name("len"),...)` | 121-122 |
| `If` and string `in` | 97-101 and 131-144 |
| string slices | 148-163 |
| string and integer `BinOp("+",...)` | 125-128 |
| `Return` and `Bool` | 110-116 |

Concrete tests exercise zero and positive loop iterations, both conditional
branches, early and final return, first and later rotation hits, complete
misses, both slice forms, and Unicode strings.

I found no locally false semantic or proof equation and therefore do not label
any inventoried rule “unsound.” In particular, I do not convert the missing
universal `indexOf` bridge theorem into an unsupported unsoundness allegation:
it is the narrower evidence/trust gap described above. The concrete rule,
fresh executions, and the theorem's interpretation-parametric structure
support treating string search as an external primitive, but finite evidence
does not prove its universal equivalence to Python.

The concrete false conclusion that decides this audit instead is at the
specification boundary, not a false K rule:

```text
a = "anything", b = ""
trusted canonical = True
candidate program = False
K theorem/helper = False
```

## 6. Fresh non-vacuity test

The fresh mutation
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) executes the exact
`solutionProgram()` on the satisfiable input `("hello","ell")` but demands
`Result(pyBool(false))`.

The mutation built successfully:

```text
kprove spec-vacuity-audit.k \
  --definition verification-haskell-kompiled \
  --spec-module SPEC-VACUITY-AUDIT --dry-run
EXIT_STATUS=0
```

The real proof then exited 1 with `WarnStuckClaimState`. Its reachable residual
is a fully terminated configuration with:

```text
<out>
  Result ( pyBool ( true ) )
</out>
```

This is exactly the expected unmet result obligation, not a parser error,
timeout, missing import, unreachable mutation, or unrelated crash.

Evidence:

- [nonvacuity_build.log](evidence/nonvacuity_build.log)
- [nonvacuity_proof_expected_failure.log](evidence/nonvacuity_proof_expected_failure.log)

Stage result: **PASS**. The reconstructed theorem discriminates a false result.

## 7. Proven versus assumed accounting

### What is formally proved

Conditional on the freshly compiled K definition, `kprove` establishes this
partial-correctness statement:

> For all K strings `A` and `B`, if the submitted generated constructor
> program terminates from the modeled entry configuration, its `<out>` cell is
> `pyBool(cyclicContains(A,B))`, where `cyclicContains` checks rotations at
> indices `0 .. length(B)-1` using `indexOf`.

The loop claim establishes the analogous result from every modeled loop head
with `0 <= I <= length(B)`. Fixed examples and boundaries are instances. The
proof constrains the returned Boolean and is sensitive to both postcondition
and executed-body mutations. It does not prove termination, which is normal
for partial correctness.

### Trust and assumption ledger

| Boundary | Influence | Accounting |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, and reachability engine | All proof and execution results | Standard trusted toolchain boundary; version recorded and rebuilt from sources. |
| Trusted `py2mpy.py` | Python-AST-to-constructor identity | Byte-identity regeneration and KAST macro comparison were checked. Translator correctness itself remains trusted. |
| Generated MPY semantics | Evaluation, state, control, return result | Audited rule by rule and concretely tested for every construct the submitted program uses. Unused explicit slice steps remain unmodeled. |
| K `INT`, `BOOL`, `STRING`, and `MAP` builtins | Arithmetic, comparisons, length, substring, concatenation, lookup/update | Ordinary low-level trusted primitives. Unicode ground witnesses agreed with Python. |
| `indexOf` concrete wrapper around `findString` | Every membership branch and final Boolean | Fixed external string-search primitive. Ground execution is connected by the `[concrete]` rule; symbolic execution is parametric. No bridge-free universal connection theorem was supplied, so the Python-membership bridge is conditional/empirical rather than independently proved. |
| `cyclicContains` equations | Formal postcondition | Truthful description of the candidate algorithm, including `False` for empty `B`; not a proof of agreement with the trusted canonical. |
| `solutionProgram` and `solutionLoop` macros | Program and loop identity | Mechanically regenerated and constructor-equal to the trusted translation. |
| Reviewer differential and concrete testing | Source/semantics bridge on tested cases | Finite evidence only. It exposes the empty-pattern mismatch and does not replace the K proof. |
| Termination | Whether a result is reached | Not established by the reachability theorem. |

### Gate accounting and verdict

- Real-program soundness/non-vacuity: passes for the submitted program under
  the named external primitive boundary. The actual program executes; no
  answer rule or free output variable bypasses it.
- Intent adequacy: fails. The theorem and implementation return `False` on
  all `b == ""` inputs, whereas the trusted canonical returns `True`. This is
  a material portion of the unrestricted string domain, not a cosmetic
  difference or a finite-test gap.
- Evidence auditability: the reconstruction, source pinning, concrete
  comparisons, claim runs, and negative mutations are preserved. The symbolic
  `indexOf` connection remains an explicitly limited trust boundary.

The successful `#Top` therefore proves a coherent but substituted
empty-pattern contract. It is not a legitimate proof of HumanEval/154 over its
real source-contract domain.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
