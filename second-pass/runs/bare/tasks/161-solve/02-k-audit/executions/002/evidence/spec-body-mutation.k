requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Material body mutation: the generator filter is false. For input "a",
  // real Python takes the reverse branch and returns "a", not expected("a")="A".
  // The candidate semantics ignores _IFS, so this false source theorem closes.
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
                    CompFor(Name("c"), Name("s"), Bool(false)))),
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
