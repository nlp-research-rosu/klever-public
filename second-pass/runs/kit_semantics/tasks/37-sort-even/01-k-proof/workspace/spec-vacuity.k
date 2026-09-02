requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the realizable witness [5, 6, 3, 4]: it demands
  // that the result remain unsorted instead of becoming [3, 6, 5, 4].
  claim [false-result]:
    <k>
      #loadAll(Module(FuncDef("sort_even", Params("l"), sortEvenBody)))
      ~> Call(
           Name("sort_even"),
           list(vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ( 0 |-> list(vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq)))))
        1 |-> list(
          buildVS(
            vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq)))),
            0,
            4,
            2))
        2 |-> list(
          sortVS(
            buildVS(
              vCons(5, vCons(6, vCons(3, vCons(4, .ValSeq)))),
              0,
              4,
              2))) )
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
