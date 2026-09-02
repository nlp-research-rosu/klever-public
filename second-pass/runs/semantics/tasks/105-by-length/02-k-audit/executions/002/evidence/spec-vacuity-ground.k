requires "verification.k"

module BY-LENGTH-SPEC-VACUITY-GROUND
  imports BY-LENGTH-VERIFICATION

  // Ground instance of the original precondition at IS = .IntSeq, with the
  // result changed from [] to ["Zero"]. This is false but fully executable.
  claim [empty-input-cannot-return-zero]:
    <k>
      #applyK(
        toCall(byLengthClosure),
        (list(intVals(.IntSeq)), .Vals))
      ~> #observeList
    =>
      list(vCons(str(strToCodes("Zero")), .ValSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
