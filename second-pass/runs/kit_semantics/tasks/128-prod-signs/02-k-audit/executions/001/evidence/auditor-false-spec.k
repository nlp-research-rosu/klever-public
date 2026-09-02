requires "verification.k"

module AUDITOR-FALSE-SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #loop(
        list(intVals(REST:IntSeq)),
        Name("value"),
        Assign(Name("seen"), Int(1))
        Assign(
          Name("total"),
          BinOp("+", Name("total"), Call(Name("abs"), Name("value"))))
        If(
          Compare(Name("value"), CmpOp("<", Int(0))),
          Assign(Name("sign"), BinOp("-", Int(0), Name("sign"))),
          If(
            Compare(Name("value"), CmpOp(">", Int(0))),
            Assign(Name("sign"), Name("sign")),
            Assign(Name("sign"), Int(0)))
          .Stmts)
        .Stmts)
      ~> If(
           Compare(Name("seen"), CmpOp("==", Int(0))),
           Return(NoneVal) .Stmts,
           .Stmts)
         Return(BinOp("*", Name("total"), Name("sign")))
         .Stmts
      ~> #endcall
      => foldResult(
           REST,
           TOTAL:Int,
           SIGN:Int)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "prod_signs" |-> CLOSURE:Val,
        parent(-1))
      1 |-> scope(
        "arr" |-> list(intVals(INPUT:IntSeq))
        "total" |-> TOTAL
        "sign" |-> SIGN
        "seen" |-> 1
        "value" |-> OLD:Int,
        parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
        "prod_signs" |-> CLOSURE,
        parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HLOC:Int </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [prod-signs]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "prod_signs",
            Params("arr"),
            Assign(Name("total"), Int(0))
            Assign(Name("sign"), Int(1))
            Assign(Name("seen"), Int(0))
            For(
              Name("value"),
              Name("arr"),
              Assign(Name("seen"), Int(1))
              Assign(
                Name("total"),
                BinOp(
                  "+",
                  Name("total"),
                  Call(Name("abs"), Name("value"))))
              If(
                Compare(Name("value"), CmpOp("<", Int(0))),
                Assign(
                  Name("sign"),
                  BinOp("-", Int(0), Name("sign"))) .Stmts,
                If(
                  Compare(Name("value"), CmpOp(">", Int(0))),
                  Assign(Name("sign"), Name("sign")) .Stmts,
                  Assign(Name("sign"), Int(0)) .Stmts)
                .Stmts)
              .Stmts)
            If(
              Compare(Name("seen"), CmpOp("==", Int(0))),
              Return(NoneVal) .Stmts,
              .Stmts)
            Return(BinOp("*", Name("total"), Name("sign")))
            .Stmts)))
      ~> Call(Name("prod_signs"), list(intVals(INPUT:IntSeq)))
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(.Map, parent(-1))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
        "prod_signs" |->
          closureVal(
            ("arr", .ParamNames),
            Assign(Name("total"), Int(0))
            Assign(Name("sign"), Int(1))
            Assign(Name("seen"), Int(0))
            For(
              Name("value"),
              Name("arr"),
              Assign(Name("seen"), Int(1))
              Assign(
                Name("total"),
                BinOp(
                  "+",
                  Name("total"),
                  Call(Name("abs"), Name("value"))))
              If(
                Compare(Name("value"), CmpOp("<", Int(0))),
                Assign(
                  Name("sign"),
                  BinOp("-", Int(0), Name("sign"))) .Stmts,
                If(
                  Compare(Name("value"), CmpOp(">", Int(0))),
                  Assign(Name("sign"), Name("sign")) .Stmts,
                  Assign(Name("sign"), Int(0)) .Stmts)
                .Stmts)
              .Stmts)
            If(
              Compare(Name("seen"), CmpOp("==", Int(0))),
              Return(NoneVal) .Stmts,
              .Stmts)
            Return(BinOp("*", Name("total"), Name("sign")))
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
