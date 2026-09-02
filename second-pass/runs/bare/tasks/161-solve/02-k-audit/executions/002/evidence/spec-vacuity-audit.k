requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh reviewer mutation: falsely require unconditional reversal.
  // Witness S = 97 :: 98 :: .PString ("ab"): execution returns [65, 66],
  // while this destination requires [98, 97].
  claim
    <humanEval>
      <k>
        Module(
          FuncDef("solve", Params("s"),
            Return(
              IfExp(
                Call(
                  Name("any"),
                  GenExp(Call(Attribute(Name("c"), "isalpha"), _ISALPHA_ARGS:Exprs),
                    CompFor(Name("c"), Name("s"), Bool(true)))),
                Call(Attribute(Name("s"), "swapcase"), _SWAPCASE_ARGS:Exprs),
                Subscript(
                  Name("s"),
                  Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))))
        => .K
      </k>
      <input> S:PString </input>
      <result> noResult => reverse(S) </result>
    </humanEval>
endmodule
