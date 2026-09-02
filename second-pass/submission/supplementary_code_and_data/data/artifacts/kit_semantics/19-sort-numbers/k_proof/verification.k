requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact values installed by loading solution.mpy.
  syntax Val ::= "numberKeyClosure" [macro]
  rule numberKeyClosure
    => closureVal(
         ("number", .ParamNames),
         (Return(
            Call(
              Attribute(
                TupleExpr(
                  Str("zero"),
                  Str("one"),
                  Str("two"),
                  Str("three"),
                  Str("four"),
                  Str("five"),
                  Str("six"),
                  Str("seven"),
                  Str("eight"),
                  Str("nine")),
                "index"),
              Name("number"))) .Stmts),
         0)

  syntax Val ::= "sortNumbersClosure" [macro]
  rule sortNumbersClosure
    => closureVal(
         ("numbers", .ParamNames),
         (Return(
            Call(
              Attribute(Str(" "), "join"),
              Call(
                Name("sorted"),
                Call(Attribute(Name("numbers"), "split"), .Exprs),
                KwArg("key", Name("_number_key"))))) .Stmts),
         0)

  // The source contract's input predicate: every token produced by Python's
  // whitespace split is one of the ten allowed numeral words.
  syntax Bool ::= isNumberWord(Val) [function, total]
  rule isNumberWord(V)
    => V ==K str(strToCodes("zero"))
       orBool V ==K str(strToCodes("one"))
       orBool V ==K str(strToCodes("two"))
       orBool V ==K str(strToCodes("three"))
       orBool V ==K str(strToCodes("four"))
       orBool V ==K str(strToCodes("five"))
       orBool V ==K str(strToCodes("six"))
       orBool V ==K str(strToCodes("seven"))
       orBool V ==K str(strToCodes("eight"))
       orBool V ==K str(strToCodes("nine"))

  syntax Bool ::= allNumberWords(ValSeq) [function, total]
  rule allNumberWords(.ValSeq) => true
  rule allNumberWords(vCons(V:Val, REST:ValSeq))
    => isNumberWord(V) andBool allNumberWords(REST)

  // Exact symbolic result under MPY's named sortKeyVS primitive.
  syntax Str ::= expectedSortNumbers(IntSeq) [function, total]
  rule expectedSortNumbers(CS)
    => str(
         joinCodes(
           strToCodes(" "),
           sortKeyVS(
             splitWS(CS, .IntSeq, .ValSeq),
             numberKeyClosure)))
endmodule
