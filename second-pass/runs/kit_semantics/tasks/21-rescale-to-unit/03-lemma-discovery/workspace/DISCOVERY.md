# Trust-boundary discovery

## Canonical input

This classification uses `/reference/rule-inventory.json` as the exhaustive
rule set. Its copied inventory digest is:

```text
92208488f5b3fbe4f881489dcbdba726ef2025162d4234a071210c0a94048c89
```

The inventory names one local module, `VERIFICATION`, and contains 27 rules.
`trust-boundary.json` preserves the canonical order and contains every
`source_rule_id` exactly once.

## Classification result

| Classification | Count |
|---|---:|
| `DEFINITION` | 25 |
| `OPERATIONAL_RULE` | 0 |
| `PROVED_DERIVED_LEMMA` | 0 |
| `DOMAIN_LEMMA` | 2 |
| Total | 27 |

### Definitions

The following rules are equations or terminating structural recurrences that
define a mathematical summary or named proof term:

- `rule-78f2a049ece805815d21e9063a74aff75f3d53f22a84a77fea64ffc91042a363`
  and
  `rule-868b8e62acc1401467478a403823568e5a884588da8cafb025ea2f898fb18fae`
  define the empty and constructor cases of `allFloatVS`.
- `rule-9a463fce3138a197dad8680039821fa743198e2199ab369aea9182134fd7a300`
  defines `definedProjectFloat`.
- `rule-64da4543da040ecadafcb80fe5586bccd61f336d51e2d69f8be37eff9757ed31`
  defines the identity case of `projectFloatTotal`.
- `rule-aa23fe12f81b217a7753242f092b83ac06262b380fcc07c5124ad5d3b540c6a2`
  and
  `rule-fbd51e78fb687e3dfa1e45a42973fd6b24a7d33ac9f67f1c65d09dbe0bf95338`
  are the concrete and symbolic orientations of the same guarded equation
  defining `projectFloatTotal` as the existing partial Float cast.
- `rule-98a366fb8c0e17ff8cd2ea3ecae7289130e9ac5e4646bc2f29025efad568dcbd`
  and
  `rule-671581927eda863f8e972b71f3e77752d3878e2f986b1dc7be6e637b838186b5`
  are definitional aliases that name the supplied `minFloat` and `maxFloat`
  operations with the proof-local opaque terms `minFOpaque` and
  `maxFOpaque`. This classification names the terms; it does not independently
  prove a numerical property of the opaque primitives.
- `rule-22cecd17d8c6d259e2d837004f0da8b773f994451c2d3f1caf4d3771ca493239`
  through
  `rule-fd99ddec1b1164da6fb41c79041f64caaa2ff613c6029d728e390082dff4ff8f`
  define the base, in-domain recurrence, and off-domain totalization cases for
  `minTailF`, `maxTailF`, `minVF`, and `maxVF`.
- `rule-6df20a8292c3b9e153217f88a855d2402c52d0210cfffac310d57d1e5d4ce947`,
  `rule-67e4a4034062128db725d895c647028b34e93bc7ddc597d290b2d6350afb9ad0`,
  and
  `rule-f602ef7b0d123be49839f9acdf43d0249cead55ad81ff3f423c136969fa6bf9c`
  define `scaleAcc`.
- `rule-b0d12452e0d35223a5064e4c1cef7b5996529e7b88c99a39c3bc66d4382aa0db`
  and
  `rule-55b5808dde3db4136e57b92991d02e6c066106cede4ab49d9dd346e9e4259c5f`
  define `lastVal`.

The recursive definitions consume one `ValSeq` constructor in each recursive
case. Their guarded in-domain and off-domain cases are disjoint.

### Operational rules

The `OPERATIONAL_RULE` set is empty. The canonical local inventory contains no
ordinary configuration or observation rule. The one rule mentioning the
existing operational dispatcher, `applyBin`, carries `simplification`, so the
requested classification constraints require it to be either a definition or
a domain lemma; it is classified as a domain lemma below.

### Separately proved derived lemmas

The `PROVED_DERIVED_LEMMA` set is empty.

There is no Stage 1 proof evidence satisfying the required ordering. In
`/reference/k-proof/prove.sh`, lines 19–22 compile `verification.k` with all 27
rules. Only afterward do lines 24–26 run `kprove spec.k` against that compiled
definition. The vacuity and body-mutation probes at lines 34–59 reuse the same
compiled definition. Consequently:

- no exact inventory rule statement is first proved in a module that omits the
  rule;
- `target-proof.log` containing `#Top` proves claim closure under the full rule
  set, not any inventory rule independently; and
- the expected-failure mutation logs test result constraint and body
  sensitivity, not an exact reusable rule statement.

Therefore no rule is promoted to `PROVED_DERIVED_LEMMA`, even where Stage 1
comments or `PROOF.md` use words such as “derived lemma.”

### Domain lemmas

The domain-lemma set is **not empty**. It contains exactly two rules:

1. `rule-57727b2acd45f64e74f4c2582f643b13345834dfbe7bf3fe97580d59dcd8ba43`
   characterizes `#Ceil` of the existing partial Val-to-Float cast. This is an
   additional definedness fact about an existing K construct, not merely a
   recurrence defining a fresh summary.
2. `rule-dc58f41e482527dda6d5bd7e29f533ee71f5356475fa5bfad6f9142925059957`
   extends the existing Float subtraction dispatch equation to a dynamically
   sorted `Val` under `isFloat(V)`. It is an additional fact about the existing
   `applyBin` operation.

Both carry a `simplification` attribute and have no prior exact,
rule-omitting Stage 1 proof. They are therefore trusted `DOMAIN_LEMMA` entries,
not `PROVED_DERIVED_LEMMA`.

## Simplification-rule check

The seven canonical rules carrying `simplification` are classified only as
permitted:

- `DEFINITION`: the three `projectFloatTotal` equations/orientations and the
  two opaque min/max aliases;
- `DOMAIN_LEMMA`: the cast `#Ceil` characterization and dynamic subtraction
  equation.

No simplification rule is classified as `OPERATIONAL_RULE` or
`PROVED_DERIVED_LEMMA`.
