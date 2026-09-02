requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inner-loop invariant.  B records whether all already-visited divisors
  // preserved primality; the loop checks the remaining interval [D, C).
  claim [inner-loop]:
    <k>
      #while(Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
             innerBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(M0:Map, parent(-1))
       1 |-> scope(
              "candidate" |-> C:Int
              "divisor"   |-> (D:Int => C)
              "n"         |-> N:Int
              "prime"     |-> (B:Bool => ?PB:Bool)
              "primes"    |-> ref(H:Int),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> H |-> list(P:ValSeq) </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires C >=Int 2 andBool D >=Int 2 andBool D <=Int C
    ensures  ?PB ==Bool (B andBool noDivisors(C, D))

  // Outer-loop invariant.  P is the already accumulated prefix; each
  // candidate contributes exactly when the inner invariant returns true.
  claim [outer-loop]:
    <k>
      #while(Compare(Name("candidate"), CmpOp("<", Name("n"))),
             outerBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(M0:Map, parent(-1))
       1 |-> scope(
              "candidate" |-> (C:Int => N:Int)
              "divisor"   |-> (D:Int => N -Int 1)
              "n"         |-> N
              "prime"     |-> (B:Bool => ?PF:Bool)
              "primes"    |-> ref(H:Int),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      H |-> list(P:ValSeq => valSeqConcat(P, primesBetween(C, N)))
    </heap>
    <heapLoc> HL:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires C >=Int 2 andBool C <Int N

  // Whole entry-point claim.  It executes the exact function definition and
  // binding, then invokes count_up_to from a fresh module configuration.
  claim [count-up-to]:
    <k>
      FuncDef("count_up_to", Params("n"), countBody)
      ~> Call(Name("count_up_to"), (N:Int, .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map => "count_up_to" |->
                    closureVal(("n", .ParamNames), countBody, 0),
                    parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(primesBelow(N)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
endmodule
