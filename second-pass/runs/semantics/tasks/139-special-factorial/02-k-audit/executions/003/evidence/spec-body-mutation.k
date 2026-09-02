requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Reviewer mutation: execute the real loop but return factorial rather than
  // result. The unchanged postcondition is false, e.g. N=3 gives 6, not 12.
  claim [special-factorial-correct-body-mutated]:
    <k>
      #loadAll(Module(
        FuncDef("special_factorial", Params("n"),
          Assign(Name("factorial"), Int(1))
          Assign(Name("result"), Int(1))
          Assign(Name("i"), Int(1))
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            AugAssign(Name("factorial"), "*", Name("i"))
            AugAssign(Name("result"), "*", Name("factorial"))
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("factorial")))
        Assign(
          Name("answer"),
          Call(Name("special_factorial"), Int(N:Int)))
      ))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
        ?REST:Map
        "answer" |-> specialFactorial(N),
        parent(-1)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 0

  claim [special-factorial-loop]:
    <k>
      #while(
        Compare(Name("i"), CmpOp("<=", Name("n"))),
        AugAssign(Name("factorial"), "*", Name("i"))
        AugAssign(Name("result"), "*", Name("factorial"))
        AugAssign(Name("i"), "+", Int(1))
      ) ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "n"         |-> N:Int
        "factorial" |-> factorial(I:Int -Int 1)
        "result"    |-> specialFactorial(I -Int 1)
        "i"         |-> I,
        parent(0)
      )
      =>
      SC
      L |-> scope(
        "n"         |-> N
        "factorial" |-> factorial(N)
        "result"    |-> specialFactorial(N)
        "i"         |-> N +Int 1,
        parent(0)
      )
    </scopes>
    requires N >=Int 1
     andBool I >=Int 1
     andBool I <=Int N +Int 1
endmodule
