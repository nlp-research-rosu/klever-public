requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the real program returns N*N, not N*N+1.
  // The satisfying witness N=3 reaches 9 while this destination requires 10.
  claim
    <k> #runCarRaceCollision(N:Int) => (N *Int N) +Int 1 </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
              "car_race_collision"
                |-> closureVal(
                      "n",
                      Return(BinOp("*", Name("n"), Name("n"))),
                      0),
              parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
