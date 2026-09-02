# Independent Stage 3 classification

The trusted lexical reconstruction found one local verification module,
`VERIFICATION`, and 12 rules. The classifications below were assigned from the
frozen rule text and the imported MPY/K operational semantics, without using
the Stage 3 rationales.

| # | Source rule ID (digest prefix) | Span | Independent class | Reason |
|---:|---|---:|---|---|
| 1 | `rule-fa3b6a435d65…` | 9–11 | `DOMAIN_LEMMA` | A freshness-conditioned Map algebra equality for removing the just-added key. It defines no symbol and was present before the only `kprove` invocation, so it is not a proved derived lemma. It is relevant: `MPY-FUNCTIONS.#pop` changes `SC` to `SC [ L <- undef ]`, while `lpf-loop` must restore the surrounding `SC`. This is the only `[simplification]` rule. |
| 2 | `rule-10c6773e6fb…` | 16–27 | `DEFINITION` | Defines the named macro/proof term `solutionModule` as the exact AST of `solution.py`. |
| 3 | `rule-807a2bdf8a6d…` | 31–32 | `DEFINITION` | Defines the named loop-condition macro `lpfCondition`. |
| 4 | `rule-02e72de380e6…` | 35–40 | `DEFINITION` | Defines the named loop-step macro `lpfStep`. |
| 5 | `rule-aa140e57384e…` | 45–46 | `DEFINITION` | Base equation of the named recurrence `lpfSpec`. |
| 6 | `rule-29f515a98517…` | 47–49 | `DEFINITION` | Divisible branch of the named recurrence `lpfSpec`. |
| 7 | `rule-9c86e4c425a8…` | 50–51 | `DEFINITION` | Nondivisible branch of the named recurrence `lpfSpec`. |
| 8 | `rule-6a699c17f671…` | 58–70 | `OPERATIONAL_RULE` | Reads `n` and `factor` from the active scope and evaluates the loop comparison. |
| 9 | `rule-4baeb4eaecc4…` | 72–86 | `OPERATIONAL_RULE` | Reads the active scope and evaluates the remainder-equality observation. |
| 10 | `rule-e93503043807…` | 88–102 | `OPERATIONAL_RULE` | Executes the floor-division assignment and updates `n` in the scope. |
| 11 | `rule-d236b7171817…` | 104–117 | `OPERATIONAL_RULE` | Executes `factor += 1` and updates the scope. |
| 12 | `rule-2d861cadc329…` | 119–128 | `OPERATIONAL_RULE` | Executes return observation/control by storing `factor` and proceeding to `#pop`. |

No rule is a `PROVED_DERIVED_LEMMA`: `prove.sh` performs one compilation of
the full `VERIFICATION` module and then one `kprove`, so no listed rule was
first proved against a module that omitted it.

The independently assigned ordered class sequence is:

```text
DOMAIN_LEMMA,
DEFINITION, DEFINITION, DEFINITION, DEFINITION, DEFINITION, DEFINITION,
OPERATIONAL_RULE, OPERATIONAL_RULE, OPERATIONAL_RULE, OPERATIONAL_RULE,
OPERATIONAL_RULE
```

It exactly matches the protected Stage 3 sequence.
