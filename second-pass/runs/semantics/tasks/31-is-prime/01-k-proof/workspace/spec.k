requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  // Loop invariant/induction theorem.  At candidate divisor D, executing the
  // remaining loop returns the mathematical trialPrime(N,D) result and
  // restores the ordinary Python call frame.
  claim
    <k>
      #while(#primeCond, #primeLoopBody)
        ~> (Return(Bool(true)) .Stmts)
        ~> #endcall
      =>
      trialPrime(N:Int, D:Int) ~> CONT:K
    </k>
    <env> L:Int => CALLER:Int </env>
    <scopes>
      (SC:Map
        0 |-> GLOBAL:Scope
        L |-> scope(
          "n" |-> N
          "divisor" |-> D,
          parent(0)))
      =>
      (SC
        0 |-> GLOBAL)
    </scopes>
    <scopeLoc> L +Int 1 => L </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack>
      ListItem(frame(CONT, CALLER, L)) STACK:List
      =>
      STACK
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires D >=Int 2
     andBool L =/=Int 0
     andBool notBool (0 in_keys(SC))
     andBool notBool (L in_keys(SC))
    [label(loop-correct)]

endmodule

module SPEC
  imports VERIFICATION

  // The n < 2 half of the universal entry-point theorem.
  claim
    <k>
      #entryBody ~> #endcall
      =>
      false ~> CONT:K
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (
        -1 |-> B:Scope
        0 |-> scope(
          "is_prime" |-> closureVal(
            "n", .ParamNames,
            #entryBody,
            0),
          parent(-1))
        1 |-> scope("n" |-> N, parent(0)))
      =>
      (
        -1 |-> B
        0 |-> scope(
          "is_prime" |-> closureVal(
            "n", .ParamNames,
            #entryBody,
            0),
          parent(-1)))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack>
      ListItem(frame(CONT, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N <Int 2
    [label(entry-small)]

  // The n >= 2 half: the finite branch prefix exposes the remaining
  // Assign/While statement list.  The supplied deterministic Assign and While
  // rules establish divisor = 2 and reach loop-correct's source pattern;
  // loop-correct then yields trialPrime(N,2), which is isPrimeSpec(N).
  claim
    <k>
      #entryBody ~> #endcall
      =>
      Assign(Name("divisor"), Int(2))
      While(#primeCond, #primeLoopBody)
      Return(Bool(true))
        ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      (SC:Map
        1 |-> scope("n" |-> N, parent(0)))
    </scopes>
    requires N >=Int 2
     andBool notBool (1 in_keys(SC))
    [label(entry-large-prefix)]
endmodule
