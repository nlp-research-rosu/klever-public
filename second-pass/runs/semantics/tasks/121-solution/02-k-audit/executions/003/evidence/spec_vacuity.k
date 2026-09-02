requires "/tmp/audit-work/reconstruction/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Inductive loop invariant: starting with TOTAL and parity EVEN, consuming
  // VS adds exactly the contract value for that suffix.  The rest of the local
  // frame is existential on the right because the loop also updates its
  // iteration variable and parity flag; neither is observable after return.
  claim [loop-invariant]:
    <k>
      #loop(list(VS:ValSeq), Name("value"), solutionLoopBody)
      ~> KONT:K
      =>
      KONT
    </k>
    <env> L:Int </env>
    <scopes>
      BASE:Map
      L |-> scope(
        "lst" |-> LIST:Val
        "total" |-> TOTAL:Int
        "even_position" |-> EVEN:Bool
        "value" |-> OLD:Val,
        P:Parent)
      =>
      BASE
      L |-> scope(
        "lst" |-> LIST
        "total" |-> oddAtEvenAcc(VS, EVEN, TOTAL)
        "even_position" |-> ?FINAL_EVEN:Bool
        "value" |-> ?FINAL_VALUE:Val,
        P)
    </scopes>
    requires allInts(VS)

  claim [solution-correct]:
    <k>
      Call(solutionClosure, (list(VS:ValSeq), .Exprs))
      =>
      oddAtEvenPositions(VS, true) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
