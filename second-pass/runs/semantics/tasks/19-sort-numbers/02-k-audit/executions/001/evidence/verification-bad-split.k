requires "reference-semantics/semantics.k"

module SORT-NUMBERS-VERIFICATION
  imports MPY

  // The exact statement bodies emitted in solution.mpy.  Naming them keeps
  // the proof claims readable without changing the translated program.
  syntax Stmts ::= "numberBody" [macro]
  rule numberBody =>
       If(Compare(Name("word"), CmpOp("==", Str("zero"))),
          Return(Int(0)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("one"))),
          Return(Int(1)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("two"))),
          Return(Int(2)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("three"))),
          Return(Int(3)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("four"))),
          Return(Int(4)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("five"))),
          Return(Int(5)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("six"))),
          Return(Int(6)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("seven"))),
          Return(Int(7)), .Stmts)
       If(Compare(Name("word"), CmpOp("==", Str("eight"))),
          Return(Int(8)), .Stmts)
       Return(Int(9))

  syntax Stmts ::= "sortBody" [macro]
  rule sortBody =>
       Return(
         Call(
           Attribute(Str(" "), "join"),
           Call(
             Name("sorted"),
             Call(Attribute(Name("numbers"), "split"), .Exprs),
             KwArg("key", Name("number_value")))))

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule =>
       Module(
         FuncDef("number_value", Params("word"), numberBody)
         FuncDef("sort_numbers", Params("numbers"), sortBody))

  // These are the actual module-level closures produced by loading the two
  // translated definitions.
  syntax Val ::= "numberKey" [macro]
  rule numberKey => closureVal("word", numberBody, 0)

  // An arbitrary valid input is represented by a sequence whose element sort
  // admits only the ten numeral words.
  syntax NumWord ::= "zeroW" | "oneW" | "twoW" | "threeW" | "fourW"
                   | "fiveW" | "sixW" | "sevenW" | "eightW" | "nineW"
  syntax NumWords ::= ".NumWords" | nw(NumWord, NumWords)

  syntax Val ::= wordVal(NumWord) [function, total]
  rule wordVal(zeroW)  => str(strToCodes("zero"))
  rule wordVal(oneW)   => str(strToCodes("one"))
  rule wordVal(twoW)   => str(strToCodes("two"))
  rule wordVal(threeW) => str(strToCodes("three"))
  rule wordVal(fourW)  => str(strToCodes("four"))
  rule wordVal(fiveW)  => str(strToCodes("five"))
  rule wordVal(sixW)   => str(strToCodes("six"))
  rule wordVal(sevenW) => str(strToCodes("seven"))
  rule wordVal(eightW) => str(strToCodes("eight"))
  rule wordVal(nineW)  => str(strToCodes("nine"))

  syntax ValSeq ::= wordsVS(NumWords) [function, total]
  rule wordsVS(.NumWords)    => .ValSeq
  rule wordsVS(nw(W, WORDS)) => vCons(wordVal(W), wordsVS(WORDS))

  syntax IntSeq ::= wordCodes(NumWord) [function, total]
  rule wordCodes(zeroW)  => strToCodes("zero")
  rule wordCodes(oneW)   => strToCodes("one")
  rule wordCodes(twoW)   => strToCodes("two")
  rule wordCodes(threeW) => strToCodes("three")
  rule wordCodes(fourW)  => strToCodes("four")
  rule wordCodes(fiveW)  => strToCodes("five")
  rule wordCodes(sixW)   => strToCodes("six")
  rule wordCodes(sevenW) => strToCodes("seven")
  rule wordCodes(eightW) => strToCodes("eight")
  rule wordCodes(nineW)  => strToCodes("nine")

  // The equations give encodedWords its concrete meaning. It remains an
  // ordinary constructor on an abstract WORDS variable, which is the
  // documented problem-local abstraction boundary for symbolic split.
  syntax IntSeq ::= encodedWords(NumWords)
  rule encodedWords(.NumWords) => .IntSeq
  rule encodedWords(nw(W, .NumWords)) => wordCodes(W)
  rule encodedWords(nw(W, nw(W2, WORDS)))
    => seqConcat(wordCodes(W),
                 iCons(32, encodedWords(nw(W2, WORDS))))

  rule <k> #applyK(
             toCall(boundMethodV(str(encodedWords(WORDS)), "split")),
             .Vals)
        => #alloc(list(.ValSeq)) ... </k>
       [priority(30)]

  // MPY-SORT specifies keyed sorting symbolically with the trusted primitive
  // sortKeyVS.  Joining that sequence is precisely the contract result.
  syntax Val ::= numericOutput(NumWords) [function, total]
  rule numericOutput(WORDS)
    => str(joinCodes(iCons(32, .IntSeq),
                     sortKeyVS(wordsVS(WORDS), numberKey)))
endmodule
