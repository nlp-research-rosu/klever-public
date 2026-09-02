requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Reviewer mutation: the actual answer is required to be one greater than
  // the submitted theorem's result.  N=4 is a satisfying witness: execution
  // returns 288, whereas this destination requires 289.
  claim [special-factorial-wrong-off-by-one]:
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
          Return(Name("result")))
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
        "answer" |-> specialFactorial(N) +Int 1,
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

  // Keep the genuine inductive support.  The mutation changes only the
  // result-constraining destination of the entry theorem.
  claim [special-factorial-loop-support]:
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
