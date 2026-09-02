# Proof-local rule review

This ledger is independent of the candidate's `PROOF.md`. Line numbers refer
to the mounted/scratch-identical `verification.k`. The exhaustive inventory of
all supplied and proof-local declarations is `05-rule-inventory.tsv`.

## Declarations and attributes

- Lines 6–7, `numericVals` and `definedProjectInt`: pure `Bool` functions.
  `numericVals` is structurally total on `ValSeq`; `definedProjectInt` has one
  all-`Val` equation.
- Line 8, `lastNumber`: pure structurally recursive `Val` function, total on
  both `ValSeq` constructors.
- Lines 9–12, `dtd`, `oddIntSquare`, `projectIntTotal`: `dtd` and
  `oddIntSquare` are exhaustively defined mathematical functions.
  `projectIntTotal` is a total, no-evaluator `Val -> Int` symbol. Its value is
  fixed to the subsort projection whenever `isInt` holds and remains opaque
  off that domain. Every result-bearing use in this proof is guarded by
  `isInt`; there is no off-domain dependent.
- Lines 16–17, `dtdLoopBody` and `dtdBody`: compile-time macros. Independent
  `kast --expand-macros` comparison gave byte-identical KORE constructor trees
  for the regenerated source function and the proof closure body.

## Rules 1–11: domain and mathematical summaries

1. Line 25, `numericVals(.ValSeq) => true`: true definition of the empty
   numeric sequence.
2. Lines 26–27, `numericVals(vCons(V,VS))`: exact structural conjunction of
   Int-or-Float head membership and the tail predicate.
3. Line 30, `dtd(.ValSeq) => 0`: correct empty sum.
4. Lines 31–32, static Int head: adds `oddIntSquare(I)` and descends on the
   strict structural tail.
5. Line 33, static Float head: ignores the non-integer head and descends.
6. Line 34, `[owise]` other-Val head: disjoint from static Int/Float heads and
   defines the broader helper by ignoring all other model values. The entry
   claims themselves exclude this case.
7. Lines 35–38, guarded dynamic Int simplification: overlaps the static Int
   equation only with the same right-hand side after projection collapse.
8. Lines 39–41, guarded dynamic Float simplification: overlaps the static
   Float equation with the same right-hand side. `isInt` and `isFloat` are
   disjoint model sort predicates.
9. Lines 43–47, `oddIntSquare`: exactly `I*I` when `I>0` and Python modulo by
   the positive divisor 2 is 1, otherwise zero.
10. Line 51, empty `lastNumber`: an empty remaining loop leaves the prior
    target value unchanged.
11. Lines 52–53, cons `lastNumber`: records the head then strictly descends,
    yielding the last element.

These rules terminate structurally (or immediately), cover their declared
used domains, and have no conflicting overlap.

## Rules 12–21: guarded Int projection and fixed-dispatch lemmas

12. Line 57, `definedProjectInt(V) => isInt(V)`: a name for the exact Int
    subsort-membership predicate.
13. Lines 58–60, `#Ceil({V}:>Int)`: the partial subsort cast is defined exactly
    when the `Val` is an Int injection. The extra `#Ceil(V)` preserves ordinary
    term definedness.
14. Lines 61–63, guarded `projectIntTotal(V) => {V}:>Int`: fixes the total
    symbol to the built-in partial cast on its defined domain.
15. Lines 64–66, reverse symbolic orientation: the same equality in the
    solver-friendly direction, under the identical guard.
16. Line 67, `projectIntTotal(I) => I`: fixes every actual Int value.
17. Lines 68–70, projection idempotence: sound because the inner result has
    sort Int and rule 16 makes projection the identity on it, including when
    the original argument was off-domain.
18. Line 71, `isIntV(V) => isInt(V)`: exact case compression of the supplied
    rules `isIntV(_:Int)=>true` and `isIntV(_:Val)=>false [owise]`.
19. Lines 72–75, dynamic `applyCmp(">")`: under `isInt(V)`, the projected value
    is exactly the Int selected by the supplied static comparison rule.
20. Lines 76–79, dynamic `applyBin("%")`: same argument for the supplied
    `pyMod` rule. The actual divisor is the defined positive Int 2.
21. Lines 80–83, dynamic `applyBin("*")`: same argument for the supplied
    static multiplication rule, with both operands guarded.

The fixed-only definition proves the corresponding universal static Int
equations with `#Top` (`05-fixed-connection-proof.log`). A stronger dynamic-Val
formulation could not be discharged by the fixed backend because it did not
case-split an abstract `Val` from `isInt(V)` (`05-fixed-connection-dynamic.log`);
that residual is an evidence/mechanization gap, not a counterexample. The
source equations and disjoint algebraic sort cases establish the derivation.
For value sensitivity, `projectIntTotal(3) => 4` parsed successfully and was
rejected with the residual value 3 (`05-projection-opposite.log`).

The two opposite simplification orientations are equalities on the same guard.
Their different simplification modes/priorities terminate in the reconstructed
proof. No off-domain opaque projection can affect a branch, state update,
returned value, summary, or postcondition.

## Rules 22–23: source macros

22. Lines 85–95 expands `dtdLoopBody` to the exact nested
    `isinstance`/positive/modulo/multiply/`AugAssign` constructor subtree.
23. Lines 97–101 expands `dtdBody` to the exact two initial assignments,
    `For`, and `Return` subtree.

These are macro equations, not runtime operational bridges. Their exact
constructor identity is recorded in `04-constructor-identity.log`. The fresh
inline body mutation changes multiplication to addition in the actual closure
term; it builds, executes to 2 on `[1]`, and fails the original result 1
(`04-body-sensitivity-inline.log`).

## Conclusion

No proof-local rule admits a concrete or symbolic false conclusion on the
entry domain. Therefore this review makes no unsoundness allegation and has no
false-conclusion witness to report. The only narrow evidence gap is the
backend's inability to prove the abstract-`Val` case-compression theorem
without the very simplification lemmas being audited; the finite and static
checks do not substitute for the source-level algebraic case argument.
