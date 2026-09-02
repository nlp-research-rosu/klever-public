requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false off-by-one mutation of the loop result in SPEC.
  claim [prod-signs-loop-off-by-one]:
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
      => foldResult(REST, TOTAL:Int, SIGN:Int) +Int 1
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
