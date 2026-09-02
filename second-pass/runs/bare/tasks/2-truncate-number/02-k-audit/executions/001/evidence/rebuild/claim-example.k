requires "verification.k"

module CLAIM-EXAMPLE
  imports VERIFICATION

  claim
    <k>
      Module(FuncDef("truncate_number", Params("number"),
        Return(BinOp("-", Name("number"),
          Call(Name("int"), Name("number"))))))
      ~> invoke("truncate_number", num(3, 5, 10))
      => .K
    </k>
    <env> .Map => "number" |-> num(3, 5, 10) </env>
    <result> noResult => num(0, 5, 10) </result>
endmodule
