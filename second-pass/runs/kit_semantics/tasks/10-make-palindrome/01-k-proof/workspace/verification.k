requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports BOOL-SYNTAX

  syntax Stmts ::= "isPalindromeBody" [macro]
                 | "makePalindromeBody" [macro]
                 | "reverseLoopBody" [macro]
                 | "searchLoopBody" [macro]
  syntax Val ::= "isPalindromeClosure" [macro]
               | "makePalindromeClosure" [macro]
  syntax Module ::= "solutionModule" [macro]

  syntax IntSeq ::= reverseAcc(IntSeq, IntSeq) [function, total]
                   | seedResult(IntSeq) [function, total]
                   | searchResult(
                       IntSeq, IntSeq, IntSeq, IntSeq,
                       IntSeq, Bool, IntSeq) [function, total]
                   | completePal(IntSeq) [function, total]
  syntax Bool ::= palIS(IntSeq) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX
  imports MPY
  imports K-EQUAL

  rule isPalindromeBody
    => Expr(Str("Test if given string is a palindrome."))
       Return(
         Compare(
           Name("string"),
           CmpOp(
             "==",
             Subscript(
               Name("string"),
               Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))))

  rule reverseLoopBody
    => Assign(
         Name("reverse_string"),
         BinOp("+", Name("char"), Name("reverse_string")))

  rule searchLoopBody
    => If(
         UnaryOp("not", Name("found")),
         Assign(
           Name("prefix"),
           BinOp("+", Name("prefix"), Name("char")))
         Assign(
           Name("reverse_prefix"),
           BinOp("+", Name("char"), Name("reverse_prefix")))
         If(
           Compare(
             BinOp("+", Name("string"), Name("reverse_prefix")),
             CmpOp(
               "==",
               BinOp("+", Name("prefix"), Name("reverse_string")))),
           Assign(
             Name("result"),
             BinOp("+", Name("string"), Name("reverse_prefix")))
           Assign(Name("found"), Bool(true)),
           .Stmts),
         .Stmts)

  rule makePalindromeBody
    => Expr(Str("Return the shortest palindrome that begins with string."))
       Assign(Name("reverse_string"), Str(""))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("string"), reverseLoopBody)
       Assign(Name("prefix"), Str(""))
       Assign(Name("reverse_prefix"), Str(""))
       Assign(
         Name("found"),
         Compare(Name("string"), CmpOp("==", Name("reverse_string"))))
       Assign(
         Name("result"),
         IfExp(
           Name("found"),
           Name("string"),
           BinOp("+", Name("string"), Name("reverse_string"))))
       For(Name("char"), Name("string"), searchLoopBody)
       Return(Name("result"))

  rule isPalindromeClosure
    => closureVal(
         ("string", .ParamNames),
         isPalindromeBody,
         0)

  rule makePalindromeClosure
    => closureVal(
         ("string", .ParamNames),
         makePalindromeBody,
         0)

  rule solutionModule
    => Module(
         FuncDef(
           "is_palindrome",
           Params("string", .ParamNames),
           isPalindromeBody)
         FuncDef(
           "make_palindrome",
           Params("string", .ParamNames),
           makePalindromeBody))

  rule reverseAcc(.IntSeq, A:IntSeq) => A
  rule reverseAcc(iCons(C:Int, R:IntSeq), A:IntSeq)
    => reverseAcc(R, iCons(C, A))

  rule palIS(S:IntSeq)
    => S ==K reverseAcc(S, .IntSeq)

  rule seedResult(S:IntSeq) => S
    requires palIS(S)
  rule seedResult(S:IntSeq)
    => seqConcat(S, reverseAcc(S, .IntSeq))
    requires notBool palIS(S)

  rule searchResult(
         _:IntSeq, _:IntSeq, _:IntSeq, _:IntSeq,
         _:IntSeq, true, RESULT:IntSeq)
    => RESULT
  rule searchResult(
         _:IntSeq, .IntSeq, _:IntSeq, _:IntSeq,
         _:IntSeq, _:Bool, RESULT:IntSeq)
    => RESULT
  rule searchResult(
         S:IntSeq, iCons(C:Int, R:IntSeq), P:IntSeq, RP:IntSeq,
         REV:IntSeq, false, RESULT:IntSeq)
    => #if
         seqConcat(seqConcat(P, iCons(C, .IntSeq)), REV)
         ==K
         seqConcat(S, iCons(C, RP))
       #then
         seqConcat(S, iCons(C, RP))
       #else
         searchResult(
           S,
           R,
           seqConcat(P, iCons(C, .IntSeq)),
           iCons(C, RP),
           REV,
           false,
           RESULT)
       #fi

  rule completePal(S:IntSeq)
    => searchResult(
         S,
         S,
         .IntSeq,
         .IntSeq,
         reverseAcc(S, .IntSeq),
         palIS(S),
         seedResult(S))
endmodule
