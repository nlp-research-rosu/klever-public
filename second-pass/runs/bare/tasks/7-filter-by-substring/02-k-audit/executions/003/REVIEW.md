# Independent adversarial review: 7-filter-by-substring

The candidate is **not a legitimate partial-correctness proof of the HumanEval
contract**. Fresh reconstruction does confirm the reported six `#Top` results,
and the program term is pinned to the trusted translation. Those facts are
insufficient for two independent reasons:

1. The generated semantics is materially wrong on a valid source-domain
   boundary: with `strings=[""]` and `substring=""`, both Python
   implementations return `[""]`, while the rebuilt K semantics returns
   `Nil`.
2. No candidate entry claim states and closes the unrestricted
   program-to-reference postcondition. The arbitrary-input entry claim stops at
   the internal evaluator; the base/step claims assume the induction hypothesis
   as a precondition. A fresh direct universal target gets stuck on the
   unproved symbolic-list equality.

## 1. Input and provenance integrity

I first read `/audit-input.json`. It declares
`record_layout=legacy-selected-stage1`, condition `bare`, and
`semantics_mode=GENERATED_SEMANTICS`. I used only its `container_paths`; the
host provenance paths were not treated as container paths.

The required launcher records are present, readable regular files and not
symlinks:

- `/audit-input.json`, `/audit-campaign-lock.json`, `/run.json`,
  `/task.json`, and `/generation-result.json`;
- `/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
  `codex-output.log`, and `prompt.txt`;
- the structured trace containing 422 valid JSONL records below
  `/generation-evidence/codex-trace/`;
- `usage.json`, which is present and was therefore inspected.

Historical `runtime-metrics.json` is absent, but this is explicitly permitted
for `legacy-selected-stage1`; I did not reconstruct it or count it as a defect.
The generation records were used only as untrusted claims. Their prior report
that six commands produced `#Top` was independently tested in stage 3.

The campaign object in `/audit-input.json` is semantically equal to
`/audit-campaign-lock.json`, and the lock's independently observed SHA-256 is
the recorded
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
The regular-file hashes for the canonical source, prompts, translators,
manifests, generation logs, usage, and trace file match their recorded values.
In particular:

| Artifact | Independently observed SHA-256 |
|---|---|
| `/reference/canonical.py` | `dbf22c38a828341a9c3cbcc30ea965e727c25b527f78a554abfbc347e228bd33` |
| trusted and candidate `prompt.py` | `5eecb2c6bb2b4fcd70989d66291a7c4c02d3afbf31591ad684e926a1e60ee969` |
| trusted and candidate `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` |
| `invocation.json` | `4bfb339557a099f58b2418c3250975dab47706296730079e0fcf7a2227cd0d24` |
| `metrics.json` | `d0015c64fed2c18442ac14d83310992ed6e890066b7319e20fc8ee0e3103174c` |
| `usage.json` | `192e78b6dee7b22b3a45c32ff19c9ad3bc13dcb26a2f753116af9a9f1af0d983` |
| `codex-output.log` | `4e1ca774fcdf73e82ddf1e14eb7afddee803535152a610840bf88568bfe2b864` |
| structured trace file | `f4eccf4ffbdab3703acbd85c841931bb2eb816462c9bf1e44b69633f80efa721` |
| `/run.json` | `16ab5496e5b7251ecd747d4b58693a614cb2f6d680317214f597d0437ab39c24` |
| `/task.json` | `26b3c229c17a51bb89c1634e50478e4b5e015b0aeacf1285b2a513c7cf4654f1` |
| `/generation-result.json` | `a4b6e19c8ae72d5ec3f820395480caef7f54fd924007e90b6747a8f23e9997ae` |

Using the pipeline tree-hash implementation, the mounted candidate hashes to
`e0fb514f85cefa15af6d674efc35a7f462d9600eb8cd68b72f86ce587b371048`,
exactly the workspace digest in both `invocation.json` and
`generation-result.json`. The structured trace tree similarly hashes to
`a3373dbcefa4261cf685d6cee840d8734f88c2f3d1c28a6de029eec50f936135`,
matching `usage.json`'s source-trace digest. The audit-input also carries
launcher-level directory fingerprints under a different serialization; the
entry-by-entry regular-file, type, and symlink checks above are independent of
those aggregates.

