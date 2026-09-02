# K proof trust-boundary discovery

The canonical inventory hash is
`3182719aa6a75a97355b7da5124d9c650a433fe9651a56b982053fc2b391951e`.
All 36 inventory rules are classified exactly once and in canonical order in
`trust-boundary.json`.

## Classification summary

| Classification | Count | Inventory members |
|---|---:|---|
| `DEFINITION` | 32 | Rules 0–10 and 14–34 |
| `OPERATIONAL_RULE` | 0 | None |
| `PROVED_DERIVED_LEMMA` | 1 | Rule 35, source ID `rule-8ff240867a86bc6a27c0862a6048100b3c2a0d8136feb76d147705805fdcb5ef` |
| `DOMAIN_LEMMA` | 3 | Rules 11–13 |

The definitions comprise four AST macro expansions; recognizers and
projections; complementary equations for ordering, winner selection, and
accumulator updates; and structurally decreasing inner, outer, and last-item
folds. These equations name syntax or mathematical summaries and do not
themselves rewrite a running `<k>` computation.

There are no unproved local execution or observation rules classified as
`OPERATIONAL_RULE`. The only local rule that rewrites running computation is
the inner-loop bridge, and the Stage 1 artifacts meet the stronger
separately-proved-derived-lemma condition described below.

## Separately proved derived lemma

Exactly one inventory rule is a `PROVED_DERIVED_LEMMA`:

- `rule-8ff240867a86bc6a27c0862a6048100b3c2a0d8136feb76d147705805fdcb5ef`
  is the priority-40 inner `#loop` transition in module `VERIFICATION`.
  Its left side fixes the iterable, target, exact `innerBody`, environment,
  builtins, function closure/body, local bindings, accumulator shape, and
  guard. Its right side and cell updates are the same as claim
  `CONNECTION-SPEC.inner-loop-connection`.

The Stage 1 proof evidence establishes the required ordering and exclusion:

1. `prove.sh` first compiles `verification.k` with
   `--main-module VERIFICATION-BASE` into `connection-kompiled`.
   `VERIFICATION-BASE` ends before the bridge; the bridge is declared only in
   the later `VERIFICATION` module.
2. It then runs
   `kprove connection-spec.k --definition connection-kompiled --spec-module CONNECTION-SPEC`.
   Stage 1 `PROOF.md` records `#Top` and exit 0 for this command.
3. Only after that successful connection proof does `prove.sh` compile
   `--main-module VERIFICATION`, which introduces the reusable priority-40
   rule, and prove the target `spec.k`.
4. The mounted compiled rule inventories corroborate exclusion:
   `connection-kompiled/allRules.txt` has 861 entries and
   `verification-kompiled/allRules.txt` has 862; the sole added entry points
   to `verification.k:255:8`, the bridge's source location.

The claim writes the fixed reference helper `builtinsScope`, while the rule
writes its equation-expanded scope map. The supplied
`reference-semantics/semantics/core.k` defines exactly that expansion, so the
compiled reachability statement and reusable rule correspond modulo
definition expansion and variable alpha-renaming. The remaining cells and
arbitrary continuation are framed in both.

The earlier fixed-semantics projection command is not evidence for another
`PROVED_DERIVED_LEMMA` classification. `projection-spec.k` proves concrete
tuple projection claims against `MPY`, but the inventory rules are guarded
`[simplification]` rewrites and the required classification constraint places
every simplification rule in `DEFINITION` or `DOMAIN_LEMMA`.

## Domain lemmas

The domain-lemma set is **not empty**. It contains exactly these three
`[simplification]` rules:

- `rule-db9d3a3e81dee21bb05c9f3240b23092771092e55e7bb6f53dc9fdcfa44b3188`:
  guarded index-0 projection from imported `applyIndex` to `itemIndex`;
- `rule-c31085d90cc1a95717c3310bccb50623ab127a57e9e6010eb23e0aa2e4377dc7`:
  guarded index-1 projection from imported `applyIndex` to `itemFloat`;
- `rule-1be94e05a1b1440cd44a316053a753efc65fc522fcdf2fd8218e40d546231a89`:
  the cross-function fact that enumerating an `allFloatVS` sequence produces
  an `allFloatItems` sequence.

They are additional mathematical facts used by symbolic simplification, not
recurrences defining the imported operations at their heads. The first two
have supporting fixed-semantics projection claims in `projection-spec.k`; the
third has no separately ordered, bridge-free claim in `prove.sh`. Under the
requested exhaustive taxonomy, all three therefore remain in the trusted
domain-lemma set rather than being reported as proved derived lemmas.
