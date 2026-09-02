requires "verification.k"

module BY-LENGTH-SPEC-VACUITY-AUDIT
  imports BY-LENGTH-VERIFICATION

  // Fresh false mutation: prepend "Zero" to every returned list. The original
  // precondition is unchanged. IS = .IntSeq is a satisfying witness: the real
  // result is [], whereas this destination requires ["Zero"].
  claim [false-leading-zero]:
    <k>
      #applyK(
        toCall(byLengthClosure),
        (list(intVals(IS:IntSeq)), .Vals))
      ~> #observeList
    =>
      list(
        vCons(
          str(strToCodes("Zero")),
          tableNames(
            revVS(
              sortVS(
                filterDigits(
                  intVals(IS)))))))
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
