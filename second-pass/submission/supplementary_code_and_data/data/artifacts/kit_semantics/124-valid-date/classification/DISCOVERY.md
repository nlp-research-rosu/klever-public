# Trust-boundary discovery

## Canonical inventory

The sole rule inventory used for this classification is
`/reference/rule-inventory.json`, with canonical inventory SHA-256
`1e1e11bd9e60b6563190fbf01074626066c574d662f30b073201e87b2c31a316`.
It lists five rules, all in `VERIFICATION`, and every one appears exactly once
in `trust-boundary.json` in the canonical order. Every inventory entry has an
empty `attributes` array, so there are no `simplification`-attributed rules to
classify.

## Classification reasoning

All five rules are `DEFINITION`:

1. `rule-415033600c05a74b967858910de7e6f137b7072cad657a6ac7aa4017632c1851`
   is the unconditional expansion of the named term `validDateProgram` into
   the MPY `Module` AST. It defines a structural proof/source term; the
   imported MPY rules, not this equation, perform module loading and program
   execution.
2. `rule-95075d83a0bfc357491c9ebdd73471597f5d3d7efa19b7eed607a527de6e57c6`
   defines `asciiDigit(C)` as the integer interval from 48 through 57.
3. `rule-213d2e3601b35f7d452f718a58bb49a80abbaf99a4343a8c4ba60f3309dc0cbd`
   defines `validMonthDay(M,D)` by the February, 30-day-month, and
   31-day-month cases.
4. `rule-d8a4e28b9a30919ceb03d02944cfc337efe8eb8e81474a454172b2d68b6bf2aa`
   defines the non-length-10 case of `validDateResult`.
5. `rule-000f1433c33376dfa1807ad42ebb0d8821bd71fb57e744c08fcbe1308f5d50cf`
   defines the complementary length-10 case of `validDateResult` by expanding
   it into separator, digit, month, and day predicates.

None of these rules is an `OPERATIONAL_RULE`: none has a configuration cell,
execution continuation, state observation, or operational transition on its
left-hand side. The first constructs program syntax, while the other four
define mathematical result predicates.

## Separately proved derived lemmas

There are no `PROVED_DERIVED_LEMMA` entries.

The mounted Stage 1 `prove.sh` first compiles `verification.k`, which already
contains all five canonical rules, and then proves `SPEC.valid-date-10` and
`SPEC.valid-date-non10` against that compiled definition. It does not prove
the exact statement of any inventory rule against a module from which that
rule is absent. The later February body mutation and false-result checks are
expected-failure sensitivity probes; neither establishes a reusable rule.
Consequently, Stage 1 contains no evidence satisfying the required
prove-before-import ordering for a derived lemma.

## Domain lemmas

The domain-lemma set is empty. No canonical rule adds a mathematical fact
beyond the definitions of the named program term and result predicates.
