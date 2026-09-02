requires "verification.k"

module SPEC
  imports VERIFICATION

  // For every input string, executing the translated solution reaches exactly
  // the result required by the prompt.
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
      <result> noResult => expected(S) </result>
    </humanEval>
endmodule
