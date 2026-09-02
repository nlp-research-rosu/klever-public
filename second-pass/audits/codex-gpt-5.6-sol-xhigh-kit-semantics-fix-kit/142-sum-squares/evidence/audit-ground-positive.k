requires "verification.k"

module AUDIT-GROUND-POSITIVE
  imports VERIFICATION

  // Concrete satisfying witness for the nonempty entry precondition.
  claim [five-twos]:
    <k> sumSquaresDef
         ~> Call(
              Name("sum_squares"),
              list(valsOf(
                intCons(2,
                  intCons(2,
                    intCons(2,
                      intCons(2,
                        intCons(2, .IntList))))))))
        => 20 </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
              .Map => "sum_squares" |-> closureVal("lst", sumSquaresBody, 0),
              parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
