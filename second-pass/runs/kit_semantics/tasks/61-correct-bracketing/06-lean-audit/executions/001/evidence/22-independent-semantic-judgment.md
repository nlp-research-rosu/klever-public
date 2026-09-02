# Independent semantic judgment

## Stage 3 classification

The trusted inventory reconstruction contains seven rules in the local
`VERIFICATION` closure.

| Inventory entry | Independent class | Reason |
|---|---|---|
| `rule-b9c21...bac0` | `DEFINITION` | Base equation of the named `scanBrackets` summary on `.IntSeq`. |
| `rule-a39e2d...5a74` | `DEFINITION` | Structural recurrence of `scanBrackets` on `iCons`; it consumes exactly one sequence constructor. |
| `rule-901168...2478` | `DEFINITION` | Negative-balance guarded branch defining `keepValid`. |
| `rule-952eaa...4dc4` | `DEFINITION` | Complementary nonnegative-balance guarded branch defining `keepValid`. |
| `rule-d9b0ad...aaa0` | `DOMAIN_LEMMA` | It does not define a fresh summary and is not an ordinary program-execution rule. It adds a simplification theorem for the pre-existing hooked conditional/equality operations. Stage 1 compiles `verification.k` containing this rule before its first `kprove`; it never first proves this exact rule against a module omitting it. |
| `rule-86c81c...a66c` | `DEFINITION` | Base equation of the named input-domain predicate `bracketInput`. |
| `rule-1e22fa...9942` | `DEFINITION` | Structural recurrence of `bracketInput` on `iCons`. |

The two `keepValid` guards, `B <Int 0` and `B >=Int 0`, are disjoint and
exhaustive on K integers. The recursive definitions descend on the
`IntSeq` tail. None of these six equations is a disguised result theorem or
execution shortcut.

The sole simplification rule is correctly classified as a `DOMAIN_LEMMA`.
Its statement is true on its full guard: KORE binds `_==Int_` to `INT.eq`,
`_=/=Int_` to `INT.ne`, and `#if` to `KEQUAL.ite`; if `C` is not 40, the
conditional's Boolean condition is false and the result is its else argument
`Y`. It is relevant rather than incidental: both the source loop and the
`scanBrackets` recurrence branch on whether the current bracket code is 40
(`'('`), and the proof needs the else branch under the emitted disequality.

Independent classification therefore agrees with the protected manifest:
six definitions, zero operational rules, zero proved-derived lemmas, and one
true, relevant domain lemma.

## Stage 4 mathematical correspondence

The single generated conjunct is:

```text
∀ Y _X C, (_=/=Int_ C 40 = true) →
  kite (_==Int_ C 40) _X Y = Y
```

This preserves the K rule's three universally quantified integers, exact
guard, conditional test, then/else arguments, and exact conclusion. No
premise or conclusion is omitted, strengthened, weakened, duplicated, or
replaced by a vacuous conjunct. `SortInt` is generated as Lean `Int`,
`SortBool` as Lean `Bool`, and `kite` as Boolean `cond`.

A non-vacuous witness is `C = 41`, `_X = 0`, `Y = 1`: integer disequality is
true, equality is false, and the else result is 1. The obligation is also
sensitive to bad parameter meanings. Constant-true equality is refuted by
that witness, and constant-true disequality is refuted at `C = 40` with
unequal branches.

The generated proposition alone can be made convenient by dishonest bridge
definitions: constant-false equality makes it trivially true, while
constant-false disequality makes its premise vacuous. The independent Stage 5
bridge check is therefore load-bearing.

## Stage 5 operational bridge

The candidate definitions are exactly:

```lean
def «_==Int_» (x y : SortInt) : SortBool := x == y
def «_=/=Int_» (x y : SortInt) : SortBool := x != y
```

Because the generated sorts are `Int` and `Bool`, these are Lean integer
Boolean equality and its Boolean negation. They match the frozen KORE hooks
`INT.eq` and `INT.ne`. The fresh build's emitted C calls
`lean_int_dec_eq` for equality and negates that result for disequality.
Ground evaluations give:

```text
eq(40,40) = true
eq(41,40) = false
ne(40,40) = false
ne(41,40) = true
```

The counterfactual Lean audit proves that the two dishonest convenient
definitions above would satisfy the target, and separately proves that the
opposite constant-true mutations are rejected by concrete witnesses. The
actual candidate is neither constant, identity, hard-coded, nor vacuous and
implements the frozen operational meaning for all Lean/K integers.