No symlink exists under `/candidate`, `/reference`, or
`/generation-evidence`. The candidate has every required proof source artifact:
`solution.py`, `solution.mpy`, `semantic.k`, `verification.k`, `spec.k`, and
`prove.sh`. Candidate `prompt.py` and `py2mpy.py` are byte-identical to their
trusted mounts.

The generated-semantics boundary is intact:
`/reference/reference-semantics` does not exist. I did not search for or use a
hidden reference semantics. There is therefore no audit infrastructure breach.

Evidence:
[provenance commands and hashes](evidence/stage1/check_provenance.log) and
[bounded generation-record/trace inspection](evidence/stage1/inspect_generation_records.log).

## 2. Program fidelity and candidate-versus-canonical checks

The trusted prompt and canonical implementation require
`filter_by_substring(strings: List[str], substring: str)` to return, in original
order and with duplicates preserved, exactly those input strings for which
Python evaluates `substring in string` to true. The type-hinted domain is not
bounded. Empty lists, empty strings, and an empty substring are valid.

`solution.py` implements:

```python
return [string for string in strings if substring in string]
```

This is the same algorithm and behavior as the trusted canonical comprehension.
Running the trusted translator on the scratch copy produced a 323-byte term
byte-identical to submitted `solution.mpy`; both have SHA-256
`03ce6c305c9520c8bb56a7c65fbfff1316e16bc1007e005af3665b2774e60866`.

The independent differential test imported the trusted and candidate entry
points from explicit paths. It covered both prompt examples, empty list,
empty substring, empty haystack, exact/prefix/middle/suffix/nonmatches,
substring-longer-than-haystack, duplicates, controls, NUL, composed and
decomposed Unicode, and emoji. It then exhausted lists of lengths 0–2 over
eight representative strings and eight substrings, plus 400 seeded lists of
length 0–8. Result: 1,000 cases, zero mismatches.

This supports program fidelity but is finite evidence, not the K proof.
Evidence:
[differential script](evidence/stage2/differential_test.py) and
[translation/differential log](evidence/stage2/run_fidelity.log).

## 3. Clean proof reconstruction

I copied only proof sources and trusted inputs to `/tmp/audit-work`. I did not
copy or use candidate `.kbuild` content. From scratch I ran:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX --output-definition concrete-kompiled
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module SEMANTIC-SYNTAX --output-definition proof-kompiled
```

Both builds exited 0 under K 7.1.293. Every positive label was selected in its
own command:

- `UNIVERSAL-PROGRAM-REDUCTION`: exit 0, exact `#Top`;
- `UNIVERSAL-BASE`: exit 0, exact `#Top`, with `WarnTrivialClaim`;
- `UNIVERSAL-STEP-KEEP`: exit 0, exact `#Top`, with `WarnTrivialClaim`;
- `UNIVERSAL-STEP-DROP`: exit 0, exact `#Top`, with `WarnTrivialClaim`;
- `EMPTY-EXAMPLE`: exit 0, exact `#Top`;
- `PROMPT-EXAMPLE`: exit 0, exact `#Top`.

Thus the old `#Top` report is reproducible, but only for the claims actually
written.

Fresh concrete execution matched both prompt cases, an all-drop case, and a
Unicode case. It exposed this decisive boundary divergence:

```text
Input:       strings=[""], substring=""
Canonical:   [""]
Candidate:   [""]
Rebuilt K:   Nil
```

A larger witness, `strings=["x","x",""]` and `substring=""`, likewise produces
`["x","x"]` in K instead of Python's `["x","x",""]`. This is a normal
terminating execution, not a parser error, timeout, or container uncertainty.
The aggregate reconstruction script exits 1 precisely because these
Python-versus-K comparisons fail; both definitions built and all six individual
proof commands still exited 0.

Evidence: [fresh build, concrete execution, and all six proof logs](evidence/stage3/clean_rebuild.log).

## 4. Adequacy and real-program pinning

### Claim meanings and satisfiable states

