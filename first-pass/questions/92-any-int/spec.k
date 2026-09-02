// spec.k — the reachability claim kprove discharges.
//
//   kompile verification.k --backend haskell \
//     --main-module ANY-INT-VERIFICATION \
//     --syntax-module ANY-INT-SYNTAX \
//     --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled \
//     --spec-module ANY-INT-SPEC

requires "verification.k"

module ANY-INT-SPEC
  imports ANY-INT-VERIFICATION

  // ---- Entry claim — see ./PROOF.md ----------------------------------------
  // Straight-line, no loop: after `result = any_int(X, Y, Z)` for arbitrary
  // symbolic integers X, Y, Z, the root scope's `result` is bound to the
  // disjunction of the three pairwise-sum equalities. Since X, Y, Z are all
  // Ints, each isinstance(_, int) is true, so the short-circuit `and` is true
  // and the outer guard is taken; the inner short-circuit `or` then yields the
  // disjunction (Return True) or its negation (Return False) — i.e. exactly the
  // Bool value of the disjunction. kprove case-splits the two short-circuit
  // chains and matches the orBool postcondition.
  claim
    <k>
      FuncDef("any_int", Params("x", "y", "z"),
        If(BoolOp("and",
            Call(Name("isinstance"), (Name("x"), Name("int"), .Exprs)),
            Call(Name("isinstance"), (Name("y"), Name("int"), .Exprs)),
            Call(Name("isinstance"), (Name("z"), Name("int"), .Exprs))),
          If(BoolOp("or",
              Compare(BinOp("+", Name("x"), Name("y")), CmpOp("==", Name("z"))),
              Compare(BinOp("+", Name("x"), Name("z")), CmpOp("==", Name("y"))),
              Compare(BinOp("+", Name("y"), Name("z")), CmpOp("==", Name("x")))),
            Return(Bool(true)),
            .Stmts)
          Return(Bool(false)),
          .Stmts)
        Return(Bool(false)))
      Assign(Name("result"), Call(Name("any_int"), (X:Int, Y:Int, Z:Int)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(.Map [ "any_int" <- ?_:Val ] [ "result" <- (X +Int Y ==Int Z) orBool (X +Int Z ==Int Y) orBool (Y +Int Z ==Int X) ], parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
