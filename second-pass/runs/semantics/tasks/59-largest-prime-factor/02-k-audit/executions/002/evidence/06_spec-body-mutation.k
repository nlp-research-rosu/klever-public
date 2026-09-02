requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  // Loop invariant/circularity: from any positive trial state, the operational
  // while loop returns exactly the value of the mathematical recurrence.
  claim [lpf-loop]:
    <k>
      #while(lpfCondition, lpfStep)
      ~> (Return(Name("factor")) .Stmts)
      ~> #endcall
      => lpfSpec(N, F) ~> CONT
    </k>
    <env> L => CALLER </env>
    <scopes>
      SC (L |-> scope(("n" |-> N) ("factor" |-> F), parent(0)))
      => SC
    </scopes>
    <scopeLoc> L +Int 1 => L </scopeLoc>
    <stack>
      ListItem(frame(CONT, CALLER, L)) REST
      => REST
    </stack>
    <ret> noRet </ret>
    requires N >Int 1
     andBool F >Int 1
     andBool L >=Int 1
     andBool notBool (L in_keys(SC))
    [circularity]

  // Symbolic execution of the finite administrative prefix: loading the exact
  // generated module, resolving the function, binding n, initializing factor,
  // and reaching precisely the loop state covered by lpf-loop.
  claim [largest-prime-factor-entry]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("largest_prime_factor"), Int(N))
      =>
      #while(lpfCondition, lpfStep)
      ~> (Return(Name("factor")) .Stmts)
      ~> #endcall
    </k>
    <env> 0 => 1 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(
        "largest_prime_factor" |->
          closureVal(
            ("n", .ParamNames),
            Assign(Name("factor"), Int(2))
            While(lpfCondition, lpfStep)
            Return(Name("factor")),
            0),
        parent(-1)))
      (-1 |-> builtinsScope)
      (1 |-> scope(
        ("n" |-> N) ("factor" |-> 2),
        parent(0)))
    </scopes>
    <scopeLoc> 1 => 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      .List
      => ListItem(frame(.K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 1

endmodule
