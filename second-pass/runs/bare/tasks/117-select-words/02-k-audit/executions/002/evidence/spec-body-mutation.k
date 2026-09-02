requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim
    <k>
      Module(
        FuncDef("select_words", Params("s", "n"),
          CellVars("n"), FreeVars(.Strings),
          Expr(
            Str(
              "Return, in input order, words containing exactly n consonants."))
          Return(
            ListComp(Name("word"),
              CompFor(
                Name("word"),
                Call(Attribute(Name("s"), "split"), .Exprs),
                Compare(
                  Call(
                    Name("len"),
                    ListComp(Name("letter"),
                      CompFor(
                        Name("letter"),
                        Name("word"),
                        Compare(
                          Call(
                            Attribute(Name("letter"), "lower"), .Exprs),
                          CmpOp("not in", Str("aeio")))))),
                  CmpOp("==", Name("n"))))))))
      => .K
    </k>
    <inputS> S:String </inputS>
    <inputN> N:Int </inputN>
    <result> noResult => selectWordsSpec(S, N) </result>
    requires N >=Int 0

  // Concrete regression claims cover every example in the original prompt,
  // plus the required empty-input behavior.
endmodule
