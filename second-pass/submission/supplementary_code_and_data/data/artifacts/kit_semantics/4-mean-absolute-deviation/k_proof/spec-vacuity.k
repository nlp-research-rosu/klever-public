requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable input []: the real result is 0.0.
  claim [false-empty-result]:
    <k>
      FuncDef(
        "mean_absolute_deviation",
        Params("numbers"),
        madBody)
      ~> Call(
           Name("mean_absolute_deviation"),
           (list(.ValSeq), .Exprs))
      => 1.0
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
              .Map
              => "mean_absolute_deviation"
                 |-> closureVal(("numbers", .ParamNames), madBody, 0),
              parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
