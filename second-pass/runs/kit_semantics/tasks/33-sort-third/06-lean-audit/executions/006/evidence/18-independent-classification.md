# Independent Stage 3 classification

The trusted lexical inventory reconstructs one local module in the selected
closure, `VERIFICATION`, and seven rules. The classification below was made
from frozen `verification.k`, `spec.k`, the source solution, and the supplied
semantics, without accepting the protected classifications as judgments.

| Source rule ID | Span | Independent class | Judgment |
|---|---:|---|---|
| `rule-ea80c64ba3e52dd72b25433dd6dd721d97e283355279ee9fc2a39f905f582faa` | 11–12 | `DEFINITION` | Base equation of the new `mergeThirdFrom` summary. |
| `rule-8eaaf331b2562006a2a6f4704a4b81a167862611d6c8b82d78a59369cb08a019` | 14–17 | `DEFINITION` | Divisible-by-three recursive equation of that summary. |
| `rule-4860445cf3432071a9a322001c5e3ce052bb80b75147a784f2df24a8fbba41ca` | 19–22 | `DEFINITION` | Complementary recursive equation of that summary. |
| `rule-0855e7c5303f3b1835ec56db22a573c2fc2903b161c139dd7b0ff4a1d1ee9ed0` | 29–35 | `DEFINITION` | Folding macro that names the exact complete summary `sortThirdResult(VS)`. |
| `rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2` | 37–39 | `DOMAIN_LEMMA` | Guarded zero-length consequence for the already named result summary. It is compiled before all claims and is never first proved without itself. |
| `rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918` | 42–44 | `DOMAIN_LEMMA` | Associativity of the supplied `valSeqConcat`; it is a mathematical law, not an equation defining that supplied function, and is not separately proved first. |
| `rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9` | 47 | `DOMAIN_LEMMA` | Right identity of the supplied `valSeqConcat`; likewise not separately proved first. |

There are no ordinary operational rules or proved-derived lemmas in the local
closure. All four `[simplification]` rules are either a definition (the fold)
or a domain lemma. The three domain lemmas are relevant: the zero-length rule
connects the empty execution to the named postcondition, while associativity
and right identity normalize the append-built loop result used by the loop
invariant and final result.
