# Independent Stage 3 classification

The trusted lexical inventory reconstructed exactly seven local rules in the
`VERIFICATION` module closure, in source order, with inventory SHA-256
`03cd112179c09fbd3bee367ec800153a9171a0e1d7bedcc3f7d88ed7d49ecc52`.

| Source rule ID | Lines | Independent class | Reason |
|---|---:|---|---|
| `rule-ea80c64ba3e52dd72b25433dd6dd721d97e283355279ee9fc2a39f905f582faa` | 11-12 | `DEFINITION` | Base equation of the named recursive suffix summary `mergeThirdFrom`. |
| `rule-8eaaf331b2562006a2a6f4704a4b81a167862611d6c8b82d78a59369cb08a019` | 14-17 | `DEFINITION` | Divisible-by-three recurrence of `mergeThirdFrom`; the index increases and `N-I` decreases. |
| `rule-4860445cf3432071a9a322001c5e3ce052bb80b75147a784f2df24a8fbba41ca` | 19-22 | `DEFINITION` | Complementary non-third recurrence of the same named summary. |
| `rule-0855e7c5303f3b1835ec56db22a573c2fc2903b161c139dd7b0ff4a1d1ee9ed0` | 29-35 | `DEFINITION` | Folding equation naming the complete `mergeThirdFrom` term as `sortThirdResult`; it is a proof-term definition, not an MPY execution rule. |
| `rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2` | 37-39 | `DOMAIN_LEMMA` | Guarded zero-length consequence of the preceding summary definition. It is compiled before all Stage 1 proofs and is never first proved without itself. |
| `rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918` | 42-44 | `DOMAIN_LEMMA` | Associativity of the pre-existing `valSeqConcat`; Stage 1 gives no earlier rule-free K proof. |
| `rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9` | 47 | `DOMAIN_LEMMA` | Right identity of the pre-existing `valSeqConcat`; Stage 1 gives no earlier rule-free K proof. |

There are no local `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries.
`prove.sh` compiles `verification.k` with all seven rules before either
`kprove` command, so none of the last three meets the required two-stage
derived-lemma protocol. The three domain lemmas are relevant: the zero rule
handles the completed empty suffix and associativity/right identity normalize
the `append`-built loop accumulator. Every `[simplification]` rule is classified
as either `DEFINITION` or `DOMAIN_LEMMA`.
