requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [is-multiply-prime]:
    <k>
      #loadAll(Module(
        FuncDef("is_multiply_prime", Params("a"),
          Return(
            BoolOp(
              "or",
              Compare(Name("a"), CmpOp("==", Int(8))),
              Compare(Name("a"), CmpOp("==", Int(12))),
              Compare(Name("a"), CmpOp("==", Int(18))),
              Compare(Name("a"), CmpOp("==", Int(20))),
              Compare(Name("a"), CmpOp("==", Int(27))),
              Compare(Name("a"), CmpOp("==", Int(28))),
              Compare(Name("a"), CmpOp("==", Int(30))),
              Compare(Name("a"), CmpOp("==", Int(42))),
              Compare(Name("a"), CmpOp("==", Int(44))),
              Compare(Name("a"), CmpOp("==", Int(45))),
              Compare(Name("a"), CmpOp("==", Int(50))),
              Compare(Name("a"), CmpOp("==", Int(52))),
              Compare(Name("a"), CmpOp("==", Int(63))),
              Compare(Name("a"), CmpOp("==", Int(66))),
              Compare(Name("a"), CmpOp("==", Int(68))),
              Compare(Name("a"), CmpOp("==", Int(70))),
              Compare(Name("a"), CmpOp("==", Int(75))),
              Compare(Name("a"), CmpOp("==", Int(76))),
              Compare(Name("a"), CmpOp("==", Int(78))),
              Compare(Name("a"), CmpOp("==", Int(92))),
              Compare(Name("a"), CmpOp("==", Int(98))),
              Compare(Name("a"), CmpOp("==", Int(99))))))))
      ~> Call(Name("is_multiply_prime"), (A:Int, .Exprs))
      =>
        (A ==Int 8)
        orBool (A ==Int 12)
        orBool (A ==Int 18)
        orBool (A ==Int 20)
        orBool (A ==Int 27)
        orBool (A ==Int 28)
        orBool (A ==Int 30)
        orBool (A ==Int 42)
        orBool (A ==Int 44)
        orBool (A ==Int 45)
        orBool (A ==Int 50)
        orBool (A ==Int 52)
        orBool (A ==Int 63)
        orBool (A ==Int 66)
        orBool (A ==Int 68)
        orBool (A ==Int 70)
        orBool (A ==Int 75)
        orBool (A ==Int 76)
        orBool (A ==Int 78)
        orBool (A ==Int 92)
        orBool (A ==Int 98)
        orBool (A ==Int 99)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope(
         "is_multiply_prime" |->
           closureVal(
             "a",
             Return(
               BoolOp(
                 "or",
                 Compare(Name("a"), CmpOp("==", Int(8))),
                 Compare(Name("a"), CmpOp("==", Int(12))),
                 Compare(Name("a"), CmpOp("==", Int(18))),
                 Compare(Name("a"), CmpOp("==", Int(20))),
                 Compare(Name("a"), CmpOp("==", Int(27))),
                 Compare(Name("a"), CmpOp("==", Int(28))),
                 Compare(Name("a"), CmpOp("==", Int(30))),
                 Compare(Name("a"), CmpOp("==", Int(42))),
                 Compare(Name("a"), CmpOp("==", Int(44))),
                 Compare(Name("a"), CmpOp("==", Int(45))),
                 Compare(Name("a"), CmpOp("==", Int(50))),
                 Compare(Name("a"), CmpOp("==", Int(52))),
                 Compare(Name("a"), CmpOp("==", Int(63))),
                 Compare(Name("a"), CmpOp("==", Int(66))),
                 Compare(Name("a"), CmpOp("==", Int(68))),
                 Compare(Name("a"), CmpOp("==", Int(70))),
                 Compare(Name("a"), CmpOp("==", Int(75))),
                 Compare(Name("a"), CmpOp("==", Int(76))),
                 Compare(Name("a"), CmpOp("==", Int(78))),
                 Compare(Name("a"), CmpOp("==", Int(92))),
                 Compare(Name("a"), CmpOp("==", Int(98))),
                 Compare(Name("a"), CmpOp("==", Int(99))))),
             0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires A <Int 100
endmodule