| Claim | Plain-language precondition | Plain-language postcondition | Satisfying witness |
|---|---|---|---|
| `UNIVERSAL-PROGRAM-REDUCTION` | Any finite K `PyList` of strings and any K string | Exact submitted program reduces to internal `evalComp(INPUT, substringFilter(SUBSTRING))` | `INPUT=Nil`, `SUBSTRING="a"` |
| `UNIVERSAL-BASE` | Any substring | Internal evaluator on `Nil` reaches `filterRef(Nil,substring)` | `SUBSTRING="a"` |
| `UNIVERSAL-STEP-KEEP` | Membership is true and tail evaluator equals tail reference | One kept-head evaluator step reaches the reference result | `HEAD="a"`, `TAIL=Nil`, `SUBSTRING="a"` |
| `UNIVERSAL-STEP-DROP` | Membership is false and tail evaluator equals tail reference | One dropped-head evaluator step reaches the reference result | `HEAD=""`, `TAIL=Nil`, `SUBSTRING="a"` |
| `EMPTY-EXAMPLE` | Fixed realizable call `([], "a")` | Result is `Nil` | Its fixed source state |
| `PROMPT-EXAMPLE` | Fixed realizable prompt call | Result is `["abc","bacd","array"]` | Its fixed source state |

The candidate does pin the immutable program term. Removing whitespace from
trusted-regenerated `solution.mpy` and from the `solutionProgram` rule's RHS
gives identical constructor-token sequences, including function name, binding,
parameters, return body, generator, and membership operator. The omitted
dynamic treatment of `ImportFrom("typing","List")` is inert for this program.

A body-sensitivity mutation changed the *executed constructor term* by making
the comprehension iterate over `Name("substring")` instead of
`Name("strings")`. The mutated definition built, but
`UNIVERSAL-PROGRAM-REDUCTION` exited 1 with `WarnStuckClaimState` at the altered
`evalList(Name("substring"), ...)`. This is real body sensitivity, not merely a
change to an unused external Python file.

The adequacy failure is the postcondition. The arbitrary-input entry claim
constrains the result only to an internal evaluator, not to the intended filtered
list or even `filterRef`. The base and step claims are separate helper
obligations; the steps put tail equality in `requires`. No candidate claim
states:

```k
execute(solutionProgram, "filter_by_substring", INPUT, SUBSTRING)
  => filterRef(INPUT, SUBSTRING)
```

A fresh reviewer-authored claim with exactly that postcondition built but
exited 1 with `WarnStuckClaimState`; its residual was
`evalComp(INPUT,substringFilter(SUBSTRING))` versus
`filterRef(INPUT,SUBSTRING)`. The base/step obligations can motivate an
informal meta-level structural induction, but the submitted K proof does not
machine-check the composed universally quantified reachability theorem.

Even granting that informal induction does not repair the real-program bridge.
Substituting the satisfying intended-domain state
`INPUT=Cons("",Nil), SUBSTRING=""` into the claimed evaluator produces `Nil`;
both Python implementations produce `Cons("",Nil)`.

Evidence:
[constructor comparison, body mutation, and direct universal-target probe](evidence/stage4/check_pinning_and_body_sensitivity.log).

## 5. Rule-by-rule static soundness review

There are no generated helper K files. The complete local inventory contains:

- 18 source/runtime syntax declarations in `SEMANTIC-SYNTAX`;
- one single-cell configuration and two further internal constructors;
- seven semantic functions, of which only `evalComp` is locally `total`;
- `solutionProgram [function]` and `filterRef [function,total]`;
- 13 rules in `semantic.k` and four in `verification.k`;
- no local `[functional]`, simplification, priority, `owise`, `anywhere`,
  fresh, or opaque declaration.

Every constructor in submitted `solution.mpy` maps to declared syntax.
Execution uses the import-skip, function lookup, return extraction, argument
binding, name lookup, specialized list-comprehension, structural filter, and
membership rules. The pure source body needs no heap, I/O, exception, or
observable local-variable cell. The specialized comprehension rule matches the
target name consistently in element, generator, and condition, fixes the
operator to `"in"`, preserves order and duplicates, and recursively descends.
Because its subexpressions are pure name lookups, the skipped generic
evaluation contexts have no material state/control effect for this exact term.
It is narrow generated semantics, not an unconstrained result oracle.

