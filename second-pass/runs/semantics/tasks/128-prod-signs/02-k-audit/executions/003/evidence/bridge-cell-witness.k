requires "verification.k"

module BRIDGE-CELL-WITNESS
  imports PROD-SIGNS-VERIFICATION

  // The candidate bridge accepts a scope in which the loop target is a
  // captured cell. It overwrites the map binding and leaves cell 0 unchanged,
  // so the observable continuation reads the stale value 99.
  claim [bridge-stale-cell]:
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
      99
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
          "value" |-> 1
          "$cells" |-> cellsMark("value"),
          parent(0)))
    </scopes>
    <heap> 0 |-> cellV(99) </heap>
endmodule
