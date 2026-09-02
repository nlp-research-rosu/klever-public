requires "semantic-no-bridge.k"

module BRIDGE-CONNECTION-SPEC
  imports SEMANTIC

  // First broad auditor attempt: execute the generic rules with the shortcut
  // removed and target the shortcut's explicit entry-rewrite form.
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
      <env> ... X |-> I:Int
                Y |-> (N:Int => N +Int evenBit(I)) ... </env>
      <result> R:Result </result>
    </exchange>
endmodule
