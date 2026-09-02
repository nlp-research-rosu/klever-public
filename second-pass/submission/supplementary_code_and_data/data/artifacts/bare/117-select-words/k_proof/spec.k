requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal functional-correctness claim.  S remains an arbitrary string;
  // the prompt assumption is represented by the documented semantic domain,
  // while N's natural-number precondition is explicit.
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
                          CmpOp("not in", Str("aeiou")))))),
                  CmpOp("==", Name("n"))))))))
      => .K
    </k>
    <inputS> S:String </inputS>
    <inputN> N:Int </inputN>
    <result> noResult => selectWordsSpec(S, N) </result>
    requires N >=Int 0

  // Concrete regression claims cover every example in the original prompt,
  // plus the required empty-input behavior.
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
    <inputS> "Mary had a little lamb" </inputS>
    <inputN> 4 </inputN>
    <result> noResult => pyList(WCons("little", .Words)) </result>

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
    <inputS> "Mary had a little lamb" </inputS>
    <inputN> 3 </inputN>
    <result> noResult
          => pyList(WCons("Mary", WCons("lamb", .Words))) </result>

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
    <inputS> "simple white space" </inputS>
    <inputN> 2 </inputN>
    <result> noResult => pyList(.Words) </result>

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
    <inputS> "Hello world" </inputS>
    <inputN> 4 </inputN>
    <result> noResult => pyList(WCons("world", .Words)) </result>

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
    <inputS> "Uncle sam" </inputS>
    <inputN> 3 </inputN>
    <result> noResult => pyList(WCons("Uncle", .Words)) </result>

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
    <inputS> "" </inputS>
    <inputN> 0 </inputN>
    <result> noResult => pyList(.Words) </result>
endmodule
