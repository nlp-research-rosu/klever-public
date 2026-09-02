requires "verification.k"

module LOOP-BODY-MUTATION-SPEC
  imports VERIFICATION

  claim [mutated-loop-must-not-prove]:
    <k>
      #while(
        Compare(Name("i"), CmpOp(">", Int(0))),
        While(
          BoolOp("and",
            ( UnaryOp("not", Name("found")),
              Call(
                Name("_is_vowel"),
                Subscript(Name("word"), Name("i"))),
              UnaryOp(
                "not",
                Call(
                  Name("_is_vowel"),
                  Subscript(
                    Name("word"),
                    BinOp("-", Name("i"), Int(1))))),
              UnaryOp(
                "not",
                Call(
                  Name("_is_vowel"),
                  Subscript(
                    Name("word"),
                    BinOp("+", Name("i"), Int(1))))),
              .Exprs)),
          Assign(Name("result"), Subscript(Name("word"), Name("i")))
          Assign(Name("found"), Bool(true)))
        Assign(Name("i"), BinOp("-", Name("i"), Int(2))))
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => str(strToCodes("a"))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( 0 |-> scope(
          ( "_is_vowel" |-> closureVal(
              ("ch", .ParamNames),
              isVowelBody,
              0)
            "get_closest_vowel" |-> closureVal(
              ("word", .ParamNames),
              getClosestBody,
              0) ),
          parent(-1))
        1 |-> scope(
          ( "word"   |-> str(strToCodes("bbabc"))
            "result" |-> str(.IntSeq)
            "found"  |-> false
            "i"      |-> 3 ),
          parent(0))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          ( "_is_vowel" |-> closureVal(
              ("ch", .ParamNames),
              isVowelBody,
              0)
            "get_closest_vowel" |-> closureVal(
              ("word", .ParamNames),
              getClosestBody,
              0) ),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
