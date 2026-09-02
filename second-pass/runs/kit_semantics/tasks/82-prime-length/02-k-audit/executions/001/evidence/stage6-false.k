requires "verification.k"

module STAGE6-FALSE
  imports VERIFICATION

  // Fresh reviewer mutation: length 5 is prime and the real body returns true.
  // The deliberately false destination must be rejected.
  claim [length-five-not-prime]:
    <k>
      Call(
        Name("prime_length"),
        str(iCons(97, iCons(98, iCons(99, iCons(100, iCons(101, .IntSeq)))))))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "prime_length" |->
          closureVal(
            ("string", .ParamNames),
            (Expr(Str("Return whether the length of string is a prime number."))
             Assign(Name("n"), Call(Name("len"), Name("string")))
             Assign(Name("divisor"), Int(2))
             Assign(
               Name("prime"),
               Compare(Name("n"), CmpOp(">=", Int(2))))
             While(
               Compare(Name("divisor"), CmpOp("<", Name("n"))),
               If(
                 Compare(
                   BinOp("%", Name("n"), Name("divisor")),
                   CmpOp("==", Int(0))),
                 Assign(Name("prime"), Bool(false)),
                 .Stmts)
               Assign(
                 Name("divisor"),
                 BinOp("+", Name("divisor"), Int(1))))
             Return(Name("prime"))
             .Stmts),
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
