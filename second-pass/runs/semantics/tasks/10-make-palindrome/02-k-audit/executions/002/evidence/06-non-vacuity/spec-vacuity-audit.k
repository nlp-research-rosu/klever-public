requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  claim
    <k>
      #loop(rangeObj(I:Int, isLen(S:IntSeq), 1), Name("i"),
        If(Call(Name("is_palindrome"),
                Subscript(Name("string"), Slice(Name("i"), NoBound, NoBound))),
           Return(BinOp("+", Name("string"),
             Subscript(Subscript(Name("string"), Slice(NoBound, Name("i"), NoBound)),
                       Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))),
           .Stmts))
      ~> Return(Name("string")) ~> #endcall
      => str(seqConcat(palindromeFrom(S, I), iCons(88, .IntSeq)))
    </k>
    <env> L:Int => CALLER:Int </env>
    <scopes>
      (L |-> scope(("string" |-> str(S)) ("i" |-> J:Int), parent(0)))
      (0 |-> scope(
        ("is_palindrome" |-> closureVal(
          ("string", .ParamNames),
          Return(Compare(Name("string"),
            CmpOp("==", Subscript(Name("string"),
              Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))) .Stmts,
          0))
        ("make_palindrome" |-> makePalindromeClosure),
        parent(-1)))
      (-1 |-> builtinsScope)
      => ((L |-> scope(("string" |-> str(S)) ("i" |-> J), parent(0)))
          (0 |-> scope(
            ("is_palindrome" |-> closureVal(
              ("string", .ParamNames),
              Return(Compare(Name("string"),
                CmpOp("==", Subscript(Name("string"),
                  Slice(NoBound, NoBound, UnaryOp("-", Int(1))))))) .Stmts,
              0))
            ("make_palindrome" |-> makePalindromeClosure),
            parent(-1)))
          (-1 |-> builtinsScope)) [ L <- undef ]
    </scopes>
    <scopeLoc> L +Int 1 => L </scopeLoc>
    <stack> ListItem(frame(.K, CALLER, L)) REST:List => REST </stack>
    <ret> noRet </ret>
    <heap> H:Map </heap>
    <heapLoc> N:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I andBool I <=Int isLen(S)
     andBool L >Int 0

endmodule
