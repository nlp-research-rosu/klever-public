requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: when the input contains ASCII letters, the submitted
  // body swaps their case instead of always reversing the input.
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
