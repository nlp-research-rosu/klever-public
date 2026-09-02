requires "verification.k"

module SPEC-VALUE-MUTATION-PRIME
  imports VERIFICATION

  // Candidate 3 has no divisor in [2,3), so forcing false must fail.
  claim [three-is-not-composite]:
    <k>
      #while(Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
             innerBody)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map, parent(-1))
       1 |-> scope(
              "candidate" |-> 3
              "divisor"   |-> (2 => 3)
              "n"         |-> 5
              "prime"     |-> (true => false)
              "primes"    |-> ref(0),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module SPEC-VALUE-MUTATION-COMPOSITE
  imports VERIFICATION

  // Candidate 4 is divisible by 2, so forcing true must fail.
  claim [four-is-not-prime]:
    <k>
      #while(Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
             innerBody)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(.Map, parent(-1))
       1 |-> scope(
              "candidate" |-> 4
              "divisor"   |-> (2 => 4)
              "n"         |-> 5
              "prime"     |-> (true => true)
              "primes"    |-> ref(0),
              parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
