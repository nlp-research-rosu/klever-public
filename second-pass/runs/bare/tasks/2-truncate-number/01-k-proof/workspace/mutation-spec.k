requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  // Deliberately false: the fractional part of 3.5 does not have integer
  // component 1.  prove.sh requires this probe to fail.
  claim
    <k>
      Module(FuncDef("truncate_number", Params("number"),
        Return(BinOp("-", Name("number"),
          Call(Name("int"), Name("number"))))))
      ~> invoke("truncate_number", num(3, 5, 10))
      => .K
    </k>
    <env> .Map => "number" |-> num(3, 5, 10) </env>
    <result> noResult => num(1, 5, 10) </result>
endmodule
