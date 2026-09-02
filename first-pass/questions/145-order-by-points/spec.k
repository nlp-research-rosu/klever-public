// spec.k — order_by_points, TRAP-FREE (P145). A single entry claim: the REAL
// sorted(nums, key=digits_sum) lands as the SHARED opaque sortKeyVS with the
// digits_sum closure value inside the atom (the trusted keyed sort; krun
// computes the real keyed order).
//
//   kompile verification.k --backend haskell --main-module ORDER-BY-POINTS-VERIFICATION \
//     --syntax-module MPY-SYNTAX --output-definition verification-kompiled
//   kprove spec.k --definition verification-kompiled --spec-module ORDER-BY-POINTS-SPEC

requires "verification.k"

module ORDER-BY-POINTS-SPEC
  imports ORDER-BY-POINTS-VERIFICATION

  claim
    <k>
      FuncDef("order_by_points", Params("nums"),
        FuncDef("digits_sum", Params("n"), CellVars(.ParamNames), FreeVars(.ParamNames),
          Assign(Name("neg"), Int(1))
          If(Compare(Name("n"), CmpOp("<", Int(0))),
            Assign(
              TupleExpr(Name("n"), Name("neg")),
              TupleExpr(
                BinOp("*", UnaryOp("-", Int(1)), Name("n")),
                UnaryOp("-", Int(1)))),
            .Stmts)
          Assign(Name("n"),
            ListComp(Call(Name("int"), Name("i")),
              CompFor(Name("i"), Call(Name("str"), Name("n")), Bool(true))))
          Assign(Subscript(Name("n"), Int(0)),
            BinOp("*", Subscript(Name("n"), Int(0)), Name("neg")))
          Return(Call(Name("sum"), Name("n"))))
        Return(Call(Name("sorted"), Name("nums"), KwArg("key", Name("digits_sum")))))
      Assign(Name("result"), Call(Name("order_by_points"), list(VS:ValSeq)))
    => .K ... </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
    =>
      -1 |-> builtinsScope
      0 |-> scope(.Map [ "order_by_points" <- ?_:Val ] [ "result" <- ref(?H:Int) ], parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map =>
      (?H |-> list(sortKeyVS(VS, closureValC("n", .ParamNames,
        Assign(Name("neg"), Int(1))
        If(Compare(Name("n"), CmpOp("<", Int(0))),
          Assign(
            TupleExpr(Name("n"), Name("neg")),
            TupleExpr(
              BinOp("*", UnaryOp("-", Int(1)), Name("n")),
              UnaryOp("-", Int(1)))),
          .Stmts)
        Assign(Name("n"),
          ListComp(Call(Name("int"), Name("i")),
            CompFor(Name("i"), Call(Name("str"), Name("n")), Bool(true))))
        Assign(Subscript(Name("n"), Int(0)),
          BinOp("*", Subscript(Name("n"), Int(0)), Name("neg")))
        Return(Call(Name("sum"), Name("n"))), .Map)))) ?_:Map </heap>
    <heapLoc> 0 => ?_:Int </heapLoc>
    <ret> noRet </ret>
    <stack> .List </stack>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [all-path]
endmodule
