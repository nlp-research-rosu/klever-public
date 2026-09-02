requires "verification.k"

module FRESH-VACUITY-SPEC
  imports VERIFICATION

  // Fresh false mutation: retain the exact submitted body and the full
  // symbolic precondition, but require an off-by-one fractional numerator.
  // num(3,1,2) is a satisfying witness and must return num(0,1,2), not
  // num(0,2,2).
  claim
    <k>
      Module(FuncDef("truncate_number", Params("number"),
        Return(BinOp("-", Name("number"),
          Call(Name("int"), Name("number"))))))
      ~> invoke("truncate_number", num(I, F, S))
      => .K
    </k>
    <env> .Map => "number" |-> num(I, F, S) </env>
    <result> noResult => num(0, F +Int 1, S) </result>
    requires validPositive(num(I, F, S))
endmodule
