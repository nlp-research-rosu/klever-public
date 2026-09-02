requires "verification.k"

module CLAIM-UNIVERSAL
  imports VERIFICATION

  claim
    <k>
      Module(FuncDef("truncate_number", Params("number"),
        Return(BinOp("-", Name("number"),
          Call(Name("int"), Name("number"))))))
      ~> invoke("truncate_number", num(I, F, S))
      => .K
    </k>
    <env> .Map => "number" |-> num(I, F, S) </env>
    <result> noResult => num(0, F, S) </result>
    requires validPositive(num(I, F, S))
    ensures validFraction(num(0, F, S))
endmodule
