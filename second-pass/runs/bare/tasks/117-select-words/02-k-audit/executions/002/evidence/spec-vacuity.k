requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim
    <k> Module(
      FuncDef("select_words", Params("s", "n"), CellVars("n"), FreeVars(.Strings),
        Expr(Str("Return, in input order, words containing exactly n consonants."))
        Return(ListComp(Name("word"),
          CompFor(Name("word"), Call(Attribute(Name("s"), "split"), .Exprs),
            Compare(Call(Name("len"), ListComp(Name("letter"),
              CompFor(Name("letter"), Name("word"),
                Compare(Call(Attribute(Name("letter"), "lower"), .Exprs),
                  CmpOp("not in", Str("aeiou")))))),
              CmpOp("==", Name("n")))))))) => .K </k>
    <inputS> "b" </inputS>
    <inputN> 1 </inputN>
    <result> noResult => pyList(.Words) </result>

endmodule
