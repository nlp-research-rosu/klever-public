requires "verification-with-lemma.k"

module SPEC-VACUITY
  imports VERIFICATION-WITH-LEMMA

  // Deliberately false: the even count is constrained to be one too large.
  claim [false-postcondition]:
    <k> Call(Name("even_odd_count"), N:Int)
        => tuple(vCons(?ER:Int, vCons(?OR:Int, .ValSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("even_odd_count" |-> evenOddClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?ER ==Int decEven(N) +Int 1
     andBool ?OR ==Int decOdd(N)
endmodule
