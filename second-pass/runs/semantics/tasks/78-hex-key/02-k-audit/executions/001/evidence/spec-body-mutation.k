requires "verification-body-mutation.k"

module HEX-KEY-SPEC-BODY-MUTATION
  imports HEX-KEY-VERIFICATION-BODY-MUTATION

  // The candidate's original invariant; it must reject the increment-by-2 body.
  claim
    <k>
      #loop(str(CS:IntSeq), Name("digit"), hexKeyLoopBody)
      ~> CONT:K
      => CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope("count" |-> ACC
                   "digit" |-> DIGIT:Val
                   "num" |-> NUM:Val,
                   parent(0))) CALLERSCOPES:Map
      =>
      (L |-> scope("count" |-> (ACC +Int hexCount(CS))
                   "digit" |-> finalDigit(CS, DIGIT)
                   "num" |-> NUM,
                   parent(0))) CALLERSCOPES
    </scopes>
    <scopeLoc> _SCOPELOC:Int </scopeLoc>
    <heap> _HEAP:Map </heap>
    <heapLoc> _HEAPLOC:Int </heapLoc>
    <stack> _STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(body-sensitive-loop)]
endmodule
