# Trust-boundary discovery

## Scope and method

`/reference/rule-inventory.json` is treated as the exhaustive canonical
inventory. It contains 29 rules, all in module `VERIFICATION`. The output keeps
their canonical order and copies inventory SHA-256
`86637211d8eb42b498d51f829d1bcd21ab5987f93b26ba91a4a35193e5b3824b`.

Classification totals are:

| Classification | Count |
|---|---:|
| `DEFINITION` | 24 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 5 |

The structural recurrences and guarded cases for `allInts`,
`definedProjectInt`, `projectIntTotal`, `magnitude`, `decimalCodes`,
`allDigitCodes`, `codeDigitSum`, `chooseFirst`, `lastCode`,
`signedDigitSum`, and `countNumsSpec` are `DEFINITION`. This includes the
guarded cast/projector orientations and projector normalization equations:
they define or normalize the newly named total-projection proof term. The
`strToCodes(Int2String(N)) => decimalCodes(N)` rule is also a definition: it
names the otherwise opaque fixed primitive result; by itself it asserts no
digit property or particular decimal value.

No canonical rule is classified `OPERATIONAL_RULE`. The inventory contains no
ordinary configuration-level execution rule from the supplied semantics.
Although three local simplifications rewrite existing observation/dispatch
symbols (`applyCmp`, `applyUn`, and `applyBuiltin`), the prompt requires every
rule carrying `simplification` to be either `DEFINITION` or `DOMAIN_LEMMA`.
Those three rules add unproved correspondence facts rather than definitions of
new summaries, so they are `DOMAIN_LEMMA`.

All 11 rules carrying a `simplification` attribute satisfy that restriction:
six are `DEFINITION` and five are `DOMAIN_LEMMA`.

## Separately proved derived lemmas

The separately proved derived-lemma set is empty.

Stage 1's `/reference/k-proof/prove.sh` first compiles `verification.k` into
`verification-kompiled`, with all 29 canonical rules already present. It then
runs `kprove` on the seven reachability claims in `spec.k`. The positive logs
`kprove-entry-nonempty.log` and `kprove-entry-empty.log` contain `#Top`, but
they prove those reachability claims under the already-extended verification
module.

There is no Stage 1 command that:

1. constructs a module omitting one of the canonical rules;
2. proves that rule's exact statement against that rule-free module; and
3. only afterward imports the proved rule for the target proof.

The false-postcondition and body-mutation commands are negative validation
probes, not exact rule proofs. Consequently, neither comments such as
"derived lemma" nor successful target claims qualify any inventory rule as
`PROVED_DERIVED_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these five rules:

1. `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43`
   characterizes the definedness of the built-in partial `Val`-to-`Int` cast
   using `definedProjectInt`. This is an additional type/domain fact about K's
   cast, not a definition of the existing `#Ceil` observation.

2. `rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69`
   lifts integer `<` dispatch from a dynamically sorted `Val` to
   `projectIntTotal(V)`. It restates intended fixed-semantics behavior, but
   Stage 1 does not first prove the exact lifted statement without the rule.

3. `rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2`
   similarly lifts unary integer negation from dynamic `Val` to the projected
   `Int`, without a prior exact rule-free proof.

4. `rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da`
   connects the existing `str` builtin on a dynamically sorted nonnegative
   integer value to `str(decimalCodes(...))`. This result-bearing bridge is
   present during every Stage 1 positive proof and has no prior exact
   connection theorem in a module that omits it.

5. `rule-5af48b88759940f404acea3042b6fa69d00290648ae1c95910aaad61bea89344`
   asserts that `decimalCodes(N)` contains only ASCII digit codes for
   `N >= 0`. Stage 1 explicitly identifies this as its value-level primitive
   contract. Concrete and differential tests support it only finitely; they do
   not prove the universal rule.

These five trusted facts are precisely the rule-level trust boundary exposed
by the canonical local inventory. The supplied reference semantics, translator,
K implementation, and solver remain broader meta-level trust assumptions, but
they are not canonical rule entries and therefore are not added to the JSON.
