requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
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
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |-> scope(
        "string"  |-> S:Str
        "n"       |-> N:Int
        "divisor" |-> (D:Int => ?D:Int)
        "prime"   |-> (P:Bool => trialPrime(N, D, P)),
        parent(0))
      ...
    </scopes>
    requires N >=Int 0 andBool D >=Int 2

  claim [prime-length]:
    <k>
      Call(Name("prime_length"), str(CS:IntSeq))
      => primeNat(isLen(CS))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
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
    requires isLen(CS) >=Int 0
endmodule
