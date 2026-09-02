requires "verification.k"

module AUDIT-CELL-WITNESS-BRIDGE-SPEC
  imports PROD-SIGNS-VERIFICATION

  claim [cell-witness-false-conclusion]:
    <k>
      For(Name("value"), list(vCons(5, .ValSeq)),
        If(Compare(Name("value"), CmpOp("<", Int(0))),
          Assign(Name("total"),
            BinOp("-", Name("total"), Name("value")))
          Assign(Name("sign"),
            BinOp("-", Int(0), Name("sign"))),
          Assign(Name("total"),
            BinOp("+", Name("total"), Name("value")))
          If(Compare(Name("value"), CmpOp("==", Int(0))),
            Assign(Name("sign"), Int(0)),
            .Stmts)))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map [ "$cells" <- cellsMark("value") ]
             [ "value" <- cellRef(0) ]
             [ "total" <- 0 ]
             [ "sign" <- 1 ]
          => .Map [ "$cells" <- cellsMark("value") ]
                  [ "value" <- 5 ]
                  [ "total" <- 5 ]
                  [ "sign" <- 1 ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> 0 |-> cellV(99) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
