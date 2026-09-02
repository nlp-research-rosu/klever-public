requires "bridge-free-verification.k"

module AUDIT-LOOP-CONTINUATION-PLAIN-SPEC
  imports AUDIT-BRIDGE-FREE-VERIFICATION

  claim [loop-continuation-plain]:
    <k>
      For(Name("value"), list(vCons(-2, vCons(0, vCons(3, .ValSeq)))),
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
      ~> Assign(Name("after"), Int(7))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map [ "total" <- 0 ] [ "sign" <- 1 ]
          => .Map [ "total" <- 5 ]
                  [ "sign" <- 0 ]
                  [ "value" <- 3 ]
                  [ "after" <- 7 ],
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
