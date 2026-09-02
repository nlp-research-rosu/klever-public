requires "semantic.k"

module BRIDGE-CONNECTION-SPEC
  imports HUMAN-EVAL

  // Bridge-free universal execution theorem for the candidate's exact loop
  // body.  The continuation and input cell are universally quantified.
  claim
    <k>
      loop("value", I :: IS,
        If(Compare(Name("previous"), CmpOp(">", Name("value"))),
          Assign(Name("drops"), BinOp("+", Name("drops"), Int(1))) .Stmts,
          .Stmts)
        Assign(Name("previous"), Name("value")) .Stmts)
      ~> KREST
    =>
      KREST
    </k>
    <input> INPUT </input>
    <env>
      ("drops" |-> iVal(D)
       "previous" |-> iVal(P)
       REST)
    =>
      ("drops" |-> iVal(D +Int dropsFrom(P, I :: IS))
       "previous" |-> iVal(last(I :: IS))
       (REST [ "value" <- iVal(last(I :: IS)) ]))
    </env>
endmodule
