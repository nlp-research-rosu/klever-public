requires "semantic-no-bridge.k"

module BRIDGE-CONNECTION-ACTUAL-SPEC
  imports SEMANTIC

  // The two exhaustive mathematical branches of the prioritized rule in the
  // exact identifier/state context reached by solution.mpy.
  claim [parity-shortcut-even-actual]:
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
        "even" |-> (N:Int => N +Int 1)
        "value" |-> I:Int
      </env>
      <result> noResult </result>
    </exchange>
    requires I %Int 2 ==Int 0

  claim [parity-shortcut-odd-actual]:
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
        "even" |-> N:Int
        "value" |-> I:Int
      </env>
      <result> noResult </result>
    </exchange>
    requires notBool (I %Int 2 ==Int 0)
endmodule
