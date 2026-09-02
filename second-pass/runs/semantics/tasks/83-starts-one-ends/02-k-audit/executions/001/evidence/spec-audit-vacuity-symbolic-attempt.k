requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Deliberately false at the satisfiable witness N = 2:
  // the program returns 18, while this destination requires 19.
  claim
    <k>
      #invokeStartsOneEnds(N:Int)
      => 19 *Int (10 ^Int (N -Int 2))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "starts_one_ends" |->
          closureVal(("n", .ParamNames), startsOneEndsBody, 0),
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
    requires N >=Int 2
endmodule
