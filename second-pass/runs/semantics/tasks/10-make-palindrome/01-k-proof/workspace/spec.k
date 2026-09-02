requires "verification.k"

module SPEC
  imports VERIFICATION

  // The helper body computes precisely palindromeIS.  This independently
  // validates the helper summary used in the main loop proof.
  claim
    <k>
      Return(Compare(Name("string"),
        CmpOp("==", Subscript(Name("string"),
          Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))))
      ~> #endcall
      => palindromeIS(S:IntSeq)
    </k>
    <env> L0:Int => CALLER0:Int </env>
    <scopes>
      (L0 |-> scope("string" |-> str(S), parent(0))) REST0:Map
      => REST0
    </scopes>
    <scopeLoc> L0 +Int 1 => L0 </scopeLoc>
    <stack> ListItem(frame(.K, CALLER0, L0)) STACK0:List => STACK0 </stack>
    <ret> noRet </ret>
    <heap> HH:Map </heap>
    <heapLoc> NN:Int </heapLoc>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires L0 >Int 0 andBool notBool (L0 in_keys(REST0))

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
      => str(palindromeFrom(S, I))
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
