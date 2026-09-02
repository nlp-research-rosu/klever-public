requires "verification-body-mutation.k"

module SUM-TO-N-BODY-MUTATION-SPEC
  imports SUM-TO-N-BODY-MUTATION

  claim
    <k> #runSumToNBodyMut(N) => triangularBodyMut(N) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "sum_to_n"
               |-> closureVal(
                     "n",
                     Return(
                       BinOp(
                         "//",
                         BinOp("*", Name("n"), BinOp("+", Name("n"), Int(2))),
                         Int(2)))
                     .Stmts,
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
    requires N >=Int 0
endmodule
