requires "verification.k"

module LOOP-WITNESS-EXTENDED
  imports VERIFICATION

  claim [boundary-witness]:
    <k>
      #loop(
        list(vCons(99, vCons(-100, vCons(7, .ValSeq)))),
        Name("element"),
        If(
          Compare(Name("remaining"), CmpOp("==", Int(0))),
          Break .Stmts,
          .Stmts
        )
        If(
          BoolOp(
            "and",
            Compare(Name("element"), CmpOp(">=", UnaryOp("-", Int(99)))),
            Compare(Name("element"), CmpOp("<=", Int(99)))
          ),
          AugAssign(Name("total"), "+", Name("element")) .Stmts,
          .Stmts
        )
        AugAssign(Name("remaining"), "-", Int(1))
      )
      ~> (Return(Name("total")) .Stmts)
      ~> #endcall
      =>
      104
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "arr" |-> list(vCons(99, vCons(-100, vCons(7, .ValSeq))))
        "k" |-> 2
        "total" |-> 5
        "element" |-> 0
        "remaining" |-> 2,
        parent(0)
      )
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
