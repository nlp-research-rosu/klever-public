requires "verification.k"

module AUDIT-FALSE-SPEC
  imports VERIFICATION

  // Fresh reviewer mutation. The real program returns 20 on five 2s:
  // 2^2 + 2 + 2 + 2^2 + 2^3 = 20. The postcondition below demands 19.
  claim [off-by-one-index-four]:
    <k> sumSquaresDef
         ~> Call(
              Name("sum_squares"),
              list(valsOf(
                intCons(2,
                  intCons(2,
                    intCons(2,
                      intCons(2,
                        intCons(2, .IntList))))))))
        => 19 </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope) => ?SC:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
