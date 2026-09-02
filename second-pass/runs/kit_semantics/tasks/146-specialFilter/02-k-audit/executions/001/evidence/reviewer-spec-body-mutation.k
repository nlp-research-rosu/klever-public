requires "verification.k"

module REVIEWER-SPEC-BODY-MUTATION
  imports VERIFICATION

  // Fresh material body mutation: change the threshold from 10 to 100.
  // The original postcondition for [15] is 1, while this body returns 0.
  claim [threshold-one-hundred]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "specialFilter",
            Params("nums"),
            Assign(Name("count"), Int(0))
            Assign(Name("num"), Int(0))
            Assign(Name("text"), Str(""))
            For(
              Name("num"),
              Name("nums"),
              If(
                Compare(Name("num"), CmpOp(">", Int(100))),
                Assign(Name("text"), Call(Name("str"), Name("num")))
                If(
                  Compare(
                    BinOp(
                      "%",
                      Call(Name("ord"), Subscript(Name("text"), Int(0))),
                      Int(2)),
                    CmpOp("==", Int(1))),
                  If(
                    Compare(
                      BinOp(
                        "%",
                        Call(
                          Name("ord"),
                          Subscript(Name("text"), UnaryOp("-", Int(1)))),
                        Int(2)),
                      CmpOp("==", Int(1))),
                    AugAssign(Name("count"), "+", Int(1)),
                    .Stmts),
                  .Stmts),
                .Stmts))
            Return(Name("count")))))
      ~> Call(Name("specialFilter"), list(vCons(15, .ValSeq)))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              .Map
              => "specialFilter"
                 |-> closureVal(
                       "nums",
                       Assign(Name("count"), Int(0))
                       Assign(Name("num"), Int(0))
                       Assign(Name("text"), Str(""))
                       For(
                         Name("num"),
                         Name("nums"),
                         If(
                           Compare(Name("num"), CmpOp(">", Int(100))),
                           Assign(Name("text"), Call(Name("str"), Name("num")))
                           If(
                             Compare(
                               BinOp(
                                 "%",
                                 Call(Name("ord"), Subscript(Name("text"), Int(0))),
                                 Int(2)),
                               CmpOp("==", Int(1))),
                             If(
                               Compare(
                                 BinOp(
                                   "%",
                                   Call(
                                     Name("ord"),
                                     Subscript(Name("text"), UnaryOp("-", Int(1)))),
                                   Int(2)),
                                 CmpOp("==", Int(1))),
                               AugAssign(Name("count"), "+", Int(1)),
                               .Stmts),
                             .Stmts),
                           .Stmts))
                       Return(Name("count")),
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
