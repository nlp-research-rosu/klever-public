requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  claim [loop]:
    <k>
      #loop(
        list(intVals(IS:IntSeq)),
        Name("value"),
        If(
          Compare(
            BinOp("%", Name("index"), Int(3)),
            CmpOp("==", Int(0))),
          Assign(
            Name("total"),
            BinOp(
              "+",
              Name("total"),
              BinOp("*", Name("value"), Name("value"))))
          .Stmts,
          If(
            Compare(
              BinOp("%", Name("index"), Int(4)),
              CmpOp("==", Int(0))),
            Assign(
              Name("total"),
              BinOp(
                "+",
                Name("total"),
                BinOp(
                  "*",
                  BinOp("*", Name("value"), Name("value")),
                  Name("value"))))
            .Stmts,
            Assign(
              Name("total"),
              BinOp("+", Name("total"), Name("value")))
            .Stmts)
          .Stmts)
        Assign(
          Name("index"),
          BinOp("+", Name("index"), Int(1)))
        .Stmts)
      ~> Return(Name("total")) .Stmts
      ~> #endcall
      => sumSquaresFrom(IS, I:Int, A:Int)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> BUILTINS:Scope
         0 |-> scope(MODULE:Map, parent(-1))
         1 |-> scope(
                "lst" |-> list(INPUT:ValSeq)
                "index" |-> I
                "total" |-> A
                "value" |-> OLD:Val,
                parent(0)) )
      =>
      ( -1 |-> BUILTINS
         0 |-> scope(MODULE, parent(-1)) )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule

module SPEC-AUDIT-FALSE
  imports VERIFICATION

  claim [entry]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "sum_squares",
            Params("lst"),
            Assign(Name("total"), Int(0))
            Assign(Name("index"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"),
              Name("lst"),
              If(
                Compare(
                  BinOp("%", Name("index"), Int(3)),
                  CmpOp("==", Int(0))),
                Assign(
                  Name("total"),
                  BinOp(
                    "+",
                    Name("total"),
                    BinOp("*", Name("value"), Name("value"))))
                .Stmts,
                If(
                  Compare(
                    BinOp("%", Name("index"), Int(4)),
                    CmpOp("==", Int(0))),
                  Assign(
                    Name("total"),
                    BinOp(
                      "+",
                      Name("total"),
                      BinOp(
                        "*",
                        BinOp("*", Name("value"), Name("value")),
                        Name("value"))))
                  .Stmts,
                  Assign(
                    Name("total"),
                    BinOp("+", Name("total"), Name("value")))
                  .Stmts)
                .Stmts)
              Assign(
                Name("index"),
                BinOp("+", Name("index"), Int(1)))
              .Stmts)
            Return(Name("total"))
            .Stmts)
          .Stmts))
      ~> Call(Name("sum_squares"), list(intVals(IS:IntSeq)))
      =>
      sumSquaresFrom(IS, 0, 0) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
               "sum_squares" |->
                 closureVal(
                   ("lst", .ParamNames),
                   Assign(Name("total"), Int(0))
                   Assign(Name("index"), Int(0))
                   Assign(Name("value"), Int(0))
                   For(
                     Name("value"),
                     Name("lst"),
                     If(
                       Compare(
                         BinOp("%", Name("index"), Int(3)),
                         CmpOp("==", Int(0))),
                       Assign(
                         Name("total"),
                         BinOp(
                           "+",
                           Name("total"),
                           BinOp("*", Name("value"), Name("value"))))
                       .Stmts,
                       If(
                         Compare(
                           BinOp("%", Name("index"), Int(4)),
                           CmpOp("==", Int(0))),
                         Assign(
                           Name("total"),
                           BinOp(
                             "+",
                             Name("total"),
                             BinOp(
                               "*",
                               BinOp("*", Name("value"), Name("value")),
                               Name("value"))))
                         .Stmts,
                         Assign(
                           Name("total"),
                           BinOp("+", Name("total"), Name("value")))
                         .Stmts)
                       .Stmts)
                     Assign(
                       Name("index"),
                       BinOp("+", Name("index"), Int(1)))
                     .Stmts)
                   Return(Name("total"))
                   .Stmts,
                   0),
               parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
