requires "verification.k"

module DIGIT-SUM-ENTRY-VACUITY-SPEC
  imports DIGIT-SUM-VERIFICATION-WITH-LOOP-LEMMA

  // False for every input, including the satisfying witness S = .IntSeq.
  claim [entry-point-off-by-one]:
    <k>
      Call(
        closureVal(("s", .ParamNames), digitSumBody, 0),
        (str(S:IntSeq), .Exprs)
      )
      => digitSumSpec(S) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> digitSumBuiltins
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
