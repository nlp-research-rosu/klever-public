requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for the satisfiable witness INPUT = "a": the real result is "A".
  claim [wrong-result]:
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
