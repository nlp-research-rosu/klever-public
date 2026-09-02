requires "loop-connection.k"

module LOOP-BODY-MUTATION-SPEC
  imports LOOP-CONNECTION

  // The first statement is deliberately changed from `seen = 1` to
  // `seen = 0`, while the original result summary is retained.
  claim [prod-signs-mutated-loop]:
    <k>
      #loop(
        list(intVals(REST:IntSeq)),
        Name("value"),
        Assign(Name("seen"), Int(0))
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
      => foldResult(REST, TOTAL:Int, SIGN:Int)
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
endmodule
