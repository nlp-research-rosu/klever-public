requires "semantic.k"

module BRIDGE-CONNECTION
  imports SEMANTIC

  claim [parity-idiom-connection]:
    <exchange>
      <k>
        exec(
          If(Compare(BinOp("%", Name("value"), Int(2)), CmpOp("==", Int(0))),
             Assign(Name("even"), BinOp("+", Name("even"), Int(1))),
             .Stmts)
          REST)
        ~> CONT
      =>
        exec(REST) ~> CONT
      </k>
      <env>
        "lst1" |-> L1
        "lst2" |-> L2
        "even" |-> N
        "value" |-> I
      =>
        "lst1" |-> L1
        "lst2" |-> L2
        "even" |-> (N +Int evenBit(I))
        "value" |-> I
      </env>
      <result> RES </result>
    </exchange>
endmodule
