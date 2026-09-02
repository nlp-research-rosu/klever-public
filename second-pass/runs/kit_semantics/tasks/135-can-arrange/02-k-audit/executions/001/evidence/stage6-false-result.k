requires "verification.k"

module REVIEWER-FRESH-NONVACUITY
  imports VERIFICATION

  // Fresh A5 mutation: the exact real program on the satisfiable empty input
  // returns -1, so changing the result obligation to 0 must get stuck.
  claim [real-body-wrong-empty-result]:
    <k>
      (#loadAll(
        Module(
          FuncDef(
            "can_arrange", Params("arr"),
            Assign(Name("index"), UnaryOp("-", Int(1)))
            Assign(Name("i"), Int(0))
            Assign(Name("previous"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"), Name("arr"),
              If(
                Compare(Name("i"), CmpOp(">", Int(0))),
                If(
                  UnaryOp(
                    "not",
                    Compare(
                      Name("value"),
                      CmpOp(">=", Name("previous")))),
                  Assign(Name("index"), Name("i")),
                  .Stmts),
                .Stmts)
              Assign(Name("previous"), Name("value"))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              .Stmts)
            Return(Name("index"))
            .Stmts)
          .Stmts))
      ~> Call(Name("can_arrange"), list(.ValSeq))
      => 0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        .Map
        => "can_arrange" |->
             closureVal(
               "arr", .ParamNames,
               Assign(Name("index"), UnaryOp("-", Int(1)))
               Assign(Name("i"), Int(0))
               Assign(Name("previous"), Int(0))
               Assign(Name("value"), Int(0))
               For(
                 Name("value"), Name("arr"),
                 If(
                   Compare(Name("i"), CmpOp(">", Int(0))),
                   If(
                     UnaryOp(
                       "not",
                       Compare(
                         Name("value"),
                         CmpOp(">=", Name("previous")))),
                     Assign(Name("index"), Name("i")),
                     .Stmts),
                   .Stmts)
                 Assign(Name("previous"), Name("value"))
                 Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
                 .Stmts)
               Return(Name("index"))
               .Stmts,
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
