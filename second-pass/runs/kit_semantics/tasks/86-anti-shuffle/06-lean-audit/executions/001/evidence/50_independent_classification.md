# Independent classification

The trusted inventory reconstruction contains exactly nine rules in the local
`VERIFICATION` closure.  The classifications below are based on the frozen
source and supplied operational semantics, not the protected Stage 3 labels.

| Source rule | Lines | Independent class | Reason |
|---|---:|---|---|
| `rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1` | 8–12 | `DOMAIN_LEMMA` | `strLt` is not introduced by `verification.k`; it is an existing supplied-semantics function declared in `semantics/str.k:48` and defined operationally at lines 49–54.  The added `[simplification]` equation compresses those existing cases for two singleton strings.  It is therefore a theorem about the domain operation, not a definition of a summary, recurrence, macro, or named proof term.  It is directly relevant: source line 17 compares the singleton `char` and `old_char` values emitted by string iteration. |
| `rule-dc6f73badfec4f23e1af1f381ddb673851960f3a7dd453b5a529e29eea13dbc1` | 21–33 | `DEFINITION` | Sole equation for the fresh zero-argument proof-term/macro `antiInnerBody`; its RHS is the exact inner-loop AST fragment. |
| `rule-d8c6975c42f7acfdc026a371bbd271bff09144d250d960f6b474f010e3a77c91` | 35–43 | `DEFINITION` | Sole equation for the fresh zero-argument AST macro `antiPostInsert`. |
| `rule-0f9f3b5d7e5349a6b9e4e08ae6ff00e9b64d8642453a18a90ada8eea2bfa6d08` | 45–56 | `DEFINITION` | Sole equation for the fresh zero-argument AST macro `antiOuterBody`. |
| `rule-5075fc023e8cdbd37d170a98412b835adec6946ebd2141dee39edbea6eb0d8ad` | 58–61 | `DEFINITION` | Sole equation for the fresh zero-argument AST macro `antiTail`. |
| `rule-c4913eca7f7a04a7ced779f502220f126d5ee7b0ee403b488e8b7e5329129ccb` | 68–72 | `DEFINITION` | Empty-input/base equation for the fresh insertion summary `insertGo`. |
| `rule-f0184627a2c4a3d544b5b84141379073793a96b835d2753217df57bda16c9883` | 73–91 | `DEFINITION` | Constructor/recursive equation for `insertGo`; it consumes the head of the old word and exactly models the source insertion step. |
| `rule-652e6e29910efceeca6a31b0b63ec16bfe1d38ac2b9054d6d2a69a37ba8dcec4` | 95–96 | `DEFINITION` | Empty-input/base equation for the fresh whole-loop summary `antiGo`. |
| `rule-6e83d7b52d40fb31d78ba87b9b7e825cf4ae9515a0fa193cce3b0b083ee08657` | 97–107 | `DEFINITION` | Constructor/recursive equation for `antiGo`; it consumes one input code and defines the space/non-space transitions. |

For the singleton `strLt` rule, the supplied equations establish:

- if `C <Int D`, the singleton/singleton operational rule returns `true`;
- if `C >Int D`, it returns `false`; and
- if `C ==Int D`, it recurses to `strLt(.IntSeq, .IntSeq)`, which returns
  `false`.

Thus the equation is mathematically true and relevant, but truth does not make
it a `DEFINITION`.  `lemma-spec.k` first proves three guarded reachability
claims, not the exact same unguarded source rule.  It therefore does not meet
the audit prompt's exact-rule requirement for `PROVED_DERIVED_LEMMA`; in any
event, the prompt requires every `[simplification]` rule to be classified as
either `DEFINITION` or `DOMAIN_LEMMA`, and this rule is the latter.

Independent domain set:

```text
rule-8035a5d5e2dd908c685b0f3f6b47722aade54582ecf7e781dfd68bc1469d72b1
```

The true domain set therefore has cardinality one, not zero.
