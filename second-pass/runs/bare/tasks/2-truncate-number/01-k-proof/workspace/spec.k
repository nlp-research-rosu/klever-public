requires "verification.k"

module SPEC
  imports VERIFICATION

  // This is exactly the constructor tree generated in solution.mpy.  The
  // symbolic claim covers every positive exact rational, hence every positive
  // finite Python float, and computes its fractional part without rounding.
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

  // Prompt example: 3.5 = 3 + 5/10 and the result is 0.5.
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
