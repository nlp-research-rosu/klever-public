requires "semantic-no-bridge.k"

module BRIDGE-CONNECTION-SPEC
  imports SEMANTIC

  // Universal equivalence target for semantic.k:91-99, executed here with
  // that prioritized shortcut removed from the definition.
  claim [parity-shortcut-connection]:
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
        (X |-> I:Int Y |-> N:Int RHO:Map)
        =>
        (X |-> I Y |-> N RHO) [ Y <- N +Int evenBit(I) ]
      </env>
      <result> _R:Result </result>
    </exchange>
endmodule
