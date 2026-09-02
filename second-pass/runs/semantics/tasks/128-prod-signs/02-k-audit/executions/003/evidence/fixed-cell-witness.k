requires "audit-fixed.k"

module FIXED-CELL-WITNESS
  imports AUDIT-FIXED

  // Under only the supplied semantics, #bindTgt writes through cell 0.
  // The same observable continuation therefore reads 1.
  claim [fixed-updated-cell]:
    <k>
      For(Name("value"), list(vCons(1, .ValSeq)),
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
      ~> cellRef(0)
      =>
      1
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(
          "total" |-> 0
          "sign" |-> 1
          "value" |-> cellRef(0)
          "$cells" |-> cellsMark("value"),
          parent(0))
       =>
       1 |-> scope(
          "total" |-> 1
          "sign" |-> 1
          "value" |-> cellRef(0)
          "$cells" |-> cellsMark("value"),
          parent(0)))
    </scopes>
    <heap> 0 |-> cellV(99 => 1) </heap>
endmodule
