requires "semantic.k"

module BRIDGE-REACHABLE-CONNECTION-SPEC
  imports HUMAN-EVAL

  // Bridge-free connection over the environment shape actually reached just
  // before this program's loop.  KREST remains arbitrary.
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
      ("arr" |-> listVal(INPUT)
       "drops" |-> iVal(D)
       "previous" |-> iVal(P))
    =>
      ("arr" |-> listVal(INPUT)
       "drops" |-> iVal(D +Int dropsFrom(P, I :: IS))
       "previous" |-> iVal(last(I :: IS))
       "value" |-> iVal(last(I :: IS)))
    </env>
endmodule
