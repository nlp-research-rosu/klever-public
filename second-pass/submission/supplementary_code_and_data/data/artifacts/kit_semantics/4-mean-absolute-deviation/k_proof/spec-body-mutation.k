requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutate the empty-list return from 0.0 to 1.0 while retaining
  // the original expected result.  The connection must no longer close.
  claim [mutated-empty-return]:
    <k>
      FuncDef(
        "mean_absolute_deviation",
        Params("numbers"),
        Assign(Name("count"), Call(Name("len"), Name("numbers")))
        If(Compare(Name("count"), CmpOp("==", Int(0))),
           Return(Float(1.0)),
           .Stmts)
        Assign(Name("total"), Float(0.0))
        Assign(Name("number"), Float(0.0))
        For(Name("number"), Name("numbers"),
            Assign(Name("total"),
                   BinOp("+", Name("total"), Name("number"))))
        Assign(Name("mean"), BinOp("/", Name("total"), Name("count")))
        Assign(Name("deviation"), Float(0.0))
        For(Name("number"), Name("numbers"),
            Assign(
              Name("deviation"),
              BinOp(
                "+",
                Name("deviation"),
                Call(Name("abs"),
                     BinOp("-", Name("number"), Name("mean"))))))
        Return(BinOp("/", Name("deviation"), Name("count"))))
      ~> Call(
           Name("mean_absolute_deviation"),
           (list(.ValSeq), .Exprs))
      => 0.0
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              .Map
              => "mean_absolute_deviation"
                 |-> closureVal(
                       ("numbers", .ParamNames),
                       Assign(
                         Name("count"),
                         Call(Name("len"), Name("numbers")))
                       If(
                         Compare(
                           Name("count"),
                           CmpOp("==", Int(0))),
                         Return(Float(1.0)),
                         .Stmts)
                       Assign(Name("total"), Float(0.0))
                       Assign(Name("number"), Float(0.0))
                       For(
                         Name("number"),
                         Name("numbers"),
                         Assign(
                           Name("total"),
                           BinOp(
                             "+",
                             Name("total"),
                             Name("number"))))
                       Assign(
                         Name("mean"),
                         BinOp(
                           "/",
                           Name("total"),
                           Name("count")))
                       Assign(Name("deviation"), Float(0.0))
                       For(
                         Name("number"),
                         Name("numbers"),
                         Assign(
                           Name("deviation"),
                           BinOp(
                             "+",
                             Name("deviation"),
                             Call(
                               Name("abs"),
                               BinOp(
                                 "-",
                                 Name("number"),
                                 Name("mean"))))))
                       Return(
                         BinOp(
                           "/",
                           Name("deviation"),
                           Name("count"))),
                       0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
