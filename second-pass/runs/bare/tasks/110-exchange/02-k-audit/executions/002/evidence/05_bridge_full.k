requires "semantic.k"

module BRIDGE-FULL
  imports SEMANTIC

  claim [parity-idiom-full-domain]:
    <exchange>
      <k>
        exec(
          If(Compare(BinOp("%", Name(X), Int(2)), CmpOp("==", Int(0))),
             Assign(Name(Y), BinOp("+", Name(Y), Int(1))),
             .Stmts)
          REST)
        ~> CONT
      =>
        exec(REST) ~> CONT
      </k>
      <env>
        ...
        X |-> I
        Y |-> (N => N +Int evenBit(I))
        ...
      </env>
      <result> RES </result>
    </exchange>
endmodule
