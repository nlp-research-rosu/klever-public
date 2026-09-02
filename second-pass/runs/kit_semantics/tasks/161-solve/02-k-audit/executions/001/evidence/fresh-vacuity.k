requires "/tmp/audit-work/161-solve/scratch/verification.k"

module FRESH-VACUITY
  imports VERIFICATION

  // Satisfying input witness: runtime string "a" (code 97).
  // Deliberately false obligation: the real program returns "A" (code 65),
  // while this target requires the unchanged lowercase "a".
  claim [false-lowercase-result]:
    <k>
      #loadAll(Module(
        FuncDef("solve", Params("s"), solveBody)
        Assign(
          Name("answer"),
          Call(Name("solve"), str(iCons(97, .IntSeq))))
        .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0  |-> scope(
               "answer" |-> str(iCons(97, .IntSeq))
               "solve"  |-> ?SOLVE:Val,
               parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
