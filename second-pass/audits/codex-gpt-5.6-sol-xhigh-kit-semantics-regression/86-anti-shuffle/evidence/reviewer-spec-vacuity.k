requires "spec.k"

module REVIEWER-SPEC-VACUITY
  imports SPEC

  // Reviewer-authored false result: prefix the actual result with ASCII '!'.
  // CS = .IntSeq satisfies the initial state and returns "", not "!".
  claim [reviewer-false-result]:
    <k>
      #loadAll(Module(FuncDef("anti_shuffle", Params("s"), antiFunctionBody())))
      ~> Call(Name("anti_shuffle"), str(CS:IntSeq))
      => str(iCons(33, antiShuffleCodes(CS)))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => (0 |-> scope(
            "anti_shuffle" |-> closureVal("s", antiFunctionBody(), 0),
            parent(-1))
          -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => antiFinalHeapMap(CS) </heap>
    <heapLoc> 0 => antiFinalHeapLoc(CS) </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