The lookup match/nonmatch guards are disjoint on the used module. The
`evalComp` and `filterRef` keep/drop guards are complementary; both recursive
definitions descend on `TAIL`, and their Nil/Cons cases cover the local
`PyList` constructors. The `total` declarations therefore have structural
coverage. Broader Python behavior such as imports with effects, duplicate
function rebinding, or multi-statement bodies is unsupported, but those
constructs are unused and are not defects under the generated-semantics
boundary.

One used rule is materially unsound as a model of Python:

```k
rule containsString(HAYSTACK, NEEDLE)
  => findString(HAYSTACK, NEEDLE, 0) >=Int 0
```

Concrete false-conclusion witness on the intended domain:

```text
HAYSTACK = ""
NEEDLE   = ""
Python conclusion: contains = True
K-enabled program conclusion: the head is dropped, result Nil
Required result: Cons("",Nil)
```

This witness is directly reachable in the submitted program. It is not a claim
about an unused extension. The `filterRef` keep/drop equations are internally
consistent with `containsString`, but that makes `filterRef(Cons("",Nil),"")`
reduce to `Nil`; it is therefore not the requested Python reference property at
the witness. The same defective predicate appears in execution and reference,
so equality between those two local functions cannot establish Python
membership semantics.

Imported K maps, Booleans, integers, strings, collection syntax, K equality,
and backend reasoning are the ordinary low-level trust boundary. No fresh or
opaque value influences a branch or result.

Evidence:
[exhaustive declaration/rule inventory with per-rule assessments](evidence/stage5/rule_inventory.md)
and [numbered source inventory](evidence/stage5/inventory_sources.log).

## 6. Fresh non-vacuity test

There was no candidate `spec-vacuity.k` to trust. I created a fresh module in
scratch that keeps the fixed prompt input but falsely requires the output to
include `"cde"`, which does not contain `"a"`.

The mutation's `kprove --dry-run` exited 0, establishing successful parsing and
proof-artifact construction. The real proof command then exited 1 with
`WarnStuckClaimState`. Its residual was the correct terminal result:

```text
Cons("abc", Cons("bacd", Cons("array", Nil)))
```

That is the expected unmet result obligation, not an unrelated error. The fixed
input has no precondition and is realizable. Thus the concrete entry claim is
discriminating and non-vacuous. This result does not supply the missing
universal theorem or validate the false substring bridge.

Evidence:
[false mutation](evidence/stage6/spec-vacuity.k) and
[build/proof log](evidence/stage6/run_false_mutation.log).

## 7. Proven versus assumed accounting

The successful reachability proofs establish only the following, conditional
on the generated K theory:

1. Exact-program execution reduces, for arbitrary K list/string inputs, to the
   local `evalComp` summary.
2. `evalComp` and `filterRef` agree at Nil and for one Cons step when their tail
   equality is already assumed.
3. Two concrete program calls reach their stated outputs.

They do **not** establish that every terminating Python call returns exactly the
source-contract filter result.

Trusted/assumed boundaries are:

- the trusted prompt, canonical source, and translator;
- exact byte regeneration and constructor comparison;
- K 7.1.293's parser, compiler, backends, and standard Map/Bool/Int/String/K
  definitions;
- a finite 1,000-case Python differential bridge;
- an informal structural-induction composition not represented by a successful
  universal K entry claim;
- the attempted `findString`-to-Python-membership bridge, which is not merely
  unproved but concretely false.

The first three are acceptable conventional or mechanically checked
boundaries. Differential testing supports only candidate-versus-canonical
behavior on its recorded cases. The informal induction is a material proof
gap. The false membership bridge is illegitimate because it changes the result
on the intended typed domain.

In Kit terms, Gate A fails despite successful body sensitivity and non-vacuity:
the semantics can prove/execute a false intended-domain result. Gate B also
fails: the contract includes the empty/empty boundary, and no successful
arbitrary-input entry claim has the intended postcondition. Gate C evidence is
reproducible but cannot repair either failure. The benchmark decision boundary
therefore requires `FAIL / NOT_LEGIT`, not `CONCERNS`.

The complete trust ledger is preserved at
[evidence/stage7/trust_ledger.md](evidence/stage7/trust_ledger.md).

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
